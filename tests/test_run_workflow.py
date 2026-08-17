import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import run_workflow


def sha256(encoded: bytes) -> str:
    return hashlib.sha256(encoded).hexdigest()


def invented_sources() -> list[dict[str, object]]:
    return [
        {
            "camera": "B",
            "mediaId": "B-001.MP4",
            "sha256": "b" * 64,
            "transcribed": False,
        },
        {
            "camera": "A",
            "mediaId": "A-001.MP4",
            "sha256": "a" * 64,
            "transcribed": True,
        },
    ]


def prepared_artifacts() -> dict[str, dict[str, str]]:
    return {
        "transcriptBundle": {
            "fileName": "transcript-bundle.json",
            "sha256": "d" * 64,
        },
        "doctorReceipt": {"fileName": "doctor.json", "sha256": "b" * 64},
        "stringOut": {"fileName": "string-out.fcpxml", "sha256": "e" * 64},
        "syncMap": {"fileName": "sync-map.json", "sha256": "c" * 64},
    }


def prepared_stages() -> list[dict[str, object]]:
    return [
        {
            "name": "emit",
            "inputHashes": {"syncMap": "c" * 64},
            "outputHashes": {"stringOut": "e" * 64},
        },
        {
            "name": "transcribe",
            "inputHashes": {"sourceSet": "2" * 64},
            "outputHashes": {"transcriptBundle": "d" * 64},
        },
        {
            "name": "sync",
            "inputHashes": {"sourceSet": "1" * 64},
            "outputHashes": {"syncMap": "c" * 64},
        },
        {
            "name": "doctor",
            "inputHashes": {"profile": "f" * 64},
            "outputHashes": {"doctorReceipt": "b" * 64},
        },
    ]


def invented_aligned() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": "cue-addressed-v1",
        "sourceBundleSha256": "1" * 64,
        "revisionSha256": "2" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "A-001.MP4",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented words.",
                        "disposition": "original",
                    }
                ],
            }
        ],
    }


def aligned_bundle_files() -> dict[str, bytes]:
    aligned = (
        json.dumps(invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    return {
        "aligned-transcript.json": aligned,
        "paper-edit.xlsx": b"PK\x03\x04invented-workbook",
    }


def aligned_manifest(files: dict[str, bytes]) -> dict[str, object]:
    artifacts = {
        "alignedTranscript": {
            "fileName": "aligned-transcript.json",
            "sha256": sha256(files["aligned-transcript.json"]),
        },
        "paperWorkbook": {
            "fileName": "paper-edit.xlsx",
            "sha256": sha256(files["paper-edit.xlsx"]),
        },
    }
    return run_workflow.build_manifest(
        run_id="run-001",
        profile_id="uhd-2997-ndf-fcpxml-1.14",
        binding_id="basic-title-v1",
        phase="aligned",
        manifest_chain=["9" * 64],
        sources=invented_sources(),
        stages=[
            {
                "name": "paper",
                "inputHashes": {"alignedTranscript": sha256(files["aligned-transcript.json"])},
                "outputHashes": {"paperWorkbook": sha256(files["paper-edit.xlsx"])},
            },
            {
                "name": "align",
                "inputHashes": {"revision": "8" * 64},
                "outputHashes": {
                    "alignedTranscript": sha256(files["aligned-transcript.json"])
                },
            },
        ],
        artifacts=artifacts,
    )


class RunManifestTest(unittest.TestCase):
    def build(self, **changes) -> dict[str, object]:
        arguments = {
            "run_id": "run-001",
            "profile_id": "uhd-2997-ndf-fcpxml-1.14",
            "binding_id": "basic-title-v1",
            "phase": "prepared",
            "manifest_chain": [],
            "sources": invented_sources(),
            "stages": prepared_stages(),
            "artifacts": prepared_artifacts(),
        }
        arguments.update(changes)
        return run_workflow.build_manifest(**arguments)

    def test_builds_sorted_immutable_canonical_manifest(self) -> None:
        sources = invented_sources()
        stages = prepared_stages()
        artifacts = prepared_artifacts()
        before = copy.deepcopy((sources, stages, artifacts))

        manifest = self.build(sources=sources, stages=stages, artifacts=artifacts)
        first = run_workflow.encode_manifest(manifest)
        second = run_workflow.encode_manifest(copy.deepcopy(manifest))

        self.assertEqual((sources, stages, artifacts), before)
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertEqual(
            [(source["camera"], source["mediaId"]) for source in manifest["sources"]],
            [("A", "A-001.MP4"), ("B", "B-001.MP4")],
        )
        self.assertEqual(
            [stage["name"] for stage in manifest["stages"]],
            ["doctor", "sync", "transcribe", "emit"],
        )
        self.assertNotIn(b"createdAt", first)
        self.assertNotIn(b"status", first)
        self.assertNotIn(b"/Users/", first)

    def test_rejects_unsafe_duplicate_and_phase_drift(self) -> None:
        duplicate = invented_sources()
        duplicate.append(
            {
                "camera": "B",
                "mediaId": "A-001.MP4",
                "sha256": "9" * 64,
                "transcribed": False,
            }
        )
        invalid = [
            {"run_id": "../run"},
            {"phase": "running"},
            {"manifest_chain": ["1" * 64]},
            {"sources": duplicate},
        ]
        for changes in invalid:
            with (
                self.subTest(changes=changes),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_MANIFEST_INVALID"
                ),
            ):
                self.build(**changes)

    def test_rejects_foreign_artifact_filename_stage_and_hash(self) -> None:
        artifacts = prepared_artifacts()
        artifacts["syncMap"]["fileName"] = "foreign.json"
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(artifacts=artifacts)

        stages = prepared_stages()
        stages[0]["name"] = "validate"
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(stages=stages)

        stages = prepared_stages()
        stages[0]["outputHashes"]["stringOut"] = "9" * 64
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(stages=stages)

    def test_loads_complete_bundle_and_returns_sanitized_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "aligned-run"
            root.mkdir()
            files = aligned_bundle_files()
            for name, encoded in files.items():
                (root / name).write_bytes(encoded)
            manifest = aligned_manifest(files)
            manifest_bytes = run_workflow.encode_manifest(manifest)
            (root / "run-manifest.json").write_bytes(manifest_bytes)

            bundle = run_workflow.load_bundle(root, expected_phase="aligned")
            summary = run_workflow.summarize_bundle(bundle)

            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.run-summary/v1",
                    "runId": "run-001",
                    "phase": "aligned",
                    "nextAction": "edit-paper-workbook",
                    "stages": ["align", "paper"],
                    "artifacts": {
                        "alignedTranscript": sha256(
                            files["aligned-transcript.json"]
                        ),
                        "paperWorkbook": sha256(files["paper-edit.xlsx"]),
                    },
                },
            )
            self.assertNotIn(str(root), json.dumps(summary))
            self.assertNotIn("Invented words", json.dumps(summary))

    def test_load_rejects_noncanonical_changed_unlisted_and_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            files = aligned_bundle_files()
            for name, encoded in files.items():
                (root / name).write_bytes(encoded)
            manifest = aligned_manifest(files)
            (root / "run-manifest.json").write_text(
                json.dumps(manifest, separators=(",", ":")), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_MANIFEST_NONCANONICAL"
            ):
                run_workflow.load_bundle(root)

            (root / "run-manifest.json").write_bytes(
                run_workflow.encode_manifest(manifest)
            )
            (root / "paper-edit.xlsx").write_bytes(b"changed")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
            ):
                run_workflow.load_bundle(root)

            (root / "paper-edit.xlsx").write_bytes(files["paper-edit.xlsx"])
            (root / "foreign.txt").write_text("foreign", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_BUNDLE_INVALID"):
                run_workflow.load_bundle(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "incomplete"
            root.mkdir()
            (root / "aligned-transcript.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
            ):
                run_workflow.load_bundle(root)


class BundlePublicationTest(unittest.TestCase):
    def builder(self, files: dict[str, bytes], calls: list[Path] | None = None):
        def build(staging: Path) -> dict[str, object]:
            if calls is not None:
                calls.append(staging)
            for name, encoded in files.items():
                (staging / name).write_bytes(encoded)
            return aligned_manifest(files)

        return build

    def test_publishes_manifest_last_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = aligned_bundle_files()
            linked: list[str] = []
            real_link = os.link

            def recording_link(source, destination):
                linked.append(Path(destination).name)
                return real_link(source, destination)

            with mock.patch.object(
                run_workflow.os, "link", side_effect=recording_link
            ):
                first = run_workflow.publish_bundle(
                    root / "first", self.builder(files)
                )
            second = run_workflow.publish_bundle(root / "second", self.builder(files))

            self.assertEqual(linked[-1], "run-manifest.json")
            self.assertEqual(first.manifest, second.manifest)
            self.assertEqual(
                (root / "first" / "run-manifest.json").read_bytes(),
                (root / "second" / "run-manifest.json").read_bytes(),
            )
            self.assertEqual(list(root.glob(".*.staging-*")), [])

    def test_rejects_missing_existing_and_dangling_outputs_before_builder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = aligned_bundle_files()
            calls: list[Path] = []
            builder = self.builder(files, calls)
            existing = root / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                run_workflow.publish_bundle(existing, builder)

            dangling = root / "dangling"
            dangling.symlink_to(root / "missing")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                run_workflow.publish_bundle(dangling, builder)

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
            ):
                run_workflow.publish_bundle(root / "missing" / "run", builder)
            self.assertEqual(calls, [])

    def test_builder_and_link_failures_clean_only_owned_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            caller_input = root / "caller-input"
            caller_input.write_text("keep", encoding="utf-8")

            def failing_builder(staging: Path):
                (staging / "partial").write_text("partial", encoding="utf-8")
                raise RuntimeError("invented failure")

            with self.assertRaisesRegex(RuntimeError, "invented failure"):
                run_workflow.publish_bundle(root / "builder-failed", failing_builder)
            self.assertFalse((root / "builder-failed").exists())
            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(root.glob(".*.staging-*")), [])

            real_link = os.link
            link_count = 0

            def failing_link(source, destination):
                nonlocal link_count
                link_count += 1
                if link_count == 2:
                    raise OSError("invented link failure")
                return real_link(source, destination)

            with (
                mock.patch.object(
                    run_workflow.os, "link", side_effect=failing_link
                ),
                self.assertRaisesRegex(OSError, "invented link failure"),
            ):
                run_workflow.publish_bundle(
                    root / "link-failed", self.builder(aligned_bundle_files())
                )
            self.assertFalse((root / "link-failed").exists())
            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")

    def test_directory_reservation_race_preserves_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "race"
            real_mkdir = os.mkdir

            def racing_mkdir(path, mode=0o777, *, dir_fd=None):
                if Path(path) == output:
                    real_mkdir(path, mode)
                    (output / "winner").write_text("keep", encoding="utf-8")
                    raise FileExistsError
                return real_mkdir(path, mode, dir_fd=dir_fd)

            with (
                mock.patch.object(
                    run_workflow.os, "mkdir", side_effect=racing_mkdir
                ),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                run_workflow.publish_bundle(
                    output, self.builder(aligned_bundle_files())
                )
            self.assertEqual((output / "winner").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
