"""Deterministic, frame-exact string-out construction."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from . import contracts, doctor

SOURCE_FIELDS = frozenset({"camera", "media_id", "path", "duration_seconds"})


@dataclass(frozen=True)
class SourceMedia:
    """One caller-owned media source normalized without changing the input."""

    camera: str
    media_id: str
    path: Path
    duration_frames: int


@dataclass(frozen=True)
class TimelineClip:
    """One source clip at an absolute, integer-frame timeline position."""

    camera: str
    media_id: str
    path: Path
    offset_frames: int
    duration_frames: int
    audio_enabled: bool


@dataclass(frozen=True)
class StringOutSegment:
    """One deterministic pair or single-source region."""

    label: str
    offset_frames: int
    duration_frames: int
    clips: tuple[TimelineClip, ...]


@dataclass(frozen=True)
class StringOut:
    """A complete string-out expressed only in integer frames."""

    profile_id: str
    frame_numerator: int
    frame_denominator: int
    duration_frames: int
    sources: tuple[SourceMedia, ...]
    segments: tuple[StringOutSegment, ...]


def _number_fraction(value: object) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("TRITRACK_EMIT_TIME_INVALID")
    if isinstance(value, Decimal):
        return Fraction(value)
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(Decimal(str(value)))
    raise ValueError("TRITRACK_EMIT_TIME_INVALID")


def _frame_duration(profile: Mapping[str, object]) -> Fraction:
    value = profile.get("frameDuration")
    if not isinstance(value, str) or not value.endswith("s"):
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    numerator, separator, denominator = value[:-1].partition("/")
    if not separator:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    try:
        result = Fraction(int(numerator), int(denominator))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID") from error
    if result <= 0:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    return result


def _round_fraction(value: Fraction) -> int:
    if value < 0:
        return -_round_fraction(-value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + (1 if remainder * 2 >= value.denominator else 0)


def seconds_to_frames(value: object, frame_duration: Fraction) -> int:
    """Quantize seconds once using deterministic half-away-from-zero rounding."""

    return _round_fraction(_number_fraction(value) / frame_duration)


def _normalize_sources(
    sources: Sequence[Mapping[str, object]],
    *,
    frame_duration: Fraction,
) -> tuple[SourceMedia, ...]:
    normalized: list[SourceMedia] = []
    seen: set[tuple[str, str]] = set()
    for source in sources:
        if not isinstance(source, Mapping) or set(source) != SOURCE_FIELDS:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        camera = source["camera"]
        media_id = source["media_id"]
        path = source["path"]
        if camera not in {"A", "B"}:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        if not isinstance(media_id, str) or not media_id:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        try:
            normalized_path = Path(path)  # type: ignore[arg-type]
        except TypeError as error:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID") from error
        duration_frames = seconds_to_frames(
            source["duration_seconds"],
            frame_duration,
        )
        if duration_frames <= 0:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        key = (camera, media_id)
        if key in seen:
            raise ValueError("TRITRACK_EMIT_SOURCE_DUPLICATE")
        seen.add(key)
        normalized.append(
            SourceMedia(camera, media_id, normalized_path, duration_frames)
        )
    return tuple(sorted(normalized, key=lambda item: (item.camera, item.media_id)))


def _expected_source_keys(sync_map: Mapping[str, Any]) -> set[tuple[str, str]]:
    expected: set[tuple[str, str]] = set()
    for pair in sync_map["pairs"]:
        expected.add(("A", str(pair["mediaA"])))
        expected.add(("B", str(pair["mediaB"])))
    expected.update(("A", str(media_id)) for media_id in sync_map["singleA"])
    expected.update(("B", str(media_id)) for media_id in sync_map["singleB"])
    return expected


def _validate_sync_relationships(sync_map: Mapping[str, Any]) -> None:
    pair_ids = [str(pair["pairId"]) for pair in sync_map["pairs"]]
    if len(pair_ids) != len(set(pair_ids)):
        raise ValueError("TRITRACK_EMIT_PAIR_ID_DUPLICATE")

    paired_a = [str(pair["mediaA"]) for pair in sync_map["pairs"]]
    if len(paired_a) != len(set(paired_a)):
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_CONFLICT")
    paired_keys = {
        *(("A", value) for value in paired_a),
        *(("B", str(pair["mediaB"])) for pair in sync_map["pairs"]),
    }
    single_keys = {
        *(("A", str(value)) for value in sync_map["singleA"]),
        *(("B", str(value)) for value in sync_map["singleB"]),
    }
    if paired_keys & single_keys:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_CONFLICT")


def build_string_out(
    sync_map: Mapping[str, Any],
    sources: Sequence[Mapping[str, object]],
    *,
    profile: Mapping[str, object],
) -> StringOut:
    """Validate inputs and build a stable pair-first string-out."""

    contracts.validate_contract("sync-map-v1", sync_map)
    sync_profile_id = str(sync_map["profileId"])
    packaged_profile = doctor.load_profile(sync_profile_id)
    contracts.validate_contract("compatibility-profile-v1", profile)
    if dict(profile) != packaged_profile:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")

    frame_duration = _frame_duration(profile)
    normalized_sources = _normalize_sources(
        sources,
        frame_duration=frame_duration,
    )
    source_by_key = {
        (source.camera, source.media_id): source for source in normalized_sources
    }
    _validate_sync_relationships(sync_map)
    if set(source_by_key) != _expected_source_keys(sync_map):
        raise ValueError("TRITRACK_EMIT_SOURCE_SET_MISMATCH")

    segments: list[StringOutSegment] = []
    cursor = 0
    sorted_pairs = sorted(
        sync_map["pairs"],
        key=lambda pair: (
            str(pair["pairId"]),
            str(pair["mediaA"]),
            str(pair["mediaB"]),
        ),
    )
    for pair in sorted_pairs:
        source_a = source_by_key[("A", str(pair["mediaA"]))]
        source_b = source_by_key[("B", str(pair["mediaB"]))]
        declared_a = seconds_to_frames(
            pair["durationASeconds"],
            frame_duration,
        )
        declared_b = seconds_to_frames(
            pair["durationBSeconds"],
            frame_duration,
        )
        if (
            declared_a != source_a.duration_frames
            or declared_b != source_b.duration_frames
        ):
            raise ValueError("TRITRACK_EMIT_DURATION_MISMATCH")

        b_from_a = seconds_to_frames(
            pair["offsetBFromASeconds"],
            frame_duration,
        )
        local_start = min(0, b_from_a)
        a_offset = cursor - local_start
        b_offset = cursor + b_from_a - local_start
        segment_duration = max(
            a_offset + source_a.duration_frames,
            b_offset + source_b.duration_frames,
        ) - cursor
        clips = (
            TimelineClip(
                "A",
                source_a.media_id,
                source_a.path,
                a_offset,
                source_a.duration_frames,
                pair["audioMaster"] == "A",
            ),
            TimelineClip(
                "B",
                source_b.media_id,
                source_b.path,
                b_offset,
                source_b.duration_frames,
                pair["audioMaster"] == "B",
            ),
        )
        segments.append(
            StringOutSegment(
                str(pair["pairId"]),
                cursor,
                segment_duration,
                clips,
            )
        )
        cursor += segment_duration

    for camera, field in (("A", "singleA"), ("B", "singleB")):
        for media_id in sorted(str(value) for value in sync_map[field]):
            source = source_by_key[(camera, media_id)]
            segments.append(
                StringOutSegment(
                    f"single-{camera}-{media_id}",
                    cursor,
                    source.duration_frames,
                    (
                        TimelineClip(
                            camera,
                            media_id,
                            source.path,
                            cursor,
                            source.duration_frames,
                            True,
                        ),
                    ),
                )
            )
            cursor += source.duration_frames

    return StringOut(
        sync_profile_id,
        frame_duration.numerator,
        frame_duration.denominator,
        cursor,
        normalized_sources,
        tuple(segments),
    )
