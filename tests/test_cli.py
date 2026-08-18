import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from tests.test_contracts import VALID_CONTRACTS
from tritrack_editing_assistant import cli, run_workflow

ROOT = Path(__file__).resolve().parents[1]


def write_alignment_inputs(root: Path) -> tuple[Path, Path]:
    transcript = {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": "whisper-cpp-cpu-no-fallback-v1",
        "language": "en",
        "modelSha256": "3" * 64,
        "engine": {
            "name": "whisper-cli",
            "version": "whisper.cpp version: invented-cli",
        },
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented private source text.",
                    }
                ],
            }
        ],
    }
    transcript_path = root / "transcript.json"
    transcript_path.write_text(
        json.dumps(transcript, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    revision = {
        "schemaVersion": "tritrack.text-revision/v1",
        "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
        "language": "en",
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "revisions": [
                    {
                        "cueId": "cue-000001",
                        "text": "Invented private revised text.",
                    }
                ],
            }
        ],
    }
    revision_path = root / "revision.json"
    revision_path.write_text(
        json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return transcript_path, revision_path


def write_hybrid_receipt(root: Path, transcript_path: Path) -> Path:
    receipt = {
        "schemaVersion": "tritrack.provider-receipt/v1",
        "provider": "gemini",
        "operation": "audio-transcription",
        "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
        "takeId": "Invented.wav",
        "requestedModel": "gemini-invented-exact",
        "observedModel": "gemini-invented-exact",
        "audioSha256": "a" * 64,
        "requestStatus": "completed",
        "responseStatus": 200,
        "upload": {
            "status": "completed",
            "serverFileIdSha256": "e" * 64,
        },
        "serverFileDeletion": {
            "attempted": True,
            "confirmed": True,
            "statusCode": 200,
        },
    }
    receipt_path = root / "receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt_path


class CliSmokeTest(unittest.TestCase):
    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_output_hash_rejects_special_files_before_blocking(self) -> None:
        observed: list[int] = []

        def reject_special(_path, flags, *_args):
            observed.append(flags)
            raise OSError("invented special file")

        with mock.patch.object(
            cli.os, "open", side_effect=reject_special
        ), self.assertRaises(OSError):
            cli._output_sha256(Path("invented-special-file"))
        self.assertEqual(len(observed), 1)
        self.assertTrue(observed[0] & os.O_NONBLOCK)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        completed = self.run_cli_unchecked(*args)
        completed.check_returncode()
        return completed

    def run_cli_unchecked(
        self,
        *args: str,
        environment_overrides: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        if environment_overrides is not None:
            environment.update(environment_overrides)
        return subprocess.run(
            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_version(self):
        completed = self.run_cli("--version")
        self.assertEqual(completed.stdout.strip(), "tritrack 0.1.0a0")

    def test_version_and_component_list(self):
        completed = self.run_cli("components", "--json")
        payload = json.loads(completed.stdout)

        self.assertEqual(payload["schemaVersion"], "tritrack.components/v1")
        self.assertEqual(len(payload["components"]), 11)
        self.assertEqual(
            [component["sourceComponent"] for component in payload["components"]],
            [
                "sync_scan.py",
                "emit_fcpxml.py",
                "transcribe_takes.py",
                "string_out.py",
                "hallucination.py",
                "organizer.py",
                "paper_edit.py",
                "align_text.py",
                "gemini_hybrid.py",
                "gemini_transcribe.mjs",
                "multicam-sync",
            ],
        )
        self.assertEqual(
            {
                component["sourceComponent"]: component["status"]
                for component in payload["components"]
            },
            {
                "sync_scan.py": "implemented",
                "emit_fcpxml.py": "implemented",
                "transcribe_takes.py": "implemented",
                "string_out.py": "implemented",
                "hallucination.py": "implemented",
                "organizer.py": "implemented",
                "paper_edit.py": "implemented",
                "align_text.py": "implemented",
                "gemini_hybrid.py": "implemented",
                "gemini_transcribe.mjs": "planned",
                "multicam-sync": "implemented",
            },
        )

    def test_help_exposes_the_complete_scaffold(self):
        completed = self.run_cli("--help")
        for command in (
            "components",
            "doctor",
            "sync",
            "transcribe",
            "align",
            "hybrid",
            "emit",
            "validate",
            "organize",
            "paper",
            "run",
        ):
            self.assertIn(command, completed.stdout)

    def test_sync_help_exposes_only_the_public_task_5_boundary(self):
        completed = self.run_cli("sync", "--help")
        for option in ("--camera-a", "--camera-b", "--profile", "--output"):
            self.assertIn(option, completed.stdout)

    def test_emit_help_exposes_only_the_public_task_6_boundary(self):
        completed = self.run_cli("emit", "--help")
        for option in (
            "--camera-a",
            "--camera-b",
            "--sync-map",
            "--profile",
            "--binding",
            "--event-name",
            "--project-name",
            "--output",
        ):
            self.assertIn(option, completed.stdout)

    def test_transcribe_help_exposes_only_the_local_task_7_boundary(self):
        completed = self.run_cli("transcribe", "--help")
        for option in ("--media", "--model", "--language", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "prompt", "fallback"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_align_help_exposes_only_the_local_cue_addressed_boundary(self):
        completed = self.run_cli("align", "--help")
        for option in ("--transcript", "--revision", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "prompt", "model", "retime"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_run_help_exposes_exact_immutable_local_transitions(self):
        run = self.run_cli("run", "--help")
        for command in ("prepare", "align", "finish", "status"):
            self.assertIn(command, run.stdout)

        prepare = self.run_cli("run", "prepare", "--help")
        for option in (
            "--camera-a",
            "--camera-b",
            "--transcribe-media",
            "--model",
            "--language",
            "--profile",
            "--binding",
            "--event-name",
            "--project-name",
            "--run-id",
            "--output",
            "--json",
        ):
            self.assertIn(option, prepare.stdout)

        align = self.run_cli("run", "align", "--help")
        for option in ("--prepared", "--revision", "--output", "--json"):
            self.assertIn(option, align.stdout)

        finish = self.run_cli("run", "finish", "--help")
        for option in (
            "--prepared",
            "--aligned",
            "--workbook",
            "--camera-a",
            "--camera-b",
            "--event-name",
            "--project-name",
            "--output",
            "--json",
        ):
            self.assertIn(option, finish.stdout)

        status = self.run_cli("run", "status", "--help")
        for option in ("--run", "--json"):
            self.assertIn(option, status.stdout)
        for completed in (run, prepare, align, finish, status):
            for excluded in (
                "provider",
                "upload",
                "credential",
                "overwrite",
                "resume",
                "release",
            ):
                self.assertNotIn(excluded, completed.stdout.lower())

    def test_run_handlers_forward_only_public_inputs_and_print_summary(self):
        summary = {
            "schemaVersion": "tritrack.run-summary/v1",
            "runId": "run-001",
            "phase": "prepared",
            "nextAction": "provide-revision",
            "stages": ["doctor", "sync", "transcribe", "emit"],
            "artifacts": {"syncMap": "a" * 64},
        }
        standard_output = io.StringIO()
        with (
            mock.patch.object(
                run_workflow, "prepare_run", return_value=summary
            ) as prepare,
            contextlib.redirect_stdout(standard_output),
        ):
            returncode = cli.main(
                [
                    "run",
                    "prepare",
                    "--camera-a",
                    "A-001.MP4",
                    "--camera-b",
                    "B-001.MP4",
                    "--transcribe-media",
                    "A-001.MP4",
                    "--model",
                    "model.bin",
                    "--language",
                    "en",
                    "--profile",
                    "uhd-2997-ndf-fcpxml-1.14",
                    "--binding",
                    "basic-title-v1",
                    "--event-name",
                    "Interview",
                    "--project-name",
                    "String-out",
                    "--run-id",
                    "run-001",
                    "--output",
                    "prepared-run",
                    "--json",
                ]
            )
        self.assertEqual(returncode, 0)
        self.assertEqual(json.loads(standard_output.getvalue()), summary)
        positional = prepare.call_args.args
        self.assertEqual(positional[0][0].media_id, "A-001.MP4")
        self.assertEqual(positional[1][0].media_id, "B-001.MP4")
        self.assertEqual(positional[2], [Path("A-001.MP4")])
        self.assertEqual(prepare.call_args.kwargs["run_id"], "run-001")

    def test_run_status_and_failure_codes_are_sanitized(self):
        summary = {
            "schemaVersion": "tritrack.run-summary/v1",
            "runId": "run-001",
            "phase": "finished",
            "nextAction": "complete",
            "stages": ["paper", "organize", "emit"],
            "artifacts": {"storyCut": "a" * 64},
        }
        standard_output = io.StringIO()
        with (
            mock.patch.object(run_workflow, "status_run", return_value=summary),
            contextlib.redirect_stdout(standard_output),
        ):
            returncode = cli.main(["run", "status", "--run", "finished", "--json"])
        self.assertEqual(returncode, 0)
        self.assertEqual(json.loads(standard_output.getvalue()), summary)

        cases = {
            "TRITRACK_OUTPUT_EXISTS": 73,
            "TRITRACK_OUTPUT_PARENT_MISSING": 74,
            "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED": 78,
            "TRITRACK_TRANSCRIBE_ENGINE_FAILED": 69,
            "TRITRACK_RUN_BUNDLE_INCOMPLETE": 65,
        }
        for code, expected in cases.items():
            standard_output = io.StringIO()
            with (
                self.subTest(code=code),
                mock.patch.object(
                    run_workflow, "status_run", side_effect=ValueError(code)
                ),
                contextlib.redirect_stdout(standard_output),
            ):
                returncode = cli.main(
                    ["run", "status", "--run", "invented", "--json"]
                )
            self.assertEqual(returncode, expected)
            self.assertEqual(json.loads(standard_output.getvalue()), {"error": code})
            self.assertNotIn("Traceback", standard_output.getvalue())

    def test_align_cli_publishes_and_prints_only_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision = write_alignment_inputs(root)
            output = root / "aligned.json"

            completed = self.run_cli_unchecked(
                "align",
                "--transcript",
                str(transcript),
                "--revision",
                str(revision),
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.align-summary/v1",
                    "takeCount": 1,
                    "cueCount": 1,
                    "revisedCueCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private", encoded_summary)

    def test_align_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "aligned.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "align",
                "--transcript",
                str(root / "missing-transcript.json"),
                "--revision",
                str(root / "missing-revision.json"),
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_organize_help_exposes_only_the_local_cue_addressed_boundary(self):
        completed = self.run_cli("organize", "--help")
        for option in ("--aligned", "--grouping", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_organize_cli_publishes_only_a_sanitized_summary(self):
        from tests.task9_fixtures import invented_aligned, invented_grouping

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned = root / "aligned.json"
            grouping = root / "grouping.json"
            output = root / "working-cut.json"
            aligned.write_text(
                json.dumps(
                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
                )
                + "\n",
                encoding="utf-8",
            )
            grouping_payload = invented_grouping()
            grouping_payload["alignedTranscriptSha256"] = hashlib.sha256(
                aligned.read_bytes()
            ).hexdigest()
            grouping.write_text(
                json.dumps(
                    grouping_payload,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(aligned),
                "--grouping",
                str(grouping),
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.organize-summary/v1",
                    "questionCount": 2,
                    "segmentCount": 2,
                    "reserveCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded = json.dumps(summary)
            self.assertNotIn(str(root), encoded)
            self.assertNotIn("What changed", encoded)

    def test_organize_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "working-cut.json"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(root / "missing-aligned.json"),
                "--grouping",
                str(root / "missing-grouping.json"),
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_organize_maps_missing_input_to_io_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(root / "missing-aligned.json"),
                "--grouping",
                str(root / "missing-grouping.json"),
                "--output",
                str(root / "working-cut.json"),
            )
            self.assertEqual(completed.returncode, 74)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_ORGANIZER_INPUT_UNREADABLE"},
            )
            self.assertNotIn("Traceback", completed.stderr)

    def test_paper_help_exposes_exact_nested_local_commands(self):
        paper = self.run_cli("paper", "--help")
        self.assertIn("export", paper.stdout)
        self.assertIn("apply", paper.stdout)

        export = self.run_cli("paper", "export", "--help")
        for option in ("--aligned", "--grouping", "--output", "--json"):
            self.assertIn(option, export.stdout)
        self.assertNotIn("--workbook", export.stdout)

        apply = self.run_cli("paper", "apply", "--help")
        for option in ("--aligned", "--workbook", "--output", "--json"):
            self.assertIn(option, apply.stdout)
        self.assertNotIn("--grouping", apply.stdout)
        for completed in (paper, export, apply):
            for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
                self.assertNotIn(excluded, completed.stdout.lower())

    def test_paper_export_and_apply_print_only_sanitized_summaries(self):
        from openpyxl import load_workbook

        from tests.task9_fixtures import invented_aligned

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned = root / "aligned.json"
            workbook = root / "paper.xlsx"
            grouping = root / "grouping.json"
            aligned.write_text(
                json.dumps(
                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
                )
                + "\n",
                encoding="utf-8",
            )

            exported = self.run_cli_unchecked(
                "paper",
                "export",
                "--aligned",
                str(aligned),
                "--output",
                str(workbook),
                "--json",
            )
            self.assertEqual(exported.returncode, 0, exported.stderr)
            export_summary = json.loads(exported.stdout)
            self.assertEqual(
                export_summary,
                {
                    "schemaVersion": "tritrack.paper-export-summary/v1",
                    "cueCount": 4,
                    "questionCount": 0,
                    "selectionCount": 0,
                    "artifactSha256": hashlib.sha256(
                        workbook.read_bytes()
                    ).hexdigest(),
                },
            )

            editable = load_workbook(workbook, data_only=False)
            editable["Questions"].append(
                ["question-001", "  Invented   question?  ", 1]
            )
            editable["Selections"].append(
                [
                    "ANSWER",
                    "answer-001",
                    "question-001",
                    1,
                    "A.wav",
                    "cue-000001",
                    "cue-000001",
                    None,
                    None,
                ]
            )
            editable.save(workbook)

            applied = self.run_cli_unchecked(
                "paper",
                "apply",
                "--aligned",
                str(aligned),
                "--workbook",
                str(workbook),
                "--output",
                str(grouping),
                "--json",
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            apply_summary = json.loads(applied.stdout)
            self.assertEqual(
                apply_summary,
                {
                    "schemaVersion": "tritrack.paper-apply-summary/v1",
                    "questionCount": 1,
                    "answerCount": 1,
                    "reserveCount": 0,
                    "artifactSha256": hashlib.sha256(
                        grouping.read_bytes()
                    ).hexdigest(),
                },
            )
            summaries = json.dumps([export_summary, apply_summary])
            self.assertNotIn(str(root), summaries)
            self.assertNotIn("Invented question", summaries)

    def test_paper_cli_maps_output_and_input_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "paper.xlsx"
            output.write_text("winner", encoding="utf-8")
            exists = self.run_cli_unchecked(
                "paper",
                "export",
                "--aligned",
                str(root / "missing.json"),
                "--output",
                str(output),
            )
            self.assertEqual(exists.returncode, 73)
            self.assertEqual(
                json.loads(exists.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
            )

            missing = self.run_cli_unchecked(
                "paper",
                "apply",
                "--aligned",
                str(root / "missing.json"),
                "--workbook",
                str(root / "missing.xlsx"),
                "--output",
                str(root / "grouping.json"),
            )
            self.assertEqual(missing.returncode, 74)
            self.assertEqual(
                json.loads(missing.stdout),
                {"error": "TRITRACK_PAPER_INPUT_UNREADABLE"},
            )
            self.assertNotIn("Traceback", missing.stderr)

    def test_hybrid_help_exposes_only_offline_receipt_validation(self):
        completed = self.run_cli("hybrid", "--help")
        for option in (
            "--transcript",
            "--proposal",
            "--receipt",
            "--model",
            "--output",
            "--json",
        ):
            self.assertIn(option, completed.stdout)
        self.assertIn("offline", completed.stdout.lower())
        self.assertIn("no network", completed.stdout.lower())
        for excluded in ("api-key", "credential", "fallback", "upload-file"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_hybrid_cli_validates_receipt_and_prints_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision = write_alignment_inputs(root)
            receipt = write_hybrid_receipt(root, transcript)
            output = root / "hybrid.json"

            completed = self.run_cli_unchecked(
                "hybrid",
                "--transcript",
                str(transcript),
                "--proposal",
                str(revision),
                "--receipt",
                str(receipt),
                "--model",
                "gemini-invented-exact",
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.align-summary/v1",
                    "takeCount": 1,
                    "cueCount": 1,
                    "revisedCueCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private", encoded_summary)

    def test_hybrid_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "hybrid.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "hybrid",
                "--transcript",
                str(root / "missing-transcript.json"),
                "--proposal",
                str(root / "missing-revision.json"),
                "--receipt",
                str(root / "missing-receipt.json"),
                "--model",
                "gemini-invented-exact",
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_transcribe_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "transcript.json"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "transcribe",
                "--media",
                str(root / "missing.MP4"),
                "--model",
                str(root / "missing-model.bin"),
                "--language",
                "zh",
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_transcribe_cli_runs_local_tools_and_prints_only_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Invented.MP4"
            model = root / "model.bin"
            output = root / "transcript.json"
            media.write_bytes(b"invented-media")
            model.write_bytes(b"invented-model")

            ffmpeg = root / "ffmpeg"
            ffmpeg.write_text(
                "#!/usr/bin/env python3\n"
                + textwrap.dedent(
                    """
                    import sys
                    import wave

                    with wave.open(sys.argv[-1], "wb") as output:
                        output.setnchannels(1)
                        output.setsampwidth(2)
                        output.setframerate(16000)
                        output.writeframes(bytes([1, 0]) * 16000)
                    """
                ),
                encoding="utf-8",
            )
            ffmpeg.chmod(0o755)

            whisper = root / "whisper-cli"
            whisper.write_text(
                "#!/usr/bin/env python3\n"
                + textwrap.dedent(
                    """
                    import json
                    import sys

                    if "--version" in sys.argv:
                        print("whisper.cpp version: invented-cli")
                        raise SystemExit(0)
                    prefix = sys.argv[sys.argv.index("--output-file") + 1]
                    payload = {
                        "result": {"language": "zh"},
                        "transcription": [
                            {
                                "offsets": {"from": 0, "to": 500},
                                "text": "Invented private transcript text.",
                            }
                        ],
                    }
                    with open(prefix + ".json", "w", encoding="utf-8") as handle:
                        json.dump(payload, handle)
                    """
                ),
                encoding="utf-8",
            )
            whisper.chmod(0o755)
            path = str(root) + os.pathsep + os.environ.get("PATH", "")

            completed = self.run_cli_unchecked(
                "transcribe",
                "--media",
                str(media),
                "--model",
                str(model),
                "--language",
                "zh",
                "--output",
                str(output),
                "--json",
                environment_overrides={"PATH": path},
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.transcribe-summary/v1",
                    "takeCount": 1,
                    "completedCount": 1,
                    "emptyCount": 0,
                    "bundleSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private transcript text", encoded_summary)

    def test_emit_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "string-out.fcpxml"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(root / "missing-sync-map.json"),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "Invented Event",
                "--project-name",
                "Invented String-out",
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_OUTPUT_EXISTS"},
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_emit_rejects_invalid_caller_metadata_at_the_cli_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(root / "missing-sync-map.json"),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "\n",
                "--project-name",
                "Invented String-out",
                "--output",
                str(root / "string-out.fcpxml"),
            )
            self.assertEqual(completed.returncode, 65)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_EMIT_METADATA_INVALID"},
            )
            self.assertEqual(completed.stderr, "")

    def test_emit_rejects_non_object_sync_map_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sync_map = root / "sync-map.json"
            sync_map.write_text("[]", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(sync_map),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "Invented Event",
                "--project-name",
                "Invented String-out",
                "--output",
                str(root / "string-out.fcpxml"),
            )

            self.assertEqual(completed.returncode, 65)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_EMIT_SYNC_MAP_INVALID"},
            )
            self.assertEqual(completed.stderr, "")

    def test_sync_rejects_existing_output_before_running_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a = root / "A-001.MP4"
            camera_b = root / "B-001.MP4"
            camera_a.write_bytes(b"invented-a")
            camera_b.write_bytes(b"invented-b")
            output = root / "sync-map.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "sync",
                "--camera-a",
                str(camera_a),
                "--camera-b",
                str(camera_b),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_OUTPUT_EXISTS"},
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")


class ValidateCliTest(unittest.TestCase):
    def run_cli_unchecked(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=environment,
        )

    def test_help_exposes_exact_four_read_only_modes(self) -> None:
        expected = {
            "contract": ("--artifact", "--json"),
            "fcpxml": ("--artifact", "--profile", "--binding", "--json"),
            "paper": ("--aligned", "--workbook", "--json"),
            "run": ("--run", "--json"),
        }
        parent = self.run_cli_unchecked("validate", "--help")
        self.assertEqual(parent.returncode, 0, parent.stderr)
        for mode in expected:
            self.assertIn(mode, parent.stdout)
        for mode, flags in expected.items():
            with self.subTest(mode=mode):
                completed = self.run_cli_unchecked("validate", mode, "--help")
                self.assertEqual(completed.returncode, 0, completed.stderr)
                for flag in flags:
                    self.assertIn(flag, completed.stdout)
                for forbidden in (
                    "output",
                    "repair",
                    "network",
                    "provider",
                    "credential",
                    "dtd",
                    "media-probe",
                ):
                    self.assertNotIn(forbidden, completed.stdout.lower())

    def test_contract_json_and_human_summaries_are_path_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "private-name.json"
            encoded = (
                json.dumps(
                    VALID_CONTRACTS["grouping-v1"],
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
            artifact.write_bytes(encoded)

            as_json = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(artifact), "--json"
            )
            human = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(artifact)
            )

            self.assertEqual(as_json.returncode, 0, as_json.stderr)
            summary = json.loads(as_json.stdout)
            self.assertEqual(summary["artifactKind"], "contract")
            self.assertEqual(summary["validationScope"], "contract")
            self.assertEqual(
                summary["hashes"]["artifact"],
                hashlib.sha256(encoded).hexdigest(),
            )
            self.assertEqual(human.returncode, 0, human.stderr)
            self.assertEqual(
                human.stdout.splitlines(),
                [
                    "VALIDATION\tcontract\tcontract",
                    f"HASH\tartifact\t{hashlib.sha256(encoded).hexdigest()}",
                    "DETAIL\tcontractName\t\"grouping-v1\"",
                    "DETAIL\tcontractSchemaVersion\t\"tritrack.grouping/v1\"",
                ],
            )
            for output in (as_json.stdout, human.stdout):
                self.assertNotIn(str(root), output)
                self.assertNotIn("What changed?", output)

    def test_dispatches_fcpxml_paper_and_run_with_exact_arguments(self) -> None:
        base_summary = {
            "schemaVersion": "tritrack.validate-summary/v1",
            "toolVersion": "0.1.0a0",
            "artifactKind": "invented",
            "validationScope": "invented-scope",
            "hashes": {},
            "counts": {},
            "details": {},
        }
        with (
            mock.patch.object(
                cli.validate_module,
                "validate_fcpxml_artifact",
                return_value=base_summary,
            ) as fcpxml,
            mock.patch.object(
                cli.validate_module,
                "validate_paper_artifacts",
                return_value=base_summary,
            ) as paper,
            mock.patch.object(
                cli.validate_module,
                "validate_run_bundle",
                return_value=base_summary,
            ) as run,
        ):
            for arguments in (
                [
                    "validate",
                    "fcpxml",
                    "--artifact",
                    "story.fcpxml",
                    "--profile",
                    "profile-id",
                    "--binding",
                    "binding-id",
                    "--json",
                ],
                [
                    "validate",
                    "paper",
                    "--aligned",
                    "aligned.json",
                    "--workbook",
                    "paper.xlsx",
                    "--json",
                ],
                ["validate", "run", "--run", "finished-run", "--json"],
            ):
                with self.subTest(arguments=arguments):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(cli.main(arguments), 0)
                    self.assertEqual(json.loads(output.getvalue()), base_summary)

        fcpxml.assert_called_once_with(
            Path("story.fcpxml"),
            profile_id="profile-id",
            binding_id="binding-id",
        )
        paper.assert_called_once_with(Path("aligned.json"), Path("paper.xlsx"))
        run.assert_called_once_with(Path("finished-run"))

    def test_usage_data_io_and_policy_failures_are_stable_and_sanitized(self) -> None:
        usage = self.run_cli_unchecked("validate", "contract")
        self.assertEqual(usage.returncode, 64)
        self.assertEqual(json.loads(usage.stdout), {"error": "TRITRACK_USAGE"})
        self.assertEqual(usage.stderr, "")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            malformed = root / "private-name.json"
            malformed.write_text("{private text", encoding="utf-8")
            data = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(malformed)
            )
            missing = self.run_cli_unchecked(
                "validate",
                "contract",
                "--artifact",
                str(root / "missing.json"),
            )
            missing_run = self.run_cli_unchecked(
                "validate",
                "run",
                "--run",
                str(root / "missing-run"),
            )
            xml = root / "story.fcpxml"
            xml.write_text("invented", encoding="utf-8")
            policy = self.run_cli_unchecked(
                "validate",
                "fcpxml",
                "--artifact",
                str(xml),
                "--profile",
                "unknown-profile",
                "--binding",
                "basic-title-v1",
            )

            self.assertEqual(data.returncode, 65)
            self.assertEqual(
                json.loads(data.stdout), {"error": "TRITRACK_VALIDATE_JSON_INVALID"}
            )
            self.assertEqual(missing.returncode, 74)
            self.assertEqual(
                json.loads(missing.stdout),
                {"error": "TRITRACK_VALIDATE_INPUT_UNREADABLE"},
            )
            self.assertEqual(missing_run.returncode, 74)
            self.assertEqual(
                json.loads(missing_run.stdout),
                {"error": "TRITRACK_RUN_INPUT_UNREADABLE"},
            )
            self.assertEqual(policy.returncode, 78)
            self.assertEqual(
                json.loads(policy.stdout), {"error": "TRITRACK_PROFILE_UNKNOWN"}
            )
            for completed in (data, missing, missing_run, policy):
                self.assertEqual(completed.stderr, "")
                self.assertNotIn(str(root), completed.stdout)
                self.assertNotIn("private text", completed.stdout)
                self.assertNotIn("Traceback", completed.stdout)

    def test_validate_does_not_change_component_registry(self) -> None:
        self.assertEqual(len(cli.COMPONENTS), 11)
        self.assertFalse(
            any(component["command"] == "validate" for component in cli.COMPONENTS)
        )


class ValidateDocumentationTest(unittest.TestCase):
    def test_public_docs_name_all_help_authorities_and_scope_boundaries(self) -> None:
        paths = (
            ROOT / "README.md",
            ROOT / "docs" / "TOOLING.md",
            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md",
        )
        commands = (
            "tritrack validate --help",
            "tritrack validate contract --help",
            "tritrack validate fcpxml --help",
            "tritrack validate paper --help",
            "tritrack validate run --help",
        )
        scopes = (
            "contract",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for command in commands:
                    self.assertIn(command, text)
                for scope in scopes:
                    self.assertIn(scope, text)
                self.assertIn("read-only", text)
                self.assertIn("does not repair", text)
                self.assertIn("source media", text)
                self.assertIn("DTD", text)
                self.assertIn("GUI", text)

    def test_release_gate_is_maintainer_only_and_python_support_is_exact(self) -> None:
        release_command = (
            "python scripts/release_gate.py --source . --output ABSENT_DIRECTORY"
        )
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        maintainer = (
            ROOT
            / ".agents"
            / "skills"
            / "tritrack-editing-assistant-maintainer"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        end_user = (
            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md"
        ).read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(release_command, tooling)
        self.assertIn(release_command, maintainer)
        for text in (readme, end_user):
            self.assertNotIn(release_command, text)
        self.assertNotIn("release", end_user.casefold())
        self.assertNotIn(".py", end_user.casefold())

        for relative in ("README.md", "docs/TOOLING.md", "CONTRIBUTING.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("Python 3.12 and 3.13", text, relative)
            self.assertNotIn("Python 3.12 or newer", text, relative)


if __name__ == "__main__":
    unittest.main()
