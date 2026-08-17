"""Deterministic projection of exact editorial authorities into story time."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from jsonschema import ValidationError

from . import (
    contracts,
    doctor,
    emit_fcpxml,
    organizer,
    process,
    string_out,
    sync_scan,
)

_SOURCE_FIELDS = frozenset(
    {"camera", "media_id", "path", "duration_seconds", "sha256"}
)
_JSON_LIMIT_BYTES = 16 * 1024 * 1024
_HASH_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class StorySource:
    """One exact local source available to the story projection."""

    camera: str
    media_id: str
    path: Path
    duration_frames: int
    sha256: str


@dataclass(frozen=True)
class StoryClip:
    """One source excerpt placed inside a story segment."""

    camera: str
    media_id: str
    path: Path
    offset_frames: int
    start_frames: int
    duration_frames: int
    audio_enabled: bool


@dataclass(frozen=True)
class StorySegment:
    """One selected cue range in final editor story order."""

    segment_id: str
    offset_frames: int
    duration_frames: int
    title_text: str
    clips: tuple[StoryClip, ...]


@dataclass(frozen=True)
class StoryTimeline:
    """A complete story projection expressed only in integer frames."""

    profile_id: str
    frame_numerator: int
    frame_denominator: int
    duration_frames: int
    sources: tuple[StorySource, ...]
    segments: tuple[StorySegment, ...]


@dataclass(frozen=True)
class _SourceRelationship:
    kind: str
    source_a: StorySource | None
    source_b: StorySource | None
    offset_b_from_a_frames: int
    audio_master: str


@dataclass(frozen=True)
class _LoadedArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str


def _validate_contract(name: str, payload: object, code: str) -> None:
    try:
        contracts.validate_contract(name, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def _seconds_from_ms(value: int) -> Decimal:
    return Decimal(value) / Decimal(1000)


def _normalize_working_cut(payload: Mapping[str, object]) -> dict[str, object]:
    segments = payload["segments"]
    assert isinstance(segments, list)
    return {
        **payload,
        "segments": sorted(segments, key=lambda item: item["storyOrder"]),
    }


def _normalize_sources(
    sync_map: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    profile: Mapping[str, object],
) -> tuple[tuple[StorySource, ...], string_out.StringOut]:
    stripped: list[dict[str, object]] = []
    hashes: dict[tuple[str, str], str] = {}
    media_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, Mapping) or set(source) != _SOURCE_FIELDS:
            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
        camera = source["camera"]
        media_id = source["media_id"]
        sha256 = source["sha256"]
        if (
            camera not in {"A", "B"}
            or not isinstance(media_id, str)
            or not media_id
            or media_id in media_ids
            or not isinstance(sha256, str)
            or len(sha256) != 64
            or any(character not in "0123456789abcdef" for character in sha256)
        ):
            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
        media_ids.add(media_id)
        hashes[(camera, media_id)] = sha256
        stripped.append(
            {
                "camera": camera,
                "media_id": media_id,
                "path": source["path"],
                "duration_seconds": source["duration_seconds"],
            }
        )

    try:
        base = string_out.build_string_out(sync_map, stripped, profile=profile)
    except (TypeError, ValueError, ValidationError) as error:
        raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID") from error
    normalized = tuple(
        StorySource(
            camera=source.camera,
            media_id=source.media_id,
            path=source.path,
            duration_frames=source.duration_frames,
            sha256=hashes[(source.camera, source.media_id)],
        )
        for source in base.sources
    )
    return normalized, base


def _build_relationships(
    sync_map: Mapping[str, object],
    source_by_media: Mapping[str, StorySource],
    *,
    frame_duration: Fraction,
) -> dict[str, _SourceRelationship]:
    relationships: dict[str, _SourceRelationship] = {}

    def register(media_id: str, relationship: _SourceRelationship) -> None:
        if media_id in relationships:
            raise ValueError("TRITRACK_STORY_SYNC_CONFLICT")
        relationships[media_id] = relationship

    pairs = sync_map["pairs"]
    assert isinstance(pairs, list)
    for pair in pairs:
        assert isinstance(pair, Mapping)
        media_a = str(pair["mediaA"])
        media_b = str(pair["mediaB"])
        source_a = source_by_media.get(media_a)
        source_b = source_by_media.get(media_b)
        if (
            source_a is None
            or source_b is None
            or source_a.camera != "A"
            or source_b.camera != "B"
        ):
            raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
        offset_frames = string_out.seconds_to_frames(
            pair["offsetBFromASeconds"], frame_duration
        )
        relationship = _SourceRelationship(
            kind="pair",
            source_a=source_a,
            source_b=source_b,
            offset_b_from_a_frames=offset_frames,
            audio_master=str(pair["audioMaster"]),
        )
        register(media_a, relationship)
        register(media_b, relationship)

    for camera, field in (("A", "singleA"), ("B", "singleB")):
        singles = sync_map[field]
        assert isinstance(singles, list)
        for value in singles:
            media_id = str(value)
            source = source_by_media.get(media_id)
            if source is None or source.camera != camera:
                raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
            register(
                media_id,
                _SourceRelationship(
                    kind="single",
                    source_a=source if camera == "A" else None,
                    source_b=source if camera == "B" else None,
                    offset_b_from_a_frames=0,
                    audio_master=camera,
                ),
            )
    return relationships


def _paired_clips(
    relationship: _SourceRelationship,
    selected: StorySource,
    *,
    selected_start: int,
    selected_end: int,
    story_offset: int,
) -> tuple[StoryClip, ...]:
    assert relationship.source_a is not None
    assert relationship.source_b is not None
    global_starts = {
        "A": 0,
        "B": relationship.offset_b_from_a_frames,
    }
    selected_global_start = selected_start + global_starts[selected.camera]
    selected_global_end = selected_end + global_starts[selected.camera]
    master = (
        relationship.source_a
        if relationship.audio_master == "A"
        else relationship.source_b
    )
    master_start = global_starts[master.camera]
    master_end = master_start + master.duration_frames
    if master_start > selected_global_start or master_end < selected_global_end:
        raise ValueError("TRITRACK_STORY_AUDIO_MASTER_COVERAGE")

    clips: list[StoryClip] = []
    for source in (relationship.source_a, relationship.source_b):
        source_global_start = global_starts[source.camera]
        source_global_end = source_global_start + source.duration_frames
        intersection_start = max(selected_global_start, source_global_start)
        intersection_end = min(selected_global_end, source_global_end)
        if intersection_end <= intersection_start:
            continue
        clips.append(
            StoryClip(
                camera=source.camera,
                media_id=source.media_id,
                path=source.path,
                offset_frames=story_offset
                + intersection_start
                - selected_global_start,
                start_frames=intersection_start - source_global_start,
                duration_frames=intersection_end - intersection_start,
                audio_enabled=source.camera == relationship.audio_master,
            )
        )
    return tuple(clips)


def build_story_timeline(
    sync_map: Mapping[str, object],
    aligned: Mapping[str, object],
    grouping: Mapping[str, object],
    working_cut: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    aligned_sha256: str,
    grouping_sha256: str,
    profile: Mapping[str, object],
) -> StoryTimeline:
    """Re-derive and project selected cue spans into deterministic story time."""

    _validate_contract("sync-map-v1", sync_map, "TRITRACK_STORY_SYNC_INVALID")
    _validate_contract(
        "aligned-transcript-v1", aligned, "TRITRACK_STORY_ALIGNED_INVALID"
    )
    _validate_contract("grouping-v1", grouping, "TRITRACK_STORY_GROUPING_INVALID")
    _validate_contract(
        "working-cut-v1", working_cut, "TRITRACK_STORY_WORKING_CUT_INVALID"
    )
    _validate_contract(
        "compatibility-profile-v1", profile, "TRITRACK_STORY_PROFILE_INVALID"
    )
    profile_id = str(profile["profileId"])
    if (
        dict(profile) != doctor.load_profile(profile_id)
        or sync_map["profileId"] != profile_id
    ):
        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")

    try:
        expected_working_cut = organizer.build_working_cut(
            aligned,
            grouping,
            aligned_sha256=aligned_sha256,
            grouping_sha256=grouping_sha256,
        )
    except (TypeError, ValueError, ValidationError) as error:
        raise ValueError("TRITRACK_STORY_AUTHORITY_INVALID") from error
    if _normalize_working_cut(working_cut) != expected_working_cut:
        raise ValueError("TRITRACK_STORY_WORKING_CUT_DRIFT")

    normalized_sources, base_timeline = _normalize_sources(
        sync_map, sources, profile=profile
    )
    source_by_media = {source.media_id: source for source in normalized_sources}
    frame_duration = Fraction(
        base_timeline.frame_numerator, base_timeline.frame_denominator
    )
    relationships = _build_relationships(
        sync_map,
        source_by_media,
        frame_duration=frame_duration,
    )

    takes = aligned["takes"]
    assert isinstance(takes, list)
    take_by_id = {str(take["takeId"]): take for take in takes}
    segments = expected_working_cut["segments"]
    assert isinstance(segments, list)
    story_segments: list[StorySegment] = []
    cursor = 0
    for segment in segments:
        assert isinstance(segment, Mapping)
        take_id = str(segment["takeId"])
        take = take_by_id.get(take_id)
        source = source_by_media.get(take_id)
        relationship = relationships.get(take_id)
        if take is None or source is None or relationship is None:
            raise ValueError("TRITRACK_STORY_TAKE_UNKNOWN")
        if take["sourceSha256"] != source.sha256:
            raise ValueError("TRITRACK_STORY_SOURCE_HASH_MISMATCH")

        cues = take["cues"]
        assert isinstance(cues, list)
        positions = {str(cue["cueId"]): index for index, cue in enumerate(cues)}
        start_position = positions.get(str(segment["startCueId"]))
        end_position = positions.get(str(segment["endCueId"]))
        if (
            start_position is None
            or end_position is None
            or start_position > end_position
        ):
            raise ValueError("TRITRACK_STORY_CUE_UNKNOWN")
        selected_cues = cues[start_position : end_position + 1]
        start_ms = int(selected_cues[0]["startMs"])
        end_ms = int(selected_cues[-1]["endMs"])
        start_frames = string_out.seconds_to_frames(
            _seconds_from_ms(start_ms), frame_duration
        )
        end_frames = string_out.seconds_to_frames(
            _seconds_from_ms(end_ms), frame_duration
        )
        if end_frames <= start_frames or end_frames > source.duration_frames:
            raise ValueError("TRITRACK_STORY_SELECTION_INVALID")
        duration_frames = end_frames - start_frames
        title_text = " ".join(str(cue["text"]) for cue in selected_cues)

        if relationship.kind == "single":
            clips = (
                StoryClip(
                    camera=source.camera,
                    media_id=source.media_id,
                    path=source.path,
                    offset_frames=cursor,
                    start_frames=start_frames,
                    duration_frames=duration_frames,
                    audio_enabled=True,
                ),
            )
        else:
            clips = _paired_clips(
                relationship,
                source,
                selected_start=start_frames,
                selected_end=end_frames,
                story_offset=cursor,
            )
        story_segments.append(
            StorySegment(
                segment_id=str(segment["id"]),
                offset_frames=cursor,
                duration_frames=duration_frames,
                title_text=title_text,
                clips=clips,
            )
        )
        cursor += duration_frames

    return StoryTimeline(
        profile_id=profile_id,
        frame_numerator=base_timeline.frame_numerator,
        frame_denominator=base_timeline.frame_denominator,
        duration_frames=cursor,
        sources=normalized_sources,
        segments=tuple(story_segments),
    )


def _frame_time(timeline: StoryTimeline, frames: int) -> str:
    if frames == 0:
        return "0s"
    return f"{frames * timeline.frame_numerator}/{timeline.frame_denominator}s"


def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
    parameters = binding["parameters"]
    if not isinstance(parameters, list):
        raise TypeError("TRITRACK_STORY_BINDING_INVALID")
    values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in parameters
        if isinstance(parameter, Mapping)
    }
    expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
    if set(values) != expected:
        raise ValueError("TRITRACK_STORY_BINDING_INVALID")
    return values


def _validate_timeline(timeline: StoryTimeline) -> None:
    if not isinstance(timeline, StoryTimeline) or timeline.duration_frames <= 0:
        raise TypeError("TRITRACK_STORY_TIMELINE_INVALID")
    source_keys = [(source.camera, source.media_id) for source in timeline.sources]
    if source_keys != sorted(source_keys) or len(source_keys) != len(set(source_keys)):
        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
    source_by_key = {
        (source.camera, source.media_id): source for source in timeline.sources
    }
    cursor = 0
    for segment in timeline.segments:
        if (
            segment.offset_frames != cursor
            or segment.duration_frames <= 0
            or not segment.title_text
            or not segment.clips
            or sum(clip.audio_enabled for clip in segment.clips) != 1
        ):
            raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
        for clip in segment.clips:
            source = source_by_key.get((clip.camera, clip.media_id))
            if (
                source is None
                or clip.path != source.path
                or clip.offset_frames < segment.offset_frames
                or clip.start_frames < 0
                or clip.duration_frames <= 0
                or clip.start_frames + clip.duration_frames > source.duration_frames
                or clip.offset_frames + clip.duration_frames
                > segment.offset_frames + segment.duration_frames
            ):
                raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
        cursor += segment.duration_frames
    if cursor != timeline.duration_frames:
        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")


def render_story_fcpxml(
    timeline: StoryTimeline,
    *,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
) -> str:
    """Render one deterministic Final Cut XML projection of a story timeline."""

    _validate_timeline(timeline)
    if not isinstance(metadata, emit_fcpxml.ProjectMetadata):
        raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    if timeline.profile_id != profile_id:
        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")
    styles = _style_values(binding)

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": emit_fcpxml.FORMAT_NAME,
            "frameDuration": str(profile["frameDuration"]),
            "width": str(profile["width"]),
            "height": str(profile["height"]),
            "colorSpace": str(profile["colorSpace"]),
        },
    )
    ET.SubElement(
        resources_element,
        "effect",
        {
            "id": "r2",
            "name": str(binding["effectName"]),
            "uid": str(binding["effectUid"]),
        },
    )
    source_ids: dict[tuple[str, str], str] = {}
    for index, source in enumerate(timeline.sources, start=3):
        resource_id = f"r{index}"
        source_ids[(source.camera, source.media_id)] = resource_id
        asset = ET.SubElement(
            resources_element,
            "asset",
            {
                "id": resource_id,
                "name": source.media_id,
                "start": "0s",
                "duration": _frame_time(timeline, source.duration_frames),
                "hasVideo": "1",
                "hasAudio": "1",
                "format": "r1",
                "audioSources": "1",
                "audioChannels": "2",
                "audioRate": f"{int(profile['audioRate']) // 1000}k",
            },
        )
        ET.SubElement(
            asset,
            "media-rep",
            {"kind": "original-media", "src": source.path.absolute().as_uri()},
        )

    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", {"name": metadata.event_name})
    project = ET.SubElement(event, "project", {"name": metadata.project_name})
    sequence = ET.SubElement(
        project,
        "sequence",
        {
            "format": "r1",
            "duration": _frame_time(timeline, timeline.duration_frames),
            "tcStart": "0s",
            "tcFormat": str(profile["timecodeFormat"]),
            "audioLayout": "stereo",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        },
    )
    spine = ET.SubElement(sequence, "spine")
    for index, segment in enumerate(timeline.segments, start=1):
        gap = ET.SubElement(
            spine,
            "gap",
            {
                "name": segment.segment_id,
                "offset": _frame_time(timeline, segment.offset_frames),
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        for lane, clip in enumerate(segment.clips, start=1):
            attributes = {
                "ref": source_ids[(clip.camera, clip.media_id)],
                "lane": str(lane),
                "offset": _frame_time(timeline, clip.offset_frames),
                "name": clip.media_id,
                "start": _frame_time(timeline, clip.start_frames),
                "duration": _frame_time(timeline, clip.duration_frames),
                "srcEnable": "all" if clip.audio_enabled else "video",
            }
            if clip.audio_enabled:
                attributes["audioRole"] = "dialogue"
            ET.SubElement(gap, "asset-clip", attributes)
        title = ET.SubElement(
            gap,
            "title",
            {
                "ref": "r2",
                "lane": str(len(segment.clips) + 1),
                "offset": _frame_time(timeline, segment.offset_frames),
                "name": f"{segment.segment_id} - Basic Title",
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        text_element = ET.SubElement(title, "text")
        style_id = f"ts{index:03d}"
        text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
        text_style.text = segment.title_text
        definition = ET.SubElement(title, "text-style-def", {"id": style_id})
        ET.SubElement(
            definition,
            "text-style",
            {
                name: styles[name]
                for name in (
                    "alignment",
                    "font",
                    "fontColor",
                    "fontFace",
                    "fontSize",
                )
            },
        )

    ET.indent(root, space="    ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    rendered = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"{emit_fcpxml.ALLOWED_DOCTYPE}\n{body}\n"
    )
    emit_fcpxml.validate_fcpxml(rendered, profile=profile, binding=binding)
    return rendered


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_JSON_LIMIT_BYTES + 1)
        if len(encoded) > _JSON_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_artifact(path: Path, *, contract: str, code: str) -> _LoadedArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected, code)
    try:
        payload = json.loads(
            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
        )
        contracts.validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(code) from error
    return _LoadedArtifact(
        path=selected,
        payload=payload,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
        invalid_code=code,
    )


def _verify_artifact(artifact: _LoadedArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_STORY_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_STORY_INPUT_CHANGED")


def _hash_regular_media(path: Path) -> str:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
    digest = hashlib.sha256()
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
            raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            while chunk := stream.read(_HASH_CHUNK_BYTES):
                digest.update(chunk)
    except OSError as error:
        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return digest.hexdigest()


def emit_story_and_publish(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    sync_map_path: Path,
    aligned_path: Path,
    grouping_path: Path,
    working_cut_path: Path,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
    output_path: Path,
) -> str:
    """Load exact authorities, render a story cut, and publish without overwrite."""

    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    sync_map = _load_artifact(
        sync_map_path, contract="sync-map-v1", code="TRITRACK_STORY_SYNC_INVALID"
    )
    aligned = _load_artifact(
        aligned_path,
        contract="aligned-transcript-v1",
        code="TRITRACK_STORY_ALIGNED_INVALID",
    )
    grouping = _load_artifact(
        grouping_path,
        contract="grouping-v1",
        code="TRITRACK_STORY_GROUPING_INVALID",
    )
    working_cut = _load_artifact(
        working_cut_path,
        contract="working-cut-v1",
        code="TRITRACK_STORY_WORKING_CUT_INVALID",
    )
    if grouping.encoded != organizer.encode_grouping(grouping.payload):
        raise ValueError("TRITRACK_STORY_GROUPING_NONCANONICAL")
    if working_cut.encoded != organizer.encode_working_cut(working_cut.payload):
        raise ValueError("TRITRACK_STORY_WORKING_CUT_NONCANONICAL")

    profile = doctor.load_profile(profile_id)
    doctor.load_title_binding(binding_id)
    source_hashes = {
        (camera, source.media_id): _hash_regular_media(source.path)
        for camera, camera_sources in (
            ("A", camera_a_sources),
            ("B", camera_b_sources),
        )
        for source in camera_sources
    }
    probed = emit_fcpxml.probe_sources(
        camera_a_sources, camera_b_sources, profile=profile
    )
    sources = [
        {**source, "sha256": source_hashes[(source["camera"], source["media_id"])]}
        for source in probed
    ]
    assert isinstance(sync_map.payload, Mapping)
    assert isinstance(aligned.payload, Mapping)
    assert isinstance(grouping.payload, Mapping)
    assert isinstance(working_cut.payload, Mapping)
    timeline = build_story_timeline(
        sync_map.payload,
        aligned.payload,
        grouping.payload,
        working_cut.payload,
        sources,
        aligned_sha256=aligned.sha256,
        grouping_sha256=grouping.sha256,
        profile=profile,
    )
    rendered = render_story_fcpxml(
        timeline,
        profile_id=profile_id,
        binding_id=binding_id,
        metadata=metadata,
    )
    for artifact in (sync_map, aligned, grouping, working_cut):
        _verify_artifact(artifact)
    for camera, camera_sources in (
        ("A", camera_a_sources),
        ("B", camera_b_sources),
    ):
        for source in camera_sources:
            if _hash_regular_media(source.path) != source_hashes[(camera, source.media_id)]:
                raise ValueError("TRITRACK_STORY_INPUT_CHANGED")
    emit_fcpxml.publish_fcpxml(
        destination,
        rendered,
        profile=profile,
        binding=doctor.load_title_binding(binding_id),
    )
    return rendered
