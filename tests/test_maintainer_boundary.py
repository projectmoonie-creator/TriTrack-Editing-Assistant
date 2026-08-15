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

    def test_public_status_records_task_9_and_schedules_task_10(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-9-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-9-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Tasks 1–9", status)
        self.assertIn("Task 6.5", status)
        self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
        self.assertLess(status.index("Task 7"), status.index("Task 8"))
        self.assertLess(status.index("Task 8"), status.index("Task 9"))
        self.assertLess(status.index("Task 9"), status.index("Task 10"))
        self.assertIn("Task 9", roadmap)
        self.assertLess(roadmap.index("Task 9"), roadmap.index("Task 10"))
        for authority in (
            "tritrack paper export --help",
            "tritrack paper apply --help",
            "tritrack organize --help",
        ):
            self.assertIn(authority, tooling)
        for text in (status, roadmap, tooling, readme, verification):
            self.assertIn("Task 9", text)
        self.assertIn("exactly four worksheets", decision)
        self.assertIn("Grouping fixpoint", verification)
        self.assertIn("no network", verification)
        self.assertIn("Task 10", status)
        self.assertIn("Task 10", roadmap)

    def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
        handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 6.5",
            handoff,
        )
        self.assertIn("242e8b5406e92049ce60c654c3c8fca11be4b596", handoff)
        self.assertIn("codex/task6-5-public-demo-readiness", handoff)
        self.assertIn("RED", handoff)
        self.assertIn("GREEN", handoff)
        self.assertIn("application submission", handoff)
        self.assertNotIn("/" + "Users" + "/", handoff)

    def test_tooling_pins_the_perpetual_final_cut_identity(self) -> None:
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        self.assertIn("/Applications/Final Cut Pro.app", tooling)
        self.assertIn("com.apple.FinalCut", tooling)
        self.assertIn("com.apple.FinalCutApp", tooling)
        self.assertIn("default file association", tooling)

    def test_authorization_is_a_capability_scoped_standing_grant(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for text in (agents, skill):
            self.assertIn("capability-scoped standing grant", text)
            self.assertIn("same target, visibility, scope, and risk", text)
            self.assertIn("until the producer revokes it", text)
            self.assertIn("Do not request it again", text)
            self.assertNotIn("without explicit producer", text)

        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("standing-authorization model", roadmap)
        self.assertNotIn("Each requires an explicit producer-approved gate", roadmap)


if __name__ == "__main__":
    unittest.main()
