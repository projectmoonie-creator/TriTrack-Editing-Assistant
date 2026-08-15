"""Local whisper.cpp evidence canonicalization and transcription workflow."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import wave
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from . import hallucination
from .contracts import validate_contract
from .process import ProcessResult, require_absent_output, run_bounded

_LANGUAGE = re.compile(r"^[a-z]{2,3}$")
_HASH_CHUNK_BYTES = 1024 * 1024
_PROCESS_CAPTURE_BYTES = 512 * 1024
_ENGINE_JSON_LIMIT_BYTES = 16 * 1024 * 1024
_MAX_FINAL_CUE_PADDING_MS = 5000
_AUDIO_TIMEOUT_SECONDS = 900
_ENGINE_TIMEOUT_SECONDS = 3600
TRANSCRIPTION_PROFILE_ID = "whisper-cpp-cpu-no-fallback-v1"


@dataclass(frozen=True)
class TranscribedTake:
    """One source-bound local transcription result."""

    take_id: str
    source_sha256: str
    status: str
    cues: tuple[dict[str, object], ...]


def _object(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    return value


def _millisecond(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    return value


def canonicalize_whisper_evidence(
    payload: object,
    *,
    requested_language: str,
    audio_duration_ms: int,
    proven_silence: bool = False,
) -> list[dict[str, object]]:
    """Extract strict canonical cues from one supported whisper JSON result."""

    if (
        isinstance(audio_duration_ms, bool)
        or not isinstance(audio_duration_ms, int)
        or audio_duration_ms < 1
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")

    evidence = _object(payload)
    result = _object(evidence.get("result"))
    if result.get("language") != requested_language:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    transcription = evidence.get("transcription")
    if not isinstance(transcription, list):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")

    cues: list[dict[str, object]] = []
    previous_end = 0
    for index, value in enumerate(transcription, start=1):
        segment = _object(value)
        text = hallucination.normalize_cue_text(segment.get("text"))
        if hallucination.is_blank_audio_sentinel(text):
            if proven_silence:
                continue
            raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID")
        offsets = _object(segment.get("offsets"))
        start_ms = _millisecond(offsets.get("from"))
        end_ms = _millisecond(offsets.get("to"))
        if end_ms > audio_duration_ms:
            if (
                index != len(transcription)
                or start_ms >= audio_duration_ms
                or end_ms - audio_duration_ms > _MAX_FINAL_CUE_PADDING_MS
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
            end_ms = audio_duration_ms
        if not (previous_end <= start_ms < end_ms <= audio_duration_ms):
            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
        cues.append(
            {
                "cueId": f"cue-{len(cues) + 1:06d}",
                "startMs": start_ms,
                "endMs": end_ms,
                "text": text,
            }
        )
        previous_end = end_ms

    hallucination.reject_repeated_cues([str(cue["text"]) for cue in cues])
    return cues


def build_transcript_bundle(
    takes: Sequence[TranscribedTake],
    *,
    language: str,
    model_sha256: str,
    engine_version: str,
) -> dict[str, object]:
    """Build and validate one stable, path-free local transcript bundle."""

    ordered = sorted(takes, key=lambda take: take.take_id)
    take_ids = [take.take_id for take in ordered]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")

    bundle: dict[str, object] = {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": TRANSCRIPTION_PROFILE_ID,
        "language": language,
        "modelSha256": model_sha256,
        "engine": {"name": "whisper-cli", "version": engine_version},
        "takes": [
            {
                "takeId": take.take_id,
                "sourceSha256": take.source_sha256,
                "status": take.status,
                "cues": [dict(cue) for cue in take.cues],
            }
            for take in ordered
        ],
    }
    validate_contract("transcript-bundle-v1", bundle)
    return bundle


def encode_transcript_bundle(bundle: object) -> str:
    """Encode a validated bundle with stable key ordering and final newline."""

    validate_contract("transcript-bundle-v1", bundle)
    return json.dumps(
        bundle,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _require_readable_file(path: Path, code: str) -> Path:
    if not path.is_file() or not os.access(path, os.R_OK):
        raise ValueError(code)
    return path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(_HASH_CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def _require_process(result: ProcessResult, code: str) -> None:
    if not result.ok:
        raise ValueError(code)


def _read_engine_version(executable: str) -> str:
    result = run_bounded(
        [executable, "--version"],
        timeout_seconds=5,
        max_captured_bytes=64 * 1024,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")
    try:
        lines = result.stdout.decode("utf-8", errors="strict").splitlines()
    except UnicodeError as error:
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID") from error
    if not lines:
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
    version = lines[0].strip()
    if (
        not version
        or len(version) > 256
        or "/" in version
        or "\\" in version
        or any(ord(character) < 32 for character in version)
    ):
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
    return version


def _normalize_audio(
    source: Path,
    destination: Path,
    *,
    ffmpeg_executable: str,
) -> None:
    result = run_bounded(
        [
            ffmpeg_executable,
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-n",
            "-i",
            str(source),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            "-f",
            "wav",
            str(destination),
        ],
        timeout_seconds=_AUDIO_TIMEOUT_SECONDS,
        max_captured_bytes=_PROCESS_CAPTURE_BYTES,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED")


def _inspect_normalized_audio(path: Path) -> tuple[int, bool]:
    try:
        with wave.open(str(path), "rb") as audio:
            if (
                audio.getnchannels() != 1
                or audio.getsampwidth() != 2
                or audio.getframerate() != 16000
                or audio.getnframes() < 1
            ):
                raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
            frame_count = audio.getnframes()
            silent = True
            while frames := audio.readframes(64 * 1024):
                if any(frames):
                    silent = False
    except (OSError, EOFError, wave.Error) as error:
        raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID") from error
    duration_ms = (frame_count * 1000 + 15999) // 16000
    return duration_ms, silent


def _run_whisper(
    audio_path: Path,
    *,
    model_path: Path,
    language: str,
    output_prefix: Path,
    whisper_executable: str,
) -> None:
    result = run_bounded(
        [
            whisper_executable,
            "--model",
            str(model_path),
            "--file",
            str(audio_path),
            "--language",
            language,
            "--temperature",
            "0",
            "--temperature-inc",
            "0",
            "--no-fallback",
            "--no-gpu",
            "--output-json-full",
            "--output-file",
            str(output_prefix),
            "--no-prints",
        ],
        timeout_seconds=_ENGINE_TIMEOUT_SECONDS,
        max_captured_bytes=_PROCESS_CAPTURE_BYTES,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")


def _load_engine_json(path: Path) -> object:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISREG(metadata.st_mode)
        or not 0 < metadata.st_size <= _ENGINE_JSON_LIMIT_BYTES
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    try:
        with path.open("rb") as stream:
            encoded = stream.read(_ENGINE_JSON_LIMIT_BYTES + 1)
        if len(encoded) > _ENGINE_JSON_LIMIT_BYTES:
            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
        return json.loads(encoded.decode("utf-8", errors="strict"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error


def _publish_transcript_bundle(output_path: Path, bundle: object) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_transcript_bundle(bundle).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)


def transcribe_and_publish(
    media_paths: Sequence[Path],
    *,
    model_path: Path,
    language: str,
    output_path: Path,
    ffmpeg_executable: str = "ffmpeg",
    whisper_executable: str = "whisper-cli",
) -> dict[str, object]:
    """Transcribe local takes once and atomically publish one canonical bundle."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    if not media_paths:
        raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
    if not isinstance(language, str) or _LANGUAGE.fullmatch(language) is None:
        raise ValueError("TRITRACK_TRANSCRIPT_LANGUAGE_INVALID")

    media = tuple(Path(path) for path in media_paths)
    take_ids = [path.name for path in media]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")
    for path in media:
        _require_readable_file(path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE")
    selected_model = _require_readable_file(
        Path(model_path), "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
    )

    engine_version = _read_engine_version(whisper_executable)
    model_sha256 = _sha256_file(selected_model)
    source_hashes = {path: _sha256_file(path) for path in media}
    takes: list[TranscribedTake] = []
    with tempfile.TemporaryDirectory(prefix="tritrack-transcribe-") as temporary:
        scratch = Path(temporary)
        for index, source in enumerate(sorted(media, key=lambda path: path.name), start=1):
            audio_path = scratch / f"audio-{index:06d}.wav"
            output_prefix = scratch / f"whisper-{index:06d}"
            _normalize_audio(
                source,
                audio_path,
                ffmpeg_executable=ffmpeg_executable,
            )
            duration_ms, silent = _inspect_normalized_audio(audio_path)
            _run_whisper(
                audio_path,
                model_path=selected_model,
                language=language,
                output_prefix=output_prefix,
                whisper_executable=whisper_executable,
            )
            evidence = _load_engine_json(Path(f"{output_prefix}.json"))
            cues = canonicalize_whisper_evidence(
                evidence,
                requested_language=language,
                audio_duration_ms=duration_ms,
                proven_silence=silent,
            )
            if (
                _sha256_file(source) != source_hashes[source]
                or _sha256_file(selected_model) != model_sha256
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")
            if silent and cues:
                raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_TEXT_DETECTED")
            if not silent and not cues:
                raise ValueError("TRITRACK_TRANSCRIPT_EMPTY_UNPROVEN")
            takes.append(
                TranscribedTake(
                    take_id=source.name,
                    source_sha256=source_hashes[source],
                    status="empty" if silent else "completed",
                    cues=tuple(cues),
                )
            )

    if _sha256_file(selected_model) != model_sha256 or any(
        _sha256_file(source) != source_hashes[source] for source in media
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")

    bundle = build_transcript_bundle(
        takes,
        language=language,
        model_sha256=model_sha256,
        engine_version=engine_version,
    )
    _publish_transcript_bundle(destination, bundle)
    return bundle
