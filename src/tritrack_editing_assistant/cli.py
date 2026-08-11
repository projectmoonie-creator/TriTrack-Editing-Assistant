"""Command-line boundary for the TriTrack Editing Assistant scaffold."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from . import __version__

EXIT_OK = 0
EXIT_USAGE = 64
EXIT_DATA = 65
EXIT_DEPENDENCY = 69
EXIT_OUTPUT_EXISTS = 73
EXIT_IO = 74
EXIT_TEMPORARY = 75
EXIT_POLICY = 78


COMPONENTS = (
    {"sourceComponent": "sync_scan.py", "command": "sync", "status": "planned"},
    {"sourceComponent": "emit_fcpxml.py", "command": "emit", "status": "planned"},
    {
        "sourceComponent": "transcribe_takes.py",
        "command": "transcribe",
        "status": "planned",
    },
    {"sourceComponent": "string_out.py", "command": "emit", "status": "planned"},
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

    planned_commands = {
        "doctor": "inspect the local compatibility profile and dependencies",
        "sync": "discover and audio-verify A/B camera pairs",
        "transcribe": "transcribe local takes",
        "align": "align provider-neutral text to local cue timing",
        "hybrid": "run an explicit optional provider-assisted alignment",
        "emit": "emit profile-bound Final Cut XML",
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
