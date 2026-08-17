# Task 11 release readiness implementation plan

> **For Codex:** Execute this plan with the official Superpowers
> `test-driven-development` workflow. Preserve each observed RED before the
> matching minimal GREEN implementation. Use `reviewing-with-multiple-ai` only
> after the complete local candidate is frozen.

**Goal:** Ship the four-mode offline `tritrack validate` command and a
maintainer-only, fail-closed release gate that proves source privacy, package
contents, reproducibility, clean-wheel installation, and fixed public CI
coverage without publishing a tag, release, package, or external artifact.

**Architecture:** End-user validation lives in the installed Python package and
reuses the existing contract, FCPXML, paper-workbook, and immutable-run
authorities. Maintainer release logic lives under `scripts/`, reads the complete
Git index, builds only from two clean snapshots of one commit, inspects archives
before extraction or installation, and publishes a path-free manifest last.
The two authority domains share no release controls or network behavior.

**Tech stack:** Python 3.12/3.13, `jsonschema` Draft 2020-12, `openpyxl`,
`setuptools`/`build`, standard-library ZIP/TAR inspection, `unittest`, Ruff,
GitHub Actions on fixed Linux x64 and macOS arm64 images.

**Approved design:**
`docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md` at
commit `87d4c32`. Do not broaden its grants or non-claims.

**Verified packaging premise:** A two-snapshot experiment at the approved-spec
commit produced byte-identical wheels. The two sdists had identical 60-member
extracted trees but different compressed bytes. Therefore the implemented
reproducibility contract is exact wheel-byte equality plus exact normalized
sdist member/content-inventory equality. The final chosen wheel and sdist still
receive their own exact SHA-256 values in `release-manifest.json`.

**Pinned CI inputs:**

- `actions/checkout@v7.0.1` →
  `3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/setup-python@v7.0.0` →
  `5fda3b95a4ea91299a34e894583c3862153e4b97`
- build constraints: `build==1.5.0`, `packaging==26.3`, `pip==26.2`,
  `pyproject-hooks==1.2.0`, `ruff==0.16.2`, `setuptools==84.0.0`, and
  `wheel==0.48.0`

---

### Task 1: Add strict installed-contract discovery and the contract validator

**Files:**

- Modify: `src/tritrack_editing_assistant/contracts.py`
- Create: `src/tritrack_editing_assistant/validate_artifacts.py`
- Create: `tests/test_validate_artifacts.py`

- [ ] **Step 1: Write the failing contract-mode tests**

Add tests that create invented valid instances for every name in
`CONTRACT_NAMES`, write canonical or non-canonical JSON bytes to a regular
file, and assert:

- `validate_contract_artifact(path)` discovers the contract only from the
  installed schema's exact `schemaVersion.const`;
- the returned summary is exactly `tritrack.validate-summary/v1`, kind
  `contract`, scope `contract`, the tool version, one artifact SHA-256, an empty
  bounded count map, and details containing only `contractName` and
  `contractSchemaVersion`;
- no input is written or normalized;
- unknown, missing, duplicate-schema, malformed UTF-8/JSON, non-regular,
  symlink, empty, oversized, schema-invalid, and late-changed inputs fail with
  stable `TRITRACK_VALIDATE_*` codes;
- summaries and errors contain no artifact path or artifact content.

Build the duplicate-schema case by mocking `load_schema`; do not add a fake
installed contract.

- [ ] **Step 2: Run the focused test and observe RED**

Run:

```bash
python -m unittest tests.test_validate_artifacts.ContractValidationTest -v
```

Expected: import failure because `validate_artifacts` and schema-version
discovery do not exist.

- [ ] **Step 3: Implement the smallest strict contract seam**

In `contracts.py`, add a cached closed map and lookup:

```python
@cache
def contract_names_by_schema_version() -> Mapping[str, str]:
    mapping: dict[str, str] = {}
    for name in sorted(CONTRACT_NAMES):
        schema = load_schema(name)
        version = schema["properties"]["schemaVersion"]["const"]
        if not isinstance(version, str) or version in mapping:
            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID")
        mapping[version] = name
    return MappingProxyType(mapping)


def contract_name_for_schema_version(schema_version: object) -> str:
    if not isinstance(schema_version, str):
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN")
    try:
        return contract_names_by_schema_version()[schema_version]
    except KeyError as error:
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN") from error
```

In `validate_artifacts.py`, define:

```python
MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024

@dataclass(frozen=True)
class LoadedValidationArtifact:
    path: Path
    encoded: bytes
    sha256: str
```

Add `validate_contract_artifact(path: Path) -> dict[str, object]` with the
exact behavior below.

Use an `O_NOFOLLOW` regular-file reader, strict UTF-8, `Decimal` for JSON
floats, the installed schema-version map, `contracts.validate_contract`, and a
second exact-byte verification before returning. Normalize all parser/schema
exceptions to stable codes without embedding exception text.

The shared summary builder must emit only:

```python
{
    "schemaVersion": "tritrack.validate-summary/v1",
    "toolVersion": __version__,
    "artifactKind": kind,
    "validationScope": scope,
    "hashes": hashes,
    "counts": counts,
    "details": details,
}
```

- [ ] **Step 4: Run focused tests and the contract regressions**

Run:

```bash
python -m unittest tests.test_validate_artifacts.ContractValidationTest tests.test_contracts -v
```

Expected: PASS.

- [ ] **Step 5: Commit the contract slice**

```bash
git add src/tritrack_editing_assistant/contracts.py \
  src/tritrack_editing_assistant/validate_artifacts.py \
  tests/test_validate_artifacts.py
git commit -m "feat: add strict contract artifact validation"
```

---

### Task 2: Add the profile-bound FCPXML validator mode

**Files:**

- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
- Modify: `tests/test_validate_artifacts.py`
- Modify: `tests/test_emit_fcpxml.py`

- [ ] **Step 1: Write the failing FCPXML-mode tests**

Render invented valid XML through the existing emitter and assert
`validate_fcpxml_artifact(path, profile_id, binding_id)`:

- loads only the exact installed profile and title binding;
- delegates structural/profile/title/time validation to
  `emit_fcpxml.validate_fcpxml`;
- returns kind `fcpxml`, scope `structural-profile`, the exact byte hash, empty
  counts, and only `profileId`/`bindingId` details;
- performs no DTD lookup, media probe, subprocess, network call, output write,
  or Final Cut operation;
- rejects unknown profile/binding, wrong profile/title/time, entity/extra
  doctype, malformed UTF-8/XML, symlink, oversize, and late change;
- never reports a DTD, GUI import, or round-trip claim.

- [ ] **Step 2: Run the focused test and observe RED**

```bash
python -m unittest tests.test_validate_artifacts.FcpxmlValidationTest -v
```

Expected: missing `validate_fcpxml_artifact`.

- [ ] **Step 3: Implement by composition, not duplicate parsing policy**

Add:

```python
def validate_fcpxml_artifact(
    path: Path,
    *,
    profile_id: str,
    binding_id: str,
) -> dict[str, object]:
    artifact = _load_regular_artifact(path, code="TRITRACK_VALIDATE_INPUT_UNREADABLE")
    try:
        text = artifact.encoded.decode("utf-8", errors="strict")
        profile = doctor.load_profile(profile_id)
        binding = doctor.load_title_binding(binding_id)
        emit_fcpxml.validate_fcpxml(text, profile=profile, binding=binding)
    except UnicodeError as error:
        raise ValueError("TRITRACK_VALIDATE_FCPXML_INVALID") from error
    _verify_unchanged(artifact)
    return _validation_summary(
        kind="fcpxml",
        scope="structural-profile",
        hashes={"artifact": artifact.sha256},
        counts={},
        details={"profileId": profile_id, "bindingId": binding_id},
    )
```

Let existing exact `TRITRACK_PROFILE_*`, `TRITRACK_TITLE_BINDING_*`, and
`TRITRACK_FCPXML_*` codes propagate; do not print their exception causes.

- [ ] **Step 4: Run focused and emitter regressions**

```bash
python -m unittest tests.test_validate_artifacts.FcpxmlValidationTest \
  tests.test_emit_fcpxml -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/validate_artifacts.py \
  tests/test_validate_artifacts.py tests/test_emit_fcpxml.py
git commit -m "feat: add profile-bound FCPXML validation"
```

---

### Task 3: Extract read-only paper-workbook validation and add paper mode

**Files:**

- Modify: `src/tritrack_editing_assistant/paper_edit.py`
- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
- Modify: `tests/test_paper_edit.py`
- Modify: `tests/test_validate_artifacts.py`

- [ ] **Step 1: Write failing pure-paper tests**

Use the existing invented aligned/workbook fixtures. Assert:

- new `paper_edit.validate_workbook(aligned, workbook)` performs every check
  currently performed by `apply_workbook` but creates no output;
- `apply_workbook` and `validate_workbook` accept and reject exactly the same
  workbooks;
- changed cue/display/manifest values, formulas, hyperlinks, unsafe ZIPs,
  extreme dimensions, invalid selection references, symlinks, and late changes
  fail closed;
- the validated internal object may retain grouping only for `apply_workbook`,
  while the public validator summary contains no transcript, question text,
  note, cue text, workbook path, or grouping body.

The public `validate paper` summary must have kind `paper`, scope
`authority-bound`, aligned/workbook hashes, and exact cue/question/answer/
reserve counts.

- [ ] **Step 2: Run the focused tests and observe RED**

```bash
python -m unittest tests.test_paper_edit.PaperEditTest \
  tests.test_validate_artifacts.PaperValidationTest -v
```

Expected: missing `validate_workbook` and `validate_paper_artifacts`.

- [ ] **Step 3: Extract one immutable validation result**

Add a frozen `ValidatedWorkbook` dataclass with exactly these fields:
`aligned_sha256`, `workbook_sha256`, `workbook_schema_version`, `cue_count`,
`question_count`, `answer_count`, `reserve_count`, and the internal `grouping`.
Add `validate_workbook(aligned_path: Path, workbook_path: Path) ->
ValidatedWorkbook` with the docstring “Validate and re-derive one workbook
without publishing output.”

Move the existing aligned/workbook loading, cue-grid derivation, unsafe-state
checks, manifest verification, grouping derivation, and final input rehash into
this function. Keep `grouping` private to the Python seam. Refactor
`apply_workbook` to reserve the absent destination first, call
`validate_workbook`, and publish only `validated.grouping`.

Add `validate_paper_artifacts` in `validate_artifacts.py`; project only hashes
and counts from `ValidatedWorkbook` into the public summary.

- [ ] **Step 4: Run paper, organizer, and validation regressions**

```bash
python -m unittest tests.test_paper_edit tests.test_organizer \
  tests.test_validate_artifacts.PaperValidationTest -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/paper_edit.py \
  src/tritrack_editing_assistant/validate_artifacts.py \
  tests/test_paper_edit.py tests/test_validate_artifacts.py
git commit -m "refactor: share paper validation authority"
```

---

### Task 4: Share immutable-run inspection with status and add run mode

**Files:**

- Modify: `src/tritrack_editing_assistant/run_workflow.py`
- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
- Modify: `tests/test_run_workflow.py`
- Modify: `tests/test_validate_artifacts.py`

- [ ] **Step 1: Write failing run-inspection tests**

For invented prepared, aligned, and finished bundles, assert:

- `inspect_run(run_dir)` uses `load_bundle`, revalidates the complete fixed
  member set and exact hashes, then rechecks the bundle before returning;
- `status_run` and `validate_run_bundle` share the same `runId`, phase,
  `nextAction`, ordered stage names, and logical artifact hashes;
- the validation summary has kind `run`, scope `complete-run-bundle`, manifest
  hash, stage/artifact counts, and its exact existing run summary under
  `details.runSummary`;
- missing/extra members, malformed/noncanonical manifest, wrong phase set,
  broken chain facts, changed artifacts, symlinks, and late changes fail with
  existing run codes;
- both surfaces write nothing and expose no transcript/editor text or path.

- [ ] **Step 2: Run focused tests and observe RED**

```bash
python -m unittest tests.test_run_workflow.RunStatusTest \
  tests.test_validate_artifacts.RunValidationTest -v
```

Expected: missing `inspect_run`/`validate_run_bundle` or mismatched late-change
behavior.

- [ ] **Step 3: Implement one shared read-only run inspection**

Add:

```python
def inspect_run(run_dir: Path) -> tuple[LoadedRunBundle, dict[str, object]]:
    bundle = load_bundle(Path(run_dir))
    _require_bundle_unchanged(bundle)
    return bundle, summarize_bundle(bundle)


def status_run(run_dir: Path) -> dict[str, object]:
    return inspect_run(run_dir)[1]
```

Then add `validate_run_bundle` that calls `inspect_run` and projects its exact
facts. Do not add sibling discovery or a second bundle parser.

- [ ] **Step 4: Run full run/validator regressions**

```bash
python -m unittest tests.test_run_workflow \
  tests.test_validate_artifacts.RunValidationTest -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/run_workflow.py \
  src/tritrack_editing_assistant/validate_artifacts.py \
  tests/test_run_workflow.py tests/test_validate_artifacts.py
git commit -m "feat: share complete run validation"
```

---

### Task 5: Replace the placeholder with the exact four-mode CLI

**Files:**

- Modify: `src/tritrack_editing_assistant/cli.py`
- Modify: `tests/test_cli.py`
- Modify: `tests/test_validate_artifacts.py`

- [ ] **Step 1: Write CLI RED tests for all four help authorities**

Exercise `cli.main` and subprocess-installed help. Assert these exact forms:

```text
tritrack validate contract --artifact FILE [--json]
tritrack validate fcpxml --artifact FILE --profile ID --binding ID [--json]
tritrack validate paper --aligned FILE --workbook FILE [--json]
tritrack validate run --run DIRECTORY [--json]
```

For success, assert JSON is exactly the core summary and human output is only
stable tab-separated kind/scope/hash/count/detail facts. For failure, assert
one JSON object `{"error":"TRITRACK_*"}`, no traceback/content/path, and these
exit classes:

- usage `64` for parser or handler usage errors;
- data `65` for malformed or semantically invalid artifacts;
- I/O `74` for missing/unreadable/non-regular input;
- policy `78` for unknown installed profile/binding.

Also assert `validate` is removed only from `planned_commands`, no twelfth
component is added, and every mode performs zero writes/network/provider/
credential/subprocess operations.

- [ ] **Step 2: Run CLI tests and observe RED**

```bash
python -m unittest tests.test_cli.ValidateCliTest -v
```

Expected: `TRITRACK_COMMAND_NOT_IMPLEMENTED: validate` or missing nested help.

- [ ] **Step 3: Add parser, handler, exit mapping, and bounded printers**

Import `validate_artifacts as validate_module`. Add `_run_validate`,
`_validate_error_exit`, and `_print_validation_summary`. Add a
`TriTrackArgumentParser` whose non-help parse errors raise one private
`CliUsageError`; catch that error in `main`, print only
`{"error":"TRITRACK_USAGE"}`, and return `EXIT_USAGE`. Use the same parser
class for nested parsers so invalid or missing validate flags return 64 rather
than argparse's default 2. Add regression coverage for existing commands'
usage errors. Construct one required nested `validate` subparser with four
required mode parsers and only the flags above. Dispatch directly to the
matching core function.

Human output must use this closed projection:

```text
VALIDATION\t<artifactKind>\t<validationScope>
HASH\t<logical-name>\t<sha256>
COUNT\t<logical-name>\t<integer>
DETAIL\t<logical-name>\t<compact-json-scalar-or-object>
```

Sort hash/count/detail keys. Never stringify an exception or `Path`.

- [ ] **Step 4: Run focused and complete validator tests**

```bash
python -m unittest tests.test_cli.ValidateCliTest \
  tests.test_validate_artifacts -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tritrack_editing_assistant/cli.py tests/test_cli.py \
  tests/test_validate_artifacts.py
git commit -m "feat: implement four-mode offline validator"
```

---

### Task 6: Freeze Python support, distribution contents, and release schemas

**Files:**

- Modify: `pyproject.toml`
- Create: `requirements/ci-constraints.txt`
- Create: `MANIFEST.in`
- Create: `release/package-policy-v1.json`
- Create: `release/release-manifest-v1.schema.json`
- Create: `tests/test_packaging.py`
- Modify: `docs/reviews/task-10-closeout-packet-2026-08-17.md`
- Modify: `docs/superpowers/plans/2026-08-17-task-10-immutable-run.md`

- [ ] **Step 1: Write packaging RED tests**

Build two wheels and two sdists from separate copied source trees with
`SOURCE_DATE_EPOCH=1704067200` and `python -m build --no-isolation`. Assert:

- `requires-python` is exactly `>=3.12,<3.14`, classifiers are exactly 3.12 and
  3.13, runtime requirements retain bounded ranges, and all build/development
  tools resolve through exact constraints;
- wheels are byte-identical and contain only runtime package code/resources,
  entry-point metadata, and required license metadata;
- wheels contain no tests, docs, skills, CI, release scripts, source-only
  examples, caches, or generated evidence;
- sdists have identical normalized member/content inventories and contain the
  currently implemented buildable package source, all public runtime tests and
  helpers, the quickstart example, CI workflow, end-user skill, public
  policies, and approved Task 11 design;
- sdists exclude `.agents`, `test_maintainer_boundary.py`, raw external-review
  artifacts, historical implementation plans, ignored outputs, caches, and
  private/binary media;
- any unexpected wheel/sdist member fails the policy test.

This base packaging test must pass before release scripts exist. Task 8 extends
the same test and manifest with the completed release entry/core, while the
closeout task makes the Task 11 verification record mandatory before the real
gate.

- [ ] **Step 2: Run and observe RED**

```bash
python -m unittest tests.test_packaging -v
```

Expected: current `>=3.12`, missing constraints/policy files, and missing
end-user skill/policy documents in the sdist.

- [ ] **Step 3: Implement explicit package policy**

Change:

```toml
[build-system]
requires = ["setuptools==84.0.0"]

[project]
requires-python = ">=3.12,<3.14"

[project.optional-dependencies]
dev = ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"]
```

Write the seven exact tool/transitive constraints listed at the top of this
plan. Use `MANIFEST.in` to include only the approved base sdist surfaces,
including `.github/workflows/ci.yml`, and explicitly prune `.agents`,
`docs/reviews`, `docs/superpowers/plans`, generated evidence, and the
maintainer-boundary test. Task 8 adds its completed release scripts to this
allowlist; do not add nonexistent placeholders.

`release/package-policy-v1.json` must be closed and versioned. It owns allowed
top-level roots, required members, forbidden roots/suffixes, count/size caps,
and the one-sdist-root rule. `release-manifest-v1.schema.json` must use
`additionalProperties: false` at every object and define exactly:

```text
schemaVersion
project(name, version, commit)
sourceInventory(count, sha256)
toolchain(python, implementation, pip, build, setuptools, wheel)
platform(system, machine)
artifacts(wheel|sdist: sha256, sizeBytes, memberCount, memberInventorySha256)
reproducibility(wheelBytesMatch, sdistMembersMatch)
gates(sourceIdentity, sourcePrivacy, wheelArchive, sdistArchive, freshInstall)
nonClaims
```

No path, timestamp, hostname, username, run ID, command, duration, log, raw
matched secret, or content field is permitted.

- [ ] **Step 4: Remove existing machine-specific path debt**

Replace the three historical machine-specific absolute skill-validator
invocations in the Task 10 plan and packet with
`${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py`. Do not
rewrite any other historical evidence. Keep generic invented editor-home
security canaries only where tests require them.

- [ ] **Step 5: Run packaging tests twice**

```bash
python -m unittest tests.test_packaging -v
python -m unittest tests.test_packaging -v
```

Expected: both PASS; wheel SHA is stable across both builds within each run,
and sdist normalized inventories match.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml requirements/ci-constraints.txt MANIFEST.in release \
  tests/test_packaging.py \
  docs/reviews/task-10-closeout-packet-2026-08-17.md \
  docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
git commit -m "build: freeze public package policy"
```

---

### Task 7: Implement tracked-source privacy and archive safety gates

**Files:**

- Create: `scripts/release_gate_core.py`
- Create: `tests/test_release_gate.py`
- Modify: `release/package-policy-v1.json`
- Modify: `release/release-manifest-v1.schema.json`

- [ ] **Step 1: Write failing source-inventory/privacy tests**

Create temporary invented Git repositories and assert the core:

- reads `git ls-files -s -z` for the complete index and accepts only stage 0
  regular `100644`/`100755` entries;
- fails on tracked symlinks, submodules, special/unsupported modes, unmerged
  entries, dirty tracked bytes, and source change during the scan;
- bounds per-file size, total size, and file count before reading;
- scans all tracked bytes, including docs and tests, for private home paths,
  credential assignments, private-key headers, and forbidden binary/media
  suffixes;
- accepts only explicit low-entropy invented canaries such as `editor`,
  `example`, `fake`, `test`, `redacted`, `placeholder`, and `secret`;
- returns only codes/counts/digests and never the matching line, value, or path.

Build realistic-looking failure strings at test runtime from split fragments so
the release gate does not reject its own tracked tests.

- [ ] **Step 2: Write failing malicious-archive tests**

Generate invented ZIP and TAR fixtures in temporary directories. Assert
rejection of:

- absolute paths and `..` traversal;
- symlink/hardlink/device/FIFO members;
- duplicate and Unicode-casefold-colliding names;
- encrypted ZIP members;
- excessive compressed artifact size, member count, individual expansion, or
  aggregate expansion;
- wrong top-level roots, unexpected files, missing required files, and
  forbidden wheel/sdist surfaces;
- credential/private-path patterns inside accepted text members.

Assert member inventory digests bind normalized relative member name, type,
mode, size, and content SHA-256, while the returned result exposes no member
names.

- [ ] **Step 3: Run tests and observe RED**

```bash
python -m unittest tests.test_release_gate.SourceGateTest \
  tests.test_release_gate.ArchiveGateTest -v
```

Expected: missing release-gate core.

- [ ] **Step 4: Implement bounded pure core functions**

Define frozen `SourceInventory` and `DistributionInspection` dataclasses plus
`ReleaseGateError`, whose constructor accepts one stable `code` and whose
string form is only that code. Implement these exact public core signatures:

- `inventory_tracked_source(source: Path) -> SourceInventory`
- `inspect_wheel(path: Path, policy: Mapping[str, object]) -> DistributionInspection`
- `inspect_sdist(path: Path, policy: Mapping[str, object]) -> DistributionInspection`
- `scan_public_bytes(encoded: bytes) -> None`

Invoke Git with argv only, `shell=False`, a fixed environment allowlist, byte
capture limits, and timeouts. Do not decode or emit unsafe subprocess output.
Read working-tree files using `O_NOFOLLOW`; scan the Git status both before and
after inventory. For ZIP/TAR, validate metadata and all bounds before reading a
member body. Never call a generic archive extraction API during inspection.

- [ ] **Step 5: Run focused and source-boundary regressions**

```bash
python -m unittest tests.test_release_gate.SourceGateTest \
  tests.test_release_gate.ArchiveGateTest tests.test_maintainer_boundary -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/release_gate_core.py tests/test_release_gate.py \
  release/package-policy-v1.json release/release-manifest-v1.schema.json
git commit -m "feat: add source privacy and archive gates"
```

---

### Task 8: Orchestrate clean builds, fresh install smoke, and manifest-last publication

**Files:**

- Create: `scripts/release_gate.py`
- Modify: `scripts/release_gate_core.py`
- Modify: `tests/test_release_gate.py`
- Modify: `tests/test_packaging.py`
- Modify: `MANIFEST.in`
- Modify: `release/package-policy-v1.json`

- [ ] **Step 1: Write orchestration and publication RED tests**

Inject bounded fake command/build/install seams and assert:

- `--source` must be one clean Git toplevel at `HEAD`; version is read from
  `pyproject.toml` and must match installed package metadata;
- output must be absent, with an existing output or race winner preserved;
- two `git archive HEAD` snapshots build under the same fixed commit time and
  exact build toolchain;
- wheel bytes must match; sdist normalized member inventories must match;
- both final archives pass privacy/content/safety inspection before install;
- a new venv installs only the chosen local wheel, `pip check` passes, and
  installed `tritrack components --json`, `validate --help`, and all four mode
  helps return success;
- any source/build/inspection/install/smoke/schema failure stops publication;
- archive files are linked into the reserved output first and canonical
  `release-manifest.json` is linked last;
- injected interruption before the last link leaves no manifest and cannot be
  mistaken for success;
- a successful manifest validates against the closed schema and contains no
  path/time/run/log/content field.

- [ ] **Step 2: Run and observe RED**

```bash
python -m unittest tests.test_release_gate.OrchestrationTest \
  tests.test_release_gate.PublicationTest -v
```

Expected: missing orchestration and CLI.

- [ ] **Step 3: Implement exact build and smoke stages**

Add bounded functions with these exact public signatures:

- `build_distributions(snapshot: Path, output: Path, *, epoch: int) -> tuple[Path, Path]`
- `fresh_install_smoke(wheel: Path, temporary: Path) -> None`
- `build_release_manifest(context: ReleaseContext) -> dict[str, object]`
- `publish_release(output: Path, wheel: Path, sdist: Path, manifest: bytes) -> None`
- `run_release_gate(source: Path, output: Path) -> dict[str, object]`

Use `sys.executable -m build --no-isolation`; validate exact installed build
tool versions, including `pip==26.2`, before building. Extract only the trusted
`git archive` after verifying its members are the exact tracked source
inventory. Create a fresh venv with `sys.executable -m venv`, install the exact
pinned pip, then install the local wheel by argv, run `pip check`, and run
installed CLI smoke. The wheel is the only TriTrack source accepted by the
smoke environment; its bounded runtime dependencies may resolve from the
configured Python index. No shell, source install, editable install, or
current-worktree import is allowed in the smoke venv.

Extend `MANIFEST.in`, `release/package-policy-v1.json`, and
`tests/test_packaging.py` so the now-existing `scripts/release_gate.py`,
`scripts/release_gate_core.py`, release schema, and package policy are mandatory
sdist members. The test must stay GREEN before commit.

Canonicalize the manifest with sorted UTF-8 JSON plus one final newline and
validate it before publication. Reserve output with `os.mkdir`, hard-link the
two archives, fsync, hard-link the manifest last, then fsync again. Never
overwrite or repair an existing output.

- [ ] **Step 4: Implement the maintainer-only CLI**

`scripts/release_gate.py` must accept only:

```text
python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

On success print only `RELEASE_GATE\tPASS`, commit, version, artifact hashes,
and manifest hash. On failure print one JSON error code without exception text
or path. It must not expose any installed `tritrack` entry point.

- [ ] **Step 5: Run unit and packaging regressions**

```bash
python -m unittest tests.test_release_gate tests.test_packaging -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/release_gate.py scripts/release_gate_core.py \
  tests/test_release_gate.py tests/test_packaging.py MANIFEST.in \
  release/package-policy-v1.json
git commit -m "feat: add maintainer release gate"
```

---

### Task 9: Replace minimal CI with the fixed release-grade matrix

**Files:**

- Modify: `.github/workflows/ci.yml`
- Create: `tests/test_release_ci.py`
- Modify: `requirements/ci-constraints.txt`
- Modify: `tests/test_quickstart_demo.py`

- [ ] **Step 1: Write CI contract RED tests**

Read the workflow as public configuration and assert:

- test matrix has exactly four include cells:
  `ubuntu-24.04`/x64 × Python 3.12/3.13 and
  `macos-26`/arm64 × Python 3.12/3.13;
- every cell runs constrained editable install, full unittest discovery,
  compileall, local wheel build, new-venv wheel install, `pip check`,
  `components --json`, and all validator helps;
- quality runs once on `ubuntu-24.04`/Python 3.13 and runs Ruff over
  `src tests examples scripts` plus package/CI contract tests;
- release gate runs once on `ubuntu-24.04`/Python 3.13 into an ignored absent
  `.release-evidence/ci` directory;
- Actions use only the two exact commit SHAs at the top of this plan;
- workflow permissions are only `contents: read`;
- no `upload-artifact`, release, tag, registry, signing, attestation, SBOM,
  provider, credential, GUI, or DTD step exists;
- no moving runner label or moving `@vN` Action reference exists.

- [ ] **Step 2: Run and observe RED**

```bash
python -m unittest tests.test_release_ci -v
```

Expected: current `ubuntu-latest`, two-cell matrix, mutable Action tags, and
missing packaging/release jobs.

- [ ] **Step 3: Write the exact workflow**

Use explicit `matrix.include`, `fail-fast: false`, fixed runner labels, and the
two pinned Action SHAs with version comments. Do not enable setup-python cache.
Install the exact pip first, then the constrained project:

```bash
python -m pip install --constraint requirements/ci-constraints.txt pip
python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
```

For the per-cell wheel smoke, build with `--wheel --no-isolation` to a fresh
runner-temp directory, create a second venv, install the single local wheel,
run `pip check`, then invoke installed help. For the release job, run only the
maintainer release-gate entry point after the constrained development install.

- [ ] **Step 4: Run CI and quickstart contract tests**

```bash
python -m unittest tests.test_release_ci tests.test_quickstart_demo -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/ci.yml requirements/ci-constraints.txt \
  tests/test_release_ci.py tests/test_quickstart_demo.py
git commit -m "ci: add fixed release-grade matrix"
```

---

### Task 10: Document validator and maintainer gate without crossing roles

**Files:**

- Modify: `README.md`
- Modify: `docs/TOOLING.md`
- Modify: `CONTRIBUTING.md`
- Modify: `CHANGELOG.md`
- Modify: `SECURITY.md`
- Modify: `skills/tritrack-editing-assistant/SKILL.md`
- Modify: `tests/test_maintainer_boundary.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write documentation/role-firewall RED tests**

Assert README, tooling, and the end-user skill contain all five validator help
authorities (`validate --help` plus four modes), state each exact scope and
non-claim, and never instruct format guessing, output repair, DTD/media/GUI
checks, provider access, credentials, or release actions.

Assert only `docs/TOOLING.md` and maintainer governance document
`python scripts/release_gate.py --source . --output ABSENT_DIRECTORY`; the end-user skill
must continue to reject `release`, task numbers, branches, standing grants,
tester language, source filenames, `.py`, and maintainer identity.

Assert public Python support says exactly 3.12 and 3.13, not “or newer.”

- [ ] **Step 2: Run and observe RED**

```bash
python -m unittest tests.test_maintainer_boundary \
  tests.test_cli.ValidateDocumentationTest -v
```

Expected: validator still described as planned and release gate undocumented.

- [ ] **Step 3: Update public and maintainer documentation**

Add a concise README section with the four commands and a table of scopes:
`contract`, `structural-profile`, `authority-bound`, and
`complete-run-bundle`. State that success is evidence only within that scope.

In `docs/TOOLING.md`, record the exact maintainer gate, absent-output rule,
source/archive/fresh-install checks, wheel/sdist reproducibility distinction,
manifest fields, fixed CI matrix, and prohibited outward actions.

In the end-user skill, add help-first read-only validation after generated
artifacts, but no release language or maintainer controls. Update changelog,
contributing, and security language truthfully; keep “no public release yet.”

- [ ] **Step 4: Validate role firewalls and skills**

```bash
python -m unittest tests.test_maintainer_boundary \
  tests.test_cli.ValidateDocumentationTest -v
TASK11_SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  .agents/skills/tritrack-editing-assistant-maintainer
python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  skills/tritrack-editing-assistant
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add README.md docs/TOOLING.md CONTRIBUTING.md CHANGELOG.md SECURITY.md \
  skills/tritrack-editing-assistant/SKILL.md \
  tests/test_maintainer_boundary.py tests/test_cli.py
git commit -m "docs: publish Task 11 validation boundaries"
```

---

### Task 11: Run the complete local candidate and create final public records

**Files:**

- Create: `docs/TASK-11-VERIFICATION.md`
- Modify: `STATUS.md`
- Modify: `docs/ROADMAP.md`
- Modify: `tests/test_maintainer_boundary.py`
- Modify: `tests/test_packaging.py`
- Modify: `MANIFEST.in`
- Modify: `release/package-policy-v1.json`
- Modify if required by observed truth: `README.md`, `docs/TOOLING.md`,
  `CHANGELOG.md`

- [ ] **Step 1: Build an exact clean verification environment**

```bash
TASK11_VENV=/private/tmp/tritrack-task11-verification-venv
python3.13 -m venv "$TASK11_VENV"
"$TASK11_VENV/bin/python" -m pip install \
  --constraint requirements/ci-constraints.txt pip
"$TASK11_VENV/bin/python" -m pip install \
  --constraint requirements/ci-constraints.txt -e '.[dev]'
"$TASK11_VENV/bin/python" -m pip check
```

Expected: install and dependency check PASS with Python 3.13.

- [ ] **Step 2: Run focused, complete, quality, compile, identity, and skill gates**

```bash
"$TASK11_VENV/bin/python" -m unittest tests.test_validate_artifacts \
  tests.test_release_gate tests.test_packaging tests.test_release_ci \
  tests.test_cli -v
"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
"$TASK11_VENV/bin/ruff" check src tests examples scripts
"$TASK11_VENV/bin/python" -m compileall -q src tests examples scripts
"$TASK11_VENV/bin/python" \
  .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py \
  --root .
TASK11_SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  .agents/skills/tritrack-editing-assistant-maintainer
python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  skills/tritrack-editing-assistant
git diff --check
git status --short
```

Expected: all PASS. Record exact test counts and tool versions; do not invent a
count in advance.

- [ ] **Step 3: Freeze the clean implementation candidate before the real gate**

Read back all changed files and confirm Tasks 1–10 already committed every
owned change. Confirm no generated build, venv, cache, `.release-evidence`,
media, workbook, FCPXML, credential, or private path is tracked. Require an
empty `git status --short`, record `git rev-parse HEAD` as the implementation
candidate, and do not create a catch-all commit.

- [ ] **Step 4: Run the real release gate into one fresh ignored directory**

```bash
"$TASK11_VENV/bin/python" scripts/release_gate.py \
  --source . \
  --output .release-evidence/task11-implementation
"$TASK11_VENV/bin/python" -m json.tool \
  .release-evidence/task11-implementation/release-manifest.json
git status --short
```

Expected: gate PASS, manifest present last, worktree still clean, and no path,
time, content, or unsupported claim in the manifest. If the gate fails, keep
that directory as incomplete evidence and use a new absent suffix after the
fix; never repair or reuse it.

- [ ] **Step 5: Write public verification and advance the roadmap**

`docs/TASK-11-VERIFICATION.md` must record:

- approved design commit and implementation candidate commit;
- exact focused/full test counts, Ruff, compile, identity, skill, package,
  release-gate, and installed-wheel results;
- wheel byte reproducibility and normalized sdist-member reproducibility;
- exact tool versions, archive hashes/member-inventory digests, and manifest
  hash from the implementation gate, without a local path;
- four validator scopes and all non-claims;
- exact action pins and fixed CI cells;
- brainstorm provenance: Codex and Gemini hashes/model ledger, plus truthful
  Claude timeout/incomplete state with no retry/fallback;
- no tag, release, package publication, PR, tester contact, upload, signing,
  attestation, SBOM, Final Cut GUI, DTD, provider, or application claim.

Update `STATUS.md` to Tasks 1–11 complete and Task 12 next. Move Task 11 to the
completed roadmap section. Make `docs/TASK-11-VERIFICATION.md` an exact
required sdist member in `MANIFEST.in`, the package policy, and packaging
tests. Add maintainer-boundary tests that require the status/roadmap truths.

- [ ] **Step 6: Run documentation regression, full suite, and commit**

```bash
"$TASK11_VENV/bin/python" -m unittest tests.test_maintainer_boundary -v
"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
"$TASK11_VENV/bin/ruff" check src tests examples scripts
git diff --check
git add docs/TASK-11-VERIFICATION.md STATUS.md docs/ROADMAP.md \
  tests/test_maintainer_boundary.py tests/test_packaging.py MANIFEST.in \
  release/package-policy-v1.json README.md docs/TOOLING.md CHANGELOG.md
git commit -m "docs: close Task 11 release readiness"
```

Stage only files that actually changed.

---

### Task 12: Independent closeout review, fix-forward, final gate, and custody

**Files:**

- Create: `docs/reviews/task-11-closeout-packet-2026-08-17.md`
- Create as produced: `docs/reviews/task-11-closeout-gemini-2026-08-17.md`
- Create as produced: provider status ledgers
- Create: `docs/reviews/task-11-closeout-adjudication-2026-08-17.md`
- Modify only for agreed in-scope findings: implementation/tests/docs above

- [ ] **Step 1: Freeze a path-safe review packet**

Include the exact base/candidate SHAs, approved design, complete diff, test and
release-manifest evidence, package member policy, CI pins/matrix, privacy and
path scans, non-goals, and finding schema. Do not include ignored artifacts,
absolute local paths, credentials, or content from user artifacts.

- [ ] **Step 2: Perform Codex independent review first**

Review the frozen target for:

1. four-mode correctness and authority reuse;
2. no-write/no-network/privacy boundaries;
3. tracked source and archive safety;
4. package content and reproducibility claims;
5. manifest-last failure/race behavior;
6. fixed CI and supply-chain pins;
7. tests, docs, role firewalls, governance, and scope.

Record findings before reading external answers.

- [ ] **Step 3: Use the approved shared Claude/Gemini wrappers once each**

Read `docs/TOOLING.md`, `docs/COLLABORATION.md` from the governing shared
workspace, and the shared tool README before invocation. Resolve the highest
eligible released models dynamically under repository routing rules. Use each
model at most once. Record requested, observed, and completed IDs exactly.

Claude must use only the subscription wrapper. A timeout or ambiguous request
remains incomplete with no retry, downgrade, paid credential, API, or provider
fallback. Gemini must fail closed if the official eligible catalog cannot be
resolved.

- [ ] **Step 4: Adjudicate and fix forward**

Classify every finding as `agree`, `upgrade`, `downgrade`, `reject`, or
`already-fixed`. For every agreed ordinary in-scope defect: add an observed RED
regression, implement the smallest fix, run focused/full/quality/package gates,
update the packet and evidence, and repeat the closeout locally. Stop only for
a true public-contract gap or unauthorized scope expansion.

- [ ] **Step 5: Commit sanitized review records**

Stage the frozen packet and adjudication by exact filename. Then inspect
`git status --short` and stage only each produced human-readable review and
`.status.json` ledger by its exact filename. Never use a wildcard that could
capture raw output.

```bash
git add docs/reviews/task-11-closeout-packet-2026-08-17.md \
  docs/reviews/task-11-closeout-adjudication-2026-08-17.md
git status --short
git commit -m "docs: record Task 11 closeout review"
```

Do not stage `.raw.json`, ignored evidence, temporary packets, or credentials.

- [ ] **Step 6: Run the final clean candidate gate**

```bash
"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
"$TASK11_VENV/bin/ruff" check src tests examples scripts
"$TASK11_VENV/bin/python" -m compileall -q src tests examples scripts
git diff --check
git status --short
"$TASK11_VENV/bin/python" scripts/release_gate.py \
  --source . \
  --output .release-evidence/task11-final
git status --short
```

Expected: clean and PASS. This final release-evidence directory remains ignored
and local; no artifact upload or publication is authorized.

- [ ] **Step 7: Fast-forward main and push under the standing grant**

Verify the branch is based on the recorded `origin/main`, fast-forward local
`main` to the fully green candidate without a merge commit, and push only
`main` to the existing public `origin`. Do not create a tag, release, PR, or
package upload.

```bash
git fetch origin main
git rev-parse origin/main
git switch main
git merge --ff-only codex/task11-release-gates
git push origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
```

All three final SHAs must match exactly.

- [ ] **Step 8: Verify remote CI at the exact pushed SHA**

Use `gh run list`, `gh run view`, and `gh run watch` for the exact pushed commit.
Require all four test cells, the single quality job, and the single release-gate
job to pass. Verify again that the workflow has no artifact upload. If an
ordinary in-scope CI defect appears, fix forward on the task branch, repeat all
local gates/review delta, fast-forward, push, and reverify the exact SHA.

Record the run ID in the final handoff only; do not edit the already-green
candidate merely to embed the CI run ID.

---

## Completion definition

Task 11 is complete only when:

- all four installed validator modes are read-only, offline, strictly scoped,
  and share existing authorities;
- source/privacy/archive/package/reproducibility/fresh-install gates pass from
  one clean commit;
- `release-manifest.json` is schema-valid, path-free, and published last;
- fixed Linux x64/macOS arm64 × Python 3.12/3.13 CI passes at the exact public
  `main` SHA;
- public docs and end-user skill describe validation without maintainer power;
- no outward action beyond the existing-main fast-forward/push grant occurs;
- Task 12, not publication, is the next roadmap action.
