import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliSmokeTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        completed = self.run_cli_unchecked(*args)
        completed.check_returncode()
        return completed

    def run_cli_unchecked(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
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
                "transcribe_takes.py": "planned",
                "string_out.py": "implemented",
                "hallucination.py": "planned",
                "organizer.py": "planned",
                "paper_edit.py": "planned",
                "align_text.py": "planned",
                "gemini_hybrid.py": "planned",
                "gemini_transcribe.mjs": "planned",
                "multicam-sync": "planned",
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


if __name__ == "__main__":
    unittest.main()
