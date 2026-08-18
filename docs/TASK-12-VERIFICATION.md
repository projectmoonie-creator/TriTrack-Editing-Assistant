# Task 12 alpha-freeze verification

Verification date: 2026-08-18

Release state: reviewed public alpha source only; no tag, GitHub Release, or
package publication exists.

## Two exact roles

`alphaReviewTarget` is
`283ec9f7018a497aa77ad54c53f380a4bc426031`. It is the clean package-relevant
commit reviewed by Codex, Gemini, and the attempted Claude lane.

`alphaEvidenceRecord` is the later commit that contains this verification,
the public review records, adjudication, completion status, and maintainer
boundary regression. Git determines its exact identity after these bytes are
committed; the document does not attempt an impossible self-referential commit
hash. It may change only the evidence-only allowlist defined by the approved
Task 12 design.

## Final frozen packet

- Exact provider packet SHA-256:
  `caea5254db417bad816ef89921541a945742968ca0be3707e6d84c2f88e7e1c9`.
- Packet size: 855,474 bytes and 23,313 lines.
- The tracked public copy removes only trailing spaces from embedded historical
  source／diff lines so `git diff --check` remains clean. Its SHA-256 is
  `895950181de3c7f3cc607ac82ff221bb79fa41301bb9b70218cf7d2625cc7b1c`
  and its size is 855,025 bytes with the same 23,313 lines. No prompt text,
  target fact, source token, or review question changed.
- The packet contains every `src/` runtime file, all three distributed public
  scripts, selected tests and governance, the cumulative fix-forward diff,
  exact Git inventory, and exact target release manifest.
- The packet passed the canonical public-content scan and contained no
  credential, private media, transcript, workbook, private FCPXML URI, local
  home path, or proprietary template.

## Independent review

Codex completed before the final external outputs were read and returned no
current finding. Its response SHA-256 is
`caac886da8dcdec3fa2519b7562cb0d804ccce9d47bb8bd28911eb57aa0e6783`.

Gemini requested, observed, and completed `gemini-3.7-flash`. It returned no
product finding. The exact wrapper response SHA-256 is
`e036c4ec2610fcef2e0040de9c97053f057df326ae4e8e987b8ab13c8c8a5153`
and the status-ledger SHA-256 is
`306d3d60ef03469bd6e423cdbc420fb0aeefcf625679d7f86150f7834a8ae4e7`.
One private-path-pattern sentence was generalized in the tracked public copy;
its SHA-256 is
`0970149df1f1d6c5e9342c7c37ed9f2de75ca2b5a18820d969182f23e8a979a4`.
Gemini's overbroad inspection-record claims are rejected as evidence; the no-
finding result is not used to override any Codex reproduction.

Claude attempt `885fb03b-3c2d-4386-a02e-b4b00e3066c3` requested the dynamic
`opus` capability alias through the approved subscription-only wrapper. It
ended `claude-timeout` with observed／completed model, output, usage, and
completion time absent and `modelRequestSent` unknown. The incomplete-ledger
SHA-256 is
`d2de328889382226137fec2e11d82defc1d9b2c5c270c507cedf7cf83ee5511c`.
There was no retry, downgrade, provider substitution, paid credential, PAYG,
Console-credit, or extra-usage route.

The initial target and review records are also preserved. They prove that a
clean reviewer headline never overrode the reproduced sync-map, subprocess,
FIFO, path-reader, sdist-tool, or package-epoch defects. Complete
classification and RED／GREEN evidence are in
`docs/reviews/task-12-alpha-adjudication-2026-08-18.md`.

## Fix-forward chain

| Commit | Closed behavior |
| --- | --- |
| `08fb19e45cf02f747ad7b3b9bf11e726d37262e5` | bounded sync-map loading and streaming release-command capture |
| `fd39ed334b5c234eadddbea053d3f7e7b6d01bfb` | nonblocking regular-file validation for descriptor inputs |
| `c688e364e51114d832defaaf79ef4c48da705f6e` | descriptor-bound transcription, WAV, and CLI output reads |
| `ca58cd0dfb214475faffaf3522646d454a53a31c` | bounded Basic Title FCPXML and binding inputs in the sdist tool |
| `283ec9f7018a497aa77ad54c53f380a4bc426031` | policy-owned fixed package build epoch and final review target |

## Review-target release gate

The clean `alphaReviewTarget` passed the maintainer gate in a fresh constrained
Python 3.13 environment. The manifest SHA-256 is
`7b14052466d591f92015729f144ab812e2089364273bd913bd9159a6c9738f5b`.

| Fact | Exact value |
| --- | --- |
| package version | `0.1.0a0` |
| tracked source files | 128 |
| tracked-source inventory SHA-256 | `673717d4ff23e23cfe31fdcccfef35834c093ecb14ca395376e183633da3bf06` |
| `src/` tree | `584e329fe535192a1fc0211d0348b5865a135754` |
| wheel bytes | 86,062 |
| wheel members | 38 |
| wheel SHA-256 | `ab3a0c0ec66bcfe09a5500034250f4076e5ead1206bf90fa350f2949d9438643` |
| wheel member-inventory SHA-256 | `4bc6644aa0dd1740783b4e26aadfab00a5a26d51233df6b54699a7df0a0f4384` |
| sdist bytes | 181,473 |
| sdist members | 103 |
| sdist SHA-256 | `75aba42a7017c7d2ab2b92e397fa94de55d6bec4ed1108ef5ef8a45d1e926b51` |
| sdist member-inventory SHA-256 | `f428677f07794ee9b10a06da8b2595843eb2af125a3362df3b41548d53d09ded` |

The gate reported `wheelBytesMatch: true` and `sdistMembersMatch: true`,
installed only the selected local wheel into a fresh environment, ran
`pip check`, confirmed the eleven-component registry, and exercised the five
validator help surfaces. The fixed `sourceDateEpoch` is owned by the closed
package policy rather than Git commit time.

## Evidence-only package-neutrality contract

Committed evidence probe
`2ff62ca705a2e3ef9188bab1aba526e94425563f` passed the clean release gate.
Its release-manifest SHA-256 is
`f339c1fcac8810c75385a07e191ee97e9f0c54834256a9203f5d32a954f664b7`.

| Required comparison | Review target | Evidence probe | Result |
| --- | --- | --- | --- |
| wheel SHA-256 | `ab3a0c0ec66bcfe09a5500034250f4076e5ead1206bf90fa350f2949d9438643` | `ab3a0c0ec66bcfe09a5500034250f4076e5ead1206bf90fa350f2949d9438643` | equal |
| wheel member inventory | `4bc6644aa0dd1740783b4e26aadfab00a5a26d51233df6b54699a7df0a0f4384` | `4bc6644aa0dd1740783b4e26aadfab00a5a26d51233df6b54699a7df0a0f4384` | equal |
| wheel member count | 38 | 38 | equal |
| sdist member inventory | `f428677f07794ee9b10a06da8b2595843eb2af125a3362df3b41548d53d09ded` | `f428677f07794ee9b10a06da8b2595843eb2af125a3362df3b41548d53d09ded` | equal |
| sdist member count | 103 | 103 | equal |
| `src/` Git tree | `584e329fe535192a1fc0211d0348b5865a135754` | `584e329fe535192a1fc0211d0348b5865a135754` | equal |

The evidence source inventory honestly changed from 128 files and
`673717d4ff23e23cfe31fdcccfef35834c093ecb14ca395376e183633da3bf06`
to 141 files and
`cf61f10f247544e4ea28eada8685324ba9b83b0cd7a56745137db05673b5a746`.
The compressed sdist SHA-256 changed from
`75aba42a7017c7d2ab2b92e397fa94de55d6bec4ed1108ef5ef8a45d1e926b51`
to
`53aa3eb05586062541c7fcd937851946e11a154f045437da73ad3898dbd1b8c4`,
which is permitted and is not misreported as normalized package drift.

The final `alphaEvidenceRecord` adds only this package-excluded closeout text
to the proven evidence set. It is accepted only if one more clean release gate
repeats all required equalities against `alphaReviewTarget`:

- exact wheel SHA-256 equality;
- exact wheel member-inventory SHA-256 equality;
- exact normalized sdist member-inventory SHA-256 equality;
- equal sdist member counts; and
- equal `src/` Git tree identity.

The final evidence gate's project commit and tracked-source inventory must
differ honestly. Compressed sdist SHA-256 may differ and is not a claimed
equality. The exact final SHA and gate result are reported in the handoff
without creating a self-referential follow-up commit.

## Local verification

Before the evidence epilogue, the exact review target passed:

- 252 complete `unittest` tests;
- Ruff over the repository;
- `compileall` over source, scripts, examples, and tests;
- public project identity;
- both canonical skill validators;
- package policy, public-content scan, runtime／script packet completeness,
  `git diff --check`, and clean tracked status; and
- the complete release gate with exact constrained Python／pip／build／
  setuptools／wheel versions recorded in its manifest.

The maintainer-boundary regression deliberately failed before this document
and the Task 12 status existed. It must pass at the evidence record together
with the complete suite and all gates above.

## Custody and exact-SHA CI

After the package-neutrality proof, the evidence record may be fast-forwarded
to the existing public `main` and pushed to the existing `origin` under the
standing grant. Local `HEAD`, `origin/main`, and the remote branch must match.
All six fixed GitHub Actions jobs must pass at that exact SHA. The run ID is
reported only in the final handoff because writing it back would create a new
candidate.

## Explicit non-claims

Task 12 creates no tag, GitHub Release, package upload, pull request, tester
contact, signing, attestation, SBOM, Final Cut GUI result, DTD result, live
provider transport, private downstream integration, application submission,
force-push, remote change, or visibility change. It does not declare
production stability and does not complete Task 13.
