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
