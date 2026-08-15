# Task 9 post-fix closeout review packet

Date: 2026-08-16

## Frozen target

- Public repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Branch: `codex/task9-organizer-paper-edit`
- Review candidate: `cc813f01176c1a9c8d0a0409b2de112ffb9ca8a5`
- Public baseline: `28ce8be5e1cfd774cce7bc11c19d2f8da83f67df`
- Diff scope: 2 files, 179 insertions, 8 deletions
- Changed files:
  - `src/tritrack_editing_assistant/paper_edit.py`
  - `tests/test_paper_edit.py`

This is a read-only review. Do not edit files. Do not request credentials,
private media, transcripts, or unpublished project state.

## Objective

Review the bounded fix-forward package added after Task 9's original closeout.
The package must make XLSX intake fail closed before expensive or unsafe
processing, reject workbook links, preserve stable paper-edit error semantics,
and leave the already-shipped organizer and paper-edit round trip unchanged for
valid invented inputs.

Task 9 is local-only. It performs no network request, provider operation,
credential lookup, media processing, subprocess invocation, FCPXML emission,
or Task 10 orchestration.

## Governing invariants

1. Aligned JSON is the only transcript, cue timing, and source-hash authority.
2. The workbook is an untrusted, non-authoritative transport with exactly four
   sheets: `Cues`, `Questions`, `Selections`, and hidden `_TriTrack`.
3. Apply re-derives the cue grid and manifest from the exact aligned bytes.
4. Formula cells, macros, merged cells, defined names, external workbook links,
   hyperlinks, unexpected structure, and unsafe archive shape fail closed.
5. JSON input is limited to 16 MiB and compressed XLSX input to 64 MiB.
6. `grouping-v1` requires at least one answer per question. Organizer validation
   gives each selected cue to at most one answer or reserve span. Therefore the
   number of question rows cannot exceed selection rows, and selection rows
   cannot exceed the completed aligned cue count.
7. Output is absent-path, atomic, no-overwrite publication. Inputs are rehashed
   before publication.

## Reproduced pre-fix failures

The maintainer independently reproduced four gaps against public baseline
`28ce8be` before changing implementation:

1. A cell hyperlink such as `https://example.invalid/external` in the Questions
   sheet was accepted by `paper apply`.
2. A schema-valid, still-sorted take ID containing vertical tab reached
   `openpyxl` and raised an uncaught `IllegalCharacterError` during export.
3. A 6,886-byte workbook whose Questions dimension reached row 1,048,576 began
   rectangular cell iteration; the three-column sheet alone implied 3,145,782
   cell visits.
4. Compressed input had a 64 MiB bound, but ZIP member count and expanded sizes
   were not checked before `openpyxl` parsed the archive.

The first RED run intentionally established hyperlink, dimension, and archive
failures. The aligned-identity fixture was then corrected from an accidentally
unsorted ID to sorted `A\v.wav`; that corrected RED produced the exact uncaught
`openpyxl.utils.exceptions.IllegalCharacterError` and no output artifact.

## Current implementation excerpts

The constants and aligned boundary now read:

```python
_WORKBOOK_LIMIT_BYTES = 64 * 1024 * 1024
_WORKBOOK_MEMBER_LIMIT = 512
_WORKBOOK_EXPANDED_LIMIT_BYTES = 256 * 1024 * 1024
_WORKBOOK_SINGLE_MEMBER_LIMIT_BYTES = 128 * 1024 * 1024


def _paper_aligned_index(aligned: object) -> organizer.AlignedIndex:
    try:
        aligned_index = organizer.index_aligned_transcript(aligned)
    except ValueError as error:
        raise ValueError("TRITRACK_PAPER_ALIGNED_INVALID") from error
    if any(
        not all(
            character in "\t\n\r"
            or 0x20 <= ord(character) <= 0xD7FF
            or 0xE000 <= ord(character) <= 0xFFFD
            or 0x10000 <= ord(character) <= 0x10FFFF
            for character in take_id
        )
        for take_id in aligned_index.takes
    ):
        raise ValueError("TRITRACK_PAPER_ALIGNED_INVALID")
    return aligned_index
```

Workbook bytes are read once as a bounded, regular, non-symlink file. Before
`openpyxl.load_workbook`, the archive preflight is:

```python
with zipfile.ZipFile(io.BytesIO(encoded)) as archive:
    members = archive.infolist()
    names = [member.filename for member in members]
    expanded_size = 0
    if (
        not members
        or len(members) > _WORKBOOK_MEMBER_LIMIT
        or len(names) != len(set(names))
    ):
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    for member in members:
        member_path = PurePosixPath(member.filename)
        if (
            member.flag_bits & 0x1
            or member.filename.startswith(("/", "\\"))
            or "\\" in member.filename
            or ".." in member_path.parts
            or member.filename.lower().endswith("vbaproject.bin")
            or member.file_size > _WORKBOOK_SINGLE_MEMBER_LIMIT_BYTES
        ):
            raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
        expanded_size += member.file_size
        if expanded_size > _WORKBOOK_EXPANDED_LIMIT_BYTES:
            raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
```

After openpyxl loads the workbook, exact sheet names and visibility, no defined
names, and no external workbook links are checked. The new dimension and cell
checks are:

```python
maximum_dimensions = {
    "Cues": (cue_row_count + 1, len(CUES_HEADERS)),
    "Questions": (cue_row_count + 1, len(QUESTIONS_HEADERS)),
    "Selections": (cue_row_count + 1, len(SELECTIONS_HEADERS)),
    "_TriTrack": (5, len(MANIFEST_HEADERS)),
}
for worksheet in workbook.worksheets:
    maximum_rows, maximum_columns = maximum_dimensions[worksheet.title]
    if (
        worksheet.max_row > maximum_rows
        or worksheet.max_column > maximum_columns
    ):
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
for worksheet in workbook.worksheets:
    if worksheet.merged_cells.ranges:
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.hyperlink is not None:
                raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
            if cell.data_type == "f":
                raise ValueError("TRITRACK_PAPER_FORMULA_FORBIDDEN")
```

`apply_workbook` computes expected cue rows before worksheet iteration:

```python
aligned_index = _paper_aligned_index(aligned.payload)
cue_rows = _cue_rows(aligned.payload)
_reject_unsafe_workbook_state(workbook, cue_row_count=len(cue_rows))
cue_rows = _verify_cues_grid(workbook, aligned.payload)
```

## Regression evidence

Four regressions now prove:

- sorted `A\v.wav` fails as `TRITRACK_PAPER_ALIGNED_INVALID`, with no output;
- an external cell hyperlink fails as `TRITRACK_PAPER_WORKBOOK_INVALID`;
- an extreme dimension fails before `Worksheet.iter_rows` can be called; and
- an archive over the patched expanded-size limit fails before
  `load_workbook` can be called.

The final post-edit verification results are:

- Task 9 focused suite: 53 passed;
- complete suite: 155 passed;
- maintainer boundary: 9 passed;
- Ruff over `src`, `tests`, and `examples`: passed;
- compileall over `src`, `tests`, and `examples`: passed;
- project identity: `ok: true`, `public-engine`, lane `OSS`;
- current maintainer-skill validator: passed;
- `git diff --check`: passed.

A non-editable local wheel was force-reinstalled without dependency or network
access. An invented installed CLI run completed `paper export -> edited XLSX ->
paper apply -> organize -> normalized re-export -> re-apply`. It reported:

```json
{"cueCount":2,"groupingFixpoint":true,"groupingSha256":"b2ad845cb687eeedd5bc2c297035aa36fb314e9e78045a7a722ff7dafedb5446","logicalGridEqual":true,"questionCount":1,"schemaVersion":"tritrack.task9-installed-acceptance/v1","segmentCount":1}
```

## Requested review dimensions

Review all of the following independently:

1. Whether the ZIP preflight runs early enough and uses sound limits and member
   metadata checks for this local XLSX boundary.
2. Whether the cue-count-derived worksheet dimension caps are valid under the
   grouping schema and unique-cue assignment invariant, including empty and
   prefilled workbook cases.
3. Whether rejecting every cell hyperlink and retaining existing external-link,
   formula, macro, merge, defined-name, and sheet checks closes the relevant
   workbook link/structure boundary.
4. Whether the XML 1.0 character-set check prevents openpyxl export tracebacks
   for all take IDs that the aligned JSON schema otherwise permits.
5. Whether paper-edit error mapping remains stable and no partial output can be
   published on these failures.
6. Whether the new checks can reject a valid workbook exported by this tool or
   allow a practical low-cost counterexample that still reaches expensive
   rectangular iteration or oversized decompression.
7. Test adequacy, documentation accuracy, privacy, determinism, and governance.

## Required response format

Return exactly these sections:

1. `VERDICT: PASS` or `VERDICT: FINDINGS`
2. `SUMMARY:` one short paragraph
3. `FINDINGS:` numbered findings, or `none`; each finding must include severity,
   current file and line, concrete counterexample or reproduction, and bounded
   remediation
4. `TEST_GAPS:` numbered gaps, or `none`
5. `DOC_GAPS:` numbered gaps, or `none`

Do not call a hypothetical concern a blocker without a current file-and-line
path plus a concrete accepted input or reproducible failure.
