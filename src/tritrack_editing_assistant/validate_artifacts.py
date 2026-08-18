"""Read-only, offline validation of public TriTrack artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import __version__, contracts, doctor, emit_fcpxml, paper_edit, run_workflow

MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class LoadedValidationArtifact:
    path: Path
    encoded: bytes
    sha256: str


def _read_regular_bytes(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE")
        if not 0 < metadata.st_size <= MAX_VALIDATION_ARTIFACT_BYTES:
            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(MAX_VALIDATION_ARTIFACT_BYTES + 1)
        if len(encoded) > MAX_VALIDATION_ARTIFACT_BYTES:
            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
        return encoded
    except OSError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_regular_artifact(path: Path) -> LoadedValidationArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected)
    return LoadedValidationArtifact(
        path=selected,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
    )


def _verify_unchanged(artifact: LoadedValidationArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path)
    except ValueError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED")


def _validation_summary(
    *,
    kind: str,
    scope: str,
    hashes: dict[str, str],
    counts: dict[str, int],
    details: dict[str, object],
) -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.validate-summary/v1",
        "toolVersion": __version__,
        "artifactKind": kind,
        "validationScope": scope,
        "hashes": hashes,
        "counts": counts,
        "details": details,
    }


def validate_contract_artifact(path: Path) -> dict[str, object]:
    """Validate one JSON file against its exact installed closed contract."""

    artifact = _load_regular_artifact(path)
    try:
        payload = json.loads(
            artifact.encoded.decode("utf-8", errors="strict"),
            parse_float=Decimal,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_VALIDATE_JSON_INVALID") from error
    try:
        schema_version = payload["schemaVersion"]
    except (KeyError, TypeError) as error:
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
    try:
        contract_name = contracts.contract_name_for_schema_version(schema_version)
    except ValueError as error:
        if str(error) == "TRITRACK_CONTRACT_REGISTRY_INVALID":
            raise
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
    try:
        contracts.validate_contract(contract_name, payload)
    except (TypeError, ValidationError) as error:
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_INVALID") from error
    _verify_unchanged(artifact)
    return _validation_summary(
        kind="contract",
        scope="contract",
        hashes={"artifact": artifact.sha256},
        counts={},
        details={
            "contractName": contract_name,
            "contractSchemaVersion": schema_version,
        },
    )


def validate_fcpxml_artifact(
    path: Path,
    *,
    profile_id: str,
    binding_id: str,
) -> dict[str, object]:
    """Validate one FCPXML file against exact installed profile authorities."""

    artifact = _load_regular_artifact(path)
    try:
        text = artifact.encoded.decode("utf-8", errors="strict")
    except UnicodeError as error:
        raise ValueError("TRITRACK_VALIDATE_FCPXML_INVALID") from error
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    emit_fcpxml.validate_fcpxml(text, profile=profile, binding=binding)
    _verify_unchanged(artifact)
    return _validation_summary(
        kind="fcpxml",
        scope="structural-profile",
        hashes={"artifact": artifact.sha256},
        counts={},
        details={"profileId": profile_id, "bindingId": binding_id},
    )


def validate_paper_artifacts(
    aligned_path: Path,
    workbook_path: Path,
) -> dict[str, object]:
    """Validate one workbook against the exact aligned JSON authority."""

    validated = paper_edit.validate_workbook(aligned_path, workbook_path)
    return _validation_summary(
        kind="paper",
        scope="authority-bound",
        hashes={
            "aligned": validated.aligned_sha256,
            "workbook": validated.workbook_sha256,
        },
        counts={
            "answerCount": validated.answer_count,
            "cueCount": validated.cue_count,
            "questionCount": validated.question_count,
            "reserveCount": validated.reserve_count,
        },
        details={
            "workbookSchemaVersion": validated.workbook_schema_version,
        },
    )


def validate_run_bundle(run_dir: Path) -> dict[str, object]:
    """Validate and summarize one complete immutable run bundle."""

    bundle, run_summary = run_workflow.inspect_run(run_dir)
    stages = run_summary["stages"]
    artifacts = run_summary["artifacts"]
    assert isinstance(stages, list)
    assert isinstance(artifacts, dict)
    return _validation_summary(
        kind="run",
        scope="complete-run-bundle",
        hashes={"manifest": bundle.manifest_sha256},
        counts={
            "artifactCount": len(artifacts),
            "stageCount": len(stages),
        },
        details={"runSummary": run_summary},
    )
