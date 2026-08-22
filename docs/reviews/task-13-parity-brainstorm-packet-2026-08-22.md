# Task 13 parity mechanisms — frozen brainstorm packet

Date: 2026-08-22

Decision owner: producer

## Decision needed now

Choose the public-engine architecture and rollout order for consuming the
hash-bound clean-room handoff `task13-parity-v1` without weakening the existing
v1 artifact／CLI compatibility decision.

Do not edit the project. Return only an independent design response using the
required schema at the end of this packet.

## Why this decision is needed now

Public base commit `d952c1fe41563c38c7859250b3f95b3d93e8929f` completed the
existing public Task 13 authority seam. Its recorded producer decision says:

- versioned artifacts plus installed `tritrack validate ... --json` commands
  are the exclusive supported v1 downstream seam;
- internal Python modules are not a compatibility surface; and
- incompatible meanings require a new schema or seam decision.

The clean-room handoff explains why a later parity proof cannot pass yet: the
public engine lacks generic behavior now required by the engine authority. The
missing mechanisms must move into the public engine before parity can be
claimed and before any downstream can consume a pinned public artifact.

## Verified intake identity

- schema: `tritrack.clean-room-handoff/v1`
- handoff id: `task13-parity-v1`
- public base: `d952c1fe41563c38c7859250b3f95b3d93e8929f`
- every declared payload SHA-256 was independently recomputed and matched
- the handoff is the only authorized source of non-public-origin behavior
- no other repository, media, status, history, or implementation may be read

Declared transformations:

1. `strip-private-context`
2. `isolate-pure-algorithm`
3. `generalize-identifiers`
4. `replace-with-invented-fixtures`
5. `narrow-compatibility-claims`

Preserved invariants:

1. four consecutive identical tokens trigger in-cue stutter; three do not;
2. cue-local boilerplate or stutter reasons outrank cross-cue repeat reasons;
3. blank cues never form a repeated run;
4. an empty transcript is not itself invalid;
5. minimum shared-audio overlap is checked before correlation ratio;
6. measured correlation outranks a clock-drift prior;
7. weak or scattered drift evidence yields no prior;
8. an extra source survives only for genuinely new time coverage;
9. a forced audio master ignores loudness;
10. hearing-affecting settings are recorded in both on and off directions;
11. reused work never inherits the current run's settings as provenance; and
12. an alternative-source retry matches the primary attempt's settings.

## Required behavior

### Transcript anomaly behavior

- Add boilerplate, consecutive cross-cue repetition, in-cue stutter, anomaly
  range merging, and a whole-transcript verdict.
- The current public guard only rejects three exactly repeated adjacent cues
  and aborts the complete batch.
- The new whole-transcript verdict must distinguish an empty transcript from
  a transcript judged invalid.
- Known and intentional limit: delimiter-free token loops are not detected by
  the in-cue detector and must not be advertised as detected.

### Pair-selection behavior

- Add a clock-drift prior with minimum sample and maximum-spread refusal.
- Accept a weak correlation only when overlap is sufficient and drift agrees.
- Correlation acceptance always outranks drift-prior acceptance.
- Select a primary source, then keep further sources only when they add at
  least the declared amount of uncovered time.
- Forced audio-master selection ignores loudness; automatic loudness remains a
  documented crude fallback.
- Known and intentional limit: this supports a relay in time, not simultaneous
  duplicate camera angles. Do not claim N simultaneous cameras.

### Voice activity, retry, and provenance behavior

- Voice-activity detection is on by default for every audio transcription;
  `--no-vad` opts out and `--vad` explicitly requests the default.
- The two switches conflict if both are present, and either switch is invalid
  when no audio is being transcribed.
- A detection-model selection is invalid when detection will not run.
- Model validation happens before audio decode.
- Selectable detection／recognition models use closed named registries with
  recorded byte length and SHA-256; rejected models are not nameable.
- Caller-owned model paths must not be falsely checked against a registry pin
  that does not describe those bytes.
- Per-run receipts and per-take reports record hearing-affecting settings in
  both directions.
- Reused work is marked unknown rather than stamped with current settings.
- An invalid transcript retries once on another synchronized audio source with
  identical settings and records both attempts.
- A take with no usable alternative degrades to failed without blocking the
  rest of the batch.

## Hard rollout constraint

Voice-activity detection must not become the default until both of these are
already on the production path and covered by tests:

1. in-cue stutter detection; and
2. alternative-source retry.

The reason is causal, not ceremonial: detection can collapse a whole take into
one looping cue. Cross-cue repetition cannot see a one-cue loop. Enabling the
default without both safety nets can silently place invented text on an
editing timeline.

## Current public architecture and exact seams

### Synchronization

- `sync_scan.py` correlates A/B audio and emits `sync-map-v1`.
- The schema has `pairs`, `singleA`, and `singleB`; each pair contains exactly
  one `mediaA`, one `mediaB`, one offset, confidence, overlap, and audio master.
- Current selection chooses one strongest B source per A source.
- Current builders always write `audioMaster: "A"`.
- `string_out.py` rejects duplicate `mediaA` pair relationships.
- story projection registers exactly one relationship per media id.
- Therefore an A take relayed across two B files cannot be represented or
  consumed honestly in v1 merely by changing the selection function.

### Transcription

- `transcribe_takes.py` transcribes a flat list of local paths and emits one
  `transcript-bundle-v1` file.
- The bundle has one run-level recognition model hash and takes with only
  `completed` or `empty` status; it has no settings receipt, attempt history,
  selected source, retry, reuse marker, or failed status.
- Any non-silent empty result or repeated-cue guard failure aborts the complete
  batch and publishes nothing.
- The standalone transcribe command has no sync-map input, so it cannot know an
  alternative source.
- `run prepare` does have camera sources and creates a sync map first, but it
  currently passes only a caller-selected flat source subset into the same
  single-pass transcriber.
- Alignment, paper edit, organization, story projection, immutable run
  manifests, validators, packaging, and the black-box downstream proof all
  consume the current exact v1 contracts.

## Current verification state

- The base commit records a green 259-test suite and Ruff result.
- A fresh 2026-08-22 run in the new worktree passed 258 product tests and Ruff;
  the sole error occurred before package build because the reused local venv
  lacked the required `setuptools==84.0.0` backend. Direct import reproduced
  the missing dependency. The repository remained clean. This is an
  environment repair, not a product-code finding.

## Constraints

- Public engine and OSS lane only.
- Use only the verified clean-room handoff, current public repository, and
  public tool documentation. Do not infer or request private implementation.
- Reimplement behavior in Python; do not port the originating TypeScript.
- Preserve existing v1 semantics. Do not silently widen a versioned schema or
  change a stable machine-readable meaning under the same version.
- Keep internal Python modules non-public; supported behavior must be reachable
  through installed public commands and versioned artifacts.
- Keep default operation local, offline, no-overwrite, deterministic where
  already promised, and public-safe.
- Use invented tests only.
- Keep the eleven-component registry count unchanged unless evidence proves a
  real product component was added rather than supporting infrastructure.
- No tag, release, package publication, private integration, pull request,
  tester contact, or application submission is authorized by this decision.
- Work will follow red／green TDD and later independent closeout review.

## Non-goals

- No parity proof in this work package; this package makes a later proof
  possible.
- No simultaneous N-camera claim.
- No model-accuracy comparison.
- No provider or live-network path.
- No private adapter, media, transcript, fixture, status, or history.
- No Python facade or plugin system unless the chosen design supplies new
  evidence that the existing process boundary is insufficient.

## Reversible boundaries

- New exact contract versions or a new manifest-like orchestration artifact
  are reversible before release and can coexist with frozen v1 validators.
- Pure decision functions can land before command integration, but completion
  may not be claimed until tests prove the functions are wired into production
  paths.
- Voice activity may remain explicit opt-in while anomaly and retry safety nets
  land; only the final default flip is order-sensitive.

## Requested ideation

Propose materially different architectures, not cosmetic variations. Address:

- versioning strategy: new v2 authorities versus additive manifest／report
  artifacts versus another bounded approach;
- how relay selection reaches FCPXML without duplicating an A take;
- how retry, failed takes, settings, and provenance are represented without
  corrupting `transcript-bundle-v1` semantics;
- how standalone `transcribe` and `run prepare` share one truthful behavior;
- how a closed VAD model registry can coexist with caller-owned recognition
  model paths without false pin claims;
- the exact milestone order that mechanically prevents a premature VAD default;
- migration blast radius across validators, downstream seam, packaging, and
  immutable run bundles; and
- whether public roadmap naming should be a Task 13 parity follow-on or a new
  Task 14, without rewriting the historical Task 13 decision.

For each proposal, give concrete tradeoffs and at least one falsifiable
experiment.

## Required response schema

1. `problem_reframe`
2. `pragmatic_path`
3. `alternative_architecture`
4. `low_cost_experiment`
5. `contrarian_challenge`
6. `unconstrained_possibility`
7. `overlooked_risks`
8. `assumptions_to_verify`
9. `recommended_next_decision`

Do not give generic agreement or a disguised implementation plan. Do not edit
the repository.
