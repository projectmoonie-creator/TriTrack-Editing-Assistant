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
