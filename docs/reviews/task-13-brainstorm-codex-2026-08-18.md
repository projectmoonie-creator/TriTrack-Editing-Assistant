# Task 13 independent Codex brainstorm

This response was completed before any Claude or Gemini answer was read.

## 1. `problem_reframe`

The missing product is not an adapter. It is a small compatibility promise.
The public engine already has authoritative artifacts, strict validators, and
an installed process boundary, but downstream authors cannot yet distinguish
the deliberately supported surface from convenient internal Python imports.
Task 13 should therefore prove that an integration can remain outside the
engine and still consume authoritative facts without copying authority.

## 2. `pragmatic_path`

Declare an artifact-and-process seam, not an in-process plugin API. Publish a
closed machine-readable seam descriptor that names the supported CLI discovery
and validation commands, accepted authoritative artifact schema versions,
immutability rules, downstream output namespace rule, compatibility policy,
and explicit non-claims. Add one tiny out-of-tree reference adapter using only
an installed wheel's `tritrack` executable and invented artifacts. It should
validate exact inputs, derive one clearly non-authoritative summary or receipt,
bind it to input hashes, and refuse changed, unknown-version, or invalid input.

Exercise that adapter from a fresh wheel-only environment in the Task 13 gate.
The proof passes only if the adapter has no source-tree imports, no private
configuration, no network, no mutation, and no ability to make its output pass
as an engine contract.

Tradeoff: this keeps the supported surface narrow and language-neutral, but a
consumer pays process startup and JSON/file I/O costs. Those costs are minor
for the current batch editing workflow.

## 3. `alternative_architecture`

Create a minimal stable Python facade such as
`tritrack_editing_assistant.integration`, exporting typed immutable handles
for contract discovery and validation while keeping all other modules private.
A standalone adapter could import only that facade. This improves ergonomics
and performance for Python consumers, but it immediately creates Python ABI
and exception-compatibility obligations and does not help non-Python tools.

A materially larger alternative is a plugin entry-point protocol in which the
engine loads adapters. That reverses custody: untrusted downstream code runs
inside the authority process. It adds discovery, isolation, crash, dependency,
and security policy before there is evidence those are needed.

## 4. `low_cost_experiment`

Before committing to a new runtime command, build a temporary out-of-tree
consumer with only three allowed operations: invoke installed
`tritrack validate contract --json`, read one invented canonical artifact, and
write a namespaced receipt to an absent directory. Run it against:

- one valid canonical artifact;
- the same semantic JSON with noncanonical bytes;
- an unknown schema version;
- an artifact changed after validation;
- an existing output path; and
- a wheel installation from which the repository source is unavailable.

If the consumer cannot safely bind its output without importing engine code or
duplicating validation rules, add the smallest discovery or canonical-byte
helper to the CLI. If it can, do not add a new runtime API.

## 5. `contrarian_challenge`

Task 13 may require no new product code. The contracts, `tritrack validate`, and
immutable manifests could already be the seam; the real defect may be only
that the compatibility and ownership promise is undocumented and untested
from outside the source checkout. A new handoff contract might become a
redundant eleventh authority-like object and weaken the system it is meant to
clarify.

## 6. `unconstrained_possibility`

In a future major version, generate language-neutral SDKs and conformance
vectors from an authority graph: each artifact node would declare its owner,
canonical encoding, parents, validators, allowed projections, and privacy
class. Downstream adapters in any language could certify against the same test
kit. This would be valuable only after multiple independent consumers expose
real common requirements.

## 7. `overlooked_risks`

- A descriptor that lists contracts but does not bind its own version and
  bytes is documentation, not a machine-checkable seam.
- A sample adapter can accidentally become normative even if its output shape
  was meant as an example.
- Valid schema bytes are not always sufficient authority; some claims require
  cross-artifact or complete-bundle validation.
- Reading an artifact after a separate validator process creates a time-of-
  check/time-of-use gap unless the adapter binds and rechecks exact bytes.
- Exporting transcript-bearing artifacts across the seam can widen custody
  without violating schema validation.
- Calling internal modules in the reference adapter would silently establish
  an unsupported Python API.
- Naming downstream products or directories in engine policy would reverse the
  dependency and leak domain assumptions.
- Adding a new packaged file requires exact wheel/sdist policy changes and can
  invalidate Task 12's package-neutrality baseline; Task 13 must report this
  honestly rather than claim Task 12 byte equality.

## 8. `assumptions_to_verify`

- A batch/file process seam is adequate for the expected integration cadence.
- Existing CLI summaries expose enough hashes and scope facts for safe binding.
- At least one existing artifact set contains all facts a generic consumer
  legitimately needs; otherwise the seam must identify a closed set rather
  than one file.
- The reference proof can run after wheel installation without importing from
  the checkout.
- Canonical-byte requirements are either already enforced for every seam input
  or can be verified without duplicating engine logic.
- Downstream authors accept explicit major seam versions instead of inferred
  compatibility from package versions.

## 9. `recommended_next_decision`

Choose between:

A. an artifact-and-process seam plus out-of-tree conformance proof;
B. a stable Python facade; or
C. an in-process plugin protocol.

Recommend A, with a decision checkpoint after the low-cost experiment on
whether a new CLI discovery command is actually necessary. Do not add a new
authority artifact merely to label existing authorities.

Falsify A if the wheel-only consumer cannot bind and validate the required
facts atomically through installed commands without duplicating engine rules,
or if a real required consumer needs high-frequency in-process calls whose
measured process/file overhead is material. In that case choose the minimal
Python facade, not the plugin loader.
