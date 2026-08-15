"""Strict XLSX transport for the cue-addressed paper-edit round trip."""

from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError
from openpyxl import Workbook
from openpyxl.cell.cell import Cell

from . import __version__, organizer
from .contracts import validate_contract
from .process import require_absent_output

WORKBOOK_SCHEMA_VERSION = "tritrack.paper-workbook/v1"
CUES_HEADERS = (
    "TakeId",
    "SourceSha256",
    "CueId",
    "StartMs",
    "EndMs",
    "Text",
    "Disposition",
)
QUESTIONS_HEADERS = ("QuestionId", "Question", "Order")
SELECTIONS_HEADERS = (
    "Placement",
    "SegmentId",
    "QuestionId",
    "Order",
    "TakeId",
    "StartCueId",
    "EndCueId",
    "ReserveReason",
    "EditorNote",
)
MANIFEST_HEADERS = ("Key", "Value")
SHEET_NAMES = ("Cues", "Questions", "Selections", "_TriTrack")
_JSON_LIMIT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class LoadedArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str


def _read_regular_bytes(path: Path, *, limit: int, invalid_code: str) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_PAPER_INPUT_UNREADABLE") from error
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(limit + 1)
        if len(encoded) > limit:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_json(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(
        selected,
        limit=_JSON_LIMIT_BYTES,
        invalid_code=invalid_code,
    )
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedArtifact(
        selected,
        payload,
        encoded,
        hashlib.sha256(encoded).hexdigest(),
        invalid_code,
    )


def _verify_unchanged(artifact: LoadedArtifact) -> None:
    try:
        encoded = _read_regular_bytes(
            artifact.path,
            limit=_JSON_LIMIT_BYTES,
            invalid_code=artifact.invalid_code,
        )
    except ValueError as error:
        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED")


def _literal(cell: Cell, value: object, *, text_format: bool = False) -> None:
    cell.value = value
    if isinstance(value, str):
        cell.data_type = "s"
    if text_format:
        cell.number_format = "@"


def _write_row(
    worksheet,
    row: int,
    values: Sequence[object],
    *,
    text_columns: frozenset[int] = frozenset(),
) -> None:
    for column, value in enumerate(values, start=1):
        _literal(
            worksheet.cell(row=row, column=column),
            value,
            text_format=column in text_columns,
        )


def _cue_rows(aligned: Mapping[str, object]) -> list[tuple[object, ...]]:
    organizer.index_aligned_transcript(aligned)
    rows: list[tuple[object, ...]] = []
    takes = aligned["takes"]
    assert isinstance(takes, list)
    for take in takes:
        assert isinstance(take, Mapping)
        if take["status"] != "completed":
            continue
        cues = take["cues"]
        assert isinstance(cues, list)
        for cue in cues:
            assert isinstance(cue, Mapping)
            rows.append(
                (
                    take["takeId"],
                    take["sourceSha256"],
                    cue["cueId"],
                    cue["startMs"],
                    cue["endMs"],
                    cue["text"],
                    cue["disposition"],
                )
            )
    return rows


def _cues_grid_sha256(rows: Sequence[Sequence[object]]) -> str:
    encoded = json.dumps(
        [list(CUES_HEADERS), *[list(row) for row in rows]],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _project_grouping(
    workbook: Workbook,
    grouping: Mapping[str, object] | None,
) -> tuple[int, int]:
    questions_sheet = workbook["Questions"]
    selections_sheet = workbook["Selections"]
    _write_row(questions_sheet, 1, QUESTIONS_HEADERS, text_columns=frozenset({1}))
    _write_row(
        selections_sheet,
        1,
        SELECTIONS_HEADERS,
        text_columns=frozenset({1, 2, 3, 5, 6, 7}),
    )
    if grouping is None:
        return 0, 0

    questions = grouping["questions"]
    reserve = grouping["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)
    question_count = 0
    selection_count = 0
    for question in sorted(questions, key=lambda item: item["order"]):
        assert isinstance(question, Mapping)
        question_count += 1
        _write_row(
            questions_sheet,
            question_count + 1,
            (question["id"], question["question"], question["order"]),
            text_columns=frozenset({1}),
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        for answer in sorted(answers, key=lambda item: item["order"]):
            assert isinstance(answer, Mapping)
            selection_count += 1
            _write_row(
                selections_sheet,
                selection_count + 1,
                (
                    "ANSWER",
                    answer["id"],
                    question["id"],
                    answer["order"],
                    answer["takeId"],
                    answer["startCueId"],
                    answer["endCueId"],
                    None,
                    answer.get("note"),
                ),
                text_columns=frozenset({1, 2, 3, 5, 6, 7}),
            )
    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
        assert isinstance(item, Mapping)
        selection_count += 1
        _write_row(
            selections_sheet,
            selection_count + 1,
            (
                "RESERVE",
                item["id"],
                None,
                item["order"],
                item["takeId"],
                item["startCueId"],
                item["endCueId"],
                item["reason"],
                item.get("note"),
            ),
            text_columns=frozenset({1, 2, 3, 5, 6, 7}),
        )
    return question_count, selection_count


def _build_workbook(
    aligned: Mapping[str, object],
    *,
    aligned_sha256: str,
    grouping: Mapping[str, object] | None,
) -> tuple[Workbook, dict[str, int]]:
    cue_rows = _cue_rows(aligned)
    workbook = Workbook()
    cues_sheet = workbook.active
    cues_sheet.title = "Cues"
    workbook.create_sheet("Questions")
    workbook.create_sheet("Selections")
    manifest_sheet = workbook.create_sheet("_TriTrack")
    manifest_sheet.sheet_state = "hidden"

    _write_row(cues_sheet, 1, CUES_HEADERS, text_columns=frozenset({1, 2, 3}))
    for row_number, row in enumerate(cue_rows, start=2):
        _write_row(
            cues_sheet,
            row_number,
            row,
            text_columns=frozenset({1, 2, 3}),
        )
    question_count, selection_count = _project_grouping(workbook, grouping)
    _write_row(manifest_sheet, 1, MANIFEST_HEADERS)
    manifest = (
        ("WorkbookSchemaVersion", WORKBOOK_SCHEMA_VERSION),
        ("ToolVersion", __version__),
        ("AlignedTranscriptSha256", aligned_sha256),
        ("CuesGridSha256", _cues_grid_sha256(cue_rows)),
    )
    for row_number, row in enumerate(manifest, start=2):
        _write_row(manifest_sheet, row_number, row, text_columns=frozenset({1, 2}))
    return workbook, {
        "cueCount": len(cue_rows),
        "questionCount": question_count,
        "selectionCount": selection_count,
    }


def _publish_bytes(encoded: bytes, output_path: Path) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
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


def export_workbook(
    aligned_path: Path,
    *,
    grouping_path: Path | None,
    output_path: Path,
) -> dict[str, int]:
    """Export one strict aligned authority to an editor-facing workbook."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned = _load_json(
        aligned_path,
        contract="aligned-transcript-v1",
        invalid_code="TRITRACK_PAPER_ALIGNED_INVALID",
    )
    assert isinstance(aligned.payload, Mapping)
    grouping: LoadedArtifact | None = None
    grouping_payload: Mapping[str, object] | None = None
    aligned_index = organizer.index_aligned_transcript(aligned.payload)
    if grouping_path is not None:
        grouping = _load_json(
            grouping_path,
            contract="grouping-v1",
            invalid_code="TRITRACK_PAPER_GROUPING_INVALID",
        )
        if grouping.encoded != organizer.encode_grouping(grouping.payload):
            raise ValueError("TRITRACK_PAPER_GROUPING_INVALID")
        grouping_payload = organizer.validate_grouping(
            grouping.payload,
            aligned_index=aligned_index,
            aligned_sha256=aligned.sha256,
        )

    workbook, summary = _build_workbook(
        aligned.payload,
        aligned_sha256=aligned.sha256,
        grouping=grouping_payload,
    )
    buffer = io.BytesIO()
    workbook.save(buffer)
    _verify_unchanged(aligned)
    if grouping is not None:
        _verify_unchanged(grouping)
    _publish_bytes(buffer.getvalue(), destination)
    return summary
