# Task 12 Codex post-fix review round 1

## Review identity

- Review target: `08fb19e45cf02f747ad7b3b9bf11e726d37262e5`
- Frozen packet: `task12-alpha-review-packet-post-fix-2026-08-18.md`
- Packet SHA-256:
  `7257902b13826e7be1c6b6e5cfaa883857fbbe618d05a135870db20603e4cc1b`
- Independence: no external post-fix review was requested or read for this
  target.

## Summary

One major finding. The two original Task 12 findings are fixed and their three
regressions pass, but the same bounded-regular-file invariant has one remaining
cross-module POSIX special-file gap.

## Finding

### T12-CX-PF1-001 — major — high confidence

- Current locations: descriptor readers beginning at
  `src/tritrack_editing_assistant/align_text.py:42`,
  `emit_fcpxml.py:46`, `organizer.py:403`, `paper_edit.py:79`,
  `run_workflow.py:216`, `story_fcpxml.py:632`,
  `validate_artifacts.py:27`, and `scripts/release_gate_core.py:247`, `:581`,
  and `:1170`.
- Failure mechanism: each path is opened with blocking `O_RDONLY` before
  `fstat` decides whether it is a regular file. On POSIX, opening a FIFO for
  reading with no writer blocks indefinitely. The code therefore never reaches
  its regular-file rejection, byte limit, stable error, or command timeout.
- Impact: a caller-selected named pipe can hang validator, authority, run, or
  maintainer-gate input inspection despite the documented bounded regular-file
  boundary. This is local denial of service and prevents deterministic failure.
- Smallest safe fix: add `O_NONBLOCK` where available to every descriptor-based
  read-only input open before `fstat`. Regular-file behavior is unchanged;
  FIFOs open without waiting and are immediately rejected by the existing mode
  check. Do not add it to directory-fsync descriptors.
- Regression: assert representative runtime and release-gate descriptor opens
  request `O_NONBLOCK`, and use a FIFO subprocess case to prove validation exits
  through its stable error instead of reaching timeout. Run the full suite and
  exact release gate after the mechanical sweep.

## Inspection record

Inspected the exact fix-forward diff, both corrected loaders, their RED／GREEN
tests, the complete descriptor-open inventory in packaged runtime and release
gate code, the 243-test result, and the exact new release manifest. The
post-fix target release gate passed, but that does not exercise a FIFO input.
