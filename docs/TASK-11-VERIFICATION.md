# Task 11 release-readiness verification

Verification date: 2026-08-18

Release state: local public-source candidate only; no public tag or package
release exists.

## Candidate identity

- Approved design commit: `87d4c32`.
- Clean implementation candidate:
  `ce562e995b63f3f1a29989de3e1ef202da27b5f2`.
- Project identity: `tritrack-editing-assistant`, `public-engine`, lane `OSS`.
- Package version: `0.1.0a0`.
- Tracked source: 115 regular stage-zero files, inventory SHA-256
  `3a0544c1d5f7b318af07382932631d702a9f5f426e00fd5790aa0c34e6bf8fb9`.
- The implementation candidate had an empty Git status before and after the
  local gate. No generated build, environment, cache, evidence, media,
  workbook, FCPXML, credential, or private-path file was tracked.

## Clean verification environment

The candidate was installed editable into a new Python environment using the
repository's exact constraints. `pip check` reported no broken requirements.
The observed toolchain was:

| Tool | Exact version |
| --- | --- |
| Python implementation | CPython |
| Python | 3.13.15 |
| pip | 26.2 |
| build | 1.5.0 |
| setuptools | 84.0.0 |
| wheel | 0.48.0 |
| packaging | 26.3 |
| pyproject-hooks | 1.2.0 |
| Ruff | 0.16.2 |

The clean-environment run produced these results:

- 69 focused validator, release-gate, packaging, CI, and CLI tests passed.
- 235 complete-suite tests passed.
- All four packaging policy tests passed, including two independent builds.
- Ruff passed over `src`, `tests`, `examples`, and `scripts`.
- Python compilation passed over the same four public surfaces.
- The public project-identity check passed.
- Both the maintainer and end-user skills passed the canonical skill
  validator.
- `git diff --check` and the clean-worktree gate passed.

## Four read-only validator scopes

`tritrack validate` keeps validation claims narrow and writes no output:

| Mode | Exact scope | Evidence boundary |
| --- | --- | --- |
| contract | `contract` | One exact artifact satisfies its installed registered JSON Schema. It does not prove references, parent artifacts, or cross-file hashes. |
| fcpxml | `structural-profile` | Exact bytes satisfy the selected installed profile and title-binding structural checks. It makes no source-media, DTD, Final Cut GUI, or target-machine claim. |
| paper | `authority-bound` | One workbook is acceptable against the exact supplied aligned transcript bytes. It does not publish grouping intent or repair either input. |
| run | `complete-run-bundle` | The fixed artifact set, strict contracts, exact hashes, manifest semantics, and prior-manifest chain form one complete immutable bundle. It does not reconstruct incomplete state. |

Successful JSON and human summaries contain only the exact scope, hashes, and
bounded counts. They contain no path, filename, transcript, workbook cell,
FCPXML text, command, time, log, or credential. The component registry remains
eleven entries; validation is supporting infrastructure, not a twelfth
component.

## Local release gate

The clean implementation candidate passed the maintainer gate. The gate built
two independently materialized `git archive` snapshots at the same commit time,
inspected both archives without generic extraction, installed only the chosen
local wheel into a new environment, ran `pip check`, confirmed eleven registry
entries, and exercised `validate --help` plus all four mode helps.

The two wheels were byte-identical. The two sdists had identical normalized
member／type／mode／size／content inventories; compressed sdist byte identity is
not claimed. The chosen artifacts and deterministic receipt were:

| Fact | Value |
| --- | --- |
| wheel bytes | 84,990 |
| wheel members | 38 |
| wheel SHA-256 | `93f8e84d513c55d37e9f214a2f55accfe4d42e6e59afa8c07d2e4839d799acc1` |
| wheel member-inventory SHA-256 | `7a4adacafdde808bba55bfb63d75dcc6215e5c8eb2442e02c888aecb47d9ae79` |
| sdist bytes | 169,699 |
| sdist members | 102 |
| sdist SHA-256 | `8cf0095b1f8f89176a6c1a1e97d67606fe2a56cc282016a94b92cf4375956637` |
| sdist member-inventory SHA-256 | `9ded2ef3d4ff445db340a2af54c8b89e5864f12d740afda4b354031f4dce8ca1` |
| release-manifest SHA-256 | `2f2847a218970410b2bac548a60ad0588d616fa1d4ca362e731e7ec4ebf7cb49` |

The canonical manifest was hard-linked after both archives and validated
against the closed Draft 2020-12 schema. It records only project, source
inventory, toolchain, platform, artifact digest／size／member facts,
reproducibility facts, passed gate names, and explicit non-claims. It records
no local path, timestamp, duration, account, host, run identifier, command,
log, source content, or matched value.

## Fixed public CI contract

The test matrix is exactly:

- `ubuntu-24.04` x64 with Python 3.12;
- `ubuntu-24.04` x64 with Python 3.13;
- `macos-26` arm64 with Python 3.12; and
- `macos-26` arm64 with Python 3.13.

One `ubuntu-24.04`／Python 3.13 quality job and one
`ubuntu-24.04`／Python 3.13 local release-gate job complete the workflow.
Permissions are only `contents: read`. The official Actions are fixed to:

- `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`
  (`v7.0.1`); and
- `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97`
  (`v7.0.0`).

Each test cell runs the complete suite, compilation, a local wheel build, a new
wheel-only installation, `pip check`, components JSON, and all validator help
surfaces. No CI artifact is uploaded or published.

## Brainstorm provenance

- Frozen public problem packet SHA-256:
  `ff145c249aae193ce80872783b8f95e840684ee3a518e4cc2788cc607aa15921`.
- Codex completed its independent first round before reading another model's
  output; response SHA-256:
  `0bdc84c66d5ca5012bcee89e8e757b0c47dae3c9e0e178a7c5118ec6427cd6c0`.
- Gemini requested, observed, and completed `gemini-3.7-flash`; response
  SHA-256:
  `1d682f99a8cfad8473c574d1e4c645a1279e56e99cf55d359a16645c896e3379`.
- Claude requested the dynamic `opus` capability alias through the approved
  subscription-only wrapper. Attempt
  `637f7c3a-cf72-4e97-9d42-ef7ef0d1400e` ended `claude-timeout`; observed and
  completed models are null. The attempt remains incomplete, with no retry,
  downgrade, paid credential, or provider fallback claim.

## Explicit non-claims

Task 11 performed no tag, public release, package publication, pull request,
tester contact, artifact upload, signing, attestation, SBOM, Final Cut GUI
operation, DTD check, live provider operation, credential access, or
application submission. It does not establish independent cross-machine build
reproducibility or downstream private integration. The evidence proves only
the tested public source, package, validator, CI contract, and local candidate
gate described above.

## Independent closeout and fix-forward

The frozen closeout target was
`d53deb28aa86ef1aba9f978f44456f71bc315e57`; the exact provider packet SHA-256
was `ab64798a971fdddeb3f093a4c3d0053e9d0d5c71712c81710cc0bb96663a92e2`.
The tracked public packet is a path-sanitized copy that preserves all target
bytes and questions while replacing two historical path literals in removed
diff lines; its SHA-256 is
`589670cfc3691274d0725d4a13f3fce7f103954e20b22e2188d83c37b9ff92a1`.
The initial unsanitized record commit was never pushed and is absent from the
public branch history. Codex completed its source review before either external result
was read. Gemini requested, observed, and completed `gemini-3.7-flash` and
returned `NO FINDINGS`. The one Claude subscription attempt requested the
dynamic `opus` alias and ended `claude-timeout`; observed and completed models
are null, dispatch completion is ambiguous, and no retry, downgrade, API
credential, or provider fallback occurred.

Codex reproduced four defects plus one policy-drift defect that was upgraded
during adjudication. Fix-forward commit
`0493a92f8257c8721e1a4564b1e43bfec44c01dc` now:

- binds archive bounds, inspection, digesting, and reproducibility comparison
  to the same regular non-symlink bytes;
- rechecks hard-linked archive size／digest facts before the manifest-last link;
- maps a missing run directory to the approved unreadable-input exit class;
- rejects conservative bare credential-token shapes without exposing values;
  and
- closes nested package policy keys and binds declared fake allowlists to the
  scanner's actual exceptions.

Commit `33b44e30c54db23a1cbff325c7f4a7410980180e` also replaced an old
username-specific historical-path assertion with the actual generic privacy
scanner, so the regression checks the rule without embedding a local identity.

The focused GREEN set passed 15 tests, the expanded complete suite passed 238
tests, Ruff and compilation passed, packaging policy tests passed twice, and
`git diff --check` passed. Complete classification and RED／GREEN evidence are
in `docs/reviews/task-11-closeout-adjudication-2026-08-17.md`.

## Producer-mediated manual Claude review and fix-forward

A later producer-mediated interactive Claude Code subscription review inspected
public `main` commit `7ae540a1ab46de39b31d826ae99752b325e6e9e1` and returned
`NO FINDINGS`. Its exact response SHA-256 is
`ffd6a408fd755ede13c5e1c5946f9aeef09a4449737edcba8416c0870ca47d09`.
The session self-reported model text `claude-opus-5[1m]` and unverified usage;
the apparent formatting residue is preserved and is not represented as an
audit-wrapper model observation.

Of its four optional hardening observations, Codex reproduced and upgraded two
minor defects: a third-party openpyxl `ValueError` could escape the stable CLI
code boundary, and “text-free working cut” overstated an artifact that retains
editor-authored text. The fixes now map the parser failure to
`TRITRACK_PAPER_WORKBOOK_INVALID` and describe the artifact as
`transcript-text-free`. A third observation became direct regression coverage
for noncanonical working-cut bytes; that test passed before product-code edits,
confirming the implementation was already correct. The hypothetical inner-pipe
engine token was rejected as a current defect because no supported token or
failing contract was identified.

Fix-forward commit `eaa17b49c9100bf92452106c1de23392a2831ae5` contains the
changes and review records. Focused RED failed on the two reproduced defects
while the coverage-only regression passed; focused GREEN passed all three.
The complete suite then passed 240 tests, and Ruff, compilation, public project
identity, both canonical skill validators, and `git diff --check` passed.

This manual result is useful independent evidence but is not a replay or
completion of a prior wrapper attempt. Every historical `claude-timeout`
record retains its original incomplete and ambiguous-dispatch state. Complete
provenance and item-by-item classification are in the matching
`tasks-7-11-claude-manual-*` review records.
