# Task 14 amendment v2 verification

Verification date: 2026-08-22

## Scope and intake

This public fix-forward consumes only the hash-bound clean-room amendment
`task13-parity-v2`, based on public commit
`1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`. It amends
`task13-parity-v1` and supersedes that handoff's
`contracts/voice-activity-default.md`. All six declared payload SHA-256 values
were checked before use and are recorded in
`docs/TASK-14-AMENDMENT-V2-DECISION.md`. No private repository, source media,
transcript, receipt, identifier, or path was read.

## Implemented guards and evidence

- The existing in-cue invention guard remains unchanged and green.
- `sparse_source.py` independently implements the public density verdict and
  one source-choice ladder. It counts Unicode letters, numbers, and symbols;
  uses exact media milliseconds; applies the strict-below 1.0 character／second
  rule only at 30 seconds or longer; and does not guess for unknown durations.
- Both the retry trigger and selected-source adoption call that policy. A
  sparse primary yields to a usable declared alternative, survives when no
  source is better, and an invalid primary never survives.
- `transcription-report-v2` records every attempted source's exact duration and
  character count, readable density, sparse verdict, selected source,
  thresholds, settings, retry／rescue／unrescued counts, and shared-alternative
  warnings without cue text or local paths.
- `transcription-result-manifest-v2` binds the unchanged
  `transcript-bundle-v1`, report v2, and deterministic human-readable
  `transcription-density.txt`. New prepared runs carry all four artifacts in
  `run-manifest-v3`; exact v1 result and v1／v2 run readers remain supported.
- Voice activity remains `off`. No VAD switch, model path, model pin, download,
  provider call, upload, or network boundary was added.

## TDD and local verification

RED checkpoints were observed before each implementation seam: the missing
hash-bound amendment decision, missing sparse policy module, absent exact
duration, unknown report／result schemas, sparse primary not retried, adoption
not using the shared policy, shared alternatives rejected across takes,
missing density artifact, and unknown run manifest v3. The corresponding
focused suites passed after each minimal change.

The first complete-suite run after implementation passed 333 of 334 tests and
failed only the closed distribution inventory, which correctly detected the
new package members. Final clean verification results and artifact hashes are
recorded below after the inventory is updated.

## Claude convergence supplement

The exact frozen Task 14 packet remained byte-identical at SHA-256
`c9c4efb8281386522f751e59c2949263b8394317dd658199650b39105dfaffae`.
Supplemental subscription-only wrapper attempt
`2263620f-be88-44e1-8c69-dceaae00606d` used those same bytes and again ended
`claude-timeout` after preflight, with observed／completed model, response, and
usage absent. It remains incomplete; there was no retry, downgrade,
substitution, paid credential, or alternate-provider fallback. The verdict
records the required conflict disclosure that Task 14 implemented a
private-authored v1 specification which the private side now knows was wrong,
so a Claude conclusion on that frozen packet would not be neutral.

## Worktree custody correction

Before the move, `git status --porcelain --untracked-files=all` was empty and
the branch tip was
`1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`. `git worktree move` relocated
`codex/task13-parity-mechanisms` to the public-safe sibling locator
`../TriTrack-Editing-Assistant-worktrees/task13-parity-mechanisms`. The
post-move porcelain listing showed that locator, no old locator, and the same
branch tip; the moved worktree was still clean before this fix-forward began.

## Outward-action boundary

This work does not authorize or claim a tag, GitHub Release, package
publication, pull request, tester or external-review contact, artifact upload,
signing, attestation, SBOM, Final Cut GUI result, DTD result, private
integration, application submission, production stability, force-push, or
visibility change.
