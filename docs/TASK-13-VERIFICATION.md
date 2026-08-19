# Task 13 generic-authority seam verification

Verification date: 2026-08-18

Status: closeout review is complete on an isolated public OSS branch;
final evidence verification and exact-SHA integration remain pending.

## Approved design

The producer selected Option A: existing versioned artifacts and installed
`tritrack validate ... --json` commands remain the exclusive v1 downstream
seam. Task 13 adds a black-box proof, not a stable Python facade, plugin loader,
network service, new runtime authority, or private integration.

## Baseline

Before Task 13 behavior tests or implementation existed, the constrained
Python 3.13 environment passed 252 complete `unittest` tests in 21.532 seconds.

## TDD evidence

The first focused run was:

```text
venv/bin/python -m unittest tests.test_downstream_seam -v
```

It ran one test and failed exactly because
`examples/downstream_seam.py` did not exist. The process returned 2 with the
Python file-open error for that missing public path. This is the observed RED
for the black-box consumer; no consumer implementation existed when it ran.

After the remaining fail-closed cases were added, a second pre-implementation
run executed four tests: the valid path failed with the same missing-file
return, and three negative cases errored only when their assertions attempted
to parse that missing-file stderr as JSON. No consumer implementation existed
for either RED run.

The complete focused GREEN run executed five tests in 1.502 seconds. All five
passed, including exact authority consumption, existing-output preservation,
unknown-version rejection, validator-hash mismatch rejection, and changed
second-validation rejection.

The release-gate RED then reported two signature errors because
`fresh_install_smoke` did not yet accept a source snapshot, one closed-manifest
gate mismatch, and one packaging member mismatch. After the gate copied the
proof out of tree and required its exact receipt, 30 release, manifest, and
seam tests passed in 2.164 seconds.

The packaging／CI RED then reported exactly three missing integrations: Task 13
members were absent from the sdist policy, the built sdist disagreed with that
policy, and the fixed CI wheel smoke did not run the consumer. After the exact
sdist and CI wiring, all 13 packaging, CI, and seam tests passed in 3.932
seconds.

## Generic-authority proof

`examples/downstream_seam.py` is a black-box standard-library consumer. It
does not import engine internals. It invokes installed
`tritrack validate contract --json`, requires
`tritrack.validate-summary/v1`, `validationScope: contract`,
`aligned-transcript-v1`, and `tritrack.aligned-transcript/v1`, then binds the
validator-reported SHA-256 to the exact regular-file bytes it consumes.

The invented fixture SHA-256 is
`602f439a2d2eb1e8479035b1d92ffeb46bf4d276e014bbe48a584b38f1c5a6f6`.
The consumer derives only one take and one cue, repeats validation before
publication, creates a canonical `example.tritrack-downstream-receipt/v1`
sidecar at an absent path, and prints a path-free, transcript-text-free
summary. The sidecar is downstream-owned and non-authoritative; it is never an
engine contract.

The maintainer release gate copies the script and fixture outside the verified
source snapshot, invokes isolated Python and the installed CLI from a fresh
wheel-only environment, and requires the exact sidecar. The release manifest
records `downstreamSeam: pass`. The wheel member set remains the original 38;
only the sdist carries the decision, verification, example, invented fixture,
and regression test.

## Design-review provenance

The frozen brainstorming packet SHA-256 was
`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`.
Codex completed its independent analysis before external results were read.
Gemini requested, observed, and completed `gemini-3.7-flash`. Claude's single
subscription-only attempt ID was
`d13e8a66-75a2-4342-a7e9-c65844a60458`; it requested the dynamic `opus`
capability alias and ended `claude-timeout` with no observed or completed model
and ambiguous dispatch. It was not retried, downgraded, substituted, or sent
through a paid API.

## Coherent implementation validation

At exact `task13ReviewTarget`
`9c9ee9c7c75254c507e9984c27b9a4195273d21c`, the constrained Python 3.13
environment passed all 259 tests in 22.265 seconds. Ruff passed every Python
surface under `src`, `tests`, `examples`, and `scripts`; `compileall` passed
the same four trees; the maintainer identity check returned
`projectKind: public-engine` and `lane: OSS`; and `git diff --check` passed.
The focused governance suite passed all 11 tests.

The clean release gate passed at that exact target with:

- wheel SHA-256:
  `7aeea40d7102bd0eb8b8059100d1d5880d2715662ea26fdb44323ad93cf4f785`;
- sdist SHA-256:
  `5f336972fc8ed206a863fafd20b31443322d7552335017f33a2c6949cef88681`;
- manifest SHA-256:
  `062c18c6402a40a486221c4d28c6d1f938097a359ea023797dbad95a66d24cd2`;
  and
- `downstreamSeam: pass` with 38 wheel members and 109 sdist members.

## Closeout review

The frozen same-byte closeout packet SHA-256 was
`4a64926fc3a325e61b7962e5c6e3ad13d39a25d5b5716e740be16b6f493c7075`.
Codex completed independently before provider outputs were read and returned
`NO FINDINGS`. Gemini requested, observed, and completed
`gemini-3.7-flash`, returning `NO FINDINGS`; wrapper usage was 80,485 input,
1,402 output, and 84,283 total tokens.

Claude's single subscription-only closeout attempt ID was
`cd73c790-5ca5-4801-ab61-9b465d50e546`. It requested the dynamic `opus`
capability alias and ended `claude-timeout` after preflight with no observed or
completed model, output, usage, or completion time. It remains incomplete and
was not retried, downgraded, substituted, or sent through a paid route.

The adjudication accepted both clean reviews and recorded the provider
observations as non-blocking. No current behavior defect was reproduced, so no
post-review code change was made. Complete records are in
`docs/reviews/task-13-closeout-*`.

## Non-claims

Task 13 makes no tag, no package publication, no private integration, no
GitHub Release, pull request, tester contact, signing, attestation, SBOM,
Final Cut GUI, DTD, live-provider, application-submission, or
production-stability claim. It adds no stable Python facade, plugin loader,
network service, new engine contract, or second authority.
