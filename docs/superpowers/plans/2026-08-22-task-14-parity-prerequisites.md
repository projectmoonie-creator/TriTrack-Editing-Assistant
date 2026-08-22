# Task 14 Parity Prerequisites Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reimplement the clean-room anomaly and pair-selection mechanisms, publish retry/degrade transcription provenance, and make temporal relay authority reach deterministic FCPXML while keeping VAD default fail-closed.

**Architecture:** Two small pure modules own anomaly and pair-selection policy. `sync-map-v2` carries relay topology to both string-out and story projections; transcription publishes an unchanged v1 cue bundle beside a text-free report and manifest, with one orchestrator shared by standalone and run workflows. Because the authorized input contains no operational VAD model pin, the command surface and defaults remain off and a tested gate prevents an accidental flip.

**Tech Stack:** Python 3.12/3.13, `unittest`, `jsonschema` Draft 2020-12, NumPy, whisper.cpp/ffmpeg subprocess adapters, deterministic JSON, manifest-last filesystem publication, Final Cut Pro XML 1.14.

---

## Locked file map

- Create `src/tritrack_editing_assistant/transcript_anomaly.py`: pure cue-level detectors, range merging, and whole-transcript verdict.
- Create `src/tritrack_editing_assistant/pair_selection.py`: pure drift prior, overlap-first acceptance, new-coverage selection, and audio-master policy.
- Create `src/tritrack_editing_assistant/transcription_result.py`: request/settings/report records, retry/degrade/reuse orchestration, canonical encoders, and manifest-last publication.
- Create `src/tritrack_editing_assistant/schemas/sync-map-v2.schema.json`: relay-capable synchronization authority.
- Create `src/tritrack_editing_assistant/schemas/transcription-report-v1.schema.json`: path-free and text-free per-run/per-take provenance.
- Create `src/tritrack_editing_assistant/schemas/transcription-result-manifest-v1.schema.json`: exact bundle/report file hashes.
- Create `src/tritrack_editing_assistant/schemas/run-manifest-v2.schema.json`: immutable-run authority that retains all three transcription result artifacts.
- Modify `src/tritrack_editing_assistant/contracts.py`: register the three mechanism schema names in Task 3 and `run-manifest-v2` in Task 8.
- Modify `src/tritrack_editing_assistant/transcribe_takes.py`: expose a one-source decode seam and route anomaly verdicts without changing bundle v1.
- Modify `src/tritrack_editing_assistant/sync_scan.py`: derive a drift prior, select relay sources, and publish v2.
- Modify `src/tritrack_editing_assistant/string_out.py`: read both map versions and construct relay intersections.
- Modify `src/tritrack_editing_assistant/story_fcpxml.py`: apply relay intersections and exactly one declared audio source to selected story ranges.
- Modify `src/tritrack_editing_assistant/emit_fcpxml.py`: accept v2 through the shared string-out builder.
- Modify `src/tritrack_editing_assistant/run_workflow.py`: call the shared transcription orchestrator and retain its three exact artifacts in prepared runs.
- Preserve `src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json` unchanged and make the run loader accept both installed manifest versions.
- Modify `src/tritrack_editing_assistant/cli.py`: add explicit alternative/reuse inputs, change transcription output to an absent directory, expose audio-master selection, and keep VAD switches absent.
- Create focused tests in `tests/test_transcript_anomaly.py`, `tests/test_pair_selection.py`, and `tests/test_transcription_result.py`.
- Extend `tests/test_contracts.py`, `tests/test_sync_scan.py`, `tests/test_string_out.py`, `tests/test_story_fcpxml.py`, `tests/test_transcribe_takes.py`, `tests/test_run_workflow.py`, and `tests/test_cli.py` at their existing component boundaries.
- Update `README.md`, `docs/ROADMAP.md`, and finally `STATUS.md` only after the candidate is fully green.

## Contract shapes locked by this plan

`sync-map-v2` has top-level keys `schemaVersion`, `profileId`, `driftPrior`,
`groups`, `singles`, and `warnings`. A group has one A anchor and zero or more B
sources:

```json
{
  "schemaVersion": "tritrack.sync-map/v2",
  "profileId": "uhd-2997-ndf-fcpxml-1.14",
  "driftPrior": {"centreSeconds": 12.1, "toleranceSeconds": 2.0, "sampleCount": 5},
  "groups": [{
    "groupId": "group-001",
    "anchor": {"camera": "A", "mediaId": "A-001.mov", "durationSeconds": 600.0, "startedAt": null},
    "sources": [{
      "camera": "B", "mediaId": "B-001.mov", "offsetFromAnchorSeconds": 0.0,
      "durationSeconds": 300.0, "confidence": 8.0, "overlapSeconds": 300.0,
      "match": "correlation", "startedAt": null
    }],
    "audioMaster": "A"
  }],
  "singles": [{"camera": "B", "mediaId": "B-099.mov"}],
  "warnings": []
}
```

`transcription-report-v1` contains no cue text and no paths. Each new attempt
states both directions of every hearing-changing setting:

```json
{
  "schemaVersion": "tritrack.transcription-report/v1",
  "profileId": "whisper-cpp-cpu-no-fallback-v1",
  "requestedTakeIds": ["A-001.mov"],
  "runSettings": {
    "language": "zh",
    "recognitionModelSha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "voiceActivity": "off",
    "voiceActivityModel": null
  },
  "takes": [{
    "takeId": "A-001.mov",
    "status": "completed",
    "selectedSourceSha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "attempts": [{
      "ordinal": 1,
      "sourceSha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "outcome": "completed",
      "failureCode": null,
      "settings": {
        "language": "zh",
        "recognitionModelSha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "voiceActivity": "off",
        "voiceActivityModel": null
      }
    }]
  }]
}
```

A reused attempt uses string `unknown` for `recognitionModelSha256`,
`voiceActivity`, and `voiceActivityModel`; it never inherits current settings.
Failed primary attempts use the stable code `TRITRACK_TRANSCRIPT_ANOMALY_INVALID`.
Process/evidence failures retain their existing stable public code. A take whose
attempts all fail has `status: "failed"`, `selectedSourceSha256: null`, and is
absent from `transcript-bundle-v1.takes`.

`transcription-result-manifest-v1` contains exactly `schemaVersion`, `bundle`,
and `report`; each artifact record contains `fileName` and `sha256`. Publication
links `transcript-bundle.json` and `transcription-report.json` before
`manifest.json`, never overwrites a destination, and removes a partially
reserved destination on failure.

## Invariant-to-test matrix

| Clean-room invariant | Owning test |
| --- | --- |
| four-token-stutter-threshold | `tests/test_transcript_anomaly.py::TranscriptAnomalyTest::test_four_identical_tokens_are_stutter_but_three_are_speech` |
| specific-reason-wins | `tests/test_transcript_anomaly.py::TranscriptAnomalyTest::test_cue_local_reason_outranks_repeat_run` |
| blank-cues-never-form-a-run | `tests/test_transcript_anomaly.py::TranscriptAnomalyTest::test_blank_cues_never_repeat` |
| empty-transcript-is-not-invalid | `tests/test_transcript_anomaly.py::TranscriptAnomalyTest::test_empty_transcript_has_valid_verdict` |
| overlap-before-ratio | `tests/test_pair_selection.py::PairSelectionTest::test_short_overlap_refuses_even_a_sharp_peak` |
| correlation-outranks-drift | `tests/test_pair_selection.py::PairSelectionTest::test_correlation_beats_drift_prior` |
| prior-refuses-on-weak-evidence | `tests/test_pair_selection.py::PairSelectionTest::test_prior_refuses_few_or_scattered_samples` |
| new-coverage-only | `tests/test_pair_selection.py::PairSelectionTest::test_relay_keeps_only_new_coverage` |
| forced-audio-master-ignores-loudness | `tests/test_pair_selection.py::PairSelectionTest::test_forced_audio_master_ignores_loudness` |
| settings-stated-in-both-directions | `tests/test_transcription_result.py::TranscriptionResultTest::test_report_states_voice_activity_off` |
| reuse-never-inherits-current-settings | `tests/test_transcription_result.py::TranscriptionResultTest::test_reuse_settings_are_unknown` |
| retry-matches-primary-settings | `tests/test_transcription_result.py::TranscriptionResultTest::test_retry_copies_primary_settings` |

### Task 1: Reimplement transcript anomaly policy

**Files:**
- Create: `tests/test_transcript_anomaly.py`
- Create: `src/tritrack_editing_assistant/transcript_anomaly.py`
- Modify: `src/tritrack_editing_assistant/transcribe_takes.py:52-109`

- [x] **Step 1: Write RED tests for the public API**

Use `CueFlag(index, start_ms, end_ms, text, reason)`,
`AnomalyRange(start_ms, end_ms, reasons, samples, long)`,
`TranscriptVerdict(cues, flagged, invalid)`, `has_in_cue_stutter(text)`,
`find_anomalies(cues)`, `merge_anomaly_ranges(flags, gap_ms=1500)`, and
`transcript_verdict(cues, flags)`. Tests use invented text, assert the five
transcript invariants above, and assert a one-cue decoder loop is invalid.

- [x] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_transcript_anomaly -v`

Expected: FAIL because `tritrack_editing_assistant.transcript_anomaly` does
not exist; no unrelated test error is acceptable.

- [x] **Step 3: Implement the minimal pure module**

Implement constants `MIN_REPEAT_CUES = 3`, `MIN_STUTTER_TOKENS = 4`,
`LONG_RANGE_MS = 60000`, and `INVALID_RATIO = 0.9`. Preserve the delimiter-only
known limitation. Use `dict.setdefault` so boilerplate/stutter reasons outrank
cross-cue repetition. An empty verdict is
`TranscriptVerdict(cues=0, flagged=0, invalid=False)`.

- [x] **Step 4: Integrate the verdict at canonicalization**

After cue construction, call `find_anomalies` and `transcript_verdict`; raise
`TRITRACK_TRANSCRIPT_ANOMALY_INVALID` only for an invalid verdict. Do not reject
a merely patchy transcript.

- [x] **Step 5: Verify GREEN and regressions**

Run: `venv/bin/python -m unittest tests.test_transcript_anomaly tests.test_transcribe_takes -v`

Expected: PASS.

- [x] **Step 6: Commit**

```bash
git add src/tritrack_editing_assistant/transcript_anomaly.py src/tritrack_editing_assistant/transcribe_takes.py tests/test_transcript_anomaly.py tests/test_transcribe_takes.py
git commit -m "feat: detect invalid transcript anomalies"
```

### Task 2: Reimplement drift, coverage, and audio-master policy

**Files:**
- Create: `tests/test_pair_selection.py`
- Create: `src/tritrack_editing_assistant/pair_selection.py`

- [x] **Step 1: Write RED tests**

Exercise `drift_prior`, `coverage`, `new_coverage_seconds`, `accept`,
`select_pairs`, and `audio_master` with new invented measurements. Pin five
drift samples, 5-second maximum spread, 2-to-10-second tolerance, 3-second
minimum overlap, 6.0 peak ratio, and 10-second minimum new coverage.

- [x] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_pair_selection -v`

Expected: FAIL because `tritrack_editing_assistant.pair_selection` does not
exist.

- [x] **Step 3: Implement the minimal pure module**

Return immutable-looking copied mappings rather than mutating measurements.
Sort accepted candidates by correlation before drift-prior, then descending
ratio, then source ID for deterministic ties. Keep the documented limitation:
a simultaneous duplicate contributes no new coverage and is discarded.

- [x] **Step 4: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_pair_selection -v`

Expected: PASS.

- [x] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/pair_selection.py tests/test_pair_selection.py
git commit -m "feat: select drift-aware relay sources"
```

### Task 3: Register strict v2 and transcription-result contracts

**Files:**
- Create: `src/tritrack_editing_assistant/schemas/sync-map-v2.schema.json`
- Create: `src/tritrack_editing_assistant/schemas/transcription-report-v1.schema.json`
- Create: `src/tritrack_editing_assistant/schemas/transcription-result-manifest-v1.schema.json`
- Modify: `src/tritrack_editing_assistant/contracts.py:12-27`
- Modify: `tests/test_contracts.py`

- [x] **Step 1: Write RED registry and schema tests**

Assert the three exact contract names are present, their schema versions
resolve in both directions, the locked examples above validate, and added
keys, cue text in a report, relative/slashed file names, invalid status-setting
combinations, duplicate take IDs, and duplicate media identities fail.

- [x] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_contracts -v`

Expected: FAIL because the closed registry does not contain the new names.

- [x] **Step 3: Add the three exact Draft 2020-12 schemas and registry names**

All objects use `additionalProperties: false`. All SHA-256 fields use lowercase
64-hex patterns. Report settings use enums so `off`, `on`, and `unknown` cannot
be confused with booleans or omission.

- [ ] **Step 4: Verify GREEN and packaged-resource access**

Run: `venv/bin/python -m unittest tests.test_contracts tests.test_packaging -v`

Expected: contract tests PASS; packaging uses the pre-existing environment
exception only until `setuptools==84.0.0` is installed in the venv.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/contracts.py src/tritrack_editing_assistant/schemas tests/test_contracts.py
git commit -m "feat: define relay and transcription result contracts"
```

### Task 4: Build and publish sync-map-v2

**Files:**
- Modify: `src/tritrack_editing_assistant/sync_scan.py:159-207,342-533`
- Modify: `src/tritrack_editing_assistant/cli.py:160-188,754-780`
- Modify: `tests/test_sync_scan.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Write RED builder and CLI tests**

Create a 600-second A anchor with B sources covering `[0,300]` and `[300,600]`.
Assert both survive in one group, the higher-quality first source is primary,
the second is relay coverage, the map validates as v2, and `--audio-master B`
selects the highest-ranked B source even when A is louder.

- [x] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_sync_scan tests.test_cli.CliSmokeTest.test_sync_help -v`

Expected: FAIL because sync still emits v1 and has no audio-master argument.

- [x] **Step 3: Implement evidence collection and deterministic selection**

Collect every candidate measurement before selection. Derive drift as metadata
offset minus audio offset only when time hints are sane. Compute a prior only
from strong-correlation samples, then pass all measurements through
`pair_selection.select_pairs`. Serialize one group per A anchor in A input
order, sources in selection order, and singles in camera/media order.

- [x] **Step 4: Publish and validate v2 without weakening v1 reads**

`publish_sync_map` resolves the schema from `schemaVersion`; new sync commands
emit v2. Reject relative output paths through the existing path boundary and
preserve absent-output publication.

- [x] **Step 5: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_pair_selection tests.test_sync_scan tests.test_cli -v`

Expected: PASS.

- [x] **Step 6: Commit**

```bash
git add src/tritrack_editing_assistant/sync_scan.py src/tritrack_editing_assistant/cli.py tests/test_sync_scan.py tests/test_cli.py
git commit -m "feat: publish relay-capable sync maps"
```

### Task 5: Project relay authority into string-out and story FCPXML

**Files:**
- Modify: `src/tritrack_editing_assistant/string_out.py:121-300`
- Modify: `src/tritrack_editing_assistant/emit_fcpxml.py`
- Modify: `src/tritrack_editing_assistant/story_fcpxml.py`
- Modify: `tests/test_string_out.py`
- Modify: `tests/test_story_fcpxml.py`
- Modify: `tests/test_cli.py`

- [x] **Step 1: Write command-level RED relay tests**

Feed a strict v2 relay map to the actual `emit` handler with invented probed
sources. Assert the resulting FCPXML contains both B relay assets, clips their
timeline intersections to `[0,300]` and `[300,600]`, never duplicates the A
anchor on the spine, and enables audio on only the map-declared rig. With a B
master, both non-overlapping B relay clips carry audio while A does not; exactly
one source is audible at every covered timeline instant.

- [x] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_string_out tests.test_story_fcpxml tests.test_cli -v`

Expected: FAIL with `TRITRACK_CONTRACT_UNKNOWN` or the v1-only relationship
error, proving relay cannot currently reach FCPXML.

- [x] **Step 3: Add a normalized relationship adapter**

Convert either v1 pairs or v2 groups into internal anchor/source spans. Keep
version branching at input normalization; timeline/rendering code consumes one
internal representation. Reject overlapping reuse of the same media identity,
missing sources, out-of-duration offsets, and an audio-master rig whose selected
relay sources do not cover the full selected span.

- [x] **Step 4: Render relay intersections**

For each timeline/story selection, intersect every source span with the anchor
selection. Emit only positive intersections and require exactly one
audio-enabled clip at every covered timeline instant.
Do not advertise simultaneous angles: a source excluded by coverage selection
cannot reappear downstream.

- [x] **Step 5: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_string_out tests.test_story_fcpxml tests.test_cli -v`

Expected: PASS.

- [x] **Step 6: Commit**

```bash
git add src/tritrack_editing_assistant/string_out.py src/tritrack_editing_assistant/emit_fcpxml.py src/tritrack_editing_assistant/story_fcpxml.py tests/test_string_out.py tests/test_story_fcpxml.py tests/test_cli.py
git commit -m "feat: carry relay authority into FCPXML"
```

### Task 6: Publish manifest-last transcription results

**Files:**
- Create: `src/tritrack_editing_assistant/transcription_result.py`
- Create: `tests/test_transcription_result.py`
- Modify: `src/tritrack_editing_assistant/transcribe_takes.py:435-528`

- [ ] **Step 1: Write RED report, publication, and no-overwrite tests**

Use a callable decoder seam returning real `TranscribedTake` values or stable
exceptions. Assert canonical sort order, no text/path fields in the report,
and exact hashes in the produced bundle/report/result-manifest bytes. Exercise
the standalone publisher for manifest-last visibility, cleanup on a publication
race, and no modification of an existing destination.

- [ ] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_transcription_result -v`

Expected: FAIL because `transcription_result` is absent.

- [ ] **Step 3: Extract one-source decode**

Add `transcribe_source(source, *, take_id, model_path, language, settings,
ffmpeg_executable, whisper_executable) -> TranscribedTake`. It performs the
existing hash-before/hash-after checks and raises existing stable errors. Keep
`build_transcript_bundle` unchanged.

- [ ] **Step 4: Implement the result records and canonical encoders**

Use frozen dataclasses `TranscriptionSettings`, `TranscriptionRequest`, and
`AttemptRecord`, plus `TranscriptionSource(path, sha256)` and
`BuiltTranscriptionResult(bundle, report, manifest, bundle_bytes, report_bytes,
manifest_bytes)`. `build_transcription_result(requests, *, settings,
engine_version, decoder)` is the shared pure orchestration seam; the decoder
receives `(source, take_id, settings)`. New settings always record language, model SHA-256,
`voiceActivity: off`, and `voiceActivityModel: null`. Reuse records use unknown
markers. Validate before encoding and add one trailing newline.

- [ ] **Step 5: Implement manifest-last publication**

Build in a sibling staging directory, hard-link the two artifacts and then the
manifest into a newly reserved destination, fsync, verify the exact entry set,
and clean the reservation on any exception.

Keep orchestration separate from publication: `build_transcription_result`
returns validated canonical bytes for the bundle, report, and result manifest.
`publish_transcription_result` writes those bytes to a standalone three-entry
directory. The run workflow writes the same bytes into its own staging root and
lets the outer run manifest remain the final publication marker.

- [ ] **Step 6: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_transcription_result tests.test_transcribe_takes -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/tritrack_editing_assistant/transcription_result.py src/tritrack_editing_assistant/transcribe_takes.py tests/test_transcription_result.py tests/test_transcribe_takes.py
git commit -m "feat: publish transcription result receipts"
```

### Task 7: Retry alternatives, degrade failed takes, and reuse honestly

**Files:**
- Modify: `src/tritrack_editing_assistant/transcription_result.py`
- Modify: `tests/test_transcription_result.py`

- [ ] **Step 1: Write RED orchestration tests**

Cover four paths: primary succeeds; invalid primary then alternative succeeds;
all attempts fail but another take ships; and a matching prior result is reused
with unknown settings. Assert retry setting equality by comparing the complete
attempt setting objects, not selected fields.

- [ ] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_transcription_result.TranscriptionResultTest -v`

Expected: FAIL because the first invalid attempt aborts or the orchestration API
is absent.

- [ ] **Step 3: Implement deterministic retry/degrade**

For each request in take-ID order, try primary then alternatives in declared
order. Record every attempt. Append a take to the bundle only after completed
or proven-empty evidence. Catch only stable per-take transcription failures;
input mutation, invalid global settings, publication races, and malformed prior
results remain run-fatal.

- [ ] **Step 4: Implement reuse from a separate immutable result**

Load and verify the prior result manifest, bundle, and report. Reuse only an
exact take ID/source hash match. Copy the cue-bearing take into the new bundle,
record `status: reused`, and stamp no current hearing-changing setting onto it.
The destination remains absent and distinct from the reuse source.

- [ ] **Step 5: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_transcription_result -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/tritrack_editing_assistant/transcription_result.py tests/test_transcription_result.py
git commit -m "feat: retry and degrade transcription takes"
```

### Task 8: Route standalone and run workflows through one orchestrator

**Files:**
- Modify: `src/tritrack_editing_assistant/cli.py:225-267,818-852,1024-1045`
- Modify: `src/tritrack_editing_assistant/run_workflow.py:29-80,256-284,520-720`
- Create: `src/tritrack_editing_assistant/schemas/run-manifest-v2.schema.json`
- Modify: `src/tritrack_editing_assistant/contracts.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_run_workflow.py`

- [ ] **Step 1: Write command-level RED retry/degrade tests**

Standalone CLI uses repeated `--media ABSOLUTE_PATH`, repeated
`--alternative-source TAKE_ID=ABSOLUTE_PATH`, optional
`--reuse-from ABSOLUTE_RESULT_DIRECTORY`, and absent `--output DIRECTORY`.
Assert a failed first take does not block a successful second take, the summary
is path/text-free, and the result directory contains exactly three files.

For `run prepare`, derive alternatives from sync-map-v2 group membership and
assert the prepared manifest retains `transcriptBundle`,
`transcriptionReport`, and `transcriptionResult` with exact hashes.

- [ ] **Step 2: Verify RED**

Run: `venv/bin/python -m unittest tests.test_cli tests.test_run_workflow -v`

Expected: FAIL because both paths still call file-output
`transcribe_and_publish` directly.

- [ ] **Step 3: Add strict alternative argument parsing**

Split once at `=`, validate the take ID against the declared primary basename,
require an absolute regular alternative path, reject duplicate mappings, and
reject `--reuse-from` unless it is absolute. Parser errors remain sanitized and
must not print a path.

- [ ] **Step 4: Use the shared orchestrator in both entry points**

Standalone builds explicit requests. `run prepare` builds equivalent requests
from the v2 sync groups and producer-selected transcription primaries. Both
pass the same `TranscriptionSettings` value and call
`transcription_result.transcribe_and_publish_result`.

- [ ] **Step 5: Retain all three artifacts in prepared-run authority**

Emit run-manifest-v2 for new runs and leave run-manifest-v1 unchanged/readable.
The v2 prepared branch requires the two text-free artifacts in addition to the
bundle. Update exact-entry validation, stage output hashes, summaries, and
source `transcribed` values so failed/excluded takes are false. Register v2 only
when this producer and consumer land together; keep the v1 schema bytes
unchanged and pin that fact in a regression.

- [ ] **Step 6: Verify GREEN**

Run: `venv/bin/python -m unittest tests.test_cli tests.test_run_workflow tests.test_validate_artifacts -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/tritrack_editing_assistant/cli.py src/tritrack_editing_assistant/run_workflow.py src/tritrack_editing_assistant/schemas/run-manifest-v2.schema.json tests/test_cli.py tests/test_run_workflow.py tests/test_validate_artifacts.py
git commit -m "feat: share resilient transcription orchestration"
```

### Task 9: Enforce the VAD default hard gate

**Files:**
- Modify: `tests/test_cli.py`
- Modify: `tests/test_transcription_result.py`
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`

- [ ] **Step 1: Write the gate tests before documentation changes**

Assert `transcribe --help` and `run prepare --help` contain neither `--vad` nor
`--no-vad`; new attempts report `voiceActivity: off`; reused attempts report
`unknown`; and there is no caller-supplied VAD model path argument.

- [ ] **Step 2: Run the gate tests**

Run: `venv/bin/python -m unittest tests.test_cli tests.test_transcription_result -v`

Expected: PASS after Tasks 6-8. Any failure blocks Task 14 completion.

- [ ] **Step 3: Document the exact deferred flip criteria**

State that anomaly/retry are now prerequisites delivered by Task 14, while the
default remains off pending a closed public VAD model pin with verified byte
length and SHA-256. Do not claim measured accuracy, simultaneous N-camera
support, or VAD-default completion.

- [ ] **Step 4: Commit**

```bash
git add tests/test_cli.py tests/test_transcription_result.py README.md docs/ROADMAP.md
git commit -m "docs: enforce the VAD default release gate"
```

### Task 10: Full verification, review, and public closeout

**Files:**
- Modify after green: `STATUS.md`
- Create: `docs/reviews/task-14-closeout-2026-08-22.md`

- [ ] **Step 1: Install the declared build backend in the existing venv**

Run: `venv/bin/python -m pip install 'setuptools==84.0.0'`

Expected: installation succeeds from the approved package source; if network
or package access is unavailable, record packaging as an environmental blocker
and do not claim the full gate is green.

- [ ] **Step 2: Run focused and full verification**

```bash
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check .
venv/bin/python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
venv/bin/python -m unittest tests.test_maintainer_boundary -v
git diff --check
```

Expected: all tests PASS, Ruff PASS, identity `ok: true`/`public-engine`/`OSS`,
boundary tests PASS, and no diff-check output.

- [ ] **Step 3: Perform closeout review and fix-forward**

Freeze a public-only review packet containing the decision, plan, diff, handoff
hash manifest, and verification log. Use the repository-approved review helper;
fix ordinary in-scope findings through new RED/GREEN cycles. Record exact
requested/observed/completed model IDs and packet hashes.

- [ ] **Step 4: Update governance only after coherent green**

Record Task 14 candidate commit, exact verification counts, VAD gate state,
remaining Task 13 parity dependency, and the next public action in `STATUS.md`.
Keep the stale historical Next action out of the new current-state section.

- [ ] **Step 5: Commit closeout**

```bash
git add STATUS.md docs/reviews/task-14-closeout-2026-08-22.md
git commit -m "docs: close Task 14 parity prerequisites"
```

- [ ] **Step 6: Integrate only the fully green candidate under the standing grant**

Fast-forward public `main`, push the existing `origin`, then compare local
`main`, `origin/main`, and the remote SHA. Do not tag, release, open a pull
request, contact testers, or publish a package.

## Plan self-review result

- All twelve clean-room invariants map to named tests.
- The two reference mechanisms are independently reimplemented rather than
  copied or imported.
- Both TypeScript-origin contracts are expressed as Python behavior and strict
  public JSON contracts, not ported source.
- Relay authority reaches both string-out and story FCPXML; no v2 data is
  computed only for a report and then discarded.
- Failed takes cannot masquerade as proven-empty takes.
- Reuse cannot inherit current settings.
- Existing run-manifest-v1 artifacts remain valid; new prepared authority uses
  v2 instead of mutating a published v1 contract.
- VAD remains off because no authorized operational pin exists, and a test
  prevents the ordering constraint from being violated.
- The plan introduces no private path, fixture, identifier, or repository
  dependency.

## Observed RED checkpoint — 2026-08-22

Before any Task 14 production code or schema was added, the first acceptance
batch ran with the isolated worktree source explicitly first on `PYTHONPATH`:

```bash
PYTHONPATH=src /Users/hsin-hsinyuan/Documents/Claude/Projects/TriTrack-Editing-Assistant/venv/bin/python -m unittest tests.test_transcript_anomaly tests.test_pair_selection tests.test_transcription_result tests.test_task14_relay_projection tests.test_cli.Task14CommandBoundaryRedTest -v
```

Observed result: **21 tests, 21 failures, 0 errors**.

- 8 anomaly tests failed because the public `transcript_anomaly` module is
  absent.
- 6 pair-selection tests failed because the public `pair_selection` module is
  absent.
- 4 provenance/retry tests failed because the public `transcription_result`
  module is absent.
- 1 relay projection failed because `string_out` validates only sync-map-v1.
- 2 command-boundary tests failed because alternative/reuse and audio-master
  arguments are not registered.

The same changed test files pass Ruff, `git diff --check` is clean, and the
plan placeholder scan is empty. These failures are the expected missing-feature
RED state, not import-collection, syntax, fixture, or test-harness errors.
