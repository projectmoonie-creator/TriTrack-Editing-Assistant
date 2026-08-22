# Task 14 amendment v2 closeout ledger

Closeout date: 2026-08-23

## Exact identities

- Public base: `1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`
- First amendment implementation target:
  `7232267a236cbb35f210d5088cb02ca69201d473`
- Post-review implementation fix:
  `f8b77e65ac0a51d19efbda159d7441cb3be870e4`
- Package-bearing closeout target:
  `90c6f45e9354cda7eb4da9fd3328fb6709268592`

The final Git evidence-record identity is supplied by Git rather than written
inside its own bytes. This ledger and `STATUS.md` are package-excluded, so they
do not change the wheel／sdist hashes below.

## Verification result

At the package-bearing closeout target:

- 344 complete unit tests passed;
- Ruff passed with cache disabled;
- `compileall` passed for source, tests, and scripts;
- Git diff hygiene passed;
- the full clean maintainer release gate passed with Python 3.13.15 and the
  pinned public toolchain.

Release-gate artifact evidence:

- wheel SHA-256:
  `f3bda52dba240a1160aa657b0dea99dc744dc5fb6d9d74a712acf5041f2d070c`;
- sdist SHA-256:
  `6abe6b98ba5261b2267cf373c1230eb63f46fbb052b3fdcfe49867018d601f0e`;
- release-manifest SHA-256:
  `5aefc5e2113808860e8dea7c1d1663f7419f550bcb9a4bf8a9ac649f4564969c`.

The first sandboxed invocation against that exact clean commit returned only
the gate's generic child-command failure and published no output directory.
The gate intentionally suppresses child stdout／stderr, so this ledger does not
invent a more specific failing child. The identical command and commit passed
when allowed to reach the pinned public dependencies needed by the fresh-install
step; the successful result above is the accepted gate evidence.

## Review disposition

The frozen amendment packet SHA-256 is
`f6c530b5886a13b1b14284d636ec8457e3c9545e91aeb4e82c6013deae9efc55`.
Gemini requested／observed／completed `gemini-3.7-flash` and returned
`NO FINDINGS`; its report and status hashes are
`24dc45a8e644cad4af876a69f0ce09923ec1fa61da3c3f0b7d60a35df2481686`
and `9adb29a313e3c9f89293c2da3d6523578e1a5a25208a1751e4664135f40b5b6e`.
The later source-grounded Codex review used `gpt-5.6-sol`, found six required
issues, and changed no file. All six were accepted, reproduced by RED tests,
and fixed; the adjudication hash is
`2a40d47a55a3319a72ef9a610846969b950fec55c8449a36f73a6c35bf37b321`.

The separate historical Task 14 Claude convergence supplement reused exact
frozen packet SHA-256
`c9c4efb8281386522f751e59c2949263b8394317dd658199650b39105dfaffae`.
Attempt `2263620f-be88-44e1-8c69-dceaae00606d` again ended
`claude-timeout` with no observed／completed model, usable response, or usage;
it remains incomplete without downgrade, substitution, paid route, or
alternate-provider fallback.

Conflict disclosure: Task 14 implemented the v1 specification authored on the
private side, and that authoring side now knows the specification was wrong
because it omitted the sparse-source failure. A Claude conclusion about that
frozen v1 packet would therefore not be neutral and cannot override the
separately hash-bound v2 amendment. No private repository was read.

## Custody and outward boundary

The worktree move preserved branch tip
`1c9334290e75d1cc70a31b4b86cc273fcc59b2ae` and registered the public-safe
sibling locator
`../TriTrack-Editing-Assistant-worktrees/task13-parity-mechanisms`; the old
misplaced locator disappeared from `git worktree list --porcelain`.

This closeout created no tag, GitHub Release, package publication, pull
request, tester／external-testing contact, signing, attestation, SBOM, Final Cut
GUI result, DTD result, private integration, or application submission.
