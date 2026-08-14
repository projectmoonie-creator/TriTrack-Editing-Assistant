# Task 6.5 public session handoff

This packet opens the next public-maintenance session for the bounded
demonstration slice between Tasks 6 and 7. It is repository state, not private
coordination memory. Resolve all paths from the current Git toplevel and do not
copy local absolute paths into tracked files or evidence.

## Session opener

Start the next session with:

```text
$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 6.5
```

Then provide this instruction:

```text
Resume only the public TriTrack Editing Assistant repository and its Git
history. Read the repository-local maintainer skill completely, run its
project identity validator, and fail closed unless projectId is
tritrack-editing-assistant, projectKind is public-engine, and lane is OSS.
Do not read another checkout, a private repository, production media, or
prior-session memory.

Task 6 base candidate is
242e8b5406e92049ce60c654c3c8fca11be4b596. Continue only on
codex/task6-5-public-demo-readiness, confirm that the worktree is clean or
contains only the documented Task 6.5 handoff commit, and confirm the branch
descends from that candidate. Active task is Task 6.5: build the smallest
public invented-media quickstart from A/B synchronization through strict
sync-map-v1 and deterministic profile-bound FCPXML emission, with minimal CI
and public-safe verification evidence. Follow RED then GREEN TDD and preserve
reproducible RED evidence before production implementation.

Closeout review, ordinary in-scope fix-forward, fast-forward integration of a
fully green candidate, push of main to the existing public origin, and exact
remote-SHA backup verification are standing grants. Do not ask again for
those unchanged actions. Force-push, remote changes, tags, GitHub releases,
pull requests, tester contact, package publication, and application submission
remain outside this task and are not authorized by this handoff.
```

The repository-owned `agents/openai.yaml` prompt remains generic on purpose.
Temporary task state belongs in this handoff, `STATUS.md`, and
`docs/ROADMAP.md`, not in the installed skill interface.

## Frozen public state

- Task 6 base candidate:
  `242e8b5406e92049ce60c654c3c8fca11be4b596`.
- Working branch: `codex/task6-5-public-demo-readiness`.
- Tasks 1–6 are complete. Task 7 remains next after this bounded slice.
- Implemented commands are `components`, `doctor`, `sync`, and `emit`.
- Public profile: `uhd-2997-ndf-fcpxml-1.14`.
- Public title binding: `basic-title-v1`.
- Synchronization contract: strict `sync-map-v1`.
- Release state: public pre-release source; no public tag or package release.

Do not treat this base SHA as the future Task 6.5 candidate SHA. Read back the
actual branch tip after implementation and record its full SHA at closeout.

## Task 6.5 objective

Make the already implemented Task 5 and Task 6 path understandable and
reproducible by a new public user in roughly one minute of interaction:

1. generate or prepare only invented local A/B media under an ignored,
   caller-selected absent demo directory;
2. invoke the installed public synchronization surface to create one strict
   `sync-map-v1`;
3. invoke the installed public emission surface to create one deterministic
   FCPXML 1.14 string-out;
4. validate the map, declared compatibility profile, generated XML structure,
   and the locally installed FCPXML 1.14 DTD when that declared application is
   available; and
5. print a concise success/failure summary without publishing media or output.

The demo must exercise the installed command surface. It must not bypass the
public CLI by recreating synchronization or FCPXML construction inside an
example script.

## Public input and output contract

Inputs are limited to:

- invented media generated deterministically on demand, or an existing
  repository fixture already explicitly cleared for public use;
- the packaged `uhd-2997-ndf-fcpxml-1.14` compatibility profile;
- the packaged `basic-title-v1` binding;
- caller-owned invented event and project names; and
- installed local executables already declared by `doctor`.

The generated video and audio characteristics must remain within the declared
profile: FCPXML 1.14, UHD 3840x2160, `1001/30000s`, NDF, Rec. 709, stereo, and
48 kHz. Choose the shortest invented clips that reliably exercise the current
public synchronization contract; do not weaken production thresholds merely
to make the example pass.

Outputs live only below one caller-selected directory that did not exist
before invocation. They may include invented source media, a strict sync map,
one FCPXML string-out, and sanitized verification output. Publication must be
atomic. An existing output root or a race winner must cause a controlled
failure without overwrite.

The demo, tests, documentation, and CI must not track generated media,
generated XML containing local source URIs, credentials, production data,
private repository names, or local absolute paths.

## First RED tests

Create `tests/test_quickstart_demo.py` before
`examples/quickstart_demo.py`, then run:

```text
venv/bin/python -m unittest tests.test_quickstart_demo -v
```

Observe and preserve failures proving these behaviors are initially absent:

1. the documented one-command quickstart entry point does not yet exist;
2. an invented A/B run produces a schema-valid `sync-map-v1` and a
   profile-bound FCPXML output through the installed `sync` and `emit`
   commands;
3. emitting twice from the same invented sources into two distinct absent
   output paths produces byte-identical XML;
4. an existing demo output root and a publication race both fail closed
   without modifying the winner;
5. malformed or profile-incompatible invented input is rejected rather than
   silently normalized;
6. XML-sensitive invented metadata is escaped correctly end to end; and
7. the tracked example, fixture recipe, CI configuration, and documentation
   contain no generated media, credentials, private names, or local absolute
   paths.

Keep external-tool integration separate from unit behavior. Unit tests must be
deterministic and may use the repository's existing bounded-process seams.
One local acceptance run must exercise the real installed `ffmpeg`, `ffprobe`,
`xmllint`, `tritrack sync`, and `tritrack emit` surfaces. A GitHub runner must
not claim local Final Cut DTD evidence when that application is absent.

Record the focused RED command, failing test names, and the missing-behavior
reason before adding production code. Do not retain raw terminal logs that
contain machine paths; normalize the evidence in the closeout report.

## Anticipated file surface

Confirm names with the RED tests before implementation. The expected bounded
surface is:

- `examples/quickstart_demo.py` as the public example entry point;
- `tests/test_quickstart_demo.py` for focused Task 6.5 behavior;
- `.github/workflows/ci.yml` for supported Python tests, Ruff, and
  compilation;
- `README.md` for the quickstart and a three-choice entry guide;
- `docs/TOOLING.md` for reproducible local demo and verification commands;
- `CHANGELOG.md`, `STATUS.md`, and `docs/ROADMAP.md` only after the coherent
  package is GREEN; and
- the component registry only if its existing statuses change. Supporting
  demo and CI work must not create a twelfth component.

Do not add an updater, CapCut path, Shorts/Reels workflow, effect library,
analytics, provider call, upload, package publisher, or end-user skill in this
slice. Task 7 transcription and Task 10 onboarding remain separate.

## Verification evidence

Before declaring a Task 6.5 candidate, run and report:

- focused Task 6.5 tests, including the preserved RED-to-GREEN result;
- Task 5 synchronization regression tests;
- Task 6 string-out, emission, and CLI regression tests;
- the complete Python test suite;
- Ruff across every changed Python surface;
- Python compilation across source, tests, and examples;
- maintainer boundary tests;
- the project identity validator;
- maintainer skill validation using the validator named in
  `docs/TOOLING.md`;
- installed `components --json`, `doctor --help`, `sync --help`, and
  `emit --help` checks;
- one real invented quickstart run in a fresh ignored output location;
- strict sync-map schema, compatibility profile, XML structure, and available
  installed FCPXML 1.14 DTD validation;
- package/build checks only if packaging metadata changes;
- `git diff --check`; and
- exact changed-file, Git status, branch, candidate SHA, local `main` SHA,
  remote `main` SHA, and ancestry readback.

Do not update public completion status until all applicable gates are GREEN.
Ordinary findings are fixed forward under the standing closeout grant; add a
reproducing RED test before each behavioral bug fix.

## Release and application boundary

Task 6.5 prepares public proof; it does not itself create a tag, GitHub
release, package publication, or application submission. A later session can
use the green demo, CI result, candidate SHA, and release notes as evidence.
When one of those outward capabilities is explicitly granted for the current
public target and risk, record it as a standing grant and do not ask for the
same authorization again.
