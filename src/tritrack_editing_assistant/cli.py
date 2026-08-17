"""Command-line boundary for the TriTrack Editing Assistant scaffold."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from . import align_text as align_module
from . import doctor as doctor_module
from . import emit_fcpxml as emit_module
from . import gemini_hybrid as hybrid_module
from . import organizer as organizer_module
from . import paper_edit as paper_module
from . import run_workflow as run_module
from . import sync_scan as sync_module
from . import transcribe_takes as transcribe_module

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
        "status": "implemented",
    },
    {
        "sourceComponent": "string_out.py",
        "command": "emit",
        "status": "implemented",
    },
    {
        "sourceComponent": "hallucination.py",
        "command": "transcribe",
        "status": "implemented",
    },
    {
        "sourceComponent": "organizer.py",
        "command": "organize",
        "status": "implemented",
    },
    {
        "sourceComponent": "paper_edit.py",
        "command": "paper",
        "status": "implemented",
    },
    {
        "sourceComponent": "align_text.py",
        "command": "align",
        "status": "implemented",
    },
    {
        "sourceComponent": "gemini_hybrid.py",
        "command": "hybrid",
        "status": "implemented",
    },
    {
        "sourceComponent": "gemini_transcribe.mjs",
        "command": "hybrid",
        "status": "planned",
    },
    {
        "sourceComponent": "multicam-sync",
        "command": "run",
        "status": "implemented",
    },
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


def _run_transcribe(arguments: argparse.Namespace) -> int:
    try:
        payload = transcribe_module.transcribe_and_publish(
            arguments.media,
            model_path=arguments.model,
            language=arguments.language,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        if code in {
            "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
            "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
            "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
        }:
            return EXIT_DEPENDENCY
        if code in {
            "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
            "TRITRACK_TRANSCRIPT_MEDIA_REQUIRED",
        }:
            return EXIT_USAGE
        return EXIT_DATA

    if arguments.json:
        takes = payload["takes"]
        assert isinstance(takes, list)
        with arguments.output.open("rb") as stream:
            bundle_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
        summary = {
            "schemaVersion": "tritrack.transcribe-summary/v1",
            "takeCount": len(takes),
            "completedCount": sum(take["status"] == "completed" for take in takes),
            "emptyCount": sum(take["status"] == "empty" for take in takes),
            "bundleSha256": bundle_sha256,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return EXIT_OK


def _alignment_summary(
    payload: dict[str, object], output_path: Path
) -> dict[str, object]:
    takes = payload["takes"]
    assert isinstance(takes, list)
    cue_count = 0
    revised_cue_count = 0
    for take in takes:
        assert isinstance(take, dict)
        cues = take["cues"]
        assert isinstance(cues, list)
        cue_count += len(cues)
        revised_cue_count += sum(
            isinstance(cue, dict) and cue["disposition"] == "revised"
            for cue in cues
        )
    with output_path.open("rb") as stream:
        artifact_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
    return {
        "schemaVersion": "tritrack.align-summary/v1",
        "takeCount": len(takes),
        "cueCount": cue_count,
        "revisedCueCount": revised_cue_count,
        "artifactSha256": artifact_sha256,
    }


def _run_align(arguments: argparse.Namespace) -> int:
    try:
        payload = align_module.align_and_publish(
            arguments.transcript,
            arguments.revision,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        return EXIT_DATA

    if arguments.json:
        print(
            json.dumps(
                _alignment_summary(payload, arguments.output),
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_hybrid(arguments: argparse.Namespace) -> int:
    try:
        payload = hybrid_module.hybrid_and_publish(
            arguments.transcript,
            arguments.proposal,
            arguments.receipt,
            exact_model=arguments.model,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        if code == "TRITRACK_HYBRID_MODEL_INVALID":
            return EXIT_USAGE
        return EXIT_DATA

    if arguments.json:
        print(
            json.dumps(
                _alignment_summary(payload, arguments.output),
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_organize(arguments: argparse.Namespace) -> int:
    try:
        payload = organizer_module.organize_and_publish(
            arguments.aligned,
            arguments.grouping,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code in {
            "TRITRACK_OUTPUT_PARENT_MISSING",
            "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
        }:
            return EXIT_IO
        return EXIT_DATA

    if arguments.json:
        questions = payload["questions"]
        segments = payload["segments"]
        reserve = payload["reserve"]
        assert isinstance(questions, list)
        assert isinstance(segments, list)
        assert isinstance(reserve, list)
        with arguments.output.open("rb") as stream:
            artifact_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.organize-summary/v1",
                    "questionCount": len(questions),
                    "segmentCount": len(segments),
                    "reserveCount": len(reserve),
                    "artifactSha256": artifact_sha256,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _paper_error_exit(code: str) -> int:
    if code == "TRITRACK_OUTPUT_EXISTS":
        return EXIT_OUTPUT_EXISTS
    if code in {
        "TRITRACK_OUTPUT_PARENT_MISSING",
        "TRITRACK_PAPER_INPUT_UNREADABLE",
    }:
        return EXIT_IO
    return EXIT_DATA


def _output_sha256(output_path: Path) -> str:
    with output_path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _run_paper_export(arguments: argparse.Namespace) -> int:
    try:
        summary = paper_module.export_workbook(
            arguments.aligned,
            grouping_path=arguments.grouping,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _paper_error_exit(code)
    if arguments.json:
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.paper-export-summary/v1",
                    **summary,
                    "artifactSha256": _output_sha256(arguments.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_paper_apply(arguments: argparse.Namespace) -> int:
    try:
        grouping = paper_module.apply_workbook(
            arguments.aligned,
            arguments.workbook,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _paper_error_exit(code)
    if arguments.json:
        questions = grouping["questions"]
        reserve = grouping["reserve"]
        assert isinstance(questions, list)
        assert isinstance(reserve, list)
        answer_count = 0
        for question in questions:
            assert isinstance(question, dict)
            answers = question["answers"]
            assert isinstance(answers, list)
            answer_count += len(answers)
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.paper-apply-summary/v1",
                    "questionCount": len(questions),
                    "answerCount": answer_count,
                    "reserveCount": len(reserve),
                    "artifactSha256": _output_sha256(arguments.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_error_exit(code: str) -> int:
    if code == "TRITRACK_OUTPUT_EXISTS":
        return EXIT_OUTPUT_EXISTS
    if code in {
        "TRITRACK_OUTPUT_PARENT_MISSING",
        "TRITRACK_RUN_INPUT_UNREADABLE",
        "TRITRACK_STORY_SOURCE_UNREADABLE",
        "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
        "TRITRACK_PAPER_INPUT_UNREADABLE",
    }:
        return EXIT_IO
    if code in {
        "TRITRACK_SYNC_PROBE_FAILED",
        "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
        "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
        "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
        "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
    }:
        return EXIT_DEPENDENCY
    if code in {
        "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED",
        "TRITRACK_PROFILE_UNKNOWN",
    }:
        return EXIT_POLICY
    if code in {
        "TRITRACK_RUN_SOURCE_REQUIRED",
        "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID",
        "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
        "TRITRACK_EMIT_METADATA_INVALID",
    }:
        return EXIT_USAGE
    return EXIT_DATA


def _print_run_summary(summary: dict[str, object], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    print(f"RUN\t{summary['runId']}")
    print(f"PHASE\t{summary['phase']}")
    print(f"NEXT\t{summary['nextAction']}")
    print(f"STAGES\t{','.join(summary['stages'])}")
    artifacts = summary["artifacts"]
    assert isinstance(artifacts, dict)
    for logical_name, sha256 in artifacts.items():
        print(f"ARTIFACT\t{logical_name}\t{sha256}")


def _run_prepare(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        summary = run_module.prepare_run(
            camera_a,
            camera_b,
            arguments.transcribe_media,
            model_path=arguments.model,
            language=arguments.language,
            profile_id=arguments.profile,
            binding_id=arguments.binding,
            metadata=emit_module.ProjectMetadata(
                arguments.event_name, arguments.project_name
            ),
            run_id=arguments.run_id,
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_align_bundle(arguments: argparse.Namespace) -> int:
    try:
        summary = run_module.align_run(
            arguments.prepared,
            arguments.revision,
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_finish(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        summary = run_module.finish_run(
            arguments.prepared,
            arguments.aligned,
            arguments.workbook,
            camera_a,
            camera_b,
            metadata=emit_module.ProjectMetadata(
                arguments.event_name, arguments.project_name
            ),
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_status(arguments: argparse.Namespace) -> int:
    try:
        summary = run_module.status_run(arguments.run_dir)
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    _print_run_summary(summary, as_json=arguments.json)
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

    transcribe = subparsers.add_parser(
        "transcribe",
        help="transcribe local media with one fixed local decoding profile",
    )
    transcribe.add_argument(
        "--media",
        action="append",
        required=True,
        type=Path,
        help="local media path; repeat for each take",
    )
    transcribe.add_argument(
        "--model",
        required=True,
        type=Path,
        help="caller-owned readable local whisper.cpp model",
    )
    transcribe.add_argument(
        "--language",
        required=True,
        help="explicit two- or three-letter spoken-language code",
    )
    transcribe.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent transcript-bundle-v1 JSON path",
    )
    transcribe.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    transcribe.set_defaults(handler=_run_transcribe)

    align = subparsers.add_parser(
        "align",
        help="promote local cue-addressed text without changing source timing",
    )
    align.add_argument(
        "--transcript",
        required=True,
        type=Path,
        help="strict transcript-bundle-v1 JSON path",
    )
    align.add_argument(
        "--revision",
        required=True,
        type=Path,
        help="strict text-revision-v1 JSON path",
    )
    align.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent aligned-transcript-v1 JSON path",
    )
    align.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    align.set_defaults(handler=_run_align)

    hybrid = subparsers.add_parser(
        "hybrid",
        help="validate optional provider evidence offline",
        description="Offline receipt validation only; no network access.",
    )
    hybrid.add_argument(
        "--transcript",
        required=True,
        type=Path,
        help="strict transcript-bundle-v1 JSON path",
    )
    hybrid.add_argument(
        "--proposal",
        required=True,
        type=Path,
        help="strict text-revision-v1 JSON path",
    )
    hybrid.add_argument(
        "--receipt",
        action="append",
        required=True,
        type=Path,
        help="strict provider-receipt-v1 path; repeat per revised take",
    )
    hybrid.add_argument(
        "--model",
        required=True,
        help="exact provider model recorded in every receipt",
    )
    hybrid.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent aligned-transcript-v1 JSON path",
    )
    hybrid.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    hybrid.set_defaults(handler=_run_hybrid)

    organize = subparsers.add_parser(
        "organize",
        help="compile cue-addressed grouping into a working cut",
    )
    organize.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    organize.add_argument(
        "--grouping",
        required=True,
        type=Path,
        help="strict grouping-v1 JSON path",
    )
    organize.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent working-cut-v1 JSON path",
    )
    organize.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    organize.set_defaults(handler=_run_organize)

    paper = subparsers.add_parser(
        "paper",
        help="export or apply a cue-addressed paper-edit workbook",
    )
    paper_subparsers = paper.add_subparsers(
        dest="paper_command",
        required=True,
    )
    paper_export = paper_subparsers.add_parser(
        "export",
        help="export an editor-facing workbook",
    )
    paper_export.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    paper_export.add_argument(
        "--grouping",
        type=Path,
        help="optional strict grouping-v1 JSON path to prefill",
    )
    paper_export.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent paper-workbook-v1 XLSX path",
    )
    paper_export.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    paper_export.set_defaults(handler=_run_paper_export)

    paper_apply = paper_subparsers.add_parser(
        "apply",
        help="apply a strict workbook to grouping authority",
    )
    paper_apply.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    paper_apply.add_argument(
        "--workbook",
        required=True,
        type=Path,
        help="strict paper-workbook-v1 XLSX path",
    )
    paper_apply.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent grouping-v1 JSON path",
    )
    paper_apply.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    paper_apply.set_defaults(handler=_run_paper_apply)

    run = subparsers.add_parser(
        "run",
        help="publish immutable local workflow stage bundles",
    )
    run_subparsers = run.add_subparsers(dest="run_command", required=True)

    run_prepare = run_subparsers.add_parser(
        "prepare", help="doctor, synchronize, transcribe, and emit a string-out"
    )
    run_prepare.add_argument(
        "--camera-a", action="append", required=True, type=Path
    )
    run_prepare.add_argument(
        "--camera-b", action="append", required=True, type=Path
    )
    run_prepare.add_argument(
        "--transcribe-media", action="append", required=True, type=Path
    )
    run_prepare.add_argument("--model", required=True, type=Path)
    run_prepare.add_argument("--language", required=True)
    run_prepare.add_argument("--profile", required=True)
    run_prepare.add_argument("--binding", required=True)
    run_prepare.add_argument("--event-name", required=True)
    run_prepare.add_argument("--project-name", required=True)
    run_prepare.add_argument("--run-id", required=True)
    run_prepare.add_argument("--output", required=True, type=Path)
    run_prepare.add_argument("--json", action="store_true")
    run_prepare.set_defaults(handler=_run_prepare)

    run_align = run_subparsers.add_parser(
        "align", help="apply one explicit text revision and export paper edit"
    )
    run_align.add_argument("--prepared", required=True, type=Path)
    run_align.add_argument("--revision", required=True, type=Path)
    run_align.add_argument("--output", required=True, type=Path)
    run_align.add_argument("--json", action="store_true")
    run_align.set_defaults(handler=_run_align_bundle)

    run_finish = run_subparsers.add_parser(
        "finish", help="apply paper intent and emit the story cut"
    )
    run_finish.add_argument("--prepared", required=True, type=Path)
    run_finish.add_argument("--aligned", required=True, type=Path)
    run_finish.add_argument("--workbook", required=True, type=Path)
    run_finish.add_argument(
        "--camera-a", action="append", required=True, type=Path
    )
    run_finish.add_argument(
        "--camera-b", action="append", required=True, type=Path
    )
    run_finish.add_argument("--event-name", required=True)
    run_finish.add_argument("--project-name", required=True)
    run_finish.add_argument("--output", required=True, type=Path)
    run_finish.add_argument("--json", action="store_true")
    run_finish.set_defaults(handler=_run_finish)

    run_status = run_subparsers.add_parser(
        "status", help="validate and summarize one complete run bundle"
    )
    run_status.add_argument("--run", dest="run_dir", required=True, type=Path)
    run_status.add_argument("--json", action="store_true")
    run_status.set_defaults(handler=_run_status)

    planned_commands = {
        "validate": "validate generated output",
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
