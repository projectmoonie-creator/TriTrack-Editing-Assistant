# Task 13 generic-authority downstream seam decision

Decision date: 2026-08-18

Decision owner: producer

Selected option: A — existing artifact／CLI seam plus black-box proof

## Decision

The public engine's existing versioned artifacts and installed command-line
validators are the exclusive supported downstream integration seam for v1.
Task 13 does not add an in-process plugin system, stable Python facade, network
service, or new runtime authority.

A separately owned downstream consumer integrates by:

1. selecting the narrowest installed `tritrack validate ... --json` scope that
   matches the artifact facts it needs;
2. accepting only the exact contract and validation scope it understands;
3. reading immutable engine artifact bytes without changing them;
4. binding any downstream-owned result to the exact hashes reported by the
   engine validator;
5. revalidating before publishing if it reads after the initial validation;
6. writing only to an absent output outside the engine artifact or run bundle;
   and
7. using its own namespace and accurately limiting its claims.

Internal Python modules and functions are implementation details. Their
current importability does not make them a compatibility surface.

## Authority ownership

The public engine remains the only authority for its existing domains:

- transcript text and cue timing: transcript and aligned-transcript artifacts;
- synchronization facts: sync-map artifacts;
- editor grouping intent: grouping artifacts;
- compiled selection facts: working-cut artifacts;
- immutable run facts: run manifests and their fixed artifact hashes; and
- structural transports and projections: workbooks and FCPXML remain
  non-authoritative for the facts from which they are derived.

A downstream sidecar may summarize, index, route, or apply separate policy to
exact engine facts. It is never an engine contract and may not claim to repair,
replace, retime, rewrite, or validate the authority it references.

## Supported process boundary

The installed help for each command remains the flag authority. Downstream
automation may rely only on machine-readable `--json` output, documented exit
classes, exact `schemaVersion`, exact `validationScope`, and exact hashes. It
must not parse human output or error prose.

The current scopes retain their existing limits:

- `contract` proves one JSON value satisfies one installed schema; it does not
  prove parent existence or cross-artifact binding;
- `structural-profile` proves installed FCPXML profile and binding structure;
- `authority-bound` proves one workbook is acceptable against exact aligned
  bytes; and
- `complete-run-bundle` proves one immutable bundle's fixed files, contracts,
  manifest semantics, and hashes, without reconstructing prior bundles.

No new schema-discovery command is added. The selected black-box proof must
first fail because installed commands cannot expose a necessary engine-owned
fact before Task 13 may add such a surface.

## Public black-box proof

`examples/downstream_seam.py` is a deliberately small out-of-tree reference
consumer. It imports only the Python standard library and invokes the installed
`tritrack validate contract --json` process. With one invented
`aligned-transcript-v1` input it:

- requires the exact contract and scope;
- binds the exact artifact hash;
- derives only take and cue counts;
- repeats validation before publication;
- writes a canonical, namespaced, non-authoritative sidecar to an absent path;
  and
- prints only a path-free, text-free completion summary.

The reference sidecar schema begins `example.`, not `tritrack.`. It is an
illustration of downstream ownership, not a new public engine contract.

The release-readiness gate copies the reference consumer and invented fixture
outside the source snapshot, runs it with isolated Python against a fresh
wheel-only installation, verifies the sidecar, and records a named
`downstreamSeam` pass. The wheel exposes no additional runtime module or
component for this proof.

## Compatibility rule

V1 compatibility is explicit rather than inferred:

- consumers select exact contract and summary schema versions;
- unknown versions fail closed;
- new incompatible meanings require a new schema or seam decision;
- internal Python changes are not seam changes; and
- an example sidecar may evolve without becoming an engine contract, but its
  example `schemaVersion` must still change when its meaning changes.

## Privacy and custody

The seam does not grant access to media or transcript-bearing artifacts. The
caller decides which local artifact enters a downstream consumer and retains
its custody obligations. Public proof uses only invented text. Engine and
consumer outputs contain no credential, private path, account, host, command,
timestamp, duration, or private-domain vocabulary.

## Rejected alternatives

- A stable Python facade would create Python ABI, exception, typing, and
  supported-version obligations without evidence that the process boundary is
  inadequate.
- An in-process plugin protocol would run downstream code inside the authority
  process and add discovery, dependency, isolation, and crash policy.
- A new handoff authority would duplicate facts already owned by existing
  contracts and manifests.
- A live private integration would cross the public／private role firewall and
  remains separately gated.

## Falsification and revision boundary

Option A is falsified only if the fresh-wheel reference consumer must import
engine internals or duplicate an engine-owned validation rule to bind the
required facts, or if a measured required integration cannot tolerate the
process boundary. The first result permits reconsidering a minimal read-only
discovery command; the second permits reconsidering a versioned Python facade.
Neither result authorizes a plugin loader or private implementation intake.

## Non-claims

Task 13 does not create a tag, release, package publication, pull request,
tester contact, signing, attestation, SBOM, live provider call, GUI result,
DTD result, private downstream implementation, application submission, or
production-stability claim.

## Brainstorm provenance

The frozen public packet SHA-256 was
`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`.
Codex completed independently before external outputs. Gemini requested,
observed, and completed `gemini-3.7-flash`. Claude's single subscription-only
attempt requested the dynamic `opus` alias and ended `claude-timeout` with no
observed or completed model and ambiguous dispatch; it remains incomplete with
no retry, downgrade, substitution, or paid fallback. The producer selected
Option A on 2026-08-18.
