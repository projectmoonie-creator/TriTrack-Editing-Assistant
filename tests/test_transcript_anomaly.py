"""Task 14 RED tests for public transcript-anomaly behavior.

All examples are invented and describe only generic recognizer failure shapes.
"""

from __future__ import annotations

import unittest

try:
    from tritrack_editing_assistant import transcript_anomaly
except ImportError:
    transcript_anomaly = None


def cue(text: str, start_ms: int = 0, end_ms: int = 1000) -> dict[str, object]:
    return {"text": text, "start_ms": start_ms, "end_ms": end_ms}


class TranscriptAnomalyTest(unittest.TestCase):
    def policy(self):
        self.assertIsNotNone(
            transcript_anomaly,
            "public transcript_anomaly module is not implemented",
        )
        return transcript_anomaly

    def test_four_identical_tokens_are_stutter_but_three_are_speech(self) -> None:
        policy = self.policy()

        self.assertFalse(policy.has_in_cue_stutter("再試一次,再試一次,再試一次"))
        self.assertTrue(policy.has_in_cue_stutter("七,七,七,七"))

    def test_stutter_must_be_consecutive_and_delimited(self) -> None:
        policy = self.policy()

        self.assertFalse(policy.has_in_cue_stutter("a,b,a,b,a,b,a,b"))
        self.assertFalse(policy.has_in_cue_stutter("好好好好好"))
        self.assertTrue(policy.has_in_cue_stutter(" Loop. loop,LOOP;loop "))

    def test_single_collapsed_loop_is_invalid(self) -> None:
        policy = self.policy()
        cues = [cue("嗯,嗯,嗯,嗯,嗯,接著說", 0, 35_800)]

        flags = policy.find_anomalies(cues)
        verdict = policy.transcript_verdict(cues, flags)

        self.assertEqual([flag.reason for flag in flags], ["stutter"])
        self.assertTrue(verdict.invalid)

    def test_cue_local_reason_outranks_repeat_run(self) -> None:
        policy = self.policy()
        cues = [cue("Go,go,go,go", index * 1000, (index + 1) * 1000) for index in range(3)]

        flags = policy.find_anomalies(cues)

        self.assertEqual([flag.reason for flag in flags], ["stutter"] * 3)

    def test_blank_cues_never_repeat(self) -> None:
        policy = self.policy()

        self.assertEqual(policy.find_anomalies([cue(""), cue("  "), cue("、")]), [])

    def test_three_normalized_cues_form_a_repeat_run_but_two_do_not(self) -> None:
        policy = self.policy()
        twice = [cue("同一句"), cue("同一句。")]
        thrice = [*twice, cue("同一句,")]

        self.assertEqual(policy.find_anomalies(twice), [])
        self.assertEqual(
            [flag.reason for flag in policy.find_anomalies(thrice)],
            ["repeat_run"] * 3,
        )

    def test_nearby_ranges_merge_and_keep_only_three_samples(self) -> None:
        policy = self.policy()
        flags = [
            policy.CueFlag(index, index * 1000, index * 1000 + 500, f"sample-{index}", "stutter")
            for index in range(4)
        ]

        ranges = policy.merge_anomaly_ranges(flags)

        self.assertEqual(len(ranges), 1)
        self.assertEqual(ranges[0].end_ms, 3500)
        self.assertEqual(ranges[0].reasons, ("stutter",))
        self.assertEqual(len(ranges[0].samples), 3)

    def test_empty_transcript_has_valid_verdict(self) -> None:
        verdict = self.policy().transcript_verdict([], [])

        self.assertEqual((verdict.cues, verdict.flagged, verdict.invalid), (0, 0, False))


if __name__ == "__main__":
    unittest.main()

