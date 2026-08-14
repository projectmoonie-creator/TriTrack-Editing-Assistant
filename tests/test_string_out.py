"""Task 6 deterministic public string-out tests."""

from __future__ import annotations

import copy
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from tritrack_editing_assistant import doctor

try:
    from tritrack_editing_assistant import string_out
except ImportError:
    string_out = None


def pair(
    pair_id: str,
    media_a: str,
    media_b: str,
    *,
    offset: str,
    duration_a: str,
    duration_b: str,
) -> dict[str, object]:
    return {
        "pairId": pair_id,
        "mediaA": media_a,
        "mediaB": media_b,
        "offsetBFromASeconds": Decimal(offset),
        "confidence": Decimal("18.5"),
        "overlapSeconds": Decimal("0.5"),
        "audioMaster": "A",
        "durationASeconds": Decimal(duration_a),
        "durationBSeconds": Decimal(duration_b),
        "startedAt": None,
    }


def sync_map() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "pairs": [
            pair(
                "pair-002",
                "A-002.MP4",
                "B-002.MP4",
                offset="-0.5",
                duration_a="2.0",
                duration_b="1.0",
            ),
            pair(
                "pair-001",
                "A-001.MP4",
                "B-001.MP4",
                offset="0.5",
                duration_a="1.0",
                duration_b="2.0",
            ),
        ],
        "singleA": ["A-003.MP4"],
        "singleB": ["B-003.MP4"],
        "warnings": [],
    }


def sources() -> list[dict[str, object]]:
    return [
        {
            "camera": "B",
            "media_id": "B-003.MP4",
            "path": Path("invented/B-003.MP4"),
            "duration_seconds": Decimal("0.5"),
        },
        {
            "camera": "A",
            "media_id": "A-002.MP4",
            "path": Path("invented/A-002.MP4"),
            "duration_seconds": Decimal("2.0"),
        },
        {
            "camera": "B",
            "media_id": "B-001.MP4",
            "path": Path("invented/B-001.MP4"),
            "duration_seconds": Decimal("2.0"),
        },
        {
            "camera": "A",
            "media_id": "A-003.MP4",
            "path": Path("invented/A-003.MP4"),
            "duration_seconds": Decimal("0.5"),
        },
        {
            "camera": "B",
            "media_id": "B-002.MP4",
            "path": Path("invented/B-002.MP4"),
            "duration_seconds": Decimal("1.0"),
        },
        {
            "camera": "A",
            "media_id": "A-001.MP4",
            "path": Path("invented/A-001.MP4"),
            "duration_seconds": Decimal("1.0"),
        },
    ]


class StringOutTest(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(
            string_out,
            "Task 6 requires the public string_out module",
        )
        return string_out

    def test_frame_exact_pair_alignment_sorting_and_input_immutability(self) -> None:
        module = self.module()
        payload = sync_map()
        media = sources()
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        before = copy.deepcopy((payload, media, profile))

        timeline = module.build_string_out(payload, media, profile=profile)

        self.assertEqual(
            [segment.label for segment in timeline.segments],
            [
                "pair-001",
                "pair-002",
                "single-A-A-003.MP4",
                "single-B-B-003.MP4",
            ],
        )
        self.assertEqual(
            [segment.offset_frames for segment in timeline.segments],
            [0, 75, 150, 165],
        )
        self.assertEqual(
            [segment.duration_frames for segment in timeline.segments],
            [75, 75, 15, 15],
        )
        first_pair = timeline.segments[0].clips
        second_pair = timeline.segments[1].clips
        self.assertEqual(
            [(clip.camera, clip.offset_frames) for clip in first_pair],
            [("A", 0), ("B", 15)],
        )
        self.assertEqual(
            [(clip.camera, clip.offset_frames) for clip in second_pair],
            [("A", 90), ("B", 75)],
        )
        self.assertEqual(timeline.duration_frames, 180)
        self.assertEqual((payload, media, profile), before)

    def test_string_out_bytes_are_independent_of_source_and_pair_input_order(self):
        module = self.module()
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        first = module.build_string_out(sync_map(), sources(), profile=profile)
        changed_map = sync_map()
        changed_map["pairs"] = list(reversed(changed_map["pairs"]))
        second = module.build_string_out(
            changed_map,
            list(reversed(sources())),
            profile=profile,
        )
        self.assertEqual(first, second)

    def test_schema_drift_unknown_profile_and_source_set_fail_closed(self) -> None:
        module = self.module()
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")

        drifted = sync_map()
        drifted["unexpected"] = True
        with self.assertRaises(ValidationError):
            module.build_string_out(drifted, sources(), profile=profile)

        unknown_profile = sync_map()
        unknown_profile["profileId"] = "unknown-profile"
        with self.assertRaisesRegex(ValueError, "TRITRACK_PROFILE_UNKNOWN"):
            module.build_string_out(unknown_profile, sources(), profile=profile)

        with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_SOURCE_SET_MISMATCH"):
            module.build_string_out(sync_map(), sources()[:-1], profile=profile)

        extra = sources() + [
            {
                "camera": "A",
                "media_id": "A-EXTRA.MP4",
                "path": Path("invented/A-EXTRA.MP4"),
                "duration_seconds": Decimal(1),
            }
        ]
        with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_SOURCE_SET_MISMATCH"):
            module.build_string_out(sync_map(), extra, profile=profile)

    def test_pair_duration_mismatch_and_duplicate_pair_id_fail_closed(self) -> None:
        module = self.module()
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        changed_sources = sources()
        changed_sources[1]["duration_seconds"] = Decimal("2.5")
        with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_DURATION_MISMATCH"):
            module.build_string_out(sync_map(), changed_sources, profile=profile)

        duplicated = sync_map()
        duplicated["pairs"][1]["pairId"] = "pair-002"
        with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_PAIR_ID_DUPLICATE"):
            module.build_string_out(duplicated, sources(), profile=profile)


if __name__ == "__main__":
    unittest.main()
