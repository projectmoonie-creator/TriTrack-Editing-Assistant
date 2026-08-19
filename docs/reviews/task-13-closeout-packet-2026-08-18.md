# Task 13 generic-authority seam closeout review packet

## Review target and packet provenance

- Repository: projectmoonie-creator/TriTrack-Editing-Assistant
- Project identity: public-engine / OSS
- Starting public main: 7bc035ee379a8a3babd2a6556eecdab2973b6301
- Exact review target: 9c9ee9c7c75254c507e9984c27b9a4195273d21c
- Package version: 0.1.0a0
- Target worktree was clean before packet construction.
- The packet SHA-256 is recorded after these exact bytes are frozen. Do not
  infer it from this sentence.

## Objective

Review whether Task 13 proves that the public engine remains the generic
authority while exposing one intentional, narrow downstream integration seam.
Return only current, actionable defects in this exact target. This is a
read-only convergence review: make no edit, test, build, network request,
provider call, tag, release, publication, or private integration.

## Selected design and authority boundary

The producer selected Option A. Existing versioned artifacts and installed
`tritrack validate ... --json` processes are the exclusive supported v1
downstream seam. Internal Python modules are implementation details. Task 13
does not add a stable Python facade, plugin loader, discovery protocol, network
service, new engine contract, or second authority.

The standard-library reference consumer runs out of tree, invokes installed
`tritrack validate contract --json`, accepts only the exact validation
summary, contract, schema, and scope it knows, binds the validator hash to the
exact regular-file bytes it reads, derives only take and cue counts, repeats
validation before publication, and writes an absent downstream-owned
`example.*` sidecar. The sidecar is never engine authority.

The release gate copies the consumer and invented fixture outside the source
snapshot and runs them with isolated Python and the CLI from a fresh wheel-only
installation. The wheel member set remains 38. The closed release manifest
records `downstreamSeam: pass`.

## Required invariants to challenge

1. The reference consumer must not import engine internals or duplicate an
   engine validation rule.
2. Unknown summary／contract versions, wrong scopes, hash mismatches, changed
   second validation, invalid inputs, and existing outputs must fail closed.
3. Success output must be canonical, path-free, transcript-text-free,
   namespaced downstream data bound to exact engine authority.
4. The release gate must execute the copied proof against the fresh installed
   wheel and must fail unless the exact receipt matches the invented fixture.
5. The proof may enter the sdist but must not change wheel runtime membership
   or the eleven-component registry.
6. Public docs, packaging, CI, manifest schema, and implementation must agree
   about the seam and its non-claims.
7. No private project content, media, subtitle, credential, path, proprietary
   template, or private integration may enter this public repository.

## Verification evidence

- Baseline before Task 13: 252 tests passed.
- Consumer RED: the script was absent. Consumer GREEN: 5 tests passed.
- Release integration RED: missing source parameter, named gate, and manifest
  schema. Focused GREEN: 30 tests passed.
- Packaging／CI RED: three missing declarations. Focused GREEN: 13 tests
  passed.
- Coherent target: all 259 tests passed in 22.265 seconds; Ruff, compileall,
  project identity, 11 governance tests, package policy, CI policy, and
  `git diff --check` passed.
- The clean maintainer release gate passed at the exact target. Its first
  sandboxed invocation was environment-incomplete because DNS was unavailable;
  the same clean target passed when the fresh environment could install public
  dependencies. No source change was made for that environmental failure.

## Exact target release manifest

~~~json
{"artifacts":{"sdist":{"memberCount":109,"memberInventorySha256":"08f20f5bf2df7e80f48080f5d57855d078bdabdd257ce67546cd99421c1b6aca","sha256":"5f336972fc8ed206a863fafd20b31443322d7552335017f33a2c6949cef88681","sizeBytes":191964},"wheel":{"memberCount":38,"memberInventorySha256":"782660ec1e7bd66a9e07f9b27f57bc5b3641431f489e84114e9303d4e9fc4739","sha256":"7aeea40d7102bd0eb8b8059100d1d5880d2715662ea26fdb44323ad93cf4f785","sizeBytes":86582}},"gates":{"downstreamSeam":"pass","freshInstall":"pass","sdistArchive":"pass","sourceIdentity":"pass","sourcePrivacy":"pass","wheelArchive":"pass"},"nonClaims":["no-tag","no-release","no-package-publication","no-pull-request","no-tester-contact","no-signing","no-attestation","no-sbom","no-final-cut-gui","no-dtd","no-provider","no-application-submission"],"platform":{"machine":"arm64","system":"Darwin"},"project":{"commit":"9c9ee9c7c75254c507e9984c27b9a4195273d21c","name":"tritrack-editing-assistant","version":"0.1.0a0"},"reproducibility":{"sdistMembersMatch":true,"wheelBytesMatch":true},"schemaVersion":"tritrack.release-manifest/v1","sourceInventory":{"count":153,"sha256":"b49f3d4a1c2ac72dabb8ed5c84092444c648f6113bb80e3936cb4731960d428f"},"toolchain":{"build":"1.5.0","implementation":"CPython","pip":"26.2","python":"3.13.15","setuptools":"84.0.0","wheel":"0.48.0"}}
~~~

## Brainstorm provenance

The design packet SHA-256 was
`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`.
Codex completed independently first. Gemini requested, observed, and completed
`gemini-3.7-flash`. Claude's one subscription-only attempt
`d13e8a66-75a2-4342-a7e9-c65844a60458` requested the dynamic `opus`
capability alias and ended `claude-timeout` with no observed／completed model
and ambiguous dispatch. It was not retried, downgraded, substituted, or sent
through a paid API.

## Requested review dimensions

1. authority ownership and non-authority of the example sidecar;
2. exact-byte binding, TOCTOU revalidation, no-overwrite publication, bounded
   inputs, stable errors, and path／content privacy;
3. subprocess boundary, exact validation summary checks, and compatibility
   semantics for unknown versions;
4. fresh-wheel isolation, snapshot copying, exact receipt verification, and
   named release-manifest gate;
5. sdist／wheel policy, fixed CI cells, registry stability, and public docs;
6. missing tests, contradictory claims, or any evidence that a new public API
   is actually required.

## Finding schema

Return:

- Summary: `NO FINDINGS` or count by severity.
- Findings, each with stable ID, blocker／major／minor severity, confidence,
  current file and line, exact failure mechanism, impact, smallest safe fix,
  and a test or reproduction.
- Optional observations in a separate non-blocking section.
- Inspection record naming only files and packet sections actually inspected.

A blocker or major finding requires current file-and-line evidence or a
reproducible failing contract. Do not turn a historical timeout, a non-goal,
or a hypothetical private consumer into a finding.

## Explicit no-edit and non-goal boundary

No tag, GitHub Release, package publication, pull request, tester contact,
signing, attestation, SBOM, Final Cut GUI result, DTD result, live provider,
application submission, private integration, production-stability claim,
force-push, remote change, or visibility change is in scope.

## Changed-file inventory

~~~text
M	.github/workflows/ci.yml
M	MANIFEST.in
M	README.md
M	STATUS.md
M	docs/ROADMAP.md
A	docs/TASK-13-DECISION.md
A	docs/TASK-13-VERIFICATION.md
M	docs/TOOLING.md
A	docs/reviews/task-13-brainstorm-claude-2026-08-18.md.status.json
A	docs/reviews/task-13-brainstorm-codex-2026-08-18.md
A	docs/reviews/task-13-brainstorm-gemini-2026-08-18.md
A	docs/reviews/task-13-brainstorm-gemini-2026-08-18.md.status.json
A	docs/reviews/task-13-brainstorm-packet-2026-08-18.md
A	docs/reviews/task-13-brainstorm-synthesis-2026-08-18.md
A	docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
A	examples/downstream_fixture/aligned-transcript.json
A	examples/downstream_seam.py
M	release/package-policy-v1.json
M	release/release-manifest-v1.schema.json
M	scripts/release_gate_core.py
A	tests/test_downstream_seam.py
M	tests/test_maintainer_boundary.py
M	tests/test_packaging.py
M	tests/test_release_ci.py
M	tests/test_release_gate.py
~~~

## Exact current contents of every changed runtime, gate, policy, CI, and test file

### .github/workflows/ci.yml

~~~text
name: Release-grade public Python CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test-matrix:
    name: ${{ matrix.os }} / Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-24.04
            python-version: "3.12"
            architecture: x64
          - os: ubuntu-24.04
            python-version: "3.13"
            architecture: x64
          - os: macos-26
            python-version: "3.12"
            architecture: arm64
          - os: macos-26
            python-version: "3.13"
            architecture: arm64
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up fixed Python cell
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: ${{ matrix.python-version }}
          architecture: ${{ matrix.architecture }}
      - name: Install constrained source and development checks
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Run complete public tests
        run: python -m unittest discover -s tests -v
      - name: Compile public Python surfaces
        run: python -m compileall -q src tests examples scripts
      - name: Build and smoke the local wheel in a new environment
        shell: bash
        run: |
          wheel_dir="$RUNNER_TEMP/tritrack-wheel-dist"
          smoke_dir="$RUNNER_TEMP/tritrack-wheel-smoke"
          test ! -e "$wheel_dir"
          test ! -e "$smoke_dir"
          python -m build --wheel --no-isolation --outdir "$wheel_dir"
          python -m venv "$smoke_dir"
          smoke_python="$smoke_dir/bin/python"
          smoke_cli="$smoke_dir/bin/tritrack"
          "$smoke_python" -m pip install --constraint requirements/ci-constraints.txt pip
          wheels=("$wheel_dir"/*.whl)
          test "${#wheels[@]}" -eq 1
          "$smoke_python" -m pip install "${wheels[0]}"
          "$smoke_python" -m pip check
          "$smoke_cli" components --json
          "$smoke_cli" validate --help
          "$smoke_cli" validate contract --help
          "$smoke_cli" validate fcpxml --help
          "$smoke_cli" validate paper --help
          "$smoke_cli" validate run --help
          downstream_dir="$RUNNER_TEMP/tritrack-downstream-seam"
          test ! -e "$downstream_dir"
          mkdir "$downstream_dir"
          cp examples/downstream_seam.py "$downstream_dir/downstream_seam.py"
          cp examples/downstream_fixture/aligned-transcript.json "$downstream_dir/aligned-transcript.json"
          "$smoke_python" -I "$downstream_dir/downstream_seam.py" \
            --tritrack "$smoke_cli" \
            --aligned "$downstream_dir/aligned-transcript.json" \
            --output "$downstream_dir/downstream-receipt.json"

  quality:
    name: Public quality and policy contracts
    runs-on: ubuntu-24.04
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python 3.13
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: "3.13"
          architecture: x64
      - name: Install constrained source and development checks
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Lint every public Python surface
        run: ruff check src tests examples scripts
      - name: Verify public role, package, and CI contracts
        run: python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v
      - name: Verify public project identity
        run: python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .

  release-gate:
    name: Local candidate gate without publication
    runs-on: ubuntu-24.04
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python 3.13
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: "3.13"
          architecture: x64
      - name: Install exact gate toolchain
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Run the maintainer release-readiness gate locally
        run: |
          mkdir -p .release-evidence
          python scripts/release_gate.py --source . --output .release-evidence/ci
~~~

### MANIFEST.in

~~~text
include README.md
include LICENSE
include NOTICE
include CHANGELOG.md
include CONTRIBUTING.md
include SECURITY.md
include CODE_OF_CONDUCT.md
include pyproject.toml
include MANIFEST.in
include .github/workflows/ci.yml
include docs/ROADMAP.md
include docs/TASK-11-VERIFICATION.md
include docs/TASK-13-DECISION.md
include docs/TASK-13-VERIFICATION.md
include docs/TOOLING.md
include docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
recursive-include examples *.py *.json
recursive-include skills/tritrack-editing-assistant *.md *.yaml
include scripts/capture_basic_title_binding.py
include scripts/release_gate.py
include scripts/release_gate_core.py
recursive-include release *.json
recursive-include requirements *.txt
recursive-include src/tritrack_editing_assistant *.py *.json *.mjs
recursive-include tests *.py
exclude tests/test_maintainer_boundary.py
prune .agents
prune .release-evidence
prune build
prune dist
prune docs/reviews
prune docs/superpowers/plans
global-exclude *.py[cod]
global-exclude .DS_Store
global-exclude __pycache__
~~~

### examples/downstream_fixture/aligned-transcript.json

~~~text
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
~~~

### examples/downstream_seam.py

~~~text
"""Black-box example of TriTrack's supported downstream process seam."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import NoReturn

MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
VALIDATE_SUMMARY_SCHEMA = "tritrack.validate-summary/v1"
ALIGNED_CONTRACT = "aligned-transcript-v1"
ALIGNED_SCHEMA = "tritrack.aligned-transcript/v1"


class DownstreamError(ValueError):
    """A stable, path-free error suitable for example automation."""


def _canonical_json(payload: Mapping[str, object]) -> bytes:
    return (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def _read_regular(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= MAX_ARTIFACT_BYTES
        ):
            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(MAX_ARTIFACT_BYTES + 1)
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(encoded) > MAX_ARTIFACT_BYTES:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    return encoded


def _validate(tritrack: Path, aligned: Path) -> dict[str, object]:
    try:
        result = subprocess.run(
            [
                os.fspath(tritrack),
                "validate",
                "contract",
                "--artifact",
                os.fspath(aligned),
                "--json",
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise DownstreamError(
            "DOWNSTREAM_ENGINE_VALIDATION_FAILED"
        ) from error
    if result.returncode != 0 or result.stderr:
        raise DownstreamError("DOWNSTREAM_ENGINE_VALIDATION_FAILED")
    try:
        decoded = result.stdout.decode("utf-8", errors="strict")
        summary = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID") from error
    if not isinstance(summary, dict):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    if (
        summary.get("schemaVersion") != VALIDATE_SUMMARY_SCHEMA
        or summary.get("artifactKind") != "contract"
        or summary.get("validationScope") != "contract"
        or summary.get("details")
        != {
            "contractName": ALIGNED_CONTRACT,
            "contractSchemaVersion": ALIGNED_SCHEMA,
        }
    ):
        raise DownstreamError("DOWNSTREAM_ENGINE_SCOPE_INVALID")
    hashes = summary.get("hashes")
    if not isinstance(hashes, dict):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    artifact_hash = hashes.get("artifact")
    if (
        not isinstance(artifact_hash, str)
        or len(artifact_hash) != 64
        or any(character not in "0123456789abcdef" for character in artifact_hash)
    ):
        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
    return summary


def _observe(encoded: bytes) -> tuple[int, int]:
    try:
        artifact = json.loads(encoded.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
    if not isinstance(artifact, dict) or artifact.get("schemaVersion") != ALIGNED_SCHEMA:
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    takes = artifact.get("takes")
    if not isinstance(takes, list):
        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
    cue_count = 0
    for take in takes:
        if not isinstance(take, dict) or not isinstance(take.get("cues"), list):
            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
        cue_count += len(take["cues"])
    return len(takes), cue_count


def _publish_absent(path: Path, payload: Mapping[str, object]) -> None:
    parent = path.parent
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            dir=parent,
            prefix=f".{path.name}.",
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(_canonical_json(payload))
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary_path, path, follow_symlinks=False)
    except FileExistsError as error:
        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS") from error
    except OSError as error:
        raise DownstreamError("DOWNSTREAM_OUTPUT_INVALID") from error
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def _artifact_hash(summary: Mapping[str, object]) -> str:
    hashes = summary["hashes"]
    assert isinstance(hashes, dict)
    artifact_hash = hashes["artifact"]
    assert isinstance(artifact_hash, str)
    return artifact_hash


def _run(tritrack: Path, aligned: Path, output: Path) -> dict[str, object]:
    if os.path.lexists(output):
        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS")

    first_summary = _validate(tritrack, aligned)
    encoded = _read_regular(aligned)
    artifact_sha256 = hashlib.sha256(encoded).hexdigest()
    if _artifact_hash(first_summary) != artifact_sha256:
        raise DownstreamError("DOWNSTREAM_ENGINE_HASH_MISMATCH")

    take_count, cue_count = _observe(encoded)
    second_summary = _validate(tritrack, aligned)
    if second_summary != first_summary:
        raise DownstreamError("DOWNSTREAM_ENGINE_CHANGED")

    receipt: dict[str, object] = {
        "schemaVersion": "example.tritrack-downstream-receipt/v1",
        "engineAuthority": {
            "artifactSha256": artifact_sha256,
            "contractName": ALIGNED_CONTRACT,
            "contractSchemaVersion": ALIGNED_SCHEMA,
            "validationScope": "contract",
        },
        "derivedObservation": {
            "takeCount": take_count,
            "cueCount": cue_count,
        },
    }
    _publish_absent(output, receipt)
    return {
        "schemaVersion": "example.tritrack-downstream-summary/v1",
        "artifactSha256": artifact_sha256,
        "takeCount": take_count,
        "cueCount": cue_count,
    }


def _fail(error: DownstreamError) -> NoReturn:
    sys.stderr.buffer.write(_canonical_json({"error": str(error)}))
    raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prove the public TriTrack CLI/artifact downstream seam."
    )
    parser.add_argument("--tritrack", required=True, type=Path)
    parser.add_argument("--aligned", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        summary = _run(arguments.tritrack, arguments.aligned, arguments.output)
    except DownstreamError as error:
        _fail(error)
    sys.stdout.buffer.write(_canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~

### release/package-policy-v1.json

~~~text
{
  "schemaVersion": "tritrack.package-policy/v1",
  "build": {
    "sourceDateEpoch": 1704067200
  },
  "limits": {
    "sourceMaxFiles": 4096,
    "sourceMaxFileBytes": 2097152,
    "sourceMaxTotalBytes": 134217728,
    "archiveMaxBytes": 67108864,
    "archiveMaxMembers": 2048,
    "memberMaxBytes": 33554432,
    "expandedMaxBytes": 268435456
  },
  "source": {
    "allowedFakeHomeUsers": [
      "editor",
      "example",
      "fake",
      "test"
    ],
    "allowedFakeSecretValues": [
      "example",
      "fake",
      "placeholder",
      "redacted",
      "secret",
      "test"
    ],
    "forbiddenSuffixes": [
      ".aac",
      ".aif",
      ".aiff",
      ".avi",
      ".fcpxmld",
      ".m4a",
      ".m4v",
      ".mkv",
      ".mov",
      ".mp3",
      ".mp4",
      ".wav",
      ".xlsx"
    ]
  },
  "wheel": {
    "expectedMembers": [
      "tritrack_editing_assistant-0.1.0a0.dist-info/METADATA",
      "tritrack_editing_assistant-0.1.0a0.dist-info/RECORD",
      "tritrack_editing_assistant-0.1.0a0.dist-info/WHEEL",
      "tritrack_editing_assistant-0.1.0a0.dist-info/entry_points.txt",
      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/LICENSE",
      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/NOTICE",
      "tritrack_editing_assistant-0.1.0a0.dist-info/top_level.txt",
      "tritrack_editing_assistant/__init__.py",
      "tritrack_editing_assistant/align_text.py",
      "tritrack_editing_assistant/cli.py",
      "tritrack_editing_assistant/contracts.py",
      "tritrack_editing_assistant/doctor.py",
      "tritrack_editing_assistant/emit_fcpxml.py",
      "tritrack_editing_assistant/gemini_hybrid.py",
      "tritrack_editing_assistant/hallucination.py",
      "tritrack_editing_assistant/organizer.py",
      "tritrack_editing_assistant/paper_edit.py",
      "tritrack_editing_assistant/process.py",
      "tritrack_editing_assistant/profiles/__init__.py",
      "tritrack_editing_assistant/profiles/basic-title-v1.json",
      "tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
      "tritrack_editing_assistant/run_workflow.py",
      "tritrack_editing_assistant/schemas/__init__.py",
      "tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
      "tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
      "tritrack_editing_assistant/schemas/grouping-v1.schema.json",
      "tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
      "tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
      "tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
      "tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
      "tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
      "tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
      "tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
      "tritrack_editing_assistant/story_fcpxml.py",
      "tritrack_editing_assistant/string_out.py",
      "tritrack_editing_assistant/sync_scan.py",
      "tritrack_editing_assistant/transcribe_takes.py",
      "tritrack_editing_assistant/validate_artifacts.py"
    ]
  },
  "sdist": {
    "root": "tritrack_editing_assistant-0.1.0a0/",
    "expectedMembers": [
      ".github/workflows/ci.yml",
      "CHANGELOG.md",
      "CODE_OF_CONDUCT.md",
      "CONTRIBUTING.md",
      "LICENSE",
      "MANIFEST.in",
      "NOTICE",
      "PKG-INFO",
      "README.md",
      "SECURITY.md",
      "docs/ROADMAP.md",
      "docs/TASK-11-VERIFICATION.md",
      "docs/TASK-13-DECISION.md",
      "docs/TASK-13-VERIFICATION.md",
      "docs/TOOLING.md",
      "docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md",
      "examples/downstream_fixture/aligned-transcript.json",
      "examples/downstream_seam.py",
      "examples/quickstart_demo.py",
      "pyproject.toml",
      "release/package-policy-v1.json",
      "release/release-manifest-v1.schema.json",
      "requirements/ci-constraints.txt",
      "scripts/capture_basic_title_binding.py",
      "scripts/release_gate.py",
      "scripts/release_gate_core.py",
      "setup.cfg",
      "skills/tritrack-editing-assistant/SKILL.md",
      "skills/tritrack-editing-assistant/agents/openai.yaml",
      "src/tritrack_editing_assistant.egg-info/PKG-INFO",
      "src/tritrack_editing_assistant.egg-info/SOURCES.txt",
      "src/tritrack_editing_assistant.egg-info/dependency_links.txt",
      "src/tritrack_editing_assistant.egg-info/entry_points.txt",
      "src/tritrack_editing_assistant.egg-info/requires.txt",
      "src/tritrack_editing_assistant.egg-info/top_level.txt",
      "src/tritrack_editing_assistant/__init__.py",
      "src/tritrack_editing_assistant/align_text.py",
      "src/tritrack_editing_assistant/cli.py",
      "src/tritrack_editing_assistant/contracts.py",
      "src/tritrack_editing_assistant/doctor.py",
      "src/tritrack_editing_assistant/emit_fcpxml.py",
      "src/tritrack_editing_assistant/gemini_hybrid.py",
      "src/tritrack_editing_assistant/hallucination.py",
      "src/tritrack_editing_assistant/organizer.py",
      "src/tritrack_editing_assistant/paper_edit.py",
      "src/tritrack_editing_assistant/process.py",
      "src/tritrack_editing_assistant/profiles/__init__.py",
      "src/tritrack_editing_assistant/profiles/basic-title-v1.json",
      "src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
      "src/tritrack_editing_assistant/run_workflow.py",
      "src/tritrack_editing_assistant/schemas/__init__.py",
      "src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/grouping-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
      "src/tritrack_editing_assistant/story_fcpxml.py",
      "src/tritrack_editing_assistant/string_out.py",
      "src/tritrack_editing_assistant/sync_scan.py",
      "src/tritrack_editing_assistant/transcribe_takes.py",
      "src/tritrack_editing_assistant/validate_artifacts.py",
      "tests/task9_fixtures.py",
      "tests/test_align_text.py",
      "tests/test_cli.py",
      "tests/test_contracts.py",
      "tests/test_doctor.py",
      "tests/test_downstream_seam.py",
      "tests/test_emit_fcpxml.py",
      "tests/test_gemini_hybrid.py",
      "tests/test_hallucination.py",
      "tests/test_organizer.py",
      "tests/test_packaging.py",
      "tests/test_paper_edit.py",
      "tests/test_process.py",
      "tests/test_quickstart_demo.py",
      "tests/test_release_gate.py",
      "tests/test_release_ci.py",
      "tests/test_run_workflow.py",
      "tests/test_story_fcpxml.py",
      "tests/test_string_out.py",
      "tests/test_sync_scan.py",
      "tests/test_title_binding.py",
      "tests/test_transcribe_takes.py",
      "tests/test_validate_artifacts.py"
    ]
  }
}
~~~

### release/release-manifest-v1.schema.json

~~~text
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.example/schemas/release-manifest-v1.schema.json",
  "title": "TriTrack release manifest v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "project",
    "sourceInventory",
    "toolchain",
    "platform",
    "artifacts",
    "reproducibility",
    "gates",
    "nonClaims"
  ],
  "properties": {
    "schemaVersion": {
      "const": "tritrack.release-manifest/v1"
    },
    "project": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "version", "commit"],
      "properties": {
        "name": {"const": "tritrack-editing-assistant"},
        "version": {"type": "string", "minLength": 1},
        "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"}
      }
    },
    "sourceInventory": {
      "type": "object",
      "additionalProperties": false,
      "required": ["count", "sha256"],
      "properties": {
        "count": {"type": "integer", "minimum": 1},
        "sha256": {"$ref": "#/$defs/sha256"}
      }
    },
    "toolchain": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "python",
        "implementation",
        "pip",
        "build",
        "setuptools",
        "wheel"
      ],
      "properties": {
        "python": {"type": "string", "minLength": 1},
        "implementation": {"const": "CPython"},
        "pip": {"type": "string", "minLength": 1},
        "build": {"type": "string", "minLength": 1},
        "setuptools": {"type": "string", "minLength": 1},
        "wheel": {"type": "string", "minLength": 1}
      }
    },
    "platform": {
      "type": "object",
      "additionalProperties": false,
      "required": ["system", "machine"],
      "properties": {
        "system": {"enum": ["Darwin", "Linux"]},
        "machine": {"enum": ["arm64", "x86_64"]}
      }
    },
    "artifacts": {
      "type": "object",
      "additionalProperties": false,
      "required": ["wheel", "sdist"],
      "properties": {
        "wheel": {"$ref": "#/$defs/artifact"},
        "sdist": {"$ref": "#/$defs/artifact"}
      }
    },
    "reproducibility": {
      "type": "object",
      "additionalProperties": false,
      "required": ["wheelBytesMatch", "sdistMembersMatch"],
      "properties": {
        "wheelBytesMatch": {"const": true},
        "sdistMembersMatch": {"const": true}
      }
    },
    "gates": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sourceIdentity",
        "sourcePrivacy",
        "wheelArchive",
        "sdistArchive",
        "freshInstall",
        "downstreamSeam"
      ],
      "properties": {
        "sourceIdentity": {"const": "pass"},
        "sourcePrivacy": {"const": "pass"},
        "wheelArchive": {"const": "pass"},
        "sdistArchive": {"const": "pass"},
        "freshInstall": {"const": "pass"},
        "downstreamSeam": {"const": "pass"}
      }
    },
    "nonClaims": {
      "type": "array",
      "minItems": 2,
      "uniqueItems": true,
      "items": {
        "enum": [
          "no-tag",
          "no-release",
          "no-package-publication",
          "no-pull-request",
          "no-tester-contact",
          "no-signing",
          "no-attestation",
          "no-sbom",
          "no-final-cut-gui",
          "no-dtd",
          "no-provider",
          "no-application-submission"
        ]
      }
    }
  },
  "$defs": {
    "sha256": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "artifact": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sha256",
        "sizeBytes",
        "memberCount",
        "memberInventorySha256"
      ],
      "properties": {
        "sha256": {"$ref": "#/$defs/sha256"},
        "sizeBytes": {"type": "integer", "minimum": 1},
        "memberCount": {"type": "integer", "minimum": 1},
        "memberInventorySha256": {"$ref": "#/$defs/sha256"}
      }
    }
  }
}
~~~

### scripts/release_gate_core.py

~~~text
"""Bounded, fail-closed primitives for the maintainer release gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import io
import json
import os
import platform
import re
import selectors
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import unicodedata
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

import jsonschema

_COMMAND_TIMEOUT_SECONDS = 30
_COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
_POLICY_LIMIT = 1024 * 1024
_ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
_ALLOWED_FAKE_SECRETS = frozenset(
    {b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
)
_READ_CHUNK_BYTES = 64 * 1024
_TERMINATION_GRACE_SECONDS = 0.2


class ReleaseGateError(Exception):
    """One stable public-safe release-gate failure code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class SourceInventory:
    count: int
    total_bytes: int
    sha256: str
    commit: str


@dataclass(frozen=True)
class DistributionInspection:
    sha256: str
    size_bytes: int
    member_count: int
    member_inventory_sha256: str


@dataclass(frozen=True)
class ReleaseContext:
    project_name: str
    version: str
    commit: str
    source_inventory: SourceInventory
    toolchain: Mapping[str, str]
    python_version: str
    implementation: str
    system: str
    machine: str
    wheel: DistributionInspection
    sdist: DistributionInspection


@dataclass(frozen=True)
class _BoundedCommandResult:
    status: str
    returncode: int | None
    stdout: bytes
    stderr: bytes


def _fail(code: str) -> None:
    raise ReleaseGateError(code)


def _safe_environment() -> dict[str, str]:
    return {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except OSError:
            if process.poll() is None:
                process.terminate()
    elif process.poll() is None:
        process.terminate()

    try:
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        pass

    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            if process.poll() is None:
                process.kill()
    elif process.poll() is None:
        process.kill()

    if process.poll() is None:
        process.wait()


def _close_process_pipes(process: subprocess.Popen[bytes]) -> None:
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()


def _run_bounded_subprocess(
    argv: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout: int,
    output_limit: int,
) -> _BoundedCommandResult:
    """Run one argv-only child while bounding combined retained output."""

    if timeout < 1 or output_limit < 1:
        return _BoundedCommandResult("invalid", None, b"", b"")
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=dict(env),
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError:
        return _BoundedCommandResult("spawn_error", None, b"", b"")

    deadline = time.monotonic() + timeout
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    captured = 0
    status = "ok"
    try:
        with selectors.DefaultSelector() as selector:
            assert process.stdout is not None
            assert process.stderr is not None
            selector.register(process.stdout, selectors.EVENT_READ, stdout_chunks)
            selector.register(process.stderr, selectors.EVENT_READ, stderr_chunks)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    status = "timeout"
                    break
                for key, _mask in selector.select(timeout=min(remaining, 0.05)):
                    allowed_read = output_limit - captured + 1
                    chunk = os.read(
                        key.fd,
                        min(_READ_CHUNK_BYTES, max(1, allowed_read)),
                    )
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    captured += len(chunk)
                    if captured > output_limit:
                        status = "output_limit_exceeded"
                        break
                    key.data.append(chunk)
                if status != "ok":
                    break

        if status == "ok":
            remaining = deadline - time.monotonic()
            if remaining <= 0 and process.poll() is None:
                status = "timeout"
            else:
                try:
                    process.wait(timeout=max(0.0, remaining))
                except subprocess.TimeoutExpired:
                    status = "timeout"
        if status != "ok":
            _terminate_process_group(process)
            return _BoundedCommandResult(status, process.returncode, b"", b"")
        return _BoundedCommandResult(
            "ok" if process.returncode == 0 else "failed",
            process.returncode,
            b"".join(stdout_chunks),
            b"".join(stderr_chunks),
        )
    except OSError:
        _terminate_process_group(process)
        return _BoundedCommandResult("capture_error", process.returncode, b"", b"")
    except BaseException:
        _terminate_process_group(process)
        raise
    finally:
        _close_process_pipes(process)


def _run_git(source: Path, *arguments: str) -> bytes:
    result = _run_bounded_subprocess(
        ["git", *arguments],
        cwd=source,
        env=_safe_environment(),
        timeout=_COMMAND_TIMEOUT_SECONDS,
        output_limit=_COMMAND_OUTPUT_LIMIT,
    )
    if result.status == "output_limit_exceeded":
        _fail("TRITRACK_RELEASE_GIT_LIMIT")
    if result.status != "ok":
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    return result.stdout


def _read_regular(path: Path, limit: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if details.st_size > limit:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        if len(encoded) > limit or len(encoded) != details.st_size:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    finally:
        os.close(descriptor)


def _mapping(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        _fail(code)
    return value


def _positive_limit(policy: Mapping[str, object], name: str) -> int:
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    value = limits.get(name)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return value


def _build_epoch(policy: Mapping[str, object]) -> int:
    build = _mapping(policy.get("build"), "TRITRACK_RELEASE_POLICY_INVALID")
    if set(build) != {"sourceDateEpoch"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    value = build.get("sourceDateEpoch")
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < 315532800
    ):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return value


def _string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if len(value) != len(set(value)):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return tuple(value)


def _load_policy(source: Path) -> Mapping[str, object]:
    encoded = _read_regular(source / "release" / "package-policy-v1.json", _POLICY_LIMIT)
    try:
        policy = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    policy = _mapping(policy, "TRITRACK_RELEASE_POLICY_INVALID")
    if policy.get("schemaVersion") != "tritrack.package-policy/v1":
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if set(policy) != {
        "schemaVersion",
        "build",
        "limits",
        "source",
        "wheel",
        "sdist",
    }:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _build_epoch(policy)
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected_limits = {
        "sourceMaxFiles",
        "sourceMaxFileBytes",
        "sourceMaxTotalBytes",
        "archiveMaxBytes",
        "archiveMaxMembers",
        "memberMaxBytes",
        "expandedMaxBytes",
    }
    if set(limits) != expected_limits:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    for name in expected_limits:
        _positive_limit(policy, name)

    source_policy = _mapping(
        policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(source_policy) != {
        "allowedFakeHomeUsers",
        "allowedFakeSecretValues",
        "forbiddenSuffixes",
    }:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    allowed_users = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeHomeUsers"))
    )
    allowed_secrets = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeSecretValues"))
    )
    if (
        allowed_users != _ALLOWED_FAKE_USERS
        or allowed_secrets != _ALLOWED_FAKE_SECRETS
    ):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(source_policy.get("forbiddenSuffixes"))

    wheel_policy = _mapping(
        policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(wheel_policy) != {"expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(wheel_policy.get("expectedMembers"))

    sdist_policy = _mapping(
        policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(sdist_policy) != {"root", "expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(sdist_policy.get("expectedMembers"))
    return policy


def _status(source: Path) -> bytes:
    return _run_git(
        source,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )


def _safe_source_path(encoded: bytes) -> str:
    try:
        name = encoded.decode("utf-8", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    candidate = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or candidate.is_absolute()
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    return name


def _parse_index(encoded: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for raw in encoded.split(b"\0"):
        if not raw:
            continue
        try:
            prefix, raw_path = raw.split(b"\t", 1)
            mode, object_id, stage = prefix.decode("ascii").split(" ")
        except (ValueError, UnicodeDecodeError):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        if stage != "0":
            _fail("TRITRACK_RELEASE_SOURCE_STAGE")
        if mode not in {"100644", "100755"}:
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        entries.append((_safe_source_path(raw_path), mode, object_id))
    if not entries:
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    if len({entry[0] for entry in entries}) != len(entries):
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    return entries


def _git_blob_hash(encoded: bytes, algorithm: str) -> str:
    if algorithm not in {"sha1", "sha256"}:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    digest = hashlib.new(algorithm)
    digest.update(f"blob {len(encoded)}\0".encode("ascii"))
    digest.update(encoded)
    return digest.hexdigest()


def _path_signature(path: Path) -> tuple[int, int, int, int]:
    try:
        details = path.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)


def _home_user_after(encoded: bytes, marker: bytes, separator: bytes) -> bytes | None:
    lowered = encoded.lower()
    offset = 0
    lowered_marker = marker.lower()
    while True:
        found = lowered.find(lowered_marker, offset)
        if found < 0:
            return None
        start = found + len(marker)
        end = start
        while end < len(encoded) and encoded[end : end + 1] not in (
            separator,
            b"/",
            b"\\",
            b"\0",
            b"\t",
            b"\r",
            b"\n",
            b" ",
            b'"',
            b"'",
        ):
            end += 1
        user = lowered[start:end]
        if user and user not in _ALLOWED_FAKE_USERS:
            return user
        offset = max(end, start + 1)


def scan_public_bytes(encoded: bytes) -> None:
    """Reject public-source privacy canaries without returning matched bytes."""

    mac_home = b"/" + b"Users" + b"/"
    linux_home = b"/" + b"home" + b"/"
    windows_home = b"\\" + b"Users" + b"\\"
    mounted_volume = b"/" + b"Volumes" + b"/"
    for marker, separator in (
        (mac_home, b"/"),
        (linux_home, b"/"),
        (windows_home, b"\\"),
    ):
        if _home_user_after(encoded, marker, separator) is not None:
            _fail("TRITRACK_RELEASE_PRIVATE_PATH")
    if mounted_volume.lower() in encoded.lower():
        _fail("TRITRACK_RELEASE_PRIVATE_PATH")

    private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
    rsa_private_key = b"-----BEGIN RSA " + b"PRIVATE KEY-----"
    if private_key in encoded or rsa_private_key in encoded:
        _fail("TRITRACK_RELEASE_PRIVATE_KEY")

    terms = (
        b"api" + b"[_-]?key",
        b"auth" + b"[_-]?token",
        b"access" + b"[_-]?token",
        b"password",
        b"passwd",
        b"secret",
    )
    assignment = re.compile(
        rb"(?im)\b(?:"
        + b"|".join(terms)
        + rb")\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+${}\-]{1,256})"
    )
    for match in assignment.finditer(encoded):
        value = match.group(1).rstrip(b"'\"").lower()
        if value not in _ALLOWED_FAKE_SECRETS:
            _fail("TRITRACK_RELEASE_CREDENTIAL")

    credential_shapes = (
        rb"\bgh" + rb"[pousr]_[A-Za-z0-9]{36,255}\b",
        rb"\bAK" + rb"IA[0-9A-Z]{16}\b",
        rb"\bAI" + rb"za[0-9A-Za-z_-]{35}\b",
        rb"\bxox" + rb"[baprs]-[0-9A-Za-z-]{20,255}\b",
    )
    if any(re.search(pattern, encoded) for pattern in credential_shapes):
        _fail("TRITRACK_RELEASE_CREDENTIAL")


def inventory_tracked_source(source: Path) -> SourceInventory:
    """Bind one clean Git index to the exact regular working-tree bytes."""

    source = source.resolve()
    policy = _load_policy(source)
    index_bytes = _run_git(source, "ls-files", "-s", "-z")
    entries = _parse_index(index_bytes)
    if _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_DIRTY")
    max_files = _positive_limit(policy, "sourceMaxFiles")
    max_file_bytes = _positive_limit(policy, "sourceMaxFileBytes")
    max_total_bytes = _positive_limit(policy, "sourceMaxTotalBytes")
    if len(entries) > max_files:
        _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
    source_policy = _mapping(policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID")
    suffixes = tuple(item.casefold() for item in _string_list(source_policy.get("forbiddenSuffixes")))
    object_format = _run_git(source, "rev-parse", "--show-object-format").strip()
    try:
        algorithm = object_format.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    commit_bytes = _run_git(source, "rev-parse", "HEAD").strip()
    try:
        commit = commit_bytes.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        _fail("TRITRACK_RELEASE_GIT_FAILED")

    total = 0
    inventory = hashlib.sha256()
    for name, mode, object_id in sorted(entries):
        if suffixes and name.casefold().endswith(suffixes):
            _fail("TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE")
        path = source / name
        before = _path_signature(path)
        if before[2] > max_file_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += before[2]
        if total > max_total_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        encoded = _read_regular(path, max_file_bytes)
        after = _path_signature(path)
        if before != after:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        if _git_blob_hash(encoded, algorithm) != object_id:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        scan_public_bytes(encoded)
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, mode, str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")

    if _run_git(source, "ls-files", "-s", "-z") != index_bytes or _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return SourceInventory(
        count=len(entries),
        total_bytes=total,
        sha256=inventory.hexdigest(),
        commit=commit,
    )


def _read_archive_bytes(path: Path, policy: Mapping[str, object]) -> bytes:
    limit = _positive_limit(policy, "archiveMaxBytes")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
        if not 0 < before.st_size <= limit:
            _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(encoded) > limit
            or len(encoded) != before.st_size
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        ):
            _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    finally:
        os.close(descriptor)


def _safe_member_name(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    normalized = unicodedata.normalize("NFC", name)
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    return normalized.rstrip("/")


def _bounded_archive_read(stream, expected: int, limit: int) -> bytes:
    if expected > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    encoded = stream.read(limit + 1)
    if len(encoded) != expected or len(encoded) > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    return encoded


def _member_digest(
    inventory: hashlib._Hash,
    name: str,
    member_type: str,
    mode: int,
    encoded: bytes,
) -> None:
    values = (
        name,
        member_type,
        f"{mode & 0o7777:o}",
        str(len(encoded)),
        hashlib.sha256(encoded).hexdigest(),
    )
    for value in values:
        inventory.update(value.encode("utf-8"))
        inventory.update(b"\0")
    inventory.update(b"\n")


def _check_collision(name: str, exact: set[str], folded: set[str]) -> None:
    if name in exact:
        _fail("TRITRACK_RELEASE_ARCHIVE_DUPLICATE")
    collision = unicodedata.normalize("NFC", name).casefold()
    if collision in folded:
        _fail("TRITRACK_RELEASE_ARCHIVE_COLLISION")
    exact.add(name)
    folded.add(collision)


def inspect_wheel(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a wheel without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    wheel_policy = _mapping(policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(wheel_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[zipfile.ZipInfo, str, int]] = []
    expanded = 0
    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            members = archive.infolist()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                name = _safe_member_name(member.filename)
                _check_collision(name, exact, folded)
                if member.flag_bits & 1:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ENCRYPTED")
                if member.is_dir():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                raw_mode = member.external_attr >> 16
                member_type = stat.S_IFMT(raw_mode)
                if member_type not in {0, stat.S_IFREG}:
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                expanded += member.file_size
                if member.file_size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, name, raw_mode))
            if {name for _, name, _ in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, raw_mode in sorted(files, key=lambda item: item[1]):
                with archive.open(member) as stream:
                    encoded = _bounded_archive_read(stream, member.file_size, max_member)
                scan_public_bytes(encoded)
                _member_digest(inventory, name, "file", raw_mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(files),
        member_inventory_sha256=inventory.hexdigest(),
    )


def inspect_sdist(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a gzipped source distribution without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    sdist_policy = _mapping(policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(sdist_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[tarfile.TarInfo, str]] = []
    all_members: list[tuple[tarfile.TarInfo, str, str]] = []
    expanded = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                full_name = _safe_member_name(member.name)
                if full_name == root.rstrip("/"):
                    relative = ""
                elif full_name.startswith(root):
                    relative = full_name[len(root) :]
                else:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ROOT")
                collision_name = relative or "."
                _check_collision(collision_name, exact, folded)
                if member.isdir():
                    all_members.append((member, relative, "directory"))
                    continue
                if not member.isreg():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                if not relative:
                    _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
                expanded += member.size
                if member.size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, relative))
                all_members.append((member, relative, "file"))
            if {name for _, name in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, member_type in sorted(all_members, key=lambda item: item[1]):
                if member_type == "directory":
                    encoded = b""
                else:
                    stream = archive.extractfile(member)
                    if stream is None:
                        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
                    with stream:
                        encoded = _bounded_archive_read(stream, member.size, max_member)
                    scan_public_bytes(encoded)
                _member_digest(inventory, name or ".", member_type, member.mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(all_members),
        member_inventory_sha256=inventory.hexdigest(),
    )


def _run_command(
    argv: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout: int = 300,
    output_limit: int = _COMMAND_OUTPUT_LIMIT,
) -> bytes:
    result = _run_bounded_subprocess(
        argv,
        cwd=cwd,
        env=env,
        timeout=timeout,
        output_limit=output_limit,
    )
    if result.status == "output_limit_exceeded":
        _fail("TRITRACK_RELEASE_COMMAND_LIMIT")
    if result.status != "ok":
        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
    return result.stdout


def _installed_tool_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("pip", "build", "setuptools", "wheel"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            _fail("TRITRACK_RELEASE_TOOLCHAIN")
    return versions


def _build_environment(epoch: int, temporary: Path) -> dict[str, str]:
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        _fail("TRITRACK_RELEASE_EPOCH")
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.defpath,
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": str(epoch),
        "TMPDIR": os.fspath(temporary),
    }
    return environment


def build_distributions(
    snapshot: Path, output: Path, *, epoch: int
) -> tuple[Path, Path]:
    """Build exactly one wheel and one sdist with the pinned local toolchain."""

    expected_tools = {
        "pip": "26.2",
        "build": "1.5.0",
        "setuptools": "84.0.0",
        "wheel": "0.48.0",
    }
    if _installed_tool_versions() != expected_tools:
        _fail("TRITRACK_RELEASE_TOOLCHAIN")
    if not snapshot.is_dir():
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    try:
        os.mkdir(output)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [
            os.fspath(Path(sys.executable)),
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            os.fspath(output),
        ],
        cwd=snapshot,
        env=_build_environment(epoch, output),
        timeout=300,
    )
    try:
        members = [
            child
            for child in output.iterdir()
            if child.is_file() and not child.is_symlink()
        ]
    except OSError:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    wheels = [child for child in members if child.suffix == ".whl"]
    sdists = [child for child in members if child.name.endswith(".tar.gz")]
    if len(members) != 2 or len(wheels) != 1 or len(sdists) != 1:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    return wheels[0], sdists[0]


def _wheel_project_identity(wheel: Path) -> tuple[str, str]:
    try:
        with zipfile.ZipFile(wheel) as archive:
            candidates = [
                member
                for member in archive.infolist()
                if member.filename.endswith(".dist-info/METADATA")
                and not member.is_dir()
            ]
            if len(candidates) != 1 or candidates[0].file_size > _POLICY_LIMIT:
                _fail("TRITRACK_RELEASE_WHEEL_METADATA")
            with archive.open(candidates[0]) as stream:
                encoded = _bounded_archive_read(
                    stream, candidates[0].file_size, _POLICY_LIMIT
                )
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    message = BytesParser().parsebytes(encoded)
    name = message.get("Name")
    version = message.get("Version")
    if not name or not version or "\n" in name or "\n" in version:
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    return name, version


def _install_environment(temporary: Path, binary: Path) -> dict[str, str]:
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.fspath(binary) + os.pathsep + os.defpath,
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PYTHONHASHSEED": "0",
        "TMPDIR": os.fspath(temporary),
    }
    for name in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "PIP_INDEX_URL",
        "PIP_TRUSTED_HOST",
    ):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    return environment


def fresh_install_smoke(wheel: Path, temporary: Path, source: Path) -> None:
    """Install only the chosen local wheel into a new external environment."""

    project_name, project_version = _wheel_project_identity(wheel)
    if project_name != "tritrack-editing-assistant":
        _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
    try:
        os.mkdir(temporary)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [os.fspath(Path(sys.executable)), "-m", "venv", os.fspath(temporary)],
        cwd=temporary.parent,
        env=_build_environment(0, temporary),
        timeout=180,
    )
    if os.name == "nt":
        binary = temporary / "Scripts"
        python = binary / "python.exe"
        tritrack = binary / "tritrack.exe"
    else:
        binary = temporary / "bin"
        python = binary / "python"
        tritrack = binary / "tritrack"
    environment = _install_environment(temporary, binary)
    pip_base = [
        os.fspath(python),
        "-m",
        "pip",
        "--disable-pip-version-check",
        "--no-input",
    ]
    _run_command(
        [*pip_base, "install", "pip==26.2"],
        cwd=temporary,
        env=environment,
        timeout=300,
    )
    _run_command(
        [*pip_base, "install", os.fspath(wheel.resolve())],
        cwd=temporary,
        env=environment,
        timeout=600,
    )
    _run_command(
        [*pip_base, "check"], cwd=temporary, env=environment, timeout=120
    )
    metadata_code = (
        "import importlib.metadata as m; "
        "d=m.distribution('tritrack-editing-assistant'); "
        "print(d.metadata['Name']+'\\t'+d.version)"
    )
    installed = _run_command(
        [os.fspath(python), "-I", "-c", metadata_code],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    expected = f"{project_name}\t{project_version}\n".encode()
    if installed != expected:
        _fail("TRITRACK_RELEASE_INSTALLED_IDENTITY")
    components = _run_command(
        [os.fspath(tritrack), "components", "--json"],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    try:
        component_summary = json.loads(components.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    if (
        not isinstance(component_summary, Mapping)
        or component_summary.get("schemaVersion") != "tritrack.components/v1"
        or not isinstance(component_summary.get("components"), list)
        or len(component_summary["components"]) != 11
    ):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    for arguments in (
        ("validate", "--help"),
        ("validate", "contract", "--help"),
        ("validate", "fcpxml", "--help"),
        ("validate", "paper", "--help"),
        ("validate", "run", "--help"),
    ):
        _run_command(
            [os.fspath(tritrack), *arguments],
            cwd=temporary,
            env=environment,
            timeout=60,
        )

    seam = temporary / "downstream-seam"
    try:
        os.mkdir(seam)
        script_bytes = _read_regular(
            source / "examples" / "downstream_seam.py", _POLICY_LIMIT
        )
        fixture_bytes = _read_regular(
            source
            / "examples"
            / "downstream_fixture"
            / "aligned-transcript.json",
            _POLICY_LIMIT,
        )
        _write_snapshot_file(seam, "downstream_seam.py", 0o644, script_bytes)
        _write_snapshot_file(
            seam, "aligned-transcript.json", 0o644, fixture_bytes
        )
    except ReleaseGateError:
        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
    except OSError:
        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")

    copied_script = seam / "downstream_seam.py"
    copied_fixture = seam / "aligned-transcript.json"
    receipt = seam / "downstream-receipt.json"
    try:
        _run_command(
            [
                os.fspath(python),
                "-I",
                os.fspath(copied_script),
                "--tritrack",
                os.fspath(tritrack),
                "--aligned",
                os.fspath(copied_fixture),
                "--output",
                os.fspath(receipt),
            ],
            cwd=seam,
            env=environment,
            timeout=60,
        )
        observed = json.loads(
            _read_regular(receipt, _POLICY_LIMIT).decode(
                "utf-8", errors="strict"
            )
        )
    except (
        ReleaseGateError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        OSError,
    ):
        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
    artifact_sha256 = hashlib.sha256(fixture_bytes).hexdigest()
    expected = {
        "schemaVersion": "example.tritrack-downstream-receipt/v1",
        "engineAuthority": {
            "artifactSha256": artifact_sha256,
            "contractName": "aligned-transcript-v1",
            "contractSchemaVersion": "tritrack.aligned-transcript/v1",
            "validationScope": "contract",
        },
        "derivedObservation": {"takeCount": 1, "cueCount": 1},
    }
    if observed != expected:
        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")


def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
    """Build and validate the deterministic, closed public release receipt."""

    manifest: dict[str, object] = {
        "schemaVersion": "tritrack.release-manifest/v1",
        "project": {
            "name": context.project_name,
            "version": context.version,
            "commit": context.commit,
        },
        "sourceInventory": {
            "count": context.source_inventory.count,
            "sha256": context.source_inventory.sha256,
        },
        "toolchain": {
            "python": context.python_version,
            "implementation": context.implementation,
            "pip": context.toolchain["pip"],
            "build": context.toolchain["build"],
            "setuptools": context.toolchain["setuptools"],
            "wheel": context.toolchain["wheel"],
        },
        "platform": {"system": context.system, "machine": context.machine},
        "artifacts": {
            "wheel": {
                "sha256": context.wheel.sha256,
                "sizeBytes": context.wheel.size_bytes,
                "memberCount": context.wheel.member_count,
                "memberInventorySha256": context.wheel.member_inventory_sha256,
            },
            "sdist": {
                "sha256": context.sdist.sha256,
                "sizeBytes": context.sdist.size_bytes,
                "memberCount": context.sdist.member_count,
                "memberInventorySha256": context.sdist.member_inventory_sha256,
            },
        },
        "reproducibility": {
            "wheelBytesMatch": True,
            "sdistMembersMatch": True,
        },
        "gates": {
            "sourceIdentity": "pass",
            "sourcePrivacy": "pass",
            "wheelArchive": "pass",
            "sdistArchive": "pass",
            "freshInstall": "pass",
            "downstreamSeam": "pass",
        },
        "nonClaims": [
            "no-tag",
            "no-release",
            "no-package-publication",
            "no-pull-request",
            "no-tester-contact",
            "no-signing",
            "no-attestation",
            "no-sbom",
            "no-final-cut-gui",
            "no-dtd",
            "no-provider",
            "no-application-submission",
        ],
    }
    schema_path = Path(__file__).resolve().parents[1] / "release" / "release-manifest-v1.schema.json"
    try:
        schema = json.loads(_read_regular(schema_path, _POLICY_LIMIT).decode("utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(manifest, schema)
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    return manifest


def _link_file(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination, follow_symlinks=False)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _publication_artifacts(manifest: bytes) -> dict[str, tuple[int, str]]:
    if not 0 < len(manifest) <= _POLICY_LIMIT:
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    try:
        payload = _mapping(
            json.loads(manifest.decode("utf-8", errors="strict")),
            "TRITRACK_RELEASE_MANIFEST_INVALID",
        )
        artifacts = _mapping(
            payload.get("artifacts"), "TRITRACK_RELEASE_MANIFEST_INVALID"
        )
        result: dict[str, tuple[int, str]] = {}
        for kind in ("wheel", "sdist"):
            artifact = _mapping(
                artifacts.get(kind), "TRITRACK_RELEASE_MANIFEST_INVALID"
            )
            size = artifact.get("sizeBytes")
            digest = artifact.get("sha256")
            if (
                not isinstance(size, int)
                or isinstance(size, bool)
                or size < 1
                or not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
            result[kind] = (size, digest)
        return result
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")


def _verify_published_archive(path: Path, expected: tuple[int, str]) -> None:
    expected_size, expected_sha256 = expected
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            details = os.fstat(descriptor)
            if not stat.S_ISREG(details.st_mode) or details.st_size != expected_size:
                _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
            digest = hashlib.sha256()
            observed_size = 0
            while observed_size <= expected_size:
                chunk = os.read(
                    descriptor,
                    min(1024 * 1024, expected_size + 1 - observed_size),
                )
                if not chunk:
                    break
                observed_size += len(chunk)
                digest.update(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
    if (
        observed_size != expected_size
        or digest.hexdigest() != expected_sha256
        or (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    ):
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")


def publish_release(
    output: Path, wheel: Path, sdist: Path, manifest: bytes
) -> None:
    """Publish two archives first and the canonical success manifest last."""

    if (
        wheel.name in {"", ".", "..", "release-manifest.json"}
        or sdist.name in {"", ".", "..", "release-manifest.json"}
        or wheel.name != os.path.basename(wheel.name)
        or sdist.name != os.path.basename(sdist.name)
        or wheel.name == sdist.name
    ):
        _fail("TRITRACK_RELEASE_PUBLISH")
    expected_artifacts = _publication_artifacts(manifest)
    try:
        parent_details = output.parent.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    if not stat.S_ISDIR(parent_details.st_mode):
        _fail("TRITRACK_RELEASE_OUTPUT")

    temporary_manifest: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=wheel.parent,
            prefix=".release-manifest-",
            delete=False,
        ) as stream:
            temporary_manifest = Path(stream.name)
            stream.write(manifest)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.mkdir(output)
        except FileExistsError:
            _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
        except OSError:
            _fail("TRITRACK_RELEASE_OUTPUT")
        _link_file(wheel, output / wheel.name)
        _link_file(sdist, output / sdist.name)
        _fsync_directory(output)
        _verify_published_archive(output / wheel.name, expected_artifacts["wheel"])
        _verify_published_archive(output / sdist.name, expected_artifacts["sdist"])
        _link_file(temporary_manifest, output / "release-manifest.json")
        _fsync_directory(output)
        _fsync_directory(output.parent)
    finally:
        if temporary_manifest is not None:
            try:
                temporary_manifest.unlink(missing_ok=True)
            except OSError:
                pass


def _assert_source_identity(source: Path) -> tuple[str, str]:
    encoded = _read_regular(source / ".tritrack-project.json", _POLICY_LIMIT)
    try:
        identity = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")
    expected = {
        "schemaVersion": "tritrack.project-identity/v1",
        "projectId": "tritrack-editing-assistant",
        "projectKind": "public-engine",
        "maintainerSkill": "tritrack-editing-assistant-maintainer",
        "lane": "OSS",
    }
    if identity != expected:
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")

    try:
        configuration = tomllib.loads(
            _read_regular(source / "pyproject.toml", _POLICY_LIMIT).decode("utf-8")
        )
        project = configuration["project"]
        project_name = project["name"]
        version = project["version"]
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    if project_name != "tritrack-editing-assistant" or not isinstance(version, str):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    init_bytes = _read_regular(
        source / "src" / "tritrack_editing_assistant" / "__init__.py",
        _POLICY_LIMIT,
    )
    match = re.fullmatch(
        rb'"""TriTrack Editing Assistant public package\."""\n\n__version__ = "([^"\r\n]+)"\n',
        init_bytes,
    )
    if match is None or match.group(1).decode("utf-8", "strict") != version:
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    return project_name, version


def _assert_git_toplevel(source: Path) -> None:
    try:
        top = Path(
            _run_git(source, "rev-parse", "--show-toplevel").decode("utf-8", "strict").strip()
        ).resolve()
    except (UnicodeDecodeError, OSError):
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if top != source:
        _fail("TRITRACK_RELEASE_GIT_TOPLEVEL")


def _snapshot_inventory(
    archive: tarfile.TarFile,
    max_file: int,
    max_total: int,
) -> tuple[list[tuple[str, int, bytes]], str]:
    files: list[tuple[str, int, bytes]] = []
    seen: set[str] = set()
    total = 0
    for member in archive.getmembers():
        name = _safe_member_name(member.name)
        if name in seen:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        seen.add(name)
        if member.isdir():
            continue
        if not member.isreg():
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        if member.size > max_file:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += member.size
        if total > max_total:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        stream = archive.extractfile(member)
        if stream is None:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        with stream:
            encoded = _bounded_archive_read(stream, member.size, max_file)
        mode = 0o755 if member.mode & 0o111 else 0o644
        files.append((name, mode, encoded))
    inventory = hashlib.sha256()
    for name, mode, encoded in sorted(files):
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, f"100{mode:o}"[-6:], str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")
    return files, inventory.hexdigest()


def _write_snapshot_file(root: Path, name: str, mode: int, encoded: bytes) -> None:
    path = root.joinpath(*PurePosixPath(name).parts)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            mode,
        )
        try:
            view = memoryview(encoded)
            while view:
                written = os.write(descriptor, view)
                if written < 1:
                    _fail("TRITRACK_RELEASE_SNAPSHOT")
                view = view[written:]
        finally:
            os.close(descriptor)
        os.chmod(path, mode, follow_symlinks=False)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")


def _materialize_snapshot(
    source: Path,
    destination: Path,
    inventory: SourceInventory,
    policy: Mapping[str, object],
) -> None:
    try:
        os.mkdir(destination)
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    archive_path = destination.parent / f".{destination.name}.tar"
    _run_command(
        [
            "git",
            "archive",
            "--format=tar",
            "--output",
            os.fspath(archive_path),
            inventory.commit,
        ],
        cwd=source,
        env=_safe_environment(),
        timeout=120,
    )
    try:
        with tarfile.open(archive_path, mode="r:") as archive:
            files, digest = _snapshot_inventory(
                archive,
                _positive_limit(policy, "sourceMaxFileBytes"),
                _positive_limit(policy, "sourceMaxTotalBytes"),
            )
        if len(files) != inventory.count or digest != inventory.sha256:
            _fail("TRITRACK_RELEASE_SNAPSHOT_MISMATCH")
        for name, mode, encoded in files:
            _write_snapshot_file(destination, name, mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    finally:
        try:
            archive_path.unlink(missing_ok=True)
        except OSError:
            pass


def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
    return (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )


def run_release_gate(source: Path, output: Path) -> dict[str, object]:
    """Run the complete local release-readiness gate and publish manifest last."""

    try:
        source = source.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE")
    if not source.is_dir():
        _fail("TRITRACK_RELEASE_SOURCE")
    _assert_git_toplevel(source)
    project_name, version = _assert_source_identity(source)
    inventory = inventory_tracked_source(source)
    policy = _load_policy(source)
    if output.exists() or output.is_symlink():
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    try:
        output_parent = output.parent.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    output = output_parent / output.name
    epoch = _build_epoch(policy)
    if _run_git(source, "rev-parse", "HEAD").strip().decode("ascii") != inventory.commit:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")

    with tempfile.TemporaryDirectory(
        dir=output.parent, prefix=".tritrack-release-staging-"
    ) as temporary:
        staging = Path(temporary)
        snapshot_one = staging / "snapshot-one"
        snapshot_two = staging / "snapshot-two"
        _materialize_snapshot(source, snapshot_one, inventory, policy)
        _materialize_snapshot(source, snapshot_two, inventory, policy)
        wheel_one, sdist_one = build_distributions(
            snapshot_one, staging / "dist-one", epoch=epoch
        )
        wheel_two, sdist_two = build_distributions(
            snapshot_two, staging / "dist-two", epoch=epoch
        )
        identities = {
            _wheel_project_identity(wheel_one),
            _wheel_project_identity(wheel_two),
        }
        if identities != {(project_name, version)}:
            _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
        if wheel_one.name != wheel_two.name or sdist_one.name != sdist_two.name:
            _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
        wheel_inspection = inspect_wheel(wheel_one, policy)
        second_wheel_inspection = inspect_wheel(wheel_two, policy)
        sdist_inspection = inspect_sdist(sdist_one, policy)
        second_sdist_inspection = inspect_sdist(sdist_two, policy)
        if wheel_inspection != second_wheel_inspection:
            _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
        if (
            sdist_inspection.member_inventory_sha256
            != second_sdist_inspection.member_inventory_sha256
        ):
            _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
        fresh_install_smoke(
            wheel_one, staging / "fresh-install", snapshot_one
        )
        context = ReleaseContext(
            project_name=project_name,
            version=version,
            commit=inventory.commit,
            source_inventory=inventory,
            toolchain=_installed_tool_versions(),
            python_version=platform.python_version(),
            implementation=platform.python_implementation(),
            system=platform.system(),
            machine=platform.machine(),
            wheel=wheel_inspection,
            sdist=sdist_inspection,
        )
        manifest = build_release_manifest(context)
        publish_release(
            output,
            wheel_one,
            sdist_one,
            _canonical_manifest(manifest),
        )
    return manifest
~~~

### tests/test_downstream_seam.py

~~~text
"""Task 13 black-box downstream integration seam proof."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples" / "downstream_seam.py"
FIXTURE = (
    ROOT / "examples" / "downstream_fixture" / "aligned-transcript.json"
)
TRITRACK = Path(sys.executable).with_name("tritrack")


def sha256(encoded: bytes) -> str:
    return hashlib.sha256(encoded).hexdigest()


def run_consumer(
    aligned: Path, output: Path, *, tritrack: Path = TRITRACK
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-I",
            os.fspath(SCRIPT),
            "--tritrack",
            os.fspath(tritrack),
            "--aligned",
            os.fspath(aligned),
            "--output",
            os.fspath(output),
        ],
        cwd=SCRIPT.parent,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


class DownstreamSeamTest(unittest.TestCase):
    def test_consumes_exact_engine_authority_without_internal_imports(self) -> None:
        self.assertTrue(TRITRACK.is_file(), TRITRACK)
        aligned_bytes = FIXTURE.read_bytes()
        artifact_sha256 = sha256(aligned_bytes)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "downstream-receipt.json"
            result = run_consumer(FIXTURE, output)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                {
                    "schemaVersion": "example.tritrack-downstream-receipt/v1",
                    "engineAuthority": {
                        "artifactSha256": artifact_sha256,
                        "contractName": "aligned-transcript-v1",
                        "contractSchemaVersion": (
                            "tritrack.aligned-transcript/v1"
                        ),
                        "validationScope": "contract",
                    },
                    "derivedObservation": {"takeCount": 1, "cueCount": 1},
                },
            )
            self.assertTrue(output.read_bytes().endswith(b"\n"))
            self.assertEqual(
                json.loads(result.stdout),
                {
                    "schemaVersion": (
                        "example.tritrack-downstream-summary/v1"
                    ),
                    "artifactSha256": artifact_sha256,
                    "takeCount": 1,
                    "cueCount": 1,
                },
            )
            self.assertNotIn(os.fspath(ROOT), result.stdout)
            self.assertNotIn("Invented public words", result.stdout)

        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("tritrack_editing_assistant", source)

    def test_preserves_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "existing.json"
            output.write_bytes(b"winner")

            result = run_consumer(FIXTURE, output)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(
                json.loads(result.stderr),
                {"error": "DOWNSTREAM_OUTPUT_EXISTS"},
            )
            self.assertEqual(output.read_bytes(), b"winner")

    def test_rejects_unknown_engine_contract_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            changed = json.loads(FIXTURE.read_text(encoding="utf-8"))
            changed["schemaVersion"] = "tritrack.aligned-transcript/v99"
            aligned = root / "future.json"
            aligned.write_text(
                json.dumps(changed, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            output = root / "receipt.json"

            result = run_consumer(aligned, output)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(
                json.loads(result.stderr),
                {"error": "DOWNSTREAM_ENGINE_VALIDATION_FAILED"},
            )
            self.assertFalse(output.exists())
            self.assertNotIn(os.fspath(root), result.stderr)

    def test_rejects_validator_hash_that_does_not_match_consumed_bytes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_cli = root / "tritrack"
            fake_cli.write_text(
                "#!" + os.fspath(sys.executable) + "\n"
                "import json\n"
                "print(json.dumps({\n"
                "  'schemaVersion': 'tritrack.validate-summary/v1',\n"
                "  'toolVersion': '0.1.0a0',\n"
                "  'artifactKind': 'contract',\n"
                "  'validationScope': 'contract',\n"
                "  'hashes': {'artifact': '0' * 64},\n"
                "  'counts': {},\n"
                "  'details': {\n"
                "    'contractName': 'aligned-transcript-v1',\n"
                "    'contractSchemaVersion': "
                "'tritrack.aligned-transcript/v1',\n"
                "  },\n"
                "}, sort_keys=True))\n",
                encoding="utf-8",
            )
            fake_cli.chmod(0o755)
            output = root / "receipt.json"

            result = run_consumer(FIXTURE, output, tritrack=fake_cli)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(
                json.loads(result.stderr),
                {"error": "DOWNSTREAM_ENGINE_HASH_MISMATCH"},
            )
            self.assertFalse(output.exists())

    def test_rejects_engine_summary_that_changes_before_publication(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_cli = root / "tritrack"
            counter = root / "calls"
            fake_cli.write_text(
                "#!" + os.fspath(sys.executable) + "\n"
                "import hashlib\n"
                "import json\n"
                "import pathlib\n"
                "import sys\n"
                f"counter = pathlib.Path({os.fspath(counter)!r})\n"
                "calls = int(counter.read_text() or '0') "
                "if counter.exists() else 0\n"
                "counter.write_text(str(calls + 1))\n"
                "artifact = pathlib.Path(sys.argv[sys.argv.index("
                "'--artifact') + 1])\n"
                "digest = hashlib.sha256(artifact.read_bytes()).hexdigest()\n"
                "print(json.dumps({\n"
                "  'schemaVersion': 'tritrack.validate-summary/v1',\n"
                "  'toolVersion': '0.1.0a0' if calls == 0 else 'changed',\n"
                "  'artifactKind': 'contract',\n"
                "  'validationScope': 'contract',\n"
                "  'hashes': {'artifact': digest},\n"
                "  'counts': {},\n"
                "  'details': {\n"
                "    'contractName': 'aligned-transcript-v1',\n"
                "    'contractSchemaVersion': "
                "'tritrack.aligned-transcript/v1',\n"
                "  },\n"
                "}, sort_keys=True))\n",
                encoding="utf-8",
            )
            fake_cli.chmod(0o755)
            output = root / "receipt.json"

            result = run_consumer(FIXTURE, output, tritrack=fake_cli)

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(
                json.loads(result.stderr),
                {"error": "DOWNSTREAM_ENGINE_CHANGED"},
            )
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
~~~

### tests/test_maintainer_boundary.py

~~~text
"""Task 4.5 tests for the public-maintainer project boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    ROOT / ".agents" / "skills" / "tritrack-editing-assistant-maintainer"
)
VALIDATOR = SKILL_ROOT / "scripts" / "check_project_identity.py"
PUBLIC_GOVERNANCE = (
    ROOT / "AGENTS.md",
    ROOT / "STATUS.md",
    ROOT / "PRODUCT-WISHES.md",
    ROOT / "docs" / "ROADMAP.md",
    ROOT / "docs" / "TOOLING.md",
    SKILL_ROOT / "SKILL.md",
)


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


class MaintainerBoundaryTest(unittest.TestCase):
    def test_public_project_identity_is_accepted(self) -> None:
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "lane": "OSS",
                "ok": True,
                "projectId": "tritrack-editing-assistant",
                "projectKind": "public-engine",
            },
        )

    def test_missing_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run_validator(Path(temporary))
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISSING", result.stderr)

    def test_private_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".tritrack-project.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": "tritrack.project-identity/v1",
                        "projectId": "some-private-production",
                        "projectKind": "private-production",
                        "maintainerSkill": "some-private-skill",
                        "lane": "MAIN",
                    }
                ),
                encoding="utf-8",
            )
            result = run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISMATCH", result.stderr)

    def test_public_governance_is_self_contained_and_public_safe(self) -> None:
        forbidden = (
            "/" + "Users" + "/",
            "TriTrack-" + "worktrees",
            "TriTrack-" + "Subtitle-" + "Studio",
            "Codex for " + "Open Source",
            "six " + "months",
            "六" + "個月",
        )
        for path in PUBLIC_GOVERNANCE:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path}: leaked {token!r}")

    def test_maintainer_and_end_user_skills_are_distinct(self) -> None:
        maintainer = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        end_user_root = ROOT / "skills" / "tritrack-editing-assistant"
        end_user = (end_user_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (end_user_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: tritrack-editing-assistant-maintainer", maintainer)
        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", maintainer)
        self.assertIn("name: tritrack-editing-assistant\n", end_user)
        self.assertIn("$tritrack-editing-assistant", metadata)
        self.assertIn('display_name: "TriTrack Editing Assistant"', metadata)

        for command in (
            "tritrack run --help",
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
            "tritrack validate --help",
            "tritrack validate contract --help",
            "tritrack validate fcpxml --help",
            "tritrack validate paper --help",
            "tritrack validate run --help",
        ):
            self.assertIn(command, end_user)
        for required in (
            "text-revision human gate",
            "paper-edit human gate",
            "takes: []",
            "Questions",
            "Selections",
            "transport, not authority",
            "absent output directory",
            "Keep media",
            "strict aligned transcript",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(required, end_user)

        lowered = end_user.lower()
        forbidden = (
            "tritrack-editing-assistant-maintainer",
            "task 10",
            "standing grant",
            "branch",
            "release",
            "tester",
            "moonie",
            "subtitle studio",
            "/" + "users" + "/",
            "api_key",
            "credential",
            "provider",
            "upload",
            "run_workflow",
            ".py",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)

    def test_public_status_records_tasks_1_through_13(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-10-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-10-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_11_verification = (ROOT / "docs" / "TASK-11-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_12_verification = (ROOT / "docs" / "TASK-12-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Tasks 1–13", status)
        self.assertIn("Task 6.5", status)
        self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
        self.assertLess(status.index("Task 7"), status.index("Task 8"))
        self.assertLess(status.index("Task 8"), status.index("Task 9"))
        self.assertLess(status.index("Task 9"), status.index("Task 10"))
        self.assertLess(status.index("Task 10"), status.index("Task 11"))
        self.assertLess(status.index("Task 11"), status.index("Task 12"))
        self.assertLess(status.index("Task 12"), status.index("Task 13"))
        self.assertIn("Task 10", roadmap)
        self.assertLess(roadmap.index("Task 10"), roadmap.index("Task 11"))
        for authority in (
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
        ):
            self.assertIn(authority, tooling)
        for text in (status, roadmap, tooling, readme, verification):
            self.assertIn("Task 10", text)
        self.assertIn("Selected option: A", decision)
        self.assertIn("immutable", verification)
        self.assertIn("story-cut.fcpxml", verification)
        self.assertIn("tritrack-editing-assistant", verification)
        self.assertIn("no network", verification)
        self.assertIn("Task 11", status)
        self.assertIn("Task 11", roadmap)
        self.assertIn("Task 12", status)
        self.assertIn("Task 12", roadmap)
        self.assertIn("Task 13", status)
        self.assertIn("Task 13", roadmap)
        self.assertIn("alphaReviewTarget", task_12_verification)
        self.assertIn("alphaEvidenceRecord", task_12_verification)
        self.assertIn("ce562e995b63f3f1a29989de3e1ef202da27b5f2", task_11_verification)
        for scope in (
            "contract",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(scope, task_11_verification)
        self.assertNotIn("`validate` and `run` remain planned", status)
        self.assertNotIn("`validate` remains planned", status)
        self.assertNotIn("`tritrack run` | planned", readme)

    def test_task_13_documents_generic_authority_and_downstream_seam(
        self,
    ) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-13-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-13-VERIFICATION.md").read_text(
            encoding="utf-8"
        )

        for text in (status, roadmap, tooling, readme, decision, verification):
            self.assertIn("Task 13", text)
        self.assertIn("Selected option: A", decision)
        self.assertIn(
            "exclusive supported downstream integration seam for v1",
            decision,
        )
        self.assertIn(
            "Internal Python modules and functions are implementation details",
            decision,
        )
        self.assertIn("never an engine contract", decision)
        for text in (status, tooling, readme, verification):
            self.assertIn("downstreamSeam", text)
            self.assertIn("wheel-only", text)
        for text in (status, roadmap, readme, verification):
            normalized = " ".join(text.split())
            self.assertIn("no tag", normalized)
            self.assertIn("no package publication", normalized)
            self.assertIn("no private integration", normalized)
        self.assertIn("examples/downstream_seam.py", tooling)
        self.assertIn("tritrack validate contract", tooling)

    def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
        handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 6.5",
            handoff,
        )
        self.assertIn("242e8b5406e92049ce60c654c3c8fca11be4b596", handoff)
        self.assertIn("codex/task6-5-public-demo-readiness", handoff)
        self.assertIn("RED", handoff)
        self.assertIn("GREEN", handoff)
        self.assertIn("application submission", handoff)
        self.assertNotIn("/" + "Users" + "/", handoff)

    def test_tooling_pins_the_perpetual_final_cut_identity(self) -> None:
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        self.assertIn("/Applications/Final Cut Pro.app", tooling)
        self.assertIn("com.apple.FinalCut", tooling)
        self.assertIn("com.apple.FinalCutApp", tooling)
        self.assertIn("default file association", tooling)

    def test_working_cut_claims_distinguish_transcript_from_editor_text(self) -> None:
        for path in (
            ROOT / "README.md",
            ROOT / "docs" / "TASK-9-VERIFICATION.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertIn("transcript-text-free", text, str(path))
            self.assertNotRegex(
                text,
                r"(?<!transcript-)text-free\s+(?:working cut|`working-cut)",
                str(path),
            )

        organizer = (
            ROOT / "src" / "tritrack_editing_assistant" / "organizer.py"
        ).read_text(encoding="utf-8")
        self.assertIn("transcript-text-free working cut", organizer)

    def test_authorization_is_a_capability_scoped_standing_grant(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for text in (agents, skill):
            self.assertIn("capability-scoped standing grant", text)
            self.assertIn("same target, visibility, scope, and risk", text)
            self.assertIn("until the producer revokes it", text)
            self.assertIn("Do not request it again", text)
            self.assertNotIn("without explicit producer", text)

        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("standing-authorization model", roadmap)
        self.assertNotIn("Each requires an explicit producer-approved gate", roadmap)


if __name__ == "__main__":
    unittest.main()
~~~

### tests/test_packaging.py

~~~text
"""Task 11 distribution policy and reproducibility tests."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path

import jsonschema

from scripts import release_gate_core

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "release" / "package-policy-v1.json"
MANIFEST_SCHEMA_PATH = ROOT / "release" / "release-manifest-v1.schema.json"
SDIST_ROOT = "tritrack_editing_assistant-0.1.0a0/"


def normalized_inventory(entries: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(entries):
        encoded = entries[name]
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(encoded)).encode("ascii"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(encoded).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


class PackagingPolicyTest(unittest.TestCase):
    def test_01_python_and_tool_constraints_are_exact(self) -> None:
        configuration = tomllib.loads((ROOT / "pyproject.toml").read_text())
        self.assertEqual(
            configuration["build-system"]["requires"],
            ["setuptools==84.0.0"],
        )
        self.assertEqual(configuration["project"]["requires-python"], ">=3.12,<3.14")
        self.assertEqual(
            configuration["project"]["optional-dependencies"]["dev"],
            ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"],
        )
        classifiers = configuration["project"]["classifiers"]
        versions = [
            value
            for value in classifiers
            if value.startswith("Programming Language :: Python :: 3.")
        ]
        self.assertEqual(
            versions,
            [
                "Programming Language :: Python :: 3.12",
                "Programming Language :: Python :: 3.13",
            ],
        )
        self.assertEqual(
            (ROOT / "requirements" / "ci-constraints.txt")
            .read_text(encoding="utf-8")
            .splitlines(),
            [
                "build==1.5.0",
                "packaging==26.3",
                "pip==26.2",
                "pyproject-hooks==1.2.0",
                "ruff==0.16.2",
                "setuptools==84.0.0",
                "wheel==0.48.0",
            ],
        )

    def test_02_package_policy_and_manifest_schema_are_closed(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(policy["schemaVersion"], "tritrack.package-policy/v1")
        self.assertEqual(
            set(policy),
            {"schemaVersion", "build", "limits", "source", "wheel", "sdist"},
        )
        self.assertEqual(policy["build"], {"sourceDateEpoch": 1704067200})
        for required in (
            "docs/TASK-11-VERIFICATION.md",
            "docs/TASK-13-DECISION.md",
            "docs/TASK-13-VERIFICATION.md",
            "examples/downstream_fixture/aligned-transcript.json",
            "examples/downstream_seam.py",
            "scripts/release_gate.py",
            "scripts/release_gate_core.py",
            "tests/test_downstream_seam.py",
        ):
            self.assertIn(required, policy["sdist"]["expectedMembers"])
        self.assertEqual(len(policy["wheel"]["expectedMembers"]), 38)
        self.assertFalse(
            any(
                "downstream" in member
                for member in policy["wheel"]["expectedMembers"]
            )
        )
        schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        sample = {
            "schemaVersion": "tritrack.release-manifest/v1",
            "project": {
                "name": "tritrack-editing-assistant",
                "version": "0.1.0a0",
                "commit": "a" * 40,
            },
            "sourceInventory": {"count": 1, "sha256": "b" * 64},
            "toolchain": {
                "python": "3.13.15",
                "implementation": "CPython",
                "pip": "26.2",
                "build": "1.5.0",
                "setuptools": "84.0.0",
                "wheel": "0.48.0",
            },
            "platform": {"system": "Darwin", "machine": "arm64"},
            "artifacts": {
                kind: {
                    "sha256": value * 64,
                    "sizeBytes": 1,
                    "memberCount": 1,
                    "memberInventorySha256": value * 64,
                }
                for kind, value in (("wheel", "c"), ("sdist", "d"))
            },
            "reproducibility": {
                "wheelBytesMatch": True,
                "sdistMembersMatch": True,
            },
            "gates": {
                name: "pass"
                for name in (
                    "sourceIdentity",
                    "sourcePrivacy",
                    "wheelArchive",
                    "sdistArchive",
                    "freshInstall",
                    "downstreamSeam",
                )
            },
            "nonClaims": ["no-tag", "no-package-publication"],
        }
        jsonschema.validate(sample, schema)
        sample["unexpected"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(sample, schema)

    def test_03_distribution_members_are_explicit_and_reproducible(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distributions: list[tuple[Path, Path]] = []
            for label in ("first", "second"):
                source = root / label / "source"
                shutil.copytree(
                    ROOT,
                    source,
                    ignore=shutil.ignore_patterns(
                        ".git",
                        ".release-evidence",
                        "__pycache__",
                        "*.egg-info",
                        "build",
                        "dist",
                    ),
                )
                output = root / label / "dist"
                output.mkdir()
                environment = os.environ.copy()
                environment["SOURCE_DATE_EPOCH"] = "1704067200"
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "build",
                        "--no-isolation",
                        "--outdir",
                        str(output),
                    ],
                    cwd=source,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                wheel = next(output.glob("*.whl"))
                sdist = next(output.glob("*.tar.gz"))
                distributions.append((wheel, sdist))

            first_wheel, first_sdist = distributions[0]
            second_wheel, second_sdist = distributions[1]
            self.assertEqual(first_wheel.read_bytes(), second_wheel.read_bytes())

            with zipfile.ZipFile(first_wheel) as archive:
                wheel_entries = {
                    member.filename: archive.read(member)
                    for member in archive.infolist()
                    if not member.is_dir()
                }
            self.assertEqual(
                set(wheel_entries),
                set(policy["wheel"]["expectedMembers"]),
            )
            for forbidden in ("tests/", "docs/", "skills/", "scripts/", ".github/"):
                self.assertFalse(any(forbidden in name for name in wheel_entries))

            sdist_inventories: list[str] = []
            for sdist in (first_sdist, second_sdist):
                with tarfile.open(sdist, mode="r:gz") as archive:
                    entries = {
                        member.name.removeprefix(SDIST_ROOT): archive.extractfile(
                            member
                        ).read()
                        for member in archive.getmembers()
                        if member.isfile()
                    }
                self.assertTrue(all(name and not name.startswith("/") for name in entries))
                self.assertEqual(
                    set(entries),
                    set(policy["sdist"]["expectedMembers"]),
                )
                sdist_inventories.append(normalized_inventory(entries))
                for forbidden in (
                    ".agents/",
                    "docs/reviews/",
                    "docs/superpowers/plans/",
                    "tests/test_maintainer_boundary.py",
                ):
                    self.assertFalse(any(name.startswith(forbidden) for name in entries))
            self.assertEqual(sdist_inventories[0], sdist_inventories[1])

    def test_04_historical_records_have_no_machine_specific_home(self) -> None:
        for relative in (
            "docs/reviews/task-10-closeout-packet-2026-08-17.md",
            "docs/superpowers/plans/2026-08-17-task-10-immutable-run.md",
        ):
            release_gate_core.scan_public_bytes((ROOT / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
~~~

### tests/test_release_ci.py

~~~text
"""Task 11 public release-grade CI configuration contract."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ci.yml"
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"


class ReleaseCiContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.lowered = cls.workflow.casefold()

    def test_exact_fixed_four_cell_matrix(self) -> None:
        cells = re.findall(
            r"- os: (ubuntu-24\.04|macos-26)\n"
            r'\s+python-version: "(3\.12|3\.13)"\n'
            r"\s+architecture: (x64|arm64)",
            self.workflow,
        )
        self.assertEqual(
            cells,
            [
                ("ubuntu-24.04", "3.12", "x64"),
                ("ubuntu-24.04", "3.13", "x64"),
                ("macos-26", "3.12", "arm64"),
                ("macos-26", "3.13", "arm64"),
            ],
        )
        self.assertIn("runs-on: ${{ matrix.os }}", self.workflow)
        self.assertIn("fail-fast: false", self.workflow)
        self.assertNotIn("-latest", self.workflow)

    def test_matrix_runs_complete_build_and_installed_smoke(self) -> None:
        required = (
            "python -m pip install --constraint requirements/ci-constraints.txt pip setuptools",
            "python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'",
            "python -m unittest discover -s tests -v",
            "python -m compileall -q src tests examples scripts",
            "python -m build --wheel --no-isolation",
            "python -m venv",
            "pip check",
            "components --json",
            "validate --help",
            "validate contract --help",
            "validate fcpxml --help",
            "validate paper --help",
            "validate run --help",
            'downstream_dir="$RUNNER_TEMP/tritrack-downstream-seam"',
            'cp examples/downstream_seam.py "$downstream_dir/downstream_seam.py"',
            'cp examples/downstream_fixture/aligned-transcript.json "$downstream_dir/aligned-transcript.json"',
            '"$smoke_python" -I "$downstream_dir/downstream_seam.py"',
            '--tritrack "$smoke_cli"',
            '--aligned "$downstream_dir/aligned-transcript.json"',
            '--output "$downstream_dir/downstream-receipt.json"',
        )
        for command in required:
            self.assertIn(command, self.workflow)

    def test_quality_and_release_jobs_are_single_fixed_cells(self) -> None:
        self.assertRegex(
            self.workflow,
            r"quality:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
        )
        self.assertRegex(
            self.workflow,
            r"release-gate:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
        )
        self.assertGreaterEqual(self.workflow.count('python-version: "3.13"'), 4)
        self.assertIn("ruff check src tests examples scripts", self.workflow)
        self.assertIn(
            "python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v",
            self.workflow,
        )
        self.assertIn(
            "python scripts/release_gate.py --source . --output .release-evidence/ci",
            self.workflow,
        )

    def test_actions_permissions_and_negative_authority_are_closed(self) -> None:
        uses = re.findall(r"uses:\s*([^\s#]+)", self.workflow)
        self.assertTrue(uses)
        self.assertEqual(
            set(uses),
            {
                f"actions/checkout@{CHECKOUT_SHA}",
                f"actions/setup-python@{SETUP_PYTHON_SHA}",
            },
        )
        for action in uses:
            self.assertRegex(action, r"@[0-9a-f]{40}$")
        self.assertRegex(
            self.workflow,
            r"permissions:\n  contents: read\n\njobs:",
        )
        self.assertNotIn("cache:", self.workflow)
        for forbidden in (
            "upload-artifact",
            "download-artifact",
            "gh release",
            "git tag",
            "twine",
            "pypi",
            "sigstore",
            "attest",
            "sbom",
            "secrets.",
            "xmllint",
            "xcodebuild",
        ):
            self.assertNotIn(forbidden, self.lowered)


if __name__ == "__main__":
    unittest.main()
~~~

### tests/test_release_gate.py

~~~text
"""Task 11 maintainer release-gate tests."""

from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import os
import stat
import subprocess
import tarfile
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock

from scripts import release_gate_core


def _policy(*, wheel: list[str] | None = None, sdist: list[str] | None = None):
    return {
        "schemaVersion": "tritrack.package-policy/v1",
        "build": {"sourceDateEpoch": 1704067200},
        "limits": {
            "sourceMaxFiles": 32,
            "sourceMaxFileBytes": 4096,
            "sourceMaxTotalBytes": 32768,
            "archiveMaxBytes": 65536,
            "archiveMaxMembers": 32,
            "memberMaxBytes": 4096,
            "expandedMaxBytes": 32768,
        },
        "source": {
            "allowedFakeHomeUsers": ["editor", "example", "fake", "test"],
            "allowedFakeSecretValues": [
                "example",
                "fake",
                "placeholder",
                "redacted",
                "secret",
                "test",
            ],
            "forbiddenSuffixes": [".mov", ".xlsx"],
        },
        "wheel": {"expectedMembers": wheel or ["demo.py"]},
        "sdist": {
            "root": "demo-1.0/",
            "expectedMembers": sdist or ["README.md"],
        },
    }


def _run(*argv: str, cwd: Path, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        argv,
        cwd=cwd,
        input=input_bytes,
        check=True,
        capture_output=True,
    ).stdout


def _make_repo(root: Path, files: dict[str, bytes] | None = None) -> None:
    (root / "release").mkdir(parents=True)
    (root / "release" / "package-policy-v1.json").write_text(
        json.dumps(_policy()), encoding="utf-8"
    )
    for name, encoded in (files or {"public.txt": b"public\n"}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encoded)
    _run("git", "init", "-q", cwd=root)
    _run("git", "config", "user.name", "Invented Tester", cwd=root)
    _run("git", "config", "user.email", "test@example.invalid", cwd=root)
    _run("git", "add", ".", cwd=root)
    _run("git", "commit", "-qm", "fixture", cwd=root)


def _zip(path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]) -> None:
    with (
        zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive,
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore", UserWarning)
        for name, encoded in entries:
            archive.writestr(name, encoded)


def _tar(
    path: Path,
    entries: list[tuple[tarfile.TarInfo | str, bytes]],
) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name, encoded in entries:
            member = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
            if member.isreg():
                member.size = len(encoded)
            archive.addfile(member, io.BytesIO(encoded) if member.isreg() else None)


class SourceGateTest(unittest.TestCase):
    def test_package_policy_owns_a_fixed_build_epoch(self) -> None:
        self.assertEqual(release_gate_core._build_epoch(_policy()), 1704067200)
        for invalid in (True, 0, -1, "1704067200"):
            policy = _policy()
            policy["build"]["sourceDateEpoch"] = invalid
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core._build_epoch(policy)

    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_gate_descriptor_readers_reject_special_files_before_blocking(self) -> None:
        selected = Path("invented-special-file")
        readers = (
            lambda: release_gate_core._read_regular(selected, 1),
            lambda: release_gate_core._read_archive_bytes(selected, _policy()),
            lambda: release_gate_core._verify_published_archive(
                selected, (1, "a" * 64)
            ),
        )

        for reader in readers:
            observed: list[int] = []

            def reject_special(_path, flags, *_args, observed=observed):
                observed.append(flags)
                raise OSError("invented special file")

            with self.subTest(reader=reader), mock.patch.object(
                release_gate_core.os, "open", side_effect=reject_special
            ), self.assertRaises(release_gate_core.ReleaseGateError):
                reader()
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_NONBLOCK)

    def test_clean_stage_zero_regular_source_is_inventory_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            first = release_gate_core.inventory_tracked_source(root)
            second = release_gate_core.inventory_tracked_source(root)
        self.assertEqual(first, second)
        self.assertEqual(first.count, 2)
        self.assertEqual(len(first.sha256), 64)
        self.assertGreater(first.total_bytes, 0)

    def test_dirty_source_and_tracked_links_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_DIRTY$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").unlink()
            os.symlink("target", root / "public.txt")
            _run("git", "add", "public.txt", cwd=root)
            _run("git", "commit", "-qm", "link", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_submodule_unmerged_and_late_change_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            head = _run("git", "rev-parse", "HEAD", cwd=root).strip().decode()
            _run(
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{head},nested",
                cwd=root,
            )
            _run("git", "commit", "-qm", "gitlink", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            original = release_gate_core._read_regular
            changed = False

            def mutate(path: Path, limit: int) -> bytes:
                nonlocal changed
                encoded = original(path, limit)
                if path.name == "public.txt" and not changed:
                    changed = True
                    path.write_text("late change\n", encoding="utf-8")
                return encoded

            with (
                mock.patch.object(
                    release_gate_core, "_read_regular", side_effect=mutate
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_SOURCE_CHANGED$",
                ),
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_source_bounds_and_forbidden_suffix_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"clip.mov": b"invented"})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE$",
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"large.txt": b"x" * 5000})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_LIMIT$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_privacy_scanner_redacts_paths_and_credentials(self) -> None:
        private_home = b"/" + b"Users" + b"/real-person/project"
        credential = b"API" + b"_KEY=" + b"A" * 36
        bare_token = b"gh" + b"p_" + b"A" * 36
        private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
        for encoded in (private_home, credential, bare_token, private_key):
            with self.subTest(kind=hashlib.sha256(encoded).hexdigest()[:8]):
                with self.assertRaises(release_gate_core.ReleaseGateError) as caught:
                    release_gate_core.scan_public_bytes(encoded)
                message = str(caught.exception)
                self.assertRegex(message, r"^TRITRACK_RELEASE_[A-Z_]+$")
                self.assertNotIn(encoded.decode(), message)

        for public in (
            b"/Users/editor/invented",
            b"/home/example/demo",
            b"password=placeholder",
            b"secret=test",
        ):
            release_gate_core.scan_public_bytes(public)

    def test_policy_allowlists_and_nested_keys_cannot_drift_from_scanner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            policy_path = root / "release" / "package-policy-v1.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["source"]["allowedFakeHomeUsers"].append("real-person")
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            _run("git", "add", ".", cwd=root)
            _run("git", "commit", "-qm", "policy drift", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            policy_path = root / "release" / "package-policy-v1.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["wheel"]["unexpected"] = True
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            _run("git", "add", ".", cwd=root)
            _run("git", "commit", "-qm", "policy extension", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core.inventory_tracked_source(root)


class ArchiveGateTest(unittest.TestCase):
    def test_safe_wheel_and_sdist_return_only_counts_and_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            _zip(wheel, [("demo.py", b"print('public')\n")])
            _tar(sdist, [("demo-1.0/README.md", b"public\n")])
            wheel_result = release_gate_core.inspect_wheel(wheel, _policy())
            sdist_result = release_gate_core.inspect_sdist(sdist, _policy())
        for result in (wheel_result, sdist_result):
            self.assertEqual(result.member_count, 1)
            self.assertEqual(len(result.sha256), 64)
            self.assertEqual(len(result.member_inventory_sha256), 64)
            self.assertNotIn("demo", repr(result))

    def test_zip_rejects_traversal_duplicates_casefold_links_and_encryption(self) -> None:
        fixtures: list[tuple[list[tuple[zipfile.ZipInfo | str, bytes]], dict]] = []
        fixtures.append(([("../demo.py", b"x")], _policy(wheel=["../demo.py"])))
        fixtures.append(
            (
                [("demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["demo.py"]),
            )
        )
        fixtures.append(
            (
                [("Demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["Demo.py", "demo.py"]),
            )
        )
        link = zipfile.ZipInfo("demo.py")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        fixtures.append(([(link, b"target")], _policy()))

        for entries, policy in fixtures:
            with self.subTest(size=len(entries)), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "bad.whl"
                _zip(path, entries)
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_wheel(path, policy)

        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "encrypted.whl"
            _zip(path, [("demo.py", b"x")])
            encoded = bytearray(path.read_bytes())
            local = encoded.find(b"PK\x03\x04")
            central = encoded.find(b"PK\x01\x02")
            encoded[local + 6] |= 1
            encoded[central + 8] |= 1
            path.write_bytes(encoded)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_ENCRYPTED$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

    def test_tar_rejects_wrong_root_links_and_unexpected_members(self) -> None:
        link = tarfile.TarInfo("demo-1.0/README.md")
        link.type = tarfile.SYMTYPE
        link.linkname = "target"
        fixtures = (
            ([("other/README.md", b"x")], _policy(sdist=["README.md"])),
            ([(link, b"")], _policy()),
            (
                [("demo-1.0/README.md", b"x"), ("demo-1.0/extra", b"x")],
                _policy(),
            ),
        )
        for entries, policy in fixtures:
            with self.subTest(), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "bad.tar.gz"
                _tar(path, list(entries))
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_sdist(path, policy)

    def test_archive_bounds_privacy_and_inventory_mode_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "large.whl"
            _zip(path, [("demo.py", b"x" * 5000)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_LIMIT$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            private_home = b"/" + b"home" + b"/real-person/private"
            _zip(path, [("demo.py", private_home)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_PRIVATE_PATH$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            executable = zipfile.ZipInfo("demo.py")
            executable.create_system = 3
            executable.external_attr = (stat.S_IFREG | 0o755) << 16
            _zip(path, [(executable, b"public\n")])
            first = release_gate_core.inspect_wheel(path, _policy())
            regular = zipfile.ZipInfo("demo.py")
            regular.create_system = 3
            regular.external_attr = (stat.S_IFREG | 0o644) << 16
            _zip(path, [(regular, b"public\n")])
            second = release_gate_core.inspect_wheel(path, _policy())
            self.assertNotEqual(
                first.member_inventory_sha256,
                second.member_inventory_sha256,
            )

    def test_archive_hash_is_bound_to_the_same_bounded_bytes_as_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "demo.whl"
            replacement = root / "replacement.whl"
            _zip(path, [("demo.py", b"public\n")])
            original = path.read_bytes()
            replaced = False

            def replace_after_member_read(_encoded: bytes) -> None:
                nonlocal replaced
                if replaced:
                    return
                replaced = True
                replacement.write_bytes(b"x" * 70000)
                os.replace(replacement, path)

            with mock.patch.object(
                release_gate_core,
                "scan_public_bytes",
                side_effect=replace_after_member_read,
            ):
                result = release_gate_core.inspect_wheel(path, _policy())

            self.assertTrue(replaced)
            self.assertEqual(result.size_bytes, len(original))
            self.assertEqual(result.sha256, hashlib.sha256(original).hexdigest())


class OrchestrationTest(unittest.TestCase):
    def test_command_output_limit_terminates_before_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            command = [
                os.fspath(Path(os.sys.executable)),
                "-c",
                "import os,time; os.write(1,b'x'*65); time.sleep(2)",
            ]
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_COMMAND_LIMIT$",
            ):
                release_gate_core._run_command(
                    command,
                    cwd=root,
                    env={"PATH": os.defpath},
                    timeout=1,
                    output_limit=64,
                )

    def test_build_uses_fixed_epoch_and_exact_local_toolchain(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot"
            snapshot.mkdir()
            output = root / "dist"

            def fake_command(argv, **_kwargs):
                calls.append(tuple(str(value) for value in argv))
                output.mkdir(exist_ok=True)
                (output / "demo-1.0-py3-none-any.whl").write_bytes(b"wheel")
                (output / "demo-1.0.tar.gz").write_bytes(b"sdist")
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_installed_tool_versions",
                    return_value={
                        "pip": "26.2",
                        "build": "1.5.0",
                        "setuptools": "84.0.0",
                        "wheel": "0.48.0",
                    },
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                wheel, sdist = release_gate_core.build_distributions(
                    snapshot, output, epoch=1704067200
                )

        self.assertEqual(wheel.name, "demo-1.0-py3-none-any.whl")
        self.assertEqual(sdist.name, "demo-1.0.tar.gz")
        self.assertEqual(
            calls,
            [
                (
                    os.fspath(Path(os.sys.executable)),
                    "-m",
                    "build",
                    "--no-isolation",
                    "--outdir",
                    os.fspath(output),
                )
            ],
        )

    def test_fresh_install_uses_only_local_wheel_and_smokes_all_help(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
            wheel.write_bytes(b"invented wheel")
            source = root / "source"
            fixture = source / "examples" / "downstream_fixture" / "aligned-transcript.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_text(
                json.dumps(
                    {
                        "schemaVersion": "tritrack.aligned-transcript/v1",
                        "takes": [{"cues": [{}]}],
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            script = source / "examples" / "downstream_seam.py"
            script.write_text("# invented public consumer\n", encoding="utf-8")

            def fake_command(argv, **_kwargs):
                normalized = tuple(str(value) for value in argv)
                calls.append(normalized)
                if normalized[-2:] == ("components", "--json"):
                    return json.dumps(
                        {
                            "schemaVersion": "tritrack.components/v1",
                            "components": [{}] * 11,
                        }
                    ).encode()
                if "importlib.metadata" in " ".join(normalized):
                    return b"tritrack-editing-assistant\t0.1.0a0\n"
                if len(normalized) > 2 and normalized[1] == "-I":
                    copied_script = Path(normalized[2])
                    copied_fixture = Path(
                        normalized[normalized.index("--aligned") + 1]
                    )
                    output = Path(normalized[normalized.index("--output") + 1])
                    self.assertNotIn(source, copied_script.parents)
                    self.assertNotIn(source, copied_fixture.parents)
                    self.assertEqual(copied_script.read_bytes(), script.read_bytes())
                    self.assertEqual(copied_fixture.read_bytes(), fixture.read_bytes())
                    artifact_sha256 = hashlib.sha256(
                        copied_fixture.read_bytes()
                    ).hexdigest()
                    output.write_text(
                        json.dumps(
                            {
                                "schemaVersion": (
                                    "example.tritrack-downstream-receipt/v1"
                                ),
                                "engineAuthority": {
                                    "artifactSha256": artifact_sha256,
                                    "contractName": "aligned-transcript-v1",
                                    "contractSchemaVersion": (
                                        "tritrack.aligned-transcript/v1"
                                    ),
                                    "validationScope": "contract",
                                },
                                "derivedObservation": {
                                    "takeCount": 1,
                                    "cueCount": 1,
                                },
                            },
                            sort_keys=True,
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                    return b'{"schemaVersion":"example.tritrack-downstream-summary/v1"}\n'
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_wheel_project_identity",
                    return_value=("tritrack-editing-assistant", "0.1.0a0"),
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                release_gate_core.fresh_install_smoke(
                    wheel, root / "smoke", source
                )

        flattened = [" ".join(call) for call in calls]
        install = [
            call
            for call in flattened
            if "pip" in call.split() and "install" in call.split()
        ]
        self.assertTrue(any("pip==26.2" in call for call in install))
        self.assertTrue(any(os.fspath(wheel) in call for call in install))
        self.assertFalse(any("-e" in call.split() for call in install))
        for mode in ("contract", "fcpxml", "paper", "run"):
            self.assertTrue(
                any(f"validate {mode} --help" in call for call in flattened), mode
            )
        self.assertTrue(
            any("-I" in call and "downstream_seam.py" in call for call in flattened)
        )

    def test_fresh_install_rejects_an_invalid_downstream_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
            wheel.write_bytes(b"invented wheel")
            source = root / "source"
            fixture = source / "examples" / "downstream_fixture" / "aligned-transcript.json"
            fixture.parent.mkdir(parents=True)
            fixture.write_text(
                '{"schemaVersion":"tritrack.aligned-transcript/v1","takes":[{"cues":[{}]}]}\n',
                encoding="utf-8",
            )
            (source / "examples" / "downstream_seam.py").write_text(
                "# invented public consumer\n", encoding="utf-8"
            )

            def fake_command(argv, **_kwargs):
                normalized = tuple(str(value) for value in argv)
                if normalized[-2:] == ("components", "--json"):
                    return json.dumps(
                        {
                            "schemaVersion": "tritrack.components/v1",
                            "components": [{}] * 11,
                        }
                    ).encode()
                if "importlib.metadata" in " ".join(normalized):
                    return b"tritrack-editing-assistant\t0.1.0a0\n"
                if len(normalized) > 2 and normalized[1] == "-I":
                    output = Path(normalized[normalized.index("--output") + 1])
                    output.write_text(
                        '{"schemaVersion":"invented.invalid/v1"}\n',
                        encoding="utf-8",
                    )
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_wheel_project_identity",
                    return_value=(
                        "tritrack-editing-assistant",
                        "0.1.0a0",
                    ),
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_DOWNSTREAM_SEAM$",
                ),
            ):
                release_gate_core.fresh_install_smoke(
                    wheel, root / "smoke", source
                )

    def test_manifest_is_closed_deterministic_and_schema_valid(self) -> None:
        inspection = release_gate_core.DistributionInspection(
            sha256="c" * 64,
            size_bytes=10,
            member_count=2,
            member_inventory_sha256="d" * 64,
        )
        context = release_gate_core.ReleaseContext(
            project_name="tritrack-editing-assistant",
            version="0.1.0a0",
            commit="a" * 40,
            source_inventory=release_gate_core.SourceInventory(
                count=3,
                total_bytes=30,
                sha256="b" * 64,
                commit="a" * 40,
            ),
            toolchain={
                "pip": "26.2",
                "build": "1.5.0",
                "setuptools": "84.0.0",
                "wheel": "0.48.0",
            },
            python_version="3.13.15",
            implementation="CPython",
            system="Darwin",
            machine="arm64",
            wheel=inspection,
            sdist=inspection,
        )
        first = release_gate_core.build_release_manifest(context)
        second = release_gate_core.build_release_manifest(context)
        self.assertEqual(first, second)
        self.assertEqual(
            set(first),
            {
                "schemaVersion",
                "project",
                "sourceInventory",
                "toolchain",
                "platform",
                "artifacts",
                "reproducibility",
                "gates",
                "nonClaims",
            },
        )
        serialized = json.dumps(first, sort_keys=True)
        self.assertEqual(
            first["gates"],
            {
                "sourceIdentity": "pass",
                "sourcePrivacy": "pass",
                "wheelArchive": "pass",
                "sdistArchive": "pass",
                "freshInstall": "pass",
                "downstreamSeam": "pass",
            },
        )
        for forbidden in ("path", "time", "duration", "command", "log", "content"):
            self.assertNotIn(forbidden, serialized.casefold())

    def test_pipeline_failure_never_calls_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(
                    release_gate_core,
                    "inventory_tracked_source",
                    side_effect=release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_SOURCE_DIRTY"
                    ),
                ),
                mock.patch.object(release_gate_core, "publish_release") as publish,
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.run_release_gate(root, root / "absent")
            publish.assert_not_called()


class PublicationTest(unittest.TestCase):
    @staticmethod
    def manifest(wheel: bytes, sdist: bytes) -> bytes:
        return (
            json.dumps(
                {
                    "artifacts": {
                        "wheel": {
                            "sha256": hashlib.sha256(wheel).hexdigest(),
                            "sizeBytes": len(wheel),
                        },
                        "sdist": {
                            "sha256": hashlib.sha256(sdist).hexdigest(),
                            "sizeBytes": len(sdist),
                        },
                    }
                },
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )

    def test_artifacts_are_linked_before_manifest_and_existing_output_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            manifest = self.manifest(b"wheel", b"sdist")
            release_gate_core.publish_release(output, wheel, sdist, manifest)
            self.assertEqual((output / wheel.name).read_bytes(), b"wheel")
            self.assertEqual((output / sdist.name).read_bytes(), b"sdist")
            self.assertEqual((output / "release-manifest.json").read_bytes(), manifest)

            sentinel = root / "existing"
            sentinel.mkdir()
            (sentinel / "keep").write_text("untouched", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_OUTPUT_EXISTS$",
            ):
                release_gate_core.publish_release(sentinel, wheel, sdist, manifest)
            self.assertEqual((sentinel / "keep").read_text(), "untouched")

    def test_interruption_before_last_link_leaves_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            real_link = os.link
            calls = 0

            def interrupted(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_INTERRUPTED"
                    )
                real_link(source, destination)

            with (
                mock.patch.object(
                    release_gate_core, "_link_file", side_effect=interrupted
                ),
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.publish_release(
                    output,
                    wheel,
                    sdist,
                    self.manifest(b"wheel", b"sdist"),
                )
            self.assertTrue(output.is_dir())
            self.assertFalse((output / "release-manifest.json").exists())

    def test_late_archive_change_before_manifest_link_fails_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            real_fsync = release_gate_core._fsync_directory
            calls = 0

            def mutate_after_archive_links(path: Path) -> None:
                nonlocal calls
                calls += 1
                real_fsync(path)
                if calls == 1:
                    wheel.write_bytes(b"changed")

            with (
                mock.patch.object(
                    release_gate_core,
                    "_fsync_directory",
                    side_effect=mutate_after_archive_links,
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_ARCHIVE_CHANGED$",
                ),
            ):
                release_gate_core.publish_release(
                    output,
                    wheel,
                    sdist,
                    self.manifest(b"wheel", b"sdist"),
                )
            self.assertTrue(output.is_dir())
            self.assertFalse((output / "release-manifest.json").exists())


class ReleaseCliTest(unittest.TestCase):
    def test_cli_success_prints_only_bounded_receipt_facts(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        manifest = {
            "project": {"commit": "a" * 40, "version": "0.1.0a0"},
            "artifacts": {
                "wheel": {"sha256": "b" * 64},
                "sdist": {"sha256": "c" * 64},
            },
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                return_value=manifest,
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", "invented-source", "--output", "invented-output"]
            )
        self.assertEqual(result, 0)
        self.assertEqual(stderr.getvalue(), "")
        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "RELEASE_GATE\tPASS")
        self.assertEqual(len(lines), 6)
        self.assertFalse(any("invented" in line for line in lines))

    def test_cli_usage_and_gate_failures_are_json_codes_only(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = release_gate.main([])
        self.assertEqual(result, 64)
        self.assertEqual(
            json.loads(stderr.getvalue()), {"error": "TRITRACK_RELEASE_USAGE"}
        )

        stderr = io.StringIO()
        private = "/" + "Users" + "/real-person/private"
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                side_effect=release_gate_core.ReleaseGateError(
                    "TRITRACK_RELEASE_PRIVATE_PATH"
                ),
            ),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", private, "--output", "invented-output"]
            )
        self.assertEqual(result, 1)
        self.assertEqual(
            json.loads(stderr.getvalue()),
            {"error": "TRITRACK_RELEASE_PRIVATE_PATH"},
        )
        self.assertNotIn(private, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
~~~

## Complete Task 13 diff from public main

~~~diff
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index cbbf8dbf6a1f3fbc25aadfdab1a1ce1e3609c830..f114376a8fdcbf4eaa02128f2b5268fab47fa032 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -65,6 +65,15 @@ jobs:
|          "$smoke_cli" validate fcpxml --help
|          "$smoke_cli" validate paper --help
|          "$smoke_cli" validate run --help
+          downstream_dir="$RUNNER_TEMP/tritrack-downstream-seam"
+          test ! -e "$downstream_dir"
+          mkdir "$downstream_dir"
+          cp examples/downstream_seam.py "$downstream_dir/downstream_seam.py"
+          cp examples/downstream_fixture/aligned-transcript.json "$downstream_dir/aligned-transcript.json"
+          "$smoke_python" -I "$downstream_dir/downstream_seam.py" \
+            --tritrack "$smoke_cli" \
+            --aligned "$downstream_dir/aligned-transcript.json" \
+            --output "$downstream_dir/downstream-receipt.json"
|
|  quality:
|    name: Public quality and policy contracts
diff --git a/MANIFEST.in b/MANIFEST.in
index 6edd3aadad38ba50caf2f7e4e09e588830461684..eb5489c7486d1966b4b3e6eb34888991a41c2500 100644
--- a/MANIFEST.in
+++ b/MANIFEST.in
@@ -10,9 +10,11 @@ include MANIFEST.in
|include .github/workflows/ci.yml
|include docs/ROADMAP.md
|include docs/TASK-11-VERIFICATION.md
+include docs/TASK-13-DECISION.md
+include docs/TASK-13-VERIFICATION.md
|include docs/TOOLING.md
|include docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
-recursive-include examples *.py
+recursive-include examples *.py *.json
|recursive-include skills/tritrack-editing-assistant *.md *.yaml
|include scripts/capture_basic_title_binding.py
|include scripts/release_gate.py
diff --git a/README.md b/README.md
index 392a6eaedd15949cc1b7be7f7586d9e3776e54e0..2a33d0b18e74fdd9b5178bd6ece6cd7f57e9fa66 100644
--- a/README.md
+++ b/README.md
@@ -293,6 +293,38 @@ a format, search sibling paths, probe source media, consult a DTD, launch a
|GUI, or make a network request. A passing result is evidence only inside the
|reported scope.
|
+## Supported downstream integration seam
+
+Task 13 makes the existing versioned artifacts and installed
+`tritrack validate ... --json` commands the exclusive supported downstream
+integration seam for v1. Internal Python modules and functions remain
+implementation details, not a compatibility contract. No plugin loader,
+stable Python facade, service, or second engine authority was added.
+
+The standard-library reference consumer demonstrates the boundary with only
+invented public data:
+
+```bash
+python -I examples/downstream_seam.py \
+  --tritrack venv/bin/tritrack \
+  --aligned examples/downstream_fixture/aligned-transcript.json \
+  --output downstream-receipt.json
+```
+
+It accepts only the exact aligned-transcript contract and `contract` scope,
+binds the validator's exact artifact SHA-256 to the bytes it reads, derives
+only take and cue counts, revalidates before publication, and creates one
+absent `example.*` sidecar. That sidecar is downstream-owned and
+non-authoritative: it does not repair, replace, retime, rewrite, or validate
+engine facts.
+
+The maintainer release gate copies the consumer and fixture outside the source
+snapshot and exercises them against a fresh wheel-only installation. A closed
+release manifest records this proof as `downstreamSeam: pass`; the wheel still
+contains only the original runtime members. Task 13 makes no tag, no package
+publication, no private integration, no release, and no production-stability
+claim.
+
|## One-minute invented quickstart
|
|After the development installation above, exercise the complete implemented
diff --git a/STATUS.md b/STATUS.md
index 02bfd42a1d506faa97a6d60308cae3c2300b30b3..b3376a83894bd9be7df8c530db52e15862ac6da5 100644
--- a/STATUS.md
+++ b/STATUS.md
@@ -8,7 +8,7 @@ tester outreach
|
|## Current gate
|
-Tasks 1–12 are complete in this public candidate. Task 6 began from exact
+Tasks 1–13 are complete in this public candidate. Task 6 began from exact
|Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
|fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
|rewrite or merge commit.
@@ -195,12 +195,35 @@ and usage provenance remain self-reported, and the result does not convert any
|earlier wrapper timeout or ambiguous dispatch into formal completion. Public
|review and adjudication records are in `docs/reviews/tasks-7-11-claude-manual-*`.
|
+Task 13 selects Option A: the existing versioned artifacts and installed
+`tritrack validate ... --json` commands are the exclusive supported v1
+downstream seam. Internal Python modules remain implementation details. The
+standard-library `examples/downstream_seam.py` consumer accepts only exact
+aligned-contract／scope／hash facts, derives only take and cue counts,
+revalidates before publication, and writes one downstream-owned `example.*`
+sidecar that is never engine authority.
+
+The implementation proof uses only invented public text. Its focused tests
+cover the successful black-box path, output preservation, unknown-version and
+hash-mismatch rejection, and changed second-validation rejection. Packaging
+keeps the wheel's original 38 members unchanged, adds the proof only to the
+sdist, and exercises it outside the source tree against a fresh wheel-only
+installation. The local release manifest records `downstreamSeam: pass`.
+Design brainstorming completed independently in Codex and through Gemini;
+Claude's single subscription-only attempt timed out and remains incomplete
+without retry, downgrade, substitution, or paid fallback.
+
+Task 13 makes no tag, no package publication, no private integration, no
+GitHub Release, pull request, tester contact, signing, attestation, SBOM,
+Final Cut GUI, DTD, live-provider, application-submission, or
+production-stability claim. Evidence is in `docs/TASK-13-VERIFICATION.md`.
+
|## Next action
|
-Task 13 proves the public engine as the generic authority and defines a
-deliberate downstream integration seam. Task 12 does not authorize or claim
-tags, releases, package publication, tester contact, private integration, or
-application submission.
+Complete Task 13 closeout review, rerun the clean release gate, fast-forward
+the reviewed candidate to public `main`, and verify the fixed six-job CI run at
+the exact remote SHA. This next action does not authorize a tag, release,
+package publication, private integration, or tester contact.
|
|## Implemented surface
|
@@ -224,6 +247,8 @@ application submission.
|- separate installed end-user editing skill with two explicit human gates;
|- four-mode read-only artifact validation with scope-limited path-free
|  summaries;
+- explicit versioned-artifact／installed-CLI downstream seam with an
+  out-of-tree standard-library proof and named `downstreamSeam` release gate;
|- clean tracked-source privacy, bounded archive inspection, reproducible
|  packaging, fresh-wheel installation, and manifest-last local candidate gate;
|- fixed Ubuntu／macOS and Python 3.12／3.13 release-grade public CI;
diff --git a/docs/ROADMAP.md b/docs/ROADMAP.md
index 6ca3bdde293d70acbf5c14d38dda0c0d19e04349..e98e876c3da2d222519d88384d410a83156574a0 100644
--- a/docs/ROADMAP.md
+++ b/docs/ROADMAP.md
@@ -35,13 +35,17 @@ here.
|  archive privacy gates, reproducible wheel／sdist package contracts, a
|  manifest-last local candidate receipt, and fixed Ubuntu／macOS CI across
|  Python 3.12／3.13.
+- Task 12: frozen and independently reviewed public alpha composition with
+  bounded-input and clean-package fix-forward hardening.
+- Task 13: the existing versioned artifacts and installed validators are the
+  exclusive v1 downstream seam; an out-of-tree standard-library consumer and
+  fresh wheel-only `downstreamSeam` gate prove the public engine remains the
+  generic authority without adding a Python API or private integration.
|
|## Alpha-candidate sequence
|
-- Task 12 freezes and independently reviews the alpha candidate. `STATUS.md`
-  alone records whether this gate is pending or complete.
-- Task 13 proves the public engine as the generic authority and defines a
-  deliberate downstream integration seam after Task 12 is complete.
+Tasks 12 and 13 are complete. `STATUS.md` owns the exact current candidate,
+verification, review, and remote-custody state.
|
|## Outward-action boundary
|
@@ -51,3 +55,6 @@ follows the standing-authorization model in `AGENTS.md` and the public
|maintainer skill: once a capability is explicitly granted for the same target,
|visibility, scope, and risk, it remains valid until revoked and must not be
|requested again.
+
+Task 13 makes no tag, no package publication, and no private integration
+claim. It also makes no release or production-stability claim.
diff --git a/docs/TASK-13-DECISION.md b/docs/TASK-13-DECISION.md
new file mode 100644
index 0000000000000000000000000000000000000000..f0d33f5246ec6505c3e6241ac9418586d8f6e674
--- /dev/null
+++ b/docs/TASK-13-DECISION.md
@@ -0,0 +1,149 @@
+# Task 13 generic-authority downstream seam decision
+
+Decision date: 2026-08-18
+
+Decision owner: producer
+
+Selected option: A — existing artifact／CLI seam plus black-box proof
+
+## Decision
+
+The public engine's existing versioned artifacts and installed command-line
+validators are the exclusive supported downstream integration seam for v1.
+Task 13 does not add an in-process plugin system, stable Python facade, network
+service, or new runtime authority.
+
+A separately owned downstream consumer integrates by:
+
+1. selecting the narrowest installed `tritrack validate ... --json` scope that
+   matches the artifact facts it needs;
+2. accepting only the exact contract and validation scope it understands;
+3. reading immutable engine artifact bytes without changing them;
+4. binding any downstream-owned result to the exact hashes reported by the
+   engine validator;
+5. revalidating before publishing if it reads after the initial validation;
+6. writing only to an absent output outside the engine artifact or run bundle;
+   and
+7. using its own namespace and accurately limiting its claims.
+
+Internal Python modules and functions are implementation details. Their
+current importability does not make them a compatibility surface.
+
+## Authority ownership
+
+The public engine remains the only authority for its existing domains:
+
+- transcript text and cue timing: transcript and aligned-transcript artifacts;
+- synchronization facts: sync-map artifacts;
+- editor grouping intent: grouping artifacts;
+- compiled selection facts: working-cut artifacts;
+- immutable run facts: run manifests and their fixed artifact hashes; and
+- structural transports and projections: workbooks and FCPXML remain
+  non-authoritative for the facts from which they are derived.
+
+A downstream sidecar may summarize, index, route, or apply separate policy to
+exact engine facts. It is never an engine contract and may not claim to repair,
+replace, retime, rewrite, or validate the authority it references.
+
+## Supported process boundary
+
+The installed help for each command remains the flag authority. Downstream
+automation may rely only on machine-readable `--json` output, documented exit
+classes, exact `schemaVersion`, exact `validationScope`, and exact hashes. It
+must not parse human output or error prose.
+
+The current scopes retain their existing limits:
+
+- `contract` proves one JSON value satisfies one installed schema; it does not
+  prove parent existence or cross-artifact binding;
+- `structural-profile` proves installed FCPXML profile and binding structure;
+- `authority-bound` proves one workbook is acceptable against exact aligned
+  bytes; and
+- `complete-run-bundle` proves one immutable bundle's fixed files, contracts,
+  manifest semantics, and hashes, without reconstructing prior bundles.
+
+No new schema-discovery command is added. The selected black-box proof must
+first fail because installed commands cannot expose a necessary engine-owned
+fact before Task 13 may add such a surface.
+
+## Public black-box proof
+
+`examples/downstream_seam.py` is a deliberately small out-of-tree reference
+consumer. It imports only the Python standard library and invokes the installed
+`tritrack validate contract --json` process. With one invented
+`aligned-transcript-v1` input it:
+
+- requires the exact contract and scope;
+- binds the exact artifact hash;
+- derives only take and cue counts;
+- repeats validation before publication;
+- writes a canonical, namespaced, non-authoritative sidecar to an absent path;
+  and
+- prints only a path-free, text-free completion summary.
+
+The reference sidecar schema begins `example.`, not `tritrack.`. It is an
+illustration of downstream ownership, not a new public engine contract.
+
+The release-readiness gate copies the reference consumer and invented fixture
+outside the source snapshot, runs it with isolated Python against a fresh
+wheel-only installation, verifies the sidecar, and records a named
+`downstreamSeam` pass. The wheel exposes no additional runtime module or
+component for this proof.
+
+## Compatibility rule
+
+V1 compatibility is explicit rather than inferred:
+
+- consumers select exact contract and summary schema versions;
+- unknown versions fail closed;
+- new incompatible meanings require a new schema or seam decision;
+- internal Python changes are not seam changes; and
+- an example sidecar may evolve without becoming an engine contract, but its
+  example `schemaVersion` must still change when its meaning changes.
+
+## Privacy and custody
+
+The seam does not grant access to media or transcript-bearing artifacts. The
+caller decides which local artifact enters a downstream consumer and retains
+its custody obligations. Public proof uses only invented text. Engine and
+consumer outputs contain no credential, private path, account, host, command,
+timestamp, duration, or private-domain vocabulary.
+
+## Rejected alternatives
+
+- A stable Python facade would create Python ABI, exception, typing, and
+  supported-version obligations without evidence that the process boundary is
+  inadequate.
+- An in-process plugin protocol would run downstream code inside the authority
+  process and add discovery, dependency, isolation, and crash policy.
+- A new handoff authority would duplicate facts already owned by existing
+  contracts and manifests.
+- A live private integration would cross the public／private role firewall and
+  remains separately gated.
+
+## Falsification and revision boundary
+
+Option A is falsified only if the fresh-wheel reference consumer must import
+engine internals or duplicate an engine-owned validation rule to bind the
+required facts, or if a measured required integration cannot tolerate the
+process boundary. The first result permits reconsidering a minimal read-only
+discovery command; the second permits reconsidering a versioned Python facade.
+Neither result authorizes a plugin loader or private implementation intake.
+
+## Non-claims
+
+Task 13 does not create a tag, release, package publication, pull request,
+tester contact, signing, attestation, SBOM, live provider call, GUI result,
+DTD result, private downstream implementation, application submission, or
+production-stability claim.
+
+## Brainstorm provenance
+
+The frozen public packet SHA-256 was
+`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`.
+Codex completed independently before external outputs. Gemini requested,
+observed, and completed `gemini-3.7-flash`. Claude's single subscription-only
+attempt requested the dynamic `opus` alias and ended `claude-timeout` with no
+observed or completed model and ambiguous dispatch; it remains incomplete with
+no retry, downgrade, substitution, or paid fallback. The producer selected
+Option A on 2026-08-18.
diff --git a/docs/TASK-13-VERIFICATION.md b/docs/TASK-13-VERIFICATION.md
new file mode 100644
index 0000000000000000000000000000000000000000..3fe8c0138164cf2e32f8e86e1664611098f32527
--- /dev/null
+++ b/docs/TASK-13-VERIFICATION.md
@@ -0,0 +1,107 @@
+# Task 13 generic-authority seam verification
+
+Verification date: 2026-08-18
+
+Status: coherent implementation is green on an isolated public OSS branch;
+closeout review and exact-SHA integration remain pending.
+
+## Approved design
+
+The producer selected Option A: existing versioned artifacts and installed
+`tritrack validate ... --json` commands remain the exclusive v1 downstream
+seam. Task 13 adds a black-box proof, not a stable Python facade, plugin loader,
+network service, new runtime authority, or private integration.
+
+## Baseline
+
+Before Task 13 behavior tests or implementation existed, the constrained
+Python 3.13 environment passed 252 complete `unittest` tests in 21.532 seconds.
+
+## TDD evidence
+
+The first focused run was:
+
+```text
+venv/bin/python -m unittest tests.test_downstream_seam -v
+```
+
+It ran one test and failed exactly because
+`examples/downstream_seam.py` did not exist. The process returned 2 with the
+Python file-open error for that missing public path. This is the observed RED
+for the black-box consumer; no consumer implementation existed when it ran.
+
+After the remaining fail-closed cases were added, a second pre-implementation
+run executed four tests: the valid path failed with the same missing-file
+return, and three negative cases errored only when their assertions attempted
+to parse that missing-file stderr as JSON. No consumer implementation existed
+for either RED run.
+
+The complete focused GREEN run executed five tests in 1.502 seconds. All five
+passed, including exact authority consumption, existing-output preservation,
+unknown-version rejection, validator-hash mismatch rejection, and changed
+second-validation rejection.
+
+The release-gate RED then reported two signature errors because
+`fresh_install_smoke` did not yet accept a source snapshot, one closed-manifest
+gate mismatch, and one packaging member mismatch. After the gate copied the
+proof out of tree and required its exact receipt, 30 release, manifest, and
+seam tests passed in 2.164 seconds.
+
+The packaging／CI RED then reported exactly three missing integrations: Task 13
+members were absent from the sdist policy, the built sdist disagreed with that
+policy, and the fixed CI wheel smoke did not run the consumer. After the exact
+sdist and CI wiring, all 13 packaging, CI, and seam tests passed in 3.932
+seconds.
+
+## Generic-authority proof
+
+`examples/downstream_seam.py` is a black-box standard-library consumer. It
+does not import engine internals. It invokes installed
+`tritrack validate contract --json`, requires
+`tritrack.validate-summary/v1`, `validationScope: contract`,
+`aligned-transcript-v1`, and `tritrack.aligned-transcript/v1`, then binds the
+validator-reported SHA-256 to the exact regular-file bytes it consumes.
+
+The invented fixture SHA-256 is
+`602f439a2d2eb1e8479035b1d92ffeb46bf4d276e014bbe48a584b38f1c5a6f6`.
+The consumer derives only one take and one cue, repeats validation before
+publication, creates a canonical `example.tritrack-downstream-receipt/v1`
+sidecar at an absent path, and prints a path-free, transcript-text-free
+summary. The sidecar is downstream-owned and non-authoritative; it is never an
+engine contract.
+
+The maintainer release gate copies the script and fixture outside the verified
+source snapshot, invokes isolated Python and the installed CLI from a fresh
+wheel-only environment, and requires the exact sidecar. The release manifest
+records `downstreamSeam: pass`. The wheel member set remains the original 38;
+only the sdist carries the decision, verification, example, invented fixture,
+and regression test.
+
+## Design-review provenance
+
+The frozen brainstorming packet SHA-256 was
+`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`.
+Codex completed its independent analysis before external results were read.
+Gemini requested, observed, and completed `gemini-3.7-flash`. Claude's single
+subscription-only attempt ID was
+`d13e8a66-75a2-4342-a7e9-c65844a60458`; it requested the dynamic `opus`
+capability alias and ended `claude-timeout` with no observed or completed model
+and ambiguous dispatch. It was not retried, downgraded, substituted, or sent
+through a paid API.
+
+## Coherent implementation validation
+
+Before the implementation-target commit, the constrained Python 3.13
+environment passed all 259 tests in 21.894 seconds. Ruff passed every Python
+surface under `src`, `tests`, `examples`, and `scripts`; `compileall` passed
+the same four trees; the maintainer identity check returned
+`projectKind: public-engine` and `lane: OSS`; and `git diff --check` passed.
+The focused governance suite passed all 11 tests.
+
+## Non-claims
+
+Task 13 makes no tag, no package publication, no private integration, no
+GitHub Release, pull request, tester contact, signing, attestation, SBOM,
+Final Cut GUI, DTD, live-provider, application-submission, or
+production-stability claim. It adds no stable Python facade, plugin loader,
+network service, new engine contract, or second authority.
diff --git a/docs/TOOLING.md b/docs/TOOLING.md
index d4ab477869bb0aeaac234584b876827e06e85505..e0d73fecd97a712fe56e7fdc1dbed0a945aa0759 100644
--- a/docs/TOOLING.md
+++ b/docs/TOOLING.md
@@ -41,6 +41,35 @@ All four modes are read-only. The command does not repair an artifact, guess a
|format, discover sibling inputs, write a result, use network access, or broaden
|success beyond its exact scope.
|
+## Task 13 downstream seam
+
+Task 13 keeps the process boundary deliberate: versioned artifacts plus the
+installed `tritrack validate ... --json` commands are the exclusive supported
+v1 integration seam. Internal Python modules are not a compatibility surface.
+Use installed help as the flag authority and accept only the exact summary
+schema, validation scope, contract version, and hashes the consumer knows.
+
+The public black-box proof is:
+
+```text
+python -I examples/downstream_seam.py \
+  --tritrack tritrack \
+  --aligned examples/downstream_fixture/aligned-transcript.json \
+  --output ABSENT_SIDECAR.json
+```
+
+`examples/downstream_seam.py` uses only the standard library. It invokes
+`tritrack validate contract --json`, binds the reported hash to the exact
+bytes it reads, accepts only `aligned-transcript-v1`, derives take／cue counts,
+revalidates, and writes one absent `example.*` sidecar. The sidecar is
+downstream-owned and never an engine contract or authority.
+
+The release-readiness gate copies both public example files outside the source
+snapshot and runs them with isolated Python and the installed CLI from a fresh
+wheel-only environment. The closed manifest records `downstreamSeam: pass`.
+The proof adds sdist documentation and examples but adds no wheel runtime
+member, plugin hook, network service, or private integration.
+
|## Maintainer release-readiness gate
|
|The only maintainer entry point is:
@@ -62,7 +91,7 @@ normalized member／content inventories while recording the chosen compressed
|archive's exact SHA-256; it does not claim byte-identical gzip output. A new
|external virtual environment installs only the selected local wheel, runs
|`pip check`, confirms the eleven-component registry, and exercises all five
-validator help authorities.
+validator help authorities plus the Task 13 out-of-tree consumer.
|
|Publication hard-links the two archives first and canonical
|`release-manifest.json` last. The closed manifest contains only project
diff --git a/docs/reviews/task-13-brainstorm-claude-2026-08-18.md.status.json b/docs/reviews/task-13-brainstorm-claude-2026-08-18.md.status.json
new file mode 100644
index 0000000000000000000000000000000000000000..ea3ce143587c2ff49c173a8c206f184f7934831d
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-claude-2026-08-18.md.status.json
@@ -0,0 +1,32 @@
+{
+  "schemaVersion": 2,
+  "attemptId": "d13e8a66-75a2-4342-a7e9-c65844a60458",
+  "startedAt": "2026-08-18T13:27:59.533Z",
+  "provider": "Claude Code",
+  "routingPolicy": "highest-capability-generally-released-at-execution",
+  "requestedModel": "opus",
+  "requestedModelKind": "dynamic-capability-alias",
+  "exactModelPinned": false,
+  "observedModel": null,
+  "completedModel": null,
+  "lane": "Claude Code subscription token via ask-claude.sh",
+  "helperProtocolVersion": "claude-subscription-review/3",
+  "result": "incomplete",
+  "failureClass": "claude-timeout",
+  "modelRequestSent": null,
+  "billingFallbackAllowed": false,
+  "paidCredentialEnvironmentDetected": false,
+  "packetSha256": "e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798",
+  "prompt": "docs/reviews/task-13-brainstorm-packet-2026-08-18.md",
+  "intendedOutput": "docs/reviews/task-13-brainstorm-claude-2026-08-18.md",
+  "rawOutput": "docs/reviews/task-13-brainstorm-claude-2026-08-18.md.raw.json",
+  "rawSha256": null,
+  "repo": ".",
+  "apiEquivalentCostUsd": null,
+  "actualSpendUsd": null,
+  "usage": null,
+  "completedAt": null,
+  "helperExitCode": null,
+  "helperSignal": "SIGALRM",
+  "note": "The hard timeout ended the helper after preflight; whether the model request completed is ambiguous."
+}
diff --git a/docs/reviews/task-13-brainstorm-codex-2026-08-18.md b/docs/reviews/task-13-brainstorm-codex-2026-08-18.md
new file mode 100644
index 0000000000000000000000000000000000000000..c3ded18f1e752222b6789d7c1669287298f3c4e4
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-codex-2026-08-18.md
@@ -0,0 +1,134 @@
+# Task 13 independent Codex brainstorm
+
+This response was completed before any Claude or Gemini answer was read.
+
+## 1. `problem_reframe`
+
+The missing product is not an adapter. It is a small compatibility promise.
+The public engine already has authoritative artifacts, strict validators, and
+an installed process boundary, but downstream authors cannot yet distinguish
+the deliberately supported surface from convenient internal Python imports.
+Task 13 should therefore prove that an integration can remain outside the
+engine and still consume authoritative facts without copying authority.
+
+## 2. `pragmatic_path`
+
+Declare an artifact-and-process seam, not an in-process plugin API. Publish a
+closed machine-readable seam descriptor that names the supported CLI discovery
+and validation commands, accepted authoritative artifact schema versions,
+immutability rules, downstream output namespace rule, compatibility policy,
+and explicit non-claims. Add one tiny out-of-tree reference adapter using only
+an installed wheel's `tritrack` executable and invented artifacts. It should
+validate exact inputs, derive one clearly non-authoritative summary or receipt,
+bind it to input hashes, and refuse changed, unknown-version, or invalid input.
+
+Exercise that adapter from a fresh wheel-only environment in the Task 13 gate.
+The proof passes only if the adapter has no source-tree imports, no private
+configuration, no network, no mutation, and no ability to make its output pass
+as an engine contract.
+
+Tradeoff: this keeps the supported surface narrow and language-neutral, but a
+consumer pays process startup and JSON/file I/O costs. Those costs are minor
+for the current batch editing workflow.
+
+## 3. `alternative_architecture`
+
+Create a minimal stable Python facade such as
+`tritrack_editing_assistant.integration`, exporting typed immutable handles
+for contract discovery and validation while keeping all other modules private.
+A standalone adapter could import only that facade. This improves ergonomics
+and performance for Python consumers, but it immediately creates Python ABI
+and exception-compatibility obligations and does not help non-Python tools.
+
+A materially larger alternative is a plugin entry-point protocol in which the
+engine loads adapters. That reverses custody: untrusted downstream code runs
+inside the authority process. It adds discovery, isolation, crash, dependency,
+and security policy before there is evidence those are needed.
+
+## 4. `low_cost_experiment`
+
+Before committing to a new runtime command, build a temporary out-of-tree
+consumer with only three allowed operations: invoke installed
+`tritrack validate contract --json`, read one invented canonical artifact, and
+write a namespaced receipt to an absent directory. Run it against:
+
+- one valid canonical artifact;
+- the same semantic JSON with noncanonical bytes;
+- an unknown schema version;
+- an artifact changed after validation;
+- an existing output path; and
+- a wheel installation from which the repository source is unavailable.
+
+If the consumer cannot safely bind its output without importing engine code or
+duplicating validation rules, add the smallest discovery or canonical-byte
+helper to the CLI. If it can, do not add a new runtime API.
+
+## 5. `contrarian_challenge`
+
+Task 13 may require no new product code. The contracts, `tritrack validate`, and
+immutable manifests could already be the seam; the real defect may be only
+that the compatibility and ownership promise is undocumented and untested
+from outside the source checkout. A new handoff contract might become a
+redundant eleventh authority-like object and weaken the system it is meant to
+clarify.
+
+## 6. `unconstrained_possibility`
+
+In a future major version, generate language-neutral SDKs and conformance
+vectors from an authority graph: each artifact node would declare its owner,
+canonical encoding, parents, validators, allowed projections, and privacy
+class. Downstream adapters in any language could certify against the same test
+kit. This would be valuable only after multiple independent consumers expose
+real common requirements.
+
+## 7. `overlooked_risks`
+
+- A descriptor that lists contracts but does not bind its own version and
+  bytes is documentation, not a machine-checkable seam.
+- A sample adapter can accidentally become normative even if its output shape
+  was meant as an example.
+- Valid schema bytes are not always sufficient authority; some claims require
+  cross-artifact or complete-bundle validation.
+- Reading an artifact after a separate validator process creates a time-of-
+  check/time-of-use gap unless the adapter binds and rechecks exact bytes.
+- Exporting transcript-bearing artifacts across the seam can widen custody
+  without violating schema validation.
+- Calling internal modules in the reference adapter would silently establish
+  an unsupported Python API.
+- Naming downstream products or directories in engine policy would reverse the
+  dependency and leak domain assumptions.
+- Adding a new packaged file requires exact wheel/sdist policy changes and can
+  invalidate Task 12's package-neutrality baseline; Task 13 must report this
+  honestly rather than claim Task 12 byte equality.
+
+## 8. `assumptions_to_verify`
+
+- A batch/file process seam is adequate for the expected integration cadence.
+- Existing CLI summaries expose enough hashes and scope facts for safe binding.
+- At least one existing artifact set contains all facts a generic consumer
+  legitimately needs; otherwise the seam must identify a closed set rather
+  than one file.
+- The reference proof can run after wheel installation without importing from
+  the checkout.
+- Canonical-byte requirements are either already enforced for every seam input
+  or can be verified without duplicating engine logic.
+- Downstream authors accept explicit major seam versions instead of inferred
+  compatibility from package versions.
+
+## 9. `recommended_next_decision`
+
+Choose between:
+
+A. an artifact-and-process seam plus out-of-tree conformance proof;
+B. a stable Python facade; or
+C. an in-process plugin protocol.
+
+Recommend A, with a decision checkpoint after the low-cost experiment on
+whether a new CLI discovery command is actually necessary. Do not add a new
+authority artifact merely to label existing authorities.
+
+Falsify A if the wheel-only consumer cannot bind and validate the required
+facts atomically through installed commands without duplicating engine rules,
+or if a real required consumer needs high-frequency in-process calls whose
+measured process/file overhead is material. In that case choose the minimal
+Python facade, not the plugin loader.
diff --git a/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md b/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md
new file mode 100644
index 0000000000000000000000000000000000000000..f3b53dfd6b98a00020138a3d68ebeea849f04e5a
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md
@@ -0,0 +1,133 @@
+### 1. `problem_reframe`
+
+The core problem is not "how does a downstream consumer execute or extend TriTrack," but **how an untrusted, out-of-tree consumer unambiguously verifies and ingests TriTrack artifacts without TriTrack giving up custodial authority or stabilizing internal Python internals.**
+
+If downstream integrations consume internal Python imports (`tritrack.core.*`), TriTrack creates an accidental, unbounded API commitment. If downstream integrations read raw filesystem directories without contract validation, they risk mutating state or making unauthorized assumptions about intermediate state.
+
+Therefore, the seam is strictly an **externalized artifact and invocation contract**:
+1. TriTrack emits sealed, immutable, canonical JSON run bundles and validation verdicts.
+2. Downstream consumers consume these as read-only inputs through the CLI and canonical JSON artifacts, using standard schema validation and bundle manifest hash checking.
+3. Downstream outputs (e.g., downstream policies, external execution reports, downstream-specific envelopes) are strictly out-of-tree sidecars referencing TriTrack run manifests by exact SHA-256 hash, with zero write-back into the TriTrack run bundle.
+
+---
+
+### 2. `pragmatic_path`
+
+The narrowest, lowest-risk implementation is a **CLI Contract Introspection & Sidecar Envelope Proof**:
+
+- **CLI Contract & Schema Discovery:** Add a non-mutating CLI inspection command (`tritrack inspect schemas` or `tritrack schema <name> [--version]`) that prints canonical JSON schemas and supported schema versions directly from the installed wheel.
+- **Strict Bundle Ingestion Verification (`tritrack validate bundle <dir>`):** Keep the existing bundle validator as the single source of truth for downstream consumption validation.
+- **Example Downstream Reference Adapter Specification (Documentation + Fixture Contract):**
+  - Define an example minimal JSON schema for downstream consumption (e.g., `downstream-reference-envelope.schema.json` or a documented specification) that lives in documentation/tests.
+  - The downstream envelope captures:
+    1. `targetManifestHash`: exact SHA-256 of the TriTrack `run-manifest.json`.
+    2. `targetSchemaVersion`: TriTrack manifest schema version.
+    3. `downstreamPayload`: domain-specific data produced out-of-tree.
+- **Integration Test Suite (Wheel-Only):**
+  - A wheel-isolated test script running as a simulated external process that:
+    1. Runs `tritrack run ...` or validates an existing bundle fixture.
+    2. Inspects TriTrack schemas via CLI.
+    3. Emits an out-of-tree sidecar referencing the run manifest hash.
+    4. Proves that modifying the TriTrack bundle invalidates the sidecar reference and fails bundle verification.
+    5. Confirms that attempting to import internal modules from a non-supported path fails or emits an unstable warning, proving the seam is CLI/Artifact-only.
+
+**Tradeoffs:**
+- *Pros:* Zero changes to core calculation logic; zero new daemon/RPC/plugin infrastructure; fully testable via installed wheel in CI; clean fail-closed isolation.
+- *Cons:* Downstream consumers must operate via process boundary or direct file/schema validation rather than linked in-process Python calls.
+
+---
+
+### 3. `alternative_architecture`
+
+**Stable Python Read-Only Ingest Module (`tritrack.api.v1` / Pure Data Transfer Objects):**
+- Expose a frozen, minimal Python namespace (`tritrack.api`) providing strictly read-only, schema-validated loader functions:
+  ```python
+  from tritrack.api.v1 import load_run_bundle, validate_contract
+  ```
+- These functions load, parse, verify SHA-256 bundle manifests, and return frozen, read-only Python dataclasses/dicts corresponding directly to the JSON contract schemas.
+- Explicitly mark all other namespaces (`tritrack.internal.*`, `tritrack.cli.*`, `tritrack.engine.*`) as private and subject to breaking changes without notice.
+
+**Tradeoffs:**
+- *Pros:* Higher ergonomics for Python-based downstream tools; avoids CLI subprocess overhead and JSON string serialization parsing if running in Python environments.
+- *Cons:* Expands the public maintenance surface; requires Python version stability guarantees; risks downstream tools attempting in-memory mutations or monkeypatching unless aggressively frozen.
+
+---
+
+### 4. `low_cost_experiment`
+
+**Experiment:** Build a standalone, out-of-repo simulated consumer script (`test_downstream_seam.py`) in CI that treats `tritrack` purely as an installed black-box package.
+
+**Steps:**
+1. Install TriTrack from the built wheel (`.whl`) into a clean virtual environment with `PYTHONPATH=""`.
+2. Generate or extract a valid run bundle fixture.
+3. Assert that `tritrack validate bundle <path>` returns exit code `0` with machine-readable JSON output on `--json`.
+4. Intentionally tamper with one byte in an upstream transcript JSON artifact; assert that `tritrack validate bundle` returns non-zero and pinpointed hash mismatch.
+5. Ingest the bundle via the simulated downstream script, generate a downstream sidecar JSON referencing the manifest hash, and verify the reference.
+6. Verify that running `python -c "import tritrack.some_internal"` produces no supported API guarantee (or is prevented by testing strict entry-point boundaries).
+
+**Falsification Criteria:**
+- If the downstream script requires importing any non-public Python symbol to verify bundle integrity, the experiment fails.
+- If downstream tampering can go undetected by `tritrack validate`, the authority boundary fails.
+
+---
+
+### 5. `contrarian_challenge`
+
+**Challenge: Does Task 13 actually require any new code or schemas at all?**
+
+*Argument:* Tasks 1–12 already defined 10 closed JSON contracts, manifest-last bundle completion, deterministic SHA-256 hashing, and four read-only validation scopes in `tritrack validate`.
+
+If the public engine's authority is *already* fully encapsulated by its immutable artifacts and CLI validator, then adding new schemas, plugin APIs, or export formats creates unneeded complexity and violates the "narrow steel thread" constraint.
+
+*Alternative approach:* Task 13 could be purely:
+1. An explicit **Authority & Seam Contract Document** (e.g. `docs/integration-seam.md`) defining the invariants, manifest pinning rule, and sidecar model.
+2. A single end-to-end integration test asserting that out-of-tree verification and sidecar referencing work exclusively using existing CLI and JSON artifacts.
+3. Formal declaration that the CLI and JSON schemas *are* the sole v1 integration surface.
+
+---
+
+### 6. `unconstrained_possibility`
+
+If freed from public-alpha scope limits, the seam could be structured as an **Attestation & Cryptographic Manifest Log**:
+- Run manifests include cryptographic signatures (ed25519) and deterministic Merkle tree roots of all inputs, sync maps, and outputs.
+- A content-addressable storage (CAS) interface where artifacts are stored by exact content hash (`sha256:...`).
+- Downstream systems attach signed provenance records (in-toto / SLSA-style attestations) claiming downstream actions against a specific immutable root hash.
+- A WebAssembly (Wasm) verification target compiled from the validation core allowing downstream runtimes (browser, Node, Rust, Python) to verify bundle authority in-process without invoking the Python CLI.
+
+---
+
+### 7. `overlooked_risks`
+
+1. **Stdout/Stderr Format Drifts:** Downstream tools wrapping the CLI might parse human-readable stdout instead of structured exit codes or JSON output. If TriTrack CLI output changes, downstream tooling breaks silently unless `--json` flags on validation commands are strictly contract-tested.
+2. **Bundle Mutation Race Conditions:** If a downstream tool attempts to read a bundle while TriTrack is still executing (violating the manifest-last rule), it might read partial outputs. The seam must enforce that a bundle is only valid if `run-manifest.json` exists and matches all artifact hashes.
+3. **Implicit Path Dependency Leakage:** Absolute paths in run manifests or receipt metadata could leak build-machine or editor-machine directory structures to downstream systems, creating brittle environment couplings.
+4. **Accidental `__all__` Exposure:** Downstream Python developers will naturally attempt `import tritrack`. If the top-level `__init__.py` exposes internal helpers without an explicit deprecation or private-warning policy, maintainers face immediate breaking-change pressure.
+
+---
+
+### 8. `assumptions_to_verify`
+
+1. **Wheel Isolation:** Verify that `tritrack validate` works identically when installed in an isolated environment without access to the Git repository root or test fixtures.
+2. **Validation Output Machine-Readability:** Verify whether `tritrack validate` currently provides deterministic, machine-parseable exit codes and JSON output suitable for automated downstream callers.
+3. **No-Write Invariant:** Verify that `tritrack validate` across all 4 scopes is guaranteed read-only and will never touch `mtime`, create lockfiles, or alter files in the target directory.
+4. **Deterministic Hash Invariance:** Verify that re-running canonical serialization and hashing across supported platforms (Linux, macOS, Windows) produces identical byte hashes for identical inputs.
+
+---
+
+### 9. `recommended_next_decision`
+
+#### Producer Decision
+The producer must choose between:
+
+- **Option A (Pure Contract & Test Seam):** Declare the CLI and existing 10 JSON schemas as the complete, exclusive v1 seam. Implement zero new runtime code except CLI schema introspection / JSON validation flags if missing, accompanied by an integration-seam document and a wheel-installed downstream consumption test.
+- **Option B (Python Ingest SPI):** Expose a dedicated, frozen `tritrack.api.v1` read-only loading/validation Python interface alongside the CLI.
+
+#### Recommendation
+**Choose Option A.**
+
+Option A strictly enforces fail-closed, out-of-process isolation, prevents accidental Python API stabilization, preserves the 11-component product registry, and provides the exact falsifiable proof required for public alpha without long-term maintenance baggage.
+
+#### Falsification Evidence
+This recommendation is falsified if:
+1. Performance requirements demand sub-millisecond in-process artifact passing where CLI process invocation latency is demonstrably unacceptable for public-alpha consumers; or
+2. Downstream consumption cannot be completely accomplished using standard Draft 2020-12 JSON Schema validation and SHA-256 hash checks on the canonical artifacts.
\ No newline at end of file
diff --git a/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md.status.json b/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md.status.json
new file mode 100644
index 0000000000000000000000000000000000000000..548af4a6b1c55e0336e1b3a7d4b65a99b8471743
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-gemini-2026-08-18.md.status.json
@@ -0,0 +1,19 @@
+{
+  "schemaVersion": 1,
+  "provider": "google-gemini-api",
+  "routingPolicy": "highest-capability-generally-released-at-execution",
+  "exactPin": null,
+  "eligibleModels": [
+    "gemini-3.7-flash",
+    "gemini-3.6-flash",
+    "gemini-3.5-flash",
+    "gemini-2.5-pro",
+    "gemini-2.5-flash"
+  ],
+  "requestedModel": "gemini-3.7-flash",
+  "observedModel": "gemini-3.7-flash",
+  "completedModel": "gemini-3.7-flash",
+  "status": "completed",
+  "resolvedAt": "2026-08-18T13:27:59.754Z",
+  "completedAt": "2026-08-18T13:28:16.285Z"
+}
diff --git a/docs/reviews/task-13-brainstorm-packet-2026-08-18.md b/docs/reviews/task-13-brainstorm-packet-2026-08-18.md
new file mode 100644
index 0000000000000000000000000000000000000000..69a78a90d1daa0e278bbd47f9f35eeda637a3e3e
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-packet-2026-08-18.md
@@ -0,0 +1,128 @@
+# Task 13 generic-authority seam brainstorm packet
+
+Date: 2026-08-18
+
+Decision owner: producer
+
+Target: public TriTrack Editing Assistant repository, branch
+`feat/task-13-generic-authority-seam`, based on exact public `main` commit
+`7bc035ee379a8a3babd2a6556eecdab2973b6301`.
+
+Instruction: provide design ideation only. Do not edit the repository, request
+private project material, or assume access to any downstream implementation.
+
+## Decision needed now
+
+Choose the smallest Task 13 mechanism that proves the public engine is the
+generic authority while defining an intentional, clear seam for separately
+owned downstream integrations.
+
+Tasks 1–12 are complete. Task 13 is the next and final scheduled public-alpha
+roadmap item. The public repository currently makes no private-integration,
+tag, release, package-publication, or production-stability claim.
+
+## Current public evidence
+
+- The package exposes one installed console entry point, `tritrack`.
+- Ten closed Draft 2020-12 JSON contracts are packaged and resolved by exact
+  `schemaVersion`: compatibility profile, sync map, transcript bundle, text
+  revision, aligned transcript, grouping, working cut, title binding, run
+  manifest, and offline provider receipt.
+- Canonical JSON authorities use exact-byte hashes and closed schemas.
+  Workbook and FCPXML products are transports or projections rather than
+  replacement authorities.
+- Immutable prepared, aligned, and finished run bundles use fixed filenames,
+  exact hashes, prior-manifest chains, absent-output publication, and a
+  manifest-last completion rule.
+- `tritrack validate` provides four read-only scopes: one JSON contract,
+  structural FCPXML profile, authority-bound workbook, and one complete run
+  bundle.
+- The wheel currently contains runtime modules, schemas, profiles, and the
+  CLI. It declares no plugin entry points, stable Python service-provider
+  interface, or public compatibility promise for internal Python functions.
+- The public release gate builds reproducible package candidates and tests a
+  fresh wheel-only installation. Public CI runs the complete suite on the
+  fixed supported OS and Python matrix.
+- Existing invented fixtures are permitted. Private media, transcripts,
+  project names, paths, credentials, templates, and operational evidence are
+  forbidden.
+
+## Required outcome
+
+Task 13 should leave falsifiable public evidence that:
+
+1. a generic, out-of-tree downstream consumer can integrate through an
+   explicit supported boundary without importing private knowledge;
+2. the public engine and its versioned artifacts remain the only authority for
+   transcript text/timing, sync, grouping, selection, and run facts;
+3. downstream-owned policy and outputs cannot silently become or mutate engine
+   authority;
+4. compatibility, failure, versioning, privacy, and ownership rules at the
+   seam are clear enough to test;
+5. no private implementation or live private integration is required or
+   claimed.
+
+## Constraints
+
+- Keep the default workflow local, offline, deterministic, no-overwrite, and
+  fail closed.
+- Prefer a narrow steel-thread proof over a general framework.
+- Reuse existing contracts, validators, bundle hashes, and installed-wheel
+  verification when that is sufficient.
+- Do not create a second transcript, timing, selection, grouping, sync, or run
+  authority.
+- Do not make internal Python modules stable by accident.
+- Do not add private-domain vocabulary or private repository assumptions.
+- Do not change the eleven-component product registry merely for supporting
+  integration infrastructure.
+- No tag, release, package publication, pull request, tester contact, signing,
+  attestation, SBOM, live provider call, GUI operation, or private write.
+- A downstream adapter may be separately owned and may produce its own
+  namespaced result, but it must treat public engine artifacts as immutable
+  inputs and accurately state the limited scope of its own output.
+
+## Non-goals
+
+- designing or implementing a specific private integration;
+- a general plugin marketplace, in-process extension framework, workflow DAG,
+  event bus, RPC service, or network daemon;
+- stabilizing every Python function as a supported API;
+- adding semantic editing decisions to the public engine;
+- changing existing artifact authority or human approval gates;
+- claiming backward compatibility beyond an explicitly selected seam.
+
+## Affected users and systems
+
+- public engine maintainers, who need a narrow compatibility surface;
+- downstream adapter authors, who need a supported consumption boundary;
+- editors, whose source and authoritative artifacts must remain under local
+  custody;
+- packaging and CI, which must prove the seam from a fresh installed wheel;
+- future contract evolution, which needs an explicit compatibility rule.
+
+## Reversible boundary
+
+Task 13 may add or tighten public contracts, metadata, documentation, examples,
+tests, CLI discovery/validation surfaces, and release-gate checks. It must not
+perform a real downstream integration. Any public v1 seam should be small
+enough that an incompatible future design can use a new explicit version
+rather than reinterpret v1.
+
+## Requested independent response
+
+Return all nine sections below. Give concrete tradeoffs and falsifiable
+experiments; do not merely agree with the problem statement or disguise a full
+implementation plan as brainstorming.
+
+1. `problem_reframe`
+2. `pragmatic_path`
+3. `alternative_architecture`
+4. `low_cost_experiment`
+5. `contrarian_challenge`
+6. `unconstrained_possibility`
+7. `overlooked_risks`
+8. `assumptions_to_verify`
+9. `recommended_next_decision`
+
+In `recommended_next_decision`, state exactly what the producer should choose
+between, what you recommend, and what evidence would falsify the choice.
diff --git a/docs/reviews/task-13-brainstorm-synthesis-2026-08-18.md b/docs/reviews/task-13-brainstorm-synthesis-2026-08-18.md
new file mode 100644
index 0000000000000000000000000000000000000000..d3e688a0c08ae0c4b9651c43329ae427b9adbbb6
--- /dev/null
+++ b/docs/reviews/task-13-brainstorm-synthesis-2026-08-18.md
@@ -0,0 +1,175 @@
+# Task 13 multi-AI brainstorm synthesis
+
+Date: 2026-08-18
+
+Frozen packet SHA-256:
+`e0923188a6084e3a48fdd640c8322b947c21dc14da316615e1a2f065656c0798`
+
+Decision owner: producer
+
+No implementation began before this synthesis and producer decision.
+
+## Consensus
+
+- The missing mechanism is a bounded compatibility promise, not a specific
+  downstream adapter.
+- The preferred boundary is out-of-process and artifact-based: installed
+  `tritrack` commands, closed versioned contracts, immutable bundles, exact
+  hashes, and read-only validators.
+- A public wheel-only, out-of-tree consumer with invented data is the most
+  direct falsifiable proof that the engine remains generic authority.
+- Downstream output must be a separately owned, namespaced sidecar bound to
+  exact engine hashes. It must never write into, replace, or masquerade as an
+  engine authority.
+- An in-process plugin loader is premature and reverses the desired trust
+  direction by running downstream code inside the authority process.
+
+## Complementary ideas
+
+- Codex emphasized starting with a no-new-runtime experiment and adding only
+  the smallest missing discovery helper revealed by RED evidence.
+- Gemini proposed an installed CLI schema-discovery surface and a reference
+  sidecar envelope bound to the exact run-manifest hash.
+- Together these form a staged decision: first prove whether the existing CLI
+  and contracts are sufficient; add machine-readable discovery only if the
+  wheel-only consumer otherwise has to duplicate engine rules.
+
+## Provider-unique ideas
+
+### Codex
+
+- Recheck exact bytes after validation to close a time-of-check/time-of-use
+  gap in any reference consumer.
+- Avoid inventing an eleventh authority-like handoff artifact merely to label
+  the ten existing authorities.
+- Report Task 13 package changes honestly instead of extending Task 12's
+  package-neutrality claim beyond its frozen target.
+
+### Gemini
+
+- Consider a read-only `schema`／`inspect schemas` command so non-Python
+  consumers can discover installed contract versions and schemas.
+- Demonstrate tamper rejection by binding a downstream sidecar to the exact
+  `run-manifest.json` hash.
+- Treat stable machine-readable CLI JSON and exit behavior as part of the seam
+  and test it explicitly.
+- The exact wrapper output was 10,497 bytes over 132 lines with SHA-256
+  `e66cb6d32e88fa80f44841c02bd69e2016405d31284914f377be59ca1fbe6e9a`.
+  The tracked public copy removes only three trailing spaces so
+  `git diff --check` remains clean; no response word or structure changed. Its
+  SHA-256 is
+  `8a20230feaacf25e176848f89374fc5060198f5c77b3e3922d28567cafe0523f`.
+
+### Claude
+
+Claude produced no usable answer. Its only subscription-wrapper attempt ended
+`claude-timeout` after preflight. Requested model was the dynamic `opus`
+capability alias; observed and completed models are null; request dispatch is
+ambiguous. The lane remains incomplete with no retry, downgrade, provider
+substitution, API credential, PAYG, Console-credit, or extra-usage fallback.
+
+## Contradictions
+
+There was no disagreement about the architecture family. The open design
+questions are about how much new public surface is justified:
+
+- Codex: make the existing CLI／artifact boundary normative first, then add a
+  discovery command only if a failing experiment proves it necessary.
+- Gemini: include schema discovery in the pragmatic path from the start.
+- Codex: keep the downstream receipt shape outside engine authority.
+- Gemini: a documented or fixture-level reference envelope may help make the
+  sidecar pattern concrete, but it should not be confused with an engine
+  authority.
+
+## Experiments
+
+The shared low-cost experiment is an isolated consumer that receives only an
+installed wheel and invented canonical artifacts. It may invoke public CLI
+commands but may not import repository runtime modules. It must prove:
+
+1. valid exact inputs are accepted;
+2. an unknown schema version is rejected;
+3. a changed byte or noncanonical authority is rejected where the selected
+   authority scope promises that check;
+4. its output binds exact engine input hashes and stays outside the run bundle;
+5. an existing output path is preserved;
+6. source-tree absence does not change behavior; and
+7. validators make no write, network, credential, or private-data access.
+
+If this consumer must duplicate contract discovery, canonicalization, bundle
+semantics, or hash-scope rules, that observed RED justifies the smallest new
+installed discovery surface.
+
+## Risks
+
+- Human CLI output may be parsed accidentally unless the seam names only
+  machine-readable JSON and stable exit classes.
+- Schema validity alone does not prove cross-artifact authority binding; the
+  seam must name the correct validator scope.
+- A separate validate-then-read sequence can race; the consumer must bind and
+  recheck exact bytes or consume a scope whose final summary proves the exact
+  hash it uses.
+- A reference adapter or sidecar shape can become accidentally normative.
+- Transcript-bearing artifacts can widen local custody even when structurally
+  valid; the seam must state custody, not just syntax.
+- Internal imports can create accidental compatibility obligations.
+- A new descriptor or envelope can look like a second authority.
+- New packaged members change Task 13 package facts; Task 12 byte identities
+  remain historical evidence only.
+
+## Options
+
+### Option A — Existing artifact／CLI seam plus black-box proof
+
+Make the existing versioned artifacts, immutable bundles, machine-readable
+CLI summaries, exit classes, and validators the exclusive v1 downstream seam.
+Add an authority／ownership／versioning specification and a wheel-only,
+out-of-tree invented consumer test. The consumer writes a downstream-owned
+sidecar bound to exact engine hashes. Add no runtime surface unless the test
+first demonstrates an actual gap.
+
+Tradeoff: smallest compatibility commitment and strongest proof against
+private coupling, but discovery may initially require documented fixed
+contract names.
+
+### Option B — Machine-readable seam discovery plus black-box proof
+
+Add everything in A plus a new read-only installed command that reports the
+closed supported seam version, contract/schema versions, validator scopes,
+authority roles, and explicit compatibility/non-authority rules.
+
+Tradeoff: clearer feature discovery for non-Python consumers, but the
+descriptor and its JSON output become another stable public contract that must
+be versioned and maintained.
+
+### Option C — Stable Python read-only facade
+
+Add everything needed for proof plus a versioned Python namespace exposing
+only frozen read-only loaders and validators.
+
+Tradeoff: convenient for Python consumers, but creates Python ABI, exception,
+typing, and supported-version obligations and excludes other languages.
+
+An in-process plugin protocol is rejected for Task 13 as disproportionate and
+trust-direction reversing.
+
+## Recommendation
+
+Choose Option A. Treat a new discovery command as a test-driven escalation:
+only add it if the isolated consumer cannot integrate without duplicating
+engine-owned rules. This makes Task 13 a proof of the authority already built,
+not a new framework.
+
+Falsify A if the wheel-only consumer cannot bind and validate the required
+facts using public installed commands without source imports or rule
+duplication, or if measured required invocation frequency makes the process
+boundary materially unsuitable. The first failure upgrades to B; only the
+second supports considering C.
+
+## Provider status
+
+| Lane | Requested | Observed | Completed | Result |
+| --- | --- | --- | --- | --- |
+| Codex | current primary model | `gpt-5.6-sol` | `gpt-5.6-sol` | completed independently before external outputs |
+| Gemini REST wrapper | `gemini-3.7-flash` | `gemini-3.7-flash` | `gemini-3.7-flash` | completed; input 1,283, output 2,302, total 3,865 tokens |
+| Claude subscription wrapper | dynamic `opus` alias | null | null | incomplete: `claude-timeout`, dispatch ambiguous |
diff --git a/docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md b/docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
new file mode 100644
index 0000000000000000000000000000000000000000..2a152bd453a549c1c862e4f265a4c8237175ac19
--- /dev/null
+++ b/docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
@@ -0,0 +1,439 @@
+# Task 13 Generic-Authority Seam Implementation Plan
+
+> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
+
+**Goal:** Prove from a fresh installed wheel that an out-of-tree consumer can bind a downstream-owned sidecar to exact public engine authority without imports, mutation, private knowledge, or a new runtime API.
+
+**Architecture:** Keep the supported v1 seam at the existing `tritrack validate ... --json` process and versioned artifact boundary. Add one standard-library-only example consumer and invented aligned-transcript fixture, then make unit tests, fixed CI, packaging policy, and the maintainer release gate execute the consumer outside the source tree against an installed wheel. The example sidecar is namespaced `example.*` and is explicitly not an engine contract.
+
+**Tech Stack:** Python 3.12／3.13 standard library, existing `unittest`, existing `tritrack` CLI and JSON contracts, setuptools sdist policy, GitHub Actions, existing release-gate framework.
+
+---
+
+### Task 1: Freeze the selected public seam contract
+
+**Files:**
+- Create: `docs/TASK-13-DECISION.md`
+- Create: `docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md`
+
+- [ ] **Step 1: Record the producer decision**
+
+Write the exact Option A authority ownership, process boundary, validation-scope limits, sidecar ownership, privacy boundary, falsification rule, rejected alternatives, non-claims, and brainstorming provenance in `docs/TASK-13-DECISION.md`.
+
+- [ ] **Step 2: Verify the plan and decision are public-safe**
+
+Run:
+
+```bash
+git diff --check
+rg -n '/''Users/|TriTrack-''Subtitle-Studio' docs/TASK-13-DECISION.md docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
+```
+
+Expected: `git diff --check` exits 0 and the privacy search returns no match.
+
+- [ ] **Step 3: Commit the approved design**
+
+```bash
+git add docs/TASK-13-DECISION.md docs/superpowers/plans/2026-08-18-task-13-generic-authority-seam.md
+git commit -m "docs: approve Task 13 downstream seam"
+```
+
+### Task 2: Prove a consumer can use the existing seam
+
+**Files:**
+- Create: `examples/downstream_seam.py`
+- Create: `examples/downstream_fixture/aligned-transcript.json`
+- Create: `tests/test_downstream_seam.py`
+- Create: `docs/TASK-13-VERIFICATION.md`
+
+- [ ] **Step 1: Add the invented authority fixture**
+
+Create canonical JSON with this complete shape:
+
+```json
+{
+  "alignmentProfileId": "cue-addressed-v1",
+  "language": "en",
+  "revisionSha256": "2222222222222222222222222222222222222222222222222222222222222222",
+  "schemaVersion": "tritrack.aligned-transcript/v1",
+  "sourceBundleSha256": "1111111111111111111111111111111111111111111111111111111111111111",
+  "takes": [
+    {
+      "cues": [
+        {
+          "cueId": "cue-000001",
+          "disposition": "original",
+          "endMs": 1250,
+          "startMs": 0,
+          "text": "Invented public words."
+        }
+      ],
+      "sourceSha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
+      "status": "completed",
+      "takeId": "invented-take.wav"
+    }
+  ]
+}
+```
+
+- [ ] **Step 2: Write failing black-box tests**
+
+Create `tests/test_downstream_seam.py` with a real installed CLI path and subprocess assertions:
+
+```python
+ROOT = Path(__file__).resolve().parents[1]
+SCRIPT = ROOT / "examples" / "downstream_seam.py"
+FIXTURE = ROOT / "examples" / "downstream_fixture" / "aligned-transcript.json"
+TRITRACK = Path(sys.executable).with_name("tritrack")
+
+def run_consumer(*arguments: object) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [
+            sys.executable,
+            "-I",
+            os.fspath(SCRIPT),
+            "--tritrack",
+            os.fspath(TRITRACK),
+            *[os.fspath(value) for value in arguments],
+        ],
+        cwd=SCRIPT.parent,
+        check=False,
+        capture_output=True,
+        text=True,
+        timeout=30,
+    )
+```
+
+Tests must assert that a valid fixture creates the exact `example.tritrack-downstream-receipt/v1` sidecar; the stdout summary contains hashes/counts but no path or transcript text; an existing output is preserved; an unknown contract version is rejected; a validator-reported hash mismatch is rejected; and the script contains no `tritrack_editing_assistant` import.
+
+- [ ] **Step 3: Run RED and preserve the expected failure**
+
+Run:
+
+```bash
+venv/bin/python -m unittest tests.test_downstream_seam -v
+```
+
+Expected: FAIL because `examples/downstream_seam.py` does not exist. Record the command, failure reason, and failing test count in the Task 13 verification draft before implementation.
+
+- [ ] **Step 4: Implement the minimal standard-library consumer**
+
+Implement these production-neutral functions in `examples/downstream_seam.py`:
+
+```python
+MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
+
+def _read_regular(path: Path) -> bytes:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    descriptor = os.open(path, flags)
+    try:
+        metadata = os.fstat(descriptor)
+        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= MAX_ARTIFACT_BYTES:
+            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(MAX_ARTIFACT_BYTES + 1)
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+    if len(encoded) > MAX_ARTIFACT_BYTES:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+    return encoded
+
+def _validate(tritrack: Path, aligned: Path) -> dict[str, object]:
+    result = subprocess.run(
+        [os.fspath(tritrack), "validate", "contract", "--artifact", os.fspath(aligned), "--json"],
+        check=False,
+        capture_output=True,
+        timeout=30,
+    )
+    if result.returncode != 0 or result.stderr:
+        raise DownstreamError("DOWNSTREAM_ENGINE_VALIDATION_FAILED")
+    summary = json.loads(result.stdout.decode("utf-8", errors="strict"))
+    if (
+        summary.get("schemaVersion") != "tritrack.validate-summary/v1"
+        or summary.get("artifactKind") != "contract"
+        or summary.get("validationScope") != "contract"
+        or summary.get("details") != {
+            "contractName": "aligned-transcript-v1",
+            "contractSchemaVersion": "tritrack.aligned-transcript/v1",
+        }
+    ):
+        raise DownstreamError("DOWNSTREAM_ENGINE_SCOPE_INVALID")
+    return summary
+```
+
+The main path validates, reads and hashes the exact fixture, checks the reported hash, derives only take/cue counts, validates again and requires identical summary facts, then atomically creates canonical JSON at an absent output. It prints only:
+
+```json
+{
+  "artifactSha256": "<exact hash>",
+  "cueCount": 1,
+  "schemaVersion": "example.tritrack-downstream-summary/v1",
+  "takeCount": 1
+}
+```
+
+- [ ] **Step 5: Run GREEN**
+
+```bash
+venv/bin/python -m unittest tests.test_downstream_seam -v
+```
+
+Expected: all downstream seam tests pass with no warnings or traceback.
+
+- [ ] **Step 6: Commit the working reference consumer**
+
+```bash
+git add examples/downstream_seam.py examples/downstream_fixture/aligned-transcript.json tests/test_downstream_seam.py
+git commit -m "test: prove the public downstream seam"
+```
+
+### Task 3: Make the fresh-wheel gate own the proof
+
+**Files:**
+- Modify: `scripts/release_gate_core.py`
+- Modify: `tests/test_release_gate.py`
+- Modify: `release/release-manifest-v1.schema.json`
+- Modify: `tests/test_packaging.py`
+
+- [ ] **Step 1: Write failing release-gate tests**
+
+Extend `test_fresh_install_uses_only_local_wheel_and_smokes_all_help` with a minimal public source tree containing the example script and fixture. Require `fresh_install_smoke(wheel, smoke, source)` to copy the two files out of the source tree, invoke isolated installed Python with the installed `tritrack`, and verify the created receipt. Extend the manifest sample and schema assertions to require:
+
+```json
+"gates": {
+  "downstreamSeam": "pass",
+  "freshInstall": "pass",
+  "sdistArchive": "pass",
+  "sourceIdentity": "pass",
+  "sourcePrivacy": "pass",
+  "wheelArchive": "pass"
+}
+```
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_release_gate tests.test_packaging -v
+```
+
+Expected: FAIL because `fresh_install_smoke` has no source argument or downstream probe and the release manifest does not allow `downstreamSeam`.
+
+- [ ] **Step 3: Implement the minimal gate integration**
+
+Change the function signature and call site:
+
+```python
+def fresh_install_smoke(wheel: Path, temporary: Path, source: Path) -> None:
+    ...
+
+fresh_install_smoke(wheel_one, staging / "fresh-install", snapshot_one)
+```
+
+After installed CLI help smoke, copy `examples/downstream_seam.py` and
+`examples/downstream_fixture/aligned-transcript.json` into
+`temporary/downstream-seam/`, run the copied consumer under installed
+`python -I` against installed `tritrack`, and read back the exact receipt. Fail
+with `TRITRACK_RELEASE_DOWNSTREAM_SEAM` unless its schema, contract, scope,
+artifact hash, take count, and cue count match the invented fixture.
+
+Add `downstreamSeam: pass` to `build_release_manifest` and its closed schema.
+
+- [ ] **Step 4: Run GREEN**
+
+```bash
+venv/bin/python -m unittest tests.test_release_gate tests.test_packaging tests.test_downstream_seam -v
+```
+
+Expected: all focused release and seam tests pass.
+
+- [ ] **Step 5: Commit the named release gate**
+
+```bash
+git add scripts/release_gate_core.py tests/test_release_gate.py release/release-manifest-v1.schema.json tests/test_packaging.py
+git commit -m "feat: gate the wheel-only downstream seam"
+```
+
+### Task 4: Distribute and exercise only the public proof
+
+**Files:**
+- Modify: `MANIFEST.in`
+- Modify: `release/package-policy-v1.json`
+- Modify: `.github/workflows/ci.yml`
+- Modify: `tests/test_release_ci.py`
+
+- [ ] **Step 1: Write failing packaging and CI policy tests**
+
+Require the sdist policy to contain the Task 13 decision, example consumer,
+invented aligned fixture, Task 13 verification, and downstream seam test while
+the wheel member set remains unchanged. Require the fixed CI wheel-smoke block
+to copy the example and fixture into `$RUNNER_TEMP` and run the consumer with
+the fresh wheel's Python and CLI.
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_packaging tests.test_release_ci -v
+```
+
+Expected: FAIL because the new public proof members and CI invocation are not
+yet declared.
+
+- [ ] **Step 3: Add exact distribution and CI wiring**
+
+Add to `MANIFEST.in`:
+
+```text
+include docs/TASK-13-DECISION.md
+include docs/TASK-13-VERIFICATION.md
+recursive-include examples *.py *.json
+```
+
+Add the exact new members to `release/package-policy-v1.json`. Extend the
+existing CI wheel-smoke shell block with one absent `$RUNNER_TEMP` directory,
+copy the consumer and fixture there, and invoke:
+
+```bash
+"$smoke_python" -I "$seam_dir/downstream_seam.py" \
+  --tritrack "$smoke_cli" \
+  --aligned "$seam_dir/aligned-transcript.json" \
+  --output "$seam_dir/downstream-receipt.json"
+```
+
+- [ ] **Step 4: Run GREEN**
+
+```bash
+venv/bin/python -m unittest tests.test_packaging tests.test_release_ci tests.test_downstream_seam -v
+```
+
+Expected: all packaging, CI, and seam tests pass and the eleven-component
+registry assertion remains unchanged.
+
+- [ ] **Step 5: Commit packaging and CI proof**
+
+```bash
+git add MANIFEST.in release/package-policy-v1.json .github/workflows/ci.yml tests/test_release_ci.py
+git commit -m "build: exercise the downstream seam in fresh wheels"
+```
+
+### Task 5: Close public documentation and local verification
+
+**Files:**
+- Modify: `README.md`
+- Modify: `docs/ROADMAP.md`
+- Modify: `docs/TOOLING.md`
+- Modify: `STATUS.md`
+- Modify: `docs/TASK-13-VERIFICATION.md`
+- Modify: `tests/test_maintainer_boundary.py`
+
+- [ ] **Step 1: Write the failing governance regression**
+
+Require Task 13 completion language, the exact Option A seam, internal-Python
+non-contract language, sidecar non-authority, wheel-only proof, named
+`downstreamSeam` gate, and explicit non-claims across the decision,
+verification, README, roadmap, tooling, and status.
+
+- [ ] **Step 2: Run RED**
+
+```bash
+venv/bin/python -m unittest tests.test_maintainer_boundary -v
+```
+
+Expected: FAIL because Task 13 has not yet been recorded complete and the
+verification file does not exist.
+
+- [ ] **Step 3: Write public documentation after coherent code is green**
+
+Document exact seam commands and limits, invented proof, RED／GREEN evidence,
+package facts, external review provenance, non-claims, and current Task 13
+candidate. Do not claim a private integration, release, tag, package upload,
+or compatibility outside the exact tested boundary.
+
+- [ ] **Step 4: Run complete local validation**
+
+```bash
+venv/bin/python -m unittest discover -s tests -v
+venv/bin/ruff check src tests examples scripts
+venv/bin/python -m compileall -q src tests examples scripts
+venv/bin/python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .
+git diff --check
+```
+
+Expected: full suite, lint, compilation, identity, and diff checks pass.
+
+- [ ] **Step 5: Commit the green implementation target**
+
+```bash
+git add README.md docs/ROADMAP.md docs/TOOLING.md STATUS.md docs/TASK-13-VERIFICATION.md tests/test_maintainer_boundary.py
+git commit -m "docs: complete Task 13 public authority proof"
+```
+
+### Task 6: Review, fix forward, integrate, and verify exact CI
+
+**Files:**
+- Create: `docs/reviews/task-13-closeout-packet-2026-08-18.md`
+- Create: `docs/reviews/task-13-closeout-codex-2026-08-18.md`
+- Create: `docs/reviews/task-13-closeout-gemini-2026-08-18.md`
+- Create: `docs/reviews/task-13-closeout-gemini-2026-08-18.md.status.json`
+- Create on completed Claude lane or status-only on failure: `docs/reviews/task-13-closeout-claude-2026-08-18.md*`
+- Create: `docs/reviews/task-13-closeout-adjudication-2026-08-18.md`
+- Modify if required by reproduced findings: only Task 13-owned source, tests, and docs
+
+- [ ] **Step 1: Run the clean maintainer release gate**
+
+Commit the implementation, require a clean worktree, create one absent output
+directory, and run:
+
+```bash
+venv/bin/python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
+```
+
+Expected: both package builds match their declared reproducibility contract,
+fresh wheel installation passes, the copied out-of-tree consumer passes, and
+the manifest records `downstreamSeam: pass`.
+
+- [ ] **Step 2: Freeze one same-byte closeout packet**
+
+Include exact candidate SHA, complete Task 13 diff, every changed runtime／gate
+file, focused and full results, release manifest, non-goals, and requested
+file-and-line finding format. Hash and scan the packet before dispatch.
+
+- [ ] **Step 3: Complete independent Codex review before external results**
+
+Read the frozen packet and source, record only reproducible findings, and save
+the independent response before reading Claude or Gemini output.
+
+- [ ] **Step 4: Dispatch the same bytes once per external lane**
+
+```bash
+review-with-claude PACKET CLAUDE_OUTPUT REPO
+review-with-gemini PACKET GEMINI_OUTPUT -
+```
+
+Expected: each lane records requested／observed／completed model provenance.
+Timeout, quota, or unavailable lanes remain incomplete with no retry, downgrade,
+provider substitution, or paid fallback.
+
+- [ ] **Step 5: Adjudicate and fix forward with TDD**
+
+Classify every finding as `agree`, `upgrade`, `downgrade`, `reject`, or
+`already-fixed`. For each accepted behavior defect, add a failing regression,
+observe RED, make the minimal fix, and rerun focused plus complete verification.
+
+- [ ] **Step 6: Final clean gate and evidence commit**
+
+Rerun full tests, Ruff, compilation, identity, both skill validators,
+maintainer boundary, package policy, public-content scan, `git diff --check`,
+and the clean release gate. Commit review and final verification records only
+after the candidate is green.
+
+- [ ] **Step 7: Fast-forward, push, and verify exact SHA**
+
+Fast-forward local `main` to the reviewed Task 13 candidate, push the existing
+public `origin/main`, and require local `HEAD`, local `main`, `origin/main`, and
+remote `refs/heads/main` to match exactly. Then watch the fixed six-job GitHub
+Actions run for that exact SHA and report its run ID and conclusion without
+writing the run ID back into a self-referential commit.
diff --git a/examples/downstream_fixture/aligned-transcript.json b/examples/downstream_fixture/aligned-transcript.json
new file mode 100644
index 0000000000000000000000000000000000000000..be876c51ca8d3eb822ac4f399880ca37b443f663
--- /dev/null
+++ b/examples/downstream_fixture/aligned-transcript.json
@@ -0,0 +1,23 @@
+{
+  "alignmentProfileId": "cue-addressed-v1",
+  "language": "en",
+  "revisionSha256": "2222222222222222222222222222222222222222222222222222222222222222",
+  "schemaVersion": "tritrack.aligned-transcript/v1",
+  "sourceBundleSha256": "1111111111111111111111111111111111111111111111111111111111111111",
+  "takes": [
+    {
+      "cues": [
+        {
+          "cueId": "cue-000001",
+          "disposition": "original",
+          "endMs": 1250,
+          "startMs": 0,
+          "text": "Invented public words."
+        }
+      ],
+      "sourceSha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
+      "status": "completed",
+      "takeId": "invented-take.wav"
+    }
+  ]
+}
diff --git a/examples/downstream_seam.py b/examples/downstream_seam.py
new file mode 100644
index 0000000000000000000000000000000000000000..a11e185757d2f5d7cecfdc12c5d13b29c793cf47
--- /dev/null
+++ b/examples/downstream_seam.py
@@ -0,0 +1,224 @@
+"""Black-box example of TriTrack's supported downstream process seam."""
+
+from __future__ import annotations
+
+import argparse
+import hashlib
+import json
+import os
+import stat
+import subprocess
+import sys
+import tempfile
+from collections.abc import Mapping
+from pathlib import Path
+from typing import NoReturn
+
+MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
+VALIDATE_SUMMARY_SCHEMA = "tritrack.validate-summary/v1"
+ALIGNED_CONTRACT = "aligned-transcript-v1"
+ALIGNED_SCHEMA = "tritrack.aligned-transcript/v1"
+
+
+class DownstreamError(ValueError):
+    """A stable, path-free error suitable for example automation."""
+
+
+def _canonical_json(payload: Mapping[str, object]) -> bytes:
+    return (
+        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
+    ).encode("utf-8")
+
+
+def _read_regular(path: Path) -> bytes:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    if hasattr(os, "O_NOFOLLOW"):
+        flags |= os.O_NOFOLLOW
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
+    try:
+        metadata = os.fstat(descriptor)
+        if (
+            not stat.S_ISREG(metadata.st_mode)
+            or not 0 < metadata.st_size <= MAX_ARTIFACT_BYTES
+        ):
+            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            encoded = stream.read(MAX_ARTIFACT_BYTES + 1)
+    except OSError as error:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
+    if len(encoded) > MAX_ARTIFACT_BYTES:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+    return encoded
+
+
+def _validate(tritrack: Path, aligned: Path) -> dict[str, object]:
+    try:
+        result = subprocess.run(
+            [
+                os.fspath(tritrack),
+                "validate",
+                "contract",
+                "--artifact",
+                os.fspath(aligned),
+                "--json",
+            ],
+            check=False,
+            capture_output=True,
+            timeout=30,
+        )
+    except (OSError, subprocess.TimeoutExpired) as error:
+        raise DownstreamError(
+            "DOWNSTREAM_ENGINE_VALIDATION_FAILED"
+        ) from error
+    if result.returncode != 0 or result.stderr:
+        raise DownstreamError("DOWNSTREAM_ENGINE_VALIDATION_FAILED")
+    try:
+        decoded = result.stdout.decode("utf-8", errors="strict")
+        summary = json.loads(decoded)
+    except (UnicodeDecodeError, json.JSONDecodeError) as error:
+        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID") from error
+    if not isinstance(summary, dict):
+        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
+    if (
+        summary.get("schemaVersion") != VALIDATE_SUMMARY_SCHEMA
+        or summary.get("artifactKind") != "contract"
+        or summary.get("validationScope") != "contract"
+        or summary.get("details")
+        != {
+            "contractName": ALIGNED_CONTRACT,
+            "contractSchemaVersion": ALIGNED_SCHEMA,
+        }
+    ):
+        raise DownstreamError("DOWNSTREAM_ENGINE_SCOPE_INVALID")
+    hashes = summary.get("hashes")
+    if not isinstance(hashes, dict):
+        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
+    artifact_hash = hashes.get("artifact")
+    if (
+        not isinstance(artifact_hash, str)
+        or len(artifact_hash) != 64
+        or any(character not in "0123456789abcdef" for character in artifact_hash)
+    ):
+        raise DownstreamError("DOWNSTREAM_ENGINE_SUMMARY_INVALID")
+    return summary
+
+
+def _observe(encoded: bytes) -> tuple[int, int]:
+    try:
+        artifact = json.loads(encoded.decode("utf-8", errors="strict"))
+    except (UnicodeDecodeError, json.JSONDecodeError) as error:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID") from error
+    if not isinstance(artifact, dict) or artifact.get("schemaVersion") != ALIGNED_SCHEMA:
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+    takes = artifact.get("takes")
+    if not isinstance(takes, list):
+        raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+    cue_count = 0
+    for take in takes:
+        if not isinstance(take, dict) or not isinstance(take.get("cues"), list):
+            raise DownstreamError("DOWNSTREAM_INPUT_INVALID")
+        cue_count += len(take["cues"])
+    return len(takes), cue_count
+
+
+def _publish_absent(path: Path, payload: Mapping[str, object]) -> None:
+    parent = path.parent
+    temporary_path: Path | None = None
+    try:
+        descriptor, temporary_name = tempfile.mkstemp(
+            dir=parent,
+            prefix=f".{path.name}.",
+        )
+        temporary_path = Path(temporary_name)
+        with os.fdopen(descriptor, "wb") as stream:
+            stream.write(_canonical_json(payload))
+            stream.flush()
+            os.fsync(stream.fileno())
+        os.link(temporary_path, path, follow_symlinks=False)
+    except FileExistsError as error:
+        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS") from error
+    except OSError as error:
+        raise DownstreamError("DOWNSTREAM_OUTPUT_INVALID") from error
+    finally:
+        if temporary_path is not None:
+            try:
+                temporary_path.unlink()
+            except FileNotFoundError:
+                pass
+
+
+def _artifact_hash(summary: Mapping[str, object]) -> str:
+    hashes = summary["hashes"]
+    assert isinstance(hashes, dict)
+    artifact_hash = hashes["artifact"]
+    assert isinstance(artifact_hash, str)
+    return artifact_hash
+
+
+def _run(tritrack: Path, aligned: Path, output: Path) -> dict[str, object]:
+    if os.path.lexists(output):
+        raise DownstreamError("DOWNSTREAM_OUTPUT_EXISTS")
+
+    first_summary = _validate(tritrack, aligned)
+    encoded = _read_regular(aligned)
+    artifact_sha256 = hashlib.sha256(encoded).hexdigest()
+    if _artifact_hash(first_summary) != artifact_sha256:
+        raise DownstreamError("DOWNSTREAM_ENGINE_HASH_MISMATCH")
+
+    take_count, cue_count = _observe(encoded)
+    second_summary = _validate(tritrack, aligned)
+    if second_summary != first_summary:
+        raise DownstreamError("DOWNSTREAM_ENGINE_CHANGED")
+
+    receipt: dict[str, object] = {
+        "schemaVersion": "example.tritrack-downstream-receipt/v1",
+        "engineAuthority": {
+            "artifactSha256": artifact_sha256,
+            "contractName": ALIGNED_CONTRACT,
+            "contractSchemaVersion": ALIGNED_SCHEMA,
+            "validationScope": "contract",
+        },
+        "derivedObservation": {
+            "takeCount": take_count,
+            "cueCount": cue_count,
+        },
+    }
+    _publish_absent(output, receipt)
+    return {
+        "schemaVersion": "example.tritrack-downstream-summary/v1",
+        "artifactSha256": artifact_sha256,
+        "takeCount": take_count,
+        "cueCount": cue_count,
+    }
+
+
+def _fail(error: DownstreamError) -> NoReturn:
+    sys.stderr.buffer.write(_canonical_json({"error": str(error)}))
+    raise SystemExit(2)
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(
+        description="Prove the public TriTrack CLI/artifact downstream seam."
+    )
+    parser.add_argument("--tritrack", required=True, type=Path)
+    parser.add_argument("--aligned", required=True, type=Path)
+    parser.add_argument("--output", required=True, type=Path)
+    arguments = parser.parse_args()
+    try:
+        summary = _run(arguments.tritrack, arguments.aligned, arguments.output)
+    except DownstreamError as error:
+        _fail(error)
+    sys.stdout.buffer.write(_canonical_json(summary))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/release/package-policy-v1.json b/release/package-policy-v1.json
index bba414acf839d7a75a858b46d8e4410fb009c589..fb9cdb0c1235b33f3274028ef0367331aaeb43f7 100644
--- a/release/package-policy-v1.json
+++ b/release/package-policy-v1.json
@@ -100,8 +100,12 @@
|      "SECURITY.md",
|      "docs/ROADMAP.md",
|      "docs/TASK-11-VERIFICATION.md",
+      "docs/TASK-13-DECISION.md",
+      "docs/TASK-13-VERIFICATION.md",
|      "docs/TOOLING.md",
|      "docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md",
+      "examples/downstream_fixture/aligned-transcript.json",
+      "examples/downstream_seam.py",
|      "examples/quickstart_demo.py",
|      "pyproject.toml",
|      "release/package-policy-v1.json",
@@ -155,6 +159,7 @@
|      "tests/test_cli.py",
|      "tests/test_contracts.py",
|      "tests/test_doctor.py",
+      "tests/test_downstream_seam.py",
|      "tests/test_emit_fcpxml.py",
|      "tests/test_gemini_hybrid.py",
|      "tests/test_hallucination.py",
diff --git a/release/release-manifest-v1.schema.json b/release/release-manifest-v1.schema.json
index 53c8c8da8fe3dd240d8e80caae956fbe08aba902..648292316e0219b46b9bc58d40b53d07d7015dc1 100644
--- a/release/release-manifest-v1.schema.json
+++ b/release/release-manifest-v1.schema.json
@@ -93,14 +93,16 @@
|        "sourcePrivacy",
|        "wheelArchive",
|        "sdistArchive",
-        "freshInstall"
+        "freshInstall",
+        "downstreamSeam"
|      ],
|      "properties": {
|        "sourceIdentity": {"const": "pass"},
|        "sourcePrivacy": {"const": "pass"},
|        "wheelArchive": {"const": "pass"},
|        "sdistArchive": {"const": "pass"},
-        "freshInstall": {"const": "pass"}
+        "freshInstall": {"const": "pass"},
+        "downstreamSeam": {"const": "pass"}
|      }
|    },
|    "nonClaims": {
diff --git a/scripts/release_gate_core.py b/scripts/release_gate_core.py
index 6236c4235e77fdaf5671c7931ae6f248e0b03a9a..db44948e62edde792d519904c25c56c401b1f43f 100644
--- a/scripts/release_gate_core.py
+++ b/scripts/release_gate_core.py
@@ -962,7 +962,7 @@ def _install_environment(temporary: Path, binary: Path) -> dict[str, str]:
|    return environment
|
|
-def fresh_install_smoke(wheel: Path, temporary: Path) -> None:
+def fresh_install_smoke(wheel: Path, temporary: Path, source: Path) -> None:
|    """Install only the chosen local wheel into a new external environment."""
|
|    project_name, project_version = _wheel_project_identity(wheel)
@@ -1056,6 +1056,74 @@ def fresh_install_smoke(wheel: Path, temporary: Path) -> None:
|            timeout=60,
|        )
|
+    seam = temporary / "downstream-seam"
+    try:
+        os.mkdir(seam)
+        script_bytes = _read_regular(
+            source / "examples" / "downstream_seam.py", _POLICY_LIMIT
+        )
+        fixture_bytes = _read_regular(
+            source
+            / "examples"
+            / "downstream_fixture"
+            / "aligned-transcript.json",
+            _POLICY_LIMIT,
+        )
+        _write_snapshot_file(seam, "downstream_seam.py", 0o644, script_bytes)
+        _write_snapshot_file(
+            seam, "aligned-transcript.json", 0o644, fixture_bytes
+        )
+    except ReleaseGateError:
+        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
+    except OSError:
+        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
+
+    copied_script = seam / "downstream_seam.py"
+    copied_fixture = seam / "aligned-transcript.json"
+    receipt = seam / "downstream-receipt.json"
+    try:
+        _run_command(
+            [
+                os.fspath(python),
+                "-I",
+                os.fspath(copied_script),
+                "--tritrack",
+                os.fspath(tritrack),
+                "--aligned",
+                os.fspath(copied_fixture),
+                "--output",
+                os.fspath(receipt),
+            ],
+            cwd=seam,
+            env=environment,
+            timeout=60,
+        )
+        observed = json.loads(
+            _read_regular(receipt, _POLICY_LIMIT).decode(
+                "utf-8", errors="strict"
+            )
+        )
+    except (
+        ReleaseGateError,
+        UnicodeDecodeError,
+        json.JSONDecodeError,
+        OSError,
+    ):
+        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
+    artifact_sha256 = hashlib.sha256(fixture_bytes).hexdigest()
+    expected = {
+        "schemaVersion": "example.tritrack-downstream-receipt/v1",
+        "engineAuthority": {
+            "artifactSha256": artifact_sha256,
+            "contractName": "aligned-transcript-v1",
+            "contractSchemaVersion": "tritrack.aligned-transcript/v1",
+            "validationScope": "contract",
+        },
+        "derivedObservation": {"takeCount": 1, "cueCount": 1},
+    }
+    if observed != expected:
+        _fail("TRITRACK_RELEASE_DOWNSTREAM_SEAM")
+
|
|def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
|    """Build and validate the deterministic, closed public release receipt."""
@@ -1104,6 +1172,7 @@ def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
|            "wheelArchive": "pass",
|            "sdistArchive": "pass",
|            "freshInstall": "pass",
+            "downstreamSeam": "pass",
|        },
|        "nonClaims": [
|            "no-tag",
@@ -1510,7 +1579,9 @@ def run_release_gate(source: Path, output: Path) -> dict[str, object]:
|            != second_sdist_inspection.member_inventory_sha256
|        ):
|            _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
-        fresh_install_smoke(wheel_one, staging / "fresh-install")
+        fresh_install_smoke(
+            wheel_one, staging / "fresh-install", snapshot_one
+        )
|        context = ReleaseContext(
|            project_name=project_name,
|            version=version,
diff --git a/tests/test_downstream_seam.py b/tests/test_downstream_seam.py
new file mode 100644
index 0000000000000000000000000000000000000000..e158155bef3c5b2cf9a714c31d57d12c4dc0b8cf
--- /dev/null
+++ b/tests/test_downstream_seam.py
@@ -0,0 +1,218 @@
+"""Task 13 black-box downstream integration seam proof."""
+
+from __future__ import annotations
+
+import hashlib
+import json
+import os
+import subprocess
+import sys
+import tempfile
+import unittest
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[1]
+SCRIPT = ROOT / "examples" / "downstream_seam.py"
+FIXTURE = (
+    ROOT / "examples" / "downstream_fixture" / "aligned-transcript.json"
+)
+TRITRACK = Path(sys.executable).with_name("tritrack")
+
+
+def sha256(encoded: bytes) -> str:
+    return hashlib.sha256(encoded).hexdigest()
+
+
+def run_consumer(
+    aligned: Path, output: Path, *, tritrack: Path = TRITRACK
+) -> subprocess.CompletedProcess[str]:
+    return subprocess.run(
+        [
+            sys.executable,
+            "-I",
+            os.fspath(SCRIPT),
+            "--tritrack",
+            os.fspath(tritrack),
+            "--aligned",
+            os.fspath(aligned),
+            "--output",
+            os.fspath(output),
+        ],
+        cwd=SCRIPT.parent,
+        check=False,
+        capture_output=True,
+        text=True,
+        timeout=30,
+    )
+
+
+class DownstreamSeamTest(unittest.TestCase):
+    def test_consumes_exact_engine_authority_without_internal_imports(self) -> None:
+        self.assertTrue(TRITRACK.is_file(), TRITRACK)
+        aligned_bytes = FIXTURE.read_bytes()
+        artifact_sha256 = sha256(aligned_bytes)
+        with tempfile.TemporaryDirectory() as temporary:
+            output = Path(temporary) / "downstream-receipt.json"
+            result = run_consumer(FIXTURE, output)
+
+            self.assertEqual(result.returncode, 0, result.stderr)
+            self.assertEqual(result.stderr, "")
+            self.assertEqual(
+                json.loads(output.read_text(encoding="utf-8")),
+                {
+                    "schemaVersion": "example.tritrack-downstream-receipt/v1",
+                    "engineAuthority": {
+                        "artifactSha256": artifact_sha256,
+                        "contractName": "aligned-transcript-v1",
+                        "contractSchemaVersion": (
+                            "tritrack.aligned-transcript/v1"
+                        ),
+                        "validationScope": "contract",
+                    },
+                    "derivedObservation": {"takeCount": 1, "cueCount": 1},
+                },
+            )
+            self.assertTrue(output.read_bytes().endswith(b"\n"))
+            self.assertEqual(
+                json.loads(result.stdout),
+                {
+                    "schemaVersion": (
+                        "example.tritrack-downstream-summary/v1"
+                    ),
+                    "artifactSha256": artifact_sha256,
+                    "takeCount": 1,
+                    "cueCount": 1,
+                },
+            )
+            self.assertNotIn(os.fspath(ROOT), result.stdout)
+            self.assertNotIn("Invented public words", result.stdout)
+
+        source = SCRIPT.read_text(encoding="utf-8")
+        self.assertNotIn("tritrack_editing_assistant", source)
+
+    def test_preserves_existing_output(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            output = Path(temporary) / "existing.json"
+            output.write_bytes(b"winner")
+
+            result = run_consumer(FIXTURE, output)
+
+            self.assertEqual(result.returncode, 2)
+            self.assertEqual(result.stdout, "")
+            self.assertEqual(
+                json.loads(result.stderr),
+                {"error": "DOWNSTREAM_OUTPUT_EXISTS"},
+            )
+            self.assertEqual(output.read_bytes(), b"winner")
+
+    def test_rejects_unknown_engine_contract_version(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            changed = json.loads(FIXTURE.read_text(encoding="utf-8"))
+            changed["schemaVersion"] = "tritrack.aligned-transcript/v99"
+            aligned = root / "future.json"
+            aligned.write_text(
+                json.dumps(changed, indent=2, sort_keys=True) + "\n",
+                encoding="utf-8",
+            )
+            output = root / "receipt.json"
+
+            result = run_consumer(aligned, output)
+
+            self.assertEqual(result.returncode, 2)
+            self.assertEqual(result.stdout, "")
+            self.assertEqual(
+                json.loads(result.stderr),
+                {"error": "DOWNSTREAM_ENGINE_VALIDATION_FAILED"},
+            )
+            self.assertFalse(output.exists())
+            self.assertNotIn(os.fspath(root), result.stderr)
+
+    def test_rejects_validator_hash_that_does_not_match_consumed_bytes(
+        self,
+    ) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            fake_cli = root / "tritrack"
+            fake_cli.write_text(
+                "#!" + os.fspath(sys.executable) + "\n"
+                "import json\n"
+                "print(json.dumps({\n"
+                "  'schemaVersion': 'tritrack.validate-summary/v1',\n"
+                "  'toolVersion': '0.1.0a0',\n"
+                "  'artifactKind': 'contract',\n"
+                "  'validationScope': 'contract',\n"
+                "  'hashes': {'artifact': '0' * 64},\n"
+                "  'counts': {},\n"
+                "  'details': {\n"
+                "    'contractName': 'aligned-transcript-v1',\n"
+                "    'contractSchemaVersion': "
+                "'tritrack.aligned-transcript/v1',\n"
+                "  },\n"
+                "}, sort_keys=True))\n",
+                encoding="utf-8",
+            )
+            fake_cli.chmod(0o755)
+            output = root / "receipt.json"
+
+            result = run_consumer(FIXTURE, output, tritrack=fake_cli)
+
+            self.assertEqual(result.returncode, 2)
+            self.assertEqual(result.stdout, "")
+            self.assertEqual(
+                json.loads(result.stderr),
+                {"error": "DOWNSTREAM_ENGINE_HASH_MISMATCH"},
+            )
+            self.assertFalse(output.exists())
+
+    def test_rejects_engine_summary_that_changes_before_publication(
+        self,
+    ) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            fake_cli = root / "tritrack"
+            counter = root / "calls"
+            fake_cli.write_text(
+                "#!" + os.fspath(sys.executable) + "\n"
+                "import hashlib\n"
+                "import json\n"
+                "import pathlib\n"
+                "import sys\n"
+                f"counter = pathlib.Path({os.fspath(counter)!r})\n"
+                "calls = int(counter.read_text() or '0') "
+                "if counter.exists() else 0\n"
+                "counter.write_text(str(calls + 1))\n"
+                "artifact = pathlib.Path(sys.argv[sys.argv.index("
+                "'--artifact') + 1])\n"
+                "digest = hashlib.sha256(artifact.read_bytes()).hexdigest()\n"
+                "print(json.dumps({\n"
+                "  'schemaVersion': 'tritrack.validate-summary/v1',\n"
+                "  'toolVersion': '0.1.0a0' if calls == 0 else 'changed',\n"
+                "  'artifactKind': 'contract',\n"
+                "  'validationScope': 'contract',\n"
+                "  'hashes': {'artifact': digest},\n"
+                "  'counts': {},\n"
+                "  'details': {\n"
+                "    'contractName': 'aligned-transcript-v1',\n"
+                "    'contractSchemaVersion': "
+                "'tritrack.aligned-transcript/v1',\n"
+                "  },\n"
+                "}, sort_keys=True))\n",
+                encoding="utf-8",
+            )
+            fake_cli.chmod(0o755)
+            output = root / "receipt.json"
+
+            result = run_consumer(FIXTURE, output, tritrack=fake_cli)
+
+            self.assertEqual(result.returncode, 2)
+            self.assertEqual(result.stdout, "")
+            self.assertEqual(
+                json.loads(result.stderr),
+                {"error": "DOWNSTREAM_ENGINE_CHANGED"},
+            )
+            self.assertFalse(output.exists())
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/test_maintainer_boundary.py b/tests/test_maintainer_boundary.py
index 77feb81e914f20c019f348ad6a983608a1bfd48e..1a83652499149b0fbb7853663fa6486c9dff9327 100644
--- a/tests/test_maintainer_boundary.py
+++ b/tests/test_maintainer_boundary.py
@@ -149,7 +149,7 @@ class MaintainerBoundaryTest(unittest.TestCase):
|        for token in forbidden:
|            self.assertNotIn(token, lowered)
|
-    def test_public_status_records_task_12_and_schedules_task_13(self) -> None:
+    def test_public_status_records_tasks_1_through_13(self) -> None:
|        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
|        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
|        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
@@ -166,7 +166,7 @@ class MaintainerBoundaryTest(unittest.TestCase):
|        task_12_verification = (ROOT / "docs" / "TASK-12-VERIFICATION.md").read_text(
|            encoding="utf-8"
|        )
-        self.assertIn("Tasks 1–12", status)
+        self.assertIn("Tasks 1–13", status)
|        self.assertIn("Task 6.5", status)
|        self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
|        self.assertLess(status.index("Task 7"), status.index("Task 8"))
@@ -211,6 +211,43 @@ class MaintainerBoundaryTest(unittest.TestCase):
|        self.assertNotIn("`validate` remains planned", status)
|        self.assertNotIn("`tritrack run` | planned", readme)
|
+    def test_task_13_documents_generic_authority_and_downstream_seam(
+        self,
+    ) -> None:
+        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
+        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
+        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
+        readme = (ROOT / "README.md").read_text(encoding="utf-8")
+        decision = (ROOT / "docs" / "TASK-13-DECISION.md").read_text(
+            encoding="utf-8"
+        )
+        verification = (ROOT / "docs" / "TASK-13-VERIFICATION.md").read_text(
+            encoding="utf-8"
+        )
+
+        for text in (status, roadmap, tooling, readme, decision, verification):
+            self.assertIn("Task 13", text)
+        self.assertIn("Selected option: A", decision)
+        self.assertIn(
+            "exclusive supported downstream integration seam for v1",
+            decision,
+        )
+        self.assertIn(
+            "Internal Python modules and functions are implementation details",
+            decision,
+        )
+        self.assertIn("never an engine contract", decision)
+        for text in (status, tooling, readme, verification):
+            self.assertIn("downstreamSeam", text)
+            self.assertIn("wheel-only", text)
+        for text in (status, roadmap, readme, verification):
+            normalized = " ".join(text.split())
+            self.assertIn("no tag", normalized)
+            self.assertIn("no package publication", normalized)
+            self.assertIn("no private integration", normalized)
+        self.assertIn("examples/downstream_seam.py", tooling)
+        self.assertIn("tritrack validate contract", tooling)
+
|    def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
|        handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
|            encoding="utf-8"
diff --git a/tests/test_packaging.py b/tests/test_packaging.py
index e3ba32465b04e69456cd0299d82d74b0e5b41b35..8dcffed97d53556d8c2608a945eaea724a762694 100644
--- a/tests/test_packaging.py
+++ b/tests/test_packaging.py
@@ -88,10 +88,22 @@ class PackagingPolicyTest(unittest.TestCase):
|        self.assertEqual(policy["build"], {"sourceDateEpoch": 1704067200})
|        for required in (
|            "docs/TASK-11-VERIFICATION.md",
+            "docs/TASK-13-DECISION.md",
+            "docs/TASK-13-VERIFICATION.md",
+            "examples/downstream_fixture/aligned-transcript.json",
+            "examples/downstream_seam.py",
|            "scripts/release_gate.py",
|            "scripts/release_gate_core.py",
+            "tests/test_downstream_seam.py",
|        ):
|            self.assertIn(required, policy["sdist"]["expectedMembers"])
+        self.assertEqual(len(policy["wheel"]["expectedMembers"]), 38)
+        self.assertFalse(
+            any(
+                "downstream" in member
+                for member in policy["wheel"]["expectedMembers"]
+            )
+        )
|        schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
|        jsonschema.Draft202012Validator.check_schema(schema)
|        sample = {
@@ -132,6 +144,7 @@ class PackagingPolicyTest(unittest.TestCase):
|                    "wheelArchive",
|                    "sdistArchive",
|                    "freshInstall",
+                    "downstreamSeam",
|                )
|            },
|            "nonClaims": ["no-tag", "no-package-publication"],
diff --git a/tests/test_release_ci.py b/tests/test_release_ci.py
index 4f357db8438fdad0294bb1076dea26317893f2fc..3a6b681a51444738ecbb5c7b6fe25d5ec7158e1e 100644
--- a/tests/test_release_ci.py
+++ b/tests/test_release_ci.py
@@ -53,6 +53,13 @@ class ReleaseCiContractTest(unittest.TestCase):
|            "validate fcpxml --help",
|            "validate paper --help",
|            "validate run --help",
+            'downstream_dir="$RUNNER_TEMP/tritrack-downstream-seam"',
+            'cp examples/downstream_seam.py "$downstream_dir/downstream_seam.py"',
+            'cp examples/downstream_fixture/aligned-transcript.json "$downstream_dir/aligned-transcript.json"',
+            '"$smoke_python" -I "$downstream_dir/downstream_seam.py"',
+            '--tritrack "$smoke_cli"',
+            '--aligned "$downstream_dir/aligned-transcript.json"',
+            '--output "$downstream_dir/downstream-receipt.json"',
|        )
|        for command in required:
|            self.assertIn(command, self.workflow)
diff --git a/tests/test_release_gate.py b/tests/test_release_gate.py
index 5c6bf3b5840355df441e47b840647146306de070..5fce883c1d77330b586c5fa104bffe9ea2087559 100644
--- a/tests/test_release_gate.py
+++ b/tests/test_release_gate.py
@@ -503,6 +503,22 @@ class OrchestrationTest(unittest.TestCase):
|            root = Path(temporary)
|            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
|            wheel.write_bytes(b"invented wheel")
+            source = root / "source"
+            fixture = source / "examples" / "downstream_fixture" / "aligned-transcript.json"
+            fixture.parent.mkdir(parents=True)
+            fixture.write_text(
+                json.dumps(
+                    {
+                        "schemaVersion": "tritrack.aligned-transcript/v1",
+                        "takes": [{"cues": [{}]}],
+                    },
+                    sort_keys=True,
+                )
+                + "\n",
+                encoding="utf-8",
+            )
+            script = source / "examples" / "downstream_seam.py"
+            script.write_text("# invented public consumer\n", encoding="utf-8")
|
|            def fake_command(argv, **_kwargs):
|                normalized = tuple(str(value) for value in argv)
@@ -516,6 +532,44 @@ class OrchestrationTest(unittest.TestCase):
|                    ).encode()
|                if "importlib.metadata" in " ".join(normalized):
|                    return b"tritrack-editing-assistant\t0.1.0a0\n"
+                if len(normalized) > 2 and normalized[1] == "-I":
+                    copied_script = Path(normalized[2])
+                    copied_fixture = Path(
+                        normalized[normalized.index("--aligned") + 1]
+                    )
+                    output = Path(normalized[normalized.index("--output") + 1])
+                    self.assertNotIn(source, copied_script.parents)
+                    self.assertNotIn(source, copied_fixture.parents)
+                    self.assertEqual(copied_script.read_bytes(), script.read_bytes())
+                    self.assertEqual(copied_fixture.read_bytes(), fixture.read_bytes())
+                    artifact_sha256 = hashlib.sha256(
+                        copied_fixture.read_bytes()
+                    ).hexdigest()
+                    output.write_text(
+                        json.dumps(
+                            {
+                                "schemaVersion": (
+                                    "example.tritrack-downstream-receipt/v1"
+                                ),
+                                "engineAuthority": {
+                                    "artifactSha256": artifact_sha256,
+                                    "contractName": "aligned-transcript-v1",
+                                    "contractSchemaVersion": (
+                                        "tritrack.aligned-transcript/v1"
+                                    ),
+                                    "validationScope": "contract",
+                                },
+                                "derivedObservation": {
+                                    "takeCount": 1,
+                                    "cueCount": 1,
+                                },
+                            },
+                            sort_keys=True,
+                        )
+                        + "\n",
+                        encoding="utf-8",
+                    )
+                    return b'{"schemaVersion":"example.tritrack-downstream-summary/v1"}\n'
|                return b""
|
|            with (
@@ -528,7 +582,9 @@ class OrchestrationTest(unittest.TestCase):
|                    release_gate_core, "_run_command", side_effect=fake_command
|                ),
|            ):
-                release_gate_core.fresh_install_smoke(wheel, root / "smoke")
+                release_gate_core.fresh_install_smoke(
+                    wheel, root / "smoke", source
+                )
|
|        flattened = [" ".join(call) for call in calls]
|        install = [
@@ -543,6 +599,65 @@ class OrchestrationTest(unittest.TestCase):
|            self.assertTrue(
|                any(f"validate {mode} --help" in call for call in flattened), mode
|            )
+        self.assertTrue(
+            any("-I" in call and "downstream_seam.py" in call for call in flattened)
+        )
+
+    def test_fresh_install_rejects_an_invalid_downstream_receipt(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
+            wheel.write_bytes(b"invented wheel")
+            source = root / "source"
+            fixture = source / "examples" / "downstream_fixture" / "aligned-transcript.json"
+            fixture.parent.mkdir(parents=True)
+            fixture.write_text(
+                '{"schemaVersion":"tritrack.aligned-transcript/v1","takes":[{"cues":[{}]}]}\n',
+                encoding="utf-8",
+            )
+            (source / "examples" / "downstream_seam.py").write_text(
+                "# invented public consumer\n", encoding="utf-8"
+            )
+
+            def fake_command(argv, **_kwargs):
+                normalized = tuple(str(value) for value in argv)
+                if normalized[-2:] == ("components", "--json"):
+                    return json.dumps(
+                        {
+                            "schemaVersion": "tritrack.components/v1",
+                            "components": [{}] * 11,
+                        }
+                    ).encode()
+                if "importlib.metadata" in " ".join(normalized):
+                    return b"tritrack-editing-assistant\t0.1.0a0\n"
+                if len(normalized) > 2 and normalized[1] == "-I":
+                    output = Path(normalized[normalized.index("--output") + 1])
+                    output.write_text(
+                        '{"schemaVersion":"invented.invalid/v1"}\n',
+                        encoding="utf-8",
+                    )
+                return b""
+
+            with (
+                mock.patch.object(
+                    release_gate_core,
+                    "_wheel_project_identity",
+                    return_value=(
+                        "tritrack-editing-assistant",
+                        "0.1.0a0",
+                    ),
+                ),
+                mock.patch.object(
+                    release_gate_core, "_run_command", side_effect=fake_command
+                ),
+                self.assertRaisesRegex(
+                    release_gate_core.ReleaseGateError,
+                    "^TRITRACK_RELEASE_DOWNSTREAM_SEAM$",
+                ),
+            ):
+                release_gate_core.fresh_install_smoke(
+                    wheel, root / "smoke", source
+                )
|
|    def test_manifest_is_closed_deterministic_and_schema_valid(self) -> None:
|        inspection = release_gate_core.DistributionInspection(
@@ -592,6 +707,17 @@ class OrchestrationTest(unittest.TestCase):
|            },
|        )
|        serialized = json.dumps(first, sort_keys=True)
+        self.assertEqual(
+            first["gates"],
+            {
+                "sourceIdentity": "pass",
+                "sourcePrivacy": "pass",
+                "wheelArchive": "pass",
+                "sdistArchive": "pass",
+                "freshInstall": "pass",
+                "downstreamSeam": "pass",
+            },
+        )
|        for forbidden in ("path", "time", "duration", "command", "log", "content"):
|            self.assertNotIn(forbidden, serialized.casefold())
|
~~~
