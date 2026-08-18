# Task 13 Generic-Authority Seam Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove from a fresh installed wheel that an out-of-tree consumer can bind a downstream-owned sidecar to exact public engine authority without imports, mutation, private knowledge, or a new runtime API.

**Architecture:** Keep the supported v1 seam at the existing `tritrack validate ... --json` process and versioned artifact boundary. Add one standard-library-only example consumer and invented aligned-transcript fixture, then make unit tests, fixed CI, packaging policy, and the maintainer release gate execute the consumer outside the source tree against an installed wheel. The example sidecar is namespaced `example.*` and is explicitly not an engine contract.

**Tech Stack:** Python 3.12／3.13 standard library, existing `unittest`, existing `tritrack` CLI and JSON contracts, setuptools sdist policy, GitHub Actions, existing release-gate framework.

---

### Task 1: Freeze the selected public seam contract

**Files:**
- Create: `docs/TASK-13-DECISION.md`
- Create: `docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md`

- [ ] **Step 1: Record the producer decision**

Write the exact Option A authority ownership, process boundary, validation-scope limits, sidecar ownership, privacy boundary, falsification rule, rejected alternatives, non-claims, and brainstorming provenance in `docs/TASK-13-DECISION.md`.

- [ ] **Step 2: Verify the plan and decision are public-safe**

Run:

```bash
git diff --check
rg -n '/''Users/|TriTrack-''Subtitle-Studio' docs/TASK-13-DECISION.md docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
```

Expected: `git diff --check` exits 0 and the privacy search returns no match.

- [ ] **Step 3: Commit the approved design**

```bash
git add docs/TASK-13-DECISION.md docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
git commit -m "docs: approve Task 13 downstream seam"
```

### Task 2: Prove a consumer can use the existing seam

**Files:**
- Create: `examples/downstream_seam.py`
- Create: `examples/downstream_fixture/aligned-transcript.json`
- Create: `tests/test_downstream_seam.py`

- [ ] **Step 1: Add the invented authority fixture**

Create canonical JSON with this complete shape:

```json
{
  "alignmentProfileId": "cue-addressed-v1",
  "language": "en",
  "revisionSha256": "2222222222222222222222222222222222222222222222222222222222222222",
  "schemaVersion": "tritrack.aligned-transcript/v1",
  "sourceBundleSha256": "1111111111111111111111111111111111111111111111111111111111111111",
  "takes": [
    {
      "cues": [
        {
          "cueId": "cue-000001",
          "disposition": "original",
          "endMs": 1250,
          "startMs": 0,
          "text": "Invented public words."
        }
      ],
      "sourceSha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "status": "completed",
      "takeId": "invented-take.wav"
    }
  ]
}
```

- [ ] **Step 2: Write failing black-box tests**

Create `tests/test_downstream_seam.py` with a real installed CLI path and subprocess assertions:

```python
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "downstream_seam.py"
FIXTURE = ROOT / "examples" / "downstream_fixture" / "aligned-transcript.json"
TRITRACK = Path(sys.executable).with_name("tritrack")

def run_consumer(*arguments: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-I",
            os.fspath(SCRIPT),
            "--tritrack",
            os.fspath(TRITRACK),
            *[os.fspath(value) for value in arguments],
        ],
        cwd=SCRIPT.parent,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
```

Tests must assert that a valid fixture creates the exact `example.tritrack-downstream-receipt/v1` sidecar; the stdout summary contains hashes/counts but no path or transcript text; an existing output is preserved; an unknown contract version is rejected; a validator-reported hash mismatch is rejected; and the script contains no `tritrack_editing_assistant` import.

- [ ] **Step 3: Run RED and preserve the expected failure**

Run:

```bash
venv/bin/python -m unittest tests.test_downstream_seam -v
```

Expected: FAIL because `examples/downstream_seam.py` does not exist. Record the command, failure reason, and failing test count in the Task 13 verification draft before implementation.

- [ ] **Step 4: Implement the minimal standard-library consumer**

Implement these production-neutral functions in `examples/downstream_seam.py`:

```python
MAX_ARTIFACT_BYTES = 16 * 1024 * 1024

def _read_regular(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= MAX_ARTIFACT_BYTES:
            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(MAX_ARTIFACT_BYTES + 1)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(encoded) > MAX_ARTIFACT_BYTES:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    return encoded

def _validate(tritrack: Path, aligned: Path) -> dict[str, object]:
    result = subprocess.run(
        [os.fspath(tritrack), "validate", "contract", "--artifact", os.fspath(aligned), "--json"],
        check=False,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0 or result.stderr:
        raise DownstreamError("DOWNSTREAM_ENGINE_VALIDATION_FAILED")
    summary = json.loads(result.stdout.decode("utf-8", errors="strict"))
    if (
        summary.get("schemaVersion") != "tritrack.validate-summary/v1"
        or summary.get("artifactKind") != "contract"
        or summary.get("validationScope") != "contract"
        or summary.get("details") != {
            "contractName": "aligned-transcript-v1",
            "contractSchemaVersion": "tritrack.aligned-transcript/v1",
        }
    ):
        raise DownstreamError("DOWNSTREAM_ENGINE_SCOPE_INVALID")
    return summary
```

The main path validates, reads and hashes the exact fixture, checks the reported hash, derives only take/cue counts, validates again and requires identical summary facts, then atomically creates canonical JSON at an absent output. It prints only:

```json
{
  "artifactSha256": "<exact hash>",
  "cueCount": 1,
  "schemaVersion": "example.tritrack-downstream-summary/v1",
  "takeCount": 1
}
```

- [ ] **Step 5: Run GREEN**

```bash
venv/bin/python -m unittest tests.test_downstream_seam -v
```

Expected: all downstream seam tests pass with no warnings or traceback.

- [ ] **Step 6: Commit the working reference consumer**

```bash
git add examples/downstream_seam.py examples/downstream_fixture/aligned-transcript.json tests/test_downstream_seam.py
git commit -m "test: prove the public downstream seam"
```

### Task 3: Make the fresh-wheel gate own the proof

**Files:**
- Modify: `scripts/release_gate_core.py`
- Modify: `tests/test_release_gate.py`
- Modify: `release/release-manifest-v1.schema.json`
- Modify: `tests/test_packaging.py`

- [ ] **Step 1: Write failing release-gate tests**

Extend `test_fresh_install_uses_only_local_wheel_and_smokes_all_help` with a minimal public source tree containing the example script and fixture. Require `fresh_install_smoke(wheel, smoke, source)` to copy the two files out of the source tree, invoke isolated installed Python with the installed `tritrack`, and verify the created receipt. Extend the manifest sample and schema assertions to require:

```json
"gates": {
  "downstreamSeam": "pass",
  "freshInstall": "pass",
  "sdistArchive": "pass",
  "sourceIdentity": "pass",
  "sourcePrivacy": "pass",
  "wheelArchive": "pass"
}
```

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_release_gate tests.test_packaging -v
```

Expected: FAIL because `fresh_install_smoke` has no source argument or downstream probe and the release manifest does not allow `downstreamSeam`.

- [ ] **Step 3: Implement the minimal gate integration**

Change the function signature and call site:

```python
def fresh_install_smoke(wheel: Path, temporary: Path, source: Path) -> None:
    ...

fresh_install_smoke(wheel_one, staging / "fresh-install", snapshot_one)
```

After installed CLI help smoke, copy `examples/downstream_seam.py` and
`examples/downstream_fixture/aligned-transcript.json` into
`temporary/downstream-seam/`, run the copied consumer under installed
`python -I` against installed `tritrack`, and read back the exact receipt. Fail
with `TRITRACK_RELEASE_DOWNSTREAM_SEAM` unless its schema, contract, scope,
artifact hash, take count, and cue count match the invented fixture.

Add `downstreamSeam: pass` to `build_release_manifest` and its closed schema.

- [ ] **Step 4: Run GREEN**

```bash
venv/bin/python -m unittest tests.test_release_gate tests.test_packaging tests.test_downstream_seam -v
```

Expected: all focused release and seam tests pass.

- [ ] **Step 5: Commit the named release gate**

```bash
git add scripts/release_gate_core.py tests/test_release_gate.py release/release-manifest-v1.schema.json tests/test_packaging.py
git commit -m "feat: gate the wheel-only downstream seam"
```

### Task 4: Distribute and exercise only the public proof

**Files:**
- Modify: `MANIFEST.in`
- Modify: `release/package-policy-v1.json`
- Modify: `.github/workflows/ci.yml`
- Modify: `tests/test_release_ci.py`

- [ ] **Step 1: Write failing packaging and CI policy tests**

Require the sdist policy to contain the Task 13 decision, example consumer,
invented aligned fixture, Task 13 verification, and downstream seam test while
the wheel member set remains unchanged. Require the fixed CI wheel-smoke block
to copy the example and fixture into `$RUNNER_TEMP` and run the consumer with
the fresh wheel's Python and CLI.

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_packaging tests.test_release_ci -v
```

Expected: FAIL because the new public proof members and CI invocation are not
yet declared.

- [ ] **Step 3: Add exact distribution and CI wiring**

Add to `MANIFEST.in`:

```text
include docs/TASK-13-DECISION.md
include docs/TASK-13-VERIFICATION.md
recursive-include examples *.py *.json
```

Add the exact new members to `release/package-policy-v1.json`. Extend the
existing CI wheel-smoke shell block with one absent `$RUNNER_TEMP` directory,
copy the consumer and fixture there, and invoke:

```bash
"$smoke_python" -I "$seam_dir/downstream_seam.py" \
  --tritrack "$smoke_cli" \
  --aligned "$seam_dir/aligned-transcript.json" \
  --output "$seam_dir/downstream-receipt.json"
```

- [ ] **Step 4: Run GREEN**

```bash
venv/bin/python -m unittest tests.test_packaging tests.test_release_ci tests.test_downstream_seam -v
```

Expected: all packaging, CI, and seam tests pass and the eleven-component
registry assertion remains unchanged.

- [ ] **Step 5: Commit packaging and CI proof**

```bash
git add MANIFEST.in release/package-policy-v1.json .github/workflows/ci.yml tests/test_release_ci.py
git commit -m "build: exercise the downstream seam in fresh wheels"
```

### Task 5: Close public documentation and local verification

**Files:**
- Modify: `README.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/TOOLING.md`
- Modify: `STATUS.md`
- Create: `docs/TASK-13-VERIFICATION.md`
- Modify: `tests/test_maintainer_boundary.py`

- [ ] **Step 1: Write the failing governance regression**

Require Task 13 completion language, the exact Option A seam, internal-Python
non-contract language, sidecar non-authority, wheel-only proof, named
`downstreamSeam` gate, and explicit non-claims across the decision,
verification, README, roadmap, tooling, and status.

- [ ] **Step 2: Run RED**

```bash
venv/bin/python -m unittest tests.test_maintainer_boundary -v
```

Expected: FAIL because Task 13 has not yet been recorded complete and the
verification file does not exist.

- [ ] **Step 3: Write public documentation after coherent code is green**

Document exact seam commands and limits, invented proof, RED／GREEN evidence,
package facts, external review provenance, non-claims, and current Task 13
candidate. Do not claim a private integration, release, tag, package upload,
or compatibility outside the exact tested boundary.

- [ ] **Step 4: Run complete local validation**

```bash
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples scripts
venv/bin/python -m compileall -q src tests examples scripts
venv/bin/python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
git diff --check
```

Expected: full suite, lint, compilation, identity, and diff checks pass.

- [ ] **Step 5: Commit the green implementation target**

```bash
git add README.md docs/ROADMAP.md docs/TOOLING.md STATUS.md docs/TASK-13-VERIFICATION.md tests/test_maintainer_boundary.py
git commit -m "docs: complete Task 13 public authority proof"
```

### Task 6: Review, fix forward, integrate, and verify exact CI

**Files:**
- Create: `docs/reviews/task-13-closeout-packet-2026-08-18.md`
- Create: `docs/reviews/task-13-closeout-codex-2026-08-18.md`
- Create: `docs/reviews/task-13-closeout-gemini-2026-08-18.md`
- Create: `docs/reviews/task-13-closeout-gemini-2026-08-18.md.status.json`
- Create on completed Claude lane or status-only on failure: `docs/reviews/task-13-closeout-claude-2026-08-18.md*`
- Create: `docs/reviews/task-13-closeout-adjudication-2026-08-18.md`
- Modify if required by reproduced findings: only Task 13-owned source, tests, and docs

- [ ] **Step 1: Run the clean maintainer release gate**

Commit the implementation, require a clean worktree, create one absent output
directory, and run:

```bash
venv/bin/python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

Expected: both package builds match their declared reproducibility contract,
fresh wheel installation passes, the copied out-of-tree consumer passes, and
the manifest records `downstreamSeam: pass`.

- [ ] **Step 2: Freeze one same-byte closeout packet**

Include exact candidate SHA, complete Task 13 diff, every changed runtime／gate
file, focused and full results, release manifest, non-goals, and requested
file-and-line finding format. Hash and scan the packet before dispatch.

- [ ] **Step 3: Complete independent Codex review before external results**

Read the frozen packet and source, record only reproducible findings, and save
the independent response before reading Claude or Gemini output.

- [ ] **Step 4: Dispatch the same bytes once per external lane**

```bash
review-with-claude PACKET CLAUDE_OUTPUT REPO
review-with-gemini PACKET GEMINI_OUTPUT -
```

Expected: each lane records requested／observed／completed model provenance.
Timeout, quota, or unavailable lanes remain incomplete with no retry, downgrade,
provider substitution, or paid fallback.

- [ ] **Step 5: Adjudicate and fix forward with TDD**

Classify every finding as `agree`, `upgrade`, `downgrade`, `reject`, or
`already-fixed`. For each accepted behavior defect, add a failing regression,
observe RED, make the minimal fix, and rerun focused plus complete verification.

- [ ] **Step 6: Final clean gate and evidence commit**

Rerun full tests, Ruff, compilation, identity, both skill validators,
maintainer boundary, package policy, public-content scan, `git diff --check`,
and the clean release gate. Commit review and final verification records only
after the candidate is green.

- [ ] **Step 7: Fast-forward, push, and verify exact SHA**

Fast-forward local `main` to the reviewed Task 13 candidate, push the existing
public `origin/main`, and require local `HEAD`, local `main`, `origin/main`, and
remote `refs/heads/main` to match exactly. Then watch the fixed six-job GitHub
Actions run for that exact SHA and report its run ID and conclusion without
writing the run ID back into a self-referential commit.
