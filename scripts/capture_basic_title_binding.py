#!/usr/bin/env python3
"""Capture a public-safe Basic Title binding from invented FCPXML."""

from __future__ import annotations

import argparse
import json
import os
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from pathlib import Path

from tritrack_editing_assistant.contracts import validate_contract
from tritrack_editing_assistant.doctor import load_profile
from tritrack_editing_assistant.process import require_absent_output

FORBIDDEN_TEXT = (
    "Artlist LT",
    "江城知音体",
    "Transcription Template",
    "/Users/",
    "/Volumes/HoneyPot/",
)
STYLE_ATTRIBUTES = ("alignment", "font", "fontColor", "fontFace", "fontSize")
ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"


def _read_public_xml(path: Path) -> str:
    data = path.read_bytes()
    if b"\x00" in data:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
    text = data.decode("utf-8")
    without_allowed_doctype = text.replace(ALLOWED_DOCTYPE, "", 1)
    if (
        "<!DOCTYPE" in without_allowed_doctype
        or "<!ENTITY" in text
        or text.count(ALLOWED_DOCTYPE) > 1
    ):
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
    if any(value in text for value in FORBIDDEN_TEXT):
        raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")
    return text


def _parameter_value(value: str) -> str | int | float | bool:
    try:
        number = float(value)
    except ValueError:
        return value
    return int(number) if number.is_integer() else number


def capture_binding(source: Path) -> dict[str, object]:
    """Extract only the referenced Basic Title effect and style attributes."""

    text = _read_public_xml(source)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML") from error

    for element in root.iter():
        source_value = element.attrib.get("src")
        if source_value:
            raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

    effects = {
        effect.attrib.get("id"): effect
        for effect in root.findall("./resources/effect")
        if effect.attrib.get("name") == "Basic Title"
    }
    titles = [
        title for title in root.iter("title") if title.attrib.get("ref") in effects
    ]
    if len(titles) != 1:
        raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")
    effect = effects[titles[0].attrib["ref"]]
    uid = effect.attrib.get("uid")
    if not uid or not uid.endswith("Basic Title.moti"):
        raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")

    style_elements = titles[0].findall("./text-style-def/text-style")
    if len(style_elements) != 1:
        raise ValueError("TRITRACK_TITLE_BINDING_STYLE_REQUIRED")
    style = style_elements[0]
    parameters = [
        {"name": name, "value": _parameter_value(style.attrib[name])}
        for name in STYLE_ATTRIBUTES
        if name in style.attrib
    ]
    binding: dict[str, object] = {
        "schemaVersion": "tritrack.title-binding/v1",
        "bindingId": "basic-title-v1",
        "effectName": "Basic Title",
        "effectUid": uid,
        "parameters": parameters,
    }
    validate_contract("title-binding-v1", binding)
    return binding


def render_basic_title_fcpxml(binding: Mapping[str, object], *, text: str) -> str:
    """Render a minimal, public-safe NDF project from a reviewed binding."""

    validate_contract("title-binding-v1", dict(binding))
    if not text.strip() or "\n" in text or "\r" in text:
        raise ValueError("TRITRACK_TITLE_BINDING_TEXT_REQUIRED")
    if any(value in text for value in FORBIDDEN_TEXT):
        raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

    profile = load_profile("uhd-2997-ndf-fcpxml-1.14")
    style_values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in binding["parameters"]  # type: ignore[index]
    }
    missing_styles = set(STYLE_ATTRIBUTES) - style_values.keys()
    if missing_styles:
        raise ValueError("TRITRACK_TITLE_BINDING_STYLE_REQUIRED")

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": "FFVideoFormat3840x2160p2997",
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

    event = ET.SubElement(root, "event", {"name": "TriTrack Public Evidence"})
    project = ET.SubElement(
        event, "project", {"name": "TriTrack Basic Title Roundtrip"}
    )
    sequence = ET.SubElement(
        project,
        "sequence",
        {
            "format": "r1",
            "duration": "180180/30000s",
            "tcStart": "0s",
            "tcFormat": str(profile["timecodeFormat"]),
            "audioLayout": "stereo",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        },
    )
    spine = ET.SubElement(sequence, "spine")
    ET.SubElement(
        spine,
        "gap",
        {
            "name": "Gap",
            "offset": "0s",
            "start": "0s",
            "duration": "90090/30000s",
        },
    )
    title = ET.SubElement(
        spine,
        "title",
        {
            "ref": "r2",
            "offset": "90090/30000s",
            "name": f"{text} - Basic Title",
            "start": "0s",
            "duration": "90090/30000s",
        },
    )
    text_element = ET.SubElement(title, "text")
    text_style = ET.SubElement(text_element, "text-style", {"ref": "ts1"})
    text_style.text = text
    text_style_definition = ET.SubElement(title, "text-style-def", {"id": "ts1"})
    ET.SubElement(
        text_style_definition,
        "text-style",
        {attribute: style_values[attribute] for attribute in STYLE_ATTRIBUTES},
    )

    ET.indent(root, space="    ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{ALLOWED_DOCTYPE}\n{body}\n'


def _write_exclusive(output: Path, encoded: bytes) -> None:
    destination = require_absent_output(output)
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def write_binding(source: Path, output: Path) -> dict[str, object]:
    binding = capture_binding(source)
    encoded = (json.dumps(binding, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _write_exclusive(output, encoded)
    return binding


def write_rendered_fcpxml(binding_path: Path, output: Path, text: str) -> None:
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    rendered = render_basic_title_fcpxml(binding, text=text)
    _write_exclusive(output, rendered.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--binding", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--text")
    arguments = parser.parse_args()
    if arguments.input is not None:
        if arguments.text is not None:
            parser.error("--text is only valid with --binding")
        write_binding(arguments.input, arguments.output)
    else:
        if arguments.text is None:
            parser.error("--text is required with --binding")
        write_rendered_fcpxml(arguments.binding, arguments.output, arguments.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
