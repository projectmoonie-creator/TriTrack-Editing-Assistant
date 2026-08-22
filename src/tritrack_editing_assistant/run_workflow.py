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

from . import (
    __version__,
    align_text,
    contracts,
    doctor,
    emit_fcpxml,
    organizer,
    paper_edit,
    process,
    story_fcpxml,
    sync_scan,
    transcription_result,
)

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
    stage_outputs: tuple[tuple[str, tuple[str, ...]], ...]


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
        stage_outputs=(
            ("doctor", ("doctorReceipt",)),
            ("sync", ("syncMap",)),
            ("transcribe", ("transcriptBundle",)),
            ("emit", ("stringOut",)),
        ),
    ),
    "aligned": PhaseSpec(
        next_action="edit-paper-workbook",
        chain_length=1,
        artifacts=(
            ("alignedTranscript", "aligned-transcript.json"),
            ("paperWorkbook", "paper-edit.xlsx"),
        ),
        stages=("align", "paper"),
        stage_outputs=(
            ("align", ("alignedTranscript",)),
            ("paper", ("paperWorkbook",)),
        ),
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
        stage_outputs=(
            ("paper", ("grouping",)),
            ("organize", ("workingCut",)),
            ("emit", ("storyCut",)),
        ),
    ),
}

_V2_PREPARED_SPEC = PhaseSpec(
    next_action="provide-revision",
    chain_length=0,
    artifacts=(
        ("doctorReceipt", "doctor.json"),
        ("syncMap", "sync-map.json"),
        ("transcriptBundle", "transcript-bundle.json"),
        ("transcriptionReport", "transcription-report.json"),
        ("transcriptionResult", "transcription-result-manifest.json"),
        ("stringOut", "string-out.fcpxml"),
    ),
    stages=("doctor", "sync", "transcribe", "emit"),
    stage_outputs=(
        ("doctor", ("doctorReceipt",)),
        ("sync", ("syncMap",)),
        (
            "transcribe",
            ("transcriptBundle", "transcriptionReport", "transcriptionResult"),
        ),
        ("emit", ("stringOut",)),
    ),
)
_RUN_MANIFEST_V1 = "tritrack.run-manifest/v1"
_RUN_MANIFEST_V2 = "tritrack.run-manifest/v2"


def _phase_spec(schema_version: str, phase: str) -> PhaseSpec:
    if schema_version not in {_RUN_MANIFEST_V1, _RUN_MANIFEST_V2}:
        raise _manifest_error()
    try:
        if schema_version == _RUN_MANIFEST_V2 and phase == "prepared":
            return _V2_PREPARED_SPEC
        return PHASE_SPECS[phase]
    except KeyError as error:
        raise _manifest_error(error)


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
        if not isinstance(payload, dict):
            raise TypeError
        schema_version = payload.get("schemaVersion")
        contract = contracts.contract_name_for_schema_version(schema_version)
        if contract not in {"run-manifest-v1", "run-manifest-v2"}:
            raise ValueError
        contracts.validate_contract(contract, payload)
    except (TypeError, ValueError, ValidationError) as error:
        raise _manifest_error(error)
    phase = payload["phase"]
    if not isinstance(phase, str) or phase not in PHASE_SPECS:
        raise _manifest_error()
    assert isinstance(schema_version, str)
    spec = _phase_spec(schema_version, phase)
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
    stage_outputs = dict(spec.stage_outputs)
    for stage, expected_name in zip(stages, spec.stages, strict=True):
        assert isinstance(stage, Mapping)
        output_hashes = stage["outputHashes"]
        expected_hashes = {
            logical_name: artifacts[logical_name]["sha256"]
            for logical_name in stage_outputs[expected_name]
        }
        if output_hashes != expected_hashes:
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
    schema_version: str = _RUN_MANIFEST_V1,
) -> dict[str, object]:
    """Build one path-free immutable run receipt from completed stage facts."""

    try:
        spec = _phase_spec(schema_version, phase)
        expected_artifacts = {logical_name for logical_name, _ in spec.artifacts}
        if set(artifacts) != expected_artifacts:
            raise ValueError
        source_copies = [copy.deepcopy(dict(source)) for source in sources]
        source_copies.sort(key=lambda source: (source["camera"], source["mediaId"]))
        stage_by_name = {
            stage["name"]: copy.deepcopy(dict(stage)) for stage in stages
        }
        if (
            len(stage_by_name) != len(stages)
            or set(stage_by_name) != set(spec.stages)
        ):
            raise ValueError
        artifact_copies = {
            logical_name: copy.deepcopy(dict(artifacts[logical_name]))
            for logical_name, _ in spec.artifacts
        }
        payload: dict[str, object] = {
            "schemaVersion": schema_version,
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
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
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
    if logical_name == "syncMap":
        try:
            payload = json.loads(encoded.decode("utf-8", errors="strict"))
            if not isinstance(payload, dict):
                raise TypeError
            contract = contracts.contract_name_for_schema_version(
                payload.get("schemaVersion")
            )
            if contract not in {"sync-map-v1", "sync-map-v2"}:
                raise ValueError
            contracts.validate_contract(contract, payload)
        except (
            UnicodeError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
            ValidationError,
        ) as error:
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
        return
    contracts_by_name = {
        "transcriptBundle": "transcript-bundle-v1",
        "transcriptionReport": "transcription-report-v1",
        "transcriptionResult": "transcription-result-manifest-v1",
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


def _validate_transcription_authority(
    artifacts: Mapping[str, bytes],
) -> None:
    names = {"transcriptBundle", "transcriptionReport", "transcriptionResult"}
    present = names.intersection(artifacts)
    if not present:
        return
    if present != names:
        raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID")
    try:
        result = json.loads(artifacts["transcriptionResult"].decode("utf-8"))
        if not isinstance(result, dict):
            raise TypeError
        bundle = result["bundle"]
        report = result["report"]
        if not isinstance(bundle, dict) or not isinstance(report, dict):
            raise TypeError
        if (
            bundle["fileName"] != "transcript-bundle.json"
            or report["fileName"] != "transcription-report.json"
            or bundle["sha256"]
            != hashlib.sha256(artifacts["transcriptBundle"]).hexdigest()
            or report["sha256"]
            != hashlib.sha256(artifacts["transcriptionReport"]).hexdigest()
        ):
            raise ValueError
    except (
        KeyError,
        TypeError,
        ValueError,
        UnicodeError,
        json.JSONDecodeError,
    ) as error:
        raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error


def _bundle_directory(path: Path) -> Path:
    selected = Path(path)
    try:
        metadata = selected.lstat()
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_RUN_INPUT_UNREADABLE") from error
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
    _validate_transcription_authority(
        {logical_name: artifact.encoded for logical_name, artifact in loaded.items()}
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
    encoded_artifacts: dict[str, bytes] = {}
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
        encoded_artifacts[str(logical_name)] = encoded
    _validate_transcription_authority(encoded_artifacts)


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


def _hash_regular_path(path: Path, *, code: str) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    digest = hashlib.sha256()
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
            raise ValueError(code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            while chunk := stream.read(_HASH_CHUNK_BYTES):
                digest.update(chunk)
    except OSError as error:
        raise ValueError(code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return digest.hexdigest()


def _hash_value(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _artifact_records(
    staging: Path,
    phase: str,
    *,
    schema_version: str = _RUN_MANIFEST_V1,
) -> dict[str, dict[str, str]]:
    return {
        logical_name: {
            "fileName": file_name,
            "sha256": _hash_regular_path(
                staging / file_name, code="TRITRACK_RUN_ARTIFACT_INVALID"
            ),
        }
        for logical_name, file_name in _phase_spec(schema_version, phase).artifacts
    }


def _source_inventory(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    transcribe_media: Sequence[Path],
) -> tuple[list[dict[str, object]], dict[Path, str]]:
    if not camera_a_sources or not camera_b_sources:
        raise ValueError("TRITRACK_RUN_SOURCE_REQUIRED")
    declared: list[tuple[str, sync_scan.MediaSource]] = [
        *(("A", source) for source in camera_a_sources),
        *(("B", source) for source in camera_b_sources),
    ]
    media_ids = [source.media_id for _, source in declared]
    if (
        len(media_ids) != len(set(media_ids))
        or any(source.media_id != source.path.name for _, source in declared)
    ):
        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
    declared_paths = [source.path for _, source in declared]
    if len(declared_paths) != len(set(declared_paths)):
        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
    selected_transcribe = [Path(path) for path in transcribe_media]
    if (
        not selected_transcribe
        or len(selected_transcribe) != len(set(selected_transcribe))
        or any(path not in declared_paths for path in selected_transcribe)
    ):
        raise ValueError("TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID")
    source_hashes = {
        source.path: _hash_regular_path(
            source.path, code="TRITRACK_RUN_INPUT_UNREADABLE"
        )
        for _, source in declared
    }
    selected_set = set(selected_transcribe)
    inventory = [
        {
            "camera": camera,
            "mediaId": source.media_id,
            "sha256": source_hashes[source.path],
            "transcribed": source.path in selected_set,
        }
        for camera, source in declared
    ]
    return inventory, source_hashes


def _require_inputs_unchanged(
    source_hashes: Mapping[Path, str], *, model_path: Path, model_sha256: str
) -> None:
    if _hash_regular_path(
        model_path, code="TRITRACK_RUN_INPUT_CHANGED"
    ) != model_sha256 or any(
        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
        for path, expected in source_hashes.items()
    ):
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def _transcription_alternatives(
    sync_payload: Mapping[str, object],
    selected: Sequence[Path],
    *,
    source_paths: Mapping[str, Path],
) -> dict[str, tuple[Path, ...]]:
    if sync_payload.get("schemaVersion") != "tritrack.sync-map/v2":
        raise ValueError("TRITRACK_RUN_SYNC_MAP_INVALID")
    groups = sync_payload.get("groups")
    memberships: dict[str, tuple[str, ...]] = {}
    try:
        if not isinstance(groups, list):
            raise TypeError
        for group in groups:
            if not isinstance(group, Mapping):
                raise TypeError
            anchor = group["anchor"]
            sources = group["sources"]
            if not isinstance(anchor, Mapping) or not isinstance(sources, list):
                raise TypeError
            members = (
                str(anchor["mediaId"]),
                *(
                    str(source["mediaId"])
                    for source in sources
                    if isinstance(source, Mapping)
                ),
            )
            if len(members) != len(sources) + 1:
                raise TypeError
            for media_id in members:
                if media_id in memberships:
                    raise ValueError
                memberships[media_id] = members
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_RUN_SYNC_MAP_INVALID") from error

    alternatives: dict[str, tuple[Path, ...]] = {}
    for primary in selected:
        members = memberships.get(primary.name, ())
        try:
            candidates = tuple(
                source_paths[media_id]
                for media_id in members
                if media_id != primary.name
            )
        except KeyError as error:
            raise ValueError("TRITRACK_RUN_SYNC_MAP_INVALID") from error
        if candidates:
            alternatives[primary.name] = candidates
    return alternatives


def prepare_run(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    transcribe_media: Sequence[Path],
    *,
    model_path: Path,
    language: str,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
    run_id: str,
    output_dir: Path,
) -> dict[str, object]:
    """Publish a doctor／sync／transcript／string-out prepared run bundle."""

    process.require_absent_output(output_dir)
    inventory, source_hashes = _source_inventory(
        camera_a_sources, camera_b_sources, transcribe_media
    )
    selected_model = Path(model_path)
    model_sha256 = _hash_regular_path(
        selected_model, code="TRITRACK_RUN_INPUT_UNREADABLE"
    )
    selected_transcribe = [Path(path) for path in transcribe_media]
    profile_hash = _hash_value(doctor.load_profile(profile_id))
    binding_hash = _hash_value(doctor.load_title_binding(binding_id))
    source_set_hash = _hash_value(inventory)
    source_paths = {
        source.media_id: source.path
        for source in (*camera_a_sources, *camera_b_sources)
    }

    def build(staging: Path) -> dict[str, object]:
        receipt = doctor.write_receipt(
            staging / "doctor.json",
            profile_id=profile_id,
            transcription_requested=True,
            whisper_model=selected_model,
        )
        if receipt.get("supported") is not True:
            raise ValueError("TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED")
        sync_payload = sync_scan.synchronize_and_publish(
            camera_a_sources,
            camera_b_sources,
            profile_id=profile_id,
            output_path=staging / "sync-map.json",
        )
        result = transcription_result.transcribe_local_result(
            selected_transcribe,
            alternative_paths=_transcription_alternatives(
                sync_payload,
                selected_transcribe,
                source_paths=source_paths,
            ),
            model_path=selected_model,
            language=language,
        )
        _write_manifest(staging / "transcript-bundle.json", result.bundle_bytes)
        _write_manifest(
            staging / "transcription-report.json", result.report_bytes
        )
        _write_manifest(
            staging / "transcription-result-manifest.json",
            result.manifest_bytes,
        )
        selected_hashes = {
            take["selectedSourceSha256"]
            for take in result.report["takes"]
            if take["status"] in {"completed", "empty", "reused"}
        }
        prepared_inventory = [
            {**source, "transcribed": source["sha256"] in selected_hashes}
            for source in inventory
        ]
        transcribed_hash = _hash_value(
            [
                source
                for source in sorted(
                    prepared_inventory, key=lambda item: item["mediaId"]
                )
                if source["transcribed"]
            ]
        )
        emit_fcpxml.emit_and_publish(
            camera_a_sources,
            camera_b_sources,
            sync_map_path=staging / "sync-map.json",
            profile_id=profile_id,
            binding_id=binding_id,
            metadata=metadata,
            output_path=staging / "string-out.fcpxml",
        )
        _require_inputs_unchanged(
            source_hashes, model_path=selected_model, model_sha256=model_sha256
        )
        artifacts = _artifact_records(
            staging, "prepared", schema_version=_RUN_MANIFEST_V2
        )
        stages = [
            {
                "name": "doctor",
                "inputHashes": {
                    "binding": binding_hash,
                    "model": model_sha256,
                    "profile": profile_hash,
                },
                "outputHashes": {
                    "doctorReceipt": artifacts["doctorReceipt"]["sha256"]
                },
            },
            {
                "name": "sync",
                "inputHashes": {"sourceSet": source_set_hash},
                "outputHashes": {"syncMap": artifacts["syncMap"]["sha256"]},
            },
            {
                "name": "transcribe",
                "inputHashes": {
                    "model": model_sha256,
                    "transcribedSources": transcribed_hash,
                },
                "outputHashes": {
                    logical_name: artifacts[logical_name]["sha256"]
                    for logical_name in (
                        "transcriptBundle",
                        "transcriptionReport",
                        "transcriptionResult",
                    )
                },
            },
            {
                "name": "emit",
                "inputHashes": {
                    "binding": binding_hash,
                    "profile": profile_hash,
                    "sourceSet": source_set_hash,
                    "syncMap": artifacts["syncMap"]["sha256"],
                },
                "outputHashes": {"stringOut": artifacts["stringOut"]["sha256"]},
            },
        ]
        return build_manifest(
            run_id=run_id,
            profile_id=profile_id,
            binding_id=binding_id,
            phase="prepared",
            manifest_chain=[],
            sources=prepared_inventory,
            stages=stages,
            artifacts=artifacts,
            schema_version=_RUN_MANIFEST_V2,
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def _require_bundle_unchanged(bundle: LoadedRunBundle) -> None:
    try:
        current = load_bundle(bundle.root, expected_phase=str(bundle.manifest["phase"]))
    except ValueError as error:
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED") from error
    if current.manifest_sha256 != bundle.manifest_sha256:
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def align_run(
    prepared_dir: Path,
    revision_path: Path,
    *,
    output_dir: Path,
) -> dict[str, object]:
    """Consume one complete prepared run and publish an aligned paper bundle."""

    process.require_absent_output(output_dir)
    prepared = load_bundle(prepared_dir, expected_phase="prepared")
    revision = align_text.load_json_artifact(
        Path(revision_path),
        contract="text-revision-v1",
        invalid_code="TRITRACK_ALIGNMENT_REVISION_INVALID",
    )

    def build(staging: Path) -> dict[str, object]:
        align_text.align_and_publish(
            prepared.artifacts["transcriptBundle"].path,
            revision.path,
            output_path=staging / "aligned-transcript.json",
        )
        paper_edit.export_workbook(
            staging / "aligned-transcript.json",
            grouping_path=None,
            output_path=staging / "paper-edit.xlsx",
        )
        align_text.verify_artifact_unchanged(revision)
        _require_bundle_unchanged(prepared)
        artifacts = _artifact_records(staging, "aligned")
        stages = [
            {
                "name": "align",
                "inputHashes": {
                    "preparedManifest": prepared.manifest_sha256,
                    "revision": revision.sha256,
                    "transcriptBundle": prepared.artifacts[
                        "transcriptBundle"
                    ].sha256,
                },
                "outputHashes": {
                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
                },
            },
            {
                "name": "paper",
                "inputHashes": {
                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
                },
                "outputHashes": {
                    "paperWorkbook": artifacts["paperWorkbook"]["sha256"]
                },
            },
        ]
        return build_manifest(
            run_id=str(prepared.manifest["runId"]),
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            phase="aligned",
            manifest_chain=[prepared.manifest_sha256],
            sources=prepared.manifest["sources"],
            stages=stages,
            artifacts=artifacts,
            schema_version=str(prepared.manifest["schemaVersion"]),
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def _finish_source_hashes(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    expected_sources: object,
) -> dict[Path, str]:
    if not camera_a_sources or not camera_b_sources:
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    declared: list[tuple[str, sync_scan.MediaSource]] = [
        *(("A", source) for source in camera_a_sources),
        *(("B", source) for source in camera_b_sources),
    ]
    media_ids = [source.media_id for _, source in declared]
    paths = [source.path for _, source in declared]
    if (
        len(media_ids) != len(set(media_ids))
        or len(paths) != len(set(paths))
        or any(source.media_id != source.path.name for _, source in declared)
    ):
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    try:
        hashes = {
            source.path: _hash_regular_path(
                source.path, code="TRITRACK_RUN_SOURCE_MISMATCH"
            )
            for _, source in declared
        }
        expected_by_id = {
            str(source["mediaId"]): source for source in expected_sources
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH") from error
    if set(media_ids) != set(expected_by_id):
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    for camera, source in declared:
        expected = expected_by_id[source.media_id]
        if (
            expected["camera"] != camera
            or expected["sha256"] != hashes[source.path]
        ):
            raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    return hashes


def _require_path_hashes_unchanged(path_hashes: Mapping[Path, str]) -> None:
    if any(
        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
        for path, expected in path_hashes.items()
    ):
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def _validate_finish_chain(
    prepared: LoadedRunBundle, aligned: LoadedRunBundle
) -> None:
    if aligned.manifest["manifestChain"] != [prepared.manifest_sha256]:
        raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")
    for field in (
        "schemaVersion",
        "runId",
        "profileId",
        "bindingId",
        "sources",
    ):
        if aligned.manifest[field] != prepared.manifest[field]:
            raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")


def finish_run(
    prepared_dir: Path,
    aligned_dir: Path,
    workbook_path: Path,
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    metadata: emit_fcpxml.ProjectMetadata,
    output_dir: Path,
) -> dict[str, object]:
    """Apply paper intent and publish one exact story-cut result bundle."""

    process.require_absent_output(output_dir)
    prepared = load_bundle(prepared_dir, expected_phase="prepared")
    aligned = load_bundle(aligned_dir, expected_phase="aligned")
    _validate_finish_chain(prepared, aligned)
    source_hashes = _finish_source_hashes(
        camera_a_sources,
        camera_b_sources,
        expected_sources=prepared.manifest["sources"],
    )
    selected_workbook = Path(workbook_path)
    workbook_sha256 = _hash_regular_path(
        selected_workbook, code="TRITRACK_PAPER_WORKBOOK_INVALID"
    )
    source_set_hash = _hash_value(prepared.manifest["sources"])

    def build(staging: Path) -> dict[str, object]:
        paper_edit.apply_workbook(
            aligned.artifacts["alignedTranscript"].path,
            selected_workbook,
            output_path=staging / "grouping.json",
        )
        organizer.organize_and_publish(
            aligned.artifacts["alignedTranscript"].path,
            staging / "grouping.json",
            output_path=staging / "working-cut.json",
        )
        story_fcpxml.emit_story_and_publish(
            camera_a_sources,
            camera_b_sources,
            sync_map_path=prepared.artifacts["syncMap"].path,
            aligned_path=aligned.artifacts["alignedTranscript"].path,
            grouping_path=staging / "grouping.json",
            working_cut_path=staging / "working-cut.json",
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            metadata=metadata,
            output_path=staging / "story-cut.fcpxml",
        )
        _require_bundle_unchanged(prepared)
        _require_bundle_unchanged(aligned)
        _require_path_hashes_unchanged(
            {**source_hashes, selected_workbook: workbook_sha256}
        )
        artifacts = _artifact_records(staging, "finished")
        stages = [
            {
                "name": "paper",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "workbook": workbook_sha256,
                },
                "outputHashes": {"grouping": artifacts["grouping"]["sha256"]},
            },
            {
                "name": "organize",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "grouping": artifacts["grouping"]["sha256"],
                },
                "outputHashes": {
                    "workingCut": artifacts["workingCut"]["sha256"]
                },
            },
            {
                "name": "emit",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "grouping": artifacts["grouping"]["sha256"],
                    "sourceSet": source_set_hash,
                    "syncMap": prepared.artifacts["syncMap"].sha256,
                    "workingCut": artifacts["workingCut"]["sha256"],
                },
                "outputHashes": {"storyCut": artifacts["storyCut"]["sha256"]},
            },
        ]
        return build_manifest(
            run_id=str(prepared.manifest["runId"]),
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            phase="finished",
            manifest_chain=[prepared.manifest_sha256, aligned.manifest_sha256],
            sources=prepared.manifest["sources"],
            stages=stages,
            artifacts=artifacts,
            schema_version=str(prepared.manifest["schemaVersion"]),
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def inspect_run(
    run_dir: Path,
) -> tuple[LoadedRunBundle, dict[str, object]]:
    """Validate, recheck, and summarize one run without writing anything."""

    bundle = load_bundle(Path(run_dir))
    _require_bundle_unchanged(bundle)
    return bundle, summarize_bundle(bundle)


def status_run(run_dir: Path) -> dict[str, object]:
    """Validate and summarize one run bundle without writing anything."""

    return inspect_run(run_dir)[1]
