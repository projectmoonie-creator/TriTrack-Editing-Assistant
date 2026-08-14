"""Profile-bound FCPXML rendering and no-overwrite publication."""

from __future__ import annotations

import json
import os
import re
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import contracts, doctor, process, string_out, sync_scan

ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
MAX_SYNC_MAP_BYTES = 16 * 1024 * 1024
FORMAT_NAME = "FFVideoFormat3840x2160p2997"


@dataclass(frozen=True)
class ProjectMetadata:
    """Caller-owned names copied into one public string-out project."""

    event_name: str
    project_name: str

    def __post_init__(self) -> None:
        for value in (self.event_name, self.project_name):
            if (
                not isinstance(value, str)
                or not value.strip()
                or any(ord(character) < 32 for character in value)
            ):
                raise ValueError("TRITRACK_EMIT_METADATA_INVALID")


def load_sync_map(path: str | os.PathLike[str]) -> dict[str, object]:
    """Load one strict sync-map-v1 while preserving decimal spellings."""

    source = Path(path)
    try:
        raw = source.read_bytes()
    except OSError as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_UNREADABLE") from error
    if len(raw) > MAX_SYNC_MAP_BYTES or b"\x00" in raw:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
    try:
        payload = json.loads(raw.decode("utf-8"), parse_float=Decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
    if not isinstance(payload, dict):
        raise TypeError("TRITRACK_EMIT_SYNC_MAP_INVALID")
    try:
        contracts.validate_contract("sync-map-v1", payload)
    except ValidationError as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
    return payload


def _frame_time(timeline: string_out.StringOut, frames: int) -> str:
    if frames == 0:
        return "0s"
    numerator = frames * timeline.frame_numerator
    return f"{numerator}/{timeline.frame_denominator}s"


def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
    parameters = binding["parameters"]
    if not isinstance(parameters, list):
        raise TypeError("TRITRACK_FCPXML_BINDING_INVALID")
    values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in parameters
        if isinstance(parameter, Mapping)
    }
    expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
    if set(values) != expected:
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
    return values


def _source_uri(path: Path) -> str:
    try:
        return path.absolute().as_uri()
    except ValueError as error:
        raise ValueError("TRITRACK_EMIT_SOURCE_INVALID") from error


def render_fcpxml(
    sync_map: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    profile_id: str,
    binding_id: str,
    metadata: ProjectMetadata,
) -> str:
    """Render deterministic FCPXML from the closed public inputs."""

    if not isinstance(metadata, ProjectMetadata):
        raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    timeline = string_out.build_string_out(sync_map, sources, profile=profile)
    if timeline.profile_id != profile_id:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    styles = _style_values(binding)

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": FORMAT_NAME,
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
            {
                "kind": "original-media",
                "src": _source_uri(source.path),
            },
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
                "name": segment.label,
                "offset": _frame_time(timeline, segment.offset_frames),
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        for lane, clip in enumerate(segment.clips, start=1):
            clip_attributes = {
                "ref": source_ids[(clip.camera, clip.media_id)],
                "lane": str(lane),
                "offset": _frame_time(timeline, clip.offset_frames),
                "name": clip.media_id,
                "start": "0s",
                "duration": _frame_time(timeline, clip.duration_frames),
                "srcEnable": "all" if clip.audio_enabled else "video",
            }
            if clip.audio_enabled:
                clip_attributes["audioRole"] = "dialogue"
            ET.SubElement(
                gap,
                "asset-clip",
                clip_attributes,
            )
        title = ET.SubElement(
            gap,
            "title",
            {
                "ref": "r2",
                "lane": str(len(segment.clips) + 1),
                "offset": _frame_time(timeline, segment.offset_frames),
                "name": f"{segment.label} - Basic Title",
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        text_element = ET.SubElement(title, "text")
        style_id = f"ts{index:03d}"
        text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
        text_style.text = segment.label
        style_definition = ET.SubElement(
            title,
            "text-style-def",
            {"id": style_id},
        )
        ET.SubElement(
            style_definition,
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
        f"{ALLOWED_DOCTYPE}\n{body}\n"
    )
    validate_fcpxml(rendered, profile=profile, binding=binding)
    return rendered


def _profile_format_attributes(profile: Mapping[str, object]) -> dict[str, str]:
    return {
        "id": "r1",
        "name": FORMAT_NAME,
        "frameDuration": str(profile["frameDuration"]),
        "width": str(profile["width"]),
        "height": str(profile["height"]),
        "colorSpace": str(profile["colorSpace"]),
    }


def _validate_time_values(root: ET.Element, profile: Mapping[str, object]) -> None:
    frame_value = str(profile["frameDuration"])
    numerator_text, _, denominator_text = frame_value[:-1].partition("/")
    frame_numerator = int(numerator_text)
    denominator = int(denominator_text)
    pattern = re.compile(rf"^-?[0-9]+/{denominator}s$")
    for element in root.iter():
        for name in ("offset", "start", "duration"):
            value = element.attrib.get(name)
            if value is None or value == "0s":
                continue
            if not pattern.fullmatch(value):
                raise ValueError("TRITRACK_FCPXML_TIME_INVALID")
            value_numerator = int(value.split("/", 1)[0])
            if value_numerator % frame_numerator:
                raise ValueError("TRITRACK_FCPXML_TIME_INVALID")


def validate_fcpxml(
    text: str,
    *,
    profile: Mapping[str, object],
    binding: Mapping[str, object],
) -> None:
    """Fail closed unless generated XML exactly retains the public profile."""

    contracts.validate_contract("compatibility-profile-v1", profile)
    contracts.validate_contract("title-binding-v1", binding)
    if dict(profile) != doctor.load_profile(str(profile["profileId"])):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    if dict(binding) != doctor.load_title_binding(str(binding["bindingId"])):
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
    if (
        not isinstance(text, str)
        or text.count(ALLOWED_DOCTYPE) != 1
        or "<!ENTITY" in text
        or "<!DOCTYPE" in text.replace(ALLOWED_DOCTYPE, "", 1)
    ):
        raise ValueError("TRITRACK_FCPXML_INVALID")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError("TRITRACK_FCPXML_INVALID") from error
    if root.tag != "fcpxml" or root.attrib != {
        "version": str(profile["fcpxmlVersion"])
    }:
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")

    format_elements = root.findall("./resources/format")
    if (
        len(format_elements) != 1
        or format_elements[0].attrib != _profile_format_attributes(profile)
    ):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    effect_elements = root.findall("./resources/effect")
    if len(effect_elements) != 1 or effect_elements[0].attrib != {
        "id": "r2",
        "name": str(binding["effectName"]),
        "uid": str(binding["effectUid"]),
    }:
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")

    sequence = root.find("./library/event/project/sequence")
    if sequence is None:
        raise ValueError("TRITRACK_FCPXML_INVALID")
    expected_sequence = {
        "format": "r1",
        "tcStart": "0s",
        "tcFormat": str(profile["timecodeFormat"]),
        "audioLayout": "stereo",
        "audioRate": f"{int(profile['audioRate']) // 1000}k",
    }
    if any(sequence.attrib.get(key) != value for key, value in expected_sequence.items()):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    if not sequence.attrib.get("duration"):
        raise ValueError("TRITRACK_FCPXML_TIME_INVALID")

    resource_ids = [
        element.attrib.get("id")
        for element in root.findall("./resources/*")
    ]
    if None in resource_ids or len(resource_ids) != len(set(resource_ids)):
        raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")
    valid_refs = set(resource_ids)
    if any(
        element.attrib["ref"] not in valid_refs
        for element in root.iter()
        if "ref" in element.attrib and element.tag != "text-style"
    ):
        raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")

    for asset in root.findall("./resources/asset"):
        media_representations = asset.findall("./media-rep")
        expected_asset_profile = {
            "format": "r1",
            "hasVideo": "1",
            "hasAudio": "1",
            "audioSources": "1",
            "audioChannels": "2",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        }
        if any(
            asset.attrib.get(name) != value
            for name, value in expected_asset_profile.items()
        ):
            raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
        if (
            "src" in asset.attrib
            or len(media_representations) != 1
            or media_representations[0].attrib.get("kind") != "original-media"
            or not media_representations[0].attrib.get("src", "").startswith("file:")
        ):
            raise ValueError("TRITRACK_FCPXML_SOURCE_INVALID")

    for gap in root.findall("./library/event/project/sequence/spine/gap"):
        clips = gap.findall("./asset-clip")
        if (
            not clips
            or sum(clip.attrib.get("srcEnable") == "all" for clip in clips) != 1
            or any(
                clip.attrib.get("srcEnable") not in {"all", "video"}
                or (
                    (clip.attrib.get("srcEnable") == "all")
                    != (clip.attrib.get("audioRole") == "dialogue")
                )
                for clip in clips
            )
        ):
            raise ValueError("TRITRACK_FCPXML_AUDIO_INVALID")

    expected_styles = _style_values(binding)
    style_ids: set[str] = set()
    for definition in root.iter("text-style-def"):
        style_id = definition.attrib.get("id")
        styles = definition.findall("./text-style")
        if (
            not style_id
            or style_id in style_ids
            or len(styles) != 1
            or styles[0].attrib != expected_styles
        ):
            raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
        style_ids.add(style_id)
    for text_style in root.iter("text-style"):
        if "ref" in text_style.attrib and text_style.attrib["ref"] not in style_ids:
            raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")
    _validate_time_values(root, profile)


def publish_fcpxml(
    output_path: str | os.PathLike[str],
    text: str,
    *,
    profile: Mapping[str, object],
    binding: Mapping[str, object],
) -> Path:
    """Atomically create one validated FCPXML path without overwriting."""

    validate_fcpxml(text, profile=profile, binding=binding)
    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def _probe_sources(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    profile: Mapping[str, object],
) -> list[dict[str, object]]:
    contracts.validate_contract("compatibility-profile-v1", profile)
    if dict(profile) != doctor.load_profile(str(profile["profileId"])):
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    frame_duration = str(profile["frameDuration"])
    numerator, separator, denominator = frame_duration.removesuffix("s").partition("/")
    if not separator or str(profile["colorSpace"]) != "1-1-1 (Rec. 709)":
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    expected_fields = {
        "videoStreamCount",
        "audioStreamCount",
        "width",
        "height",
        "frameRate",
        "colorSpace",
        "colorTransfer",
        "colorPrimaries",
        "sampleRate",
        "channels",
    }
    expected_values = {
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "frameRate": f"{denominator}/{numerator}",
        "colorSpace": "bt709",
        "colorTransfer": "bt709",
        "colorPrimaries": "bt709",
        "sampleRate": str(profile["audioRate"]),
        "channels": 2,
    }
    media: list[dict[str, object]] = []
    for camera, sources in (("A", camera_a_sources), ("B", camera_b_sources)):
        for source in sources:
            probed = sync_scan.probe_media(source)
            compatibility = probed.get("compatibility")
            if (
                not isinstance(compatibility, Mapping)
                or set(compatibility) != expected_fields
                or not isinstance(compatibility["videoStreamCount"], int)
                or compatibility["videoStreamCount"] < 1
                or not isinstance(compatibility["audioStreamCount"], int)
                or compatibility["audioStreamCount"] < 1
                or any(
                    compatibility[field] != value
                    for field, value in expected_values.items()
                )
            ):
                raise ValueError("TRITRACK_EMIT_SOURCE_PROFILE_MISMATCH")
            media.append(
                {
                    "camera": camera,
                    "media_id": source.media_id,
                    "path": source.path,
                    "duration_seconds": Decimal(str(probed["duration_seconds"])),
                }
            )
    return media


def emit_and_publish(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    sync_map_path: str | os.PathLike[str],
    profile_id: str,
    binding_id: str,
    metadata: ProjectMetadata,
    output_path: str | os.PathLike[str],
) -> str:
    """Load, probe, render, validate, and atomically publish one FCPXML."""

    process.require_absent_output(output_path)
    sync_map = load_sync_map(sync_map_path)
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    if sync_map["profileId"] != profile_id:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    media = _probe_sources(
        camera_a_sources,
        camera_b_sources,
        profile=profile,
    )
    rendered = render_fcpxml(
        sync_map,
        media,
        profile_id=profile_id,
        binding_id=binding_id,
        metadata=metadata,
    )
    publish_fcpxml(
        output_path,
        rendered,
        profile=profile,
        binding=binding,
    )
    return rendered
