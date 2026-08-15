from __future__ import annotations

import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.task9_fixtures import (
    ALIGNED_SHA256,
    GROUPING_SHA256,
    invented_aligned,
    invented_grouping,
)
from tritrack_editing_assistant import organizer
from tritrack_editing_assistant.contracts import validate_contract


class PureOrganizerTest(unittest.TestCase):
    def build(self, aligned=None, grouping=None):
        return organizer.build_working_cut(
            invented_aligned() if aligned is None else aligned,
            invented_grouping() if grouping is None else grouping,
            aligned_sha256=ALIGNED_SHA256,
            grouping_sha256=GROUPING_SHA256,
        )

    def test_builds_strict_immutable_text_free_working_cut(self) -> None:
        aligned = invented_aligned()
        grouping = invented_grouping()
        aligned_before = copy.deepcopy(aligned)
        grouping_before = copy.deepcopy(grouping)

        working_cut = self.build(aligned, grouping)

        validate_contract("working-cut-v1", working_cut)
        self.assertEqual(aligned, aligned_before)
        self.assertEqual(grouping, grouping_before)
        self.assertEqual(
            working_cut,
            {
                "schemaVersion": "tritrack.working-cut/v1",
                "organizationProfileId": "cue-addressed-question-groups-v1",
                "alignedTranscriptSha256": ALIGNED_SHA256,
                "groupingSha256": GROUPING_SHA256,
                "questions": [
                    {
                        "id": "question-001",
                        "question": "What changed?",
                        "order": 1,
                    },
                    {
                        "id": "question-002",
                        "question": "What comes next?",
                        "order": 2,
                    },
                ],
                "segments": [
                    {
                        "id": "answer-001",
                        "storyOrder": 1,
                        "questionId": "question-001",
                        "takeId": "A.wav",
                        "sourceSha256": "3" * 64,
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000002",
                        "startMs": 0,
                        "endMs": 1100,
                        "note": "Primary invented answer",
                    },
                    {
                        "id": "answer-002",
                        "storyOrder": 2,
                        "questionId": "question-002",
                        "takeId": "B.wav",
                        "sourceSha256": "4" * 64,
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000001",
                        "startMs": 100,
                        "endMs": 700,
                    },
                ],
                "reserve": [
                    {
                        "id": "reserve-001",
                        "order": 1,
                        "takeId": "B.wav",
                        "sourceSha256": "4" * 64,
                        "startCueId": "cue-000002",
                        "endCueId": "cue-000002",
                        "startMs": 900,
                        "endMs": 1400,
                        "reason": "Alternate invented answer",
                        "note": "Keep available",
                    }
                ],
            },
        )
        self.assertNotIn("Invented first answer", json.dumps(working_cut))

    def test_rejects_invalid_or_noncanonical_aligned_authority(self) -> None:
        duplicate_take = invented_aligned()
        duplicate_take["takes"].append(copy.deepcopy(duplicate_take["takes"][0]))
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
            self.build(duplicate_take)

        duplicate_cue = invented_aligned()
        duplicate_cue["takes"][0]["cues"].append(
            copy.deepcopy(duplicate_cue["takes"][0]["cues"][0])
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
            self.build(duplicate_cue)

        unsorted = invented_aligned()
        unsorted["takes"][0], unsorted["takes"][1] = (
            unsorted["takes"][1],
            unsorted["takes"][0],
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
            self.build(unsorted)

        invalid_timing = invented_aligned()
        invalid_timing["takes"][0]["cues"][1]["startMs"] = 400
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
            self.build(invalid_timing)

    def test_rejects_hash_order_id_and_text_drift(self) -> None:
        bad_hash = invented_grouping()
        bad_hash["alignedTranscriptSha256"] = "f" * 64
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH"
        ):
            self.build(grouping=bad_hash)

        gapped_order = invented_grouping()
        gapped_order["questions"][1]["order"] = 3
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ORDER_INVALID"):
            self.build(grouping=gapped_order)

        duplicate_id = invented_grouping()
        duplicate_id["questions"][1]["answers"][0]["id"] = "answer-001"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_DUPLICATE_ID"):
            self.build(grouping=duplicate_id)

        noncanonical_text = invented_grouping()
        noncanonical_text["questions"][0]["question"] = "  What   changed?  "
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ORGANIZER_TEXT_NONCANONICAL"
        ):
            self.build(grouping=noncanonical_text)

    def test_rejects_unknown_empty_reversed_and_reused_spans(self) -> None:
        unknown_take = invented_grouping()
        unknown_take["questions"][0]["answers"][0]["takeId"] = "Unknown.wav"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_TAKE_UNKNOWN"):
            self.build(grouping=unknown_take)

        empty_take = invented_grouping()
        empty_take["questions"][0]["answers"][0]["takeId"] = "C.wav"
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_ORGANIZER_TAKE_NOT_COMPLETED"
        ):
            self.build(grouping=empty_take)

        reversed_span = invented_grouping()
        selection = reversed_span["questions"][0]["answers"][0]
        selection["startCueId"], selection["endCueId"] = (
            selection["endCueId"],
            selection["startCueId"],
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_SPAN_INVALID"):
            self.build(grouping=reversed_span)

        unknown_cue = invented_grouping()
        unknown_cue["questions"][0]["answers"][0]["endCueId"] = "cue-999999"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_CUE_UNKNOWN"):
            self.build(grouping=unknown_cue)

        reused = invented_grouping()
        reused["reserve"][0]["takeId"] = "A.wav"
        reused["reserve"][0]["startCueId"] = "cue-000002"
        reused["reserve"][0]["endCueId"] = "cue-000002"
        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_CUE_REUSED"):
            self.build(grouping=reused)


class OrganizerFileBoundaryTest(unittest.TestCase):
    def write_inputs(self, root: Path) -> tuple[Path, Path, bytes, bytes]:
        aligned_path = root / "aligned.json"
        grouping_path = root / "grouping.json"
        aligned_bytes = (
            json.dumps(
                invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
            )
            + "\n"
        ).encode("utf-8")
        aligned_path.write_bytes(aligned_bytes)
        grouping = invented_grouping()
        grouping["alignedTranscriptSha256"] = hashlib.sha256(
            aligned_bytes
        ).hexdigest()
        grouping_bytes = organizer.encode_grouping(grouping)
        grouping_path.write_bytes(grouping_bytes)
        return aligned_path, grouping_path, aligned_bytes, grouping_bytes

    def test_publishes_deterministic_exact_bound_bytes_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, grouping, aligned_before, grouping_before = self.write_inputs(root)
            first = root / "first.json"
            second = root / "second.json"

            first_payload = organizer.organize_and_publish(
                aligned, grouping, output_path=first
            )
            second_payload = organizer.organize_and_publish(
                aligned, grouping, output_path=second
            )

            self.assertEqual(first_payload, second_payload)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(aligned.read_bytes(), aligned_before)
            self.assertEqual(grouping.read_bytes(), grouping_before)
            self.assertEqual(
                first_payload["alignedTranscriptSha256"],
                hashlib.sha256(aligned_before).hexdigest(),
            )
            self.assertEqual(
                first_payload["groupingSha256"],
                hashlib.sha256(grouping_before).hexdigest(),
            )

    def test_existing_output_and_missing_parent_fail_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "working-cut.json"
            output.write_text("winner", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                organizer.organize_and_publish(
                    root / "missing-aligned.json",
                    root / "missing-grouping.json",
                    output_path=output,
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "winner")

            aligned, grouping, _, _ = self.write_inputs(root)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
            ):
                organizer.organize_and_publish(
                    aligned,
                    grouping,
                    output_path=root / "missing" / "working-cut.json",
                )

    def test_rejects_noncanonical_malformed_symlink_and_oversized_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, grouping, _, _ = self.write_inputs(root)

            noncanonical = root / "noncanonical.json"
            noncanonical.write_text(
                json.dumps(json.loads(grouping.read_text(encoding="utf-8"))),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ORGANIZER_GROUPING_NONCANONICAL"
            ):
                organizer.organize_and_publish(
                    aligned, noncanonical, output_path=root / "noncanonical-out.json"
                )

            malformed = root / "malformed.json"
            malformed.write_bytes(b"\xff")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
            ):
                organizer.organize_and_publish(
                    aligned, malformed, output_path=root / "malformed-out.json"
                )

            symlink = root / "grouping-link.json"
            symlink.symlink_to(grouping)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
            ):
                organizer.organize_and_publish(
                    aligned, symlink, output_path=root / "symlink-out.json"
                )

            oversized = root / "oversized.json"
            with oversized.open("wb") as stream:
                stream.truncate(16 * 1024 * 1024 + 1)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
            ):
                organizer.organize_and_publish(
                    aligned, oversized, output_path=root / "oversized-out.json"
                )

    def test_detects_late_mutation_and_never_overwrites_race_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, grouping, _, _ = self.write_inputs(root)
            changed_output = root / "changed.json"
            original_verify = organizer._verify_artifact_unchanged

            def mutate_then_verify(artifact):
                if artifact.path == grouping:
                    grouping.write_bytes(grouping.read_bytes() + b" ")
                return original_verify(artifact)

            with (
                mock.patch.object(
                    organizer,
                    "_verify_artifact_unchanged",
                    side_effect=mutate_then_verify,
                ),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_ORGANIZER_INPUT_CHANGED"
                ),
            ):
                organizer.organize_and_publish(
                    aligned, grouping, output_path=changed_output
                )
            self.assertFalse(changed_output.exists())

            aligned, grouping, _, _ = self.write_inputs(root)
            race_output = root / "race.json"

            def race_winner(_source, destination):
                Path(destination).write_text("winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(os, "link", side_effect=race_winner),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                organizer.organize_and_publish(
                    aligned, grouping, output_path=race_output
                )
            self.assertEqual(race_output.read_text(encoding="utf-8"), "winner")
            self.assertEqual(list(root.glob(".race.json.*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
