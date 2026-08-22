"""Task 14 RED tests for text-free transcription provenance and retry."""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import sparse_source, transcribe_takes

try:
    from tritrack_editing_assistant import transcription_result
except ImportError:
    transcription_result = None


class TranscriptionResultTest(unittest.TestCase):
    def workflow(self):
        self.assertIsNotNone(
            transcription_result,
            "public transcription_result module is not implemented",
        )
        return transcription_result

    def test_exposes_hash_bound_local_command_orchestrator(self) -> None:
        self.assertTrue(
            hasattr(self.workflow(), "transcribe_and_publish_result"),
            "local command orchestrator is not implemented",
        )

    def test_local_orchestrator_rejects_reusing_primary_as_alternative(self) -> None:
        workflow = self.workflow()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "take-001.mov"
            model = root / "model.bin"
            media.write_bytes(b"invented media")
            model.write_bytes(b"invented model")
            with (
                mock.patch.object(
                    transcribe_takes,
                    "_read_engine_version",
                    side_effect=AssertionError("engine must not start"),
                ),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_TRANSCRIPT_ALTERNATIVE_INVALID"
                ),
            ):
                workflow.transcribe_local_result(
                    [media],
                    alternative_paths={media.name: [media]},
                    model_path=model,
                    language="zh",
                )

    def test_local_orchestrator_allows_one_alternative_for_multiple_takes(self) -> None:
        workflow = self.workflow()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "take-001.mov"
            second = root / "take-002.mov"
            shared = root / "shared-master.mov"
            model = root / "model.bin"
            for path in (first, second, shared, model):
                path.write_bytes(path.name.encode("utf-8"))

            captured = None

            def build(requests, **_arguments):
                nonlocal captured
                captured = requests
                return "invented-result"

            with (
                mock.patch.object(
                    transcribe_takes,
                    "_read_engine_version",
                    return_value="whisper.cpp invented-version",
                ),
                mock.patch.object(
                    workflow, "build_transcription_result", side_effect=build
                ),
            ):
                result = workflow.transcribe_local_result(
                    [first, second],
                    alternative_paths={
                        first.name: [shared],
                        second.name: [shared],
                    },
                    model_path=model,
                    language="zh",
                )

            self.assertEqual(result, "invented-result")
            self.assertIsNotNone(captured)
            self.assertEqual(
                [request.sources[1].path for request in captured],
                [shared, shared],
            )

    def settings(self):
        workflow = self.workflow()
        return workflow.TranscriptionSettings(
            language="zh",
            recognition_model_sha256="f" * 64,
            voice_activity="off",
            voice_activity_model=None,
        )

    def source(self, name: str, digest: str):
        return self.workflow().TranscriptionSource(
            path=Path(f"/invented/{name}"),
            sha256=digest,
        )

    def request(self, take_id: str, *sources):
        return self.workflow().TranscriptionRequest(
            take_id=take_id,
            sources=tuple(sources),
        )

    def completed(
        self,
        take_id: str,
        digest: str,
        *,
        text: str = "Invented cue.",
        duration_ms: int = 1000,
        duration_frame_count: int | None = None,
        sample_rate_hz: int | None = None,
    ):
        return transcribe_takes.TranscribedTake(
            take_id=take_id,
            source_sha256=digest,
            status="completed",
            cues=(
                {
                    "cueId": "cue-000001",
                    "startMs": 0,
                    "endMs": 1000,
                    "text": text,
                },
            ),
            duration_ms=duration_ms,
            duration_frame_count=duration_frame_count,
            sample_rate_hz=sample_rate_hz,
        )

    def resigned_result(self, result, report):
        workflow = self.workflow()
        report_bytes = workflow._canonical_bytes("transcription-report-v2", report)
        density_bytes = workflow._density_table(report)
        manifest = copy.deepcopy(result.manifest)
        manifest["report"]["sha256"] = hashlib.sha256(report_bytes).hexdigest()
        manifest["densityTable"]["sha256"] = hashlib.sha256(
            density_bytes
        ).hexdigest()
        return workflow.BuiltTranscriptionResult(
            bundle=result.bundle,
            report=report,
            manifest=manifest,
            bundle_bytes=result.bundle_bytes,
            report_bytes=report_bytes,
            manifest_bytes=workflow._canonical_bytes(
                "transcription-result-manifest-v2", manifest
            ),
            density_table_bytes=density_bytes,
        )

    def sparse(self, take_id: str, digest: str):
        return self.completed(
            take_id,
            digest,
            text="嗯",
            duration_ms=120_000,
        )

    def test_report_states_voice_activity_off(self) -> None:
        workflow = self.workflow()
        source = self.source("primary.mov", "a" * 64)

        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )

        self.assertEqual(result.report["runSettings"]["voiceActivity"], "off")
        self.assertIsNone(result.report["runSettings"]["voiceActivityModel"])
        attempt_settings = result.report["takes"][0]["attempts"][0]["settings"]
        self.assertEqual(attempt_settings, result.report["runSettings"])

    def test_retry_copies_primary_settings(self) -> None:
        workflow = self.workflow()
        observed_settings = []
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        def decode(source, take_id, settings):
            observed_settings.append(settings)
            if source.sha256 == "a" * 64:
                raise ValueError("TRITRACK_TRANSCRIPT_ANOMALY_INVALID")
            return self.completed(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        self.assertEqual(observed_settings, [self.settings(), self.settings()])
        attempts = result.report["takes"][0]["attempts"]
        self.assertEqual(
            [attempt["outcome"] for attempt in attempts],
            ["invalid", "completed"],
        )
        self.assertEqual(attempts[0]["settings"], attempts[1]["settings"])

    def test_sparse_primary_retries_and_adopts_usable_alternative(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)
        decoded = []

        def decode(source, take_id, _settings):
            decoded.append(source.sha256)
            if source.sha256 == "a" * 64:
                return self.sparse(take_id, source.sha256)
            return self.completed(
                take_id,
                source.sha256,
                text="足夠的 invented alternative content" * 4,
                duration_ms=60_000,
            )

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        self.assertEqual(decoded, ["a" * 64, "b" * 64])
        take = result.report["takes"][0]
        self.assertEqual([item["outcome"] for item in take["attempts"]], ["sparse", "completed"])
        self.assertEqual(take["selectedSourceSha256"], "b" * 64)
        self.assertEqual(take["selectionReason"], "primary-sparse")
        self.assertEqual(result.bundle["takes"][0]["sourceSha256"], "b" * 64)

    def test_sparse_primary_survives_when_alternative_is_not_better(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda source, take_id, _settings: self.sparse(
                take_id, source.sha256
            ),
        )

        take = result.report["takes"][0]
        self.assertEqual([item["outcome"] for item in take["attempts"]], ["sparse", "sparse"])
        self.assertEqual(take["selectionReason"], "no-better-source")
        self.assertEqual(take["selectedSourceSha256"], "a" * 64)
        self.assertEqual(result.report["summary"]["unrescuedTakeCount"], 1)

    def test_invalid_primary_can_adopt_sparse_alternative(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                raise ValueError("TRITRACK_TRANSCRIPT_ANOMALY_INVALID")
            return self.sparse(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        take = result.report["takes"][0]
        self.assertEqual([item["outcome"] for item in take["attempts"]], ["invalid", "sparse"])
        self.assertEqual(take["selectedSourceSha256"], "b" * 64)
        self.assertEqual(take["selectionReason"], "primary-invalid")

    def test_retry_and_adoption_call_the_shared_sparse_policy(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        with (
            mock.patch.object(
                sparse_source,
                "requires_retry",
                wraps=sparse_source.requires_retry,
            ) as retry_policy,
            mock.patch.object(
                sparse_source,
                "choose_source",
                wraps=sparse_source.choose_source,
            ) as choice_policy,
        ):
            workflow.build_transcription_result(
                [self.request("take-001", primary, alternative)],
                settings=self.settings(),
                engine_version="whisper.cpp invented-version",
                decoder=lambda source, take_id, _settings: self.sparse(
                    take_id, source.sha256
                ),
            )

        self.assertGreaterEqual(retry_policy.call_count, 1)
        self.assertGreaterEqual(choice_policy.call_count, 1)

    def test_report_records_metrics_summary_and_sorted_density_table(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                return self.sparse(take_id, source.sha256)
            return self.completed(
                take_id,
                source.sha256,
                text="x" * 120,
                duration_ms=60_000,
            )

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        self.assertEqual(
            result.report["schemaVersion"],
            "tritrack.transcription-report/v2",
        )
        attempts = result.report["takes"][0]["attempts"]
        self.assertEqual(
            attempts[0]["metrics"],
            {
                "durationMs": 120000,
                "durationFrameCount": 1920000,
                "sampleRateHz": 16000,
                "characterCount": 1,
                "charactersPerSecond": "0.008",
                "sparse": True,
            },
        )
        self.assertEqual(result.report["summary"]["retryAttemptCount"], 1)
        self.assertEqual(result.report["summary"]["sparseSourceCount"], 1)
        table = result.density_table_bytes.decode("utf-8")
        self.assertLess(table.index("0.008"), table.index("THRESHOLD"))
        self.assertLess(table.index("THRESHOLD"), table.index("2.000"))
        self.assertIn("THRESHOLD\t1.000\t-\t30.000", table)
        self.assertNotIn("/invented/", table)
        self.assertNotIn("x" * 20, table)

    def test_long_empty_source_counts_as_a_sparse_verdict(self) -> None:
        workflow = self.workflow()
        silent = self.source("silent.mov", "a" * 64)
        usable = self.source("usable.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                return transcribe_takes.TranscribedTake(
                    take_id=take_id,
                    source_sha256=source.sha256,
                    status="empty",
                    cues=(),
                    duration_ms=120_000,
                )
            return self.completed(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [
                self.request("take-001", silent),
                self.request("take-002", usable),
            ],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        attempt = result.report["takes"][0]["attempts"][0]
        self.assertEqual(attempt["outcome"], "empty")
        self.assertIs(attempt["metrics"]["sparse"], True)
        self.assertEqual(result.report["summary"]["sparseSourceCount"], 1)

    def test_shared_alternative_is_announced_on_both_takes(self) -> None:
        workflow = self.workflow()
        first = self.source("first.mov", "a" * 64)
        second = self.source("second.mov", "b" * 64)
        shared = self.source("shared.mov", "c" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 != "c" * 64:
                raise ValueError("TRITRACK_TRANSCRIPT_ANOMALY_INVALID")
            return self.completed(
                take_id,
                source.sha256,
                text="usable shared alternative" * 4,
                duration_ms=60_000,
            )

        result = workflow.build_transcription_result(
            [
                self.request("take-001", first, shared),
                self.request("take-002", second, shared),
            ],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        first_report, second_report = result.report["takes"]
        self.assertEqual(first_report["sharedAlternativeWithTakeIds"], ["take-002"])
        self.assertEqual(second_report["sharedAlternativeWithTakeIds"], ["take-001"])

    def test_one_failed_take_does_not_block_the_batch(self) -> None:
        workflow = self.workflow()
        failed = self.source("failed.mov", "a" * 64)
        usable = self.source("usable.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                raise ValueError("TRITRACK_TRANSCRIPT_ANOMALY_INVALID")
            return self.completed(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [self.request("take-failed", failed), self.request("take-usable", usable)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )

        self.assertEqual(
            [take["status"] for take in result.report["takes"]],
            ["failed", "completed"],
        )
        self.assertEqual(
            [take["takeId"] for take in result.bundle["takes"]],
            ["take-usable"],
        )

    def test_reuse_settings_are_unknown(self) -> None:
        attempt = self.workflow().reused_attempt("a" * 64)

        self.assertEqual(attempt.settings.language, "unknown")
        self.assertEqual(attempt.settings.recognition_model_sha256, "unknown")
        self.assertEqual(attempt.settings.voice_activity, "unknown")
        self.assertEqual(attempt.settings.voice_activity_model, "unknown")

    def test_matching_reuse_skips_decode_and_keeps_unknown_attempt_settings(self) -> None:
        workflow = self.workflow()
        self.assertIn(
            "reuse",
            inspect.signature(workflow.build_transcription_result).parameters,
            "immutable reuse input is not implemented",
        )
        source = self.source("primary.mov", "a" * 64)
        prior = self.completed("take-001", "a" * 64)

        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda *_arguments: self.fail("reused take must not decode"),
            reuse={"take-001": prior},
        )

        self.assertEqual(result.bundle["takes"][0]["cues"][0]["text"], "Invented cue.")
        report = result.report["takes"][0]
        self.assertEqual(report["status"], "reused")
        self.assertEqual(
            report["attempts"][0]["settings"],
            {
                "language": "unknown",
                "recognitionModelSha256": "unknown",
                "voiceActivity": "unknown",
                "voiceActivityModel": "unknown",
            },
        )

    def test_standalone_result_publishes_manifest_last_exact_directory(self) -> None:
        workflow = self.workflow()
        self.assertTrue(
            hasattr(workflow, "publish_transcription_result"),
            "manifest-last result publisher is not implemented",
        )
        source = self.source("primary.mov", "a" * 64)
        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            workflow.publish_transcription_result(output, result)

            self.assertEqual(
                {entry.name for entry in output.iterdir()},
                {
                    "manifest.json",
                    "transcript-bundle.json",
                    "transcription-report.json",
                    "transcription-density.txt",
                },
            )
            self.assertEqual(
                json.loads((output / "manifest.json").read_text(encoding="utf-8")),
                result.manifest,
            )

    def test_loader_verifies_exact_hash_bound_result_for_reuse(self) -> None:
        workflow = self.workflow()
        self.assertTrue(
            hasattr(workflow, "load_transcription_result"),
            "immutable transcription result loader is not implemented",
        )
        source = self.source("primary.mov", "a" * 64)
        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            workflow.publish_transcription_result(output, result)

            loaded = workflow.load_transcription_result(output)

        self.assertEqual(loaded.bundle, result.bundle)
        self.assertEqual(loaded.report, result.report)
        self.assertEqual(loaded.manifest, result.manifest)

    def test_loader_keeps_accepting_exact_v1_results(self) -> None:
        workflow = self.workflow()
        source = self.source("primary.mov", "a" * 64)
        current = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )
        report = {
            "schemaVersion": "tritrack.transcription-report/v1",
            "profileId": current.report["profileId"],
            "requestedTakeIds": current.report["requestedTakeIds"],
            "runSettings": current.report["runSettings"],
            "takes": [
                {
                    "takeId": "take-001",
                    "status": "completed",
                    "selectedSourceSha256": "a" * 64,
                    "attempts": [
                        {
                            "ordinal": 1,
                            "sourceSha256": "a" * 64,
                            "outcome": "completed",
                            "failureCode": None,
                            "settings": current.report["runSettings"],
                        }
                    ],
                }
            ],
        }
        report_bytes = workflow._canonical_bytes("transcription-report-v1", report)
        manifest = {
            "schemaVersion": "tritrack.transcription-result-manifest/v1",
            "bundle": {
                "fileName": "transcript-bundle.json",
                "sha256": hashlib.sha256(current.bundle_bytes).hexdigest(),
            },
            "report": {
                "fileName": "transcription-report.json",
                "sha256": hashlib.sha256(report_bytes).hexdigest(),
            },
        }
        legacy = workflow.BuiltTranscriptionResult(
            bundle=current.bundle,
            report=report,
            manifest=manifest,
            bundle_bytes=current.bundle_bytes,
            report_bytes=report_bytes,
            manifest_bytes=workflow._canonical_bytes(
                "transcription-result-manifest-v1", manifest
            ),
        )

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "legacy-result"
            workflow.publish_transcription_result(output, legacy)
            loaded = workflow.load_transcription_result(output)

        self.assertEqual(loaded.report["schemaVersion"], report["schemaVersion"])
        self.assertIsNone(loaded.density_table_bytes)

    def test_loader_rejects_hash_valid_report_disconnected_from_bundle(self) -> None:
        workflow = self.workflow()
        source = self.source("primary.mov", "a" * 64)
        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )
        report = copy.deepcopy(result.report)
        report["requestedTakeIds"] = ["different-take"]
        report["takes"][0]["takeId"] = "different-take"
        disconnected = self.resigned_result(result, report)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            workflow.publish_transcription_result(output, disconnected)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_RESULT_INVALID"
            ):
                workflow.load_transcription_result(output)

    def test_loader_rejects_hash_valid_retry_with_changed_settings(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                raise ValueError("TRITRACK_TRANSCRIPT_ANOMALY_INVALID")
            return self.completed(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )
        report = copy.deepcopy(result.report)
        report["takes"][0]["attempts"][1]["settings"]["language"] = "en"
        disconnected = self.resigned_result(result, report)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            workflow.publish_transcription_result(output, disconnected)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_RESULT_INVALID"
            ):
                workflow.load_transcription_result(output)

    def test_relationships_reject_internally_inconsistent_attempt_metrics(self) -> None:
        workflow = self.workflow()
        primary = self.source("primary.mov", "a" * 64)
        alternative = self.source("alternative.mov", "b" * 64)

        def decode(source, take_id, _settings):
            if source.sha256 == "a" * 64:
                return self.sparse(take_id, source.sha256)
            return self.completed(take_id, source.sha256)

        result = workflow.build_transcription_result(
            [self.request("take-001", primary, alternative)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=decode,
        )
        report = copy.deepcopy(result.report)
        report["takes"][0]["attempts"][0]["metrics"][
            "charactersPerSecond"
        ] = "9.999"

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_RESULT_INVALID"
        ):
            workflow.validate_result_relationships(result.bundle, report)

    def test_loader_rejects_fully_resigned_retry_after_usable_source(self) -> None:
        workflow = self.workflow()
        source = self.source("primary.mov", "a" * 64)
        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.completed(
                take_id, "a" * 64
            ),
        )
        report = copy.deepcopy(result.report)
        extra = copy.deepcopy(report["takes"][0]["attempts"][0])
        extra["ordinal"] = 2
        extra["sourceSha256"] = "b" * 64
        report["takes"][0]["attempts"].append(extra)
        report["summary"].update(
            {
                "sourceAttemptCount": 2,
                "retryAttemptCount": 1,
                "unrescuedTakeCount": 1,
            }
        )
        resigned = self.resigned_result(result, report)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            workflow.publish_transcription_result(output, resigned)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_RESULT_INVALID"
            ):
                workflow.load_transcription_result(output)

    def test_relationships_reject_sparse_label_for_selected_empty_bundle(self) -> None:
        workflow = self.workflow()
        source = self.source("primary.mov", "a" * 64)
        result = workflow.build_transcription_result(
            [self.request("take-001", source)],
            settings=self.settings(),
            engine_version="whisper.cpp invented-version",
            decoder=lambda _source, take_id, _settings: self.sparse(
                take_id, "a" * 64
            ),
        )
        bundle = copy.deepcopy(result.bundle)
        bundle["takes"][0]["status"] = "empty"
        bundle["takes"][0]["cues"] = []
        report = copy.deepcopy(result.report)
        report["takes"][0]["status"] = "empty"
        metrics = report["takes"][0]["attempts"][0]["metrics"]
        metrics["characterCount"] = 0
        metrics["charactersPerSecond"] = "0.000"

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_RESULT_INVALID"
        ):
            workflow.validate_result_relationships(bundle, report)


if __name__ == "__main__":
    unittest.main()
