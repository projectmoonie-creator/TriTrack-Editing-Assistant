"""Invented regressions for sparse-source detection and source choice."""

from __future__ import annotations

import unittest

try:
    from tritrack_editing_assistant import sparse_source
except ImportError:
    sparse_source = None


def cue(text: str) -> dict[str, str]:
    return {"text": text}


def speech(seconds: int, per_second: int = 3) -> tuple[dict[str, str], ...]:
    total = seconds * per_second
    text = "".join(chr(0x4E00 + index % 200) for index in range(total))
    return tuple(cue(text[start : start + 10]) for start in range(0, total, 10))


class SparseSourcePolicyTest(unittest.TestCase):
    def policy(self):
        self.assertIsNotNone(sparse_source, "sparse-source policy is missing")
        return sparse_source

    def candidate(
        self,
        cues: tuple[dict[str, str], ...],
        duration_ms: int | None,
        *,
        invalid: bool = False,
    ):
        return self.policy().SourceCandidate(
            cues=cues,
            duration_ms=duration_ms,
            invalid=invalid,
        )

    def test_segmentation_cannot_change_content_count(self) -> None:
        policy = self.policy()
        self.assertEqual(
            policy.transcript_characters((cue("我們"), cue("在一起"))),
            policy.transcript_characters((cue("我們在一起"),)),
        )

    def test_punctuation_spacing_and_marks_are_not_content(self) -> None:
        policy = self.policy()
        self.assertEqual(policy.transcript_characters((cue("我 們，Cafe\u0301。"),)), 6)

    def test_letters_digits_and_symbols_are_content(self) -> None:
        self.assertEqual(
            self.policy().transcript_characters((cue("ab 12 +"),)),
            5,
        )

    def test_missing_and_empty_cues_are_tolerated(self) -> None:
        self.assertEqual(
            self.policy().transcript_characters(({}, {"text": ""}, None)),
            0,
        )

    def test_density_requires_a_positive_numeric_duration(self) -> None:
        policy = self.policy()
        for duration in (None, "60000", 0, -1, True, False):
            with self.subTest(duration=duration):
                self.assertIsNone(policy.characters_per_second((cue("x"),), duration))

    def test_density_uses_exact_milliseconds(self) -> None:
        self.assertEqual(
            self.policy().characters_per_second((cue("abcd"),), 2000),
            2.0,
        )

    def test_ordinary_speech_is_not_sparse(self) -> None:
        self.assertFalse(self.policy().is_sparse(speech(60), 60_000))

    def test_lost_microphone_is_sparse(self) -> None:
        self.assertTrue(
            self.policy().is_sparse((cue("對"), cue("嗯")), 300_000)
        )

    def test_short_media_is_never_judged(self) -> None:
        policy = self.policy()
        self.assertFalse(policy.is_sparse((cue("好"),), 10_000))
        self.assertFalse(policy.is_sparse((), 10_000))

    def test_minimum_duration_is_inclusive(self) -> None:
        policy = self.policy()
        self.assertFalse(policy.is_sparse((), 29_999))
        self.assertTrue(policy.is_sparse((), 30_000))

    def test_rate_boundary_is_strictly_below(self) -> None:
        self.assertFalse(
            self.policy().is_sparse((cue("x" * 60),), 60_000)
        )

    def test_unknown_duration_never_guesses(self) -> None:
        policy = self.policy()
        for duration in (None, "300000", 0, -5, True):
            with self.subTest(duration=duration):
                self.assertFalse(policy.is_sparse((), duration))

    def test_usable_primary_wins_without_retry(self) -> None:
        policy = self.policy()
        primary = self.candidate(speech(60), 60_000)
        alternative = self.candidate(speech(60), 60_000)
        self.assertFalse(policy.requires_retry(primary))
        self.assertEqual(
            policy.choose_source((primary, alternative)),
            policy.SourceChoice(index=0, reason="primary-usable"),
        )

    def test_sparse_primary_drives_retry_and_usable_alternative_wins(self) -> None:
        policy = self.policy()
        primary = self.candidate((cue("嗯"),), 120_000)
        alternative = self.candidate(speech(60), 60_000)
        self.assertTrue(policy.requires_retry(primary))
        self.assertEqual(
            policy.choose_source((primary, alternative)),
            policy.SourceChoice(index=1, reason="primary-sparse"),
        )

    def test_invalid_primary_drives_retry_and_usable_alternative_wins(self) -> None:
        policy = self.policy()
        primary = self.candidate(speech(60), 60_000, invalid=True)
        alternative = self.candidate(speech(60), 60_000)
        self.assertTrue(policy.requires_retry(primary))
        self.assertEqual(
            policy.choose_source((primary, alternative)),
            policy.SourceChoice(index=1, reason="primary-invalid"),
        )

    def test_sparse_primary_survives_when_nothing_is_better(self) -> None:
        policy = self.policy()
        primary = self.candidate((cue("嗯"),), 120_000)
        alternative = self.candidate((cue("對"),), 120_000)
        self.assertEqual(
            policy.choose_source((primary, alternative)),
            policy.SourceChoice(index=0, reason="no-better-source"),
        )

    def test_invalid_primary_never_survives(self) -> None:
        policy = self.policy()
        primary = self.candidate(speech(60), 60_000, invalid=True)
        self.assertEqual(
            policy.choose_source((primary,)),
            policy.SourceChoice(index=None, reason="invalid"),
        )

    def test_invalid_primary_accepts_sparse_alternative(self) -> None:
        policy = self.policy()
        primary = self.candidate(speech(60), 60_000, invalid=True)
        alternative = self.candidate((cue("嗯"),), 120_000)
        self.assertEqual(
            policy.choose_source((primary, alternative)),
            policy.SourceChoice(index=1, reason="primary-invalid"),
        )

    def test_invalid_alternative_never_survives(self) -> None:
        policy = self.policy()
        primary = self.candidate(speech(60), 60_000, invalid=True)
        alternative = self.candidate(speech(60), 60_000, invalid=True)
        self.assertIsNone(policy.choose_source((primary, alternative)).index)

    def test_empty_primary_yields_to_content_but_not_to_nothing(self) -> None:
        policy = self.policy()
        empty = self.candidate((), 120_000)
        usable = self.candidate(speech(60), 60_000)
        self.assertEqual(policy.choose_source((empty, usable)).index, 1)
        self.assertIsNone(policy.choose_source((empty, empty)).index)


if __name__ == "__main__":
    unittest.main()
