# Task 12 alpha review adjudication

Adjudication date: 2026-08-18

Final `alphaReviewTarget`:
`283ec9f7018a497aa77ad54c53f380a4bc426031`

Final provider packet SHA-256:
`caea5254db417bad816ef89921541a945742968ca0be3707e6d84c2f88e7e1c9`

The tracked public packet removes only trailing spaces from embedded
historical source／diff lines. Its SHA-256 is
`895950181de3c7f3cc607ac82ff221bb79fa41301bb9b70218cf7d2625cc7b1c`;
the target, review instructions, and substantive bytes are unchanged.

## Outcome

All reproducible Task 12 findings were fixed before the final target was sent
to external reviewers. Codex's final independent review and Gemini's final
review returned no current product findings. Claude's single final
subscription-only attempt ended `claude-timeout` and remains incomplete.

## Finding-by-finding classification

| ID | Source target | Classification | Result |
| --- | --- | --- | --- |
| T12-CX-001 | `7ec69bd0ef045c18eb7899e95ff1472ca5913d05` | agree | The sync-map loader read the complete path before applying its 16 MiB limit and followed symlinks. Commit `08fb19e45cf02f747ad7b3b9bf11e726d37262e5` replaced it with a bounded descriptor reader. |
| T12-CX-002 | `7ec69bd0ef045c18eb7899e95ff1472ca5913d05` | agree | Release commands used fully buffered `subprocess.run` capture, so output limits applied only after child completion. Commit `08fb19e45cf02f747ad7b3b9bf11e726d37262e5` added streaming combined-output bounds, timeouts, and process-group termination. |
| T12-CX-PF1-001 | `08fb19e45cf02f747ad7b3b9bf11e726d37262e5` | agree | Descriptor readers could block opening a FIFO before reaching `fstat`. Commit `fd39ed334b5c234eadddbea053d3f7e7b6d01bfb` added nonblocking opens across the runtime and release gate. |
| T12-CX-PF2-001 | `fd39ed334b5c234eadddbea053d3f7e7b6d01bfb` | agree | Older transcription, normalized-WAV, and CLI output-hash paths still used path-based blocking opens. Commit `c688e364e51114d832defaaf79ef4c48da705f6e` added descriptor-bound hashing, nonblocking regular-file checks, and before／after identity checks. |
| T12-CX-PF3-001 | `c688e364e51114d832defaaf79ef4c48da705f6e` | agree | The sdist Basic Title capture utility still used unbounded path reads for FCPXML and binding JSON. Commit `ca58cd0dfb214475faffaf3522646d454a53a31c` bounded both inputs and rejected links, special files, changes, and oversize bytes. |
| T12-CX-PF4-001 | `ca58cd0dfb214475faffaf3522646d454a53a31c` | agree | A commit-derived build epoch changed wheel bytes after package-excluded evidence commits, making the approved exact-wheel comparison impossible. Commit `283ec9f7018a497aa77ad54c53f380a4bc426031` moved the fixed epoch into the closed package policy. |
| T12-GM-INITIAL-000 | `7ec69bd0ef045c18eb7899e95ff1472ca5913d05` | reject | Initial Gemini returned no findings and described release subprocess output as bounded. The source-backed T12-CX-002 reproduction overrode that assertion. |
| T12-CX-FINAL-000 | `283ec9f7018a497aa77ad54c53f380a4bc426031` | agree | Final Codex review returned no current finding after inspecting the cumulative fixes and complete selected composition. |
| T12-GM-FINAL-000 | `283ec9f7018a497aa77ad54c53f380a4bc426031` | agree | Final Gemini returned no product finding. Its two optional observations correctly described the platform fallback and fixed epoch; neither requires a change. |
| T12-GM-FINAL-SCOPE | `283ec9f7018a497aa77ad54c53f380a4bc426031` | reject | Gemini's inspection record named files whose names appeared only in the Git inventory but whose bytes were not embedded in the packet. Those scope claims are not used as evidence. |
| T12-CL-FINAL-000 | `283ec9f7018a497aa77ad54c53f380a4bc426031` | reject | There is no Claude finding to adjudicate. Attempt `885fb03b-3c2d-4386-a02e-b4b00e3066c3` ended `claude-timeout` with observed／completed model, output, usage, and completion time all absent. It is incomplete, not a clean review. |

## RED／GREEN record

- T12-CX-001 and T12-CX-002: three focused regressions failed before the
  implementation edit. The same three passed afterward; the complete suite
  passed 243 tests.
- T12-CX-PF1-001: two focused flag-boundary tests failed, including one
  validator FIFO process that could otherwise hang. The regressions passed
  after the fix; the complete suite passed 246 tests.
- T12-CX-PF2-001: the transcription flag regression failed and the real FIFO
  hash process hit its three-second timeout. Both passed in under one tenth of
  a second after the fix. The CLI output-hash regression then failed before its
  edit and passed after it; the complete suite passed 249 tests.
- T12-CX-PF3-001: both Basic Title FIFO command paths hit their three-second
  test timeouts before the fix. They returned immediately afterward; the
  complete suite passed 251 tests.
- T12-CX-PF4-001: the policy-epoch regression failed because no policy-owned
  epoch existed. It passed after the implementation. The closed-policy test
  then correctly failed until its six-key contract and exact epoch assertion
  were updated. The complete suite passed 252 tests.

Every final local pass also included Ruff, `compileall`, `git diff --check`,
and public-content scanning of the changed files. The exact final target then
passed the release gate.

## Package-neutral evidence proof

Committed evidence probe
`2ff62ca705a2e3ef9188bab1aba526e94425563f` passed the release gate. Against
`alphaReviewTarget`, wheel SHA-256, wheel member inventory, wheel member count,
normalized sdist member inventory, sdist member count, and the `src/` Git tree
were all exactly equal. Its manifest SHA-256 was
`f339c1fcac8810c75385a07e191ee97e9f0c54834256a9203f5d32a954f664b7`.
Tracked-source inventory and compressed sdist bytes differed as explicitly
permitted. The final evidence-only closeout commit must repeat the same clean
comparison before custody transfer.

## Review provenance

The initial provider packet SHA-256 was
`38873ec0d33715d2e7f162f4cafbbad78994fc9b4cd0fb88d7320ab33985c8d1`.
Initial Codex response SHA-256 was
`5ee9e175c1794207c460f20a301b350a5a28ec9cb5ea7fdcc509a5e993b1a9dd`.
Initial Gemini requested, observed, and completed `gemini-3.7-flash`; response
SHA-256 was
`943c38770e5d1e903710631dcdf266a08c126d6ef3b40f319097a2b6bfc3765f`
and status-ledger SHA-256 was
`5b14d6621ef3f44f8a5ec08037a29ba4721122f87773431bd23da2a23ec76321`.
The initial Claude attempt
`ac9fa90b-b1b5-40b9-b5de-14380bcaa688` ended `claude-timeout`; its incomplete
ledger SHA-256 was
`5a95fa456840f341197349254e488cfe786d4970c32da02c984da50c22ecbd90`.

The final Codex response SHA-256 was
`caac886da8dcdec3fa2519b7562cb0d804ccce9d47bb8bd28911eb57aa0e6783`.
Final Gemini requested, observed, and completed `gemini-3.7-flash`; its exact
wrapper output SHA-256 was
`e036c4ec2610fcef2e0040de9c97053f057df326ae4e8e987b8ab13c8c8a5153`
and ledger SHA-256 was
`306d3d60ef03469bd6e423cdbc420fb0aeefcf625679d7f86150f7834a8ae4e7`.
The tracked response replaces one sentence containing literal private-path
patterns with an equivalent generic description so the canonical public scan
can pass; its tracked SHA-256 is
`0970149df1f1d6c5e9342c7c37ed9f2de75ca2b5a18820d969182f23e8a979a4`.
No finding, severity, target, model, or review conclusion changed.

Final Claude attempt `885fb03b-3c2d-4386-a02e-b4b00e3066c3` requested the
dynamic `opus` capability alias through the subscription-only wrapper and
ended `claude-timeout`. Observed／completed models, output, usage, and completion
time are null; `modelRequestSent` remains unknown. Its ledger SHA-256 is
`d2de328889382226137fec2e11d82defc1d9b2c5c270c507cedf7cf83ee5511c`.
Neither Claude attempt was retried, downgraded, substituted, or sent through a
paid credential／PAYG／extra-usage route.

## Non-claims

This adjudication does not claim a tag, GitHub Release, package publication,
pull request, tester contact, signing, attestation, SBOM, Final Cut GUI result,
DTD result, live provider transport, application submission, force-push,
remote change, or Task 13 completion.
