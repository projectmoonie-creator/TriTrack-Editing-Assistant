"""Deterministic cue-addressed editorial grouping and compilation."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError

from . import hallucination
from .contracts import validate_contract
from .process import require_absent_output

ORGANIZATION_PROFILE_ID = "cue-addressed-question-groups-v1"
QUESTION_TEXT_LIMIT = 500
NOTE_TEXT_LIMIT = 2000
_JSON_LIMIT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class IndexedCue:
    cue_id: str
    start_ms: int
    end_ms: int


@dataclass(frozen=True)
class IndexedTake:
    take_id: str
    source_sha256: str
    status: str
    cues: tuple[IndexedCue, ...]
    cue_positions: Mapping[str, int]


@dataclass(frozen=True)
class AlignedIndex:
    takes: Mapping[str, IndexedTake]
    completed_take_order: tuple[str, ...]


@dataclass(frozen=True)
class LoadedJsonArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str


def _validate_contract(name: str, payload: object, code: str) -> None:
    try:
        validate_contract(name, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def canonical_editor_text(
    value: object,
    *,
    maximum: int,
    required: bool,
) -> str | None:
    """Normalize one bounded editor-authored field without interpreting it."""

    if value is None or value == "":
        if required:
            raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
        return None
    if not isinstance(value, str):
        raise TypeError("TRITRACK_ORGANIZER_TEXT_INVALID")
    if any(unicodedata.category(character).startswith("C") for character in value):
        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
    normalized = " ".join(unicodedata.normalize("NFC", value).split())
    if (required and not normalized) or not 0 < len(normalized) <= maximum:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
    return normalized


def index_aligned_transcript(payload: object) -> AlignedIndex:
    """Validate and index one canonical aligned transcript authority."""

    _validate_contract(
        "aligned-transcript-v1",
        payload,
        "TRITRACK_ORGANIZER_ALIGNED_INVALID",
    )
    assert isinstance(payload, Mapping)
    takes = payload["takes"]
    assert isinstance(takes, list)
    take_ids = [take["takeId"] for take in takes]
    if take_ids != sorted(take_ids) or len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")

    indexed: dict[str, IndexedTake] = {}
    completed_order: list[str] = []
    for take in takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        source_sha256 = take["sourceSha256"]
        status = take["status"]
        cues = take["cues"]
        assert isinstance(take_id, str)
        assert isinstance(source_sha256, str)
        assert isinstance(status, str)
        assert isinstance(cues, list)

        indexed_cues: list[IndexedCue] = []
        positions: dict[str, int] = {}
        previous_end = 0
        for position, cue in enumerate(cues):
            assert isinstance(cue, Mapping)
            cue_id = cue["cueId"]
            start_ms = cue["startMs"]
            end_ms = cue["endMs"]
            text = cue["text"]
            assert isinstance(cue_id, str)
            assert isinstance(start_ms, int)
            assert isinstance(end_ms, int)
            assert isinstance(text, str)
            if cue_id in positions or not (previous_end <= start_ms < end_ms):
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
            try:
                normalized_text = hallucination.normalize_cue_text(text)
            except (TypeError, ValueError) as error:
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID") from error
            if normalized_text != text:
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
            positions[cue_id] = position
            indexed_cues.append(IndexedCue(cue_id, start_ms, end_ms))
            previous_end = end_ms

        if status == "completed":
            completed_order.append(take_id)
        indexed[take_id] = IndexedTake(
            take_id=take_id,
            source_sha256=source_sha256,
            status=status,
            cues=tuple(indexed_cues),
            cue_positions=positions,
        )
    return AlignedIndex(indexed, tuple(completed_order))


def _require_permutation(items: list[object], field: str) -> None:
    orders = [item[field] for item in items]
    if orders != list(range(1, len(items) + 1)):
        raise ValueError("TRITRACK_ORGANIZER_ORDER_INVALID")


def _resolve_span(
    selection: Mapping[str, object],
    *,
    aligned_index: AlignedIndex,
) -> tuple[IndexedTake, int, int]:
    take_id = selection["takeId"]
    start_cue_id = selection["startCueId"]
    end_cue_id = selection["endCueId"]
    assert isinstance(take_id, str)
    assert isinstance(start_cue_id, str)
    assert isinstance(end_cue_id, str)
    take = aligned_index.takes.get(take_id)
    if take is None:
        raise ValueError("TRITRACK_ORGANIZER_TAKE_UNKNOWN")
    if take.status != "completed":
        raise ValueError("TRITRACK_ORGANIZER_TAKE_NOT_COMPLETED")
    start_position = take.cue_positions.get(start_cue_id)
    end_position = take.cue_positions.get(end_cue_id)
    if start_position is None or end_position is None:
        raise ValueError("TRITRACK_ORGANIZER_CUE_UNKNOWN")
    if start_position > end_position:
        raise ValueError("TRITRACK_ORGANIZER_SPAN_INVALID")
    return take, start_position, end_position


def _require_canonical_text(
    item: Mapping[str, object],
    field: str,
    *,
    maximum: int,
    required: bool,
) -> None:
    original = item.get(field)
    try:
        canonical = canonical_editor_text(
            original,
            maximum=maximum,
            required=required,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL") from error
    if canonical != original:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL")


def validate_grouping(
    payload: object,
    *,
    aligned_index: AlignedIndex,
    aligned_sha256: str,
) -> dict[str, object]:
    """Validate canonical editor intent against one exact aligned authority."""

    _validate_contract(
        "grouping-v1",
        payload,
        "TRITRACK_ORGANIZER_GROUPING_INVALID",
    )
    assert isinstance(payload, dict)
    if payload["alignedTranscriptSha256"] != aligned_sha256:
        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH")

    questions = payload["questions"]
    reserve = payload["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)
    _require_permutation(questions, "order")
    _require_permutation(reserve, "order")

    all_ids: set[str] = set()
    assigned_cues: set[tuple[str, str]] = set()

    def require_unique_id(item: Mapping[str, object]) -> None:
        identifier = item["id"]
        assert isinstance(identifier, str)
        if identifier in all_ids:
            raise ValueError("TRITRACK_ORGANIZER_DUPLICATE_ID")
        all_ids.add(identifier)

    def assign_span(item: Mapping[str, object]) -> None:
        take, start_position, end_position = _resolve_span(
            item,
            aligned_index=aligned_index,
        )
        for cue in take.cues[start_position : end_position + 1]:
            address = (take.take_id, cue.cue_id)
            if address in assigned_cues:
                raise ValueError("TRITRACK_ORGANIZER_CUE_REUSED")
            assigned_cues.add(address)

    for question in questions:
        assert isinstance(question, Mapping)
        require_unique_id(question)
        _require_canonical_text(
            question,
            "question",
            maximum=QUESTION_TEXT_LIMIT,
            required=True,
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        _require_permutation(answers, "order")
        for answer in answers:
            assert isinstance(answer, Mapping)
            require_unique_id(answer)
            if "note" in answer:
                _require_canonical_text(
                    answer,
                    "note",
                    maximum=NOTE_TEXT_LIMIT,
                    required=False,
                )
            assign_span(answer)

    for item in reserve:
        assert isinstance(item, Mapping)
        require_unique_id(item)
        _require_canonical_text(
            item,
            "reason",
            maximum=QUESTION_TEXT_LIMIT,
            required=True,
        )
        if "note" in item:
            _require_canonical_text(
                item,
                "note",
                maximum=NOTE_TEXT_LIMIT,
                required=False,
            )
        assign_span(item)
    return payload


def _compiled_span(
    selection: Mapping[str, object],
    *,
    aligned_index: AlignedIndex,
) -> dict[str, object]:
    take, start_position, end_position = _resolve_span(
        selection,
        aligned_index=aligned_index,
    )
    return {
        "takeId": take.take_id,
        "sourceSha256": take.source_sha256,
        "startCueId": take.cues[start_position].cue_id,
        "endCueId": take.cues[end_position].cue_id,
        "startMs": take.cues[start_position].start_ms,
        "endMs": take.cues[end_position].end_ms,
    }


def build_working_cut(
    aligned: object,
    grouping: object,
    *,
    aligned_sha256: str,
    grouping_sha256: str,
) -> dict[str, object]:
    """Compile one grouping into a deterministic transcript-text-free working cut."""

    aligned_index = index_aligned_transcript(aligned)
    canonical_grouping = validate_grouping(
        grouping,
        aligned_index=aligned_index,
        aligned_sha256=aligned_sha256,
    )
    questions = canonical_grouping["questions"]
    reserve = canonical_grouping["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)

    compiled_questions: list[dict[str, object]] = []
    segments: list[dict[str, object]] = []
    story_order = 0
    for question in sorted(questions, key=lambda item: item["order"]):
        assert isinstance(question, Mapping)
        compiled_questions.append(
            {
                "id": question["id"],
                "question": question["question"],
                "order": question["order"],
            }
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        for answer in sorted(answers, key=lambda item: item["order"]):
            assert isinstance(answer, Mapping)
            story_order += 1
            compiled = {
                "id": answer["id"],
                "storyOrder": story_order,
                "questionId": question["id"],
                **_compiled_span(answer, aligned_index=aligned_index),
            }
            if "note" in answer:
                compiled["note"] = answer["note"]
            segments.append(compiled)

    compiled_reserve: list[dict[str, object]] = []
    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
        assert isinstance(item, Mapping)
        compiled = {
            "id": item["id"],
            "order": item["order"],
            **_compiled_span(item, aligned_index=aligned_index),
            "reason": item["reason"],
        }
        if "note" in item:
            compiled["note"] = item["note"]
        compiled_reserve.append(compiled)

    working_cut: dict[str, object] = {
        "schemaVersion": "tritrack.working-cut/v1",
        "organizationProfileId": ORGANIZATION_PROFILE_ID,
        "alignedTranscriptSha256": aligned_sha256,
        "groupingSha256": grouping_sha256,
        "questions": compiled_questions,
        "segments": segments,
        "reserve": compiled_reserve,
    }
    validate_contract("working-cut-v1", working_cut)
    return working_cut


def _encode_contract(name: str, payload: object) -> bytes:
    validate_contract(name, payload)
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def encode_grouping(payload: object) -> bytes:
    """Return canonical bytes for one schema-valid grouping."""

    return _encode_contract("grouping-v1", payload)


def encode_working_cut(payload: object) -> bytes:
    """Return canonical bytes for one strict working cut."""

    return _encode_contract("working-cut-v1", payload)


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_UNREADABLE") from error
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_JSON_LIMIT_BYTES + 1)
        if len(encoded) > _JSON_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_json_artifact(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedJsonArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected, invalid_code)
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedJsonArtifact(
        path=selected,
        payload=payload,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
        invalid_code=invalid_code,
    )


def _verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED")


def _publish_working_cut(payload: object, output_path: Path) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_working_cut(payload)
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


def organize_and_publish(
    aligned_path: Path,
    grouping_path: Path,
    *,
    output_path: Path,
) -> dict[str, object]:
    """Compile exact local inputs and atomically publish a working cut."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned = _load_json_artifact(
        aligned_path,
        contract="aligned-transcript-v1",
        invalid_code="TRITRACK_ORGANIZER_ALIGNED_INVALID",
    )
    grouping = _load_json_artifact(
        grouping_path,
        contract="grouping-v1",
        invalid_code="TRITRACK_ORGANIZER_GROUPING_INVALID",
    )
    if grouping.encoded != encode_grouping(grouping.payload):
        raise ValueError("TRITRACK_ORGANIZER_GROUPING_NONCANONICAL")
    working_cut = build_working_cut(
        aligned.payload,
        grouping.payload,
        aligned_sha256=aligned.sha256,
        grouping_sha256=grouping.sha256,
    )
    _verify_artifact_unchanged(aligned)
    _verify_artifact_unchanged(grouping)
    _publish_working_cut(working_cut, destination)
    return working_cut
