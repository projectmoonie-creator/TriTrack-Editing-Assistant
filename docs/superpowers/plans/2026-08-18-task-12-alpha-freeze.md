# Task 12 Alpha Freeze Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Freeze one exact public alpha review target, independently assess its
cross-task composition, preserve truthful provider evidence, and publish a
package-neutral evidence record without creating a release.

**Architecture:** Use the producer-approved two-layer Git design. A clean
`alphaReviewTarget` contains every package-relevant byte and is the exact
external review target; a later `alphaEvidenceRecord` contains only files
excluded from wheel and sdist. Existing Git, review wrappers, package policy,
release gate, and six-job CI remain the only authorities.

**Tech Stack:** Git, Python 3.13, `unittest`, Ruff, `compileall`, setuptools／
build, the existing release gate, the shared Gemini REST and Claude
subscription review wrappers, GitHub Actions, Markdown, and JSON ledgers.

---

## File map

- Create
  `docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md`:
  producer-approved freeze and review contract.
- Create `docs/superpowers/plans/2026-08-18-task-12-alpha-freeze.md`:
  executable plan and exact verification sequence.
- Modify `docs/ROADMAP.md`: make the Task 12 → Task 13 sequence status-neutral
  before the review target is frozen.
- Create `docs/reviews/task-12-alpha-review-packet-2026-08-18.md`: exact public
  packet sent to each convergent reviewer.
- Create `docs/reviews/task-12-alpha-codex-2026-08-18.md`: Codex findings fixed
  before external answers are read.
- Create as produced
  `docs/reviews/task-12-alpha-gemini-2026-08-18.md` and its `.status.json`:
  public-safe Gemini result and provenance.
- Create as produced
  `docs/reviews/task-12-alpha-claude-2026-08-18.md` and／or its `.status.json`:
  public-safe Claude result or truthful incomplete ledger.
- Create `docs/reviews/task-12-alpha-adjudication-2026-08-18.md`: every finding,
  classification, fix, and package-neutrality result.
- Create `docs/TASK-12-VERIFICATION.md`: final freeze, review, local gate,
  custody, and non-claim evidence.
- Modify `tests/test_maintainer_boundary.py`: require Tasks 1–12 complete and
  Task 13 next only in the evidence epilogue.
- Modify `STATUS.md`: record Task 12 completion only after all local gates and
  review adjudication are green.
- Create only under ignored `.release-evidence/task12-*`: raw provider
  envelopes, transient local packets, release artifacts, and comparison data.
- Create only under `/private/tmp`: one-off packet-building support. Never stage
  it or add it to package policy.

## Task 1: Commit the approved design and freeze all packaged documentation

**Files:**

- Create:
  `docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md`
- Create: `docs/superpowers/plans/2026-08-18-task-12-alpha-freeze.md`
- Modify: `docs/ROADMAP.md`

- [ ] **Step 1: Read back the selected design and confirm Option A**

Run:

```bash
sed -n '1,360p' docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md
```

Expected: the file says `Selected option: A`, names
`alphaReviewTarget`／`alphaEvidenceRecord`, requires package neutrality, and
forbids tags and releases.

- [ ] **Step 2: Make the roadmap sequence status-neutral**

Replace the current `## Next` block with:

```markdown
## Alpha-candidate sequence

- Task 12 freezes and independently reviews the alpha candidate. `STATUS.md`
  alone records whether this gate is pending or complete.
- Task 13 proves the public engine as the generic authority and defines a
  deliberate downstream integration seam after Task 12 is complete.
```

Do not mark Task 12 complete in `STATUS.md` yet.

- [ ] **Step 3: Create the fresh Task 12 verification environment**

Run:

```bash
python3.13 -m venv /private/tmp/tritrack-task12-verification-venv
/private/tmp/tritrack-task12-verification-venv/bin/python -m pip install \
  --constraint requirements/ci-constraints.txt pip setuptools
/private/tmp/tritrack-task12-verification-venv/bin/python -m pip install \
  --constraint requirements/ci-constraints.txt -e '.[dev]'
/private/tmp/tritrack-task12-verification-venv/bin/python -m pip check
```

Expected: the exact constrained toolchain installs and `pip check` reports no
broken requirement.

- [ ] **Step 4: Verify the current governance test remains green**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m unittest tests.test_maintainer_boundary -v
git diff --check
```

Expected: the existing Task 11／Task 12 ordering test passes and the diff has no
whitespace error.

- [ ] **Step 5: Verify intended Task 12 records are excluded from packages**

Run:

```bash
rg -n 'docs/reviews|TASK-12|STATUS|test_maintainer_boundary|docs/superpowers/plans' \
  MANIFEST.in release/package-policy-v1.json tests/test_packaging.py
```

Expected: `docs/reviews` and plan files are pruned,
`tests/test_maintainer_boundary.py` is excluded, and neither `STATUS.md` nor
`docs/TASK-12-VERIFICATION.md` is an expected sdist member.

- [ ] **Step 6: Commit only the design package**

Run:

```bash
git add docs/ROADMAP.md \
  docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md \
  docs/superpowers/plans/2026-08-18-task-12-alpha-freeze.md
git diff --cached --check
git status --short
git commit -m "docs: define Task 12 alpha freeze"
```

Expected: exactly those three files are committed.

## Task 2: Establish the clean `alphaReviewTarget`

**Files:**

- No tracked file changes.
- Create ignored output:
  `.release-evidence/task12-review-target/`

- [ ] **Step 1: Verify the fresh exact Python environment**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python --version
/private/tmp/tritrack-task12-verification-venv/bin/python -m pip --version
/private/tmp/tritrack-task12-verification-venv/bin/ruff --version
/private/tmp/tritrack-task12-verification-venv/bin/python -m pip check
```

Expected: CPython 3.13, the constrained pip／Ruff toolchain, and no broken
requirement.

- [ ] **Step 2: Run complete local verification**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m unittest discover -s tests -v
/private/tmp/tritrack-task12-verification-venv/bin/ruff \
  check src tests examples scripts
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m compileall -q src tests examples scripts
/private/tmp/tritrack-task12-verification-venv/bin/python \
  .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py \
  --root .
TASK12_SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
python3 "$TASK12_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  .agents/skills/tritrack-editing-assistant-maintainer
python3 "$TASK12_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
  skills/tritrack-editing-assistant
git diff --check
git status --short
```

Expected: every command passes and Git status is empty.

- [ ] **Step 3: Run the existing release gate once**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  scripts/release_gate.py \
  --source . \
  --output .release-evidence/task12-review-target
/private/tmp/tritrack-task12-verification-venv/bin/python -m json.tool \
  .release-evidence/task12-review-target/release-manifest.json
```

Expected: `RELEASE_GATE PASS`; the canonical manifest names the exact current
commit and records exact wheel and sdist facts.

- [ ] **Step 4: Record the immutable target facts outside Git**

Run:

```bash
git rev-parse HEAD
git rev-parse HEAD:src
shasum -a 256 \
  .release-evidence/task12-review-target/release-manifest.json
git status --short
```

Expected: Git status remains empty. The full commit becomes
`alphaReviewTarget`; the `src` tree and manifest digests are retained for the
later comparison.

## Task 3: Build the bounded frozen review packet

**Files:**

- Create ignored:
  `.release-evidence/task12-alpha-review-packet-2026-08-18.md`
- Later create exact public copy:
  `docs/reviews/task-12-alpha-review-packet-2026-08-18.md`

- [ ] **Step 1: Assemble one target-bound public packet**

Create the packet with these exact sections:

```text
# Task 12 public alpha independent review packet
## Review target and packet provenance
## Objective
## Current alpha surface
## Authority and privacy invariants
## Package and release-gate facts
## Fixed CI contract
## Prior review state
## Exact selected current files
## Requested review dimensions
## Finding schema
## Explicit no-edit and non-goal boundary
```

Include complete current bytes of these target files using `git show
<alphaReviewTarget>:<path>` with fenced file markers:

```text
.tritrack-project.json
AGENTS.md
README.md
STATUS.md
docs/ROADMAP.md
docs/TOOLING.md
pyproject.toml
MANIFEST.in
release/package-policy-v1.json
release/release-manifest-v1.schema.json
.github/workflows/ci.yml
.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
skills/tritrack-editing-assistant/SKILL.md
src/tritrack_editing_assistant/cli.py
src/tritrack_editing_assistant/contracts.py
src/tritrack_editing_assistant/process.py
src/tritrack_editing_assistant/align_text.py
src/tritrack_editing_assistant/gemini_hybrid.py
src/tritrack_editing_assistant/hallucination.py
src/tritrack_editing_assistant/organizer.py
src/tritrack_editing_assistant/paper_edit.py
src/tritrack_editing_assistant/run_workflow.py
src/tritrack_editing_assistant/story_fcpxml.py
src/tritrack_editing_assistant/string_out.py
src/tritrack_editing_assistant/sync_scan.py
src/tritrack_editing_assistant/transcribe_takes.py
src/tritrack_editing_assistant/validate_artifacts.py
scripts/release_gate.py
scripts/release_gate_core.py
tests/test_maintainer_boundary.py
tests/test_packaging.py
tests/test_release_ci.py
tests/test_release_gate.py
tests/test_run_workflow.py
tests/test_validate_artifacts.py
```

Also include the exact review-target release manifest and a sorted
`git ls-tree -r --full-tree` inventory. Do not include ignored artifacts other
than the sanitized release manifest facts.

- [ ] **Step 2: Scan and freeze the packet**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  scripts/release_gate.py \
  --source . \
  --output .release-evidence/task12-packet-preflight
shasum -a 256 \
  .release-evidence/task12-alpha-review-packet-2026-08-18.md
/private/tmp/tritrack-task12-verification-venv/bin/python -c \
  "from pathlib import Path; from scripts.release_gate_core import scan_public_bytes; scan_public_bytes(Path('.release-evidence/task12-alpha-review-packet-2026-08-18.md').read_bytes()); print('PUBLIC_SCAN PASS')"
```

Expected: the gate passes, the packet has one recorded SHA-256, and the
canonical private-path／credential scan passes without returning matched data.

## Task 4: Complete Codex review before external answers

**Files:**

- Create ignored first:
  `.release-evidence/task12-alpha-codex-2026-08-18.md`
- Later create exact public copy:
  `docs/reviews/task-12-alpha-codex-2026-08-18.md`

- [ ] **Step 1: Inspect the exact target, not the branch tip**

Review the target commit across the ten dimensions in the approved design.
Every finding must contain:

```text
id
severity: blocker | major | minor | note
confidence: high | medium | low
current file and line
impact
smallest safe fix
test or reproduction
```

No finding may rely on remembered private context or ignored output.

- [ ] **Step 2: Freeze Codex's answer before provider dispatch**

Run:

```bash
shasum -a 256 .release-evidence/task12-alpha-codex-2026-08-18.md
```

Expected: a stable response hash exists before either external output is read.

## Task 5: Run one Gemini and one Claude review attempt

**Files:**

- Create ignored as produced:
  `.release-evidence/task12-alpha-gemini-2026-08-18.md*`
- Create ignored as produced:
  `.release-evidence/task12-alpha-claude-2026-08-18.md*`

- [ ] **Step 1: Dispatch the exact packet once to Gemini**

Run:

```bash
review-with-gemini \
  .release-evidence/task12-alpha-review-packet-2026-08-18.md \
  .release-evidence/task12-alpha-gemini-2026-08-18.md \
  -
```

Expected: completed result with requested／observed／completed model IDs, or one
truthful incomplete ledger. Do not retry a quota or ambiguous failure.

- [ ] **Step 2: Dispatch the exact packet once to Claude**

Run:

```bash
review-with-claude \
  .release-evidence/task12-alpha-review-packet-2026-08-18.md \
  .release-evidence/task12-alpha-claude-2026-08-18.md \
  .
```

Expected: completed subscription-only result with exact provenance, or one
truthful incomplete ledger. No retry, API key, PAYG, extra usage, direct print
mode, downgrade, or provider substitution.

- [ ] **Step 3: Preserve hashes and attempt facts**

Run `shasum -a 256` separately for every produced human response and
`.status.json` ledger. Never hash or print a credential file.

## Task 6: Adjudicate every finding and fix forward

**Files:**

- Create:
  `docs/reviews/task-12-alpha-adjudication-2026-08-18.md`
- Modify only if an agreed finding requires it: exact source, test, or public
  documentation named by that finding.

- [ ] **Step 1: Build the classification table**

For every Codex, Gemini, and Claude item, record exactly one of:

```text
agree | upgrade | downgrade | reject | already-fixed
```

Require current file-and-line or reproducible behavior for a blocker.

- [ ] **Step 2: For each agreed behavior defect, run RED first**

Add one narrow regression in the owning existing test module. Run only that
test and record the exact failure before changing implementation.

- [ ] **Step 3: Implement the smallest fix and run focused GREEN**

Change no unrelated authority. Run the new regression plus the nearest
existing sibling tests until green.

- [ ] **Step 4: Determine target supersession honestly**

Run:

```bash
git diff --name-only <alphaReviewTarget>
```

If any changed path is a wheel／sdist member or runtime source, commit the
fix-forward package, rerun Task 2's complete gates, record a new exact
candidate, and perform an explicit Codex delta review. Preserve external
provider results as reviews of their original exact target; never claim they
reviewed later bytes.

## Task 7: Create the package-neutral evidence epilogue

**Files:**

- Create all public-safe `docs/reviews/task-12-alpha-*` records.
- Create `docs/TASK-12-VERIFICATION.md`.
- Modify `tests/test_maintainer_boundary.py`.
- Modify `STATUS.md`.

- [ ] **Step 1: Copy only public-safe provider evidence**

Preserve the exact frozen packet and Codex response. For each provider, copy
the human-readable result and `.status.json` ledger only. Do not stage raw JSON
envelopes, ignored archives, temporary prompts, logs, or credentials. If a
public copy is sanitized, disclose the transformation and both hashes.

- [ ] **Step 2: Write the failing Task 12 completion boundary**

Rename the current status test to
`test_public_status_records_task_12_and_schedules_task_13` and change its
current-gate assertions to:

```python
self.assertIn("Tasks 1–12", status)
self.assertIn("Task 12", status)
self.assertIn("Task 13", status)
self.assertLess(status.index("Task 12"), status.index("Task 13"))
self.assertIn("Task 12", roadmap)
self.assertIn("Task 13", roadmap)
self.assertIn("alphaReviewTarget", task_12_verification)
self.assertIn("alphaEvidenceRecord", task_12_verification)
```

Load `docs/TASK-12-VERIFICATION.md` in the test. Keep the existing Tasks 6.5–11
ordering and four validator-scope assertions.

- [ ] **Step 3: Run the status regression and observe RED**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m unittest tests.test_maintainer_boundary -v
```

Expected: FAIL because `STATUS.md` still says Tasks 1–11 and Task 12 next.

- [ ] **Step 4: Write Task 12 verification and update status**

`docs/TASK-12-VERIFICATION.md` must record:

- exact `alphaReviewTarget` and review packet hash;
- Codex／Gemini／Claude attempt provenance and truthful incomplete lanes;
- adjudication and fix-forward commits;
- review-target release-manifest and artifact facts;
- `alphaEvidenceRecord` role;
- complete local verification;
- wheel／sdist package-neutrality comparison;
- remote and CI checks that will be reported in the handoff; and
- every explicit non-claim.

Update `STATUS.md` to Tasks 1–12 complete and Task 13 next. Do not modify the
already reviewed package-member roadmap, README, changelog, tooling, policy,
runtime source, or CI merely to record completion.

- [ ] **Step 5: Run GREEN and the complete suite**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m unittest tests.test_maintainer_boundary -v
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m unittest discover -s tests -v
/private/tmp/tritrack-task12-verification-venv/bin/ruff \
  check src tests examples scripts
/private/tmp/tritrack-task12-verification-venv/bin/python \
  -m compileall -q src tests examples scripts
git diff --check
```

Expected: all pass.

- [ ] **Step 6: Verify the evidence-only allowlist and commit**

Run:

```bash
git diff --name-only <alphaReviewTarget>
git status --short
```

Expected: only `docs/reviews/task-12-*`, `docs/TASK-12-VERIFICATION.md`,
`STATUS.md`, and `tests/test_maintainer_boundary.py`, unless an explicitly
recorded fix-forward superseded the target.

Stage every file by exact name, inspect the staged diff, and commit:

```bash
git commit -m "docs: record Task 12 alpha freeze"
```

The resulting SHA is `alphaEvidenceRecord`.

## Task 8: Prove package neutrality and run the final clean gate

**Files:**

- Create ignored:
  `.release-evidence/task12-evidence-record/`

- [ ] **Step 1: Run the release gate on the clean evidence record**

Run:

```bash
/private/tmp/tritrack-task12-verification-venv/bin/python \
  scripts/release_gate.py \
  --source . \
  --output .release-evidence/task12-evidence-record
```

Expected: `RELEASE_GATE PASS` and clean Git status.

- [ ] **Step 2: Compare exact package facts**

Compare the JSON fields from the two canonical manifests. Require:

```text
artifacts.wheel.sha256                         equal
artifacts.wheel.memberInventorySha256          equal
artifacts.sdist.memberInventorySha256          equal
artifacts.sdist.memberCount                    equal
```

Require `git rev-parse <alphaReviewTarget>:src` and
`git rev-parse <alphaEvidenceRecord>:src` to be equal. Permit project commit,
tracked-source count／digest, compressed sdist SHA-256, and manifest SHA-256 to
differ only as documented.

- [ ] **Step 3: Repeat final non-package gates**

Run the complete suite, Ruff, compilation, identity, both skill validators,
`git diff --check`, and `git status --short` once more. Expected: all pass and
clean.

## Task 9: Fast-forward public custody and verify exact-SHA CI

**Files:**

- No tracked changes.

- [ ] **Step 1: Refresh and validate the existing remote**

Run:

```bash
git fetch origin main
git rev-parse origin/main
git merge-base --is-ancestor origin/main codex/task12-alpha-freeze
```

Expected: remote `main` is the recorded base and is an ancestor of the green
Task 12 branch.

- [ ] **Step 2: Fast-forward and push under the standing grant**

Run:

```bash
git switch main
git merge --ff-only codex/task12-alpha-freeze
git push origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
```

Expected: all three final SHAs equal `alphaEvidenceRecord`. No tag, release,
PR, package upload, or force-push occurs.

- [ ] **Step 3: Require all six exact-SHA jobs**

Use:

```bash
gh run list --repo projectmoonie-creator/TriTrack-Editing-Assistant \
  --commit <alphaEvidenceRecord> --limit 10
gh run view <run-id> \
  --repo projectmoonie-creator/TriTrack-Editing-Assistant \
  --json status,conclusion,headSha,url,jobs
gh run watch <run-id> \
  --repo projectmoonie-creator/TriTrack-Editing-Assistant --exit-status
```

Expected: exact head SHA and success for:

```text
ubuntu-24.04 / Python 3.12
ubuntu-24.04 / Python 3.13
macos-26 / Python 3.12
macos-26 / Python 3.13
Public quality and policy contracts
Local candidate gate without publication
```

Record the run ID in the final handoff only.

## Final self-review checklist

- [ ] Every Task 12 design requirement maps to a task above.
- [ ] No unfinished marker, generic implementation instruction, or unspecified
  test remains.
- [ ] `alphaReviewTarget` and `alphaEvidenceRecord` retain distinct meanings in
  every file.
- [ ] The review packet and external calls target exact commits, not `main`.
- [ ] Provider failures remain incomplete; no substitution or retry is hidden.
- [ ] Any accepted runtime／package change supersedes the old target.
- [ ] Evidence-only files are proven absent from wheel and normalized sdist.
- [ ] Release-manifest differences are not misreported as package differences.
- [ ] Final CI run ID is not written back into the candidate.
- [ ] Task 13 and every outward release action remain outside scope.
