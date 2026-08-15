"""Offline Gemini receipt conformance for deterministic cue promotion."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from . import align_text
from .process import require_absent_output


def _validate_exact_model(exact_model: str) -> None:
    if (
        not isinstance(exact_model, str)
        or not exact_model
        or len(exact_model) > 256
        or any(character.isspace() for character in exact_model)
    ):
        raise ValueError("TRITRACK_HYBRID_MODEL_INVALID")


def _revised_take_sources(revision: object) -> dict[str, str]:
    assert isinstance(revision, Mapping)
    takes = revision["takes"]
    assert isinstance(takes, list)
    sources: dict[str, str] = {}
    for take in takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        source_sha256 = take["sourceSha256"]
        assert isinstance(take_id, str)
        assert isinstance(source_sha256, str)
        sources[take_id] = source_sha256
    return sources


def _receipt_take_id(receipt: align_text.LoadedJsonArtifact) -> str:
    payload = receipt.payload
    assert isinstance(payload, Mapping)
    take_id = payload["takeId"]
    assert isinstance(take_id, str)
    return take_id


def _is_success_status(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 200 <= value < 300


def _validate_receipt(
    receipt: align_text.LoadedJsonArtifact,
    *,
    source_bundle_sha256: str,
    take_id: str,
    source_sha256: str,
    exact_model: str,
) -> None:
    payload = receipt.payload
    assert isinstance(payload, Mapping)
    upload = payload["upload"]
    deletion = payload["serverFileDeletion"]
    assert isinstance(upload, Mapping)
    assert isinstance(deletion, Mapping)

    if not (
        payload["provider"] == "gemini"
        and payload["sourceBundleSha256"] == source_bundle_sha256
        and payload["takeId"] == take_id
        and payload["audioSha256"] == source_sha256
        and payload["requestedModel"] == exact_model
        and payload["observedModel"] == exact_model
        and payload["requestStatus"] == "completed"
        and _is_success_status(payload["responseStatus"])
        and upload["status"] == "completed"
        and upload["serverFileIdSha256"] is not None
        and deletion["attempted"] is True
        and deletion["confirmed"] is True
        and _is_success_status(deletion["statusCode"])
    ):
        raise ValueError("TRITRACK_HYBRID_RECEIPT_REJECTED")


def hybrid_and_publish(
    transcript_path: Path,
    revision_path: Path,
    receipt_paths: Sequence[Path],
    *,
    exact_model: str,
    output_path: Path,
) -> dict[str, object]:
    """Validate offline receipts, then publish through the local aligner."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    _validate_exact_model(exact_model)
    if isinstance(receipt_paths, (str, bytes)) or not isinstance(
        receipt_paths, Sequence
    ):
        raise TypeError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")

    aligned, alignment_inputs = align_text.prepare_alignment(
        transcript_path, revision_path
    )
    transcript, revision = alignment_inputs
    revised_sources = _revised_take_sources(revision.payload)

    receipts = [
        align_text.load_json_artifact(
            Path(path),
            contract="provider-receipt-v1",
            invalid_code="TRITRACK_HYBRID_RECEIPT_INVALID",
        )
        for path in receipt_paths
    ]
    receipts_by_take: dict[str, align_text.LoadedJsonArtifact] = {}
    for receipt in receipts:
        take_id = _receipt_take_id(receipt)
        if take_id in receipts_by_take:
            raise ValueError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")
        receipts_by_take[take_id] = receipt
    if set(receipts_by_take) != set(revised_sources):
        raise ValueError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")

    for take_id, source_sha256 in revised_sources.items():
        _validate_receipt(
            receipts_by_take[take_id],
            source_bundle_sha256=transcript.sha256,
            take_id=take_id,
            source_sha256=source_sha256,
            exact_model=exact_model,
        )

    for artifact in (*alignment_inputs, *receipts):
        align_text.verify_artifact_unchanged(artifact)
    align_text.publish_aligned_transcript(aligned, destination)
    return aligned
