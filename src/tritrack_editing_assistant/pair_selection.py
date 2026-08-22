"""Select drift-supported temporal relay sources by genuinely new coverage."""

from __future__ import annotations

import statistics
from collections.abc import Mapping, Sequence
from typing import Any

MIN_OVERLAP_SECONDS = 3.0
MIN_PEAK_RATIO = 6.0
MIN_DRIFT_SAMPLES = 5
MAX_DRIFT_SPREAD_SECONDS = 5.0
MIN_DRIFT_TOLERANCE_SECONDS = 2.0
MAX_DRIFT_TOLERANCE_SECONDS = 10.0
MIN_EXTRA_COVERAGE_SECONDS = 10.0

Measurement = Mapping[str, Any]
DriftPrior = tuple[float, float]


def drift_prior(drifts: Sequence[float]) -> DriftPrior | None:
    """Return a bounded constant-clock prior only from coherent evidence."""

    if len(drifts) < MIN_DRIFT_SAMPLES:
        return None
    centre = float(statistics.median(drifts))
    spread = float(statistics.pstdev(drifts))
    if spread > MAX_DRIFT_SPREAD_SECONDS:
        return None
    tolerance = min(
        MAX_DRIFT_TOLERANCE_SECONDS,
        max(MIN_DRIFT_TOLERANCE_SECONDS, 4.0 * spread),
    )
    return centre, tolerance


def coverage(
    take_duration: float, offset: float, source_duration: float
) -> tuple[float, float] | None:
    """Clip one source span to its anchor take."""

    start = max(0.0, offset)
    end = min(take_duration, offset + source_duration)
    return (start, end) if end > start else None


def new_coverage_seconds(
    take_duration: float,
    held: Sequence[tuple[float, float]],
    offset: float,
    source_duration: float,
) -> float:
    """Measure source coverage not already represented by held spans."""

    source_span = coverage(take_duration, offset, source_duration)
    if source_span is None:
        return 0.0
    remaining = [source_span]
    for held_start, held_end in held:
        next_remaining: list[tuple[float, float]] = []
        for start, end in remaining:
            if held_end <= start or held_start >= end:
                next_remaining.append((start, end))
                continue
            if start < held_start:
                next_remaining.append((start, held_start))
            if held_end < end:
                next_remaining.append((held_end, end))
        remaining = next_remaining
    return sum(end - start for start, end in remaining)


def accept(measurement: Measurement, prior: DriftPrior | None) -> str | None:
    """Accept by measured correlation first, then by a coherent drift prior."""

    if float(measurement["overlap"]) < MIN_OVERLAP_SECONDS:
        return None
    if float(measurement["ratio"]) >= MIN_PEAK_RATIO:
        return "correlation"
    drift = measurement.get("drift")
    if prior is None or drift is None:
        return None
    centre, tolerance = prior
    if abs(float(drift) - centre) <= tolerance:
        return "drift-prior"
    return None


def select_pairs(
    measurements: Sequence[Measurement], *, prior: DriftPrior | None = None
) -> dict[str, dict[str, object]]:
    """Choose one primary source per take and temporal relay extras."""

    accepted: dict[str, list[dict[str, object]]] = {}
    for measurement in measurements:
        match = accept(measurement, prior)
        if match is None:
            continue
        take = str(measurement["take"])
        accepted.setdefault(take, []).append({**measurement, "match": match})

    chosen: dict[str, dict[str, object]] = {}
    for take, candidates in accepted.items():
        candidates.sort(
            key=lambda item: (
                0 if item["match"] == "correlation" else 1,
                -float(item["ratio"]),
                str(item.get("source", "")),
            )
        )
        primary = candidates[0]
        held: list[tuple[float, float]] = []
        primary_span = coverage(
            float(primary["take_duration"]),
            float(primary["offset"]),
            float(primary["source_duration"]),
        )
        if primary_span is not None:
            held.append(primary_span)

        extra: list[dict[str, object]] = []
        for candidate in candidates[1:]:
            gained = new_coverage_seconds(
                float(candidate["take_duration"]),
                held,
                float(candidate["offset"]),
                float(candidate["source_duration"]),
            )
            if gained < MIN_EXTRA_COVERAGE_SECONDS:
                continue
            extra.append(candidate)
            candidate_span = coverage(
                float(candidate["take_duration"]),
                float(candidate["offset"]),
                float(candidate["source_duration"]),
            )
            if candidate_span is not None:
                held.append(candidate_span)
        chosen[take] = {"primary": primary, "extra": extra}
    return chosen


def audio_master(loudness_a: float, loudness_b: float, mode: str) -> str:
    """Return a forced rig, with loudness only as the explicit auto fallback."""

    if mode in {"A", "B"}:
        return mode
    return "A" if loudness_a >= loudness_b else "B"

