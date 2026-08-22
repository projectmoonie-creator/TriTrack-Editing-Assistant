import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from openpyxl import load_workbook

from tritrack_editing_assistant import (
    align_text,
    doctor,
    emit_fcpxml,
    organizer,
    paper_edit,
    run_workflow,
    story_fcpxml,
    sync_scan,
    transcribe_takes,
    transcription_result,
)


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


def prepared_artifacts_v2() -> dict[str, dict[str, str]]:
    artifacts = prepared_artifacts()
    artifacts.update(
        {
            "transcriptionReport": {
                "fileName": "transcription-report.json",
                "sha256": "6" * 64,
            },
            "transcriptionResult": {
                "fileName": "transcription-result-manifest.json",
                "sha256": "7" * 64,
            },
        }
    )
    return artifacts


def prepared_stages_v2() -> list[dict[str, object]]:
    stages = prepared_stages()
    transcribe = next(stage for stage in stages if stage["name"] == "transcribe")
    transcribe["outputHashes"] = {
        "transcriptBundle": "d" * 64,
        "transcriptionReport": "6" * 64,
        "transcriptionResult": "7" * 64,
    }
    return stages


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

    def test_builds_v2_prepared_manifest_with_complete_transcription_authority(self) -> None:
        manifest = self.build(
            schema_version="tritrack.run-manifest/v2",
            artifacts=prepared_artifacts_v2(),
            stages=prepared_stages_v2(),
        )

        self.assertEqual(manifest["schemaVersion"], "tritrack.run-manifest/v2")
        self.assertEqual(
            set(manifest["artifacts"]),
            {
                "doctorReceipt",
                "syncMap",
                "transcriptBundle",
                "transcriptionReport",
                "transcriptionResult",
                "stringOut",
            },
        )
        transcribe = next(
            stage for stage in manifest["stages"] if stage["name"] == "transcribe"
        )
        self.assertEqual(
            set(transcribe["outputHashes"]),
            {"transcriptBundle", "transcriptionReport", "transcriptionResult"},
        )

    def test_run_manifest_v1_schema_bytes_remain_pinned(self) -> None:
        schema_path = (
            Path(run_workflow.__file__).parent
            / "schemas"
            / "run-manifest-v1.schema.json"
        )
        self.assertEqual(
            sha256(schema_path.read_bytes()),
            "f2cc085ddff1db4a83074de2d8f132823136a5689a98aa244e1278e1920242bf",
        )

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

    def test_rejects_extra_artifact_and_stage_facts(self) -> None:
        artifacts = prepared_artifacts()
        artifacts["foreign"] = {
            "fileName": "foreign.json",
            "sha256": "9" * 64,
        }
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(artifacts=artifacts)

        stages = prepared_stages()
        stages.append(
            {
                "name": "foreign",
                "action": "foreign",
                "outputHashes": {"foreign": "9" * 64},
            }
        )
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


class PrepareAlignTransitionTest(unittest.TestCase):
    def write_sources(
        self, root: Path
    ) -> tuple[list[sync_scan.MediaSource], list[sync_scan.MediaSource], Path]:
        source_a = root / "A-001.MP4"
        source_b = root / "B-001.MP4"
        model = root / "ggml-model.bin"
        source_a.write_bytes(b"invented-source-a")
        source_b.write_bytes(b"invented-source-b")
        model.write_bytes(b"invented-model")
        return (
            [sync_scan.MediaSource(source_a.name, source_a)],
            [sync_scan.MediaSource(source_b.name, source_b)],
            model,
        )

    @staticmethod
    def sync_payload() -> dict[str, object]:
        return {
            "schemaVersion": "tritrack.sync-map/v2",
            "profileId": "uhd-2997-ndf-fcpxml-1.14",
            "driftPrior": None,
            "groups": [
                {
                    "groupId": "group-001",
                    "anchor": {
                        "camera": "A",
                        "mediaId": "A-001.MP4",
                        "durationSeconds": 10.0,
                        "startedAt": None,
                    },
                    "sources": [
                        {
                            "camera": "B",
                            "mediaId": "B-001.MP4",
                            "offsetFromAnchorSeconds": 1.0,
                            "durationSeconds": 8.0,
                            "confidence": 20.0,
                            "overlapSeconds": 8.0,
                            "match": "correlation",
                            "startedAt": None,
                        }
                    ],
                    "audioMaster": "A",
                }
            ],
            "singles": [],
            "warnings": [],
        }

    def fakes(self, calls: list[str], *, supported: bool = True):
        def fake_doctor(output: Path, **_arguments):
            calls.append("doctor")
            receipt = {
                "schemaVersion": "tritrack.doctor-receipt/v1",
                "profileId": "uhd-2997-ndf-fcpxml-1.14",
                "titleBindingId": "basic-title-v1",
                "supported": supported,
                "checks": [],
                "remediation": [] if supported else ["Invented remediation"],
            }
            output.write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return receipt

        def fake_sync(_camera_a, _camera_b, *, output_path, **_arguments):
            calls.append("sync")
            payload = self.sync_payload()
            output_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return payload

        def fake_transcribe(
            media_paths, *, alternative_paths, model_path, language, **_
        ):
            calls.append("transcribe")
            source = Path(media_paths[0])
            self.assertEqual(
                alternative_paths,
                {source.name: (source.with_name("B-001.MP4"),)},
            )
            source_hash = sha256(source.read_bytes())
            settings = transcription_result.TranscriptionSettings(
                language=language,
                recognition_model_sha256=sha256(Path(model_path).read_bytes()),
                voice_activity="off",
                voice_activity_model=None,
            )
            request = transcription_result.TranscriptionRequest(
                take_id=source.name,
                sources=(
                    transcription_result.TranscriptionSource(source, source_hash),
                ),
            )
            return transcription_result.build_transcription_result(
                [request],
                settings=settings,
                engine_version="whisper.cpp version: invented",
                decoder=lambda _source, take_id, _settings: (
                    transcribe_takes.TranscribedTake(
                        take_id=take_id,
                        source_sha256=source_hash,
                        status="completed",
                        cues=(
                            {
                                "cueId": "cue-000001",
                                "startMs": 0,
                                "endMs": 500,
                                "text": "Invented words.",
                            },
                        ),
                    )
                ),
            )

        def fake_emit(
            camera_a,
            camera_b,
            *,
            sync_map_path,
            profile_id,
            binding_id,
            metadata,
            output_path,
        ):
            calls.append("emit")
            sources = [
                {
                    "camera": "A",
                    "media_id": camera_a[0].media_id,
                    "path": camera_a[0].path,
                    "duration_seconds": 10.0,
                },
                {
                    "camera": "B",
                    "media_id": camera_b[0].media_id,
                    "path": camera_b[0].path,
                    "duration_seconds": 8.0,
                },
            ]
            rendered = emit_fcpxml.render_fcpxml(
                json.loads(Path(sync_map_path).read_text(encoding="utf-8")),
                sources,
                profile_id=profile_id,
                binding_id=binding_id,
                metadata=metadata,
            )
            output_path.write_text(rendered, encoding="utf-8")
            return rendered

        return fake_doctor, fake_sync, fake_transcribe, fake_emit

    def prepare(
        self, root: Path, *, calls: list[str] | None = None
    ) -> tuple[run_workflow.LoadedRunBundle, list[sync_scan.MediaSource], Path]:
        camera_a, camera_b, model = self.write_sources(root)
        observed_calls = [] if calls is None else calls
        fake_doctor, fake_sync, fake_transcribe, fake_emit = self.fakes(
            observed_calls
        )
        output = root / "prepared-run"
        with (
            mock.patch.object(doctor, "write_receipt", side_effect=fake_doctor),
            mock.patch.object(
                sync_scan, "synchronize_and_publish", side_effect=fake_sync
            ),
            mock.patch.object(
                transcription_result,
                "transcribe_local_result",
                side_effect=fake_transcribe,
            ),
            mock.patch.object(
                emit_fcpxml, "emit_and_publish", side_effect=fake_emit
            ),
        ):
            summary = run_workflow.prepare_run(
                camera_a,
                camera_b,
                [camera_a[0].path],
                model_path=model,
                language="en",
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=emit_fcpxml.ProjectMetadata("Interview", "String-out"),
                run_id="run-001",
                output_dir=output,
            )
        self.assertEqual(summary["phase"], "prepared")
        return run_workflow.load_bundle(output), [*camera_a, *camera_b], model

    def test_prepare_calls_existing_engines_in_order_and_binds_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            calls: list[str] = []
            bundle, sources, model = self.prepare(root, calls=calls)

            self.assertEqual(calls, ["doctor", "sync", "transcribe", "emit"])
            self.assertEqual(bundle.manifest["phase"], "prepared")
            self.assertEqual(
                bundle.manifest["schemaVersion"], "tritrack.run-manifest/v2"
            )
            self.assertEqual(
                set(bundle.artifacts),
                {
                    "doctorReceipt",
                    "syncMap",
                    "transcriptBundle",
                    "transcriptionReport",
                    "transcriptionResult",
                    "stringOut",
                },
            )
            result_manifest = json.loads(
                bundle.artifacts["transcriptionResult"].encoded
            )
            self.assertEqual(
                result_manifest["bundle"]["sha256"],
                bundle.artifacts["transcriptBundle"].sha256,
            )
            self.assertEqual(
                result_manifest["report"]["sha256"],
                bundle.artifacts["transcriptionReport"].sha256,
            )
            self.assertEqual(
                [source["mediaId"] for source in bundle.manifest["sources"]],
                ["A-001.MP4", "B-001.MP4"],
            )
            self.assertEqual(
                [source["transcribed"] for source in bundle.manifest["sources"]],
                [True, False],
            )
            for source in sources:
                manifest_source = next(
                    item
                    for item in bundle.manifest["sources"]
                    if item["mediaId"] == source.media_id
                )
                self.assertEqual(
                    manifest_source["sha256"], sha256(source.path.read_bytes())
                )
            encoded = bundle.manifest_bytes
            self.assertNotIn(str(root).encode(), encoded)
            self.assertNotIn(model.name.encode(), encoded)
            self.assertNotIn(b"Invented words", encoded)

    def test_prepare_rejects_unsupported_subset_duplicate_and_late_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, model = self.write_sources(root)
            calls: list[str] = []
            fakes = self.fakes(calls, supported=False)
            with (
                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
                mock.patch.object(
                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
                ) as sync,
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED"
                ),
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-unsupported",
                    output_dir=root / "unsupported",
                )
            sync.assert_not_called()
            self.assertFalse((root / "unsupported").exists())

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID"
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [root / "foreign.MP4"],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-foreign",
                    output_dir=root / "foreign",
                )

            duplicate_path = root / "other" / "A-001.MP4"
            duplicate_path.parent.mkdir()
            duplicate_path.write_bytes(b"duplicate")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_SOURCE_ID_DUPLICATE"
            ):
                run_workflow.prepare_run(
                    camera_a,
                    [sync_scan.MediaSource("A-001.MP4", duplicate_path)],
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-duplicate",
                    output_dir=root / "duplicate",
                )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, model = self.write_sources(root)
            calls: list[str] = []
            fakes = list(self.fakes(calls))
            original_emit = fakes[3]

            def changing_emit(*args, **kwargs):
                rendered = original_emit(*args, **kwargs)
                model.write_bytes(b"changed-model")
                return rendered

            with (
                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
                mock.patch.object(
                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
                ),
                mock.patch.object(
                    transcription_result,
                    "transcribe_local_result",
                    side_effect=fakes[2],
                ),
                mock.patch.object(
                    emit_fcpxml, "emit_and_publish", side_effect=changing_emit
                ),
                self.assertRaisesRegex(ValueError, "TRITRACK_RUN_INPUT_CHANGED"),
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-changed",
                    output_dir=root / "changed",
                )
            self.assertFalse((root / "changed").exists())

    def test_align_accepts_no_change_revision_and_chains_prepared(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, _, _ = self.prepare(root)
            transcript = prepared.artifacts["transcriptBundle"]
            revision = {
                "schemaVersion": "tritrack.text-revision/v1",
                "sourceBundleSha256": transcript.sha256,
                "language": "en",
                "takes": [],
            }
            revision_path = root / "revision.json"
            revision_bytes = (
                json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            ).encode("utf-8")
            revision_path.write_bytes(revision_bytes)
            output = root / "aligned-run"

            with (
                mock.patch.object(
                    align_text,
                    "align_and_publish",
                    wraps=align_text.align_and_publish,
                ) as align,
                mock.patch.object(
                    paper_edit,
                    "export_workbook",
                    wraps=paper_edit.export_workbook,
                ) as paper,
            ):
                summary = run_workflow.align_run(
                    prepared.root, revision_path, output_dir=output
                )

            self.assertEqual([align.call_count, paper.call_count], [1, 1])
            self.assertEqual(summary["phase"], "aligned")
            aligned_bundle = run_workflow.load_bundle(output)
            self.assertEqual(
                aligned_bundle.manifest["manifestChain"],
                [prepared.manifest_sha256],
            )
            self.assertEqual(
                aligned_bundle.manifest["sources"], prepared.manifest["sources"]
            )
            aligned_payload = json.loads(
                aligned_bundle.artifacts["alignedTranscript"].encoded
            )
            self.assertTrue(
                all(
                    cue["disposition"] == "original"
                    for take in aligned_payload["takes"]
                    for cue in take["cues"]
                )
            )
            self.assertEqual(revision_path.read_bytes(), revision_bytes)

    def test_align_validates_prepared_bundle_before_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            incomplete = root / "incomplete"
            incomplete.mkdir()
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
            ):
                run_workflow.align_run(
                    incomplete,
                    root / "missing-revision.json",
                    output_dir=root / "aligned",
                )


class FinishStatusTransitionTest(PrepareAlignTransitionTest):
    def prepare_and_align(
        self, root: Path
    ) -> tuple[
        run_workflow.LoadedRunBundle,
        run_workflow.LoadedRunBundle,
        list[sync_scan.MediaSource],
    ]:
        prepared, sources, _ = self.prepare(root)
        transcript = prepared.artifacts["transcriptBundle"]
        revision = {
            "schemaVersion": "tritrack.text-revision/v1",
            "sourceBundleSha256": transcript.sha256,
            "language": "en",
            "takes": [],
        }
        revision_path = root / "revision.json"
        revision_path.write_text(
            json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        aligned_path = root / "aligned-run"
        run_workflow.align_run(
            prepared.root, revision_path, output_dir=aligned_path
        )
        return prepared, run_workflow.load_bundle(aligned_path), sources

    @staticmethod
    def edit_workbook(aligned: run_workflow.LoadedRunBundle, output: Path) -> None:
        output.write_bytes(aligned.artifacts["paperWorkbook"].encoded)
        workbook = load_workbook(output, data_only=False)
        workbook["Questions"].append(["question-001", "What happened?", 1])
        workbook["Selections"].append(
            [
                "ANSWER",
                "answer-001",
                "question-001",
                1,
                "A-001.MP4",
                "cue-000001",
                "cue-000001",
                None,
                None,
            ]
        )
        workbook.save(output)

    @staticmethod
    def probe(source: sync_scan.MediaSource) -> dict[str, object]:
        durations = {"A-001.MP4": 10.0, "B-001.MP4": 8.0}
        return {
            "duration_seconds": durations[source.media_id],
            "compatibility": {
                "videoStreamCount": 1,
                "audioStreamCount": 1,
                "width": 3840,
                "height": 2160,
                "frameRate": "30000/1001",
                "colorSpace": "bt709",
                "colorTransfer": "bt709",
                "colorPrimaries": "bt709",
                "sampleRate": "48000",
                "channels": 2,
            },
        }

    def finish(
        self,
        root: Path,
        prepared: run_workflow.LoadedRunBundle,
        aligned: run_workflow.LoadedRunBundle,
        sources: list[sync_scan.MediaSource],
        *,
        calls: list[str] | None = None,
    ) -> tuple[dict[str, object], Path]:
        workbook = root / "edited-paper.xlsx"
        self.edit_workbook(aligned, workbook)
        output = root / "finished-run"
        camera_a = [source for source in sources if source.media_id.startswith("A-")]
        camera_b = [source for source in sources if source.media_id.startswith("B-")]
        observed = [] if calls is None else calls
        real_apply = paper_edit.apply_workbook
        real_organize = organizer.organize_and_publish
        real_story = story_fcpxml.emit_story_and_publish

        def apply(*args, **kwargs):
            observed.append("paper")
            return real_apply(*args, **kwargs)

        def organize(*args, **kwargs):
            observed.append("organize")
            return real_organize(*args, **kwargs)

        def story(*args, **kwargs):
            observed.append("emit")
            return real_story(*args, **kwargs)

        with (
            mock.patch.object(paper_edit, "apply_workbook", side_effect=apply),
            mock.patch.object(
                organizer, "organize_and_publish", side_effect=organize
            ),
            mock.patch.object(
                story_fcpxml, "emit_story_and_publish", side_effect=story
            ),
            mock.patch.object(sync_scan, "probe_media", side_effect=self.probe),
        ):
            summary = run_workflow.finish_run(
                prepared.root,
                aligned.root,
                workbook,
                camera_a,
                camera_b,
                metadata=emit_fcpxml.ProjectMetadata("Interview", "Story cut"),
                output_dir=output,
            )
        return summary, output

    def test_finish_applies_organizes_emits_and_chains_exact_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            calls: list[str] = []

            summary, output = self.finish(
                root, prepared, aligned, sources, calls=calls
            )

            self.assertEqual(calls, ["paper", "organize", "emit"])
            self.assertEqual(summary["phase"], "finished")
            finished = run_workflow.load_bundle(output, expected_phase="finished")
            self.assertEqual(
                finished.manifest["manifestChain"],
                [prepared.manifest_sha256, aligned.manifest_sha256],
            )
            self.assertEqual(
                finished.manifest["sources"], prepared.manifest["sources"]
            )
            self.assertEqual(
                set(finished.artifacts), {"grouping", "workingCut", "storyCut"}
            )
            self.assertNotIn("What happened?", json.dumps(summary))
            self.assertNotIn(str(root), json.dumps(summary))

    def test_finish_rejects_chain_source_and_existing_output_before_engines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            workbook = root / "edited.xlsx"
            self.edit_workbook(aligned, workbook)
            camera_a = [sources[0]]
            camera_b = [sources[1]]
            existing = root / "existing"
            existing.mkdir()
            with (
                mock.patch.object(paper_edit, "apply_workbook") as apply,
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    camera_a,
                    camera_b,
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=existing,
                )
            apply.assert_not_called()

            sources[0].path.write_bytes(b"changed-source")
            with (
                mock.patch.object(paper_edit, "apply_workbook") as apply,
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_SOURCE_MISMATCH"
                ),
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    camera_a,
                    camera_b,
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=root / "source-mismatch",
                )
            apply.assert_not_called()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            changed = copy.deepcopy(aligned.manifest)
            changed["manifestChain"] = ["8" * 64]
            (aligned.root / "run-manifest.json").write_bytes(
                run_workflow.encode_manifest(changed)
            )
            workbook = root / "edited.xlsx"
            self.edit_workbook(aligned, workbook)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_CHAIN_MISMATCH"
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    [sources[0]],
                    [sources[1]],
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=root / "bad-chain",
                )

    def test_status_is_read_only_and_rejects_changed_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            _, output = self.finish(root, prepared, aligned, sources)
            before = {
                path.name: path.read_bytes() for path in output.iterdir()
            }

            summary = run_workflow.status_run(output)

            self.assertEqual(summary["phase"], "finished")
            self.assertEqual(summary["nextAction"], "complete")
            self.assertEqual(
                before,
                {path.name: path.read_bytes() for path in output.iterdir()},
            )
            self.assertNotIn("What happened?", json.dumps(summary))

            (output / "story-cut.fcpxml").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
            ):
                run_workflow.status_run(output)


if __name__ == "__main__":
    unittest.main()
