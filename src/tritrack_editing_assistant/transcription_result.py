"""Build path-free transcription provenance and exact result artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from . import contracts, process, transcribe_takes

_FATAL_TAKE_ERRORS = frozenset(
    {
        "TRITRACK_TRANSCRIPT_INPUT_CHANGED",
        "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
        "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
    }
)


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


@dataclass(frozen=True)
class BuiltTranscriptionResult:
    """Validated authorities and their canonical bytes."""

    bundle: dict[str, object]
    report: dict[str, object]
    manifest: dict[str, object]
    bundle_bytes: bytes
    report_bytes: bytes
    manifest_bytes: bytes


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
    }


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
    )


def build_transcription_result(
    requests: Sequence[TranscriptionRequest],
    *,
    settings: TranscriptionSettings,
    engine_version: str,
    decoder: Decoder,
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
        attempts: list[AttemptRecord] = []
        selected: transcribe_takes.TranscribedTake | None = None
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
                    )
                )
                continue
            if (
                take.take_id != request.take_id
                or take.source_sha256 != source.sha256
                or take.status not in {"completed", "empty"}
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")
            selected = take
            attempts.append(
                AttemptRecord(
                    ordinal=ordinal,
                    source_sha256=source.sha256,
                    outcome=take.status,
                    failure_code=None,
                    settings=settings,
                )
            )
            break

        if selected is None:
            reports.append(
                {
                    "takeId": request.take_id,
                    "status": "failed",
                    "selectedSourceSha256": None,
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
                "attempts": [_attempt_payload(attempt) for attempt in attempts],
            }
        )

    bundle = transcribe_takes.build_transcript_bundle(
        completed,
        language=settings.language,
        model_sha256=settings.recognition_model_sha256,
        engine_version=engine_version,
    )
    report: dict[str, object] = {
        "schemaVersion": "tritrack.transcription-report/v1",
        "profileId": transcribe_takes.TRANSCRIPTION_PROFILE_ID,
        "requestedTakeIds": take_ids,
        "runSettings": _settings_payload(settings),
        "takes": reports,
    }
    bundle_bytes = transcribe_takes.encode_transcript_bundle(bundle).encode("utf-8")
    report_bytes = _canonical_bytes("transcription-report-v1", report)
    manifest: dict[str, object] = {
        "schemaVersion": "tritrack.transcription-result-manifest/v1",
        "bundle": {
            "fileName": "transcript-bundle.json",
            "sha256": hashlib.sha256(bundle_bytes).hexdigest(),
        },
        "report": {
            "fileName": "transcription-report.json",
            "sha256": hashlib.sha256(report_bytes).hexdigest(),
        },
    }
    manifest_bytes = _canonical_bytes("transcription-result-manifest-v1", manifest)
    return BuiltTranscriptionResult(
        bundle=bundle,
        report=report,
        manifest=manifest,
        bundle_bytes=bundle_bytes,
        report_bytes=report_bytes,
        manifest_bytes=manifest_bytes,
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
    """Publish two authorities and then their manifest into an absent directory."""

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
        files = (
            ("transcript-bundle.json", result.bundle_bytes),
            ("transcription-report.json", result.report_bytes),
            ("manifest.json", result.manifest_bytes),
        )
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
