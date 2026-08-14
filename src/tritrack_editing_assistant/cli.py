"""Command-line boundary for the TriTrack Editing Assistant scaffold."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from . import doctor as doctor_module
from . import emit_fcpxml as emit_module
from . import sync_scan as sync_module

EXIT_OK = 0
EXIT_USAGE = 64
EXIT_DATA = 65
EXIT_DEPENDENCY = 69
EXIT_OUTPUT_EXISTS = 73
EXIT_IO = 74
EXIT_TEMPORARY = 75
EXIT_POLICY = 78


COMPONENTS = (
    {
        "sourceComponent": "sync_scan.py",
        "command": "sync",
        "status": "implemented",
    },
    {
        "sourceComponent": "emit_fcpxml.py",
        "command": "emit",
        "status": "implemented",
    },
    {
        "sourceComponent": "transcribe_takes.py",
        "command": "transcribe",
        "status": "planned",
    },
    {
        "sourceComponent": "string_out.py",
        "command": "emit",
        "status": "implemented",
    },
    {
        "sourceComponent": "hallucination.py",
        "command": "transcribe",
        "status": "planned",
    },
    {"sourceComponent": "organizer.py", "command": "organize", "status": "planned"},
    {"sourceComponent": "paper_edit.py", "command": "paper", "status": "planned"},
    {"sourceComponent": "align_text.py", "command": "align", "status": "planned"},
    {
        "sourceComponent": "gemini_hybrid.py",
        "command": "hybrid",
        "status": "planned",
    },
    {
        "sourceComponent": "gemini_transcribe.mjs",
        "command": "hybrid",
        "status": "planned",
    },
    {"sourceComponent": "multicam-sync", "command": "run", "status": "planned"},
)


def _print_components(arguments: argparse.Namespace) -> int:
    payload = {
        "schemaVersion": "tritrack.components/v1",
        "toolVersion": __version__,
        "components": list(COMPONENTS),
    }
    if arguments.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return EXIT_OK

    print("COMPONENT\tCOMMAND\tSTATUS")
    for component in COMPONENTS:
        print(
            f"{component['sourceComponent']}\t"
            f"{component['command']}\t{component['status']}"
        )
    return EXIT_OK


def _planned_command(arguments: argparse.Namespace) -> int:
    print(
        f"TRITRACK_COMMAND_NOT_IMPLEMENTED: {arguments.command}",
        flush=True,
    )
    return EXIT_USAGE


def _print_doctor(arguments: argparse.Namespace) -> int:
    try:
        doctor_arguments = {
            "profile_id": arguments.profile,
            "transcription_requested": arguments.transcription,
            "whisper_model": arguments.whisper_model,
        }
        if arguments.output is None:
            receipt = doctor_module.build_receipt(**doctor_arguments)
        else:
            receipt = doctor_module.write_receipt(arguments.output, **doctor_arguments)
    except ValueError as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return EXIT_OUTPUT_EXISTS if code == "TRITRACK_OUTPUT_EXISTS" else EXIT_POLICY

    if arguments.json or arguments.output is None:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    if receipt["supported"]:
        return EXIT_OK
    checks = receipt["checks"]
    assert isinstance(checks, list)
    if any(check["status"] in {"missing", "unreadable"} for check in checks):
        return EXIT_DEPENDENCY
    return EXIT_POLICY


def _run_sync(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        payload = sync_module.synchronize_and_publish(
            camera_a,
            camera_b,
            profile_id=arguments.profile,
            output_path=arguments.output,
        )
    except ValueError as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code in {
            "TRITRACK_SYNC_PROBE_FAILED",
            "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
        }:
            return EXIT_DEPENDENCY
        return EXIT_DATA

    if arguments.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return EXIT_OK


def _run_emit(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        metadata = emit_module.ProjectMetadata(
            event_name=arguments.event_name,
            project_name=arguments.project_name,
        )
        emit_module.emit_and_publish(
            camera_a,
            camera_b,
            sync_map_path=arguments.sync_map,
            profile_id=arguments.profile,
            binding_id=arguments.binding,
            metadata=metadata,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_SYNC_PROBE_FAILED":
            return EXIT_DEPENDENCY
        if code == "TRITRACK_PROFILE_UNKNOWN":
            return EXIT_POLICY
        return EXIT_DATA
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tritrack",
        description="Local-first Final Cut editing-assistant workflow",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    components = subparsers.add_parser(
        "components",
        help="list the eleven workflow components and current status",
    )
    components.add_argument("--json", action="store_true", help="emit JSON")
    components.set_defaults(handler=_print_components)

    doctor = subparsers.add_parser(
        "doctor",
        help="inspect the local compatibility profile and dependencies",
    )
    doctor.add_argument("--profile", required=True, help="closed compatibility profile id")
    doctor.add_argument("--output", type=Path, help="create an absent receipt path")
    doctor.add_argument("--json", action="store_true", help="print the sanitized receipt")
    doctor.add_argument(
        "--transcription",
        action="store_true",
        help="also require a readable local whisper model",
    )
    doctor.add_argument("--whisper-model", type=Path)
    doctor.set_defaults(handler=_print_doctor)

    sync = subparsers.add_parser(
        "sync",
        help="discover and audio-verify A/B camera pairs",
    )
    sync.add_argument(
        "--camera-a",
        action="append",
        required=True,
        type=Path,
        help="local camera-A media path; repeat for each source",
    )
    sync.add_argument(
        "--camera-b",
        action="append",
        required=True,
        type=Path,
        help="local camera-B media path; repeat for each source",
    )
    sync.add_argument("--profile", required=True, help="public compatibility profile id")
    sync.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent sync-map-v1 JSON path",
    )
    sync.add_argument("--json", action="store_true", help="also print the sync map")
    sync.set_defaults(handler=_run_sync)

    emit = subparsers.add_parser(
        "emit",
        help="emit a profile-bound deterministic Final Cut XML string-out",
    )
    emit.add_argument(
        "--camera-a",
        action="append",
        required=True,
        type=Path,
        help="local camera-A media path; repeat for each source",
    )
    emit.add_argument(
        "--camera-b",
        action="append",
        required=True,
        type=Path,
        help="local camera-B media path; repeat for each source",
    )
    emit.add_argument(
        "--sync-map",
        required=True,
        type=Path,
        help="strict sync-map-v1 JSON path",
    )
    emit.add_argument("--profile", required=True, help="public compatibility profile id")
    emit.add_argument("--binding", required=True, help="public title binding id")
    emit.add_argument("--event-name", required=True, help="caller-owned event name")
    emit.add_argument("--project-name", required=True, help="caller-owned project name")
    emit.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent FCPXML path",
    )
    emit.set_defaults(handler=_run_emit)

    planned_commands = {
        "transcribe": "transcribe local takes",
        "align": "align provider-neutral text to local cue timing",
        "hybrid": "run an explicit optional provider-assisted alignment",
        "validate": "validate generated output",
        "organize": "build a validated question-grouped working cut",
        "paper": "export or apply a paper-edit workbook",
        "run": "orchestrate the complete local workflow",
    }
    for name, help_text in planned_commands.items():
        command_parser = subparsers.add_parser(name, help=help_text)
        command_parser.set_defaults(handler=_planned_command)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    return arguments.handler(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
