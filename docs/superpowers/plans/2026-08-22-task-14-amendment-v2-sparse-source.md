# Task 14 Amendment v2 Sparse-Source Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consume the hash-bound `task13-parity-v2` amendment by adding a sparse-source guard, making both invention and absence drive retry and adoption, and publishing density evidence while keeping VAD unavailable.

**Architecture:** Add one pure `sparse_source` policy module and keep `transcript-bundle-v1` unchanged. New runs publish `transcription-report-v2`, `transcription-result-manifest-v2`, and `run-manifest-v3`; all v1/v2 readers remain available. The orchestrator records exact duration and character counts for decoded sources, asks the pure policy both whether to retry and which source to adopt, and emits one deterministic human density table alongside the machine report.

**Tech Stack:** Python 3.12/3.13, `unittest`, Draft 2020-12 JSON Schema, existing canonical JSON and manifest-last publishers.

---

### Task 1: Pin the clean-room intake and public decision

**Files:**
- Create: `docs/TASK-14-AMENDMENT-V2-DECISION.md`
- Modify: `tests/test_maintainer_boundary.py`

- [ ] **Step 1: Write the failing governance test**

Assert the public decision records handoff ID `task13-parity-v2`, `amends=task13-parity-v1`, public base `1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`, all six verified payload hashes, the three-part VAD gate, and the rule that v1's voice-activity contract is superseded.

- [ ] **Step 2: Run the RED test**

Run: `venv/bin/python -m unittest tests.test_maintainer_boundary.MaintainerBoundaryTest.test_task_14_v2_amendment_is_hash_bound -v`

Expected: FAIL because `docs/TASK-14-AMENDMENT-V2-DECISION.md` does not exist.

- [ ] **Step 3: Write the bounded public decision**

Record only the reviewed handoff identity, aggregate public measurements, preserved invariants, compatibility strategy, VAD-off state, and non-goals. Do not copy private paths, identifiers, media, transcripts, or history.

- [ ] **Step 4: Run the test to GREEN**

Run the same command; expected: PASS.

### Task 2: Reimplement the pure sparse-source policy

**Files:**
- Create: `src/tritrack_editing_assistant/sparse_source.py`
- Create: `tests/test_sparse_source.py`

- [ ] **Step 1: Write RED policy tests**

Cover content-character counting independent of cue segmentation, punctuation/spacing/mark exclusion, Latin/digit support, invalid duration, the inclusive 30-second floor, strict-below 1.0 boundary, short-media exemption, usable-primary precedence, both invalid and sparse retry triggers, sparse-primary survival when nothing better exists, invalid-primary refusal, and sparse-alternative adoption when primary is invalid.

- [ ] **Step 2: Run the RED suite**

Run: `venv/bin/python -m unittest tests.test_sparse_source -v`

Expected: FAIL because the module and API are absent.

- [ ] **Step 3: Implement the minimal pure API**

Provide `transcript_characters(cues)`, `characters_per_second(cues, duration_ms)`, `is_sparse(cues, duration_ms)`, `requires_retry(problem)`, and `choose_source(candidates)`. The selection ladder is primary usable, first usable alternative, sparse primary, first sparse alternative, then none.

- [ ] **Step 4: Run the suite to GREEN**

Run the same command; expected: all policy tests PASS.

### Task 3: Carry duration out of the decoder

**Files:**
- Modify: `src/tritrack_editing_assistant/transcribe_takes.py`
- Modify: `tests/test_transcribe_takes.py`

- [ ] **Step 1: Write a RED decoder test**

Assert `transcribe_source` returns the exact inspected normalized-audio duration on `TranscribedTake.duration_ms`, including a non-silent invented WAV.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_transcribe_takes.LocalTranscriptionWorkflowTest.test_source_result_carries_exact_audio_duration -v`

Expected: FAIL because the field is absent.

- [ ] **Step 3: Add the minimal field**

Add optional `duration_ms` to `TranscribedTake` for backward-compatible construction and populate it from `_inspect_normalized_audio` in every new decode.

- [ ] **Step 4: Run focused tests to GREEN**

Run the new test and `venv/bin/python -m unittest tests.test_transcribe_takes -v`; expected: PASS.

### Task 4: Version the report and result manifest

**Files:**
- Create: `src/tritrack_editing_assistant/schemas/transcription-report-v2.schema.json`
- Create: `src/tritrack_editing_assistant/schemas/transcription-result-manifest-v2.schema.json`
- Modify: `src/tritrack_editing_assistant/contracts.py`
- Modify: `tests/test_contracts.py`

- [ ] **Step 1: Write RED contract fixtures**

Add valid v2 fixtures with `sparsePolicy`, per-attempt `metrics`, `selectionReason`, `sharedAlternativeWithTakeIds`, and job `summary`; add invalid fixtures for missing metrics, inconsistent sparse/null values, and a v2 result manifest missing the density table hash.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_contracts -v`

Expected: FAIL with unknown v2 contracts.

- [ ] **Step 3: Add closed schemas and registry entries**

Keep v1 schemas byte-for-byte unchanged. Require every v2 attempt to carry `durationMs`, `characterCount`, rounded `charactersPerSecond`, and `sparse`, using explicit nulls only when evidence is unavailable. Bind `transcription-density.txt` in result manifest v2.

- [ ] **Step 4: Run contract tests to GREEN**

Run the same command; expected: PASS.

### Task 5: Make sparse drive retry and adoption

**Files:**
- Modify: `src/tritrack_editing_assistant/transcription_result.py`
- Modify: `tests/test_transcription_result.py`

- [ ] **Step 1: Write RED orchestration tests**

Prove a sparse primary triggers an alternative decode; a usable alternative is adopted; a sparse primary survives when alternatives are not better; an invalid primary may adopt a sparse alternative; invalid never survives; retry and adoption share `sparse_source`; metrics exist on every attempt; and two takes selecting one alternative announce each other.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_transcription_result -v`

Expected: FAIL because completed sparse takes currently terminate retry and v1 reports have no metrics.

- [ ] **Step 3: Implement minimal v2 orchestration**

Build candidate evaluations from decoder results, continue only when `requires_retry` says so, make final adoption solely through `choose_source`, keep selected sparse text as bundle status `completed`, and emit v2 report summary fields from actual attempts. Reused v1 evidence keeps explicit unknown metrics.

- [ ] **Step 4: Emit and bind the deterministic density table**

Sort measured attempts by exact rational density, insert a threshold row, place unknown rows last, include no paths or transcript text, and bind the bytes in result manifest v2. Loaders dispatch from manifest/report schema version and continue accepting exact v1 directories.

- [ ] **Step 5: Run focused suites to GREEN**

Run `venv/bin/python -m unittest tests.test_sparse_source tests.test_transcription_result -v`; expected: PASS.

### Task 6: Carry v2 authority through immutable runs

**Files:**
- Create: `src/tritrack_editing_assistant/schemas/run-manifest-v3.schema.json`
- Modify: `src/tritrack_editing_assistant/run_workflow.py`
- Modify: `tests/test_run_workflow.py`
- Modify: `tests/test_contracts.py`

- [ ] **Step 1: Write RED run tests**

Assert new prepared runs contain and hash-bind `transcription-density.txt`, use `run-manifest-v3`, reject a changed table even when other artifacts are canonical, and continue loading existing run-manifest-v1/v2 bundles.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_run_workflow -v`

Expected: FAIL because v3 and the density artifact are absent.

- [ ] **Step 3: Implement v3 prepared authority**

Add a v3 prepared phase spec and dynamic transcription-authority validation for v1/v2 result families. New `prepare_run` writes the density table and publishes v3; aligned and finished phases preserve the manifest-chain reader compatibility already required for prior versions.

- [ ] **Step 4: Run focused suites to GREEN**

Run `venv/bin/python -m unittest tests.test_run_workflow tests.test_contracts -v`; expected: PASS.

### Task 7: Keep VAD off and update public surfaces

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `README.md`
- Modify: `docs/TOOLING.md`
- Modify: `docs/ROADMAP.md`
- Modify: `STATUS.md`
- Create: `docs/TASK-14-AMENDMENT-V2-VERIFICATION.md`
- Modify: `release/package-policy-v1.json`
- Modify: `MANIFEST.in`
- Modify: `tests/test_packaging.py`

- [ ] **Step 1: Write RED boundary and packaging tests**

Require the third sparse guard in public docs, keep `--vad`, `--no-vad`, and caller VAD model paths absent, require new schema/package members, and require the public record to use the repo-relative retained worktree locator without a home path.

- [ ] **Step 2: Observe RED**

Run: `venv/bin/python -m unittest tests.test_cli tests.test_maintainer_boundary tests.test_packaging -v`

Expected: FAIL on missing v2 public claims and package members.

- [ ] **Step 3: Update public records and package policy**

State that VAD remains off until all three guards plus the existing closed model/argument gate are present. Record the retained worktree as `../TriTrack-Editing-Assistant-worktrees/task13-parity-mechanisms`, without an absolute home path. Add only the new runtime/schema/docs files to package inventories.

- [ ] **Step 4: Run focused suites to GREEN**

Run the same focused command; expected: PASS.

### Task 8: Record the frozen Task 14 Claude recovery attempt

**Files:**
- Modify: `docs/reviews/task-14-closeout-2026-08-22.md`
- Modify: `STATUS.md`
- Preserve: `docs/reviews/task-14-closeout-packet-2026-08-22.md`
- Preserve: `docs/reviews/task-14-closeout-claude-2026-08-22.md.attempts/1061392e-4861-43b2-aac2-2f5511a70c20/`

- [ ] **Step 1: Verify the frozen bytes and both ledgers**

Run `shasum -a 256 docs/reviews/task-14-closeout-packet-2026-08-22.md` and require `c9c4efb8281386522f751e59c2949263b8394317dd658199650b39105dfaffae`.

- [ ] **Step 2: Record exact attempt provenance**

Record recovery attempt `2263620f-be88-44e1-8c69-dceaae00606d` as `claude-timeout`, requested dynamic `opus`, observed/completed null, dispatch ambiguous, with no retry, downgrade, provider substitution, or paid fallback.

- [ ] **Step 3: Add the producer-required conflict disclosure**

State that Task 14 implemented the private author's v1 specification and that the author now knows that specification was wrong, so any Claude conclusion on the frozen Task 14 packet is not neutral. Do not alter the packet bytes.

### Task 9: Final verification and coherent commit

**Files:**
- Modify: `docs/TASK-14-AMENDMENT-V2-VERIFICATION.md`
- Modify: `STATUS.md`

- [ ] **Step 1: Run focused and complete verification**

Run the sparse/result/run/contract/CLI/packaging/boundary focused suites, then `venv/bin/python -m unittest discover -s tests -v`, `venv/bin/ruff check src tests examples scripts`, both skill validators, project identity, compilation, and `git diff --check`.

- [ ] **Step 2: Run the clean release-readiness gate**

After a coherent commit and clean source, run `python scripts/release_gate.py --source . --output ABSENT_DIRECTORY` and record machine-generated hashes. This creates no tag, release, upload, package publication, tester contact, or submission.

- [ ] **Step 3: Read back every claim and commit only task-owned files**

Verify exact changed paths, worktree position, packet hash, attempt ledgers, VAD-off help surface, test counts, and Git status before committing.
