# Task 13 generic-authority seam brainstorm packet

Date: 2026-08-18

Decision owner: producer

Target: public TriTrack Editing Assistant repository, branch
`feat/task-13-generic-authority-seam`, based on exact public `main` commit
`7bc035ee379a8a3babd2a6556eecdab2973b6301`.

Instruction: provide design ideation only. Do not edit the repository, request
private project material, or assume access to any downstream implementation.

## Decision needed now

Choose the smallest Task 13 mechanism that proves the public engine is the
generic authority while defining an intentional, clear seam for separately
owned downstream integrations.

Tasks 1–12 are complete. Task 13 is the next and final scheduled public-alpha
roadmap item. The public repository currently makes no private-integration,
tag, release, package-publication, or production-stability claim.

## Current public evidence

- The package exposes one installed console entry point, `tritrack`.
- Ten closed Draft 2020-12 JSON contracts are packaged and resolved by exact
  `schemaVersion`: compatibility profile, sync map, transcript bundle, text
  revision, aligned transcript, grouping, working cut, title binding, run
  manifest, and offline provider receipt.
- Canonical JSON authorities use exact-byte hashes and closed schemas.
  Workbook and FCPXML products are transports or projections rather than
  replacement authorities.
- Immutable prepared, aligned, and finished run bundles use fixed filenames,
  exact hashes, prior-manifest chains, absent-output publication, and a
  manifest-last completion rule.
- `tritrack validate` provides four read-only scopes: one JSON contract,
  structural FCPXML profile, authority-bound workbook, and one complete run
  bundle.
- The wheel currently contains runtime modules, schemas, profiles, and the
  CLI. It declares no plugin entry points, stable Python service-provider
  interface, or public compatibility promise for internal Python functions.
- The public release gate builds reproducible package candidates and tests a
  fresh wheel-only installation. Public CI runs the complete suite on the
  fixed supported OS and Python matrix.
- Existing invented fixtures are permitted. Private media, transcripts,
  project names, paths, credentials, templates, and operational evidence are
  forbidden.

## Required outcome

Task 13 should leave falsifiable public evidence that:

1. a generic, out-of-tree downstream consumer can integrate through an
   explicit supported boundary without importing private knowledge;
2. the public engine and its versioned artifacts remain the only authority for
   transcript text/timing, sync, grouping, selection, and run facts;
3. downstream-owned policy and outputs cannot silently become or mutate engine
   authority;
4. compatibility, failure, versioning, privacy, and ownership rules at the
   seam are clear enough to test;
5. no private implementation or live private integration is required or
   claimed.

## Constraints

- Keep the default workflow local, offline, deterministic, no-overwrite, and
  fail closed.
- Prefer a narrow steel-thread proof over a general framework.
- Reuse existing contracts, validators, bundle hashes, and installed-wheel
  verification when that is sufficient.
- Do not create a second transcript, timing, selection, grouping, sync, or run
  authority.
- Do not make internal Python modules stable by accident.
- Do not add private-domain vocabulary or private repository assumptions.
- Do not change the eleven-component product registry merely for supporting
  integration infrastructure.
- No tag, release, package publication, pull request, tester contact, signing,
  attestation, SBOM, live provider call, GUI operation, or private write.
- A downstream adapter may be separately owned and may produce its own
  namespaced result, but it must treat public engine artifacts as immutable
  inputs and accurately state the limited scope of its own output.

## Non-goals

- designing or implementing a specific private integration;
- a general plugin marketplace, in-process extension framework, workflow DAG,
  event bus, RPC service, or network daemon;
- stabilizing every Python function as a supported API;
- adding semantic editing decisions to the public engine;
- changing existing artifact authority or human approval gates;
- claiming backward compatibility beyond an explicitly selected seam.

## Affected users and systems

- public engine maintainers, who need a narrow compatibility surface;
- downstream adapter authors, who need a supported consumption boundary;
- editors, whose source and authoritative artifacts must remain under local
  custody;
- packaging and CI, which must prove the seam from a fresh installed wheel;
- future contract evolution, which needs an explicit compatibility rule.

## Reversible boundary

Task 13 may add or tighten public contracts, metadata, documentation, examples,
tests, CLI discovery/validation surfaces, and release-gate checks. It must not
perform a real downstream integration. Any public v1 seam should be small
enough that an incompatible future design can use a new explicit version
rather than reinterpret v1.

## Requested independent response

Return all nine sections below. Give concrete tradeoffs and falsifiable
experiments; do not merely agree with the problem statement or disguise a full
implementation plan as brainstorming.

1. `problem_reframe`
2. `pragmatic_path`
3. `alternative_architecture`
4. `low_cost_experiment`
5. `contrarian_challenge`
6. `unconstrained_possibility`
7. `overlooked_risks`
8. `assumptions_to_verify`
9. `recommended_next_decision`

In `recommended_next_decision`, state exactly what the producer should choose
between, what you recommend, and what evidence would falsify the choice.
