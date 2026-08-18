# Task 13 generic-authority seam verification

Verification date: 2026-08-18

Status: coherent implementation is green on an isolated public OSS branch;
closeout review and exact-SHA integration remain pending.

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

Before the implementation-target commit, the constrained Python 3.13
environment passed all 259 tests in 21.894 seconds. Ruff passed every Python
surface under `src`, `tests`, `examples`, and `scripts`; `compileall` passed
the same four trees; the maintainer identity check returned
`projectKind: public-engine` and `lane: OSS`; and `git diff --check` passed.
The focused governance suite passed all 11 tests.

## Non-claims

Task 13 makes no tag, no package publication, no private integration, no
GitHub Release, pull request, tester contact, signing, attestation, SBOM,
Final Cut GUI, DTD, live-provider, application-submission, or
production-stability claim. It adds no stable Python facade, plugin loader,
network service, new engine contract, or second authority.
