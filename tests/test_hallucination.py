"""Task 7 tests for deterministic structural transcript guards."""

from __future__ import annotations

import unittest

from tritrack_editing_assistant import hallucination


class HallucinationGuardTest(unittest.TestCase):
    def test_normalizes_unicode_and_whitespace_without_inventing_words(self) -> None:
        text = hallucination.normalize_cue_text("  Cafe\u0301\r\n  invented\twords  ")

        self.assertEqual(text, "Café invented words")

    def test_rejects_blank_control_characters_and_whisper_tokens(self) -> None:
        for value in (" \n\t", "safe\x00unsafe", "hello <|endoftext|>"):
            with self.subTest(value=repr(value)), self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_TEXT_INVALID"
            ):
                hallucination.normalize_cue_text(value)

    def test_rejects_three_adjacent_identical_normalized_cues(self) -> None:
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_REPETITION_DETECTED"
        ):
            hallucination.reject_repeated_cues(
                ["Invented phrase", " Invented  phrase ", "Invented phrase"]
            )

        hallucination.reject_repeated_cues(["One", "One", "Two", "One"])


if __name__ == "__main__":
    unittest.main()
