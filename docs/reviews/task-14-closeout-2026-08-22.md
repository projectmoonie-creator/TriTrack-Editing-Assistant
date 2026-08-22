# Task 14 parity-prerequisites closeout

Closeout date: 2026-08-22

Exact implementation review target:
`e4e8fc24efedc7c300583deb6164d58889fbfb63`

Exact post-review target:
`ea3a73fc3225bb2c3841e7bd435a2dd6e94e1ff3`

## Outcome

Task 14's public prerequisites are coherent and green. The post-review target
passes 299 tests, Ruff, diff hygiene, and the clean maintainer release gate.
Voice-activity detection remains off, with no VAD CLI or caller-supplied model
surface, because no authorized closed public VAD model pin includes both exact
byte length and SHA-256.

The implementation independently reexpresses the two clean-room reference
mechanisms and rewrites the two TypeScript-origin behavioral contracts for the
public Python engine. No private repository was read. The input guide,
identity, transformations, and two contract hashes remain recorded in the
frozen packet.

## RED and GREEN evidence

The first Task 14 acceptance run observed 21 tests, 21 failures, and zero
errors before implementation. Those failures covered the absent anomaly,
pair-selection, retry/provenance, relay, and command-boundary mechanisms.
Workflow, demo, and packaging integration produced later RED checkpoints
before their implementations were added.

Source-grounded closeout review found two additional defects after the first
clean release candidate:

| ID | Severity | RED evidence | Fix |
| --- | --- | --- | --- |
| T14-CX-001 | major | Two tests proved that individually schema-valid, canonical, correctly rehashed bundle／report／manifest files could disagree on take identity or retry settings and still pass both reuse and run loading. Both tests failed because no exception was raised. | Test commit `b5844ec57ff02a598de58866938676b84126129f`; fix commit `79c1a94dc22dcfe43526f0593202a59db1f04957` adds shared semantic cross-binding for requested takes, bundle membership, selected sources, attempt order, retry settings, reuse unknowns, and terminal outcomes. |
| T14-CX-002 | minor | One test mapped a take's primary path back as its own alternative. The engine-version probe was reached instead of fail-closed input rejection. | The same RED／GREEN commits reject any duplicate primary or alternative path before an engine process starts. |

The focused transcription-result suite then passed 11 tests. The direct
run-bundle cross-binding test passed. The complete suite passed all 299 tests
in 22.666 seconds.

## Review provenance and adjudication

### Conflict disclosure

Task 14 implemented the v1 specification authored on the private side, and
the private side now knows that specification was wrong because it omitted
the sparse-source failure mode. Therefore any Claude-lane conclusion about
this frozen Task 14 packet is not neutral. The packet remains the required
historical review object, but neither a favorable nor an unfavorable answer
may override the corrected, separately hash-bound v2 amendment. This
disclosure comes from the producer-authorized amendment; no private repository
was read.

The frozen closeout packet SHA-256 is
`c9c4efb8281386522f751e59c2949263b8394317dd658199650b39105dfaffae`.
Both external lanes received those exact bytes once.

Packet erratum: its `Exact public base` line incorrectly expanded the correct
short review range `d952c1f` as a non-existent full object name. The
hash-bound handoff identity and Git both record the authoritative public base
as `d952c1fe41563c38c7859250b3f95b3d93e8929f`. The exact review target and
short `d952c1f..e4e8fc2` range in the packet were correct. The reviewed packet
bytes remain unchanged so its hash and both attempt ledgers stay auditable;
this erratum supersedes only that mistyped expansion.

Gemini requested, observed, and completed `gemini-3.7-flash`; wrapper usage was
2,974 input, 1,418 output, and 5,581 total tokens. It returned `NO FINDINGS`,
but its inspection record named non-existent schema paths without the actual
`.schema.json` suffix and the lane received no repository argument. Its result
is therefore retained as a completed packet-level advisory, not accepted as
source-inspection evidence. Report SHA-256:
`1412033c2314660e0dc99944f24a5630c19f0979008df958f4c9267aba2c0ec8`.
Status-ledger SHA-256:
`3f54024d988d86d2fac56cdf31bab5d403c15cb1933d5a660d93cdb7b008fd1f`.

The original Claude attempt `1061392e-4861-43b2-aac2-2f5511a70c20` requested
the dynamic `opus` capability alias through the approved subscription-only
wrapper. It ended `claude-timeout`; observed and completed models, response,
usage, and completion time are absent, and `modelRequestSent` is ambiguous.
Its archived incomplete-ledger SHA-256 is
`b148126331feded641b8eb4b66489730826d9ac2a0856ba122273e3a7d8f8ded`.

After the lane was reported restored, the required convergence supplement
sent the exact same frozen packet bytes through the same audit-grade wrapper;
it did not re-freeze a packet or use a weaker gate. Supplemental attempt
`2263620f-be88-44e1-8c69-dceaae00606d` also ended `claude-timeout` after
preflight. Its requested model was the dynamic `opus` capability alias;
observed and completed models, response, usage, completion time, and
`modelRequestSent` remain absent or ambiguous. Its current incomplete-ledger
SHA-256 is
`aeaf7dcfbaf3d874a3d33f2a108257d20256ba782d353d2ebce6590e87d0336d`.
Both attempts remain incomplete. The supplement was not retried, downgraded,
substituted, or sent through an API key, PAYG, Console-credit, extra-usage, or
alternate-provider lane.

## Post-review release gate

The clean detached source snapshot at exact post-review target
`ea3a73fc3225bb2c3841e7bd435a2dd6e94e1ff3` passed the full maintainer gate
with Python 3.13.15, pip 26.2, build 1.5.0, setuptools 84.0.0, and wheel
0.48.0. The first sandboxed invocation was environment-incomplete at the
fresh-install command; the same exact snapshot passed when its pinned public
dependencies were available.

- wheel SHA-256:
  `872b0bb15616f7b5b4f41188f463b0ab47ecf99617d1d1429ce90bd4f64cae87`;
- sdist SHA-256:
  `9b3f083e8c630eefbae621c0176c349e533c7d5e11e6144d820abd2f03e5d12f`;
- release-manifest SHA-256:
  `3caf84fe590f2b1771c5598c3230124201659005fd903ff572b10473b650bf8a`.

Fresh install, wheel and sdist archive inspection, source identity, source
privacy, downstream seam, and reproducibility gates all passed.

## Release state and remaining dependency

Task 14 completes the public anomaly, selection, alternative retry,
provenance, relay, and v2 run-authority prerequisites. It does not itself prove
a downstream parity run and does not flip VAD. A later VAD-default task must
first add one closed, non-rejected public registry entry with exact size and
hash, exercise the installed-engine argument contract, and keep the in-cue
stutter and synchronized alternative retry paths green.

No tag, GitHub Release, package publication, pull request, tester contact,
signing, attestation, SBOM, Final Cut GUI result, DTD result, live speech
provider, application submission, private integration, simultaneous N-camera
claim, production-stability claim, force-push, or visibility change is claimed.
