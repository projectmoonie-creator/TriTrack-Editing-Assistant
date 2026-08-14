"""Task 5 public synchronization-engine tests."""

from __future__ import annotations

import copy
import json
import struct
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import contracts, process

try:
    from tritrack_editing_assistant import sync_scan
except ImportError:
    sync_scan = None


class SyncAlgorithmTest(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(
            sync_scan,
            "Task 5 requires the public sync_scan module",
        )
        return sync_scan

    def clip(self, identifier: str, start: str, duration: float):
        module = self.module()
        return {
            "id": identifier,
            "duration_seconds": duration,
            "start": module.parse_media_time(start),
            "has_audio": True,
        }

    def test_normalized_audio_correlation_recovers_offset(self) -> None:
        module = self.module()
        offset, ratio = module.normalized_audio_correlation(
            [0.0, 0.0, 1.0, 2.0, 4.0, 1.0, 0.0],
            [1.0, 2.0, 4.0, 1.0],
            sample_rate=1,
        )
        self.assertEqual(offset, 2.0)
        self.assertGreater(ratio, 1.0)

        with self.assertRaisesRegex(ValueError, "TRITRACK_SYNC_AUDIO_FLAT"):
            module.normalized_audio_correlation(
                [1.0, 1.0],
                [0.0, 1.0],
                sample_rate=1,
            )

    def test_stale_time_hints_fall_back_to_the_full_audio_cross_product(self) -> None:
        module = self.module()
        camera_a = [
            self.clip("A-001.MP4", "1980-01-01T00:00:00Z", 8.0),
            self.clip("A-002.MP4", "1980-01-01T00:00:10Z", 8.0),
        ]
        camera_b = [
            self.clip("B-001.MP4", "1980-01-01T00:00:00Z", 30.0),
            self.clip("B-002.MP4", "1980-01-01T02:00:00Z", 30.0),
        ]
        hints_ok = module.time_hints_are_sane(
            camera_a,
            camera_b,
            today=date(2026, 8, 13),
        )

        self.assertFalse(hints_ok)
        self.assertEqual(
            len(list(module.candidate_pairs(camera_a, camera_b, hints_ok=hints_ok))),
            4,
        )

    def test_sane_time_hints_narrow_audio_candidates(self) -> None:
        module = self.module()
        camera_a = [self.clip("A-001.MP4", "2026-08-13T01:00:00Z", 8.0)]
        camera_b = [
            self.clip("B-NEAR.MP4", "2026-08-13T01:00:00Z", 30.0),
            self.clip("B-FAR.MP4", "2026-08-13T02:00:00Z", 30.0),
        ]
        hints_ok = module.time_hints_are_sane(
            camera_a,
            camera_b,
            today=date(2026, 8, 13),
        )

        candidates = list(
            module.candidate_pairs(
                camera_a,
                camera_b,
                hints_ok=hints_ok,
                tolerance_seconds=0,
            )
        )
        self.assertTrue(hints_ok)
        self.assertEqual(
            [(a_clip["id"], b_clip["id"]) for a_clip, b_clip in candidates],
            [("A-001.MP4", "B-NEAR.MP4")],
        )

    def test_strongest_candidate_wins_long_b_is_reused_and_inputs_are_immutable(
        self,
    ) -> None:
        module = self.module()
        camera_a = [
            self.clip("A-001.MP4", "1980-01-01T00:00:00Z", 8.0),
            self.clip("A-002.MP4", "1980-01-01T00:00:10Z", 8.0),
        ]
        camera_b = [
            self.clip("B-WEAK.MP4", "1980-01-01T00:00:00Z", 30.0),
            self.clip("B-STRONG.MP4", "1980-01-01T00:00:00Z", 30.0),
        ]
        before = copy.deepcopy((camera_a, camera_b))

        def evidence_for(_a_clip, b_clip):
            return {
                "offset_seconds": 0.5,
                "peak_ratio": 7.0 if b_clip["id"] == "B-WEAK.MP4" else 20.0,
                "overlap_seconds": 8.0,
            }

        pairs = module.select_strongest_pairs(
            camera_a,
            camera_b,
            evidence_for=evidence_for,
            hints_ok=False,
        )

        self.assertEqual(
            [(pair["a"], pair["b"]) for pair in pairs],
            [
                ("A-001.MP4", "B-STRONG.MP4"),
                ("A-002.MP4", "B-STRONG.MP4"),
            ],
        )
        self.assertEqual((camera_a, camera_b), before)

    def test_sync_map_rejects_an_undeclared_compatibility_profile(self) -> None:
        module = self.module()
        with self.assertRaisesRegex(ValueError, "TRITRACK_PROFILE_UNKNOWN"):
            module.build_sync_map(
                [],
                [],
                profile_id="undeclared-profile",
                evidence_for=lambda _a_clip, _b_clip: None,
            )


class SyncIntegrationTest(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(
            sync_scan,
            "Task 5 requires the public sync_scan module",
        )
        return sync_scan

    def test_probe_media_uses_public_bounded_process_and_preserves_source(self):
        module = self.module()
        probe_payload = {
            "format": {
                "duration": "8.0",
                "tags": {"creation_time": "2026-08-13T01:00:00Z"},
            },
            "streams": [
                {
                    "codec_type": "video",
                    "width": 3840,
                    "height": 2160,
                    "r_frame_rate": "30000/1001",
                    "color_space": "bt709",
                    "color_transfer": "bt709",
                    "color_primaries": "bt709",
                },
                {
                    "codec_type": "audio",
                    "sample_rate": "48000",
                    "channels": 2,
                },
            ],
        }
        result = process.ProcessResult(
            status="ok",
            returncode=0,
            stdout=json.dumps(probe_payload).encode("utf-8"),
            stderr=b"",
            receipt={"schemaVersion": "tritrack.process-receipt/v1"},
        )

        with tempfile.TemporaryDirectory() as temporary:
            source_path = Path(temporary) / "A-001.MP4"
            source_path.write_bytes(b"invented-source")
            source = module.MediaSource("A-001.MP4", source_path)
            before = source_path.read_bytes()
            with mock.patch.object(module.process, "run_bounded", return_value=result) as run:
                clip = module.probe_media(source)

            command = run.call_args.args[0]
            self.assertEqual(command[0], "ffprobe")
            self.assertIn(str(source_path), command)
            self.assertEqual(clip["id"], "A-001.MP4")
            self.assertEqual(clip["duration_seconds"], 8.0)
            self.assertTrue(clip["has_audio"])
            self.assertEqual(
                clip["compatibility"],
                {
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
            )
            self.assertIn("width", command[command.index("-show_entries") + 1])
            self.assertIn("sample_rate", command[command.index("-show_entries") + 1])
            self.assertEqual(source_path.read_bytes(), before)

    def test_scan_builds_valid_contract_and_atomically_publishes_absent_output(
        self,
    ) -> None:
        module = self.module()
        probe_results = [
            process.ProcessResult(
                "ok",
                0,
                json.dumps(
                    {
                        "format": {
                            "duration": "7.0",
                            "tags": {"creation_time": "2026-08-13T01:00:00Z"},
                        },
                        "streams": [{"codec_type": "audio"}],
                    }
                ).encode(),
                b"",
                {},
            ),
            process.ProcessResult(
                "ok",
                0,
                json.dumps(
                    {
                        "format": {
                            "duration": "4.0",
                            "tags": {"creation_time": "2026-08-13T01:00:02Z"},
                        },
                        "streams": [{"codec_type": "audio"}],
                    }
                ).encode(),
                b"",
                {},
            ),
            process.ProcessResult(
                "ok",
                0,
                struct.pack("<7f", 0.0, 0.0, 1.0, 2.0, 4.0, 1.0, 0.0),
                b"",
                {},
            ),
            process.ProcessResult(
                "ok",
                0,
                struct.pack("<4f", 1.0, 2.0, 4.0, 1.0),
                b"",
                {},
            ),
        ]

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            a_path = root / "A-001.MP4"
            b_path = root / "B-001.MP4"
            a_path.write_bytes(b"invented-a")
            b_path.write_bytes(b"invented-b")
            before = {path: path.read_bytes() for path in (a_path, b_path)}
            output = root / "sync-map.json"
            with mock.patch.object(
                module.process,
                "run_bounded",
                side_effect=probe_results,
            ) as run:
                payload = module.synchronize_and_publish(
                    [module.MediaSource("A-001.MP4", a_path)],
                    [module.MediaSource("B-001.MP4", b_path)],
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    output_path=output,
                    today=date(2026, 8, 13),
                    sample_rate=1,
                    min_peak_ratio=1.0,
                )

            contracts.validate_contract("sync-map-v1", payload)
            self.assertEqual(json.loads(output.read_text()), payload)
            self.assertEqual(payload["pairs"][0]["offsetBFromASeconds"], 2.0)
            self.assertEqual(run.call_count, 4)
            self.assertEqual(
                {call.args[0][0] for call in run.call_args_list},
                {"ffprobe", "ffmpeg"},
            )
            self.assertEqual(
                {path: path.read_bytes() for path in (a_path, b_path)},
                before,
            )
            self.assertEqual(list(root.glob(".*.tmp")), [])

    def test_existing_output_fails_before_any_process_and_is_not_overwritten(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "A-001.MP4"
            source.write_bytes(b"source")
            output = root / "sync-map.json"
            output.write_text("sentinel", encoding="utf-8")
            with (
                mock.patch.object(module.process, "run_bounded") as run,
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                module.synchronize_and_publish(
                    [module.MediaSource("A-001.MP4", source)],
                    [module.MediaSource("B-001.MP4", source)],
                    profile_id="profile",
                    output_path=output,
                )

            run.assert_not_called()
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_publication_race_never_overwrites_the_winning_output(self) -> None:
        module = self.module()
        payload = {
            "schemaVersion": "tritrack.sync-map/v1",
            "profileId": "profile",
            "pairs": [],
            "singleA": [],
            "singleB": [],
            "warnings": [],
        }

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "sync-map.json"

            def racing_link(_temporary_path, destination):
                Path(destination).write_text("race-winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(module.os, "link", side_effect=racing_link),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                module.publish_sync_map(output, payload)

            self.assertEqual(output.read_text(encoding="utf-8"), "race-winner")
            self.assertEqual(list(root.glob(".*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
