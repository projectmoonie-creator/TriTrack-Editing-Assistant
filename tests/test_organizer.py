from __future__ import annotations

import copy
import json
import unittest

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


if __name__ == "__main__":
    unittest.main()
