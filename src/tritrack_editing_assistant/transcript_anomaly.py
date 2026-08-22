"""Detect recognizer artifacts without depending on transcription plumbing."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise

MIN_REPEAT_CUES = 3
MIN_STUTTER_TOKENS = 4
LONG_RANGE_MS = 60_000
INVALID_RATIO = 0.9

_DELIMITERS = re.compile(r"[\s,，。.!！?？:：;；、'\"「」『』()（）\-—~]+")
_BOILERPLATE = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"中文字幕",
        r"字幕(由|組|志[愿願]者|提供)",
        r"(感謝|感谢|謝謝|谢谢|多謝|多谢)(觀看|观看|收看|支持)",
        r"(歡迎|欢迎)(訂閱|订阅|收看|回來|回来)",
        r"(訂閱|订阅).{0,6}(頻道|频道)",
        r"(請|请)?(不吝)?(點贊|点赞|按讚|按赞)",
        r"(轉發|转发|打賞|打赏)",
        r"amara\.org",
        r"thank\s*you\s*(so\s*much\s*)?for\s*watching",
        r"(please\s+)?subscribe(\s+to)?(\s+my|\s+our)?(\s+channel)?",
        r"see\s+you\s+(in\s+the\s+)?next\s+(video|time)",
    )
)


@dataclass(frozen=True)
class CueFlag:
    """One cue-local anomaly finding."""

    index: int
    start_ms: int
    end_ms: int
    text: str
    reason: str


@dataclass(frozen=True)
class AnomalyRange:
    """Nearby anomaly findings merged into one review interval."""

    start_ms: int
    end_ms: int
    reasons: tuple[str, ...]
    samples: tuple[str, ...]
    long: bool


@dataclass(frozen=True)
class TranscriptVerdict:
    """Whole-transcript usability decision."""

    cues: int
    flagged: int
    invalid: bool


def _normalized_text(text: object) -> str:
    return _DELIMITERS.sub("", str(text)).casefold()


def has_in_cue_stutter(text: str) -> bool:
    """Return true for four consecutive identical delimiter-separated tokens."""

    tokens = [token for token in _DELIMITERS.split(text.strip().casefold()) if token]
    repeated = 1
    for previous, current in pairwise(tokens):
        repeated = repeated + 1 if current == previous else 1
        if repeated >= MIN_STUTTER_TOKENS:
            return True
    return False


def find_anomalies(cues: Sequence[Mapping[str, object]]) -> list[CueFlag]:
    """Return deterministic cue flags with cue-local reasons taking priority."""

    reasons: dict[int, str] = {}
    for index, cue in enumerate(cues):
        text = str(cue["text"])
        if any(pattern.search(text) for pattern in _BOILERPLATE):
            reasons[index] = "boilerplate"
        elif has_in_cue_stutter(text):
            reasons[index] = "stutter"

    run_start = 0
    previous: str | None = None
    for index in range(len(cues) + 1):
        key = _normalized_text(cues[index]["text"]) if index < len(cues) else None
        if key != previous or key == "":
            if previous not in (None, "") and index - run_start >= MIN_REPEAT_CUES:
                for position in range(run_start, index):
                    reasons.setdefault(position, "repeat_run")
            run_start = index
            previous = key

    return [
        CueFlag(
            index=index,
            start_ms=int(cues[index]["start_ms"]),
            end_ms=int(cues[index]["end_ms"]),
            text=str(cues[index]["text"]),
            reason=reason,
        )
        for index, reason in sorted(reasons.items())
    ]


def merge_anomaly_ranges(
    flags: Sequence[CueFlag], *, gap_ms: int = 1500
) -> list[AnomalyRange]:
    """Merge flags separated by no more than ``gap_ms`` milliseconds."""

    merged: list[dict[str, object]] = []
    for flag in sorted(flags, key=lambda item: (item.start_ms, item.index)):
        if merged and flag.start_ms - int(merged[-1]["end_ms"]) <= gap_ms:
            current = merged[-1]
            current["end_ms"] = max(int(current["end_ms"]), flag.end_ms)
            current["reasons"] = tuple(
                sorted({*current["reasons"], flag.reason})  # type: ignore[misc]
            )
            samples = tuple(current["samples"])  # type: ignore[arg-type]
            current["samples"] = (*samples, flag.text)[:3]
            continue
        merged.append(
            {
                "start_ms": flag.start_ms,
                "end_ms": flag.end_ms,
                "reasons": (flag.reason,),
                "samples": (flag.text,),
            }
        )

    return [
        AnomalyRange(
            start_ms=int(item["start_ms"]),
            end_ms=int(item["end_ms"]),
            reasons=tuple(item["reasons"]),  # type: ignore[arg-type]
            samples=tuple(item["samples"]),  # type: ignore[arg-type]
            long=int(item["end_ms"]) - int(item["start_ms"]) >= LONG_RANGE_MS,
        )
        for item in merged
    ]


def transcript_verdict(
    cues: Sequence[Mapping[str, object]], flags: Sequence[CueFlag]
) -> TranscriptVerdict:
    """Decide whether anomaly coverage makes the whole transcript unusable."""

    cue_count = len(cues)
    flag_count = len(flags)
    return TranscriptVerdict(
        cues=cue_count,
        flagged=flag_count,
        invalid=cue_count > 0 and flag_count / cue_count >= INVALID_RATIO,
    )
