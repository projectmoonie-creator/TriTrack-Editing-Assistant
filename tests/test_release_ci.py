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
