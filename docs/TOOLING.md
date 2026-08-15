# Maintainer tooling facts

This file records stable, public-safe facts needed to reproduce local
maintenance. It must not contain credentials, private paths, transient tokens,
or another project's tool state.

## Python

- Supported runtime: Python 3.12 or newer.
- Full tests: `python -m unittest discover -s tests -v`
- Lint: `ruff check src tests`
- Skill validation uses the current Codex `skill-creator` validator against
  `.agents/skills/tritrack-editing-assistant-maintainer`.

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
