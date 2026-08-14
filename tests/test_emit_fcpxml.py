"""Task 6 profile-bound FCPXML emission tests."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import doctor, sync_scan

try:
    from tritrack_editing_assistant import emit_fcpxml
except ImportError:
    emit_fcpxml = None


def sync_payload() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": "uhd-2997-ndf-fcpxml-1.14",
        "pairs": [
            {
                "pairId": "pair-001",
                "mediaA": "A & 001.MP4",
                "mediaB": "B-001.MP4",
                "offsetBFromASeconds": Decimal("0.5"),
                "confidence": Decimal(20),
                "overlapSeconds": Decimal("0.5"),
                "audioMaster": "A",
                "durationASeconds": Decimal(1),
                "durationBSeconds": Decimal(1),
                "startedAt": None,
            }
        ],
        "singleA": [],
        "singleB": [],
        "warnings": [],
    }


def media(root: Path) -> list[dict[str, object]]:
    return [
        {
            "camera": "B",
            "media_id": "B-001.MP4",
            "path": root / "B-001.MP4",
            "duration_seconds": Decimal(1),
        },
        {
            "camera": "A",
            "media_id": "A & 001.MP4",
            "path": root / "A & 001.MP4",
            "duration_seconds": Decimal(1),
        },
    ]


class FcpxmlRenderingTest(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(
            emit_fcpxml,
            "Task 6 requires the public emit_fcpxml module",
        )
        return emit_fcpxml

    def test_render_is_byte_deterministic_profile_bound_and_xml_escaped(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            payload = sync_payload()
            sources = media(root_path)
            metadata = module.ProjectMetadata(
                event_name='Invented & Event <One> "safe"',
                project_name="Invented > String-out & Cut",
            )
            before = copy.deepcopy((payload, sources, metadata))

            first = module.render_fcpxml(
                payload,
                sources,
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=metadata,
            )
            second = module.render_fcpxml(
                payload,
                list(reversed(sources)),
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=metadata,
            )

        self.assertEqual(first, second)
        self.assertEqual((payload, sources, metadata), before)
        self.assertTrue(first.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn("<!DOCTYPE fcpxml>", first)
        self.assertIn(
            'Invented &amp; Event &lt;One&gt; &quot;safe&quot;',
            first,
        )
        self.assertNotIn('event name="Invented & Event', first)

        root = ET.fromstring(first)
        self.assertEqual(root.attrib, {"version": "1.14"})
        format_element = root.find("./resources/format")
        self.assertIsNotNone(format_element)
        self.assertEqual(
            format_element.attrib,
            {
                "id": "r1",
                "name": "FFVideoFormat3840x2160p2997",
                "frameDuration": "1001/30000s",
                "width": "3840",
                "height": "2160",
                "colorSpace": "1-1-1 (Rec. 709)",
            },
        )
        assets = root.findall("./resources/asset")
        self.assertEqual([asset.attrib["id"] for asset in assets], ["r3", "r4"])
        self.assertEqual(
            [asset.attrib["name"] for asset in assets],
            ["A & 001.MP4", "B-001.MP4"],
        )
        sequence = root.find("./library/event/project/sequence")
        self.assertIsNotNone(sequence)
        self.assertEqual(sequence.attrib["duration"], "45045/30000s")
        self.assertEqual(sequence.attrib["tcFormat"], "NDF")
        self.assertEqual(sequence.attrib["audioRate"], "48k")
        module.validate_fcpxml(
            first,
            profile=doctor.load_profile("uhd-2997-ndf-fcpxml-1.14"),
            binding=doctor.load_title_binding("basic-title-v1"),
        )

    def test_unknown_binding_and_generated_profile_drift_fail_closed(self) -> None:
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "TRITRACK_PROFILE_UNKNOWN"):
                module.render_fcpxml(
                    sync_payload(),
                    media(Path(temporary)),
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="unknown-binding",
                    metadata=module.ProjectMetadata("Event", "Project"),
                )

            rendered = module.render_fcpxml(
                sync_payload(),
                media(Path(temporary)),
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=module.ProjectMetadata("Event", "Project"),
            )
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        binding = doctor.load_title_binding("basic-title-v1")
        with self.assertRaisesRegex(ValueError, "TRITRACK_FCPXML_PROFILE_MISMATCH"):
            module.validate_fcpxml(
                rendered.replace('width="3840"', 'width="1920"'),
                profile=profile,
                binding=binding,
            )
        with self.assertRaisesRegex(ValueError, "TRITRACK_FCPXML_PROFILE_MISMATCH"):
            module.validate_fcpxml(
                rendered.replace('audioRate="48k"', 'audioRate="44.1k"', 1),
                profile=profile,
                binding=binding,
            )

    def test_fcpxml_114_assets_use_required_original_media_rep(self) -> None:
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            rendered = module.render_fcpxml(
                sync_payload(),
                media(Path(temporary)),
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=module.ProjectMetadata("Event", "Project"),
            )

        root = ET.fromstring(rendered)
        for asset in root.findall("./resources/asset"):
            self.assertNotIn("src", asset.attrib)
            media_representations = asset.findall("./media-rep")
            self.assertEqual(len(media_representations), 1)
            self.assertEqual(
                media_representations[0].attrib["kind"],
                "original-media",
            )
            self.assertTrue(media_representations[0].attrib["src"].startswith("file:"))

    def test_publish_is_atomic_and_never_overwrites_a_race_winner(self) -> None:
        module = self.module()
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        binding = doctor.load_title_binding("basic-title-v1")
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            rendered = module.render_fcpxml(
                sync_payload(),
                media(root_path),
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=module.ProjectMetadata("Event", "Project"),
            )
            output = root_path / "string-out.fcpxml"
            module.publish_fcpxml(
                output,
                rendered,
                profile=profile,
                binding=binding,
            )
            self.assertEqual(output.read_text(encoding="utf-8"), rendered)

            race_output = root_path / "race.fcpxml"

            def racing_link(_temporary_path, destination):
                Path(destination).write_text("race-winner", encoding="utf-8")
                raise FileExistsError

            with (
                mock.patch.object(module.os, "link", side_effect=racing_link),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                module.publish_fcpxml(
                    race_output,
                    rendered,
                    profile=profile,
                    binding=binding,
                )
            self.assertEqual(race_output.read_text(encoding="utf-8"), "race-winner")
            self.assertEqual(list(root_path.glob(".*.tmp")), [])

    def test_existing_output_fails_before_sync_map_or_source_probe(self) -> None:
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            root_path = Path(temporary)
            output = root_path / "existing.fcpxml"
            output.write_text("sentinel", encoding="utf-8")
            with (
                mock.patch.object(sync_scan, "probe_media") as probe,
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                module.emit_and_publish(
                    [sync_scan.MediaSource("A.MP4", root_path / "missing-a")],
                    [sync_scan.MediaSource("B.MP4", root_path / "missing-b")],
                    sync_map_path=root_path / "missing-sync-map.json",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=module.ProjectMetadata("Event", "Project"),
                    output_path=output,
                )
            probe.assert_not_called()
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_sync_map_loader_preserves_decimal_timing_and_rejects_drift(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "sync-map.json"
            source.write_text(
                json.dumps(sync_payload(), default=float),
                encoding="utf-8",
            )
            loaded = module.load_sync_map(source)
            self.assertIsInstance(
                loaded["pairs"][0]["offsetBFromASeconds"],
                Decimal,
            )
            changed = sync_payload()
            changed["schemaVersion"] = "tritrack.sync-map/v2"
            source.write_text(json.dumps(changed, default=float), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_SYNC_MAP_INVALID"):
                module.load_sync_map(source)


if __name__ == "__main__":
    unittest.main()
