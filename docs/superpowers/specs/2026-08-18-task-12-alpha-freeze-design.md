# Task 12 alpha-freeze and independent-review design

Decision date: 2026-08-18

Decision owner: producer

Selected option: A — two-layer Git freeze with a package-neutral evidence
epilogue

Starting public candidate:
`71d719770f5b335ecd2f5f31ce98ea886e76b955`

## Decision

Task 12 freezes and independently reviews the public alpha without creating a
tag, release, package upload, signature, attestation, or second package
authority.

The design names two exact Git commits with different roles:

1. `alphaReviewTarget` is the clean immutable commit whose complete public
   engine, package, tests, contracts, CI, selected packaged documentation, and
   Task 12 review boundary are independently assessed.
2. `alphaEvidenceRecord` is a later commit that adds only public-safe review
   evidence, adjudication, verification, current status, and the status
   regression. It points back to `alphaReviewTarget` and never claims that an
   external reviewer saw its own answer.

The split is mandatory because a Git commit cannot contain the result of a
review of that same commit without changing its identity. The later evidence
record is not silently relabelled as the external review target.

Task 11's existing `scripts/release_gate.py` remains the only maintainer
packaging authority. Task 12 adds no runtime command, JSON contract, validator,
package format, CI job, component, tag, audit branch, Git note, or release
workflow.

## Freeze identities

### `alphaReviewTarget`

The review target is one exact clean commit on the isolated Task 12 branch. It
must contain:

- the complete Tasks 1–11 public implementation and tests;
- the selected Task 12 design and execution plan;
- the final intended Task 12-neutral bytes of every document that enters the
  wheel or sdist; and
- a status-neutral roadmap sequence that remains true before and after Task 12
  completion while `STATUS.md` continues to own the current gate.

Before the target is declared, the full suite, Ruff, compilation, project
identity, both canonical skill validators, package policy, `git diff --check`,
and the existing release gate must pass from the clean commit.

The target identity is its full Git commit SHA-1. The local release manifest
for that commit additionally records the exact project version, tracked-source
inventory, toolchain, wheel SHA-256 and member inventory, sdist SHA-256 and
normalized member inventory, passed gates, and explicit non-claims.

### `alphaEvidenceRecord`

The evidence record may add or change only package-excluded public evidence:

- `docs/reviews/task-12-*` public-safe packets, responses, ledgers, and
  adjudication;
- `docs/TASK-12-VERIFICATION.md`;
- `STATUS.md`; and
- `tests/test_maintainer_boundary.py`, solely to require Tasks 1–12 complete
  and Task 13 next.

Under the current package contract, `docs/reviews/` and
`docs/superpowers/plans/` are pruned, `docs/TASK-12-VERIFICATION.md` and
`STATUS.md` are not selected sdist members, and
`tests/test_maintainer_boundary.py` is explicitly excluded. None enters the
wheel.

If any post-review change touches runtime source, a packaged test, contract,
package policy, CI, README, changelog, tooling, roadmap, selected verification,
or another wheel／sdist member, it is not an evidence epilogue. The old target
is superseded, the changed commit becomes a new candidate, and the relevant
review and gate steps repeat.

## Package-neutrality proof

Run the release gate once at `alphaReviewTarget` and once at the clean
`alphaEvidenceRecord`. The evidence epilogue is package-neutral only when:

- the wheel SHA-256 values are exactly equal;
- the wheel member-inventory SHA-256 values are exactly equal;
- the sdist normalized member-inventory SHA-256 values are exactly equal;
- the sdist member counts are equal; and
- the selected runtime `src/` tree hash is equal.

Compressed sdist byte equality is not required because the existing project
does not claim it. The second `release-manifest.json` is expected to differ:
its candidate commit and tracked-source inventory honestly describe the later
evidence record. Task 12 must not mistake manifest inequality for package
drift, nor mistake package equality for Git-tree equality.

If the wheel or normalized sdist contents differ, the epilogue fails closed.
The final commit is then a new alpha candidate, not merely a record, and must be
reviewed as such.

## Frozen review packet

One path-safe packet is built after the review target commit exists. It names
the exact full target SHA and packet SHA-256 and includes:

- objective, scope, decision, non-goals, and requested finding schema;
- public project identity, version, clean-state facts, Git inventory digest,
  and selected current file contents;
- the Task 12 design and package-membership boundary;
- current release-manifest facts and the exact local gate result;
- exact fixed CI matrix, action pins, permissions, and last known baseline run;
- current public command／authority map and eleven-component registry;
- strict cross-task invariants and explicit claim／non-claim boundaries;
- prior independent-review outcomes, including incomplete provider lanes;
- targeted source, schema, package, CI, governance, and test excerpts needed to
  support file-and-line findings; and
- instructions for a read-only review of the exact checkout.

The packet does not include credentials, absolute home paths, ignored raw
artifacts, local media, transcripts, workbooks, FCPXML with private URIs,
provider prompts from another project, private repositories, or proprietary
templates. It is bounded for reviewer attention and focuses on compositional
seams rather than reproducing every historical packet.

The exact packet sent to providers is preserved publicly after adjudication.
Raw transport envelopes and transient local release artifacts remain ignored.

## Independent-review sequence

The first round is isolated:

1. Codex reviews the frozen target and records findings before reading an
   external answer.
2. Gemini receives the exact same frozen packet once through the controlled
   REST wrapper with dynamic highest-eligible released-model routing.
3. Claude receives the exact same frozen packet once through the registered
   subscription-only wrapper and dynamic `opus` capability request.

Every provider lane records requested, observed, and completed model IDs,
invocation lane, packet hash, attempt state, usage when available, result, and
failure class. A timeout, quota error, authentication failure, empty answer,
missing exact provenance, or ambiguous dispatch is `incomplete`, not a clean
review and not a finding.

There is no provider substitution. Claude never uses an API credential, PAYG,
Console credit, extra usage, direct standalone print mode, downgrade, or retry
after an ambiguous dispatch. Historical model IDs are provenance only.

## Review dimensions

The independent reviewers inspect the whole alpha composition across these
dimensions:

1. component registry and implemented／planned truth;
2. exact authority ownership across sync map, transcript, revision, aligned
   transcript, grouping, working cut, run manifests, workbook, and FCPXML;
3. local-first, no-network, credential, subprocess, source-immutability, and
   no-overwrite boundaries;
4. deterministic timing, ordering, canonical bytes, exact hashes, and
   cross-artifact binding;
5. four validator scopes, stable errors, read-only behavior, and claim limits;
6. run-bundle manifest chains, fixed members, manifest-last publication, and
   interruption／race behavior;
7. source privacy, archive safety, package membership, reproducibility, fresh
   wheel installation, and release-manifest authority;
8. fixed CI matrix, pinned Actions, permissions, installed-wheel smoke, and no
   artifact publication;
9. public documentation, role firewall, maintainer／end-user skill separation,
   compatibility claims, and outward-action boundary; and
10. test gaps and cross-task seams not already covered by incremental reviews.

Reviewers return only actionable findings with severity, confidence, current
file-and-line evidence, impact, and smallest safe fix. Optional observations
remain clearly separate from blockers.

## Adjudication and fix-forward

Codex checks every external statement against the frozen source, tests, and
reproducible behavior. Each item is classified exactly as `agree`, `upgrade`,
`downgrade`, `reject`, or `already-fixed`.

An ordinary agreed defect is fixed forward under the standing grant:

1. add or identify an observed failing regression;
2. record the RED behavior;
3. implement the smallest in-scope correction;
4. run the focused GREEN set and full public gates; and
5. determine whether the changed bytes supersede `alphaReviewTarget`.

A reviewer headline never overrides source-backed findings, and an optional
observation is not ignored merely because the headline says `NO FINDINGS`.

A true public-contract gap, private-data requirement, remote／visibility
change, or separately gated outward action stops the task for producer
direction. Ordinary code, test, and documentation fixes do not trigger another
authorization request.

## Public evidence record

The tracked Task 12 record contains:

- the exact provider packet;
- Codex's pre-external review;
- each usable public-safe provider answer;
- each machine-readable status ledger;
- an explicit incomplete ledger for every failed lane;
- finding-by-finding adjudication and RED／GREEN evidence;
- `alphaReviewTarget`, fix-forward commits, and `alphaEvidenceRecord` roles;
- both release-gate manifest facts and the package-neutrality comparison;
- complete local test, lint, compilation, identity, skill, and diff results;
  and
- explicit non-claims.

Ignored raw envelopes are never staged. Provider output is sanitized only for
public-path and credential safety; any transformation and resulting tracked
copy hash are disclosed.

## Final local, remote, and CI proof

After the evidence record is committed and the package-neutrality proof passes:

- run the complete suite, Ruff, compilation, identity, both skill validators,
  maintainer boundary, package policy, and `git diff --check`;
- require a clean worktree;
- run the final release gate into one fresh ignored absent directory;
- fast-forward local `main` without a merge commit;
- push only `main` to the existing public `origin`;
- prove local `HEAD`, `origin/main`, and remote `refs/heads/main` are identical;
  and
- require all six CI jobs at that exact pushed SHA to pass.

The final GitHub Actions run ID belongs in the handoff only. Editing a tracked
file to embed it would create another candidate and another CI run.

## Completion definition

Task 12 is complete when:

- one exact `alphaReviewTarget` is frozen from a clean full-gate commit;
- Codex completes first and both external lanes have truthful completed or
  incomplete ledgers;
- every finding is adjudicated and every ordinary agreed defect is fixed with
  regression evidence;
- one exact `alphaEvidenceRecord` preserves the public evidence without
  pretending to be the external review target;
- the evidence epilogue proves exact wheel and normalized sdist content
  invariance or supersedes and re-reviews the candidate;
- the final release gate passes;
- public `main` and the remote backup match the exact green evidence commit;
- all six exact-SHA CI jobs pass; and
- `STATUS.md` records Tasks 1–12 complete with Task 13 next.

## Explicit non-claims

Task 12 does not create or authorize a tag, GitHub Release, package
publication, tester outreach, signing, attestation, SBOM, PR, application
submission, Final Cut GUI operation, DTD claim, live provider transport,
private downstream integration, force-push, remote change, or visibility
change. It does not declare production stability or solve Task 13.

## Brainstorm provenance

The frozen problem-frame SHA-256 was
`afdcba263df1dfd2bd54f484e6638a8b52c33fe3dfe9240eab893cb38f474657`.
Codex completed before external output; response SHA-256 was
`eced0a2adc2fc2bf381013023483e04c712f2d41f4b29890e6bd6e51edeaa466`.

Gemini requested, observed, and completed `gemini-3.7-flash`; response SHA-256
was `9e54a5b8bdec883eda872b8933a1339f9a10a55b957e09e11748f7670f1b0f4c`.

Claude's subscription-only attempt
`2f5e3114-392c-48df-8f76-eea51b9bf033` requested dynamic `opus` and ended
`claude-timeout`. Observed／completed models, usage, raw output, and completion
time are null; `modelRequestSent` is unknown. There was no retry, downgrade,
paid credential, API／PAYG／extra-usage route, or provider substitution. Its
status-ledger SHA-256 is
`b32d0a4b177ccfe5d8e0978d8b6f4eed1c44bbcdbd2039a7614329ddf1844030`.

The producer selected Option A on 2026-08-18.
