"""Deterministic cue-addressed transcript promotion."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError

from . import hallucination
from .contracts import validate_contract
from .process import require_absent_output

ALIGNMENT_PROFILE_ID = "cue-addressed-v1"
_ARTIFACT_LIMIT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class LoadedJsonArtifact:
    """One validated exact-byte JSON input and its immutable provenance."""

    path: Path
    contract: str
    invalid_code: str
    payload: object
    sha256: str


def _validate_input(contract: str, payload: object, code: str) -> None:
    try:
        validate_contract(contract, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _ARTIFACT_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_ARTIFACT_LIMIT_BYTES + 1)
        if len(encoded) > _ARTIFACT_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def load_json_artifact(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedJsonArtifact:
    """Load one bounded regular JSON file and validate its strict contract."""

    selected = Path(path)
    encoded = _read_regular_bytes(selected, invalid_code)
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedJsonArtifact(
        path=selected,
        contract=contract,
        invalid_code=invalid_code,
        payload=payload,
        sha256=hashlib.sha256(encoded).hexdigest(),
    )


def verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
    """Fail closed when an exact input file changed after validated loading."""

    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED")


def _canonical_source_cues(take: Mapping[str, object]) -> list[dict[str, object]]:
    status = take["status"]
    cues = take["cues"]
    assert isinstance(cues, list)
    if status == "empty":
        return []

    canonical: list[dict[str, object]] = []
    cue_ids: set[str] = set()
    previous_end = 0
    for cue in cues:
        assert isinstance(cue, Mapping)
        cue_id = cue["cueId"]
        start_ms = cue["startMs"]
        end_ms = cue["endMs"]
        text = cue["text"]
        assert isinstance(cue_id, str)
        assert isinstance(start_ms, int)
        assert isinstance(end_ms, int)
        assert isinstance(text, str)
        if cue_id in cue_ids:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_CUE")
        cue_ids.add(cue_id)
        try:
            normalized = hallucination.normalize_cue_text(text)
        except (TypeError, ValueError) as error:
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_INVALID") from error
        if normalized != text or not (previous_end <= start_ms < end_ms):
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_INVALID")
        canonical.append(
            {
                "cueId": cue_id,
                "startMs": start_ms,
                "endMs": end_ms,
                "text": text,
                "disposition": "original",
            }
        )
        previous_end = end_ms
    return canonical


def build_aligned_transcript(
    transcript: object,
    revision: object,
    *,
    source_bundle_sha256: str,
    revision_sha256: str,
) -> dict[str, object]:
    """Promote cue-addressed text while preserving canonical source timing."""

    _validate_input(
        "transcript-bundle-v1",
        transcript,
        "TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID",
    )
    _validate_input(
        "text-revision-v1",
        revision,
        "TRITRACK_ALIGNMENT_REVISION_INVALID",
    )
    assert isinstance(transcript, Mapping)
    assert isinstance(revision, Mapping)

    if revision["sourceBundleSha256"] != source_bundle_sha256:
        raise ValueError("TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH")
    if revision["language"] != transcript["language"]:
        raise ValueError("TRITRACK_ALIGNMENT_LANGUAGE_MISMATCH")

    source_takes = transcript["takes"]
    revision_takes = revision["takes"]
    assert isinstance(source_takes, list)
    assert isinstance(revision_takes, list)

    aligned_by_take: dict[str, dict[str, object]] = {}
    source_by_take: dict[str, Mapping[str, object]] = {}
    for take in source_takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        assert isinstance(take_id, str)
        if take_id in source_by_take:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_TAKE")
        source_by_take[take_id] = take
        aligned_by_take[take_id] = {
            "takeId": take_id,
            "sourceSha256": take["sourceSha256"],
            "status": take["status"],
            "cues": _canonical_source_cues(take),
        }

    revised_take_ids: set[str] = set()
    for revised_take in revision_takes:
        assert isinstance(revised_take, Mapping)
        take_id = revised_take["takeId"]
        assert isinstance(take_id, str)
        if take_id in revised_take_ids:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_TAKE")
        revised_take_ids.add(take_id)
        source_take = source_by_take.get(take_id)
        if source_take is None:
            raise ValueError("TRITRACK_ALIGNMENT_TAKE_UNKNOWN")
        if revised_take["sourceSha256"] != source_take["sourceSha256"]:
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH")
        if source_take["status"] == "empty":
            raise ValueError("TRITRACK_ALIGNMENT_EMPTY_TAKE_IMMUTABLE")

        aligned_cues = aligned_by_take[take_id]["cues"]
        assert isinstance(aligned_cues, list)
        cues_by_id = {cue["cueId"]: cue for cue in aligned_cues}
        revised_cue_ids: set[str] = set()
        revisions = revised_take["revisions"]
        assert isinstance(revisions, list)
        for cue_revision in revisions:
            assert isinstance(cue_revision, Mapping)
            cue_id = cue_revision["cueId"]
            assert isinstance(cue_id, str)
            if cue_id in revised_cue_ids:
                raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_CUE")
            revised_cue_ids.add(cue_id)
            cue = cues_by_id.get(cue_id)
            if cue is None:
                raise ValueError("TRITRACK_ALIGNMENT_CUE_UNKNOWN")
            try:
                normalized = hallucination.normalize_cue_text(cue_revision["text"])
            except (TypeError, ValueError) as error:
                raise ValueError("TRITRACK_ALIGNMENT_TEXT_INVALID") from error
            cue["text"] = normalized
            cue["disposition"] = "revised"

    aligned: dict[str, object] = {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": ALIGNMENT_PROFILE_ID,
        "sourceBundleSha256": source_bundle_sha256,
        "revisionSha256": revision_sha256,
        "language": transcript["language"],
        "takes": [aligned_by_take[take_id] for take_id in sorted(aligned_by_take)],
    }
    validate_contract("aligned-transcript-v1", aligned)
    return aligned


def encode_aligned_transcript(payload: object) -> bytes:
    """Return stable UTF-8 bytes for one strict aligned transcript."""

    validate_contract("aligned-transcript-v1", payload)
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def publish_aligned_transcript(payload: object, output_path: Path) -> None:
    """Publish one aligned transcript without overwriting a race winner."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_aligned_transcript(payload)
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


def prepare_alignment(
    transcript_path: Path,
    revision_path: Path,
) -> tuple[dict[str, object], tuple[LoadedJsonArtifact, LoadedJsonArtifact]]:
    """Load exact inputs and build an unpublished deterministic alignment."""

    transcript = load_json_artifact(
        transcript_path,
        contract="transcript-bundle-v1",
        invalid_code="TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID",
    )
    revision = load_json_artifact(
        revision_path,
        contract="text-revision-v1",
        invalid_code="TRITRACK_ALIGNMENT_REVISION_INVALID",
    )
    aligned = build_aligned_transcript(
        transcript.payload,
        revision.payload,
        source_bundle_sha256=transcript.sha256,
        revision_sha256=revision.sha256,
    )
    return aligned, (transcript, revision)


def align_and_publish(
    transcript_path: Path,
    revision_path: Path,
    *,
    output_path: Path,
) -> dict[str, object]:
    """Promote local cue revisions and atomically publish stable bytes."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned, inputs = prepare_alignment(transcript_path, revision_path)
    for artifact in inputs:
        verify_artifact_unchanged(artifact)
    publish_aligned_transcript(aligned, destination)
    return aligned
