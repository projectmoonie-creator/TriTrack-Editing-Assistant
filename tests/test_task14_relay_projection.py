"""End-to-end RED boundary from sync-map-v2 authority to a timeline."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema.exceptions import ValidationError

from tritrack_editing_assistant import doctor, emit_fcpxml, string_out


class RelayProjectionRedTest(unittest.TestCase):
    def test_v2_relay_reaches_timeline_with_one_audio_rig(self) -> None:
        sync_map = {
            "schemaVersion": "tritrack.sync-map/v2",
            "profileId": "uhd-2997-ndf-fcpxml-1.14",
            "driftPrior": None,
            "groups": [
                {
                    "groupId": "group-001",
                    "anchor": {
                        "camera": "A",
                        "mediaId": "anchor.mov",
                        "durationSeconds": 600.0,
                        "startedAt": None,
                    },
                    "sources": [
                        {
                            "camera": "B",
                            "mediaId": "relay-first.mov",
                            "offsetFromAnchorSeconds": 0.0,
                            "durationSeconds": 300.0,
                            "confidence": 8.0,
                            "overlapSeconds": 300.0,
                            "match": "correlation",
                            "startedAt": None,
                        },
                        {
                            "camera": "B",
                            "mediaId": "relay-second.mov",
                            "offsetFromAnchorSeconds": 300.0,
                            "durationSeconds": 300.0,
                            "confidence": 7.0,
                            "overlapSeconds": 300.0,
                            "match": "correlation",
                            "startedAt": None,
                        },
                    ],
                    "audioMaster": "B",
                }
            ],
            "singles": [],
            "warnings": [],
        }
        sources = [
            {
                "camera": "A",
                "media_id": "anchor.mov",
                "path": Path("/invented/anchor.mov"),
                "duration_seconds": 600.0,
            },
            {
                "camera": "B",
                "media_id": "relay-first.mov",
                "path": Path("/invented/relay-first.mov"),
                "duration_seconds": 300.0,
            },
            {
                "camera": "B",
                "media_id": "relay-second.mov",
                "path": Path("/invented/relay-second.mov"),
                "duration_seconds": 300.0,
            },
        ]

        try:
            timeline = string_out.build_string_out(
                sync_map,
                sources,
                profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
            )
        except (TypeError, ValueError, ValidationError) as error:
            self.fail(f"sync-map-v2 relay is not consumable: {error}")

        self.assertEqual(len(timeline.segments), 1)
        clips = timeline.segments[0].clips
        self.assertEqual([clip.media_id for clip in clips], [
            "anchor.mov",
            "relay-first.mov",
            "relay-second.mov",
        ])
        self.assertEqual(
            [clip.media_id for clip in clips if clip.audio_enabled],
            ["relay-first.mov", "relay-second.mov"],
        )
        self.assertEqual(clips[1].offset_frames, 0)
        self.assertGreater(clips[2].offset_frames, clips[1].offset_frames)

        with tempfile.TemporaryDirectory() as temporary:
            sync_path = Path(temporary) / "sync-map.json"
            sync_path.write_text(json.dumps(sync_map), encoding="utf-8")
            try:
                loaded = emit_fcpxml.load_sync_map(sync_path)
            except ValueError as error:
                self.fail(f"emit command loader rejects sync-map-v2: {error}")
        self.assertEqual(loaded["schemaVersion"], "tritrack.sync-map/v2")

        try:
            rendered = emit_fcpxml.render_fcpxml(
                sync_map,
                sources,
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=emit_fcpxml.ProjectMetadata("Invented event", "Relay cut"),
            )
        except ValueError as error:
            self.fail(f"sync-map-v2 relay does not reach valid FCPXML: {error}")
        self.assertEqual(rendered.count('srcEnable="all"'), 2)
        self.assertIn('name="relay-first.mov"', rendered)
        self.assertIn('name="relay-second.mov"', rendered)


if __name__ == "__main__":
    unittest.main()
