"""Task 14 RED tests for text-free transcription provenance and retry."""

from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()

