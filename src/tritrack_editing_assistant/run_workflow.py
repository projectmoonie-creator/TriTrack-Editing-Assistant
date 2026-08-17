"""Immutable run manifests and complete bundle publication."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import __version__, contracts, doctor, emit_fcpxml, process

MANIFEST_FILE_NAME = "run-manifest.json"
_MANIFEST_LIMIT_BYTES = 16 * 1024 * 1024
_ARTIFACT_LIMIT_BYTES = 512 * 1024 * 1024
_HASH_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class PhaseSpec:
    next_action: str
    chain_length: int
    artifacts: tuple[tuple[str, str], ...]
    stages: tuple[str, ...]


PHASE_SPECS = {
    "prepared": PhaseSpec(
        next_action="provide-revision",
        chain_length=0,
        artifacts=(
            ("doctorReceipt", "doctor.json"),
            ("syncMap", "sync-map.json"),
            ("transcriptBundle", "transcript-bundle.json"),
            ("stringOut", "string-out.fcpxml"),
        ),
        stages=("doctor", "sync", "transcribe", "emit"),
    ),
    "aligned": PhaseSpec(
        next_action="edit-paper-workbook",
        chain_length=1,
        artifacts=(
            ("alignedTranscript", "aligned-transcript.json"),
            ("paperWorkbook", "paper-edit.xlsx"),
        ),
        stages=("align", "paper"),
    ),
    "finished": PhaseSpec(
        next_action="complete",
        chain_length=2,
        artifacts=(
            ("grouping", "grouping.json"),
            ("workingCut", "working-cut.json"),
            ("storyCut", "story-cut.fcpxml"),
        ),
        stages=("paper", "organize", "emit"),
    ),
}


@dataclass(frozen=True)
class LoadedRunArtifact:
    logical_name: str
    file_name: str
    path: Path
    encoded: bytes
    sha256: str


@dataclass(frozen=True)
class LoadedRunBundle:
    root: Path
    manifest: dict[str, object]
    manifest_bytes: bytes
    manifest_sha256: str
    artifacts: Mapping[str, LoadedRunArtifact]


def _manifest_error(error: BaseException | None = None) -> ValueError:
    result = ValueError("TRITRACK_RUN_MANIFEST_INVALID")
    if error is not None:
        result.__cause__ = error
    return result


def _validate_manifest(payload: object) -> dict[str, object]:
    try:
        contracts.validate_contract("run-manifest-v1", payload)
    except (TypeError, ValueError, ValidationError) as error:
        raise _manifest_error(error)
    if not isinstance(payload, dict):
        raise _manifest_error()
    phase = payload["phase"]
    if not isinstance(phase, str) or phase not in PHASE_SPECS:
        raise _manifest_error()
    spec = PHASE_SPECS[phase]
    if (
        payload["nextAction"] != spec.next_action
        or len(payload["manifestChain"]) != spec.chain_length
    ):
        raise _manifest_error()

    sources = payload["sources"]
    assert isinstance(sources, list)
    source_order = [(source["camera"], source["mediaId"]) for source in sources]
    media_ids = [source["mediaId"] for source in sources]
    if source_order != sorted(source_order) or len(media_ids) != len(set(media_ids)):
        raise _manifest_error()

    artifacts = payload["artifacts"]
    assert isinstance(artifacts, dict)
    expected_artifacts = dict(spec.artifacts)
    if set(artifacts) != set(expected_artifacts):
        raise _manifest_error()
    for logical_name, file_name in spec.artifacts:
        artifact = artifacts[logical_name]
        if not isinstance(artifact, Mapping) or artifact["fileName"] != file_name:
            raise _manifest_error()

    stages = payload["stages"]
    assert isinstance(stages, list)
    if [stage["name"] for stage in stages] != list(spec.stages):
        raise _manifest_error()
    for stage, expected_name in zip(stages, spec.stages, strict=True):
        assert isinstance(stage, Mapping)
        output_hashes = stage["outputHashes"]
        expected_logical = dict(zip(spec.stages, spec.artifacts, strict=True))[
            expected_name
        ][0]
        if output_hashes != {
            expected_logical: artifacts[expected_logical]["sha256"]
        }:
            raise _manifest_error()
    return payload


def build_manifest(
    *,
    run_id: str,
    profile_id: str,
    binding_id: str,
    phase: str,
    manifest_chain: Sequence[str],
    sources: Sequence[Mapping[str, object]],
    stages: Sequence[Mapping[str, object]],
    artifacts: Mapping[str, Mapping[str, str]],
) -> dict[str, object]:
    """Build one path-free immutable run receipt from completed stage facts."""

    try:
        spec = PHASE_SPECS[phase]
        source_copies = [copy.deepcopy(dict(source)) for source in sources]
        source_copies.sort(key=lambda source: (source["camera"], source["mediaId"]))
        stage_by_name = {
            stage["name"]: copy.deepcopy(dict(stage)) for stage in stages
        }
        if len(stage_by_name) != len(stages):
            raise ValueError
        artifact_copies = {
            logical_name: copy.deepcopy(dict(artifacts[logical_name]))
            for logical_name, _ in spec.artifacts
        }
        payload: dict[str, object] = {
            "schemaVersion": "tritrack.run-manifest/v1",
            "toolVersion": __version__,
            "runId": run_id,
            "profileId": profile_id,
            "bindingId": binding_id,
            "phase": phase,
            "nextAction": spec.next_action,
            "manifestChain": list(manifest_chain),
            "sources": source_copies,
            "artifacts": artifact_copies,
            "stages": [stage_by_name[name] for name in spec.stages],
        }
    except (KeyError, TypeError, ValueError) as error:
        raise _manifest_error(error)
    return _validate_manifest(payload)


def encode_manifest(payload: object) -> bytes:
    """Return canonical UTF-8 bytes for one semantically strict manifest."""

    validated = _validate_manifest(payload)
    return (
        json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
            raise ValueError(code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(limit + 1)
        if len(encoded) > limit:
            raise ValueError(code)
        return encoded
    except OSError as error:
        raise ValueError(code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _validate_json_artifact(
    encoded: bytes, *, contract: str, code: str
) -> object:
    try:
        payload = json.loads(
            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
        )
        contracts.validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(code) from error
    return payload


def _validate_artifact(
    logical_name: str,
    encoded: bytes,
    *,
    manifest: Mapping[str, object],
) -> None:
    contracts_by_name = {
        "syncMap": "sync-map-v1",
        "transcriptBundle": "transcript-bundle-v1",
        "alignedTranscript": "aligned-transcript-v1",
        "grouping": "grouping-v1",
        "workingCut": "working-cut-v1",
    }
    contract = contracts_by_name.get(logical_name)
    if contract is not None:
        _validate_json_artifact(
            encoded, contract=contract, code="TRITRACK_RUN_ARTIFACT_INVALID"
        )
        return
    if logical_name == "doctorReceipt":
        try:
            payload = json.loads(encoded.decode("utf-8", errors="strict"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
        if (
            not isinstance(payload, dict)
            or payload.get("schemaVersion") != "tritrack.doctor-receipt/v1"
            or payload.get("profileId") != manifest["profileId"]
            or payload.get("titleBindingId") != manifest["bindingId"]
            or not isinstance(payload.get("supported"), bool)
            or not isinstance(payload.get("checks"), list)
            or not isinstance(payload.get("remediation"), list)
        ):
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID")
        return
    if logical_name in {"stringOut", "storyCut"}:
        try:
            text = encoded.decode("utf-8", errors="strict")
            emit_fcpxml.validate_fcpxml(
                text,
                profile=doctor.load_profile(str(manifest["profileId"])),
                binding=doctor.load_title_binding(str(manifest["bindingId"])),
            )
        except (UnicodeError, TypeError, ValueError, ValidationError) as error:
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error


def _bundle_directory(path: Path) -> Path:
    selected = Path(path)
    try:
        metadata = selected.lstat()
    except OSError as error:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
    return selected


def load_bundle(
    path: Path, *, expected_phase: str | None = None
) -> LoadedRunBundle:
    """Load and verify one complete immutable run bundle."""

    root = _bundle_directory(path)
    manifest_path = root / MANIFEST_FILE_NAME
    if not os.path.lexists(manifest_path):
        raise ValueError("TRITRACK_RUN_BUNDLE_INCOMPLETE")
    manifest_bytes = _read_regular_bytes(
        manifest_path,
        limit=_MANIFEST_LIMIT_BYTES,
        code="TRITRACK_RUN_MANIFEST_INVALID",
    )
    try:
        payload = json.loads(manifest_bytes.decode("utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_RUN_MANIFEST_INVALID") from error
    manifest = _validate_manifest(payload)
    if manifest_bytes != encode_manifest(manifest):
        raise ValueError("TRITRACK_RUN_MANIFEST_NONCANONICAL")
    if expected_phase is not None and manifest["phase"] != expected_phase:
        raise ValueError("TRITRACK_RUN_PHASE_MISMATCH")

    artifacts_payload = manifest["artifacts"]
    assert isinstance(artifacts_payload, Mapping)
    expected_entries = {MANIFEST_FILE_NAME}
    expected_entries.update(
        str(artifact["fileName"]) for artifact in artifacts_payload.values()
    )
    try:
        observed_entries = {entry.name for entry in os.scandir(root)}
    except OSError as error:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
    if observed_entries != expected_entries:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")

    loaded: dict[str, LoadedRunArtifact] = {}
    for logical_name, artifact_payload in artifacts_payload.items():
        assert isinstance(artifact_payload, Mapping)
        file_name = str(artifact_payload["fileName"])
        encoded = _read_regular_bytes(
            root / file_name,
            limit=_ARTIFACT_LIMIT_BYTES,
            code="TRITRACK_RUN_ARTIFACT_INVALID",
        )
        observed_hash = hashlib.sha256(encoded).hexdigest()
        if observed_hash != artifact_payload["sha256"]:
            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
        _validate_artifact(logical_name, encoded, manifest=manifest)
        loaded[logical_name] = LoadedRunArtifact(
            logical_name=logical_name,
            file_name=file_name,
            path=root / file_name,
            encoded=encoded,
            sha256=observed_hash,
        )
    return LoadedRunBundle(
        root=root,
        manifest=manifest,
        manifest_bytes=manifest_bytes,
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
        artifacts=loaded,
    )


def summarize_bundle(bundle: LoadedRunBundle) -> dict[str, object]:
    """Return a path-free and text-free status projection."""

    if not isinstance(bundle, LoadedRunBundle):
        raise TypeError("TRITRACK_RUN_BUNDLE_INVALID")
    return {
        "schemaVersion": "tritrack.run-summary/v1",
        "runId": bundle.manifest["runId"],
        "phase": bundle.manifest["phase"],
        "nextAction": bundle.manifest["nextAction"],
        "stages": [stage["name"] for stage in bundle.manifest["stages"]],
        "artifacts": {
            logical_name: artifact.sha256
            for logical_name, artifact in bundle.artifacts.items()
        },
    }


def _write_manifest(path: Path, encoded: bytes) -> None:
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


def _verify_staging(staging: Path, manifest: Mapping[str, object]) -> None:
    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, Mapping)
    expected = {str(artifact["fileName"]) for artifact in artifacts.values()}
    observed = {entry.name for entry in os.scandir(staging)}
    if observed != expected:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
    for logical_name, artifact in artifacts.items():
        assert isinstance(artifact, Mapping)
        encoded = _read_regular_bytes(
            staging / str(artifact["fileName"]),
            limit=_ARTIFACT_LIMIT_BYTES,
            code="TRITRACK_RUN_ARTIFACT_INVALID",
        )
        if hashlib.sha256(encoded).hexdigest() != artifact["sha256"]:
            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
        _validate_artifact(str(logical_name), encoded, manifest=manifest)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_bundle(
    output_dir: Path,
    builder: Callable[[Path], Mapping[str, object]],
) -> LoadedRunBundle:
    """Build privately, then hard-link a complete absent bundle manifest last."""

    destination = process.require_absent_output(output_dir)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-", dir=destination.parent
        )
    )
    reserved = False
    linked: list[Path] = []
    try:
        manifest = _validate_manifest(builder(staging))
        _verify_staging(staging, manifest)
        manifest_bytes = encode_manifest(manifest)
        _write_manifest(staging / MANIFEST_FILE_NAME, manifest_bytes)
        try:
            os.mkdir(destination, 0o755)
            reserved = True
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error

        artifacts = manifest["artifacts"]
        assert isinstance(artifacts, Mapping)
        file_names = sorted(
            str(artifact["fileName"]) for artifact in artifacts.values()
        )
        for file_name in (*file_names, MANIFEST_FILE_NAME):
            target = destination / file_name
            os.link(staging / file_name, target)
            linked.append(target)
        _fsync_directory(destination)
        return load_bundle(destination, expected_phase=str(manifest["phase"]))
    except BaseException:
        if reserved:
            for path in reversed(linked):
                try:
                    path.unlink()
                except OSError:
                    pass
            try:
                destination.rmdir()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
