"""Deterministic structural guards for local transcript evidence."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Sequence

_WHISPER_TOKEN = re.compile(r"<\|[^|]*\|>")
_ALLOWED_CONTROLS = frozenset({"\t", "\n", "\r"})
MAX_ADJACENT_IDENTICAL_CUES = 2
BLANK_AUDIO_SENTINEL = "[BLANK_AUDIO]"


def normalize_cue_text(value: object) -> str:
    """Return NFC, single-spaced cue text without engine control tokens."""

    if not isinstance(value, str):
        raise TypeError("TRITRACK_TRANSCRIPT_TEXT_INVALID")
    if any(
        unicodedata.category(character) == "Cc"
        and character not in _ALLOWED_CONTROLS
        for character in value
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_TEXT_INVALID")

    normalized = unicodedata.normalize("NFC", " ".join(value.split()))
    if not normalized or _WHISPER_TOKEN.search(normalized):
        raise ValueError("TRITRACK_TRANSCRIPT_TEXT_INVALID")
    return normalized


def reject_repeated_cues(values: Sequence[str]) -> None:
    """Reject only an exact normalized three-cue adjacent repetition run."""

    previous: str | None = None
    run_length = 0
    for value in values:
        normalized = normalize_cue_text(value)
        if normalized == previous:
            run_length += 1
        else:
            previous = normalized
            run_length = 1
        if run_length > MAX_ADJACENT_IDENTICAL_CUES:
            raise ValueError("TRITRACK_TRANSCRIPT_REPETITION_DETECTED")


def is_blank_audio_sentinel(value: str) -> bool:
    """Return true only for whisper.cpp's observed exact blank-audio marker."""

    return value == BLANK_AUDIO_SENTINEL
