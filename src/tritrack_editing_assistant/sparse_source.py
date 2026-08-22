"""Pure sparse-source verdict and source-choice policy."""

from __future__ import annotations

import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction

SPARSE_CHARACTERS_PER_SECOND = 1.0
SPARSE_MINIMUM_DURATION_MS = 30_000


@dataclass(frozen=True)
class SourceCandidate:
    """One decoded source, without paths or engine state."""

    cues: Sequence[Mapping[str, object] | None]
    duration_ms: float | Fraction | None
    invalid: bool = False


@dataclass(frozen=True)
class SourceChoice:
    """The candidate index a consumer reads and the policy reason."""

    index: int | None
    reason: str


def transcript_characters(
    cues: Sequence[Mapping[str, object] | None] | None,
) -> int:
    """Count spoken-content characters independent of formatting and cues."""

    total = 0
    for cue in cues or ():
        text = "" if cue is None else cue.get("text") or ""
        if not isinstance(text, str):
            raise TypeError("TRITRACK_TRANSCRIPT_CONTENT_INVALID")
        for character in text:
            if unicodedata.category(character)[0] in {"L", "N", "S"}:
                total += 1
    return total


def characters_per_second(
    cues: Sequence[Mapping[str, object] | None] | None,
    duration_ms: float | Fraction | None,
) -> float | Fraction | None:
    """Return content density when duration is usable."""

    if (
        isinstance(duration_ms, bool)
        or not isinstance(duration_ms, (int, float, Fraction))
        or duration_ms <= 0
    ):
        return None
    return transcript_characters(cues) * 1000 / duration_ms


def is_sparse(
    cues: Sequence[Mapping[str, object] | None] | None,
    duration_ms: float | Fraction | None,
) -> bool:
    """Return whether a long source retained too little spoken content."""

    if (
        isinstance(duration_ms, bool)
        or not isinstance(duration_ms, (int, float, Fraction))
        or duration_ms < SPARSE_MINIMUM_DURATION_MS
    ):
        return False
    measured = characters_per_second(cues, duration_ms)
    return measured is not None and measured < SPARSE_CHARACTERS_PER_SECOND


def source_problem(candidate: SourceCandidate) -> str | None:
    """Classify only the problems that change retry or adoption."""

    if candidate.invalid:
        return "invalid"
    if not candidate.cues:
        return "empty"
    if is_sparse(candidate.cues, candidate.duration_ms):
        return "sparse"
    return None


def requires_retry(candidate: SourceCandidate) -> bool:
    """Return whether a different microphone must be tried when available."""

    return source_problem(candidate) is not None


def choose_source(candidates: Sequence[SourceCandidate]) -> SourceChoice:
    """Apply one choice ladder to primary then declared alternatives."""

    if not candidates:
        return SourceChoice(None, "empty")
    primary_problem = source_problem(candidates[0])
    if primary_problem is None:
        return SourceChoice(0, "primary-usable")

    for index, candidate in enumerate(candidates[1:], start=1):
        if source_problem(candidate) is None:
            return SourceChoice(index, f"primary-{primary_problem}")

    if primary_problem == "sparse":
        return SourceChoice(0, "no-better-source")

    for index, candidate in enumerate(candidates[1:], start=1):
        if source_problem(candidate) == "sparse":
            return SourceChoice(index, f"primary-{primary_problem}")

    return SourceChoice(None, primary_problem)
