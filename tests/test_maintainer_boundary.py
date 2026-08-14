"""Task 4.5 tests for the public-maintainer project boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    ROOT / ".agents" / "skills" / "tritrack-editing-assistant-maintainer"
)
VALIDATOR = SKILL_ROOT / "scripts" / "check_project_identity.py"
PUBLIC_GOVERNANCE = (
    ROOT / "AGENTS.md",
    ROOT / "STATUS.md",
    ROOT / "PRODUCT-WISHES.md",
    ROOT / "docs" / "ROADMAP.md",
    ROOT / "docs" / "TOOLING.md",
    SKILL_ROOT / "SKILL.md",
)


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


class MaintainerBoundaryTest(unittest.TestCase):
    def test_public_project_identity_is_accepted(self) -> None:
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "lane": "OSS",
                "ok": True,
                "projectId": "tritrack-editing-assistant",
                "projectKind": "public-engine",
            },
        )

    def test_missing_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run_validator(Path(temporary))
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISSING", result.stderr)

    def test_private_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".tritrack-project.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": "tritrack.project-identity/v1",
                        "projectId": "some-private-production",
                        "projectKind": "private-production",
                        "maintainerSkill": "some-private-skill",
                        "lane": "MAIN",
                    }
                ),
                encoding="utf-8",
            )
            result = run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISMATCH", result.stderr)

    def test_public_governance_is_self_contained_and_public_safe(self) -> None:
        forbidden = (
            "/" + "Users" + "/",
            "TriTrack-" + "worktrees",
            "TriTrack-" + "Subtitle-" + "Studio",
            "Codex for " + "Open Source",
            "six " + "months",
            "六" + "個月",
        )
        for path in PUBLIC_GOVERNANCE:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path}: leaked {token!r}")

    def test_maintainer_and_end_user_skills_are_distinct(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: tritrack-editing-assistant-maintainer", skill)
        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", skill)
        self.assertFalse((ROOT / "skills" / "tritrack-editing-assistant").exists())

    def test_public_status_advances_to_task_6(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("Tasks 1–5", status)
        self.assertIn("Task 6", status)
        self.assertIn("Task 6", roadmap)

    def test_tooling_pins_the_perpetual_final_cut_identity(self) -> None:
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        self.assertIn("/Applications/Final Cut Pro.app", tooling)
        self.assertIn("com.apple.FinalCut", tooling)
        self.assertIn("com.apple.FinalCutApp", tooling)
        self.assertIn("default file association", tooling)


if __name__ == "__main__":
    unittest.main()
