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

## Local-only custody

No public remote exists at this stage. Do not create one, push, tag, publish,
or contact testers without the explicit outward-action approval gate.
