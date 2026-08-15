# Task 7 public verification

Date: 2026-08-15

Implementation candidate:
`60811a7af117a6dfd70d470513676d87db0922bb`

Branch: `codex/task7-local-transcription`

This report records sanitized, invented-content evidence for the fixed-profile
local-transcription slice. It contains no generated media, transcript text,
model bytes, credentials, local home paths, or raw engine output.

## Decision and TDD evidence

The producer selected Option A, the single-pass canonical bundle recorded in
`docs/TASK-7-DECISION.md`. The fixed
`whisper-cpp-cpu-no-fallback-v1` profile runs one CPU-only whisper.cpp decode
per take with engine temperature fallback disabled. Determinism is claimed for
bounded orchestration, canonicalization, state transitions, and artifact bytes
given the same normalized engine evidence; no cross-model, cross-version, or
cross-machine inference claim is made.

Observed RED-to-GREEN slices covered the initially unknown strict schema,
missing canonicalizer and guards, missing workflow, planned CLI surface,
unnoticed input mutation, real GPU-backend failure, real silence sentinel,
invalid version bytes, and profile provenance. During local closeout review, a
new two-take test reproduced one additional RED: the first source could change
while the second take was running after its per-take hash check. The minimal
fix added a full-batch source/model hash recheck before publication; the focused
case and suite then passed.

## Automated gates

- Task 7 focused contract, guard, workflow, and CLI tests: 37/37 passed.
- Complete Python suite: 100/100 passed.
- Maintainer boundary suite: 9/9 passed.
- Ruff over `src` and `tests`: passed.
- Python compilation over `src`, `tests`, and `examples`: passed.
- Project identity: `public-engine`, lane `OSS`, accepted.
- Maintainer skill validation: `Skill is valid!`.
- Installed `transcribe --help` and `components --json`: passed; the
  registry remained eleven components and both Task 7 components reported
  `implemented`.
- Draft 2020-12 validation of all three real temporary bundles: passed.
- `git diff --check`: passed.

The workflow tests include bounded subprocess failures and capture limits,
malformed／oversized／nonregular engine evidence, invalid timing and text,
duplicate basenames, source/model mutation, existing-output and publication
race behavior, cleanup, deterministic bytes, and path-free CLI summaries.

## Real local whisper.cpp evidence

A public-safe temporary run used invented speech and exact digital silence,
FFmpeg normalization, `whisper-cli` 1.9.1, and the caller-supplied official
`ggml-tiny.en.bin` from the whisper.cpp Hugging Face repository. The observed
model SHA-256 was
`921e4cf8686fdd993dcd081a5da5b6c365bfde1162e72b08d75ac75289920b1f`.

The first real speech attempt exposed a local Metal allocation failure. The
fixed profile was consequently made CPU-only with `--no-gpu`; the successful
engine output also exposed bounded final timestamp padding, which the
canonicalizer clips only on the final cue and only within the recorded
5,000 ms limit.

Two fresh installed-command speech runs produced byte-identical strict bundles
with SHA-256
`e4b7c59040e4f910312a730042faeabb369d6d3ab1c841bcbd37a4d52a04a10a`.
The canonical final cue ended at the measured 3,424 ms PCM duration. A separate
digital-silence run converted the observed exact `[BLANK_AUDIO]` sentinel to
an `empty` take with zero cues only after the normalized PCM independently
proved byte-zero; its bundle SHA-256 was
`3c601800d904e32c799e04e7bcb40c079c0ba636492c94805ddb5213e236a774`.
All three bundles validated against the packaged schema and contained the fixed
profile ID, model hash, sanitized engine version, source hash, basename-scoped
take identity, and no local absolute or temporary path.

The model download was a maintainer-only verification prerequisite. The
product transcription runs themselves made no provider, upload, or network
request, and TriTrack neither bundles nor downloads a model.

## Closeout review

One 79,694-byte frozen public packet at SHA-256
`e9ccd13d16bfadd7fd15939a640cb4589a18bcc71b77af9d3f3d82fb148776be`
contained the exact implementation-candidate patch and the evidence above.

- Gemini REST review used the dynamic
  `highest-capability-generally-released-at-execution` policy. Requested,
  observed, and completed model were all `gemini-3.7-flash`; result:
  `PASS` with no findings, test gaps, or documentation gaps.
- Claude subscription review requested the dynamic `opus` capability alias
  through the approved subscription-only wrapper. Attempt
  `b5479357-f27c-4930-a51c-d5bbbb14092c` ended incomplete with
  `claude-timeout`; observed and completed model are null,
  `modelRequestSent` is unknown, and no usable finding exists. It was not
  retried, downgraded, relabeled, or routed to API／PAYG fallback.

The completed Gemini review therefore supplies the external closeout finding
set; the Claude lane remains explicitly incomplete rather than being counted
as a second completed review. Local adjudication found no external action item.

## Public boundary

All media, model bytes, raw engine evidence, and generated bundles remained in
an untracked temporary directory. No production input, provider transcription,
upload, tag, release, pull request, tester contact, package publication, or
application submission occurred.
