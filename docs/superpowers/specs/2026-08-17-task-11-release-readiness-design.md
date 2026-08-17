# Task 11 release-readiness design

Decision date: 2026-08-17

Decision owner: producer

Selected option: explicit four-mode end-user validator plus one separate
deterministic maintainer release gate

Frozen source candidate:
`b4e21d660170dfd000c99ba38f55f825565ab922`

## Decision

Task 11 closes the public alpha's remaining ordinary command and makes one
source candidate mechanically releasable without publishing it.

The task has two deliberately separate authority domains:

1. `tritrack validate` is a read-only, offline, end-user artifact validator.
2. `scripts/release_gate.py` is the repository-maintainer entry point for
   source privacy, package contents, build provenance, and release readiness.

The runtime command has no maintainer task state, release authority, Git
operation, build operation, network access, credential lookup, publication,
repair, or overwrite behavior. The maintainer gate is not exposed through the
end-user skill or runtime CLI.

## End-user command surface

Task 11 implements these exact help authorities:

```text
tritrack validate contract \
  --artifact ARTIFACT.json \
  [--json]

tritrack validate fcpxml \
  --artifact OUTPUT.fcpxml \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --binding basic-title-v1 \
  [--json]

tritrack validate paper \
  --aligned ALIGNED.json \
  --workbook PAPER.xlsx \
  [--json]

tritrack validate run \
  --run RUN-DIRECTORY \
  [--json]
```

No mode guesses a file type from a suffix, scans sibling directories, searches
for authorities, repairs an artifact, or creates an output. The caller selects
one mode and supplies every authority required by that mode.

## Validation scopes

Every successful result includes one exact `validationScope`. A scope is a
claim boundary, not a confidence score.

### `contract`

`validate contract` reads one bounded regular non-symlink JSON file. It accepts
only a closed `schemaVersion` registered in the installed contract package and
calls the same `contracts.validate_contract` authority used by product
consumers.

Success proves only:

- the artifact is valid under that installed JSON Schema contract; and
- the reported SHA-256 identifies the exact bytes that were validated.

It returns `validationScope: contract`. It does not prove that a referenced
source, parent artifact, model, media file, workbook, receipt, manifest chain,
or cross-file SHA-256 exists or matches. It does not add a separate
canonical-byte requirement when the existing contract does not require one.

Unknown, missing, non-string, or unregistered `schemaVersion` values fail
closed. Arbitrary JSON Schema files and third-party JSON are outside scope.

### `fcpxml`

`validate fcpxml` reads one bounded regular non-symlink FCPXML file and reuses
the existing installed profile, title-binding, and structural FCPXML validator.
It returns `validationScope: structural-profile`.

Success proves that the exact bytes satisfy the installed structural checks
for the explicit public profile and title binding. It performs no source-media
probe, DTD lookup, network request, external entity resolution, Final Cut
launch, GUI import, or round trip. The result therefore makes no DTD, media
availability, application, or target-machine compatibility claim.

### `paper`

`validate paper` reads the exact aligned transcript and XLSX workbook through
the same bounded regular-file and archive-safety boundaries used by
`paper apply`. It re-derives the complete cue reference grid and public-safe
workbook manifest, verifies immutable identity and display cells, rejects
formulas and unsupported workbook structure, and validates editor-authored
question and selection intent.

It returns `validationScope: authority-bound`. Success proves that the supplied
workbook is acceptable against the exact supplied aligned transcript bytes.
It does not publish `grouping-v1`, normalize the workbook, or change either
input. Task 11 extracts one pure validation seam from the existing apply path;
`paper apply` and `validate paper` must not diverge in acceptance semantics.

### `run`

`validate run` calls the same complete immutable-bundle loader used by
`tritrack run status`. It validates the exact phase-specific artifact set,
fixed filenames, bounded regular members, manifest schema and semantics,
artifact SHA-256 values, prior-manifest chain, and supported artifact contracts.

It returns `validationScope: complete-run-bundle`. `run status` and
`validate run` share the loader and sanitized summary builder. The two commands
may use different outer summary schema names, but their run ID, phase, next
action, stages, logical artifacts, and hashes must be equal for the same bytes.

## Runtime summary and failure boundary

The JSON completion summary is closed and contains only:

- one validator-summary schema version;
- tool version;
- artifact kind;
- `validationScope`;
- exact validated artifact or authority hashes; and
- bounded, non-content counts that apply to the selected mode.

It contains no absolute or relative path, filename, transcript text, cue text,
question text, notes, FCPXML text, workbook cells, command arguments, logs,
credentials, timestamps, or duration. Human-readable output follows the same
information boundary.

Validation errors use stable `TRITRACK_VALIDATE_*` prefixes at the new command
boundary while preserving existing component codes when a reused authority
rejects an artifact. The CLI retains the project's established exit classes:

- malformed command intent: `64` (usage);
- invalid schema, content, structure, binding, or semantic authority: `65`
  (data);
- unsupported profile or policy: `78` (policy);
- missing or unreadable input: `74` (I/O); and
- no failure prints a traceback, input content, matched secret, or full path.

All runtime inputs are read through bounded, regular non-symlink file or
directory boundaries. The validator writes no output, temporary artifact,
receipt, cache, repaired file, or adjacent state.

## Maintainer release-gate entry point

The only repository-owned Task 11 release-readiness entry point is:

```text
python scripts/release_gate.py \
  --source . \
  --output .release-evidence/CANDIDATE
```

The output directory and its parent follow the existing absent-output rule:
the parent exists, the requested output is absent, and an existing path or race
winner is never overwritten. The gate builds in invocation-owned staging,
publishes package artifacts into the reserved directory, and publishes
`release-manifest.json` last. Ordinary failures remove only unpublished state
created by that invocation. A crash may leave a mechanically incomplete
directory with no manifest; the gate never repairs or resumes it.

Release mode requires:

- the public project identity to match `public-engine`／`OSS`;
- an exact Git `HEAD` candidate;
- no tracked or untracked change outside ignored output roots; and
- the package version, runtime `__version__`, distribution names, and artifact
  basenames to agree.

Task 11 also closes the interpreter-eligibility claim. The current
`requires-python >=3.12` range would allow an unverified Python 3.14 install,
while the selected release matrix covers exactly Python 3.12 and 3.13. The
package metadata therefore becomes `>=3.12,<3.14`; classifiers and public setup
documentation name the same two-version set. Adding Python 3.14 later requires
its own green compatibility evidence and metadata change.

The ordered gate stages are:

1. project, Git, version, and clean-candidate identity;
2. tracked-source inventory and privacy checks;
3. wheel and sdist build;
4. bounded archive safety, member inventory, privacy, metadata, and content
   contracts;
5. fresh environment wheel installation, `pip check`, installed CLI help,
   eleven-component registry, and four-mode invented validation smoke; and
6. exact artifact hashing and manifest-last publication.

The script performs no tag, release, upload, signing, attestation, remote
mutation, branch-protection change, tester contact, or application operation.

## `release-manifest.json`

The manifest uses a new closed receipt schema owned by the maintainer gate. It
records:

- schema version and gate version;
- exact candidate commit;
- distribution name and project version;
- tracked-source file count and one canonical inventory SHA-256;
- actual build Python implementation/version;
- actual build frontend and backend versions;
- wheel and sdist safe basenames, byte sizes, exact SHA-256 values, member
  counts, and canonical member-inventory SHA-256 values;
- the ordered gate names and `passed` outcomes; and
- explicit non-claims for reproducible bytes, publication, signatures,
  attestations, Final Cut, DTD, and GUI evidence.

It records no timestamp, duration, local path, account, host name, credential,
Git remote token, CI run ID, workflow URL, logs, source text, or matched private
content. Repeating the gate with identical source, toolchain, and build outputs
must produce identical manifest bytes. Task 11 records exact build provenance;
it does not claim that independently built wheel or sdist bytes are
reproducible until the separate experiment proves that property.

## Privacy gate

The source scan enumerates the complete Git-tracked index and requires every
entry to be one expected regular file. A tracked symlink, submodule, unsupported
mode, or path outside the public distribution policy fails closed rather than
being skipped. The scanner does not walk a developer workspace, virtual
environment, ignored output, source-media folder, or adjacent repository.

The archive scan first rejects unsafe structure before reading member content:

- absolute or parent-traversing member names;
- symlinks, hard links, devices, or unsupported member types;
- duplicate or case-colliding names;
- excess member count, individual expanded size, or total expanded size; and
- members outside the distribution's exact allowlisted roots.

Source and accepted archive members are then checked for public generic
privacy boundaries:

- absolute macOS, Linux, Windows-home, and mounted-volume path shapes;
- credential assignments or credential-like high-entropy values;
- unexpected media, transcript, database, archive, executable, or proprietary
  asset types; and
- repository-boundary tokens already declared by public governance tests.

The tracked implementation contains only generic patterns and invented
canaries. It never embeds a real credential, private path, production name, or
private-media excerpt. A failure reports only a stable gate code and public
artifact class; it never echoes the matching bytes. Narrow documented
false-positive exceptions must bind an exact public file and rule ID, never a
secret value or arbitrary directory.

## Distribution content contracts

### Wheel

The wheel contains only:

- `tritrack_editing_assistant` runtime Python modules;
- installed strict schemas, compatibility profiles, and any implemented
  provider resource explicitly named by package data;
- console-script and standard distribution metadata; and
- Apache-2.0 license／notice material in standard wheel metadata locations.

It excludes tests, fixtures, examples, repository docs, review packets,
maintainer governance, the maintainer skill, release tools, CI configuration,
and the end-user skill.

### Sdist

The sdist is the buildable and publicly verifiable source payload. Its exact
allowlist includes:

- runtime source and installed resources;
- `pyproject.toml` and any build manifest／constraints required to reproduce
  the declared build;
- invented tests and fixtures required to verify the source;
- `scripts/release_gate.py` and its public test support;
- `skills/tritrack-editing-assistant/SKILL.md` and its metadata;
- `README.md`, `LICENSE`, `NOTICE`, `CHANGELOG.md`, `CONTRIBUTING.md`, and
  `SECURITY.md`; and
- the bounded Task 11 public design and verification documents required to
  understand the artifact and claim boundary.

It excludes ignored outputs, local environments, media, credentials, private
state, raw external-review attempts, and unrelated maintenance-history packets.
The exact member allowlist is tested; new members require an intentional test
and policy change.

The end-user skill is source-distributed and separately installable. Installing
the Python wheel does not install or register that skill. Documentation must
use those exact claims and must not broaden Task 10's repository-installed
skill evidence into a wheel-install claim.

## CI design

The public workflow uses fixed, non-`latest` runner labels verified against the
official GitHub runner-image catalog before implementation:

- `ubuntu-24.04` (x64); and
- `macos-26` (arm64).

The Python matrix and `requires-python >=3.12,<3.14` metadata both declare the
3.12 and 3.13 support set. Adding Python 3.14 or another OS is a separate
compatibility decision.

The workflow has three layers.

### `test-matrix`

Four cells run Ubuntu／macOS × Python 3.12／3.13. Every cell:

- installs the source and exact development constraints;
- runs the complete unittest suite;
- compiles public Python surfaces;
- builds a local non-editable wheel;
- installs that wheel into a fresh environment outside the checkout;
- runs `pip check`; and
- runs installed help, component-registry, and four-mode invented smoke.

Each cell builds locally. Task 11 does not transfer packages between jobs with
an artifact-upload action.

### `quality`

One `ubuntu-24.04`／Python 3.13 cell runs Ruff, the maintainer/end-user role and
privacy boundary tests, deterministic configuration checks, and repository-
self-contained skill checks. The canonical external skill validator remains a
local closeout requirement when it is not part of the public repository; CI
does not pretend to have that external tool.

### `release-gate`

One canonical `ubuntu-24.04`／Python 3.13 cell runs the complete maintainer
release gate. Its package output is job-local and is not uploaded, published,
signed, or attested.

Workflow permissions remain:

```yaml
permissions:
  contents: read
```

Third-party Actions are pinned to exact commit SHA values resolved from their
official repositories during implementation. Build and development tooling are
pinned by a repository-owned exact constraints file; runtime dependency
metadata keeps its reviewed compatibility ranges. The release manifest records
the actual resolved toolchain.

## CI and release claim boundary

Passing CI proves only that:

- the Python contract and installed CLI passed on the named runner/Python
  cells;
- the wheel installed and passed the declared smoke checks;
- tracked source and built distributions passed the declared privacy and
  content gates; and
- one exact candidate produced the artifact hashes in its local release
  manifest.

It does not prove a licensed Final Cut installation, DTD validation, GUI
import, round trip, macOS 26.5.2 compatibility, independent build
reproducibility, publication, signature, attestation, or downstream private
integration. A post-push verification record may record a GitHub Actions run ID
and exact public remote SHA; those transient facts do not enter the deterministic
release manifest.

## Experiment before implementation

Before freezing any reproducibility or member-inventory assertion in tests,
Task 11 runs one disposable experiment against the frozen source candidate:

1. build wheel and sdist twice in separate absent directories with a fixed
   `SOURCE_DATE_EPOCH` and the same toolchain;
2. compare full archive SHA-256 values;
3. compare normalized safe member lists and per-member content SHA-256 values;
4. inspect license, schema, profile, source, test, policy, and skill membership;
5. install the wheel in a new repository-external environment; and
6. record only observed facts in the design implementation plan.

If full archive hashes differ, Task 11 validates exact final artifact hashes
and normalized member equivalence but makes no reproducible-byte claim. The
experiment does not mutate tracked source and its scratch output is discarded.

## TDD and verification target

Implementation preserves observed RED-to-GREEN evidence in five groups.

### Runtime validators

- all four help surfaces and stable CLI mappings;
- valid, invalid, malformed, unknown-contract, missing, unreadable, symlink,
  oversized, and late-change inputs;
- exact successful hashes and scope labels;
- contract-only non-claims;
- FCPXML structural/profile validation with DTD, entity resolution, network,
  media probing, and application launch absent;
- paper authority rebinding with no grouping publication;
- complete run-bundle validation; and
- byte-for-byte input immutability and no created files.

### Shared authority

- `paper apply` and `validate paper` accept and reject the same workbook facts;
- `run status` and `validate run` return equal core facts for the same bundle;
  and
- refactoring does not create a second schema, workbook, FCPXML, or run
  authority.

### Privacy and release gate

- every invented path and credential canary;
- failure-output redaction;
- tracked-file scoping;
- archive traversal, link, duplicate, case-collision, type, count, and size
  rejection;
- exact wheel and sdist content allowlists;
- existing output and publication races;
- cleanup of invocation-owned state; and
- manifest-last completeness.

### Packaging and installed acceptance

- real wheel and sdist build;
- exact member inventories and required license／resource presence;
- absent forbidden files;
- repository-external fresh installation;
- `pip check`;
- eleven-component registry unchanged; and
- all four installed validator modes exercised with invented artifacts.

### Closeout

- focused tests and complete suite;
- Ruff and compilation;
- public project identity;
- maintainer and end-user role-boundary tests;
- canonical validation of both skills in the local maintainer environment;
- privacy and package gates;
- `git diff --check`;
- the four-cell public CI matrix and canonical release-gate job; and
- independent closeout review with ordinary in-scope fix-forward.

`STATUS.md` changes only after the coherent package is green. The standing
grant then permits fast-forward integration into `main`, pushing the existing
public `origin`, and exact remote-SHA backup verification. No tag, release,
pull request, package publication, tester contact, application submission,
force-push, remote change, or visibility change is performed.

## Deferred alternatives and non-goals

- automatic artifact-type detection or sibling discovery;
- an all-purpose validation DAG or plugin framework;
- a maintainer/release flag in the end-user command;
- a separate end-user-skill release archive;
- wheel installation or automatic registration of the end-user skill;
- SBOM, signing, SLSA provenance, OIDC, package attestation, release workflow,
  tag, GitHub release, or PyPI publication;
- adding Python 3.14 or broadening the public compatibility profile;
- live provider transport, credentials, upload, or deletion;
- new editing semantics, cue changes, media processing, or Final Cut
  automation;
- Task 12 alpha freeze and independent candidate review; and
- Task 13 downstream integration.

## Brainstorm provenance

The frozen public problem packet SHA-256 was
`ff145c249aae193ce80872783b8f95e840684ee3a518e4cc2788cc607aa15921`.

Codex completed its independent first round before reading any external output.
Its response SHA-256 was
`0bdc84c66d5ca5012bcee89e8e757b0c47dae3c9e0e178a7c5118ec6427cd6c0`.

Gemini dynamically requested, observed, and completed `gemini-3.7-flash`.
Its response SHA-256 was
`1d682f99a8cfad8473c574d1e4c645a1279e56e99cf55d359a16645c896e3379`.

Claude requested the dynamic `opus` capability alias through the approved
subscription-only wrapper. Attempt
`637f7c3a-cf72-4e97-9d42-ef7ef0d1400e` ended `claude-timeout`; observed and
completed models are null and request completion is ambiguous. The lane remains
explicitly incomplete with no retry, downgrade, paid credential, provider
fallback, or completion claim.

The producer selected the four-mode validator and approved the architecture,
validation semantics, maintainer release/packaging boundary, CI/provenance
boundary, and privacy/error/acceptance design on 2026-08-17.
