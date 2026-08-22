"""Build path-free transcription provenance and exact result artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from jsonschema import ValidationError

from . import contracts, process, sparse_source, transcribe_takes

_FATAL_TAKE_ERRORS = frozenset(
    {
        "TRITRACK_TRANSCRIPT_INPUT_CHANGED",
        "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
        "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
    }
)
_RESULT_FILE_LIMIT_BYTES = 16 * 1024 * 1024
_RESULT_FILE_NAMES = frozenset(
    {"manifest.json", "transcript-bundle.json", "transcription-report.json"}
)
_RESULT_FILE_NAMES_V2 = frozenset(
    {*_RESULT_FILE_NAMES, "transcription-density.txt"}
)
_LANGUAGE = re.compile(r"^[a-z]{2,3}$")


@dataclass(frozen=True)
class TranscriptionSettings:
    """Every setting that changes what the recognizer hears."""

    language: str
    recognition_model_sha256: str
    voice_activity: str
    voice_activity_model: str | None


@dataclass(frozen=True)
class TranscriptionSource:
    """Caller-owned source path paired with its already observed digest."""

    path: Path
    sha256: str


@dataclass(frozen=True)
class TranscriptionRequest:
    """One logical take and its primary-to-alternative source order."""

    take_id: str
    sources: tuple[TranscriptionSource, ...]


@dataclass(frozen=True)
class AttemptRecord:
    """One text-free source attempt."""

    ordinal: int
    source_sha256: str
    outcome: str
    failure_code: str | None
    settings: TranscriptionSettings
    metrics: AttemptMetrics


@dataclass(frozen=True)
class AttemptMetrics:
    """Observable content-density facts for one attempted source."""

    duration_ms: int | None
    duration_frame_count: int | None
    sample_rate_hz: int | None
    character_count: int | None
    characters_per_second: str | None
    sparse: bool | None


@dataclass(frozen=True)
class BuiltTranscriptionResult:
    """Validated authorities and their canonical bytes."""

    bundle: dict[str, object]
    report: dict[str, object]
    manifest: dict[str, object]
    bundle_bytes: bytes
    report_bytes: bytes
    manifest_bytes: bytes
    density_table_bytes: bytes | None = None


Decoder = Callable[
    [TranscriptionSource, str, TranscriptionSettings],
    transcribe_takes.TranscribedTake,
]


def _settings_payload(settings: TranscriptionSettings) -> dict[str, object]:
    return {
        "language": settings.language,
        "recognitionModelSha256": settings.recognition_model_sha256,
        "voiceActivity": settings.voice_activity,
        "voiceActivityModel": settings.voice_activity_model,
    }


def _attempt_payload(attempt: AttemptRecord) -> dict[str, object]:
    return {
        "ordinal": attempt.ordinal,
        "sourceSha256": attempt.source_sha256,
        "outcome": attempt.outcome,
        "failureCode": attempt.failure_code,
        "settings": _settings_payload(attempt.settings),
        "metrics": {
            "durationMs": attempt.metrics.duration_ms,
            "durationFrameCount": attempt.metrics.duration_frame_count,
            "sampleRateHz": attempt.metrics.sample_rate_hz,
            "characterCount": attempt.metrics.character_count,
            "charactersPerSecond": attempt.metrics.characters_per_second,
            "sparse": attempt.metrics.sparse,
        },
    }


def _unknown_metrics() -> AttemptMetrics:
    return AttemptMetrics(None, None, None, None, None, None)


def _exact_duration_ms(
    take: transcribe_takes.TranscribedTake,
) -> Fraction | None:
    """Return exact normalized duration while retaining ceiling ms for cues."""

    duration_ms = take.duration_ms
    frame_count = take.duration_frame_count
    sample_rate_hz = take.sample_rate_hz
    if frame_count is None and sample_rate_hz is None:
        if duration_ms is None:
            return None
        if isinstance(duration_ms, bool) or not isinstance(duration_ms, int):
            raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
        return Fraction(duration_ms, 1)
    if (
        isinstance(frame_count, bool)
        or not isinstance(frame_count, int)
        or frame_count <= 0
        or isinstance(sample_rate_hz, bool)
        or not isinstance(sample_rate_hz, int)
        or sample_rate_hz <= 0
        or isinstance(duration_ms, bool)
        or not isinstance(duration_ms, int)
        or duration_ms
        != (frame_count * 1000 + sample_rate_hz - 1) // sample_rate_hz
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    return Fraction(frame_count * 1000, sample_rate_hz)


def _duration_evidence(
    take: transcribe_takes.TranscribedTake,
) -> tuple[int, int, int] | None:
    exact_ms = _exact_duration_ms(take)
    if exact_ms is None or take.duration_ms is None:
        return None
    if take.duration_frame_count is None:
        return take.duration_ms, take.duration_ms * 16, 16_000
    assert take.sample_rate_hz is not None
    return take.duration_ms, take.duration_frame_count, take.sample_rate_hz


def _measured_metrics(take: transcribe_takes.TranscribedTake) -> AttemptMetrics:
    evidence = _duration_evidence(take)
    if evidence is None:
        return _unknown_metrics()
    duration_ms, frame_count, sample_rate_hz = evidence
    exact_duration_ms = Fraction(frame_count * 1000, sample_rate_hz)
    count = sparse_source.transcript_characters(take.cues)
    rate = sparse_source.characters_per_second(take.cues, exact_duration_ms)
    if rate is None:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    return AttemptMetrics(
        duration_ms=duration_ms,
        duration_frame_count=frame_count,
        sample_rate_hz=sample_rate_hz,
        character_count=count,
        characters_per_second=f"{rate:.3f}",
        sparse=sparse_source.is_sparse(take.cues, exact_duration_ms),
    )


def _candidate_for_take(
    take: transcribe_takes.TranscribedTake,
) -> sparse_source.SourceCandidate:
    return sparse_source.SourceCandidate(
        cues=take.cues,
        duration_ms=_exact_duration_ms(take),
        invalid=False,
    )


def _candidate_for_error() -> sparse_source.SourceCandidate:
    return sparse_source.SourceCandidate(cues=(), duration_ms=None, invalid=True)


def _canonical_bytes(contract: str, payload: object) -> bytes:
    contracts.validate_contract(contract, payload)
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _error_code(error: ValueError) -> str:
    code = str(error)
    if not code.startswith("TRITRACK_") or any(character.isspace() for character in code):
        return "TRITRACK_TRANSCRIPT_ATTEMPT_FAILED"
    return code


def _validate_settings(settings: TranscriptionSettings) -> None:
    payload = {
        "schemaVersion": "tritrack.transcription-report/v1",
        "profileId": transcribe_takes.TRANSCRIPTION_PROFILE_ID,
        "requestedTakeIds": ["settings-probe"],
        "runSettings": _settings_payload(settings),
        "takes": [
            {
                "takeId": "settings-probe",
                "status": "failed",
                "selectedSourceSha256": None,
                "attempts": [
                    {
                        "ordinal": 1,
                        "sourceSha256": "0" * 64,
                        "outcome": "failed",
                        "failureCode": "TRITRACK_TRANSCRIPT_ATTEMPT_FAILED",
                        "settings": _settings_payload(settings),
                    }
                ],
            }
        ],
    }
    contracts.validate_contract("transcription-report-v1", payload)


def reused_attempt(source_sha256: str) -> AttemptRecord:
    """Return an honest reuse marker that inherits no current settings."""

    return AttemptRecord(
        ordinal=1,
        source_sha256=source_sha256,
        outcome="reused",
        failure_code=None,
        settings=TranscriptionSettings(
            language="unknown",
            recognition_model_sha256="unknown",
            voice_activity="unknown",
            voice_activity_model="unknown",
        ),
        metrics=_unknown_metrics(),
    )


def _density_table(report: Mapping[str, object]) -> bytes:
    """Render deterministic path-free density evidence for a person."""

    measured: list[
        tuple[Fraction, Fraction, str, int, Mapping[str, object], bool, str]
    ] = []
    unknown: list[tuple[str, int, bool, str]] = []
    for take_value in report["takes"]:
        take = take_value
        take_id = str(take["takeId"])
        selected = take["selectedSourceSha256"]
        shared = ",".join(take["sharedAlternativeWithTakeIds"]) or "-"
        for attempt_value in take["attempts"]:
            attempt = attempt_value
            ordinal = int(attempt["ordinal"])
            is_selected = attempt["sourceSha256"] == selected
            metrics = attempt["metrics"]
            duration_ms = metrics["durationMs"]
            frame_count = metrics["durationFrameCount"]
            sample_rate_hz = metrics["sampleRateHz"]
            character_count = metrics["characterCount"]
            if (
                isinstance(duration_ms, int)
                and isinstance(frame_count, int)
                and isinstance(sample_rate_hz, int)
                and isinstance(character_count, int)
            ):
                measured.append(
                    (
                        Fraction(character_count * sample_rate_hz, frame_count),
                        Fraction(frame_count, sample_rate_hz),
                        take_id,
                        ordinal,
                        metrics,
                        is_selected,
                        shared,
                    )
                )
            else:
                unknown.append((take_id, ordinal, is_selected, shared))

    measured.sort(key=lambda item: (item[0], item[2], item[3]))
    threshold = Fraction(
        int(sparse_source.SPARSE_CHARACTERS_PER_SECOND * 1000), 1000
    )
    below = [row for row in measured if row[0] < threshold]
    at_or_above = [row for row in measured if row[0] >= threshold]
    lines = [
        f"profileId\t{report['profileId']}",
        f"language\t{report['runSettings']['language']}",
        f"voiceActivity\t{report['runSettings']['voiceActivity']}",
        "row\tdensity\tcharacters\tseconds\tsparse\ttakeId\tattempt\tselected\tsharedAlternativeWith",
    ]

    def exact_decimal(value: Fraction) -> str:
        denominator = value.denominator
        twos = fives = 0
        while denominator % 2 == 0:
            denominator //= 2
            twos += 1
        while denominator % 5 == 0:
            denominator //= 5
            fives += 1
        if denominator != 1:
            return f"{value.numerator}/{value.denominator}"
        places = max(twos, fives)
        scaled = value.numerator * (10**places) // value.denominator
        if places == 0:
            return str(scaled)
        digits = str(abs(scaled)).zfill(places + 1)
        sign = "-" if scaled < 0 else ""
        return f"{sign}{digits[:-places]}.{digits[-places:]}"

    def append_measured(row) -> None:
        _rate, exact_seconds, take_id, ordinal, metrics, selected, shared = row
        lines.append(
            "\t".join(
                (
                    "SOURCE",
                    str(metrics["charactersPerSecond"]),
                    str(metrics["characterCount"]),
                    exact_decimal(exact_seconds),
                    "yes" if metrics["sparse"] else "no",
                    take_id,
                    str(ordinal),
                    "yes" if selected else "no",
                    shared,
                )
            )
        )

    for row in below:
        append_measured(row)
    lines.append(
        f"THRESHOLD\t{sparse_source.SPARSE_CHARACTERS_PER_SECOND:.3f}\t-\t"
        f"{sparse_source.SPARSE_MINIMUM_DURATION_MS / 1000:.3f}\t-\t-\t-\t-\t-"
    )
    for row in at_or_above:
        append_measured(row)
    for take_id, ordinal, selected, shared in sorted(unknown):
        lines.append(
            f"UNKNOWN\tunknown\t-\t-\t-\t{take_id}\t{ordinal}\t"
            f"{'yes' if selected else 'no'}\t{shared}"
        )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _reported_candidate(outcome: object) -> sparse_source.SourceCandidate:
    if outcome == "completed":
        return sparse_source.SourceCandidate(({"text": "x"},), 1000)
    if outcome == "sparse":
        return sparse_source.SourceCandidate(({"text": "x"},), 120_000)
    if outcome == "empty":
        return sparse_source.SourceCandidate((), 1000)
    return sparse_source.SourceCandidate((), None, invalid=True)


def _validate_attempt_metrics(attempt: Mapping[str, object]) -> None:
    metrics = attempt["metrics"]
    if not isinstance(metrics, Mapping):
        raise TypeError
    values = tuple(
        metrics.get(name)
        for name in (
            "durationMs",
            "durationFrameCount",
            "sampleRateHz",
            "characterCount",
            "charactersPerSecond",
            "sparse",
        )
    )
    outcome = attempt["outcome"]
    if outcome in {"invalid", "failed", "reused"}:
        if any(value is not None for value in values):
            raise ValueError
        return
    duration_ms, frame_count, sample_rate_hz, character_count, rate, sparse = values
    if (
        isinstance(duration_ms, bool)
        or not isinstance(duration_ms, int)
        or duration_ms <= 0
        or isinstance(frame_count, bool)
        or not isinstance(frame_count, int)
        or frame_count <= 0
        or isinstance(sample_rate_hz, bool)
        or not isinstance(sample_rate_hz, int)
        or sample_rate_hz <= 0
        or isinstance(character_count, bool)
        or not isinstance(character_count, int)
        or character_count < 0
        or not isinstance(rate, str)
        or not isinstance(sparse, bool)
    ):
        raise ValueError
    exact_duration_ms = Fraction(frame_count * 1000, sample_rate_hz)
    if duration_ms != (frame_count * 1000 + sample_rate_hz - 1) // sample_rate_hz:
        raise ValueError
    exact_rate = Fraction(character_count * sample_rate_hz, frame_count)
    expected_sparse = (
        exact_duration_ms >= sparse_source.SPARSE_MINIMUM_DURATION_MS
        and exact_rate < sparse_source.SPARSE_CHARACTERS_PER_SECOND
    )
    if rate != f"{exact_rate:.3f}" or sparse is not expected_sparse:
        raise ValueError
    if outcome == "sparse" and sparse is not True:
        raise ValueError
    if outcome == "completed" and sparse is not False:
        raise ValueError
    if outcome == "empty" and character_count != 0:
        raise ValueError


def _validate_v2_relationships(
    bundle: Mapping[str, object], report: Mapping[str, object]
) -> None:
    run_settings = report["runSettings"]
    requested_take_ids = report["requestedTakeIds"]
    reported_takes = report["takes"]
    bundled_takes = bundle["takes"]
    if (
        not isinstance(run_settings, Mapping)
        or not isinstance(requested_take_ids, list)
        or not isinstance(reported_takes, list)
        or not isinstance(bundled_takes, list)
        or bundle["profileId"] != report["profileId"]
        or bundle["language"] != run_settings["language"]
        or bundle["modelSha256"] != run_settings["recognitionModelSha256"]
    ):
        raise ValueError

    report_ids = [take["takeId"] for take in reported_takes]
    bundle_ids = [take["takeId"] for take in bundled_takes]
    if (
        requested_take_ids != report_ids
        or report_ids != sorted(report_ids)
        or len(report_ids) != len(set(report_ids))
        or bundle_ids != sorted(bundle_ids)
        or len(bundle_ids) != len(set(bundle_ids))
    ):
        raise ValueError
    report_by_id = {take["takeId"]: take for take in reported_takes}
    bundle_by_id = {take["takeId"]: take for take in bundled_takes}
    if set(bundle_by_id) != {
        take_id
        for take_id, take in report_by_id.items()
        if take["status"] != "failed"
    }:
        raise ValueError

    unknown_settings = {
        "language": "unknown",
        "recognitionModelSha256": "unknown",
        "voiceActivity": "unknown",
        "voiceActivityModel": "unknown",
    }
    selected_alternatives: dict[str, list[str]] = {}
    source_attempt_count = 0
    sparse_source_count = 0
    retry_attempt_count = 0
    rescued_take_count = 0
    unrescued_take_count = 0
    for take_id, take in report_by_id.items():
        attempts = take["attempts"]
        if (
            not isinstance(attempts, list)
            or [attempt["ordinal"] for attempt in attempts]
            != list(range(1, len(attempts) + 1))
            or len({attempt["sourceSha256"] for attempt in attempts})
            != len(attempts)
        ):
            raise ValueError
        for attempt in attempts:
            _validate_attempt_metrics(attempt)
        source_attempt_count += len(attempts)
        sparse_source_count += sum(
            attempt["metrics"]["sparse"] is True for attempt in attempts
        )
        retry_attempt_count += max(0, len(attempts) - 1)

        selected_source = take["selectedSourceSha256"]
        if take["status"] == "reused":
            if (
                len(attempts) != 1
                or attempts[0]["outcome"] != "reused"
                or attempts[0]["settings"] != unknown_settings
                or any(value is not None for value in attempts[0]["metrics"].values())
                or selected_source != attempts[0]["sourceSha256"]
                or take["selectionReason"] != "reused"
            ):
                raise ValueError
        else:
            if any(attempt["settings"] != run_settings for attempt in attempts):
                raise ValueError
            candidates = tuple(
                _reported_candidate(attempt["outcome"]) for attempt in attempts
            )
            if any(
                not sparse_source.requires_retry(candidate)
                for candidate in candidates[:-1]
            ):
                raise ValueError
            choice = sparse_source.choose_source(candidates)
            expected_source = (
                None
                if choice.index is None
                else attempts[choice.index]["sourceSha256"]
            )
            if (
                selected_source != expected_source
                or take["selectionReason"] != choice.reason
                or (choice.index is None) != (take["status"] == "failed")
            ):
                raise ValueError

        selected_ordinal = next(
            (
                int(attempt["ordinal"])
                for attempt in attempts
                if attempt["sourceSha256"] == selected_source
            ),
            None,
        )
        if selected_ordinal is not None and selected_ordinal > 1:
            rescued_take_count += 1
            selected_alternatives.setdefault(str(selected_source), []).append(take_id)
        elif len(attempts) > 1:
            unrescued_take_count += 1

        if take["status"] == "failed":
            continue
        bundled = bundle_by_id[take_id]
        if bundled["sourceSha256"] != selected_source:
            raise ValueError
        if take["status"] == "reused":
            if bundled["status"] not in {"completed", "empty"}:
                raise ValueError
        elif bundled["status"] != take["status"]:
            raise ValueError
        selected_attempt = attempts[selected_ordinal - 1]
        if take["status"] != "reused" and (
            selected_attempt["outcome"] not in {"completed", "sparse"}
            or bundled["status"] != "completed"
            or not bundled["cues"]
        ):
            raise ValueError
        metrics = selected_attempt["metrics"]
        if metrics["durationMs"] is not None:
            count = sparse_source.transcript_characters(bundled["cues"])
            exact_duration_ms = Fraction(
                metrics["durationFrameCount"] * 1000,
                metrics["sampleRateHz"],
            )
            rate = sparse_source.characters_per_second(
                bundled["cues"], exact_duration_ms
            )
            if (
                metrics["characterCount"] != count
                or metrics["charactersPerSecond"] != f"{rate:.3f}"
                or metrics["sparse"]
                != sparse_source.is_sparse(bundled["cues"], exact_duration_ms)
            ):
                raise ValueError

    for take_id, take in report_by_id.items():
        peers = selected_alternatives.get(str(take["selectedSourceSha256"]), [])
        expected_peers = sorted(peer for peer in peers if peer != take_id)
        if take["sharedAlternativeWithTakeIds"] != expected_peers:
            raise ValueError
    if report["summary"] != {
        "sourceAttemptCount": source_attempt_count,
        "sparseSourceCount": sparse_source_count,
        "retryAttemptCount": retry_attempt_count,
        "rescuedTakeCount": rescued_take_count,
        "unrescuedTakeCount": unrescued_take_count,
    }:
        raise ValueError


def validate_result_relationships(
    bundle: Mapping[str, object], report: Mapping[str, object]
) -> None:
    """Reject individually valid authorities that disagree about their takes."""

    try:
        if report.get("schemaVersion") == "tritrack.transcription-report/v2":
            _validate_v2_relationships(bundle, report)
            return
        if report.get("schemaVersion") != "tritrack.transcription-report/v1":
            raise ValueError
        run_settings = report["runSettings"]
        requested_take_ids = report["requestedTakeIds"]
        reported_takes = report["takes"]
        bundled_takes = bundle["takes"]
        if (
            not isinstance(run_settings, Mapping)
            or not isinstance(requested_take_ids, list)
            or not isinstance(reported_takes, list)
            or not isinstance(bundled_takes, list)
            or bundle["profileId"] != report["profileId"]
            or bundle["language"] != run_settings["language"]
            or bundle["modelSha256"] != run_settings["recognitionModelSha256"]
        ):
            raise ValueError

        report_ids = [take["takeId"] for take in reported_takes]
        bundle_ids = [take["takeId"] for take in bundled_takes]
        if (
            requested_take_ids != report_ids
            or report_ids != sorted(report_ids)
            or len(report_ids) != len(set(report_ids))
            or bundle_ids != sorted(bundle_ids)
            or len(bundle_ids) != len(set(bundle_ids))
        ):
            raise ValueError

        report_by_id = {take["takeId"]: take for take in reported_takes}
        bundle_by_id = {take["takeId"]: take for take in bundled_takes}
        expected_bundle_ids = {
            take_id
            for take_id, take in report_by_id.items()
            if take["status"] != "failed"
        }
        if set(bundle_by_id) != expected_bundle_ids:
            raise ValueError

        unknown_settings = {
            "language": "unknown",
            "recognitionModelSha256": "unknown",
            "voiceActivity": "unknown",
            "voiceActivityModel": "unknown",
        }
        for take_id, reported in report_by_id.items():
            status = reported["status"]
            selected_source = reported["selectedSourceSha256"]
            attempts = reported["attempts"]
            if not isinstance(attempts, list) or [
                attempt["ordinal"] for attempt in attempts
            ] != list(range(1, len(attempts) + 1)):
                raise ValueError

            if status == "reused":
                if (
                    len(attempts) != 1
                    or attempts[0]["outcome"] != "reused"
                    or attempts[0]["settings"] != unknown_settings
                    or selected_source != attempts[0]["sourceSha256"]
                ):
                    raise ValueError
            else:
                if any(
                    attempt["settings"] != run_settings for attempt in attempts
                ):
                    raise ValueError
                if status == "failed":
                    if selected_source is not None or any(
                        attempt["outcome"] not in {"failed", "invalid"}
                        for attempt in attempts
                    ):
                        raise ValueError
                elif (
                    attempts[-1]["outcome"] != status
                    or selected_source != attempts[-1]["sourceSha256"]
                    or any(
                        attempt["outcome"] not in {"failed", "invalid"}
                        for attempt in attempts[:-1]
                    )
                ):
                    raise ValueError

            if status == "failed":
                continue
            bundled = bundle_by_id[take_id]
            if (
                bundled["sourceSha256"] != selected_source
                or (
                    status != "reused"
                    and bundled["status"] != status
                )
                or (
                    status == "reused"
                    and bundled["status"] not in {"completed", "empty"}
                )
            ):
                raise ValueError
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error


def build_transcription_result(
    requests: Sequence[TranscriptionRequest],
    *,
    settings: TranscriptionSettings,
    engine_version: str,
    decoder: Decoder,
    reuse: Mapping[str, transcribe_takes.TranscribedTake] | None = None,
) -> BuiltTranscriptionResult:
    """Retry each take in source order and build deterministic authorities."""

    _validate_settings(settings)
    ordered = sorted(requests, key=lambda request: request.take_id)
    take_ids = [request.take_id for request in ordered]
    if not take_ids:
        raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")

    completed: list[transcribe_takes.TranscribedTake] = []
    reports: list[dict[str, object]] = []
    for request in ordered:
        if not request.sources:
            raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
        reusable = (reuse or {}).get(request.take_id)
        if reusable is not None:
            if (
                reusable.take_id != request.take_id
                or reusable.status not in {"completed", "empty"}
                or reusable.source_sha256
                not in {source.sha256 for source in request.sources}
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_REUSE_MISMATCH")
            attempt = reused_attempt(reusable.source_sha256)
            completed.append(reusable)
            reports.append(
                {
                    "takeId": request.take_id,
                    "status": "reused",
                    "selectedSourceSha256": reusable.source_sha256,
                    "selectionReason": "reused",
                    "sharedAlternativeWithTakeIds": [],
                    "attempts": [_attempt_payload(attempt)],
                }
            )
            continue
        attempts: list[AttemptRecord] = []
        decoded: list[transcribe_takes.TranscribedTake | None] = []
        candidates: list[sparse_source.SourceCandidate] = []
        for ordinal, source in enumerate(request.sources, start=1):
            try:
                take = decoder(source, request.take_id, settings)
            except ValueError as error:
                code = _error_code(error)
                if code in _FATAL_TAKE_ERRORS:
                    raise
                attempts.append(
                    AttemptRecord(
                        ordinal=ordinal,
                        source_sha256=source.sha256,
                        outcome=(
                            "invalid"
                            if code
                            in {
                                "TRITRACK_TRANSCRIPT_ANOMALY_INVALID",
                                "TRITRACK_TRANSCRIPT_REPEATED_CUES",
                            }
                            else "failed"
                        ),
                        failure_code=code,
                        settings=settings,
                        metrics=_unknown_metrics(),
                    )
                )
                decoded.append(None)
                candidates.append(_candidate_for_error())
                continue
            if (
                take.take_id != request.take_id
                or take.source_sha256 != source.sha256
                or take.status not in {"completed", "empty"}
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
            metrics = _measured_metrics(take)
            candidate = _candidate_for_take(take)
            problem = sparse_source.source_problem(candidate)
            attempts.append(
                AttemptRecord(
                    ordinal=ordinal,
                    source_sha256=source.sha256,
                    outcome="sparse" if problem == "sparse" else take.status,
                    failure_code=None,
                    settings=settings,
                    metrics=metrics,
                )
            )
            decoded.append(take)
            candidates.append(candidate)
            if not sparse_source.requires_retry(candidate):
                break

        choice = sparse_source.choose_source(candidates)
        selected = decoded[choice.index] if choice.index is not None else None
        if selected is None:
            reports.append(
                {
                    "takeId": request.take_id,
                    "status": "failed",
                    "selectedSourceSha256": None,
                    "selectionReason": choice.reason,
                    "sharedAlternativeWithTakeIds": [],
                    "attempts": [_attempt_payload(attempt) for attempt in attempts],
                }
            )
            continue
        completed.append(selected)
        reports.append(
            {
                "takeId": request.take_id,
                "status": selected.status,
                "selectedSourceSha256": selected.source_sha256,
                "selectionReason": choice.reason,
                "sharedAlternativeWithTakeIds": [],
                "attempts": [_attempt_payload(attempt) for attempt in attempts],
            }
        )

    selected_alternatives: dict[str, list[str]] = {}
    for take in reports:
        selected_sha256 = take["selectedSourceSha256"]
        attempts = take["attempts"]
        if (
            isinstance(selected_sha256, str)
            and isinstance(attempts, list)
            and attempts
            and attempts[0]["sourceSha256"] != selected_sha256
        ):
            selected_alternatives.setdefault(selected_sha256, []).append(
                str(take["takeId"])
            )
    for take in reports:
        selected_sha256 = take["selectedSourceSha256"]
        peers = selected_alternatives.get(str(selected_sha256), [])
        if len(peers) > 1:
            take["sharedAlternativeWithTakeIds"] = sorted(
                take_id for take_id in peers if take_id != take["takeId"]
            )

    bundle = transcribe_takes.build_transcript_bundle(
        completed,
        language=settings.language,
        model_sha256=settings.recognition_model_sha256,
        engine_version=engine_version,
    )
    retry_attempt_count = sum(
        max(0, len(take["attempts"]) - 1) for take in reports
    )
    rescued_take_count = sum(
        1
        for take in reports
        if take["selectedSourceSha256"] is not None
        and take["attempts"][0]["sourceSha256"]
        != take["selectedSourceSha256"]
    )
    unrescued_take_count = sum(
        1
        for take in reports
        if len(take["attempts"]) > 1
        and (
            take["selectedSourceSha256"] is None
            or take["attempts"][0]["sourceSha256"]
            == take["selectedSourceSha256"]
        )
    )
    report: dict[str, object] = {
        "schemaVersion": "tritrack.transcription-report/v2",
        "profileId": transcribe_takes.TRANSCRIPTION_PROFILE_ID,
        "requestedTakeIds": take_ids,
        "runSettings": _settings_payload(settings),
        "sparsePolicy": {
            "charactersPerSecond": sparse_source.SPARSE_CHARACTERS_PER_SECOND,
            "minimumDurationMs": sparse_source.SPARSE_MINIMUM_DURATION_MS,
            "contentDefinition": "unicode-letters-numbers-symbols-v1",
        },
        "summary": {
            "sourceAttemptCount": sum(len(take["attempts"]) for take in reports),
            "sparseSourceCount": sum(
                1
                for take in reports
                for attempt in take["attempts"]
                if attempt["metrics"]["sparse"] is True
            ),
            "retryAttemptCount": retry_attempt_count,
            "rescuedTakeCount": rescued_take_count,
            "unrescuedTakeCount": unrescued_take_count,
        },
        "takes": reports,
    }
    validate_result_relationships(bundle, report)
    bundle_bytes = transcribe_takes.encode_transcript_bundle(bundle).encode("utf-8")
    report_bytes = _canonical_bytes("transcription-report-v2", report)
    density_table_bytes = _density_table(report)
    manifest: dict[str, object] = {
        "schemaVersion": "tritrack.transcription-result-manifest/v2",
        "bundle": {
            "fileName": "transcript-bundle.json",
            "sha256": hashlib.sha256(bundle_bytes).hexdigest(),
        },
        "report": {
            "fileName": "transcription-report.json",
            "sha256": hashlib.sha256(report_bytes).hexdigest(),
        },
        "densityTable": {
            "fileName": "transcription-density.txt",
            "sha256": hashlib.sha256(density_table_bytes).hexdigest(),
        },
    }
    manifest_bytes = _canonical_bytes("transcription-result-manifest-v2", manifest)
    return BuiltTranscriptionResult(
        bundle=bundle,
        report=report,
        manifest=manifest,
        bundle_bytes=bundle_bytes,
        report_bytes=report_bytes,
        manifest_bytes=manifest_bytes,
        density_table_bytes=density_table_bytes,
    )


def _write_new(path: Path, encoded: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_transcription_result(
    output_dir: Path, result: BuiltTranscriptionResult
) -> Path:
    """Publish all authorities and then their manifest into an absent directory."""

    if not isinstance(result, BuiltTranscriptionResult):
        raise TypeError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    destination = process.require_absent_output(output_dir)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-",
            dir=destination.parent,
        )
    )
    linked: list[Path] = []
    reserved = False
    try:
        manifest_version = result.manifest.get("schemaVersion")
        if manifest_version == "tritrack.transcription-result-manifest/v1":
            if result.density_table_bytes is not None:
                raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
            authorities = (
                ("transcript-bundle.json", result.bundle_bytes),
                ("transcription-report.json", result.report_bytes),
            )
        elif manifest_version == "tritrack.transcription-result-manifest/v2":
            if result.density_table_bytes is None:
                raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
            authorities = (
                ("transcript-bundle.json", result.bundle_bytes),
                ("transcription-report.json", result.report_bytes),
                ("transcription-density.txt", result.density_table_bytes),
            )
        else:
            raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
        files = (*authorities, ("manifest.json", result.manifest_bytes))
        for file_name, encoded in files:
            _write_new(staging / file_name, encoded)
        try:
            os.mkdir(destination, 0o755)
            reserved = True
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
        for file_name, _encoded in files:
            target = destination / file_name
            os.link(staging / file_name, target)
            linked.append(target)
        _fsync_directory(destination)
        return destination
    except BaseException:
        if reserved:
            for target in reversed(linked):
                try:
                    target.unlink()
                except OSError:
                    pass
            try:
                destination.rmdir()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def _read_result_file(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _RESULT_FILE_LIMIT_BYTES
        ):
            raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_RESULT_FILE_LIMIT_BYTES + 1)
        if len(encoded) > _RESULT_FILE_LIMIT_BYTES:
            raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
        return encoded
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _decode_json(encoded: bytes) -> object:
    try:
        return json.loads(encoded.decode("utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error


def validate_transcription_result_bytes(
    *,
    bundle_bytes: bytes,
    report_bytes: bytes,
    manifest_bytes: bytes,
    density_table_bytes: bytes | None,
) -> BuiltTranscriptionResult:
    """Validate one result family from exact bytes, independent of storage."""

    bundle = _decode_json(bundle_bytes)
    report = _decode_json(report_bytes)
    manifest = _decode_json(manifest_bytes)
    if not all(isinstance(payload, dict) for payload in (bundle, report, manifest)):
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    assert isinstance(bundle, dict)
    assert isinstance(report, dict)
    assert isinstance(manifest, dict)
    try:
        canonical_bundle = transcribe_takes.encode_transcript_bundle(bundle).encode(
            "utf-8"
        )
        manifest_version = manifest.get("schemaVersion")
        report_version = report.get("schemaVersion")
        if (
            manifest_version == "tritrack.transcription-result-manifest/v1"
            and report_version == "tritrack.transcription-report/v1"
            and density_table_bytes is None
        ):
            canonical_report = _canonical_bytes("transcription-report-v1", report)
            canonical_manifest = _canonical_bytes(
                "transcription-result-manifest-v1", manifest
            )
            canonical_density_table = None
        elif (
            manifest_version == "tritrack.transcription-result-manifest/v2"
            and report_version == "tritrack.transcription-report/v2"
            and density_table_bytes is not None
        ):
            canonical_report = _canonical_bytes("transcription-report-v2", report)
            canonical_manifest = _canonical_bytes(
                "transcription-result-manifest-v2", manifest
            )
            canonical_density_table = _density_table(report)
        else:
            raise ValueError
    except (KeyError, TypeError, ValueError, ValidationError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    if (
        bundle_bytes != canonical_bundle
        or report_bytes != canonical_report
        or manifest_bytes != canonical_manifest
        or manifest["bundle"]["sha256"]
        != hashlib.sha256(bundle_bytes).hexdigest()
        or manifest["report"]["sha256"]
        != hashlib.sha256(report_bytes).hexdigest()
        or density_table_bytes != canonical_density_table
        or (
            density_table_bytes is not None
            and manifest["densityTable"]["sha256"]
            != hashlib.sha256(density_table_bytes).hexdigest()
        )
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    validate_result_relationships(bundle, report)
    return BuiltTranscriptionResult(
        bundle=bundle,
        report=report,
        manifest=manifest,
        bundle_bytes=bundle_bytes,
        report_bytes=report_bytes,
        manifest_bytes=manifest_bytes,
        density_table_bytes=density_table_bytes,
    )


def load_transcription_result(result_dir: Path) -> BuiltTranscriptionResult:
    """Load an exact immutable result and verify every canonical byte and hash."""

    root = Path(result_dir)
    try:
        metadata = root.lstat()
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
    try:
        entries = {entry.name for entry in os.scandir(root)}
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    if entries not in {_RESULT_FILE_NAMES, _RESULT_FILE_NAMES_V2}:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")

    bundle_bytes = _read_result_file(root / "transcript-bundle.json")
    report_bytes = _read_result_file(root / "transcription-report.json")
    manifest_bytes = _read_result_file(root / "manifest.json")
    density_table_bytes = (
        _read_result_file(root / "transcription-density.txt")
        if entries == _RESULT_FILE_NAMES_V2
        else None
    )
    return validate_transcription_result_bytes(
        bundle_bytes=bundle_bytes,
        report_bytes=report_bytes,
        manifest_bytes=manifest_bytes,
        density_table_bytes=density_table_bytes,
    )


def _reuse_takes(
    result: BuiltTranscriptionResult,
) -> dict[str, transcribe_takes.TranscribedTake]:
    takes = result.bundle["takes"]
    assert isinstance(takes, list)
    reusable: dict[str, transcribe_takes.TranscribedTake] = {}
    for value in takes:
        assert isinstance(value, dict)
        take_id = str(value["takeId"])
        cues = value["cues"]
        assert isinstance(cues, list)
        reusable[take_id] = transcribe_takes.TranscribedTake(
            take_id=take_id,
            source_sha256=str(value["sourceSha256"]),
            status=str(value["status"]),
            cues=tuple(dict(cue) for cue in cues),
        )
    return reusable


def _require_absolute(path: Path) -> Path:
    selected = Path(path)
    if not selected.is_absolute():
        raise ValueError("TRITRACK_PATH_NOT_ABSOLUTE")
    return selected


def transcribe_local_result(
    primary_paths: Sequence[Path],
    *,
    alternative_paths: Mapping[str, Sequence[Path]] | None,
    model_path: Path,
    language: str,
    reuse_from: Path | None = None,
    ffmpeg_executable: str = "ffmpeg",
    whisper_executable: str = "whisper-cli",
) -> BuiltTranscriptionResult:
    """Run the local decoder through retry/degrade without publishing paths."""

    if not primary_paths:
        raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
    if not isinstance(language, str) or _LANGUAGE.fullmatch(language) is None:
        raise ValueError("TRITRACK_TRANSCRIPT_LANGUAGE_INVALID")

    primary = tuple(_require_absolute(Path(path)) for path in primary_paths)
    take_ids = [path.name for path in primary]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")
    alternatives = {
        take_id: tuple(_require_absolute(Path(path)) for path in paths)
        for take_id, paths in (alternative_paths or {}).items()
    }
    if set(alternatives) - set(take_ids):
        raise ValueError("TRITRACK_TRANSCRIPT_ALTERNATIVE_INVALID")
    for paths in alternatives.values():
        if len(paths) != len(set(paths)):
            raise ValueError("TRITRACK_TRANSCRIPT_ALTERNATIVE_INVALID")
    alternative_values = tuple(
        path for paths in alternatives.values() for path in paths
    )
    if set(primary) & set(alternative_values):
        raise ValueError("TRITRACK_TRANSCRIPT_ALTERNATIVE_INVALID")
    all_paths = tuple(dict.fromkeys((*primary, *alternative_values)))
    for path in all_paths:
        transcribe_takes._require_readable_file(
            path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE"
        )
    selected_model = transcribe_takes._require_readable_file(
        _require_absolute(model_path), "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
    )
    engine_version = transcribe_takes._read_engine_version(whisper_executable)
    model_sha256 = transcribe_takes._sha256_file(
        selected_model, "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
    )
    source_hashes = {
        path: transcribe_takes._sha256_file(
            path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE"
        )
        for path in all_paths
    }
    requests = [
        TranscriptionRequest(
            take_id=path.name,
            sources=tuple(
                TranscriptionSource(candidate, source_hashes[candidate])
                for candidate in (path, *alternatives.get(path.name, ()))
            ),
        )
        for path in primary
    ]
    settings = TranscriptionSettings(
        language=language,
        recognition_model_sha256=model_sha256,
        voice_activity="off",
        voice_activity_model=None,
    )
    reuse = (
        _reuse_takes(load_transcription_result(_require_absolute(reuse_from)))
        if reuse_from is not None
        else None
    )

    def decoder(
        source: TranscriptionSource,
        take_id: str,
        _settings: TranscriptionSettings,
    ) -> transcribe_takes.TranscribedTake:
        return transcribe_takes.transcribe_source(
            source.path,
            take_id=take_id,
            source_sha256=source.sha256,
            model_path=selected_model,
            model_sha256=model_sha256,
            language=language,
            ffmpeg_executable=ffmpeg_executable,
            whisper_executable=whisper_executable,
        )

    result = build_transcription_result(
        requests,
        settings=settings,
        engine_version=engine_version,
        decoder=decoder,
        reuse=reuse,
    )
    if (
        transcribe_takes._sha256_file(selected_model) != model_sha256
        or any(
            transcribe_takes._sha256_file(path) != digest
            for path, digest in source_hashes.items()
        )
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")
    return result


def transcribe_and_publish_result(
    primary_paths: Sequence[Path],
    *,
    alternative_paths: Mapping[str, Sequence[Path]] | None,
    model_path: Path,
    language: str,
    output_dir: Path,
    reuse_from: Path | None = None,
    ffmpeg_executable: str = "ffmpeg",
    whisper_executable: str = "whisper-cli",
) -> BuiltTranscriptionResult:
    """Run the shared local orchestrator and publish one immutable result."""

    destination = process.require_absent_output(_require_absolute(output_dir))
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    result = transcribe_local_result(
        primary_paths,
        alternative_paths=alternative_paths,
        model_path=model_path,
        language=language,
        reuse_from=reuse_from,
        ffmpeg_executable=ffmpeg_executable,
        whisper_executable=whisper_executable,
    )
    publish_transcription_result(destination, result)
    return result
