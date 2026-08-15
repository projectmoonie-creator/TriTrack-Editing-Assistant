# TriTrack Editing Assistant

TriTrack Editing Assistant is a local-first command-line project for building
editable Final Cut Pro interview workflows from local A/B-camera media. It is
designed for editors working with a terminal-capable agent while keeping story
decisions with the editor.

> Development scaffold: `0.1.0a0` currently exposes the component registry,
> the fail-closed `doctor` command, local audio-verified `sync`, fixed-profile
> local `transcribe`, deterministic cue-addressed `align`, offline receipt-only
> `hybrid`, profile-bound deterministic `emit`, strict `paper export`／
> `paper apply`, and deterministic `organize`. Remaining editing commands are
> listed as `planned` and deliberately return a non-success status until their
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

The default workflow is intended to operate without a network call or paid
model. The implemented optional `hybrid` command only validates existing
provider receipts offline; it performs no request, upload, deletion,
subprocess, credential lookup, or network access. No live provider transport is
operational in this scaffold.

Do not place production clips, transcripts, credentials, private home paths,
or proprietary title templates in this repository or in a public issue.

## Development installation

This repository currently supports source installation for development:

```bash
python3.13 -m venv venv
venv/bin/pip install -e '.[dev]'
venv/bin/tritrack components --json
```

Run the implemented compatibility preflight with:

```bash
venv/bin/tritrack doctor \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --json
```

The command reports sanitized dependency and compatibility checks. It does not
claim that a manual Final Cut import occurred.

Run local A/B synchronization with one repeatable flag per source:

```bash
venv/bin/tritrack sync \
  --camera-a A-001.MP4 \
  --camera-a A-002.MP4 \
  --camera-b B-001.MP4 \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --output results/sync-map.json
```

The output path and its parent directory must already be absent and present,
respectively. The command reads local metadata and audio through bounded
`ffprobe`/`ffmpeg` argv calls, validates `sync-map-v1`, and publishes the map
atomically without modifying source media or overwriting an existing result.

Emit a deterministic string-out from that strict map with the same repeatable
source set:

```bash
venv/bin/tritrack emit \
  --camera-a A-001.MP4 \
  --camera-a A-002.MP4 \
  --camera-b B-001.MP4 \
  --sync-map results/sync-map.json \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --binding basic-title-v1 \
  --event-name "Invented Interview" \
  --project-name "Invented String-out" \
  --output results/string-out.fcpxml
```

The source basenames must exactly match the camera-specific media IDs in the
map, including its unpaired entries. The command validates the public schema,
profile, and title binding; checks the declared source video and audio profile
through the bounded probe boundary; honors each pair's `audioMaster`; quantizes
timing once to integer frames; and creates one absent FCPXML path atomically.
It does not mutate its inputs or overwrite a race winner. The FCPXML contains
local source file URIs and should remain under the same custody as the source
media. Automated FCPXML 1.14 DTD validation does not claim that a Final Cut GUI
import or round trip ran.

Run one fixed local whisper.cpp transcription pass with one repeatable flag per
source:

```bash
venv/bin/tritrack transcribe \
  --media A-001.MP4 \
  --media A-002.MP4 \
  --model models/ggml-model.bin \
  --language zh \
  --output results/transcript-bundle.json \
  --json
```

The model is caller-owned and is never bundled or downloaded by TriTrack. The
command normalizes each source to temporary mono 16 kHz PCM, runs the installed
`whisper-cli` once per take with the fixed
`whisper-cpp-cpu-no-fallback-v1` profile, and creates one absent strict
`transcript-bundle-v1` path atomically. Media basenames must be unique and the
two- or three-letter language code must be explicit. CPU-only decoding removes
the local GPU backend as a profile variable; it does not claim bit-identical
inference across engine versions, models, or machines.

Recognized cues are NFC-normalized, single-spaced, ordered, and bounded to
integer milliseconds. A bounded final whisper.cpp timestamp pad is clipped to
the real PCM duration. Exact digital silence may produce an empty take; the
observed `[BLANK_AUDIO]` engine sentinel is discarded only after the PCM has
independently been proven all-zero. Non-silent empty output, text over proven
silence, malformed timing, leaked control tokens, or repeated structural
artifacts fail closed without publishing. No retry ladder, prompt, translation,
provider call, upload, or network access is part of this command.

The bundle contains transcript text and source basenames, so keep it under the
same local custody as the media. `--json` prints only a path-free completion
summary and bundle hash; it does not print transcript text.

Promote strict cue-addressed revisions without changing source timing:

```bash
venv/bin/tritrack align \
  --transcript results/transcript-bundle.json \
  --revision results/text-revision.json \
  --output results/aligned-transcript.json \
  --json
```

The `text-revision-v1` file binds its changes to the SHA-256 of the exact source
bundle bytes and addresses existing take and cue IDs. The command preserves
take IDs, source hashes, status, cue IDs, and integer-millisecond timing;
unmentioned cues retain their original text. Empty takes cannot be revised.
The absent output is a deterministic `aligned-transcript-v1` artifact bound to
both exact input hashes. The source, revision, and aligned artifacts all contain
transcript text and remain under local-media custody.

Validate already-produced Gemini evidence before promoting the same revision:

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

Export an editor-facing workbook from the strict aligned authority:

```bash
venv/bin/tritrack paper export \
  --aligned results/aligned-transcript.json \
  --output results/paper-edit.xlsx \
  --json
```

Add `--grouping results/grouping.json` to prefill a workbook from existing
canonical editor intent. The XLSX file is a transport, not an authority. Its
complete `Cues` reference grid and hidden public-safe manifest bind it to the
exact aligned bytes. Formula cells, reference/display changes, unexpected
sheets, macros, external links, merged cells, and structural drift fail closed.
Formula-looking transcript text is exported as a literal display string.

After editing only the `Questions` and `Selections` tables, apply the workbook
back to strict JSON authority:

```bash
venv/bin/tritrack paper apply \
  --aligned results/aligned-transcript.json \
  --workbook results/paper-edit.xlsx \
  --output results/grouping.json \
  --json
```

The resulting `grouping-v1` contains cue addresses and normalized editor text,
but no transcript text, source hash, or millisecond timing. Compile it into a
deterministic text-free working cut with timing copied only from the exact
aligned authority:

```bash
venv/bin/tritrack organize \
  --aligned results/aligned-transcript.json \
  --grouping results/grouping.json \
  --output results/working-cut.json \
  --json
```

All three Task 9 operations are local-only and make no network, provider,
credential, media-processing, subprocess, FCPXML, or orchestration request.
Every output path must be absent.

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
6. Use `tritrack paper export` then `tritrack paper apply` to author durable
   cue-addressed grouping intent through a non-authoritative workbook.
7. Use `tritrack organize` to compile that intent into a deterministic
   text-free working cut.
8. Use `tritrack components --json` to inspect what is implemented before
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
| 6 | `organizer.py` | `tritrack organize` | implemented |
| 7 | `paper_edit.py` | `tritrack paper` | implemented |
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
