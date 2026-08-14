"""Generate invented A/B media and exercise the installed public CLI."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from jsonschema import ValidationError

from tritrack_editing_assistant import contracts, doctor, emit_fcpxml, process

PROFILE_ID = "uhd-2997-ndf-fcpxml-1.14"
BINDING_ID = "basic-title-v1"
DEFAULT_EVENT_NAME = "Invented & Public Demo"
DEFAULT_PROJECT_NAME = "Invented <A/B> String-out"
PROCESS_TIMEOUT_SECONDS = 300.0
PROCESS_CAPTURE_BYTES = 1024 * 1024
_AUTO_DTD = object()

Runner = Callable[..., process.ProcessResult]


class DemoFailure(RuntimeError):
    """One controlled, public-safe quickstart failure."""


def _reserve_output_root(output_root: Path) -> None:
    try:
        process.require_absent_output(output_root)
    except ValueError as error:
        raise DemoFailure("TRITRACK_DEMO_OUTPUT_EXISTS") from error
    if not output_root.parent.is_dir():
        raise DemoFailure("TRITRACK_DEMO_OUTPUT_PARENT_MISSING")
    try:
        os.mkdir(output_root, 0o755)
    except FileExistsError as error:
        raise DemoFailure("TRITRACK_DEMO_OUTPUT_EXISTS") from error
    except OSError as error:
        raise DemoFailure("TRITRACK_DEMO_OUTPUT_CREATE_FAILED") from error


def _default_tritrack_executable() -> str:
    beside_python = Path(sys.executable).with_name("tritrack")
    if beside_python.is_file():
        return str(beside_python)
    discovered = shutil.which("tritrack")
    if discovered is None:
        raise DemoFailure("TRITRACK_DEMO_CLI_MISSING")
    return discovered


def _run_checked(
    runner: Runner,
    command: Sequence[str],
    *,
    error_code: str,
) -> process.ProcessResult:
    result = runner(
        command,
        timeout_seconds=PROCESS_TIMEOUT_SECONDS,
        max_captured_bytes=PROCESS_CAPTURE_BYTES,
    )
    if not result.ok:
        raise DemoFailure(error_code)
    return result


def _media_command(output: Path, *, color: str) -> list[str]:
    return [
        "ffmpeg",
        "-nostdin",
        "-v",
        "error",
        "-n",
        "-f",
        "lavfi",
        "-i",
        f"color=c={color}:s=3840x2160:r=30000/1001:d=4",
        "-f",
        "lavfi",
        "-i",
        "anoisesrc=color=white:r=48000:a=0.1:seed=20260814:d=4",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-tune",
        "stillimage",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30000/1001",
        "-video_track_timescale",
        "30000",
        "-colorspace",
        "bt709",
        "-color_trc",
        "bt709",
        "-color_primaries",
        "bt709",
        "-x264-params",
        "colorprim=bt709:transfer=bt709:colormatrix=bt709",
        "-c:a",
        "aac",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-metadata",
        "creation_time=2026-08-14T00:00:00Z",
        "-shortest",
        str(output),
    ]


def _load_and_validate_outputs(sync_map_path: Path, fcpxml_path: Path) -> dict:
    try:
        sync_map = json.loads(sync_map_path.read_text(encoding="utf-8"))
        contracts.validate_contract("sync-map-v1", sync_map)
        if sync_map["profileId"] != PROFILE_ID:
            raise DemoFailure("TRITRACK_DEMO_PROFILE_MISMATCH")
        if len(sync_map["pairs"]) != 1:
            raise DemoFailure("TRITRACK_DEMO_SYNC_PAIR_MISSING")
        profile = doctor.load_profile(PROFILE_ID)
        binding = doctor.load_title_binding(BINDING_ID)
        xml_text = fcpxml_path.read_text(encoding="utf-8")
        emit_fcpxml.validate_fcpxml(
            xml_text,
            profile=profile,
            binding=binding,
        )
    except DemoFailure:
        raise
    except (OSError, TypeError, ValueError, json.JSONDecodeError, ValidationError) as error:
        raise DemoFailure("TRITRACK_DEMO_VALIDATION_FAILED") from error
    return sync_map


def _resolve_dtd(dtd_path: object) -> Path | None:
    if dtd_path is None:
        return None
    if dtd_path is _AUTO_DTD:
        candidate = doctor.FINAL_CUT_DTD_DIRECTORY / "FCPXMLv1_14.dtd"
        return candidate if candidate.is_file() else None
    candidate = Path(dtd_path)  # type: ignore[arg-type]
    if not candidate.is_file():
        raise DemoFailure("TRITRACK_DEMO_DTD_UNREADABLE")
    return candidate


def run_demo(
    output_root: str | os.PathLike[str],
    *,
    tritrack_executable: str | None = None,
    runner: Runner = process.run_bounded,
    dtd_path: object = _AUTO_DTD,
    event_name: str = DEFAULT_EVENT_NAME,
    project_name: str = DEFAULT_PROJECT_NAME,
) -> dict[str, object]:
    """Run one no-overwrite invented demo and return a sanitized report."""

    root = Path(output_root)
    _reserve_output_root(root)
    executable = tritrack_executable or _default_tritrack_executable()
    media_root = root / "media"
    results_root = root / "results"
    media_root.mkdir()
    results_root.mkdir()

    camera_a = media_root / "A & invented.MP4"
    camera_b = media_root / "B invented.MP4"
    for path, color in ((camera_a, "0x274060"), (camera_b, "0x6b2d5c")):
        _run_checked(
            runner,
            _media_command(path, color=color),
            error_code="TRITRACK_DEMO_MEDIA_GENERATION_FAILED",
        )

    components_result = _run_checked(
        runner,
        [executable, "components", "--json"],
        error_code="TRITRACK_DEMO_COMPONENTS_FAILED",
    )
    try:
        component_count = len(json.loads(components_result.stdout)["components"])
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise DemoFailure("TRITRACK_DEMO_COMPONENTS_INVALID") from error
    if component_count != 11:
        raise DemoFailure("TRITRACK_DEMO_COMPONENT_COUNT_CHANGED")

    sync_map_path = results_root / "sync-map.json"
    _run_checked(
        runner,
        [
            executable,
            "sync",
            "--camera-a",
            str(camera_a),
            "--camera-b",
            str(camera_b),
            "--profile",
            PROFILE_ID,
            "--output",
            str(sync_map_path),
            "--json",
        ],
        error_code="TRITRACK_DEMO_SYNC_FAILED",
    )

    primary_fcpxml = results_root / "string-out.fcpxml"
    comparison_fcpxml = results_root / ".determinism-check.fcpxml"
    emit_base = [
        executable,
        "emit",
        "--camera-a",
        str(camera_a),
        "--camera-b",
        str(camera_b),
        "--sync-map",
        str(sync_map_path),
        "--profile",
        PROFILE_ID,
        "--binding",
        BINDING_ID,
        "--event-name",
        event_name,
        "--project-name",
        project_name,
        "--output",
    ]
    for output in (primary_fcpxml, comparison_fcpxml):
        _run_checked(
            runner,
            [*emit_base, str(output)],
            error_code="TRITRACK_DEMO_EMIT_FAILED",
        )
    try:
        deterministic = primary_fcpxml.read_bytes() == comparison_fcpxml.read_bytes()
    except OSError as error:
        raise DemoFailure("TRITRACK_DEMO_FCPXML_UNREADABLE") from error
    if not deterministic:
        raise DemoFailure("TRITRACK_DEMO_FCPXML_NONDETERMINISTIC")
    try:
        comparison_fcpxml.unlink()
    except OSError as error:
        raise DemoFailure("TRITRACK_DEMO_CLEANUP_FAILED") from error

    sync_map = _load_and_validate_outputs(sync_map_path, primary_fcpxml)
    selected_dtd = _resolve_dtd(dtd_path)
    dtd_status = "not-available"
    if selected_dtd is not None:
        _run_checked(
            runner,
            [
                "xmllint",
                "--noout",
                "--dtdvalid",
                selected_dtd.absolute().as_uri(),
                str(primary_fcpxml),
            ],
            error_code="TRITRACK_DEMO_DTD_VALIDATION_FAILED",
        )
        dtd_status = "passed"

    return {
        "status": "ok",
        "profileId": PROFILE_ID,
        "titleBindingId": BINDING_ID,
        "componentCount": component_count,
        "syncPairCount": len(sync_map["pairs"]),
        "deterministicFcpxml": deterministic,
        "fcpxmlStructure": "passed",
        "dtdValidation": dtd_status,
        "outputs": [
            "media/A & invented.MP4",
            "media/B invented.MP4",
            "results/sync-map.json",
            "results/string-out.fcpxml",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate invented local A/B media, synchronize it, and emit one "
            "deterministic FCPXML string-out."
        )
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="caller-selected demo directory that must not already exist",
    )
    parser.add_argument("--event-name", default=DEFAULT_EVENT_NAME)
    parser.add_argument("--project-name", default=DEFAULT_PROJECT_NAME)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        report = run_demo(
            arguments.output,
            event_name=arguments.event_name,
            project_name=arguments.project_name,
        )
    except DemoFailure as error:
        print(json.dumps({"status": "failed", "error": str(error)}))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
