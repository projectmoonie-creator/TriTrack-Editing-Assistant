# Task 10 immutable run-workflow decision

Decision date: 2026-08-17

Decision owner: producer

Selected option: A — immutable explicit stage bundles with final story FCPXML

## Decision

Task 10 implements the installed `tritrack run` surface as three explicit,
immutable transitions plus one read-only status command:

```text
prepare -> human text-revision gate -> align
        -> human paper-edit gate -> finish -> story-cut FCPXML
```

Every mutating transition publishes a new absent directory. It never changes a
prior bundle, source artifact, workbook, manifest, or result. A bundle is
complete only when its manifest is present and validates every fixed artifact
name and exact byte hash. Ordinary failures remove the unpublished staging
directory. A process crash may leave an incomplete reserved output directory;
the runner never repairs or overwrites it.

`run-manifest-v1` is workflow receipt and index authority only. It is not
transcript, cue timing, grouping, working-cut, media, workbook, or FCPXML
authority. Those roles remain with their existing strict artifacts.

## Public command surface

### Prepare

```text
tritrack run prepare \
  --camera-a A-001.MP4 [--camera-a ...] \
  --camera-b B-001.MP4 [--camera-b ...] \
  --transcribe-media A-001.MP4 [--transcribe-media ...] \
  --model ggml-model.bin \
  --language en \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --binding basic-title-v1 \
  --event-name "Interview" \
  --project-name "Synchronized string-out" \
  --run-id interview-001 \
  --output prepared-run \
  [--json]
```

`prepare` requires globally unique source basenames. Every transcribed path
must be one of the declared camera sources. It performs the exact installed
doctor, synchronization, fixed local transcription, and synchronized
string-out operations through product Python functions, not a shell or nested
CLI. The doctor receipt must report `supported: true` before later engines run.

The absent bundle contains exactly:

- `doctor.json`;
- `sync-map.json`;
- `transcript-bundle.json`;
- `string-out.fcpxml`; and
- `run-manifest.json`.

The published manifest reports `nextAction: provide-revision`. The editor or
terminal-capable agent then authors one strict `text-revision-v1` bound to the
exact transcript bytes. Task 10 permits `takes: []` as an explicit no-change
approval; it does not silently infer approval.

### Align

```text
tritrack run align \
  --prepared prepared-run \
  --revision text-revision.json \
  --output aligned-run \
  [--json]
```

`align` validates the complete prepared bundle and the strict revision before
writing. It invokes the existing alignment core and exports the Task 9 paper
workbook from the exact aligned bytes.

The absent bundle contains exactly:

- `aligned-transcript.json`;
- `paper-edit.xlsx`; and
- `run-manifest.json`.

The manifest binds the exact prepared-manifest and revision hashes and reports
`nextAction: edit-paper-workbook`. The workbook remains a transport only. The
editor changes only the Task 9 `Questions` and `Selections` tables.

### Finish

```text
tritrack run finish \
  --prepared prepared-run \
  --aligned aligned-run \
  --workbook edited-paper.xlsx \
  --camera-a A-001.MP4 [--camera-a ...] \
  --camera-b B-001.MP4 [--camera-b ...] \
  --event-name "Interview" \
  --project-name "Story cut" \
  --output finished-run \
  [--json]
```

`finish` validates both earlier bundles and their manifest chain, rehashes the
caller-supplied media against the prepared source set, applies the workbook to
canonical `grouping-v1`, compiles `working-cut-v1`, and renders a deterministic
story-ordered FCPXML from the exact sync map, aligned transcript, grouping,
working cut, and local media.

The absent bundle contains exactly:

- `grouping.json`;
- `working-cut.json`;
- `story-cut.fcpxml`; and
- `run-manifest.json`.

The manifest reports `nextAction: complete`. It does not claim a Final Cut GUI
import, DTD validation, or round trip.

### Status

```text
tritrack run status --run prepared-run [--json]
```

`status` is read-only. It validates one complete bundle, fixed names, exact
artifact hashes, strict manifest semantics, and supported artifact contracts
where applicable. It emits only run ID, phase, next action, stage names, and
artifact logical names／hashes. It does not print paths, transcript text,
question text, notes, or FCPXML content.

## `run-manifest-v1`

The unused pre-release schema is tightened in place. Canonical bytes are UTF-8
JSON with sorted keys, two-space indentation, and one final newline. The
manifest contains:

- closed schema and tool versions;
- a safe caller-owned `runId`;
- exact public profile and title-binding IDs;
- `phase`: `prepared`, `aligned`, or `finished`;
- `nextAction`: `provide-revision`, `edit-paper-workbook`, or `complete`;
- `manifestChain`: the ordered SHA-256 values of prior manifests;
- a sorted path-free source list with camera, basename media ID, exact source
  SHA-256, and whether that source was transcribed;
- a closed artifact map whose entries contain a fixed safe filename and exact
  SHA-256; and
- completed stage records with closed names plus exact input and output hash
  maps.

There are no timestamps, mutable statuses, absolute paths, command arguments,
logs, durations, transcript text, editor text, or credentials. An immutable
manifest describes only completed work; `planned`, `running`, and `failed`
states therefore do not belong in the contract.

The phase-specific artifact sets are exact:

- prepared: doctor receipt, sync map, transcript bundle, string-out FCPXML;
- aligned: aligned transcript and paper workbook;
- finished: grouping, working cut, and story-cut FCPXML.

The aligned manifest chain contains the prepared manifest hash. The finished
chain contains the prepared and aligned manifest hashes in that order.

## Final story projection

The story renderer never trusts copied timing or text:

1. Reopen and hash the exact aligned, grouping, and working-cut artifacts.
2. Require `working-cut-v1` to bind the exact aligned and grouping bytes.
3. Re-derive every story segment's take, cue range, source hash, start/end
   milliseconds, question membership, and `storyOrder` from the aligned and
   grouping authorities.
4. Match each selected take ID to one globally unique source basename and
   require the current source bytes to match the recorded source SHA-256.
5. Quantize cue boundaries once to the declared integer-frame profile.
6. For paired sources, use the sync-map offset to layer both intersecting
   camera clips. Require the declared audio-master clip to cover the complete
   selected interval; otherwise fail closed. Unpaired selections retain their
   own audio.
7. Concatenate only the selected authoritative cue text into the public Basic
   Title for that story segment. The FCPXML is a rendered output, not a new
   transcript authority.
8. Validate the resulting FCPXML against the existing strict public profile
   and Basic Title binding, then publish only to an absent path.

Reserve ranges do not enter the active story timeline. Segment order is the
exact `storyOrder` permutation. No semantic classification, retiming, cue
splitting, angle choice, effect design, or title-layout invention occurs.

## Bundle publication and resume boundary

Each transition builds under a hidden sibling staging directory. After every
component succeeds and all inputs are rehashed, it atomically reserves the
absent destination directory and links the fixed staged files into it with the
manifest last. On an ordinary error it removes only files and directories
created by that invocation. It never removes or modifies caller input.

The manifest-last rule makes an interrupted bundle mechanically incomplete.
No command infers or reconstructs a missing manifest from nearby artifacts.
Resume always means consuming a complete immutable prior bundle and publishing
a new absent bundle.

## End-user skill boundary

`skills/tritrack-editing-assistant/SKILL.md` is an installed editing co-pilot
entry point. It:

- checks installed `tritrack ... --help` before naming flags;
- helps the editor choose source roles, transcription inputs, run ID, and
  absent output directories;
- invokes only the public installed commands;
- explains the two human gates and never authors silent approval;
- treats the workbook as transport and JSON as authority;
- reads only sanitized command summaries and local artifacts the editor puts
  in scope; and
- stops on a compatibility, custody, overwrite, or strict-artifact failure.

It contains no maintainer task numbers, branch or release state, standing
grants, tester strategy, private repository references, private workflow
knowledge, credentials, or publication authority. The maintainer skill remains
the only development and release entry point.

## Stable failure boundaries

Task 10 uses `TRITRACK_RUN_*` for manifest, bundle, source-set, stage, and
workflow errors; `TRITRACK_STORY_*` for story projection errors; and existing
component error codes when a component itself rejects input. CLI mapping keeps
the established exit classes:

- malformed command intent: usage;
- invalid schema, manifest chain, hashes, source identity, workbook state, or
  story semantics: data;
- unsupported doctor result or missing processing dependency: dependency／
  policy as already classified;
- unreadable input or missing parent: I/O;
- existing output or publication race: output-exists; and
- no failure prints a traceback or sensitive content.

## Deferred alternatives and non-goals

- one mutable project directory or mutable manifest;
- automatic resume by scanning nearby files;
- a general DAG or plugin workflow engine;
- live provider transport, upload, deletion, credentials, or model selection;
- implementation of the planned `validate` command;
- workbook or manifest authority over transcript, timing, or editor intent;
- Final Cut GUI automation or unrecorded import claims;
- Task 11 release CI, tags, releases, pull requests, tester contact, package
  publication, or private downstream integration.

## Verification target

Acceptance preserves observed RED-to-GREEN evidence for the manifest contract,
explicit no-change revision, pure story projection, exact authority rebinding,
frame quantization, paired／unpaired audio behavior, bundle loading and
publication, every phase transition, CLI help／exit behavior, sanitized status,
and the maintainer／end-user skill firewall.

Closeout additionally requires focused and full tests, Ruff, compilation,
project identity, both skill validations, public-boundary tests,
`git diff --check`, installed CLI acceptance with invented inputs, deterministic
repeat outputs, closeout review with bounded fix-forward, minimal CI, and exact
public remote-main SHA backup verification.

## Brainstorm provenance

The frozen public problem packet SHA-256 was
`80af43be795fc7638b7ecd49c26b6f7525ab7e97239f9d9b71b804caf0cf06c5`.

Codex completed its independent first round before reading external outputs.
Gemini requested, observed, and completed `gemini-3.7-flash`; its response
SHA-256 was
`18a1d0ce36cdae9c6c192116a30d5f233812ce60fe82ddc91a4ad39db183904c`.
Claude requested the dynamic `opus` capability alias through the approved
subscription-only wrapper. Attempt
`2dcf4cdb-6654-4a29-8fd7-f4131fa9f1f4` timed out with no observed or completed
model and ambiguous request state; it remains explicitly incomplete with no
retry or billing fallback. The producer selected option A on 2026-08-17.
