# Task 8 text-alignment decision

Decision date: 2026-08-15

Decision owner: producer

Selected option: A — strict local promotion with deferred live transport

## Decision

Task 8 treats Task 7 cue identity and timing as immutable local authority.
Editor or provider text is untrusted revision evidence. A single deterministic
local promotion boundary validates cue-addressed revisions and creates a new
provider-neutral aligned transcript without changing take IDs, cue IDs,
source hashes, status, or integer-millisecond timing.

The local command accepts only strict cue-addressed revisions in v1. Arbitrary
full-text dynamic-programming alignment is deferred because repeated tokens,
multilingual tokenization, and equally optimal mappings can create false
deterministic confidence.

## Public artifacts

- `text-revision-v1` binds a partial set of cue-addressed text revisions to
  the SHA-256 of one exact `transcript-bundle-v1` file.
- `aligned-transcript-v1` binds the resulting immutable timing structure to
  both the exact source-bundle and revision-file SHA-256 values. Each completed
  cue records whether its text is original or revised.
- Empty takes are immutable and may not receive revision text.
- The same source bundle and revision file must produce identical aligned
  artifact bytes whether promoted through the local or offline hybrid command.

Hashes refer to the exact input file bytes after strict schema validation.
Inputs are hashed before and after processing. Any change fails closed before
publication.

## Local alignment boundary

`tritrack align` is fully local and network-free. It consumes one strict
transcript bundle, one strict revision artifact, and one absent output path.
Unknown, duplicate, foreign, or malformed take/cue identifiers; source hash or
language mismatches; invalid normalized text; invalid source cue structure; and
attempts to edit empty takes fail closed. Unmentioned completed cues retain
their original text and timing.

## Optional provider boundary

Task 8 implements an offline `tritrack hybrid` conformance path. It consumes
the same local transcript and revision plus one strict
`provider-receipt-v1` per revised take and an exact caller-declared provider
model. It performs no provider request, upload, deletion, subprocess, or
network access.

Each receipt must bind to the exact source bundle, take ID, and source audio
SHA-256; report provider `gemini`, the requested exact model as both requested
and observed, a completed request and upload, a successful response, and
attempted plus confirmed successful server-file deletion. Otherwise hybrid
fails closed and publishes nothing. After conformance checks, hybrid invokes
the same local promotion core as `align`.

The existing provider receipt scaffold gains the missing source-bundle and
take bindings while it is still a pre-release, unimplemented contract.
`gemini_hybrid.py` becomes implemented as the offline conformance adapter.
`gemini_transcribe.mjs` remains planned and no network-capable transport is
shipped. A later live transport requires a separate producer decision and real
invented-media upload/deletion acceptance evidence.

## Deferred alternatives

- arbitrary full-text LCS／Needleman-Wunsch alignment;
- cue merging, splitting, deletion, or retiming;
- revisions to proven-empty takes;
- a live Gemini upload／transcribe／delete transport;
- provider fallback or model substitution;
- provider output that bypasses local promotion; and
- Task 9 organizer or paper-edit behavior.

## Brainstorm provenance

The frozen public problem packet SHA-256 was
`15269143be8c01bd24c03cd224b5c6adabe8a587805c485bdf31cc9c336e7479`.

Codex and Gemini independently completed the first round. Gemini requested,
observed, and completed `gemini-3.7-flash`. Claude requested the dynamic
`opus` capability alias but attempt
`ba290d4b-2867-4241-ac13-e9f288c10914` ended incomplete with
`claude-timeout`; observed and completed model are null and request delivery
is unknown. It was not retried, downgraded, or replaced.

## Acceptance evidence

- observed RED-to-GREEN TDD for schemas, pure alignment, publication, CLI, and
  offline hybrid conformance;
- invented transcript, revision, and provider-receipt fixtures only;
- byte-identical repeat output and byte-identical local/hybrid promotion;
- source/revision/receipt immutability, absent-output, race, cleanup, strict
  schema, duplicate/foreign ID, empty-take, exact-model, receipt custody, and
  sanitized-summary tests;
- focused and full tests, Ruff, compilation, project identity, maintainer-skill
  validation, repository-boundary tests, and `git diff --check`;
- convergent closeout review and ordinary fix-forward; and
- minimal CI plus exact remote-main SHA verification.

No real provider call, upload, tag, release, pull request, tester contact,
package publication, or application submission is authorized by this decision.
