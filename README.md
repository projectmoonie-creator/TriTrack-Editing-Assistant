# TriTrack Editing Assistant

TriTrack Editing Assistant is a local-first command-line project for building
editable Final Cut Pro interview workflows from local A/B-camera media. It is
designed for editors working with a terminal-capable agent while keeping story
decisions with the editor.

> Development scaffold: `0.1.0a0` currently exposes the component registry,
> the fail-closed `doctor` command, and local audio-verified `sync`. Remaining
> editing commands are listed as `planned` and deliberately return a
> non-success status until their implementation and tests land. There is no
> public release yet.

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
model. Media must remain local unless an editor later invokes a separately
documented optional provider adapter with explicit off-device-audio consent,
their own credential, and an exact provider model. No such provider path is
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

## Eleven-component roadmap

The component registry is the machine-readable source for current status:

```bash
tritrack components --json
```

| # | Component | Public command | Current status |
| ---: | --- | --- | --- |
| 1 | `sync_scan.py` | `tritrack sync` | implemented |
| 2 | `emit_fcpxml.py` | `tritrack emit` | planned |
| 3 | `transcribe_takes.py` | `tritrack transcribe` | planned |
| 4 | `string_out.py` | `tritrack emit` | planned |
| 5 | `hallucination.py` | `tritrack transcribe` | planned |
| 6 | `organizer.py` | `tritrack organize` | planned |
| 7 | `paper_edit.py` | `tritrack paper` | planned |
| 8 | `align_text.py` | `tritrack align` | planned |
| 9 | `gemini_hybrid.py` | `tritrack hybrid` | planned, optional |
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
