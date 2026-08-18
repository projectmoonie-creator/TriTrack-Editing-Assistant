# Maintainer tooling facts

This file records stable, public-safe facts needed to reproduce local
maintenance. It must not contain credentials, private paths, transient tokens,
or another project's tool state.

## Python

- Supported runtime: Python 3.12 and 3.13.
- Clean gate environments install both `pip` and `setuptools` through the
  exact `requirements/ci-constraints.txt` pins before installing `.[dev]`.
- Full tests: `python -m unittest discover -s tests -v`
- Lint: `ruff check src tests examples scripts`
- Skill validation uses the current Codex `skill-creator` validator against
  both `.agents/skills/tritrack-editing-assistant-maintainer` and
  `skills/tritrack-editing-assistant`.

## Read-only artifact validation

The installed help authorities are:

```text
tritrack validate --help
tritrack validate contract --help
tritrack validate fcpxml --help
tritrack validate paper --help
tritrack validate run --help
```

- `contract` reports `validationScope: contract` and proves only that one exact
  JSON artifact satisfies its installed registered schema.
- `fcpxml` reports `validationScope: structural-profile` and proves only the
  installed profile and title-binding structural checks. It does not probe
  source media, validate against a DTD, or launch a Final Cut GUI.
- `paper` reports `validationScope: authority-bound` and proves that the
  workbook is acceptable against the exact supplied aligned transcript bytes.
- `run` reports `validationScope: complete-run-bundle` and proves the complete
  immutable artifact set, manifest chain, contracts, and hashes agree.

All four modes are read-only. The command does not repair an artifact, guess a
format, discover sibling inputs, write a result, use network access, or broaden
success beyond its exact scope.

## Task 13 downstream seam

Task 13 keeps the process boundary deliberate: versioned artifacts plus the
installed `tritrack validate ... --json` commands are the exclusive supported
v1 integration seam. Internal Python modules are not a compatibility surface.
Use installed help as the flag authority and accept only the exact summary
schema, validation scope, contract version, and hashes the consumer knows.

The public black-box proof is:

```text
python -I examples/downstream_seam.py \
  --tritrack tritrack \
  --aligned examples/downstream_fixture/aligned-transcript.json \
  --output ABSENT_SIDECAR.json
```

`examples/downstream_seam.py` uses only the standard library. It invokes
`tritrack validate contract --json`, binds the reported hash to the exact
bytes it reads, accepts only `aligned-transcript-v1`, derives take／cue counts,
revalidates, and writes one absent `example.*` sidecar. The sidecar is
downstream-owned and never an engine contract or authority.

The release-readiness gate copies both public example files outside the source
snapshot and runs them with isolated Python and the installed CLI from a fresh
wheel-only environment. The closed manifest records `downstreamSeam: pass`.
The proof adds sdist documentation and examples but adds no wheel runtime
member, plugin hook, network service, or private integration.

## Maintainer release-readiness gate

The only maintainer entry point is:

```text
python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

The source must be one clean Git toplevel at `HEAD`. The output parent must
exist and the named output directory must be absent; an existing path or race
winner is preserved. The gate inventories every stage-zero tracked regular
file, rejects private-path／credential shapes and forbidden binary surfaces,
builds twice from separately verified `git archive` snapshots, and inspects
wheel／sdist metadata, paths, types, bounds, exact members, contents, and hashes
without generic extraction.

The gate requires byte-identical wheels. For sdists it requires identical
normalized member／content inventories while recording the chosen compressed
archive's exact SHA-256; it does not claim byte-identical gzip output. A new
external virtual environment installs only the selected local wheel, runs
`pip check`, confirms the eleven-component registry, and exercises all five
validator help authorities plus the Task 13 out-of-tree consumer.

Publication hard-links the two archives first and canonical
`release-manifest.json` last. The closed manifest contains only project
name／version／commit, tracked-source count and digest, exact toolchain and
platform facts, artifact sizes／hashes／member counts／inventory hashes, passed
gate names, reproducibility facts, and explicit non-claims. It contains no
path, time, account, host, command, log, source content, or matched value.

Public CI uses exactly Ubuntu 24.04 x64 and macOS 26 arm64 with Python 3.12
and 3.13, plus one Ubuntu 24.04／Python 3.13 quality job and one local candidate
gate job. CI and the maintainer gate do not tag, publish, upload, sign, attest,
contact testers, operate a GUI, or submit an application.

## Local synchronization

- `tritrack sync --help` is the command authority for Task 5 flags.
- Media metadata and mono float audio are read through `ffprobe` and `ffmpeg`
  using the public bounded-process wrapper. No shell command is constructed.
- The command creates one absent `sync-map-v1` JSON path atomically and never
  rewrites source media or an existing output path.

## Local FCPXML emission

- `tritrack emit --help` is the command authority for Task 6 flags.
- The command consumes one strict `sync-map-v1`, repeatable local camera A/B
  paths, the exact public compatibility profile, the public Basic Title
  binding, and caller-owned event and project names.
- Source duration, video dimensions, frame rate, Rec. 709 fields, and stereo
  48 kHz audio fields are read through the existing bounded `ffprobe` boundary
  and must match the declared profile before emission. JSON decimal timing is
  converted to rational values and quantized once to integer frames; timeline
  accumulation never uses binary floating point.
- Each paired segment enables audio only for the sync map's declared
  `audioMaster`; unpaired source segments retain their own audio.
- The command creates one absent FCPXML path atomically. It never rewrites
  source media, the sync map, an existing output, profile data, binding data,
  or caller metadata.
- Generated FCPXML contains caller-supplied local source file URIs and should
  remain under the same local-media custody as those sources.
- Automated DTD verification uses the installed FCPXML 1.14 DTD through its
  percent-encoded `file:` URI. Passing an unescaped application path containing
  spaces to `xmllint --dtdvalid` does not resolve as a DTD URI.
- A passing structural and DTD check does not claim that a Final Cut GUI import
  or round trip ran.

## Local transcription

- `tritrack transcribe --help` is the command authority for Task 7 flags.
- The caller supplies repeatable local media paths, one readable local
  whisper.cpp model, an explicit lowercase two- or three-letter language code,
  and one absent output path. TriTrack does not bundle or download a model.
- The fixed `whisper-cpp-cpu-no-fallback-v1` profile normalizes each source to
  temporary mono 16 kHz signed 16-bit PCM through bounded FFmpeg, then invokes
  `whisper-cli` exactly once with zero temperature, zero temperature increment,
  engine fallback disabled, and GPU decoding disabled. It sends no prompt,
  translation request, provider request, or network request.
- Raw engine JSON is an untrusted temporary side effect with a 16 MiB limit.
  Only the observed language, integer offsets, and cue text enter the strict
  canonicalizer. The temporary directory is removed after success or failure.
- The canonical `transcript-bundle-v1` records the fixed profile ID, sanitized
  engine version, model SHA-256, source SHA-256, stable basename-scoped take
  identities, stable cue IDs, and integer-millisecond cue timing. It records no
  absolute paths, temporary paths, logs, execution duration, or credentials.
- Input hashes are checked before and after local processing. Any media or
  model change fails closed. Output publication uses the same absent-path,
  temporary-file, hard-link race boundary as synchronization and FCPXML output.
- A final cue may exceed the decoded PCM duration by at most 5,000 ms to match
  observed whisper.cpp tail padding; only that final end is clipped to the real
  duration. Other invalid or non-monotonic timing fails closed.
- Exact `[BLANK_AUDIO]` evidence becomes an empty take only after the normalized
  PCM has independently been proven byte-zero. Non-silent empty evidence and
  any text over proven silence fail closed. This is a deterministic outcome
  rule, not a semantic claim about transcription accuracy.
- The bundle contains local transcript text and media basenames. Keep it under
  the same custody as source media. `--json` prints only counts and the bundle
  SHA-256.

## Local text alignment

- `tritrack align --help` is the command authority for the local Task 8 flags.
- The command consumes one strict `transcript-bundle-v1`, one strict
  `text-revision-v1` bound to the exact source bytes, and one absent output
  path. It makes no subprocess or network request.
- Revisions address existing take and cue IDs. Promotion preserves take IDs,
  source hashes, status, cue IDs, and integer-millisecond timing. Unknown or
  duplicate addresses, source or language mismatch, invalid normalized text,
  and attempts to edit empty takes fail closed.
- `aligned-transcript-v1` records the exact source-bundle and revision-file
  SHA-256 values. Inputs are rehashed before atomic publication. Repeating the
  operation with the same exact inputs produces identical artifact bytes.
- All three artifacts contain transcript text and remain under the same local
  custody as the source media. `--json` prints only counts and the aligned
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

## Local paper edit and organization

- `tritrack paper export --help`, `tritrack paper apply --help`, and
  `tritrack organize --help` are the command authorities for Task 9 flags.
- Export reads one strict `aligned-transcript-v1` and optionally one canonical
  `grouping-v1`, then creates one absent XLSX workbook. Apply reopens the exact
  aligned bytes and one bounded regular non-symlink workbook, re-derives every
  cue/display/manifest value, and creates one absent canonical grouping JSON.
- The workbook has exactly four worksheets: visible `Cues`, `Questions`, and
  `Selections`, plus hidden `_TriTrack`. Hidden state is a usability aid, not a
  security boundary. Formula cells anywhere in the accepted sheets fail
  closed; cell hyperlinks, external workbook links, macros, merged cells,
  defined names, and structural drift also fail closed. Formula-looking
  transcript text is stored as a literal string.
- `grouping-v1` is exact-byte bound to the aligned authority and contains only
  cue-addressed editor intent. `working-cut-v1` is exact-byte bound to both
  aligned and grouping inputs and copies source hashes and millisecond timing
  only from aligned cues. Neither artifact creates a second transcript
  authority.
- The grouping fixpoint is exact canonical JSON bytes. XLSX ZIP-byte identity
  is not promised; repeated export instead guarantees the same logical grids,
  and subsequent apply returns the same grouping bytes.
- Task 9 performs no network access, provider call, credential lookup, media
  processing, subprocess invocation, FCPXML emission, or Task 10 orchestration.
- JSON inputs are bounded to 16 MiB and compressed XLSX inputs to 64 MiB.
  Workbook ZIP preflight additionally caps 512 members, 256 MiB total expanded
  bytes, and 128 MiB per member before openpyxl parsing. Worksheet rows and
  columns are capped from the exact aligned cue count before rectangular cell
  inspection. Inputs are rehashed before temporary-file plus hard-link
  publication; existing outputs and race winners are never overwritten.

## Immutable local run workflow

- `tritrack run prepare --help`, `tritrack run align --help`,
  `tritrack run finish --help`, and `tritrack run status --help` are the
  installed command authorities for Task 10 flags.
- `prepare`, `align`, and `finish` each publish a new absent directory. A
  bundle is complete only when its canonical `run-manifest.json` is present,
  lists the exact phase-specific filenames and hashes, and chains the exact
  prior manifest hashes. Publication reserves the directory, hard-links
  artifacts, and links the manifest last. No command overwrites or repairs an
  earlier bundle.
- Prepared bundles contain doctor, sync-map, transcript-bundle, and string-out
  artifacts. Aligned bundles contain aligned-transcript and paper-workbook
  artifacts. Finished bundles contain grouping, working-cut, and story-cut
  artifacts. Manifests contain no timestamp, mutable stage status, absolute
  path, transcript text, editor text, command arguments, logs, or credentials.
- `prepare` calls the existing doctor → sync → transcribe → emit Python
  functions directly. A doctor receipt with `supported: false` stops before
  processing. Declared media basenames are globally unique, transcription
  inputs are a strict subset, and media plus model hashes are rechecked before
  publication.
- `align` requires a complete prepared bundle and one explicit
  `text-revision-v1`. `takes: []` is a valid no-change revision only when the
  editor deliberately supplies it. The emitted workbook remains transport,
  not text, timing, or selection authority.
- `finish` validates the prepared → aligned manifest chain, current media
  hashes, and workbook binding before applying paper intent, compiling the
  working cut, and rendering `story-cut.fcpxml`. Story order, cue text, timing,
  source hashes, sync offsets, and audio-master coverage are re-derived from
  exact strict artifacts; reserve does not enter the active timeline.
- `status` is read-only and reports only run ID, phase, next action, completed
  stage names, and logical artifact hashes. Task 10 makes no network access and
  does not claim a Final Cut GUI import, DTD result, or round trip.
- `skills/tritrack-editing-assistant/SKILL.md` is the separate end-user entry
  point. It uses installed help first and preserves explicit text-revision and
  paper-edit human gates; the repository-local maintainer skill retains all
  development and publication authority.

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
GUI evidence. Local Task 6.5 acceptance additionally runs:

```bash
venv/bin/python -m unittest tests.test_quickstart_demo -v
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples
venv/bin/python -m compileall -q src tests examples
```

## Final Cut Pro verification target

The current compatibility evidence targets:

- application: `/Applications/Final Cut Pro.app`
- bundle identifier: `com.apple.FinalCut`
- version: `12.3`

A separately installed subscription application may register bundle identifier
`com.apple.FinalCutApp`. It is outside the current compatibility evidence.
Never rely on Finder's default file association. For GUI verification, launch
the declared application explicitly by exact bundle identifier or exact
application path, and record that identity in the evidence.

The product doctor reads only the declared perpetual application bundle and
its installed FCPXML DTD. A successful version check does not claim that a GUI
round trip ran; manual Final Cut evidence remains a separate artifact.

## Public remote custody

- Authorization follows the capability-scoped standing-grant model in
  `AGENTS.md`; unchanged authorized actions are not re-approved per task.
- Public `origin`:
  `https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`
- After a coherent package is green, the standing authorization permits a
  fast-forward `main` push to this existing public `origin` and exact remote-SHA
  verification as the off-device Git backup.
- Remote changes, visibility changes, force-push, tags, releases, pull requests,
  tester contact, package publication, and application submission have not yet
  been granted. If later granted for an unchanged scope, that grant persists
  until revoked.
