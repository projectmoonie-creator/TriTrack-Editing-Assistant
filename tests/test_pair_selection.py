"""Task 14 RED tests for drift-aware relay selection.

Measurements are invented and contain no production identifiers or timings.
"""

from __future__ import annotations

import unittest

try:
    from tritrack_editing_assistant import pair_selection
except ImportError:
    pair_selection = None


def measurement(
    source: str,
    *,
    ratio: float,
    offset: float,
    source_duration: float,
    **overrides: object,
) -> dict[str, object]:
    value: dict[str, object] = {
        "take": "anchor-001.mov",
        "source": source,
        "overlap": 30.0,
        "ratio": ratio,
        "offset": offset,
        "take_duration": 600.0,
        "source_duration": source_duration,
    }
    value.update(overrides)
    return value


class PairSelectionTest(unittest.TestCase):
    def policy(self):
        self.assertIsNotNone(
            pair_selection,
            "public pair_selection module is not implemented",
        )
        return pair_selection

    def test_prior_refuses_few_or_scattered_samples(self) -> None:
        policy = self.policy()

        self.assertIsNone(policy.drift_prior([8.0, 8.1, 7.9, 8.2]))
        self.assertIsNone(policy.drift_prior([-20.0, 0.0, 15.0, 33.0, 50.0]))

    def test_consistent_samples_create_a_bounded_prior(self) -> None:
        policy = self.policy()

        centre, tolerance = policy.drift_prior([8.0, 8.2, 7.9, 8.1, 8.0])

        self.assertAlmostEqual(centre, 8.0)
        self.assertGreaterEqual(tolerance, 2.0)
        self.assertLessEqual(tolerance, 10.0)

    def test_short_overlap_refuses_even_a_sharp_peak(self) -> None:
        candidate = measurement(
            "relay-a.mov",
            ratio=80.0,
            offset=0.0,
            source_duration=120.0,
            overlap=2.99,
        )

        self.assertIsNone(self.policy().accept(candidate, None))

    def test_correlation_beats_drift_prior(self) -> None:
        policy = self.policy()
        correlated = measurement(
            "measured.mov", ratio=6.5, offset=0.0, source_duration=600.0
        )
        prior_only = measurement(
            "prior.mov",
            ratio=2.0,
            offset=0.0,
            source_duration=600.0,
            drift=8.0,
        )

        chosen = policy.select_pairs([prior_only, correlated], prior=(8.0, 2.0))

        self.assertEqual(chosen["anchor-001.mov"]["primary"]["source"], "measured.mov")
        self.assertEqual(chosen["anchor-001.mov"]["primary"]["match"], "correlation")

    def test_relay_keeps_only_new_coverage(self) -> None:
        policy = self.policy()
        first = measurement(
            "relay-a.mov", ratio=8.0, offset=0.0, source_duration=300.0
        )
        second = measurement(
            "relay-b.mov", ratio=7.0, offset=300.0, source_duration=300.0
        )
        duplicate = measurement(
            "duplicate.mov", ratio=6.5, offset=0.0, source_duration=300.0
        )

        chosen = policy.select_pairs([first, second, duplicate])

        self.assertEqual(chosen["anchor-001.mov"]["primary"]["source"], "relay-a.mov")
        self.assertEqual(
            [item["source"] for item in chosen["anchor-001.mov"]["extra"]],
            ["relay-b.mov"],
        )

    def test_forced_audio_master_ignores_loudness(self) -> None:
        policy = self.policy()

        self.assertEqual(policy.audio_master(0.99, 0.01, "B"), "B")
        self.assertEqual(policy.audio_master(0.01, 0.99, "A"), "A")


if __name__ == "__main__":
    unittest.main()

