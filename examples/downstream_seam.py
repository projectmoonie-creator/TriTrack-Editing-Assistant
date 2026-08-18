"""Black-box example of TriTrack's supported downstream process seam."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import NoReturn

MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
VALIDATE_SUMMARY_SCHEMA = "tritrack.validate-summary/v1"
ALIGNED_CONTRACT = "aligned-transcript-v1"
ALIGNED_SCHEMA = "tritrack.aligned-transcript/v1"


class DownstreamError(ValueError):
    """A stable, path-free error suitable for example automation."""


def _canonical_json(payload: Mapping[str, object]) -> bytes:
    return (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _read_regular(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= MAX_ARTIFACT_BYTES
        ):
            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(MAX_ARTIFACT_BYTES + 1)
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(encoded) > MAX_ARTIFACT_BYTES:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    return encoded


def _validate(tritrack: Path, aligned: Path) -> dict[str, object]:
    try:
        result = subprocess.run(
            [
                os.fspath(tritrack),
                "validate",
                "contract",
                "--artifact",
                os.fspath(aligned),
                "--json",
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise DownstreamError(
            "DOWNSTREAM_ENGINE_VALIDATION_FAILED"
        ) from error
    if result.returncode != 0 or result.stderr:
        raise DownstreamError("DOWNSTREAM_ENGINE_VALIDATION_FAILED")
    try:
        decoded = result.stdout.decode("utf-8", errors="strict")
        summary = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID") from error
    if not isinstance(summary, dict):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    if (
        summary.get("schemaVersion") != VALIDATE_SUMMARY_SCHEMA
        or summary.get("artifactKind") != "contract"
        or summary.get("validationScope") != "contract"
        or summary.get("details")
        != {
            "contractName": ALIGNED_CONTRACT,
            "contractSchemaVersion": ALIGNED_SCHEMA,
        }
    ):
        raise DownstreamError("DOWNSTREAM_ENGINE_SCOPE_INVALID")
    hashes = summary.get("hashes")
    if not isinstance(hashes, dict):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    artifact_hash = hashes.get("artifact")
    if (
        not isinstance(artifact_hash, str)
        or len(artifact_hash) != 64
        or any(character not in "0123456789abcdef" for character in artifact_hash)
    ):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    return summary


def _observe(encoded: bytes) -> tuple[int, int]:
    try:
        artifact = json.loads(encoded.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    if not isinstance(artifact, dict) or artifact.get("schemaVersion") != ALIGNED_SCHEMA:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    takes = artifact.get("takes")
    if not isinstance(takes, list):
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    cue_count = 0
    for take in takes:
        if not isinstance(take, dict) or not isinstance(take.get("cues"), list):
            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
        cue_count += len(take["cues"])
    return len(takes), cue_count


def _publish_absent(path: Path, payload: Mapping[str, object]) -> None:
    parent = path.parent
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            dir=parent,
            prefix=f".{path.name}.",
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary_path, path, follow_symlinks=False)
    except FileExistsError as error:
        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS") from error
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_OUTPUT_INVALID") from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def _artifact_hash(summary: Mapping[str, object]) -> str:
    hashes = summary["hashes"]
    assert isinstance(hashes, dict)
    artifact_hash = hashes["artifact"]
    assert isinstance(artifact_hash, str)
    return artifact_hash


def _run(tritrack: Path, aligned: Path, output: Path) -> dict[str, object]:
    if os.path.lexists(output):
        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS")

    first_summary = _validate(tritrack, aligned)
    encoded = _read_regular(aligned)
    artifact_sha256 = hashlib.sha256(encoded).hexdigest()
    if _artifact_hash(first_summary) != artifact_sha256:
        raise DownstreamError("DOWNSTREAM_ENGINE_HASH_MISMATCH")

    take_count, cue_count = _observe(encoded)
    second_summary = _validate(tritrack, aligned)
    if second_summary != first_summary:
        raise DownstreamError("DOWNSTREAM_ENGINE_CHANGED")

    receipt: dict[str, object] = {
        "schemaVersion": "example.tritrack-downstream-receipt/v1",
        "engineAuthority": {
            "artifactSha256": artifact_sha256,
            "contractName": ALIGNED_CONTRACT,
            "contractSchemaVersion": ALIGNED_SCHEMA,
            "validationScope": "contract",
        },
        "derivedObservation": {
            "takeCount": take_count,
            "cueCount": cue_count,
        },
    }
    _publish_absent(output, receipt)
    return {
        "schemaVersion": "example.tritrack-downstream-summary/v1",
        "artifactSha256": artifact_sha256,
        "takeCount": take_count,
        "cueCount": cue_count,
    }


def _fail(error: DownstreamError) -> NoReturn:
    sys.stderr.buffer.write(_canonical_json({"error": str(error)}))
    raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prove the public TriTrack CLI/artifact downstream seam."
    )
    parser.add_argument("--tritrack", required=True, type=Path)
    parser.add_argument("--aligned", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        summary = _run(arguments.tritrack, arguments.aligned, arguments.output)
    except DownstreamError as error:
        _fail(error)
    sys.stdout.buffer.write(_canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
