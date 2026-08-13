"""Task 4 tests for packaged public profiles and Basic Title capture."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from tritrack_editing_assistant import doctor

SCRIPT = Path(__file__).parents[1] / "scripts" / "capture_basic_title_binding.py"


def load_capture_module():
    spec = importlib.util.spec_from_file_location("capture_basic_title_binding", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("capture script loader unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAFE_FCPXML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.14">
  <resources>
    <effect id="r2" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>
    <format id="r1" name="FFVideoFormat3840x2160p2997" frameDuration="1001/30000s" width="3840" height="2160" colorSpace="1-1-1 (Rec. 709)"/>
  </resources>
  <library><event name="Invented"><project name="Invented Basic Title"><sequence format="r1" duration="3003/30000s" tcFormat="NDF"><spine>
    <title name="Invented subtitle" ref="r2" offset="0s" start="0s" duration="3003/30000s">
      <text><text-style ref="ts1">Invented subtitle</text-style></text>
      <text-style-def id="ts1"><text-style font="Helvetica" fontSize="72" fontFace="Regular" fontColor="1 1 1 1" alignment="center"/></text-style-def>
    </title>
  </spine></sequence></project></event></library>
</fcpxml>
"""


class TitleBindingTest(unittest.TestCase):
    def test_packaged_compatibility_profile_has_exact_alpha_values(self) -> None:
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        self.assertEqual(profile["schemaVersion"], "tritrack.compatibility-profile/v1")
        self.assertEqual(profile["frameDuration"], "1001/30000s")
        self.assertEqual((profile["width"], profile["height"]), (3840, 2160))
        self.assertEqual(profile["timecodeFormat"], "NDF")
        self.assertEqual(profile["audioRate"], 48000)

    def test_packaged_basic_title_binding_validates(self) -> None:
        binding = doctor.load_title_binding("basic-title-v1")
        self.assertEqual(binding["schemaVersion"], "tritrack.title-binding/v1")
        self.assertEqual(binding["effectName"], "Basic Title")
        self.assertTrue(binding["effectUid"].endswith("Basic Title.moti"))

    def test_capture_extracts_only_public_effect_and_style_values(self) -> None:
        capture = load_capture_module()
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "invented.fcpxml"
            source.write_text(SAFE_FCPXML, encoding="utf-8")

            binding = capture.capture_binding(source)

        self.assertEqual(binding["effectName"], "Basic Title")
        self.assertEqual(
            {parameter["name"] for parameter in binding["parameters"]},
            {"alignment", "font", "fontColor", "fontFace", "fontSize"},
        )
        self.assertNotIn("Invented subtitle", json.dumps(binding))

    def test_capture_rejects_doctype_subsets_and_entities(self) -> None:
        capture = load_capture_module()
        source_xml = SAFE_FCPXML.replace(
            "<!DOCTYPE fcpxml>",
            '<!DOCTYPE fcpxml [<!ENTITY private SYSTEM "file:///etc/passwd">]>',
        )
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "entity.fcpxml"
            source.write_text(source_xml, encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TITLE_BINDING_INVALID_XML"
            ):
                capture.capture_binding(source)

    def test_rendered_basic_title_roundtrips_through_public_binding(self) -> None:
        capture = load_capture_module()
        binding = doctor.load_title_binding("basic-title-v1")
        rendered = capture.render_basic_title_fcpxml(
            binding,
            text="TRITRACK GENERATED BASIC TITLE",
        )

        self.assertIn('<fcpxml version="1.14">', rendered)
        self.assertIn('frameDuration="1001/30000s"', rendered)
        self.assertIn('tcFormat="NDF"', rendered)
        self.assertIn('duration="180180/30000s"', rendered)
        self.assertEqual(rendered.count('duration="90090/30000s"'), 2)
        self.assertIn('offset="90090/30000s"', rendered)
        self.assertNotIn('duration="3s"', rendered)
        self.assertNotIn("src=", rendered)

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "generated.fcpxml"
            source.write_text(rendered, encoding="utf-8")
            recaptured = capture.capture_binding(source)

        self.assertEqual(recaptured, binding)

    def test_capture_rejects_private_title_font_path_and_template(self) -> None:
        capture = load_capture_module()
        forbidden_variants = (
            SAFE_FCPXML.replace("Basic Title", "Artlist LT", 1),
            SAFE_FCPXML.replace("Helvetica", "江城知音体"),
            SAFE_FCPXML.replace(
                ".../Titles.localized",
                "/Users/editor/Movies/Motion Templates/Titles.localized",
            ),
            SAFE_FCPXML.replace(
                '<title name="Invented subtitle"',
                '<title src="relative/private.mov" name="Invented subtitle"',
            ),
            SAFE_FCPXML.replace("Basic Title.moti", "Transcription Template.moti"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            for index, xml in enumerate(forbidden_variants):
                with self.subTest(index=index):
                    source = Path(temporary) / f"forbidden-{index}.fcpxml"
                    source.write_text(xml, encoding="utf-8")
                    with self.assertRaisesRegex(
                        ValueError, "TRITRACK_TITLE_BINDING_FORBIDDEN"
                    ):
                        capture.capture_binding(source)


if __name__ == "__main__":
    unittest.main()
