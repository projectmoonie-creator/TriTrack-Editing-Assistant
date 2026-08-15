from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

from tests.task9_fixtures import invented_aligned, invented_grouping
from tritrack_editing_assistant import paper_edit


def write_aligned(root: Path, *, formula_text: bool = False) -> tuple[Path, bytes]:
    aligned = invented_aligned()
    if formula_text:
        aligned["takes"][0]["cues"][0]["text"] = "=INVENTED()"
    encoded = (
        json.dumps(aligned, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path = root / "aligned.json"
    path.write_bytes(encoded)
    return path, encoded


def write_grouping(root: Path, aligned_bytes: bytes) -> tuple[Path, bytes]:
    grouping = invented_grouping()
    grouping["alignedTranscriptSha256"] = hashlib.sha256(aligned_bytes).hexdigest()
    encoded = (
        json.dumps(grouping, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    path = root / "grouping.json"
    path.write_bytes(encoded)
    return path, encoded


def logical_grid(path: Path) -> dict[str, list[list[object]]]:
    workbook = load_workbook(path, data_only=False)
    return {
        name: [list(row) for row in workbook[name].iter_rows(values_only=True)]
        for name in workbook.sheetnames
    }


class PaperExportTest(unittest.TestCase):
    def test_exports_exact_reference_grid_and_hidden_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, aligned_bytes = write_aligned(root)
            output = root / "paper.xlsx"

            summary = paper_edit.export_workbook(
                aligned,
                grouping_path=None,
                output_path=output,
            )

            workbook = load_workbook(output, data_only=False)
            self.assertEqual(
                workbook.sheetnames,
                ["Cues", "Questions", "Selections", "_TriTrack"],
            )
            self.assertEqual(workbook["_TriTrack"].sheet_state, "hidden")
            self.assertEqual(
                [cell.value for cell in workbook["Cues"][1]],
                [
                    "TakeId",
                    "SourceSha256",
                    "CueId",
                    "StartMs",
                    "EndMs",
                    "Text",
                    "Disposition",
                ],
            )
            self.assertEqual(workbook["Cues"].max_row, 5)
            self.assertEqual(
                [cell.value for cell in workbook["Cues"][2]],
                [
                    "A.wav",
                    "3" * 64,
                    "cue-000001",
                    0,
                    500,
                    "Invented first answer.",
                    "original",
                ],
            )
            self.assertEqual(workbook["Questions"].max_row, 1)
            self.assertEqual(workbook["Selections"].max_row, 1)
            manifest = {
                workbook["_TriTrack"].cell(row=row, column=1).value:
                workbook["_TriTrack"].cell(row=row, column=2).value
                for row in range(2, workbook["_TriTrack"].max_row + 1)
            }
            self.assertEqual(
                manifest["WorkbookSchemaVersion"],
                "tritrack.paper-workbook/v1",
            )
            self.assertEqual(
                manifest["AlignedTranscriptSha256"],
                hashlib.sha256(aligned_bytes).hexdigest(),
            )
            self.assertEqual(
                summary,
                {
                    "cueCount": 4,
                    "questionCount": 0,
                    "selectionCount": 0,
                },
            )

    def test_prefills_grouping_as_a_direct_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, aligned_bytes = write_aligned(root)
            grouping, _ = write_grouping(root, aligned_bytes)
            output = root / "prefilled.xlsx"

            summary = paper_edit.export_workbook(
                aligned,
                grouping_path=grouping,
                output_path=output,
            )

            workbook = load_workbook(output, data_only=False)
            self.assertEqual(
                [cell.value for cell in workbook["Questions"][2]],
                ["question-001", "What changed?", 1],
            )
            self.assertEqual(
                [cell.value for cell in workbook["Selections"][2]],
                [
                    "ANSWER",
                    "answer-001",
                    "question-001",
                    1,
                    "A.wav",
                    "cue-000001",
                    "cue-000002",
                    None,
                    "Primary invented answer",
                ],
            )
            self.assertEqual(
                [cell.value for cell in workbook["Selections"][4]],
                [
                    "RESERVE",
                    "reserve-001",
                    None,
                    1,
                    "B.wav",
                    "cue-000002",
                    "cue-000002",
                    "Alternate invented answer",
                    "Keep available",
                ],
            )
            self.assertEqual(
                summary,
                {"cueCount": 4, "questionCount": 2, "selectionCount": 3},
            )

    def test_formula_looking_transcript_text_is_saved_as_literal_string(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned, _ = write_aligned(root, formula_text=True)
            output = root / "literal.xlsx"

            paper_edit.export_workbook(
                aligned,
                grouping_path=None,
                output_path=output,
            )

            workbook = load_workbook(output, data_only=False)
            cell = workbook["Cues"]["F2"]
            self.assertEqual(cell.value, "=INVENTED()")
            self.assertEqual(cell.data_type, "s")

    def test_existing_output_and_missing_parent_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "paper.xlsx"
            output.write_text("winner", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                paper_edit.export_workbook(
                    root / "missing.json",
                    grouping_path=None,
                    output_path=output,
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "winner")

            aligned, _ = write_aligned(root)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
            ):
                paper_edit.export_workbook(
                    aligned,
                    grouping_path=None,
                    output_path=root / "missing" / "paper.xlsx",
                )


if __name__ == "__main__":
    unittest.main()
