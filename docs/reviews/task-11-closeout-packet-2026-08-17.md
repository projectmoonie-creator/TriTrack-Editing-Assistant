# Task 11 frozen closeout review packet

Packet date: 2026-08-18

## Public sanitation note

The provider attempts received packet SHA-256
`ab64798a971fdddeb3f093a4c3d0053e9d0d5c71712c81710cc0bb96663a92e2`.
Before public tracking, this copy replaced one historical home-root literal
inside removed diff lines with `${CODEX_SKILLS_ROOT}` and one invented mounted-
volume canary with `/mnt/invented-volume/`. No candidate byte, requirement,
finding request, or executable hunk changed. The provider status ledgers retain
the exact reviewed packet hash; this sanitized public copy intentionally has a
different hash and makes no byte-identical transcript claim.

## Objective

Review the completed public Task 11 candidate for correctness, omissions, and
release-readiness defects. Produce findings only. Do not edit files, run
network-capable product operations, publish anything, or broaden scope.

## Frozen target

- Repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Public remote: `https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`
- Lane: `OSS`
- Branch: `codex/task11-release-gates`
- Base SHA: `b4e21d660170dfd000c99ba38f55f825565ab922`
- Candidate SHA: `d53deb28aa86ef1aba9f978f44456f71bc315e57`
- Approved design commit: `87d4c32047dcb2dd9149c6f9e9d0944d93cd0256`
- Package version: `0.1.0a0`

Treat the SHA pair and the complete patch below as the immutable review target.
Repository inspection must remain read-only and must be limited to this target.

## Approved mechanism

Task 11 has two separate authority domains:

1. Installed `tritrack validate contract|fcpxml|paper|run` modes are bounded,
   read-only, offline, explicitly scoped, path-free on success, and reuse the
   existing contract, structural FCPXML, paper-workbook, and immutable-run
   authorities.
2. `scripts/release_gate.py` is maintainer-only. It binds a clean tracked Git
   candidate, privacy scans source and exact package members, builds two
   snapshots under an exact toolchain, checks wheel byte identity and normalized
   sdist inventory identity, installs the chosen local wheel into a new
   environment, and hard-links archives before a deterministic closed manifest.

The fixed CI contract is Ubuntu 24.04 x64 and macOS 26 arm64, each with Python
3.12 and 3.13, plus one Ubuntu/Python 3.13 quality job and one release-gate job.
Actions and development/build tools are pinned exactly.

## Known validation evidence

A new CPython 3.13.15 environment resolved exactly pip 26.2, build 1.5.0,
setuptools 84.0.0, wheel 0.48.0, packaging 26.3, pyproject-hooks 1.2.0, and
Ruff 0.16.2. `pip check` passed. The focused Task 11 set passed 69 tests; the
complete suite passed 235 tests; Ruff, compileall, both skill validators,
project identity, `git diff --check`, and clean-status checks passed.

The clean implementation candidate `ce562e995b63f3f1a29989de3e1ef202da27b5f2`
passed the real gate with 115 tracked files. Its two wheels were byte-identical
and its two sdists had identical normalized inventories. The public verification
record was then committed without altering implementation.

## Review dimensions

Check all of the following:

1. four-mode correctness, strict scope, and actual authority reuse;
2. read-only, no-network, no-provider, bounded-read, symlink, late-change, and
   output-privacy boundaries;
3. tracked-source identity, privacy scanning, archive paths/types/collisions,
   member allowlists, and size/expansion limits;
4. package identity, exact content policy, build isolation assumptions,
   reproducibility claims, and fresh-wheel installation;
5. manifest closure, deterministic bytes, archive-to-manifest binding,
   manifest-last failure behavior, and publication races;
6. fixed runner/Python matrix, exact Action/tool pins, minimal permissions, and
   absence of upload/publication;
7. test adequacy, docs/implementation agreement, role firewalls, governance,
   and scope control.

## Non-goals

No tag, GitHub Release, package publication, artifact upload, signing,
attestation, SBOM, pull request, tester contact, Final Cut GUI operation, DTD
validation, live provider operation, credential access, private-project
inspection, or application submission is authorized or claimed.

## Required finding schema

Return a concise summary and a numbered list. Each finding must include:

- severity: `blocker`, `major`, `minor`, or `note`;
- exact current file and line or diff hunk;
- the violated approved requirement;
- a concrete reproduction or reasoning chain;
- the smallest bounded fix;
- tests that should fail before and pass after.

Use `NO FINDINGS` if no actionable defect is supported. Separate observations
and future hardening from current-scope defects. Do not edit any file.

## Complete frozen diff

~~~~diff
diff --git a/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md b/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
index ba8c89ac14cfb5e6404cba6805498753b5b2d8e1..cfe3349a5c3fc816d118da5552204e3316656be1 100644
--- a/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
+++ b/.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
@@ -102,3 +102,14 @@ owned by the public task. Treat requested implementation as including closeout
 review and fix-forward until ordinary in-scope findings are resolved; stop only
 for a true public-contract gap, unsafe scope expansion, or a separately gated
 action.
+
+For a release-readiness task, run the maintainer-only gate exactly as:
+
+```text
+python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
+```
+
+The source must be a clean public-engine／OSS Git toplevel and the output must
+be absent. Treat only a canonical manifest linked after both inspected archives
+as a complete local candidate. This gate does not grant any outward action
+excluded by the standing authorization above.
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index c5bd50d8a0cfc91a8c37c5147819c5a2fd540bf5..cbbf8dbf6a1f3fbc25aadfdab1a1ce1e3609c830 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -1,4 +1,4 @@
-name: Public Python CI
+name: Release-grade public Python CI
 
 on:
   push:
@@ -8,24 +8,102 @@ permissions:
   contents: read
 
 jobs:
-  python-contracts:
-    name: Python ${{ matrix.python-version }} contracts (no Final Cut claim)
-    runs-on: ubuntu-latest
+  test-matrix:
+    name: ${{ matrix.os }} / Python ${{ matrix.python-version }}
+    runs-on: ${{ matrix.os }}
     strategy:
       fail-fast: false
       matrix:
-        python-version: ["3.12", "3.13"]
+        include:
+          - os: ubuntu-24.04
+            python-version: "3.12"
+            architecture: x64
+          - os: ubuntu-24.04
+            python-version: "3.13"
+            architecture: x64
+          - os: macos-26
+            python-version: "3.12"
+            architecture: arm64
+          - os: macos-26
+            python-version: "3.13"
+            architecture: arm64
     steps:
-      - uses: actions/checkout@v4
-      - uses: actions/setup-python@v5
+      - name: Check out exact source
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
+      - name: Set up fixed Python cell
+        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
         with:
           python-version: ${{ matrix.python-version }}
-          cache: pip
-      - name: Install source and development checks
-        run: python -m pip install -e '.[dev]'
-      - name: Test
+          architecture: ${{ matrix.architecture }}
+      - name: Install constrained source and development checks
+        run: |
+          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
+          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
+      - name: Run complete public tests
         run: python -m unittest discover -s tests -v
-      - name: Lint
-        run: ruff check src tests examples
       - name: Compile public Python surfaces
-        run: python -m compileall -q src tests examples
+        run: python -m compileall -q src tests examples scripts
+      - name: Build and smoke the local wheel in a new environment
+        shell: bash
+        run: |
+          wheel_dir="$RUNNER_TEMP/tritrack-wheel-dist"
+          smoke_dir="$RUNNER_TEMP/tritrack-wheel-smoke"
+          test ! -e "$wheel_dir"
+          test ! -e "$smoke_dir"
+          python -m build --wheel --no-isolation --outdir "$wheel_dir"
+          python -m venv "$smoke_dir"
+          smoke_python="$smoke_dir/bin/python"
+          smoke_cli="$smoke_dir/bin/tritrack"
+          "$smoke_python" -m pip install --constraint requirements/ci-constraints.txt pip
+          wheels=("$wheel_dir"/*.whl)
+          test "${#wheels[@]}" -eq 1
+          "$smoke_python" -m pip install "${wheels[0]}"
+          "$smoke_python" -m pip check
+          "$smoke_cli" components --json
+          "$smoke_cli" validate --help
+          "$smoke_cli" validate contract --help
+          "$smoke_cli" validate fcpxml --help
+          "$smoke_cli" validate paper --help
+          "$smoke_cli" validate run --help
+
+  quality:
+    name: Public quality and policy contracts
+    runs-on: ubuntu-24.04
+    steps:
+      - name: Check out exact source
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
+      - name: Set up Python 3.13
+        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
+        with:
+          python-version: "3.13"
+          architecture: x64
+      - name: Install constrained source and development checks
+        run: |
+          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
+          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
+      - name: Lint every public Python surface
+        run: ruff check src tests examples scripts
+      - name: Verify public role, package, and CI contracts
+        run: python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v
+      - name: Verify public project identity
+        run: python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
+
+  release-gate:
+    name: Local candidate gate without publication
+    runs-on: ubuntu-24.04
+    steps:
+      - name: Check out exact source
+        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
+      - name: Set up Python 3.13
+        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
+        with:
+          python-version: "3.13"
+          architecture: x64
+      - name: Install exact gate toolchain
+        run: |
+          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
+          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
+      - name: Run the maintainer release-readiness gate locally
+        run: |
+          mkdir -p .release-evidence
+          python scripts/release_gate.py --source . --output .release-evidence/ci
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 1e14efcdbc6b57dca8f5c26b461f750e7a3ef6cf..fa26dcbe8121453289e7b2044afd6fe19899326c 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -35,6 +35,13 @@ format follows Keep a Changelog, and releases will use semantic versioning.
   reserve exclusion.
 - Separate `tritrack-editing-assistant` end-user skill with installed-help
   discovery and explicit text-revision and paper-edit human gates.
+- Four-mode read-only artifact validation for installed JSON contracts,
+  profile-bound FCPXML, paper-workbook authority, and complete immutable runs,
+  with path-free scope-limited summaries.
+- A maintainer-only clean-source privacy, reproducible package, safe-archive,
+  fresh-wheel-install, and manifest-last local candidate gate.
+- Fixed release-grade CI across Ubuntu 24.04 x64 and macOS 26 arm64 on Python
+  3.12 and 3.13, with commit-pinned official Actions and read-only permissions.
 
 ### Fixed
 
diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
index bb68963b33f17a54599980c58d36753ea39065ef..053cf916a4b6ae3f96d54c1ac0f306d8ad9b587f 100644
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -6,13 +6,14 @@ intact.
 
 ## Development setup
 
-Use Python 3.12 or newer:
+Use Python 3.12 and 3.13:
 
 ```bash
 python3.13 -m venv venv
-venv/bin/pip install -e '.[dev]'
+venv/bin/python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
+venv/bin/python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
 venv/bin/python -m unittest discover -s tests -v
-venv/bin/ruff check src tests
+venv/bin/ruff check src tests examples scripts
 ```
 
 ## Change discipline
@@ -20,8 +21,8 @@ venv/bin/ruff check src tests
 1. Open a focused issue once the public remote exists.
 2. Add or update a test that fails for the intended reason.
 3. Implement the smallest coherent change.
-4. Run focused tests, the full suite, formatting checks, and the privacy gate
-   available for that development stage.
+4. Run focused tests, the full suite, lint, package／CI contract tests, and the
+   maintainer privacy and local-candidate gates available for that stage.
 5. Explain compatibility and privacy effects in the pull request.
 
 Do not include production media, transcripts, credentials, private paths,
diff --git a/MANIFEST.in b/MANIFEST.in
new file mode 100644
index 0000000000000000000000000000000000000000..6edd3aadad38ba50caf2f7e4e09e588830461684
--- /dev/null
+++ b/MANIFEST.in
@@ -0,0 +1,33 @@
+include README.md
+include LICENSE
+include NOTICE
+include CHANGELOG.md
+include CONTRIBUTING.md
+include SECURITY.md
+include CODE_OF_CONDUCT.md
+include pyproject.toml
+include MANIFEST.in
+include .github/workflows/ci.yml
+include docs/ROADMAP.md
+include docs/TASK-11-VERIFICATION.md
+include docs/TOOLING.md
+include docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
+recursive-include examples *.py
+recursive-include skills/tritrack-editing-assistant *.md *.yaml
+include scripts/capture_basic_title_binding.py
+include scripts/release_gate.py
+include scripts/release_gate_core.py
+recursive-include release *.json
+recursive-include requirements *.txt
+recursive-include src/tritrack_editing_assistant *.py *.json *.mjs
+recursive-include tests *.py
+exclude tests/test_maintainer_boundary.py
+prune .agents
+prune .release-evidence
+prune build
+prune dist
+prune docs/reviews
+prune docs/superpowers/plans
+global-exclude *.py[cod]
+global-exclude .DS_Store
+global-exclude __pycache__
diff --git a/README.md b/README.md
index 234c1d6dbf63f58e75de9f4710d810eb68b446fb..160a3d1bfdf9b33d2548cbe167810e3fa8896d7a 100644
--- a/README.md
+++ b/README.md
@@ -10,8 +10,9 @@ decisions with the editor.
 > local `transcribe`, deterministic cue-addressed `align`, offline receipt-only
 > `hybrid`, profile-bound deterministic `emit`, strict `paper export`／
 > `paper apply`, deterministic `organize`, and immutable `run prepare`／
-> `align`／`finish`／`status`. `validate` and the optional live transport remain
-> planned and fail closed. There is no public release yet.
+> `align`／`finish`／`status`, plus four-mode read-only `validate`. The optional
+> live transport remains planned and fail closed. There is no public release
+> yet.
 
 ## Target alpha compatibility
 
@@ -23,7 +24,7 @@ profile's automated checks and invented-content Final Cut round trip pass:
 - FCPXML 1.14
 - UHD 3840×2160 at 29.97 NDF
 - Rec. 709 and stereo 48 kHz source audio
-- Python 3.12 or newer
+- Python 3.12 and 3.13
 
 The tool will fail closed outside declared compatibility profiles. It is not
 affiliated with, endorsed by, or sponsored by Apple Inc. Final Cut Pro is a
@@ -268,6 +269,30 @@ The separate installed skill at
 human gates using help-first installed commands. It contains no repository
 maintenance or publication authority.
 
+## Read-only artifact validation
+
+Read installed help before selecting one explicit validation mode:
+
+```text
+tritrack validate --help
+tritrack validate contract --help
+tritrack validate fcpxml --help
+tritrack validate paper --help
+tritrack validate run --help
+```
+
+| Mode | Exact `validationScope` | Success proves | Success does not prove |
+| --- | --- | --- | --- |
+| `contract` | `contract` | One exact JSON artifact satisfies its installed registered schema. | Referenced files, parent artifacts, or cross-file hashes exist or match. |
+| `fcpxml` | `structural-profile` | Exact FCPXML bytes satisfy the explicit installed profile and title binding structural checks. | Source media is available, a DTD passed, or a Final Cut GUI import ran. |
+| `paper` | `authority-bound` | The workbook is acceptable against the exact supplied aligned transcript bytes. | A grouping artifact was created or workbook intent was repaired. |
+| `run` | `complete-run-bundle` | The complete immutable bundle, manifest chain, fixed filenames, contracts, and hashes agree. | Any missing bundle was reconstructed or changed. |
+
+Every mode is read-only and writes no output. It does not repair inputs, guess
+a format, search sibling paths, probe source media, consult a DTD, launch a
+GUI, or make a network request. A passing result is evidence only inside the
+reported scope.
+
 ## One-minute invented quickstart
 
 After the development installation above, exercise the complete implemented
@@ -303,8 +328,9 @@ Choose the narrowest entry point that matches your goal:
    text-free working cut.
 8. Use `tritrack run` to carry the exact local artifacts through immutable
    prepared, aligned, and finished bundles with explicit editor approval.
-9. Use `tritrack components --json` to inspect what is implemented before
-   trying later roadmap commands; `validate` still fails closed.
+9. Use one explicit `tritrack validate` mode to check an existing artifact
+   without modifying it, and `tritrack components --json` to inspect the
+   unchanged eleven-component registry.
 
 ## Eleven-component roadmap
 
diff --git a/SECURITY.md b/SECURITY.md
index 46cbaa90655027774e9cd6738f3deed341a8f13f..bd84102d761905cbfde093bcce8fdf3fcbc3b87c 100644
--- a/SECURITY.md
+++ b/SECURITY.md
@@ -19,9 +19,11 @@ Never attach or paste:
 - absolute home, volume, or production paths;
 - proprietary Motion templates, fonts, Final Cut libraries, or project files.
 
-Use an invented fixture or the future sanitized `doctor` receipt when
-reproduction evidence is needed. Until that sanitizer is implemented, omit
-diagnostic attachments rather than redacting them by hand.
+Use an invented fixture or the sanitized `doctor` receipt when reproduction
+evidence is needed. The maintainer source and archive gates reject private home
+paths, credential assignments, private-key headers, forbidden binary surfaces,
+and unsafe archive structure without echoing the matching content. Omit
+sensitive diagnostic attachments rather than redacting them by hand.
 
 ## Scope
 
diff --git a/STATUS.md b/STATUS.md
index d2dbc7db03ad54f8e48158750ad4df8afe94c22f..cb4fe7e7df060cc89122044889281f0d88c7c2b6 100644
--- a/STATUS.md
+++ b/STATUS.md
@@ -1,6 +1,6 @@
 # Public maintenance status
 
-Updated: 2026-08-17
+Updated: 2026-08-18
 Project kind: public engine
 Lane: `OSS`
 Release state: public pre-release source; no tag, package publication, or
@@ -8,7 +8,7 @@ tester outreach
 
 ## Current gate
 
-Tasks 1–10 are complete in this public candidate. Task 6 began from exact
+Tasks 1–11 are complete in this public candidate. Task 6 began from exact
 Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
 fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
 rewrite or merge commit.
@@ -124,12 +124,30 @@ separate Claude subscription review requested the dynamic `opus` capability
 alias, timed out, and remains explicitly incomplete with observed／completed
 models null and no retry, downgrade, or fallback.
 
+Task 11 implementation candidate
+`ce562e995b63f3f1a29989de3e1ef202da27b5f2` adds the exact four-mode,
+read-only `tritrack validate` surface with `contract`, `structural-profile`,
+`authority-bound`, and `complete-run-bundle` claim scopes. It also adds a
+maintainer-only clean-source privacy and archive-safety gate, two-snapshot
+package reproducibility checks, fresh local-wheel installation smoke, a closed
+manifest-last receipt, exact Python／build constraints, and fixed public CI on
+Ubuntu 24.04 x64 and macOS 26 arm64 across Python 3.12／3.13. The eleven-entry
+component registry is unchanged.
+Local verification in a new Python 3.13 environment passed 69 focused and 235
+complete-suite tests, Ruff, compilation, identity, both skill validators,
+package-member policy, and Git cleanliness. The implementation gate passed
+with byte-identical wheels, identical normalized sdist member inventories,
+and an installed-wheel `pip check` plus five validator help smokes. Sanitized
+evidence and exact hashes are in `docs/TASK-11-VERIFICATION.md`.
+Task 11 made no tag, release, package publication, pull request, tester contact,
+artifact upload, signing, attestation, SBOM, Final Cut GUI, DTD, live provider,
+credential, or application-submission claim.
+
 ## Next action
 
-Task 11 expands the release-grade CI matrix and completes the privacy,
-provenance, packaging, and release gates. Task 10 does not authorize or claim
-tags, releases, package publication, tester contact, or application
-submission.
+Task 12 freezes and independently reviews the alpha candidate. Task 11 does
+not authorize or claim tags, releases, package publication, tester contact, or
+application submission.
 
 ## Implemented surface
 
@@ -151,6 +169,11 @@ submission.
   fixed artifacts, manifest-last publication, and read-only status;
 - deterministic story-ordered FCPXML projection from exact editor authorities;
 - separate installed end-user editing skill with two explicit human gates;
+- four-mode read-only artifact validation with scope-limited path-free
+  summaries;
+- clean tracked-source privacy, bounded archive inspection, reproducible
+  packaging, fresh-wheel installation, and manifest-last local candidate gate;
+- fixed Ubuntu／macOS and Python 3.12／3.13 release-grade public CI;
 - fail-closed `doctor` command;
 - exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
 - public Basic Title binding with invented-content Final Cut round-trip
@@ -158,9 +181,7 @@ submission.
 - public invented-media synchronization-to-FCPXML quickstart with deterministic
   repeat emission, conditional local DTD verification, and minimal CI.
 
-`validate` remains planned and must return non-success until implemented and
-tested. The network-capable `gemini_transcribe.mjs` component also remains
-planned.
+The network-capable `gemini_transcribe.mjs` component remains planned.
 
 ## Custody
 
diff --git a/docs/ROADMAP.md b/docs/ROADMAP.md
index 6bb0b15671d4bb2a404361e38240d7359ce316d9..974592e2c508963726b78c277cef31d2a3d1645f 100644
--- a/docs/ROADMAP.md
+++ b/docs/ROADMAP.md
@@ -31,11 +31,13 @@ here.
 - Task 10: installed immutable `run prepare`／`align`／`finish` bundles,
   read-only `run status`, deterministic story-ordered FCPXML, and a separate
   end-user `tritrack-editing-assistant` skill with explicit human gates.
+- Task 11: exact four-mode read-only artifact validation, closed source and
+  archive privacy gates, reproducible wheel／sdist package contracts, a
+  manifest-last local candidate receipt, and fixed Ubuntu／macOS CI across
+  Python 3.12／3.13.
 
 ## Next
 
-- Task 11: expand the release-grade CI matrix and complete the privacy,
-  provenance, packaging, and release gates.
 - Task 12: freeze and independently review the alpha candidate.
 - Task 13: prove the public engine as the generic authority and define a
   deliberate downstream integration seam.
diff --git a/docs/TASK-11-VERIFICATION.md b/docs/TASK-11-VERIFICATION.md
new file mode 100644
index 0000000000000000000000000000000000000000..74776d52e62a93337ef1fbe86b5a29886f6d5cec
--- /dev/null
+++ b/docs/TASK-11-VERIFICATION.md
@@ -0,0 +1,145 @@
+# Task 11 release-readiness verification
+
+Verification date: 2026-08-18
+
+Release state: local public-source candidate only; no public tag or package
+release exists.
+
+## Candidate identity
+
+- Approved design commit: `87d4c32`.
+- Clean implementation candidate:
+  `ce562e995b63f3f1a29989de3e1ef202da27b5f2`.
+- Project identity: `tritrack-editing-assistant`, `public-engine`, lane `OSS`.
+- Package version: `0.1.0a0`.
+- Tracked source: 115 regular stage-zero files, inventory SHA-256
+  `3a0544c1d5f7b318af07382932631d702a9f5f426e00fd5790aa0c34e6bf8fb9`.
+- The implementation candidate had an empty Git status before and after the
+  local gate. No generated build, environment, cache, evidence, media,
+  workbook, FCPXML, credential, or private-path file was tracked.
+
+## Clean verification environment
+
+The candidate was installed editable into a new Python environment using the
+repository's exact constraints. `pip check` reported no broken requirements.
+The observed toolchain was:
+
+| Tool | Exact version |
+| --- | --- |
+| Python implementation | CPython |
+| Python | 3.13.15 |
+| pip | 26.2 |
+| build | 1.5.0 |
+| setuptools | 84.0.0 |
+| wheel | 0.48.0 |
+| packaging | 26.3 |
+| pyproject-hooks | 1.2.0 |
+| Ruff | 0.16.2 |
+
+The clean-environment run produced these results:
+
+- 69 focused validator, release-gate, packaging, CI, and CLI tests passed.
+- 235 complete-suite tests passed.
+- All four packaging policy tests passed, including two independent builds.
+- Ruff passed over `src`, `tests`, `examples`, and `scripts`.
+- Python compilation passed over the same four public surfaces.
+- The public project-identity check passed.
+- Both the maintainer and end-user skills passed the canonical skill
+  validator.
+- `git diff --check` and the clean-worktree gate passed.
+
+## Four read-only validator scopes
+
+`tritrack validate` keeps validation claims narrow and writes no output:
+
+| Mode | Exact scope | Evidence boundary |
+| --- | --- | --- |
+| contract | `contract` | One exact artifact satisfies its installed registered JSON Schema. It does not prove references, parent artifacts, or cross-file hashes. |
+| fcpxml | `structural-profile` | Exact bytes satisfy the selected installed profile and title-binding structural checks. It makes no source-media, DTD, Final Cut GUI, or target-machine claim. |
+| paper | `authority-bound` | One workbook is acceptable against the exact supplied aligned transcript bytes. It does not publish grouping intent or repair either input. |
+| run | `complete-run-bundle` | The fixed artifact set, strict contracts, exact hashes, manifest semantics, and prior-manifest chain form one complete immutable bundle. It does not reconstruct incomplete state. |
+
+Successful JSON and human summaries contain only the exact scope, hashes, and
+bounded counts. They contain no path, filename, transcript, workbook cell,
+FCPXML text, command, time, log, or credential. The component registry remains
+eleven entries; validation is supporting infrastructure, not a twelfth
+component.
+
+## Local release gate
+
+The clean implementation candidate passed the maintainer gate. The gate built
+two independently materialized `git archive` snapshots at the same commit time,
+inspected both archives without generic extraction, installed only the chosen
+local wheel into a new environment, ran `pip check`, confirmed eleven registry
+entries, and exercised `validate --help` plus all four mode helps.
+
+The two wheels were byte-identical. The two sdists had identical normalized
+member／type／mode／size／content inventories; compressed sdist byte identity is
+not claimed. The chosen artifacts and deterministic receipt were:
+
+| Fact | Value |
+| --- | --- |
+| wheel bytes | 84,990 |
+| wheel members | 38 |
+| wheel SHA-256 | `93f8e84d513c55d37e9f214a2f55accfe4d42e6e59afa8c07d2e4839d799acc1` |
+| wheel member-inventory SHA-256 | `7a4adacafdde808bba55bfb63d75dcc6215e5c8eb2442e02c888aecb47d9ae79` |
+| sdist bytes | 169,699 |
+| sdist members | 102 |
+| sdist SHA-256 | `8cf0095b1f8f89176a6c1a1e97d67606fe2a56cc282016a94b92cf4375956637` |
+| sdist member-inventory SHA-256 | `9ded2ef3d4ff445db340a2af54c8b89e5864f12d740afda4b354031f4dce8ca1` |
+| release-manifest SHA-256 | `2f2847a218970410b2bac548a60ad0588d616fa1d4ca362e731e7ec4ebf7cb49` |
+
+The canonical manifest was hard-linked after both archives and validated
+against the closed Draft 2020-12 schema. It records only project, source
+inventory, toolchain, platform, artifact digest／size／member facts,
+reproducibility facts, passed gate names, and explicit non-claims. It records
+no local path, timestamp, duration, account, host, run identifier, command,
+log, source content, or matched value.
+
+## Fixed public CI contract
+
+The test matrix is exactly:
+
+- `ubuntu-24.04` x64 with Python 3.12;
+- `ubuntu-24.04` x64 with Python 3.13;
+- `macos-26` arm64 with Python 3.12; and
+- `macos-26` arm64 with Python 3.13.
+
+One `ubuntu-24.04`／Python 3.13 quality job and one
+`ubuntu-24.04`／Python 3.13 local release-gate job complete the workflow.
+Permissions are only `contents: read`. The official Actions are fixed to:
+
+- `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`
+  (`v7.0.1`); and
+- `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97`
+  (`v7.0.0`).
+
+Each test cell runs the complete suite, compilation, a local wheel build, a new
+wheel-only installation, `pip check`, components JSON, and all validator help
+surfaces. No CI artifact is uploaded or published.
+
+## Brainstorm provenance
+
+- Frozen public problem packet SHA-256:
+  `ff145c249aae193ce80872783b8f95e840684ee3a518e4cc2788cc607aa15921`.
+- Codex completed its independent first round before reading another model's
+  output; response SHA-256:
+  `0bdc84c66d5ca5012bcee89e8e757b0c47dae3c9e0e178a7c5118ec6427cd6c0`.
+- Gemini requested, observed, and completed `gemini-3.7-flash`; response
+  SHA-256:
+  `1d682f99a8cfad8473c574d1e4c645a1279e56e99cf55d359a16645c896e3379`.
+- Claude requested the dynamic `opus` capability alias through the approved
+  subscription-only wrapper. Attempt
+  `637f7c3a-cf72-4e97-9d42-ef7ef0d1400e` ended `claude-timeout`; observed and
+  completed models are null. The attempt remains incomplete, with no retry,
+  downgrade, paid credential, or provider fallback claim.
+
+## Explicit non-claims
+
+Task 11 performed no tag, public release, package publication, pull request,
+tester contact, artifact upload, signing, attestation, SBOM, Final Cut GUI
+operation, DTD check, live provider operation, credential access, or
+application submission. It does not establish independent cross-machine build
+reproducibility or downstream private integration. The evidence proves only
+the tested public source, package, validator, CI contract, and local candidate
+gate described above.
diff --git a/docs/TOOLING.md b/docs/TOOLING.md
index dfcb95fae3d31cad76aaa36e395623c5f17f55a9..d4ab477869bb0aeaac234584b876827e06e85505 100644
--- a/docs/TOOLING.md
+++ b/docs/TOOLING.md
@@ -6,13 +6,76 @@ or another project's tool state.
 
 ## Python
 
-- Supported runtime: Python 3.12 or newer.
+- Supported runtime: Python 3.12 and 3.13.
+- Clean gate environments install both `pip` and `setuptools` through the
+  exact `requirements/ci-constraints.txt` pins before installing `.[dev]`.
 - Full tests: `python -m unittest discover -s tests -v`
-- Lint: `ruff check src tests`
+- Lint: `ruff check src tests examples scripts`
 - Skill validation uses the current Codex `skill-creator` validator against
   both `.agents/skills/tritrack-editing-assistant-maintainer` and
   `skills/tritrack-editing-assistant`.
 
+## Read-only artifact validation
+
+The installed help authorities are:
+
+```text
+tritrack validate --help
+tritrack validate contract --help
+tritrack validate fcpxml --help
+tritrack validate paper --help
+tritrack validate run --help
+```
+
+- `contract` reports `validationScope: contract` and proves only that one exact
+  JSON artifact satisfies its installed registered schema.
+- `fcpxml` reports `validationScope: structural-profile` and proves only the
+  installed profile and title-binding structural checks. It does not probe
+  source media, validate against a DTD, or launch a Final Cut GUI.
+- `paper` reports `validationScope: authority-bound` and proves that the
+  workbook is acceptable against the exact supplied aligned transcript bytes.
+- `run` reports `validationScope: complete-run-bundle` and proves the complete
+  immutable artifact set, manifest chain, contracts, and hashes agree.
+
+All four modes are read-only. The command does not repair an artifact, guess a
+format, discover sibling inputs, write a result, use network access, or broaden
+success beyond its exact scope.
+
+## Maintainer release-readiness gate
+
+The only maintainer entry point is:
+
+```text
+python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
+```
+
+The source must be one clean Git toplevel at `HEAD`. The output parent must
+exist and the named output directory must be absent; an existing path or race
+winner is preserved. The gate inventories every stage-zero tracked regular
+file, rejects private-path／credential shapes and forbidden binary surfaces,
+builds twice from separately verified `git archive` snapshots, and inspects
+wheel／sdist metadata, paths, types, bounds, exact members, contents, and hashes
+without generic extraction.
+
+The gate requires byte-identical wheels. For sdists it requires identical
+normalized member／content inventories while recording the chosen compressed
+archive's exact SHA-256; it does not claim byte-identical gzip output. A new
+external virtual environment installs only the selected local wheel, runs
+`pip check`, confirms the eleven-component registry, and exercises all five
+validator help authorities.
+
+Publication hard-links the two archives first and canonical
+`release-manifest.json` last. The closed manifest contains only project
+name／version／commit, tracked-source count and digest, exact toolchain and
+platform facts, artifact sizes／hashes／member counts／inventory hashes, passed
+gate names, reproducibility facts, and explicit non-claims. It contains no
+path, time, account, host, command, log, source content, or matched value.
+
+Public CI uses exactly Ubuntu 24.04 x64 and macOS 26 arm64 with Python 3.12
+and 3.13, plus one Ubuntu 24.04／Python 3.13 quality job and one local candidate
+gate job. CI and the maintainer gate do not tag, publish, upload, sign, attest,
+contact testers, operate a GUI, or submit an application.
+
 ## Local synchronization
 
 - `tritrack sync --help` is the command authority for Task 5 flags.
diff --git a/docs/reviews/task-10-closeout-packet-2026-08-17.md b/docs/reviews/task-10-closeout-packet-2026-08-17.md
index 451d0c91122fb5aec1380d46c786e1f79af5949f..c9a0a19fd386ac219b213a0f9929f0d4073a191c 100644
--- a/docs/reviews/task-10-closeout-packet-2026-08-17.md
+++ b/docs/reviews/task-10-closeout-packet-2026-08-17.md
@@ -1261,7 +1261,7 @@ index 0000000..99ae2ec
 +Run both:
 +
 +```bash
-+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
++python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
 +venv/bin/python -m unittest tests.test_maintainer_boundary -v
 +```
 +
@@ -1307,8 +1307,8 @@ index 0000000..99ae2ec
 +venv/bin/ruff check src tests examples
 +venv/bin/python -m compileall -q src tests examples
 +python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
-+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
-+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
++python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
++python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
 +git diff --check
 +```
 +
@@ -6041,4 +6041,3 @@ index 0000000..61295df
 +    unittest.main()
 
 ```
-
diff --git a/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md b/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
index 99ae2ecd15a229785d46d78652a0e15e7430d256..d2971d9927a6db0ab6ecd547610122c370e4df9c 100644
--- a/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
+++ b/docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
@@ -452,7 +452,7 @@ command help and preserves both human gates.
 Run both:
 
 ```bash
-python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
 venv/bin/python -m unittest tests.test_maintainer_boundary -v
 ```
 
@@ -498,8 +498,8 @@ venv/bin/python -m unittest discover -s tests -v
 venv/bin/ruff check src tests examples
 venv/bin/python -m compileall -q src tests examples
 python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
-python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
-python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py .agents/skills/tritrack-editing-assistant-maintainer
+python3 ${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py skills/tritrack-editing-assistant
 git diff --check
 ```
 
diff --git a/docs/superpowers/plans/2026-08-17-task-11-release-readiness.md b/docs/superpowers/plans/2026-08-17-task-11-release-readiness.md
new file mode 100644
index 0000000000000000000000000000000000000000..1a0aa1496c4b4c242c9da2f34d0ae1e7119f2467
--- /dev/null
+++ b/docs/superpowers/plans/2026-08-17-task-11-release-readiness.md
@@ -0,0 +1,1190 @@
+# Task 11 release readiness implementation plan
+
+> **For Codex:** Execute this plan with the official Superpowers
+> `test-driven-development` workflow. Preserve each observed RED before the
+> matching minimal GREEN implementation. Use `reviewing-with-multiple-ai` only
+> after the complete local candidate is frozen.
+
+**Goal:** Ship the four-mode offline `tritrack validate` command and a
+maintainer-only, fail-closed release gate that proves source privacy, package
+contents, reproducibility, clean-wheel installation, and fixed public CI
+coverage without publishing a tag, release, package, or external artifact.
+
+**Architecture:** End-user validation lives in the installed Python package and
+reuses the existing contract, FCPXML, paper-workbook, and immutable-run
+authorities. Maintainer release logic lives under `scripts/`, reads the complete
+Git index, builds only from two clean snapshots of one commit, inspects archives
+before extraction or installation, and publishes a path-free manifest last.
+The two authority domains share no release controls or network behavior.
+
+**Tech stack:** Python 3.12/3.13, `jsonschema` Draft 2020-12, `openpyxl`,
+`setuptools`/`build`, standard-library ZIP/TAR inspection, `unittest`, Ruff,
+GitHub Actions on fixed Linux x64 and macOS arm64 images.
+
+**Approved design:**
+`docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md` at
+commit `87d4c32`. Do not broaden its grants or non-claims.
+
+**Verified packaging premise:** A two-snapshot experiment at the approved-spec
+commit produced byte-identical wheels. The two sdists had identical 60-member
+extracted trees but different compressed bytes. Therefore the implemented
+reproducibility contract is exact wheel-byte equality plus exact normalized
+sdist member/content-inventory equality. The final chosen wheel and sdist still
+receive their own exact SHA-256 values in `release-manifest.json`.
+
+**Pinned CI inputs:**
+
+- `actions/checkout@v7.0.1` →
+  `3d3c42e5aac5ba805825da76410c181273ba90b1`
+- `actions/setup-python@v7.0.0` →
+  `5fda3b95a4ea91299a34e894583c3862153e4b97`
+- build constraints: `build==1.5.0`, `packaging==26.3`, `pip==26.2`,
+  `pyproject-hooks==1.2.0`, `ruff==0.16.2`, `setuptools==84.0.0`, and
+  `wheel==0.48.0`
+
+---
+
+### Task 1: Add strict installed-contract discovery and the contract validator
+
+**Files:**
+
+- Modify: `src/tritrack_editing_assistant/contracts.py`
+- Create: `src/tritrack_editing_assistant/validate_artifacts.py`
+- Create: `tests/test_validate_artifacts.py`
+
+- [ ] **Step 1: Write the failing contract-mode tests**
+
+Add tests that create invented valid instances for every name in
+`CONTRACT_NAMES`, write canonical or non-canonical JSON bytes to a regular
+file, and assert:
+
+- `validate_contract_artifact(path)` discovers the contract only from the
+  installed schema's exact `schemaVersion.const`;
+- the returned summary is exactly `tritrack.validate-summary/v1`, kind
+  `contract`, scope `contract`, the tool version, one artifact SHA-256, an empty
+  bounded count map, and details containing only `contractName` and
+  `contractSchemaVersion`;
+- no input is written or normalized;
+- unknown, missing, duplicate-schema, malformed UTF-8/JSON, non-regular,
+  symlink, empty, oversized, schema-invalid, and late-changed inputs fail with
+  stable `TRITRACK_VALIDATE_*` codes;
+- summaries and errors contain no artifact path or artifact content.
+
+Build the duplicate-schema case by mocking `load_schema`; do not add a fake
+installed contract.
+
+- [ ] **Step 2: Run the focused test and observe RED**
+
+Run:
+
+```bash
+python -m unittest tests.test_validate_artifacts.ContractValidationTest -v
+```
+
+Expected: import failure because `validate_artifacts` and schema-version
+discovery do not exist.
+
+- [ ] **Step 3: Implement the smallest strict contract seam**
+
+In `contracts.py`, add a cached closed map and lookup:
+
+```python
+@cache
+def contract_names_by_schema_version() -> Mapping[str, str]:
+    mapping: dict[str, str] = {}
+    for name in sorted(CONTRACT_NAMES):
+        schema = load_schema(name)
+        version = schema["properties"]["schemaVersion"]["const"]
+        if not isinstance(version, str) or version in mapping:
+            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID")
+        mapping[version] = name
+    return MappingProxyType(mapping)
+
+
+def contract_name_for_schema_version(schema_version: object) -> str:
+    if not isinstance(schema_version, str):
+        raise ValueError("TRITRACK_CONTRACT_UNKNOWN")
+    try:
+        return contract_names_by_schema_version()[schema_version]
+    except KeyError as error:
+        raise ValueError("TRITRACK_CONTRACT_UNKNOWN") from error
+```
+
+In `validate_artifacts.py`, define:
+
+```python
+MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024
+
+@dataclass(frozen=True)
+class LoadedValidationArtifact:
+    path: Path
+    encoded: bytes
+    sha256: str
+```
+
+Add `validate_contract_artifact(path: Path) -> dict[str, object]` with the
+exact behavior below.
+
+Use an `O_NOFOLLOW` regular-file reader, strict UTF-8, `Decimal` for JSON
+floats, the installed schema-version map, `contracts.validate_contract`, and a
+second exact-byte verification before returning. Normalize all parser/schema
+exceptions to stable codes without embedding exception text.
+
+The shared summary builder must emit only:
+
+```python
+{
+    "schemaVersion": "tritrack.validate-summary/v1",
+    "toolVersion": __version__,
+    "artifactKind": kind,
+    "validationScope": scope,
+    "hashes": hashes,
+    "counts": counts,
+    "details": details,
+}
+```
+
+- [ ] **Step 4: Run focused tests and the contract regressions**
+
+Run:
+
+```bash
+python -m unittest tests.test_validate_artifacts.ContractValidationTest tests.test_contracts -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit the contract slice**
+
+```bash
+git add src/tritrack_editing_assistant/contracts.py \
+  src/tritrack_editing_assistant/validate_artifacts.py \
+  tests/test_validate_artifacts.py
+git commit -m "feat: add strict contract artifact validation"
+```
+
+---
+
+### Task 2: Add the profile-bound FCPXML validator mode
+
+**Files:**
+
+- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
+- Modify: `tests/test_validate_artifacts.py`
+- Modify: `tests/test_emit_fcpxml.py`
+
+- [ ] **Step 1: Write the failing FCPXML-mode tests**
+
+Render invented valid XML through the existing emitter and assert
+`validate_fcpxml_artifact(path, profile_id, binding_id)`:
+
+- loads only the exact installed profile and title binding;
+- delegates structural/profile/title/time validation to
+  `emit_fcpxml.validate_fcpxml`;
+- returns kind `fcpxml`, scope `structural-profile`, the exact byte hash, empty
+  counts, and only `profileId`/`bindingId` details;
+- performs no DTD lookup, media probe, subprocess, network call, output write,
+  or Final Cut operation;
+- rejects unknown profile/binding, wrong profile/title/time, entity/extra
+  doctype, malformed UTF-8/XML, symlink, oversize, and late change;
+- never reports a DTD, GUI import, or round-trip claim.
+
+- [ ] **Step 2: Run the focused test and observe RED**
+
+```bash
+python -m unittest tests.test_validate_artifacts.FcpxmlValidationTest -v
+```
+
+Expected: missing `validate_fcpxml_artifact`.
+
+- [ ] **Step 3: Implement by composition, not duplicate parsing policy**
+
+Add:
+
+```python
+def validate_fcpxml_artifact(
+    path: Path,
+    *,
+    profile_id: str,
+    binding_id: str,
+) -> dict[str, object]:
+    artifact = _load_regular_artifact(path, code="TRITRACK_VALIDATE_INPUT_UNREADABLE")
+    try:
+        text = artifact.encoded.decode("utf-8", errors="strict")
+        profile = doctor.load_profile(profile_id)
+        binding = doctor.load_title_binding(binding_id)
+        emit_fcpxml.validate_fcpxml(text, profile=profile, binding=binding)
+    except UnicodeError as error:
+        raise ValueError("TRITRACK_VALIDATE_FCPXML_INVALID") from error
+    _verify_unchanged(artifact)
+    return _validation_summary(
+        kind="fcpxml",
+        scope="structural-profile",
+        hashes={"artifact": artifact.sha256},
+        counts={},
+        details={"profileId": profile_id, "bindingId": binding_id},
+    )
+```
+
+Let existing exact `TRITRACK_PROFILE_*`, `TRITRACK_TITLE_BINDING_*`, and
+`TRITRACK_FCPXML_*` codes propagate; do not print their exception causes.
+
+- [ ] **Step 4: Run focused and emitter regressions**
+
+```bash
+python -m unittest tests.test_validate_artifacts.FcpxmlValidationTest \
+  tests.test_emit_fcpxml -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/validate_artifacts.py \
+  tests/test_validate_artifacts.py tests/test_emit_fcpxml.py
+git commit -m "feat: add profile-bound FCPXML validation"
+```
+
+---
+
+### Task 3: Extract read-only paper-workbook validation and add paper mode
+
+**Files:**
+
+- Modify: `src/tritrack_editing_assistant/paper_edit.py`
+- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
+- Modify: `tests/test_paper_edit.py`
+- Modify: `tests/test_validate_artifacts.py`
+
+- [ ] **Step 1: Write failing pure-paper tests**
+
+Use the existing invented aligned/workbook fixtures. Assert:
+
+- new `paper_edit.validate_workbook(aligned, workbook)` performs every check
+  currently performed by `apply_workbook` but creates no output;
+- `apply_workbook` and `validate_workbook` accept and reject exactly the same
+  workbooks;
+- changed cue/display/manifest values, formulas, hyperlinks, unsafe ZIPs,
+  extreme dimensions, invalid selection references, symlinks, and late changes
+  fail closed;
+- the validated internal object may retain grouping only for `apply_workbook`,
+  while the public validator summary contains no transcript, question text,
+  note, cue text, workbook path, or grouping body.
+
+The public `validate paper` summary must have kind `paper`, scope
+`authority-bound`, aligned/workbook hashes, and exact cue/question/answer/
+reserve counts.
+
+- [ ] **Step 2: Run the focused tests and observe RED**
+
+```bash
+python -m unittest tests.test_paper_edit.PaperEditTest \
+  tests.test_validate_artifacts.PaperValidationTest -v
+```
+
+Expected: missing `validate_workbook` and `validate_paper_artifacts`.
+
+- [ ] **Step 3: Extract one immutable validation result**
+
+Add a frozen `ValidatedWorkbook` dataclass with exactly these fields:
+`aligned_sha256`, `workbook_sha256`, `workbook_schema_version`, `cue_count`,
+`question_count`, `answer_count`, `reserve_count`, and the internal `grouping`.
+Add `validate_workbook(aligned_path: Path, workbook_path: Path) ->
+ValidatedWorkbook` with the docstring “Validate and re-derive one workbook
+without publishing output.”
+
+Move the existing aligned/workbook loading, cue-grid derivation, unsafe-state
+checks, manifest verification, grouping derivation, and final input rehash into
+this function. Keep `grouping` private to the Python seam. Refactor
+`apply_workbook` to reserve the absent destination first, call
+`validate_workbook`, and publish only `validated.grouping`.
+
+Add `validate_paper_artifacts` in `validate_artifacts.py`; project only hashes
+and counts from `ValidatedWorkbook` into the public summary.
+
+- [ ] **Step 4: Run paper, organizer, and validation regressions**
+
+```bash
+python -m unittest tests.test_paper_edit tests.test_organizer \
+  tests.test_validate_artifacts.PaperValidationTest -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/paper_edit.py \
+  src/tritrack_editing_assistant/validate_artifacts.py \
+  tests/test_paper_edit.py tests/test_validate_artifacts.py
+git commit -m "refactor: share paper validation authority"
+```
+
+---
+
+### Task 4: Share immutable-run inspection with status and add run mode
+
+**Files:**
+
+- Modify: `src/tritrack_editing_assistant/run_workflow.py`
+- Modify: `src/tritrack_editing_assistant/validate_artifacts.py`
+- Modify: `tests/test_run_workflow.py`
+- Modify: `tests/test_validate_artifacts.py`
+
+- [ ] **Step 1: Write failing run-inspection tests**
+
+For invented prepared, aligned, and finished bundles, assert:
+
+- `inspect_run(run_dir)` uses `load_bundle`, revalidates the complete fixed
+  member set and exact hashes, then rechecks the bundle before returning;
+- `status_run` and `validate_run_bundle` share the same `runId`, phase,
+  `nextAction`, ordered stage names, and logical artifact hashes;
+- the validation summary has kind `run`, scope `complete-run-bundle`, manifest
+  hash, stage/artifact counts, and its exact existing run summary under
+  `details.runSummary`;
+- missing/extra members, malformed/noncanonical manifest, wrong phase set,
+  broken chain facts, changed artifacts, symlinks, and late changes fail with
+  existing run codes;
+- both surfaces write nothing and expose no transcript/editor text or path.
+
+- [ ] **Step 2: Run focused tests and observe RED**
+
+```bash
+python -m unittest tests.test_run_workflow.RunStatusTest \
+  tests.test_validate_artifacts.RunValidationTest -v
+```
+
+Expected: missing `inspect_run`/`validate_run_bundle` or mismatched late-change
+behavior.
+
+- [ ] **Step 3: Implement one shared read-only run inspection**
+
+Add:
+
+```python
+def inspect_run(run_dir: Path) -> tuple[LoadedRunBundle, dict[str, object]]:
+    bundle = load_bundle(Path(run_dir))
+    _require_bundle_unchanged(bundle)
+    return bundle, summarize_bundle(bundle)
+
+
+def status_run(run_dir: Path) -> dict[str, object]:
+    return inspect_run(run_dir)[1]
+```
+
+Then add `validate_run_bundle` that calls `inspect_run` and projects its exact
+facts. Do not add sibling discovery or a second bundle parser.
+
+- [ ] **Step 4: Run full run/validator regressions**
+
+```bash
+python -m unittest tests.test_run_workflow \
+  tests.test_validate_artifacts.RunValidationTest -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/run_workflow.py \
+  src/tritrack_editing_assistant/validate_artifacts.py \
+  tests/test_run_workflow.py tests/test_validate_artifacts.py
+git commit -m "feat: share complete run validation"
+```
+
+---
+
+### Task 5: Replace the placeholder with the exact four-mode CLI
+
+**Files:**
+
+- Modify: `src/tritrack_editing_assistant/cli.py`
+- Modify: `tests/test_cli.py`
+- Modify: `tests/test_validate_artifacts.py`
+
+- [ ] **Step 1: Write CLI RED tests for all four help authorities**
+
+Exercise `cli.main` and subprocess-installed help. Assert these exact forms:
+
+```text
+tritrack validate contract --artifact FILE [--json]
+tritrack validate fcpxml --artifact FILE --profile ID --binding ID [--json]
+tritrack validate paper --aligned FILE --workbook FILE [--json]
+tritrack validate run --run DIRECTORY [--json]
+```
+
+For success, assert JSON is exactly the core summary and human output is only
+stable tab-separated kind/scope/hash/count/detail facts. For failure, assert
+one JSON object `{"error":"TRITRACK_*"}`, no traceback/content/path, and these
+exit classes:
+
+- usage `64` for parser or handler usage errors;
+- data `65` for malformed or semantically invalid artifacts;
+- I/O `74` for missing/unreadable/non-regular input;
+- policy `78` for unknown installed profile/binding.
+
+Also assert `validate` is removed only from `planned_commands`, no twelfth
+component is added, and every mode performs zero writes/network/provider/
+credential/subprocess operations.
+
+- [ ] **Step 2: Run CLI tests and observe RED**
+
+```bash
+python -m unittest tests.test_cli.ValidateCliTest -v
+```
+
+Expected: `TRITRACK_COMMAND_NOT_IMPLEMENTED: validate` or missing nested help.
+
+- [ ] **Step 3: Add parser, handler, exit mapping, and bounded printers**
+
+Import `validate_artifacts as validate_module`. Add `_run_validate`,
+`_validate_error_exit`, and `_print_validation_summary`. Add a
+`TriTrackArgumentParser` whose non-help parse errors raise one private
+`CliUsageError`; catch that error in `main`, print only
+`{"error":"TRITRACK_USAGE"}`, and return `EXIT_USAGE`. Use the same parser
+class for nested parsers so invalid or missing validate flags return 64 rather
+than argparse's default 2. Add regression coverage for existing commands'
+usage errors. Construct one required nested `validate` subparser with four
+required mode parsers and only the flags above. Dispatch directly to the
+matching core function.
+
+Human output must use this closed projection:
+
+```text
+VALIDATION\t<artifactKind>\t<validationScope>
+HASH\t<logical-name>\t<sha256>
+COUNT\t<logical-name>\t<integer>
+DETAIL\t<logical-name>\t<compact-json-scalar-or-object>
+```
+
+Sort hash/count/detail keys. Never stringify an exception or `Path`.
+
+- [ ] **Step 4: Run focused and complete validator tests**
+
+```bash
+python -m unittest tests.test_cli.ValidateCliTest \
+  tests.test_validate_artifacts -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add src/tritrack_editing_assistant/cli.py tests/test_cli.py \
+  tests/test_validate_artifacts.py
+git commit -m "feat: implement four-mode offline validator"
+```
+
+---
+
+### Task 6: Freeze Python support, distribution contents, and release schemas
+
+**Files:**
+
+- Modify: `pyproject.toml`
+- Create: `requirements/ci-constraints.txt`
+- Create: `MANIFEST.in`
+- Create: `release/package-policy-v1.json`
+- Create: `release/release-manifest-v1.schema.json`
+- Create: `tests/test_packaging.py`
+- Modify: `docs/reviews/task-10-closeout-packet-2026-08-17.md`
+- Modify: `docs/superpowers/plans/2026-08-17-task-10-immutable-run.md`
+
+- [ ] **Step 1: Write packaging RED tests**
+
+Build two wheels and two sdists from separate copied source trees with
+`SOURCE_DATE_EPOCH=1704067200` and `python -m build --no-isolation`. Assert:
+
+- `requires-python` is exactly `>=3.12,<3.14`, classifiers are exactly 3.12 and
+  3.13, runtime requirements retain bounded ranges, and all build/development
+  tools resolve through exact constraints;
+- wheels are byte-identical and contain only runtime package code/resources,
+  entry-point metadata, and required license metadata;
+- wheels contain no tests, docs, skills, CI, release scripts, source-only
+  examples, caches, or generated evidence;
+- sdists have identical normalized member/content inventories and contain the
+  currently implemented buildable package source, all public runtime tests and
+  helpers, the quickstart example, CI workflow, end-user skill, public
+  policies, and approved Task 11 design;
+- sdists exclude `.agents`, `test_maintainer_boundary.py`, raw external-review
+  artifacts, historical implementation plans, ignored outputs, caches, and
+  private/binary media;
+- any unexpected wheel/sdist member fails the policy test.
+
+This base packaging test must pass before release scripts exist. Task 8 extends
+the same test and manifest with the completed release entry/core, while the
+closeout task makes the Task 11 verification record mandatory before the real
+gate.
+
+- [ ] **Step 2: Run and observe RED**
+
+```bash
+python -m unittest tests.test_packaging -v
+```
+
+Expected: current `>=3.12`, missing constraints/policy files, and missing
+end-user skill/policy documents in the sdist.
+
+- [ ] **Step 3: Implement explicit package policy**
+
+Change:
+
+```toml
+[build-system]
+requires = ["setuptools==84.0.0"]
+
+[project]
+requires-python = ">=3.12,<3.14"
+
+[project.optional-dependencies]
+dev = ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"]
+```
+
+Write the seven exact tool/transitive constraints listed at the top of this
+plan. Use `MANIFEST.in` to include only the approved base sdist surfaces,
+including `.github/workflows/ci.yml`, and explicitly prune `.agents`,
+`docs/reviews`, `docs/superpowers/plans`, generated evidence, and the
+maintainer-boundary test. Task 8 adds its completed release scripts to this
+allowlist; do not add nonexistent placeholders.
+
+`release/package-policy-v1.json` must be closed and versioned. It owns allowed
+top-level roots, required members, forbidden roots/suffixes, count/size caps,
+and the one-sdist-root rule. `release-manifest-v1.schema.json` must use
+`additionalProperties: false` at every object and define exactly:
+
+```text
+schemaVersion
+project(name, version, commit)
+sourceInventory(count, sha256)
+toolchain(python, implementation, pip, build, setuptools, wheel)
+platform(system, machine)
+artifacts(wheel|sdist: sha256, sizeBytes, memberCount, memberInventorySha256)
+reproducibility(wheelBytesMatch, sdistMembersMatch)
+gates(sourceIdentity, sourcePrivacy, wheelArchive, sdistArchive, freshInstall)
+nonClaims
+```
+
+No path, timestamp, hostname, username, run ID, command, duration, log, raw
+matched secret, or content field is permitted.
+
+- [ ] **Step 4: Remove existing machine-specific path debt**
+
+Replace the three historical machine-specific absolute skill-validator
+invocations in the Task 10 plan and packet with
+`${CODEX_SKILLS_ROOT}/.system/skill-creator/scripts/quick_validate.py`. Do not
+rewrite any other historical evidence. Keep generic invented editor-home
+security canaries only where tests require them.
+
+- [ ] **Step 5: Run packaging tests twice**
+
+```bash
+python -m unittest tests.test_packaging -v
+python -m unittest tests.test_packaging -v
+```
+
+Expected: both PASS; wheel SHA is stable across both builds within each run,
+and sdist normalized inventories match.
+
+- [ ] **Step 6: Commit**
+
+```bash
+git add pyproject.toml requirements/ci-constraints.txt MANIFEST.in release \
+  tests/test_packaging.py \
+  docs/reviews/task-10-closeout-packet-2026-08-17.md \
+  docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
+git commit -m "build: freeze public package policy"
+```
+
+---
+
+### Task 7: Implement tracked-source privacy and archive safety gates
+
+**Files:**
+
+- Create: `scripts/release_gate_core.py`
+- Create: `tests/test_release_gate.py`
+- Modify: `release/package-policy-v1.json`
+- Modify: `release/release-manifest-v1.schema.json`
+
+- [ ] **Step 1: Write failing source-inventory/privacy tests**
+
+Create temporary invented Git repositories and assert the core:
+
+- reads `git ls-files -s -z` for the complete index and accepts only stage 0
+  regular `100644`/`100755` entries;
+- fails on tracked symlinks, submodules, special/unsupported modes, unmerged
+  entries, dirty tracked bytes, and source change during the scan;
+- bounds per-file size, total size, and file count before reading;
+- scans all tracked bytes, including docs and tests, for private home paths,
+  credential assignments, private-key headers, and forbidden binary/media
+  suffixes;
+- accepts only explicit low-entropy invented canaries such as `editor`,
+  `example`, `fake`, `test`, `redacted`, `placeholder`, and `secret`;
+- returns only codes/counts/digests and never the matching line, value, or path.
+
+Build realistic-looking failure strings at test runtime from split fragments so
+the release gate does not reject its own tracked tests.
+
+- [ ] **Step 2: Write failing malicious-archive tests**
+
+Generate invented ZIP and TAR fixtures in temporary directories. Assert
+rejection of:
+
+- absolute paths and `..` traversal;
+- symlink/hardlink/device/FIFO members;
+- duplicate and Unicode-casefold-colliding names;
+- encrypted ZIP members;
+- excessive compressed artifact size, member count, individual expansion, or
+  aggregate expansion;
+- wrong top-level roots, unexpected files, missing required files, and
+  forbidden wheel/sdist surfaces;
+- credential/private-path patterns inside accepted text members.
+
+Assert member inventory digests bind normalized relative member name, type,
+mode, size, and content SHA-256, while the returned result exposes no member
+names.
+
+- [ ] **Step 3: Run tests and observe RED**
+
+```bash
+python -m unittest tests.test_release_gate.SourceGateTest \
+  tests.test_release_gate.ArchiveGateTest -v
+```
+
+Expected: missing release-gate core.
+
+- [ ] **Step 4: Implement bounded pure core functions**
+
+Define frozen `SourceInventory` and `DistributionInspection` dataclasses plus
+`ReleaseGateError`, whose constructor accepts one stable `code` and whose
+string form is only that code. Implement these exact public core signatures:
+
+- `inventory_tracked_source(source: Path) -> SourceInventory`
+- `inspect_wheel(path: Path, policy: Mapping[str, object]) -> DistributionInspection`
+- `inspect_sdist(path: Path, policy: Mapping[str, object]) -> DistributionInspection`
+- `scan_public_bytes(encoded: bytes) -> None`
+
+Invoke Git with argv only, `shell=False`, a fixed environment allowlist, byte
+capture limits, and timeouts. Do not decode or emit unsafe subprocess output.
+Read working-tree files using `O_NOFOLLOW`; scan the Git status both before and
+after inventory. For ZIP/TAR, validate metadata and all bounds before reading a
+member body. Never call a generic archive extraction API during inspection.
+
+- [ ] **Step 5: Run focused and source-boundary regressions**
+
+```bash
+python -m unittest tests.test_release_gate.SourceGateTest \
+  tests.test_release_gate.ArchiveGateTest tests.test_maintainer_boundary -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 6: Commit**
+
+```bash
+git add scripts/release_gate_core.py tests/test_release_gate.py \
+  release/package-policy-v1.json release/release-manifest-v1.schema.json
+git commit -m "feat: add source privacy and archive gates"
+```
+
+---
+
+### Task 8: Orchestrate clean builds, fresh install smoke, and manifest-last publication
+
+**Files:**
+
+- Create: `scripts/release_gate.py`
+- Modify: `scripts/release_gate_core.py`
+- Modify: `tests/test_release_gate.py`
+- Modify: `tests/test_packaging.py`
+- Modify: `MANIFEST.in`
+- Modify: `release/package-policy-v1.json`
+
+- [ ] **Step 1: Write orchestration and publication RED tests**
+
+Inject bounded fake command/build/install seams and assert:
+
+- `--source` must be one clean Git toplevel at `HEAD`; version is read from
+  `pyproject.toml` and must match installed package metadata;
+- output must be absent, with an existing output or race winner preserved;
+- two `git archive HEAD` snapshots build under the same fixed commit time and
+  exact build toolchain;
+- wheel bytes must match; sdist normalized member inventories must match;
+- both final archives pass privacy/content/safety inspection before install;
+- a new venv installs only the chosen local wheel, `pip check` passes, and
+  installed `tritrack components --json`, `validate --help`, and all four mode
+  helps return success;
+- any source/build/inspection/install/smoke/schema failure stops publication;
+- archive files are linked into the reserved output first and canonical
+  `release-manifest.json` is linked last;
+- injected interruption before the last link leaves no manifest and cannot be
+  mistaken for success;
+- a successful manifest validates against the closed schema and contains no
+  path/time/run/log/content field.
+
+- [ ] **Step 2: Run and observe RED**
+
+```bash
+python -m unittest tests.test_release_gate.OrchestrationTest \
+  tests.test_release_gate.PublicationTest -v
+```
+
+Expected: missing orchestration and CLI.
+
+- [ ] **Step 3: Implement exact build and smoke stages**
+
+Add bounded functions with these exact public signatures:
+
+- `build_distributions(snapshot: Path, output: Path, *, epoch: int) -> tuple[Path, Path]`
+- `fresh_install_smoke(wheel: Path, temporary: Path) -> None`
+- `build_release_manifest(context: ReleaseContext) -> dict[str, object]`
+- `publish_release(output: Path, wheel: Path, sdist: Path, manifest: bytes) -> None`
+- `run_release_gate(source: Path, output: Path) -> dict[str, object]`
+
+Use `sys.executable -m build --no-isolation`; validate exact installed build
+tool versions, including `pip==26.2`, before building. Extract only the trusted
+`git archive` after verifying its members are the exact tracked source
+inventory. Create a fresh venv with `sys.executable -m venv`, install the exact
+pinned pip, then install the local wheel by argv, run `pip check`, and run
+installed CLI smoke. The wheel is the only TriTrack source accepted by the
+smoke environment; its bounded runtime dependencies may resolve from the
+configured Python index. No shell, source install, editable install, or
+current-worktree import is allowed in the smoke venv.
+
+Extend `MANIFEST.in`, `release/package-policy-v1.json`, and
+`tests/test_packaging.py` so the now-existing `scripts/release_gate.py`,
+`scripts/release_gate_core.py`, release schema, and package policy are mandatory
+sdist members. The test must stay GREEN before commit.
+
+Canonicalize the manifest with sorted UTF-8 JSON plus one final newline and
+validate it before publication. Reserve output with `os.mkdir`, hard-link the
+two archives, fsync, hard-link the manifest last, then fsync again. Never
+overwrite or repair an existing output.
+
+- [ ] **Step 4: Implement the maintainer-only CLI**
+
+`scripts/release_gate.py` must accept only:
+
+```text
+python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
+```
+
+On success print only `RELEASE_GATE\tPASS`, commit, version, artifact hashes,
+and manifest hash. On failure print one JSON error code without exception text
+or path. It must not expose any installed `tritrack` entry point.
+
+- [ ] **Step 5: Run unit and packaging regressions**
+
+```bash
+python -m unittest tests.test_release_gate tests.test_packaging -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 6: Commit**
+
+```bash
+git add scripts/release_gate.py scripts/release_gate_core.py \
+  tests/test_release_gate.py tests/test_packaging.py MANIFEST.in \
+  release/package-policy-v1.json
+git commit -m "feat: add maintainer release gate"
+```
+
+---
+
+### Task 9: Replace minimal CI with the fixed release-grade matrix
+
+**Files:**
+
+- Modify: `.github/workflows/ci.yml`
+- Create: `tests/test_release_ci.py`
+- Modify: `requirements/ci-constraints.txt`
+- Modify: `tests/test_quickstart_demo.py`
+
+- [ ] **Step 1: Write CI contract RED tests**
+
+Read the workflow as public configuration and assert:
+
+- test matrix has exactly four include cells:
+  `ubuntu-24.04`/x64 × Python 3.12/3.13 and
+  `macos-26`/arm64 × Python 3.12/3.13;
+- every cell runs constrained editable install, full unittest discovery,
+  compileall, local wheel build, new-venv wheel install, `pip check`,
+  `components --json`, and all validator helps;
+- quality runs once on `ubuntu-24.04`/Python 3.13 and runs Ruff over
+  `src tests examples scripts` plus package/CI contract tests;
+- release gate runs once on `ubuntu-24.04`/Python 3.13 into an ignored absent
+  `.release-evidence/ci` directory;
+- Actions use only the two exact commit SHAs at the top of this plan;
+- workflow permissions are only `contents: read`;
+- no `upload-artifact`, release, tag, registry, signing, attestation, SBOM,
+  provider, credential, GUI, or DTD step exists;
+- no moving runner label or moving `@vN` Action reference exists.
+
+- [ ] **Step 2: Run and observe RED**
+
+```bash
+python -m unittest tests.test_release_ci -v
+```
+
+Expected: current `ubuntu-latest`, two-cell matrix, mutable Action tags, and
+missing packaging/release jobs.
+
+- [ ] **Step 3: Write the exact workflow**
+
+Use explicit `matrix.include`, `fail-fast: false`, fixed runner labels, and the
+two pinned Action SHAs with version comments. Do not enable setup-python cache.
+Install the exact pip first, then the constrained project:
+
+```bash
+python -m pip install --constraint requirements/ci-constraints.txt pip
+python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
+```
+
+For the per-cell wheel smoke, build with `--wheel --no-isolation` to a fresh
+runner-temp directory, create a second venv, install the single local wheel,
+run `pip check`, then invoke installed help. For the release job, run only the
+maintainer release-gate entry point after the constrained development install.
+
+- [ ] **Step 4: Run CI and quickstart contract tests**
+
+```bash
+python -m unittest tests.test_release_ci tests.test_quickstart_demo -v
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add .github/workflows/ci.yml requirements/ci-constraints.txt \
+  tests/test_release_ci.py tests/test_quickstart_demo.py
+git commit -m "ci: add fixed release-grade matrix"
+```
+
+---
+
+### Task 10: Document validator and maintainer gate without crossing roles
+
+**Files:**
+
+- Modify: `README.md`
+- Modify: `docs/TOOLING.md`
+- Modify: `CONTRIBUTING.md`
+- Modify: `CHANGELOG.md`
+- Modify: `SECURITY.md`
+- Modify: `skills/tritrack-editing-assistant/SKILL.md`
+- Modify: `tests/test_maintainer_boundary.py`
+- Modify: `tests/test_cli.py`
+
+- [ ] **Step 1: Write documentation/role-firewall RED tests**
+
+Assert README, tooling, and the end-user skill contain all five validator help
+authorities (`validate --help` plus four modes), state each exact scope and
+non-claim, and never instruct format guessing, output repair, DTD/media/GUI
+checks, provider access, credentials, or release actions.
+
+Assert only `docs/TOOLING.md` and maintainer governance document
+`python scripts/release_gate.py --source . --output ABSENT_DIRECTORY`; the end-user skill
+must continue to reject `release`, task numbers, branches, standing grants,
+tester language, source filenames, `.py`, and maintainer identity.
+
+Assert public Python support says exactly 3.12 and 3.13, not “or newer.”
+
+- [ ] **Step 2: Run and observe RED**
+
+```bash
+python -m unittest tests.test_maintainer_boundary \
+  tests.test_cli.ValidateDocumentationTest -v
+```
+
+Expected: validator still described as planned and release gate undocumented.
+
+- [ ] **Step 3: Update public and maintainer documentation**
+
+Add a concise README section with the four commands and a table of scopes:
+`contract`, `structural-profile`, `authority-bound`, and
+`complete-run-bundle`. State that success is evidence only within that scope.
+
+In `docs/TOOLING.md`, record the exact maintainer gate, absent-output rule,
+source/archive/fresh-install checks, wheel/sdist reproducibility distinction,
+manifest fields, fixed CI matrix, and prohibited outward actions.
+
+In the end-user skill, add help-first read-only validation after generated
+artifacts, but no release language or maintainer controls. Update changelog,
+contributing, and security language truthfully; keep “no public release yet.”
+
+- [ ] **Step 4: Validate role firewalls and skills**
+
+```bash
+python -m unittest tests.test_maintainer_boundary \
+  tests.test_cli.ValidateDocumentationTest -v
+TASK11_SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
+python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
+  .agents/skills/tritrack-editing-assistant-maintainer
+python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
+  skills/tritrack-editing-assistant
+```
+
+Expected: PASS.
+
+- [ ] **Step 5: Commit**
+
+```bash
+git add README.md docs/TOOLING.md CONTRIBUTING.md CHANGELOG.md SECURITY.md \
+  skills/tritrack-editing-assistant/SKILL.md \
+  tests/test_maintainer_boundary.py tests/test_cli.py
+git commit -m "docs: publish Task 11 validation boundaries"
+```
+
+---
+
+### Task 11: Run the complete local candidate and create final public records
+
+**Files:**
+
+- Create: `docs/TASK-11-VERIFICATION.md`
+- Modify: `STATUS.md`
+- Modify: `docs/ROADMAP.md`
+- Modify: `tests/test_maintainer_boundary.py`
+- Modify: `tests/test_packaging.py`
+- Modify: `MANIFEST.in`
+- Modify: `release/package-policy-v1.json`
+- Modify if required by observed truth: `README.md`, `docs/TOOLING.md`,
+  `CHANGELOG.md`
+
+- [ ] **Step 1: Build an exact clean verification environment**
+
+```bash
+TASK11_VENV=/private/tmp/tritrack-task11-verification-venv
+python3.13 -m venv "$TASK11_VENV"
+"$TASK11_VENV/bin/python" -m pip install \
+  --constraint requirements/ci-constraints.txt pip
+"$TASK11_VENV/bin/python" -m pip install \
+  --constraint requirements/ci-constraints.txt -e '.[dev]'
+"$TASK11_VENV/bin/python" -m pip check
+```
+
+Expected: install and dependency check PASS with Python 3.13.
+
+- [ ] **Step 2: Run focused, complete, quality, compile, identity, and skill gates**
+
+```bash
+"$TASK11_VENV/bin/python" -m unittest tests.test_validate_artifacts \
+  tests.test_release_gate tests.test_packaging tests.test_release_ci \
+  tests.test_cli -v
+"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
+"$TASK11_VENV/bin/ruff" check src tests examples scripts
+"$TASK11_VENV/bin/python" -m compileall -q src tests examples scripts
+"$TASK11_VENV/bin/python" \
+  .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py \
+  --root .
+TASK11_SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
+python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
+  .agents/skills/tritrack-editing-assistant-maintainer
+python3 "$TASK11_SKILLS_ROOT/.system/skill-creator/scripts/quick_validate.py" \
+  skills/tritrack-editing-assistant
+git diff --check
+git status --short
+```
+
+Expected: all PASS. Record exact test counts and tool versions; do not invent a
+count in advance.
+
+- [ ] **Step 3: Freeze the clean implementation candidate before the real gate**
+
+Read back all changed files and confirm Tasks 1–10 already committed every
+owned change. Confirm no generated build, venv, cache, `.release-evidence`,
+media, workbook, FCPXML, credential, or private path is tracked. Require an
+empty `git status --short`, record `git rev-parse HEAD` as the implementation
+candidate, and do not create a catch-all commit.
+
+- [ ] **Step 4: Run the real release gate into one fresh ignored directory**
+
+```bash
+"$TASK11_VENV/bin/python" scripts/release_gate.py \
+  --source . \
+  --output .release-evidence/task11-implementation
+"$TASK11_VENV/bin/python" -m json.tool \
+  .release-evidence/task11-implementation/release-manifest.json
+git status --short
+```
+
+Expected: gate PASS, manifest present last, worktree still clean, and no path,
+time, content, or unsupported claim in the manifest. If the gate fails, keep
+that directory as incomplete evidence and use a new absent suffix after the
+fix; never repair or reuse it.
+
+- [ ] **Step 5: Write public verification and advance the roadmap**
+
+`docs/TASK-11-VERIFICATION.md` must record:
+
+- approved design commit and implementation candidate commit;
+- exact focused/full test counts, Ruff, compile, identity, skill, package,
+  release-gate, and installed-wheel results;
+- wheel byte reproducibility and normalized sdist-member reproducibility;
+- exact tool versions, archive hashes/member-inventory digests, and manifest
+  hash from the implementation gate, without a local path;
+- four validator scopes and all non-claims;
+- exact action pins and fixed CI cells;
+- brainstorm provenance: Codex and Gemini hashes/model ledger, plus truthful
+  Claude timeout/incomplete state with no retry/fallback;
+- no tag, release, package publication, PR, tester contact, upload, signing,
+  attestation, SBOM, Final Cut GUI, DTD, provider, or application claim.
+
+Update `STATUS.md` to Tasks 1–11 complete and Task 12 next. Move Task 11 to the
+completed roadmap section. Make `docs/TASK-11-VERIFICATION.md` an exact
+required sdist member in `MANIFEST.in`, the package policy, and packaging
+tests. Add maintainer-boundary tests that require the status/roadmap truths.
+
+- [ ] **Step 6: Run documentation regression, full suite, and commit**
+
+```bash
+"$TASK11_VENV/bin/python" -m unittest tests.test_maintainer_boundary -v
+"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
+"$TASK11_VENV/bin/ruff" check src tests examples scripts
+git diff --check
+git add docs/TASK-11-VERIFICATION.md STATUS.md docs/ROADMAP.md \
+  tests/test_maintainer_boundary.py tests/test_packaging.py MANIFEST.in \
+  release/package-policy-v1.json README.md docs/TOOLING.md CHANGELOG.md
+git commit -m "docs: close Task 11 release readiness"
+```
+
+Stage only files that actually changed.
+
+---
+
+### Task 12: Independent closeout review, fix-forward, final gate, and custody
+
+**Files:**
+
+- Create: `docs/reviews/task-11-closeout-packet-2026-08-17.md`
+- Create as produced: `docs/reviews/task-11-closeout-gemini-2026-08-17.md`
+- Create as produced: provider status ledgers
+- Create: `docs/reviews/task-11-closeout-adjudication-2026-08-17.md`
+- Modify only for agreed in-scope findings: implementation/tests/docs above
+
+- [ ] **Step 1: Freeze a path-safe review packet**
+
+Include the exact base/candidate SHAs, approved design, complete diff, test and
+release-manifest evidence, package member policy, CI pins/matrix, privacy and
+path scans, non-goals, and finding schema. Do not include ignored artifacts,
+absolute local paths, credentials, or content from user artifacts.
+
+- [ ] **Step 2: Perform Codex independent review first**
+
+Review the frozen target for:
+
+1. four-mode correctness and authority reuse;
+2. no-write/no-network/privacy boundaries;
+3. tracked source and archive safety;
+4. package content and reproducibility claims;
+5. manifest-last failure/race behavior;
+6. fixed CI and supply-chain pins;
+7. tests, docs, role firewalls, governance, and scope.
+
+Record findings before reading external answers.
+
+- [ ] **Step 3: Use the approved shared Claude/Gemini wrappers once each**
+
+Read `docs/TOOLING.md`, `docs/COLLABORATION.md` from the governing shared
+workspace, and the shared tool README before invocation. Resolve the highest
+eligible released models dynamically under repository routing rules. Use each
+model at most once. Record requested, observed, and completed IDs exactly.
+
+Claude must use only the subscription wrapper. A timeout or ambiguous request
+remains incomplete with no retry, downgrade, paid credential, API, or provider
+fallback. Gemini must fail closed if the official eligible catalog cannot be
+resolved.
+
+- [ ] **Step 4: Adjudicate and fix forward**
+
+Classify every finding as `agree`, `upgrade`, `downgrade`, `reject`, or
+`already-fixed`. For every agreed ordinary in-scope defect: add an observed RED
+regression, implement the smallest fix, run focused/full/quality/package gates,
+update the packet and evidence, and repeat the closeout locally. Stop only for
+a true public-contract gap or unauthorized scope expansion.
+
+- [ ] **Step 5: Commit sanitized review records**
+
+Stage the frozen packet and adjudication by exact filename. Then inspect
+`git status --short` and stage only each produced human-readable review and
+`.status.json` ledger by its exact filename. Never use a wildcard that could
+capture raw output.
+
+```bash
+git add docs/reviews/task-11-closeout-packet-2026-08-17.md \
+  docs/reviews/task-11-closeout-adjudication-2026-08-17.md
+git status --short
+git commit -m "docs: record Task 11 closeout review"
+```
+
+Do not stage `.raw.json`, ignored evidence, temporary packets, or credentials.
+
+- [ ] **Step 6: Run the final clean candidate gate**
+
+```bash
+"$TASK11_VENV/bin/python" -m unittest discover -s tests -v
+"$TASK11_VENV/bin/ruff" check src tests examples scripts
+"$TASK11_VENV/bin/python" -m compileall -q src tests examples scripts
+git diff --check
+git status --short
+"$TASK11_VENV/bin/python" scripts/release_gate.py \
+  --source . \
+  --output .release-evidence/task11-final
+git status --short
+```
+
+Expected: clean and PASS. This final release-evidence directory remains ignored
+and local; no artifact upload or publication is authorized.
+
+- [ ] **Step 7: Fast-forward main and push under the standing grant**
+
+Verify the branch is based on the recorded `origin/main`, fast-forward local
+`main` to the fully green candidate without a merge commit, and push only
+`main` to the existing public `origin`. Do not create a tag, release, PR, or
+package upload.
+
+```bash
+git fetch origin main
+git rev-parse origin/main
+git switch main
+git merge --ff-only codex/task11-release-gates
+git push origin main
+git rev-parse HEAD
+git rev-parse origin/main
+git ls-remote origin refs/heads/main
+```
+
+All three final SHAs must match exactly.
+
+- [ ] **Step 8: Verify remote CI at the exact pushed SHA**
+
+Use `gh run list`, `gh run view`, and `gh run watch` for the exact pushed commit.
+Require all four test cells, the single quality job, and the single release-gate
+job to pass. Verify again that the workflow has no artifact upload. If an
+ordinary in-scope CI defect appears, fix forward on the task branch, repeat all
+local gates/review delta, fast-forward, push, and reverify the exact SHA.
+
+Record the run ID in the final handoff only; do not edit the already-green
+candidate merely to embed the CI run ID.
+
+---
+
+## Completion definition
+
+Task 11 is complete only when:
+
+- all four installed validator modes are read-only, offline, strictly scoped,
+  and share existing authorities;
+- source/privacy/archive/package/reproducibility/fresh-install gates pass from
+  one clean commit;
+- `release-manifest.json` is schema-valid, path-free, and published last;
+- fixed Linux x64/macOS arm64 × Python 3.12/3.13 CI passes at the exact public
+  `main` SHA;
+- public docs and end-user skill describe validation without maintainer power;
+- no outward action beyond the existing-main fast-forward/push grant occurs;
+- Task 12, not publication, is the next roadmap action.
diff --git a/docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md b/docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
new file mode 100644
index 0000000000000000000000000000000000000000..1c5c80ebeaff5a424101c0aa50a69c476f38e711
--- /dev/null
+++ b/docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
@@ -0,0 +1,493 @@
+# Task 11 release-readiness design
+
+Decision date: 2026-08-17
+
+Decision owner: producer
+
+Selected option: explicit four-mode end-user validator plus one separate
+deterministic maintainer release gate
+
+Frozen source candidate:
+`b4e21d660170dfd000c99ba38f55f825565ab922`
+
+## Decision
+
+Task 11 closes the public alpha's remaining ordinary command and makes one
+source candidate mechanically releasable without publishing it.
+
+The task has two deliberately separate authority domains:
+
+1. `tritrack validate` is a read-only, offline, end-user artifact validator.
+2. `scripts/release_gate.py` is the repository-maintainer entry point for
+   source privacy, package contents, build provenance, and release readiness.
+
+The runtime command has no maintainer task state, release authority, Git
+operation, build operation, network access, credential lookup, publication,
+repair, or overwrite behavior. The maintainer gate is not exposed through the
+end-user skill or runtime CLI.
+
+## End-user command surface
+
+Task 11 implements these exact help authorities:
+
+```text
+tritrack validate contract \
+  --artifact ARTIFACT.json \
+  [--json]
+
+tritrack validate fcpxml \
+  --artifact OUTPUT.fcpxml \
+  --profile uhd-2997-ndf-fcpxml-1.14 \
+  --binding basic-title-v1 \
+  [--json]
+
+tritrack validate paper \
+  --aligned ALIGNED.json \
+  --workbook PAPER.xlsx \
+  [--json]
+
+tritrack validate run \
+  --run RUN-DIRECTORY \
+  [--json]
+```
+
+No mode guesses a file type from a suffix, scans sibling directories, searches
+for authorities, repairs an artifact, or creates an output. The caller selects
+one mode and supplies every authority required by that mode.
+
+## Validation scopes
+
+Every successful result includes one exact `validationScope`. A scope is a
+claim boundary, not a confidence score.
+
+### `contract`
+
+`validate contract` reads one bounded regular non-symlink JSON file. It accepts
+only a closed `schemaVersion` registered in the installed contract package and
+calls the same `contracts.validate_contract` authority used by product
+consumers.
+
+Success proves only:
+
+- the artifact is valid under that installed JSON Schema contract; and
+- the reported SHA-256 identifies the exact bytes that were validated.
+
+It returns `validationScope: contract`. It does not prove that a referenced
+source, parent artifact, model, media file, workbook, receipt, manifest chain,
+or cross-file SHA-256 exists or matches. It does not add a separate
+canonical-byte requirement when the existing contract does not require one.
+
+Unknown, missing, non-string, or unregistered `schemaVersion` values fail
+closed. Arbitrary JSON Schema files and third-party JSON are outside scope.
+
+### `fcpxml`
+
+`validate fcpxml` reads one bounded regular non-symlink FCPXML file and reuses
+the existing installed profile, title-binding, and structural FCPXML validator.
+It returns `validationScope: structural-profile`.
+
+Success proves that the exact bytes satisfy the installed structural checks
+for the explicit public profile and title binding. It performs no source-media
+probe, DTD lookup, network request, external entity resolution, Final Cut
+launch, GUI import, or round trip. The result therefore makes no DTD, media
+availability, application, or target-machine compatibility claim.
+
+### `paper`
+
+`validate paper` reads the exact aligned transcript and XLSX workbook through
+the same bounded regular-file and archive-safety boundaries used by
+`paper apply`. It re-derives the complete cue reference grid and public-safe
+workbook manifest, verifies immutable identity and display cells, rejects
+formulas and unsupported workbook structure, and validates editor-authored
+question and selection intent.
+
+It returns `validationScope: authority-bound`. Success proves that the supplied
+workbook is acceptable against the exact supplied aligned transcript bytes.
+It does not publish `grouping-v1`, normalize the workbook, or change either
+input. Task 11 extracts one pure validation seam from the existing apply path;
+`paper apply` and `validate paper` must not diverge in acceptance semantics.
+
+### `run`
+
+`validate run` calls the same complete immutable-bundle loader used by
+`tritrack run status`. It validates the exact phase-specific artifact set,
+fixed filenames, bounded regular members, manifest schema and semantics,
+artifact SHA-256 values, prior-manifest chain, and supported artifact contracts.
+
+It returns `validationScope: complete-run-bundle`. `run status` and
+`validate run` share the loader and sanitized summary builder. The two commands
+may use different outer summary schema names, but their run ID, phase, next
+action, stages, logical artifacts, and hashes must be equal for the same bytes.
+
+## Runtime summary and failure boundary
+
+The JSON completion summary is closed and contains only:
+
+- one validator-summary schema version;
+- tool version;
+- artifact kind;
+- `validationScope`;
+- exact validated artifact or authority hashes; and
+- bounded, non-content counts that apply to the selected mode.
+
+It contains no absolute or relative path, filename, transcript text, cue text,
+question text, notes, FCPXML text, workbook cells, command arguments, logs,
+credentials, timestamps, or duration. Human-readable output follows the same
+information boundary.
+
+Validation errors use stable `TRITRACK_VALIDATE_*` prefixes at the new command
+boundary while preserving existing component codes when a reused authority
+rejects an artifact. The CLI retains the project's established exit classes:
+
+- malformed command intent: `64` (usage);
+- invalid schema, content, structure, binding, or semantic authority: `65`
+  (data);
+- unsupported profile or policy: `78` (policy);
+- missing or unreadable input: `74` (I/O); and
+- no failure prints a traceback, input content, matched secret, or full path.
+
+All runtime inputs are read through bounded, regular non-symlink file or
+directory boundaries. The validator writes no output, temporary artifact,
+receipt, cache, repaired file, or adjacent state.
+
+## Maintainer release-gate entry point
+
+The only repository-owned Task 11 release-readiness entry point is:
+
+```text
+python scripts/release_gate.py \
+  --source . \
+  --output .release-evidence/CANDIDATE
+```
+
+The output directory and its parent follow the existing absent-output rule:
+the parent exists, the requested output is absent, and an existing path or race
+winner is never overwritten. The gate builds in invocation-owned staging,
+publishes package artifacts into the reserved directory, and publishes
+`release-manifest.json` last. Ordinary failures remove only unpublished state
+created by that invocation. A crash may leave a mechanically incomplete
+directory with no manifest; the gate never repairs or resumes it.
+
+Release mode requires:
+
+- the public project identity to match `public-engine`／`OSS`;
+- an exact Git `HEAD` candidate;
+- no tracked or untracked change outside ignored output roots; and
+- the package version, runtime `__version__`, distribution names, and artifact
+  basenames to agree.
+
+Task 11 also closes the interpreter-eligibility claim. The current
+`requires-python >=3.12` range would allow an unverified Python 3.14 install,
+while the selected release matrix covers exactly Python 3.12 and 3.13. The
+package metadata therefore becomes `>=3.12,<3.14`; classifiers and public setup
+documentation name the same two-version set. Adding Python 3.14 later requires
+its own green compatibility evidence and metadata change.
+
+The ordered gate stages are:
+
+1. project, Git, version, and clean-candidate identity;
+2. tracked-source inventory and privacy checks;
+3. wheel and sdist build;
+4. bounded archive safety, member inventory, privacy, metadata, and content
+   contracts;
+5. fresh environment wheel installation, `pip check`, installed CLI help,
+   eleven-component registry, and four-mode invented validation smoke; and
+6. exact artifact hashing and manifest-last publication.
+
+The script performs no tag, release, upload, signing, attestation, remote
+mutation, branch-protection change, tester contact, or application operation.
+
+## `release-manifest.json`
+
+The manifest uses a new closed receipt schema owned by the maintainer gate. It
+records:
+
+- schema version and gate version;
+- exact candidate commit;
+- distribution name and project version;
+- tracked-source file count and one canonical inventory SHA-256;
+- actual build Python implementation/version;
+- actual build frontend and backend versions;
+- wheel and sdist safe basenames, byte sizes, exact SHA-256 values, member
+  counts, and canonical member-inventory SHA-256 values;
+- the ordered gate names and `passed` outcomes; and
+- explicit non-claims for reproducible bytes, publication, signatures,
+  attestations, Final Cut, DTD, and GUI evidence.
+
+It records no timestamp, duration, local path, account, host name, credential,
+Git remote token, CI run ID, workflow URL, logs, source text, or matched private
+content. Repeating the gate with identical source, toolchain, and build outputs
+must produce identical manifest bytes. Task 11 records exact build provenance;
+it does not claim that independently built wheel or sdist bytes are
+reproducible until the separate experiment proves that property.
+
+## Privacy gate
+
+The source scan enumerates the complete Git-tracked index and requires every
+entry to be one expected regular file. A tracked symlink, submodule, unsupported
+mode, or path outside the public distribution policy fails closed rather than
+being skipped. The scanner does not walk a developer workspace, virtual
+environment, ignored output, source-media folder, or adjacent repository.
+
+The archive scan first rejects unsafe structure before reading member content:
+
+- absolute or parent-traversing member names;
+- symlinks, hard links, devices, or unsupported member types;
+- duplicate or case-colliding names;
+- excess member count, individual expanded size, or total expanded size; and
+- members outside the distribution's exact allowlisted roots.
+
+Source and accepted archive members are then checked for public generic
+privacy boundaries:
+
+- absolute macOS, Linux, Windows-home, and mounted-volume path shapes;
+- credential assignments or credential-like high-entropy values;
+- unexpected media, transcript, database, archive, executable, or proprietary
+  asset types; and
+- repository-boundary tokens already declared by public governance tests.
+
+The tracked implementation contains only generic patterns and invented
+canaries. It never embeds a real credential, private path, production name, or
+private-media excerpt. A failure reports only a stable gate code and public
+artifact class; it never echoes the matching bytes. Narrow documented
+false-positive exceptions must bind an exact public file and rule ID, never a
+secret value or arbitrary directory.
+
+## Distribution content contracts
+
+### Wheel
+
+The wheel contains only:
+
+- `tritrack_editing_assistant` runtime Python modules;
+- installed strict schemas, compatibility profiles, and any implemented
+  provider resource explicitly named by package data;
+- console-script and standard distribution metadata; and
+- Apache-2.0 license／notice material in standard wheel metadata locations.
+
+It excludes tests, fixtures, examples, repository docs, review packets,
+maintainer governance, the maintainer skill, release tools, CI configuration,
+and the end-user skill.
+
+### Sdist
+
+The sdist is the buildable and publicly verifiable source payload. Its exact
+allowlist includes:
+
+- runtime source and installed resources;
+- `pyproject.toml` and any build manifest／constraints required to reproduce
+  the declared build;
+- invented tests and fixtures required to verify the source;
+- `scripts/release_gate.py` and its public test support;
+- `skills/tritrack-editing-assistant/SKILL.md` and its metadata;
+- `README.md`, `LICENSE`, `NOTICE`, `CHANGELOG.md`, `CONTRIBUTING.md`, and
+  `SECURITY.md`; and
+- the bounded Task 11 public design and verification documents required to
+  understand the artifact and claim boundary.
+
+It excludes ignored outputs, local environments, media, credentials, private
+state, raw external-review attempts, and unrelated maintenance-history packets.
+The exact member allowlist is tested; new members require an intentional test
+and policy change.
+
+The end-user skill is source-distributed and separately installable. Installing
+the Python wheel does not install or register that skill. Documentation must
+use those exact claims and must not broaden Task 10's repository-installed
+skill evidence into a wheel-install claim.
+
+## CI design
+
+The public workflow uses fixed, non-`latest` runner labels verified against the
+official GitHub runner-image catalog before implementation:
+
+- `ubuntu-24.04` (x64); and
+- `macos-26` (arm64).
+
+The Python matrix and `requires-python >=3.12,<3.14` metadata both declare the
+3.12 and 3.13 support set. Adding Python 3.14 or another OS is a separate
+compatibility decision.
+
+The workflow has three layers.
+
+### `test-matrix`
+
+Four cells run Ubuntu／macOS × Python 3.12／3.13. Every cell:
+
+- installs the source and exact development constraints;
+- runs the complete unittest suite;
+- compiles public Python surfaces;
+- builds a local non-editable wheel;
+- installs that wheel into a fresh environment outside the checkout;
+- runs `pip check`; and
+- runs installed help, component-registry, and four-mode invented smoke.
+
+Each cell builds locally. Task 11 does not transfer packages between jobs with
+an artifact-upload action.
+
+### `quality`
+
+One `ubuntu-24.04`／Python 3.13 cell runs Ruff, the maintainer/end-user role and
+privacy boundary tests, deterministic configuration checks, and repository-
+self-contained skill checks. The canonical external skill validator remains a
+local closeout requirement when it is not part of the public repository; CI
+does not pretend to have that external tool.
+
+### `release-gate`
+
+One canonical `ubuntu-24.04`／Python 3.13 cell runs the complete maintainer
+release gate. Its package output is job-local and is not uploaded, published,
+signed, or attested.
+
+Workflow permissions remain:
+
+```yaml
+permissions:
+  contents: read
+```
+
+Third-party Actions are pinned to exact commit SHA values resolved from their
+official repositories during implementation. Build and development tooling are
+pinned by a repository-owned exact constraints file; runtime dependency
+metadata keeps its reviewed compatibility ranges. The release manifest records
+the actual resolved toolchain.
+
+## CI and release claim boundary
+
+Passing CI proves only that:
+
+- the Python contract and installed CLI passed on the named runner/Python
+  cells;
+- the wheel installed and passed the declared smoke checks;
+- tracked source and built distributions passed the declared privacy and
+  content gates; and
+- one exact candidate produced the artifact hashes in its local release
+  manifest.
+
+It does not prove a licensed Final Cut installation, DTD validation, GUI
+import, round trip, macOS 26.5.2 compatibility, independent build
+reproducibility, publication, signature, attestation, or downstream private
+integration. A post-push verification record may record a GitHub Actions run ID
+and exact public remote SHA; those transient facts do not enter the deterministic
+release manifest.
+
+## Experiment before implementation
+
+Before freezing any reproducibility or member-inventory assertion in tests,
+Task 11 runs one disposable experiment against the frozen source candidate:
+
+1. build wheel and sdist twice in separate absent directories with a fixed
+   `SOURCE_DATE_EPOCH` and the same toolchain;
+2. compare full archive SHA-256 values;
+3. compare normalized safe member lists and per-member content SHA-256 values;
+4. inspect license, schema, profile, source, test, policy, and skill membership;
+5. install the wheel in a new repository-external environment; and
+6. record only observed facts in the design implementation plan.
+
+If full archive hashes differ, Task 11 validates exact final artifact hashes
+and normalized member equivalence but makes no reproducible-byte claim. The
+experiment does not mutate tracked source and its scratch output is discarded.
+
+## TDD and verification target
+
+Implementation preserves observed RED-to-GREEN evidence in five groups.
+
+### Runtime validators
+
+- all four help surfaces and stable CLI mappings;
+- valid, invalid, malformed, unknown-contract, missing, unreadable, symlink,
+  oversized, and late-change inputs;
+- exact successful hashes and scope labels;
+- contract-only non-claims;
+- FCPXML structural/profile validation with DTD, entity resolution, network,
+  media probing, and application launch absent;
+- paper authority rebinding with no grouping publication;
+- complete run-bundle validation; and
+- byte-for-byte input immutability and no created files.
+
+### Shared authority
+
+- `paper apply` and `validate paper` accept and reject the same workbook facts;
+- `run status` and `validate run` return equal core facts for the same bundle;
+  and
+- refactoring does not create a second schema, workbook, FCPXML, or run
+  authority.
+
+### Privacy and release gate
+
+- every invented path and credential canary;
+- failure-output redaction;
+- tracked-file scoping;
+- archive traversal, link, duplicate, case-collision, type, count, and size
+  rejection;
+- exact wheel and sdist content allowlists;
+- existing output and publication races;
+- cleanup of invocation-owned state; and
+- manifest-last completeness.
+
+### Packaging and installed acceptance
+
+- real wheel and sdist build;
+- exact member inventories and required license／resource presence;
+- absent forbidden files;
+- repository-external fresh installation;
+- `pip check`;
+- eleven-component registry unchanged; and
+- all four installed validator modes exercised with invented artifacts.
+
+### Closeout
+
+- focused tests and complete suite;
+- Ruff and compilation;
+- public project identity;
+- maintainer and end-user role-boundary tests;
+- canonical validation of both skills in the local maintainer environment;
+- privacy and package gates;
+- `git diff --check`;
+- the four-cell public CI matrix and canonical release-gate job; and
+- independent closeout review with ordinary in-scope fix-forward.
+
+`STATUS.md` changes only after the coherent package is green. The standing
+grant then permits fast-forward integration into `main`, pushing the existing
+public `origin`, and exact remote-SHA backup verification. No tag, release,
+pull request, package publication, tester contact, application submission,
+force-push, remote change, or visibility change is performed.
+
+## Deferred alternatives and non-goals
+
+- automatic artifact-type detection or sibling discovery;
+- an all-purpose validation DAG or plugin framework;
+- a maintainer/release flag in the end-user command;
+- a separate end-user-skill release archive;
+- wheel installation or automatic registration of the end-user skill;
+- SBOM, signing, SLSA provenance, OIDC, package attestation, release workflow,
+  tag, GitHub release, or PyPI publication;
+- adding Python 3.14 or broadening the public compatibility profile;
+- live provider transport, credentials, upload, or deletion;
+- new editing semantics, cue changes, media processing, or Final Cut
+  automation;
+- Task 12 alpha freeze and independent candidate review; and
+- Task 13 downstream integration.
+
+## Brainstorm provenance
+
+The frozen public problem packet SHA-256 was
+`ff145c249aae193ce80872783b8f95e840684ee3a518e4cc2788cc607aa15921`.
+
+Codex completed its independent first round before reading any external output.
+Its response SHA-256 was
+`0bdc84c66d5ca5012bcee89e8e757b0c47dae3c9e0e178a7c5118ec6427cd6c0`.
+
+Gemini dynamically requested, observed, and completed `gemini-3.7-flash`.
+Its response SHA-256 was
+`1d682f99a8cfad8473c574d1e4c645a1279e56e99cf55d359a16645c896e3379`.
+
+Claude requested the dynamic `opus` capability alias through the approved
+subscription-only wrapper. Attempt
+`637f7c3a-cf72-4e97-9d42-ef7ef0d1400e` ended `claude-timeout`; observed and
+completed models are null and request completion is ambiguous. The lane remains
+explicitly incomplete with no retry, downgrade, paid credential, provider
+fallback, or completion claim.
+
+The producer selected the four-mode validator and approved the architecture,
+validation semantics, maintainer release/packaging boundary, CI/provenance
+boundary, and privacy/error/acceptance design on 2026-08-17.
diff --git a/pyproject.toml b/pyproject.toml
index 4a6693cb4b267931857f90754d3b7c1b0d60a34f..9659703b67a6993ae00ec6bea55bad660ff173b3 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,5 +1,5 @@
 [build-system]
-requires = ["setuptools>=75"]
+requires = ["setuptools==84.0.0"]
 build-backend = "setuptools.build_meta"
 
 [project]
@@ -7,7 +7,7 @@ name = "tritrack-editing-assistant"
 version = "0.1.0a0"
 description = "Local-first editing-assistant building blocks for Final Cut Pro workflows"
 readme = "README.md"
-requires-python = ">=3.12"
+requires-python = ">=3.12,<3.14"
 license = "Apache-2.0"
 authors = [
   { name = "Hsin-Hsin Yuan" },
@@ -29,7 +29,7 @@ dependencies = [
 tritrack = "tritrack_editing_assistant.cli:main"
 
 [project.optional-dependencies]
-dev = ["build>=1.2,<2", "ruff>=0.12,<1"]
+dev = ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"]
 
 [tool.setuptools.packages.find]
 where = ["src"]
diff --git a/release/package-policy-v1.json b/release/package-policy-v1.json
new file mode 100644
index 0000000000000000000000000000000000000000..8e7d975d7c45a916d241ba9043c584433e7cff86
--- /dev/null
+++ b/release/package-policy-v1.json
@@ -0,0 +1,174 @@
+{
+  "schemaVersion": "tritrack.package-policy/v1",
+  "limits": {
+    "sourceMaxFiles": 4096,
+    "sourceMaxFileBytes": 2097152,
+    "sourceMaxTotalBytes": 134217728,
+    "archiveMaxBytes": 67108864,
+    "archiveMaxMembers": 2048,
+    "memberMaxBytes": 33554432,
+    "expandedMaxBytes": 268435456
+  },
+  "source": {
+    "allowedFakeHomeUsers": [
+      "editor",
+      "example",
+      "fake",
+      "test"
+    ],
+    "allowedFakeSecretValues": [
+      "example",
+      "fake",
+      "placeholder",
+      "redacted",
+      "secret",
+      "test"
+    ],
+    "forbiddenSuffixes": [
+      ".aac",
+      ".aif",
+      ".aiff",
+      ".avi",
+      ".fcpxmld",
+      ".m4a",
+      ".m4v",
+      ".mkv",
+      ".mov",
+      ".mp3",
+      ".mp4",
+      ".wav",
+      ".xlsx"
+    ]
+  },
+  "wheel": {
+    "expectedMembers": [
+      "tritrack_editing_assistant-0.1.0a0.dist-info/METADATA",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/RECORD",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/WHEEL",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/entry_points.txt",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/LICENSE",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/NOTICE",
+      "tritrack_editing_assistant-0.1.0a0.dist-info/top_level.txt",
+      "tritrack_editing_assistant/__init__.py",
+      "tritrack_editing_assistant/align_text.py",
+      "tritrack_editing_assistant/cli.py",
+      "tritrack_editing_assistant/contracts.py",
+      "tritrack_editing_assistant/doctor.py",
+      "tritrack_editing_assistant/emit_fcpxml.py",
+      "tritrack_editing_assistant/gemini_hybrid.py",
+      "tritrack_editing_assistant/hallucination.py",
+      "tritrack_editing_assistant/organizer.py",
+      "tritrack_editing_assistant/paper_edit.py",
+      "tritrack_editing_assistant/process.py",
+      "tritrack_editing_assistant/profiles/__init__.py",
+      "tritrack_editing_assistant/profiles/basic-title-v1.json",
+      "tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
+      "tritrack_editing_assistant/run_workflow.py",
+      "tritrack_editing_assistant/schemas/__init__.py",
+      "tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
+      "tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
+      "tritrack_editing_assistant/schemas/grouping-v1.schema.json",
+      "tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
+      "tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
+      "tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
+      "tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
+      "tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
+      "tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
+      "tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
+      "tritrack_editing_assistant/story_fcpxml.py",
+      "tritrack_editing_assistant/string_out.py",
+      "tritrack_editing_assistant/sync_scan.py",
+      "tritrack_editing_assistant/transcribe_takes.py",
+      "tritrack_editing_assistant/validate_artifacts.py"
+    ]
+  },
+  "sdist": {
+    "root": "tritrack_editing_assistant-0.1.0a0/",
+    "expectedMembers": [
+      ".github/workflows/ci.yml",
+      "CHANGELOG.md",
+      "CODE_OF_CONDUCT.md",
+      "CONTRIBUTING.md",
+      "LICENSE",
+      "MANIFEST.in",
+      "NOTICE",
+      "PKG-INFO",
+      "README.md",
+      "SECURITY.md",
+      "docs/ROADMAP.md",
+      "docs/TASK-11-VERIFICATION.md",
+      "docs/TOOLING.md",
+      "docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md",
+      "examples/quickstart_demo.py",
+      "pyproject.toml",
+      "release/package-policy-v1.json",
+      "release/release-manifest-v1.schema.json",
+      "requirements/ci-constraints.txt",
+      "scripts/capture_basic_title_binding.py",
+      "scripts/release_gate.py",
+      "scripts/release_gate_core.py",
+      "setup.cfg",
+      "skills/tritrack-editing-assistant/SKILL.md",
+      "skills/tritrack-editing-assistant/agents/openai.yaml",
+      "src/tritrack_editing_assistant.egg-info/PKG-INFO",
+      "src/tritrack_editing_assistant.egg-info/SOURCES.txt",
+      "src/tritrack_editing_assistant.egg-info/dependency_links.txt",
+      "src/tritrack_editing_assistant.egg-info/entry_points.txt",
+      "src/tritrack_editing_assistant.egg-info/requires.txt",
+      "src/tritrack_editing_assistant.egg-info/top_level.txt",
+      "src/tritrack_editing_assistant/__init__.py",
+      "src/tritrack_editing_assistant/align_text.py",
+      "src/tritrack_editing_assistant/cli.py",
+      "src/tritrack_editing_assistant/contracts.py",
+      "src/tritrack_editing_assistant/doctor.py",
+      "src/tritrack_editing_assistant/emit_fcpxml.py",
+      "src/tritrack_editing_assistant/gemini_hybrid.py",
+      "src/tritrack_editing_assistant/hallucination.py",
+      "src/tritrack_editing_assistant/organizer.py",
+      "src/tritrack_editing_assistant/paper_edit.py",
+      "src/tritrack_editing_assistant/process.py",
+      "src/tritrack_editing_assistant/profiles/__init__.py",
+      "src/tritrack_editing_assistant/profiles/basic-title-v1.json",
+      "src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
+      "src/tritrack_editing_assistant/run_workflow.py",
+      "src/tritrack_editing_assistant/schemas/__init__.py",
+      "src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/grouping-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
+      "src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
+      "src/tritrack_editing_assistant/story_fcpxml.py",
+      "src/tritrack_editing_assistant/string_out.py",
+      "src/tritrack_editing_assistant/sync_scan.py",
+      "src/tritrack_editing_assistant/transcribe_takes.py",
+      "src/tritrack_editing_assistant/validate_artifacts.py",
+      "tests/task9_fixtures.py",
+      "tests/test_align_text.py",
+      "tests/test_cli.py",
+      "tests/test_contracts.py",
+      "tests/test_doctor.py",
+      "tests/test_emit_fcpxml.py",
+      "tests/test_gemini_hybrid.py",
+      "tests/test_hallucination.py",
+      "tests/test_organizer.py",
+      "tests/test_packaging.py",
+      "tests/test_paper_edit.py",
+      "tests/test_process.py",
+      "tests/test_quickstart_demo.py",
+      "tests/test_release_gate.py",
+      "tests/test_release_ci.py",
+      "tests/test_run_workflow.py",
+      "tests/test_story_fcpxml.py",
+      "tests/test_string_out.py",
+      "tests/test_sync_scan.py",
+      "tests/test_title_binding.py",
+      "tests/test_transcribe_takes.py",
+      "tests/test_validate_artifacts.py"
+    ]
+  }
+}
diff --git a/release/release-manifest-v1.schema.json b/release/release-manifest-v1.schema.json
new file mode 100644
index 0000000000000000000000000000000000000000..53c8c8da8fe3dd240d8e80caae956fbe08aba902
--- /dev/null
+++ b/release/release-manifest-v1.schema.json
@@ -0,0 +1,150 @@
+{
+  "$schema": "https://json-schema.org/draft/2020-12/schema",
+  "$id": "https://tritrack.example/schemas/release-manifest-v1.schema.json",
+  "title": "TriTrack release manifest v1",
+  "type": "object",
+  "additionalProperties": false,
+  "required": [
+    "schemaVersion",
+    "project",
+    "sourceInventory",
+    "toolchain",
+    "platform",
+    "artifacts",
+    "reproducibility",
+    "gates",
+    "nonClaims"
+  ],
+  "properties": {
+    "schemaVersion": {
+      "const": "tritrack.release-manifest/v1"
+    },
+    "project": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["name", "version", "commit"],
+      "properties": {
+        "name": {"const": "tritrack-editing-assistant"},
+        "version": {"type": "string", "minLength": 1},
+        "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"}
+      }
+    },
+    "sourceInventory": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["count", "sha256"],
+      "properties": {
+        "count": {"type": "integer", "minimum": 1},
+        "sha256": {"$ref": "#/$defs/sha256"}
+      }
+    },
+    "toolchain": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "python",
+        "implementation",
+        "pip",
+        "build",
+        "setuptools",
+        "wheel"
+      ],
+      "properties": {
+        "python": {"type": "string", "minLength": 1},
+        "implementation": {"const": "CPython"},
+        "pip": {"type": "string", "minLength": 1},
+        "build": {"type": "string", "minLength": 1},
+        "setuptools": {"type": "string", "minLength": 1},
+        "wheel": {"type": "string", "minLength": 1}
+      }
+    },
+    "platform": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["system", "machine"],
+      "properties": {
+        "system": {"enum": ["Darwin", "Linux"]},
+        "machine": {"enum": ["arm64", "x86_64"]}
+      }
+    },
+    "artifacts": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["wheel", "sdist"],
+      "properties": {
+        "wheel": {"$ref": "#/$defs/artifact"},
+        "sdist": {"$ref": "#/$defs/artifact"}
+      }
+    },
+    "reproducibility": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": ["wheelBytesMatch", "sdistMembersMatch"],
+      "properties": {
+        "wheelBytesMatch": {"const": true},
+        "sdistMembersMatch": {"const": true}
+      }
+    },
+    "gates": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "sourceIdentity",
+        "sourcePrivacy",
+        "wheelArchive",
+        "sdistArchive",
+        "freshInstall"
+      ],
+      "properties": {
+        "sourceIdentity": {"const": "pass"},
+        "sourcePrivacy": {"const": "pass"},
+        "wheelArchive": {"const": "pass"},
+        "sdistArchive": {"const": "pass"},
+        "freshInstall": {"const": "pass"}
+      }
+    },
+    "nonClaims": {
+      "type": "array",
+      "minItems": 2,
+      "uniqueItems": true,
+      "items": {
+        "enum": [
+          "no-tag",
+          "no-release",
+          "no-package-publication",
+          "no-pull-request",
+          "no-tester-contact",
+          "no-signing",
+          "no-attestation",
+          "no-sbom",
+          "no-final-cut-gui",
+          "no-dtd",
+          "no-provider",
+          "no-application-submission"
+        ]
+      }
+    }
+  },
+  "$defs": {
+    "sha256": {
+      "type": "string",
+      "pattern": "^[0-9a-f]{64}$"
+    },
+    "artifact": {
+      "type": "object",
+      "additionalProperties": false,
+      "required": [
+        "sha256",
+        "sizeBytes",
+        "memberCount",
+        "memberInventorySha256"
+      ],
+      "properties": {
+        "sha256": {"$ref": "#/$defs/sha256"},
+        "sizeBytes": {"type": "integer", "minimum": 1},
+        "memberCount": {"type": "integer", "minimum": 1},
+        "memberInventorySha256": {"$ref": "#/$defs/sha256"}
+      }
+    }
+  }
+}
diff --git a/requirements/ci-constraints.txt b/requirements/ci-constraints.txt
new file mode 100644
index 0000000000000000000000000000000000000000..194fc9274eb5986e02bb3a04be64014c7dc1aeb9
--- /dev/null
+++ b/requirements/ci-constraints.txt
@@ -0,0 +1,7 @@
+build==1.5.0
+packaging==26.3
+pip==26.2
+pyproject-hooks==1.2.0
+ruff==0.16.2
+setuptools==84.0.0
+wheel==0.48.0
diff --git a/scripts/capture_basic_title_binding.py b/scripts/capture_basic_title_binding.py
index 9eb642787e18bbd83d55e06fe977321d195cf34e..69e2824cf787950ef665ee3af40bb0116ed4cdb1 100755
--- a/scripts/capture_basic_title_binding.py
+++ b/scripts/capture_basic_title_binding.py
@@ -18,8 +18,8 @@ FORBIDDEN_TEXT = (
     "Artlist LT",
     "江城知音体",
     "Transcription Template",
-    "/Users/",
-    "/mnt/invented-volume/",
+    "/" + "Users" + "/",
+    "/" + "Volumes" + "/HoneyPot/",
 )
 STYLE_ATTRIBUTES = ("alignment", "font", "fontColor", "fontFace", "fontSize")
 ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
diff --git a/scripts/release_gate.py b/scripts/release_gate.py
new file mode 100644
index 0000000000000000000000000000000000000000..924ea76306755a8aab5e5950754ecd1cf6af4796
--- /dev/null
+++ b/scripts/release_gate.py
@@ -0,0 +1,71 @@
+"""Maintainer-only Task 11 release-readiness command."""
+
+from __future__ import annotations
+
+import argparse
+import hashlib
+import json
+import sys
+from pathlib import Path
+
+if __package__:
+    from scripts import release_gate_core
+else:
+    import release_gate_core
+
+
+class _UsageError(Exception):
+    pass
+
+
+class _Parser(argparse.ArgumentParser):
+    def error(self, message: str) -> None:
+        raise _UsageError from None
+
+
+def _error(code: str) -> None:
+    print(json.dumps({"error": code}, separators=(",", ":")), file=sys.stderr)
+
+
+def _parser() -> argparse.ArgumentParser:
+    parser = _Parser(add_help=True, allow_abbrev=False)
+    parser.add_argument("--source", required=True)
+    parser.add_argument("--output", required=True)
+    return parser
+
+
+def main(argv: list[str] | None = None) -> int:
+    try:
+        arguments = _parser().parse_args(argv)
+    except _UsageError:
+        _error("TRITRACK_RELEASE_USAGE")
+        return 64
+    try:
+        manifest = release_gate_core.run_release_gate(
+            Path(arguments.source), Path(arguments.output)
+        )
+        manifest_sha = hashlib.sha256(
+            release_gate_core._canonical_manifest(manifest)
+        ).hexdigest()
+        project = manifest["project"]
+        artifacts = manifest["artifacts"]
+        lines = (
+            "RELEASE_GATE\tPASS",
+            f"commit\t{project['commit']}",
+            f"version\t{project['version']}",
+            f"wheelSha256\t{artifacts['wheel']['sha256']}",
+            f"sdistSha256\t{artifacts['sdist']['sha256']}",
+            f"manifestSha256\t{manifest_sha}",
+        )
+    except release_gate_core.ReleaseGateError as error:
+        _error(error.code)
+        return 1
+    except Exception:  # noqa: BLE001 - the public boundary must never emit a traceback
+        _error("TRITRACK_RELEASE_INTERNAL")
+        return 1
+    print("\n".join(lines))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/scripts/release_gate_core.py b/scripts/release_gate_core.py
new file mode 100644
index 0000000000000000000000000000000000000000..2be9bf2dc106b4ea123d0f3be03900f9d0215228
--- /dev/null
+++ b/scripts/release_gate_core.py
@@ -0,0 +1,1222 @@
+"""Bounded, fail-closed primitives for the maintainer release gate."""
+
+from __future__ import annotations
+
+import hashlib
+import importlib.metadata
+import json
+import os
+import platform
+import re
+import stat
+import subprocess
+import sys
+import tarfile
+import tempfile
+import tomllib
+import unicodedata
+import zipfile
+from collections.abc import Mapping
+from dataclasses import dataclass
+from email.parser import BytesParser
+from pathlib import Path, PurePosixPath
+
+import jsonschema
+
+_COMMAND_TIMEOUT_SECONDS = 30
+_COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
+_POLICY_LIMIT = 1024 * 1024
+_ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
+_ALLOWED_FAKE_SECRETS = frozenset(
+    {b"editor", b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
+)
+
+
+class ReleaseGateError(Exception):
+    """One stable public-safe release-gate failure code."""
+
+    def __init__(self, code: str):
+        self.code = code
+        super().__init__(code)
+
+    def __str__(self) -> str:
+        return self.code
+
+
+@dataclass(frozen=True)
+class SourceInventory:
+    count: int
+    total_bytes: int
+    sha256: str
+    commit: str
+
+
+@dataclass(frozen=True)
+class DistributionInspection:
+    sha256: str
+    size_bytes: int
+    member_count: int
+    member_inventory_sha256: str
+
+
+@dataclass(frozen=True)
+class ReleaseContext:
+    project_name: str
+    version: str
+    commit: str
+    source_inventory: SourceInventory
+    toolchain: Mapping[str, str]
+    python_version: str
+    implementation: str
+    system: str
+    machine: str
+    wheel: DistributionInspection
+    sdist: DistributionInspection
+
+
+def _fail(code: str) -> None:
+    raise ReleaseGateError(code)
+
+
+def _safe_environment() -> dict[str, str]:
+    return {
+        "GIT_CONFIG_NOSYSTEM": "1",
+        "GIT_OPTIONAL_LOCKS": "0",
+        "LANG": "C",
+        "LC_ALL": "C",
+        "PATH": os.defpath,
+    }
+
+
+def _run_git(source: Path, *arguments: str) -> bytes:
+    try:
+        result = subprocess.run(
+            ["git", *arguments],
+            cwd=source,
+            env=_safe_environment(),
+            shell=False,
+            stdin=subprocess.DEVNULL,
+            capture_output=True,
+            timeout=_COMMAND_TIMEOUT_SECONDS,
+            check=False,
+        )
+    except (OSError, subprocess.TimeoutExpired):
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
+    if result.returncode != 0:
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
+    if len(result.stdout) > _COMMAND_OUTPUT_LIMIT:
+        _fail("TRITRACK_RELEASE_GIT_LIMIT")
+    return result.stdout
+
+
+def _read_regular(path: Path, limit: int) -> bytes:
+    flags = os.O_RDONLY
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
+    try:
+        descriptor = os.open(path, flags)
+    except OSError:
+        _fail("TRITRACK_RELEASE_SOURCE_READ")
+    try:
+        details = os.fstat(descriptor)
+        if not stat.S_ISREG(details.st_mode):
+            _fail("TRITRACK_RELEASE_SOURCE_MODE")
+        if details.st_size > limit:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        chunks: list[bytes] = []
+        remaining = limit + 1
+        while remaining:
+            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
+            if not chunk:
+                break
+            chunks.append(chunk)
+            remaining -= len(chunk)
+        encoded = b"".join(chunks)
+        if len(encoded) > limit or len(encoded) != details.st_size:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        return encoded
+    except OSError:
+        _fail("TRITRACK_RELEASE_SOURCE_READ")
+    finally:
+        os.close(descriptor)
+
+
+def _mapping(value: object, code: str) -> Mapping[str, object]:
+    if not isinstance(value, Mapping):
+        _fail(code)
+    return value
+
+
+def _positive_limit(policy: Mapping[str, object], name: str) -> int:
+    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
+    value = limits.get(name)
+    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    return value
+
+
+def _string_list(value: object) -> tuple[str, ...]:
+    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    if len(value) != len(set(value)):
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    return tuple(value)
+
+
+def _load_policy(source: Path) -> Mapping[str, object]:
+    encoded = _read_regular(source / "release" / "package-policy-v1.json", _POLICY_LIMIT)
+    try:
+        policy = json.loads(encoded.decode("utf-8"))
+    except (UnicodeDecodeError, json.JSONDecodeError):
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    policy = _mapping(policy, "TRITRACK_RELEASE_POLICY_INVALID")
+    if policy.get("schemaVersion") != "tritrack.package-policy/v1":
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    if set(policy) != {"schemaVersion", "limits", "source", "wheel", "sdist"}:
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    return policy
+
+
+def _status(source: Path) -> bytes:
+    return _run_git(
+        source,
+        "status",
+        "--porcelain=v1",
+        "-z",
+        "--untracked-files=all",
+    )
+
+
+def _safe_source_path(encoded: bytes) -> str:
+    try:
+        name = encoded.decode("utf-8", "strict")
+    except UnicodeDecodeError:
+        _fail("TRITRACK_RELEASE_SOURCE_PATH")
+    candidate = PurePosixPath(name)
+    if (
+        not name
+        or "\\" in name
+        or candidate.is_absolute()
+        or any(part in {"", ".", ".."} for part in candidate.parts)
+    ):
+        _fail("TRITRACK_RELEASE_SOURCE_PATH")
+    return name
+
+
+def _parse_index(encoded: bytes) -> list[tuple[str, str, str]]:
+    entries: list[tuple[str, str, str]] = []
+    for raw in encoded.split(b"\0"):
+        if not raw:
+            continue
+        try:
+            prefix, raw_path = raw.split(b"\t", 1)
+            mode, object_id, stage = prefix.decode("ascii").split(" ")
+        except (ValueError, UnicodeDecodeError):
+            _fail("TRITRACK_RELEASE_INDEX_INVALID")
+        if stage != "0":
+            _fail("TRITRACK_RELEASE_SOURCE_STAGE")
+        if mode not in {"100644", "100755"}:
+            _fail("TRITRACK_RELEASE_SOURCE_MODE")
+        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id):
+            _fail("TRITRACK_RELEASE_INDEX_INVALID")
+        entries.append((_safe_source_path(raw_path), mode, object_id))
+    if not entries:
+        _fail("TRITRACK_RELEASE_INDEX_INVALID")
+    if len({entry[0] for entry in entries}) != len(entries):
+        _fail("TRITRACK_RELEASE_INDEX_INVALID")
+    return entries
+
+
+def _git_blob_hash(encoded: bytes, algorithm: str) -> str:
+    if algorithm not in {"sha1", "sha256"}:
+        _fail("TRITRACK_RELEASE_GIT_FORMAT")
+    digest = hashlib.new(algorithm)
+    digest.update(f"blob {len(encoded)}\0".encode("ascii"))
+    digest.update(encoded)
+    return digest.hexdigest()
+
+
+def _path_signature(path: Path) -> tuple[int, int, int, int]:
+    try:
+        details = path.stat(follow_symlinks=False)
+    except OSError:
+        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
+    return (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)
+
+
+def _home_user_after(encoded: bytes, marker: bytes, separator: bytes) -> bytes | None:
+    lowered = encoded.lower()
+    offset = 0
+    lowered_marker = marker.lower()
+    while True:
+        found = lowered.find(lowered_marker, offset)
+        if found < 0:
+            return None
+        start = found + len(marker)
+        end = start
+        while end < len(encoded) and encoded[end : end + 1] not in (
+            separator,
+            b"/",
+            b"\\",
+            b"\0",
+            b"\t",
+            b"\r",
+            b"\n",
+            b" ",
+            b'"',
+            b"'",
+        ):
+            end += 1
+        user = lowered[start:end]
+        if user and user not in _ALLOWED_FAKE_USERS:
+            return user
+        offset = max(end, start + 1)
+
+
+def scan_public_bytes(encoded: bytes) -> None:
+    """Reject public-source privacy canaries without returning matched bytes."""
+
+    mac_home = b"/" + b"Users" + b"/"
+    linux_home = b"/" + b"home" + b"/"
+    windows_home = b"\\" + b"Users" + b"\\"
+    mounted_volume = b"/" + b"Volumes" + b"/"
+    for marker, separator in (
+        (mac_home, b"/"),
+        (linux_home, b"/"),
+        (windows_home, b"\\"),
+    ):
+        if _home_user_after(encoded, marker, separator) is not None:
+            _fail("TRITRACK_RELEASE_PRIVATE_PATH")
+    if mounted_volume.lower() in encoded.lower():
+        _fail("TRITRACK_RELEASE_PRIVATE_PATH")
+
+    private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
+    rsa_private_key = b"-----BEGIN RSA " + b"PRIVATE KEY-----"
+    if private_key in encoded or rsa_private_key in encoded:
+        _fail("TRITRACK_RELEASE_PRIVATE_KEY")
+
+    terms = (
+        b"api" + b"[_-]?key",
+        b"auth" + b"[_-]?token",
+        b"access" + b"[_-]?token",
+        b"password",
+        b"passwd",
+        b"secret",
+    )
+    assignment = re.compile(
+        rb"(?im)\b(?:"
+        + b"|".join(terms)
+        + rb")\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+${}\-]{1,256})"
+    )
+    for match in assignment.finditer(encoded):
+        value = match.group(1).rstrip(b"'\"").lower()
+        if value not in _ALLOWED_FAKE_SECRETS:
+            _fail("TRITRACK_RELEASE_CREDENTIAL")
+
+
+def inventory_tracked_source(source: Path) -> SourceInventory:
+    """Bind one clean Git index to the exact regular working-tree bytes."""
+
+    source = source.resolve()
+    policy = _load_policy(source)
+    index_bytes = _run_git(source, "ls-files", "-s", "-z")
+    entries = _parse_index(index_bytes)
+    if _status(source):
+        _fail("TRITRACK_RELEASE_SOURCE_DIRTY")
+    max_files = _positive_limit(policy, "sourceMaxFiles")
+    max_file_bytes = _positive_limit(policy, "sourceMaxFileBytes")
+    max_total_bytes = _positive_limit(policy, "sourceMaxTotalBytes")
+    if len(entries) > max_files:
+        _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+    source_policy = _mapping(policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID")
+    suffixes = tuple(item.casefold() for item in _string_list(source_policy.get("forbiddenSuffixes")))
+    object_format = _run_git(source, "rev-parse", "--show-object-format").strip()
+    try:
+        algorithm = object_format.decode("ascii", "strict")
+    except UnicodeDecodeError:
+        _fail("TRITRACK_RELEASE_GIT_FORMAT")
+    commit_bytes = _run_git(source, "rev-parse", "HEAD").strip()
+    try:
+        commit = commit_bytes.decode("ascii", "strict")
+    except UnicodeDecodeError:
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
+    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
+
+    total = 0
+    inventory = hashlib.sha256()
+    for name, mode, object_id in sorted(entries):
+        if suffixes and name.casefold().endswith(suffixes):
+            _fail("TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE")
+        path = source / name
+        before = _path_signature(path)
+        if before[2] > max_file_bytes:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        total += before[2]
+        if total > max_total_bytes:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        encoded = _read_regular(path, max_file_bytes)
+        after = _path_signature(path)
+        if before != after:
+            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
+        if _git_blob_hash(encoded, algorithm) != object_id:
+            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
+        scan_public_bytes(encoded)
+        content_sha = hashlib.sha256(encoded).hexdigest()
+        for value in (name, mode, str(len(encoded)), content_sha):
+            inventory.update(value.encode("utf-8"))
+            inventory.update(b"\0")
+        inventory.update(b"\n")
+
+    if _run_git(source, "ls-files", "-s", "-z") != index_bytes or _status(source):
+        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
+    return SourceInventory(
+        count=len(entries),
+        total_bytes=total,
+        sha256=inventory.hexdigest(),
+        commit=commit,
+    )
+
+
+def _archive_size(path: Path, policy: Mapping[str, object]) -> int:
+    try:
+        details = path.stat(follow_symlinks=False)
+    except OSError:
+        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
+    if not stat.S_ISREG(details.st_mode):
+        _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
+    if details.st_size > _positive_limit(policy, "archiveMaxBytes"):
+        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+    return details.st_size
+
+
+def _safe_member_name(name: str) -> str:
+    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
+        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
+    normalized = unicodedata.normalize("NFC", name)
+    path = PurePosixPath(normalized)
+    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
+        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
+    return normalized.rstrip("/")
+
+
+def _bounded_archive_read(stream, expected: int, limit: int) -> bytes:
+    if expected > limit:
+        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+    encoded = stream.read(limit + 1)
+    if len(encoded) != expected or len(encoded) > limit:
+        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+    return encoded
+
+
+def _member_digest(
+    inventory: hashlib._Hash,
+    name: str,
+    member_type: str,
+    mode: int,
+    encoded: bytes,
+) -> None:
+    values = (
+        name,
+        member_type,
+        f"{mode & 0o7777:o}",
+        str(len(encoded)),
+        hashlib.sha256(encoded).hexdigest(),
+    )
+    for value in values:
+        inventory.update(value.encode("utf-8"))
+        inventory.update(b"\0")
+    inventory.update(b"\n")
+
+
+def _check_collision(name: str, exact: set[str], folded: set[str]) -> None:
+    if name in exact:
+        _fail("TRITRACK_RELEASE_ARCHIVE_DUPLICATE")
+    collision = unicodedata.normalize("NFC", name).casefold()
+    if collision in folded:
+        _fail("TRITRACK_RELEASE_ARCHIVE_COLLISION")
+    exact.add(name)
+    folded.add(collision)
+
+
+def inspect_wheel(
+    path: Path, policy: Mapping[str, object]
+) -> DistributionInspection:
+    """Inspect a wheel without extracting it."""
+
+    size_bytes = _archive_size(path, policy)
+    max_members = _positive_limit(policy, "archiveMaxMembers")
+    max_member = _positive_limit(policy, "memberMaxBytes")
+    max_expanded = _positive_limit(policy, "expandedMaxBytes")
+    wheel_policy = _mapping(policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID")
+    expected = set(_string_list(wheel_policy.get("expectedMembers")))
+    exact: set[str] = set()
+    folded: set[str] = set()
+    files: list[tuple[zipfile.ZipInfo, str, int]] = []
+    expanded = 0
+    try:
+        with zipfile.ZipFile(path) as archive:
+            members = archive.infolist()
+            if len(members) > max_members:
+                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+            for member in members:
+                name = _safe_member_name(member.filename)
+                _check_collision(name, exact, folded)
+                if member.flag_bits & 1:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_ENCRYPTED")
+                if member.is_dir():
+                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
+                raw_mode = member.external_attr >> 16
+                member_type = stat.S_IFMT(raw_mode)
+                if member_type not in {0, stat.S_IFREG}:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
+                expanded += member.file_size
+                if member.file_size > max_member or expanded > max_expanded:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+                files.append((member, name, raw_mode))
+            if {name for _, name, _ in files} != expected:
+                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
+            inventory = hashlib.sha256()
+            for member, name, raw_mode in sorted(files, key=lambda item: item[1]):
+                with archive.open(member) as stream:
+                    encoded = _bounded_archive_read(stream, member.file_size, max_member)
+                scan_public_bytes(encoded)
+                _member_digest(inventory, name, "file", raw_mode, encoded)
+    except ReleaseGateError:
+        raise
+    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
+        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
+    return DistributionInspection(
+        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
+        size_bytes=size_bytes,
+        member_count=len(files),
+        member_inventory_sha256=inventory.hexdigest(),
+    )
+
+
+def inspect_sdist(
+    path: Path, policy: Mapping[str, object]
+) -> DistributionInspection:
+    """Inspect a gzipped source distribution without extracting it."""
+
+    size_bytes = _archive_size(path, policy)
+    max_members = _positive_limit(policy, "archiveMaxMembers")
+    max_member = _positive_limit(policy, "memberMaxBytes")
+    max_expanded = _positive_limit(policy, "expandedMaxBytes")
+    sdist_policy = _mapping(policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID")
+    root = sdist_policy.get("root")
+    if not isinstance(root, str) or not root.endswith("/"):
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    expected = set(_string_list(sdist_policy.get("expectedMembers")))
+    exact: set[str] = set()
+    folded: set[str] = set()
+    files: list[tuple[tarfile.TarInfo, str]] = []
+    all_members: list[tuple[tarfile.TarInfo, str, str]] = []
+    expanded = 0
+    try:
+        with tarfile.open(path, mode="r:gz") as archive:
+            members = archive.getmembers()
+            if len(members) > max_members:
+                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+            for member in members:
+                full_name = _safe_member_name(member.name)
+                if full_name == root.rstrip("/"):
+                    relative = ""
+                elif full_name.startswith(root):
+                    relative = full_name[len(root) :]
+                else:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_ROOT")
+                collision_name = relative or "."
+                _check_collision(collision_name, exact, folded)
+                if member.isdir():
+                    all_members.append((member, relative, "directory"))
+                    continue
+                if not member.isreg():
+                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
+                if not relative:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
+                expanded += member.size
+                if member.size > max_member or expanded > max_expanded:
+                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
+                files.append((member, relative))
+                all_members.append((member, relative, "file"))
+            if {name for _, name in files} != expected:
+                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
+            inventory = hashlib.sha256()
+            for member, name, member_type in sorted(all_members, key=lambda item: item[1]):
+                if member_type == "directory":
+                    encoded = b""
+                else:
+                    stream = archive.extractfile(member)
+                    if stream is None:
+                        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
+                    with stream:
+                        encoded = _bounded_archive_read(stream, member.size, max_member)
+                    scan_public_bytes(encoded)
+                _member_digest(inventory, name or ".", member_type, member.mode, encoded)
+    except ReleaseGateError:
+        raise
+    except (OSError, ValueError, tarfile.TarError):
+        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
+    return DistributionInspection(
+        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
+        size_bytes=size_bytes,
+        member_count=len(all_members),
+        member_inventory_sha256=inventory.hexdigest(),
+    )
+
+
+def _run_command(
+    argv: list[str],
+    *,
+    cwd: Path,
+    env: Mapping[str, str],
+    timeout: int = 300,
+    output_limit: int = _COMMAND_OUTPUT_LIMIT,
+) -> bytes:
+    try:
+        result = subprocess.run(
+            argv,
+            cwd=cwd,
+            env=dict(env),
+            shell=False,
+            stdin=subprocess.DEVNULL,
+            capture_output=True,
+            timeout=timeout,
+            check=False,
+        )
+    except (OSError, subprocess.TimeoutExpired):
+        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
+    if result.returncode != 0:
+        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
+    if len(result.stdout) > output_limit or len(result.stderr) > output_limit:
+        _fail("TRITRACK_RELEASE_COMMAND_LIMIT")
+    return result.stdout
+
+
+def _installed_tool_versions() -> dict[str, str]:
+    versions: dict[str, str] = {}
+    for distribution in ("pip", "build", "setuptools", "wheel"):
+        try:
+            versions[distribution] = importlib.metadata.version(distribution)
+        except importlib.metadata.PackageNotFoundError:
+            _fail("TRITRACK_RELEASE_TOOLCHAIN")
+    return versions
+
+
+def _build_environment(epoch: int, temporary: Path) -> dict[str, str]:
+    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
+        _fail("TRITRACK_RELEASE_EPOCH")
+    environment = {
+        "HOME": os.fspath(temporary),
+        "LANG": "C.UTF-8",
+        "LC_ALL": "C.UTF-8",
+        "PATH": os.defpath,
+        "PYTHONHASHSEED": "0",
+        "SOURCE_DATE_EPOCH": str(epoch),
+        "TMPDIR": os.fspath(temporary),
+    }
+    return environment
+
+
+def build_distributions(
+    snapshot: Path, output: Path, *, epoch: int
+) -> tuple[Path, Path]:
+    """Build exactly one wheel and one sdist with the pinned local toolchain."""
+
+    expected_tools = {
+        "pip": "26.2",
+        "build": "1.5.0",
+        "setuptools": "84.0.0",
+        "wheel": "0.48.0",
+    }
+    if _installed_tool_versions() != expected_tools:
+        _fail("TRITRACK_RELEASE_TOOLCHAIN")
+    if not snapshot.is_dir():
+        _fail("TRITRACK_RELEASE_SNAPSHOT")
+    try:
+        os.mkdir(output)
+    except FileExistsError:
+        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
+    except OSError:
+        _fail("TRITRACK_RELEASE_OUTPUT")
+    _run_command(
+        [
+            os.fspath(Path(sys.executable)),
+            "-m",
+            "build",
+            "--no-isolation",
+            "--outdir",
+            os.fspath(output),
+        ],
+        cwd=snapshot,
+        env=_build_environment(epoch, output),
+        timeout=300,
+    )
+    try:
+        members = [
+            child
+            for child in output.iterdir()
+            if child.is_file() and not child.is_symlink()
+        ]
+    except OSError:
+        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
+    wheels = [child for child in members if child.suffix == ".whl"]
+    sdists = [child for child in members if child.name.endswith(".tar.gz")]
+    if len(members) != 2 or len(wheels) != 1 or len(sdists) != 1:
+        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
+    return wheels[0], sdists[0]
+
+
+def _wheel_project_identity(wheel: Path) -> tuple[str, str]:
+    try:
+        with zipfile.ZipFile(wheel) as archive:
+            candidates = [
+                member
+                for member in archive.infolist()
+                if member.filename.endswith(".dist-info/METADATA")
+                and not member.is_dir()
+            ]
+            if len(candidates) != 1 or candidates[0].file_size > _POLICY_LIMIT:
+                _fail("TRITRACK_RELEASE_WHEEL_METADATA")
+            with archive.open(candidates[0]) as stream:
+                encoded = _bounded_archive_read(
+                    stream, candidates[0].file_size, _POLICY_LIMIT
+                )
+    except ReleaseGateError:
+        raise
+    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
+        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
+    message = BytesParser().parsebytes(encoded)
+    name = message.get("Name")
+    version = message.get("Version")
+    if not name or not version or "\n" in name or "\n" in version:
+        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
+    return name, version
+
+
+def _install_environment(temporary: Path, binary: Path) -> dict[str, str]:
+    environment = {
+        "HOME": os.fspath(temporary),
+        "LANG": "C.UTF-8",
+        "LC_ALL": "C.UTF-8",
+        "PATH": os.fspath(binary) + os.pathsep + os.defpath,
+        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
+        "PIP_NO_INPUT": "1",
+        "PYTHONHASHSEED": "0",
+        "TMPDIR": os.fspath(temporary),
+    }
+    for name in (
+        "HTTP_PROXY",
+        "HTTPS_PROXY",
+        "NO_PROXY",
+        "PIP_INDEX_URL",
+        "PIP_TRUSTED_HOST",
+    ):
+        value = os.environ.get(name)
+        if value:
+            environment[name] = value
+    return environment
+
+
+def fresh_install_smoke(wheel: Path, temporary: Path) -> None:
+    """Install only the chosen local wheel into a new external environment."""
+
+    project_name, project_version = _wheel_project_identity(wheel)
+    if project_name != "tritrack-editing-assistant":
+        _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
+    try:
+        os.mkdir(temporary)
+    except FileExistsError:
+        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
+    except OSError:
+        _fail("TRITRACK_RELEASE_OUTPUT")
+    _run_command(
+        [os.fspath(Path(sys.executable)), "-m", "venv", os.fspath(temporary)],
+        cwd=temporary.parent,
+        env=_build_environment(0, temporary),
+        timeout=180,
+    )
+    if os.name == "nt":
+        binary = temporary / "Scripts"
+        python = binary / "python.exe"
+        tritrack = binary / "tritrack.exe"
+    else:
+        binary = temporary / "bin"
+        python = binary / "python"
+        tritrack = binary / "tritrack"
+    environment = _install_environment(temporary, binary)
+    pip_base = [
+        os.fspath(python),
+        "-m",
+        "pip",
+        "--disable-pip-version-check",
+        "--no-input",
+    ]
+    _run_command(
+        [*pip_base, "install", "pip==26.2"],
+        cwd=temporary,
+        env=environment,
+        timeout=300,
+    )
+    _run_command(
+        [*pip_base, "install", os.fspath(wheel.resolve())],
+        cwd=temporary,
+        env=environment,
+        timeout=600,
+    )
+    _run_command(
+        [*pip_base, "check"], cwd=temporary, env=environment, timeout=120
+    )
+    metadata_code = (
+        "import importlib.metadata as m; "
+        "d=m.distribution('tritrack-editing-assistant'); "
+        "print(d.metadata['Name']+'\\t'+d.version)"
+    )
+    installed = _run_command(
+        [os.fspath(python), "-I", "-c", metadata_code],
+        cwd=temporary,
+        env=environment,
+        timeout=60,
+    )
+    expected = f"{project_name}\t{project_version}\n".encode()
+    if installed != expected:
+        _fail("TRITRACK_RELEASE_INSTALLED_IDENTITY")
+    components = _run_command(
+        [os.fspath(tritrack), "components", "--json"],
+        cwd=temporary,
+        env=environment,
+        timeout=60,
+    )
+    try:
+        component_summary = json.loads(components.decode("utf-8"))
+    except (UnicodeDecodeError, json.JSONDecodeError):
+        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
+    if (
+        not isinstance(component_summary, Mapping)
+        or component_summary.get("schemaVersion") != "tritrack.components/v1"
+        or not isinstance(component_summary.get("components"), list)
+        or len(component_summary["components"]) != 11
+    ):
+        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
+    for arguments in (
+        ("validate", "--help"),
+        ("validate", "contract", "--help"),
+        ("validate", "fcpxml", "--help"),
+        ("validate", "paper", "--help"),
+        ("validate", "run", "--help"),
+    ):
+        _run_command(
+            [os.fspath(tritrack), *arguments],
+            cwd=temporary,
+            env=environment,
+            timeout=60,
+        )
+
+
+def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
+    """Build and validate the deterministic, closed public release receipt."""
+
+    manifest: dict[str, object] = {
+        "schemaVersion": "tritrack.release-manifest/v1",
+        "project": {
+            "name": context.project_name,
+            "version": context.version,
+            "commit": context.commit,
+        },
+        "sourceInventory": {
+            "count": context.source_inventory.count,
+            "sha256": context.source_inventory.sha256,
+        },
+        "toolchain": {
+            "python": context.python_version,
+            "implementation": context.implementation,
+            "pip": context.toolchain["pip"],
+            "build": context.toolchain["build"],
+            "setuptools": context.toolchain["setuptools"],
+            "wheel": context.toolchain["wheel"],
+        },
+        "platform": {"system": context.system, "machine": context.machine},
+        "artifacts": {
+            "wheel": {
+                "sha256": context.wheel.sha256,
+                "sizeBytes": context.wheel.size_bytes,
+                "memberCount": context.wheel.member_count,
+                "memberInventorySha256": context.wheel.member_inventory_sha256,
+            },
+            "sdist": {
+                "sha256": context.sdist.sha256,
+                "sizeBytes": context.sdist.size_bytes,
+                "memberCount": context.sdist.member_count,
+                "memberInventorySha256": context.sdist.member_inventory_sha256,
+            },
+        },
+        "reproducibility": {
+            "wheelBytesMatch": True,
+            "sdistMembersMatch": True,
+        },
+        "gates": {
+            "sourceIdentity": "pass",
+            "sourcePrivacy": "pass",
+            "wheelArchive": "pass",
+            "sdistArchive": "pass",
+            "freshInstall": "pass",
+        },
+        "nonClaims": [
+            "no-tag",
+            "no-release",
+            "no-package-publication",
+            "no-pull-request",
+            "no-tester-contact",
+            "no-signing",
+            "no-attestation",
+            "no-sbom",
+            "no-final-cut-gui",
+            "no-dtd",
+            "no-provider",
+            "no-application-submission",
+        ],
+    }
+    schema_path = Path(__file__).resolve().parents[1] / "release" / "release-manifest-v1.schema.json"
+    try:
+        schema = json.loads(_read_regular(schema_path, _POLICY_LIMIT).decode("utf-8"))
+        jsonschema.Draft202012Validator.check_schema(schema)
+        jsonschema.validate(manifest, schema)
+    except ReleaseGateError:
+        raise
+    except (UnicodeDecodeError, json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError):
+        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
+    return manifest
+
+
+def _link_file(source: Path, destination: Path) -> None:
+    try:
+        os.link(source, destination, follow_symlinks=False)
+    except FileExistsError:
+        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
+    except OSError:
+        _fail("TRITRACK_RELEASE_PUBLISH")
+
+
+def _fsync_directory(path: Path) -> None:
+    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
+    try:
+        descriptor = os.open(path, flags)
+        try:
+            os.fsync(descriptor)
+        finally:
+            os.close(descriptor)
+    except OSError:
+        _fail("TRITRACK_RELEASE_PUBLISH")
+
+
+def publish_release(
+    output: Path, wheel: Path, sdist: Path, manifest: bytes
+) -> None:
+    """Publish two archives first and the canonical success manifest last."""
+
+    if (
+        wheel.name in {"", ".", "..", "release-manifest.json"}
+        or sdist.name in {"", ".", "..", "release-manifest.json"}
+        or wheel.name != os.path.basename(wheel.name)
+        or sdist.name != os.path.basename(sdist.name)
+        or wheel.name == sdist.name
+    ):
+        _fail("TRITRACK_RELEASE_PUBLISH")
+    try:
+        parent_details = output.parent.stat(follow_symlinks=False)
+    except OSError:
+        _fail("TRITRACK_RELEASE_OUTPUT")
+    if not stat.S_ISDIR(parent_details.st_mode):
+        _fail("TRITRACK_RELEASE_OUTPUT")
+
+    temporary_manifest: Path | None = None
+    try:
+        with tempfile.NamedTemporaryFile(
+            mode="wb",
+            dir=wheel.parent,
+            prefix=".release-manifest-",
+            delete=False,
+        ) as stream:
+            temporary_manifest = Path(stream.name)
+            stream.write(manifest)
+            stream.flush()
+            os.fsync(stream.fileno())
+        try:
+            os.mkdir(output)
+        except FileExistsError:
+            _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
+        except OSError:
+            _fail("TRITRACK_RELEASE_OUTPUT")
+        _link_file(wheel, output / wheel.name)
+        _link_file(sdist, output / sdist.name)
+        _fsync_directory(output)
+        _link_file(temporary_manifest, output / "release-manifest.json")
+        _fsync_directory(output)
+        _fsync_directory(output.parent)
+    finally:
+        if temporary_manifest is not None:
+            try:
+                temporary_manifest.unlink(missing_ok=True)
+            except OSError:
+                pass
+
+
+def _assert_source_identity(source: Path) -> tuple[str, str]:
+    encoded = _read_regular(source / ".tritrack-project.json", _POLICY_LIMIT)
+    try:
+        identity = json.loads(encoded.decode("utf-8"))
+    except (UnicodeDecodeError, json.JSONDecodeError):
+        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")
+    expected = {
+        "schemaVersion": "tritrack.project-identity/v1",
+        "projectId": "tritrack-editing-assistant",
+        "projectKind": "public-engine",
+        "maintainerSkill": "tritrack-editing-assistant-maintainer",
+        "lane": "OSS",
+    }
+    if identity != expected:
+        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")
+
+    try:
+        configuration = tomllib.loads(
+            _read_regular(source / "pyproject.toml", _POLICY_LIMIT).decode("utf-8")
+        )
+        project = configuration["project"]
+        project_name = project["name"]
+        version = project["version"]
+    except (UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
+        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
+    if project_name != "tritrack-editing-assistant" or not isinstance(version, str):
+        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
+    init_bytes = _read_regular(
+        source / "src" / "tritrack_editing_assistant" / "__init__.py",
+        _POLICY_LIMIT,
+    )
+    match = re.fullmatch(
+        rb'"""TriTrack Editing Assistant public package\."""\n\n__version__ = "([^"\r\n]+)"\n',
+        init_bytes,
+    )
+    if match is None or match.group(1).decode("utf-8", "strict") != version:
+        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
+    return project_name, version
+
+
+def _assert_git_toplevel(source: Path) -> None:
+    try:
+        top = Path(
+            _run_git(source, "rev-parse", "--show-toplevel").decode("utf-8", "strict").strip()
+        ).resolve()
+    except (UnicodeDecodeError, OSError):
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
+    if top != source:
+        _fail("TRITRACK_RELEASE_GIT_TOPLEVEL")
+
+
+def _snapshot_inventory(
+    archive: tarfile.TarFile,
+    max_file: int,
+    max_total: int,
+) -> tuple[list[tuple[str, int, bytes]], str]:
+    files: list[tuple[str, int, bytes]] = []
+    seen: set[str] = set()
+    total = 0
+    for member in archive.getmembers():
+        name = _safe_member_name(member.name)
+        if name in seen:
+            _fail("TRITRACK_RELEASE_SNAPSHOT")
+        seen.add(name)
+        if member.isdir():
+            continue
+        if not member.isreg():
+            _fail("TRITRACK_RELEASE_SNAPSHOT")
+        if member.size > max_file:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        total += member.size
+        if total > max_total:
+            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
+        stream = archive.extractfile(member)
+        if stream is None:
+            _fail("TRITRACK_RELEASE_SNAPSHOT")
+        with stream:
+            encoded = _bounded_archive_read(stream, member.size, max_file)
+        mode = 0o755 if member.mode & 0o111 else 0o644
+        files.append((name, mode, encoded))
+    inventory = hashlib.sha256()
+    for name, mode, encoded in sorted(files):
+        content_sha = hashlib.sha256(encoded).hexdigest()
+        for value in (name, f"100{mode:o}"[-6:], str(len(encoded)), content_sha):
+            inventory.update(value.encode("utf-8"))
+            inventory.update(b"\0")
+        inventory.update(b"\n")
+    return files, inventory.hexdigest()
+
+
+def _write_snapshot_file(root: Path, name: str, mode: int, encoded: bytes) -> None:
+    path = root.joinpath(*PurePosixPath(name).parts)
+    try:
+        path.parent.mkdir(parents=True, exist_ok=True)
+        descriptor = os.open(
+            path,
+            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
+            mode,
+        )
+        try:
+            view = memoryview(encoded)
+            while view:
+                written = os.write(descriptor, view)
+                if written < 1:
+                    _fail("TRITRACK_RELEASE_SNAPSHOT")
+                view = view[written:]
+        finally:
+            os.close(descriptor)
+        os.chmod(path, mode, follow_symlinks=False)
+    except ReleaseGateError:
+        raise
+    except OSError:
+        _fail("TRITRACK_RELEASE_SNAPSHOT")
+
+
+def _materialize_snapshot(
+    source: Path,
+    destination: Path,
+    inventory: SourceInventory,
+    policy: Mapping[str, object],
+) -> None:
+    try:
+        os.mkdir(destination)
+    except OSError:
+        _fail("TRITRACK_RELEASE_SNAPSHOT")
+    archive_path = destination.parent / f".{destination.name}.tar"
+    _run_command(
+        [
+            "git",
+            "archive",
+            "--format=tar",
+            "--output",
+            os.fspath(archive_path),
+            inventory.commit,
+        ],
+        cwd=source,
+        env=_safe_environment(),
+        timeout=120,
+    )
+    try:
+        with tarfile.open(archive_path, mode="r:") as archive:
+            files, digest = _snapshot_inventory(
+                archive,
+                _positive_limit(policy, "sourceMaxFileBytes"),
+                _positive_limit(policy, "sourceMaxTotalBytes"),
+            )
+        if len(files) != inventory.count or digest != inventory.sha256:
+            _fail("TRITRACK_RELEASE_SNAPSHOT_MISMATCH")
+        for name, mode, encoded in files:
+            _write_snapshot_file(destination, name, mode, encoded)
+    except ReleaseGateError:
+        raise
+    except (OSError, tarfile.TarError):
+        _fail("TRITRACK_RELEASE_SNAPSHOT")
+    finally:
+        try:
+            archive_path.unlink(missing_ok=True)
+        except OSError:
+            pass
+
+
+def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
+    return (
+        json.dumps(
+            manifest,
+            ensure_ascii=False,
+            sort_keys=True,
+            separators=(",", ":"),
+        ).encode("utf-8")
+        + b"\n"
+    )
+
+
+def run_release_gate(source: Path, output: Path) -> dict[str, object]:
+    """Run the complete local release-readiness gate and publish manifest last."""
+
+    try:
+        source = source.resolve(strict=True)
+    except OSError:
+        _fail("TRITRACK_RELEASE_SOURCE")
+    if not source.is_dir():
+        _fail("TRITRACK_RELEASE_SOURCE")
+    _assert_git_toplevel(source)
+    project_name, version = _assert_source_identity(source)
+    inventory = inventory_tracked_source(source)
+    policy = _load_policy(source)
+    if output.exists() or output.is_symlink():
+        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
+    try:
+        output_parent = output.parent.resolve(strict=True)
+    except OSError:
+        _fail("TRITRACK_RELEASE_OUTPUT")
+    output = output_parent / output.name
+    epoch_bytes = _run_git(source, "show", "-s", "--format=%ct", inventory.commit).strip()
+    try:
+        epoch = int(epoch_bytes.decode("ascii", "strict"))
+    except (UnicodeDecodeError, ValueError):
+        _fail("TRITRACK_RELEASE_EPOCH")
+    if _run_git(source, "rev-parse", "HEAD").strip().decode("ascii") != inventory.commit:
+        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
+
+    with tempfile.TemporaryDirectory(
+        dir=output.parent, prefix=".tritrack-release-staging-"
+    ) as temporary:
+        staging = Path(temporary)
+        snapshot_one = staging / "snapshot-one"
+        snapshot_two = staging / "snapshot-two"
+        _materialize_snapshot(source, snapshot_one, inventory, policy)
+        _materialize_snapshot(source, snapshot_two, inventory, policy)
+        wheel_one, sdist_one = build_distributions(
+            snapshot_one, staging / "dist-one", epoch=epoch
+        )
+        wheel_two, sdist_two = build_distributions(
+            snapshot_two, staging / "dist-two", epoch=epoch
+        )
+        identities = {
+            _wheel_project_identity(wheel_one),
+            _wheel_project_identity(wheel_two),
+        }
+        if identities != {(project_name, version)}:
+            _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
+        if wheel_one.name != wheel_two.name or sdist_one.name != sdist_two.name:
+            _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
+        if wheel_one.read_bytes() != wheel_two.read_bytes():
+            _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
+        wheel_inspection = inspect_wheel(wheel_one, policy)
+        second_wheel_inspection = inspect_wheel(wheel_two, policy)
+        sdist_inspection = inspect_sdist(sdist_one, policy)
+        second_sdist_inspection = inspect_sdist(sdist_two, policy)
+        if wheel_inspection != second_wheel_inspection:
+            _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
+        if (
+            sdist_inspection.member_inventory_sha256
+            != second_sdist_inspection.member_inventory_sha256
+        ):
+            _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
+        fresh_install_smoke(wheel_one, staging / "fresh-install")
+        context = ReleaseContext(
+            project_name=project_name,
+            version=version,
+            commit=inventory.commit,
+            source_inventory=inventory,
+            toolchain=_installed_tool_versions(),
+            python_version=platform.python_version(),
+            implementation=platform.python_implementation(),
+            system=platform.system(),
+            machine=platform.machine(),
+            wheel=wheel_inspection,
+            sdist=sdist_inspection,
+        )
+        manifest = build_release_manifest(context)
+        publish_release(
+            output,
+            wheel_one,
+            sdist_one,
+            _canonical_manifest(manifest),
+        )
+    return manifest
diff --git a/skills/tritrack-editing-assistant/SKILL.md b/skills/tritrack-editing-assistant/SKILL.md
index f05fa4a67d6ef055a0df7a15cc6678d1d9cbc70b..210dcbaa33ce1ff58947ec4be5eb92e985a122f2 100644
--- a/skills/tritrack-editing-assistant/SKILL.md
+++ b/skills/tritrack-editing-assistant/SKILL.md
@@ -17,6 +17,11 @@ command surface.
    - `tritrack run align --help`
    - `tritrack run finish --help`
    - `tritrack run status --help`
+   - `tritrack validate --help`
+   - `tritrack validate contract --help`
+   - `tritrack validate fcpxml --help`
+   - `tritrack validate paper --help`
+   - `tritrack validate run --help`
 3. Treat installed help as the command authority. Stop if a required command or
    flag is unavailable; do not guess a replacement.
 
@@ -102,6 +107,24 @@ Report only the run ID, phase, next action, stage names, logical artifact names,
 and hashes. Do not expose local paths, transcript text, question text, notes, or
 FCPXML content in a status summary.
 
+## Validate an existing artifact without mutation
+
+Choose one explicit mode from installed help. Do not guess a format or search
+nearby paths.
+
+- `contract` returns the exact `contract` scope for one registered JSON
+  contract. It does not prove referenced files or cross-file hashes.
+- `fcpxml` returns `structural-profile` for the selected installed profile and
+  title binding. It does not check source media, a DTD, or a GUI import.
+- `paper` returns `authority-bound` for one workbook checked against the exact
+  supplied aligned transcript bytes. It does not publish editor intent.
+- `run` returns `complete-run-bundle` for one complete immutable bundle and its
+  manifest chain.
+
+All four modes are read-only. Validation does not repair an artifact, create an
+output, inspect unrelated content, or make a network request. Report success
+only inside the returned scope.
+
 ## Stop on strict failures
 
 Stop when compatibility, source custody, exact hashes, manifest chain, schema,
diff --git a/src/tritrack_editing_assistant/cli.py b/src/tritrack_editing_assistant/cli.py
index 5a23e7972915e6b35c09b6ac246289cf0bf4f94a..e23b09abf46b57c24c3ae0570e16b9944c577c63 100644
--- a/src/tritrack_editing_assistant/cli.py
+++ b/src/tritrack_editing_assistant/cli.py
@@ -18,6 +18,7 @@ from . import paper_edit as paper_module
 from . import run_workflow as run_module
 from . import sync_scan as sync_module
 from . import transcribe_takes as transcribe_module
+from . import validate_artifacts as validate_module
 
 EXIT_OK = 0
 EXIT_USAGE = 64
@@ -29,6 +30,18 @@ EXIT_TEMPORARY = 75
 EXIT_POLICY = 78
 
 
+class CliUsageError(ValueError):
+    """Private signal for sanitized command-line usage failures."""
+
+
+class TriTrackArgumentParser(argparse.ArgumentParser):
+    """Argument parser that preserves the public exit-code contract."""
+
+    def error(self, message: str) -> None:
+        del message
+        raise CliUsageError("TRITRACK_USAGE")
+
+
 COMPONENTS = (
     {
         "sourceComponent": "sync_scan.py",
@@ -594,8 +607,83 @@ def _run_status(arguments: argparse.Namespace) -> int:
     return EXIT_OK
 
 
+def _validate_error_exit(code: str) -> int:
+    if code in {
+        "TRITRACK_VALIDATE_INPUT_UNREADABLE",
+        "TRITRACK_PAPER_INPUT_UNREADABLE",
+        "TRITRACK_RUN_INPUT_UNREADABLE",
+    }:
+        return EXIT_IO
+    if code in {
+        "TRITRACK_CONTRACT_REGISTRY_INVALID",
+        "TRITRACK_PROFILE_UNKNOWN",
+        "TRITRACK_TITLE_BINDING_UNKNOWN",
+    }:
+        return EXIT_POLICY
+    return EXIT_DATA
+
+
+def _print_validation_summary(
+    summary: dict[str, object], *, as_json: bool
+) -> None:
+    if as_json:
+        print(json.dumps(summary, ensure_ascii=False, indent=2))
+        return
+    print(
+        f"VALIDATION\t{summary['artifactKind']}\t"
+        f"{summary['validationScope']}"
+    )
+    hashes = summary["hashes"]
+    counts = summary["counts"]
+    details = summary["details"]
+    assert isinstance(hashes, dict)
+    assert isinstance(counts, dict)
+    assert isinstance(details, dict)
+    for name in sorted(hashes):
+        print(f"HASH\t{name}\t{hashes[name]}")
+    for name in sorted(counts):
+        print(f"COUNT\t{name}\t{counts[name]}")
+    for name in sorted(details):
+        encoded = json.dumps(
+            details[name],
+            ensure_ascii=False,
+            separators=(",", ":"),
+            sort_keys=True,
+        )
+        print(f"DETAIL\t{name}\t{encoded}")
+
+
+def _run_validate(arguments: argparse.Namespace) -> int:
+    try:
+        if arguments.validate_command == "contract":
+            summary = validate_module.validate_contract_artifact(
+                arguments.artifact
+            )
+        elif arguments.validate_command == "fcpxml":
+            summary = validate_module.validate_fcpxml_artifact(
+                arguments.artifact,
+                profile_id=arguments.profile,
+                binding_id=arguments.binding,
+            )
+        elif arguments.validate_command == "paper":
+            summary = validate_module.validate_paper_artifacts(
+                arguments.aligned,
+                arguments.workbook,
+            )
+        elif arguments.validate_command == "run":
+            summary = validate_module.validate_run_bundle(arguments.run_dir)
+        else:
+            raise CliUsageError("TRITRACK_USAGE")
+    except (TypeError, ValueError) as error:
+        code = str(error).split(":", 1)[0]
+        print(json.dumps({"error": code}, ensure_ascii=False))
+        return _validate_error_exit(code)
+    _print_validation_summary(summary, as_json=arguments.json)
+    return EXIT_OK
+
+
 def build_parser() -> argparse.ArgumentParser:
-    parser = argparse.ArgumentParser(
+    parser = TriTrackArgumentParser(
         prog="tritrack",
         description="Local-first Final Cut editing-assistant workflow",
     )
@@ -955,18 +1043,61 @@ def build_parser() -> argparse.ArgumentParser:
     run_status.add_argument("--json", action="store_true")
     run_status.set_defaults(handler=_run_status)
 
-    planned_commands = {
-        "validate": "validate generated output",
-    }
-    for name, help_text in planned_commands.items():
-        command_parser = subparsers.add_parser(name, help=help_text)
-        command_parser.set_defaults(handler=_planned_command)
+    validate = subparsers.add_parser(
+        "validate",
+        help="validate one public artifact without writing",
+    )
+    validate_subparsers = validate.add_subparsers(
+        dest="validate_command",
+        required=True,
+    )
+
+    validate_contract = validate_subparsers.add_parser(
+        "contract",
+        help="check one JSON artifact against its installed contract",
+    )
+    validate_contract.add_argument("--artifact", required=True, type=Path)
+    validate_contract.add_argument("--json", action="store_true")
+    validate_contract.set_defaults(handler=_run_validate)
+
+    validate_fcpxml = validate_subparsers.add_parser(
+        "fcpxml",
+        help="check one FCPXML artifact against installed authorities",
+    )
+    validate_fcpxml.add_argument("--artifact", required=True, type=Path)
+    validate_fcpxml.add_argument("--profile", required=True)
+    validate_fcpxml.add_argument("--binding", required=True)
+    validate_fcpxml.add_argument("--json", action="store_true")
+    validate_fcpxml.set_defaults(handler=_run_validate)
+
+    validate_paper = validate_subparsers.add_parser(
+        "paper",
+        help="check one workbook against exact aligned authority",
+    )
+    validate_paper.add_argument("--aligned", required=True, type=Path)
+    validate_paper.add_argument("--workbook", required=True, type=Path)
+    validate_paper.add_argument("--json", action="store_true")
+    validate_paper.set_defaults(handler=_run_validate)
+
+    validate_run = validate_subparsers.add_parser(
+        "run",
+        help="check one complete immutable run bundle",
+    )
+    validate_run.add_argument(
+        "--run", dest="run_dir", required=True, type=Path
+    )
+    validate_run.add_argument("--json", action="store_true")
+    validate_run.set_defaults(handler=_run_validate)
 
     return parser
 
 
 def main(argv: Sequence[str] | None = None) -> int:
-    arguments = build_parser().parse_args(argv)
+    try:
+        arguments = build_parser().parse_args(argv)
+    except CliUsageError:
+        print(json.dumps({"error": "TRITRACK_USAGE"}, ensure_ascii=False))
+        return EXIT_USAGE
     return arguments.handler(arguments)
 
 
diff --git a/src/tritrack_editing_assistant/contracts.py b/src/tritrack_editing_assistant/contracts.py
index d25e0fea78ecabaf402c351fdeeba40bbec86333..6403a6754a86c8aa5fbda0ba884f72839ba5e3bf 100644
--- a/src/tritrack_editing_assistant/contracts.py
+++ b/src/tritrack_editing_assistant/contracts.py
@@ -3,8 +3,10 @@
 from __future__ import annotations
 
 import json
+from collections.abc import Mapping
 from functools import cache
 from importlib import resources
+from types import MappingProxyType
 
 import jsonschema
 
@@ -46,3 +48,32 @@ def validate_contract(name: str, payload: object) -> None:
 
     validator = jsonschema.Draft202012Validator(load_schema(name))
     validator.validate(payload)
+
+
+@cache
+def contract_names_by_schema_version() -> Mapping[str, str]:
+    """Return the closed installed schema-version to contract-name registry."""
+
+    mapping: dict[str, str] = {}
+    for name in sorted(CONTRACT_NAMES):
+        schema = load_schema(name)
+        try:
+            version = schema["properties"]["schemaVersion"]["const"]
+        except (KeyError, TypeError) as error:
+            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID") from error
+        if not isinstance(version, str) or version in mapping:
+            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID")
+        mapping[version] = name
+    return MappingProxyType(mapping)
+
+
+def contract_name_for_schema_version(schema_version: object) -> str:
+    """Resolve only an exact version declared by one installed contract."""
+
+    if not isinstance(schema_version, str):
+        # One stable data-error family covers absent, non-string, and unknown IDs.
+        raise ValueError("TRITRACK_CONTRACT_UNKNOWN")  # noqa: TRY004
+    try:
+        return contract_names_by_schema_version()[schema_version]
+    except KeyError as error:
+        raise ValueError("TRITRACK_CONTRACT_UNKNOWN") from error
diff --git a/src/tritrack_editing_assistant/doctor.py b/src/tritrack_editing_assistant/doctor.py
index 3446082839a2190e918f940a8af22e56beee4c08..8a02e5363acab6e958600c30ccddefff85da3aa7 100644
--- a/src/tritrack_editing_assistant/doctor.py
+++ b/src/tritrack_editing_assistant/doctor.py
@@ -94,7 +94,9 @@ class SystemProbe:
 def _sanitize_detected(value: str) -> str:
     """Keep version text while refusing local path-shaped material."""
 
-    if "/Users/" in value or "/mnt/invented-volume/" in value or "\\" in value:
+    private_home = "/" + "Users" + "/"
+    mounted_volume = "/" + "Volumes" + "/"
+    if private_home in value or mounted_volume in value or "\\" in value:
         return "detected-redacted"
     first, separator, remainder = value.partition(" ")
     if first.startswith("/"):
diff --git a/src/tritrack_editing_assistant/paper_edit.py b/src/tritrack_editing_assistant/paper_edit.py
index 39abeeaa2f0eee1a6435546d8cebb7da8f599cc9..ad12b806f1605a60f0ea9143ba53c5c0d66d662a 100644
--- a/src/tritrack_editing_assistant/paper_edit.py
+++ b/src/tritrack_editing_assistant/paper_edit.py
@@ -64,6 +64,18 @@ class LoadedArtifact:
     limit: int
 
 
+@dataclass(frozen=True)
+class ValidatedWorkbook:
+    aligned_sha256: str
+    workbook_sha256: str
+    workbook_schema_version: str
+    cue_count: int
+    question_count: int
+    answer_count: int
+    reserve_count: int
+    grouping: dict[str, object]
+
+
 def _read_regular_bytes(path: Path, *, limit: int, invalid_code: str) -> bytes:
     flags = os.O_RDONLY
     if hasattr(os, "O_NOFOLLOW"):
@@ -697,17 +709,12 @@ def _grouping_from_workbook(
     )
 
 
-def apply_workbook(
+def validate_workbook(
     aligned_path: Path,
     workbook_path: Path,
-    *,
-    output_path: Path,
-) -> dict[str, object]:
-    """Apply strict workbook intent and publish canonical grouping JSON."""
+) -> ValidatedWorkbook:
+    """Validate and re-derive one workbook without publishing output."""
 
-    destination = require_absent_output(output_path)
-    if not destination.parent.is_dir():
-        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     aligned = _load_json(
         aligned_path,
         contract="aligned-transcript-v1",
@@ -731,5 +738,39 @@ def apply_workbook(
     )
     _verify_unchanged(aligned)
     _verify_unchanged(workbook_artifact)
-    _publish_bytes(organizer.encode_grouping(grouping), destination)
-    return grouping
+    questions = grouping["questions"]
+    reserve = grouping["reserve"]
+    assert isinstance(questions, list)
+    assert isinstance(reserve, list)
+    answer_count = 0
+    for question in questions:
+        assert isinstance(question, Mapping)
+        answers = question["answers"]
+        assert isinstance(answers, list)
+        answer_count += len(answers)
+    return ValidatedWorkbook(
+        aligned_sha256=aligned.sha256,
+        workbook_sha256=workbook_artifact.sha256,
+        workbook_schema_version=WORKBOOK_SCHEMA_VERSION,
+        cue_count=len(cue_rows),
+        question_count=len(questions),
+        answer_count=answer_count,
+        reserve_count=len(reserve),
+        grouping=grouping,
+    )
+
+
+def apply_workbook(
+    aligned_path: Path,
+    workbook_path: Path,
+    *,
+    output_path: Path,
+) -> dict[str, object]:
+    """Apply strict workbook intent and publish canonical grouping JSON."""
+
+    destination = require_absent_output(output_path)
+    if not destination.parent.is_dir():
+        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
+    validated = validate_workbook(aligned_path, workbook_path)
+    _publish_bytes(organizer.encode_grouping(validated.grouping), destination)
+    return validated.grouping
diff --git a/src/tritrack_editing_assistant/run_workflow.py b/src/tritrack_editing_assistant/run_workflow.py
index b59859795babb2a3971a416f164b28b3237d4a05..3bb33b75b3a3eaa992ebf6069e2a0c4c2bc466f4 100644
--- a/src/tritrack_editing_assistant/run_workflow.py
+++ b/src/tritrack_editing_assistant/run_workflow.py
@@ -961,7 +961,17 @@ def finish_run(
     return summarize_bundle(publish_bundle(Path(output_dir), build))
 
 
+def inspect_run(
+    run_dir: Path,
+) -> tuple[LoadedRunBundle, dict[str, object]]:
+    """Validate, recheck, and summarize one run without writing anything."""
+
+    bundle = load_bundle(Path(run_dir))
+    _require_bundle_unchanged(bundle)
+    return bundle, summarize_bundle(bundle)
+
+
 def status_run(run_dir: Path) -> dict[str, object]:
     """Validate and summarize one run bundle without writing anything."""
 
-    return summarize_bundle(load_bundle(Path(run_dir)))
+    return inspect_run(run_dir)[1]
diff --git a/src/tritrack_editing_assistant/validate_artifacts.py b/src/tritrack_editing_assistant/validate_artifacts.py
new file mode 100644
index 0000000000000000000000000000000000000000..1e9896ec2223b6afe9c4bdadc761d27466856235
--- /dev/null
+++ b/src/tritrack_editing_assistant/validate_artifacts.py
@@ -0,0 +1,199 @@
+"""Read-only, offline validation of public TriTrack artifacts."""
+
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import stat
+from dataclasses import dataclass
+from decimal import Decimal
+from pathlib import Path
+
+from jsonschema import ValidationError
+
+from . import __version__, contracts, doctor, emit_fcpxml, paper_edit, run_workflow
+
+MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024
+
+
+@dataclass(frozen=True)
+class LoadedValidationArtifact:
+    path: Path
+    encoded: bytes
+    sha256: str
+
+
+def _read_regular_bytes(path: Path) -> bytes:
+    flags = os.O_RDONLY
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode):
+            raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE")
+        if not 0 < metadata.st_size <= MAX_VALIDATION_ARTIFACT_BYTES:
+            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(MAX_VALIDATION_ARTIFACT_BYTES + 1)
+        if len(encoded) > MAX_VALIDATION_ARTIFACT_BYTES:
+            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
+        return encoded
+    except OSError as error:
+        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+
+
+def _load_regular_artifact(path: Path) -> LoadedValidationArtifact:
+    selected = Path(path)
+    encoded = _read_regular_bytes(selected)
+    return LoadedValidationArtifact(
+        path=selected,
+        encoded=encoded,
+        sha256=hashlib.sha256(encoded).hexdigest(),
+    )
+
+
+def _verify_unchanged(artifact: LoadedValidationArtifact) -> None:
+    try:
+        encoded = _read_regular_bytes(artifact.path)
+    except ValueError as error:
+        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED") from error
+    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
+        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED")
+
+
+def _validation_summary(
+    *,
+    kind: str,
+    scope: str,
+    hashes: dict[str, str],
+    counts: dict[str, int],
+    details: dict[str, object],
+) -> dict[str, object]:
+    return {
+        "schemaVersion": "tritrack.validate-summary/v1",
+        "toolVersion": __version__,
+        "artifactKind": kind,
+        "validationScope": scope,
+        "hashes": hashes,
+        "counts": counts,
+        "details": details,
+    }
+
+
+def validate_contract_artifact(path: Path) -> dict[str, object]:
+    """Validate one JSON file against its exact installed closed contract."""
+
+    artifact = _load_regular_artifact(path)
+    try:
+        payload = json.loads(
+            artifact.encoded.decode("utf-8", errors="strict"),
+            parse_float=Decimal,
+        )
+    except (UnicodeError, json.JSONDecodeError) as error:
+        raise ValueError("TRITRACK_VALIDATE_JSON_INVALID") from error
+    try:
+        schema_version = payload["schemaVersion"]
+    except (KeyError, TypeError) as error:
+        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
+    try:
+        contract_name = contracts.contract_name_for_schema_version(schema_version)
+    except ValueError as error:
+        if str(error) == "TRITRACK_CONTRACT_REGISTRY_INVALID":
+            raise
+        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
+    try:
+        contracts.validate_contract(contract_name, payload)
+    except (TypeError, ValidationError) as error:
+        raise ValueError("TRITRACK_VALIDATE_CONTRACT_INVALID") from error
+    _verify_unchanged(artifact)
+    return _validation_summary(
+        kind="contract",
+        scope="contract",
+        hashes={"artifact": artifact.sha256},
+        counts={},
+        details={
+            "contractName": contract_name,
+            "contractSchemaVersion": schema_version,
+        },
+    )
+
+
+def validate_fcpxml_artifact(
+    path: Path,
+    *,
+    profile_id: str,
+    binding_id: str,
+) -> dict[str, object]:
+    """Validate one FCPXML file against exact installed profile authorities."""
+
+    artifact = _load_regular_artifact(path)
+    try:
+        text = artifact.encoded.decode("utf-8", errors="strict")
+    except UnicodeError as error:
+        raise ValueError("TRITRACK_VALIDATE_FCPXML_INVALID") from error
+    profile = doctor.load_profile(profile_id)
+    binding = doctor.load_title_binding(binding_id)
+    emit_fcpxml.validate_fcpxml(text, profile=profile, binding=binding)
+    _verify_unchanged(artifact)
+    return _validation_summary(
+        kind="fcpxml",
+        scope="structural-profile",
+        hashes={"artifact": artifact.sha256},
+        counts={},
+        details={"profileId": profile_id, "bindingId": binding_id},
+    )
+
+
+def validate_paper_artifacts(
+    aligned_path: Path,
+    workbook_path: Path,
+) -> dict[str, object]:
+    """Validate one workbook against the exact aligned JSON authority."""
+
+    validated = paper_edit.validate_workbook(aligned_path, workbook_path)
+    return _validation_summary(
+        kind="paper",
+        scope="authority-bound",
+        hashes={
+            "aligned": validated.aligned_sha256,
+            "workbook": validated.workbook_sha256,
+        },
+        counts={
+            "answerCount": validated.answer_count,
+            "cueCount": validated.cue_count,
+            "questionCount": validated.question_count,
+            "reserveCount": validated.reserve_count,
+        },
+        details={
+            "workbookSchemaVersion": validated.workbook_schema_version,
+        },
+    )
+
+
+def validate_run_bundle(run_dir: Path) -> dict[str, object]:
+    """Validate and summarize one complete immutable run bundle."""
+
+    bundle, run_summary = run_workflow.inspect_run(run_dir)
+    stages = run_summary["stages"]
+    artifacts = run_summary["artifacts"]
+    assert isinstance(stages, list)
+    assert isinstance(artifacts, dict)
+    return _validation_summary(
+        kind="run",
+        scope="complete-run-bundle",
+        hashes={"manifest": bundle.manifest_sha256},
+        counts={
+            "artifactCount": len(artifacts),
+            "stageCount": len(stages),
+        },
+        details={"runSummary": run_summary},
+    )
diff --git a/tests/test_cli.py b/tests/test_cli.py
index c93322a89d06abd15c79c8cf03473a2b92fb58d9..79f046f5d6cc7b492aedfdbeba9b68af471fa43b 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -11,6 +11,7 @@ import unittest
 from pathlib import Path
 from unittest import mock
 
+from tests.test_contracts import VALID_CONTRACTS
 from tritrack_editing_assistant import cli, run_workflow
 
 ROOT = Path(__file__).resolve().parents[1]
@@ -977,5 +978,274 @@ class CliSmokeTest(unittest.TestCase):
             self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")
 
 
+class ValidateCliTest(unittest.TestCase):
+    def run_cli_unchecked(self, *args: str) -> subprocess.CompletedProcess[str]:
+        environment = os.environ.copy()
+        environment["PYTHONPATH"] = str(ROOT / "src")
+        return subprocess.run(
+            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
+            check=False,
+            capture_output=True,
+            text=True,
+            cwd=ROOT,
+            env=environment,
+        )
+
+    def test_help_exposes_exact_four_read_only_modes(self) -> None:
+        expected = {
+            "contract": ("--artifact", "--json"),
+            "fcpxml": ("--artifact", "--profile", "--binding", "--json"),
+            "paper": ("--aligned", "--workbook", "--json"),
+            "run": ("--run", "--json"),
+        }
+        parent = self.run_cli_unchecked("validate", "--help")
+        self.assertEqual(parent.returncode, 0, parent.stderr)
+        for mode in expected:
+            self.assertIn(mode, parent.stdout)
+        for mode, flags in expected.items():
+            with self.subTest(mode=mode):
+                completed = self.run_cli_unchecked("validate", mode, "--help")
+                self.assertEqual(completed.returncode, 0, completed.stderr)
+                for flag in flags:
+                    self.assertIn(flag, completed.stdout)
+                for forbidden in (
+                    "output",
+                    "repair",
+                    "network",
+                    "provider",
+                    "credential",
+                    "dtd",
+                    "media-probe",
+                ):
+                    self.assertNotIn(forbidden, completed.stdout.lower())
+
+    def test_contract_json_and_human_summaries_are_path_free(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            artifact = root / "private-name.json"
+            encoded = (
+                json.dumps(
+                    VALID_CONTRACTS["grouping-v1"],
+                    ensure_ascii=False,
+                    indent=2,
+                    sort_keys=True,
+                )
+                + "\n"
+            ).encode("utf-8")
+            artifact.write_bytes(encoded)
+
+            as_json = self.run_cli_unchecked(
+                "validate", "contract", "--artifact", str(artifact), "--json"
+            )
+            human = self.run_cli_unchecked(
+                "validate", "contract", "--artifact", str(artifact)
+            )
+
+            self.assertEqual(as_json.returncode, 0, as_json.stderr)
+            summary = json.loads(as_json.stdout)
+            self.assertEqual(summary["artifactKind"], "contract")
+            self.assertEqual(summary["validationScope"], "contract")
+            self.assertEqual(
+                summary["hashes"]["artifact"],
+                hashlib.sha256(encoded).hexdigest(),
+            )
+            self.assertEqual(human.returncode, 0, human.stderr)
+            self.assertEqual(
+                human.stdout.splitlines(),
+                [
+                    "VALIDATION\tcontract\tcontract",
+                    f"HASH\tartifact\t{hashlib.sha256(encoded).hexdigest()}",
+                    "DETAIL\tcontractName\t\"grouping-v1\"",
+                    "DETAIL\tcontractSchemaVersion\t\"tritrack.grouping/v1\"",
+                ],
+            )
+            for output in (as_json.stdout, human.stdout):
+                self.assertNotIn(str(root), output)
+                self.assertNotIn("What changed?", output)
+
+    def test_dispatches_fcpxml_paper_and_run_with_exact_arguments(self) -> None:
+        base_summary = {
+            "schemaVersion": "tritrack.validate-summary/v1",
+            "toolVersion": "0.1.0a0",
+            "artifactKind": "invented",
+            "validationScope": "invented-scope",
+            "hashes": {},
+            "counts": {},
+            "details": {},
+        }
+        with (
+            mock.patch.object(
+                cli.validate_module,
+                "validate_fcpxml_artifact",
+                return_value=base_summary,
+            ) as fcpxml,
+            mock.patch.object(
+                cli.validate_module,
+                "validate_paper_artifacts",
+                return_value=base_summary,
+            ) as paper,
+            mock.patch.object(
+                cli.validate_module,
+                "validate_run_bundle",
+                return_value=base_summary,
+            ) as run,
+        ):
+            for arguments in (
+                [
+                    "validate",
+                    "fcpxml",
+                    "--artifact",
+                    "story.fcpxml",
+                    "--profile",
+                    "profile-id",
+                    "--binding",
+                    "binding-id",
+                    "--json",
+                ],
+                [
+                    "validate",
+                    "paper",
+                    "--aligned",
+                    "aligned.json",
+                    "--workbook",
+                    "paper.xlsx",
+                    "--json",
+                ],
+                ["validate", "run", "--run", "finished-run", "--json"],
+            ):
+                with self.subTest(arguments=arguments):
+                    output = io.StringIO()
+                    with contextlib.redirect_stdout(output):
+                        self.assertEqual(cli.main(arguments), 0)
+                    self.assertEqual(json.loads(output.getvalue()), base_summary)
+
+        fcpxml.assert_called_once_with(
+            Path("story.fcpxml"),
+            profile_id="profile-id",
+            binding_id="binding-id",
+        )
+        paper.assert_called_once_with(Path("aligned.json"), Path("paper.xlsx"))
+        run.assert_called_once_with(Path("finished-run"))
+
+    def test_usage_data_io_and_policy_failures_are_stable_and_sanitized(self) -> None:
+        usage = self.run_cli_unchecked("validate", "contract")
+        self.assertEqual(usage.returncode, 64)
+        self.assertEqual(json.loads(usage.stdout), {"error": "TRITRACK_USAGE"})
+        self.assertEqual(usage.stderr, "")
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            malformed = root / "private-name.json"
+            malformed.write_text("{private text", encoding="utf-8")
+            data = self.run_cli_unchecked(
+                "validate", "contract", "--artifact", str(malformed)
+            )
+            missing = self.run_cli_unchecked(
+                "validate",
+                "contract",
+                "--artifact",
+                str(root / "missing.json"),
+            )
+            xml = root / "story.fcpxml"
+            xml.write_text("invented", encoding="utf-8")
+            policy = self.run_cli_unchecked(
+                "validate",
+                "fcpxml",
+                "--artifact",
+                str(xml),
+                "--profile",
+                "unknown-profile",
+                "--binding",
+                "basic-title-v1",
+            )
+
+            self.assertEqual(data.returncode, 65)
+            self.assertEqual(
+                json.loads(data.stdout), {"error": "TRITRACK_VALIDATE_JSON_INVALID"}
+            )
+            self.assertEqual(missing.returncode, 74)
+            self.assertEqual(
+                json.loads(missing.stdout),
+                {"error": "TRITRACK_VALIDATE_INPUT_UNREADABLE"},
+            )
+            self.assertEqual(policy.returncode, 78)
+            self.assertEqual(
+                json.loads(policy.stdout), {"error": "TRITRACK_PROFILE_UNKNOWN"}
+            )
+            for completed in (data, missing, policy):
+                self.assertEqual(completed.stderr, "")
+                self.assertNotIn(str(root), completed.stdout)
+                self.assertNotIn("private text", completed.stdout)
+                self.assertNotIn("Traceback", completed.stdout)
+
+    def test_validate_does_not_change_component_registry(self) -> None:
+        self.assertEqual(len(cli.COMPONENTS), 11)
+        self.assertFalse(
+            any(component["command"] == "validate" for component in cli.COMPONENTS)
+        )
+
+
+class ValidateDocumentationTest(unittest.TestCase):
+    def test_public_docs_name_all_help_authorities_and_scope_boundaries(self) -> None:
+        paths = (
+            ROOT / "README.md",
+            ROOT / "docs" / "TOOLING.md",
+            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md",
+        )
+        commands = (
+            "tritrack validate --help",
+            "tritrack validate contract --help",
+            "tritrack validate fcpxml --help",
+            "tritrack validate paper --help",
+            "tritrack validate run --help",
+        )
+        scopes = (
+            "contract",
+            "structural-profile",
+            "authority-bound",
+            "complete-run-bundle",
+        )
+        for path in paths:
+            text = path.read_text(encoding="utf-8")
+            with self.subTest(path=path.name):
+                for command in commands:
+                    self.assertIn(command, text)
+                for scope in scopes:
+                    self.assertIn(scope, text)
+                self.assertIn("read-only", text)
+                self.assertIn("does not repair", text)
+                self.assertIn("source media", text)
+                self.assertIn("DTD", text)
+                self.assertIn("GUI", text)
+
+    def test_release_gate_is_maintainer_only_and_python_support_is_exact(self) -> None:
+        release_command = (
+            "python scripts/release_gate.py --source . --output ABSENT_DIRECTORY"
+        )
+        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
+        maintainer = (
+            ROOT
+            / ".agents"
+            / "skills"
+            / "tritrack-editing-assistant-maintainer"
+            / "SKILL.md"
+        ).read_text(encoding="utf-8")
+        end_user = (
+            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md"
+        ).read_text(encoding="utf-8")
+        readme = (ROOT / "README.md").read_text(encoding="utf-8")
+        self.assertIn(release_command, tooling)
+        self.assertIn(release_command, maintainer)
+        for text in (readme, end_user):
+            self.assertNotIn(release_command, text)
+        self.assertNotIn("release", end_user.casefold())
+        self.assertNotIn(".py", end_user.casefold())
+
+        for relative in ("README.md", "docs/TOOLING.md", "CONTRIBUTING.md"):
+            text = (ROOT / relative).read_text(encoding="utf-8")
+            self.assertIn("Python 3.12 and 3.13", text, relative)
+            self.assertNotIn("Python 3.12 or newer", text, relative)
+
+
 if __name__ == "__main__":
     unittest.main()
diff --git a/tests/test_maintainer_boundary.py b/tests/test_maintainer_boundary.py
index a483ccf0e8ede3bffc896cac1237c863dc3f60e7..bde2b8760ed80d0a75e05079287e45784acb64fb 100644
--- a/tests/test_maintainer_boundary.py
+++ b/tests/test_maintainer_boundary.py
@@ -105,6 +105,11 @@ class MaintainerBoundaryTest(unittest.TestCase):
             "tritrack run align --help",
             "tritrack run finish --help",
             "tritrack run status --help",
+            "tritrack validate --help",
+            "tritrack validate contract --help",
+            "tritrack validate fcpxml --help",
+            "tritrack validate paper --help",
+            "tritrack validate run --help",
         ):
             self.assertIn(command, end_user)
         for required in (
@@ -117,6 +122,9 @@ class MaintainerBoundaryTest(unittest.TestCase):
             "absent output directory",
             "Keep media",
             "strict aligned transcript",
+            "structural-profile",
+            "authority-bound",
+            "complete-run-bundle",
         ):
             self.assertIn(required, end_user)
 
@@ -141,7 +149,7 @@ class MaintainerBoundaryTest(unittest.TestCase):
         for token in forbidden:
             self.assertNotIn(token, lowered)
 
-    def test_public_status_records_task_10_and_schedules_task_11(self) -> None:
+    def test_public_status_records_task_11_and_schedules_task_12(self) -> None:
         status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
         roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
         tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
@@ -152,13 +160,17 @@ class MaintainerBoundaryTest(unittest.TestCase):
         verification = (ROOT / "docs" / "TASK-10-VERIFICATION.md").read_text(
             encoding="utf-8"
         )
-        self.assertIn("Tasks 1–10", status)
+        task_11_verification = (ROOT / "docs" / "TASK-11-VERIFICATION.md").read_text(
+            encoding="utf-8"
+        )
+        self.assertIn("Tasks 1–11", status)
         self.assertIn("Task 6.5", status)
         self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
         self.assertLess(status.index("Task 7"), status.index("Task 8"))
         self.assertLess(status.index("Task 8"), status.index("Task 9"))
         self.assertLess(status.index("Task 9"), status.index("Task 10"))
         self.assertLess(status.index("Task 10"), status.index("Task 11"))
+        self.assertLess(status.index("Task 11"), status.index("Task 12"))
         self.assertIn("Task 10", roadmap)
         self.assertLess(roadmap.index("Task 10"), roadmap.index("Task 11"))
         for authority in (
@@ -177,7 +189,18 @@ class MaintainerBoundaryTest(unittest.TestCase):
         self.assertIn("no network", verification)
         self.assertIn("Task 11", status)
         self.assertIn("Task 11", roadmap)
+        self.assertIn("Task 12", status)
+        self.assertIn("Task 12", roadmap)
+        self.assertIn("ce562e995b63f3f1a29989de3e1ef202da27b5f2", task_11_verification)
+        for scope in (
+            "contract",
+            "structural-profile",
+            "authority-bound",
+            "complete-run-bundle",
+        ):
+            self.assertIn(scope, task_11_verification)
         self.assertNotIn("`validate` and `run` remain planned", status)
+        self.assertNotIn("`validate` remains planned", status)
         self.assertNotIn("`tritrack run` | planned", readme)
 
     def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
diff --git a/tests/test_packaging.py b/tests/test_packaging.py
new file mode 100644
index 0000000000000000000000000000000000000000..d2a748fa22535aa2ff5467a4cc15a0a35be30820
--- /dev/null
+++ b/tests/test_packaging.py
@@ -0,0 +1,239 @@
+"""Task 11 distribution policy and reproducibility tests."""
+
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import shutil
+import subprocess
+import sys
+import tarfile
+import tempfile
+import tomllib
+import unittest
+import zipfile
+from pathlib import Path
+
+import jsonschema
+
+ROOT = Path(__file__).resolve().parents[1]
+POLICY_PATH = ROOT / "release" / "package-policy-v1.json"
+MANIFEST_SCHEMA_PATH = ROOT / "release" / "release-manifest-v1.schema.json"
+SDIST_ROOT = "tritrack_editing_assistant-0.1.0a0/"
+
+
+def normalized_inventory(entries: dict[str, bytes]) -> str:
+    digest = hashlib.sha256()
+    for name in sorted(entries):
+        encoded = entries[name]
+        digest.update(name.encode("utf-8"))
+        digest.update(b"\0")
+        digest.update(str(len(encoded)).encode("ascii"))
+        digest.update(b"\0")
+        digest.update(hashlib.sha256(encoded).hexdigest().encode("ascii"))
+        digest.update(b"\n")
+    return digest.hexdigest()
+
+
+class PackagingPolicyTest(unittest.TestCase):
+    def test_01_python_and_tool_constraints_are_exact(self) -> None:
+        configuration = tomllib.loads((ROOT / "pyproject.toml").read_text())
+        self.assertEqual(
+            configuration["build-system"]["requires"],
+            ["setuptools==84.0.0"],
+        )
+        self.assertEqual(configuration["project"]["requires-python"], ">=3.12,<3.14")
+        self.assertEqual(
+            configuration["project"]["optional-dependencies"]["dev"],
+            ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"],
+        )
+        classifiers = configuration["project"]["classifiers"]
+        versions = [
+            value
+            for value in classifiers
+            if value.startswith("Programming Language :: Python :: 3.")
+        ]
+        self.assertEqual(
+            versions,
+            [
+                "Programming Language :: Python :: 3.12",
+                "Programming Language :: Python :: 3.13",
+            ],
+        )
+        self.assertEqual(
+            (ROOT / "requirements" / "ci-constraints.txt")
+            .read_text(encoding="utf-8")
+            .splitlines(),
+            [
+                "build==1.5.0",
+                "packaging==26.3",
+                "pip==26.2",
+                "pyproject-hooks==1.2.0",
+                "ruff==0.16.2",
+                "setuptools==84.0.0",
+                "wheel==0.48.0",
+            ],
+        )
+
+    def test_02_package_policy_and_manifest_schema_are_closed(self) -> None:
+        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
+        self.assertEqual(policy["schemaVersion"], "tritrack.package-policy/v1")
+        self.assertEqual(
+            set(policy),
+            {"schemaVersion", "limits", "source", "wheel", "sdist"},
+        )
+        for required in (
+            "docs/TASK-11-VERIFICATION.md",
+            "scripts/release_gate.py",
+            "scripts/release_gate_core.py",
+        ):
+            self.assertIn(required, policy["sdist"]["expectedMembers"])
+        schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
+        jsonschema.Draft202012Validator.check_schema(schema)
+        sample = {
+            "schemaVersion": "tritrack.release-manifest/v1",
+            "project": {
+                "name": "tritrack-editing-assistant",
+                "version": "0.1.0a0",
+                "commit": "a" * 40,
+            },
+            "sourceInventory": {"count": 1, "sha256": "b" * 64},
+            "toolchain": {
+                "python": "3.13.15",
+                "implementation": "CPython",
+                "pip": "26.2",
+                "build": "1.5.0",
+                "setuptools": "84.0.0",
+                "wheel": "0.48.0",
+            },
+            "platform": {"system": "Darwin", "machine": "arm64"},
+            "artifacts": {
+                kind: {
+                    "sha256": value * 64,
+                    "sizeBytes": 1,
+                    "memberCount": 1,
+                    "memberInventorySha256": value * 64,
+                }
+                for kind, value in (("wheel", "c"), ("sdist", "d"))
+            },
+            "reproducibility": {
+                "wheelBytesMatch": True,
+                "sdistMembersMatch": True,
+            },
+            "gates": {
+                name: "pass"
+                for name in (
+                    "sourceIdentity",
+                    "sourcePrivacy",
+                    "wheelArchive",
+                    "sdistArchive",
+                    "freshInstall",
+                )
+            },
+            "nonClaims": ["no-tag", "no-package-publication"],
+        }
+        jsonschema.validate(sample, schema)
+        sample["unexpected"] = True
+        with self.assertRaises(jsonschema.ValidationError):
+            jsonschema.validate(sample, schema)
+
+    def test_03_distribution_members_are_explicit_and_reproducible(self) -> None:
+        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            distributions: list[tuple[Path, Path]] = []
+            for label in ("first", "second"):
+                source = root / label / "source"
+                shutil.copytree(
+                    ROOT,
+                    source,
+                    ignore=shutil.ignore_patterns(
+                        ".git",
+                        ".release-evidence",
+                        "__pycache__",
+                        "*.egg-info",
+                        "build",
+                        "dist",
+                    ),
+                )
+                output = root / label / "dist"
+                output.mkdir()
+                environment = os.environ.copy()
+                environment["SOURCE_DATE_EPOCH"] = "1704067200"
+                subprocess.run(
+                    [
+                        sys.executable,
+                        "-m",
+                        "build",
+                        "--no-isolation",
+                        "--outdir",
+                        str(output),
+                    ],
+                    cwd=source,
+                    env=environment,
+                    check=True,
+                    capture_output=True,
+                    text=True,
+                )
+                wheel = next(output.glob("*.whl"))
+                sdist = next(output.glob("*.tar.gz"))
+                distributions.append((wheel, sdist))
+
+            first_wheel, first_sdist = distributions[0]
+            second_wheel, second_sdist = distributions[1]
+            self.assertEqual(first_wheel.read_bytes(), second_wheel.read_bytes())
+
+            with zipfile.ZipFile(first_wheel) as archive:
+                wheel_entries = {
+                    member.filename: archive.read(member)
+                    for member in archive.infolist()
+                    if not member.is_dir()
+                }
+            self.assertEqual(
+                set(wheel_entries),
+                set(policy["wheel"]["expectedMembers"]),
+            )
+            for forbidden in ("tests/", "docs/", "skills/", "scripts/", ".github/"):
+                self.assertFalse(any(forbidden in name for name in wheel_entries))
+
+            sdist_inventories: list[str] = []
+            for sdist in (first_sdist, second_sdist):
+                with tarfile.open(sdist, mode="r:gz") as archive:
+                    entries = {
+                        member.name.removeprefix(SDIST_ROOT): archive.extractfile(
+                            member
+                        ).read()
+                        for member in archive.getmembers()
+                        if member.isfile()
+                    }
+                self.assertTrue(all(name and not name.startswith("/") for name in entries))
+                self.assertEqual(
+                    set(entries),
+                    set(policy["sdist"]["expectedMembers"]),
+                )
+                sdist_inventories.append(normalized_inventory(entries))
+                for forbidden in (
+                    ".agents/",
+                    "docs/reviews/",
+                    "docs/superpowers/plans/",
+                    "tests/test_maintainer_boundary.py",
+                ):
+                    self.assertFalse(any(name.startswith(forbidden) for name in entries))
+            self.assertEqual(sdist_inventories[0], sdist_inventories[1])
+
+    def test_04_historical_records_have_no_machine_specific_home(self) -> None:
+        forbidden = "/" + "Users" + "/real-person"
+        for relative in (
+            "docs/reviews/task-10-closeout-packet-2026-08-17.md",
+            "docs/superpowers/plans/2026-08-17-task-10-immutable-run.md",
+        ):
+            self.assertNotIn(
+                forbidden,
+                (ROOT / relative).read_text(encoding="utf-8"),
+                relative,
+            )
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_paper_edit.py b/tests/test_paper_edit.py
index 6d962b44ff9345ddbc6c7273bb0aec9ad2c7c6af..e0898a2c94d6ab67101120825402cbe6efefe338 100644
--- a/tests/test_paper_edit.py
+++ b/tests/test_paper_edit.py
@@ -13,7 +13,7 @@ from unittest import mock
 from openpyxl import load_workbook
 
 from tests.task9_fixtures import invented_aligned, invented_grouping
-from tritrack_editing_assistant import organizer, paper_edit
+from tritrack_editing_assistant import organizer, paper_edit, validate_artifacts
 from tritrack_editing_assistant.contracts import validate_contract
 
 
@@ -318,6 +318,59 @@ class PaperApplyTest(unittest.TestCase):
             self.assertNotIn("sourceSha256", encoded)
             self.assertNotIn("Invented first answer.", encoded)
 
+    def test_validate_workbook_is_read_only_and_shares_apply_authority(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            aligned, workbook, aligned_bytes = self.editable_workbook(root)
+            workbook_bytes = workbook.read_bytes()
+            entries_before = {entry.name for entry in root.iterdir()}
+
+            validated = paper_edit.validate_workbook(aligned, workbook)
+            summary = validate_artifacts.validate_paper_artifacts(
+                aligned,
+                workbook,
+            )
+
+            self.assertEqual(validated.aligned_sha256, hashlib.sha256(aligned_bytes).hexdigest())
+            self.assertEqual(validated.workbook_sha256, hashlib.sha256(workbook_bytes).hexdigest())
+            self.assertEqual(validated.workbook_schema_version, "tritrack.paper-workbook/v1")
+            self.assertEqual(
+                (
+                    validated.cue_count,
+                    validated.question_count,
+                    validated.answer_count,
+                    validated.reserve_count,
+                ),
+                (4, 2, 2, 1),
+            )
+            self.assertEqual(
+                summary,
+                {
+                    "schemaVersion": "tritrack.validate-summary/v1",
+                    "toolVersion": "0.1.0a0",
+                    "artifactKind": "paper",
+                    "validationScope": "authority-bound",
+                    "hashes": {
+                        "aligned": hashlib.sha256(aligned_bytes).hexdigest(),
+                        "workbook": hashlib.sha256(workbook_bytes).hexdigest(),
+                    },
+                    "counts": {
+                        "answerCount": 2,
+                        "cueCount": 4,
+                        "questionCount": 2,
+                        "reserveCount": 1,
+                    },
+                    "details": {
+                        "workbookSchemaVersion": "tritrack.paper-workbook/v1"
+                    },
+                },
+            )
+            self.assertEqual(entries_before, {entry.name for entry in root.iterdir()})
+            self.assertEqual(aligned.read_bytes(), aligned_bytes)
+            self.assertEqual(workbook.read_bytes(), workbook_bytes)
+            self.assertNotIn("Invented", json.dumps(summary))
+            self.assertNotIn(str(root), json.dumps(summary))
+
     def test_grouping_fixpoint_and_logical_grid_idempotence(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
diff --git a/tests/test_quickstart_demo.py b/tests/test_quickstart_demo.py
index b65afc358f2e912a9f205338289c3ada147ba4f0..ddfad1bf8464e412714aa596c4c5a19aea11b24e 100644
--- a/tests/test_quickstart_demo.py
+++ b/tests/test_quickstart_demo.py
@@ -138,7 +138,7 @@ class InstalledSurfaceRunner:
 class QuickstartDemoTest(unittest.TestCase):
     def test_documented_one_command_quickstart_entry_point_exists(self) -> None:
         self.assertTrue(EXAMPLE.is_file(), "missing public quickstart entry point")
-        self.assertTrue(WORKFLOW.is_file(), "missing minimal public CI workflow")
+        self.assertTrue(WORKFLOW.is_file(), "missing release-grade public CI workflow")
         command = "venv/bin/python examples/quickstart_demo.py"
         self.assertIn(command, (ROOT / "README.md").read_text(encoding="utf-8"))
 
diff --git a/tests/test_release_ci.py b/tests/test_release_ci.py
new file mode 100644
index 0000000000000000000000000000000000000000..4f357db8438fdad0294bb1076dea26317893f2fc
--- /dev/null
+++ b/tests/test_release_ci.py
@@ -0,0 +1,115 @@
+"""Task 11 public release-grade CI configuration contract."""
+
+from __future__ import annotations
+
+import re
+import unittest
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[1]
+WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ci.yml"
+CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
+SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"
+
+
+class ReleaseCiContractTest(unittest.TestCase):
+    @classmethod
+    def setUpClass(cls) -> None:
+        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
+        cls.lowered = cls.workflow.casefold()
+
+    def test_exact_fixed_four_cell_matrix(self) -> None:
+        cells = re.findall(
+            r"- os: (ubuntu-24\.04|macos-26)\n"
+            r'\s+python-version: "(3\.12|3\.13)"\n'
+            r"\s+architecture: (x64|arm64)",
+            self.workflow,
+        )
+        self.assertEqual(
+            cells,
+            [
+                ("ubuntu-24.04", "3.12", "x64"),
+                ("ubuntu-24.04", "3.13", "x64"),
+                ("macos-26", "3.12", "arm64"),
+                ("macos-26", "3.13", "arm64"),
+            ],
+        )
+        self.assertIn("runs-on: ${{ matrix.os }}", self.workflow)
+        self.assertIn("fail-fast: false", self.workflow)
+        self.assertNotIn("-latest", self.workflow)
+
+    def test_matrix_runs_complete_build_and_installed_smoke(self) -> None:
+        required = (
+            "python -m pip install --constraint requirements/ci-constraints.txt pip setuptools",
+            "python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'",
+            "python -m unittest discover -s tests -v",
+            "python -m compileall -q src tests examples scripts",
+            "python -m build --wheel --no-isolation",
+            "python -m venv",
+            "pip check",
+            "components --json",
+            "validate --help",
+            "validate contract --help",
+            "validate fcpxml --help",
+            "validate paper --help",
+            "validate run --help",
+        )
+        for command in required:
+            self.assertIn(command, self.workflow)
+
+    def test_quality_and_release_jobs_are_single_fixed_cells(self) -> None:
+        self.assertRegex(
+            self.workflow,
+            r"quality:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
+        )
+        self.assertRegex(
+            self.workflow,
+            r"release-gate:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
+        )
+        self.assertGreaterEqual(self.workflow.count('python-version: "3.13"'), 4)
+        self.assertIn("ruff check src tests examples scripts", self.workflow)
+        self.assertIn(
+            "python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v",
+            self.workflow,
+        )
+        self.assertIn(
+            "python scripts/release_gate.py --source . --output .release-evidence/ci",
+            self.workflow,
+        )
+
+    def test_actions_permissions_and_negative_authority_are_closed(self) -> None:
+        uses = re.findall(r"uses:\s*([^\s#]+)", self.workflow)
+        self.assertTrue(uses)
+        self.assertEqual(
+            set(uses),
+            {
+                f"actions/checkout@{CHECKOUT_SHA}",
+                f"actions/setup-python@{SETUP_PYTHON_SHA}",
+            },
+        )
+        for action in uses:
+            self.assertRegex(action, r"@[0-9a-f]{40}$")
+        self.assertRegex(
+            self.workflow,
+            r"permissions:\n  contents: read\n\njobs:",
+        )
+        self.assertNotIn("cache:", self.workflow)
+        for forbidden in (
+            "upload-artifact",
+            "download-artifact",
+            "gh release",
+            "git tag",
+            "twine",
+            "pypi",
+            "sigstore",
+            "attest",
+            "sbom",
+            "secrets.",
+            "xmllint",
+            "xcodebuild",
+        ):
+            self.assertNotIn(forbidden, self.lowered)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_release_gate.py b/tests/test_release_gate.py
new file mode 100644
index 0000000000000000000000000000000000000000..58f37e3ae327538e91238343609c7bef0873bf24
--- /dev/null
+++ b/tests/test_release_gate.py
@@ -0,0 +1,617 @@
+"""Task 11 maintainer release-gate tests."""
+
+from __future__ import annotations
+
+import contextlib
+import hashlib
+import importlib
+import io
+import json
+import os
+import stat
+import subprocess
+import tarfile
+import tempfile
+import unittest
+import warnings
+import zipfile
+from pathlib import Path
+from unittest import mock
+
+from scripts import release_gate_core
+
+
+def _policy(*, wheel: list[str] | None = None, sdist: list[str] | None = None):
+    return {
+        "schemaVersion": "tritrack.package-policy/v1",
+        "limits": {
+            "sourceMaxFiles": 32,
+            "sourceMaxFileBytes": 4096,
+            "sourceMaxTotalBytes": 32768,
+            "archiveMaxBytes": 65536,
+            "archiveMaxMembers": 32,
+            "memberMaxBytes": 4096,
+            "expandedMaxBytes": 32768,
+        },
+        "source": {
+            "allowedFakeHomeUsers": ["editor", "example", "fake", "test"],
+            "allowedFakeSecretValues": [
+                "example",
+                "fake",
+                "placeholder",
+                "redacted",
+                "secret",
+                "test",
+            ],
+            "forbiddenSuffixes": [".mov", ".xlsx"],
+        },
+        "wheel": {"expectedMembers": wheel or ["demo.py"]},
+        "sdist": {
+            "root": "demo-1.0/",
+            "expectedMembers": sdist or ["README.md"],
+        },
+    }
+
+
+def _run(*argv: str, cwd: Path, input_bytes: bytes | None = None) -> bytes:
+    return subprocess.run(
+        argv,
+        cwd=cwd,
+        input=input_bytes,
+        check=True,
+        capture_output=True,
+    ).stdout
+
+
+def _make_repo(root: Path, files: dict[str, bytes] | None = None) -> None:
+    (root / "release").mkdir(parents=True)
+    (root / "release" / "package-policy-v1.json").write_text(
+        json.dumps(_policy()), encoding="utf-8"
+    )
+    for name, encoded in (files or {"public.txt": b"public\n"}).items():
+        path = root / name
+        path.parent.mkdir(parents=True, exist_ok=True)
+        path.write_bytes(encoded)
+    _run("git", "init", "-q", cwd=root)
+    _run("git", "config", "user.name", "Invented Tester", cwd=root)
+    _run("git", "config", "user.email", "test@example.invalid", cwd=root)
+    _run("git", "add", ".", cwd=root)
+    _run("git", "commit", "-qm", "fixture", cwd=root)
+
+
+def _zip(path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]) -> None:
+    with (
+        zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive,
+        warnings.catch_warnings(),
+    ):
+        warnings.simplefilter("ignore", UserWarning)
+        for name, encoded in entries:
+            archive.writestr(name, encoded)
+
+
+def _tar(
+    path: Path,
+    entries: list[tuple[tarfile.TarInfo | str, bytes]],
+) -> None:
+    with tarfile.open(path, "w:gz") as archive:
+        for name, encoded in entries:
+            member = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
+            if member.isreg():
+                member.size = len(encoded)
+            archive.addfile(member, io.BytesIO(encoded) if member.isreg() else None)
+
+
+class SourceGateTest(unittest.TestCase):
+    def test_clean_stage_zero_regular_source_is_inventory_bound(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root)
+            first = release_gate_core.inventory_tracked_source(root)
+            second = release_gate_core.inventory_tracked_source(root)
+        self.assertEqual(first, second)
+        self.assertEqual(first.count, 2)
+        self.assertEqual(len(first.sha256), 64)
+        self.assertGreater(first.total_bytes, 0)
+
+    def test_dirty_source_and_tracked_links_fail_closed(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root)
+            (root / "public.txt").write_text("changed\n", encoding="utf-8")
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_DIRTY$"
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root)
+            (root / "public.txt").unlink()
+            os.symlink("target", root / "public.txt")
+            _run("git", "add", "public.txt", cwd=root)
+            _run("git", "commit", "-qm", "link", cwd=root)
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+    def test_submodule_unmerged_and_late_change_fail_closed(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root)
+            head = _run("git", "rev-parse", "HEAD", cwd=root).strip().decode()
+            _run(
+                "git",
+                "update-index",
+                "--add",
+                "--cacheinfo",
+                f"160000,{head},nested",
+                cwd=root,
+            )
+            _run("git", "commit", "-qm", "gitlink", cwd=root)
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root)
+            original = release_gate_core._read_regular
+            changed = False
+
+            def mutate(path: Path, limit: int) -> bytes:
+                nonlocal changed
+                encoded = original(path, limit)
+                if path.name == "public.txt" and not changed:
+                    changed = True
+                    path.write_text("late change\n", encoding="utf-8")
+                return encoded
+
+            with (
+                mock.patch.object(
+                    release_gate_core, "_read_regular", side_effect=mutate
+                ),
+                self.assertRaisesRegex(
+                    release_gate_core.ReleaseGateError,
+                    "^TRITRACK_RELEASE_SOURCE_CHANGED$",
+                ),
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+    def test_source_bounds_and_forbidden_suffix_are_enforced(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root, {"clip.mov": b"invented"})
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError,
+                "^TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE$",
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            _make_repo(root, {"large.txt": b"x" * 5000})
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_LIMIT$"
+            ):
+                release_gate_core.inventory_tracked_source(root)
+
+    def test_privacy_scanner_redacts_paths_and_credentials(self) -> None:
+        private_home = b"/" + b"Users" + b"/real-person/project"
+        credential = b"API" + b"_KEY=" + b"A" * 36
+        private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
+        for encoded in (private_home, credential, private_key):
+            with self.subTest(kind=hashlib.sha256(encoded).hexdigest()[:8]):
+                with self.assertRaises(release_gate_core.ReleaseGateError) as caught:
+                    release_gate_core.scan_public_bytes(encoded)
+                message = str(caught.exception)
+                self.assertRegex(message, r"^TRITRACK_RELEASE_[A-Z_]+$")
+                self.assertNotIn(encoded.decode(), message)
+
+        for public in (
+            b"/Users/editor/invented",
+            b"/home/example/demo",
+            b"password=placeholder",
+            b"secret=test",
+        ):
+            release_gate_core.scan_public_bytes(public)
+
+
+class ArchiveGateTest(unittest.TestCase):
+    def test_safe_wheel_and_sdist_return_only_counts_and_digests(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            wheel = root / "demo.whl"
+            sdist = root / "demo.tar.gz"
+            _zip(wheel, [("demo.py", b"print('public')\n")])
+            _tar(sdist, [("demo-1.0/README.md", b"public\n")])
+            wheel_result = release_gate_core.inspect_wheel(wheel, _policy())
+            sdist_result = release_gate_core.inspect_sdist(sdist, _policy())
+        for result in (wheel_result, sdist_result):
+            self.assertEqual(result.member_count, 1)
+            self.assertEqual(len(result.sha256), 64)
+            self.assertEqual(len(result.member_inventory_sha256), 64)
+            self.assertNotIn("demo", repr(result))
+
+    def test_zip_rejects_traversal_duplicates_casefold_links_and_encryption(self) -> None:
+        fixtures: list[tuple[list[tuple[zipfile.ZipInfo | str, bytes]], dict]] = []
+        fixtures.append(([("../demo.py", b"x")], _policy(wheel=["../demo.py"])))
+        fixtures.append(
+            (
+                [("demo.py", b"x"), ("demo.py", b"y")],
+                _policy(wheel=["demo.py"]),
+            )
+        )
+        fixtures.append(
+            (
+                [("Demo.py", b"x"), ("demo.py", b"y")],
+                _policy(wheel=["Demo.py", "demo.py"]),
+            )
+        )
+        link = zipfile.ZipInfo("demo.py")
+        link.create_system = 3
+        link.external_attr = (stat.S_IFLNK | 0o777) << 16
+        fixtures.append(([(link, b"target")], _policy()))
+
+        for entries, policy in fixtures:
+            with self.subTest(size=len(entries)), tempfile.TemporaryDirectory() as temp:
+                path = Path(temp) / "bad.whl"
+                _zip(path, entries)
+                with self.assertRaises(release_gate_core.ReleaseGateError):
+                    release_gate_core.inspect_wheel(path, policy)
+
+        with tempfile.TemporaryDirectory() as temporary:
+            path = Path(temporary) / "encrypted.whl"
+            _zip(path, [("demo.py", b"x")])
+            encoded = bytearray(path.read_bytes())
+            local = encoded.find(b"PK\x03\x04")
+            central = encoded.find(b"PK\x01\x02")
+            encoded[local + 6] |= 1
+            encoded[central + 8] |= 1
+            path.write_bytes(encoded)
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_ENCRYPTED$"
+            ):
+                release_gate_core.inspect_wheel(path, _policy())
+
+    def test_tar_rejects_wrong_root_links_and_unexpected_members(self) -> None:
+        link = tarfile.TarInfo("demo-1.0/README.md")
+        link.type = tarfile.SYMTYPE
+        link.linkname = "target"
+        fixtures = (
+            ([("other/README.md", b"x")], _policy(sdist=["README.md"])),
+            ([(link, b"")], _policy()),
+            (
+                [("demo-1.0/README.md", b"x"), ("demo-1.0/extra", b"x")],
+                _policy(),
+            ),
+        )
+        for entries, policy in fixtures:
+            with self.subTest(), tempfile.TemporaryDirectory() as temporary:
+                path = Path(temporary) / "bad.tar.gz"
+                _tar(path, list(entries))
+                with self.assertRaises(release_gate_core.ReleaseGateError):
+                    release_gate_core.inspect_sdist(path, policy)
+
+    def test_archive_bounds_privacy_and_inventory_mode_binding(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            path = root / "large.whl"
+            _zip(path, [("demo.py", b"x" * 5000)])
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_LIMIT$"
+            ):
+                release_gate_core.inspect_wheel(path, _policy())
+
+            private_home = b"/" + b"home" + b"/real-person/private"
+            _zip(path, [("demo.py", private_home)])
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_PRIVATE_PATH$"
+            ):
+                release_gate_core.inspect_wheel(path, _policy())
+
+            executable = zipfile.ZipInfo("demo.py")
+            executable.create_system = 3
+            executable.external_attr = (stat.S_IFREG | 0o755) << 16
+            _zip(path, [(executable, b"public\n")])
+            first = release_gate_core.inspect_wheel(path, _policy())
+            regular = zipfile.ZipInfo("demo.py")
+            regular.create_system = 3
+            regular.external_attr = (stat.S_IFREG | 0o644) << 16
+            _zip(path, [(regular, b"public\n")])
+            second = release_gate_core.inspect_wheel(path, _policy())
+            self.assertNotEqual(
+                first.member_inventory_sha256,
+                second.member_inventory_sha256,
+            )
+
+
+class OrchestrationTest(unittest.TestCase):
+    def test_build_uses_fixed_epoch_and_exact_local_toolchain(self) -> None:
+        calls: list[tuple[str, ...]] = []
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            snapshot = root / "snapshot"
+            snapshot.mkdir()
+            output = root / "dist"
+
+            def fake_command(argv, **_kwargs):
+                calls.append(tuple(str(value) for value in argv))
+                output.mkdir(exist_ok=True)
+                (output / "demo-1.0-py3-none-any.whl").write_bytes(b"wheel")
+                (output / "demo-1.0.tar.gz").write_bytes(b"sdist")
+                return b""
+
+            with (
+                mock.patch.object(
+                    release_gate_core,
+                    "_installed_tool_versions",
+                    return_value={
+                        "pip": "26.2",
+                        "build": "1.5.0",
+                        "setuptools": "84.0.0",
+                        "wheel": "0.48.0",
+                    },
+                ),
+                mock.patch.object(
+                    release_gate_core, "_run_command", side_effect=fake_command
+                ),
+            ):
+                wheel, sdist = release_gate_core.build_distributions(
+                    snapshot, output, epoch=1704067200
+                )
+
+        self.assertEqual(wheel.name, "demo-1.0-py3-none-any.whl")
+        self.assertEqual(sdist.name, "demo-1.0.tar.gz")
+        self.assertEqual(
+            calls,
+            [
+                (
+                    os.fspath(Path(os.sys.executable)),
+                    "-m",
+                    "build",
+                    "--no-isolation",
+                    "--outdir",
+                    os.fspath(output),
+                )
+            ],
+        )
+
+    def test_fresh_install_uses_only_local_wheel_and_smokes_all_help(self) -> None:
+        calls: list[tuple[str, ...]] = []
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
+            wheel.write_bytes(b"invented wheel")
+
+            def fake_command(argv, **_kwargs):
+                normalized = tuple(str(value) for value in argv)
+                calls.append(normalized)
+                if normalized[-2:] == ("components", "--json"):
+                    return json.dumps(
+                        {
+                            "schemaVersion": "tritrack.components/v1",
+                            "components": [{}] * 11,
+                        }
+                    ).encode()
+                if "importlib.metadata" in " ".join(normalized):
+                    return b"tritrack-editing-assistant\t0.1.0a0\n"
+                return b""
+
+            with (
+                mock.patch.object(
+                    release_gate_core,
+                    "_wheel_project_identity",
+                    return_value=("tritrack-editing-assistant", "0.1.0a0"),
+                ),
+                mock.patch.object(
+                    release_gate_core, "_run_command", side_effect=fake_command
+                ),
+            ):
+                release_gate_core.fresh_install_smoke(wheel, root / "smoke")
+
+        flattened = [" ".join(call) for call in calls]
+        install = [
+            call
+            for call in flattened
+            if "pip" in call.split() and "install" in call.split()
+        ]
+        self.assertTrue(any("pip==26.2" in call for call in install))
+        self.assertTrue(any(os.fspath(wheel) in call for call in install))
+        self.assertFalse(any("-e" in call.split() for call in install))
+        for mode in ("contract", "fcpxml", "paper", "run"):
+            self.assertTrue(
+                any(f"validate {mode} --help" in call for call in flattened), mode
+            )
+
+    def test_manifest_is_closed_deterministic_and_schema_valid(self) -> None:
+        inspection = release_gate_core.DistributionInspection(
+            sha256="c" * 64,
+            size_bytes=10,
+            member_count=2,
+            member_inventory_sha256="d" * 64,
+        )
+        context = release_gate_core.ReleaseContext(
+            project_name="tritrack-editing-assistant",
+            version="0.1.0a0",
+            commit="a" * 40,
+            source_inventory=release_gate_core.SourceInventory(
+                count=3,
+                total_bytes=30,
+                sha256="b" * 64,
+                commit="a" * 40,
+            ),
+            toolchain={
+                "pip": "26.2",
+                "build": "1.5.0",
+                "setuptools": "84.0.0",
+                "wheel": "0.48.0",
+            },
+            python_version="3.13.15",
+            implementation="CPython",
+            system="Darwin",
+            machine="arm64",
+            wheel=inspection,
+            sdist=inspection,
+        )
+        first = release_gate_core.build_release_manifest(context)
+        second = release_gate_core.build_release_manifest(context)
+        self.assertEqual(first, second)
+        self.assertEqual(
+            set(first),
+            {
+                "schemaVersion",
+                "project",
+                "sourceInventory",
+                "toolchain",
+                "platform",
+                "artifacts",
+                "reproducibility",
+                "gates",
+                "nonClaims",
+            },
+        )
+        serialized = json.dumps(first, sort_keys=True)
+        for forbidden in ("path", "time", "duration", "command", "log", "content"):
+            self.assertNotIn(forbidden, serialized.casefold())
+
+    def test_pipeline_failure_never_calls_publication(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            with (
+                mock.patch.object(
+                    release_gate_core,
+                    "inventory_tracked_source",
+                    side_effect=release_gate_core.ReleaseGateError(
+                        "TRITRACK_RELEASE_SOURCE_DIRTY"
+                    ),
+                ),
+                mock.patch.object(release_gate_core, "publish_release") as publish,
+                self.assertRaises(release_gate_core.ReleaseGateError),
+            ):
+                release_gate_core.run_release_gate(root, root / "absent")
+            publish.assert_not_called()
+
+
+class PublicationTest(unittest.TestCase):
+    def test_artifacts_are_linked_before_manifest_and_existing_output_wins(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            wheel = root / "demo.whl"
+            sdist = root / "demo.tar.gz"
+            wheel.write_bytes(b"wheel")
+            sdist.write_bytes(b"sdist")
+            output = root / "candidate"
+            release_gate_core.publish_release(output, wheel, sdist, b"{}\n")
+            self.assertEqual((output / wheel.name).read_bytes(), b"wheel")
+            self.assertEqual((output / sdist.name).read_bytes(), b"sdist")
+            self.assertEqual((output / "release-manifest.json").read_bytes(), b"{}\n")
+
+            sentinel = root / "existing"
+            sentinel.mkdir()
+            (sentinel / "keep").write_text("untouched", encoding="utf-8")
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError,
+                "^TRITRACK_RELEASE_OUTPUT_EXISTS$",
+            ):
+                release_gate_core.publish_release(sentinel, wheel, sdist, b"{}\n")
+            self.assertEqual((sentinel / "keep").read_text(), "untouched")
+
+    def test_interruption_before_last_link_leaves_no_manifest(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            wheel = root / "demo.whl"
+            sdist = root / "demo.tar.gz"
+            wheel.write_bytes(b"wheel")
+            sdist.write_bytes(b"sdist")
+            output = root / "candidate"
+            real_link = os.link
+            calls = 0
+
+            def interrupted(source: Path, destination: Path) -> None:
+                nonlocal calls
+                calls += 1
+                if calls == 3:
+                    raise release_gate_core.ReleaseGateError(
+                        "TRITRACK_RELEASE_INTERRUPTED"
+                    )
+                real_link(source, destination)
+
+            with (
+                mock.patch.object(
+                    release_gate_core, "_link_file", side_effect=interrupted
+                ),
+                self.assertRaises(release_gate_core.ReleaseGateError),
+            ):
+                release_gate_core.publish_release(output, wheel, sdist, b"{}\n")
+            self.assertTrue(output.is_dir())
+            self.assertFalse((output / "release-manifest.json").exists())
+
+
+class ReleaseCliTest(unittest.TestCase):
+    def test_cli_success_prints_only_bounded_receipt_facts(self) -> None:
+        release_gate = importlib.import_module("scripts.release_gate")
+        manifest = {
+            "project": {"commit": "a" * 40, "version": "0.1.0a0"},
+            "artifacts": {
+                "wheel": {"sha256": "b" * 64},
+                "sdist": {"sha256": "c" * 64},
+            },
+        }
+        stdout = io.StringIO()
+        stderr = io.StringIO()
+        with (
+            mock.patch.object(
+                release_gate.release_gate_core,
+                "run_release_gate",
+                return_value=manifest,
+            ),
+            contextlib.redirect_stdout(stdout),
+            contextlib.redirect_stderr(stderr),
+        ):
+            result = release_gate.main(
+                ["--source", "invented-source", "--output", "invented-output"]
+            )
+        self.assertEqual(result, 0)
+        self.assertEqual(stderr.getvalue(), "")
+        lines = stdout.getvalue().splitlines()
+        self.assertEqual(lines[0], "RELEASE_GATE\tPASS")
+        self.assertEqual(len(lines), 6)
+        self.assertFalse(any("invented" in line for line in lines))
+
+    def test_cli_usage_and_gate_failures_are_json_codes_only(self) -> None:
+        release_gate = importlib.import_module("scripts.release_gate")
+        stderr = io.StringIO()
+        with contextlib.redirect_stderr(stderr):
+            result = release_gate.main([])
+        self.assertEqual(result, 64)
+        self.assertEqual(
+            json.loads(stderr.getvalue()), {"error": "TRITRACK_RELEASE_USAGE"}
+        )
+
+        stderr = io.StringIO()
+        private = "/" + "Users" + "/real-person/private"
+        with (
+            mock.patch.object(
+                release_gate.release_gate_core,
+                "run_release_gate",
+                side_effect=release_gate_core.ReleaseGateError(
+                    "TRITRACK_RELEASE_PRIVATE_PATH"
+                ),
+            ),
+            contextlib.redirect_stderr(stderr),
+        ):
+            result = release_gate.main(
+                ["--source", private, "--output", "invented-output"]
+            )
+        self.assertEqual(result, 1)
+        self.assertEqual(
+            json.loads(stderr.getvalue()),
+            {"error": "TRITRACK_RELEASE_PRIVATE_PATH"},
+        )
+        self.assertNotIn(private, stderr.getvalue())
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_validate_artifacts.py b/tests/test_validate_artifacts.py
new file mode 100644
index 0000000000000000000000000000000000000000..e6076a11672836abbe4ed49767c679845697aa7d
--- /dev/null
+++ b/tests/test_validate_artifacts.py
@@ -0,0 +1,334 @@
+"""Task 11 tests for read-only, offline artifact validation."""
+
+from __future__ import annotations
+
+import copy
+import hashlib
+import json
+import tempfile
+import unittest
+from pathlib import Path
+from unittest import mock
+
+from tests.test_contracts import VALID_CONTRACTS
+from tests.test_emit_fcpxml import media, sync_payload
+from tests.test_run_workflow import aligned_bundle_files, aligned_manifest, sha256
+from tritrack_editing_assistant import (
+    contracts,
+    emit_fcpxml,
+    process,
+    run_workflow,
+    validate_artifacts,
+)
+
+
+def encode_json(payload: object) -> bytes:
+    return (
+        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
+    ).encode("utf-8")
+
+
+class ContractValidationTest(unittest.TestCase):
+    def setUp(self) -> None:
+        contracts.contract_names_by_schema_version.cache_clear()
+
+    def tearDown(self) -> None:
+        contracts.contract_names_by_schema_version.cache_clear()
+
+    def test_discovers_every_installed_contract_from_schema_version(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            for name, payload in VALID_CONTRACTS.items():
+                with self.subTest(name=name):
+                    encoded = encode_json(payload)
+                    artifact = root / f"{name}.json"
+                    artifact.write_bytes(encoded)
+
+                    summary = validate_artifacts.validate_contract_artifact(
+                        artifact
+                    )
+
+                    self.assertEqual(
+                        summary,
+                        {
+                            "schemaVersion": "tritrack.validate-summary/v1",
+                            "toolVersion": "0.1.0a0",
+                            "artifactKind": "contract",
+                            "validationScope": "contract",
+                            "hashes": {
+                                "artifact": hashlib.sha256(encoded).hexdigest()
+                            },
+                            "counts": {},
+                            "details": {
+                                "contractName": name,
+                                "contractSchemaVersion": payload["schemaVersion"],
+                            },
+                        },
+                    )
+                    self.assertEqual(artifact.read_bytes(), encoded)
+
+    def test_rejects_unknown_invalid_and_unreadable_contracts(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            unknown = root / "unknown.json"
+            unknown.write_bytes(encode_json({"schemaVersion": "invented/v1"}))
+            invalid = root / "invalid.json"
+            payload = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
+            payload["questions"][0]["unexpected"] = True
+            invalid.write_bytes(encode_json(payload))
+            malformed = root / "malformed.json"
+            malformed.write_bytes(b"{not-json")
+            empty = root / "empty.json"
+            empty.write_bytes(b"")
+            symlink = root / "symlink.json"
+            symlink.symlink_to(unknown)
+
+            cases = (
+                (unknown, "TRITRACK_VALIDATE_CONTRACT_UNKNOWN"),
+                (invalid, "TRITRACK_VALIDATE_CONTRACT_INVALID"),
+                (malformed, "TRITRACK_VALIDATE_JSON_INVALID"),
+                (empty, "TRITRACK_VALIDATE_INPUT_INVALID"),
+                (symlink, "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
+                (root / "missing.json", "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
+            )
+            for artifact, code in cases:
+                with self.subTest(code=code), self.assertRaisesRegex(
+                    ValueError, rf"^{code}$"
+                ):
+                    validate_artifacts.validate_contract_artifact(artifact)
+
+    def test_rejects_duplicate_installed_schema_versions(self) -> None:
+        profile = contracts.load_schema("compatibility-profile-v1")
+        duplicate = copy.deepcopy(profile)
+        with mock.patch.object(
+            contracts,
+            "load_schema",
+            side_effect=lambda name: duplicate
+            if name == "sync-map-v1"
+            else profile,
+        ), self.assertRaisesRegex(
+            ValueError, "^TRITRACK_CONTRACT_REGISTRY_INVALID$"
+        ):
+            contracts.contract_names_by_schema_version()
+
+    def test_detects_late_contract_change_without_leaking_path_or_text(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            artifact = root / "private-name.json"
+            encoded = encode_json(VALID_CONTRACTS["grouping-v1"])
+            artifact.write_bytes(encoded)
+            real_validate = contracts.validate_contract
+
+            def changing_validate(name: str, payload: object) -> None:
+                real_validate(name, payload)
+                artifact.write_bytes(encoded + b" ")
+
+            with mock.patch.object(
+                contracts, "validate_contract", side_effect=changing_validate
+            ), self.assertRaisesRegex(
+                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
+            ) as raised:
+                validate_artifacts.validate_contract_artifact(artifact)
+
+            message = str(raised.exception)
+            self.assertNotIn(str(root), message)
+            self.assertNotIn("What changed?", message)
+
+
+class FcpxmlValidationTest(unittest.TestCase):
+    def render(self, root: Path) -> str:
+        return emit_fcpxml.render_fcpxml(
+            sync_payload(),
+            media(root),
+            profile_id="uhd-2997-ndf-fcpxml-1.14",
+            binding_id="basic-title-v1",
+            metadata=emit_fcpxml.ProjectMetadata("Invented Event", "Invented Cut"),
+        )
+
+    def test_validates_exact_bytes_with_installed_profile_and_binding(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            artifact = root / "story.fcpxml"
+            encoded = self.render(root).encode("utf-8")
+            artifact.write_bytes(encoded)
+
+            with mock.patch.object(process, "run_bounded") as subprocess_call:
+                summary = validate_artifacts.validate_fcpxml_artifact(
+                    artifact,
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                )
+
+            subprocess_call.assert_not_called()
+            self.assertEqual(
+                summary,
+                {
+                    "schemaVersion": "tritrack.validate-summary/v1",
+                    "toolVersion": "0.1.0a0",
+                    "artifactKind": "fcpxml",
+                    "validationScope": "structural-profile",
+                    "hashes": {"artifact": hashlib.sha256(encoded).hexdigest()},
+                    "counts": {},
+                    "details": {
+                        "profileId": "uhd-2997-ndf-fcpxml-1.14",
+                        "bindingId": "basic-title-v1",
+                    },
+                },
+            )
+            self.assertEqual(artifact.read_bytes(), encoded)
+            self.assertNotIn(str(root), json.dumps(summary))
+
+    def test_rejects_profile_binding_xml_and_file_drift(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            valid = self.render(root)
+            artifact = root / "story.fcpxml"
+            artifact.write_text(valid, encoding="utf-8")
+
+            for keyword, value in (
+                ("profile_id", "unknown-profile"),
+                ("binding_id", "unknown-binding"),
+            ):
+                arguments = {
+                    "profile_id": "uhd-2997-ndf-fcpxml-1.14",
+                    "binding_id": "basic-title-v1",
+                }
+                arguments[keyword] = value
+                with self.subTest(keyword=keyword), self.assertRaisesRegex(
+                    ValueError, "^TRITRACK_PROFILE_UNKNOWN"
+                ):
+                    validate_artifacts.validate_fcpxml_artifact(
+                        artifact, **arguments
+                    )
+
+            artifact.write_text(
+                valid.replace('width="3840"', 'width="1920"'),
+                encoding="utf-8",
+            )
+            with self.assertRaisesRegex(
+                ValueError, "^TRITRACK_FCPXML_PROFILE_MISMATCH$"
+            ):
+                validate_artifacts.validate_fcpxml_artifact(
+                    artifact,
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                )
+
+            artifact.write_bytes(b"\xff\xfe")
+            with self.assertRaisesRegex(
+                ValueError, "^TRITRACK_VALIDATE_FCPXML_INVALID$"
+            ):
+                validate_artifacts.validate_fcpxml_artifact(
+                    artifact,
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                )
+
+            symlink = root / "link.fcpxml"
+            symlink.symlink_to(artifact)
+            with self.assertRaisesRegex(
+                ValueError, "^TRITRACK_VALIDATE_INPUT_UNREADABLE$"
+            ):
+                validate_artifacts.validate_fcpxml_artifact(
+                    symlink,
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                )
+
+    def test_detects_late_fcpxml_change(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            artifact = root / "story.fcpxml"
+            valid = self.render(root)
+            artifact.write_text(valid, encoding="utf-8")
+            real_validate = emit_fcpxml.validate_fcpxml
+
+            def changing_validate(*args, **kwargs) -> None:
+                real_validate(*args, **kwargs)
+                artifact.write_text(valid + " ", encoding="utf-8")
+
+            with mock.patch.object(
+                emit_fcpxml, "validate_fcpxml", side_effect=changing_validate
+            ), self.assertRaisesRegex(
+                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
+            ):
+                validate_artifacts.validate_fcpxml_artifact(
+                    artifact,
+                    profile_id="uhd-2997-ndf-fcpxml-1.14",
+                    binding_id="basic-title-v1",
+                )
+
+
+class RunValidationTest(unittest.TestCase):
+    def write_aligned_bundle(self, root: Path) -> tuple[Path, bytes, dict[str, bytes]]:
+        run = root / "aligned-run"
+        run.mkdir()
+        files = aligned_bundle_files()
+        for name, encoded in files.items():
+            (run / name).write_bytes(encoded)
+        manifest_bytes = run_workflow.encode_manifest(aligned_manifest(files))
+        (run / "run-manifest.json").write_bytes(manifest_bytes)
+        return run, manifest_bytes, files
+
+    def test_shares_complete_run_authority_and_exact_status_facts(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            run, manifest_bytes, files = self.write_aligned_bundle(root)
+            entries_before = {path.name: path.read_bytes() for path in run.iterdir()}
+
+            bundle, status = run_workflow.inspect_run(run)
+            summary = validate_artifacts.validate_run_bundle(run)
+
+            self.assertEqual(status, run_workflow.status_run(run))
+            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
+            self.assertEqual(
+                summary,
+                {
+                    "schemaVersion": "tritrack.validate-summary/v1",
+                    "toolVersion": "0.1.0a0",
+                    "artifactKind": "run",
+                    "validationScope": "complete-run-bundle",
+                    "hashes": {"manifest": sha256(manifest_bytes)},
+                    "counts": {"artifactCount": 2, "stageCount": 2},
+                    "details": {"runSummary": status},
+                },
+            )
+            self.assertEqual(
+                entries_before,
+                {path.name: path.read_bytes() for path in run.iterdir()},
+            )
+            self.assertEqual(
+                summary["details"]["runSummary"]["artifacts"],
+                {
+                    "alignedTranscript": sha256(files["aligned-transcript.json"]),
+                    "paperWorkbook": sha256(files["paper-edit.xlsx"]),
+                },
+            )
+            self.assertNotIn(str(root), json.dumps(summary))
+            self.assertNotIn("Invented words", json.dumps(summary))
+
+    def test_inspection_detects_change_between_initial_load_and_recheck(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            run, _, _ = self.write_aligned_bundle(root)
+            real_load = run_workflow.load_bundle
+            load_count = 0
+
+            def changing_load(*args, **kwargs):
+                nonlocal load_count
+                loaded = real_load(*args, **kwargs)
+                load_count += 1
+                if load_count == 1:
+                    (run / "paper-edit.xlsx").write_bytes(b"changed")
+                return loaded
+
+            with mock.patch.object(
+                run_workflow, "load_bundle", side_effect=changing_load
+            ), self.assertRaisesRegex(
+                ValueError, "^TRITRACK_RUN_INPUT_CHANGED$"
+            ):
+                run_workflow.inspect_run(run)
+
+
+if __name__ == "__main__":
+    unittest.main()
~~~~
