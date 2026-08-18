# Task 13 multi-AI brainstorm synthesis

Date: 2026-08-18

Frozen packet SHA-256:
`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`

Decision owner: producer

No implementation began before this synthesis and producer decision.

## Consensus

- The missing mechanism is a bounded compatibility promise, not a specific
  downstream adapter.
- The preferred boundary is out-of-process and artifact-based: installed
  `tritrack` commands, closed versioned contracts, immutable bundles, exact
  hashes, and read-only validators.
- A public wheel-only, out-of-tree consumer with invented data is the most
  direct falsifiable proof that the engine remains generic authority.
- Downstream output must be a separately owned, namespaced sidecar bound to
  exact engine hashes. It must never write into, replace, or masquerade as an
  engine authority.
- An in-process plugin loader is premature and reverses the desired trust
  direction by running downstream code inside the authority process.

## Complementary ideas

- Codex emphasized starting with a no-new-runtime experiment and adding only
  the smallest missing discovery helper revealed by RED evidence.
- Gemini proposed an installed CLI schema-discovery surface and a reference
  sidecar envelope bound to the exact run-manifest hash.
- Together these form a staged decision: first prove whether the existing CLI
  and contracts are sufficient; add machine-readable discovery only if the
  wheel-only consumer otherwise has to duplicate engine rules.

## Provider-unique ideas

### Codex

- Recheck exact bytes after validation to close a time-of-check/time-of-use
  gap in any reference consumer.
- Avoid inventing an eleventh authority-like handoff artifact merely to label
  the ten existing authorities.
- Report Task 13 package changes honestly instead of extending Task 12's
  package-neutrality claim beyond its frozen target.

### Gemini

- Consider a read-only `schema`／`inspect schemas` command so non-Python
  consumers can discover installed contract versions and schemas.
- Demonstrate tamper rejection by binding a downstream sidecar to the exact
  `run-manifest.json` hash.
- Treat stable machine-readable CLI JSON and exit behavior as part of the seam
  and test it explicitly.
- The exact wrapper output was 10,497 bytes over 132 lines with SHA-256
  `e66cb6d32e88fa80f44841c02bd69e2016405d31284914f377be59ca1fbe6e9a`.
  The tracked public copy removes only three trailing spaces so
  `git diff --check` remains clean; no response word or structure changed. Its
  SHA-256 is
  `8a20230feaacf25e176848f89374fc5060198f5c77b3e3922d28567cafe0523f`.

### Claude

Claude produced no usable answer. Its only subscription-wrapper attempt ended
`claude-timeout` after preflight. Requested model was the dynamic `opus`
capability alias; observed and completed models are null; request dispatch is
ambiguous. The lane remains incomplete with no retry, downgrade, provider
substitution, API credential, PAYG, Console-credit, or extra-usage fallback.

## Contradictions

There was no disagreement about the architecture family. The open design
questions are about how much new public surface is justified:

- Codex: make the existing CLI／artifact boundary normative first, then add a
  discovery command only if a failing experiment proves it necessary.
- Gemini: include schema discovery in the pragmatic path from the start.
- Codex: keep the downstream receipt shape outside engine authority.
- Gemini: a documented or fixture-level reference envelope may help make the
  sidecar pattern concrete, but it should not be confused with an engine
  authority.

## Experiments

The shared low-cost experiment is an isolated consumer that receives only an
installed wheel and invented canonical artifacts. It may invoke public CLI
commands but may not import repository runtime modules. It must prove:

1. valid exact inputs are accepted;
2. an unknown schema version is rejected;
3. a changed byte or noncanonical authority is rejected where the selected
   authority scope promises that check;
4. its output binds exact engine input hashes and stays outside the run bundle;
5. an existing output path is preserved;
6. source-tree absence does not change behavior; and
7. validators make no write, network, credential, or private-data access.

If this consumer must duplicate contract discovery, canonicalization, bundle
semantics, or hash-scope rules, that observed RED justifies the smallest new
installed discovery surface.

## Risks

- Human CLI output may be parsed accidentally unless the seam names only
  machine-readable JSON and stable exit classes.
- Schema validity alone does not prove cross-artifact authority binding; the
  seam must name the correct validator scope.
- A separate validate-then-read sequence can race; the consumer must bind and
  recheck exact bytes or consume a scope whose final summary proves the exact
  hash it uses.
- A reference adapter or sidecar shape can become accidentally normative.
- Transcript-bearing artifacts can widen local custody even when structurally
  valid; the seam must state custody, not just syntax.
- Internal imports can create accidental compatibility obligations.
- A new descriptor or envelope can look like a second authority.
- New packaged members change Task 13 package facts; Task 12 byte identities
  remain historical evidence only.

## Options

### Option A — Existing artifact／CLI seam plus black-box proof

Make the existing versioned artifacts, immutable bundles, machine-readable
CLI summaries, exit classes, and validators the exclusive v1 downstream seam.
Add an authority／ownership／versioning specification and a wheel-only,
out-of-tree invented consumer test. The consumer writes a downstream-owned
sidecar bound to exact engine hashes. Add no runtime surface unless the test
first demonstrates an actual gap.

Tradeoff: smallest compatibility commitment and strongest proof against
private coupling, but discovery may initially require documented fixed
contract names.

### Option B — Machine-readable seam discovery plus black-box proof

Add everything in A plus a new read-only installed command that reports the
closed supported seam version, contract/schema versions, validator scopes,
authority roles, and explicit compatibility/non-authority rules.

Tradeoff: clearer feature discovery for non-Python consumers, but the
descriptor and its JSON output become another stable public contract that must
be versioned and maintained.

### Option C — Stable Python read-only facade

Add everything needed for proof plus a versioned Python namespace exposing
only frozen read-only loaders and validators.

Tradeoff: convenient for Python consumers, but creates Python ABI, exception,
typing, and supported-version obligations and excludes other languages.

An in-process plugin protocol is rejected for Task 13 as disproportionate and
trust-direction reversing.

## Recommendation

Choose Option A. Treat a new discovery command as a test-driven escalation:
only add it if the isolated consumer cannot integrate without duplicating
engine-owned rules. This makes Task 13 a proof of the authority already built,
not a new framework.

Falsify A if the wheel-only consumer cannot bind and validate the required
facts using public installed commands without source imports or rule
duplication, or if measured required invocation frequency makes the process
boundary materially unsuitable. The first failure upgrades to B; only the
second supports considering C.

## Provider status

| Lane | Requested | Observed | Completed | Result |
| --- | --- | --- | --- | --- |
| Codex | current primary model | `gpt-5.6-sol` | `gpt-5.6-sol` | completed independently before external outputs |
| Gemini REST wrapper | `gemini-3.7-flash` | `gemini-3.7-flash` | `gemini-3.7-flash` | completed; input 1,283, output 2,302, total 3,865 tokens |
| Claude subscription wrapper | dynamic `opus` alias | null | null | incomplete: `claude-timeout`, dispatch ambiguous |
