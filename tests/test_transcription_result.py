"""Task 14 RED tests for text-free transcription provenance and retry."""

from __future__ import annotations

import inspect
import json
import tempfile
import unittest
from pathlib import Path

from tritrack_editing_assistant import transcribe_takes

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

    def completed(self, take_id: str, digest: str):
        return transcribe_takes.TranscribedTake(
            take_id=take_id,
            source_sha256=digest,
            status="completed",
            cues=(
                {
                    "cueId": "cue-000001",
                    "startMs": 0,
                    "endMs": 1000,
                    "text": "Invented cue.",
                },
            ),
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


if __name__ == "__main__":
    unittest.main()
