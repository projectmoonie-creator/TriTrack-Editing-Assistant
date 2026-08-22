"""Task 7 tests for local transcript evidence canonicalization."""

from __future__ import annotations

import hashlib
import inspect
import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import contracts, transcribe_takes


class TranscriptCanonicalizationTest(unittest.TestCase):
    def evidence(self) -> dict[str, object]:
        return {
            "result": {"language": "zh"},
            "transcription": [
                {
                    "offsets": {"from": 125, "to": 900},
                    "text": "  第一個 invented cue。 ",
                    "tokens": [{"id": 1}],
                },
                {
                    "offsets": {"from": 900, "to": 1500},
                    "text": "Cafe\u0301  cue",
                },
            ],
            "systeminfo": "ignored engine detail",
        }

    def test_canonicalizes_supported_whisper_evidence(self) -> None:
        cues = transcribe_takes.canonicalize_whisper_evidence(
            self.evidence(),
            requested_language="zh",
            audio_duration_ms=2000,
        )

        self.assertEqual(
            cues,
            [
                {
                    "cueId": "cue-000001",
                    "startMs": 125,
                    "endMs": 900,
                    "text": "第一個 invented cue。",
                },
                {
                    "cueId": "cue-000002",
                    "startMs": 900,
                    "endMs": 1500,
                    "text": "Café cue",
                },
            ],
        )

    def test_rejects_language_mismatch_and_invalid_timing(self) -> None:
        cases = []

        wrong_language = self.evidence()
        wrong_language["result"] = {"language": "en"}
        cases.append(wrong_language)

        overlapping = self.evidence()
        transcription = overlapping["transcription"]
        assert isinstance(transcription, list)
        second = transcription[1]
        assert isinstance(second, dict)
        second["offsets"] = {"from": 899, "to": 1500}
        cases.append(overlapping)

        bool_offset = self.evidence()
        transcription = bool_offset["transcription"]
        assert isinstance(transcription, list)
        first = transcription[0]
        assert isinstance(first, dict)
        first["offsets"] = {"from": False, "to": 900}
        cases.append(bool_offset)

        beyond_audio = self.evidence()
        transcription = beyond_audio["transcription"]
        assert isinstance(transcription, list)
        second = transcription[1]
        assert isinstance(second, dict)
        second["offsets"] = {"from": 2000, "to": 2001}
        cases.append(beyond_audio)

        for payload in cases:
            with self.subTest(payload=payload), self.assertRaisesRegex(
                (TypeError, ValueError), "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
            ):
                transcribe_takes.canonicalize_whisper_evidence(
                    payload,
                    requested_language="zh",
                    audio_duration_ms=2000,
                )

    def test_clamps_only_bounded_final_whisper_padding_to_audio_duration(self) -> None:
        evidence = {
            "result": {"language": "en"},
            "transcription": [
                {
                    "offsets": {"from": 0, "to": 5000},
                    "text": "Invented short cue.",
                }
            ],
        }

        cues = transcribe_takes.canonicalize_whisper_evidence(
            evidence,
            requested_language="en",
            audio_duration_ms=3424,
        )

        self.assertEqual(cues[0]["endMs"], 3424)

        evidence["transcription"][0]["offsets"] = {"from": 0, "to": 9000}
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
        ):
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=3424,
            )

    def test_rejects_one_cue_decoder_stutter_as_invalid_transcript(self) -> None:
        evidence = {
            "result": {"language": "zh"},
            "transcription": [
                {
                    "offsets": {"from": 0, "to": 35_800},
                    "text": "嗯,嗯,嗯,嗯,嗯,後面還有 invented speech",
                }
            ],
        }

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_ANOMALY_INVALID"
        ):
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="zh",
                audio_duration_ms=35_800,
            )

    def test_accepts_exact_blank_audio_sentinel_only_for_proven_silence(self) -> None:
        evidence = {
            "result": {"language": "en"},
            "transcription": [
                {
                    "offsets": {"from": 0, "to": 10000},
                    "text": " [BLANK_AUDIO]",
                }
            ],
        }

        self.assertEqual(
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=2000,
                proven_silence=True,
            ),
            [],
        )
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID"
        ):
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=2000,
            )

    def test_builds_strict_stably_sorted_bundle_and_bytes(self) -> None:
        take_a = transcribe_takes.TranscribedTake(
            take_id="A-001.MP4",
            source_sha256="a" * 64,
            status="completed",
            cues=(
                {
                    "cueId": "cue-000001",
                    "startMs": 0,
                    "endMs": 500,
                    "text": "Invented A cue.",
                },
            ),
        )
        take_b = transcribe_takes.TranscribedTake(
            take_id="B-001.MP4",
            source_sha256="b" * 64,
            status="empty",
            cues=(),
        )

        first = transcribe_takes.build_transcript_bundle(
            [take_b, take_a],
            language="zh",
            model_sha256="f" * 64,
            engine_version="whisper.cpp version: 1.9.1",
        )
        second = transcribe_takes.build_transcript_bundle(
            [take_a, take_b],
            language="zh",
            model_sha256="f" * 64,
            engine_version="whisper.cpp version: 1.9.1",
        )

        contracts.validate_contract("transcript-bundle-v1", first)
        self.assertEqual(first, second)
        self.assertEqual(first["profileId"], "whisper-cpp-cpu-no-fallback-v1")
        self.assertEqual(
            [take["takeId"] for take in first["takes"]],
            ["A-001.MP4", "B-001.MP4"],
        )
        self.assertEqual(
            transcribe_takes.encode_transcript_bundle(first),
            transcribe_takes.encode_transcript_bundle(second),
        )
        self.assertEqual(
            json.loads(transcribe_takes.encode_transcript_bundle(first)), first
        )

    def test_bundle_rejects_duplicate_take_ids(self) -> None:
        take = transcribe_takes.TranscribedTake(
            take_id="A-001.MP4",
            source_sha256="a" * 64,
            status="empty",
            cues=(),
        )

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_DUPLICATE_TAKE"
        ):
            transcribe_takes.build_transcript_bundle(
                [take, take],
                language="zh",
                model_sha256="f" * 64,
                engine_version="whisper.cpp version: 1.9.1",
            )

    def test_exposes_hash_bound_one_source_decode_seam(self) -> None:
        self.assertTrue(
            hasattr(transcribe_takes, "transcribe_source"),
            "one-source retry seam is not implemented",
        )
        parameters = inspect.signature(transcribe_takes.transcribe_source).parameters
        self.assertTrue(
            {
                "source_sha256",
                "model_sha256",
                "take_id",
                "model_path",
                "language",
            }.issubset(parameters)
        )


class LocalTranscriptionWorkflowTest(unittest.TestCase):
    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_descriptor_input_readers_reject_special_files_before_blocking(self) -> None:
        selected = Path("invented-special-file")
        readers = (
            lambda: transcribe_takes._sha256_file(selected),
            lambda: transcribe_takes._inspect_normalized_audio(selected),
            lambda: transcribe_takes._load_engine_json(selected),
        )

        for reader in readers:
            observed: list[int] = []

            def reject_special(_path, flags, *_args, observed=observed):
                observed.append(flags)
                raise OSError("invented special file")

            with self.subTest(reader=reader), mock.patch.object(
                transcribe_takes.os, "open", side_effect=reject_special
            ), self.assertRaises((OSError, ValueError)):
                reader()
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_NONBLOCK)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
    def test_transcript_hash_rejects_fifo_without_waiting_for_a_writer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fifo = Path(temporary) / "media.mov"
            os.mkfifo(fifo)
            code = (
                "from pathlib import Path; import sys; "
                "from tritrack_editing_assistant.transcribe_takes "
                "import _sha256_file; "
                "\ntry: _sha256_file(Path(sys.argv[1]))"
                "\nexcept ValueError as error: print(error); raise SystemExit(0)"
                "\nraise SystemExit(1)"
            )
            completed = subprocess.run(
                [os.fspath(Path(os.sys.executable)), "-c", code, os.fspath(fifo)],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "TRITRACK_TRANSCRIPT_INPUT_CHANGED\n")
        self.assertEqual(completed.stderr, "")

    def write_executable(self, root: Path, name: str, body: str) -> Path:
        path = root / name
        path.write_text(
            "#!/usr/bin/env python3\n" + textwrap.dedent(body),
            encoding="utf-8",
        )
        path.chmod(0o755)
        return path

    def write_ffmpeg(self, root: Path, *, sample: int) -> Path:
        return self.write_executable(
            root,
            "invented-ffmpeg",
            f"""
            import sys
            import wave

            with wave.open(sys.argv[-1], "wb") as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(16000)
                output.writeframes(bytes([{sample & 255}, {(sample >> 8) & 255}]) * 16000)
            """,
        )

    def write_whisper(
        self,
        root: Path,
        *,
        transcription: list[dict[str, object]],
        log: Path | None = None,
    ) -> Path:
        payload = {
            "result": {"language": "zh"},
            "transcription": transcription,
        }
        return self.write_executable(
            root,
            "invented-whisper",
            f"""
            import json
            import sys

            log_path = {str(log) if log is not None else None!r}
            if log_path is not None:
                with open(log_path, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(sys.argv[1:]) + "\\n")

            if "--version" in sys.argv:
                print("whisper.cpp version: invented-1")
                raise SystemExit(0)

            required = [
                "--model",
                "--file",
                "--language",
                "zh",
                "--temperature",
                "0",
                "--temperature-inc",
                "0",
                "--no-fallback",
                "--no-gpu",
                "--output-json-full",
                "--output-file",
                "--no-prints",
            ]
            if any(value not in sys.argv for value in required):
                raise SystemExit(9)
            if "--prompt" in sys.argv or "--translate" in sys.argv:
                raise SystemExit(10)

            prefix = sys.argv[sys.argv.index("--output-file") + 1]
            with open(prefix + ".json", "w", encoding="utf-8") as handle:
                json.dump({payload!r}, handle, ensure_ascii=False)
            """,
        )

    def test_source_result_carries_exact_audio_duration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "invented.mov"
            model = root / "invented-model.bin"
            media.write_bytes(b"invented source")
            model.write_bytes(b"invented model")
            ffmpeg = self.write_ffmpeg(root, sample=1)
            whisper = self.write_whisper(
                root,
                transcription=[
                    {
                        "offsets": {"from": 0, "to": 500},
                        "text": "Invented duration cue.",
                    }
                ],
            )

            result = transcribe_takes.transcribe_source(
                media,
                take_id=media.name,
                source_sha256=transcribe_takes._sha256_file(media),
                model_path=model,
                model_sha256=transcribe_takes._sha256_file(model),
                language="zh",
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )

        self.assertTrue(
            hasattr(result, "duration_ms"),
            "decoded source duration is not carried to orchestration",
        )
        self.assertEqual(result.duration_ms, 1000)

    def test_single_pass_publishes_stable_path_free_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media_a = root / "A-001.MP4"
            media_b = root / "B-001.MP4"
            model = root / "invented-model.bin"
            media_a.write_bytes(b"invented-source-a")
            media_b.write_bytes(b"invented-source-b")
            model.write_bytes(b"invented-local-model")
            ffmpeg = self.write_ffmpeg(root, sample=1)
            log = root / "whisper-argv.jsonl"
            whisper = self.write_whisper(
                root,
                transcription=[
                    {
                        "offsets": {"from": 0, "to": 500},
                        "text": " Invented local cue. ",
                    }
                ],
                log=log,
            )
            first_output = root / "first.json"
            second_output = root / "second.json"

            first = transcribe_takes.transcribe_and_publish(
                [media_b, media_a],
                model_path=model,
                language="zh",
                output_path=first_output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )
            second = transcribe_takes.transcribe_and_publish(
                [media_a, media_b],
                model_path=model,
                language="zh",
                output_path=second_output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )

            self.assertEqual(first, second)
            self.assertEqual(first_output.read_bytes(), second_output.read_bytes())
            self.assertEqual(
                first["modelSha256"], hashlib.sha256(model.read_bytes()).hexdigest()
            )
            self.assertEqual(
                [take["takeId"] for take in first["takes"]],
                ["A-001.MP4", "B-001.MP4"],
            )
            encoded = first_output.read_text(encoding="utf-8")
            self.assertNotIn(str(root), encoded)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            inference_calls = [call for call in calls if "--version" not in call]
            self.assertEqual(len(inference_calls), 4)
            self.assertTrue(all(call.count("--no-fallback") == 1 for call in inference_calls))

    def test_digital_silence_is_the_only_empty_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Silent.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-silent-source")
            model.write_bytes(b"invented-model")
            ffmpeg = self.write_ffmpeg(root, sample=0)
            whisper = self.write_whisper(
                root,
                transcription=[
                    {
                        "offsets": {"from": 0, "to": 10000},
                        "text": " [BLANK_AUDIO]",
                    }
                ],
            )
            output = root / "transcript.json"

            payload = transcribe_takes.transcribe_and_publish(
                [media],
                model_path=model,
                language="zh",
                output_path=output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )

            self.assertEqual(payload["takes"][0]["status"], "empty")
            self.assertEqual(payload["takes"][0]["cues"], [])

    def test_non_silent_empty_and_silent_text_fail_without_output(self) -> None:
        cases = ((1, []), (0, [{"offsets": {"from": 0, "to": 500}, "text": "Invented"}]))
        for sample, transcription in cases:
            with (
                self.subTest(sample=sample, transcription=transcription),
                tempfile.TemporaryDirectory() as temporary,
            ):
                    root = Path(temporary)
                    media = root / "Take.MP4"
                    model = root / "model.bin"
                    media.write_bytes(b"invented-source")
                    model.write_bytes(b"invented-model")
                    output = root / "transcript.json"

                    with self.assertRaisesRegex(
                        ValueError, "TRITRACK_TRANSCRIPT_(EMPTY_UNPROVEN|SILENCE_TEXT_DETECTED)"
                    ):
                        transcribe_takes.transcribe_and_publish(
                            [media],
                            model_path=model,
                            language="zh",
                            output_path=output,
                            ffmpeg_executable=str(self.write_ffmpeg(root, sample=sample)),
                            whisper_executable=str(
                                self.write_whisper(root, transcription=transcription)
                            ),
                        )
                    self.assertFalse(output.exists())

    def test_existing_output_and_duplicate_basenames_fail_before_processes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "transcript.json"
            output.write_text("sentinel", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                transcribe_takes.transcribe_and_publish(
                    [root / "missing.MP4"],
                    model_path=root / "missing-model.bin",
                    language="zh",
                    output_path=output,
                    ffmpeg_executable="missing-ffmpeg",
                    whisper_executable="missing-whisper",
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

            (root / "one").mkdir()
            (root / "two").mkdir()
            first = root / "one" / "Take.MP4"
            second = root / "two" / "Take.MP4"
            first.write_bytes(b"one")
            second.write_bytes(b"two")
            model = root / "model.bin"
            model.write_bytes(b"model")

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_DUPLICATE_TAKE"
            ):
                transcribe_takes.transcribe_and_publish(
                    [first, second],
                    model_path=model,
                    language="zh",
                    output_path=root / "new.json",
                    ffmpeg_executable="missing-ffmpeg",
                    whisper_executable="missing-whisper",
                )

    def test_detects_source_changes_during_audio_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source-before")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            ffmpeg = self.write_executable(
                root,
                "mutating-ffmpeg",
                """
                import sys
                import wave

                source = sys.argv[sys.argv.index("-i") + 1]
                with open(source, "ab") as handle:
                    handle.write(b"-changed")
                with wave.open(sys.argv[-1], "wb") as audio:
                    audio.setnchannels(1)
                    audio.setsampwidth(2)
                    audio.setframerate(16000)
                    audio.writeframes(bytes([1, 0]) * 16000)
                """,
            )
            whisper = self.write_whisper(
                root,
                transcription=[
                    {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                ],
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(ffmpeg),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_detects_model_changes_during_inference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model-before")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "mutating-whisper",
                """
                import json
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                model = sys.argv[sys.argv.index("--model") + 1]
                with open(model, "ab") as handle:
                    handle.write(b"-changed")
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {
                    "result": {"language": "zh"},
                    "transcription": [
                        {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                    ],
                }
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_rechecks_all_sources_after_the_complete_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "A.MP4"
            second = root / "B.MP4"
            model = root / "model.bin"
            first.write_bytes(b"invented-source-a")
            second.write_bytes(b"invented-source-b")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "late-mutating-whisper",
                """
                import json
                import sys
                from pathlib import Path

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                state = Path(__file__).with_suffix(".state")
                if state.exists():
                    with (Path(__file__).parent / "A.MP4").open("ab") as handle:
                        handle.write(b"-changed-after-first-take")
                else:
                    state.write_text("first", encoding="utf-8")
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {
                    "result": {"language": "zh"},
                    "transcription": [
                        {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                    ],
                }
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [first, second],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_invalid_engine_version_bytes_fail_with_stable_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "invalid-version-whisper",
                """
                import sys

                if "--version" in sys.argv:
                    sys.stdout.buffer.write(bytes([255]))
                    raise SystemExit(0)
                raise SystemExit(91)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_malformed_or_oversized_engine_output_never_publishes(self) -> None:
        scripts = {
            "malformed": """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    handle.write("{")
            """,
            "oversized": """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                with open(prefix + ".json", "wb") as handle:
                    handle.truncate(16 * 1024 * 1024 + 1)
            """,
        }
        for name, script in scripts.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                media = root / "Take.MP4"
                model = root / "model.bin"
                media.write_bytes(b"invented-source")
                model.write_bytes(b"invented-model")
                output = root / "transcript.json"

                with self.assertRaisesRegex(
                    ValueError, "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
                ):
                    transcribe_takes.transcribe_and_publish(
                        [media],
                        model_path=model,
                        language="zh",
                        output_path=output,
                        ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                        whisper_executable=str(
                            self.write_executable(root, f"{name}-whisper", script)
                        ),
                    )
                self.assertFalse(output.exists())

    def test_engine_capture_overflow_never_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "noisy-whisper",
                """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                sys.stdout.write("x" * (600 * 1024))
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIBE_ENGINE_FAILED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_publication_race_preserves_the_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "racing-whisper",
                f"""
                import json
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {{
                    "result": {{"language": "zh"}},
                    "transcription": [
                        {{"offsets": {{"from": 0, "to": 500}}, "text": "Invented"}}
                    ],
                }}
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                with open({str(output)!r}, "w", encoding="utf-8") as handle:
                    handle.write("race-winner")
                """,
            )

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "race-winner")


if __name__ == "__main__":
    unittest.main()
