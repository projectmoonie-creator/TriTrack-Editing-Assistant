# Task 6.5 public verification

Date: 2026-08-14

Implementation candidate:
`8dae7719374e4e653130c0830d78dbcb2d687002`

Branch: `codex/task6-5-public-demo-readiness`

This report records sanitized, invented-content evidence for the bounded
quickstart and minimal-CI slice. It contains no generated media, generated XML,
credentials, local home paths, or production data.

## TDD evidence

The first focused RED command was:

```bash
venv/bin/python -m unittest tests.test_quickstart_demo -v
```

All seven initial tests failed because the public
`examples/quickstart_demo.py` entry point did not exist. The failing behaviors
were the documented one-command entry, installed `sync`／`emit` orchestration,
byte-identical repeat emission, output-root and race no-overwrite behavior,
profile rejection, XML-sensitive metadata escaping, and tracked-surface safety.

The first real installed-tool run then found one additional compatibility gap:
libx264 output carried the Rec. 709 matrix but omitted transfer and primaries
from the probed stream. A focused VUI recipe test was observed RED before the
single source fix added the exact x264 Rec. 709 VUI parameters. The final
focused result was 8／8 GREEN.

## Automated gates

- Task 6.5 focused tests: 8／8 passed.
- Task 5 and Task 6 synchronization, string-out, emission, and CLI regressions:
  31／31 passed.
- Complete Python suite: 77／77 passed.
- Maintainer boundary suite: 9／9 passed.
- Ruff over `src`, `tests`, and `examples`: passed.
- Python compilation over `src`, `tests`, and `examples`: passed.
- Project identity: `public-engine`, lane `OSS`, accepted.
- Maintainer skill validation: `Skill is valid!`.
- Installed `components --json`, `doctor --help`, `sync --help`, and
  `emit --help`: passed; the registry remained eleven components.
- `git diff --check`: passed.

## Real invented quickstart

One fresh absent-root run exercised the installed `ffmpeg`, `ffprobe`,
`tritrack sync`, `tritrack emit`, and `xmllint` surfaces. Its sanitized result
reported:

- strict profile `uhd-2997-ndf-fcpxml-1.14`;
- public title binding `basic-title-v1`;
- one audio-verified A/B pair;
- byte-identical output from two distinct absent FCPXML paths;
- passing packaged profile and XML-structure validation; and
- passing installed FCPXML 1.14 DTD validation.

The real `doctor` receipt reported the declared Darwin／arm64 environment,
Python 3.13.15, FFmpeg／FFprobe 7.1, Final Cut Pro 12.3, the installed DTD, the
profile, and the title binding as supported. The run did not open Final Cut and
does not claim a GUI import or round trip.

## Public boundary

Generated sources and results remained in an untracked temporary output root.
The tracked quickstart, test, CI, and documentation surfaces passed credential,
project-name, local-home-path, and generated-output scans. No provider call,
upload, tag, release, pull request, tester contact, package publication, or
application submission occurred.
