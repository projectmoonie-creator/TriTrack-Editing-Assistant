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
from pathlib import Path

from . import contracts, process, transcribe_takes

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


def validate_result_relationships(
    bundle: Mapping[str, object], report: Mapping[str, object]
) -> None:
    """Reject individually valid authorities that disagree about their takes."""

    try:
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
                    "attempts": [_attempt_payload(attempt)],
                }
            )
            continue
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
    validate_result_relationships(bundle, report)
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
    if entries != _RESULT_FILE_NAMES:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID")

    bundle_bytes = _read_result_file(root / "transcript-bundle.json")
    report_bytes = _read_result_file(root / "transcription-report.json")
    manifest_bytes = _read_result_file(root / "manifest.json")
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
        canonical_report = _canonical_bytes("transcription-report-v1", report)
        canonical_manifest = _canonical_bytes(
            "transcription-result-manifest-v1", manifest
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_RESULT_INVALID") from error
    if (
        bundle_bytes != canonical_bundle
        or report_bytes != canonical_report
        or manifest_bytes != canonical_manifest
        or manifest["bundle"]["sha256"]
        != hashlib.sha256(bundle_bytes).hexdigest()
        or manifest["report"]["sha256"]
        != hashlib.sha256(report_bytes).hexdigest()
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
    all_paths = (*primary, *(path for paths in alternatives.values() for path in paths))
    if len(all_paths) != len(set(all_paths)):
        raise ValueError("TRITRACK_TRANSCRIPT_ALTERNATIVE_INVALID")
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
