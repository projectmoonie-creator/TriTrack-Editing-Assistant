"""Audio-verified A/B synchronization with no-overwrite publication."""

from __future__ import annotations

import datetime as dt
import json
import math
import os
import struct
import tempfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from . import contracts, doctor, process

MIN_OVERLAP_SECONDS = 3.0
MIN_PEAK_RATIO = 6.0
CLOCK_SANITY_DAYS = 30
PAIR_TOLERANCE_SECONDS = 180.0
DEFAULT_SAMPLE_RATE = 1_000
PROBE_TIMEOUT_SECONDS = 30.0
AUDIO_TIMEOUT_SECONDS = 300.0
MAX_PROBE_BYTES = 1024 * 1024
MAX_AUDIO_BYTES = 512 * 1024 * 1024

Clip = Mapping[str, Any]
Evidence = Mapping[str, float]


@dataclass(frozen=True)
class MediaSource:
    """An opaque public media id and a local source path."""

    media_id: str
    path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.media_id, str) or not self.media_id:
            raise ValueError("TRITRACK_SYNC_MEDIA_ID_INVALID")
        object.__setattr__(self, "path", Path(self.path))


def parse_media_time(value: str) -> dt.datetime:
    """Return a timezone-aware timestamp from ISO-8601 metadata."""

    try:
        parsed = dt.datetime.fromisoformat(value)
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_SYNC_TIME_INVALID") from error
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed


def _one_camera_hints_are_sane(
    clips: Iterable[Clip], *, today: dt.date, max_days: int
) -> bool:
    stamped = [clip["start"] for clip in clips if clip.get("start") is not None]
    if not stamped:
        return False
    nearest_days = min(abs((stamp.date() - today).days) for stamp in stamped)
    return nearest_days <= max_days


def time_hints_are_sane(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    today: dt.date | None = None,
    max_days: int = CLOCK_SANITY_DAYS,
) -> bool:
    """Accept time hints only when both camera sets have a plausible stamp."""

    observed_today = today or dt.datetime.now(dt.UTC).astimezone().date()
    return _one_camera_hints_are_sane(
        camera_a, today=observed_today, max_days=max_days
    ) and _one_camera_hints_are_sane(
        camera_b, today=observed_today, max_days=max_days
    )


def candidate_pairs(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    hints_ok: bool,
    tolerance_seconds: float = PAIR_TOLERANCE_SECONDS,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
):
    """Yield time-near candidates, or all candidates when hints are stale."""

    camera_b_items = tuple(camera_b)
    if not hints_ok:
        for a_clip in camera_a:
            for b_clip in camera_b_items:
                yield a_clip, b_clip
        return

    pad = dt.timedelta(seconds=tolerance_seconds)
    for a_clip in camera_a:
        a_start = a_clip.get("start")
        if a_start is None:
            continue
        a_end = a_start + dt.timedelta(seconds=a_clip["duration_seconds"])
        for b_clip in camera_b_items:
            b_start = b_clip.get("start")
            if b_start is None:
                continue
            b_end = b_start + dt.timedelta(seconds=b_clip["duration_seconds"])
            overlap = (min(a_end, b_end) + pad - max(a_start, b_start)).total_seconds()
            if overlap > min_overlap_seconds:
                yield a_clip, b_clip


def normalized_audio_correlation(
    a_samples: Sequence[float],
    b_samples: Sequence[float],
    *,
    sample_rate: int,
) -> tuple[float, float]:
    """Return the strongest normalized lag and separated-peak ratio."""

    if sample_rate <= 0 or len(a_samples) == 0 or len(b_samples) == 0:
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")

    def normalize(samples: Sequence[float]) -> np.ndarray:
        values = np.asarray(samples, dtype=np.float64)
        if values.ndim != 1 or not np.all(np.isfinite(values)):
            raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
        centered = values - values.mean()
        deviation = math.sqrt(float(np.mean(centered**2)))
        if deviation == 0:
            raise ValueError("TRITRACK_SYNC_AUDIO_FLAT")
        return centered / deviation

    normalized_a = normalize(a_samples)
    normalized_b = normalize(b_samples)
    score_count = len(normalized_a) + len(normalized_b) - 1
    fft_length = 1 << (score_count - 1).bit_length()
    scores = np.fft.irfft(
        np.fft.rfft(normalized_a, fft_length)
        * np.fft.rfft(normalized_b[::-1], fft_length),
        fft_length,
    )[:score_count]
    scores = np.abs(scores)
    strongest_index = int(np.argmax(scores))
    strongest_lag = strongest_index - (len(normalized_b) - 1)
    strongest_score = float(scores[strongest_index])
    lags = np.arange(-(len(normalized_b) - 1), len(normalized_a))
    separated_scores = scores[np.abs(lags - strongest_lag) > sample_rate]
    second_score = float(separated_scores.max()) if separated_scores.size else 0.0
    return strongest_lag / sample_rate, strongest_score / (second_score + 1e-9)


def select_strongest_pairs(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    evidence_for: Callable[[Clip, Clip], Evidence | None],
    hints_ok: bool,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> list[dict[str, float | str]]:
    """Select one strongest B per A without consuming a reusable B clip."""

    camera_a_items = tuple(camera_a)
    camera_b_items = tuple(camera_b)
    strongest_by_a: dict[str, dict[str, float | str]] = {}

    for a_clip, b_clip in candidate_pairs(
        camera_a_items,
        camera_b_items,
        hints_ok=hints_ok,
        min_overlap_seconds=min_overlap_seconds,
    ):
        if not (a_clip.get("has_audio") and b_clip.get("has_audio")):
            continue
        evidence = evidence_for(a_clip, b_clip)
        if evidence is None:
            continue
        peak_ratio = float(evidence["peak_ratio"])
        overlap_seconds = float(evidence["overlap_seconds"])
        if peak_ratio < min_peak_ratio or overlap_seconds < min_overlap_seconds:
            continue

        a_id = str(a_clip["id"])
        candidate: dict[str, float | str] = {
            "a": a_id,
            "b": str(b_clip["id"]),
            "offset_seconds": float(evidence["offset_seconds"]),
            "peak_ratio": peak_ratio,
            "overlap_seconds": overlap_seconds,
        }
        current = strongest_by_a.get(a_id)
        if current is None or float(current["peak_ratio"]) < peak_ratio:
            strongest_by_a[a_id] = candidate

    return [
        strongest_by_a[str(a_clip["id"])]
        for a_clip in camera_a_items
        if str(a_clip["id"]) in strongest_by_a
    ]


def _process_stdout(result: process.ProcessResult, error_code: str) -> bytes:
    if not result.ok:
        raise ValueError(error_code)
    return result.stdout


def probe_media(
    source: MediaSource,
    *,
    executable: str = "ffprobe",
    timeout_seconds: float = PROBE_TIMEOUT_SECONDS,
    max_captured_bytes: int = MAX_PROBE_BYTES,
) -> dict[str, object]:
    """Read one source's public probe fields through the bounded process API."""

    if not source.path.is_file():
        raise ValueError("TRITRACK_SYNC_SOURCE_MISSING")
    command = [
        executable,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_entries",
        "format=duration:format_tags=creation_time:stream=codec_type",
        str(source.path),
    ]
    result = process.run_bounded(
        command,
        timeout_seconds=timeout_seconds,
        max_captured_bytes=max_captured_bytes,
    )
    raw = _process_stdout(result, "TRITRACK_SYNC_PROBE_FAILED")
    try:
        payload = json.loads(raw)
        format_data = payload["format"]
        streams = payload["streams"]
        duration = float(format_data["duration"])
        tags = format_data.get("tags", {})
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID") from error
    if (
        not isinstance(payload, Mapping)
        or not isinstance(format_data, Mapping)
        or not isinstance(streams, list)
        or not isinstance(tags, Mapping)
        or not math.isfinite(duration)
        or duration <= 0
    ):
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID")
    creation_time = tags.get("creation_time")
    if creation_time is not None and not isinstance(creation_time, str):
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID")
    start = parse_media_time(creation_time) if creation_time else None
    has_audio = any(
        isinstance(stream, Mapping) and stream.get("codec_type") == "audio"
        for stream in streams
    )
    return {
        "id": source.media_id,
        "duration_seconds": duration,
        "start": start,
        "has_audio": has_audio,
        "source": source,
    }


def extract_audio_samples(
    source: MediaSource,
    *,
    executable: str = "ffmpeg",
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    timeout_seconds: float = AUDIO_TIMEOUT_SECONDS,
    max_captured_bytes: int = MAX_AUDIO_BYTES,
) -> tuple[float, ...]:
    """Decode mono float samples through the bounded process API."""

    if sample_rate <= 0:
        raise ValueError("TRITRACK_SYNC_SAMPLE_RATE_INVALID")
    result = process.run_bounded(
        [
            executable,
            "-nostdin",
            "-v",
            "error",
            "-i",
            str(source.path),
            "-map",
            "0:a:0",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "f32le",
            "pipe:1",
        ],
        timeout_seconds=timeout_seconds,
        max_captured_bytes=max_captured_bytes,
    )
    raw = _process_stdout(result, "TRITRACK_SYNC_AUDIO_DECODE_FAILED")
    if not raw or len(raw) % 4:
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
    samples = tuple(value[0] for value in struct.iter_unpack("<f", raw))
    if any(not math.isfinite(value) for value in samples):
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
    return samples


def _audio_evidence(
    a_clip: Clip,
    b_clip: Clip,
    *,
    samples_for: Callable[[Clip], Sequence[float]],
    sample_rate: int,
) -> dict[str, float]:
    a_samples = samples_for(a_clip)
    b_samples = samples_for(b_clip)
    offset_seconds, peak_ratio = normalized_audio_correlation(
        a_samples,
        b_samples,
        sample_rate=sample_rate,
    )
    lag_samples = round(offset_seconds * sample_rate)
    first_b_index = max(0, -lag_samples)
    last_b_index = min(len(b_samples), len(a_samples) - lag_samples)
    overlap_samples = max(0, last_b_index - first_b_index)
    return {
        "offset_seconds": offset_seconds,
        "peak_ratio": peak_ratio,
        "overlap_seconds": overlap_samples / sample_rate,
    }


def _validate_unique_media(clips: Sequence[Clip]) -> None:
    identifiers = [str(clip["id"]) for clip in clips]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("TRITRACK_SYNC_MEDIA_ID_DUPLICATE")


def _started_at_text(value: object) -> str | None:
    if not isinstance(value, dt.datetime):
        return None
    return value.isoformat().replace("+00:00", "Z")


def build_sync_map(
    camera_a: Sequence[Clip],
    camera_b: Sequence[Clip],
    *,
    profile_id: str,
    evidence_for: Callable[[Clip, Clip], Evidence | None],
    today: dt.date | None = None,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> dict[str, object]:
    """Build and validate the public sync-map-v1 payload."""

    doctor.load_profile(profile_id)
    _validate_unique_media(camera_a)
    _validate_unique_media(camera_b)
    hints_ok = time_hints_are_sane(camera_a, camera_b, today=today)
    selected = select_strongest_pairs(
        camera_a,
        camera_b,
        evidence_for=evidence_for,
        hints_ok=hints_ok,
        min_peak_ratio=min_peak_ratio,
        min_overlap_seconds=min_overlap_seconds,
    )
    a_by_id = {str(clip["id"]): clip for clip in camera_a}
    selected_a = {str(pair["a"]) for pair in selected}
    selected_b = {str(pair["b"]) for pair in selected}

    pairs: list[dict[str, object]] = []
    for index, pair in enumerate(selected, start=1):
        a_clip = a_by_id[str(pair["a"])]
        b_clip = next(
            clip for clip in camera_b if str(clip["id"]) == str(pair["b"])
        )
        pairs.append(
            {
                "pairId": f"pair-{index:03d}",
                "mediaA": pair["a"],
                "mediaB": pair["b"],
                "offsetBFromASeconds": pair["offset_seconds"],
                "confidence": pair["peak_ratio"],
                "overlapSeconds": pair["overlap_seconds"],
                "audioMaster": "A",
                "durationASeconds": float(a_clip["duration_seconds"]),
                "durationBSeconds": float(b_clip["duration_seconds"]),
                "startedAt": _started_at_text(a_clip.get("start"))
                if hints_ok
                else None,
            }
        )

    warnings: list[dict[str, str]] = []
    if not hints_ok:
        warnings.append({"code": "SYNC_TIME_HINTS_STALE"})
    for clip in (*camera_a, *camera_b):
        if not clip.get("has_audio"):
            warnings.append(
                {"code": "SYNC_AUDIO_MISSING", "mediaId": str(clip["id"])}
            )

    payload: dict[str, object] = {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": profile_id,
        "pairs": pairs,
        "singleA": [
            str(clip["id"]) for clip in camera_a if str(clip["id"]) not in selected_a
        ],
        "singleB": [
            str(clip["id"]) for clip in camera_b if str(clip["id"]) not in selected_b
        ],
        "warnings": warnings,
    }
    contracts.validate_contract("sync-map-v1", payload)
    return payload


def publish_sync_map(
    output_path: str | os.PathLike[str], payload: object
) -> Path:
    """Atomically create one validated map without overwriting any path."""

    contracts.validate_contract("sync-map-v1", payload)
    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def synchronize_and_publish(
    camera_a_sources: Sequence[MediaSource],
    camera_b_sources: Sequence[MediaSource],
    *,
    profile_id: str,
    output_path: str | os.PathLike[str],
    today: dt.date | None = None,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> dict[str, object]:
    """Probe, correlate, validate, and publish one local synchronization map."""

    process.require_absent_output(output_path)
    camera_a = tuple(probe_media(source) for source in camera_a_sources)
    camera_b = tuple(probe_media(source) for source in camera_b_sources)
    sample_cache: dict[MediaSource, tuple[float, ...]] = {}

    def samples_for(clip: Clip) -> Sequence[float]:
        source = clip["source"]
        if not isinstance(source, MediaSource):
            raise TypeError("TRITRACK_SYNC_SOURCE_INVALID")
        if source not in sample_cache:
            sample_cache[source] = extract_audio_samples(
                source,
                sample_rate=sample_rate,
            )
        return sample_cache[source]

    def evidence_for(a_clip: Clip, b_clip: Clip) -> Evidence:
        return _audio_evidence(
            a_clip,
            b_clip,
            samples_for=samples_for,
            sample_rate=sample_rate,
        )

    payload = build_sync_map(
        camera_a,
        camera_b,
        profile_id=profile_id,
        evidence_for=evidence_for,
        today=today,
        min_peak_ratio=min_peak_ratio,
        min_overlap_seconds=min_overlap_seconds,
    )
    publish_sync_map(output_path, payload)
    return payload
