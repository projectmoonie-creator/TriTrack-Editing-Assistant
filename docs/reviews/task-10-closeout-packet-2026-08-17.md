# Task 10 Closeout Review Packet — 2026-08-17

## Frozen review target

- Repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Lane: public OSS engine
- Branch: `codex/task10-run-end-user-skill`
- Base: `a0dd314938286414f218f5011b5090c6734e9c78` (`origin/main` at kickoff)
- Candidate: `08517f477ae263664f981c002cc974c77fba291a`
- Scope: Task 10 — immutable prepared/aligned/finished run bundles, read-only status, deterministic story-ordered FCPXML, and the separate end-user editing skill.
- Review mode: read-only independent closeout review. Do not edit files.

## Accepted architecture and contracts

The producer selected option A: three explicit immutable stage bundles plus a
final story-ordered FCPXML projection.

- `tritrack run prepare` calls the existing doctor → sync → transcribe → emit
  functions and publishes fixed prepared artifacts into one absent directory.
- The editor must deliberately supply one exact-byte-bound
  `text-revision-v1`; `takes: []` is the explicit no-change approval.
- `tritrack run align` promotes that revision, exports the non-authoritative
  paper workbook, and publishes a separate aligned bundle.
- The editor changes only the workbook's allowed intent tables.
- `tritrack run finish` applies the workbook, compiles the working cut, and
  emits `story-cut.fcpxml` into a separate finished bundle.
- `tritrack run status` validates a complete bundle and returns only a
  path-free, text-free summary.

Every phase has a closed artifact set, completed stage set, exact artifact
hashes, ordered prior-manifest hashes, and a canonical manifest. Mutating
transitions require absent output directories, reserve the directory, hard-link
artifacts, and hard-link the manifest last. Existing state and race winners are
never overwritten or repaired.

The story renderer must reopen the exact aligned, grouping, working-cut,
sync-map, and source authorities; rederive active cue text/timing/story order;
quantize boundaries once to the compatibility profile's frame grid; preserve
paired-source offsets; require full declared audio-master coverage; exclude
reserve; detect late input mutation; and atomically publish deterministic strict
FCPXML.

The workbook remains transport only. The end-user skill must discover installed
help before flags, keep the two human gates explicit, and contain no maintainer
task state, release authority, private workflow, credentials, or provider
transport.

## Non-goals

No network request, credential lookup, provider transport, live upload, Final
Cut automation, DTD claim, Final Cut GUI claim, release tag, package
publication, tester contact, application submission, or private-project
operation is in Task 10.

## Verification completed on the frozen candidate

- Baseline before Task 10: 155 tests passed.
- Full source suite after the final manifest closure fix: 193 tests passed.
- Maintainer boundary suite: 9/9 passed.
- Ruff over `src tests examples`: passed.
- `compileall` over `src tests examples`: passed.
- Repository identity: `ok: true`, `lane: OSS`, `projectKind: public-engine`.
- Current skill validator: maintainer skill and end-user skill both passed.
- `git diff --check`: passed.
- Non-editable wheel build/install passed installed `run --help`, the exact
  eleven-component registry with component 11 implemented, and read-only
  `run status` against a complete invented aligned bundle.
- Wheel SHA-256:
  `078c8761a663baca1b567ef9978bf07cfbf092537d504574811e4418ffc5a534`.
- All test and acceptance fixtures use invented content.

## Review request

Review the complete frozen diff below for release-blocking defects and material
gaps. Concentrate on:

1. Manifest/schema/semantic fidelity, closed phase sets, exact chain binding,
   canonical encoding, and installed-resource behavior.
2. Immutable publication: no overwrite, races, incomplete bundles, cleanup,
   hard-link assumptions, symlinks, TOCTOU, mutation detection, and custody.
3. Transition orchestration: doctor fail-fast, exact dependency order,
   source/model/transcript/revision/workbook binding, and error sanitization.
4. Story FCPXML: authority rebinding, frame math, story ordering, paired-source
   offsets, dialogue master coverage, reserve exclusion, deterministic XML, and
   Final Cut profile consistency.
5. End-user/maintainer role firewall, help-first guidance, human gates, privacy,
   network/provider boundaries, and honest non-goals.
6. CLI exit semantics, path/text leakage, complete-bundle status, component
   registry accuracy, and wheel-installed behavior.
7. Test adequacy, documentation accuracy, roadmap/status coherence, and
   governance compliance.

Return exactly this structure:

- `VERDICT: PASS` or `VERDICT: CHANGES_REQUIRED`
- `MODEL: <exact observed model id if known, otherwise unknown>`
- `SUMMARY: <brief assessment>`
- `FINDINGS:`
  - If none, write `NO_FINDINGS`.
  - Otherwise, one finding per item with ID, severity P0/P1/P2/P3, file and
    line, evidence, impact, reproduction or missing test, and minimal fix.
- `CONTRACT_COVERAGE:` checklist across the seven dimensions above.

Do not report speculative style preferences as defects. Every finding must cite
concrete code evidence and an actionable failure mode. Do not claim to have run
tools or tests unless you actually did. Do not modify the repository.

## Complete frozen diff

```diff
diff --git a/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md b/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
index 46e15d9..ba8c89a 100644
--- a/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
+++ b/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
@@ -43,9 +43,9 @@ TriTrack project.
 ## Hold the role firewall
 
 - This skill owns public repository development and maintenance only.
-- The future `skills/tritrack-editing-assistant/SKILL.md` is the end-user
-  product skill. Do not create it before its roadmap task or put maintainer
-  state, task numbers, release authority, or application strategy inside it.
+- `skills/tritrack-editing-assistant/SKILL.md` is the separate installed
+  end-user product skill. Keep maintainer state, task numbers, release
+  authority, and application strategy out of it.
 - Never browse another repository for source, status, media, transcripts,
   journals, templates, credentials, or history. Consume only a separately
   reviewed clean-room intake that has been deliberately handed to the public
diff --git a/AGENTS.md b/AGENTS.md
index dca0d9b..3c0ad2e 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -26,9 +26,8 @@ planned evidence before mutating project state.
 
 - `tritrack-editing-assistant-maintainer` owns this repository's development
   and maintenance.
-- The later `tritrack-editing-assistant` skill is an installed end-user
-  product surface. It must contain no maintainer task state or release
-  authority.
+- `skills/tritrack-editing-assistant/SKILL.md` is the installed end-user
+  product surface. It contains no maintainer task state or release authority.
 - Private production orchestration is a different project. Do not scan its
   repositories or import its status, media, transcripts, journals, templates,
   credentials, or history. Accept only reviewed clean-room intake with exact
diff --git a/CHANGELOG.md b/CHANGELOG.md
index f44e23b..1e14efc 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -25,6 +25,16 @@ format follows Keep a Changelog, and releases will use semantic versioning.
   `transcript-bundle-v1`, model/source hash provenance, deterministic cue
   canonicalization and silence outcomes, structural artifact guards, input
   change detection, bounded temporary evidence, and atomic no-overwrite output.
+- Cue-addressed revision promotion, strict grouping and working-cut JSON, and a
+  four-worksheet paper-edit transport that preserves aligned text and timing
+  authority.
+- Task 10 immutable prepared／aligned／finished run bundles with exact manifest
+  chains, fixed artifact sets, manifest-last publication, and read-only status.
+- Deterministic story-ordered FCPXML projection with authoritative cue text and
+  timing re-derivation, paired-source offsets, audio-master coverage, and
+  reserve exclusion.
+- Separate `tritrack-editing-assistant` end-user skill with installed-help
+  discovery and explicit text-revision and paper-edit human gates.
 
 ### Fixed
 
diff --git a/README.md b/README.md
index 546bf07..234c1d6 100644
--- a/README.md
+++ b/README.md
@@ -9,9 +9,9 @@ decisions with the editor.
 > the fail-closed `doctor` command, local audio-verified `sync`, fixed-profile
 > local `transcribe`, deterministic cue-addressed `align`, offline receipt-only
 > `hybrid`, profile-bound deterministic `emit`, strict `paper export`／
-> `paper apply`, and deterministic `organize`. Remaining editing commands are
-> listed as `planned` and deliberately return a non-success status until their
-> implementation and tests land. There is no public release yet.
+> `paper apply`, deterministic `organize`, and immutable `run prepare`／
+> `align`／`finish`／`status`. `validate` and the optional live transport remain
+> planned and fail closed. There is no public release yet.
 
 ## Target alpha compatibility
 
@@ -223,6 +223,51 @@ All three Task 9 operations are local-only and make no network, provider,
 credential, media-processing, subprocess, FCPXML, or orchestration request.
 Every output path must be absent.
 
+## Task 10 immutable run workflow
+
+Task 10 connects the installed local commands through three immutable bundles
+and two explicit editor gates. Start by reading the installed command help:
+
+```bash
+venv/bin/tritrack run --help
+venv/bin/tritrack run prepare --help
+venv/bin/tritrack run align --help
+venv/bin/tritrack run finish --help
+venv/bin/tritrack run status --help
+```
+
+`run prepare` accepts repeatable camera A／B paths, a repeatable transcription
+subset, the caller-owned local model, explicit language, public profile and
+title binding, caller-owned event／project names, a safe run ID, and one absent
+output directory. It runs doctor → sync → transcribe → string-out and publishes
+exactly `doctor.json`, `sync-map.json`, `transcript-bundle.json`,
+`string-out.fcpxml`, and `run-manifest.json`.
+
+Pause for the editor to provide one strict `text-revision-v1` bound to the
+exact transcript bytes. An empty `takes: []` is accepted only as explicit
+no-change approval. Then `run align` consumes the complete prepared bundle and
+revision, publishing `aligned-transcript.json`, `paper-edit.xlsx`, and a new
+manifest into another absent directory.
+
+Pause again while the editor changes only the workbook's `Questions` and
+`Selections` tables. The workbook is transport, not authority. `run finish`
+consumes the exact prepared and aligned bundles, edited workbook, and original
+camera sources; it publishes canonical `grouping.json`, text-free
+`working-cut.json`, story-ordered `story-cut.fcpxml`, and a finished manifest.
+The story renderer re-derives cue text and timing from strict JSON authorities,
+honors sync offsets and the declared audio master, and excludes reserve ranges.
+
+Every mutating stage requires a new absent directory and publishes its manifest
+last. `run status` is read-only and returns only the run ID, phase, next action,
+completed stage names, and logical artifact hashes. The workflow makes no
+network call and does not claim a Final Cut GUI import, DTD validation, or
+round trip.
+
+The separate installed skill at
+`skills/tritrack-editing-assistant/SKILL.md` guides editors through the two
+human gates using help-first installed commands. It contains no repository
+maintenance or publication authority.
+
 ## One-minute invented quickstart
 
 After the development installation above, exercise the complete implemented
@@ -256,8 +301,10 @@ Choose the narrowest entry point that matches your goal:
    cue-addressed grouping intent through a non-authoritative workbook.
 7. Use `tritrack organize` to compile that intent into a deterministic
    text-free working cut.
-8. Use `tritrack components --json` to inspect what is implemented before
-   trying later roadmap commands; planned commands still fail closed.
+8. Use `tritrack run` to carry the exact local artifacts through immutable
+   prepared, aligned, and finished bundles with explicit editor approval.
+9. Use `tritrack components --json` to inspect what is implemented before
+   trying later roadmap commands; `validate` still fails closed.
 
 ## Eleven-component roadmap
 
@@ -279,7 +326,7 @@ tritrack components --json
 | 8 | `align_text.py` | `tritrack align` | implemented |
 | 9 | `gemini_hybrid.py` | `tritrack hybrid` | implemented, offline optional |
 | 10 | `gemini_transcribe.mjs` | `tritrack hybrid` | planned, optional |
-| 11 | `multicam-sync` | `tritrack run` | planned |
+| 11 | `multicam-sync` | `tritrack run` | implemented |
 
 `components`, `doctor`, schemas, packaging, fixtures, tests, and release
 automation are supporting infrastructure and do not increase the component
diff --git a/STATUS.md b/STATUS.md
index 8a13ca2..2d1ded3 100644
--- a/STATUS.md
+++ b/STATUS.md
@@ -1,6 +1,6 @@
 # Public maintenance status
 
-Updated: 2026-08-15
+Updated: 2026-08-17
 Project kind: public engine
 Lane: `OSS`
 Release state: public pre-release source; no tag, package publication, or
@@ -8,7 +8,7 @@ tester outreach
 
 ## Current gate
 
-Tasks 1–9 are complete in this public candidate. Task 6 began from exact
+Tasks 1–10 are complete in this public candidate. Task 6 began from exact
 Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
 fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
 rewrite or merge commit.
@@ -99,12 +99,31 @@ compile matrix. Post-fix review-record candidate
 and GitHub Actions run `31907255236` passed its Python 3.12／3.13 test, lint,
 and compile matrix. Sanitized evidence is in `docs/TASK-9-VERIFICATION.md`.
 
+Task 10 implementation candidate
+`5fe9a4531f8dbd23f98174023d61f66a359d461b` adds installed
+`tritrack run prepare`, `align`, `finish`, and read-only `status` commands.
+Each mutating transition publishes a new immutable absent directory with its
+manifest hard-linked last; fixed artifact names, exact byte hashes,
+phase-specific completed stages, and the prior-manifest chain are validated
+before reuse. The final story renderer re-derives every active range and title
+from exact aligned／grouping／working-cut authorities, quantizes once to profile
+frames, honors paired-source offsets and the declared audio master, excludes
+reserve, and emits strict story-ordered FCPXML. Task 10 also installs the
+separate end-user `tritrack-editing-assistant` skill with help-first command
+discovery and explicit text-revision and paper-edit human gates. The workbook
+remains transport only. The workflow makes no network request and does not
+claim a Final Cut GUI import, DTD result, or round trip. Sanitized evidence is
+in `docs/TASK-10-VERIFICATION.md`.
+Local verification passed 193 complete-suite and 9 maintainer-boundary tests,
+plus Ruff, compilation, identity, both skill validators, non-editable wheel
+help／status smoke, registry, and diff gates.
+
 ## Next action
 
-Task 10 implements the installed `run` workflow and the separate end-user
-`tritrack-editing-assistant` skill. It must preserve the maintainer/end-user
-role firewall and must not turn the Task 9 workbook into transcript or timing
-authority.
+Task 11 expands the release-grade CI matrix and completes the privacy,
+provenance, packaging, and release gates. Task 10 does not authorize or claim
+tags, releases, package publication, tester contact, or application
+submission.
 
 ## Implemented surface
 
@@ -122,6 +141,10 @@ authority.
 - cue-addressed grouping with deterministic working-cut compilation;
 - strict local paper-edit export/apply with complete aligned-grid
   re-derivation, semantic round trips, and atomic no-overwrite publication;
+- immutable prepared／aligned／finished run bundles with exact manifest chains,
+  fixed artifacts, manifest-last publication, and read-only status;
+- deterministic story-ordered FCPXML projection from exact editor authorities;
+- separate installed end-user editing skill with two explicit human gates;
 - fail-closed `doctor` command;
 - exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
 - public Basic Title binding with invented-content Final Cut round-trip
@@ -129,9 +152,9 @@ authority.
 - public invented-media synchronization-to-FCPXML quickstart with deterministic
   repeat emission, conditional local DTD verification, and minimal CI.
 
-`validate` and `run` remain planned and must return non-success until
-implemented and tested. The network-capable
-`gemini_transcribe.mjs` component also remains planned.
+`validate` remains planned and must return non-success until implemented and
+tested. The network-capable `gemini_transcribe.mjs` component also remains
+planned.
 
 ## Custody
 
diff --git a/docs/ROADMAP.md b/docs/ROADMAP.md
index 71adbb8..6bb0b15 100644
--- a/docs/ROADMAP.md
+++ b/docs/ROADMAP.md
@@ -28,11 +28,12 @@ here.
 - Task 9: strict cue-addressed grouping, deterministic working-cut compilation,
   and a local XLSX paper-edit round trip with complete reference-grid
   re-derivation. The workbook is a transport; JSON remains authoritative.
+- Task 10: installed immutable `run prepare`／`align`／`finish` bundles,
+  read-only `run status`, deterministic story-ordered FCPXML, and a separate
+  end-user `tritrack-editing-assistant` skill with explicit human gates.
 
 ## Next
 
-- Task 10: implement the installed `run` workflow and create the separate
-  end-user `skills/tritrack-editing-assistant/SKILL.md`.
 - Task 11: expand the release-grade CI matrix and complete the privacy,
   provenance, packaging, and release gates.
 - Task 12: freeze and independently review the alpha candidate.
diff --git a/docs/TASK-10-DECISION.md b/docs/TASK-10-DECISION.md
new file mode 100644
index 0000000..260e213
--- /dev/null
+++ b/docs/TASK-10-DECISION.md
@@ -0,0 +1,283 @@
+# Task 10 immutable run-workflow decision
+
+Decision date: 2026-08-17
+
+Decision owner: producer
+
+Selected option: A — immutable explicit stage bundles with final story FCPXML
+
+## Decision
+
+Task 10 implements the installed `tritrack run` surface as three explicit,
+immutable transitions plus one read-only status command:
+
+```text
+prepare -> human text-revision gate -> align
+        -> human paper-edit gate -> finish -> story-cut FCPXML
+```
+
+Every mutating transition publishes a new absent directory. It never changes a
+prior bundle, source artifact, workbook, manifest, or result. A bundle is
+complete only when its manifest is present and validates every fixed artifact
+name and exact byte hash. Ordinary failures remove the unpublished staging
+directory. A process crash may leave an incomplete reserved output directory;
+the runner never repairs or overwrites it.
+
+`run-manifest-v1` is workflow receipt and index authority only. It is not
+transcript, cue timing, grouping, working-cut, media, workbook, or FCPXML
+authority. Those roles remain with their existing strict artifacts.
+
+## Public command surface
+
+### Prepare
+
+```text
+tritrack run prepare \
+  --camera-a A-001.MP4 [--camera-a ...] \
+  --camera-b B-001.MP4 [--camera-b ...] \
+  --transcribe-media A-001.MP4 [--transcribe-media ...] \
+  --model ggml-model.bin \
+  --language en \
+  --profile uhd-2997-ndf-fcpxml-1.14 \
+  --binding basic-title-v1 \
+  --event-name "Interview" \
+  --project-name "Synchronized string-out" \
+  --run-id interview-001 \
+  --output prepared-run \
+  [--json]
+```
+
+`prepare` requires globally unique source basenames. Every transcribed path
+must be one of the declared camera sources. It performs the exact installed
+doctor, synchronization, fixed local transcription, and synchronized
+string-out operations through product Python functions, not a shell or nested
+CLI. The doctor receipt must report `supported: true` before later engines run.
+
+The absent bundle contains exactly:
+
+- `doctor.json`;
+- `sync-map.json`;
+- `transcript-bundle.json`;
+- `string-out.fcpxml`; and
+- `run-manifest.json`.
+
+The published manifest reports `nextAction: provide-revision`. The editor or
+terminal-capable agent then authors one strict `text-revision-v1` bound to the
+exact transcript bytes. Task 10 permits `takes: []` as an explicit no-change
+approval; it does not silently infer approval.
+
+### Align
+
+```text
+tritrack run align \
+  --prepared prepared-run \
+  --revision text-revision.json \
+  --output aligned-run \
+  [--json]
+```
+
+`align` validates the complete prepared bundle and the strict revision before
+writing. It invokes the existing alignment core and exports the Task 9 paper
+workbook from the exact aligned bytes.
+
+The absent bundle contains exactly:
+
+- `aligned-transcript.json`;
+- `paper-edit.xlsx`; and
+- `run-manifest.json`.
+
+The manifest binds the exact prepared-manifest and revision hashes and reports
+`nextAction: edit-paper-workbook`. The workbook remains a transport only. The
+editor changes only the Task 9 `Questions` and `Selections` tables.
+
+### Finish
+
+```text
+tritrack run finish \
+  --prepared prepared-run \
+  --aligned aligned-run \
+  --workbook edited-paper.xlsx \
+  --camera-a A-001.MP4 [--camera-a ...] \
+  --camera-b B-001.MP4 [--camera-b ...] \
+  --event-name "Interview" \
+  --project-name "Story cut" \
+  --output finished-run \
+  [--json]
+```
+
+`finish` validates both earlier bundles and their manifest chain, rehashes the
+caller-supplied media against the prepared source set, applies the workbook to
+canonical `grouping-v1`, compiles `working-cut-v1`, and renders a deterministic
+story-ordered FCPXML from the exact sync map, aligned transcript, grouping,
+working cut, and local media.
+
+The absent bundle contains exactly:
+
+- `grouping.json`;
+- `working-cut.json`;
+- `story-cut.fcpxml`; and
+- `run-manifest.json`.
+
+The manifest reports `nextAction: complete`. It does not claim a Final Cut GUI
+import, DTD validation, or round trip.
+
+### Status
+
+```text
+tritrack run status --run prepared-run [--json]
+```
+
+`status` is read-only. It validates one complete bundle, fixed names, exact
+artifact hashes, strict manifest semantics, and supported artifact contracts
+where applicable. It emits only run ID, phase, next action, stage names, and
+artifact logical names／hashes. It does not print paths, transcript text,
+question text, notes, or FCPXML content.
+
+## `run-manifest-v1`
+
+The unused pre-release schema is tightened in place. Canonical bytes are UTF-8
+JSON with sorted keys, two-space indentation, and one final newline. The
+manifest contains:
+
+- closed schema and tool versions;
+- a safe caller-owned `runId`;
+- exact public profile and title-binding IDs;
+- `phase`: `prepared`, `aligned`, or `finished`;
+- `nextAction`: `provide-revision`, `edit-paper-workbook`, or `complete`;
+- `manifestChain`: the ordered SHA-256 values of prior manifests;
+- a sorted path-free source list with camera, basename media ID, exact source
+  SHA-256, and whether that source was transcribed;
+- a closed artifact map whose entries contain a fixed safe filename and exact
+  SHA-256; and
+- completed stage records with closed names plus exact input and output hash
+  maps.
+
+There are no timestamps, mutable statuses, absolute paths, command arguments,
+logs, durations, transcript text, editor text, or credentials. An immutable
+manifest describes only completed work; `planned`, `running`, and `failed`
+states therefore do not belong in the contract.
+
+The phase-specific artifact sets are exact:
+
+- prepared: doctor receipt, sync map, transcript bundle, string-out FCPXML;
+- aligned: aligned transcript and paper workbook;
+- finished: grouping, working cut, and story-cut FCPXML.
+
+The aligned manifest chain contains the prepared manifest hash. The finished
+chain contains the prepared and aligned manifest hashes in that order.
+
+## Final story projection
+
+The story renderer never trusts copied timing or text:
+
+1. Reopen and hash the exact aligned, grouping, and working-cut artifacts.
+2. Require `working-cut-v1` to bind the exact aligned and grouping bytes.
+3. Re-derive every story segment's take, cue range, source hash, start/end
+   milliseconds, question membership, and `storyOrder` from the aligned and
+   grouping authorities.
+4. Match each selected take ID to one globally unique source basename and
+   require the current source bytes to match the recorded source SHA-256.
+5. Quantize cue boundaries once to the declared integer-frame profile.
+6. For paired sources, use the sync-map offset to layer both intersecting
+   camera clips. Require the declared audio-master clip to cover the complete
+   selected interval; otherwise fail closed. Unpaired selections retain their
+   own audio.
+7. Concatenate only the selected authoritative cue text into the public Basic
+   Title for that story segment. The FCPXML is a rendered output, not a new
+   transcript authority.
+8. Validate the resulting FCPXML against the existing strict public profile
+   and Basic Title binding, then publish only to an absent path.
+
+Reserve ranges do not enter the active story timeline. Segment order is the
+exact `storyOrder` permutation. No semantic classification, retiming, cue
+splitting, angle choice, effect design, or title-layout invention occurs.
+
+## Bundle publication and resume boundary
+
+Each transition builds under a hidden sibling staging directory. After every
+component succeeds and all inputs are rehashed, it atomically reserves the
+absent destination directory and links the fixed staged files into it with the
+manifest last. On an ordinary error it removes only files and directories
+created by that invocation. It never removes or modifies caller input.
+
+The manifest-last rule makes an interrupted bundle mechanically incomplete.
+No command infers or reconstructs a missing manifest from nearby artifacts.
+Resume always means consuming a complete immutable prior bundle and publishing
+a new absent bundle.
+
+## End-user skill boundary
+
+`skills/tritrack-editing-assistant/SKILL.md` is an installed editing co-pilot
+entry point. It:
+
+- checks installed `tritrack ... --help` before naming flags;
+- helps the editor choose source roles, transcription inputs, run ID, and
+  absent output directories;
+- invokes only the public installed commands;
+- explains the two human gates and never authors silent approval;
+- treats the workbook as transport and JSON as authority;
+- reads only sanitized command summaries and local artifacts the editor puts
+  in scope; and
+- stops on a compatibility, custody, overwrite, or strict-artifact failure.
+
+It contains no maintainer task numbers, branch or release state, standing
+grants, tester strategy, private repository references, private workflow
+knowledge, credentials, or publication authority. The maintainer skill remains
+the only development and release entry point.
+
+## Stable failure boundaries
+
+Task 10 uses `TRITRACK_RUN_*` for manifest, bundle, source-set, stage, and
+workflow errors; `TRITRACK_STORY_*` for story projection errors; and existing
+component error codes when a component itself rejects input. CLI mapping keeps
+the established exit classes:
+
+- malformed command intent: usage;
+- invalid schema, manifest chain, hashes, source identity, workbook state, or
+  story semantics: data;
+- unsupported doctor result or missing processing dependency: dependency／
+  policy as already classified;
+- unreadable input or missing parent: I/O;
+- existing output or publication race: output-exists; and
+- no failure prints a traceback or sensitive content.
+
+## Deferred alternatives and non-goals
+
+- one mutable project directory or mutable manifest;
+- automatic resume by scanning nearby files;
+- a general DAG or plugin workflow engine;
+- live provider transport, upload, deletion, credentials, or model selection;
+- implementation of the planned `validate` command;
+- workbook or manifest authority over transcript, timing, or editor intent;
+- Final Cut GUI automation or unrecorded import claims;
+- Task 11 release CI, tags, releases, pull requests, tester contact, package
+  publication, or private downstream integration.
+
+## Verification target
+
+Acceptance preserves observed RED-to-GREEN evidence for the manifest contract,
+explicit no-change revision, pure story projection, exact authority rebinding,
+frame quantization, paired／unpaired audio behavior, bundle loading and
+publication, every phase transition, CLI help／exit behavior, sanitized status,
+and the maintainer／end-user skill firewall.
+
+Closeout additionally requires focused and full tests, Ruff, compilation,
+project identity, both skill validations, public-boundary tests,
+`git diff --check`, installed CLI acceptance with invented inputs, deterministic
+repeat outputs, closeout review with bounded fix-forward, minimal CI, and exact
+public remote-main SHA backup verification.
+
+## Brainstorm provenance
+
+The frozen public problem packet SHA-256 was
+`80af43be795fc7638b7ecd49c26b6f7525ab7e97239f9d9b71b804caf0cf06c5`.
+
+Codex completed its independent first round before reading external outputs.
+Gemini requested, observed, and completed `gemini-3.7-flash`; its response
+SHA-256 was
+`18a1d0ce36cdae9c6c192116a30d5f233812ce60fe82ddc91a4ad39db183904c`.
+Claude requested the dynamic `opus` capability alias through the approved
+subscription-only wrapper. Attempt
+`2dcf4cdb-6654-4a29-8fd7-f4131fa9f1f4` timed out with no observed or completed
+model and ambiguous request state; it remains explicitly incomplete with no
+retry or billing fallback. The producer selected option A on 2026-08-17.
diff --git a/docs/TASK-10-VERIFICATION.md b/docs/TASK-10-VERIFICATION.md
new file mode 100644
index 0000000..19f8f78
--- /dev/null
+++ b/docs/TASK-10-VERIFICATION.md
@@ -0,0 +1,94 @@
+# Task 10 verification
+
+Date: 2026-08-17
+
+Implementation candidate: `5fe9a4531f8dbd23f98174023d61f66a359d461b`
+
+## Public scope proven
+
+Task 10 implements the installed `tritrack run prepare`, `run align`, `run
+finish`, and read-only `run status` commands. Every mutating transition creates
+a new immutable absent directory with a canonical phase-specific manifest,
+fixed artifact names, exact SHA-256 values, completed stage records, and the
+ordered hashes of prior manifests. The manifest is published last.
+
+The finished bundle contains canonical grouping and working-cut JSON plus
+`story-cut.fcpxml`. The story renderer reopens the exact aligned, grouping, and
+working-cut authorities; re-derives each active cue span, text, timing, source
+hash, and story order; converts boundaries once to profile frames; layers
+paired sources through the sync offset; requires full declared audio-master
+coverage; and excludes reserve ranges.
+
+The separate `skills/tritrack-editing-assistant/SKILL.md` is the installed
+end-user editing entry point. It consults installed help before flags, preserves
+the explicit text-revision and paper-edit human gates, requires absent outputs,
+and states that the workbook is transport rather than authority. Maintainer
+task state and publication authority remain in the repository-local maintainer
+skill.
+
+The workflow performs no network request, credential lookup, provider
+transport, live upload, Final Cut automation, or private-project operation. It
+makes no claim of a Final Cut GUI import, DTD validation, or round trip.
+
+## Architecture decision and consultation
+
+The producer selected option A: three explicit immutable stage bundles plus a
+final story-ordered FCPXML projection. The frozen brainstorm packet SHA-256 was
+`80af43be795fc7638b7ecd49c26b6f7525ab7e97239f9d9b71b804caf0cf06c5`.
+Codex completed its independent analysis before external results. Gemini
+dynamically requested, observed, and completed `gemini-3.7-flash`. The separate
+Claude subscription wrapper requested the dynamic `opus` capability alias but
+timed out; observed and completed models are null and that attempt remains
+explicitly incomplete without retry, downgrade, paid credential, or provider
+fallback. The selected contract is frozen in `docs/TASK-10-DECISION.md`.
+
+## Preserved RED-to-GREEN evidence
+
+- Manifest／revision RED: the old mutable run manifest rejected immutable
+  bundle fields and `text-revision-v1` rejected explicit `takes: []`. GREEN
+  closes phase artifacts, actions, chains, sources, and completed stages while
+  retaining non-empty revisions inside any listed take.
+- Story projection RED: `story_fcpxml.py` and its renderer did not exist. GREEN
+  covers authority rebinding, story-order permutations, exact frame timing,
+  paired and single sources, one dialogue master, title text, reserve exclusion,
+  deterministic XML, source starts, XML escaping, late mutation, symlinks, and
+  publication races.
+- Bundle RED: `run_workflow.py` did not exist. GREEN covers canonical manifests,
+  fixed filenames, exact hashes, sanitized summaries, complete-bundle loading,
+  manifest-last hard links, directory races, incomplete bundles, and cleanup of
+  invocation-owned state only.
+- Transition RED: prepare／align／finish／status interfaces were absent. GREEN
+  covers installed engine order, unsupported-doctor fail-fast, source and model
+  custody, explicit no-change revision, workbook application, exact chain
+  matching, story emission, and read-only status.
+- CLI RED: `run` was a planned placeholder and component 11 was planned. GREEN
+  exposes four nested help surfaces, sanitized exit mappings, and exactly eleven
+  components with `multicam-sync` implemented.
+- Skill RED: no separate end-user skill existed. GREEN passes the canonical
+  skill validator and a role-firewall test that rejects maintenance, private,
+  credential, transport, and source-module content.
+
+## Local verification state
+
+The coherent implementation and governance package passed:
+
+- 193 complete-suite tests;
+- 9 maintainer-boundary tests;
+- Ruff over `src`, `tests`, and `examples`;
+- Python compilation over `src`, `tests`, and `examples`;
+- project identity with `ok: true`, kind `public-engine`, and lane `OSS`;
+- the current canonical validator for both the maintainer and end-user skills;
+- `git diff --check`; and
+- a non-editable wheel build and install with `run --help`, the eleven-item
+  component registry, and read-only `run status` against a complete invented
+  aligned bundle.
+
+The wheel SHA-256 was
+`078c8761a663baca1b567ef9978bf07cfbf092537d504574811e4418ffc5a534`.
+All run-workflow fixtures use invented content.
+
+Closeout-review provenance is recorded in the Task 10 closeout packet and
+provider status／adjudication files under `docs/reviews/`.
+
+No tag, release, pull request, tester contact, package publication, application
+submission, Final Cut GUI evidence, or DTD evidence is claimed by Task 10.
diff --git a/docs/TOOLING.md b/docs/TOOLING.md
index 50476c0..dfcb95f 100644
--- a/docs/TOOLING.md
+++ b/docs/TOOLING.md
@@ -10,7 +10,8 @@ or another project's tool state.
 - Full tests: `python -m unittest discover -s tests -v`
 - Lint: `ruff check src tests`
 - Skill validation uses the current Codex `skill-creator` validator against
-  `.agents/skills/tritrack-editing-assistant-maintainer`.
+  both `.agents/skills/tritrack-editing-assistant-maintainer` and
+  `skills/tritrack-editing-assistant`.
 
 ## Local synchronization
 
@@ -142,6 +143,44 @@ or another project's tool state.
   inspection. Inputs are rehashed before temporary-file plus hard-link
   publication; existing outputs and race winners are never overwritten.
 
+## Immutable local run workflow
+
+- `tritrack run prepare --help`, `tritrack run align --help`,
+  `tritrack run finish --help`, and `tritrack run status --help` are the
+  installed command authorities for Task 10 flags.
+- `prepare`, `align`, and `finish` each publish a new absent directory. A
+  bundle is complete only when its canonical `run-manifest.json` is present,
+  lists the exact phase-specific filenames and hashes, and chains the exact
+  prior manifest hashes. Publication reserves the directory, hard-links
+  artifacts, and links the manifest last. No command overwrites or repairs an
+  earlier bundle.
+- Prepared bundles contain doctor, sync-map, transcript-bundle, and string-out
+  artifacts. Aligned bundles contain aligned-transcript and paper-workbook
+  artifacts. Finished bundles contain grouping, working-cut, and story-cut
+  artifacts. Manifests contain no timestamp, mutable stage status, absolute
+  path, transcript text, editor text, command arguments, logs, or credentials.
+- `prepare` calls the existing doctor → sync → transcribe → emit Python
+  functions directly. A doctor receipt with `supported: false` stops before
+  processing. Declared media basenames are globally unique, transcription
+  inputs are a strict subset, and media plus model hashes are rechecked before
+  publication.
+- `align` requires a complete prepared bundle and one explicit
+  `text-revision-v1`. `takes: []` is a valid no-change revision only when the
+  editor deliberately supplies it. The emitted workbook remains transport,
+  not text, timing, or selection authority.
+- `finish` validates the prepared → aligned manifest chain, current media
+  hashes, and workbook binding before applying paper intent, compiling the
+  working cut, and rendering `story-cut.fcpxml`. Story order, cue text, timing,
+  source hashes, sync offsets, and audio-master coverage are re-derived from
+  exact strict artifacts; reserve does not enter the active timeline.
+- `status` is read-only and reports only run ID, phase, next action, completed
+  stage names, and logical artifact hashes. Task 10 makes no network access and
+  does not claim a Final Cut GUI import, DTD result, or round trip.
+- `skills/tritrack-editing-assistant/SKILL.md` is the separate end-user entry
+  point. It uses installed help first and preserves explicit text-revision and
+  paper-edit human gates; the repository-local maintainer skill retains all
+  development and publication authority.
+
 ## Invented quickstart verification
 
 From an editable development installation, run the public Task 6.5 example
diff --git a/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md b/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
new file mode 100644
index 0000000..99ae2ec
--- /dev/null
+++ b/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
@@ -0,0 +1,535 @@
+# Task 10 Immutable Run Workflow Implementation Plan
+
+> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
+
+**Goal:** Ship three immutable local run transitions, read-only status, deterministic story-cut FCPXML, and a separate end-user editing skill without weakening Tasks 5–9 authority boundaries.
+
+**Architecture:** `run_workflow.py` owns exact run manifests, complete-bundle validation, staged absent-directory publication, and prepare／align／finish transitions that call existing product functions directly. `story_fcpxml.py` owns the final projection from exact sync, aligned, grouping, and working-cut authorities into frame-exact FCPXML. The CLI exposes nested run verbs; the end-user skill guides only installed usage and human gates.
+
+**Tech Stack:** Python 3.12+, `jsonschema` Draft 2020-12, `unittest`, existing bounded FFmpeg／whisper.cpp engines, `openpyxl`, FCPXML 1.14, Ruff, Codex skill validator.
+
+---
+
+## Frozen implementation details
+
+- Mutating verbs are exactly `prepare`, `align`, and `finish`; `status` is
+  read-only.
+- Bundle filenames and phase artifact sets are exact as recorded in
+  `docs/TASK-10-DECISION.md`.
+- Canonical JSON uses UTF-8, `ensure_ascii=False`, `indent=2`,
+  `sort_keys=True`, and one final newline.
+- `runId` uses `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`. Media IDs are globally
+  unique basenames. Source hashes are lowercase SHA-256.
+- JSON artifacts are limited to 16 MiB; manifests and bundle artifacts must be
+  nonempty regular non-symlink files. Fixed filenames never come from caller
+  input.
+- There are no timestamps or mutable run states. A published manifest means
+  every listed stage completed.
+- `text-revision-v1.takes` permits an empty list as explicit no-change
+  approval. Per-take `revisions` remains nonempty when a take entry exists.
+- A story segment uses authoritative aligned cue text and timing, working-cut
+  order, exact grouping binding, current source hashes, sync offsets, and the
+  declared audio master. Reserve entries are excluded.
+
+### Task 1: Freeze the Task 10 contracts
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json`
+- Modify: `src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json`
+- Modify: `tests/test_contracts.py`
+- Modify: `tests/test_align_text.py`
+
+- [ ] **Step 1: Write failing contract tests**
+
+Replace the minimum run-manifest fixture with one prepared immutable manifest
+containing closed phase／next-action values, an empty chain, one source, exact
+artifacts, and completed stages. Add rejection cases for timestamps, mutable
+status, unsafe filenames, phase/action mismatch, unsafe run IDs, bad source
+hashes, duplicate source identity, and unknown stage names. Add an explicit
+empty-`takes` no-change revision fixture and assert alignment preserves every
+cue as `original` while binding the revision bytes.
+
+- [ ] **Step 2: Run RED**
+
+Run:
+
+```bash
+venv/bin/python -m unittest tests.test_contracts tests.test_align_text -v
+```
+
+Expected: FAIL because the old manifest shape is accepted／required and an
+empty revision take list violates the current schema.
+
+- [ ] **Step 3: Tighten the unused manifest and widen explicit approval**
+
+Implement the exact manifest fields from the decision with
+`additionalProperties: false`, closed enums, safe filenames, path-free source
+entries, artifact hashes, stage input／output hash maps, and phase conditionals.
+Change only the top-level revision `takes.minItems` from `1` to `0`.
+
+- [ ] **Step 4: Run GREEN and full contract regression**
+
+Run the focused command above, then:
+
+```bash
+venv/bin/python -m unittest tests.test_gemini_hybrid tests.test_organizer tests.test_paper_edit -v
+```
+
+Expected: all pass; offline hybrid still requires receipts only for revised
+takes and Task 9 authority is unchanged.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json \
+  src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json \
+  tests/test_contracts.py tests/test_align_text.py docs/TASK-10-DECISION.md \
+  docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
+git commit -m "feat: freeze Task 10 run contracts"
+```
+
+### Task 2: Build the pure story-cut projection
+
+**Files:**
+- Create: `src/tritrack_editing_assistant/story_fcpxml.py`
+- Create: `tests/test_story_fcpxml.py`
+- Modify: `src/tritrack_editing_assistant/emit_fcpxml.py`
+
+- [ ] **Step 1: Write the failing story happy-path test**
+
+Build invented strict sync／aligned／grouping／working-cut objects plus probed
+source records. Assert `build_story_timeline()` leaves inputs unchanged,
+reorders active segments by `storyOrder`, derives title text from the aligned
+cue range, quantizes start/end once to profile frames, layers paired A/B clips
+using the sync offset, enables audio only on the declared master, excludes
+reserve, and exposes stable sources／duration.
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_story_fcpxml.StoryTimelineTest -v
+```
+
+Expected: import failure because `story_fcpxml.py` does not exist.
+
+- [ ] **Step 3: Implement the pure timeline types and validation**
+
+Create frozen `StorySource`, `StoryClip`, `StorySegment`, and `StoryTimeline`
+dataclasses. Add `build_story_timeline(sync_map, aligned, grouping,
+working_cut, sources, *, aligned_sha256, grouping_sha256, profile)` that:
+
+- validates all strict contracts and exact bindings;
+- reuses Task 9 grouping semantics;
+- requires question and story-order permutations;
+- re-derives every selected cue span／text／timing／source hash;
+- resolves unique source basenames against sync-map pairs／singles;
+- converts milliseconds and sync offsets with
+  `string_out.seconds_to_frames`; and
+- requires complete declared audio-master coverage for paired selections.
+
+Add a small public `probe_sources()` wrapper in `emit_fcpxml.py` around the
+existing profile-bound probe implementation so the new module does not depend
+on its private name.
+
+- [ ] **Step 4: Run GREEN**
+
+Run the focused story test and existing string-out／emit tests. Expected: PASS.
+
+- [ ] **Step 5: Add semantic RED cases**
+
+Cover changed aligned／grouping hashes, copied timing or source drift, unknown
+take or cue, duplicate／gapped story order, mismatched grouping semantics,
+foreign source hashes, missing sync source, insufficient audio-master
+coverage, sub-frame／zero-length selection, and reserve leakage.
+
+- [ ] **Step 6: Implement only missing guards and rerun GREEN**
+
+Use stable `TRITRACK_STORY_*` codes and leave all source objects unchanged.
+
+- [ ] **Step 7: Commit the pure projection**
+
+```bash
+git add src/tritrack_editing_assistant/story_fcpxml.py \
+  src/tritrack_editing_assistant/emit_fcpxml.py tests/test_story_fcpxml.py
+git commit -m "feat: build deterministic story timelines"
+```
+
+### Task 3: Render and publish story FCPXML
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/story_fcpxml.py`
+- Modify: `tests/test_story_fcpxml.py`
+
+- [ ] **Step 1: Write RED renderer and file-boundary tests**
+
+Assert deterministic XML bytes, stable resource／style IDs, XML escaping,
+profile and Basic Title retention, exact story duration, source clip starts,
+one dialogue source per gap, title text from aligned authority, and successful
+reuse of `emit_fcpxml.validate_fcpxml`. Add bounded regular JSON inputs,
+canonical grouping／working-cut bytes, source rehash, late mutation, missing
+parent, existing output before reads, publication race, cleanup, and unchanged
+input cases.
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_story_fcpxml.StoryRenderingTest \
+  tests.test_story_fcpxml.StoryFileBoundaryTest -v
+```
+
+Expected: failures because rendering and publication interfaces are absent.
+
+- [ ] **Step 3: Implement renderer and end-to-end writer**
+
+Add:
+
+```python
+def render_story_fcpxml(timeline: StoryTimeline, *, profile_id: str,
+                        binding_id: str,
+                        metadata: emit_fcpxml.ProjectMetadata) -> str: ...
+
+def emit_story_and_publish(camera_a_sources, camera_b_sources, *,
+                           sync_map_path: Path, aligned_path: Path,
+                           grouping_path: Path, working_cut_path: Path,
+                           profile_id: str, binding_id: str,
+                           metadata: emit_fcpxml.ProjectMetadata,
+                           output_path: Path) -> str: ...
+```
+
+Load 16 MiB JSON artifacts with `O_NOFOLLOW`, retain exact bytes／hashes,
+require canonical grouping and working-cut encodings, probe and hash current
+media, build and render in memory, rehash every input, then delegate final
+validated absent-file publication to `emit_fcpxml.publish_fcpxml`.
+
+- [ ] **Step 4: Run story GREEN and Task 6／9 regression**
+
+```bash
+venv/bin/python -m unittest tests.test_story_fcpxml tests.test_emit_fcpxml \
+  tests.test_organizer tests.test_paper_edit -v
+```
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/story_fcpxml.py \
+  tests/test_story_fcpxml.py
+git commit -m "feat: emit story-ordered Final Cut XML"
+```
+
+### Task 4: Implement manifest and immutable bundle infrastructure
+
+**Files:**
+- Create: `src/tritrack_editing_assistant/run_workflow.py`
+- Create: `tests/test_run_workflow.py`
+
+- [ ] **Step 1: Write RED pure manifest tests**
+
+Assert canonical deterministic bytes, strict phase-specific artifact sets,
+exact manifest chains, sorted unique sources, completed stage sets, artifact
+filenames, and sanitized summaries. Assert invalid／noncanonical payloads,
+unsafe IDs, duplicate sources, phase drift, wrong action, foreign artifact
+sets, unknown stages, and path-shaped material fail closed.
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_run_workflow.RunManifestTest -v
+```
+
+Expected: import failure because `run_workflow.py` does not exist.
+
+- [ ] **Step 3: Implement manifest builders and loaders**
+
+Add focused interfaces:
+
+```python
+def build_manifest(*, run_id: str, profile_id: str, binding_id: str,
+                   phase: str, manifest_chain: list[str],
+                   sources: list[dict[str, object]],
+                   stages: list[dict[str, object]],
+                   artifacts: dict[str, dict[str, str]]) -> dict[str, object]: ...
+def encode_manifest(payload: object) -> bytes: ...
+def load_bundle(path: Path, *, expected_phase: str | None = None) -> LoadedRunBundle: ...
+def summarize_bundle(bundle: LoadedRunBundle) -> dict[str, object]: ...
+```
+
+`load_bundle` requires an exact regular manifest, canonical bytes, fixed
+artifact names, bounded regular non-symlink artifacts, exact hashes, semantic
+phase invariants, and no unlisted entries other than the fixed files.
+
+- [ ] **Step 4: Run manifest GREEN**
+
+Expected: all pure tests pass.
+
+- [ ] **Step 5: Write RED publication tests**
+
+Cover absent parent／destination, dangling symlink, preexisting directory,
+directory-reservation race, manifest-last linking, ordinary failure cleanup,
+link failure cleanup, no caller-input deletion, deterministic repeat bundles,
+and incomplete manifest-less bundle rejection.
+
+- [ ] **Step 6: Implement staged bundle publication and rerun GREEN**
+
+Use a hidden sibling temporary directory, reserve the destination with
+`mkdir`, link fixed files with `run-manifest.json` last, fsync, and remove only
+invocation-owned temporary／partial files on ordinary failures.
+
+- [ ] **Step 7: Commit infrastructure**
+
+```bash
+git add src/tritrack_editing_assistant/run_workflow.py \
+  tests/test_run_workflow.py
+git commit -m "feat: add immutable run bundle core"
+```
+
+### Task 5: Implement prepare and align transitions
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/run_workflow.py`
+- Modify: `tests/test_run_workflow.py`
+
+- [ ] **Step 1: Write RED prepare tests**
+
+Through injected／patched existing engine boundaries, assert the exact call
+order doctor → sync → transcribe → emit, fail-fast unsupported doctor,
+globally unique basenames, transcribe-media subset, current source hashes,
+fixed output names, stage hashes, sanitized manifest, input rechecks, ordinary
+failure cleanup, and no nested CLI／shell call.
+
+- [ ] **Step 2: Observe RED and implement `prepare_run()`**
+
+```python
+def prepare_run(camera_a_sources, camera_b_sources, transcribe_media, *,
+                model_path: Path, language: str, profile_id: str,
+                binding_id: str, metadata: emit_fcpxml.ProjectMetadata,
+                run_id: str, output_dir: Path) -> dict[str, object]: ...
+```
+
+Build all component artifacts in the staged directory, rehash source media and
+model before publication, then publish the manifest last. Rerun and expect
+GREEN.
+
+- [ ] **Step 3: Write RED align tests**
+
+Assert complete prepared-bundle validation before revision reads, exact
+prepared and revision hash binding, no-change revision acceptance, calls to
+alignment then paper export, fixed artifacts, manifest chain, unchanged
+inputs, and cleanup／no-overwrite behavior.
+
+- [ ] **Step 4: Implement `align_run()` and rerun GREEN**
+
+```python
+def align_run(prepared_dir: Path, revision_path: Path, *,
+              output_dir: Path) -> dict[str, object]: ...
+```
+
+- [ ] **Step 5: Commit transitions**
+
+```bash
+git add src/tritrack_editing_assistant/run_workflow.py \
+  tests/test_run_workflow.py
+git commit -m "feat: prepare and align immutable runs"
+```
+
+### Task 6: Implement finish and status transitions
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/run_workflow.py`
+- Modify: `tests/test_run_workflow.py`
+
+- [ ] **Step 1: Write RED finish tests**
+
+Assert prepared／aligned phase and chain validation, exact run/profile/binding/
+source equality, current caller media hashes, workbook apply → organizer →
+story emit order, fixed outputs, finished chain, input rechecks, sanitized
+manifest, no-overwrite, and failure cleanup.
+
+- [ ] **Step 2: Implement `finish_run()` and rerun GREEN**
+
+```python
+def finish_run(prepared_dir: Path, aligned_dir: Path, workbook_path: Path,
+               camera_a_sources, camera_b_sources, *,
+               metadata: emit_fcpxml.ProjectMetadata,
+               output_dir: Path) -> dict[str, object]: ...
+```
+
+- [ ] **Step 3: Write RED read-only status tests**
+
+Assert status validates exact artifacts, writes nothing, returns only schema,
+run ID, phase, next action, stage names, logical artifact names, and hashes,
+and rejects incomplete／changed／symlinked bundles.
+
+- [ ] **Step 4: Implement `status_run()` and run complete workflow GREEN**
+
+```python
+def status_run(run_dir: Path) -> dict[str, object]: ...
+```
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/run_workflow.py \
+  tests/test_run_workflow.py
+git commit -m "feat: finish and inspect immutable runs"
+```
+
+### Task 7: Expose the installed CLI
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/cli.py`
+- Modify: `tests/test_cli.py`
+- Modify: `tests/test_quickstart_demo.py`
+
+- [ ] **Step 1: Write RED parser／help tests**
+
+Assert exact nested verbs and flags from the decision; exclude provider,
+upload, credential, overwrite, mutable-resume, private, and release language.
+Change component 11 only from planned to implemented; keep exactly eleven.
+
+- [ ] **Step 2: Run RED and wire parsers／handlers**
+
+Map source arguments into `MediaSource`, construct metadata, invoke only
+`run_workflow` functions, print sanitized JSON summaries, and classify stable
+run／story／existing component codes into the established exit classes.
+
+- [ ] **Step 3: Add RED installed smoke and failure mapping**
+
+Cover status success, existing output before engine work, incomplete bundle,
+invalid manifest／chain, source mismatch, missing parent, unsupported doctor,
+and no traceback／stderr leakage. Use invented fixtures and patch only external
+media engines where unavoidable.
+
+- [ ] **Step 4: Run CLI and registry GREEN**
+
+```bash
+venv/bin/python -m unittest tests.test_cli tests.test_quickstart_demo -v
+venv/bin/tritrack run --help
+venv/bin/tritrack components --json
+```
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/cli.py tests/test_cli.py \
+  tests/test_quickstart_demo.py
+git commit -m "feat: expose immutable run commands"
+```
+
+### Task 8: Create and firewall the end-user skill
+
+**Files:**
+- Create: `skills/tritrack-editing-assistant/SKILL.md`
+- Create: `skills/tritrack-editing-assistant/agents/openai.yaml`
+- Modify: `tests/test_maintainer_boundary.py`
+
+- [ ] **Step 1: Write RED firewall tests**
+
+Require the separate end-user skill and agent metadata; exact name／trigger;
+help-first installed command usage; prepare／revision／align／paper／finish human
+gates; no-overwrite／local-only rules; and explicit workbook non-authority.
+Reject maintainer skill name, task numbers, branch／release／standing-grant／
+tester language, private project names, absolute home paths, credentials,
+provider transport, and direct source-module orchestration.
+
+- [ ] **Step 2: Observe RED**
+
+```bash
+venv/bin/python -m unittest tests.test_maintainer_boundary -v
+```
+
+Expected: FAIL because the end-user skill is absent.
+
+- [ ] **Step 3: Initialize and author the skill**
+
+Run the canonical `skill-creator/scripts/init_skill.py` for
+`tritrack-editing-assistant` at repository `skills/`, with exact interface
+metadata and no unused resource folders. Replace the generated body with a
+concise imperative workflow that delegates all product behavior to installed
+command help and preserves both human gates.
+
+- [ ] **Step 4: Validate and run firewall GREEN**
+
+Run both:
+
+```bash
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
+venv/bin/python -m unittest tests.test_maintainer_boundary -v
+```
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add skills/tritrack-editing-assistant tests/test_maintainer_boundary.py
+git commit -m "feat: add the end-user editing skill"
+```
+
+### Task 9: Documentation, verification, and closeout
+
+**Files:**
+- Modify: `README.md`
+- Modify: `docs/TOOLING.md`
+- Modify: `docs/ROADMAP.md`
+- Modify: `STATUS.md`
+- Modify: `CHANGELOG.md`
+- Create: `docs/TASK-10-VERIFICATION.md`
+- Create: `docs/reviews/task-10-closeout-packet-2026-08-17.md`
+- Create: closeout raw status／adjudication files under `docs/reviews/`
+
+- [ ] **Step 1: Write RED documentation／boundary assertions**
+
+Update maintainer tests to require Task 10 command authorities, immutable
+bundle language, final story projection, separate skill identity, Task 11 as
+next action, and honest deferrals. Keep public governance free of private paths
+and unimplemented claims.
+
+- [ ] **Step 2: Update public docs after the coherent implementation is green**
+
+Document exact installed examples, fixed bundle contents, both human gates,
+manifest non-authority, source custody, story FCPXML scope, crash-incomplete
+behavior, and unchanged outward-action boundary. Update component 11 to
+implemented and retain `validate`／live provider transport as planned.
+
+- [ ] **Step 3: Run final local gates after the last edit**
+
+```bash
+venv/bin/python -m unittest tests.test_run_workflow tests.test_story_fcpxml \
+  tests.test_cli tests.test_maintainer_boundary -v
+venv/bin/python -m unittest discover -s tests -v
+venv/bin/ruff check src tests examples
+venv/bin/python -m compileall -q src tests examples
+python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
+git diff --check
+```
+
+Build an sdist／wheel in an absent ignored directory, install it into an absent
+temporary Python 3.13 environment, and run installed components, run help,
+strict invented manifest/status, no-change align, finish, and deterministic
+story-output acceptance. Validate story FCPXML against the installed DTD when
+available without claiming GUI import.
+
+- [ ] **Step 4: Freeze and send one public-safe closeout packet**
+
+Include candidate commit/tree identity, decision, diff, RED／GREEN evidence,
+tests, role firewall, privacy／authority matrix, and explicit non-claims. Send
+the same bytes through the approved Gemini and Claude wrappers. Preserve exact
+requested／observed／completed models and incomplete attempts. Locally
+adjudicate every finding, fix ordinary in-scope issues with new RED tests, and
+rerun all gates. Stop after two NEEDS_REVISION rounds for producer adjudication.
+
+- [ ] **Step 5: Record verification and custody**
+
+Only after the last edit and full green, write `docs/TASK-10-VERIFICATION.md`
+and update `STATUS.md` to make Task 11 next. Commit only Task 10 files,
+fast-forward local `main`, push existing public `origin/main`, and require:
+
+```bash
+git rev-parse HEAD
+git rev-parse main
+git rev-parse origin/main
+git ls-remote origin refs/heads/main
+```
+
+All four SHA values must match the final green candidate. No tag, release, PR,
+tester contact, package publication, or application submission is performed.
diff --git a/skills/tritrack-editing-assistant/SKILL.md b/skills/tritrack-editing-assistant/SKILL.md
new file mode 100644
index 0000000..f05fa4a
--- /dev/null
+++ b/skills/tritrack-editing-assistant/SKILL.md
@@ -0,0 +1,110 @@
+---
+name: tritrack-editing-assistant
+description: Guide an editor or terminal-capable agent through TriTrack's installed, local Final Cut workflow. Use when preparing synchronized A/B interview media, reviewing cue-addressed transcript corrections, organizing an edit in the paper workbook, finishing a story-ordered FCPXML, or checking an immutable run bundle.
+---
+
+# TriTrack Editing Assistant
+
+Guide the edit through explicit immutable stages. Keep media and editorial
+artifacts local, preserve editor intent, and use only the installed `tritrack`
+command surface.
+
+## Start help-first
+
+1. Run `tritrack run --help`.
+2. Run the selected subcommand's `--help` before naming or using its flags:
+   - `tritrack run prepare --help`
+   - `tritrack run align --help`
+   - `tritrack run finish --help`
+   - `tritrack run status --help`
+3. Treat installed help as the command authority. Stop if a required command or
+   flag is unavailable; do not guess a replacement.
+
+## Preserve local custody
+
+- Keep source media, the local speech model, JSON artifacts, workbook, and
+  FCPXML on paths the editor explicitly places in scope.
+- Require globally unique media basenames across camera A and camera B.
+- Choose only declared camera sources for transcription.
+- Use a new absent output directory for every mutating stage. Never overwrite,
+  repair, resume, or add files inside an earlier bundle.
+- Read sanitized command summaries by default. Inspect transcript or workbook
+  content only when the editor explicitly puts that artifact in scope.
+
+## Prepare the synchronized run
+
+Help the editor choose camera roles, transcription sources, spoken language,
+public profile and title binding, event and project names, a safe run ID, and an
+absent prepared output directory. Then run the installed command in the shape
+reported by:
+
+```text
+tritrack run prepare --help
+```
+
+Confirm that the summary reports `phase: prepared` and
+`nextAction: provide-revision`. Do not claim that the string-out is a final
+story edit.
+
+## Hold the text-revision human gate
+
+Pause for the editor to review `transcript-bundle.json`. Preserve every cue ID,
+source hash, language, and timing. Help encode only corrections the editor
+explicitly approves in one strict `tritrack.text-revision/v1` JSON artifact
+bound to the exact transcript-bundle bytes.
+
+Never infer approval. Use `takes: []` only after the editor explicitly confirms
+that no text changes are wanted. Do not retime, split, merge, translate, or
+invent cues.
+
+Run the installed alignment command in the shape reported by:
+
+```text
+tritrack run align --help
+```
+
+Confirm `phase: aligned` and `nextAction: edit-paper-workbook`.
+
+## Hold the paper-edit human gate
+
+Pause for the editor to edit `paper-edit.xlsx`. Allow edits only in the
+`Questions` and `Selections` tables. Keep cue addresses intact and require the
+editor to decide active answers, story order, and reserve ranges.
+
+Treat the workbook as transport, not authority. The strict aligned transcript
+remains text and timing authority; grouping JSON records editor intent; the
+working-cut JSON is the compiled selection authority.
+
+## Finish the story projection
+
+Reuse the exact prepared and aligned bundles, the editor-approved workbook, and
+the same local camera sources. Choose a new absent finished output directory.
+Run the installed command in the shape reported by:
+
+```text
+tritrack run finish --help
+```
+
+Confirm `phase: finished` and `nextAction: complete`. Describe
+`story-cut.fcpxml` as a deterministic story-ordered projection. Do not claim a
+GUI import, application round trip, or external DTD validation unless the
+editor separately performs and records it.
+
+## Inspect without mutation
+
+Use the installed read-only command in the shape reported by:
+
+```text
+tritrack run status --help
+```
+
+Report only the run ID, phase, next action, stage names, logical artifact names,
+and hashes. Do not expose local paths, transcript text, question text, notes, or
+FCPXML content in a status summary.
+
+## Stop on strict failures
+
+Stop when compatibility, source custody, exact hashes, manifest chain, schema,
+workbook integrity, media coverage, or absent-output checks fail. Preserve the
+error code and existing files. Do not weaken validation, reconstruct a missing
+manifest, or continue from an incomplete bundle.
diff --git a/skills/tritrack-editing-assistant/agents/openai.yaml b/skills/tritrack-editing-assistant/agents/openai.yaml
new file mode 100644
index 0000000..169cb80
--- /dev/null
+++ b/skills/tritrack-editing-assistant/agents/openai.yaml
@@ -0,0 +1,4 @@
+interface:
+  display_name: "TriTrack Editing Assistant"
+  short_description: "Guide immutable local Final Cut editing runs"
+  default_prompt: "Use $tritrack-editing-assistant to guide this local edit through immutable TriTrack run stages."
diff --git a/src/tritrack_editing_assistant/cli.py b/src/tritrack_editing_assistant/cli.py
index 6c9151f..5a23e79 100644
--- a/src/tritrack_editing_assistant/cli.py
+++ b/src/tritrack_editing_assistant/cli.py
@@ -15,6 +15,7 @@ from . import emit_fcpxml as emit_module
 from . import gemini_hybrid as hybrid_module
 from . import organizer as organizer_module
 from . import paper_edit as paper_module
+from . import run_workflow as run_module
 from . import sync_scan as sync_module
 from . import transcribe_takes as transcribe_module
 
@@ -79,7 +80,11 @@ COMPONENTS = (
         "command": "hybrid",
         "status": "planned",
     },
-    {"sourceComponent": "multicam-sync", "command": "run", "status": "planned"},
+    {
+        "sourceComponent": "multicam-sync",
+        "command": "run",
+        "status": "implemented",
+    },
 )
 
 
@@ -455,6 +460,140 @@ def _run_paper_apply(arguments: argparse.Namespace) -> int:
     return EXIT_OK
 
 
+def _run_error_exit(code: str) -> int:
+    if code == "TRITRACK_OUTPUT_EXISTS":
+        return EXIT_OUTPUT_EXISTS
+    if code in {
+        "TRITRACK_OUTPUT_PARENT_MISSING",
+        "TRITRACK_RUN_INPUT_UNREADABLE",
+        "TRITRACK_STORY_SOURCE_UNREADABLE",
+        "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
+        "TRITRACK_PAPER_INPUT_UNREADABLE",
+    }:
+        return EXIT_IO
+    if code in {
+        "TRITRACK_SYNC_PROBE_FAILED",
+        "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
+        "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
+        "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
+        "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
+    }:
+        return EXIT_DEPENDENCY
+    if code in {
+        "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED",
+        "TRITRACK_PROFILE_UNKNOWN",
+    }:
+        return EXIT_POLICY
+    if code in {
+        "TRITRACK_RUN_SOURCE_REQUIRED",
+        "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID",
+        "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
+        "TRITRACK_EMIT_METADATA_INVALID",
+    }:
+        return EXIT_USAGE
+    return EXIT_DATA
+
+
+def _print_run_summary(summary: dict[str, object], *, as_json: bool) -> None:
+    if as_json:
+        print(json.dumps(summary, ensure_ascii=False, indent=2))
+        return
+    print(f"RUN\t{summary['runId']}")
+    print(f"PHASE\t{summary['phase']}")
+    print(f"NEXT\t{summary['nextAction']}")
+    print(f"STAGES\t{','.join(summary['stages'])}")
+    artifacts = summary["artifacts"]
+    assert isinstance(artifacts, dict)
+    for logical_name, sha256 in artifacts.items():
+        print(f"ARTIFACT\t{logical_name}\t{sha256}")
+
+
+def _run_prepare(arguments: argparse.Namespace) -> int:
+    camera_a = [
+        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
+    ]
+    camera_b = [
+        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
+    ]
+    try:
+        summary = run_module.prepare_run(
+            camera_a,
+            camera_b,
+            arguments.transcribe_media,
+            model_path=arguments.model,
+            language=arguments.language,
+            profile_id=arguments.profile,
+            binding_id=arguments.binding,
+            metadata=emit_module.ProjectMetadata(
+                arguments.event_name, arguments.project_name
+            ),
+            run_id=arguments.run_id,
+            output_dir=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _run_error_exit(code)
+    if arguments.json:
+        _print_run_summary(summary, as_json=True)
+    return EXIT_OK
+
+
+def _run_align_bundle(arguments: argparse.Namespace) -> int:
+    try:
+        summary = run_module.align_run(
+            arguments.prepared,
+            arguments.revision,
+            output_dir=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _run_error_exit(code)
+    if arguments.json:
+        _print_run_summary(summary, as_json=True)
+    return EXIT_OK
+
+
+def _run_finish(arguments: argparse.Namespace) -> int:
+    camera_a = [
+        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
+    ]
+    camera_b = [
+        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
+    ]
+    try:
+        summary = run_module.finish_run(
+            arguments.prepared,
+            arguments.aligned,
+            arguments.workbook,
+            camera_a,
+            camera_b,
+            metadata=emit_module.ProjectMetadata(
+                arguments.event_name, arguments.project_name
+            ),
+            output_dir=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _run_error_exit(code)
+    if arguments.json:
+        _print_run_summary(summary, as_json=True)
+    return EXIT_OK
+
+
+def _run_status(arguments: argparse.Namespace) -> int:
+    try:
+        summary = run_module.status_run(arguments.run_dir)
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _run_error_exit(code)
+    _print_run_summary(summary, as_json=arguments.json)
+    return EXIT_OK
+
+
 def build_parser() -> argparse.ArgumentParser:
     parser = argparse.ArgumentParser(
         prog="tritrack",
@@ -753,9 +892,71 @@ def build_parser() -> argparse.ArgumentParser:
     )
     paper_apply.set_defaults(handler=_run_paper_apply)
 
+    run = subparsers.add_parser(
+        "run",
+        help="publish immutable local workflow stage bundles",
+    )
+    run_subparsers = run.add_subparsers(dest="run_command", required=True)
+
+    run_prepare = run_subparsers.add_parser(
+        "prepare", help="doctor, synchronize, transcribe, and emit a string-out"
+    )
+    run_prepare.add_argument(
+        "--camera-a", action="append", required=True, type=Path
+    )
+    run_prepare.add_argument(
+        "--camera-b", action="append", required=True, type=Path
+    )
+    run_prepare.add_argument(
+        "--transcribe-media", action="append", required=True, type=Path
+    )
+    run_prepare.add_argument("--model", required=True, type=Path)
+    run_prepare.add_argument("--language", required=True)
+    run_prepare.add_argument("--profile", required=True)
+    run_prepare.add_argument("--binding", required=True)
+    run_prepare.add_argument("--event-name", required=True)
+    run_prepare.add_argument("--project-name", required=True)
+    run_prepare.add_argument("--run-id", required=True)
+    run_prepare.add_argument("--output", required=True, type=Path)
+    run_prepare.add_argument("--json", action="store_true")
+    run_prepare.set_defaults(handler=_run_prepare)
+
+    run_align = run_subparsers.add_parser(
+        "align", help="apply one explicit text revision and export paper edit"
+    )
+    run_align.add_argument("--prepared", required=True, type=Path)
+    run_align.add_argument("--revision", required=True, type=Path)
+    run_align.add_argument("--output", required=True, type=Path)
+    run_align.add_argument("--json", action="store_true")
+    run_align.set_defaults(handler=_run_align_bundle)
+
+    run_finish = run_subparsers.add_parser(
+        "finish", help="apply paper intent and emit the story cut"
+    )
+    run_finish.add_argument("--prepared", required=True, type=Path)
+    run_finish.add_argument("--aligned", required=True, type=Path)
+    run_finish.add_argument("--workbook", required=True, type=Path)
+    run_finish.add_argument(
+        "--camera-a", action="append", required=True, type=Path
+    )
+    run_finish.add_argument(
+        "--camera-b", action="append", required=True, type=Path
+    )
+    run_finish.add_argument("--event-name", required=True)
+    run_finish.add_argument("--project-name", required=True)
+    run_finish.add_argument("--output", required=True, type=Path)
+    run_finish.add_argument("--json", action="store_true")
+    run_finish.set_defaults(handler=_run_finish)
+
+    run_status = run_subparsers.add_parser(
+        "status", help="validate and summarize one complete run bundle"
+    )
+    run_status.add_argument("--run", dest="run_dir", required=True, type=Path)
+    run_status.add_argument("--json", action="store_true")
+    run_status.set_defaults(handler=_run_status)
+
     planned_commands = {
         "validate": "validate generated output",
-        "run": "orchestrate the complete local workflow",
     }
     for name, help_text in planned_commands.items():
         command_parser = subparsers.add_parser(name, help=help_text)
diff --git a/src/tritrack_editing_assistant/emit_fcpxml.py b/src/tritrack_editing_assistant/emit_fcpxml.py
index ce598c4..e6e6945 100644
--- a/src/tritrack_editing_assistant/emit_fcpxml.py
+++ b/src/tritrack_editing_assistant/emit_fcpxml.py
@@ -509,6 +509,17 @@ def _probe_sources(
     return media
 
 
+def probe_sources(
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    *,
+    profile: Mapping[str, object],
+) -> list[dict[str, object]]:
+    """Probe public media inputs against one exact compatibility profile."""
+
+    return _probe_sources(camera_a_sources, camera_b_sources, profile=profile)
+
+
 def emit_and_publish(
     camera_a_sources: Sequence[sync_scan.MediaSource],
     camera_b_sources: Sequence[sync_scan.MediaSource],
@@ -527,7 +538,7 @@ def emit_and_publish(
     binding = doctor.load_title_binding(binding_id)
     if sync_map["profileId"] != profile_id:
         raise ValueError("TRITRACK_PROFILE_MISMATCH")
-    media = _probe_sources(
+    media = probe_sources(
         camera_a_sources,
         camera_b_sources,
         profile=profile,
diff --git a/src/tritrack_editing_assistant/run_workflow.py b/src/tritrack_editing_assistant/run_workflow.py
new file mode 100644
index 0000000..b598597
--- /dev/null
+++ b/src/tritrack_editing_assistant/run_workflow.py
@@ -0,0 +1,967 @@
+"""Immutable run manifests and complete bundle publication."""
+
+from __future__ import annotations
+
+import copy
+import hashlib
+import json
+import os
+import shutil
+import stat
+import tempfile
+from collections.abc import Callable, Mapping, Sequence
+from dataclasses import dataclass
+from decimal import Decimal
+from pathlib import Path
+
+from jsonschema import ValidationError
+
+from . import (
+    __version__,
+    align_text,
+    contracts,
+    doctor,
+    emit_fcpxml,
+    organizer,
+    paper_edit,
+    process,
+    story_fcpxml,
+    sync_scan,
+    transcribe_takes,
+)
+
+MANIFEST_FILE_NAME = "run-manifest.json"
+_MANIFEST_LIMIT_BYTES = 16 * 1024 * 1024
+_ARTIFACT_LIMIT_BYTES = 512 * 1024 * 1024
+_HASH_CHUNK_BYTES = 1024 * 1024
+
+
+@dataclass(frozen=True)
+class PhaseSpec:
+    next_action: str
+    chain_length: int
+    artifacts: tuple[tuple[str, str], ...]
+    stages: tuple[str, ...]
+
+
+PHASE_SPECS = {
+    "prepared": PhaseSpec(
+        next_action="provide-revision",
+        chain_length=0,
+        artifacts=(
+            ("doctorReceipt", "doctor.json"),
+            ("syncMap", "sync-map.json"),
+            ("transcriptBundle", "transcript-bundle.json"),
+            ("stringOut", "string-out.fcpxml"),
+        ),
+        stages=("doctor", "sync", "transcribe", "emit"),
+    ),
+    "aligned": PhaseSpec(
+        next_action="edit-paper-workbook",
+        chain_length=1,
+        artifacts=(
+            ("alignedTranscript", "aligned-transcript.json"),
+            ("paperWorkbook", "paper-edit.xlsx"),
+        ),
+        stages=("align", "paper"),
+    ),
+    "finished": PhaseSpec(
+        next_action="complete",
+        chain_length=2,
+        artifacts=(
+            ("grouping", "grouping.json"),
+            ("workingCut", "working-cut.json"),
+            ("storyCut", "story-cut.fcpxml"),
+        ),
+        stages=("paper", "organize", "emit"),
+    ),
+}
+
+
+@dataclass(frozen=True)
+class LoadedRunArtifact:
+    logical_name: str
+    file_name: str
+    path: Path
+    encoded: bytes
+    sha256: str
+
+
+@dataclass(frozen=True)
+class LoadedRunBundle:
+    root: Path
+    manifest: dict[str, object]
+    manifest_bytes: bytes
+    manifest_sha256: str
+    artifacts: Mapping[str, LoadedRunArtifact]
+
+
+def _manifest_error(error: BaseException | None = None) -> ValueError:
+    result = ValueError("TRITRACK_RUN_MANIFEST_INVALID")
+    if error is not None:
+        result.__cause__ = error
+    return result
+
+
+def _validate_manifest(payload: object) -> dict[str, object]:
+    try:
+        contracts.validate_contract("run-manifest-v1", payload)
+    except (TypeError, ValueError, ValidationError) as error:
+        raise _manifest_error(error)
+    if not isinstance(payload, dict):
+        raise _manifest_error()
+    phase = payload["phase"]
+    if not isinstance(phase, str) or phase not in PHASE_SPECS:
+        raise _manifest_error()
+    spec = PHASE_SPECS[phase]
+    if (
+        payload["nextAction"] != spec.next_action
+        or len(payload["manifestChain"]) != spec.chain_length
+    ):
+        raise _manifest_error()
+
+    sources = payload["sources"]
+    assert isinstance(sources, list)
+    source_order = [(source["camera"], source["mediaId"]) for source in sources]
+    media_ids = [source["mediaId"] for source in sources]
+    if source_order != sorted(source_order) or len(media_ids) != len(set(media_ids)):
+        raise _manifest_error()
+
+    artifacts = payload["artifacts"]
+    assert isinstance(artifacts, dict)
+    expected_artifacts = dict(spec.artifacts)
+    if set(artifacts) != set(expected_artifacts):
+        raise _manifest_error()
+    for logical_name, file_name in spec.artifacts:
+        artifact = artifacts[logical_name]
+        if not isinstance(artifact, Mapping) or artifact["fileName"] != file_name:
+            raise _manifest_error()
+
+    stages = payload["stages"]
+    assert isinstance(stages, list)
+    if [stage["name"] for stage in stages] != list(spec.stages):
+        raise _manifest_error()
+    for stage, expected_name in zip(stages, spec.stages, strict=True):
+        assert isinstance(stage, Mapping)
+        output_hashes = stage["outputHashes"]
+        expected_logical = dict(zip(spec.stages, spec.artifacts, strict=True))[
+            expected_name
+        ][0]
+        if output_hashes != {
+            expected_logical: artifacts[expected_logical]["sha256"]
+        }:
+            raise _manifest_error()
+    return payload
+
+
+def build_manifest(
+    *,
+    run_id: str,
+    profile_id: str,
+    binding_id: str,
+    phase: str,
+    manifest_chain: Sequence[str],
+    sources: Sequence[Mapping[str, object]],
+    stages: Sequence[Mapping[str, object]],
+    artifacts: Mapping[str, Mapping[str, str]],
+) -> dict[str, object]:
+    """Build one path-free immutable run receipt from completed stage facts."""
+
+    try:
+        spec = PHASE_SPECS[phase]
+        expected_artifacts = {logical_name for logical_name, _ in spec.artifacts}
+        if set(artifacts) != expected_artifacts:
+            raise ValueError
+        source_copies = [copy.deepcopy(dict(source)) for source in sources]
+        source_copies.sort(key=lambda source: (source["camera"], source["mediaId"]))
+        stage_by_name = {
+            stage["name"]: copy.deepcopy(dict(stage)) for stage in stages
+        }
+        if (
+            len(stage_by_name) != len(stages)
+            or set(stage_by_name) != set(spec.stages)
+        ):
+            raise ValueError
+        artifact_copies = {
+            logical_name: copy.deepcopy(dict(artifacts[logical_name]))
+            for logical_name, _ in spec.artifacts
+        }
+        payload: dict[str, object] = {
+            "schemaVersion": "tritrack.run-manifest/v1",
+            "toolVersion": __version__,
+            "runId": run_id,
+            "profileId": profile_id,
+            "bindingId": binding_id,
+            "phase": phase,
+            "nextAction": spec.next_action,
+            "manifestChain": list(manifest_chain),
+            "sources": source_copies,
+            "artifacts": artifact_copies,
+            "stages": [stage_by_name[name] for name in spec.stages],
+        }
+    except (KeyError, TypeError, ValueError) as error:
+        raise _manifest_error(error)
+    return _validate_manifest(payload)
+
+
+def encode_manifest(payload: object) -> bytes:
+    """Return canonical UTF-8 bytes for one semantically strict manifest."""
+
+    validated = _validate_manifest(payload)
+    return (
+        json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+    ).encode("utf-8")
+
+
+def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError(code) from error
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
+            raise ValueError(code)
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(limit + 1)
+        if len(encoded) > limit:
+            raise ValueError(code)
+        return encoded
+    except OSError as error:
+        raise ValueError(code) from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+
+
+def _validate_json_artifact(
+    encoded: bytes, *, contract: str, code: str
+) -> object:
+    try:
+        payload = json.loads(
+            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
+        )
+        contracts.validate_contract(contract, payload)
+    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
+        raise ValueError(code) from error
+    return payload
+
+
+def _validate_artifact(
+    logical_name: str,
+    encoded: bytes,
+    *,
+    manifest: Mapping[str, object],
+) -> None:
+    contracts_by_name = {
+        "syncMap": "sync-map-v1",
+        "transcriptBundle": "transcript-bundle-v1",
+        "alignedTranscript": "aligned-transcript-v1",
+        "grouping": "grouping-v1",
+        "workingCut": "working-cut-v1",
+    }
+    contract = contracts_by_name.get(logical_name)
+    if contract is not None:
+        _validate_json_artifact(
+            encoded, contract=contract, code="TRITRACK_RUN_ARTIFACT_INVALID"
+        )
+        return
+    if logical_name == "doctorReceipt":
+        try:
+            payload = json.loads(encoded.decode("utf-8", errors="strict"))
+        except (UnicodeError, json.JSONDecodeError) as error:
+            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
+        if (
+            not isinstance(payload, dict)
+            or payload.get("schemaVersion") != "tritrack.doctor-receipt/v1"
+            or payload.get("profileId") != manifest["profileId"]
+            or payload.get("titleBindingId") != manifest["bindingId"]
+            or not isinstance(payload.get("supported"), bool)
+            or not isinstance(payload.get("checks"), list)
+            or not isinstance(payload.get("remediation"), list)
+        ):
+            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID")
+        return
+    if logical_name in {"stringOut", "storyCut"}:
+        try:
+            text = encoded.decode("utf-8", errors="strict")
+            emit_fcpxml.validate_fcpxml(
+                text,
+                profile=doctor.load_profile(str(manifest["profileId"])),
+                binding=doctor.load_title_binding(str(manifest["bindingId"])),
+            )
+        except (UnicodeError, TypeError, ValueError, ValidationError) as error:
+            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
+
+
+def _bundle_directory(path: Path) -> Path:
+    selected = Path(path)
+    try:
+        metadata = selected.lstat()
+    except OSError as error:
+        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
+    if not stat.S_ISDIR(metadata.st_mode):
+        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
+    return selected
+
+
+def load_bundle(
+    path: Path, *, expected_phase: str | None = None
+) -> LoadedRunBundle:
+    """Load and verify one complete immutable run bundle."""
+
+    root = _bundle_directory(path)
+    manifest_path = root / MANIFEST_FILE_NAME
+    if not os.path.lexists(manifest_path):
+        raise ValueError("TRITRACK_RUN_BUNDLE_INCOMPLETE")
+    manifest_bytes = _read_regular_bytes(
+        manifest_path,
+        limit=_MANIFEST_LIMIT_BYTES,
+        code="TRITRACK_RUN_MANIFEST_INVALID",
+    )
+    try:
+        payload = json.loads(manifest_bytes.decode("utf-8", errors="strict"))
+    except (UnicodeError, json.JSONDecodeError) as error:
+        raise ValueError("TRITRACK_RUN_MANIFEST_INVALID") from error
+    manifest = _validate_manifest(payload)
+    if manifest_bytes != encode_manifest(manifest):
+        raise ValueError("TRITRACK_RUN_MANIFEST_NONCANONICAL")
+    if expected_phase is not None and manifest["phase"] != expected_phase:
+        raise ValueError("TRITRACK_RUN_PHASE_MISMATCH")
+
+    artifacts_payload = manifest["artifacts"]
+    assert isinstance(artifacts_payload, Mapping)
+    expected_entries = {MANIFEST_FILE_NAME}
+    expected_entries.update(
+        str(artifact["fileName"]) for artifact in artifacts_payload.values()
+    )
+    try:
+        observed_entries = {entry.name for entry in os.scandir(root)}
+    except OSError as error:
+        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
+    if observed_entries != expected_entries:
+        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
+
+    loaded: dict[str, LoadedRunArtifact] = {}
+    for logical_name, artifact_payload in artifacts_payload.items():
+        assert isinstance(artifact_payload, Mapping)
+        file_name = str(artifact_payload["fileName"])
+        encoded = _read_regular_bytes(
+            root / file_name,
+            limit=_ARTIFACT_LIMIT_BYTES,
+            code="TRITRACK_RUN_ARTIFACT_INVALID",
+        )
+        observed_hash = hashlib.sha256(encoded).hexdigest()
+        if observed_hash != artifact_payload["sha256"]:
+            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
+        _validate_artifact(logical_name, encoded, manifest=manifest)
+        loaded[logical_name] = LoadedRunArtifact(
+            logical_name=logical_name,
+            file_name=file_name,
+            path=root / file_name,
+            encoded=encoded,
+            sha256=observed_hash,
+        )
+    return LoadedRunBundle(
+        root=root,
+        manifest=manifest,
+        manifest_bytes=manifest_bytes,
+        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
+        artifacts=loaded,
+    )
+
+
+def summarize_bundle(bundle: LoadedRunBundle) -> dict[str, object]:
+    """Return a path-free and text-free status projection."""
+
+    if not isinstance(bundle, LoadedRunBundle):
+        raise TypeError("TRITRACK_RUN_BUNDLE_INVALID")
+    return {
+        "schemaVersion": "tritrack.run-summary/v1",
+        "runId": bundle.manifest["runId"],
+        "phase": bundle.manifest["phase"],
+        "nextAction": bundle.manifest["nextAction"],
+        "stages": [stage["name"] for stage in bundle.manifest["stages"]],
+        "artifacts": {
+            logical_name: artifact.sha256
+            for logical_name, artifact in bundle.artifacts.items()
+        },
+    }
+
+
+def _write_manifest(path: Path, encoded: bytes) -> None:
+    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
+    try:
+        with os.fdopen(descriptor, "wb") as stream:
+            descriptor = -1
+            stream.write(encoded)
+            stream.flush()
+            os.fsync(stream.fileno())
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+
+
+def _verify_staging(staging: Path, manifest: Mapping[str, object]) -> None:
+    artifacts = manifest["artifacts"]
+    assert isinstance(artifacts, Mapping)
+    expected = {str(artifact["fileName"]) for artifact in artifacts.values()}
+    observed = {entry.name for entry in os.scandir(staging)}
+    if observed != expected:
+        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
+    for logical_name, artifact in artifacts.items():
+        assert isinstance(artifact, Mapping)
+        encoded = _read_regular_bytes(
+            staging / str(artifact["fileName"]),
+            limit=_ARTIFACT_LIMIT_BYTES,
+            code="TRITRACK_RUN_ARTIFACT_INVALID",
+        )
+        if hashlib.sha256(encoded).hexdigest() != artifact["sha256"]:
+            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
+        _validate_artifact(str(logical_name), encoded, manifest=manifest)
+
+
+def _fsync_directory(path: Path) -> None:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_DIRECTORY"):
+        flags |= os.O_DIRECTORY
+    descriptor = os.open(path, flags)
+    try:
+        os.fsync(descriptor)
+    finally:
+        os.close(descriptor)
+
+
+def publish_bundle(
+    output_dir: Path,
+    builder: Callable[[Path], Mapping[str, object]],
+) -> LoadedRunBundle:
+    """Build privately, then hard-link a complete absent bundle manifest last."""
+
+    destination = process.require_absent_output(output_dir)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    staging = Path(
+        tempfile.mkdtemp(
+            prefix=f".{destination.name}.staging-", dir=destination.parent
+        )
+    )
+    reserved = False
+    linked: list[Path] = []
+    try:
+        manifest = _validate_manifest(builder(staging))
+        _verify_staging(staging, manifest)
+        manifest_bytes = encode_manifest(manifest)
+        _write_manifest(staging / MANIFEST_FILE_NAME, manifest_bytes)
+        try:
+            os.mkdir(destination, 0o755)
+            reserved = True
+        except FileExistsError as error:
+            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
+
+        artifacts = manifest["artifacts"]
+        assert isinstance(artifacts, Mapping)
+        file_names = sorted(
+            str(artifact["fileName"]) for artifact in artifacts.values()
+        )
+        for file_name in (*file_names, MANIFEST_FILE_NAME):
+            target = destination / file_name
+            os.link(staging / file_name, target)
+            linked.append(target)
+        _fsync_directory(destination)
+        return load_bundle(destination, expected_phase=str(manifest["phase"]))
+    except BaseException:
+        if reserved:
+            for path in reversed(linked):
+                try:
+                    path.unlink()
+                except OSError:
+                    pass
+            try:
+                destination.rmdir()
+            except OSError:
+                pass
+        raise
+    finally:
+        shutil.rmtree(staging, ignore_errors=True)
+
+
+def _hash_regular_path(path: Path, *, code: str) -> str:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError(code) from error
+    digest = hashlib.sha256()
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
+            raise ValueError(code)
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            while chunk := stream.read(_HASH_CHUNK_BYTES):
+                digest.update(chunk)
+    except OSError as error:
+        raise ValueError(code) from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+    return digest.hexdigest()
+
+
+def _hash_value(payload: object) -> str:
+    encoded = json.dumps(
+        payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
+    ).encode("utf-8")
+    return hashlib.sha256(encoded).hexdigest()
+
+
+def _artifact_records(
+    staging: Path, phase: str
+) -> dict[str, dict[str, str]]:
+    return {
+        logical_name: {
+            "fileName": file_name,
+            "sha256": _hash_regular_path(
+                staging / file_name, code="TRITRACK_RUN_ARTIFACT_INVALID"
+            ),
+        }
+        for logical_name, file_name in PHASE_SPECS[phase].artifacts
+    }
+
+
+def _source_inventory(
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    transcribe_media: Sequence[Path],
+) -> tuple[list[dict[str, object]], dict[Path, str]]:
+    if not camera_a_sources or not camera_b_sources:
+        raise ValueError("TRITRACK_RUN_SOURCE_REQUIRED")
+    declared: list[tuple[str, sync_scan.MediaSource]] = [
+        *(("A", source) for source in camera_a_sources),
+        *(("B", source) for source in camera_b_sources),
+    ]
+    media_ids = [source.media_id for _, source in declared]
+    if (
+        len(media_ids) != len(set(media_ids))
+        or any(source.media_id != source.path.name for _, source in declared)
+    ):
+        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
+    declared_paths = [source.path for _, source in declared]
+    if len(declared_paths) != len(set(declared_paths)):
+        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
+    selected_transcribe = [Path(path) for path in transcribe_media]
+    if (
+        not selected_transcribe
+        or len(selected_transcribe) != len(set(selected_transcribe))
+        or any(path not in declared_paths for path in selected_transcribe)
+    ):
+        raise ValueError("TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID")
+    source_hashes = {
+        source.path: _hash_regular_path(
+            source.path, code="TRITRACK_RUN_INPUT_UNREADABLE"
+        )
+        for _, source in declared
+    }
+    selected_set = set(selected_transcribe)
+    inventory = [
+        {
+            "camera": camera,
+            "mediaId": source.media_id,
+            "sha256": source_hashes[source.path],
+            "transcribed": source.path in selected_set,
+        }
+        for camera, source in declared
+    ]
+    return inventory, source_hashes
+
+
+def _require_inputs_unchanged(
+    source_hashes: Mapping[Path, str], *, model_path: Path, model_sha256: str
+) -> None:
+    if _hash_regular_path(
+        model_path, code="TRITRACK_RUN_INPUT_CHANGED"
+    ) != model_sha256 or any(
+        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
+        for path, expected in source_hashes.items()
+    ):
+        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")
+
+
+def prepare_run(
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    transcribe_media: Sequence[Path],
+    *,
+    model_path: Path,
+    language: str,
+    profile_id: str,
+    binding_id: str,
+    metadata: emit_fcpxml.ProjectMetadata,
+    run_id: str,
+    output_dir: Path,
+) -> dict[str, object]:
+    """Publish a doctor／sync／transcript／string-out prepared run bundle."""
+
+    process.require_absent_output(output_dir)
+    inventory, source_hashes = _source_inventory(
+        camera_a_sources, camera_b_sources, transcribe_media
+    )
+    selected_model = Path(model_path)
+    model_sha256 = _hash_regular_path(
+        selected_model, code="TRITRACK_RUN_INPUT_UNREADABLE"
+    )
+    selected_transcribe = [Path(path) for path in transcribe_media]
+    profile_hash = _hash_value(doctor.load_profile(profile_id))
+    binding_hash = _hash_value(doctor.load_title_binding(binding_id))
+    source_set_hash = _hash_value(inventory)
+    transcribed_hash = _hash_value(
+        [
+            source
+            for source in sorted(inventory, key=lambda item: item["mediaId"])
+            if source["transcribed"]
+        ]
+    )
+
+    def build(staging: Path) -> dict[str, object]:
+        receipt = doctor.write_receipt(
+            staging / "doctor.json",
+            profile_id=profile_id,
+            transcription_requested=True,
+            whisper_model=selected_model,
+        )
+        if receipt.get("supported") is not True:
+            raise ValueError("TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED")
+        sync_scan.synchronize_and_publish(
+            camera_a_sources,
+            camera_b_sources,
+            profile_id=profile_id,
+            output_path=staging / "sync-map.json",
+        )
+        transcribe_takes.transcribe_and_publish(
+            selected_transcribe,
+            model_path=selected_model,
+            language=language,
+            output_path=staging / "transcript-bundle.json",
+        )
+        emit_fcpxml.emit_and_publish(
+            camera_a_sources,
+            camera_b_sources,
+            sync_map_path=staging / "sync-map.json",
+            profile_id=profile_id,
+            binding_id=binding_id,
+            metadata=metadata,
+            output_path=staging / "string-out.fcpxml",
+        )
+        _require_inputs_unchanged(
+            source_hashes, model_path=selected_model, model_sha256=model_sha256
+        )
+        artifacts = _artifact_records(staging, "prepared")
+        stages = [
+            {
+                "name": "doctor",
+                "inputHashes": {
+                    "binding": binding_hash,
+                    "model": model_sha256,
+                    "profile": profile_hash,
+                },
+                "outputHashes": {
+                    "doctorReceipt": artifacts["doctorReceipt"]["sha256"]
+                },
+            },
+            {
+                "name": "sync",
+                "inputHashes": {"sourceSet": source_set_hash},
+                "outputHashes": {"syncMap": artifacts["syncMap"]["sha256"]},
+            },
+            {
+                "name": "transcribe",
+                "inputHashes": {
+                    "model": model_sha256,
+                    "transcribedSources": transcribed_hash,
+                },
+                "outputHashes": {
+                    "transcriptBundle": artifacts["transcriptBundle"]["sha256"]
+                },
+            },
+            {
+                "name": "emit",
+                "inputHashes": {
+                    "binding": binding_hash,
+                    "profile": profile_hash,
+                    "sourceSet": source_set_hash,
+                    "syncMap": artifacts["syncMap"]["sha256"],
+                },
+                "outputHashes": {"stringOut": artifacts["stringOut"]["sha256"]},
+            },
+        ]
+        return build_manifest(
+            run_id=run_id,
+            profile_id=profile_id,
+            binding_id=binding_id,
+            phase="prepared",
+            manifest_chain=[],
+            sources=inventory,
+            stages=stages,
+            artifacts=artifacts,
+        )
+
+    return summarize_bundle(publish_bundle(Path(output_dir), build))
+
+
+def _require_bundle_unchanged(bundle: LoadedRunBundle) -> None:
+    try:
+        current = load_bundle(bundle.root, expected_phase=str(bundle.manifest["phase"]))
+    except ValueError as error:
+        raise ValueError("TRITRACK_RUN_INPUT_CHANGED") from error
+    if current.manifest_sha256 != bundle.manifest_sha256:
+        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")
+
+
+def align_run(
+    prepared_dir: Path,
+    revision_path: Path,
+    *,
+    output_dir: Path,
+) -> dict[str, object]:
+    """Consume one complete prepared run and publish an aligned paper bundle."""
+
+    process.require_absent_output(output_dir)
+    prepared = load_bundle(prepared_dir, expected_phase="prepared")
+    revision = align_text.load_json_artifact(
+        Path(revision_path),
+        contract="text-revision-v1",
+        invalid_code="TRITRACK_ALIGNMENT_REVISION_INVALID",
+    )
+
+    def build(staging: Path) -> dict[str, object]:
+        align_text.align_and_publish(
+            prepared.artifacts["transcriptBundle"].path,
+            revision.path,
+            output_path=staging / "aligned-transcript.json",
+        )
+        paper_edit.export_workbook(
+            staging / "aligned-transcript.json",
+            grouping_path=None,
+            output_path=staging / "paper-edit.xlsx",
+        )
+        align_text.verify_artifact_unchanged(revision)
+        _require_bundle_unchanged(prepared)
+        artifacts = _artifact_records(staging, "aligned")
+        stages = [
+            {
+                "name": "align",
+                "inputHashes": {
+                    "preparedManifest": prepared.manifest_sha256,
+                    "revision": revision.sha256,
+                    "transcriptBundle": prepared.artifacts[
+                        "transcriptBundle"
+                    ].sha256,
+                },
+                "outputHashes": {
+                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
+                },
+            },
+            {
+                "name": "paper",
+                "inputHashes": {
+                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
+                },
+                "outputHashes": {
+                    "paperWorkbook": artifacts["paperWorkbook"]["sha256"]
+                },
+            },
+        ]
+        return build_manifest(
+            run_id=str(prepared.manifest["runId"]),
+            profile_id=str(prepared.manifest["profileId"]),
+            binding_id=str(prepared.manifest["bindingId"]),
+            phase="aligned",
+            manifest_chain=[prepared.manifest_sha256],
+            sources=prepared.manifest["sources"],
+            stages=stages,
+            artifacts=artifacts,
+        )
+
+    return summarize_bundle(publish_bundle(Path(output_dir), build))
+
+
+def _finish_source_hashes(
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    *,
+    expected_sources: object,
+) -> dict[Path, str]:
+    if not camera_a_sources or not camera_b_sources:
+        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
+    declared: list[tuple[str, sync_scan.MediaSource]] = [
+        *(("A", source) for source in camera_a_sources),
+        *(("B", source) for source in camera_b_sources),
+    ]
+    media_ids = [source.media_id for _, source in declared]
+    paths = [source.path for _, source in declared]
+    if (
+        len(media_ids) != len(set(media_ids))
+        or len(paths) != len(set(paths))
+        or any(source.media_id != source.path.name for _, source in declared)
+    ):
+        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
+    try:
+        hashes = {
+            source.path: _hash_regular_path(
+                source.path, code="TRITRACK_RUN_SOURCE_MISMATCH"
+            )
+            for _, source in declared
+        }
+        expected_by_id = {
+            str(source["mediaId"]): source for source in expected_sources
+        }
+    except (KeyError, TypeError, ValueError) as error:
+        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH") from error
+    if set(media_ids) != set(expected_by_id):
+        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
+    for camera, source in declared:
+        expected = expected_by_id[source.media_id]
+        if (
+            expected["camera"] != camera
+            or expected["sha256"] != hashes[source.path]
+        ):
+            raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
+    return hashes
+
+
+def _require_path_hashes_unchanged(path_hashes: Mapping[Path, str]) -> None:
+    if any(
+        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
+        for path, expected in path_hashes.items()
+    ):
+        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")
+
+
+def _validate_finish_chain(
+    prepared: LoadedRunBundle, aligned: LoadedRunBundle
+) -> None:
+    if aligned.manifest["manifestChain"] != [prepared.manifest_sha256]:
+        raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")
+    for field in ("runId", "profileId", "bindingId", "sources"):
+        if aligned.manifest[field] != prepared.manifest[field]:
+            raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")
+
+
+def finish_run(
+    prepared_dir: Path,
+    aligned_dir: Path,
+    workbook_path: Path,
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    *,
+    metadata: emit_fcpxml.ProjectMetadata,
+    output_dir: Path,
+) -> dict[str, object]:
+    """Apply paper intent and publish one exact story-cut result bundle."""
+
+    process.require_absent_output(output_dir)
+    prepared = load_bundle(prepared_dir, expected_phase="prepared")
+    aligned = load_bundle(aligned_dir, expected_phase="aligned")
+    _validate_finish_chain(prepared, aligned)
+    source_hashes = _finish_source_hashes(
+        camera_a_sources,
+        camera_b_sources,
+        expected_sources=prepared.manifest["sources"],
+    )
+    selected_workbook = Path(workbook_path)
+    workbook_sha256 = _hash_regular_path(
+        selected_workbook, code="TRITRACK_PAPER_WORKBOOK_INVALID"
+    )
+    source_set_hash = _hash_value(prepared.manifest["sources"])
+
+    def build(staging: Path) -> dict[str, object]:
+        paper_edit.apply_workbook(
+            aligned.artifacts["alignedTranscript"].path,
+            selected_workbook,
+            output_path=staging / "grouping.json",
+        )
+        organizer.organize_and_publish(
+            aligned.artifacts["alignedTranscript"].path,
+            staging / "grouping.json",
+            output_path=staging / "working-cut.json",
+        )
+        story_fcpxml.emit_story_and_publish(
+            camera_a_sources,
+            camera_b_sources,
+            sync_map_path=prepared.artifacts["syncMap"].path,
+            aligned_path=aligned.artifacts["alignedTranscript"].path,
+            grouping_path=staging / "grouping.json",
+            working_cut_path=staging / "working-cut.json",
+            profile_id=str(prepared.manifest["profileId"]),
+            binding_id=str(prepared.manifest["bindingId"]),
+            metadata=metadata,
+            output_path=staging / "story-cut.fcpxml",
+        )
+        _require_bundle_unchanged(prepared)
+        _require_bundle_unchanged(aligned)
+        _require_path_hashes_unchanged(
+            {**source_hashes, selected_workbook: workbook_sha256}
+        )
+        artifacts = _artifact_records(staging, "finished")
+        stages = [
+            {
+                "name": "paper",
+                "inputHashes": {
+                    "alignedTranscript": aligned.artifacts[
+                        "alignedTranscript"
+                    ].sha256,
+                    "workbook": workbook_sha256,
+                },
+                "outputHashes": {"grouping": artifacts["grouping"]["sha256"]},
+            },
+            {
+                "name": "organize",
+                "inputHashes": {
+                    "alignedTranscript": aligned.artifacts[
+                        "alignedTranscript"
+                    ].sha256,
+                    "grouping": artifacts["grouping"]["sha256"],
+                },
+                "outputHashes": {
+                    "workingCut": artifacts["workingCut"]["sha256"]
+                },
+            },
+            {
+                "name": "emit",
+                "inputHashes": {
+                    "alignedTranscript": aligned.artifacts[
+                        "alignedTranscript"
+                    ].sha256,
+                    "grouping": artifacts["grouping"]["sha256"],
+                    "sourceSet": source_set_hash,
+                    "syncMap": prepared.artifacts["syncMap"].sha256,
+                    "workingCut": artifacts["workingCut"]["sha256"],
+                },
+                "outputHashes": {"storyCut": artifacts["storyCut"]["sha256"]},
+            },
+        ]
+        return build_manifest(
+            run_id=str(prepared.manifest["runId"]),
+            profile_id=str(prepared.manifest["profileId"]),
+            binding_id=str(prepared.manifest["bindingId"]),
+            phase="finished",
+            manifest_chain=[prepared.manifest_sha256, aligned.manifest_sha256],
+            sources=prepared.manifest["sources"],
+            stages=stages,
+            artifacts=artifacts,
+        )
+
+    return summarize_bundle(publish_bundle(Path(output_dir), build))
+
+
+def status_run(run_dir: Path) -> dict[str, object]:
+    """Validate and summarize one run bundle without writing anything."""
+
+    return summarize_bundle(load_bundle(Path(run_dir)))
diff --git a/src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json b/src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json
index 2725568..6b20f42 100644
--- a/src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json
+++ b/src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json
@@ -1,27 +1,193 @@
 {
   "$schema": "https://json-schema.org/draft/2020-12/schema",
   "$id": "https://tritrack.dev/schemas/run-manifest-v1.schema.json",
-  "title": "TriTrack run manifest v1",
+  "title": "TriTrack immutable run manifest v1",
   "type": "object",
   "additionalProperties": false,
-  "required": ["schemaVersion", "toolVersion", "runId", "profileId", "stages"],
+  "required": [
+    "schemaVersion",
+    "toolVersion",
+    "runId",
+    "profileId",
+    "bindingId",
+    "phase",
+    "nextAction",
+    "manifestChain",
+    "sources",
+    "artifacts",
+    "stages"
+  ],
   "properties": {
     "schemaVersion": {"const": "tritrack.run-manifest/v1"},
-    "toolVersion": {"type": "string", "minLength": 1},
-    "runId": {"type": "string", "minLength": 1},
-    "profileId": {"type": "string", "minLength": 1},
-    "createdAt": {"type": "string", "format": "date-time"},
+    "toolVersion": {"const": "0.1.0a0"},
+    "runId": {
+      "type": "string",
+      "minLength": 1,
+      "maxLength": 128,
+      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
+    },
+    "profileId": {"const": "uhd-2997-ndf-fcpxml-1.14"},
+    "bindingId": {"const": "basic-title-v1"},
+    "phase": {"enum": ["prepared", "aligned", "finished"]},
+    "nextAction": {
+      "enum": ["provide-revision", "edit-paper-workbook", "complete"]
+    },
+    "manifestChain": {
+      "type": "array",
+      "uniqueItems": true,
+      "items": {"$ref": "#/$defs/sha256"}
+    },
+    "sources": {
+      "type": "array",
+      "minItems": 1,
+      "uniqueItems": true,
+      "items": {"$ref": "#/$defs/source"}
+    },
+    "artifacts": {
+      "type": "object",
+      "additionalProperties": false,
+      "properties": {
+        "doctorReceipt": {"$ref": "#/$defs/artifact"},
+        "syncMap": {"$ref": "#/$defs/artifact"},
+        "transcriptBundle": {"$ref": "#/$defs/artifact"},
+        "stringOut": {"$ref": "#/$defs/artifact"},
+        "alignedTranscript": {"$ref": "#/$defs/artifact"},
+        "paperWorkbook": {"$ref": "#/$defs/artifact"},
+        "grouping": {"$ref": "#/$defs/artifact"},
+        "workingCut": {"$ref": "#/$defs/artifact"},
+        "storyCut": {"$ref": "#/$defs/artifact"}
+      }
+    },
     "stages": {
       "type": "array",
+      "minItems": 1,
       "items": {"$ref": "#/$defs/stage"}
     }
   },
+  "allOf": [
+    {
+      "if": {"properties": {"phase": {"const": "prepared"}}},
+      "then": {
+        "properties": {
+          "nextAction": {"const": "provide-revision"},
+          "manifestChain": {"maxItems": 0},
+          "artifacts": {
+            "required": [
+              "doctorReceipt",
+              "syncMap",
+              "transcriptBundle",
+              "stringOut"
+            ],
+            "propertyNames": {
+              "enum": [
+                "doctorReceipt",
+                "syncMap",
+                "transcriptBundle",
+                "stringOut"
+              ]
+            }
+          },
+          "stages": {
+            "minItems": 4,
+            "maxItems": 4,
+            "prefixItems": [
+              {"properties": {"name": {"const": "doctor"}}},
+              {"properties": {"name": {"const": "sync"}}},
+              {"properties": {"name": {"const": "transcribe"}}},
+              {"properties": {"name": {"const": "emit"}}}
+            ]
+          }
+        }
+      }
+    },
+    {
+      "if": {"properties": {"phase": {"const": "aligned"}}},
+      "then": {
+        "properties": {
+          "nextAction": {"const": "edit-paper-workbook"},
+          "manifestChain": {"minItems": 1, "maxItems": 1},
+          "artifacts": {
+            "required": ["alignedTranscript", "paperWorkbook"],
+            "propertyNames": {
+              "enum": ["alignedTranscript", "paperWorkbook"]
+            }
+          },
+          "stages": {
+            "minItems": 2,
+            "maxItems": 2,
+            "prefixItems": [
+              {"properties": {"name": {"const": "align"}}},
+              {"properties": {"name": {"const": "paper"}}}
+            ]
+          }
+        }
+      }
+    },
+    {
+      "if": {"properties": {"phase": {"const": "finished"}}},
+      "then": {
+        "properties": {
+          "nextAction": {"const": "complete"},
+          "manifestChain": {"minItems": 2, "maxItems": 2},
+          "artifacts": {
+            "required": ["grouping", "workingCut", "storyCut"],
+            "propertyNames": {"enum": ["grouping", "workingCut", "storyCut"]}
+          },
+          "stages": {
+            "minItems": 3,
+            "maxItems": 3,
+            "prefixItems": [
+              {"properties": {"name": {"const": "paper"}}},
+              {"properties": {"name": {"const": "organize"}}},
+              {"properties": {"name": {"const": "emit"}}}
+            ]
+          }
+        }
+      }
+    }
+  ],
   "$defs": {
     "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
+    "hashMap": {
+      "type": "object",
+      "minProperties": 1,
+      "propertyNames": {"pattern": "^[A-Za-z][A-Za-z0-9]*$"},
+      "additionalProperties": {"$ref": "#/$defs/sha256"}
+    },
+    "source": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["camera", "mediaId", "sha256", "transcribed"],
+      "properties": {
+        "camera": {"enum": ["A", "B"]},
+        "mediaId": {
+          "type": "string",
+          "minLength": 1,
+          "maxLength": 255,
+          "pattern": "^[^/\\\\\\r\\n]+$"
+        },
+        "sha256": {"$ref": "#/$defs/sha256"},
+        "transcribed": {"type": "boolean"}
+      }
+    },
+    "artifact": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["fileName", "sha256"],
+      "properties": {
+        "fileName": {
+          "type": "string",
+          "minLength": 1,
+          "maxLength": 128,
+          "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
+        },
+        "sha256": {"$ref": "#/$defs/sha256"}
+      }
+    },
     "stage": {
       "type": "object",
       "additionalProperties": false,
-      "required": ["name", "status", "inputHashes", "receiptSha256"],
+      "required": ["name", "inputHashes", "outputHashes"],
       "properties": {
         "name": {
           "enum": [
@@ -29,22 +195,13 @@
             "sync",
             "transcribe",
             "align",
-            "hybrid",
             "emit",
-            "validate",
             "organize",
             "paper"
           ]
         },
-        "status": {"enum": ["planned", "running", "completed", "failed", "skipped"]},
-        "inputHashes": {
-          "type": "object",
-          "minProperties": 1,
-          "propertyNames": {"pattern": "^[A-Za-z][A-Za-z0-9]*$"},
-          "additionalProperties": {"$ref": "#/$defs/sha256"}
-        },
-        "receiptSha256": {"$ref": "#/$defs/sha256"},
-        "outputManifestSha256": {"$ref": "#/$defs/sha256"}
+        "inputHashes": {"$ref": "#/$defs/hashMap"},
+        "outputHashes": {"$ref": "#/$defs/hashMap"}
       }
     }
   }
diff --git a/src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json b/src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json
index 7345557..f005cc8 100644
--- a/src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json
+++ b/src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json
@@ -11,7 +11,6 @@
     "language": {"type": "string", "pattern": "^[a-z]{2,3}$"},
     "takes": {
       "type": "array",
-      "minItems": 1,
       "items": {"$ref": "#/$defs/take"}
     }
   },
diff --git a/src/tritrack_editing_assistant/story_fcpxml.py b/src/tritrack_editing_assistant/story_fcpxml.py
new file mode 100644
index 0000000..a755325
--- /dev/null
+++ b/src/tritrack_editing_assistant/story_fcpxml.py
@@ -0,0 +1,806 @@
+"""Deterministic projection of exact editorial authorities into story time."""
+
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import stat
+import xml.etree.ElementTree as ET
+from collections.abc import Mapping, Sequence
+from dataclasses import dataclass
+from decimal import Decimal
+from fractions import Fraction
+from pathlib import Path
+
+from jsonschema import ValidationError
+
+from . import (
+    contracts,
+    doctor,
+    emit_fcpxml,
+    organizer,
+    process,
+    string_out,
+    sync_scan,
+)
+
+_SOURCE_FIELDS = frozenset(
+    {"camera", "media_id", "path", "duration_seconds", "sha256"}
+)
+_JSON_LIMIT_BYTES = 16 * 1024 * 1024
+_HASH_CHUNK_BYTES = 1024 * 1024
+
+
+@dataclass(frozen=True)
+class StorySource:
+    """One exact local source available to the story projection."""
+
+    camera: str
+    media_id: str
+    path: Path
+    duration_frames: int
+    sha256: str
+
+
+@dataclass(frozen=True)
+class StoryClip:
+    """One source excerpt placed inside a story segment."""
+
+    camera: str
+    media_id: str
+    path: Path
+    offset_frames: int
+    start_frames: int
+    duration_frames: int
+    audio_enabled: bool
+
+
+@dataclass(frozen=True)
+class StorySegment:
+    """One selected cue range in final editor story order."""
+
+    segment_id: str
+    offset_frames: int
+    duration_frames: int
+    title_text: str
+    clips: tuple[StoryClip, ...]
+
+
+@dataclass(frozen=True)
+class StoryTimeline:
+    """A complete story projection expressed only in integer frames."""
+
+    profile_id: str
+    frame_numerator: int
+    frame_denominator: int
+    duration_frames: int
+    sources: tuple[StorySource, ...]
+    segments: tuple[StorySegment, ...]
+
+
+@dataclass(frozen=True)
+class _SourceRelationship:
+    kind: str
+    source_a: StorySource | None
+    source_b: StorySource | None
+    offset_b_from_a_frames: int
+    audio_master: str
+
+
+@dataclass(frozen=True)
+class _LoadedArtifact:
+    path: Path
+    payload: object
+    encoded: bytes
+    sha256: str
+    invalid_code: str
+
+
+def _validate_contract(name: str, payload: object, code: str) -> None:
+    try:
+        contracts.validate_contract(name, payload)
+    except ValidationError as error:
+        raise ValueError(code) from error
+
+
+def _seconds_from_ms(value: int) -> Decimal:
+    return Decimal(value) / Decimal(1000)
+
+
+def _normalize_working_cut(payload: Mapping[str, object]) -> dict[str, object]:
+    segments = payload["segments"]
+    assert isinstance(segments, list)
+    return {
+        **payload,
+        "segments": sorted(segments, key=lambda item: item["storyOrder"]),
+    }
+
+
+def _normalize_sources(
+    sync_map: Mapping[str, object],
+    sources: Sequence[Mapping[str, object]],
+    *,
+    profile: Mapping[str, object],
+) -> tuple[tuple[StorySource, ...], string_out.StringOut]:
+    stripped: list[dict[str, object]] = []
+    hashes: dict[tuple[str, str], str] = {}
+    media_ids: set[str] = set()
+    for source in sources:
+        if not isinstance(source, Mapping) or set(source) != _SOURCE_FIELDS:
+            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
+        camera = source["camera"]
+        media_id = source["media_id"]
+        sha256 = source["sha256"]
+        if (
+            camera not in {"A", "B"}
+            or not isinstance(media_id, str)
+            or not media_id
+            or media_id in media_ids
+            or not isinstance(sha256, str)
+            or len(sha256) != 64
+            or any(character not in "0123456789abcdef" for character in sha256)
+        ):
+            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
+        media_ids.add(media_id)
+        hashes[(camera, media_id)] = sha256
+        stripped.append(
+            {
+                "camera": camera,
+                "media_id": media_id,
+                "path": source["path"],
+                "duration_seconds": source["duration_seconds"],
+            }
+        )
+
+    try:
+        base = string_out.build_string_out(sync_map, stripped, profile=profile)
+    except (TypeError, ValueError, ValidationError) as error:
+        raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID") from error
+    normalized = tuple(
+        StorySource(
+            camera=source.camera,
+            media_id=source.media_id,
+            path=source.path,
+            duration_frames=source.duration_frames,
+            sha256=hashes[(source.camera, source.media_id)],
+        )
+        for source in base.sources
+    )
+    return normalized, base
+
+
+def _build_relationships(
+    sync_map: Mapping[str, object],
+    source_by_media: Mapping[str, StorySource],
+    *,
+    frame_duration: Fraction,
+) -> dict[str, _SourceRelationship]:
+    relationships: dict[str, _SourceRelationship] = {}
+
+    def register(media_id: str, relationship: _SourceRelationship) -> None:
+        if media_id in relationships:
+            raise ValueError("TRITRACK_STORY_SYNC_CONFLICT")
+        relationships[media_id] = relationship
+
+    pairs = sync_map["pairs"]
+    assert isinstance(pairs, list)
+    for pair in pairs:
+        assert isinstance(pair, Mapping)
+        media_a = str(pair["mediaA"])
+        media_b = str(pair["mediaB"])
+        source_a = source_by_media.get(media_a)
+        source_b = source_by_media.get(media_b)
+        if (
+            source_a is None
+            or source_b is None
+            or source_a.camera != "A"
+            or source_b.camera != "B"
+        ):
+            raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
+        offset_frames = string_out.seconds_to_frames(
+            pair["offsetBFromASeconds"], frame_duration
+        )
+        relationship = _SourceRelationship(
+            kind="pair",
+            source_a=source_a,
+            source_b=source_b,
+            offset_b_from_a_frames=offset_frames,
+            audio_master=str(pair["audioMaster"]),
+        )
+        register(media_a, relationship)
+        register(media_b, relationship)
+
+    for camera, field in (("A", "singleA"), ("B", "singleB")):
+        singles = sync_map[field]
+        assert isinstance(singles, list)
+        for value in singles:
+            media_id = str(value)
+            source = source_by_media.get(media_id)
+            if source is None or source.camera != camera:
+                raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
+            register(
+                media_id,
+                _SourceRelationship(
+                    kind="single",
+                    source_a=source if camera == "A" else None,
+                    source_b=source if camera == "B" else None,
+                    offset_b_from_a_frames=0,
+                    audio_master=camera,
+                ),
+            )
+    return relationships
+
+
+def _paired_clips(
+    relationship: _SourceRelationship,
+    selected: StorySource,
+    *,
+    selected_start: int,
+    selected_end: int,
+    story_offset: int,
+) -> tuple[StoryClip, ...]:
+    assert relationship.source_a is not None
+    assert relationship.source_b is not None
+    global_starts = {
+        "A": 0,
+        "B": relationship.offset_b_from_a_frames,
+    }
+    selected_global_start = selected_start + global_starts[selected.camera]
+    selected_global_end = selected_end + global_starts[selected.camera]
+    master = (
+        relationship.source_a
+        if relationship.audio_master == "A"
+        else relationship.source_b
+    )
+    master_start = global_starts[master.camera]
+    master_end = master_start + master.duration_frames
+    if master_start > selected_global_start or master_end < selected_global_end:
+        raise ValueError("TRITRACK_STORY_AUDIO_MASTER_COVERAGE")
+
+    clips: list[StoryClip] = []
+    for source in (relationship.source_a, relationship.source_b):
+        source_global_start = global_starts[source.camera]
+        source_global_end = source_global_start + source.duration_frames
+        intersection_start = max(selected_global_start, source_global_start)
+        intersection_end = min(selected_global_end, source_global_end)
+        if intersection_end <= intersection_start:
+            continue
+        clips.append(
+            StoryClip(
+                camera=source.camera,
+                media_id=source.media_id,
+                path=source.path,
+                offset_frames=story_offset
+                + intersection_start
+                - selected_global_start,
+                start_frames=intersection_start - source_global_start,
+                duration_frames=intersection_end - intersection_start,
+                audio_enabled=source.camera == relationship.audio_master,
+            )
+        )
+    return tuple(clips)
+
+
+def build_story_timeline(
+    sync_map: Mapping[str, object],
+    aligned: Mapping[str, object],
+    grouping: Mapping[str, object],
+    working_cut: Mapping[str, object],
+    sources: Sequence[Mapping[str, object]],
+    *,
+    aligned_sha256: str,
+    grouping_sha256: str,
+    profile: Mapping[str, object],
+) -> StoryTimeline:
+    """Re-derive and project selected cue spans into deterministic story time."""
+
+    _validate_contract("sync-map-v1", sync_map, "TRITRACK_STORY_SYNC_INVALID")
+    _validate_contract(
+        "aligned-transcript-v1", aligned, "TRITRACK_STORY_ALIGNED_INVALID"
+    )
+    _validate_contract("grouping-v1", grouping, "TRITRACK_STORY_GROUPING_INVALID")
+    _validate_contract(
+        "working-cut-v1", working_cut, "TRITRACK_STORY_WORKING_CUT_INVALID"
+    )
+    _validate_contract(
+        "compatibility-profile-v1", profile, "TRITRACK_STORY_PROFILE_INVALID"
+    )
+    profile_id = str(profile["profileId"])
+    if (
+        dict(profile) != doctor.load_profile(profile_id)
+        or sync_map["profileId"] != profile_id
+    ):
+        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")
+
+    try:
+        expected_working_cut = organizer.build_working_cut(
+            aligned,
+            grouping,
+            aligned_sha256=aligned_sha256,
+            grouping_sha256=grouping_sha256,
+        )
+    except (TypeError, ValueError, ValidationError) as error:
+        raise ValueError("TRITRACK_STORY_AUTHORITY_INVALID") from error
+    if _normalize_working_cut(working_cut) != expected_working_cut:
+        raise ValueError("TRITRACK_STORY_WORKING_CUT_DRIFT")
+
+    normalized_sources, base_timeline = _normalize_sources(
+        sync_map, sources, profile=profile
+    )
+    source_by_media = {source.media_id: source for source in normalized_sources}
+    frame_duration = Fraction(
+        base_timeline.frame_numerator, base_timeline.frame_denominator
+    )
+    relationships = _build_relationships(
+        sync_map,
+        source_by_media,
+        frame_duration=frame_duration,
+    )
+
+    takes = aligned["takes"]
+    assert isinstance(takes, list)
+    take_by_id = {str(take["takeId"]): take for take in takes}
+    segments = expected_working_cut["segments"]
+    assert isinstance(segments, list)
+    story_segments: list[StorySegment] = []
+    cursor = 0
+    for segment in segments:
+        assert isinstance(segment, Mapping)
+        take_id = str(segment["takeId"])
+        take = take_by_id.get(take_id)
+        source = source_by_media.get(take_id)
+        relationship = relationships.get(take_id)
+        if take is None or source is None or relationship is None:
+            raise ValueError("TRITRACK_STORY_TAKE_UNKNOWN")
+        if take["sourceSha256"] != source.sha256:
+            raise ValueError("TRITRACK_STORY_SOURCE_HASH_MISMATCH")
+
+        cues = take["cues"]
+        assert isinstance(cues, list)
+        positions = {str(cue["cueId"]): index for index, cue in enumerate(cues)}
+        start_position = positions.get(str(segment["startCueId"]))
+        end_position = positions.get(str(segment["endCueId"]))
+        if (
+            start_position is None
+            or end_position is None
+            or start_position > end_position
+        ):
+            raise ValueError("TRITRACK_STORY_CUE_UNKNOWN")
+        selected_cues = cues[start_position : end_position + 1]
+        start_ms = int(selected_cues[0]["startMs"])
+        end_ms = int(selected_cues[-1]["endMs"])
+        start_frames = string_out.seconds_to_frames(
+            _seconds_from_ms(start_ms), frame_duration
+        )
+        end_frames = string_out.seconds_to_frames(
+            _seconds_from_ms(end_ms), frame_duration
+        )
+        if end_frames <= start_frames or end_frames > source.duration_frames:
+            raise ValueError("TRITRACK_STORY_SELECTION_INVALID")
+        duration_frames = end_frames - start_frames
+        title_text = " ".join(str(cue["text"]) for cue in selected_cues)
+
+        if relationship.kind == "single":
+            clips = (
+                StoryClip(
+                    camera=source.camera,
+                    media_id=source.media_id,
+                    path=source.path,
+                    offset_frames=cursor,
+                    start_frames=start_frames,
+                    duration_frames=duration_frames,
+                    audio_enabled=True,
+                ),
+            )
+        else:
+            clips = _paired_clips(
+                relationship,
+                source,
+                selected_start=start_frames,
+                selected_end=end_frames,
+                story_offset=cursor,
+            )
+        story_segments.append(
+            StorySegment(
+                segment_id=str(segment["id"]),
+                offset_frames=cursor,
+                duration_frames=duration_frames,
+                title_text=title_text,
+                clips=clips,
+            )
+        )
+        cursor += duration_frames
+
+    return StoryTimeline(
+        profile_id=profile_id,
+        frame_numerator=base_timeline.frame_numerator,
+        frame_denominator=base_timeline.frame_denominator,
+        duration_frames=cursor,
+        sources=normalized_sources,
+        segments=tuple(story_segments),
+    )
+
+
+def _frame_time(timeline: StoryTimeline, frames: int) -> str:
+    if frames == 0:
+        return "0s"
+    return f"{frames * timeline.frame_numerator}/{timeline.frame_denominator}s"
+
+
+def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
+    parameters = binding["parameters"]
+    if not isinstance(parameters, list):
+        raise TypeError("TRITRACK_STORY_BINDING_INVALID")
+    values = {
+        str(parameter["name"]): str(parameter["value"])
+        for parameter in parameters
+        if isinstance(parameter, Mapping)
+    }
+    expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
+    if set(values) != expected:
+        raise ValueError("TRITRACK_STORY_BINDING_INVALID")
+    return values
+
+
+def _validate_timeline(timeline: StoryTimeline) -> None:
+    if not isinstance(timeline, StoryTimeline) or timeline.duration_frames <= 0:
+        raise TypeError("TRITRACK_STORY_TIMELINE_INVALID")
+    source_keys = [(source.camera, source.media_id) for source in timeline.sources]
+    if source_keys != sorted(source_keys) or len(source_keys) != len(set(source_keys)):
+        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
+    source_by_key = {
+        (source.camera, source.media_id): source for source in timeline.sources
+    }
+    cursor = 0
+    for segment in timeline.segments:
+        if (
+            segment.offset_frames != cursor
+            or segment.duration_frames <= 0
+            or not segment.title_text
+            or not segment.clips
+            or sum(clip.audio_enabled for clip in segment.clips) != 1
+        ):
+            raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
+        for clip in segment.clips:
+            source = source_by_key.get((clip.camera, clip.media_id))
+            if (
+                source is None
+                or clip.path != source.path
+                or clip.offset_frames < segment.offset_frames
+                or clip.start_frames < 0
+                or clip.duration_frames <= 0
+                or clip.start_frames + clip.duration_frames > source.duration_frames
+                or clip.offset_frames + clip.duration_frames
+                > segment.offset_frames + segment.duration_frames
+            ):
+                raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
+        cursor += segment.duration_frames
+    if cursor != timeline.duration_frames:
+        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
+
+
+def render_story_fcpxml(
+    timeline: StoryTimeline,
+    *,
+    profile_id: str,
+    binding_id: str,
+    metadata: emit_fcpxml.ProjectMetadata,
+) -> str:
+    """Render one deterministic Final Cut XML projection of a story timeline."""
+
+    _validate_timeline(timeline)
+    if not isinstance(metadata, emit_fcpxml.ProjectMetadata):
+        raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
+    profile = doctor.load_profile(profile_id)
+    binding = doctor.load_title_binding(binding_id)
+    if timeline.profile_id != profile_id:
+        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")
+    styles = _style_values(binding)
+
+    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
+    resources_element = ET.SubElement(root, "resources")
+    ET.SubElement(
+        resources_element,
+        "format",
+        {
+            "id": "r1",
+            "name": emit_fcpxml.FORMAT_NAME,
+            "frameDuration": str(profile["frameDuration"]),
+            "width": str(profile["width"]),
+            "height": str(profile["height"]),
+            "colorSpace": str(profile["colorSpace"]),
+        },
+    )
+    ET.SubElement(
+        resources_element,
+        "effect",
+        {
+            "id": "r2",
+            "name": str(binding["effectName"]),
+            "uid": str(binding["effectUid"]),
+        },
+    )
+    source_ids: dict[tuple[str, str], str] = {}
+    for index, source in enumerate(timeline.sources, start=3):
+        resource_id = f"r{index}"
+        source_ids[(source.camera, source.media_id)] = resource_id
+        asset = ET.SubElement(
+            resources_element,
+            "asset",
+            {
+                "id": resource_id,
+                "name": source.media_id,
+                "start": "0s",
+                "duration": _frame_time(timeline, source.duration_frames),
+                "hasVideo": "1",
+                "hasAudio": "1",
+                "format": "r1",
+                "audioSources": "1",
+                "audioChannels": "2",
+                "audioRate": f"{int(profile['audioRate']) // 1000}k",
+            },
+        )
+        ET.SubElement(
+            asset,
+            "media-rep",
+            {"kind": "original-media", "src": source.path.absolute().as_uri()},
+        )
+
+    library = ET.SubElement(root, "library")
+    event = ET.SubElement(library, "event", {"name": metadata.event_name})
+    project = ET.SubElement(event, "project", {"name": metadata.project_name})
+    sequence = ET.SubElement(
+        project,
+        "sequence",
+        {
+            "format": "r1",
+            "duration": _frame_time(timeline, timeline.duration_frames),
+            "tcStart": "0s",
+            "tcFormat": str(profile["timecodeFormat"]),
+            "audioLayout": "stereo",
+            "audioRate": f"{int(profile['audioRate']) // 1000}k",
+        },
+    )
+    spine = ET.SubElement(sequence, "spine")
+    for index, segment in enumerate(timeline.segments, start=1):
+        gap = ET.SubElement(
+            spine,
+            "gap",
+            {
+                "name": segment.segment_id,
+                "offset": _frame_time(timeline, segment.offset_frames),
+                "start": "0s",
+                "duration": _frame_time(timeline, segment.duration_frames),
+            },
+        )
+        for lane, clip in enumerate(segment.clips, start=1):
+            attributes = {
+                "ref": source_ids[(clip.camera, clip.media_id)],
+                "lane": str(lane),
+                "offset": _frame_time(timeline, clip.offset_frames),
+                "name": clip.media_id,
+                "start": _frame_time(timeline, clip.start_frames),
+                "duration": _frame_time(timeline, clip.duration_frames),
+                "srcEnable": "all" if clip.audio_enabled else "video",
+            }
+            if clip.audio_enabled:
+                attributes["audioRole"] = "dialogue"
+            ET.SubElement(gap, "asset-clip", attributes)
+        title = ET.SubElement(
+            gap,
+            "title",
+            {
+                "ref": "r2",
+                "lane": str(len(segment.clips) + 1),
+                "offset": _frame_time(timeline, segment.offset_frames),
+                "name": f"{segment.segment_id} - Basic Title",
+                "start": "0s",
+                "duration": _frame_time(timeline, segment.duration_frames),
+            },
+        )
+        text_element = ET.SubElement(title, "text")
+        style_id = f"ts{index:03d}"
+        text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
+        text_style.text = segment.title_text
+        definition = ET.SubElement(title, "text-style-def", {"id": style_id})
+        ET.SubElement(
+            definition,
+            "text-style",
+            {
+                name: styles[name]
+                for name in (
+                    "alignment",
+                    "font",
+                    "fontColor",
+                    "fontFace",
+                    "fontSize",
+                )
+            },
+        )
+
+    ET.indent(root, space="    ")
+    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
+    rendered = (
+        '<?xml version="1.0" encoding="UTF-8"?>\n'
+        f"{emit_fcpxml.ALLOWED_DOCTYPE}\n{body}\n"
+    )
+    emit_fcpxml.validate_fcpxml(rendered, profile=profile, binding=binding)
+    return rendered
+
+
+def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError(invalid_code) from error
+    try:
+        metadata = os.fstat(descriptor)
+        if (
+            not stat.S_ISREG(metadata.st_mode)
+            or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
+        ):
+            raise ValueError(invalid_code)
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(_JSON_LIMIT_BYTES + 1)
+        if len(encoded) > _JSON_LIMIT_BYTES:
+            raise ValueError(invalid_code)
+        return encoded
+    except OSError as error:
+        raise ValueError(invalid_code) from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+
+
+def _load_artifact(path: Path, *, contract: str, code: str) -> _LoadedArtifact:
+    selected = Path(path)
+    encoded = _read_regular_bytes(selected, code)
+    try:
+        payload = json.loads(
+            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
+        )
+        contracts.validate_contract(contract, payload)
+    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
+        raise ValueError(code) from error
+    return _LoadedArtifact(
+        path=selected,
+        payload=payload,
+        encoded=encoded,
+        sha256=hashlib.sha256(encoded).hexdigest(),
+        invalid_code=code,
+    )
+
+
+def _verify_artifact(artifact: _LoadedArtifact) -> None:
+    try:
+        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
+    except ValueError as error:
+        raise ValueError("TRITRACK_STORY_INPUT_CHANGED") from error
+    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
+        raise ValueError("TRITRACK_STORY_INPUT_CHANGED")
+
+
+def _hash_regular_media(path: Path) -> str:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
+    digest = hashlib.sha256()
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
+            raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            while chunk := stream.read(_HASH_CHUNK_BYTES):
+                digest.update(chunk)
+    except OSError as error:
+        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+    return digest.hexdigest()
+
+
+def emit_story_and_publish(
+    camera_a_sources: Sequence[sync_scan.MediaSource],
+    camera_b_sources: Sequence[sync_scan.MediaSource],
+    *,
+    sync_map_path: Path,
+    aligned_path: Path,
+    grouping_path: Path,
+    working_cut_path: Path,
+    profile_id: str,
+    binding_id: str,
+    metadata: emit_fcpxml.ProjectMetadata,
+    output_path: Path,
+) -> str:
+    """Load exact authorities, render a story cut, and publish without overwrite."""
+
+    destination = process.require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    sync_map = _load_artifact(
+        sync_map_path, contract="sync-map-v1", code="TRITRACK_STORY_SYNC_INVALID"
+    )
+    aligned = _load_artifact(
+        aligned_path,
+        contract="aligned-transcript-v1",
+        code="TRITRACK_STORY_ALIGNED_INVALID",
+    )
+    grouping = _load_artifact(
+        grouping_path,
+        contract="grouping-v1",
+        code="TRITRACK_STORY_GROUPING_INVALID",
+    )
+    working_cut = _load_artifact(
+        working_cut_path,
+        contract="working-cut-v1",
+        code="TRITRACK_STORY_WORKING_CUT_INVALID",
+    )
+    if grouping.encoded != organizer.encode_grouping(grouping.payload):
+        raise ValueError("TRITRACK_STORY_GROUPING_NONCANONICAL")
+    if working_cut.encoded != organizer.encode_working_cut(working_cut.payload):
+        raise ValueError("TRITRACK_STORY_WORKING_CUT_NONCANONICAL")
+
+    profile = doctor.load_profile(profile_id)
+    doctor.load_title_binding(binding_id)
+    source_hashes = {
+        (camera, source.media_id): _hash_regular_media(source.path)
+        for camera, camera_sources in (
+            ("A", camera_a_sources),
+            ("B", camera_b_sources),
+        )
+        for source in camera_sources
+    }
+    probed = emit_fcpxml.probe_sources(
+        camera_a_sources, camera_b_sources, profile=profile
+    )
+    sources = [
+        {**source, "sha256": source_hashes[(source["camera"], source["media_id"])]}
+        for source in probed
+    ]
+    assert isinstance(sync_map.payload, Mapping)
+    assert isinstance(aligned.payload, Mapping)
+    assert isinstance(grouping.payload, Mapping)
+    assert isinstance(working_cut.payload, Mapping)
+    timeline = build_story_timeline(
+        sync_map.payload,
+        aligned.payload,
+        grouping.payload,
+        working_cut.payload,
+        sources,
+        aligned_sha256=aligned.sha256,
+        grouping_sha256=grouping.sha256,
+        profile=profile,
+    )
+    rendered = render_story_fcpxml(
+        timeline,
+        profile_id=profile_id,
+        binding_id=binding_id,
+        metadata=metadata,
+    )
+    for artifact in (sync_map, aligned, grouping, working_cut):
+        _verify_artifact(artifact)
+    for camera, camera_sources in (
+        ("A", camera_a_sources),
+        ("B", camera_b_sources),
+    ):
+        for source in camera_sources:
+            if _hash_regular_media(source.path) != source_hashes[(camera, source.media_id)]:
+                raise ValueError("TRITRACK_STORY_INPUT_CHANGED")
+    emit_fcpxml.publish_fcpxml(
+        destination,
+        rendered,
+        profile=profile,
+        binding=doctor.load_title_binding(binding_id),
+    )
+    return rendered
diff --git a/tests/test_align_text.py b/tests/test_align_text.py
index f5ab10b..4116dbb 100644
--- a/tests/test_align_text.py
+++ b/tests/test_align_text.py
@@ -130,6 +130,26 @@ class PureCueAlignmentTest(unittest.TestCase):
             },
         )
 
+    def test_accepts_explicit_no_change_revision(self) -> None:
+        revision = invented_revision()
+        revision["takes"] = []
+
+        aligned = align_text.build_aligned_transcript(
+            invented_transcript(),
+            revision,
+            source_bundle_sha256=SOURCE_BUNDLE_SHA,
+            revision_sha256=REVISION_SHA,
+        )
+
+        validate_contract("aligned-transcript-v1", aligned)
+        completed = next(
+            take for take in aligned["takes"] if take["status"] == "completed"
+        )
+        self.assertEqual(
+            [cue["disposition"] for cue in completed["cues"]],
+            ["original", "original"],
+        )
+
     def test_rejects_bundle_hash_and_language_mismatch(self) -> None:
         bad_hash = invented_revision()
         bad_hash["sourceBundleSha256"] = "f" * 64
diff --git a/tests/test_cli.py b/tests/test_cli.py
index 6a0834d..c93322a 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -1,4 +1,6 @@
+import contextlib
 import hashlib
+import io
 import json
 import os
 import subprocess
@@ -7,6 +9,9 @@ import tempfile
 import textwrap
 import unittest
 from pathlib import Path
+from unittest import mock
+
+from tritrack_editing_assistant import cli, run_workflow
 
 ROOT = Path(__file__).resolve().parents[1]
 
@@ -163,7 +168,7 @@ class CliSmokeTest(unittest.TestCase):
                 "align_text.py": "implemented",
                 "gemini_hybrid.py": "implemented",
                 "gemini_transcribe.mjs": "planned",
-                "multicam-sync": "planned",
+                "multicam-sync": "implemented",
             },
         )
 
@@ -217,6 +222,154 @@ class CliSmokeTest(unittest.TestCase):
         for excluded in ("provider", "upload", "prompt", "model", "retime"):
             self.assertNotIn(excluded, completed.stdout.lower())
 
+    def test_run_help_exposes_exact_immutable_local_transitions(self):
+        run = self.run_cli("run", "--help")
+        for command in ("prepare", "align", "finish", "status"):
+            self.assertIn(command, run.stdout)
+
+        prepare = self.run_cli("run", "prepare", "--help")
+        for option in (
+            "--camera-a",
+            "--camera-b",
+            "--transcribe-media",
+            "--model",
+            "--language",
+            "--profile",
+            "--binding",
+            "--event-name",
+            "--project-name",
+            "--run-id",
+            "--output",
+            "--json",
+        ):
+            self.assertIn(option, prepare.stdout)
+
+        align = self.run_cli("run", "align", "--help")
+        for option in ("--prepared", "--revision", "--output", "--json"):
+            self.assertIn(option, align.stdout)
+
+        finish = self.run_cli("run", "finish", "--help")
+        for option in (
+            "--prepared",
+            "--aligned",
+            "--workbook",
+            "--camera-a",
+            "--camera-b",
+            "--event-name",
+            "--project-name",
+            "--output",
+            "--json",
+        ):
+            self.assertIn(option, finish.stdout)
+
+        status = self.run_cli("run", "status", "--help")
+        for option in ("--run", "--json"):
+            self.assertIn(option, status.stdout)
+        for completed in (run, prepare, align, finish, status):
+            for excluded in (
+                "provider",
+                "upload",
+                "credential",
+                "overwrite",
+                "resume",
+                "release",
+            ):
+                self.assertNotIn(excluded, completed.stdout.lower())
+
+    def test_run_handlers_forward_only_public_inputs_and_print_summary(self):
+        summary = {
+            "schemaVersion": "tritrack.run-summary/v1",
+            "runId": "run-001",
+            "phase": "prepared",
+            "nextAction": "provide-revision",
+            "stages": ["doctor", "sync", "transcribe", "emit"],
+            "artifacts": {"syncMap": "a" * 64},
+        }
+        standard_output = io.StringIO()
+        with (
+            mock.patch.object(
+                run_workflow, "prepare_run", return_value=summary
+            ) as prepare,
+            contextlib.redirect_stdout(standard_output),
+        ):
+            returncode = cli.main(
+                [
+                    "run",
+                    "prepare",
+                    "--camera-a",
+                    "A-001.MP4",
+                    "--camera-b",
+                    "B-001.MP4",
+                    "--transcribe-media",
+                    "A-001.MP4",
+                    "--model",
+                    "model.bin",
+                    "--language",
+                    "en",
+                    "--profile",
+                    "uhd-2997-ndf-fcpxml-1.14",
+                    "--binding",
+                    "basic-title-v1",
+                    "--event-name",
+                    "Interview",
+                    "--project-name",
+                    "String-out",
+                    "--run-id",
+                    "run-001",
+                    "--output",
+                    "prepared-run",
+                    "--json",
+                ]
+            )
+        self.assertEqual(returncode, 0)
+        self.assertEqual(json.loads(standard_output.getvalue()), summary)
+        positional = prepare.call_args.args
+        self.assertEqual(positional[0][0].media_id, "A-001.MP4")
+        self.assertEqual(positional[1][0].media_id, "B-001.MP4")
+        self.assertEqual(positional[2], [Path("A-001.MP4")])
+        self.assertEqual(prepare.call_args.kwargs["run_id"], "run-001")
+
+    def test_run_status_and_failure_codes_are_sanitized(self):
+        summary = {
+            "schemaVersion": "tritrack.run-summary/v1",
+            "runId": "run-001",
+            "phase": "finished",
+            "nextAction": "complete",
+            "stages": ["paper", "organize", "emit"],
+            "artifacts": {"storyCut": "a" * 64},
+        }
+        standard_output = io.StringIO()
+        with (
+            mock.patch.object(run_workflow, "status_run", return_value=summary),
+            contextlib.redirect_stdout(standard_output),
+        ):
+            returncode = cli.main(["run", "status", "--run", "finished", "--json"])
+        self.assertEqual(returncode, 0)
+        self.assertEqual(json.loads(standard_output.getvalue()), summary)
+
+        cases = {
+            "TRITRACK_OUTPUT_EXISTS": 73,
+            "TRITRACK_OUTPUT_PARENT_MISSING": 74,
+            "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED": 78,
+            "TRITRACK_TRANSCRIBE_ENGINE_FAILED": 69,
+            "TRITRACK_RUN_BUNDLE_INCOMPLETE": 65,
+        }
+        for code, expected in cases.items():
+            standard_output = io.StringIO()
+            with (
+                self.subTest(code=code),
+                mock.patch.object(
+                    run_workflow, "status_run", side_effect=ValueError(code)
+                ),
+                contextlib.redirect_stdout(standard_output),
+            ):
+                returncode = cli.main(
+                    ["run", "status", "--run", "invented", "--json"]
+                )
+            self.assertEqual(returncode, expected)
+            self.assertEqual(json.loads(standard_output.getvalue()), {"error": code})
+            self.assertNotIn("Traceback", standard_output.getvalue())
+
     def test_align_cli_publishes_and_prints_only_sanitized_summary(self):
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
diff --git a/tests/test_contracts.py b/tests/test_contracts.py
index 6de88ac..ea341a2 100644
--- a/tests/test_contracts.py
+++ b/tests/test_contracts.py
@@ -192,13 +192,51 @@ VALID_CONTRACTS = {
         "toolVersion": "0.1.0a0",
         "runId": "run-001",
         "profileId": "uhd-2997-ndf-fcpxml-1.14",
+        "bindingId": "basic-title-v1",
+        "phase": "prepared",
+        "nextAction": "provide-revision",
+        "manifestChain": [],
+        "sources": [
+            {
+                "camera": "A",
+                "mediaId": "A-001.MP4",
+                "sha256": "a" * 64,
+                "transcribed": True,
+            }
+        ],
+        "artifacts": {
+            "doctorReceipt": {"fileName": "doctor.json", "sha256": "b" * 64},
+            "syncMap": {"fileName": "sync-map.json", "sha256": "c" * 64},
+            "transcriptBundle": {
+                "fileName": "transcript-bundle.json",
+                "sha256": "d" * 64,
+            },
+            "stringOut": {
+                "fileName": "string-out.fcpxml",
+                "sha256": "e" * 64,
+            },
+        },
         "stages": [
+            {
+                "name": "doctor",
+                "inputHashes": {"profile": "f" * 64},
+                "outputHashes": {"doctorReceipt": "b" * 64},
+            },
             {
                 "name": "sync",
-                "status": "completed",
-                "inputHashes": {"cameraA": "a" * 64, "cameraB": "b" * 64},
-                "receiptSha256": "c" * 64,
-            }
+                "inputHashes": {"sourceSet": "1" * 64},
+                "outputHashes": {"syncMap": "c" * 64},
+            },
+            {
+                "name": "transcribe",
+                "inputHashes": {"transcribedSources": "2" * 64},
+                "outputHashes": {"transcriptBundle": "d" * 64},
+            },
+            {
+                "name": "emit",
+                "inputHashes": {"syncMap": "c" * 64},
+                "outputHashes": {"stringOut": "e" * 64},
+            },
         ],
     },
     "provider-receipt-v1": {
@@ -327,6 +365,42 @@ class ContractValidationTest(unittest.TestCase):
             ):
                 contracts.validate_contract(name, payload)
 
+    def test_task_10_manifest_rejects_mutable_or_phase_inconsistent_state(self):
+        invalid_cases = []
+
+        mutable_stage = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        mutable_stage["stages"][0]["status"] = "running"
+        invalid_cases.append(mutable_stage)
+
+        timestamped = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        timestamped["createdAt"] = "2026-08-17T00:00:00Z"
+        invalid_cases.append(timestamped)
+
+        wrong_next_action = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        wrong_next_action["nextAction"] = "complete"
+        invalid_cases.append(wrong_next_action)
+
+        wrong_chain_length = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        wrong_chain_length["manifestChain"] = ["9" * 64]
+        invalid_cases.append(wrong_chain_length)
+
+        extra_artifact = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        extra_artifact["artifacts"]["workingCut"] = {
+            "fileName": "working-cut.json",
+            "sha256": "8" * 64,
+        }
+        invalid_cases.append(extra_artifact)
+
+        duplicate_source = copy.deepcopy(VALID_CONTRACTS["run-manifest-v1"])
+        duplicate_source["sources"].append(
+            copy.deepcopy(duplicate_source["sources"][0])
+        )
+        invalid_cases.append(duplicate_source)
+
+        for payload in invalid_cases:
+            with self.subTest(payload=payload), self.assertRaises(ValidationError):
+                contracts.validate_contract("run-manifest-v1", payload)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/tests/test_maintainer_boundary.py b/tests/test_maintainer_boundary.py
index 856c1ed..a483ccf 100644
--- a/tests/test_maintainer_boundary.py
+++ b/tests/test_maintainer_boundary.py
@@ -87,43 +87,98 @@ class MaintainerBoundaryTest(unittest.TestCase):
                 self.assertNotIn(token, text, f"{path}: leaked {token!r}")
 
     def test_maintainer_and_end_user_skills_are_distinct(self) -> None:
-        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
-        self.assertIn("name: tritrack-editing-assistant-maintainer", skill)
-        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", skill)
-        self.assertFalse((ROOT / "skills" / "tritrack-editing-assistant").exists())
+        maintainer = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
+        end_user_root = ROOT / "skills" / "tritrack-editing-assistant"
+        end_user = (end_user_root / "SKILL.md").read_text(encoding="utf-8")
+        metadata = (end_user_root / "agents" / "openai.yaml").read_text(
+            encoding="utf-8"
+        )
+        self.assertIn("name: tritrack-editing-assistant-maintainer", maintainer)
+        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", maintainer)
+        self.assertIn("name: tritrack-editing-assistant\n", end_user)
+        self.assertIn("$tritrack-editing-assistant", metadata)
+        self.assertIn('display_name: "TriTrack Editing Assistant"', metadata)
+
+        for command in (
+            "tritrack run --help",
+            "tritrack run prepare --help",
+            "tritrack run align --help",
+            "tritrack run finish --help",
+            "tritrack run status --help",
+        ):
+            self.assertIn(command, end_user)
+        for required in (
+            "text-revision human gate",
+            "paper-edit human gate",
+            "takes: []",
+            "Questions",
+            "Selections",
+            "transport, not authority",
+            "absent output directory",
+            "Keep media",
+            "strict aligned transcript",
+        ):
+            self.assertIn(required, end_user)
 
-    def test_public_status_records_task_9_and_schedules_task_10(self) -> None:
+        lowered = end_user.lower()
+        forbidden = (
+            "tritrack-editing-assistant-maintainer",
+            "task 10",
+            "standing grant",
+            "branch",
+            "release",
+            "tester",
+            "moonie",
+            "subtitle studio",
+            "/" + "users" + "/",
+            "api_key",
+            "credential",
+            "provider",
+            "upload",
+            "run_workflow",
+            ".py",
+        )
+        for token in forbidden:
+            self.assertNotIn(token, lowered)
+
+    def test_public_status_records_task_10_and_schedules_task_11(self) -> None:
         status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
         roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
         tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
         readme = (ROOT / "README.md").read_text(encoding="utf-8")
-        decision = (ROOT / "docs" / "TASK-9-DECISION.md").read_text(
+        decision = (ROOT / "docs" / "TASK-10-DECISION.md").read_text(
             encoding="utf-8"
         )
-        verification = (ROOT / "docs" / "TASK-9-VERIFICATION.md").read_text(
+        verification = (ROOT / "docs" / "TASK-10-VERIFICATION.md").read_text(
             encoding="utf-8"
         )
-        self.assertIn("Tasks 1–9", status)
+        self.assertIn("Tasks 1–10", status)
         self.assertIn("Task 6.5", status)
         self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
         self.assertLess(status.index("Task 7"), status.index("Task 8"))
         self.assertLess(status.index("Task 8"), status.index("Task 9"))
         self.assertLess(status.index("Task 9"), status.index("Task 10"))
-        self.assertIn("Task 9", roadmap)
-        self.assertLess(roadmap.index("Task 9"), roadmap.index("Task 10"))
+        self.assertLess(status.index("Task 10"), status.index("Task 11"))
+        self.assertIn("Task 10", roadmap)
+        self.assertLess(roadmap.index("Task 10"), roadmap.index("Task 11"))
         for authority in (
-            "tritrack paper export --help",
-            "tritrack paper apply --help",
-            "tritrack organize --help",
+            "tritrack run prepare --help",
+            "tritrack run align --help",
+            "tritrack run finish --help",
+            "tritrack run status --help",
         ):
             self.assertIn(authority, tooling)
         for text in (status, roadmap, tooling, readme, verification):
-            self.assertIn("Task 9", text)
-        self.assertIn("exactly four worksheets", decision)
-        self.assertIn("Grouping fixpoint", verification)
+            self.assertIn("Task 10", text)
+        self.assertIn("Selected option: A", decision)
+        self.assertIn("immutable", verification)
+        self.assertIn("story-cut.fcpxml", verification)
+        self.assertIn("tritrack-editing-assistant", verification)
         self.assertIn("no network", verification)
-        self.assertIn("Task 10", status)
-        self.assertIn("Task 10", roadmap)
+        self.assertIn("Task 11", status)
+        self.assertIn("Task 11", roadmap)
+        self.assertNotIn("`validate` and `run` remain planned", status)
+        self.assertNotIn("`tritrack run` | planned", readme)
 
     def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
         handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
diff --git a/tests/test_run_workflow.py b/tests/test_run_workflow.py
new file mode 100644
index 0000000..56c58ae
--- /dev/null
+++ b/tests/test_run_workflow.py
@@ -0,0 +1,1073 @@
+import copy
+import hashlib
+import json
+import os
+import tempfile
+import unittest
+from pathlib import Path
+from unittest import mock
+
+from openpyxl import load_workbook
+
+from tritrack_editing_assistant import (
+    align_text,
+    doctor,
+    emit_fcpxml,
+    organizer,
+    paper_edit,
+    run_workflow,
+    story_fcpxml,
+    sync_scan,
+    transcribe_takes,
+)
+
+
+def sha256(encoded: bytes) -> str:
+    return hashlib.sha256(encoded).hexdigest()
+
+
+def invented_sources() -> list[dict[str, object]]:
+    return [
+        {
+            "camera": "B",
+            "mediaId": "B-001.MP4",
+            "sha256": "b" * 64,
+            "transcribed": False,
+        },
+        {
+            "camera": "A",
+            "mediaId": "A-001.MP4",
+            "sha256": "a" * 64,
+            "transcribed": True,
+        },
+    ]
+
+
+def prepared_artifacts() -> dict[str, dict[str, str]]:
+    return {
+        "transcriptBundle": {
+            "fileName": "transcript-bundle.json",
+            "sha256": "d" * 64,
+        },
+        "doctorReceipt": {"fileName": "doctor.json", "sha256": "b" * 64},
+        "stringOut": {"fileName": "string-out.fcpxml", "sha256": "e" * 64},
+        "syncMap": {"fileName": "sync-map.json", "sha256": "c" * 64},
+    }
+
+
+def prepared_stages() -> list[dict[str, object]]:
+    return [
+        {
+            "name": "emit",
+            "inputHashes": {"syncMap": "c" * 64},
+            "outputHashes": {"stringOut": "e" * 64},
+        },
+        {
+            "name": "transcribe",
+            "inputHashes": {"sourceSet": "2" * 64},
+            "outputHashes": {"transcriptBundle": "d" * 64},
+        },
+        {
+            "name": "sync",
+            "inputHashes": {"sourceSet": "1" * 64},
+            "outputHashes": {"syncMap": "c" * 64},
+        },
+        {
+            "name": "doctor",
+            "inputHashes": {"profile": "f" * 64},
+            "outputHashes": {"doctorReceipt": "b" * 64},
+        },
+    ]
+
+
+def invented_aligned() -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.aligned-transcript/v1",
+        "alignmentProfileId": "cue-addressed-v1",
+        "sourceBundleSha256": "1" * 64,
+        "revisionSha256": "2" * 64,
+        "language": "en",
+        "takes": [
+            {
+                "takeId": "A-001.MP4",
+                "sourceSha256": "a" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 0,
+                        "endMs": 500,
+                        "text": "Invented words.",
+                        "disposition": "original",
+                    }
+                ],
+            }
+        ],
+    }
+
+
+def aligned_bundle_files() -> dict[str, bytes]:
+    aligned = (
+        json.dumps(invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True)
+        + "\n"
+    ).encode("utf-8")
+    return {
+        "aligned-transcript.json": aligned,
+        "paper-edit.xlsx": b"PK\x03\x04invented-workbook",
+    }
+
+
+def aligned_manifest(files: dict[str, bytes]) -> dict[str, object]:
+    artifacts = {
+        "alignedTranscript": {
+            "fileName": "aligned-transcript.json",
+            "sha256": sha256(files["aligned-transcript.json"]),
+        },
+        "paperWorkbook": {
+            "fileName": "paper-edit.xlsx",
+            "sha256": sha256(files["paper-edit.xlsx"]),
+        },
+    }
+    return run_workflow.build_manifest(
+        run_id="run-001",
+        profile_id="uhd-2997-ndf-fcpxml-1.14",
+        binding_id="basic-title-v1",
+        phase="aligned",
+        manifest_chain=["9" * 64],
+        sources=invented_sources(),
+        stages=[
+            {
+                "name": "paper",
+                "inputHashes": {"alignedTranscript": sha256(files["aligned-transcript.json"])},
+                "outputHashes": {"paperWorkbook": sha256(files["paper-edit.xlsx"])},
+            },
+            {
+                "name": "align",
+                "inputHashes": {"revision": "8" * 64},
+                "outputHashes": {
+                    "alignedTranscript": sha256(files["aligned-transcript.json"])
+                },
+            },
+        ],
+        artifacts=artifacts,
+    )
+
+
+class RunManifestTest(unittest.TestCase):
+    def build(self, **changes) -> dict[str, object]:
+        arguments = {
+            "run_id": "run-001",
+            "profile_id": "uhd-2997-ndf-fcpxml-1.14",
+            "binding_id": "basic-title-v1",
+            "phase": "prepared",
+            "manifest_chain": [],
+            "sources": invented_sources(),
+            "stages": prepared_stages(),
+            "artifacts": prepared_artifacts(),
+        }
+        arguments.update(changes)
+        return run_workflow.build_manifest(**arguments)
+
+    def test_builds_sorted_immutable_canonical_manifest(self) -> None:
+        sources = invented_sources()
+        stages = prepared_stages()
+        artifacts = prepared_artifacts()
+        before = copy.deepcopy((sources, stages, artifacts))
+
+        manifest = self.build(sources=sources, stages=stages, artifacts=artifacts)
+        first = run_workflow.encode_manifest(manifest)
+        second = run_workflow.encode_manifest(copy.deepcopy(manifest))
+
+        self.assertEqual((sources, stages, artifacts), before)
+        self.assertEqual(first, second)
+        self.assertTrue(first.endswith(b"\n"))
+        self.assertEqual(
+            [(source["camera"], source["mediaId"]) for source in manifest["sources"]],
+            [("A", "A-001.MP4"), ("B", "B-001.MP4")],
+        )
+        self.assertEqual(
+            [stage["name"] for stage in manifest["stages"]],
+            ["doctor", "sync", "transcribe", "emit"],
+        )
+        self.assertNotIn(b"createdAt", first)
+        self.assertNotIn(b"status", first)
+        self.assertNotIn(b"/Users/", first)
+
+    def test_rejects_unsafe_duplicate_and_phase_drift(self) -> None:
+        duplicate = invented_sources()
+        duplicate.append(
+            {
+                "camera": "B",
+                "mediaId": "A-001.MP4",
+                "sha256": "9" * 64,
+                "transcribed": False,
+            }
+        )
+        invalid = [
+            {"run_id": "../run"},
+            {"phase": "running"},
+            {"manifest_chain": ["1" * 64]},
+            {"sources": duplicate},
+        ]
+        for changes in invalid:
+            with (
+                self.subTest(changes=changes),
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_RUN_MANIFEST_INVALID"
+                ),
+            ):
+                self.build(**changes)
+
+    def test_rejects_foreign_artifact_filename_stage_and_hash(self) -> None:
+        artifacts = prepared_artifacts()
+        artifacts["syncMap"]["fileName"] = "foreign.json"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
+            self.build(artifacts=artifacts)
+
+        stages = prepared_stages()
+        stages[0]["name"] = "validate"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
+            self.build(stages=stages)
+
+    def test_rejects_extra_artifact_and_stage_facts(self) -> None:
+        artifacts = prepared_artifacts()
+        artifacts["foreign"] = {
+            "fileName": "foreign.json",
+            "sha256": "9" * 64,
+        }
+        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
+            self.build(artifacts=artifacts)
+
+        stages = prepared_stages()
+        stages.append(
+            {
+                "name": "foreign",
+                "action": "foreign",
+                "outputHashes": {"foreign": "9" * 64},
+            }
+        )
+        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
+            self.build(stages=stages)
+
+        stages = prepared_stages()
+        stages[0]["outputHashes"]["stringOut"] = "9" * 64
+        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
+            self.build(stages=stages)
+
+    def test_loads_complete_bundle_and_returns_sanitized_summary(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary) / "aligned-run"
+            root.mkdir()
+            files = aligned_bundle_files()
+            for name, encoded in files.items():
+                (root / name).write_bytes(encoded)
+            manifest = aligned_manifest(files)
+            manifest_bytes = run_workflow.encode_manifest(manifest)
+            (root / "run-manifest.json").write_bytes(manifest_bytes)
+
+            bundle = run_workflow.load_bundle(root, expected_phase="aligned")
+            summary = run_workflow.summarize_bundle(bundle)
+
+            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
+            self.assertEqual(
+                summary,
+                {
+                    "schemaVersion": "tritrack.run-summary/v1",
+                    "runId": "run-001",
+                    "phase": "aligned",
+                    "nextAction": "edit-paper-workbook",
+                    "stages": ["align", "paper"],
+                    "artifacts": {
+                        "alignedTranscript": sha256(
+                            files["aligned-transcript.json"]
+                        ),
+                        "paperWorkbook": sha256(files["paper-edit.xlsx"]),
+                    },
+                },
+            )
+            self.assertNotIn(str(root), json.dumps(summary))
+            self.assertNotIn("Invented words", json.dumps(summary))
+
+    def test_load_rejects_noncanonical_changed_unlisted_and_incomplete(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary) / "run"
+            root.mkdir()
+            files = aligned_bundle_files()
+            for name, encoded in files.items():
+                (root / name).write_bytes(encoded)
+            manifest = aligned_manifest(files)
+            (root / "run-manifest.json").write_text(
+                json.dumps(manifest, separators=(",", ":")), encoding="utf-8"
+            )
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_MANIFEST_NONCANONICAL"
+            ):
+                run_workflow.load_bundle(root)
+
+            (root / "run-manifest.json").write_bytes(
+                run_workflow.encode_manifest(manifest)
+            )
+            (root / "paper-edit.xlsx").write_bytes(b"changed")
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
+            ):
+                run_workflow.load_bundle(root)
+
+            (root / "paper-edit.xlsx").write_bytes(files["paper-edit.xlsx"])
+            (root / "foreign.txt").write_text("foreign", encoding="utf-8")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_BUNDLE_INVALID"):
+                run_workflow.load_bundle(root)
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary) / "incomplete"
+            root.mkdir()
+            (root / "aligned-transcript.json").write_text("{}", encoding="utf-8")
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
+            ):
+                run_workflow.load_bundle(root)
+
+
+class BundlePublicationTest(unittest.TestCase):
+    def builder(self, files: dict[str, bytes], calls: list[Path] | None = None):
+        def build(staging: Path) -> dict[str, object]:
+            if calls is not None:
+                calls.append(staging)
+            for name, encoded in files.items():
+                (staging / name).write_bytes(encoded)
+            return aligned_manifest(files)
+
+        return build
+
+    def test_publishes_manifest_last_and_is_deterministic(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            files = aligned_bundle_files()
+            linked: list[str] = []
+            real_link = os.link
+
+            def recording_link(source, destination):
+                linked.append(Path(destination).name)
+                return real_link(source, destination)
+
+            with mock.patch.object(
+                run_workflow.os, "link", side_effect=recording_link
+            ):
+                first = run_workflow.publish_bundle(
+                    root / "first", self.builder(files)
+                )
+            second = run_workflow.publish_bundle(root / "second", self.builder(files))
+
+            self.assertEqual(linked[-1], "run-manifest.json")
+            self.assertEqual(first.manifest, second.manifest)
+            self.assertEqual(
+                (root / "first" / "run-manifest.json").read_bytes(),
+                (root / "second" / "run-manifest.json").read_bytes(),
+            )
+            self.assertEqual(list(root.glob(".*.staging-*")), [])
+
+    def test_rejects_missing_existing_and_dangling_outputs_before_builder(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            files = aligned_bundle_files()
+            calls: list[Path] = []
+            builder = self.builder(files, calls)
+            existing = root / "existing"
+            existing.mkdir()
+            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
+                run_workflow.publish_bundle(existing, builder)
+
+            dangling = root / "dangling"
+            dangling.symlink_to(root / "missing")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
+                run_workflow.publish_bundle(dangling, builder)
+
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
+            ):
+                run_workflow.publish_bundle(root / "missing" / "run", builder)
+            self.assertEqual(calls, [])
+
+    def test_builder_and_link_failures_clean_only_owned_state(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            caller_input = root / "caller-input"
+            caller_input.write_text("keep", encoding="utf-8")
+
+            def failing_builder(staging: Path):
+                (staging / "partial").write_text("partial", encoding="utf-8")
+                raise RuntimeError("invented failure")
+
+            with self.assertRaisesRegex(RuntimeError, "invented failure"):
+                run_workflow.publish_bundle(root / "builder-failed", failing_builder)
+            self.assertFalse((root / "builder-failed").exists())
+            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")
+            self.assertEqual(list(root.glob(".*.staging-*")), [])
+
+            real_link = os.link
+            link_count = 0
+
+            def failing_link(source, destination):
+                nonlocal link_count
+                link_count += 1
+                if link_count == 2:
+                    raise OSError("invented link failure")
+                return real_link(source, destination)
+
+            with (
+                mock.patch.object(
+                    run_workflow.os, "link", side_effect=failing_link
+                ),
+                self.assertRaisesRegex(OSError, "invented link failure"),
+            ):
+                run_workflow.publish_bundle(
+                    root / "link-failed", self.builder(aligned_bundle_files())
+                )
+            self.assertFalse((root / "link-failed").exists())
+            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")
+
+    def test_directory_reservation_race_preserves_winner(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "race"
+            real_mkdir = os.mkdir
+
+            def racing_mkdir(path, mode=0o777, *, dir_fd=None):
+                if Path(path) == output:
+                    real_mkdir(path, mode)
+                    (output / "winner").write_text("keep", encoding="utf-8")
+                    raise FileExistsError
+                return real_mkdir(path, mode, dir_fd=dir_fd)
+
+            with (
+                mock.patch.object(
+                    run_workflow.os, "mkdir", side_effect=racing_mkdir
+                ),
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                run_workflow.publish_bundle(
+                    output, self.builder(aligned_bundle_files())
+                )
+            self.assertEqual((output / "winner").read_text(encoding="utf-8"), "keep")
+
+
+class PrepareAlignTransitionTest(unittest.TestCase):
+    def write_sources(
+        self, root: Path
+    ) -> tuple[list[sync_scan.MediaSource], list[sync_scan.MediaSource], Path]:
+        source_a = root / "A-001.MP4"
+        source_b = root / "B-001.MP4"
+        model = root / "ggml-model.bin"
+        source_a.write_bytes(b"invented-source-a")
+        source_b.write_bytes(b"invented-source-b")
+        model.write_bytes(b"invented-model")
+        return (
+            [sync_scan.MediaSource(source_a.name, source_a)],
+            [sync_scan.MediaSource(source_b.name, source_b)],
+            model,
+        )
+
+    @staticmethod
+    def sync_payload() -> dict[str, object]:
+        return {
+            "schemaVersion": "tritrack.sync-map/v1",
+            "profileId": "uhd-2997-ndf-fcpxml-1.14",
+            "pairs": [
+                {
+                    "pairId": "pair-001",
+                    "mediaA": "A-001.MP4",
+                    "mediaB": "B-001.MP4",
+                    "offsetBFromASeconds": 1.0,
+                    "confidence": 20.0,
+                    "overlapSeconds": 8.0,
+                    "audioMaster": "A",
+                    "durationASeconds": 10.0,
+                    "durationBSeconds": 8.0,
+                    "startedAt": None,
+                }
+            ],
+            "singleA": [],
+            "singleB": [],
+            "warnings": [],
+        }
+
+    def fakes(self, calls: list[str], *, supported: bool = True):
+        def fake_doctor(output: Path, **_arguments):
+            calls.append("doctor")
+            receipt = {
+                "schemaVersion": "tritrack.doctor-receipt/v1",
+                "profileId": "uhd-2997-ndf-fcpxml-1.14",
+                "titleBindingId": "basic-title-v1",
+                "supported": supported,
+                "checks": [],
+                "remediation": [] if supported else ["Invented remediation"],
+            }
+            output.write_text(
+                json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
+                encoding="utf-8",
+            )
+            return receipt
+
+        def fake_sync(_camera_a, _camera_b, *, output_path, **_arguments):
+            calls.append("sync")
+            payload = self.sync_payload()
+            output_path.write_text(
+                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
+                encoding="utf-8",
+            )
+            return payload
+
+        def fake_transcribe(media_paths, *, model_path, language, output_path, **_):
+            calls.append("transcribe")
+            source = Path(media_paths[0])
+            bundle = {
+                "schemaVersion": "tritrack.transcript-bundle/v1",
+                "profileId": "whisper-cpp-cpu-no-fallback-v1",
+                "language": language,
+                "modelSha256": sha256(Path(model_path).read_bytes()),
+                "engine": {
+                    "name": "whisper-cli",
+                    "version": "whisper.cpp version: invented",
+                },
+                "takes": [
+                    {
+                        "takeId": source.name,
+                        "sourceSha256": sha256(source.read_bytes()),
+                        "status": "completed",
+                        "cues": [
+                            {
+                                "cueId": "cue-000001",
+                                "startMs": 0,
+                                "endMs": 500,
+                                "text": "Invented words.",
+                            }
+                        ],
+                    }
+                ],
+            }
+            output_path.write_text(
+                transcribe_takes.encode_transcript_bundle(bundle), encoding="utf-8"
+            )
+            return bundle
+
+        def fake_emit(
+            camera_a,
+            camera_b,
+            *,
+            sync_map_path,
+            profile_id,
+            binding_id,
+            metadata,
+            output_path,
+        ):
+            calls.append("emit")
+            sources = [
+                {
+                    "camera": "A",
+                    "media_id": camera_a[0].media_id,
+                    "path": camera_a[0].path,
+                    "duration_seconds": 10.0,
+                },
+                {
+                    "camera": "B",
+                    "media_id": camera_b[0].media_id,
+                    "path": camera_b[0].path,
+                    "duration_seconds": 8.0,
+                },
+            ]
+            rendered = emit_fcpxml.render_fcpxml(
+                json.loads(Path(sync_map_path).read_text(encoding="utf-8")),
+                sources,
+                profile_id=profile_id,
+                binding_id=binding_id,
+                metadata=metadata,
+            )
+            output_path.write_text(rendered, encoding="utf-8")
+            return rendered
+
+        return fake_doctor, fake_sync, fake_transcribe, fake_emit
+
+    def prepare(
+        self, root: Path, *, calls: list[str] | None = None
+    ) -> tuple[run_workflow.LoadedRunBundle, list[sync_scan.MediaSource], Path]:
+        camera_a, camera_b, model = self.write_sources(root)
+        observed_calls = [] if calls is None else calls
+        fake_doctor, fake_sync, fake_transcribe, fake_emit = self.fakes(
+            observed_calls
+        )
+        output = root / "prepared-run"
+        with (
+            mock.patch.object(doctor, "write_receipt", side_effect=fake_doctor),
+            mock.patch.object(
+                sync_scan, "synchronize_and_publish", side_effect=fake_sync
+            ),
+            mock.patch.object(
+                transcribe_takes,
+                "transcribe_and_publish",
+                side_effect=fake_transcribe,
+            ),
+            mock.patch.object(
+                emit_fcpxml, "emit_and_publish", side_effect=fake_emit
+            ),
+        ):
+            summary = run_workflow.prepare_run(
+                camera_a,
+                camera_b,
+                [camera_a[0].path],
+                model_path=model,
+                language="en",
+                profile_id="uhd-2997-ndf-fcpxml-1.14",
+                binding_id="basic-title-v1",
+                metadata=emit_fcpxml.ProjectMetadata("Interview", "String-out"),
+                run_id="run-001",
+                output_dir=output,
+            )
+        self.assertEqual(summary["phase"], "prepared")
+        return run_workflow.load_bundle(output), [*camera_a, *camera_b], model
+
+    def test_prepare_calls_existing_engines_in_order_and_binds_sources(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            calls: list[str] = []
+            bundle, sources, model = self.prepare(root, calls=calls)
+
+            self.assertEqual(calls, ["doctor", "sync", "transcribe", "emit"])
+            self.assertEqual(bundle.manifest["phase"], "prepared")
+            self.assertEqual(
+                [source["mediaId"] for source in bundle.manifest["sources"]],
+                ["A-001.MP4", "B-001.MP4"],
+            )
+            self.assertEqual(
+                [source["transcribed"] for source in bundle.manifest["sources"]],
+                [True, False],
+            )
+            for source in sources:
+                manifest_source = next(
+                    item
+                    for item in bundle.manifest["sources"]
+                    if item["mediaId"] == source.media_id
+                )
+                self.assertEqual(
+                    manifest_source["sha256"], sha256(source.path.read_bytes())
+                )
+            encoded = bundle.manifest_bytes
+            self.assertNotIn(str(root).encode(), encoded)
+            self.assertNotIn(model.name.encode(), encoded)
+            self.assertNotIn(b"Invented words", encoded)
+
+    def test_prepare_rejects_unsupported_subset_duplicate_and_late_change(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, model = self.write_sources(root)
+            calls: list[str] = []
+            fakes = self.fakes(calls, supported=False)
+            with (
+                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
+                mock.patch.object(
+                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
+                ) as sync,
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED"
+                ),
+            ):
+                run_workflow.prepare_run(
+                    camera_a,
+                    camera_b,
+                    [camera_a[0].path],
+                    model_path=model,
+                    language="en",
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    run_id="run-unsupported",
+                    output_dir=root / "unsupported",
+                )
+            sync.assert_not_called()
+            self.assertFalse((root / "unsupported").exists())
+
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID"
+            ):
+                run_workflow.prepare_run(
+                    camera_a,
+                    camera_b,
+                    [root / "foreign.MP4"],
+                    model_path=model,
+                    language="en",
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    run_id="run-foreign",
+                    output_dir=root / "foreign",
+                )
+
+            duplicate_path = root / "other" / "A-001.MP4"
+            duplicate_path.parent.mkdir()
+            duplicate_path.write_bytes(b"duplicate")
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_SOURCE_ID_DUPLICATE"
+            ):
+                run_workflow.prepare_run(
+                    camera_a,
+                    [sync_scan.MediaSource("A-001.MP4", duplicate_path)],
+                    [camera_a[0].path],
+                    model_path=model,
+                    language="en",
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    run_id="run-duplicate",
+                    output_dir=root / "duplicate",
+                )
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, model = self.write_sources(root)
+            calls: list[str] = []
+            fakes = list(self.fakes(calls))
+            original_emit = fakes[3]
+
+            def changing_emit(*args, **kwargs):
+                rendered = original_emit(*args, **kwargs)
+                model.write_bytes(b"changed-model")
+                return rendered
+
+            with (
+                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
+                mock.patch.object(
+                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
+                ),
+                mock.patch.object(
+                    transcribe_takes,
+                    "transcribe_and_publish",
+                    side_effect=fakes[2],
+                ),
+                mock.patch.object(
+                    emit_fcpxml, "emit_and_publish", side_effect=changing_emit
+                ),
+                self.assertRaisesRegex(ValueError, "TRITRACK_RUN_INPUT_CHANGED"),
+            ):
+                run_workflow.prepare_run(
+                    camera_a,
+                    camera_b,
+                    [camera_a[0].path],
+                    model_path=model,
+                    language="en",
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    run_id="run-changed",
+                    output_dir=root / "changed",
+                )
+            self.assertFalse((root / "changed").exists())
+
+    def test_align_accepts_no_change_revision_and_chains_prepared(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            prepared, _, _ = self.prepare(root)
+            transcript = prepared.artifacts["transcriptBundle"]
+            revision = {
+                "schemaVersion": "tritrack.text-revision/v1",
+                "sourceBundleSha256": transcript.sha256,
+                "language": "en",
+                "takes": [],
+            }
+            revision_path = root / "revision.json"
+            revision_bytes = (
+                json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True)
+                + "\n"
+            ).encode("utf-8")
+            revision_path.write_bytes(revision_bytes)
+            output = root / "aligned-run"
+
+            with (
+                mock.patch.object(
+                    align_text,
+                    "align_and_publish",
+                    wraps=align_text.align_and_publish,
+                ) as align,
+                mock.patch.object(
+                    paper_edit,
+                    "export_workbook",
+                    wraps=paper_edit.export_workbook,
+                ) as paper,
+            ):
+                summary = run_workflow.align_run(
+                    prepared.root, revision_path, output_dir=output
+                )
+
+            self.assertEqual([align.call_count, paper.call_count], [1, 1])
+            self.assertEqual(summary["phase"], "aligned")
+            aligned_bundle = run_workflow.load_bundle(output)
+            self.assertEqual(
+                aligned_bundle.manifest["manifestChain"],
+                [prepared.manifest_sha256],
+            )
+            self.assertEqual(
+                aligned_bundle.manifest["sources"], prepared.manifest["sources"]
+            )
+            aligned_payload = json.loads(
+                aligned_bundle.artifacts["alignedTranscript"].encoded
+            )
+            self.assertTrue(
+                all(
+                    cue["disposition"] == "original"
+                    for take in aligned_payload["takes"]
+                    for cue in take["cues"]
+                )
+            )
+            self.assertEqual(revision_path.read_bytes(), revision_bytes)
+
+    def test_align_validates_prepared_bundle_before_revision(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            incomplete = root / "incomplete"
+            incomplete.mkdir()
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
+            ):
+                run_workflow.align_run(
+                    incomplete,
+                    root / "missing-revision.json",
+                    output_dir=root / "aligned",
+                )
+
+
+class FinishStatusTransitionTest(PrepareAlignTransitionTest):
+    def prepare_and_align(
+        self, root: Path
+    ) -> tuple[
+        run_workflow.LoadedRunBundle,
+        run_workflow.LoadedRunBundle,
+        list[sync_scan.MediaSource],
+    ]:
+        prepared, sources, _ = self.prepare(root)
+        transcript = prepared.artifacts["transcriptBundle"]
+        revision = {
+            "schemaVersion": "tritrack.text-revision/v1",
+            "sourceBundleSha256": transcript.sha256,
+            "language": "en",
+            "takes": [],
+        }
+        revision_path = root / "revision.json"
+        revision_path.write_text(
+            json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
+            encoding="utf-8",
+        )
+        aligned_path = root / "aligned-run"
+        run_workflow.align_run(
+            prepared.root, revision_path, output_dir=aligned_path
+        )
+        return prepared, run_workflow.load_bundle(aligned_path), sources
+
+    @staticmethod
+    def edit_workbook(aligned: run_workflow.LoadedRunBundle, output: Path) -> None:
+        output.write_bytes(aligned.artifacts["paperWorkbook"].encoded)
+        workbook = load_workbook(output, data_only=False)
+        workbook["Questions"].append(["question-001", "What happened?", 1])
+        workbook["Selections"].append(
+            [
+                "ANSWER",
+                "answer-001",
+                "question-001",
+                1,
+                "A-001.MP4",
+                "cue-000001",
+                "cue-000001",
+                None,
+                None,
+            ]
+        )
+        workbook.save(output)
+
+    @staticmethod
+    def probe(source: sync_scan.MediaSource) -> dict[str, object]:
+        durations = {"A-001.MP4": 10.0, "B-001.MP4": 8.0}
+        return {
+            "duration_seconds": durations[source.media_id],
+            "compatibility": {
+                "videoStreamCount": 1,
+                "audioStreamCount": 1,
+                "width": 3840,
+                "height": 2160,
+                "frameRate": "30000/1001",
+                "colorSpace": "bt709",
+                "colorTransfer": "bt709",
+                "colorPrimaries": "bt709",
+                "sampleRate": "48000",
+                "channels": 2,
+            },
+        }
+
+    def finish(
+        self,
+        root: Path,
+        prepared: run_workflow.LoadedRunBundle,
+        aligned: run_workflow.LoadedRunBundle,
+        sources: list[sync_scan.MediaSource],
+        *,
+        calls: list[str] | None = None,
+    ) -> tuple[dict[str, object], Path]:
+        workbook = root / "edited-paper.xlsx"
+        self.edit_workbook(aligned, workbook)
+        output = root / "finished-run"
+        camera_a = [source for source in sources if source.media_id.startswith("A-")]
+        camera_b = [source for source in sources if source.media_id.startswith("B-")]
+        observed = [] if calls is None else calls
+        real_apply = paper_edit.apply_workbook
+        real_organize = organizer.organize_and_publish
+        real_story = story_fcpxml.emit_story_and_publish
+
+        def apply(*args, **kwargs):
+            observed.append("paper")
+            return real_apply(*args, **kwargs)
+
+        def organize(*args, **kwargs):
+            observed.append("organize")
+            return real_organize(*args, **kwargs)
+
+        def story(*args, **kwargs):
+            observed.append("emit")
+            return real_story(*args, **kwargs)
+
+        with (
+            mock.patch.object(paper_edit, "apply_workbook", side_effect=apply),
+            mock.patch.object(
+                organizer, "organize_and_publish", side_effect=organize
+            ),
+            mock.patch.object(
+                story_fcpxml, "emit_story_and_publish", side_effect=story
+            ),
+            mock.patch.object(sync_scan, "probe_media", side_effect=self.probe),
+        ):
+            summary = run_workflow.finish_run(
+                prepared.root,
+                aligned.root,
+                workbook,
+                camera_a,
+                camera_b,
+                metadata=emit_fcpxml.ProjectMetadata("Interview", "Story cut"),
+                output_dir=output,
+            )
+        return summary, output
+
+    def test_finish_applies_organizes_emits_and_chains_exact_inputs(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            prepared, aligned, sources = self.prepare_and_align(root)
+            calls: list[str] = []
+
+            summary, output = self.finish(
+                root, prepared, aligned, sources, calls=calls
+            )
+
+            self.assertEqual(calls, ["paper", "organize", "emit"])
+            self.assertEqual(summary["phase"], "finished")
+            finished = run_workflow.load_bundle(output, expected_phase="finished")
+            self.assertEqual(
+                finished.manifest["manifestChain"],
+                [prepared.manifest_sha256, aligned.manifest_sha256],
+            )
+            self.assertEqual(
+                finished.manifest["sources"], prepared.manifest["sources"]
+            )
+            self.assertEqual(
+                set(finished.artifacts), {"grouping", "workingCut", "storyCut"}
+            )
+            self.assertNotIn("What happened?", json.dumps(summary))
+            self.assertNotIn(str(root), json.dumps(summary))
+
+    def test_finish_rejects_chain_source_and_existing_output_before_engines(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            prepared, aligned, sources = self.prepare_and_align(root)
+            workbook = root / "edited.xlsx"
+            self.edit_workbook(aligned, workbook)
+            camera_a = [sources[0]]
+            camera_b = [sources[1]]
+            existing = root / "existing"
+            existing.mkdir()
+            with (
+                mock.patch.object(paper_edit, "apply_workbook") as apply,
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                run_workflow.finish_run(
+                    prepared.root,
+                    aligned.root,
+                    workbook,
+                    camera_a,
+                    camera_b,
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    output_dir=existing,
+                )
+            apply.assert_not_called()
+
+            sources[0].path.write_bytes(b"changed-source")
+            with (
+                mock.patch.object(paper_edit, "apply_workbook") as apply,
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_RUN_SOURCE_MISMATCH"
+                ),
+            ):
+                run_workflow.finish_run(
+                    prepared.root,
+                    aligned.root,
+                    workbook,
+                    camera_a,
+                    camera_b,
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    output_dir=root / "source-mismatch",
+                )
+            apply.assert_not_called()
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            prepared, aligned, sources = self.prepare_and_align(root)
+            changed = copy.deepcopy(aligned.manifest)
+            changed["manifestChain"] = ["8" * 64]
+            (aligned.root / "run-manifest.json").write_bytes(
+                run_workflow.encode_manifest(changed)
+            )
+            workbook = root / "edited.xlsx"
+            self.edit_workbook(aligned, workbook)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_CHAIN_MISMATCH"
+            ):
+                run_workflow.finish_run(
+                    prepared.root,
+                    aligned.root,
+                    workbook,
+                    [sources[0]],
+                    [sources[1]],
+                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
+                    output_dir=root / "bad-chain",
+                )
+
+    def test_status_is_read_only_and_rejects_changed_bundle(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            prepared, aligned, sources = self.prepare_and_align(root)
+            _, output = self.finish(root, prepared, aligned, sources)
+            before = {
+                path.name: path.read_bytes() for path in output.iterdir()
+            }
+
+            summary = run_workflow.status_run(output)
+
+            self.assertEqual(summary["phase"], "finished")
+            self.assertEqual(summary["nextAction"], "complete")
+            self.assertEqual(
+                before,
+                {path.name: path.read_bytes() for path in output.iterdir()},
+            )
+            self.assertNotIn("What happened?", json.dumps(summary))
+
+            (output / "story-cut.fcpxml").write_text("changed", encoding="utf-8")
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
+            ):
+                run_workflow.status_run(output)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_story_fcpxml.py b/tests/test_story_fcpxml.py
new file mode 100644
index 0000000..61295df
--- /dev/null
+++ b/tests/test_story_fcpxml.py
@@ -0,0 +1,749 @@
+import copy
+import hashlib
+import json
+import tempfile
+import unittest
+import xml.etree.ElementTree as ET
+from decimal import Decimal
+from pathlib import Path
+from unittest import mock
+
+from tritrack_editing_assistant import (
+    doctor,
+    emit_fcpxml,
+    organizer,
+    story_fcpxml,
+    sync_scan,
+)
+
+ALIGNED_SHA = "1" * 64
+GROUPING_SHA = "2" * 64
+
+
+def invented_sync_map() -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.sync-map/v1",
+        "profileId": "uhd-2997-ndf-fcpxml-1.14",
+        "pairs": [
+            {
+                "pairId": "pair-001",
+                "mediaA": "A-001.MP4",
+                "mediaB": "B-001.MP4",
+                "offsetBFromASeconds": 1.0,
+                "confidence": 20.0,
+                "overlapSeconds": 8.0,
+                "audioMaster": "B",
+                "durationASeconds": 10.0,
+                "durationBSeconds": 8.0,
+                "startedAt": None,
+            }
+        ],
+        "singleA": ["A-002.MP4"],
+        "singleB": [],
+        "warnings": [],
+    }
+
+
+def invented_aligned() -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.aligned-transcript/v1",
+        "alignmentProfileId": "cue-addressed-v1",
+        "sourceBundleSha256": "3" * 64,
+        "revisionSha256": "4" * 64,
+        "language": "en",
+        "takes": [
+            {
+                "takeId": "A-001.MP4",
+                "sourceSha256": "a" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 1000,
+                        "endMs": 2000,
+                        "text": "First paired thought.",
+                        "disposition": "original",
+                    },
+                    {
+                        "cueId": "cue-000002",
+                        "startMs": 2000,
+                        "endMs": 3500,
+                        "text": "Second paired thought.",
+                        "disposition": "revised",
+                    },
+                ],
+            },
+            {
+                "takeId": "A-002.MP4",
+                "sourceSha256": "c" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 0,
+                        "endMs": 1000,
+                        "text": "Opening thought.",
+                        "disposition": "original",
+                    }
+                ],
+            },
+            {
+                "takeId": "B-001.MP4",
+                "sourceSha256": "b" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 4000,
+                        "endMs": 5000,
+                        "text": "Reserve thought.",
+                        "disposition": "original",
+                    }
+                ],
+            },
+        ],
+    }
+
+
+def invented_grouping() -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.grouping/v1",
+        "alignedTranscriptSha256": ALIGNED_SHA,
+        "questions": [
+            {
+                "id": "question-opening",
+                "question": "How does it begin?",
+                "order": 1,
+                "answers": [
+                    {
+                        "id": "answer-opening",
+                        "order": 1,
+                        "takeId": "A-002.MP4",
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000001",
+                    }
+                ],
+            },
+            {
+                "id": "question-detail",
+                "question": "What is the detail?",
+                "order": 2,
+                "answers": [
+                    {
+                        "id": "answer-paired",
+                        "order": 1,
+                        "takeId": "A-001.MP4",
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000002",
+                    }
+                ],
+            },
+        ],
+        "reserve": [
+            {
+                "id": "reserve-b",
+                "order": 1,
+                "takeId": "B-001.MP4",
+                "startCueId": "cue-000001",
+                "endCueId": "cue-000001",
+                "reason": "Alternate angle",
+            }
+        ],
+    }
+
+
+def invented_working_cut(
+    aligned: object, grouping: object
+) -> dict[str, object]:
+    result = organizer.build_working_cut(
+        aligned,
+        grouping,
+        aligned_sha256=ALIGNED_SHA,
+        grouping_sha256=GROUPING_SHA,
+    )
+    result["segments"].reverse()
+    return result
+
+
+def invented_sources() -> list[dict[str, object]]:
+    return [
+        {
+            "camera": "B",
+            "media_id": "B-001.MP4",
+            "path": Path("/invented/B-001.MP4"),
+            "duration_seconds": Decimal(8),
+            "sha256": "b" * 64,
+        },
+        {
+            "camera": "A",
+            "media_id": "A-002.MP4",
+            "path": Path("/invented/A-002.MP4"),
+            "duration_seconds": Decimal(6),
+            "sha256": "c" * 64,
+        },
+        {
+            "camera": "A",
+            "media_id": "A-001.MP4",
+            "path": Path("/invented/A-001.MP4"),
+            "duration_seconds": Decimal(10),
+            "sha256": "a" * 64,
+        },
+    ]
+
+
+class StoryTimelineTest(unittest.TestCase):
+    def build(
+        self,
+        *,
+        sync_map: dict[str, object] | None = None,
+        aligned: dict[str, object] | None = None,
+        grouping: dict[str, object] | None = None,
+        working_cut: dict[str, object] | None = None,
+        sources: list[dict[str, object]] | None = None,
+        aligned_sha256: str = ALIGNED_SHA,
+        grouping_sha256: str = GROUPING_SHA,
+    ) -> story_fcpxml.StoryTimeline:
+        selected_aligned = aligned or invented_aligned()
+        selected_grouping = grouping or invented_grouping()
+        selected_working_cut = working_cut or invented_working_cut(
+            selected_aligned, selected_grouping
+        )
+        return story_fcpxml.build_story_timeline(
+            sync_map or invented_sync_map(),
+            selected_aligned,
+            selected_grouping,
+            selected_working_cut,
+            sources or invented_sources(),
+            aligned_sha256=aligned_sha256,
+            grouping_sha256=grouping_sha256,
+            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
+        )
+
+    def test_builds_story_order_from_exact_authorities(self) -> None:
+        sync_map = invented_sync_map()
+        aligned = invented_aligned()
+        grouping = invented_grouping()
+        working_cut = invented_working_cut(aligned, grouping)
+        sources = invented_sources()
+        before = copy.deepcopy((sync_map, aligned, grouping, working_cut, sources))
+
+        timeline = story_fcpxml.build_story_timeline(
+            sync_map,
+            aligned,
+            grouping,
+            working_cut,
+            sources,
+            aligned_sha256=ALIGNED_SHA,
+            grouping_sha256=GROUPING_SHA,
+            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
+        )
+
+        self.assertEqual((sync_map, aligned, grouping, working_cut, sources), before)
+        self.assertEqual(timeline.profile_id, "uhd-2997-ndf-fcpxml-1.14")
+        self.assertEqual(timeline.duration_frames, 105)
+        self.assertEqual(
+            [(source.camera, source.media_id) for source in timeline.sources],
+            [("A", "A-001.MP4"), ("A", "A-002.MP4"), ("B", "B-001.MP4")],
+        )
+        self.assertEqual(
+            [segment.segment_id for segment in timeline.segments],
+            ["answer-opening", "answer-paired"],
+        )
+
+        opening, paired = timeline.segments
+        self.assertEqual(
+            (opening.offset_frames, opening.duration_frames, opening.title_text),
+            (0, 30, "Opening thought."),
+        )
+        self.assertEqual(len(opening.clips), 1)
+        self.assertTrue(opening.clips[0].audio_enabled)
+
+        self.assertEqual(
+            (paired.offset_frames, paired.duration_frames, paired.title_text),
+            (30, 75, "First paired thought. Second paired thought."),
+        )
+        self.assertEqual(
+            [
+                (
+                    clip.camera,
+                    clip.media_id,
+                    clip.offset_frames,
+                    clip.start_frames,
+                    clip.duration_frames,
+                    clip.audio_enabled,
+                )
+                for clip in paired.clips
+            ],
+            [
+                ("A", "A-001.MP4", 30, 30, 75, False),
+                ("B", "B-001.MP4", 30, 0, 75, True),
+            ],
+        )
+        self.assertNotIn("reserve-b", [segment.segment_id for segment in timeline.segments])
+
+    def test_rejects_authority_hash_and_copied_field_drift(self) -> None:
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
+            self.build(aligned_sha256="9" * 64)
+
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
+            self.build(grouping_sha256="9" * 64)
+
+        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
+        working_cut["segments"][0]["startMs"] += 1
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
+            self.build(working_cut=working_cut)
+
+        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
+        working_cut["segments"][0]["sourceSha256"] = "9" * 64
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
+            self.build(working_cut=working_cut)
+
+    def test_rejects_unknown_selection_and_nonpermutation_story_order(self) -> None:
+        grouping = invented_grouping()
+        grouping["questions"][0]["answers"][0]["takeId"] = "unknown.MP4"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
+            self.build(
+                grouping=grouping,
+                working_cut=invented_working_cut(
+                    invented_aligned(), invented_grouping()
+                ),
+            )
+
+        grouping = invented_grouping()
+        grouping["questions"][0]["answers"][0]["startCueId"] = "cue-999999"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
+            self.build(
+                grouping=grouping,
+                working_cut=invented_working_cut(
+                    invented_aligned(), invented_grouping()
+                ),
+            )
+
+        for story_order in (1, 3):
+            working_cut = invented_working_cut(
+                invented_aligned(), invented_grouping()
+            )
+            working_cut["segments"][0]["storyOrder"] = story_order
+            with (
+                self.subTest(story_order=story_order),
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"
+                ),
+            ):
+                self.build(working_cut=working_cut)
+
+    def test_rejects_source_hash_set_and_audio_master_failures(self) -> None:
+        sources = invented_sources()
+        sources[2]["sha256"] = "9" * 64
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_STORY_SOURCE_HASH_MISMATCH"
+        ):
+            self.build(sources=sources)
+
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_STORY_SOURCE_SET_INVALID"
+        ):
+            self.build(sources=invented_sources()[:-1])
+
+        sync_map = invented_sync_map()
+        sync_map["pairs"][0]["durationBSeconds"] = 2.0
+        sync_map["pairs"][0]["overlapSeconds"] = 2.0
+        sources = invented_sources()
+        sources[0]["duration_seconds"] = Decimal(2)
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_STORY_AUDIO_MASTER_COVERAGE"
+        ):
+            self.build(sync_map=sync_map, sources=sources)
+
+    def test_rejects_zero_frame_selection_and_reserve_leakage(self) -> None:
+        aligned = invented_aligned()
+        aligned["takes"][1]["cues"][0]["endMs"] = 1
+        grouping = invented_grouping()
+        working_cut = invented_working_cut(aligned, grouping)
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_SELECTION_INVALID"):
+            self.build(
+                aligned=aligned,
+                grouping=grouping,
+                working_cut=working_cut,
+            )
+
+        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
+        reserve = working_cut["reserve"][0]
+        working_cut["segments"].append(
+            {
+                "id": reserve["id"],
+                "storyOrder": 3,
+                "questionId": "question-detail",
+                "takeId": reserve["takeId"],
+                "sourceSha256": reserve["sourceSha256"],
+                "startCueId": reserve["startCueId"],
+                "endCueId": reserve["endCueId"],
+                "startMs": reserve["startMs"],
+                "endMs": reserve["endMs"],
+            }
+        )
+        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
+            self.build(working_cut=working_cut)
+
+
+class StoryRenderingTest(unittest.TestCase):
+    def timeline(self) -> story_fcpxml.StoryTimeline:
+        aligned = invented_aligned()
+        grouping = invented_grouping()
+        return story_fcpxml.build_story_timeline(
+            invented_sync_map(),
+            aligned,
+            grouping,
+            invented_working_cut(aligned, grouping),
+            invented_sources(),
+            aligned_sha256=ALIGNED_SHA,
+            grouping_sha256=GROUPING_SHA,
+            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
+        )
+
+    def test_renders_deterministic_profile_bound_story_xml(self) -> None:
+        timeline = self.timeline()
+        metadata = emit_fcpxml.ProjectMetadata("Interview & more", "Story cut")
+
+        first = story_fcpxml.render_story_fcpxml(
+            timeline,
+            profile_id="uhd-2997-ndf-fcpxml-1.14",
+            binding_id="basic-title-v1",
+            metadata=metadata,
+        )
+        second = story_fcpxml.render_story_fcpxml(
+            timeline,
+            profile_id="uhd-2997-ndf-fcpxml-1.14",
+            binding_id="basic-title-v1",
+            metadata=metadata,
+        )
+
+        self.assertEqual(first, second)
+        self.assertIn("Interview &amp; more", first)
+        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
+        binding = doctor.load_title_binding("basic-title-v1")
+        emit_fcpxml.validate_fcpxml(first, profile=profile, binding=binding)
+        root = ET.fromstring(first)
+        sequence = root.find("./library/event/project/sequence")
+        assert sequence is not None
+        self.assertEqual(sequence.attrib["duration"], "105105/30000s")
+        gaps = root.findall("./library/event/project/sequence/spine/gap")
+        self.assertEqual(
+            [gap.attrib["name"] for gap in gaps],
+            ["answer-opening", "answer-paired"],
+        )
+        self.assertEqual(
+            [gap.find("./title/text/text-style").text for gap in gaps],
+            [
+                "Opening thought.",
+                "First paired thought. Second paired thought.",
+            ],
+        )
+        paired_clips = gaps[1].findall("./asset-clip")
+        self.assertEqual(
+            [
+                (
+                    clip.attrib["name"],
+                    clip.attrib["offset"],
+                    clip.attrib["start"],
+                    clip.attrib["duration"],
+                    clip.attrib["srcEnable"],
+                )
+                for clip in paired_clips
+            ],
+            [
+                (
+                    "A-001.MP4",
+                    "30030/30000s",
+                    "30030/30000s",
+                    "75075/30000s",
+                    "video",
+                ),
+                (
+                    "B-001.MP4",
+                    "30030/30000s",
+                    "0s",
+                    "75075/30000s",
+                    "all",
+                ),
+            ],
+        )
+
+
+class StoryFileBoundaryTest(unittest.TestCase):
+    def write_inputs(
+        self, root: Path
+    ) -> tuple[
+        list[sync_scan.MediaSource],
+        list[sync_scan.MediaSource],
+        dict[str, Path],
+        dict[Path, bytes],
+    ]:
+        source_paths = {
+            "A-001.MP4": root / "A-001.MP4",
+            "A-002.MP4": root / "A-002.MP4",
+            "B-001.MP4": root / "B-001.MP4",
+        }
+        source_bytes = {
+            "A-001.MP4": b"invented-camera-a-one",
+            "A-002.MP4": b"invented-camera-a-two",
+            "B-001.MP4": b"invented-camera-b-one",
+        }
+        for media_id, path in source_paths.items():
+            path.write_bytes(source_bytes[media_id])
+
+        aligned = invented_aligned()
+        for take in aligned["takes"]:
+            take["sourceSha256"] = hashlib.sha256(
+                source_bytes[take["takeId"]]
+            ).hexdigest()
+        aligned_bytes = (
+            json.dumps(aligned, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+        ).encode("utf-8")
+        aligned_path = root / "aligned-transcript.json"
+        aligned_path.write_bytes(aligned_bytes)
+
+        grouping = invented_grouping()
+        grouping["alignedTranscriptSha256"] = hashlib.sha256(
+            aligned_bytes
+        ).hexdigest()
+        grouping_bytes = organizer.encode_grouping(grouping)
+        grouping_path = root / "grouping.json"
+        grouping_path.write_bytes(grouping_bytes)
+
+        working_cut = organizer.build_working_cut(
+            aligned,
+            grouping,
+            aligned_sha256=hashlib.sha256(aligned_bytes).hexdigest(),
+            grouping_sha256=hashlib.sha256(grouping_bytes).hexdigest(),
+        )
+        working_cut_bytes = organizer.encode_working_cut(working_cut)
+        working_cut_path = root / "working-cut.json"
+        working_cut_path.write_bytes(working_cut_bytes)
+
+        sync_bytes = (
+            json.dumps(
+                invented_sync_map(), ensure_ascii=False, indent=2, sort_keys=True
+            )
+            + "\n"
+        ).encode("utf-8")
+        sync_path = root / "sync-map.json"
+        sync_path.write_bytes(sync_bytes)
+        paths = {
+            "sync": sync_path,
+            "aligned": aligned_path,
+            "grouping": grouping_path,
+            "working": working_cut_path,
+        }
+        before = {
+            **{path: path.read_bytes() for path in source_paths.values()},
+            **{path: path.read_bytes() for path in paths.values()},
+        }
+        return (
+            [
+                sync_scan.MediaSource("A-001.MP4", source_paths["A-001.MP4"]),
+                sync_scan.MediaSource("A-002.MP4", source_paths["A-002.MP4"]),
+            ],
+            [sync_scan.MediaSource("B-001.MP4", source_paths["B-001.MP4"])],
+            paths,
+            before,
+        )
+
+    @staticmethod
+    def probe(media_id: str) -> dict[str, object]:
+        durations = {"A-001.MP4": 10.0, "A-002.MP4": 6.0, "B-001.MP4": 8.0}
+        return {
+            "duration_seconds": durations[media_id],
+            "compatibility": {
+                "videoStreamCount": 1,
+                "audioStreamCount": 1,
+                "width": 3840,
+                "height": 2160,
+                "frameRate": "30000/1001",
+                "colorSpace": "bt709",
+                "colorTransfer": "bt709",
+                "colorPrimaries": "bt709",
+                "sampleRate": "48000",
+                "channels": 2,
+            },
+        }
+
+    def emit(
+        self,
+        camera_a: list[sync_scan.MediaSource],
+        camera_b: list[sync_scan.MediaSource],
+        paths: dict[str, Path],
+        output: Path,
+    ) -> str:
+        return story_fcpxml.emit_story_and_publish(
+            camera_a,
+            camera_b,
+            sync_map_path=paths["sync"],
+            aligned_path=paths["aligned"],
+            grouping_path=paths["grouping"],
+            working_cut_path=paths["working"],
+            profile_id="uhd-2997-ndf-fcpxml-1.14",
+            binding_id="basic-title-v1",
+            metadata=emit_fcpxml.ProjectMetadata("Interview", "Story cut"),
+            output_path=output,
+        )
+
+    def test_publishes_exact_story_xml_without_mutating_inputs(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, before = self.write_inputs(root)
+            output = root / "story-cut.fcpxml"
+            with mock.patch.object(
+                sync_scan,
+                "probe_media",
+                side_effect=lambda source: self.probe(source.media_id),
+            ):
+                rendered = self.emit(camera_a, camera_b, paths, output)
+
+            self.assertEqual(output.read_text(encoding="utf-8"), rendered)
+            self.assertTrue(rendered.endswith("\n"))
+            self.assertEqual({path: path.read_bytes() for path in before}, before)
+
+    def test_existing_output_and_missing_parent_fail_before_input_reads(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "story-cut.fcpxml"
+            output.write_text("winner", encoding="utf-8")
+            missing = {
+                "sync": root / "missing-sync",
+                "aligned": root / "missing-aligned",
+                "grouping": root / "missing-grouping",
+                "working": root / "missing-working",
+            }
+            with (
+                mock.patch.object(emit_fcpxml, "probe_sources") as probe,
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                self.emit([], [], missing, output)
+            probe.assert_not_called()
+            self.assertEqual(output.read_text(encoding="utf-8"), "winner")
+
+            with (
+                mock.patch.object(emit_fcpxml, "probe_sources") as probe,
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
+                ),
+            ):
+                self.emit([], [], missing, root / "absent" / "story.fcpxml")
+            probe.assert_not_called()
+
+    def test_rejects_malformed_symlink_and_noncanonical_authorities(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            paths["sync"].write_bytes(b"not-json")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_SYNC_INVALID"):
+                self.emit(camera_a, camera_b, paths, root / "malformed.fcpxml")
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            target = root / "aligned-target.json"
+            target.write_bytes(paths["aligned"].read_bytes())
+            paths["aligned"].unlink()
+            paths["aligned"].symlink_to(target)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_STORY_ALIGNED_INVALID"
+            ):
+                self.emit(camera_a, camera_b, paths, root / "symlink.fcpxml")
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            grouping = json.loads(paths["grouping"].read_text(encoding="utf-8"))
+            paths["grouping"].write_text(
+                json.dumps(grouping, separators=(",", ":")), encoding="utf-8"
+            )
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_STORY_GROUPING_NONCANONICAL"
+            ):
+                self.emit(camera_a, camera_b, paths, root / "compact.fcpxml")
+
+    def test_late_source_mutation_is_detected_before_publication(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            mutated = False
+
+            def mutating_probe(source: sync_scan.MediaSource) -> dict[str, object]:
+                nonlocal mutated
+                result = self.probe(source.media_id)
+                if not mutated:
+                    source.path.write_bytes(b"changed-after-first-hash")
+                    mutated = True
+                return result
+
+            with (
+                mock.patch.object(
+                    sync_scan, "probe_media", side_effect=mutating_probe
+                ),
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_STORY_INPUT_CHANGED"
+                ),
+            ):
+                self.emit(camera_a, camera_b, paths, root / "changed.fcpxml")
+            self.assertFalse((root / "changed.fcpxml").exists())
+
+    def test_late_symlink_swap_is_reported_as_input_change(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            original_render = story_fcpxml.render_story_fcpxml
+            target = root / "late-target.json"
+            target.write_bytes(paths["aligned"].read_bytes())
+
+            def render_then_swap(*args, **kwargs):
+                rendered = original_render(*args, **kwargs)
+                paths["aligned"].unlink()
+                paths["aligned"].symlink_to(target)
+                return rendered
+
+            with (
+                mock.patch.object(
+                    sync_scan,
+                    "probe_media",
+                    side_effect=lambda source: self.probe(source.media_id),
+                ),
+                mock.patch.object(
+                    story_fcpxml,
+                    "render_story_fcpxml",
+                    side_effect=render_then_swap,
+                ),
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_STORY_INPUT_CHANGED"
+                ),
+            ):
+                self.emit(camera_a, camera_b, paths, root / "late.fcpxml")
+            self.assertFalse((root / "late.fcpxml").exists())
+
+    def test_publication_race_preserves_the_winner_and_cleans_temporary(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            camera_a, camera_b, paths, _ = self.write_inputs(root)
+            output = root / "race.fcpxml"
+
+            def racing_link(_temporary: Path, destination: Path) -> None:
+                Path(destination).write_text("race-winner", encoding="utf-8")
+                raise FileExistsError
+
+            with (
+                mock.patch.object(
+                    sync_scan,
+                    "probe_media",
+                    side_effect=lambda source: self.probe(source.media_id),
+                ),
+                mock.patch.object(emit_fcpxml.os, "link", side_effect=racing_link),
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                self.emit(camera_a, camera_b, paths, output)
+            self.assertEqual(output.read_text(encoding="utf-8"), "race-winner")
+            self.assertEqual(list(root.glob(".*.tmp")), [])
+
+
+if __name__ == "__main__":
+    unittest.main()

```
