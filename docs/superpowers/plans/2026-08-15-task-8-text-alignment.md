# Task 8 Deterministic Text Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic cue-addressed local alignment artifact and an offline provider-receipt conformance path without shipping network transport.

**Architecture:** `align_text.py` owns strict loading, semantic validation, immutable cue promotion, stable encoding, input rechecks, and atomic publication. `gemini_hybrid.py` validates exact-model and upload/deletion receipts, then calls the same pure alignment builder and publisher, so provider-assisted and local promotion are byte-identical. The network-capable JavaScript component remains planned.

**Tech Stack:** Python 3.12+, Draft 2020-12 JSON Schema, unittest, jsonschema, existing absent-path hard-link publication pattern.

---

## File structure

- Create `src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json`:
  strict partial cue-addressed revision contract.
- Create `src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json`:
  strict Task 9 input with immutable timing and revision dispositions.
- Modify `src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json`:
  add exact source-bundle and take bindings before the planned contract is used.
- Modify `src/tritrack_editing_assistant/contracts.py`: allow the two new
  contracts.
- Create `src/tritrack_editing_assistant/align_text.py`: local promotion core.
- Create `src/tritrack_editing_assistant/gemini_hybrid.py`: offline receipt
  validator and shared-core entry point; no network or subprocess code.
- Modify `src/tritrack_editing_assistant/cli.py`: implement `align` and
  offline `hybrid`, update only the matching component statuses.
- Create `tests/test_align_text.py` and `tests/test_gemini_hybrid.py`.
- Modify `tests/test_contracts.py`, `tests/test_cli.py`, and
  `tests/test_maintainer_boundary.py`.
- Modify `README.md`, `docs/TOOLING.md`, `docs/ROADMAP.md`,
  `CHANGELOG.md`, and finally `STATUS.md`.
- Create `docs/TASK-8-VERIFICATION.md` only after implementation and review
  are green.

### Task 1: Freeze strict Task 8 contracts

**Files:**
- Create: `src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json`
- Create: `src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json`
- Modify: `src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json`
- Modify: `src/tritrack_editing_assistant/contracts.py`
- Modify: `tests/test_contracts.py`

- [ ] **Step 1: Write failing contract fixtures**

Add exact valid fixtures with these shapes:

```python
"text-revision-v1": {
    "schemaVersion": "tritrack.text-revision/v1",
    "sourceBundleSha256": "a" * 64,
    "language": "en",
    "takes": [{
        "takeId": "Take-A.wav",
        "sourceSha256": "b" * 64,
        "revisions": [{"cueId": "cue-000001", "text": "Corrected words"}],
    }],
},
"aligned-transcript-v1": {
    "schemaVersion": "tritrack.aligned-transcript/v1",
    "alignmentProfileId": "cue-addressed-v1",
    "sourceBundleSha256": "a" * 64,
    "revisionSha256": "c" * 64,
    "language": "en",
    "takes": [{
        "takeId": "Take-A.wav",
        "sourceSha256": "b" * 64,
        "status": "completed",
        "cues": [{
            "cueId": "cue-000001",
            "startMs": 0,
            "endMs": 500,
            "text": "Corrected words",
            "disposition": "revised",
        }],
    }],
},
```

Extend the provider receipt fixture with
`sourceBundleSha256` and `takeId`. Add invalid cases for extra properties,
bad hashes, unsafe IDs, empty revision arrays, completed takes without cues,
empty takes with cues, and missing receipt bindings.

- [ ] **Step 2: Run contract tests and verify RED**

Run:

```bash
venv/bin/python -m unittest tests.test_contracts -v
```

Expected: FAIL because both new contract names are unknown and the provider
receipt schema does not require the new bindings.

- [ ] **Step 3: Add minimal schemas and allowlist entries**

Both schemas must use Draft 2020-12, `additionalProperties: false`, exact
schemaVersion constants, lowercase two/three-letter languages, safe
path-free take IDs, six-digit cue IDs, and lowercase 64-hex SHA-256 values.
The aligned schema must enforce completed/nonempty and empty/zero-cue states.
Add both filenames to `contracts._CONTRACT_NAMES`.

- [ ] **Step 4: Run contract tests and verify GREEN**

Run the Step 2 command. Expected: all contract tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/schemas src/tritrack_editing_assistant/contracts.py tests/test_contracts.py
git commit -m "feat: add deterministic alignment contracts"
```

### Task 2: Build the local cue-addressed promotion core

**Files:**
- Create: `tests/test_align_text.py`
- Create: `src/tritrack_editing_assistant/align_text.py`

- [ ] **Step 1: Write failing pure-alignment tests**

Define a wished-for API:

```python
aligned = align_text.build_aligned_transcript(
    transcript,
    revision,
    source_bundle_sha256="a" * 64,
    revision_sha256="c" * 64,
)
```

Assert that it sorts takes deterministically, preserves source hashes, status,
cue IDs and timing, revises only addressed cues, marks dispositions, and
validates against `aligned-transcript-v1`. Assert input objects remain equal
to deep copies.

Add one test per failure: bundle-hash mismatch, language mismatch, unknown or
duplicate take/cue IDs, revision source-hash mismatch, edit to an empty take,
invalid normalized text, duplicate or non-monotonic source cues, and no actual
revision entries.

- [ ] **Step 2: Run focused tests and verify RED**

```bash
venv/bin/python -m unittest tests.test_align_text -v
```

Expected: import failure because `align_text.py` does not exist.

- [ ] **Step 3: Implement the minimal pure builder**

Use `hallucination.normalize_cue_text` for revision text. Build explicit
take/cue indexes with duplicate rejection. Validate source cue monotonicity and
status semantics beyond JSON Schema. Preserve timing exactly. Emit:

```python
{
    "schemaVersion": "tritrack.aligned-transcript/v1",
    "alignmentProfileId": "cue-addressed-v1",
    "sourceBundleSha256": source_bundle_sha256,
    "revisionSha256": revision_sha256,
    "language": transcript["language"],
    "takes": [...],
}
```

Validate the final object through `validate_contract`.

- [ ] **Step 4: Verify GREEN**

Run the Step 2 command. Expected: all pure alignment tests pass.

- [ ] **Step 5: Write failing file-boundary tests**

Add tests for exact-byte hashes, nonregular／symlink／oversized JSON rejection,
malformed UTF-8/JSON, absent parent, existing output, race winner, source and
revision mutation after initial read, stable bytes across repeated calls, and
cleanup. The wished-for entry point is:

```python
align_text.align_and_publish(
    transcript_path,
    revision_path,
    output_path=output_path,
)
```

- [ ] **Step 6: Verify file-boundary RED**

Run the focused test module. Expected: failures because file loading and
publication functions are absent.

- [ ] **Step 7: Implement bounded loading and atomic publication**

Use a 16 MiB per-input size limit; `lstat` to reject symlink/nonregular files;
strict UTF-8/JSON; exact input bytes for hashes; a full pre-publication re-read
hash check; stable sorted-key JSON with final newline; and the existing
temporary-file plus hard-link absent-output pattern.

- [ ] **Step 8: Verify GREEN and regressions**

```bash
venv/bin/python -m unittest tests.test_align_text -v
venv/bin/python -m unittest tests.test_contracts tests.test_hallucination tests.test_transcribe_takes -v
```

Expected: all pass.

- [ ] **Step 9: Commit**

```bash
git add src/tritrack_editing_assistant/align_text.py tests/test_align_text.py
git commit -m "feat: add deterministic cue alignment"
```

### Task 3: Expose the local align CLI

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `src/tritrack_editing_assistant/cli.py`

- [ ] **Step 1: Write failing CLI tests**

Require:

```text
tritrack align --transcript INPUT --revision REVISION --output ABSENT --json
```

Assert `align_text.py` becomes implemented, while both Gemini components
remain planned. Assert a successful path-free summary containing only
`schemaVersion`, `takeCount`, `cueCount`, `revisedCueCount`, and
`artifactSha256`. Assert stable usage/data/I/O/output-exists exit mappings and
no transcript text or path on stdout.

- [ ] **Step 2: Run CLI tests and verify RED**

```bash
venv/bin/python -m unittest tests.test_cli -v
```

Expected: align remains planned and flags are absent.

- [ ] **Step 3: Implement minimal CLI wiring**

Import `align_text`, add the four exact flags, invoke
`align_and_publish`, map stable error codes, and compute the output hash from
the created file. Change only `align_text.py` to `implemented` in the
registry.

- [ ] **Step 4: Verify GREEN and installed help**

```bash
venv/bin/python -m unittest tests.test_cli -v
venv/bin/tritrack align --help
venv/bin/tritrack components --json
```

Expected: tests pass; help matches the tested surface; registry count remains
eleven.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/cli.py tests/test_cli.py
git commit -m "feat: expose local alignment command"
```

### Task 4: Add offline Gemini receipt conformance

**Files:**
- Create: `tests/test_gemini_hybrid.py`
- Create: `src/tritrack_editing_assistant/gemini_hybrid.py`
- Modify: `tests/test_cli.py`
- Modify: `src/tritrack_editing_assistant/cli.py`

- [ ] **Step 1: Write failing receipt-validation tests**

Use invented receipt files only. Define:

```python
payload = gemini_hybrid.hybrid_and_publish(
    transcript_path,
    revision_path,
    receipt_paths,
    exact_model="gemini-invented-exact",
    output_path=output_path,
)
```

Require one uniquely bound receipt per revised take. Require provider
`gemini`, source-bundle/take/audio hashes, requested and observed exact model,
completed request/upload, 2xx response, and attempted/confirmed 2xx deletion.
Reject missing/extra/duplicate receipts, null/mismatched models, failed or
privacy-incomplete status, unconfirmed deletion, nonregular receipt files,
receipt mutation, output collisions, and races. Assert no output on failure.

Assert that local `align_and_publish` and offline `hybrid_and_publish` with
the same exact transcript/revision bytes produce byte-identical aligned
artifacts at two absent paths.

- [ ] **Step 2: Run hybrid tests and verify RED**

```bash
venv/bin/python -m unittest tests.test_gemini_hybrid -v
```

Expected: import failure because `gemini_hybrid.py` does not exist.

- [ ] **Step 3: Implement the offline validator**

Reuse `align_text` validated byte loaders, pure builder, input recheck, and
publisher. Do not import an HTTP client, Node, subprocess, environment
credential, or provider SDK. Hash every receipt before and after processing.
Only after every receipt is conformant may the shared local publisher run.

- [ ] **Step 4: Verify hybrid GREEN**

Run the Step 2 command. Expected: all tests pass.

- [ ] **Step 5: Write CLI RED tests**

Require:

```text
tritrack hybrid --transcript INPUT --proposal REVISION
                --receipt RECEIPT [--receipt RECEIPT ...]
                --model EXACT --output ABSENT --json
```

The help must explicitly say offline validation and no network. The summary
uses the same path-free fields as align. `gemini_hybrid.py` becomes
implemented; `gemini_transcribe.mjs` remains planned.

- [ ] **Step 6: Implement CLI wiring and verify GREEN**

Wire the exact flags and stable exit mappings, then run:

```bash
venv/bin/python -m unittest tests.test_gemini_hybrid tests.test_cli -v
venv/bin/tritrack hybrid --help
venv/bin/tritrack components --json
```

Expected: all pass, eleven components remain, and no live transport exists.

- [ ] **Step 7: Commit**

```bash
git add src/tritrack_editing_assistant/gemini_hybrid.py src/tritrack_editing_assistant/cli.py tests/test_gemini_hybrid.py tests/test_cli.py
git commit -m "feat: add offline provider conformance"
```

### Task 5: Documentation, verification, and closeout

**Files:**
- Modify: `README.md`
- Modify: `docs/TOOLING.md`
- Modify: `docs/ROADMAP.md`
- Modify: `CHANGELOG.md`
- Modify: `tests/test_maintainer_boundary.py`
- Create after green: `docs/TASK-8-VERIFICATION.md`
- Modify after green: `STATUS.md`

- [ ] **Step 1: Document only the tested surface**

Add local align and offline hybrid examples, custody rules, exact-byte hash
meaning, empty-take immutability, provider receipt requirements, and the
explicit statement that no network transport is shipped. Keep
`gemini_transcribe.mjs` planned in the registry table.

- [ ] **Step 2: Run all local gates**

```bash
venv/bin/python -m unittest tests.test_contracts tests.test_align_text tests.test_gemini_hybrid tests.test_cli
venv/bin/python -m unittest discover -s tests
venv/bin/ruff check src tests
venv/bin/python -m compileall -q src tests examples
venv/bin/python -m unittest tests.test_maintainer_boundary -v
python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
git diff --check
```

Expected: all pass with no warnings or dirty unrelated files.

- [ ] **Step 3: Run installed deterministic acceptance**

Create invented temporary transcript/revision/receipt artifacts outside Git.
Run installed `align` twice to distinct absent outputs, then `hybrid` once.
Require all three output files to be byte-identical, schema-valid, and free of
local absolute paths and provider metadata. Run negative exact-model and
deletion-confirmation cases and require no output.

- [ ] **Step 4: Freeze and run closeout review**

Use `reviewing-with-multiple-ai` with one frozen public-only packet. Preserve
requested/observed/completed model provenance and incomplete lanes. Adjudicate
every finding locally; add a reproducing RED test before behavioral fixes.

- [ ] **Step 5: Rerun gates after the last implementation edit**

Repeat Steps 2 and 3. Update `docs/TASK-8-VERIFICATION.md`, `STATUS.md`, and
the boundary test only after the coherent package is green. Record no real
provider claim.

- [ ] **Step 6: Commit, integrate, and verify backup**

Commit only Task 8 files. Confirm clean status, fetch origin, require local and
remote main to match the Task 7 base, and require main to be an ancestor of the
Task 8 candidate. Fast-forward main, push the existing public origin, verify
the exact remote SHA, and wait for the Python 3.12/3.13 GitHub Actions matrix.

- [ ] **Step 7: Stop at the Task 9 session boundary**

After Task 8 is fully green and backed up, hand off Task 9 to a fresh session.
Do not begin organizer or paper-edit code in this session.

## Self-review

- Spec coverage: all Option A decisions map to Tasks 1–5; no live transport,
  full-text DP, retiming, empty-take revisions, Task 9, or release action leaks
  into implementation.
- Incomplete-step scan: every behavior and command is concrete.
- Type consistency: `sourceBundleSha256`, `revisionSha256`, `takeId`,
  `sourceSha256`, `cueId`, `text`, and `disposition` are consistent
  across schemas, builders, tests, CLI, and docs.
- Execution mode: inline in the existing isolated Task 8 branch, because
  subagent delegation was not requested and the producer chose the same
  session.
