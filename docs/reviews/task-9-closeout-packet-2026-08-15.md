# Task 9 Closeout Review Packet — 2026-08-15

## Frozen review target

- Repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Lane: public OSS engine
- Branch: `codex/task9-organizer-paper-edit`
- Base: `b7b6724cbdab8c724ec80e0518aaba43538773d6` (`origin/main`)
- Candidate: `6d7610182406e1e6854f6c10267d87d4b6523b08`
- Scope: Task 9 — question-grouped organizer, strict paper-edit XLSX round trip, and deterministic text-free working-cut compilation.
- Review mode: read-only, independent closeout review. Do not edit files.

## Accepted architecture and contracts

The producer accepted the paper-first compiler design with JSON authority:

- `tritrack paper export --aligned A [--grouping G] --output W [--json]`
- `tritrack paper apply --aligned A --workbook W --output G [--json]`
- `tritrack organize --aligned A --grouping G --output WC [--json]`

The workbook is a bounded transport artifact with exactly four worksheets: `Cues`, `Questions`, `Selections`, and hidden `_TriTrack`. It is not authority. Aligned JSON remains immutable timing/text authority. Grouping JSON is the editable selection/order authority. Working-cut JSON is a deterministic, text-free derivative that copies cue timing and source hashes from aligned authority.

Required safety properties include exact-byte SHA binding; canonical JSON; strict schema plus semantic validation; complete cue grid; deterministic re-derived hidden manifest; formula rejection everywhere; literal export of formula-looking transcript text; rejection of extra/missing/renamed/reordered sheets, merged cells, defined names, external links, macros, structural drift, invalid coercions, duplicate or missing rows, and cue reassignment; bounded regular non-symlink inputs; late-mutation detection; non-overwriting atomic publication with race-winner preservation; sanitized CLI summaries and stable exit behavior.

## Non-goals

No transcript editing, timing editing, ASR, media handling, render execution, package publication, app submission, release tagging, or GUI feature is in Task 9.

## Verification already completed on the frozen candidate

- Baseline before Task 9: 126 tests passed.
- Focused Task 9 final suite: 49 tests passed.
- Full source suite: 151 tests passed.
- Ruff over `src tests examples`: passed.
- `compileall` over `src tests examples`: passed.
- Repository identity check: passed.
- Maintainer skill validator: `Skill is valid!`
- `git diff --check`: passed.
- Maintainer boundary tests: 9/9 passed.
- Installed-wheel-style acceptance after `pip install . --force-reinstall --no-deps --no-build-isolation`: actual installed CLI export → apply → organize round trip passed; grouping was a fixpoint and logical workbook grids were equal after re-export.

Installed acceptance summary:

```json
{"cueCount":2,"groupingFixpoint":true,"groupingSha256":"6b6b0736391ca349ea2d3453557c58dc9facb84bbe312f7e2b5f83664ddad145","logicalGridEqual":true,"questionCount":1,"schemaVersion":"tritrack.task9-installed-acceptance/v1","segmentCount":1}
```

## Review request

Review the complete diff below for release-blocking defects and material gaps. Concentrate on:

1. Contract fidelity and schema/semantic consistency.
2. Adversarial XLSX handling: formulas, links, macros, hidden structures, merges, defined names, worksheet structure, type coercion, blank/duplicate/missing rows, and ZIP/container behavior.
3. Determinism and canonicalization, including export/apply/export fixpoint behavior.
4. Atomicity, overwrite prevention, races, TOCTOU, mutation detection, cleanup, and filesystem assumptions.
5. Working-cut timing/text authority boundaries and cue assignment/order invariants.
6. CLI exit semantics, path/privacy leakage, and installed-package resource behavior.
7. Test adequacy, documentation accuracy, and governance/boundary compliance.

Return exactly this structure:

- `VERDICT: PASS` or `VERDICT: CHANGES_REQUIRED`
- `MODEL: <exact observed model id if known, otherwise unknown>`
- `SUMMARY: <brief assessment>`
- `FINDINGS:`
  - If none, write `NO_FINDINGS`.
  - Otherwise, one finding per item with:
    - ID
    - Severity: P0, P1, P2, or P3
    - File and line
    - Evidence
    - Impact
    - Reproduction or missing test
    - Minimal fix
- `CONTRACT_COVERAGE:` checklist across the seven review dimensions above.

Do not report speculative style preferences as defects. Every finding must cite concrete code evidence and an actionable failure mode. Do not claim to have run tools or tests unless you actually did. Do not modify the repository.

## Complete frozen diff

```diff
diff --git a/README.md b/README.md
index 0867225..814cde1 100644
--- a/README.md
+++ b/README.md
@@ -1,32 +1,33 @@
 # TriTrack Editing Assistant
 
 TriTrack Editing Assistant is a local-first command-line project for building
 editable Final Cut Pro interview workflows from local A/B-camera media. It is
 designed for editors working with a terminal-capable agent while keeping story
 decisions with the editor.
 
 > Development scaffold: `0.1.0a0` currently exposes the component registry,
 > the fail-closed `doctor` command, local audio-verified `sync`, fixed-profile
 > local `transcribe`, deterministic cue-addressed `align`, offline receipt-only
-> `hybrid`, and profile-bound deterministic `emit`. Remaining editing commands are listed as
-> `planned` and deliberately return a non-success status until their
+> `hybrid`, profile-bound deterministic `emit`, strict `paper export`／
+> `paper apply`, and deterministic `organize`. Remaining editing commands are
+> listed as `planned` and deliberately return a non-success status until their
 > implementation and tests land. There is no public release yet.
 
 ## Target alpha compatibility
 
 The first alpha targets only this profile; support is not claimed until the
 profile's automated checks and invented-content Final Cut round trip pass:
 
 - macOS 26.5.2
 - Final Cut Pro 12.3
 - FCPXML 1.14
 - UHD 3840×2160 at 29.97 NDF
 - Rec. 709 and stereo 48 kHz source audio
 - Python 3.12 or newer
 
 The tool will fail closed outside declared compatibility profiles. It is not
 affiliated with, endorsed by, or sponsored by Apple Inc. Final Cut Pro is a
 trademark of Apple Inc.
 
 ## Local-first boundary
 
@@ -159,88 +160,136 @@ Validate already-produced Gemini evidence before promoting the same revision:
 
 ```bash
 venv/bin/tritrack hybrid \
   --transcript results/transcript-bundle.json \
   --proposal results/text-revision.json \
   --receipt results/provider-receipt-A-001.json \
   --model gemini-exact-model-id \
   --output results/hybrid-aligned-transcript.json \
   --json
 ```
 
 Repeat `--receipt` once per revised take. This command is an offline conformance
 adapter, not a provider client: it makes no network call and cannot create the
 receipts it consumes. Every receipt must bind the exact bundle, take, source
 audio hash, requested and observed model, completed upload and request, 2xx
 response, and attempted plus confirmed 2xx server-file deletion. It then uses
 the same local promotion core as `align`, producing byte-identical output for
 the same transcript and revision bytes. `gemini_transcribe.mjs`, live upload,
 and provider credentials remain unimplemented.
 
+Export an editor-facing workbook from the strict aligned authority:
+
+```bash
+venv/bin/tritrack paper export \
+  --aligned results/aligned-transcript.json \
+  --output results/paper-edit.xlsx \
+  --json
+```
+
+Add `--grouping results/grouping.json` to prefill a workbook from existing
+canonical editor intent. The XLSX file is a transport, not an authority. Its
+complete `Cues` reference grid and hidden public-safe manifest bind it to the
+exact aligned bytes. Formula cells, reference/display changes, unexpected
+sheets, macros, external links, merged cells, and structural drift fail closed.
+Formula-looking transcript text is exported as a literal display string.
+
+After editing only the `Questions` and `Selections` tables, apply the workbook
+back to strict JSON authority:
+
+```bash
+venv/bin/tritrack paper apply \
+  --aligned results/aligned-transcript.json \
+  --workbook results/paper-edit.xlsx \
+  --output results/grouping.json \
+  --json
+```
+
+The resulting `grouping-v1` contains cue addresses and normalized editor text,
+but no transcript text, source hash, or millisecond timing. Compile it into a
+deterministic text-free working cut with timing copied only from the exact
+aligned authority:
+
+```bash
+venv/bin/tritrack organize \
+  --aligned results/aligned-transcript.json \
+  --grouping results/grouping.json \
+  --output results/working-cut.json \
+  --json
+```
+
+All three Task 9 operations are local-only and make no network, provider,
+credential, media-processing, subprocess, FCPXML, or orchestration request.
+Every output path must be absent.
+
 ## One-minute invented quickstart
 
 After the development installation above, exercise the complete implemented
 path with deterministic invented media and one absent, ignored output root:
 
 ```bash
 venv/bin/python examples/quickstart_demo.py --output .fixture-runs
 ```
 
 The example exercises the implemented synchronization-to-emission path. It
 generates two four-second UHD 29.97 NDF Rec. 709 clips with stereo
 48 kHz invented audio, calls the installed `tritrack sync` and `tritrack emit`
 surfaces, validates the strict map and profile-bound XML, checks deterministic
 FCPXML bytes, and uses the installed FCPXML 1.14 DTD when the declared Final Cut
 application is available. It prints only a sanitized relative-path summary and
 does not upload or publish anything. The output root must be absent; choose a
 new ignored path for another run.
 
 Choose the narrowest entry point that matches your goal:
 
 1. Use the invented quickstart above to verify the implemented local path.
 2. Use `tritrack sync` then `tritrack emit` with your own local compatible
    media when you need an editable string-out.
 3. Use `tritrack transcribe` with a caller-owned local whisper.cpp model when
    you need the strict local cue bundle.
 4. Use `tritrack align` to promote a strict cue-addressed revision while
    preserving local cue timing.
 5. Use `tritrack hybrid` only to validate already-produced provider receipts
    offline before running the same local promotion.
-6. Use `tritrack components --json` to inspect what is implemented before
+6. Use `tritrack paper export` then `tritrack paper apply` to author durable
+   cue-addressed grouping intent through a non-authoritative workbook.
+7. Use `tritrack organize` to compile that intent into a deterministic
+   text-free working cut.
+8. Use `tritrack components --json` to inspect what is implemented before
    trying later roadmap commands; planned commands still fail closed.
 
 ## Eleven-component roadmap
 
 The component registry is the machine-readable source for current status:
 
 ```bash
 tritrack components --json
 ```
 
 | # | Component | Public command | Current status |
 | ---: | --- | --- | --- |
 | 1 | `sync_scan.py` | `tritrack sync` | implemented |
 | 2 | `emit_fcpxml.py` | `tritrack emit` | implemented |
 | 3 | `transcribe_takes.py` | `tritrack transcribe` | implemented |
 | 4 | `string_out.py` | `tritrack emit` | implemented |
 | 5 | `hallucination.py` | `tritrack transcribe` | implemented |
-| 6 | `organizer.py` | `tritrack organize` | planned |
-| 7 | `paper_edit.py` | `tritrack paper` | planned |
+| 6 | `organizer.py` | `tritrack organize` | implemented |
+| 7 | `paper_edit.py` | `tritrack paper` | implemented |
 | 8 | `align_text.py` | `tritrack align` | implemented |
 | 9 | `gemini_hybrid.py` | `tritrack hybrid` | implemented, offline optional |
 | 10 | `gemini_transcribe.mjs` | `tritrack hybrid` | planned, optional |
 | 11 | `multicam-sync` | `tritrack run` | planned |
 
 `components`, `doctor`, schemas, packaging, fixtures, tests, and release
 automation are supporting infrastructure and do not increase the component
 count.
 
 ## Project policies
 
 - [Contributing](CONTRIBUTING.md)
 - [Security and private-media reporting](SECURITY.md)
 - [Code of Conduct](CODE_OF_CONDUCT.md)
 - [Changelog](CHANGELOG.md)
 - [Public roadmap](docs/ROADMAP.md)
 - [Current maintenance status](STATUS.md)
 
 Licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE).
diff --git a/STATUS.md b/STATUS.md
index 9949112..6a21a71 100644
--- a/STATUS.md
+++ b/STATUS.md
@@ -1,31 +1,31 @@
 # Public maintenance status
 
 Updated: 2026-08-15
 Project kind: public engine
 Lane: `OSS`
 Release state: public pre-release source; no tag, package publication, or
 tester outreach
 
 ## Current gate
 
-Tasks 1–8 are complete in this public candidate. Task 6 began from exact
+Tasks 1–9 are complete in this public candidate. Task 6 began from exact
 Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
 fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
 rewrite or merge commit.
 
 Task 6 implements strict `sync-map-v1` loading, exact public profile and Basic
 Title binding checks, integer-frame pair alignment, deterministic pair-first
 string-out ordering, stable XML identifiers and bytes, XML escaping, source
 immutability, sync-map audio-master selection, source-profile probing, and
 race-safe absent-output FCPXML publication. The implementation retains FCPXML
 1.14, UHD 3840×2160, `1001/30000s`, NDF, Rec. 709, stereo, and 48 kHz profile
 values. Closeout-review verification after the last implementation edit passed
 67 tests and Ruff; invented temporary output also passed the declared Final Cut
 Pro 12.3 FCPXML 1.14 DTD. This is automated DTD evidence, not a claim that a
 Task 6 GUI import or round trip ran.
 
 Task 6.5 implementation candidate
 `0a99fb65979930385a6a267d596f0baa2ea5aaf3` adds one public invented-media
 quickstart from installed `sync` through installed `emit`, exact repeat-output
 determinism, strict profile／map／XML checks, conditional local DTD validation,
 minimal Python 3.12／3.13 CI, and a three-choice public entry guide without
@@ -56,59 +56,75 @@ incomplete, with no retry or fallback. Sanitized evidence is in
 
 Task 8 implementation candidate
 `4cc25b5248fe67a7cce656f0e810976f18565c16` adds strict cue-addressed
 `text-revision-v1` promotion into
 provider-neutral `aligned-transcript-v1`, exact-byte source and revision
 binding, immutable take／cue timing, input-change detection, and atomic
 no-overwrite publication. Its optional `hybrid` command validates one existing
 Gemini receipt per revised take, including exact model, bundle／take／audio
 binding, request and upload completion, and confirmed server-file deletion,
 then invokes the same local promotion core. It performs no provider request,
 upload, deletion, subprocess, credential lookup, or network access;
 `gemini_transcribe.mjs` remains planned. Sanitized evidence is in
 `docs/TASK-8-VERIFICATION.md`.
 Local verification passed 43 focused, 126 complete-suite, and 9 boundary
 tests, plus Ruff, compilation, identity, skill, installed CLI, registry, and
 diff gates.
 Gemini's dynamic-model closeout review passed with no findings, test gaps, or
 documentation gaps. The separately requested Claude subscription review timed
 out and remains explicitly incomplete, with no retry or fallback.
 
+Task 9 implementation candidate
+`f4e8074936674407e21bab2928701b4c88e6216c` tightens cue-addressed
+`grouping-v1`, adds deterministic dual-bound `working-cut-v1` compilation, and
+implements the local `paper export`, `paper apply`, and `organize` surfaces.
+The XLSX workbook is a four-worksheet editor transport, not an authority:
+apply re-derives its complete cue/display grid and public-safe manifest from
+the exact aligned bytes, rejects formulas and structural drift, normalizes
+only editor-authored text, and returns canonical grouping JSON. Task 9 never
+retimes, rewrites, splits, merges, or deletes aligned cues and performs no
+network, provider, credential, media, subprocess, FCPXML, or orchestration
+operation. Sanitized evidence is in `docs/TASK-9-VERIFICATION.md`.
+
 ## Next action
 
-Task 9 adds organizer and paper-edit round trip. It remains a separate public
-task and must not broaden Task 8 into arbitrary full-text alignment, cue
-retiming, or a live provider transport.
+Task 10 implements the installed `run` workflow and the separate end-user
+`tritrack-editing-assistant` skill. It must preserve the maintainer/end-user
+role firewall and must not turn the Task 9 workbook into transcript or timing
+authority.
 
 ## Implemented surface
 
 - clean Python package and eleven-component status registry;
 - Draft 2020-12 contracts loaded from installed package resources;
 - bounded argv-only subprocess execution and sanitized receipts;
 - audio-verified A/B synchronization with atomic `sync-map-v1` publication;
 - profile-bound deterministic string-out and atomic FCPXML 1.14 publication;
 - fixed-profile CPU-only local transcription with strict deterministic bundle
   canonicalization and atomic no-overwrite publication;
 - deterministic cue-addressed text promotion with immutable local timing and
   exact-byte provenance;
 - optional offline Gemini receipt conformance that shares the local promotion
   core and performs no network access;
+- cue-addressed grouping with deterministic working-cut compilation;
+- strict local paper-edit export/apply with complete aligned-grid
+  re-derivation, semantic round trips, and atomic no-overwrite publication;
 - fail-closed `doctor` command;
 - exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
 - public Basic Title binding with invented-content Final Cut round-trip
   evidence;
 - public invented-media synchronization-to-FCPXML quickstart with deterministic
   repeat emission, conditional local DTD verification, and minimal CI.
 
-`organize`, `paper`, `validate`, and `run` remain planned and must return
-non-success until implemented and tested. The network-capable
+`validate` and `run` remain planned and must return non-success until
+implemented and tested. The network-capable
 `gemini_transcribe.mjs` component also remains planned.
 
 ## Custody
 
 The public `origin` is
 `https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`.
 Closeout requires verifying that its `main` SHA exactly matches the local green
 candidate, making the GitHub copy the off-device Git backup. Tags, releases,
 pull requests, tester contact, package publication, and application submission
 have not yet been granted. All grants follow the standing-authorization model
 in `AGENTS.md`.
diff --git a/docs/ROADMAP.md b/docs/ROADMAP.md
index 38a38b6..71adbb8 100644
--- a/docs/ROADMAP.md
+++ b/docs/ROADMAP.md
@@ -8,40 +8,42 @@ here.
 
 - Tasks 1–4: clean-history scaffold, contracts, bounded process receipts,
   compatibility doctor, and public Basic Title evidence.
 - Task 4.5: public-native maintainer governance and the three-role skill
   boundary are complete.
 - Task 5: audio-verified A/B synchronization from the reviewed clean-room
   intake, with strict `sync-map-v1` and no-overwrite publication.
 - Task 6: profile-bound FCPXML 1.14 emission and deterministic string-out, with
   integer-frame timing, strict public profile, source-probe and binding checks,
   sync-map audio-master selection, and atomic no-overwrite publication.
 - Task 6.5: self-contained invented-media quickstart through installed
   synchronization and deterministic FCPXML emission, with minimal CI and
   public-safe readiness evidence. It remains supporting infrastructure, not a
   twelfth workflow component.
 - Task 7: fixed-profile CPU-only local whisper.cpp transcription, strict
   provider-neutral cue bundles, deterministic canonicalization and silence
   outcomes, input-change detection, and atomic no-overwrite publication.
 - Task 8: deterministic cue-addressed text promotion with immutable local
   timing, exact-byte provenance, and an isolated offline Gemini-receipt
   conformance adapter. No live provider transport is shipped.
+- Task 9: strict cue-addressed grouping, deterministic working-cut compilation,
+  and a local XLSX paper-edit round trip with complete reference-grid
+  re-derivation. The workbook is a transport; JSON remains authoritative.
 
 ## Next
 
-- Task 9: add organizer and paper-edit round trip.
 - Task 10: implement the installed `run` workflow and create the separate
   end-user `skills/tritrack-editing-assistant/SKILL.md`.
 - Task 11: expand the release-grade CI matrix and complete the privacy,
   provenance, packaging, and release gates.
 - Task 12: freeze and independently review the alpha candidate.
 - Task 13: prove the public engine as the generic authority and define a
   deliberate downstream integration seam.
 
 ## Outward-action boundary
 
 Repository publication, tags, releases, tester contact, and package
 publication are not authorized merely by completing this roadmap. Authorization
 follows the standing-authorization model in `AGENTS.md` and the public
 maintainer skill: once a capability is explicitly granted for the same target,
 visibility, scope, and risk, it remains valid until revoked and must not be
 requested again.
diff --git a/docs/TASK-9-DECISION.md b/docs/TASK-9-DECISION.md
new file mode 100644
index 0000000..83aca90
--- /dev/null
+++ b/docs/TASK-9-DECISION.md
@@ -0,0 +1,375 @@
+# Task 9 organizer and paper-edit decision
+
+Decision date: 2026-08-15
+
+Decision owner: producer
+
+Selected option: A — paper-first compiler with JSON authority
+
+## Decision
+
+Task 9 adds a local, cue-addressed paper-edit round trip and a separate
+organizer compiler. The workbook is an editor-facing transport, not an
+authority. Strict JSON artifacts remain the deterministic, versioned authority
+for editor intent and the compiled working cut.
+
+The accepted flow is:
+
+```text
+aligned-transcript-v1
+        │
+        ├── paper export ──> paper-workbook-v1.xlsx
+        │                         │
+        │                    editor changes
+        │                         │
+        └── paper apply  <────────┘
+                 │
+                 v
+            grouping-v1
+                 │
+                 └── organize ──> working-cut-v1
+```
+
+`paper export` may also consume an existing `grouping-v1` to prefill a
+workbook. This closes the round trip without requiring an editor to hand-write
+cue identifiers before a workbook exists.
+
+Task 8 remains the immutable timing and transcript authority. Task 9 does not
+retime, split, merge, delete, rewrite, or align cues. A Task 9 segment is an
+inclusive, contiguous cue span inside one completed take. Mid-cue trims and
+word-level selections remain outside the public alpha.
+
+## Public command surface
+
+Task 9 implements these exact local commands:
+
+```text
+tritrack paper export \
+  --aligned ALIGNED.json \
+  [--grouping GROUPING.json] \
+  --output PAPER.xlsx \
+  [--json]
+
+tritrack paper apply \
+  --aligned ALIGNED.json \
+  --workbook PAPER.xlsx \
+  --output GROUPING.json \
+  [--json]
+
+tritrack organize \
+  --aligned ALIGNED.json \
+  --grouping GROUPING.json \
+  --output WORKING-CUT.json \
+  [--json]
+```
+
+Nested `export` and `apply` subcommands are required because their inputs and
+outputs are disjoint. A mode flag would permit nonsensical argument
+combinations and make the help surface ambiguous.
+
+All three commands are local and network-free. They perform no provider call,
+credential lookup, media processing, subprocess invocation, transcript
+generation, FCPXML emission, or Task 10 orchestration.
+
+## `grouping-v1` editor-intent authority
+
+The existing pre-release `grouping-v1` contract is tightened in place. It has
+no implemented consumer and Task 8 established the same in-place tightening
+precedent for another unused pre-release contract. A fictitious migration to
+`grouping-v2` is therefore not introduced.
+
+The contract binds to the SHA-256 of the exact `aligned-transcript-v1` bytes and
+contains only editor intent:
+
+```json
+{
+  "schemaVersion": "tritrack.grouping/v1",
+  "alignedTranscriptSha256": "<64 lowercase hex>",
+  "questions": [
+    {
+      "id": "question-001",
+      "question": "What changed?",
+      "order": 1,
+      "answers": [
+        {
+          "id": "answer-001",
+          "order": 1,
+          "takeId": "Take-A.wav",
+          "startCueId": "cue-000001",
+          "endCueId": "cue-000003",
+          "note": "Optional editor note"
+        }
+      ]
+    }
+  ],
+  "reserve": [
+    {
+      "id": "reserve-001",
+      "order": 1,
+      "takeId": "Take-B.wav",
+      "startCueId": "cue-000004",
+      "endCueId": "cue-000004",
+      "reason": "Alternate answer",
+      "note": "Optional editor note"
+    }
+  ]
+}
+```
+
+The JSON Schema uses Draft 2020-12, rejects unknown fields, requires safe
+path-free identifiers and lowercase SHA-256 values, bounds all editor-authored
+text, and makes `note` optional. Millisecond values and transcript text do not
+appear in this intent artifact, so the editor cannot create a second timing or
+transcript authority.
+
+Semantic validation additionally requires:
+
+- the exact aligned artifact hash to match;
+- unique question, answer, and reserve IDs;
+- question orders to be the permutation `1..N`;
+- answer orders to be `1..N` inside each question;
+- reserve orders to be `1..N` globally;
+- at least one question and at least one answer per question;
+- every span to address one completed take by `(takeId, cueId)`;
+- `startCueId` through `endCueId` to be inclusive and contiguous in the take's
+  canonical cue-array order;
+- no cue to appear in more than one answer or reserve span; and
+- omitted aligned cues to remain valid and unchanged.
+
+The single-assignment rule deliberately prevents duplicated source material in
+the first public working-cut contract. Cue reuse is deferred rather than
+silently inferred.
+
+Question text, reserve reasons, and notes are NFC-normalized, have leading and
+trailing whitespace removed, collapse internal whitespace, reject control
+characters, and obey explicit length limits. Directly authored grouping JSON
+must already be canonical; `organize` validates it without rewriting it.
+
+## `working-cut-v1` compiled authority
+
+`organize` validates the exact aligned and grouping bytes, resolves every cue
+span, and publishes a new deterministic `working-cut-v1` JSON artifact. It is
+dual-bound to both exact inputs:
+
+```json
+{
+  "schemaVersion": "tritrack.working-cut/v1",
+  "organizationProfileId": "cue-addressed-question-groups-v1",
+  "alignedTranscriptSha256": "<64 lowercase hex>",
+  "groupingSha256": "<64 lowercase hex>",
+  "questions": [
+    {"id": "question-001", "question": "What changed?", "order": 1}
+  ],
+  "segments": [
+    {
+      "id": "answer-001",
+      "storyOrder": 1,
+      "questionId": "question-001",
+      "takeId": "Take-A.wav",
+      "sourceSha256": "<64 lowercase hex>",
+      "startCueId": "cue-000001",
+      "endCueId": "cue-000003",
+      "startMs": 0,
+      "endMs": 3200,
+      "note": "Optional editor note"
+    }
+  ],
+  "reserve": [
+    {
+      "id": "reserve-001",
+      "order": 1,
+      "takeId": "Take-B.wav",
+      "sourceSha256": "<64 lowercase hex>",
+      "startCueId": "cue-000004",
+      "endCueId": "cue-000004",
+      "startMs": 4500,
+      "endMs": 5200,
+      "reason": "Alternate answer",
+      "note": "Optional editor note"
+    }
+  ]
+}
+```
+
+Active `segments` are flattened in question order and then answer order;
+`storyOrder` is the derived global permutation `1..N`. Millisecond boundaries
+and source hashes are copied only from the aligned authority. Transcript text
+is not copied, preventing a second text authority. Task 10 can consume the flat
+ordered seam while reopening the exact aligned artifact for authoritative cue
+text.
+
+The same exact aligned and grouping bytes must produce byte-identical canonical
+JSON, using sorted keys and one final newline. Inputs are rehashed before atomic
+publication. Existing outputs and race winners are never overwritten.
+
+## Workbook contract
+
+`paper-workbook-v1` is an `.xlsx` transport with exactly four worksheets:
+
+### `Cues`
+
+One row per cue from completed aligned takes, ordered by canonical take order
+and cue order.
+
+| Column | Class | Apply behavior |
+| --- | --- | --- |
+| `TakeId` | identity | must exactly match the re-derived grid |
+| `SourceSha256` | identity | must exactly match the aligned take |
+| `CueId` | identity | must exactly match `(takeId, cueId)` |
+| `StartMs` | identity | must exactly match aligned timing |
+| `EndMs` | identity | must exactly match aligned timing |
+| `Text` | immutable display | must match aligned text; never imported |
+| `Disposition` | immutable display | must match aligned disposition; never imported |
+
+Full reference-grid equality detects row insertion, deletion, reordering,
+identity edits, and misleading display edits. Display columns help the editor
+make decisions but never enter JSON authority; they are compared only to the
+aligned authority. Workbook sheet protection, if present for usability, is
+never described or relied upon as a security control.
+
+### `Questions`
+
+The editor authors `QuestionId`, `Question`, and `Order`. Blank trailing rows
+are ignored. Nonblank partial rows fail closed.
+
+### `Selections`
+
+Each row describes one answer or reserve segment. Editable columns are:
+
+| Column | Required behavior |
+| --- | --- |
+| `Placement` | exact enum `ANSWER` or `RESERVE` |
+| `SegmentId` | safe unique ID |
+| `QuestionId` | required for `ANSWER`; empty for `RESERVE` |
+| `Order` | positive integer, validated in its question or reserve list |
+| `TakeId` | must address one completed aligned take |
+| `StartCueId` | inclusive start cue in the declared take |
+| `EndCueId` | inclusive end cue in the declared take |
+| `ReserveReason` | required for `RESERVE`; empty for `ANSWER` |
+| `EditorNote` | optional canonical editor text |
+
+Blank trailing rows are ignored; partially populated rows fail closed. A
+prefilled export is a direct projection of one strict grouping artifact.
+
+### `_TriTrack`
+
+The hidden manifest records only public-safe identity metadata:
+
+- workbook schema version `tritrack.paper-workbook/v1`;
+- tool version;
+- exact aligned-transcript SHA-256; and
+- SHA-256 of the canonical complete `Cues` reference grid.
+
+The hidden state is a usability aid, not a security boundary. `paper apply`
+re-derives and verifies all values from the supplied aligned artifact.
+
+## Workbook safety and failure behavior
+
+Workbook parsing uses formulas as formulas (`data_only=False`) and rejects any
+formula cell anywhere in the accepted sheets. It also rejects unexpected or
+missing sheets, merged cells, unexpected defined names, external links,
+macros, malformed cell types, duplicate IDs, duplicate or gapped ordering,
+foreign cue addresses, non-contiguous spans, overlapping assignments,
+noncanonical text, and a manifest or reference-grid mismatch.
+
+Export writes text cells explicitly as strings and uses text number formats for
+identifiers to reduce spreadsheet coercion. Formula-looking transcript text is
+display-only and must be serialized as a literal string, never as a formula.
+
+Workbook and JSON inputs have independent declared size limits, must be regular
+non-symlink files, and are hashed before and after parsing. Any change before
+publication fails closed. Workbook export and both JSON writers publish only
+to absent paths through the existing temporary-file plus hard-link race
+boundary, with cleanup after success or failure.
+
+Command summaries contain only schema version, bounded counts, and artifact
+SHA-256. They never print transcript text, question text, notes, filenames, or
+absolute paths.
+
+## Round-trip invariants
+
+XLSX byte identity is explicitly not promised. A scratch openpyxl probe on the
+selected dependency produced different ZIP bytes for two logically identical
+workbooks while all cell grids remained equal; 11 ZIP members differed.
+Formula cells loaded as formula strings with `data_only=False` and as null
+without a cached result under `data_only=True`, so apply must use the former and
+reject formulas rather than trusting cached values.
+
+Task 9 instead proves three semantic invariants:
+
+1. **Grouping fixpoint:** for every canonical grouping `G` valid against exact
+   aligned bytes `A`, `paper apply(A, paper export(A, G))` publishes bytes
+   identical to `G`.
+2. **Edited-workbook normalization:** for every human-edited workbook `W` that
+   apply accepts, if `G = paper apply(A, W)`, then repeated
+   `paper export(A, G)` operations have identical logical grids and every
+   subsequent apply publishes bytes identical to `G`.
+3. **Structural transcript immutability:** apply and organize cannot publish a
+   take, cue, source hash, or millisecond boundary not re-derived from `A`.
+
+## Error boundaries
+
+The commands retain the project's stable CLI exit classes:
+
+- malformed CLI intent returns usage;
+- invalid schema, workbook state, foreign identity, or semantic conflict
+  returns data;
+- missing or unreadable parents and file I/O failures return I/O;
+- an existing output or publication race returns output-exists; and
+- no failure prints a traceback or creates a partial output.
+
+Validation errors use stable `TRITRACK_*` prefixes. Exact codes are frozen in
+the implementation plan and tests, not invented ad hoc by individual call
+sites.
+
+## Deferred alternatives and non-goals
+
+- organize-first hand-authored JSON as the only way to bootstrap a workbook;
+- direct workbook-to-working-cut compilation with no durable grouping intent;
+- XLSX as an authoritative or byte-deterministic artifact;
+- mid-cue, word-level, or frame-level trims;
+- cue reuse in multiple story positions;
+- transcript text editing, cue retiming, merge, split, or deletion;
+- automatic semantic question classification;
+- provider calls, credentials, upload, or model selection;
+- FCPXML emission from the working cut;
+- Task 10 orchestration or end-user skill creation; and
+- tags, releases, pull requests, tester contact, package publication, or
+  application submission.
+
+## Verification target
+
+Implementation acceptance must preserve observed RED-to-GREEN evidence for:
+
+- tightened grouping and new working-cut contracts;
+- pure organizer compilation and every semantic rejection above;
+- workbook export, apply, prefill, literal formula-looking display text,
+  formula rejection, complete reference-grid re-derivation, and exact grouping
+  fixpoint;
+- logical-grid idempotence without XLSX byte claims;
+- regular-file and size boundaries, exact input hashes, late input mutation,
+  absent-output publication, races, cleanup, source immutability, and sanitized
+  summaries;
+- installed CLI help and the unchanged eleven-component registry; and
+- invented fixtures only.
+
+Closeout additionally requires focused and complete tests, Ruff, compilation,
+project identity, maintainer-skill validation, public-boundary tests,
+`git diff --check`, installed invented acceptance, convergent independent
+review with fix-forward, minimal CI, and exact public remote-main SHA backup
+verification.
+
+## Brainstorm provenance
+
+The frozen public problem packet SHA-256 was
+`992b621a93955277455b99aa9005ae4250f0727397b9ed9dfe30091e9be95727`.
+
+Codex froze its independent first round before reading other answers. Gemini
+requested, observed, and completed `gemini-3.7-flash`; its response SHA-256 was
+`c05d6967ef4ffe4a1b56f1c4cccb62ff52c397d9806700d7ee18bc9415ac26b9`.
+Claude requested the dynamic `opus` capability alias and completed with
+`claude-opus-5`; attempt `a68cdd57-889f-4cdc-8f5e-46383c8ec356` and response
+SHA-256
+`e71764b0ce60caf3503865bbce1293a171e69f8c11f5821451564895ac2a761c`
+record the exact completed lane. The producer selected option A on
+2026-08-15.
diff --git a/docs/TASK-9-VERIFICATION.md b/docs/TASK-9-VERIFICATION.md
new file mode 100644
index 0000000..543a193
--- /dev/null
+++ b/docs/TASK-9-VERIFICATION.md
@@ -0,0 +1,78 @@
+# Task 9 verification
+
+Date: 2026-08-15
+
+Candidate implementation: `f4e8074936674407e21bab2928701b4c88e6216c`
+
+## Public scope proven
+
+Task 9 implements three local-only commands:
+
+- `tritrack paper export` creates a strict four-worksheet XLSX transport from
+  exact aligned transcript bytes, optionally prefilled from canonical grouping
+  intent;
+- `tritrack paper apply` re-derives the complete cue reference grid and hidden
+  manifest before publishing canonical `grouping-v1`; and
+- `tritrack organize` compiles exact aligned and grouping bytes into a
+  deterministic, dual-bound, text-free `working-cut-v1`.
+
+The commands make no network access, provider request, credential lookup,
+media-processing call, subprocess invocation, FCPXML emission, or Task 10
+orchestration call. All tracked fixtures and tests use invented content.
+
+## Preserved RED-to-GREEN evidence
+
+- Contract RED: the tightened grouping fixture failed against the old schema
+  and `working-cut-v1` returned `TRITRACK_CONTRACT_UNKNOWN`. GREEN added the
+  strict Draft 2020-12 resources and package registry entry.
+- Organizer RED: `organizer.py` was absent. GREEN covers canonical aligned
+  indexing, exact hash binding, unique IDs, order permutations, completed-take
+  spans, single cue assignment, copied timing/source hashes, deterministic
+  bytes, late mutation, output conflicts, and hard-link races.
+- Paper export RED: `paper_edit.py` was absent. GREEN covers the exact four
+  worksheets, complete cue grid, hidden manifest, grouping projection, literal
+  formula-looking transcript display, and absent-output publication.
+- Paper apply RED: `apply_workbook()` was absent. GREEN covers formula and
+  structural rejection, complete grid/manifest re-derivation, editor-text
+  normalization, reference immutability, symlink/ZIP/input-change boundaries,
+  deterministic grouping bytes, and publication races.
+- CLI RED: `paper` had no nested commands and both Task 9 components remained
+  planned. GREEN exposes the three exact help authorities, stable exit classes,
+  sanitized summaries, and an unchanged eleven-component registry.
+
+## Semantic round trips
+
+1. **Grouping fixpoint:** applying a workbook exported from one canonical
+   grouping publishes bytes identical to that grouping.
+2. **Edited workbook normalization:** two exports from the normalized grouping
+   have identical logical cell grids even though XLSX ZIP bytes are not claimed
+   deterministic; applying either returns the same grouping bytes.
+3. **Structural transcript immutability:** grouping contains no transcript,
+   source-hash, or timing authority, and organizer copies every emitted source
+   hash and millisecond boundary only from the exact aligned artifact.
+
+## Local verification state
+
+The coherent implementation and governance package passed:
+
+- 49 focused contract, organizer, paper-edit, and CLI tests;
+- 151 complete-suite tests;
+- Ruff over `src`, `tests`, and `examples`;
+- Python compilation over `src`, `tests`, and `examples`;
+- project identity with `ok: true`, kind `public-engine`, and lane `OSS`;
+- the current Codex skill validator for the public maintainer skill; and
+- `git diff --check`.
+
+A non-editable local wheel installation exposed all three installed help
+surfaces and the unchanged eleven-component registry. One invented installed
+round trip exported two cues including literal formula-looking display text,
+normalized one question and selection into grouping, compiled one working-cut
+segment, produced equal re-exported logical grids, and returned the same
+grouping bytes from both re-applies. Its grouping SHA-256 was
+`6b6b0736391ca349ea2d3453557c58dc9facb84bbe312f7e2b5f83664ddad145`.
+
+Independent closeout review, remote CI, and exact remote-main custody are not
+claimed in this local-evidence section; they are recorded only after those
+separate gates actually complete. No Final Cut GUI import, DTD validation,
+tag, release, package publication, tester contact, or application submission
+is claimed by Task 9.
diff --git a/docs/TOOLING.md b/docs/TOOLING.md
index 78c71a4..7d37d53 100644
--- a/docs/TOOLING.md
+++ b/docs/TOOLING.md
@@ -94,40 +94,66 @@ or another project's tool state.
   artifact SHA-256.
 
 ## Offline provider conformance
 
 - `tritrack hybrid --help` is the command authority for the optional Task 8
   flags. It performs offline validation only and has no network access.
 - The caller supplies the same transcript and revision, one strict
   `provider-receipt-v1` per revised take, an exact provider model ID, and one
   absent output path. The command cannot create receipts and reads no
   credential or environment secret.
 - Every receipt must uniquely bind the exact bundle, revised take, source audio
   hash, requested and observed Gemini model, completed request and upload, 2xx
   response, and attempted plus confirmed 2xx server-file deletion. Missing,
   extra, duplicate, malformed, changed, failed, or privacy-incomplete evidence
   fails closed before publication.
 - Conformant evidence flows through the same local alignment builder and
   publisher, so local and offline-hybrid promotion are byte-identical for the
   same exact transcript and revision files. The live network-capable
   `gemini_transcribe.mjs` component remains planned.
 
+## Local paper edit and organization
+
+- `tritrack paper export --help`, `tritrack paper apply --help`, and
+  `tritrack organize --help` are the command authorities for Task 9 flags.
+- Export reads one strict `aligned-transcript-v1` and optionally one canonical
+  `grouping-v1`, then creates one absent XLSX workbook. Apply reopens the exact
+  aligned bytes and one bounded regular non-symlink workbook, re-derives every
+  cue/display/manifest value, and creates one absent canonical grouping JSON.
+- The workbook has exactly four worksheets: visible `Cues`, `Questions`, and
+  `Selections`, plus hidden `_TriTrack`. Hidden state is a usability aid, not a
+  security boundary. Formula cells anywhere in the accepted sheets fail
+  closed; formula-looking transcript text is stored as a literal string.
+- `grouping-v1` is exact-byte bound to the aligned authority and contains only
+  cue-addressed editor intent. `working-cut-v1` is exact-byte bound to both
+  aligned and grouping inputs and copies source hashes and millisecond timing
+  only from aligned cues. Neither artifact creates a second transcript
+  authority.
+- The grouping fixpoint is exact canonical JSON bytes. XLSX ZIP-byte identity
+  is not promised; repeated export instead guarantees the same logical grids,
+  and subsequent apply returns the same grouping bytes.
+- Task 9 performs no network access, provider call, credential lookup, media
+  processing, subprocess invocation, FCPXML emission, or Task 10 orchestration.
+- JSON inputs are bounded to 16 MiB and XLSX inputs to 64 MiB. Inputs are
+  rehashed before temporary-file plus hard-link publication; existing outputs
+  and race winners are never overwritten.
+
 ## Invented quickstart verification
 
 From an editable development installation, run the public Task 6.5 example
 with one caller-selected output root that does not already exist:
 
 ```bash
 venv/bin/python examples/quickstart_demo.py --output .fixture-runs
 ```
 
 The example creates all invented sources and results below that root, invokes
 the installed `tritrack components`, `tritrack sync`, and `tritrack emit`
 surfaces through bounded argv-only processes, performs a second emit to an
 absent temporary result and compares exact bytes, then removes only that
 temporary comparison. The retained output is one strict `sync-map-v1`, one
 deterministic FCPXML string-out, and the invented source pair. The output-root
 reservation and both public result writers fail closed without overwrite.
 
 The summary reports `dtdValidation: passed` only when the declared perpetual
 Final Cut FCPXML 1.14 DTD exists locally and `xmllint` accepts the output. On a
 runner without that application it reports `not-available`; this is not DTD or
diff --git a/docs/superpowers/plans/2026-08-15-task-9-organizer-paper-edit.md b/docs/superpowers/plans/2026-08-15-task-9-organizer-paper-edit.md
new file mode 100644
index 0000000..1739f7f
--- /dev/null
+++ b/docs/superpowers/plans/2026-08-15-task-9-organizer-paper-edit.md
@@ -0,0 +1,501 @@
+# Task 9 Organizer and Paper-Edit Implementation Plan
+
+> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
+
+**Goal:** Ship a deterministic, local-only round trip from strict aligned transcript bytes through an editor-facing workbook to grouping intent and a compiled working cut.
+
+**Architecture:** `organizer.py` owns the strict JSON authority: aligned indexing, grouping semantics, deterministic `working-cut-v1` compilation, and no-overwrite JSON publication. `paper_edit.py` owns the non-authoritative XLSX transport and delegates all final grouping semantics to the organizer. The CLI exposes nested `paper export`／`paper apply` commands plus `organize`, while exact hashes, absent-output publication, and sanitized summaries preserve the existing public boundaries.
+
+**Tech Stack:** Python 3.12+, `jsonschema` Draft 2020-12, `openpyxl` 3.1, `unittest`, Ruff, setuptools package resources.
+
+---
+
+## Frozen implementation details
+
+- The workbook has exactly four worksheets: visible `Cues`, `Questions`, and
+  `Selections`, plus hidden `_TriTrack`. The sentence “exactly three sheets” in
+  `docs/TASK-9-DECISION.md` is corrected because the same accepted contract
+  explicitly defines all four sheets and requires the manifest.
+- Canonical JSON is UTF-8, `ensure_ascii=False`, `indent=2`, `sort_keys=True`,
+  and one final newline.
+- JSON inputs are limited to 16 MiB; XLSX inputs are limited to 64 MiB. Inputs
+  must be nonempty regular non-symlink files and are hashed before and after
+  processing.
+- Safe editor IDs use `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$`. Question and
+  reserve-reason text is bounded to 500 characters; notes to 2,000 characters.
+- `_TriTrack` is a two-column `Key`／`Value` table containing
+  `WorkbookSchemaVersion`, `ToolVersion`, `AlignedTranscriptSha256`, and
+  `CuesGridSha256` in that order. The sheet state is `hidden`; it is not a
+  security boundary.
+- Stable data failures use these families:
+  `TRITRACK_ORGANIZER_*` for aligned／grouping semantics and compilation,
+  `TRITRACK_PAPER_*` for workbook structure and transport, and the existing
+  `TRITRACK_OUTPUT_EXISTS`／`TRITRACK_OUTPUT_PARENT_MISSING` publication codes.
+  Late mutation is `TRITRACK_ORGANIZER_INPUT_CHANGED` or
+  `TRITRACK_PAPER_INPUT_CHANGED`.
+
+### Task 1: Freeze strict Task 9 JSON contracts
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/schemas/grouping-v1.schema.json`
+- Create: `src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json`
+- Modify: `src/tritrack_editing_assistant/contracts.py`
+- Modify: `tests/test_contracts.py`
+
+- [ ] **Step 1: Write failing contract tests**
+
+Add canonical `grouping-v1` and `working-cut-v1` fixtures to
+`VALID_CONTRACTS`, then add `test_task_9_contracts_reject_invalid_state_shapes`
+covering missing exact-hash bindings, unsafe IDs, missing answer order, timing
+inside grouping, text inside working-cut segments, unknown fields, and invalid
+profile IDs.
+
+```python
+"grouping-v1": {
+    "schemaVersion": "tritrack.grouping/v1",
+    "alignedTranscriptSha256": "4" * 64,
+    "questions": [{
+        "id": "question-001", "question": "What changed?", "order": 1,
+        "answers": [{
+            "id": "answer-001", "order": 1, "takeId": "Take-A.wav",
+            "startCueId": "cue-000001", "endCueId": "cue-000002",
+        }],
+    }],
+    "reserve": [],
+},
+```
+
+- [ ] **Step 2: Run RED and preserve the expected failure**
+
+Run: `venv/bin/python -m unittest tests.test_contracts -v`
+
+Expected: FAIL because `working-cut-v1` is unknown and the old grouping schema
+does not accept the exact-byte and cue-addressed fields.
+
+- [ ] **Step 3: Tighten grouping and add working-cut schemas**
+
+Implement the exact decision shapes with `additionalProperties: false`, closed
+schema/profile constants, lowercase SHA-256 patterns, safe IDs and take IDs,
+cue-ID patterns, positive orders, text length bounds, and optional notes. Add
+`working-cut-v1` to `CONTRACT_NAMES`.
+
+- [ ] **Step 4: Run GREEN**
+
+Run: `venv/bin/python -m unittest tests.test_contracts -v`
+
+Expected: all contract tests pass.
+
+- [ ] **Step 5: Commit the contract unit**
+
+```bash
+git add src/tritrack_editing_assistant/contracts.py \
+  src/tritrack_editing_assistant/schemas/grouping-v1.schema.json \
+  src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json \
+  tests/test_contracts.py
+git commit -m "feat: define Task 9 editorial contracts"
+```
+
+### Task 2: Build the pure organizer compiler
+
+**Files:**
+- Create: `src/tritrack_editing_assistant/organizer.py`
+- Create: `tests/task9_fixtures.py`
+- Create: `tests/test_organizer.py`
+
+- [ ] **Step 1: Write the failing happy-path organizer test**
+
+Create invented aligned/grouping builders and assert that
+`build_working_cut()` leaves both inputs unchanged, copies timing/source hashes
+only from aligned cues, flattens answers by question/order, derives
+`storyOrder`, excludes transcript text, and validates `working-cut-v1`.
+
+```python
+working_cut = organizer.build_working_cut(
+    aligned,
+    grouping,
+    aligned_sha256="a" * 64,
+    grouping_sha256="b" * 64,
+)
+self.assertEqual([item["storyOrder"] for item in working_cut["segments"]], [1, 2])
+self.assertNotIn("text", json.dumps(working_cut))
+```
+
+- [ ] **Step 2: Run RED**
+
+Run: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`
+
+Expected: import failure because `organizer.py` does not exist.
+
+- [ ] **Step 3: Implement the minimal compiler core**
+
+Add these focused interfaces:
+
+```python
+ORGANIZATION_PROFILE_ID = "cue-addressed-question-groups-v1"
+
+def canonical_editor_text(value: object, *, maximum: int, required: bool) -> str | None: ...
+def index_aligned_transcript(payload: object) -> AlignedIndex: ...
+def validate_grouping(payload: object, *, aligned_index: AlignedIndex,
+                      aligned_sha256: str) -> dict[str, object]: ...
+def build_working_cut(aligned: object, grouping: object, *,
+                      aligned_sha256: str,
+                      grouping_sha256: str) -> dict[str, object]: ...
+def encode_grouping(payload: object) -> bytes: ...
+def encode_working_cut(payload: object) -> bytes: ...
+```
+
+The validator enforces canonical aligned semantics, exact binding, unique IDs,
+order permutations, completed-take cue spans, single assignment across active
+and reserve selections, and already-canonical editor text.
+
+- [ ] **Step 4: Run GREEN**
+
+Run: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`
+
+Expected: happy-path tests pass.
+
+- [ ] **Step 5: Add RED semantic rejection tests**
+
+Add separate tests for duplicate take/cue/segment IDs; unsorted or invalid
+aligned timing; noncanonical text; hash mismatch; gapped orders; empty
+questions; unknown/empty take; reversed/unknown cue spans; and cue reuse across
+answer/reserve.
+
+- [ ] **Step 6: Run RED and implement only the missing checks**
+
+Run after tests: `venv/bin/python -m unittest tests.test_organizer.PureOrganizerTest -v`
+
+Expected RED codes include `TRITRACK_ORGANIZER_ALIGNED_INVALID`,
+`TRITRACK_ORGANIZER_GROUPING_INVALID`,
+`TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH`,
+`TRITRACK_ORGANIZER_ORDER_INVALID`,
+`TRITRACK_ORGANIZER_TEXT_NONCANONICAL`,
+`TRITRACK_ORGANIZER_SPAN_INVALID`, and
+`TRITRACK_ORGANIZER_CUE_REUSED`. Implement the checks, rerun, and expect PASS.
+
+- [ ] **Step 7: Commit the pure compiler**
+
+```bash
+git add src/tritrack_editing_assistant/organizer.py \
+  tests/task9_fixtures.py tests/test_organizer.py
+git commit -m "feat: compile deterministic question-grouped cuts"
+```
+
+### Task 3: Add organizer file and CLI boundaries
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/organizer.py`
+- Modify: `src/tritrack_editing_assistant/cli.py`
+- Modify: `tests/test_organizer.py`
+- Modify: `tests/test_cli.py`
+
+- [ ] **Step 1: Write RED publication-boundary tests**
+
+Cover regular/non-symlink 16 MiB inputs, invalid UTF-8/JSON/schema, exact
+canonical grouping bytes, input hash changes, missing parent, existing output
+before input reads, hard-link race winner, temp cleanup, deterministic bytes,
+and unchanged sources.
+
+- [ ] **Step 2: Observe RED**
+
+Run: `venv/bin/python -m unittest tests.test_organizer.OrganizerFileBoundaryTest -v`
+
+Expected: failures because `organize_and_publish()` is absent.
+
+- [ ] **Step 3: Implement exact-byte loading and atomic publication**
+
+Add:
+
+```python
+def organize_and_publish(aligned_path: Path, grouping_path: Path, *,
+                         output_path: Path) -> dict[str, object]: ...
+```
+
+Reserve the absent output first, load bounded regular inputs with `O_NOFOLLOW`,
+validate and compile in memory, rehash both inputs, then write/fsync a sibling
+temporary file and hard-link it to the absent destination. Always remove the
+temporary file.
+
+- [ ] **Step 4: Run organizer boundary GREEN**
+
+Run: `venv/bin/python -m unittest tests.test_organizer -v`
+
+Expected: PASS.
+
+- [ ] **Step 5: Write RED CLI tests and implement the exact command**
+
+Assert `tritrack organize --help` exposes only `--aligned`, `--grouping`,
+`--output`, and `--json`; a successful summary contains only schema version,
+counts, and output hash; malformed data maps to 65, missing parent/input I/O to
+74, and output conflicts to 73.
+
+- [ ] **Step 6: Run CLI GREEN and commit**
+
+Run: `venv/bin/python -m unittest tests.test_cli.CliSmokeTest -v`
+
+Expected: PASS with `organizer.py` marked `implemented` while the registry
+still has exactly eleven components.
+
+```bash
+git add src/tritrack_editing_assistant/organizer.py \
+  src/tritrack_editing_assistant/cli.py tests/test_organizer.py tests/test_cli.py
+git commit -m "feat: expose atomic organizer command"
+```
+
+### Task 4: Export strict paper-edit workbooks
+
+**Files:**
+- Create: `src/tritrack_editing_assistant/paper_edit.py`
+- Create: `tests/test_paper_edit.py`
+
+- [ ] **Step 1: Write RED workbook-export tests**
+
+Assert exact four-sheet names and order, `_TriTrack.sheet_state == "hidden"`,
+exact headers, complete cue grid, correct manifest hashes, blank editor tables
+without grouping, exact grouping projection with grouping, text number formats
+for identifiers, and literal formula-looking aligned text after save/reload
+with `data_only=False`.
+
+```python
+paper_edit.export_workbook(aligned_path, grouping_path=None, output_path=output)
+book = load_workbook(output, data_only=False)
+self.assertEqual(book.sheetnames, ["Cues", "Questions", "Selections", "_TriTrack"])
+self.assertEqual(book["Cues"]["F2"].value, "=INVENTED()")
+self.assertEqual(book["Cues"]["F2"].data_type, "s")
+```
+
+- [ ] **Step 2: Observe RED**
+
+Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperExportTest -v`
+
+Expected: import failure because `paper_edit.py` does not exist.
+
+- [ ] **Step 3: Implement deterministic logical export**
+
+Add fixed headers, a canonical cue-grid hash, grouping projection, string-cell
+writing that forces `data_type="s"`, exact input verification, and atomic XLSX
+publication through a temporary file plus hard link. Do not promise ZIP-byte
+identity.
+
+- [ ] **Step 4: Run export GREEN and commit**
+
+Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperExportTest -v`
+
+Expected: PASS.
+
+```bash
+git add src/tritrack_editing_assistant/paper_edit.py tests/test_paper_edit.py
+git commit -m "feat: export strict paper-edit workbooks"
+```
+
+### Task 5: Apply workbook edits back to grouping authority
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/paper_edit.py`
+- Modify: `tests/test_paper_edit.py`
+
+- [ ] **Step 1: Write RED apply and fixpoint tests**
+
+Edit an invented workbook through openpyxl, apply it, validate the grouping,
+and assert: grouping bytes are deterministic; export(A,G) then apply(A,W)
+returns bytes identical to G; two re-exports have equal logical grids; source
+take/cue/hash/timing structure cannot enter grouping from workbook edits.
+
+- [ ] **Step 2: Observe RED**
+
+Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperApplyTest -v`
+
+Expected: failures because `apply_workbook()` is absent.
+
+- [ ] **Step 3: Implement strict workbook parsing and normalization**
+
+Add:
+
+```python
+def apply_workbook(aligned_path: Path, workbook_path: Path, *,
+                   output_path: Path) -> dict[str, object]: ...
+```
+
+Load exact XLSX bytes with `data_only=False`; reject formulas in every accepted
+sheet, missing/extra/reordered sheets, wrong headers, merged cells, defined
+names, external links, macros, invalid cell types, partial rows, duplicate IDs,
+bad orders, manifest/reference-grid drift, and invalid grouping semantics.
+Normalize workbook-authored editor text, delegate final semantic validation to
+`organizer.validate_grouping`, rehash inputs, and atomically publish canonical
+grouping JSON.
+
+- [ ] **Step 4: Run GREEN**
+
+Run: `venv/bin/python -m unittest tests.test_paper_edit.PaperApplyTest -v`
+
+Expected: PASS.
+
+- [ ] **Step 5: Add RED adversarial workbook and file-boundary tests**
+
+Cover formula cells, cached-formula ambiguity, cue insertion/deletion/reorder,
+display edits, hidden-manifest drift, partial rows, formula-looking display
+text, foreign spans, overlaps, symlinks, size limits, invalid ZIP, late
+mutation, existing output/races, cleanup, and sanitized failure messages.
+
+- [ ] **Step 6: Implement missing checks, run GREEN, and commit**
+
+Run: `venv/bin/python -m unittest tests.test_paper_edit -v`
+
+Expected: PASS with stable `TRITRACK_PAPER_*` errors and no traceback.
+
+```bash
+git add src/tritrack_editing_assistant/paper_edit.py tests/test_paper_edit.py
+git commit -m "feat: apply paper edits to grouping authority"
+```
+
+### Task 6: Expose nested paper CLI and installed round trip
+
+**Files:**
+- Modify: `src/tritrack_editing_assistant/cli.py`
+- Modify: `tests/test_cli.py`
+
+- [ ] **Step 1: Write RED nested-command and summary tests**
+
+Assert exact `paper export`／`paper apply` help, disjoint argument sets,
+sanitized summaries, exit mappings, no tracebacks, and `paper_edit.py` status
+`implemented` without changing registry length.
+
+- [ ] **Step 2: Observe RED**
+
+Run: `venv/bin/python -m unittest tests.test_cli.CliSmokeTest -v`
+
+Expected: `paper export` and `paper apply` parse/behavior failures.
+
+- [ ] **Step 3: Implement nested parsers and handlers**
+
+`paper export` accepts `--aligned`, optional `--grouping`, `--output`, and
+`--json`. `paper apply` accepts `--aligned`, `--workbook`, `--output`, and
+`--json`. Summaries include only schema version, bounded counts, and exact
+artifact hash.
+
+- [ ] **Step 4: Run GREEN and installed CLI acceptance**
+
+Run:
+
+```bash
+venv/bin/python -m unittest tests.test_cli -v
+venv/bin/pip install -e '.[dev]'
+venv/bin/tritrack paper export --help
+venv/bin/tritrack paper apply --help
+venv/bin/tritrack organize --help
+```
+
+Expected: PASS/help exit 0; help names only the frozen local flags.
+
+- [ ] **Step 5: Commit the CLI unit**
+
+```bash
+git add src/tritrack_editing_assistant/cli.py tests/test_cli.py
+git commit -m "feat: expose paper-edit round trip"
+```
+
+### Task 7: Document and verify the coherent Task 9 package
+
+**Files:**
+- Modify: `docs/TASK-9-DECISION.md`
+- Modify: `README.md`
+- Modify: `docs/TOOLING.md`
+- Modify: `docs/ROADMAP.md`
+- Modify: `STATUS.md`
+- Modify: `tests/test_maintainer_boundary.py`
+- Create: `docs/TASK-9-VERIFICATION.md`
+
+- [ ] **Step 1: Write RED governance assertions**
+
+Update boundary tests to require implemented Task 9 status, the three exact
+help authorities, local/network-free wording, round-trip invariants, sanitized
+evidence, and Task 10 as the next gate.
+
+- [ ] **Step 2: Observe RED**
+
+Run: `venv/bin/python -m unittest tests.test_maintainer_boundary -v`
+
+Expected: FAIL against Task 8-era status/docs.
+
+- [ ] **Step 3: Update public documentation without release claims**
+
+Correct the workbook sheet-count typo, document the three commands, strict
+JSON authority, XLSX non-authority, exact-hash/no-overwrite boundaries, and
+Task 10 deferrals. Record only invented and reproducible verification in
+`docs/TASK-9-VERIFICATION.md`.
+
+- [ ] **Step 4: Run focused, full, lint, compile, identity, skill, and diff gates**
+
+```bash
+venv/bin/python -m unittest tests.test_contracts tests.test_organizer tests.test_paper_edit tests.test_cli -v
+venv/bin/python -m unittest discover -s tests -v
+venv/bin/ruff check src tests examples
+venv/bin/python -m compileall -q src tests examples
+python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
+venv/bin/python -m unittest tests.test_maintainer_boundary -v
+git diff --check
+```
+
+Expected: every command passes; identity reports `ok: true`, `public-engine`,
+and `OSS`.
+
+- [ ] **Step 5: Commit the green documentation package**
+
+```bash
+git add docs/TASK-9-DECISION.md README.md docs/TOOLING.md docs/ROADMAP.md \
+  STATUS.md tests/test_maintainer_boundary.py docs/TASK-9-VERIFICATION.md
+git commit -m "docs: record Task 9 verification"
+```
+
+### Task 8: Independent closeout, fix-forward, CI, and custody
+
+**Files:**
+- Create or modify only sanitized `docs/reviews/task-9-*` artifacts required by
+  the repository collaboration contract.
+- Modify Task 9-owned code/tests/docs only for ordinary in-scope review fixes.
+
+- [ ] **Step 1: Freeze the review packet**
+
+Read the repository collaboration/tooling contract, record candidate SHA,
+changed-file list, focused/full/lint/boundary results, and ask independent
+reviewers to check contract fidelity, workbook adversarial safety, privacy,
+determinism, and test gaps.
+
+- [ ] **Step 2: Run convergent independent review**
+
+Use the approved Claude subscription-only and dynamically resolved Gemini
+lanes. Record requested, observed, and completed model IDs and preserve any
+incomplete lane truthfully.
+
+- [ ] **Step 3: Fix-forward ordinary findings with RED/GREEN evidence**
+
+For every accepted behavior finding, add a failing regression test, observe
+the expected failure, implement the minimal fix, and rerun focused plus full
+gates. Update verification evidence only after the last implementation edit.
+
+- [ ] **Step 4: Fast-forward and push under the standing grant**
+
+After all local gates and review are green, fast-forward local `main` to the
+Task 9 candidate, push `main` to the existing public `origin`, and verify
+`origin/main`, remote API SHA, and local `main` are exactly identical. Do not
+create a tag, release, pull request, tester contact, package publication, or
+application submission.
+
+- [ ] **Step 5: Verify minimal CI at the exact public candidate**
+
+Confirm the GitHub Actions Python 3.12/3.13 matrix passes at the exact pushed
+SHA. Record the run ID and distinguish Linux automated evidence from Final Cut
+GUI/DTD claims.
+
+## Self-review result
+
+- Spec coverage: every accepted Task 9 command, JSON contract, workbook sheet,
+  semantic rejection, round-trip invariant, file/race boundary, CLI summary,
+  documentation gate, independent review, CI gate, and custody gate maps to a
+  task above.
+- Placeholder scan: no implementation step contains `TBD`, `TODO`, or an
+  unfrozen product choice.
+- Type consistency: all later tasks use `alignedTranscriptSha256`,
+  `groupingSha256`, `organizationProfileId`, `startCueId`, and `endCueId` with
+  the exact decision names; workbook headers and CLI flags are frozen once and
+  reused unchanged.
diff --git a/src/tritrack_editing_assistant/cli.py b/src/tritrack_editing_assistant/cli.py
index 6d09a17..6c9151f 100644
--- a/src/tritrack_editing_assistant/cli.py
+++ b/src/tritrack_editing_assistant/cli.py
@@ -1,76 +1,86 @@
 """Command-line boundary for the TriTrack Editing Assistant scaffold."""
 
 from __future__ import annotations
 
 import argparse
 import hashlib
 import json
 from collections.abc import Sequence
 from pathlib import Path
 
 from . import __version__
 from . import align_text as align_module
 from . import doctor as doctor_module
 from . import emit_fcpxml as emit_module
 from . import gemini_hybrid as hybrid_module
+from . import organizer as organizer_module
+from . import paper_edit as paper_module
 from . import sync_scan as sync_module
 from . import transcribe_takes as transcribe_module
 
 EXIT_OK = 0
 EXIT_USAGE = 64
 EXIT_DATA = 65
 EXIT_DEPENDENCY = 69
 EXIT_OUTPUT_EXISTS = 73
 EXIT_IO = 74
 EXIT_TEMPORARY = 75
 EXIT_POLICY = 78
 
 
 COMPONENTS = (
     {
         "sourceComponent": "sync_scan.py",
         "command": "sync",
         "status": "implemented",
     },
     {
         "sourceComponent": "emit_fcpxml.py",
         "command": "emit",
         "status": "implemented",
     },
     {
         "sourceComponent": "transcribe_takes.py",
         "command": "transcribe",
         "status": "implemented",
     },
     {
         "sourceComponent": "string_out.py",
         "command": "emit",
         "status": "implemented",
     },
     {
         "sourceComponent": "hallucination.py",
         "command": "transcribe",
         "status": "implemented",
     },
-    {"sourceComponent": "organizer.py", "command": "organize", "status": "planned"},
-    {"sourceComponent": "paper_edit.py", "command": "paper", "status": "planned"},
+    {
+        "sourceComponent": "organizer.py",
+        "command": "organize",
+        "status": "implemented",
+    },
+    {
+        "sourceComponent": "paper_edit.py",
+        "command": "paper",
+        "status": "implemented",
+    },
     {
         "sourceComponent": "align_text.py",
         "command": "align",
         "status": "implemented",
     },
     {
         "sourceComponent": "gemini_hybrid.py",
         "command": "hybrid",
         "status": "implemented",
     },
     {
         "sourceComponent": "gemini_transcribe.mjs",
         "command": "hybrid",
         "status": "planned",
     },
     {"sourceComponent": "multicam-sync", "command": "run", "status": "planned"},
 )
 
 
 def _print_components(arguments: argparse.Namespace) -> int:
@@ -304,40 +314,164 @@ def _run_hybrid(arguments: argparse.Namespace) -> int:
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code == "TRITRACK_OUTPUT_PARENT_MISSING":
             return EXIT_IO
         if code == "TRITRACK_HYBRID_MODEL_INVALID":
             return EXIT_USAGE
         return EXIT_DATA
 
     if arguments.json:
         print(
             json.dumps(
                 _alignment_summary(payload, arguments.output),
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK
 
 
+def _run_organize(arguments: argparse.Namespace) -> int:
+    try:
+        payload = organizer_module.organize_and_publish(
+            arguments.aligned,
+            arguments.grouping,
+            output_path=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        if code == "TRITRACK_OUTPUT_EXISTS":
+            return EXIT_OUTPUT_EXISTS
+        if code in {
+            "TRITRACK_OUTPUT_PARENT_MISSING",
+            "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
+        }:
+            return EXIT_IO
+        return EXIT_DATA
+
+    if arguments.json:
+        questions = payload["questions"]
+        segments = payload["segments"]
+        reserve = payload["reserve"]
+        assert isinstance(questions, list)
+        assert isinstance(segments, list)
+        assert isinstance(reserve, list)
+        with arguments.output.open("rb") as stream:
+            artifact_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
+        print(
+            json.dumps(
+                {
+                    "schemaVersion": "tritrack.organize-summary/v1",
+                    "questionCount": len(questions),
+                    "segmentCount": len(segments),
+                    "reserveCount": len(reserve),
+                    "artifactSha256": artifact_sha256,
+                },
+                ensure_ascii=False,
+                indent=2,
+            )
+        )
+    return EXIT_OK
+
+
+def _paper_error_exit(code: str) -> int:
+    if code == "TRITRACK_OUTPUT_EXISTS":
+        return EXIT_OUTPUT_EXISTS
+    if code in {
+        "TRITRACK_OUTPUT_PARENT_MISSING",
+        "TRITRACK_PAPER_INPUT_UNREADABLE",
+    }:
+        return EXIT_IO
+    return EXIT_DATA
+
+
+def _output_sha256(output_path: Path) -> str:
+    with output_path.open("rb") as stream:
+        return hashlib.file_digest(stream, "sha256").hexdigest()
+
+
+def _run_paper_export(arguments: argparse.Namespace) -> int:
+    try:
+        summary = paper_module.export_workbook(
+            arguments.aligned,
+            grouping_path=arguments.grouping,
+            output_path=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _paper_error_exit(code)
+    if arguments.json:
+        print(
+            json.dumps(
+                {
+                    "schemaVersion": "tritrack.paper-export-summary/v1",
+                    **summary,
+                    "artifactSha256": _output_sha256(arguments.output),
+                },
+                ensure_ascii=False,
+                indent=2,
+            )
+        )
+    return EXIT_OK
+
+
+def _run_paper_apply(arguments: argparse.Namespace) -> int:
+    try:
+        grouping = paper_module.apply_workbook(
+            arguments.aligned,
+            arguments.workbook,
+            output_path=arguments.output,
+        )
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _paper_error_exit(code)
+    if arguments.json:
+        questions = grouping["questions"]
+        reserve = grouping["reserve"]
+        assert isinstance(questions, list)
+        assert isinstance(reserve, list)
+        answer_count = 0
+        for question in questions:
+            assert isinstance(question, dict)
+            answers = question["answers"]
+            assert isinstance(answers, list)
+            answer_count += len(answers)
+        print(
+            json.dumps(
+                {
+                    "schemaVersion": "tritrack.paper-apply-summary/v1",
+                    "questionCount": len(questions),
+                    "answerCount": answer_count,
+                    "reserveCount": len(reserve),
+                    "artifactSha256": _output_sha256(arguments.output),
+                },
+                ensure_ascii=False,
+                indent=2,
+            )
+        )
+    return EXIT_OK
+
+
 def build_parser() -> argparse.ArgumentParser:
     parser = argparse.ArgumentParser(
         prog="tritrack",
         description="Local-first Final Cut editing-assistant workflow",
     )
     parser.add_argument(
         "--version",
         action="version",
         version=f"%(prog)s {__version__}",
     )
     subparsers = parser.add_subparsers(dest="command", required=True)
 
     components = subparsers.add_parser(
         "components",
         help="list the eleven workflow components and current status",
     )
     components.add_argument("--json", action="store_true", help="emit JSON")
     components.set_defaults(handler=_print_components)
 
     doctor = subparsers.add_parser(
@@ -508,40 +642,132 @@ def build_parser() -> argparse.ArgumentParser:
         help="strict provider-receipt-v1 path; repeat per revised take",
     )
     hybrid.add_argument(
         "--model",
         required=True,
         help="exact provider model recorded in every receipt",
     )
     hybrid.add_argument(
         "--output",
         required=True,
         type=Path,
         help="create an absent aligned-transcript-v1 JSON path",
     )
     hybrid.add_argument(
         "--json",
         action="store_true",
         help="print only a sanitized completion summary",
     )
     hybrid.set_defaults(handler=_run_hybrid)
 
+    organize = subparsers.add_parser(
+        "organize",
+        help="compile cue-addressed grouping into a working cut",
+    )
+    organize.add_argument(
+        "--aligned",
+        required=True,
+        type=Path,
+        help="strict aligned-transcript-v1 JSON path",
+    )
+    organize.add_argument(
+        "--grouping",
+        required=True,
+        type=Path,
+        help="strict grouping-v1 JSON path",
+    )
+    organize.add_argument(
+        "--output",
+        required=True,
+        type=Path,
+        help="create an absent working-cut-v1 JSON path",
+    )
+    organize.add_argument(
+        "--json",
+        action="store_true",
+        help="print only a sanitized completion summary",
+    )
+    organize.set_defaults(handler=_run_organize)
+
+    paper = subparsers.add_parser(
+        "paper",
+        help="export or apply a cue-addressed paper-edit workbook",
+    )
+    paper_subparsers = paper.add_subparsers(
+        dest="paper_command",
+        required=True,
+    )
+    paper_export = paper_subparsers.add_parser(
+        "export",
+        help="export an editor-facing workbook",
+    )
+    paper_export.add_argument(
+        "--aligned",
+        required=True,
+        type=Path,
+        help="strict aligned-transcript-v1 JSON path",
+    )
+    paper_export.add_argument(
+        "--grouping",
+        type=Path,
+        help="optional strict grouping-v1 JSON path to prefill",
+    )
+    paper_export.add_argument(
+        "--output",
+        required=True,
+        type=Path,
+        help="create an absent paper-workbook-v1 XLSX path",
+    )
+    paper_export.add_argument(
+        "--json",
+        action="store_true",
+        help="print only a sanitized completion summary",
+    )
+    paper_export.set_defaults(handler=_run_paper_export)
+
+    paper_apply = paper_subparsers.add_parser(
+        "apply",
+        help="apply a strict workbook to grouping authority",
+    )
+    paper_apply.add_argument(
+        "--aligned",
+        required=True,
+        type=Path,
+        help="strict aligned-transcript-v1 JSON path",
+    )
+    paper_apply.add_argument(
+        "--workbook",
+        required=True,
+        type=Path,
+        help="strict paper-workbook-v1 XLSX path",
+    )
+    paper_apply.add_argument(
+        "--output",
+        required=True,
+        type=Path,
+        help="create an absent grouping-v1 JSON path",
+    )
+    paper_apply.add_argument(
+        "--json",
+        action="store_true",
+        help="print only a sanitized completion summary",
+    )
+    paper_apply.set_defaults(handler=_run_paper_apply)
+
     planned_commands = {
         "validate": "validate generated output",
-        "organize": "build a validated question-grouped working cut",
-        "paper": "export or apply a paper-edit workbook",
         "run": "orchestrate the complete local workflow",
     }
     for name, help_text in planned_commands.items():
         command_parser = subparsers.add_parser(name, help=help_text)
         command_parser.set_defaults(handler=_planned_command)
 
     return parser
 
 
 def main(argv: Sequence[str] | None = None) -> int:
     arguments = build_parser().parse_args(argv)
     return arguments.handler(arguments)
 
 
 if __name__ == "__main__":
     raise SystemExit(main())
diff --git a/src/tritrack_editing_assistant/contracts.py b/src/tritrack_editing_assistant/contracts.py
index f2024a4..d25e0fe 100644
--- a/src/tritrack_editing_assistant/contracts.py
+++ b/src/tritrack_editing_assistant/contracts.py
@@ -1,38 +1,39 @@
 """Strict loaders for the public versioned JSON contracts."""
 
 from __future__ import annotations
 
 import json
 from functools import cache
 from importlib import resources
 
 import jsonschema
 
 CONTRACT_NAMES = frozenset(
     {
         "compatibility-profile-v1",
         "sync-map-v1",
         "transcript-bundle-v1",
         "text-revision-v1",
         "aligned-transcript-v1",
         "grouping-v1",
+        "working-cut-v1",
         "title-binding-v1",
         "run-manifest-v1",
         "provider-receipt-v1",
     }
 )
 
 
 @cache
 def load_schema(name: str) -> dict[str, object]:
     """Load and meta-validate one packaged schema by its closed public name."""
 
     if name not in CONTRACT_NAMES:
         raise ValueError(f"TRITRACK_CONTRACT_UNKNOWN: {name!r}")
 
     schema_text = (
         resources.files("tritrack_editing_assistant.schemas")
         .joinpath(f"{name}.schema.json")
         .read_text(encoding="utf-8")
     )
     schema = json.loads(schema_text)
diff --git a/src/tritrack_editing_assistant/organizer.py b/src/tritrack_editing_assistant/organizer.py
new file mode 100644
index 0000000..985270a
--- /dev/null
+++ b/src/tritrack_editing_assistant/organizer.py
@@ -0,0 +1,520 @@
+"""Deterministic cue-addressed editorial grouping and compilation."""
+
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import stat
+import tempfile
+import unicodedata
+from collections.abc import Mapping
+from dataclasses import dataclass
+from pathlib import Path
+
+from jsonschema import ValidationError
+
+from . import hallucination
+from .contracts import validate_contract
+from .process import require_absent_output
+
+ORGANIZATION_PROFILE_ID = "cue-addressed-question-groups-v1"
+QUESTION_TEXT_LIMIT = 500
+NOTE_TEXT_LIMIT = 2000
+_JSON_LIMIT_BYTES = 16 * 1024 * 1024
+
+
+@dataclass(frozen=True)
+class IndexedCue:
+    cue_id: str
+    start_ms: int
+    end_ms: int
+
+
+@dataclass(frozen=True)
+class IndexedTake:
+    take_id: str
+    source_sha256: str
+    status: str
+    cues: tuple[IndexedCue, ...]
+    cue_positions: Mapping[str, int]
+
+
+@dataclass(frozen=True)
+class AlignedIndex:
+    takes: Mapping[str, IndexedTake]
+    completed_take_order: tuple[str, ...]
+
+
+@dataclass(frozen=True)
+class LoadedJsonArtifact:
+    path: Path
+    payload: object
+    encoded: bytes
+    sha256: str
+    invalid_code: str
+
+
+def _validate_contract(name: str, payload: object, code: str) -> None:
+    try:
+        validate_contract(name, payload)
+    except ValidationError as error:
+        raise ValueError(code) from error
+
+
+def canonical_editor_text(
+    value: object,
+    *,
+    maximum: int,
+    required: bool,
+) -> str | None:
+    """Normalize one bounded editor-authored field without interpreting it."""
+
+    if value is None or value == "":
+        if required:
+            raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
+        return None
+    if not isinstance(value, str):
+        raise TypeError("TRITRACK_ORGANIZER_TEXT_INVALID")
+    if any(unicodedata.category(character).startswith("C") for character in value):
+        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
+    normalized = " ".join(unicodedata.normalize("NFC", value).split())
+    if (required and not normalized) or not 0 < len(normalized) <= maximum:
+        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
+    return normalized
+
+
+def index_aligned_transcript(payload: object) -> AlignedIndex:
+    """Validate and index one canonical aligned transcript authority."""
+
+    _validate_contract(
+        "aligned-transcript-v1",
+        payload,
+        "TRITRACK_ORGANIZER_ALIGNED_INVALID",
+    )
+    assert isinstance(payload, Mapping)
+    takes = payload["takes"]
+    assert isinstance(takes, list)
+    take_ids = [take["takeId"] for take in takes]
+    if take_ids != sorted(take_ids) or len(take_ids) != len(set(take_ids)):
+        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
+
+    indexed: dict[str, IndexedTake] = {}
+    completed_order: list[str] = []
+    for take in takes:
+        assert isinstance(take, Mapping)
+        take_id = take["takeId"]
+        source_sha256 = take["sourceSha256"]
+        status = take["status"]
+        cues = take["cues"]
+        assert isinstance(take_id, str)
+        assert isinstance(source_sha256, str)
+        assert isinstance(status, str)
+        assert isinstance(cues, list)
+
+        indexed_cues: list[IndexedCue] = []
+        positions: dict[str, int] = {}
+        previous_end = 0
+        for position, cue in enumerate(cues):
+            assert isinstance(cue, Mapping)
+            cue_id = cue["cueId"]
+            start_ms = cue["startMs"]
+            end_ms = cue["endMs"]
+            text = cue["text"]
+            assert isinstance(cue_id, str)
+            assert isinstance(start_ms, int)
+            assert isinstance(end_ms, int)
+            assert isinstance(text, str)
+            if cue_id in positions or not (previous_end <= start_ms < end_ms):
+                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
+            try:
+                normalized_text = hallucination.normalize_cue_text(text)
+            except (TypeError, ValueError) as error:
+                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID") from error
+            if normalized_text != text:
+                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
+            positions[cue_id] = position
+            indexed_cues.append(IndexedCue(cue_id, start_ms, end_ms))
+            previous_end = end_ms
+
+        if status == "completed":
+            completed_order.append(take_id)
+        indexed[take_id] = IndexedTake(
+            take_id=take_id,
+            source_sha256=source_sha256,
+            status=status,
+            cues=tuple(indexed_cues),
+            cue_positions=positions,
+        )
+    return AlignedIndex(indexed, tuple(completed_order))
+
+
+def _require_permutation(items: list[object], field: str) -> None:
+    orders = [item[field] for item in items]
+    if orders != list(range(1, len(items) + 1)):
+        raise ValueError("TRITRACK_ORGANIZER_ORDER_INVALID")
+
+
+def _resolve_span(
+    selection: Mapping[str, object],
+    *,
+    aligned_index: AlignedIndex,
+) -> tuple[IndexedTake, int, int]:
+    take_id = selection["takeId"]
+    start_cue_id = selection["startCueId"]
+    end_cue_id = selection["endCueId"]
+    assert isinstance(take_id, str)
+    assert isinstance(start_cue_id, str)
+    assert isinstance(end_cue_id, str)
+    take = aligned_index.takes.get(take_id)
+    if take is None:
+        raise ValueError("TRITRACK_ORGANIZER_TAKE_UNKNOWN")
+    if take.status != "completed":
+        raise ValueError("TRITRACK_ORGANIZER_TAKE_NOT_COMPLETED")
+    start_position = take.cue_positions.get(start_cue_id)
+    end_position = take.cue_positions.get(end_cue_id)
+    if start_position is None or end_position is None:
+        raise ValueError("TRITRACK_ORGANIZER_CUE_UNKNOWN")
+    if start_position > end_position:
+        raise ValueError("TRITRACK_ORGANIZER_SPAN_INVALID")
+    return take, start_position, end_position
+
+
+def _require_canonical_text(
+    item: Mapping[str, object],
+    field: str,
+    *,
+    maximum: int,
+    required: bool,
+) -> None:
+    original = item.get(field)
+    try:
+        canonical = canonical_editor_text(
+            original,
+            maximum=maximum,
+            required=required,
+        )
+    except (TypeError, ValueError) as error:
+        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL") from error
+    if canonical != original:
+        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL")
+
+
+def validate_grouping(
+    payload: object,
+    *,
+    aligned_index: AlignedIndex,
+    aligned_sha256: str,
+) -> dict[str, object]:
+    """Validate canonical editor intent against one exact aligned authority."""
+
+    _validate_contract(
+        "grouping-v1",
+        payload,
+        "TRITRACK_ORGANIZER_GROUPING_INVALID",
+    )
+    assert isinstance(payload, dict)
+    if payload["alignedTranscriptSha256"] != aligned_sha256:
+        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH")
+
+    questions = payload["questions"]
+    reserve = payload["reserve"]
+    assert isinstance(questions, list)
+    assert isinstance(reserve, list)
+    _require_permutation(questions, "order")
+    _require_permutation(reserve, "order")
+
+    all_ids: set[str] = set()
+    assigned_cues: set[tuple[str, str]] = set()
+
+    def require_unique_id(item: Mapping[str, object]) -> None:
+        identifier = item["id"]
+        assert isinstance(identifier, str)
+        if identifier in all_ids:
+            raise ValueError("TRITRACK_ORGANIZER_DUPLICATE_ID")
+        all_ids.add(identifier)
+
+    def assign_span(item: Mapping[str, object]) -> None:
+        take, start_position, end_position = _resolve_span(
+            item,
+            aligned_index=aligned_index,
+        )
+        for cue in take.cues[start_position : end_position + 1]:
+            address = (take.take_id, cue.cue_id)
+            if address in assigned_cues:
+                raise ValueError("TRITRACK_ORGANIZER_CUE_REUSED")
+            assigned_cues.add(address)
+
+    for question in questions:
+        assert isinstance(question, Mapping)
+        require_unique_id(question)
+        _require_canonical_text(
+            question,
+            "question",
+            maximum=QUESTION_TEXT_LIMIT,
+            required=True,
+        )
+        answers = question["answers"]
+        assert isinstance(answers, list)
+        _require_permutation(answers, "order")
+        for answer in answers:
+            assert isinstance(answer, Mapping)
+            require_unique_id(answer)
+            if "note" in answer:
+                _require_canonical_text(
+                    answer,
+                    "note",
+                    maximum=NOTE_TEXT_LIMIT,
+                    required=False,
+                )
+            assign_span(answer)
+
+    for item in reserve:
+        assert isinstance(item, Mapping)
+        require_unique_id(item)
+        _require_canonical_text(
+            item,
+            "reason",
+            maximum=QUESTION_TEXT_LIMIT,
+            required=True,
+        )
+        if "note" in item:
+            _require_canonical_text(
+                item,
+                "note",
+                maximum=NOTE_TEXT_LIMIT,
+                required=False,
+            )
+        assign_span(item)
+    return payload
+
+
+def _compiled_span(
+    selection: Mapping[str, object],
+    *,
+    aligned_index: AlignedIndex,
+) -> dict[str, object]:
+    take, start_position, end_position = _resolve_span(
+        selection,
+        aligned_index=aligned_index,
+    )
+    return {
+        "takeId": take.take_id,
+        "sourceSha256": take.source_sha256,
+        "startCueId": take.cues[start_position].cue_id,
+        "endCueId": take.cues[end_position].cue_id,
+        "startMs": take.cues[start_position].start_ms,
+        "endMs": take.cues[end_position].end_ms,
+    }
+
+
+def build_working_cut(
+    aligned: object,
+    grouping: object,
+    *,
+    aligned_sha256: str,
+    grouping_sha256: str,
+) -> dict[str, object]:
+    """Compile one strict grouping into a deterministic text-free working cut."""
+
+    aligned_index = index_aligned_transcript(aligned)
+    canonical_grouping = validate_grouping(
+        grouping,
+        aligned_index=aligned_index,
+        aligned_sha256=aligned_sha256,
+    )
+    questions = canonical_grouping["questions"]
+    reserve = canonical_grouping["reserve"]
+    assert isinstance(questions, list)
+    assert isinstance(reserve, list)
+
+    compiled_questions: list[dict[str, object]] = []
+    segments: list[dict[str, object]] = []
+    story_order = 0
+    for question in sorted(questions, key=lambda item: item["order"]):
+        assert isinstance(question, Mapping)
+        compiled_questions.append(
+            {
+                "id": question["id"],
+                "question": question["question"],
+                "order": question["order"],
+            }
+        )
+        answers = question["answers"]
+        assert isinstance(answers, list)
+        for answer in sorted(answers, key=lambda item: item["order"]):
+            assert isinstance(answer, Mapping)
+            story_order += 1
+            compiled = {
+                "id": answer["id"],
+                "storyOrder": story_order,
+                "questionId": question["id"],
+                **_compiled_span(answer, aligned_index=aligned_index),
+            }
+            if "note" in answer:
+                compiled["note"] = answer["note"]
+            segments.append(compiled)
+
+    compiled_reserve: list[dict[str, object]] = []
+    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
+        assert isinstance(item, Mapping)
+        compiled = {
+            "id": item["id"],
+            "order": item["order"],
+            **_compiled_span(item, aligned_index=aligned_index),
+            "reason": item["reason"],
+        }
+        if "note" in item:
+            compiled["note"] = item["note"]
+        compiled_reserve.append(compiled)
+
+    working_cut: dict[str, object] = {
+        "schemaVersion": "tritrack.working-cut/v1",
+        "organizationProfileId": ORGANIZATION_PROFILE_ID,
+        "alignedTranscriptSha256": aligned_sha256,
+        "groupingSha256": grouping_sha256,
+        "questions": compiled_questions,
+        "segments": segments,
+        "reserve": compiled_reserve,
+    }
+    validate_contract("working-cut-v1", working_cut)
+    return working_cut
+
+
+def _encode_contract(name: str, payload: object) -> bytes:
+    validate_contract(name, payload)
+    return (
+        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+    ).encode("utf-8")
+
+
+def encode_grouping(payload: object) -> bytes:
+    """Return canonical bytes for one schema-valid grouping."""
+
+    return _encode_contract("grouping-v1", payload)
+
+
+def encode_working_cut(payload: object) -> bytes:
+    """Return canonical bytes for one strict working cut."""
+
+    return _encode_contract("working-cut-v1", payload)
+
+
+def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
+        raise ValueError("TRITRACK_ORGANIZER_INPUT_UNREADABLE") from error
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
+def _load_json_artifact(
+    path: Path,
+    *,
+    contract: str,
+    invalid_code: str,
+) -> LoadedJsonArtifact:
+    selected = Path(path)
+    encoded = _read_regular_bytes(selected, invalid_code)
+    try:
+        payload = json.loads(encoded.decode("utf-8", errors="strict"))
+        validate_contract(contract, payload)
+    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
+        raise ValueError(invalid_code) from error
+    return LoadedJsonArtifact(
+        path=selected,
+        payload=payload,
+        encoded=encoded,
+        sha256=hashlib.sha256(encoded).hexdigest(),
+        invalid_code=invalid_code,
+    )
+
+
+def _verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
+    try:
+        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
+    except ValueError as error:
+        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED") from error
+    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
+        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED")
+
+
+def _publish_working_cut(payload: object, output_path: Path) -> None:
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    encoded = encode_working_cut(payload)
+    descriptor, temporary_name = tempfile.mkstemp(
+        prefix=f".{destination.name}.",
+        suffix=".tmp",
+        dir=destination.parent,
+    )
+    temporary_path = Path(temporary_name)
+    try:
+        with os.fdopen(descriptor, "wb") as stream:
+            stream.write(encoded)
+            stream.flush()
+            os.fsync(stream.fileno())
+        try:
+            os.link(temporary_path, destination)
+        except FileExistsError as error:
+            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
+    finally:
+        temporary_path.unlink(missing_ok=True)
+
+
+def organize_and_publish(
+    aligned_path: Path,
+    grouping_path: Path,
+    *,
+    output_path: Path,
+) -> dict[str, object]:
+    """Compile exact local inputs and atomically publish a working cut."""
+
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    aligned = _load_json_artifact(
+        aligned_path,
+        contract="aligned-transcript-v1",
+        invalid_code="TRITRACK_ORGANIZER_ALIGNED_INVALID",
+    )
+    grouping = _load_json_artifact(
+        grouping_path,
+        contract="grouping-v1",
+        invalid_code="TRITRACK_ORGANIZER_GROUPING_INVALID",
+    )
+    if grouping.encoded != encode_grouping(grouping.payload):
+        raise ValueError("TRITRACK_ORGANIZER_GROUPING_NONCANONICAL")
+    working_cut = build_working_cut(
+        aligned.payload,
+        grouping.payload,
+        aligned_sha256=aligned.sha256,
+        grouping_sha256=grouping.sha256,
+    )
+    _verify_artifact_unchanged(aligned)
+    _verify_artifact_unchanged(grouping)
+    _publish_working_cut(working_cut, destination)
+    return working_cut
diff --git a/src/tritrack_editing_assistant/paper_edit.py b/src/tritrack_editing_assistant/paper_edit.py
new file mode 100644
index 0000000..78a961b
--- /dev/null
+++ b/src/tritrack_editing_assistant/paper_edit.py
@@ -0,0 +1,673 @@
+"""Strict XLSX transport for the cue-addressed paper-edit round trip."""
+
+from __future__ import annotations
+
+import hashlib
+import io
+import json
+import os
+import stat
+import tempfile
+import xml.etree.ElementTree as element_tree
+import zipfile
+from collections.abc import Mapping, Sequence
+from dataclasses import dataclass
+from pathlib import Path
+
+from jsonschema import ValidationError
+from openpyxl import Workbook, load_workbook
+from openpyxl.cell.cell import Cell
+from openpyxl.utils.exceptions import InvalidFileException
+
+from . import __version__, organizer
+from .contracts import validate_contract
+from .process import require_absent_output
+
+WORKBOOK_SCHEMA_VERSION = "tritrack.paper-workbook/v1"
+CUES_HEADERS = (
+    "TakeId",
+    "SourceSha256",
+    "CueId",
+    "StartMs",
+    "EndMs",
+    "Text",
+    "Disposition",
+)
+QUESTIONS_HEADERS = ("QuestionId", "Question", "Order")
+SELECTIONS_HEADERS = (
+    "Placement",
+    "SegmentId",
+    "QuestionId",
+    "Order",
+    "TakeId",
+    "StartCueId",
+    "EndCueId",
+    "ReserveReason",
+    "EditorNote",
+)
+MANIFEST_HEADERS = ("Key", "Value")
+SHEET_NAMES = ("Cues", "Questions", "Selections", "_TriTrack")
+_JSON_LIMIT_BYTES = 16 * 1024 * 1024
+_WORKBOOK_LIMIT_BYTES = 64 * 1024 * 1024
+
+
+@dataclass(frozen=True)
+class LoadedArtifact:
+    path: Path
+    payload: object
+    encoded: bytes
+    sha256: str
+    invalid_code: str
+    limit: int
+
+
+def _read_regular_bytes(path: Path, *, limit: int, invalid_code: str) -> bytes:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
+        raise ValueError("TRITRACK_PAPER_INPUT_UNREADABLE") from error
+    except OSError as error:
+        raise ValueError(invalid_code) from error
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
+            raise ValueError(invalid_code)
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(limit + 1)
+        if len(encoded) > limit:
+            raise ValueError(invalid_code)
+        return encoded
+    except OSError as error:
+        raise ValueError(invalid_code) from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+
+
+def _load_json(
+    path: Path,
+    *,
+    contract: str,
+    invalid_code: str,
+) -> LoadedArtifact:
+    selected = Path(path)
+    encoded = _read_regular_bytes(
+        selected,
+        limit=_JSON_LIMIT_BYTES,
+        invalid_code=invalid_code,
+    )
+    try:
+        payload = json.loads(encoded.decode("utf-8", errors="strict"))
+        validate_contract(contract, payload)
+    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
+        raise ValueError(invalid_code) from error
+    return LoadedArtifact(
+        selected,
+        payload,
+        encoded,
+        hashlib.sha256(encoded).hexdigest(),
+        invalid_code,
+        _JSON_LIMIT_BYTES,
+    )
+
+
+def _verify_unchanged(artifact: LoadedArtifact) -> None:
+    try:
+        encoded = _read_regular_bytes(
+            artifact.path,
+            limit=artifact.limit,
+            invalid_code=artifact.invalid_code,
+        )
+    except ValueError as error:
+        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED") from error
+    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
+        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED")
+
+
+def _literal(cell: Cell, value: object, *, text_format: bool = False) -> None:
+    cell.value = value
+    if isinstance(value, str):
+        cell.data_type = "s"
+    if text_format:
+        cell.number_format = "@"
+
+
+def _write_row(
+    worksheet,
+    row: int,
+    values: Sequence[object],
+    *,
+    text_columns: frozenset[int] = frozenset(),
+) -> None:
+    for column, value in enumerate(values, start=1):
+        _literal(
+            worksheet.cell(row=row, column=column),
+            value,
+            text_format=column in text_columns,
+        )
+
+
+def _cue_rows(aligned: Mapping[str, object]) -> list[tuple[object, ...]]:
+    organizer.index_aligned_transcript(aligned)
+    rows: list[tuple[object, ...]] = []
+    takes = aligned["takes"]
+    assert isinstance(takes, list)
+    for take in takes:
+        assert isinstance(take, Mapping)
+        if take["status"] != "completed":
+            continue
+        cues = take["cues"]
+        assert isinstance(cues, list)
+        for cue in cues:
+            assert isinstance(cue, Mapping)
+            rows.append(
+                (
+                    take["takeId"],
+                    take["sourceSha256"],
+                    cue["cueId"],
+                    cue["startMs"],
+                    cue["endMs"],
+                    cue["text"],
+                    cue["disposition"],
+                )
+            )
+    return rows
+
+
+def _cues_grid_sha256(rows: Sequence[Sequence[object]]) -> str:
+    encoded = json.dumps(
+        [list(CUES_HEADERS), *[list(row) for row in rows]],
+        ensure_ascii=False,
+        separators=(",", ":"),
+    ).encode("utf-8")
+    return hashlib.sha256(encoded).hexdigest()
+
+
+def _project_grouping(
+    workbook: Workbook,
+    grouping: Mapping[str, object] | None,
+) -> tuple[int, int]:
+    questions_sheet = workbook["Questions"]
+    selections_sheet = workbook["Selections"]
+    _write_row(questions_sheet, 1, QUESTIONS_HEADERS, text_columns=frozenset({1}))
+    _write_row(
+        selections_sheet,
+        1,
+        SELECTIONS_HEADERS,
+        text_columns=frozenset({1, 2, 3, 5, 6, 7}),
+    )
+    if grouping is None:
+        return 0, 0
+
+    questions = grouping["questions"]
+    reserve = grouping["reserve"]
+    assert isinstance(questions, list)
+    assert isinstance(reserve, list)
+    question_count = 0
+    selection_count = 0
+    for question in sorted(questions, key=lambda item: item["order"]):
+        assert isinstance(question, Mapping)
+        question_count += 1
+        _write_row(
+            questions_sheet,
+            question_count + 1,
+            (question["id"], question["question"], question["order"]),
+            text_columns=frozenset({1}),
+        )
+        answers = question["answers"]
+        assert isinstance(answers, list)
+        for answer in sorted(answers, key=lambda item: item["order"]):
+            assert isinstance(answer, Mapping)
+            selection_count += 1
+            _write_row(
+                selections_sheet,
+                selection_count + 1,
+                (
+                    "ANSWER",
+                    answer["id"],
+                    question["id"],
+                    answer["order"],
+                    answer["takeId"],
+                    answer["startCueId"],
+                    answer["endCueId"],
+                    None,
+                    answer.get("note"),
+                ),
+                text_columns=frozenset({1, 2, 3, 5, 6, 7}),
+            )
+    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
+        assert isinstance(item, Mapping)
+        selection_count += 1
+        _write_row(
+            selections_sheet,
+            selection_count + 1,
+            (
+                "RESERVE",
+                item["id"],
+                None,
+                item["order"],
+                item["takeId"],
+                item["startCueId"],
+                item["endCueId"],
+                item["reason"],
+                item.get("note"),
+            ),
+            text_columns=frozenset({1, 2, 3, 5, 6, 7}),
+        )
+    return question_count, selection_count
+
+
+def _build_workbook(
+    aligned: Mapping[str, object],
+    *,
+    aligned_sha256: str,
+    grouping: Mapping[str, object] | None,
+) -> tuple[Workbook, dict[str, int]]:
+    cue_rows = _cue_rows(aligned)
+    workbook = Workbook()
+    cues_sheet = workbook.active
+    cues_sheet.title = "Cues"
+    workbook.create_sheet("Questions")
+    workbook.create_sheet("Selections")
+    manifest_sheet = workbook.create_sheet("_TriTrack")
+    manifest_sheet.sheet_state = "hidden"
+
+    _write_row(cues_sheet, 1, CUES_HEADERS, text_columns=frozenset({1, 2, 3}))
+    for row_number, row in enumerate(cue_rows, start=2):
+        _write_row(
+            cues_sheet,
+            row_number,
+            row,
+            text_columns=frozenset({1, 2, 3}),
+        )
+    question_count, selection_count = _project_grouping(workbook, grouping)
+    _write_row(manifest_sheet, 1, MANIFEST_HEADERS)
+    manifest = (
+        ("WorkbookSchemaVersion", WORKBOOK_SCHEMA_VERSION),
+        ("ToolVersion", __version__),
+        ("AlignedTranscriptSha256", aligned_sha256),
+        ("CuesGridSha256", _cues_grid_sha256(cue_rows)),
+    )
+    for row_number, row in enumerate(manifest, start=2):
+        _write_row(manifest_sheet, row_number, row, text_columns=frozenset({1, 2}))
+    return workbook, {
+        "cueCount": len(cue_rows),
+        "questionCount": question_count,
+        "selectionCount": selection_count,
+    }
+
+
+def _publish_bytes(encoded: bytes, output_path: Path) -> None:
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    descriptor, temporary_name = tempfile.mkstemp(
+        prefix=f".{destination.name}.",
+        suffix=".tmp",
+        dir=destination.parent,
+    )
+    temporary_path = Path(temporary_name)
+    try:
+        with os.fdopen(descriptor, "wb") as stream:
+            stream.write(encoded)
+            stream.flush()
+            os.fsync(stream.fileno())
+        try:
+            os.link(temporary_path, destination)
+        except FileExistsError as error:
+            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
+    finally:
+        temporary_path.unlink(missing_ok=True)
+
+
+def export_workbook(
+    aligned_path: Path,
+    *,
+    grouping_path: Path | None,
+    output_path: Path,
+) -> dict[str, int]:
+    """Export one strict aligned authority to an editor-facing workbook."""
+
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    aligned = _load_json(
+        aligned_path,
+        contract="aligned-transcript-v1",
+        invalid_code="TRITRACK_PAPER_ALIGNED_INVALID",
+    )
+    assert isinstance(aligned.payload, Mapping)
+    grouping: LoadedArtifact | None = None
+    grouping_payload: Mapping[str, object] | None = None
+    aligned_index = organizer.index_aligned_transcript(aligned.payload)
+    if grouping_path is not None:
+        grouping = _load_json(
+            grouping_path,
+            contract="grouping-v1",
+            invalid_code="TRITRACK_PAPER_GROUPING_INVALID",
+        )
+        if grouping.encoded != organizer.encode_grouping(grouping.payload):
+            raise ValueError("TRITRACK_PAPER_GROUPING_INVALID")
+        grouping_payload = organizer.validate_grouping(
+            grouping.payload,
+            aligned_index=aligned_index,
+            aligned_sha256=aligned.sha256,
+        )
+
+    workbook, summary = _build_workbook(
+        aligned.payload,
+        aligned_sha256=aligned.sha256,
+        grouping=grouping_payload,
+    )
+    buffer = io.BytesIO()
+    workbook.save(buffer)
+    _verify_unchanged(aligned)
+    if grouping is not None:
+        _verify_unchanged(grouping)
+    _publish_bytes(buffer.getvalue(), destination)
+    return summary
+
+
+def _load_workbook_artifact(path: Path) -> tuple[LoadedArtifact, Workbook]:
+    selected = Path(path)
+    encoded = _read_regular_bytes(
+        selected,
+        limit=_WORKBOOK_LIMIT_BYTES,
+        invalid_code="TRITRACK_PAPER_WORKBOOK_INVALID",
+    )
+    artifact = LoadedArtifact(
+        selected,
+        None,
+        encoded,
+        hashlib.sha256(encoded).hexdigest(),
+        "TRITRACK_PAPER_WORKBOOK_INVALID",
+        _WORKBOOK_LIMIT_BYTES,
+    )
+    try:
+        with zipfile.ZipFile(io.BytesIO(encoded)) as archive:
+            names = archive.namelist()
+            if any(name.lower().endswith("vbaproject.bin") for name in names):
+                raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
+        workbook = load_workbook(
+            io.BytesIO(encoded),
+            data_only=False,
+            read_only=False,
+            keep_links=True,
+        )
+    except ValueError:
+        raise
+    except (
+        OSError,
+        KeyError,
+        TypeError,
+        zipfile.BadZipFile,
+        InvalidFileException,
+        element_tree.ParseError,
+    ) as error:
+        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID") from error
+    return artifact, workbook
+
+
+def _reject_unsafe_workbook_state(workbook: Workbook) -> None:
+    if workbook.sheetnames != list(SHEET_NAMES):
+        raise ValueError("TRITRACK_PAPER_SHEETS_INVALID")
+    if workbook["_TriTrack"].sheet_state != "hidden" or any(
+        workbook[name].sheet_state != "visible" for name in SHEET_NAMES[:-1]
+    ):
+        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
+    if len(workbook.defined_names) or getattr(workbook, "_external_links", []):
+        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
+    for worksheet in workbook.worksheets:
+        if worksheet.merged_cells.ranges:
+            raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
+        for row in worksheet.iter_rows():
+            for cell in row:
+                if cell.data_type == "f":
+                    raise ValueError("TRITRACK_PAPER_FORMULA_FORBIDDEN")
+
+
+def _sheet_rows(
+    worksheet,
+    headers: Sequence[str],
+    *,
+    invalid_code: str,
+) -> list[tuple[object, ...]]:
+    actual_headers = tuple(
+        worksheet.cell(row=1, column=column).value
+        for column in range(1, len(headers) + 1)
+    )
+    if actual_headers != tuple(headers):
+        raise ValueError(invalid_code)
+    if any(
+        worksheet.cell(row=row, column=column).value is not None
+        for row in range(1, worksheet.max_row + 1)
+        for column in range(len(headers) + 1, worksheet.max_column + 1)
+    ):
+        raise ValueError(invalid_code)
+    raw_rows = [
+        tuple(
+            worksheet.cell(row=row, column=column).value
+            for column in range(1, len(headers) + 1)
+        )
+        for row in range(2, worksheet.max_row + 1)
+    ]
+    while raw_rows and all(value is None for value in raw_rows[-1]):
+        raw_rows.pop()
+    if any(all(value is None for value in row) for row in raw_rows):
+        raise ValueError(invalid_code)
+    return raw_rows
+
+
+def _require_exact_row_types(
+    actual: Sequence[object],
+    expected: Sequence[object],
+) -> None:
+    if len(actual) != len(expected) or any(
+        value != reference or type(value) is not type(reference)
+        for value, reference in zip(actual, expected, strict=True)
+    ):
+        raise ValueError("TRITRACK_PAPER_REFERENCE_MISMATCH")
+
+
+def _verify_cues_grid(
+    workbook: Workbook,
+    aligned: Mapping[str, object],
+) -> list[tuple[object, ...]]:
+    expected = _cue_rows(aligned)
+    actual = _sheet_rows(
+        workbook["Cues"],
+        CUES_HEADERS,
+        invalid_code="TRITRACK_PAPER_REFERENCE_MISMATCH",
+    )
+    if len(actual) != len(expected):
+        raise ValueError("TRITRACK_PAPER_REFERENCE_MISMATCH")
+    for actual_row, expected_row in zip(actual, expected, strict=True):
+        _require_exact_row_types(actual_row, expected_row)
+    return expected
+
+
+def _verify_manifest(
+    workbook: Workbook,
+    *,
+    aligned_sha256: str,
+    cue_rows: Sequence[Sequence[object]],
+) -> None:
+    expected = [
+        ("WorkbookSchemaVersion", WORKBOOK_SCHEMA_VERSION),
+        ("ToolVersion", __version__),
+        ("AlignedTranscriptSha256", aligned_sha256),
+        ("CuesGridSha256", _cues_grid_sha256(cue_rows)),
+    ]
+    actual = _sheet_rows(
+        workbook["_TriTrack"],
+        MANIFEST_HEADERS,
+        invalid_code="TRITRACK_PAPER_MANIFEST_MISMATCH",
+    )
+    if actual != expected:
+        raise ValueError("TRITRACK_PAPER_MANIFEST_MISMATCH")
+
+
+def _canonical_workbook_text(
+    value: object,
+    *,
+    maximum: int,
+    required: bool,
+) -> str | None:
+    try:
+        return organizer.canonical_editor_text(
+            value,
+            maximum=maximum,
+            required=required,
+        )
+    except (TypeError, ValueError) as error:
+        raise ValueError("TRITRACK_PAPER_ROW_INVALID") from error
+
+
+def _positive_integer(value: object) -> int:
+    if type(value) is not int or value < 1:
+        raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+    return value
+
+
+def _required_string(value: object) -> str:
+    if not isinstance(value, str) or not value:
+        raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+    return value
+
+
+def _grouping_from_workbook(
+    workbook: Workbook,
+    *,
+    aligned_index: organizer.AlignedIndex,
+    aligned_sha256: str,
+) -> dict[str, object]:
+    question_rows = _sheet_rows(
+        workbook["Questions"],
+        QUESTIONS_HEADERS,
+        invalid_code="TRITRACK_PAPER_ROW_INVALID",
+    )
+    selection_rows = _sheet_rows(
+        workbook["Selections"],
+        SELECTIONS_HEADERS,
+        invalid_code="TRITRACK_PAPER_ROW_INVALID",
+    )
+    questions: list[dict[str, object]] = []
+    questions_by_id: dict[str, dict[str, object]] = {}
+    for question_id, question_text, order in question_rows:
+        identifier = _required_string(question_id)
+        question = {
+            "id": identifier,
+            "question": _canonical_workbook_text(
+                question_text,
+                maximum=organizer.QUESTION_TEXT_LIMIT,
+                required=True,
+            ),
+            "order": _positive_integer(order),
+            "answers": [],
+        }
+        if identifier in questions_by_id:
+            raise ValueError("TRITRACK_ORGANIZER_DUPLICATE_ID")
+        questions.append(question)
+        questions_by_id[identifier] = question
+
+    reserve: list[dict[str, object]] = []
+    for row in selection_rows:
+        (
+            placement,
+            segment_id,
+            question_id,
+            order,
+            take_id,
+            start_cue_id,
+            end_cue_id,
+            reserve_reason,
+            editor_note,
+        ) = row
+        placement = _required_string(placement)
+        common: dict[str, object] = {
+            "id": _required_string(segment_id),
+            "order": _positive_integer(order),
+            "takeId": _required_string(take_id),
+            "startCueId": _required_string(start_cue_id),
+            "endCueId": _required_string(end_cue_id),
+        }
+        note = _canonical_workbook_text(
+            editor_note,
+            maximum=organizer.NOTE_TEXT_LIMIT,
+            required=False,
+        )
+        if note is not None:
+            common["note"] = note
+        if placement == "ANSWER":
+            if reserve_reason not in {None, ""}:
+                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+            selected_question = questions_by_id.get(_required_string(question_id))
+            if selected_question is None:
+                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+            answers = selected_question["answers"]
+            assert isinstance(answers, list)
+            answers.append(common)
+        elif placement == "RESERVE":
+            if question_id not in {None, ""}:
+                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+            common["reason"] = _canonical_workbook_text(
+                reserve_reason,
+                maximum=organizer.QUESTION_TEXT_LIMIT,
+                required=True,
+            )
+            reserve.append(common)
+        else:
+            raise ValueError("TRITRACK_PAPER_ROW_INVALID")
+
+    grouping: dict[str, object] = {
+        "schemaVersion": "tritrack.grouping/v1",
+        "alignedTranscriptSha256": aligned_sha256,
+        "questions": questions,
+        "reserve": reserve,
+    }
+    return organizer.validate_grouping(
+        grouping,
+        aligned_index=aligned_index,
+        aligned_sha256=aligned_sha256,
+    )
+
+
+def apply_workbook(
+    aligned_path: Path,
+    workbook_path: Path,
+    *,
+    output_path: Path,
+) -> dict[str, object]:
+    """Apply strict workbook intent and publish canonical grouping JSON."""
+
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    aligned = _load_json(
+        aligned_path,
+        contract="aligned-transcript-v1",
+        invalid_code="TRITRACK_PAPER_ALIGNED_INVALID",
+    )
+    workbook_artifact, workbook = _load_workbook_artifact(workbook_path)
+    assert isinstance(aligned.payload, Mapping)
+    aligned_index = organizer.index_aligned_transcript(aligned.payload)
+    _reject_unsafe_workbook_state(workbook)
+    cue_rows = _verify_cues_grid(workbook, aligned.payload)
+    _verify_manifest(
+        workbook,
+        aligned_sha256=aligned.sha256,
+        cue_rows=cue_rows,
+    )
+    grouping = _grouping_from_workbook(
+        workbook,
+        aligned_index=aligned_index,
+        aligned_sha256=aligned.sha256,
+    )
+    _verify_unchanged(aligned)
+    _verify_unchanged(workbook_artifact)
+    _publish_bytes(organizer.encode_grouping(grouping), destination)
+    return grouping
diff --git a/src/tritrack_editing_assistant/schemas/grouping-v1.schema.json b/src/tritrack_editing_assistant/schemas/grouping-v1.schema.json
index 980ac67..ffec142 100644
--- a/src/tritrack_editing_assistant/schemas/grouping-v1.schema.json
+++ b/src/tritrack_editing_assistant/schemas/grouping-v1.schema.json
@@ -1,55 +1,102 @@
 {
   "$schema": "https://json-schema.org/draft/2020-12/schema",
   "$id": "https://tritrack.dev/schemas/grouping-v1.schema.json",
-  "title": "TriTrack editorial grouping v1",
+  "title": "TriTrack cue-addressed editorial grouping v1",
   "type": "object",
   "additionalProperties": false,
-  "required": ["schemaVersion", "questions", "reserve"],
+  "required": [
+    "schemaVersion",
+    "alignedTranscriptSha256",
+    "questions",
+    "reserve"
+  ],
   "properties": {
     "schemaVersion": {"const": "tritrack.grouping/v1"},
+    "alignedTranscriptSha256": {"$ref": "#/$defs/sha256"},
     "questions": {
       "type": "array",
+      "minItems": 1,
+      "maxItems": 10000,
       "items": {"$ref": "#/$defs/question"}
     },
     "reserve": {
       "type": "array",
+      "maxItems": 10000,
       "items": {"$ref": "#/$defs/reserveRange"}
     }
   },
   "$defs": {
+    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
+    "safeId": {
+      "type": "string",
+      "minLength": 1,
+      "maxLength": 128,
+      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
+    },
+    "takeId": {
+      "type": "string",
+      "minLength": 1,
+      "maxLength": 255,
+      "pattern": "^[^/\\\\\\r\\n]+$"
+    },
+    "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
+    "questionText": {"type": "string", "minLength": 1, "maxLength": 500},
+    "note": {"type": "string", "minLength": 1, "maxLength": 2000},
     "answerRange": {
       "type": "object",
       "additionalProperties": false,
-      "required": ["takeId", "startMs", "endMs"],
+      "required": [
+        "id",
+        "order",
+        "takeId",
+        "startCueId",
+        "endCueId"
+      ],
       "properties": {
-        "takeId": {"type": "string", "minLength": 1},
-        "startMs": {"type": "integer", "minimum": 0},
-        "endMs": {"type": "integer", "minimum": 1}
+        "id": {"$ref": "#/$defs/safeId"},
+        "order": {"type": "integer", "minimum": 1},
+        "takeId": {"$ref": "#/$defs/takeId"},
+        "startCueId": {"$ref": "#/$defs/cueId"},
+        "endCueId": {"$ref": "#/$defs/cueId"},
+        "note": {"$ref": "#/$defs/note"}
       }
     },
     "question": {
       "type": "object",
       "additionalProperties": false,
-      "required": ["id", "question", "answers"],
+      "required": ["id", "question", "order", "answers"],
       "properties": {
-        "id": {"type": "string", "minLength": 1},
-        "question": {"type": "string", "minLength": 1},
+        "id": {"$ref": "#/$defs/safeId"},
+        "question": {"$ref": "#/$defs/questionText"},
+        "order": {"type": "integer", "minimum": 1},
         "answers": {
           "type": "array",
+          "minItems": 1,
+          "maxItems": 10000,
           "items": {"$ref": "#/$defs/answerRange"}
         }
       }
     },
     "reserveRange": {
       "type": "object",
       "additionalProperties": false,
-      "required": ["takeId", "startMs", "endMs", "reason"],
+      "required": [
+        "id",
+        "order",
+        "takeId",
+        "startCueId",
+        "endCueId",
+        "reason"
+      ],
       "properties": {
-        "takeId": {"type": "string", "minLength": 1},
-        "startMs": {"type": "integer", "minimum": 0},
-        "endMs": {"type": "integer", "minimum": 1},
-        "reason": {"type": "string", "minLength": 1}
+        "id": {"$ref": "#/$defs/safeId"},
+        "order": {"type": "integer", "minimum": 1},
+        "takeId": {"$ref": "#/$defs/takeId"},
+        "startCueId": {"$ref": "#/$defs/cueId"},
+        "endCueId": {"$ref": "#/$defs/cueId"},
+        "reason": {"$ref": "#/$defs/questionText"},
+        "note": {"$ref": "#/$defs/note"}
       }
     }
   }
 }
diff --git a/src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json b/src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json
new file mode 100644
index 0000000..6ef57c5
--- /dev/null
+++ b/src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json
@@ -0,0 +1,123 @@
+{
+  "$schema": "https://json-schema.org/draft/2020-12/schema",
+  "$id": "https://tritrack.dev/schemas/working-cut-v1.schema.json",
+  "title": "TriTrack compiled working cut v1",
+  "type": "object",
+  "additionalProperties": false,
+  "required": [
+    "schemaVersion",
+    "organizationProfileId",
+    "alignedTranscriptSha256",
+    "groupingSha256",
+    "questions",
+    "segments",
+    "reserve"
+  ],
+  "properties": {
+    "schemaVersion": {"const": "tritrack.working-cut/v1"},
+    "organizationProfileId": {
+      "const": "cue-addressed-question-groups-v1"
+    },
+    "alignedTranscriptSha256": {"$ref": "#/$defs/sha256"},
+    "groupingSha256": {"$ref": "#/$defs/sha256"},
+    "questions": {
+      "type": "array",
+      "minItems": 1,
+      "maxItems": 10000,
+      "items": {"$ref": "#/$defs/question"}
+    },
+    "segments": {
+      "type": "array",
+      "minItems": 1,
+      "maxItems": 10000,
+      "items": {"$ref": "#/$defs/segment"}
+    },
+    "reserve": {
+      "type": "array",
+      "maxItems": 10000,
+      "items": {"$ref": "#/$defs/reserveRange"}
+    }
+  },
+  "$defs": {
+    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
+    "safeId": {
+      "type": "string",
+      "minLength": 1,
+      "maxLength": 128,
+      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
+    },
+    "takeId": {
+      "type": "string",
+      "minLength": 1,
+      "maxLength": 255,
+      "pattern": "^[^/\\\\\\r\\n]+$"
+    },
+    "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
+    "editorText": {"type": "string", "minLength": 1, "maxLength": 500},
+    "note": {"type": "string", "minLength": 1, "maxLength": 2000},
+    "question": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["id", "question", "order"],
+      "properties": {
+        "id": {"$ref": "#/$defs/safeId"},
+        "question": {"$ref": "#/$defs/editorText"},
+        "order": {"type": "integer", "minimum": 1}
+      }
+    },
+    "segment": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "id",
+        "storyOrder",
+        "questionId",
+        "takeId",
+        "sourceSha256",
+        "startCueId",
+        "endCueId",
+        "startMs",
+        "endMs"
+      ],
+      "properties": {
+        "id": {"$ref": "#/$defs/safeId"},
+        "storyOrder": {"type": "integer", "minimum": 1},
+        "questionId": {"$ref": "#/$defs/safeId"},
+        "takeId": {"$ref": "#/$defs/takeId"},
+        "sourceSha256": {"$ref": "#/$defs/sha256"},
+        "startCueId": {"$ref": "#/$defs/cueId"},
+        "endCueId": {"$ref": "#/$defs/cueId"},
+        "startMs": {"type": "integer", "minimum": 0},
+        "endMs": {"type": "integer", "minimum": 1},
+        "note": {"$ref": "#/$defs/note"}
+      }
+    },
+    "reserveRange": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "id",
+        "order",
+        "takeId",
+        "sourceSha256",
+        "startCueId",
+        "endCueId",
+        "startMs",
+        "endMs",
+        "reason"
+      ],
+      "properties": {
+        "id": {"$ref": "#/$defs/safeId"},
+        "order": {"type": "integer", "minimum": 1},
+        "takeId": {"$ref": "#/$defs/takeId"},
+        "sourceSha256": {"$ref": "#/$defs/sha256"},
+        "startCueId": {"$ref": "#/$defs/cueId"},
+        "endCueId": {"$ref": "#/$defs/cueId"},
+        "startMs": {"type": "integer", "minimum": 0},
+        "endMs": {"type": "integer", "minimum": 1},
+        "reason": {"$ref": "#/$defs/editorText"},
+        "note": {"$ref": "#/$defs/note"}
+      }
+    }
+  }
+}
diff --git a/tests/task9_fixtures.py b/tests/task9_fixtures.py
new file mode 100644
index 0000000..e161e0b
--- /dev/null
+++ b/tests/task9_fixtures.py
@@ -0,0 +1,114 @@
+"""Invented, public-safe Task 9 fixtures shared by focused tests."""
+
+
+ALIGNED_SHA256 = "a" * 64
+GROUPING_SHA256 = "b" * 64
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
+                "takeId": "A.wav",
+                "sourceSha256": "3" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 0,
+                        "endMs": 500,
+                        "text": "Invented first answer.",
+                        "disposition": "original",
+                    },
+                    {
+                        "cueId": "cue-000002",
+                        "startMs": 500,
+                        "endMs": 1100,
+                        "text": "Invented continuation.",
+                        "disposition": "revised",
+                    },
+                ],
+            },
+            {
+                "takeId": "B.wav",
+                "sourceSha256": "4" * 64,
+                "status": "completed",
+                "cues": [
+                    {
+                        "cueId": "cue-000001",
+                        "startMs": 100,
+                        "endMs": 700,
+                        "text": "Invented second answer.",
+                        "disposition": "original",
+                    },
+                    {
+                        "cueId": "cue-000002",
+                        "startMs": 900,
+                        "endMs": 1400,
+                        "text": "Invented reserve.",
+                        "disposition": "original",
+                    },
+                ],
+            },
+            {
+                "takeId": "C.wav",
+                "sourceSha256": "5" * 64,
+                "status": "empty",
+                "cues": [],
+            },
+        ],
+    }
+
+
+def invented_grouping() -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.grouping/v1",
+        "alignedTranscriptSha256": ALIGNED_SHA256,
+        "questions": [
+            {
+                "id": "question-001",
+                "question": "What changed?",
+                "order": 1,
+                "answers": [
+                    {
+                        "id": "answer-001",
+                        "order": 1,
+                        "takeId": "A.wav",
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000002",
+                        "note": "Primary invented answer",
+                    }
+                ],
+            },
+            {
+                "id": "question-002",
+                "question": "What comes next?",
+                "order": 2,
+                "answers": [
+                    {
+                        "id": "answer-002",
+                        "order": 1,
+                        "takeId": "B.wav",
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000001",
+                    }
+                ],
+            },
+        ],
+        "reserve": [
+            {
+                "id": "reserve-001",
+                "order": 1,
+                "takeId": "B.wav",
+                "startCueId": "cue-000002",
+                "endCueId": "cue-000002",
+                "reason": "Alternate invented answer",
+                "note": "Keep available",
+            }
+        ],
+    }
diff --git a/tests/test_cli.py b/tests/test_cli.py
index d0fe653..6a0834d 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -141,42 +141,42 @@ class CliSmokeTest(unittest.TestCase):
                 "hallucination.py",
                 "organizer.py",
                 "paper_edit.py",
                 "align_text.py",
                 "gemini_hybrid.py",
                 "gemini_transcribe.mjs",
                 "multicam-sync",
             ],
         )
         self.assertEqual(
             {
                 component["sourceComponent"]: component["status"]
                 for component in payload["components"]
             },
             {
                 "sync_scan.py": "implemented",
                 "emit_fcpxml.py": "implemented",
                 "transcribe_takes.py": "implemented",
                 "string_out.py": "implemented",
                 "hallucination.py": "implemented",
-                "organizer.py": "planned",
-                "paper_edit.py": "planned",
+                "organizer.py": "implemented",
+                "paper_edit.py": "implemented",
                 "align_text.py": "implemented",
                 "gemini_hybrid.py": "implemented",
                 "gemini_transcribe.mjs": "planned",
                 "multicam-sync": "planned",
             },
         )
 
     def test_help_exposes_the_complete_scaffold(self):
         completed = self.run_cli("--help")
         for command in (
             "components",
             "doctor",
             "sync",
             "transcribe",
             "align",
             "hybrid",
             "emit",
             "validate",
             "organize",
             "paper",
@@ -253,40 +253,286 @@ class CliSmokeTest(unittest.TestCase):
     def test_align_rejects_existing_output_before_reading_inputs(self):
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             output = root / "aligned.json"
             output.write_text("sentinel", encoding="utf-8")
 
             completed = self.run_cli_unchecked(
                 "align",
                 "--transcript",
                 str(root / "missing-transcript.json"),
                 "--revision",
                 str(root / "missing-revision.json"),
                 "--output",
                 str(output),
             )
 
             self.assertEqual(completed.returncode, 73)
             self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
             self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")
 
+    def test_organize_help_exposes_only_the_local_cue_addressed_boundary(self):
+        completed = self.run_cli("organize", "--help")
+        for option in ("--aligned", "--grouping", "--output", "--json"):
+            self.assertIn(option, completed.stdout)
+        for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
+            self.assertNotIn(excluded, completed.stdout.lower())
+
+    def test_organize_cli_publishes_only_a_sanitized_summary(self):
+        from tests.task9_fixtures import invented_aligned, invented_grouping
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned = root / "aligned.json"
+            grouping = root / "grouping.json"
+            output = root / "working-cut.json"
+            aligned.write_text(
+                json.dumps(
+                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
+                )
+                + "\n",
+                encoding="utf-8",
+            )
+            grouping_payload = invented_grouping()
+            grouping_payload["alignedTranscriptSha256"] = hashlib.sha256(
+                aligned.read_bytes()
+            ).hexdigest()
+            grouping.write_text(
+                json.dumps(
+                    grouping_payload,
+                    ensure_ascii=False,
+                    indent=2,
+                    sort_keys=True,
+                )
+                + "\n",
+                encoding="utf-8",
+            )
+
+            completed = self.run_cli_unchecked(
+                "organize",
+                "--aligned",
+                str(aligned),
+                "--grouping",
+                str(grouping),
+                "--output",
+                str(output),
+                "--json",
+            )
+
+            self.assertEqual(completed.returncode, 0, completed.stderr)
+            summary = json.loads(completed.stdout)
+            self.assertEqual(
+                summary,
+                {
+                    "schemaVersion": "tritrack.organize-summary/v1",
+                    "questionCount": 2,
+                    "segmentCount": 2,
+                    "reserveCount": 1,
+                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
+                },
+            )
+            encoded = json.dumps(summary)
+            self.assertNotIn(str(root), encoded)
+            self.assertNotIn("What changed", encoded)
+
+    def test_organize_rejects_existing_output_before_reading_inputs(self):
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "working-cut.json"
+            output.write_text("sentinel", encoding="utf-8")
+            completed = self.run_cli_unchecked(
+                "organize",
+                "--aligned",
+                str(root / "missing-aligned.json"),
+                "--grouping",
+                str(root / "missing-grouping.json"),
+                "--output",
+                str(output),
+            )
+            self.assertEqual(completed.returncode, 73)
+            self.assertEqual(
+                json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
+            )
+            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")
+
+    def test_organize_maps_missing_input_to_io_without_traceback(self):
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            completed = self.run_cli_unchecked(
+                "organize",
+                "--aligned",
+                str(root / "missing-aligned.json"),
+                "--grouping",
+                str(root / "missing-grouping.json"),
+                "--output",
+                str(root / "working-cut.json"),
+            )
+            self.assertEqual(completed.returncode, 74)
+            self.assertEqual(
+                json.loads(completed.stdout),
+                {"error": "TRITRACK_ORGANIZER_INPUT_UNREADABLE"},
+            )
+            self.assertNotIn("Traceback", completed.stderr)
+
+    def test_paper_help_exposes_exact_nested_local_commands(self):
+        paper = self.run_cli("paper", "--help")
+        self.assertIn("export", paper.stdout)
+        self.assertIn("apply", paper.stdout)
+
+        export = self.run_cli("paper", "export", "--help")
+        for option in ("--aligned", "--grouping", "--output", "--json"):
+            self.assertIn(option, export.stdout)
+        self.assertNotIn("--workbook", export.stdout)
+
+        apply = self.run_cli("paper", "apply", "--help")
+        for option in ("--aligned", "--workbook", "--output", "--json"):
+            self.assertIn(option, apply.stdout)
+        self.assertNotIn("--grouping", apply.stdout)
+        for completed in (paper, export, apply):
+            for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
+                self.assertNotIn(excluded, completed.stdout.lower())
+
+    def test_paper_export_and_apply_print_only_sanitized_summaries(self):
+        from openpyxl import load_workbook
+
+        from tests.task9_fixtures import invented_aligned
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned = root / "aligned.json"
+            workbook = root / "paper.xlsx"
+            grouping = root / "grouping.json"
+            aligned.write_text(
+                json.dumps(
+                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
+                )
+                + "\n",
+                encoding="utf-8",
+            )
+
+            exported = self.run_cli_unchecked(
+                "paper",
+                "export",
+                "--aligned",
+                str(aligned),
+                "--output",
+                str(workbook),
+                "--json",
+            )
+            self.assertEqual(exported.returncode, 0, exported.stderr)
+            export_summary = json.loads(exported.stdout)
+            self.assertEqual(
+                export_summary,
+                {
+                    "schemaVersion": "tritrack.paper-export-summary/v1",
+                    "cueCount": 4,
+                    "questionCount": 0,
+                    "selectionCount": 0,
+                    "artifactSha256": hashlib.sha256(
+                        workbook.read_bytes()
+                    ).hexdigest(),
+                },
+            )
+
+            editable = load_workbook(workbook, data_only=False)
+            editable["Questions"].append(
+                ["question-001", "  Invented   question?  ", 1]
+            )
+            editable["Selections"].append(
+                [
+                    "ANSWER",
+                    "answer-001",
+                    "question-001",
+                    1,
+                    "A.wav",
+                    "cue-000001",
+                    "cue-000001",
+                    None,
+                    None,
+                ]
+            )
+            editable.save(workbook)
+
+            applied = self.run_cli_unchecked(
+                "paper",
+                "apply",
+                "--aligned",
+                str(aligned),
+                "--workbook",
+                str(workbook),
+                "--output",
+                str(grouping),
+                "--json",
+            )
+            self.assertEqual(applied.returncode, 0, applied.stderr)
+            apply_summary = json.loads(applied.stdout)
+            self.assertEqual(
+                apply_summary,
+                {
+                    "schemaVersion": "tritrack.paper-apply-summary/v1",
+                    "questionCount": 1,
+                    "answerCount": 1,
+                    "reserveCount": 0,
+                    "artifactSha256": hashlib.sha256(
+                        grouping.read_bytes()
+                    ).hexdigest(),
+                },
+            )
+            summaries = json.dumps([export_summary, apply_summary])
+            self.assertNotIn(str(root), summaries)
+            self.assertNotIn("Invented question", summaries)
+
+    def test_paper_cli_maps_output_and_input_failures(self):
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "paper.xlsx"
+            output.write_text("winner", encoding="utf-8")
+            exists = self.run_cli_unchecked(
+                "paper",
+                "export",
+                "--aligned",
+                str(root / "missing.json"),
+                "--output",
+                str(output),
+            )
+            self.assertEqual(exists.returncode, 73)
+            self.assertEqual(
+                json.loads(exists.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
+            )
+
+            missing = self.run_cli_unchecked(
+                "paper",
+                "apply",
+                "--aligned",
+                str(root / "missing.json"),
+                "--workbook",
+                str(root / "missing.xlsx"),
+                "--output",
+                str(root / "grouping.json"),
+            )
+            self.assertEqual(missing.returncode, 74)
+            self.assertEqual(
+                json.loads(missing.stdout),
+                {"error": "TRITRACK_PAPER_INPUT_UNREADABLE"},
+            )
+            self.assertNotIn("Traceback", missing.stderr)
+
     def test_hybrid_help_exposes_only_offline_receipt_validation(self):
         completed = self.run_cli("hybrid", "--help")
         for option in (
             "--transcript",
             "--proposal",
             "--receipt",
             "--model",
             "--output",
             "--json",
         ):
             self.assertIn(option, completed.stdout)
         self.assertIn("offline", completed.stdout.lower())
         self.assertIn("no network", completed.stdout.lower())
         for excluded in ("api-key", "credential", "fallback", "upload-file"):
             self.assertNotIn(excluded, completed.stdout.lower())
 
     def test_hybrid_cli_validates_receipt_and_prints_sanitized_summary(self):
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             transcript, revision = write_alignment_inputs(root)
diff --git a/tests/test_contracts.py b/tests/test_contracts.py
index 92f7220..6de88ac 100644
--- a/tests/test_contracts.py
+++ b/tests/test_contracts.py
@@ -23,58 +23,105 @@ VALID_CONTRACTS = {
         "pairs": [
             {
                 "pairId": "pair-001",
                 "mediaA": "camera-a-001",
                 "mediaB": "camera-b-001",
                 "offsetBFromASeconds": -1.25,
                 "confidence": 18.5,
                 "overlapSeconds": 42.0,
                 "audioMaster": "A",
                 "durationASeconds": 45.0,
                 "durationBSeconds": 44.0,
                 "startedAt": None,
             }
         ],
         "singleA": ["camera-a-002"],
         "singleB": [],
         "warnings": [{"code": "SYNC_AUDIO_MISSING", "mediaId": "camera-a-002"}],
     },
     "grouping-v1": {
         "schemaVersion": "tritrack.grouping/v1",
+        "alignedTranscriptSha256": "4" * 64,
         "questions": [
             {
                 "id": "question-001",
                 "question": "What changed?",
+                "order": 1,
                 "answers": [
                     {
-                        "takeId": "take-001",
-                        "startMs": 500,
-                        "endMs": 2500,
+                        "id": "answer-001",
+                        "order": 1,
+                        "takeId": "Take-A.wav",
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000002",
+                        "note": "Primary answer",
                     }
                 ],
             }
         ],
         "reserve": [
             {
-                "takeId": "take-002",
+                "id": "reserve-001",
+                "order": 1,
+                "takeId": "Take-B.wav",
+                "startCueId": "cue-000003",
+                "endCueId": "cue-000003",
+                "reason": "Alternate answer",
+            }
+        ],
+    },
+    "working-cut-v1": {
+        "schemaVersion": "tritrack.working-cut/v1",
+        "organizationProfileId": "cue-addressed-question-groups-v1",
+        "alignedTranscriptSha256": "4" * 64,
+        "groupingSha256": "5" * 64,
+        "questions": [
+            {
+                "id": "question-001",
+                "question": "What changed?",
+                "order": 1,
+            }
+        ],
+        "segments": [
+            {
+                "id": "answer-001",
+                "storyOrder": 1,
+                "questionId": "question-001",
+                "takeId": "Take-A.wav",
+                "sourceSha256": "a" * 64,
+                "startCueId": "cue-000001",
+                "endCueId": "cue-000002",
                 "startMs": 0,
-                "endMs": 1000,
+                "endMs": 1200,
+                "note": "Primary answer",
+            }
+        ],
+        "reserve": [
+            {
+                "id": "reserve-001",
+                "order": 1,
+                "takeId": "Take-B.wav",
+                "sourceSha256": "b" * 64,
+                "startCueId": "cue-000003",
+                "endCueId": "cue-000003",
+                "startMs": 2000,
+                "endMs": 2500,
                 "reason": "Alternate answer",
             }
         ],
     },
     "title-binding-v1": {
         "schemaVersion": "tritrack.title-binding/v1",
         "bindingId": "basic-title-v1",
         "effectName": "Basic Title",
         "effectUid": ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti",
         "parameters": [
             {"name": "fontSize", "value": 72.0},
             {"name": "alignment", "value": "center"},
         ],
     },
     "transcript-bundle-v1": {
         "schemaVersion": "tritrack.transcript-bundle/v1",
         "profileId": "whisper-cpp-cpu-no-fallback-v1",
         "language": "zh",
         "modelSha256": "f" * 64,
         "engine": {
@@ -229,23 +276,57 @@ class ContractValidationTest(unittest.TestCase):
         empty_with_cues["takes"][0]["status"] = "empty"
         invalid_cases.append(("aligned-transcript-v1", empty_with_cues))
 
         missing_receipt_binding = copy.deepcopy(
             VALID_CONTRACTS["provider-receipt-v1"]
         )
         del missing_receipt_binding["sourceBundleSha256"]
         invalid_cases.append(("provider-receipt-v1", missing_receipt_binding))
 
         unsafe_take_id = copy.deepcopy(VALID_CONTRACTS["text-revision-v1"])
         unsafe_take_id["takes"][0]["takeId"] = "../Take-A.wav"
         invalid_cases.append(("text-revision-v1", unsafe_take_id))
 
         for name, payload in invalid_cases:
             with (
                 self.subTest(name=name, payload=payload),
                 self.assertRaises(ValidationError),
             ):
                 contracts.validate_contract(name, payload)
 
+    def test_task_9_contracts_reject_invalid_state_shapes(self):
+        invalid_cases = []
+
+        missing_binding = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
+        del missing_binding["alignedTranscriptSha256"]
+        invalid_cases.append(("grouping-v1", missing_binding))
+
+        unsafe_question_id = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
+        unsafe_question_id["questions"][0]["id"] = "../question"
+        invalid_cases.append(("grouping-v1", unsafe_question_id))
+
+        missing_answer_order = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
+        del missing_answer_order["questions"][0]["answers"][0]["order"]
+        invalid_cases.append(("grouping-v1", missing_answer_order))
+
+        timing_in_grouping = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
+        timing_in_grouping["questions"][0]["answers"][0]["startMs"] = 0
+        invalid_cases.append(("grouping-v1", timing_in_grouping))
+
+        text_in_segment = copy.deepcopy(VALID_CONTRACTS["working-cut-v1"])
+        text_in_segment["segments"][0]["text"] = "Not a second authority"
+        invalid_cases.append(("working-cut-v1", text_in_segment))
+
+        wrong_profile = copy.deepcopy(VALID_CONTRACTS["working-cut-v1"])
+        wrong_profile["organizationProfileId"] = "future-profile"
+        invalid_cases.append(("working-cut-v1", wrong_profile))
+
+        for name, payload in invalid_cases:
+            with (
+                self.subTest(name=name, payload=payload),
+                self.assertRaises(ValidationError),
+            ):
+                contracts.validate_contract(name, payload)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/tests/test_maintainer_boundary.py b/tests/test_maintainer_boundary.py
index 97872ff..856c1ed 100644
--- a/tests/test_maintainer_boundary.py
+++ b/tests/test_maintainer_boundary.py
@@ -75,54 +75,72 @@ class MaintainerBoundaryTest(unittest.TestCase):
     def test_public_governance_is_self_contained_and_public_safe(self) -> None:
         forbidden = (
             "/" + "Users" + "/",
             "TriTrack-" + "worktrees",
             "TriTrack-" + "Subtitle-" + "Studio",
             "Codex for " + "Open Source",
             "six " + "months",
             "六" + "個月",
         )
         for path in PUBLIC_GOVERNANCE:
             text = path.read_text(encoding="utf-8")
             for token in forbidden:
                 self.assertNotIn(token, text, f"{path}: leaked {token!r}")
 
     def test_maintainer_and_end_user_skills_are_distinct(self) -> None:
         skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
         self.assertIn("name: tritrack-editing-assistant-maintainer", skill)
         self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", skill)
         self.assertFalse((ROOT / "skills" / "tritrack-editing-assistant").exists())
 
-    def test_public_status_records_task_8_and_schedules_task_9(self) -> None:
+    def test_public_status_records_task_9_and_schedules_task_10(self) -> None:
         status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
         roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
         tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
-        self.assertIn("Tasks 1–8", status)
+        readme = (ROOT / "README.md").read_text(encoding="utf-8")
+        decision = (ROOT / "docs" / "TASK-9-DECISION.md").read_text(
+            encoding="utf-8"
+        )
+        verification = (ROOT / "docs" / "TASK-9-VERIFICATION.md").read_text(
+            encoding="utf-8"
+        )
+        self.assertIn("Tasks 1–9", status)
         self.assertIn("Task 6.5", status)
         self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
         self.assertLess(status.index("Task 7"), status.index("Task 8"))
         self.assertLess(status.index("Task 8"), status.index("Task 9"))
-        self.assertIn("Task 8", roadmap)
-        self.assertLess(roadmap.index("Task 8"), roadmap.index("Task 9"))
-        self.assertIn("tritrack align --help", tooling)
-        self.assertIn("tritrack hybrid --help", tooling)
-        self.assertIn("no network access", tooling)
+        self.assertLess(status.index("Task 9"), status.index("Task 10"))
+        self.assertIn("Task 9", roadmap)
+        self.assertLess(roadmap.index("Task 9"), roadmap.index("Task 10"))
+        for authority in (
+            "tritrack paper export --help",
+            "tritrack paper apply --help",
+            "tritrack organize --help",
+        ):
+            self.assertIn(authority, tooling)
+        for text in (status, roadmap, tooling, readme, verification):
+            self.assertIn("Task 9", text)
+        self.assertIn("exactly four worksheets", decision)
+        self.assertIn("Grouping fixpoint", verification)
+        self.assertIn("no network", verification)
+        self.assertIn("Task 10", status)
+        self.assertIn("Task 10", roadmap)
 
     def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
         handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
             encoding="utf-8"
         )
         self.assertIn(
             "$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 6.5",
             handoff,
         )
         self.assertIn("242e8b5406e92049ce60c654c3c8fca11be4b596", handoff)
         self.assertIn("codex/task6-5-public-demo-readiness", handoff)
         self.assertIn("RED", handoff)
         self.assertIn("GREEN", handoff)
         self.assertIn("application submission", handoff)
         self.assertNotIn("/" + "Users" + "/", handoff)
 
     def test_tooling_pins_the_perpetual_final_cut_identity(self) -> None:
         tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
         self.assertIn("/Applications/Final Cut Pro.app", tooling)
         self.assertIn("com.apple.FinalCut", tooling)
diff --git a/tests/test_organizer.py b/tests/test_organizer.py
new file mode 100644
index 0000000..7c12d24
--- /dev/null
+++ b/tests/test_organizer.py
@@ -0,0 +1,350 @@
+from __future__ import annotations
+
+import copy
+import hashlib
+import json
+import os
+import tempfile
+import unittest
+from pathlib import Path
+from unittest import mock
+
+from tests.task9_fixtures import (
+    ALIGNED_SHA256,
+    GROUPING_SHA256,
+    invented_aligned,
+    invented_grouping,
+)
+from tritrack_editing_assistant import organizer
+from tritrack_editing_assistant.contracts import validate_contract
+
+
+class PureOrganizerTest(unittest.TestCase):
+    def build(self, aligned=None, grouping=None):
+        return organizer.build_working_cut(
+            invented_aligned() if aligned is None else aligned,
+            invented_grouping() if grouping is None else grouping,
+            aligned_sha256=ALIGNED_SHA256,
+            grouping_sha256=GROUPING_SHA256,
+        )
+
+    def test_builds_strict_immutable_text_free_working_cut(self) -> None:
+        aligned = invented_aligned()
+        grouping = invented_grouping()
+        aligned_before = copy.deepcopy(aligned)
+        grouping_before = copy.deepcopy(grouping)
+
+        working_cut = self.build(aligned, grouping)
+
+        validate_contract("working-cut-v1", working_cut)
+        self.assertEqual(aligned, aligned_before)
+        self.assertEqual(grouping, grouping_before)
+        self.assertEqual(
+            working_cut,
+            {
+                "schemaVersion": "tritrack.working-cut/v1",
+                "organizationProfileId": "cue-addressed-question-groups-v1",
+                "alignedTranscriptSha256": ALIGNED_SHA256,
+                "groupingSha256": GROUPING_SHA256,
+                "questions": [
+                    {
+                        "id": "question-001",
+                        "question": "What changed?",
+                        "order": 1,
+                    },
+                    {
+                        "id": "question-002",
+                        "question": "What comes next?",
+                        "order": 2,
+                    },
+                ],
+                "segments": [
+                    {
+                        "id": "answer-001",
+                        "storyOrder": 1,
+                        "questionId": "question-001",
+                        "takeId": "A.wav",
+                        "sourceSha256": "3" * 64,
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000002",
+                        "startMs": 0,
+                        "endMs": 1100,
+                        "note": "Primary invented answer",
+                    },
+                    {
+                        "id": "answer-002",
+                        "storyOrder": 2,
+                        "questionId": "question-002",
+                        "takeId": "B.wav",
+                        "sourceSha256": "4" * 64,
+                        "startCueId": "cue-000001",
+                        "endCueId": "cue-000001",
+                        "startMs": 100,
+                        "endMs": 700,
+                    },
+                ],
+                "reserve": [
+                    {
+                        "id": "reserve-001",
+                        "order": 1,
+                        "takeId": "B.wav",
+                        "sourceSha256": "4" * 64,
+                        "startCueId": "cue-000002",
+                        "endCueId": "cue-000002",
+                        "startMs": 900,
+                        "endMs": 1400,
+                        "reason": "Alternate invented answer",
+                        "note": "Keep available",
+                    }
+                ],
+            },
+        )
+        self.assertNotIn("Invented first answer", json.dumps(working_cut))
+
+    def test_rejects_invalid_or_noncanonical_aligned_authority(self) -> None:
+        duplicate_take = invented_aligned()
+        duplicate_take["takes"].append(copy.deepcopy(duplicate_take["takes"][0]))
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
+            self.build(duplicate_take)
+
+        duplicate_cue = invented_aligned()
+        duplicate_cue["takes"][0]["cues"].append(
+            copy.deepcopy(duplicate_cue["takes"][0]["cues"][0])
+        )
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
+            self.build(duplicate_cue)
+
+        unsorted = invented_aligned()
+        unsorted["takes"][0], unsorted["takes"][1] = (
+            unsorted["takes"][1],
+            unsorted["takes"][0],
+        )
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
+            self.build(unsorted)
+
+        invalid_timing = invented_aligned()
+        invalid_timing["takes"][0]["cues"][1]["startMs"] = 400
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ALIGNED_INVALID"):
+            self.build(invalid_timing)
+
+    def test_rejects_hash_order_id_and_text_drift(self) -> None:
+        bad_hash = invented_grouping()
+        bad_hash["alignedTranscriptSha256"] = "f" * 64
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH"
+        ):
+            self.build(grouping=bad_hash)
+
+        gapped_order = invented_grouping()
+        gapped_order["questions"][1]["order"] = 3
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_ORDER_INVALID"):
+            self.build(grouping=gapped_order)
+
+        duplicate_id = invented_grouping()
+        duplicate_id["questions"][1]["answers"][0]["id"] = "answer-001"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_DUPLICATE_ID"):
+            self.build(grouping=duplicate_id)
+
+        noncanonical_text = invented_grouping()
+        noncanonical_text["questions"][0]["question"] = "  What   changed?  "
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_ORGANIZER_TEXT_NONCANONICAL"
+        ):
+            self.build(grouping=noncanonical_text)
+
+    def test_rejects_unknown_empty_reversed_and_reused_spans(self) -> None:
+        unknown_take = invented_grouping()
+        unknown_take["questions"][0]["answers"][0]["takeId"] = "Unknown.wav"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_TAKE_UNKNOWN"):
+            self.build(grouping=unknown_take)
+
+        empty_take = invented_grouping()
+        empty_take["questions"][0]["answers"][0]["takeId"] = "C.wav"
+        with self.assertRaisesRegex(
+            ValueError, "TRITRACK_ORGANIZER_TAKE_NOT_COMPLETED"
+        ):
+            self.build(grouping=empty_take)
+
+        reversed_span = invented_grouping()
+        selection = reversed_span["questions"][0]["answers"][0]
+        selection["startCueId"], selection["endCueId"] = (
+            selection["endCueId"],
+            selection["startCueId"],
+        )
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_SPAN_INVALID"):
+            self.build(grouping=reversed_span)
+
+        unknown_cue = invented_grouping()
+        unknown_cue["questions"][0]["answers"][0]["endCueId"] = "cue-999999"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_CUE_UNKNOWN"):
+            self.build(grouping=unknown_cue)
+
+        reused = invented_grouping()
+        reused["reserve"][0]["takeId"] = "A.wav"
+        reused["reserve"][0]["startCueId"] = "cue-000002"
+        reused["reserve"][0]["endCueId"] = "cue-000002"
+        with self.assertRaisesRegex(ValueError, "TRITRACK_ORGANIZER_CUE_REUSED"):
+            self.build(grouping=reused)
+
+
+class OrganizerFileBoundaryTest(unittest.TestCase):
+    def write_inputs(self, root: Path) -> tuple[Path, Path, bytes, bytes]:
+        aligned_path = root / "aligned.json"
+        grouping_path = root / "grouping.json"
+        aligned_bytes = (
+            json.dumps(
+                invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
+            )
+            + "\n"
+        ).encode("utf-8")
+        aligned_path.write_bytes(aligned_bytes)
+        grouping = invented_grouping()
+        grouping["alignedTranscriptSha256"] = hashlib.sha256(
+            aligned_bytes
+        ).hexdigest()
+        grouping_bytes = organizer.encode_grouping(grouping)
+        grouping_path.write_bytes(grouping_bytes)
+        return aligned_path, grouping_path, aligned_bytes, grouping_bytes
+
+    def test_publishes_deterministic_exact_bound_bytes_without_mutation(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, grouping, aligned_before, grouping_before = self.write_inputs(root)
+            first = root / "first.json"
+            second = root / "second.json"
+
+            first_payload = organizer.organize_and_publish(
+                aligned, grouping, output_path=first
+            )
+            second_payload = organizer.organize_and_publish(
+                aligned, grouping, output_path=second
+            )
+
+            self.assertEqual(first_payload, second_payload)
+            self.assertEqual(first.read_bytes(), second.read_bytes())
+            self.assertEqual(aligned.read_bytes(), aligned_before)
+            self.assertEqual(grouping.read_bytes(), grouping_before)
+            self.assertEqual(
+                first_payload["alignedTranscriptSha256"],
+                hashlib.sha256(aligned_before).hexdigest(),
+            )
+            self.assertEqual(
+                first_payload["groupingSha256"],
+                hashlib.sha256(grouping_before).hexdigest(),
+            )
+
+    def test_existing_output_and_missing_parent_fail_before_publication(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "working-cut.json"
+            output.write_text("winner", encoding="utf-8")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
+                organizer.organize_and_publish(
+                    root / "missing-aligned.json",
+                    root / "missing-grouping.json",
+                    output_path=output,
+                )
+            self.assertEqual(output.read_text(encoding="utf-8"), "winner")
+
+            aligned, grouping, _, _ = self.write_inputs(root)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
+            ):
+                organizer.organize_and_publish(
+                    aligned,
+                    grouping,
+                    output_path=root / "missing" / "working-cut.json",
+                )
+
+    def test_rejects_noncanonical_malformed_symlink_and_oversized_inputs(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, grouping, _, _ = self.write_inputs(root)
+
+            noncanonical = root / "noncanonical.json"
+            noncanonical.write_text(
+                json.dumps(json.loads(grouping.read_text(encoding="utf-8"))),
+                encoding="utf-8",
+            )
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_ORGANIZER_GROUPING_NONCANONICAL"
+            ):
+                organizer.organize_and_publish(
+                    aligned, noncanonical, output_path=root / "noncanonical-out.json"
+                )
+
+            malformed = root / "malformed.json"
+            malformed.write_bytes(b"\xff")
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
+            ):
+                organizer.organize_and_publish(
+                    aligned, malformed, output_path=root / "malformed-out.json"
+                )
+
+            symlink = root / "grouping-link.json"
+            symlink.symlink_to(grouping)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
+            ):
+                organizer.organize_and_publish(
+                    aligned, symlink, output_path=root / "symlink-out.json"
+                )
+
+            oversized = root / "oversized.json"
+            with oversized.open("wb") as stream:
+                stream.truncate(16 * 1024 * 1024 + 1)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_ORGANIZER_GROUPING_INVALID"
+            ):
+                organizer.organize_and_publish(
+                    aligned, oversized, output_path=root / "oversized-out.json"
+                )
+
+    def test_detects_late_mutation_and_never_overwrites_race_winner(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, grouping, _, _ = self.write_inputs(root)
+            changed_output = root / "changed.json"
+            original_verify = organizer._verify_artifact_unchanged
+
+            def mutate_then_verify(artifact):
+                if artifact.path == grouping:
+                    grouping.write_bytes(grouping.read_bytes() + b" ")
+                return original_verify(artifact)
+
+            with (
+                mock.patch.object(
+                    organizer,
+                    "_verify_artifact_unchanged",
+                    side_effect=mutate_then_verify,
+                ),
+                self.assertRaisesRegex(
+                    ValueError, "TRITRACK_ORGANIZER_INPUT_CHANGED"
+                ),
+            ):
+                organizer.organize_and_publish(
+                    aligned, grouping, output_path=changed_output
+                )
+            self.assertFalse(changed_output.exists())
+
+            aligned, grouping, _, _ = self.write_inputs(root)
+            race_output = root / "race.json"
+
+            def race_winner(_source, destination):
+                Path(destination).write_text("winner", encoding="utf-8")
+                raise FileExistsError
+
+            with (
+                mock.patch.object(os, "link", side_effect=race_winner),
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                organizer.organize_and_publish(
+                    aligned, grouping, output_path=race_output
+                )
+            self.assertEqual(race_output.read_text(encoding="utf-8"), "winner")
+            self.assertEqual(list(root.glob(".race.json.*.tmp")), [])
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_paper_edit.py b/tests/test_paper_edit.py
new file mode 100644
index 0000000..437cddd
--- /dev/null
+++ b/tests/test_paper_edit.py
@@ -0,0 +1,496 @@
+from __future__ import annotations
+
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
+from tests.task9_fixtures import invented_aligned, invented_grouping
+from tritrack_editing_assistant import organizer, paper_edit
+from tritrack_editing_assistant.contracts import validate_contract
+
+
+def write_aligned(root: Path, *, formula_text: bool = False) -> tuple[Path, bytes]:
+    root.mkdir(parents=True, exist_ok=True)
+    aligned = invented_aligned()
+    if formula_text:
+        aligned["takes"][0]["cues"][0]["text"] = "=INVENTED()"
+    encoded = (
+        json.dumps(aligned, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+    ).encode("utf-8")
+    path = root / "aligned.json"
+    path.write_bytes(encoded)
+    return path, encoded
+
+
+def write_grouping(root: Path, aligned_bytes: bytes) -> tuple[Path, bytes]:
+    grouping = invented_grouping()
+    grouping["alignedTranscriptSha256"] = hashlib.sha256(aligned_bytes).hexdigest()
+    encoded = (
+        json.dumps(grouping, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+    ).encode("utf-8")
+    path = root / "grouping.json"
+    path.write_bytes(encoded)
+    return path, encoded
+
+
+def logical_grid(path: Path) -> dict[str, list[list[object]]]:
+    workbook = load_workbook(path, data_only=False)
+    return {
+        name: [list(row) for row in workbook[name].iter_rows(values_only=True)]
+        for name in workbook.sheetnames
+    }
+
+
+class PaperExportTest(unittest.TestCase):
+    def test_exports_exact_reference_grid_and_hidden_manifest(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, aligned_bytes = write_aligned(root)
+            output = root / "paper.xlsx"
+
+            summary = paper_edit.export_workbook(
+                aligned,
+                grouping_path=None,
+                output_path=output,
+            )
+
+            workbook = load_workbook(output, data_only=False)
+            self.assertEqual(
+                workbook.sheetnames,
+                ["Cues", "Questions", "Selections", "_TriTrack"],
+            )
+            self.assertEqual(workbook["_TriTrack"].sheet_state, "hidden")
+            self.assertEqual(
+                [cell.value for cell in workbook["Cues"][1]],
+                [
+                    "TakeId",
+                    "SourceSha256",
+                    "CueId",
+                    "StartMs",
+                    "EndMs",
+                    "Text",
+                    "Disposition",
+                ],
+            )
+            self.assertEqual(workbook["Cues"].max_row, 5)
+            self.assertEqual(
+                [cell.value for cell in workbook["Cues"][2]],
+                [
+                    "A.wav",
+                    "3" * 64,
+                    "cue-000001",
+                    0,
+                    500,
+                    "Invented first answer.",
+                    "original",
+                ],
+            )
+            self.assertEqual(workbook["Questions"].max_row, 1)
+            self.assertEqual(workbook["Selections"].max_row, 1)
+            manifest = {
+                workbook["_TriTrack"].cell(row=row, column=1).value:
+                workbook["_TriTrack"].cell(row=row, column=2).value
+                for row in range(2, workbook["_TriTrack"].max_row + 1)
+            }
+            self.assertEqual(
+                manifest["WorkbookSchemaVersion"],
+                "tritrack.paper-workbook/v1",
+            )
+            self.assertEqual(
+                manifest["AlignedTranscriptSha256"],
+                hashlib.sha256(aligned_bytes).hexdigest(),
+            )
+            self.assertEqual(
+                summary,
+                {
+                    "cueCount": 4,
+                    "questionCount": 0,
+                    "selectionCount": 0,
+                },
+            )
+
+    def test_prefills_grouping_as_a_direct_projection(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, aligned_bytes = write_aligned(root)
+            grouping, _ = write_grouping(root, aligned_bytes)
+            output = root / "prefilled.xlsx"
+
+            summary = paper_edit.export_workbook(
+                aligned,
+                grouping_path=grouping,
+                output_path=output,
+            )
+
+            workbook = load_workbook(output, data_only=False)
+            self.assertEqual(
+                [cell.value for cell in workbook["Questions"][2]],
+                ["question-001", "What changed?", 1],
+            )
+            self.assertEqual(
+                [cell.value for cell in workbook["Selections"][2]],
+                [
+                    "ANSWER",
+                    "answer-001",
+                    "question-001",
+                    1,
+                    "A.wav",
+                    "cue-000001",
+                    "cue-000002",
+                    None,
+                    "Primary invented answer",
+                ],
+            )
+            self.assertEqual(
+                [cell.value for cell in workbook["Selections"][4]],
+                [
+                    "RESERVE",
+                    "reserve-001",
+                    None,
+                    1,
+                    "B.wav",
+                    "cue-000002",
+                    "cue-000002",
+                    "Alternate invented answer",
+                    "Keep available",
+                ],
+            )
+            self.assertEqual(
+                summary,
+                {"cueCount": 4, "questionCount": 2, "selectionCount": 3},
+            )
+
+    def test_formula_looking_transcript_text_is_saved_as_literal_string(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, _ = write_aligned(root, formula_text=True)
+            output = root / "literal.xlsx"
+
+            paper_edit.export_workbook(
+                aligned,
+                grouping_path=None,
+                output_path=output,
+            )
+
+            workbook = load_workbook(output, data_only=False)
+            cell = workbook["Cues"]["F2"]
+            self.assertEqual(cell.value, "=INVENTED()")
+            self.assertEqual(cell.data_type, "s")
+
+    def test_existing_output_and_missing_parent_fail_closed(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            output = root / "paper.xlsx"
+            output.write_text("winner", encoding="utf-8")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
+                paper_edit.export_workbook(
+                    root / "missing.json",
+                    grouping_path=None,
+                    output_path=output,
+                )
+            self.assertEqual(output.read_text(encoding="utf-8"), "winner")
+
+            aligned, _ = write_aligned(root)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
+            ):
+                paper_edit.export_workbook(
+                    aligned,
+                    grouping_path=None,
+                    output_path=root / "missing" / "paper.xlsx",
+                )
+
+
+class PaperApplyTest(unittest.TestCase):
+    def editable_workbook(self, root: Path) -> tuple[Path, Path, bytes]:
+        aligned, aligned_bytes = write_aligned(root)
+        workbook_path = root / "editable.xlsx"
+        paper_edit.export_workbook(
+            aligned,
+            grouping_path=None,
+            output_path=workbook_path,
+        )
+        workbook = load_workbook(workbook_path, data_only=False)
+        questions = workbook["Questions"]
+        questions.append(["question-001", "  What   changed?  ", 1])
+        questions.append(["question-002", "What comes next?", 2])
+        selections = workbook["Selections"]
+        selections.append(
+            [
+                "ANSWER",
+                "answer-001",
+                "question-001",
+                1,
+                "A.wav",
+                "cue-000001",
+                "cue-000002",
+                None,
+                "  Primary   invented answer  ",
+            ]
+        )
+        selections.append(
+            [
+                "ANSWER",
+                "answer-002",
+                "question-002",
+                1,
+                "B.wav",
+                "cue-000001",
+                "cue-000001",
+                None,
+                None,
+            ]
+        )
+        selections.append(
+            [
+                "RESERVE",
+                "reserve-001",
+                None,
+                1,
+                "B.wav",
+                "cue-000002",
+                "cue-000002",
+                " Alternate   invented answer ",
+                "  Keep   available ",
+            ]
+        )
+        workbook.save(workbook_path)
+        return aligned, workbook_path, aligned_bytes
+
+    def test_applies_normalized_edits_to_strict_grouping(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, workbook, aligned_bytes = self.editable_workbook(root)
+            output = root / "grouping.json"
+
+            grouping = paper_edit.apply_workbook(
+                aligned,
+                workbook,
+                output_path=output,
+            )
+
+            validate_contract("grouping-v1", grouping)
+            expected = invented_grouping()
+            expected["alignedTranscriptSha256"] = hashlib.sha256(
+                aligned_bytes
+            ).hexdigest()
+            self.assertEqual(grouping, expected)
+            self.assertEqual(output.read_bytes(), organizer.encode_grouping(expected))
+            encoded = output.read_text(encoding="utf-8")
+            self.assertNotIn("startMs", encoded)
+            self.assertNotIn("sourceSha256", encoded)
+            self.assertNotIn("Invented first answer.", encoded)
+
+    def test_grouping_fixpoint_and_logical_grid_idempotence(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, aligned_bytes = write_aligned(root)
+            grouping, grouping_bytes = write_grouping(root, aligned_bytes)
+            workbook = root / "prefilled.xlsx"
+            applied = root / "applied.json"
+
+            paper_edit.export_workbook(
+                aligned,
+                grouping_path=grouping,
+                output_path=workbook,
+            )
+            paper_edit.apply_workbook(aligned, workbook, output_path=applied)
+            self.assertEqual(applied.read_bytes(), grouping_bytes)
+
+            edited_aligned, edited_workbook, _ = self.editable_workbook(root / "edit")
+            normalized = root / "normalized.json"
+            paper_edit.apply_workbook(
+                edited_aligned,
+                edited_workbook,
+                output_path=normalized,
+            )
+            first = root / "first.xlsx"
+            second = root / "second.xlsx"
+            paper_edit.export_workbook(
+                edited_aligned,
+                grouping_path=normalized,
+                output_path=first,
+            )
+            paper_edit.export_workbook(
+                edited_aligned,
+                grouping_path=normalized,
+                output_path=second,
+            )
+            self.assertEqual(logical_grid(first), logical_grid(second))
+            first_applied = root / "first-applied.json"
+            second_applied = root / "second-applied.json"
+            paper_edit.apply_workbook(
+                edited_aligned, first, output_path=first_applied
+            )
+            paper_edit.apply_workbook(
+                edited_aligned, second, output_path=second_applied
+            )
+            self.assertEqual(first_applied.read_bytes(), normalized.read_bytes())
+            self.assertEqual(second_applied.read_bytes(), normalized.read_bytes())
+
+    def test_rejects_formula_reference_manifest_and_sheet_tampering(self) -> None:
+        def reject_edit(mutator, code: str) -> None:
+            with tempfile.TemporaryDirectory() as temporary:
+                root = Path(temporary)
+                aligned, workbook_path, _ = self.editable_workbook(root)
+                workbook = load_workbook(workbook_path, data_only=False)
+                mutator(workbook)
+                workbook.save(workbook_path)
+                with self.assertRaisesRegex(ValueError, code):
+                    paper_edit.apply_workbook(
+                        aligned,
+                        workbook_path,
+                        output_path=root / "grouping.json",
+                    )
+
+        reject_edit(
+            lambda workbook: setattr(
+                workbook["Questions"]["B2"], "value", "=INVENTED()"
+            ),
+            "TRITRACK_PAPER_FORMULA_FORBIDDEN",
+        )
+        reject_edit(
+            lambda workbook: setattr(workbook["Cues"]["F2"], "value", "Misleading"),
+            "TRITRACK_PAPER_REFERENCE_MISMATCH",
+        )
+        reject_edit(
+            lambda workbook: setattr(
+                workbook["_TriTrack"]["B4"], "value", "f" * 64
+            ),
+            "TRITRACK_PAPER_MANIFEST_MISMATCH",
+        )
+        reject_edit(
+            lambda workbook: workbook.create_sheet("Unexpected"),
+            "TRITRACK_PAPER_SHEETS_INVALID",
+        )
+        reject_edit(
+            lambda workbook: workbook["Selections"].merge_cells("A2:B2"),
+            "TRITRACK_PAPER_WORKBOOK_INVALID",
+        )
+
+    def test_rejects_partial_rows_bad_placement_and_foreign_spans(self) -> None:
+        def reject_selection(row, code: str) -> None:
+            with tempfile.TemporaryDirectory() as temporary:
+                root = Path(temporary)
+                aligned, _ = write_aligned(root)
+                workbook_path = root / "paper.xlsx"
+                paper_edit.export_workbook(
+                    aligned,
+                    grouping_path=None,
+                    output_path=workbook_path,
+                )
+                workbook = load_workbook(workbook_path, data_only=False)
+                workbook["Questions"].append(
+                    ["question-001", "What changed?", 1]
+                )
+                workbook["Selections"].append(row)
+                workbook.save(workbook_path)
+                with self.assertRaisesRegex(ValueError, code):
+                    paper_edit.apply_workbook(
+                        aligned,
+                        workbook_path,
+                        output_path=root / "grouping.json",
+                    )
+
+        reject_selection(
+            ["ANSWER", "answer-001", "question-001"],
+            "TRITRACK_PAPER_ROW_INVALID",
+        )
+        reject_selection(
+            [
+                "OTHER",
+                "answer-001",
+                "question-001",
+                1,
+                "A.wav",
+                "cue-000001",
+                "cue-000001",
+                None,
+                None,
+            ],
+            "TRITRACK_PAPER_ROW_INVALID",
+        )
+        reject_selection(
+            [
+                "ANSWER",
+                "answer-001",
+                "question-001",
+                1,
+                "Unknown.wav",
+                "cue-000001",
+                "cue-000001",
+                None,
+                None,
+            ],
+            "TRITRACK_ORGANIZER_TAKE_UNKNOWN",
+        )
+
+    def test_file_boundaries_late_mutation_and_publication_race(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, workbook, _ = self.editable_workbook(root)
+            symlink = root / "paper-link.xlsx"
+            symlink.symlink_to(workbook)
+            with self.assertRaisesRegex(ValueError, "TRITRACK_PAPER_WORKBOOK_INVALID"):
+                paper_edit.apply_workbook(
+                    aligned,
+                    symlink,
+                    output_path=root / "symlink.json",
+                )
+
+            invalid_zip = root / "invalid.xlsx"
+            invalid_zip.write_bytes(b"not a workbook")
+            with self.assertRaisesRegex(ValueError, "TRITRACK_PAPER_WORKBOOK_INVALID"):
+                paper_edit.apply_workbook(
+                    aligned,
+                    invalid_zip,
+                    output_path=root / "invalid.json",
+                )
+
+            output = root / "changed.json"
+            original_verify = paper_edit._verify_unchanged
+
+            def mutate_then_verify(artifact):
+                if artifact.path == workbook:
+                    workbook.write_bytes(workbook.read_bytes() + b" ")
+                return original_verify(artifact)
+
+            with (
+                mock.patch.object(
+                    paper_edit,
+                    "_verify_unchanged",
+                    side_effect=mutate_then_verify,
+                ),
+                self.assertRaisesRegex(ValueError, "TRITRACK_PAPER_INPUT_CHANGED"),
+            ):
+                paper_edit.apply_workbook(aligned, workbook, output_path=output)
+            self.assertFalse(output.exists())
+
+            aligned, workbook, _ = self.editable_workbook(root / "race-input")
+            race_output = root / "race.json"
+
+            def race_winner(_source, destination):
+                Path(destination).write_text("winner", encoding="utf-8")
+                raise FileExistsError
+
+            with (
+                mock.patch.object(os, "link", side_effect=race_winner),
+                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
+            ):
+                paper_edit.apply_workbook(
+                    aligned,
+                    workbook,
+                    output_path=race_output,
+                )
+            self.assertEqual(race_output.read_text(encoding="utf-8"), "winner")
+            self.assertEqual(list(root.glob(".race.json.*.tmp")), [])
+
+
+if __name__ == "__main__":
+    unittest.main()

```


