import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CliSmokeTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=True,
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
            {component["status"] for component in payload["components"]}, {"planned"}
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


if __name__ == "__main__":
    unittest.main()
