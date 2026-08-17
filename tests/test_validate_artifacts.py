"""Task 11 tests for read-only, offline artifact validation."""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.test_contracts import VALID_CONTRACTS
from tritrack_editing_assistant import contracts, validate_artifacts


def encode_json(payload: object) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


class ContractValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        contracts.contract_names_by_schema_version.cache_clear()

    def tearDown(self) -> None:
        contracts.contract_names_by_schema_version.cache_clear()

    def test_discovers_every_installed_contract_from_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, payload in VALID_CONTRACTS.items():
                with self.subTest(name=name):
                    encoded = encode_json(payload)
                    artifact = root / f"{name}.json"
                    artifact.write_bytes(encoded)

                    summary = validate_artifacts.validate_contract_artifact(
                        artifact
                    )

                    self.assertEqual(
                        summary,
                        {
                            "schemaVersion": "tritrack.validate-summary/v1",
                            "toolVersion": "0.1.0a0",
                            "artifactKind": "contract",
                            "validationScope": "contract",
                            "hashes": {
                                "artifact": hashlib.sha256(encoded).hexdigest()
                            },
                            "counts": {},
                            "details": {
                                "contractName": name,
                                "contractSchemaVersion": payload["schemaVersion"],
                            },
                        },
                    )
                    self.assertEqual(artifact.read_bytes(), encoded)

    def test_rejects_unknown_invalid_and_unreadable_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            unknown = root / "unknown.json"
            unknown.write_bytes(encode_json({"schemaVersion": "invented/v1"}))
            invalid = root / "invalid.json"
            payload = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
            payload["questions"][0]["unexpected"] = True
            invalid.write_bytes(encode_json(payload))
            malformed = root / "malformed.json"
            malformed.write_bytes(b"{not-json")
            empty = root / "empty.json"
            empty.write_bytes(b"")
            symlink = root / "symlink.json"
            symlink.symlink_to(unknown)

            cases = (
                (unknown, "TRITRACK_VALIDATE_CONTRACT_UNKNOWN"),
                (invalid, "TRITRACK_VALIDATE_CONTRACT_INVALID"),
                (malformed, "TRITRACK_VALIDATE_JSON_INVALID"),
                (empty, "TRITRACK_VALIDATE_INPUT_INVALID"),
                (symlink, "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
                (root / "missing.json", "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
            )
            for artifact, code in cases:
                with self.subTest(code=code), self.assertRaisesRegex(
                    ValueError, rf"^{code}$"
                ):
                    validate_artifacts.validate_contract_artifact(artifact)

    def test_rejects_duplicate_installed_schema_versions(self) -> None:
        profile = contracts.load_schema("compatibility-profile-v1")
        duplicate = copy.deepcopy(profile)
        with mock.patch.object(
            contracts,
            "load_schema",
            side_effect=lambda name: duplicate
            if name == "sync-map-v1"
            else profile,
        ):
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_CONTRACT_REGISTRY_INVALID$"
            ):
                contracts.contract_names_by_schema_version()

    def test_detects_late_contract_change_without_leaking_path_or_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "private-name.json"
            encoded = encode_json(VALID_CONTRACTS["grouping-v1"])
            artifact.write_bytes(encoded)
            real_validate = contracts.validate_contract

            def changing_validate(name: str, payload: object) -> None:
                real_validate(name, payload)
                artifact.write_bytes(encoded + b" ")

            with mock.patch.object(
                contracts, "validate_contract", side_effect=changing_validate
            ):
                with self.assertRaisesRegex(
                    ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
                ) as raised:
                    validate_artifacts.validate_contract_artifact(artifact)

            message = str(raised.exception)
            self.assertNotIn(str(root), message)
            self.assertNotIn("What changed?", message)


if __name__ == "__main__":
    unittest.main()
