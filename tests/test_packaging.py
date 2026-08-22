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
        self.assertEqual(len(policy["wheel"]["expectedMembers"]), 45)
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
