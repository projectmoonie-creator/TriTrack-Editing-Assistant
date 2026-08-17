# Task 10 Immutable Run Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship three immutable local run transitions, read-only status, deterministic story-cut FCPXML, and a separate end-user editing skill without weakening Tasks 5–9 authority boundaries.

**Architecture:** `run_workflow.py` owns exact run manifests, complete-bundle validation, staged absent-directory publication, and prepare／align／finish transitions that call existing product functions directly. `story_fcpxml.py` owns the final projection from exact sync, aligned, grouping, and working-cut authorities into frame-exact FCPXML. The CLI exposes nested run verbs; the end-user skill guides only installed usage and human gates.

**Tech Stack:** Python 3.12+, `jsonschema` Draft 2020-12, `unittest`, existing bounded FFmpeg／whisper.cpp engines, `openpyxl`, FCPXML 1.14, Ruff, Codex skill validator.

---

## Frozen implementation details

- Mutating verbs are exactly `prepare`, `align`, and `finish`; `status` is
  read-only.
- Bundle filenames and phase artifact sets are exact as recorded in
  `docs/TASK-10-DECISION.md`.
- Canonical JSON uses UTF-8, `ensure_ascii=False`, `indent=2`,
  `sort_keys=True`, and one final newline.
- `runId` uses `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`. Media IDs are globally
  unique basenames. Source hashes are lowercase SHA-256.
- JSON artifacts are limited to 16 MiB; manifests and bundle artifacts must be
  nonempty regular non-symlink files. Fixed filenames never come from caller
  input.
- There are no timestamps or mutable run states. A published manifest means
  every listed stage completed.
- `text-revision-v1.takes` permits an empty list as explicit no-change
  approval. Per-take `revisions` remains nonempty when a take entry exists.
- A story segment uses authoritative aligned cue text and timing, working-cut
  order, exact grouping binding, current source hashes, sync offsets, and the
  declared audio master. Reserve entries are excluded.

### Task 1: Freeze the Task 10 contracts

**Files:**
- Modify: `src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json`
- Modify: `src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json`
- Modify: `tests/test_contracts.py`
- Modify: `tests/test_align_text.py`

- [ ] **Step 1: Write failing contract tests**

Replace the minimum run-manifest fixture with one prepared immutable manifest
containing closed phase／next-action values, an empty chain, one source, exact
artifacts, and completed stages. Add rejection cases for timestamps, mutable
status, unsafe filenames, phase/action mismatch, unsafe run IDs, bad source
hashes, duplicate source identity, and unknown stage names. Add an explicit
empty-`takes` no-change revision fixture and assert alignment preserves every
cue as `original` while binding the revision bytes.

- [ ] **Step 2: Run RED**

Run:

```bash
venv/bin/python -m unittest tests.test_contracts tests.test_align_text -v
```

Expected: FAIL because the old manifest shape is accepted／required and an
empty revision take list violates the current schema.

- [ ] **Step 3: Tighten the unused manifest and widen explicit approval**

Implement the exact manifest fields from the decision with
`additionalProperties: false`, closed enums, safe filenames, path-free source
entries, artifact hashes, stage input／output hash maps, and phase conditionals.
Change only the top-level revision `takes.minItems` from `1` to `0`.

- [ ] **Step 4: Run GREEN and full contract regression**

Run the focused command above, then:

```bash
venv/bin/python -m unittest tests.test_gemini_hybrid tests.test_organizer tests.test_paper_edit -v
```

Expected: all pass; offline hybrid still requires receipts only for revised
takes and Task 9 authority is unchanged.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json \
  src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json \
  tests/test_contracts.py tests/test_align_text.py docs/TASK-10-DECISION.md \
  docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
git commit -m "feat: freeze Task 10 run contracts"
```

### Task 2: Build the pure story-cut projection

**Files:**
- Create: `src/tritrack_editing_assistant/story_fcpxml.py`
- Create: `tests/test_story_fcpxml.py`
- Modify: `src/tritrack_editing_assistant/emit_fcpxml.py`

- [ ] **Step 1: Write the failing story happy-path test**

Build invented strict sync／aligned／grouping／working-cut objects plus probed
source records. Assert `build_story_timeline()` leaves inputs unchanged,
reorders active segments by `storyOrder`, derives title text from the aligned
cue range, quantizes start/end once to profile frames, layers paired A/B clips
using the sync offset, enables audio only on the declared master, excludes
reserve, and exposes stable sources／duration.

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_story_fcpxml.StoryTimelineTest -v
```

Expected: import failure because `story_fcpxml.py` does not exist.

- [ ] **Step 3: Implement the pure timeline types and validation**

Create frozen `StorySource`, `StoryClip`, `StorySegment`, and `StoryTimeline`
dataclasses. Add `build_story_timeline(sync_map, aligned, grouping,
working_cut, sources, *, aligned_sha256, grouping_sha256, profile)` that:

- validates all strict contracts and exact bindings;
- reuses Task 9 grouping semantics;
- requires question and story-order permutations;
- re-derives every selected cue span／text／timing／source hash;
- resolves unique source basenames against sync-map pairs／singles;
- converts milliseconds and sync offsets with
  `string_out.seconds_to_frames`; and
- requires complete declared audio-master coverage for paired selections.

Add a small public `probe_sources()` wrapper in `emit_fcpxml.py` around the
existing profile-bound probe implementation so the new module does not depend
on its private name.

- [ ] **Step 4: Run GREEN**

Run the focused story test and existing string-out／emit tests. Expected: PASS.

- [ ] **Step 5: Add semantic RED cases**

Cover changed aligned／grouping hashes, copied timing or source drift, unknown
take or cue, duplicate／gapped story order, mismatched grouping semantics,
foreign source hashes, missing sync source, insufficient audio-master
coverage, sub-frame／zero-length selection, and reserve leakage.

- [ ] **Step 6: Implement only missing guards and rerun GREEN**

Use stable `TRITRACK_STORY_*` codes and leave all source objects unchanged.

- [ ] **Step 7: Commit the pure projection**

```bash
git add src/tritrack_editing_assistant/story_fcpxml.py \
  src/tritrack_editing_assistant/emit_fcpxml.py tests/test_story_fcpxml.py
git commit -m "feat: build deterministic story timelines"
```

### Task 3: Render and publish story FCPXML

**Files:**
- Modify: `src/tritrack_editing_assistant/story_fcpxml.py`
- Modify: `tests/test_story_fcpxml.py`

- [ ] **Step 1: Write RED renderer and file-boundary tests**

Assert deterministic XML bytes, stable resource／style IDs, XML escaping,
profile and Basic Title retention, exact story duration, source clip starts,
one dialogue source per gap, title text from aligned authority, and successful
reuse of `emit_fcpxml.validate_fcpxml`. Add bounded regular JSON inputs,
canonical grouping／working-cut bytes, source rehash, late mutation, missing
parent, existing output before reads, publication race, cleanup, and unchanged
input cases.

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_story_fcpxml.StoryRenderingTest \
  tests.test_story_fcpxml.StoryFileBoundaryTest -v
```

Expected: failures because rendering and publication interfaces are absent.

- [ ] **Step 3: Implement renderer and end-to-end writer**

Add:

```python
def render_story_fcpxml(timeline: StoryTimeline, *, profile_id: str,
                        binding_id: str,
                        metadata: emit_fcpxml.ProjectMetadata) -> str: ...

def emit_story_and_publish(camera_a_sources, camera_b_sources, *,
                           sync_map_path: Path, aligned_path: Path,
                           grouping_path: Path, working_cut_path: Path,
                           profile_id: str, binding_id: str,
                           metadata: emit_fcpxml.ProjectMetadata,
                           output_path: Path) -> str: ...
```

Load 16 MiB JSON artifacts with `O_NOFOLLOW`, retain exact bytes／hashes,
require canonical grouping and working-cut encodings, probe and hash current
media, build and render in memory, rehash every input, then delegate final
validated absent-file publication to `emit_fcpxml.publish_fcpxml`.

- [ ] **Step 4: Run story GREEN and Task 6／9 regression**

```bash
venv/bin/python -m unittest tests.test_story_fcpxml tests.test_emit_fcpxml \
  tests.test_organizer tests.test_paper_edit -v
```

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/story_fcpxml.py \
  tests/test_story_fcpxml.py
git commit -m "feat: emit story-ordered Final Cut XML"
```

### Task 4: Implement manifest and immutable bundle infrastructure

**Files:**
- Create: `src/tritrack_editing_assistant/run_workflow.py`
- Create: `tests/test_run_workflow.py`

- [ ] **Step 1: Write RED pure manifest tests**

Assert canonical deterministic bytes, strict phase-specific artifact sets,
exact manifest chains, sorted unique sources, completed stage sets, artifact
filenames, and sanitized summaries. Assert invalid／noncanonical payloads,
unsafe IDs, duplicate sources, phase drift, wrong action, foreign artifact
sets, unknown stages, and path-shaped material fail closed.

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_run_workflow.RunManifestTest -v
```

Expected: import failure because `run_workflow.py` does not exist.

- [ ] **Step 3: Implement manifest builders and loaders**

Add focused interfaces:

```python
def build_manifest(*, run_id: str, profile_id: str, binding_id: str,
                   phase: str, manifest_chain: list[str],
                   sources: list[dict[str, object]],
                   stages: list[dict[str, object]],
                   artifacts: dict[str, dict[str, str]]) -> dict[str, object]: ...
def encode_manifest(payload: object) -> bytes: ...
def load_bundle(path: Path, *, expected_phase: str | None = None) -> LoadedRunBundle: ...
def summarize_bundle(bundle: LoadedRunBundle) -> dict[str, object]: ...
```

`load_bundle` requires an exact regular manifest, canonical bytes, fixed
artifact names, bounded regular non-symlink artifacts, exact hashes, semantic
phase invariants, and no unlisted entries other than the fixed files.

- [ ] **Step 4: Run manifest GREEN**

Expected: all pure tests pass.

- [ ] **Step 5: Write RED publication tests**

Cover absent parent／destination, dangling symlink, preexisting directory,
directory-reservation race, manifest-last linking, ordinary failure cleanup,
link failure cleanup, no caller-input deletion, deterministic repeat bundles,
and incomplete manifest-less bundle rejection.

- [ ] **Step 6: Implement staged bundle publication and rerun GREEN**

Use a hidden sibling temporary directory, reserve the destination with
`mkdir`, link fixed files with `run-manifest.json` last, fsync, and remove only
invocation-owned temporary／partial files on ordinary failures.

- [ ] **Step 7: Commit infrastructure**

```bash
git add src/tritrack_editing_assistant/run_workflow.py \
  tests/test_run_workflow.py
git commit -m "feat: add immutable run bundle core"
```

### Task 5: Implement prepare and align transitions

**Files:**
- Modify: `src/tritrack_editing_assistant/run_workflow.py`
- Modify: `tests/test_run_workflow.py`

- [ ] **Step 1: Write RED prepare tests**

Through injected／patched existing engine boundaries, assert the exact call
order doctor → sync → transcribe → emit, fail-fast unsupported doctor,
globally unique basenames, transcribe-media subset, current source hashes,
fixed output names, stage hashes, sanitized manifest, input rechecks, ordinary
failure cleanup, and no nested CLI／shell call.

- [ ] **Step 2: Observe RED and implement `prepare_run()`**

```python
def prepare_run(camera_a_sources, camera_b_sources, transcribe_media, *,
                model_path: Path, language: str, profile_id: str,
                binding_id: str, metadata: emit_fcpxml.ProjectMetadata,
                run_id: str, output_dir: Path) -> dict[str, object]: ...
```

Build all component artifacts in the staged directory, rehash source media and
model before publication, then publish the manifest last. Rerun and expect
GREEN.

- [ ] **Step 3: Write RED align tests**

Assert complete prepared-bundle validation before revision reads, exact
prepared and revision hash binding, no-change revision acceptance, calls to
alignment then paper export, fixed artifacts, manifest chain, unchanged
inputs, and cleanup／no-overwrite behavior.

- [ ] **Step 4: Implement `align_run()` and rerun GREEN**

```python
def align_run(prepared_dir: Path, revision_path: Path, *,
              output_dir: Path) -> dict[str, object]: ...
```

- [ ] **Step 5: Commit transitions**

```bash
git add src/tritrack_editing_assistant/run_workflow.py \
  tests/test_run_workflow.py
git commit -m "feat: prepare and align immutable runs"
```

### Task 6: Implement finish and status transitions

**Files:**
- Modify: `src/tritrack_editing_assistant/run_workflow.py`
- Modify: `tests/test_run_workflow.py`

- [ ] **Step 1: Write RED finish tests**

Assert prepared／aligned phase and chain validation, exact run/profile/binding/
source equality, current caller media hashes, workbook apply → organizer →
story emit order, fixed outputs, finished chain, input rechecks, sanitized
manifest, no-overwrite, and failure cleanup.

- [ ] **Step 2: Implement `finish_run()` and rerun GREEN**

```python
def finish_run(prepared_dir: Path, aligned_dir: Path, workbook_path: Path,
               camera_a_sources, camera_b_sources, *,
               metadata: emit_fcpxml.ProjectMetadata,
               output_dir: Path) -> dict[str, object]: ...
```

- [ ] **Step 3: Write RED read-only status tests**

Assert status validates exact artifacts, writes nothing, returns only schema,
run ID, phase, next action, stage names, logical artifact names, and hashes,
and rejects incomplete／changed／symlinked bundles.

- [ ] **Step 4: Implement `status_run()` and run complete workflow GREEN**

```python
def status_run(run_dir: Path) -> dict[str, object]: ...
```

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/run_workflow.py \
  tests/test_run_workflow.py
git commit -m "feat: finish and inspect immutable runs"
```

### Task 7: Expose the installed CLI

**Files:**
- Modify: `src/tritrack_editing_assistant/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_quickstart_demo.py`

- [ ] **Step 1: Write RED parser／help tests**

Assert exact nested verbs and flags from the decision; exclude provider,
upload, credential, overwrite, mutable-resume, private, and release language.
Change component 11 only from planned to implemented; keep exactly eleven.

- [ ] **Step 2: Run RED and wire parsers／handlers**

Map source arguments into `MediaSource`, construct metadata, invoke only
`run_workflow` functions, print sanitized JSON summaries, and classify stable
run／story／existing component codes into the established exit classes.

- [ ] **Step 3: Add RED installed smoke and failure mapping**

Cover status success, existing output before engine work, incomplete bundle,
invalid manifest／chain, source mismatch, missing parent, unsupported doctor,
and no traceback／stderr leakage. Use invented fixtures and patch only external
media engines where unavoidable.

- [ ] **Step 4: Run CLI and registry GREEN**

```bash
venv/bin/python -m unittest tests.test_cli tests.test_quickstart_demo -v
venv/bin/tritrack run --help
venv/bin/tritrack components --json
```

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/cli.py tests/test_cli.py \
  tests/test_quickstart_demo.py
git commit -m "feat: expose immutable run commands"
```

### Task 8: Create and firewall the end-user skill

**Files:**
- Create: `skills/tritrack-editing-assistant/SKILL.md`
- Create: `skills/tritrack-editing-assistant/agents/openai.yaml`
- Modify: `tests/test_maintainer_boundary.py`

- [ ] **Step 1: Write RED firewall tests**

Require the separate end-user skill and agent metadata; exact name／trigger;
help-first installed command usage; prepare／revision／align／paper／finish human
gates; no-overwrite／local-only rules; and explicit workbook non-authority.
Reject maintainer skill name, task numbers, branch／release／standing-grant／
tester language, private project names, absolute home paths, credentials,
provider transport, and direct source-module orchestration.

- [ ] **Step 2: Observe RED**

```bash
venv/bin/python -m unittest tests.test_maintainer_boundary -v
```

Expected: FAIL because the end-user skill is absent.

- [ ] **Step 3: Initialize and author the skill**

Run the canonical `skill-creator/scripts/init_skill.py` for
`tritrack-editing-assistant` at repository `skills/`, with exact interface
metadata and no unused resource folders. Replace the generated body with a
concise imperative workflow that delegates all product behavior to installed
command help and preserves both human gates.

- [ ] **Step 4: Validate and run firewall GREEN**

Run both:

```bash
python3 /Users/hsin-hsinyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
venv/bin/python -m unittest tests.test_maintainer_boundary -v
```

- [ ] **Step 5: Commit**

```bash
git add skills/tritrack-editing-assistant tests/test_maintainer_boundary.py
git commit -m "feat: add the end-user editing skill"
```

### Task 9: Documentation, verification, and closeout

**Files:**
- Modify: `README.md`
- Modify: `docs/TOOLING.md`
- Modify: `docs/ROADMAP.md`
- Modify: `STATUS.md`
- Modify: `CHANGELOG.md`
- Create: `docs/TASK-10-VERIFICATION.md`
- Create: `docs/reviews/task-10-closeout-packet-2026-08-17.md`
- Create: closeout raw status／adjudication files under `docs/reviews/`

- [ ] **Step 1: Write RED documentation／boundary assertions**

Update maintainer tests to require Task 10 command authorities, immutable
bundle language, final story projection, separate skill identity, Task 11 as
next action, and honest deferrals. Keep public governance free of private paths
and unimplemented claims.

- [ ] **Step 2: Update public docs after the coherent implementation is green**

Document exact installed examples, fixed bundle contents, both human gates,
manifest non-authority, source custody, story FCPXML scope, crash-incomplete
behavior, and unchanged outward-action boundary. Update component 11 to
implemented and retain `validate`／live provider transport as planned.

- [ ] **Step 3: Run final local gates after the last edit**

```bash
venv/bin/python -m unittest tests.test_run_workflow tests.test_story_fcpxml \
  tests.test_cli tests.test_maintainer_boundary -v
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples
venv/bin/python -m compileall -q src tests examples
python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
python3 /Users/hsin-hsinyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
python3 /Users/hsin-hsinyuan/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
git diff --check
```

Build an sdist／wheel in an absent ignored directory, install it into an absent
temporary Python 3.13 environment, and run installed components, run help,
strict invented manifest/status, no-change align, finish, and deterministic
story-output acceptance. Validate story FCPXML against the installed DTD when
available without claiming GUI import.

- [ ] **Step 4: Freeze and send one public-safe closeout packet**

Include candidate commit/tree identity, decision, diff, RED／GREEN evidence,
tests, role firewall, privacy／authority matrix, and explicit non-claims. Send
the same bytes through the approved Gemini and Claude wrappers. Preserve exact
requested／observed／completed models and incomplete attempts. Locally
adjudicate every finding, fix ordinary in-scope issues with new RED tests, and
rerun all gates. Stop after two NEEDS_REVISION rounds for producer adjudication.

- [ ] **Step 5: Record verification and custody**

Only after the last edit and full green, write `docs/TASK-10-VERIFICATION.md`
and update `STATUS.md` to make Task 11 next. Commit only Task 10 files,
fast-forward local `main`, push existing public `origin/main`, and require:

```bash
git rev-parse HEAD
git rev-parse main
git rev-parse origin/main
git ls-remote origin refs/heads/main
```

All four SHA values must match the final green candidate. No tag, release, PR,
tester contact, package publication, or application submission is performed.
