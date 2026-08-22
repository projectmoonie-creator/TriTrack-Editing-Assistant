# Task 14 parity-prerequisites closeout review packet

## Review target and authorization boundary

- Repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Project identity: `public-engine` / OSS
- Exact public base: `d952c1fce7e38e4791fbd1f616407ca6c0e58d7e`
- Exact review target: `e4e8fc24efedc7c300583deb6164d58889fbfb63`
- Review range: `d952c1f..e4e8fc2`
- Package version: `0.1.0a0`
- Target worktree was clean before this packet was added.

This is a read-only review of the public candidate. Inspect only the public
repository and this packet. Do not inspect a private repository, an old clone,
or any external handoff directory. The implementation author was authorized
to consume one clean-room handoff; the reviewer is given all required behavior
below and must judge only the resulting public code and tests.

Make no edit, commit, build, network request, provider call, tag, release,
publication, private integration, or remote change.

## Objective and selected design

Task 14 adds the public prerequisites needed for a later downstream parity
proof:

1. deterministic transcript anomaly classification;
2. deterministic source-pair and audio-master selection;
3. per-take transcription attempts, alternative-source retry, reuse
   provenance, degradation, and manifest-last result publication;
4. `sync-map-v2`, `run-manifest-v2`, transcription report, and result-manifest
   contracts while retaining v1 readers;
5. relay of selected source authority into string-out, story, and FCPXML;
6. one shared orchestration core for standalone and prepared-run transcription.

The selected design is deliberately asymmetric. The in-cue stutter detector
and alternative-source retry ship now. Voice-activity detection remains OFF
and has no CLI switches or model-path surface because the authorized input did
not provide a closed, non-rejected public model pin with byte length and
SHA-256. Enabling VAD by default before both prerequisite mechanisms and a
verifiable model pin would violate the release gate. The candidate must not
claim that VAD default, recognition accuracy, or simultaneous duplicate-angle
preservation is complete.

## Clean-room provenance

The implementation input was hash-bound to public base `d952c1f`. The five
behavioral source-document hashes were:

- handoff identity: `069391afa36c1080f04747f2cfe27152f14ef30cff3e2b20852ec62b5d82bf76`
- handoff guide: `719a5a0124bd3181d07093fd85d3ccb2678ac511b8873fb24fe7d4aa66eb1bae`
- transformations and invariants: `5158b32c9f70b2174a335d0f5cada78fa5d35c897868cdbc9d6e29d558fd98b7`
- transcription provenance contract: `f4c0fab7163e1e942fe5578fd4cbde83aec1d861697e4fb251225adaed7f8873`
- VAD-default contract: `3b6ee4a2cc7ee8007131945ac61c73602f96c33c8b14af693efad290d36f6c91`

The reference algorithms were reimplemented rather than copied, and the
TypeScript-origin contracts were rewritten for this Python engine. No private
repository was read.

## Twelve required invariants

All twelve must survive implementation and have direct public tests:

1. Four consecutive identical tokens trigger in-cue stutter; three do not.
2. A cue-local boilerplate or stutter reason outranks a repeated-run reason.
3. Blank cues never form a repetition run.
4. An empty transcript is not invalid.
5. Minimum shared-audio overlap is checked before trusting a correlation
   ratio.
6. Measured correlation outranks a drift prior.
7. Weak or scattered evidence yields no drift prior.
8. An extra source survives only when it adds new temporal coverage.
9. A forced audio master ignores loudness.
10. Recognition settings are stated in both the enabled and disabled
    directions.
11. A reused take never inherits the current run's settings; relevant
    provenance is unknown.
12. An alternative-source retry uses the same settings as its primary.

## Additional behavioral contracts to challenge

- A failed primary attempt and every retry remain in the report, including a
  stable failure code and chosen source. A failed take degrades the batch and
  never enters the transcript bundle.
- Successful, empty, and reused takes may enter the bundle. The result report
  is machine data, path-free, and transcript-text-free.
- A published result directory has exactly three authority files: bundle,
  report, and result manifest. The manifest is published last and binds the
  other two hashes. An incomplete publication must not look complete.
- A retry may consume only a synchronized alternative source associated with
  the same take. CLI and prepared-run paths must use the same orchestration
  core and produce equivalent authority.
- `sync-map-v2` records drift evidence, selected coverage sources, and audio
  master. Relay projections must preserve selected source identity and valid,
  non-overlapping audio continuity into FCPXML.
- New prepared runs use `run-manifest-v2` and cross-bind doctor, sync, bundle,
  report, result manifest, and string-out authority. Existing
  `run-manifest-v1` and `sync-map-v1` inputs remain readable and their schemas
  are not silently rewritten.
- The exact pre-existing `run-manifest-v1` schema hash remains
  `f2cc085ddff1db4a83074de2d8f132823136a5689a98aa244e1278e1920242bf`.
- VAD remains hard OFF. No `--vad`, `--no-vad`, or caller-supplied detection
  model path is accepted. Documentation must state the prerequisites and
  missing public pin without claiming the deferred default.
- Public output and diagnostics must not expose transcript text, absolute
  source paths, credentials, private names, or proprietary integration data.

## High-risk implementation surfaces

Inspect the complete review-range diff, with particular attention to:

- `src/tritrack_editing_assistant/transcript_anomaly.py`
- `src/tritrack_editing_assistant/pair_selection.py`
- `src/tritrack_editing_assistant/transcription_result.py`
- `src/tritrack_editing_assistant/transcribe_takes.py`
- `src/tritrack_editing_assistant/sync_scan.py`
- `src/tritrack_editing_assistant/run_workflow.py`
- `src/tritrack_editing_assistant/string_out.py`
- `src/tritrack_editing_assistant/story_fcpxml.py`
- `src/tritrack_editing_assistant/emit_fcpxml.py`
- `src/tritrack_editing_assistant/cli.py`
- `src/tritrack_editing_assistant/contracts.py`
- the four new schemas under `src/tritrack_editing_assistant/schemas/`
- `release/package-policy-v1.json`, `MANIFEST.in`, and the public docs

The direct test anchors are:

- `tests/test_transcript_anomaly.py`
- `tests/test_pair_selection.py`
- `tests/test_transcription_result.py`
- `tests/test_task14_relay_projection.py`
- `tests/test_transcribe_takes.py`
- `tests/test_sync_scan.py`
- `tests/test_run_workflow.py`
- `tests/test_cli.py`
- `tests/test_contracts.py`
- `tests/test_story_fcpxml.py`
- `tests/test_quickstart_demo.py`
- `tests/test_packaging.py`

## TDD and verification evidence

- Initial focused RED: 21 tests failed, with zero errors, before implementation.
- Workflow RED: new manifest-version and prepared-run authority expectations
  failed before the shared orchestration was added.
- Packaging and demo gates later caught a stale v1 assumption and incomplete
  wheel membership; both were fixed forward.
- Coherent public target: all 294 tests passed.
- Ruff passed.
- Public identity check returned `lane=OSS`, `projectKind=public-engine`,
  `ok=true`.
- All 11 maintainer-boundary tests passed.
- `git diff --check` passed.
- A clean detached snapshot at the exact target passed the full maintainer
  release gate with Python 3.13.15, pip 26.2, build 1.5.0, setuptools 84.0.0,
  and wheel 0.48.0.
- Release manifest SHA-256:
  `1e0b1caaddfe26d746d4f151ff8c308996062f93cd4aa212f256143d091250a0`
- Wheel: 45 members, SHA-256
  `aca03e80b09616f1d482291d86142bdf39a82dde41993a7a87c187312a7dab22`
- Sdist: 121 members, SHA-256
  `7d389198bc90e06b18818b5c9e4bebafbbb1f8b3544d52336b538cc4128118d0`
- Release source inventory: 178 files, SHA-256
  `5b7d5f0007b6ed2e79adbaff403865ad8a5ebcd1c5ddae33d2958ea0e1e8946c`
- Reproducible wheel bytes and sdist member inventory both passed. Fresh
  install, archive, source identity, source privacy, and downstream-seam gates
  all passed.

## Requested review dimensions

1. Find semantic gaps between the twelve invariants and their implementations.
2. Challenge retry ordering, attempt provenance, reuse-unknown behavior,
   per-take degradation, path/text privacy, and manifest-last publication.
3. Challenge source-selection authority, drift/overlap precedence, relay
   mapping, audio-master behavior, and FCPXML continuity.
4. Challenge v1/v2 compatibility, schema strictness, hash cross-binding,
   tamper detection, and standalone/prepared-run equivalence.
5. Search for any path that accidentally enables VAD, exposes a detection
   model argument, or claims the deferred default is complete.
6. Challenge CLI parser behavior, output-directory semantics, alternative
   source validation, package membership, demo assumptions, and docs.
7. Identify missing adversarial tests, contradictory claims, or any private or
   downstream authority that escaped into the public engine.

## Finding schema

Return:

- Summary: `NO FINDINGS` or count by severity.
- Findings, each with stable ID, blocker/major/minor severity, confidence,
  current file and line, exact failure mechanism, impact, smallest safe fix,
  and a test or reproduction.
- Optional observations in a separate non-blocking section.
- Inspection record naming only files and packet sections actually inspected.

A blocker or major finding requires current file-and-line evidence or a
reproducible failing contract. Do not promote a non-goal, deferred VAD default,
historical RED state, or hypothetical private consumer into a finding.

## Explicit non-claims

No tag, GitHub Release, package publication, pull request, tester contact,
signing, attestation, SBOM, Final Cut GUI result, DTD result, live speech
provider, application submission, private integration, simultaneous
N-camera preservation, production-stability claim, force-push, remote change,
or visibility change is in scope.
