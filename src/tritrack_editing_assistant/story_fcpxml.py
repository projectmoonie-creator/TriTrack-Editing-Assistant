"""Deterministic projection of exact editorial authorities into story time."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from jsonschema import ValidationError

from . import contracts, doctor, organizer, string_out

_SOURCE_FIELDS = frozenset(
    {"camera", "media_id", "path", "duration_seconds", "sha256"}
)


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
