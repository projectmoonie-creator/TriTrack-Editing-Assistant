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
from tests.test_emit_fcpxml import media, sync_payload
from tests.test_run_workflow import aligned_bundle_files, aligned_manifest, sha256
from tritrack_editing_assistant import (
    contracts,
    emit_fcpxml,
    process,
    run_workflow,
    validate_artifacts,
)


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
        ), self.assertRaisesRegex(
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
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
            ) as raised:
                validate_artifacts.validate_contract_artifact(artifact)

            message = str(raised.exception)
            self.assertNotIn(str(root), message)
            self.assertNotIn("What changed?", message)


class FcpxmlValidationTest(unittest.TestCase):
    def render(self, root: Path) -> str:
        return emit_fcpxml.render_fcpxml(
            sync_payload(),
            media(root),
            profile_id="uhd-2997-ndf-fcpxml-1.14",
            binding_id="basic-title-v1",
            metadata=emit_fcpxml.ProjectMetadata("Invented Event", "Invented Cut"),
        )

    def test_validates_exact_bytes_with_installed_profile_and_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "story.fcpxml"
            encoded = self.render(root).encode("utf-8")
            artifact.write_bytes(encoded)

            with mock.patch.object(process, "run_bounded") as subprocess_call:
                summary = validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            subprocess_call.assert_not_called()
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.validate-summary/v1",
                    "toolVersion": "0.1.0a0",
                    "artifactKind": "fcpxml",
                    "validationScope": "structural-profile",
                    "hashes": {"artifact": hashlib.sha256(encoded).hexdigest()},
                    "counts": {},
                    "details": {
                        "profileId": "uhd-2997-ndf-fcpxml-1.14",
                        "bindingId": "basic-title-v1",
                    },
                },
            )
            self.assertEqual(artifact.read_bytes(), encoded)
            self.assertNotIn(str(root), json.dumps(summary))

    def test_rejects_profile_binding_xml_and_file_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = self.render(root)
            artifact = root / "story.fcpxml"
            artifact.write_text(valid, encoding="utf-8")

            for keyword, value in (
                ("profile_id", "unknown-profile"),
                ("binding_id", "unknown-binding"),
            ):
                arguments = {
                    "profile_id": "uhd-2997-ndf-fcpxml-1.14",
                    "binding_id": "basic-title-v1",
                }
                arguments[keyword] = value
                with self.subTest(keyword=keyword), self.assertRaisesRegex(
                    ValueError, "^TRITRACK_PROFILE_UNKNOWN"
                ):
                    validate_artifacts.validate_fcpxml_artifact(
                        artifact, **arguments
                    )

            artifact.write_text(
                valid.replace('width="3840"', 'width="1920"'),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_FCPXML_PROFILE_MISMATCH$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            artifact.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_FCPXML_INVALID$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            symlink = root / "link.fcpxml"
            symlink.symlink_to(artifact)
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_UNREADABLE$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    symlink,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

    def test_detects_late_fcpxml_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "story.fcpxml"
            valid = self.render(root)
            artifact.write_text(valid, encoding="utf-8")
            real_validate = emit_fcpxml.validate_fcpxml

            def changing_validate(*args, **kwargs) -> None:
                real_validate(*args, **kwargs)
                artifact.write_text(valid + " ", encoding="utf-8")

            with mock.patch.object(
                emit_fcpxml, "validate_fcpxml", side_effect=changing_validate
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )


class RunValidationTest(unittest.TestCase):
    def write_aligned_bundle(self, root: Path) -> tuple[Path, bytes, dict[str, bytes]]:
        run = root / "aligned-run"
        run.mkdir()
        files = aligned_bundle_files()
        for name, encoded in files.items():
            (run / name).write_bytes(encoded)
        manifest_bytes = run_workflow.encode_manifest(aligned_manifest(files))
        (run / "run-manifest.json").write_bytes(manifest_bytes)
        return run, manifest_bytes, files

    def test_shares_complete_run_authority_and_exact_status_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, manifest_bytes, files = self.write_aligned_bundle(root)
            entries_before = {path.name: path.read_bytes() for path in run.iterdir()}

            bundle, status = run_workflow.inspect_run(run)
            summary = validate_artifacts.validate_run_bundle(run)

            self.assertEqual(status, run_workflow.status_run(run))
            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.validate-summary/v1",
                    "toolVersion": "0.1.0a0",
                    "artifactKind": "run",
                    "validationScope": "complete-run-bundle",
                    "hashes": {"manifest": sha256(manifest_bytes)},
                    "counts": {"artifactCount": 2, "stageCount": 2},
                    "details": {"runSummary": status},
                },
            )
            self.assertEqual(
                entries_before,
                {path.name: path.read_bytes() for path in run.iterdir()},
            )
            self.assertEqual(
                summary["details"]["runSummary"]["artifacts"],
                {
                    "alignedTranscript": sha256(files["aligned-transcript.json"]),
                    "paperWorkbook": sha256(files["paper-edit.xlsx"]),
                },
            )
            self.assertNotIn(str(root), json.dumps(summary))
            self.assertNotIn("Invented words", json.dumps(summary))

    def test_inspection_detects_change_between_initial_load_and_recheck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, _, _ = self.write_aligned_bundle(root)
            real_load = run_workflow.load_bundle
            load_count = 0

            def changing_load(*args, **kwargs):
                nonlocal load_count
                loaded = real_load(*args, **kwargs)
                load_count += 1
                if load_count == 1:
                    (run / "paper-edit.xlsx").write_bytes(b"changed")
                return loaded

            with mock.patch.object(
                run_workflow, "load_bundle", side_effect=changing_load
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_RUN_INPUT_CHANGED$"
            ):
                run_workflow.inspect_run(run)


if __name__ == "__main__":
    unittest.main()
