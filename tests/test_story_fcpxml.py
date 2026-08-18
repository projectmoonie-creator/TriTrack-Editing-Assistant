import copy
import hashlib
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import (
    doctor,
    emit_fcpxml,
    organizer,
    story_fcpxml,
    sync_scan,
)

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


class StoryRenderingTest(unittest.TestCase):
    def timeline(self) -> story_fcpxml.StoryTimeline:
        aligned = invented_aligned()
        grouping = invented_grouping()
        return story_fcpxml.build_story_timeline(
            invented_sync_map(),
            aligned,
            grouping,
            invented_working_cut(aligned, grouping),
            invented_sources(),
            aligned_sha256=ALIGNED_SHA,
            grouping_sha256=GROUPING_SHA,
            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
        )

    def test_renders_deterministic_profile_bound_story_xml(self) -> None:
        timeline = self.timeline()
        metadata = emit_fcpxml.ProjectMetadata("Interview & more", "Story cut")

        first = story_fcpxml.render_story_fcpxml(
            timeline,
            profile_id="uhd-2997-ndf-fcpxml-1.14",
            binding_id="basic-title-v1",
            metadata=metadata,
        )
        second = story_fcpxml.render_story_fcpxml(
            timeline,
            profile_id="uhd-2997-ndf-fcpxml-1.14",
            binding_id="basic-title-v1",
            metadata=metadata,
        )

        self.assertEqual(first, second)
        self.assertIn("Interview &amp; more", first)
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        binding = doctor.load_title_binding("basic-title-v1")
        emit_fcpxml.validate_fcpxml(first, profile=profile, binding=binding)
        root = ET.fromstring(first)
        sequence = root.find("./library/event/project/sequence")
        assert sequence is not None
        self.assertEqual(sequence.attrib["duration"], "105105/30000s")
        gaps = root.findall("./library/event/project/sequence/spine/gap")
        self.assertEqual(
            [gap.attrib["name"] for gap in gaps],
            ["answer-opening", "answer-paired"],
        )
        self.assertEqual(
            [gap.find("./title/text/text-style").text for gap in gaps],
            [
                "Opening thought.",
                "First paired thought. Second paired thought.",
            ],
        )
        paired_clips = gaps[1].findall("./asset-clip")
        self.assertEqual(
            [
                (
                    clip.attrib["name"],
                    clip.attrib["offset"],
                    clip.attrib["start"],
                    clip.attrib["duration"],
                    clip.attrib["srcEnable"],
                )
                for clip in paired_clips
            ],
            [
                (
                    "A-001.MP4",
                    "30030/30000s",
                    "30030/30000s",
                    "75075/30000s",
                    "video",
                ),
                (
                    "B-001.MP4",
                    "30030/30000s",
                    "0s",
                    "75075/30000s",
                    "all",
                ),
            ],
        )


class StoryFileBoundaryTest(unittest.TestCase):
    def write_inputs(
        self, root: Path
    ) -> tuple[
        list[sync_scan.MediaSource],
        list[sync_scan.MediaSource],
        dict[str, Path],
        dict[Path, bytes],
    ]:
        source_paths = {
            "A-001.MP4": root / "A-001.MP4",
            "A-002.MP4": root / "A-002.MP4",
            "B-001.MP4": root / "B-001.MP4",
        }
        source_bytes = {
            "A-001.MP4": b"invented-camera-a-one",
            "A-002.MP4": b"invented-camera-a-two",
            "B-001.MP4": b"invented-camera-b-one",
        }
        for media_id, path in source_paths.items():
            path.write_bytes(source_bytes[media_id])

        aligned = invented_aligned()
        for take in aligned["takes"]:
            take["sourceSha256"] = hashlib.sha256(
                source_bytes[take["takeId"]]
            ).hexdigest()
        aligned_bytes = (
            json.dumps(aligned, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")
        aligned_path = root / "aligned-transcript.json"
        aligned_path.write_bytes(aligned_bytes)

        grouping = invented_grouping()
        grouping["alignedTranscriptSha256"] = hashlib.sha256(
            aligned_bytes
        ).hexdigest()
        grouping_bytes = organizer.encode_grouping(grouping)
        grouping_path = root / "grouping.json"
        grouping_path.write_bytes(grouping_bytes)

        working_cut = organizer.build_working_cut(
            aligned,
            grouping,
            aligned_sha256=hashlib.sha256(aligned_bytes).hexdigest(),
            grouping_sha256=hashlib.sha256(grouping_bytes).hexdigest(),
        )
        working_cut_bytes = organizer.encode_working_cut(working_cut)
        working_cut_path = root / "working-cut.json"
        working_cut_path.write_bytes(working_cut_bytes)

        sync_bytes = (
            json.dumps(
                invented_sync_map(), ensure_ascii=False, indent=2, sort_keys=True
            )
            + "\n"
        ).encode("utf-8")
        sync_path = root / "sync-map.json"
        sync_path.write_bytes(sync_bytes)
        paths = {
            "sync": sync_path,
            "aligned": aligned_path,
            "grouping": grouping_path,
            "working": working_cut_path,
        }
        before = {
            **{path: path.read_bytes() for path in source_paths.values()},
            **{path: path.read_bytes() for path in paths.values()},
        }
        return (
            [
                sync_scan.MediaSource("A-001.MP4", source_paths["A-001.MP4"]),
                sync_scan.MediaSource("A-002.MP4", source_paths["A-002.MP4"]),
            ],
            [sync_scan.MediaSource("B-001.MP4", source_paths["B-001.MP4"])],
            paths,
            before,
        )

    @staticmethod
    def probe(media_id: str) -> dict[str, object]:
        durations = {"A-001.MP4": 10.0, "A-002.MP4": 6.0, "B-001.MP4": 8.0}
        return {
            "duration_seconds": durations[media_id],
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

    def emit(
        self,
        camera_a: list[sync_scan.MediaSource],
        camera_b: list[sync_scan.MediaSource],
        paths: dict[str, Path],
        output: Path,
    ) -> str:
        return story_fcpxml.emit_story_and_publish(
            camera_a,
            camera_b,
            sync_map_path=paths["sync"],
            aligned_path=paths["aligned"],
            grouping_path=paths["grouping"],
            working_cut_path=paths["working"],
            profile_id="uhd-2997-ndf-fcpxml-1.14",
            binding_id="basic-title-v1",
            metadata=emit_fcpxml.ProjectMetadata("Interview", "Story cut"),
            output_path=output,
        )

    def test_publishes_exact_story_xml_without_mutating_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, before = self.write_inputs(root)
            output = root / "story-cut.fcpxml"
            with mock.patch.object(
                sync_scan,
                "probe_media",
                side_effect=lambda source: self.probe(source.media_id),
            ):
                rendered = self.emit(camera_a, camera_b, paths, output)

            self.assertEqual(output.read_text(encoding="utf-8"), rendered)
            self.assertTrue(rendered.endswith("\n"))
            self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_existing_output_and_missing_parent_fail_before_input_reads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "story-cut.fcpxml"
            output.write_text("winner", encoding="utf-8")
            missing = {
                "sync": root / "missing-sync",
                "aligned": root / "missing-aligned",
                "grouping": root / "missing-grouping",
                "working": root / "missing-working",
            }
            with (
                mock.patch.object(emit_fcpxml, "probe_sources") as probe,
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                self.emit([], [], missing, output)
            probe.assert_not_called()
            self.assertEqual(output.read_text(encoding="utf-8"), "winner")

            with (
                mock.patch.object(emit_fcpxml, "probe_sources") as probe,
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
                ),
            ):
                self.emit([], [], missing, root / "absent" / "story.fcpxml")
            probe.assert_not_called()

    def test_rejects_malformed_symlink_and_noncanonical_authorities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            paths["sync"].write_bytes(b"not-json")
            with self.assertRaisesRegex(ValueError, "TRITRACK_STORY_SYNC_INVALID"):
                self.emit(camera_a, camera_b, paths, root / "malformed.fcpxml")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            target = root / "aligned-target.json"
            target.write_bytes(paths["aligned"].read_bytes())
            paths["aligned"].unlink()
            paths["aligned"].symlink_to(target)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_STORY_ALIGNED_INVALID"
            ):
                self.emit(camera_a, camera_b, paths, root / "symlink.fcpxml")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            grouping = json.loads(paths["grouping"].read_text(encoding="utf-8"))
            paths["grouping"].write_text(
                json.dumps(grouping, separators=(",", ":")), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_STORY_GROUPING_NONCANONICAL"
            ):
                self.emit(camera_a, camera_b, paths, root / "compact.fcpxml")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            working_cut = json.loads(
                paths["working"].read_text(encoding="utf-8")
            )
            paths["working"].write_text(
                json.dumps(working_cut, separators=(",", ":")), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_STORY_WORKING_CUT_NONCANONICAL"
            ):
                self.emit(
                    camera_a,
                    camera_b,
                    paths,
                    root / "compact-working-cut.fcpxml",
                )

    def test_late_source_mutation_is_detected_before_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            mutated = False

            def mutating_probe(source: sync_scan.MediaSource) -> dict[str, object]:
                nonlocal mutated
                result = self.probe(source.media_id)
                if not mutated:
                    source.path.write_bytes(b"changed-after-first-hash")
                    mutated = True
                return result

            with (
                mock.patch.object(
                    sync_scan, "probe_media", side_effect=mutating_probe
                ),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_STORY_INPUT_CHANGED"
                ),
            ):
                self.emit(camera_a, camera_b, paths, root / "changed.fcpxml")
            self.assertFalse((root / "changed.fcpxml").exists())

    def test_late_symlink_swap_is_reported_as_input_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            original_render = story_fcpxml.render_story_fcpxml
            target = root / "late-target.json"
            target.write_bytes(paths["aligned"].read_bytes())

            def render_then_swap(*args, **kwargs):
                rendered = original_render(*args, **kwargs)
                paths["aligned"].unlink()
                paths["aligned"].symlink_to(target)
                return rendered

            with (
                mock.patch.object(
                    sync_scan,
                    "probe_media",
                    side_effect=lambda source: self.probe(source.media_id),
                ),
                mock.patch.object(
                    story_fcpxml,
                    "render_story_fcpxml",
                    side_effect=render_then_swap,
                ),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_STORY_INPUT_CHANGED"
                ),
            ):
                self.emit(camera_a, camera_b, paths, root / "late.fcpxml")
            self.assertFalse((root / "late.fcpxml").exists())

    def test_publication_race_preserves_the_winner_and_cleans_temporary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, paths, _ = self.write_inputs(root)
            output = root / "race.fcpxml"

            def racing_link(_temporary: Path, destination: Path) -> None:
                Path(destination).write_text("race-winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(
                    sync_scan,
                    "probe_media",
                    side_effect=lambda source: self.probe(source.media_id),
                ),
                mock.patch.object(emit_fcpxml.os, "link", side_effect=racing_link),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                self.emit(camera_a, camera_b, paths, output)
            self.assertEqual(output.read_text(encoding="utf-8"), "race-winner")
            self.assertEqual(list(root.glob(".*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
