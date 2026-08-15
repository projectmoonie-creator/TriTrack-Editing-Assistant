# Task 9 Organizer and Paper-Edit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a deterministic, local-only round trip from strict aligned transcript bytes through an editor-facing workbook to grouping intent and a compiled working cut.

**Architecture:** `organizer.py` owns the strict JSON authority: aligned indexing, grouping semantics, deterministic `working-cut-v1` compilation, and no-overwrite JSON publication. `paper_edit.py` owns the non-authoritative XLSX transport and delegates all final grouping semantics to the organizer. The CLI exposes nested `paper export`／`paper apply` commands plus `organize`, while exact hashes, absent-output publication, and sanitized summaries preserve the existing public boundaries.

**Tech Stack:** Python 3.12+, `jsonschema` Draft 2020-12, `openpyxl` 3.1, `unittest`, Ruff, setuptools package resources.

---

## Frozen implementation details

- The workbook has exactly four worksheets: visible `Cues`, `Questions`, and
  `Selections`, plus hidden `_TriTrack`. The sentence “exactly three sheets” in
  `docs/TASK-9-DECISION.md` is corrected because the same accepted contract
  explicitly defines all four sheets and requires the manifest.
- Canonical JSON is UTF-8, `ensure_ascii=False`, `indent=2`, `sort_keys=True`,
  and one final newline.
- JSON inputs are limited to 16 MiB; XLSX inputs are limited to 64 MiB. Inputs
  must be nonempty regular non-symlink files and are hashed before and after
  processing.
- Safe editor IDs use `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`. Question and
  reserve-reason text is bounded to 500 characters; notes to 2,000 characters.
- `_TriTrack` is a two-column `Key`／`Value` table containing
  `WorkbookSchemaVersion`, `ToolVersion`, `AlignedTranscriptSha256`, and
  `CuesGridSha256` in that order. The sheet state is `hidden`; it is not a
  security boundary.
- Stable data failures use these families:
  `TRITRACK_ORGANIZER_*` for aligned／grouping semantics and compilation,
  `TRITRACK_PAPER_*` for workbook structure and transport, and the existing
  `TRITRACK_OUTPUT_EXISTS`／`TRITRACK_OUTPUT_PARENT_MISSING` publication codes.
  Late mutation is `TRITRACK_ORGANIZER_INPUT_CHANGED` or
  `TRITRACK_PAPER_INPUT_CHANGED`.

### Task 1: Freeze strict Task 9 JSON contracts

**Files:**
- Modify: `src/tritrack_editing_assistant/schemas/grouping-v1.schema.json`
- Create: `src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json`
- Modify: `src/tritrack_editing_assistant/contracts.py`
- Modify: `tests/test_contracts.py`

- [ ] **Step 1: Write failing contract tests**

Add canonical `grouping-v1` and `working-cut-v1` fixtures to
`VALID_CONTRACTS`, then add `test_task_9_contracts_reject_invalid_state_shapes`
covering missing exact-hash bindings, unsafe IDs, missing answer order, timing
inside grouping, text inside working-cut segments, unknown fields, and invalid
profile IDs.

```python
"grouping-v1": {
    "schemaVersion": "tritrack.grouping/v1",
    "alignedTranscriptSha256": "4" * 64,
    "questions": [{
        "id": "question-001", "question": "What changed?", "order": 1,
        "answers": [{
            "id": "answer-001", "order": 1, "takeId": "Take-A.wav",
            "startCueId": "cue-000001", "endCueId": "cue-000002",
        }],
    }],
    "reserve": [],
},
```

- [ ] **Step 2: Run RED and preserve the expected failure**

Run: `venv/bin/python -m unittest tests.test_contracts -v`

Expected: FAIL because `working-cut-v1` is unknown and the old grouping schema
does not accept the exact-byte and cue-addressed fields.

- [ ] **Step 3: Tighten grouping and add working-cut schemas**

Implement the exact decision shapes with `additionalProperties: false`, closed
schema/profile constants, lowercase SHA-256 patterns, safe IDs and take IDs,
cue-ID patterns, positive orders, text length bounds, and optional notes. Add
`working-cut-v1` to `CONTRACT_NAMES`.

- [ ] **Step 4: Run GREEN**

Run: `venv/bin/python -m unittest tests.test_contracts -v`

Expected: all contract tests pass.

- [ ] **Step 5: Commit the contract unit**

```bash
git add src/tritrack_editing_assistant/contracts.py \
  src/tritrack_editing_assistant/schemas/grouping-v1.schema.json \
  src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json \
  tests/test_contracts.py
git commit -m "feat: define Task 9 editorial contracts"
```

### Task 2: Build the pure organizer compiler

**Files:**
- Create: `src/tritrack_editing_assistant/organizer.py`
- Create: `tests/task9_fixtures.py`
- Create: `tests/test_organizer.py`

- [ ] **Step 1: Write the failing happy-path organizer test**

Create invented aligned/grouping builders and assert that
`build_working_cut()` leaves both inputs unchanged, copies timing/source hashes
only from aligned cues, flattens answers by question/order, derives
`storyOrder`, excludes transcript text, and validates `working-cut-v1`.

```python
working_cut = organizer.build_working_cut(
    aligned,
    grouping,
    aligned_sha256="a" * 64,
    grouping_sha256="b" * 64,
)
self.assertEqual([item["storyOrder"] for item in working_cut["segments"]], [1, 2])
self.assertNotIn("text", json.dumps(working_cut))
```

- [ ] **Step 2: Run RED**

Run: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`

Expected: import failure because `organizer.py` does not exist.

- [ ] **Step 3: Implement the minimal compiler core**

Add these focused interfaces:

```python
ORGANIZATION_PROFILE_ID = "cue-addressed-question-groups-v1"

def canonical_editor_text(value: object, *, maximum: int, required: bool) -> str | None: ...
def index_aligned_transcript(payload: object) -> AlignedIndex: ...
def validate_grouping(payload: object, *, aligned_index: AlignedIndex,
                      aligned_sha256: str) -> dict[str, object]: ...
def build_working_cut(aligned: object, grouping: object, *,
                      aligned_sha256: str,
                      grouping_sha256: str) -> dict[str, object]: ...
def encode_grouping(payload: object) -> bytes: ...
def encode_working_cut(payload: object) -> bytes: ...
```

The validator enforces canonical aligned semantics, exact binding, unique IDs,
order permutations, completed-take cue spans, single assignment across active
and reserve selections, and already-canonical editor text.

- [ ] **Step 4: Run GREEN**

Run: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`

Expected: happy-path tests pass.

- [ ] **Step 5: Add RED semantic rejection tests**

Add separate tests for duplicate take/cue/segment IDs; unsorted or invalid
aligned timing; noncanonical text; hash mismatch; gapped orders; empty
questions; unknown/empty take; reversed/unknown cue spans; and cue reuse across
answer/reserve.

- [ ] **Step 6: Run RED and implement only the missing checks**

Run after tests: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`

Expected RED codes include `TRITRACK_ORGANIZER_ALIGNED_INVALID`,
`TRITRACK_ORGANIZER_GROUPING_INVALID`,
`TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH`,
`TRITRACK_ORGANIZER_ORDER_INVALID`,
`TRITRACK_ORGANIZER_TEXT_NONCANONICAL`,
`TRITRACK_ORGANIZER_SPAN_INVALID`, and
`TRITRACK_ORGANIZER_CUE_REUSED`. Implement the checks, rerun, and expect PASS.

- [ ] **Step 7: Commit the pure compiler**

```bash
git add src/tritrack_editing_assistant/organizer.py \
  tests/task9_fixtures.py tests/test_organizer.py
git commit -m "feat: compile deterministic question-grouped cuts"
```

### Task 3: Add organizer file and CLI boundaries

**Files:**
- Modify: `src/tritrack_editing_assistant/organizer.py`
- Modify: `src/tritrack_editing_assistant/cli.py`
- Modify: `tests/test_organizer.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write RED publication-boundary tests**

Cover regular/non-symlink 16 MiB inputs, invalid UTF-8/JSON/schema, exact
canonical grouping bytes, input hash changes, missing parent, existing output
before input reads, hard-link race winner, temp cleanup, deterministic bytes,
and unchanged sources.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_organizer.OrganizerFileBoundaryTest -v`

Expected: failures because `organize_and_publish()` is absent.

- [ ] **Step 3: Implement exact-byte loading and atomic publication**

Add:

```python
def organize_and_publish(aligned_path: Path, grouping_path: Path, *,
                         output_path: Path) -> dict[str, object]: ...
```

Reserve the absent output first, load bounded regular inputs with `O_NOFOLLOW`,
validate and compile in memory, rehash both inputs, then write/fsync a sibling
temporary file and hard-link it to the absent destination. Always remove the
temporary file.

- [ ] **Step 4: Run organizer boundary GREEN**

Run: `venv/bin/python -m unittest tests.test_organizer -v`

Expected: PASS.

- [ ] **Step 5: Write RED CLI tests and implement the exact command**

Assert `tritrack organize --help` exposes only `--aligned`, `--grouping`,
`--output`, and `--json`; a successful summary contains only schema version,
counts, and output hash; malformed data maps to 65, missing parent/input I/O to
74, and output conflicts to 73.

- [ ] **Step 6: Run CLI GREEN and commit**

Run: `venv/bin/python -m unittest tests.test_cli.CliSmokeTest -v`

Expected: PASS with `organizer.py` marked `implemented` while the registry
still has exactly eleven components.

```bash
git add src/tritrack_editing_assistant/organizer.py \
  src/tritrack_editing_assistant/cli.py tests/test_organizer.py tests/test_cli.py
git commit -m "feat: expose atomic organizer command"
```

### Task 4: Export strict paper-edit workbooks

**Files:**
- Create: `src/tritrack_editing_assistant/paper_edit.py`
- Create: `tests/test_paper_edit.py`

- [ ] **Step 1: Write RED workbook-export tests**

Assert exact four-sheet names and order, `_TriTrack.sheet_state == "hidden"`,
exact headers, complete cue grid, correct manifest hashes, blank editor tables
without grouping, exact grouping projection with grouping, text number formats
for identifiers, and literal formula-looking aligned text after save/reload
with `data_only=False`.

```python
paper_edit.export_workbook(aligned_path, grouping_path=None, output_path=output)
book = load_workbook(output, data_only=False)
self.assertEqual(book.sheetnames, ["Cues", "Questions", "Selections", "_TriTrack"])
self.assertEqual(book["Cues"]["F2"].value, "=INVENTED()")
self.assertEqual(book["Cues"]["F2"].data_type, "s")
```

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperExportTest -v`

Expected: import failure because `paper_edit.py` does not exist.

- [ ] **Step 3: Implement deterministic logical export**

Add fixed headers, a canonical cue-grid hash, grouping projection, string-cell
writing that forces `data_type="s"`, exact input verification, and atomic XLSX
publication through a temporary file plus hard link. Do not promise ZIP-byte
identity.

- [ ] **Step 4: Run export GREEN and commit**

Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperExportTest -v`

Expected: PASS.

```bash
git add src/tritrack_editing_assistant/paper_edit.py tests/test_paper_edit.py
git commit -m "feat: export strict paper-edit workbooks"
```

### Task 5: Apply workbook edits back to grouping authority

**Files:**
- Modify: `src/tritrack_editing_assistant/paper_edit.py`
- Modify: `tests/test_paper_edit.py`

- [ ] **Step 1: Write RED apply and fixpoint tests**

Edit an invented workbook through openpyxl, apply it, validate the grouping,
and assert: grouping bytes are deterministic; export(A,G) then apply(A,W)
returns bytes identical to G; two re-exports have equal logical grids; source
take/cue/hash/timing structure cannot enter grouping from workbook edits.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperApplyTest -v`

Expected: failures because `apply_workbook()` is absent.

- [ ] **Step 3: Implement strict workbook parsing and normalization**

Add:

```python
def apply_workbook(aligned_path: Path, workbook_path: Path, *,
                   output_path: Path) -> dict[str, object]: ...
```

Load exact XLSX bytes with `data_only=False`; reject formulas in every accepted
sheet, missing/extra/reordered sheets, wrong headers, merged cells, defined
names, external links, macros, invalid cell types, partial rows, duplicate IDs,
bad orders, manifest/reference-grid drift, and invalid grouping semantics.
Normalize workbook-authored editor text, delegate final semantic validation to
`organizer.validate_grouping`, rehash inputs, and atomically publish canonical
grouping JSON.

- [ ] **Step 4: Run GREEN**

Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperApplyTest -v`

Expected: PASS.

- [ ] **Step 5: Add RED adversarial workbook and file-boundary tests**

Cover formula cells, cached-formula ambiguity, cue insertion/deletion/reorder,
display edits, hidden-manifest drift, partial rows, formula-looking display
text, foreign spans, overlaps, symlinks, size limits, invalid ZIP, late
mutation, existing output/races, cleanup, and sanitized failure messages.

- [ ] **Step 6: Implement missing checks, run GREEN, and commit**

Run: `venv/bin/python -m unittest tests.test_paper_edit -v`

Expected: PASS with stable `TRITRACK_PAPER_*` errors and no traceback.

```bash
git add src/tritrack_editing_assistant/paper_edit.py tests/test_paper_edit.py
git commit -m "feat: apply paper edits to grouping authority"
```

### Task 6: Expose nested paper CLI and installed round trip

**Files:**
- Modify: `src/tritrack_editing_assistant/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write RED nested-command and summary tests**

Assert exact `paper export`／`paper apply` help, disjoint argument sets,
sanitized summaries, exit mappings, no tracebacks, and `paper_edit.py` status
`implemented` without changing registry length.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_cli.CliSmokeTest -v`

Expected: `paper export` and `paper apply` parse/behavior failures.

- [ ] **Step 3: Implement nested parsers and handlers**

`paper export` accepts `--aligned`, optional `--grouping`, `--output`, and
`--json`. `paper apply` accepts `--aligned`, `--workbook`, `--output`, and
`--json`. Summaries include only schema version, bounded counts, and exact
artifact hash.

- [ ] **Step 4: Run GREEN and installed CLI acceptance**

Run:

```bash
venv/bin/python -m unittest tests.test_cli -v
venv/bin/pip install -e '.[dev]'
venv/bin/tritrack paper export --help
venv/bin/tritrack paper apply --help
venv/bin/tritrack organize --help
```

Expected: PASS/help exit 0; help names only the frozen local flags.

- [ ] **Step 5: Commit the CLI unit**

```bash
git add src/tritrack_editing_assistant/cli.py tests/test_cli.py
git commit -m "feat: expose paper-edit round trip"
```

### Task 7: Document and verify the coherent Task 9 package

**Files:**
- Modify: `docs/TASK-9-DECISION.md`
- Modify: `README.md`
- Modify: `docs/TOOLING.md`
- Modify: `docs/ROADMAP.md`
- Modify: `STATUS.md`
- Modify: `tests/test_maintainer_boundary.py`
- Create: `docs/TASK-9-VERIFICATION.md`

- [ ] **Step 1: Write RED governance assertions**

Update boundary tests to require implemented Task 9 status, the three exact
help authorities, local/network-free wording, round-trip invariants, sanitized
evidence, and Task 10 as the next gate.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_maintainer_boundary -v`

Expected: FAIL against Task 8-era status/docs.

- [ ] **Step 3: Update public documentation without release claims**

Correct the workbook sheet-count typo, document the three commands, strict
JSON authority, XLSX non-authority, exact-hash/no-overwrite boundaries, and
Task 10 deferrals. Record only invented and reproducible verification in
`docs/TASK-9-VERIFICATION.md`.

- [ ] **Step 4: Run focused, full, lint, compile, identity, skill, and diff gates**

```bash
venv/bin/python -m unittest tests.test_contracts tests.test_organizer tests.test_paper_edit tests.test_cli -v
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples
venv/bin/python -m compileall -q src tests examples
python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
venv/bin/python -m unittest tests.test_maintainer_boundary -v
git diff --check
```

Expected: every command passes; identity reports `ok: true`, `public-engine`,
and `OSS`.

- [ ] **Step 5: Commit the green documentation package**

```bash
git add docs/TASK-9-DECISION.md README.md docs/TOOLING.md docs/ROADMAP.md \
  STATUS.md tests/test_maintainer_boundary.py docs/TASK-9-VERIFICATION.md
git commit -m "docs: record Task 9 verification"
```

### Task 8: Independent closeout, fix-forward, CI, and custody

**Files:**
- Create or modify only sanitized `docs/reviews/task-9-*` artifacts required by
  the repository collaboration contract.
- Modify Task 9-owned code/tests/docs only for ordinary in-scope review fixes.

- [ ] **Step 1: Freeze the review packet**

Read the repository collaboration/tooling contract, record candidate SHA,
changed-file list, focused/full/lint/boundary results, and ask independent
reviewers to check contract fidelity, workbook adversarial safety, privacy,
determinism, and test gaps.

- [ ] **Step 2: Run convergent independent review**

Use the approved Claude subscription-only and dynamically resolved Gemini
lanes. Record requested, observed, and completed model IDs and preserve any
incomplete lane truthfully.

- [ ] **Step 3: Fix-forward ordinary findings with RED/GREEN evidence**

For every accepted behavior finding, add a failing regression test, observe
the expected failure, implement the minimal fix, and rerun focused plus full
gates. Update verification evidence only after the last implementation edit.

- [ ] **Step 4: Fast-forward and push under the standing grant**

After all local gates and review are green, fast-forward local `main` to the
Task 9 candidate, push `main` to the existing public `origin`, and verify
`origin/main`, remote API SHA, and local `main` are exactly identical. Do not
create a tag, release, pull request, tester contact, package publication, or
application submission.

- [ ] **Step 5: Verify minimal CI at the exact public candidate**

Confirm the GitHub Actions Python 3.12/3.13 matrix passes at the exact pushed
SHA. Record the run ID and distinguish Linux automated evidence from Final Cut
GUI/DTD claims.

## Self-review result

- Spec coverage: every accepted Task 9 command, JSON contract, workbook sheet,
  semantic rejection, round-trip invariant, file/race boundary, CLI summary,
  documentation gate, independent review, CI gate, and custody gate maps to a
  task above.
- Placeholder scan: no implementation step contains `TBD`, `TODO`, or an
  unfrozen product choice.
- Type consistency: all later tasks use `alignedTranscriptSha256`,
  `groupingSha256`, `organizationProfileId`, `startCueId`, and `endCueId` with
  the exact decision names; workbook headers and CLI flags are frozen once and
  reused unchanged.
