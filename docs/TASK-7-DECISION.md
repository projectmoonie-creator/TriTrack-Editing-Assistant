# Task 7 local-transcription decision

Decision date: 2026-08-15

Decision owner: producer

Selected option: A — single-pass canonical bundle

## Decision

Task 7 will run one fixed local whisper.cpp decoding profile with the engine's
temperature fallback disabled. The deterministic guarantee covers bounded
orchestration, canonicalization, state transitions, and artifact bytes given
the same normalized engine evidence. It does not claim bit-identical speech
inference across engine versions, models, or hardware.

Each take has only three possible outcomes:

1. structurally valid recognized cues produce `completed`;
2. independently proven digital silence produces `empty` with no cues;
3. every other outcome fails closed and publishes no bundle.

Rejected, malformed, repetitive, or otherwise suspect engine text is never
converted into a successful empty transcript, and the tool never invents
placeholder words such as `[inaudible]`.

## Public Task 7 boundary

- `tritrack transcribe` accepts repeatable local media paths, one caller-owned
  readable whisper.cpp model, one explicit language, and one absent output
  path.
- Camera audio is normalized to temporary mono 16 kHz PCM through the existing
  bounded FFmpeg process boundary.
- `whisper-cli` is invoked once per take through the same argv-only bounded
  process boundary with no shell, no prompt, no translation, no network, and
  no temperature retry ladder. The fixed
  `whisper-cpp-cpu-no-fallback-v1` profile disables GPU decoding as well as
  engine temperature fallback so backend selection is not an implicit input.
- The strict `transcript-bundle-v1` artifact stores stable take/cue IDs, integer
  millisecond timing, normalized cue text, source/model SHA-256 provenance, and
  a sanitized engine version. It stores no absolute paths, execution times,
  raw logs, temporary paths, or credentials.
- Inputs are immutable. The bundle is published atomically only when every take
  has a valid `completed` or proven-silence `empty` outcome. Existing outputs
  and race winners are never overwritten.
- Task 8 may rely only on the canonical bundle. Raw whisper.cpp JSON remains an
  internal temporary evidence format.
- The observed whisper.cpp final-cue padding may be clipped to the real PCM
  duration only when it is the last cue and no more than 5,000 ms beyond the
  source. Other timing overflow fails closed.
- Exact `[BLANK_AUDIO]` evidence is discarded only when the normalized PCM has
  independently been proven all-zero; it is invalid over non-silent audio.

## Deterministic guard boundary

The Task 7 guard rejects structural transcript artifacts, including leaked
whisper control-token syntax, empty cue text, invalid or non-monotonic timing,
and exact repeated adjacent cue runs beyond the frozen public limit. It does
not claim to detect semantic truth or silently rewrite recognized words.

## Deferred alternatives

A bounded second decoding profile, persisted engine-evidence layer, and VAD
pre-segmentation remain deferred. Any of them requires a separately recorded
decision and invented-media stability evidence before changing Task 7's
single-pass guarantee.

## Acceptance evidence

- observed red/green TDD for the schema, canonicalizer, guards, workflow, and
  installed CLI;
- invented speech and digital-silence fixtures only;
- deterministic repeat artifact bytes from identical normalized evidence;
- bounded timeout, capture limit, malformed JSON, invalid timing, duplicate
  media ID, dependency failure, output collision, race, cleanup, and privacy
  tests;
- focused and full tests, Ruff, compilation, project identity, maintainer-skill
  validation, repository-boundary tests, and `git diff --check`;
- a real local FFmpeg/whisper.cpp run when a public-safe temporary model is
  available, recorded without committing media, transcript text, model, or
  private paths.

No provider call, upload, package publication, tag, release, pull request,
tester contact, or application submission is part of this decision.
