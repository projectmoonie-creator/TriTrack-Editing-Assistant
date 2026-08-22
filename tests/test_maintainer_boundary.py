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
        maintainer = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        end_user_root = ROOT / "skills" / "tritrack-editing-assistant"
        end_user = (end_user_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (end_user_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: tritrack-editing-assistant-maintainer", maintainer)
        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", maintainer)
        self.assertIn("name: tritrack-editing-assistant\n", end_user)
        self.assertIn("$tritrack-editing-assistant", metadata)
        self.assertIn('display_name: "TriTrack Editing Assistant"', metadata)

        for command in (
            "tritrack run --help",
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
            "tritrack validate --help",
            "tritrack validate contract --help",
            "tritrack validate fcpxml --help",
            "tritrack validate paper --help",
            "tritrack validate run --help",
        ):
            self.assertIn(command, end_user)
        for required in (
            "text-revision human gate",
            "paper-edit human gate",
            "takes: []",
            "Questions",
            "Selections",
            "transport, not authority",
            "absent output directory",
            "Keep media",
            "strict aligned transcript",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(required, end_user)

        lowered = end_user.lower()
        forbidden = (
            "tritrack-editing-assistant-maintainer",
            "task 10",
            "standing grant",
            "branch",
            "release",
            "tester",
            "moonie",
            "subtitle studio",
            "/" + "users" + "/",
            "api_key",
            "credential",
            "provider",
            "upload",
            "run_workflow",
            ".py",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)

    def test_public_status_records_tasks_1_through_14(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-10-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-10-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_11_verification = (ROOT / "docs" / "TASK-11-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_12_verification = (ROOT / "docs" / "TASK-12-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_14_decision = (ROOT / "docs" / "TASK-14-DECISION.md").read_text(
            encoding="utf-8"
        )
        task_14_closeout = (
            ROOT / "docs" / "reviews" / "task-14-closeout-2026-08-22.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Tasks 1–14", status)
        self.assertIn("Task 6.5", status)
        self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
        self.assertLess(status.index("Task 7"), status.index("Task 8"))
        self.assertLess(status.index("Task 8"), status.index("Task 9"))
        self.assertLess(status.index("Task 9"), status.index("Task 10"))
        self.assertLess(status.index("Task 10"), status.index("Task 11"))
        self.assertLess(status.index("Task 11"), status.index("Task 12"))
        self.assertLess(status.index("Task 12"), status.index("Task 13"))
        self.assertLess(status.index("Task 13"), status.index("Task 14"))
        self.assertIn("Task 10", roadmap)
        self.assertLess(roadmap.index("Task 10"), roadmap.index("Task 11"))
        for authority in (
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
        ):
            self.assertIn(authority, tooling)
        for text in (status, roadmap, tooling, readme, verification):
            self.assertIn("Task 10", text)
        self.assertIn("Selected option: A", decision)
        self.assertIn("immutable", verification)
        self.assertIn("story-cut.fcpxml", verification)
        self.assertIn("tritrack-editing-assistant", verification)
        self.assertIn("no network", verification)
        self.assertIn("Task 11", status)
        self.assertIn("Task 11", roadmap)
        self.assertIn("Task 12", status)
        self.assertIn("Task 12", roadmap)
        self.assertIn("Task 13", status)
        self.assertIn("Task 13", roadmap)
        self.assertIn("Task 14", status)
        self.assertIn("Task 14", roadmap)
        self.assertIn("Voice-activity detection remains **off by default**", task_14_decision)
        self.assertIn("299 tests", task_14_closeout)
        self.assertIn("semantic cross-binding", task_14_closeout)
        self.assertIn("claude-timeout", task_14_closeout)
        self.assertIn("advisory", task_14_closeout)
        self.assertIn(
            "d952c1fe41563c38c7859250b3f95b3d93e8929f",
            task_14_closeout,
        )
        self.assertNotIn("Commit the sanitized Task 13 review evidence", status)
        self.assertIn("alphaReviewTarget", task_12_verification)
        self.assertIn("alphaEvidenceRecord", task_12_verification)
        self.assertIn("ce562e995b63f3f1a29989de3e1ef202da27b5f2", task_11_verification)
        for scope in (
            "contract",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(scope, task_11_verification)
        self.assertNotIn("`validate` and `run` remain planned", status)
        self.assertNotIn("`validate` remains planned", status)
        self.assertNotIn("`tritrack run` | planned", readme)

    def test_task_13_documents_generic_authority_and_downstream_seam(
        self,
    ) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-13-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-13-VERIFICATION.md").read_text(
            encoding="utf-8"
        )

        for text in (status, roadmap, tooling, readme, decision, verification):
            self.assertIn("Task 13", text)
        self.assertIn("Selected option: A", decision)
        self.assertIn(
            "exclusive supported downstream integration seam for v1",
            decision,
        )
        self.assertIn(
            "Internal Python modules and functions are implementation details",
            decision,
        )
        self.assertIn("never an engine contract", decision)
        for text in (status, tooling, readme, verification):
            self.assertIn("downstreamSeam", text)
            self.assertIn("wheel-only", text)
        for text in (status, roadmap, readme, verification):
            normalized = " ".join(text.split())
            self.assertIn("no tag", normalized)
            self.assertIn("no package publication", normalized)
            self.assertIn("no private integration", normalized)
        self.assertIn("examples/downstream_seam.py", tooling)
        self.assertIn("tritrack validate contract", tooling)

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

    def test_working_cut_claims_distinguish_transcript_from_editor_text(self) -> None:
        for path in (
            ROOT / "README.md",
            ROOT / "docs" / "TASK-9-VERIFICATION.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertIn("transcript-text-free", text, str(path))
            self.assertNotRegex(
                text,
                r"(?<!transcript-)text-free\s+(?:working cut|`working-cut)",
                str(path),
            )

        organizer = (
            ROOT / "src" / "tritrack_editing_assistant" / "organizer.py"
        ).read_text(encoding="utf-8")
        self.assertIn("transcript-text-free working cut", organizer)

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
