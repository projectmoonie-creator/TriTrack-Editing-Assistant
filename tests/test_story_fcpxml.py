import copy
import unittest
from decimal import Decimal
from pathlib import Path

from tritrack_editing_assistant import doctor, organizer, story_fcpxml

ALIGNED_SHA = "1" * 64
GROUPING_SHA = "2" * 64


def invented_sync_map() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "pairs": [
            {
                "pairId": "pair-001",
                "mediaA": "A-001.MP4",
                "mediaB": "B-001.MP4",
                "offsetBFromASeconds": 1.0,
                "confidence": 20.0,
                "overlapSeconds": 8.0,
                "audioMaster": "B",
                "durationASeconds": 10.0,
                "durationBSeconds": 8.0,
                "startedAt": None,
            }
        ],
        "singleA": ["A-002.MP4"],
        "singleB": [],
        "warnings": [],
    }


def invented_aligned() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": "cue-addressed-v1",
        "sourceBundleSha256": "3" * 64,
        "revisionSha256": "4" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "A-001.MP4",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 1000,
                        "endMs": 2000,
                        "text": "First paired thought.",
                        "disposition": "original",
                    },
                    {
                        "cueId": "cue-000002",
                        "startMs": 2000,
                        "endMs": 3500,
                        "text": "Second paired thought.",
                        "disposition": "revised",
                    },
                ],
            },
            {
                "takeId": "A-002.MP4",
                "sourceSha256": "c" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 1000,
                        "text": "Opening thought.",
                        "disposition": "original",
                    }
                ],
            },
            {
                "takeId": "B-001.MP4",
                "sourceSha256": "b" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 4000,
                        "endMs": 5000,
                        "text": "Reserve thought.",
                        "disposition": "original",
                    }
                ],
            },
        ],
    }


def invented_grouping() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.grouping/v1",
        "alignedTranscriptSha256": ALIGNED_SHA,
        "questions": [
            {
                "id": "question-opening",
                "question": "How does it begin?",
                "order": 1,
                "answers": [
                    {
                        "id": "answer-opening",
                        "order": 1,
                        "takeId": "A-002.MP4",
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000001",
                    }
                ],
            },
            {
                "id": "question-detail",
                "question": "What is the detail?",
                "order": 2,
                "answers": [
                    {
                        "id": "answer-paired",
                        "order": 1,
                        "takeId": "A-001.MP4",
                        "startCueId": "cue-000001",
                        "endCueId": "cue-000002",
                    }
                ],
            },
        ],
        "reserve": [
            {
                "id": "reserve-b",
                "order": 1,
                "takeId": "B-001.MP4",
                "startCueId": "cue-000001",
                "endCueId": "cue-000001",
                "reason": "Alternate angle",
            }
        ],
    }


def invented_working_cut(
    aligned: object, grouping: object
) -> dict[str, object]:
    result = organizer.build_working_cut(
        aligned,
        grouping,
        aligned_sha256=ALIGNED_SHA,
        grouping_sha256=GROUPING_SHA,
    )
    result["segments"].reverse()
    return result


def invented_sources() -> list[dict[str, object]]:
    return [
        {
            "camera": "B",
            "media_id": "B-001.MP4",
            "path": Path("/invented/B-001.MP4"),
            "duration_seconds": Decimal(8),
            "sha256": "b" * 64,
        },
        {
            "camera": "A",
            "media_id": "A-002.MP4",
            "path": Path("/invented/A-002.MP4"),
            "duration_seconds": Decimal(6),
            "sha256": "c" * 64,
        },
        {
            "camera": "A",
            "media_id": "A-001.MP4",
            "path": Path("/invented/A-001.MP4"),
            "duration_seconds": Decimal(10),
            "sha256": "a" * 64,
        },
    ]


class StoryTimelineTest(unittest.TestCase):
    def build(
        self,
        *,
        sync_map: dict[str, object] | None = None,
        aligned: dict[str, object] | None = None,
        grouping: dict[str, object] | None = None,
        working_cut: dict[str, object] | None = None,
        sources: list[dict[str, object]] | None = None,
        aligned_sha256: str = ALIGNED_SHA,
        grouping_sha256: str = GROUPING_SHA,
    ) -> story_fcpxml.StoryTimeline:
        selected_aligned = aligned or invented_aligned()
        selected_grouping = grouping or invented_grouping()
        selected_working_cut = working_cut or invented_working_cut(
            selected_aligned, selected_grouping
        )
        return story_fcpxml.build_story_timeline(
            sync_map or invented_sync_map(),
            selected_aligned,
            selected_grouping,
            selected_working_cut,
            sources or invented_sources(),
            aligned_sha256=aligned_sha256,
            grouping_sha256=grouping_sha256,
            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
        )

    def test_builds_story_order_from_exact_authorities(self) -> None:
        sync_map = invented_sync_map()
        aligned = invented_aligned()
        grouping = invented_grouping()
        working_cut = invented_working_cut(aligned, grouping)
        sources = invented_sources()
        before = copy.deepcopy((sync_map, aligned, grouping, working_cut, sources))

        timeline = story_fcpxml.build_story_timeline(
            sync_map,
            aligned,
            grouping,
            working_cut,
            sources,
            aligned_sha256=ALIGNED_SHA,
            grouping_sha256=GROUPING_SHA,
            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
        )

        self.assertEqual((sync_map, aligned, grouping, working_cut, sources), before)
        self.assertEqual(timeline.profile_id, "uhd-2997-ndf-fcpxml-1.14")
        self.assertEqual(timeline.duration_frames, 105)
        self.assertEqual(
            [(source.camera, source.media_id) for source in timeline.sources],
            [("A", "A-001.MP4"), ("A", "A-002.MP4"), ("B", "B-001.MP4")],
        )
        self.assertEqual(
            [segment.segment_id for segment in timeline.segments],
            ["answer-opening", "answer-paired"],
        )

        opening, paired = timeline.segments
        self.assertEqual(
            (opening.offset_frames, opening.duration_frames, opening.title_text),
            (0, 30, "Opening thought."),
        )
        self.assertEqual(len(opening.clips), 1)
        self.assertTrue(opening.clips[0].audio_enabled)

        self.assertEqual(
            (paired.offset_frames, paired.duration_frames, paired.title_text),
            (30, 75, "First paired thought. Second paired thought."),
        )
        self.assertEqual(
            [
                (
                    clip.camera,
                    clip.media_id,
                    clip.offset_frames,
                    clip.start_frames,
                    clip.duration_frames,
                    clip.audio_enabled,
                )
                for clip in paired.clips
            ],
            [
                ("A", "A-001.MP4", 30, 30, 75, False),
                ("B", "B-001.MP4", 30, 0, 75, True),
            ],
        )
        self.assertNotIn("reserve-b", [segment.segment_id for segment in timeline.segments])

    def test_rejects_authority_hash_and_copied_field_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
            self.build(aligned_sha256="9" * 64)

        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
            self.build(grouping_sha256="9" * 64)

        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
        working_cut["segments"][0]["startMs"] += 1
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
            self.build(working_cut=working_cut)

        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
        working_cut["segments"][0]["sourceSha256"] = "9" * 64
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
            self.build(working_cut=working_cut)

    def test_rejects_unknown_selection_and_nonpermutation_story_order(self) -> None:
        grouping = invented_grouping()
        grouping["questions"][0]["answers"][0]["takeId"] = "unknown.MP4"
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
            self.build(
                grouping=grouping,
                working_cut=invented_working_cut(
                    invented_aligned(), invented_grouping()
                ),
            )

        grouping = invented_grouping()
        grouping["questions"][0]["answers"][0]["startCueId"] = "cue-999999"
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_AUTHORITY_INVALID"):
            self.build(
                grouping=grouping,
                working_cut=invented_working_cut(
                    invented_aligned(), invented_grouping()
                ),
            )

        for story_order in (1, 3):
            working_cut = invented_working_cut(
                invented_aligned(), invented_grouping()
            )
            working_cut["segments"][0]["storyOrder"] = story_order
            with (
                self.subTest(story_order=story_order),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"
                ),
            ):
                self.build(working_cut=working_cut)

    def test_rejects_source_hash_set_and_audio_master_failures(self) -> None:
        sources = invented_sources()
        sources[2]["sha256"] = "9" * 64
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_STORY_SOURCE_HASH_MISMATCH"
        ):
            self.build(sources=sources)

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_STORY_SOURCE_SET_INVALID"
        ):
            self.build(sources=invented_sources()[:-1])

        sync_map = invented_sync_map()
        sync_map["pairs"][0]["durationBSeconds"] = 2.0
        sync_map["pairs"][0]["overlapSeconds"] = 2.0
        sources = invented_sources()
        sources[0]["duration_seconds"] = Decimal(2)
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_STORY_AUDIO_MASTER_COVERAGE"
        ):
            self.build(sync_map=sync_map, sources=sources)

    def test_rejects_zero_frame_selection_and_reserve_leakage(self) -> None:
        aligned = invented_aligned()
        aligned["takes"][1]["cues"][0]["endMs"] = 1
        grouping = invented_grouping()
        working_cut = invented_working_cut(aligned, grouping)
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_SELECTION_INVALID"):
            self.build(
                aligned=aligned,
                grouping=grouping,
                working_cut=working_cut,
            )

        working_cut = invented_working_cut(invented_aligned(), invented_grouping())
        reserve = working_cut["reserve"][0]
        working_cut["segments"].append(
            {
                "id": reserve["id"],
                "storyOrder": 3,
                "questionId": "question-detail",
                "takeId": reserve["takeId"],
                "sourceSha256": reserve["sourceSha256"],
                "startCueId": reserve["startCueId"],
                "endCueId": reserve["endCueId"],
                "startMs": reserve["startMs"],
                "endMs": reserve["endMs"],
            }
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_WORKING_CUT_DRIFT"):
            self.build(working_cut=working_cut)


if __name__ == "__main__":
    unittest.main()
