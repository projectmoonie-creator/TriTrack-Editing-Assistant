### 1. `problem_reframe`

The core problem is not "how does a downstream consumer execute or extend TriTrack," but **how an untrusted, out-of-tree consumer unambiguously verifies and ingests TriTrack artifacts without TriTrack giving up custodial authority or stabilizing internal Python internals.**

If downstream integrations consume internal Python imports (`tritrack.core.*`), TriTrack creates an accidental, unbounded API commitment. If downstream integrations read raw filesystem directories without contract validation, they risk mutating state or making unauthorized assumptions about intermediate state.

Therefore, the seam is strictly an **externalized artifact and invocation contract**:
1. TriTrack emits sealed, immutable, canonical JSON run bundles and validation verdicts.
2. Downstream consumers consume these as read-only inputs through the CLI and canonical JSON artifacts, using standard schema validation and bundle manifest hash checking.
3. Downstream outputs (e.g., downstream policies, external execution reports, downstream-specific envelopes) are strictly out-of-tree sidecars referencing TriTrack run manifests by exact SHA-256 hash, with zero write-back into the TriTrack run bundle.

---

### 2. `pragmatic_path`

The narrowest, lowest-risk implementation is a **CLI Contract Introspection & Sidecar Envelope Proof**:

- **CLI Contract & Schema Discovery:** Add a non-mutating CLI inspection command (`tritrack inspect schemas` or `tritrack schema <name> [--version]`) that prints canonical JSON schemas and supported schema versions directly from the installed wheel.
- **Strict Bundle Ingestion Verification (`tritrack validate bundle <dir>`):** Keep the existing bundle validator as the single source of truth for downstream consumption validation.
- **Example Downstream Reference Adapter Specification (Documentation + Fixture Contract):**
  - Define an example minimal JSON schema for downstream consumption (e.g., `downstream-reference-envelope.schema.json` or a documented specification) that lives in documentation/tests.
  - The downstream envelope captures:
    1. `targetManifestHash`: exact SHA-256 of the TriTrack `run-manifest.json`.
    2. `targetSchemaVersion`: TriTrack manifest schema version.
    3. `downstreamPayload`: domain-specific data produced out-of-tree.
- **Integration Test Suite (Wheel-Only):**
  - A wheel-isolated test script running as a simulated external process that:
    1. Runs `tritrack run ...` or validates an existing bundle fixture.
    2. Inspects TriTrack schemas via CLI.
    3. Emits an out-of-tree sidecar referencing the run manifest hash.
    4. Proves that modifying the TriTrack bundle invalidates the sidecar reference and fails bundle verification.
    5. Confirms that attempting to import internal modules from a non-supported path fails or emits an unstable warning, proving the seam is CLI/Artifact-only.

**Tradeoffs:**
- *Pros:* Zero changes to core calculation logic; zero new daemon/RPC/plugin infrastructure; fully testable via installed wheel in CI; clean fail-closed isolation.
- *Cons:* Downstream consumers must operate via process boundary or direct file/schema validation rather than linked in-process Python calls.

---

### 3. `alternative_architecture`

**Stable Python Read-Only Ingest Module (`tritrack.api.v1` / Pure Data Transfer Objects):**
- Expose a frozen, minimal Python namespace (`tritrack.api`) providing strictly read-only, schema-validated loader functions:
  ```python
  from tritrack.api.v1 import load_run_bundle, validate_contract
  ```
- These functions load, parse, verify SHA-256 bundle manifests, and return frozen, read-only Python dataclasses/dicts corresponding directly to the JSON contract schemas.
- Explicitly mark all other namespaces (`tritrack.internal.*`, `tritrack.cli.*`, `tritrack.engine.*`) as private and subject to breaking changes without notice.

**Tradeoffs:**
- *Pros:* Higher ergonomics for Python-based downstream tools; avoids CLI subprocess overhead and JSON string serialization parsing if running in Python environments.
- *Cons:* Expands the public maintenance surface; requires Python version stability guarantees; risks downstream tools attempting in-memory mutations or monkeypatching unless aggressively frozen.

---

### 4. `low_cost_experiment`

**Experiment:** Build a standalone, out-of-repo simulated consumer script (`test_downstream_seam.py`) in CI that treats `tritrack` purely as an installed black-box package.

**Steps:**
1. Install TriTrack from the built wheel (`.whl`) into a clean virtual environment with `PYTHONPATH=""`.
2. Generate or extract a valid run bundle fixture.
3. Assert that `tritrack validate bundle <path>` returns exit code `0` with machine-readable JSON output on `--json`.
4. Intentionally tamper with one byte in an upstream transcript JSON artifact; assert that `tritrack validate bundle` returns non-zero and pinpointed hash mismatch.
5. Ingest the bundle via the simulated downstream script, generate a downstream sidecar JSON referencing the manifest hash, and verify the reference.
6. Verify that running `python -c "import tritrack.some_internal"` produces no supported API guarantee (or is prevented by testing strict entry-point boundaries).

**Falsification Criteria:**
- If the downstream script requires importing any non-public Python symbol to verify bundle integrity, the experiment fails.
- If downstream tampering can go undetected by `tritrack validate`, the authority boundary fails.

---

### 5. `contrarian_challenge`

**Challenge: Does Task 13 actually require any new code or schemas at all?**

*Argument:* Tasks 1–12 already defined 10 closed JSON contracts, manifest-last bundle completion, deterministic SHA-256 hashing, and four read-only validation scopes in `tritrack validate`.

If the public engine's authority is *already* fully encapsulated by its immutable artifacts and CLI validator, then adding new schemas, plugin APIs, or export formats creates unneeded complexity and violates the "narrow steel thread" constraint.

*Alternative approach:* Task 13 could be purely:
1. An explicit **Authority & Seam Contract Document** (e.g. `docs/integration-seam.md`) defining the invariants, manifest pinning rule, and sidecar model.
2. A single end-to-end integration test asserting that out-of-tree verification and sidecar referencing work exclusively using existing CLI and JSON artifacts.
3. Formal declaration that the CLI and JSON schemas *are* the sole v1 integration surface.

---

### 6. `unconstrained_possibility`

If freed from public-alpha scope limits, the seam could be structured as an **Attestation & Cryptographic Manifest Log**:
- Run manifests include cryptographic signatures (ed25519) and deterministic Merkle tree roots of all inputs, sync maps, and outputs.
- A content-addressable storage (CAS) interface where artifacts are stored by exact content hash (`sha256:...`).
- Downstream systems attach signed provenance records (in-toto / SLSA-style attestations) claiming downstream actions against a specific immutable root hash.
- A WebAssembly (Wasm) verification target compiled from the validation core allowing downstream runtimes (browser, Node, Rust, Python) to verify bundle authority in-process without invoking the Python CLI.

---

### 7. `overlooked_risks`

1. **Stdout/Stderr Format Drifts:** Downstream tools wrapping the CLI might parse human-readable stdout instead of structured exit codes or JSON output. If TriTrack CLI output changes, downstream tooling breaks silently unless `--json` flags on validation commands are strictly contract-tested.
2. **Bundle Mutation Race Conditions:** If a downstream tool attempts to read a bundle while TriTrack is still executing (violating the manifest-last rule), it might read partial outputs. The seam must enforce that a bundle is only valid if `run-manifest.json` exists and matches all artifact hashes.
3. **Implicit Path Dependency Leakage:** Absolute paths in run manifests or receipt metadata could leak build-machine or editor-machine directory structures to downstream systems, creating brittle environment couplings.
4. **Accidental `__all__` Exposure:** Downstream Python developers will naturally attempt `import tritrack`. If the top-level `__init__.py` exposes internal helpers without an explicit deprecation or private-warning policy, maintainers face immediate breaking-change pressure.

---

### 8. `assumptions_to_verify`

1. **Wheel Isolation:** Verify that `tritrack validate` works identically when installed in an isolated environment without access to the Git repository root or test fixtures.
2. **Validation Output Machine-Readability:** Verify whether `tritrack validate` currently provides deterministic, machine-parseable exit codes and JSON output suitable for automated downstream callers.
3. **No-Write Invariant:** Verify that `tritrack validate` across all 4 scopes is guaranteed read-only and will never touch `mtime`, create lockfiles, or alter files in the target directory.
4. **Deterministic Hash Invariance:** Verify that re-running canonical serialization and hashing across supported platforms (Linux, macOS, Windows) produces identical byte hashes for identical inputs.

---

### 9. `recommended_next_decision`

#### Producer Decision
The producer must choose between:

- **Option A (Pure Contract & Test Seam):** Declare the CLI and existing 10 JSON schemas as the complete, exclusive v1 seam. Implement zero new runtime code except CLI schema introspection / JSON validation flags if missing, accompanied by an integration-seam document and a wheel-installed downstream consumption test.
- **Option B (Python Ingest SPI):** Expose a dedicated, frozen `tritrack.api.v1` read-only loading/validation Python interface alongside the CLI.

#### Recommendation
**Choose Option A.**

Option A strictly enforces fail-closed, out-of-process isolation, prevents accidental Python API stabilization, preserves the 11-component product registry, and provides the exact falsifiable proof required for public alpha without long-term maintenance baggage.

#### Falsification Evidence
This recommendation is falsified if:
1. Performance requirements demand sub-millisecond in-process artifact passing where CLI process invocation latency is demonstrably unacceptable for public-alpha consumers; or
2. Downstream consumption cannot be completely accomplished using standard Draft 2020-12 JSON Schema validation and SHA-256 hash checks on the canonical artifacts.