# Task 8 public verification

Date: 2026-08-15

Implementation candidate:
`4cc25b5248fe67a7cce656f0e810976f18565c16`

Branch: `codex/task8-text-alignment-recovery`

This report records sanitized, invented-content evidence for deterministic
cue-addressed text promotion and offline provider-receipt conformance. It
contains no production media, transcript, credential, local home path, raw
provider output, or server file identifier.

## Decision and boundary

The producer selected Option A from `docs/TASK-8-DECISION.md`: local Task 7 cue
identity and integer-millisecond timing remain immutable authority. A strict
`text-revision-v1` addresses existing cues and binds to the SHA-256 of one
exact `transcript-bundle-v1` file. Promotion emits a provider-neutral
`aligned-transcript-v1` bound to both exact input-file hashes.

The optional `hybrid` path is offline conformance only. It validates one
existing `provider-receipt-v1` per revised take and then invokes the same local
promotion core. It contains no HTTP client, provider SDK, subprocess, upload,
deletion, credential lookup, or network request. The network-capable
`gemini_transcribe.mjs` component remains planned.

## Observed RED-to-GREEN evidence

- Contract RED: 13 expected schema errors while `text-revision-v1` and
  `aligned-transcript-v1` were unknown and provider receipts lacked exact
  bundle／take bindings. Contract GREEN: 6/6.
- Pure align RED: import failure because `align_text.py` did not exist. File
  boundary RED: 5 expected missing-API errors after the test structure itself
  was corrected. Pure and file-boundary GREEN: 13/13.
- Local CLI RED: 4 expected failures for the planned component status, missing
  flags, missing execution, and missing output-exists mapping. CLI GREEN was
  observed before commit.
- Hybrid RED: import failure because `gemini_hybrid.py` did not exist. Hybrid
  core GREEN: 6/6. Hybrid CLI RED: 4 expected failures for planned status and
  missing flags／execution／mapping, followed by GREEN.
- Public status RED: the boundary test found `STATUS.md` still stopped at Tasks
  1–7. Documentation and the 9/9 maintainer boundary suite then passed.

## Automated gates

- Task 8 focused contract, alignment, hybrid, and CLI tests: 43/43 passed.
- Complete Python suite: 126/126 passed.
- Maintainer boundary suite: 9/9 passed.
- Ruff over `src`, `tests`, and `examples`: passed after one mechanical test
  context-manager formatting fix.
- Python compilation over `src`, `tests`, and `examples`: passed.
- Project identity: `public-engine`, lane `OSS`, accepted.
- Maintainer skill validation: `Skill is valid!`.
- Installed `align --help`, `hybrid --help`, and `components --json`: passed;
  the registry remained eleven components, `align_text.py` and
  `gemini_hybrid.py` reported `implemented`, and `gemini_transcribe.mjs`
  remained `planned`.
- `git diff --check`: passed.

Tests cover strict schemas, exact-byte hashes, deterministic take ordering,
immutable source timing and status, original／revised cue disposition,
duplicate／unknown take and cue rejection, empty-take immutability, malformed／
oversized／nonregular inputs, input mutation, existing outputs, publication
races, path-free summaries, exact-model matching, one receipt per revised take,
bundle／take／audio binding, completed request and upload, successful response,
confirmed server-file deletion, and failed or privacy-incomplete custody.

Two absent outputs created from identical transcript and revision bytes through
local `align` and offline `hybrid` were asserted byte-identical in the automated
suite. All fixtures and generated artifacts were invented and temporary.

## Brainstorm provenance

The frozen public decision packet SHA-256 was
`15269143be8c01bd24c03cd224b5c6adabe8a587805c485bdf31cc9c336e7479`.

Codex and Gemini independently completed the architecture round. Gemini
requested, observed, and completed `gemini-3.7-flash`. Claude requested the
dynamic `opus` capability alias, but attempt
`ba290d4b-2867-4241-ac13-e9f288c10914` ended incomplete with
`claude-timeout`; observed and completed model are null and request delivery is
unknown. It was not retried, downgraded, relabeled, or routed to API／PAYG
fallback.

## Closeout review

One 118,478-byte frozen public packet at SHA-256
`77643160c1c7b902faf052243443a910a45098f9e71aebc23299e272fd079df8`
contained the exact Task 7 base-to-candidate patch, implemented contract,
non-goals, and verification evidence. Its frozen candidate was
`5b7ce4e6ad50d5451159363caa36b1d9acc5dfba`.

After the operating system's file-provider permission made the original local
checkout inaccessible, the candidate was recovered from that frozen patch on
the exact Task 7 base. The extracted reviewed patch and the recovery commit's
base-to-candidate diff compared byte-for-byte equal; both had SHA-256
`1f385980f195ea44bfe99d10fb6a5b12de76344f7b72d1710cde67dbb8c79d07`.
All automated gates above were rerun successfully in the recovery checkout.

- Gemini REST review used the dynamic
  `highest-capability-generally-released-at-execution` policy. Requested,
  observed, and completed model were all `gemini-3.7-flash`; usage was 34,916
  input and 119 output tokens. Result: `PASS` with no findings, test gaps, or
  documentation gaps. It also confirmed the candidate stays inside Task 8
  Option A and contains no network-capable provider transport.
- Claude subscription review requested the dynamic `opus` capability alias
  through the approved subscription-only wrapper. Attempt
  `b35fb467-7046-424d-816e-dd497096f170` ended incomplete with
  `claude-timeout`; observed and completed model are null and
  `modelRequestSent` is unknown. It produced no usable finding and was not
  retried, downgraded, relabeled, or routed to API／PAYG／extra-usage fallback.

The completed Gemini review supplies the external closeout finding set; the
Claude lane remains explicitly incomplete rather than being counted as a
second completed review. Local adjudication checked the reviewed source,
tests, and behavior and found no action item or fix-forward change.

## Public boundary

No real provider call, upload, deletion, production input, tag, release, pull
request, tester contact, package publication, or application submission
occurred. The only authorized outward action at closeout is a fast-forward push
of the fully green candidate to the existing public `origin`, followed by exact
remote-SHA and minimal-CI verification.
