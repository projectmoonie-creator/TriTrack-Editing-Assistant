"""Task 6.5 public invented-media quickstart tests."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import random
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import (
    cli,
    contracts,
    doctor,
    emit_fcpxml,
    process,
    sync_scan,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "quickstart_demo.py"
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
PROFILE_ID = "uhd-2997-ndf-fcpxml-1.14"
BINDING_ID = "basic-title-v1"


def load_quickstart():
    if not EXAMPLE.is_file():
        raise AssertionError(
            "Task 6.5 requires examples/quickstart_demo.py as the public entry point"
        )
    specification = importlib.util.spec_from_file_location(
        "tritrack_quickstart_demo",
        EXAMPLE,
    )
    if specification is None or specification.loader is None:
        raise AssertionError("Task 6.5 quickstart entry point is not importable")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def compatible_probe(source: sync_scan.MediaSource, *, compatible: bool = True):
    return {
        "id": source.media_id,
        "duration_seconds": 4.0,
        "start": None,
        "has_audio": True,
        "compatibility": {
            "videoStreamCount": 1,
            "audioStreamCount": 1,
            "width": 3840 if compatible else 1920,
            "height": 2160,
            "frameRate": "30000/1001",
            "colorSpace": "bt709",
            "colorTransfer": "bt709",
            "colorPrimaries": "bt709",
            "sampleRate": "48000",
            "channels": 2,
        },
        "source": source,
    }


class InstalledSurfaceRunner:
    """Exercise the real CLI while replacing only external media processes."""

    def __init__(self, *, profile_compatible: bool = True) -> None:
        self.commands: list[tuple[str, ...]] = []
        self.emitted_bytes: list[bytes] = []
        self.profile_compatible = profile_compatible
        generator = random.Random(20260814)
        self.samples = tuple(generator.uniform(-1.0, 1.0) for _ in range(4_000))

    def __call__(
        self,
        command,
        *,
        timeout_seconds: float,
        max_captured_bytes: int,
        environment=None,
    ) -> process.ProcessResult:
        del timeout_seconds, max_captured_bytes, environment
        checked = tuple(str(argument) for argument in command)
        self.commands.append(checked)
        executable = Path(checked[0]).name
        if executable == "ffmpeg":
            Path(checked[-1]).write_bytes(b"invented-public-media")
            return self.result("ok", 0)
        if executable == "xmllint":
            return self.result("ok", 0)
        if executable != "tritrack":
            return self.result("failed", 127, stderr=b"unexpected executable")

        standard_output = io.StringIO()

        def probe(source):
            return compatible_probe(
                source,
                compatible=self.profile_compatible,
            )
        with (
            mock.patch.object(sync_scan, "probe_media", side_effect=probe),
            mock.patch.object(
                sync_scan,
                "extract_audio_samples",
                return_value=self.samples,
            ),
            contextlib.redirect_stdout(standard_output),
        ):
            returncode = cli.main(checked[1:])
        if checked[1] == "emit" and returncode == 0:
            output = Path(checked[checked.index("--output") + 1])
            self.emitted_bytes.append(output.read_bytes())
        return self.result(
            "ok" if returncode == 0 else "failed",
            returncode,
            stdout=standard_output.getvalue().encode("utf-8"),
        )

    @staticmethod
    def result(
        status: str,
        returncode: int,
        *,
        stdout: bytes = b"",
        stderr: bytes = b"",
    ) -> process.ProcessResult:
        return process.ProcessResult(status, returncode, stdout, stderr, {})


class QuickstartDemoTest(unittest.TestCase):
    def test_documented_one_command_quickstart_entry_point_exists(self) -> None:
        self.assertTrue(EXAMPLE.is_file(), "missing public quickstart entry point")
        self.assertTrue(WORKFLOW.is_file(), "missing release-grade public CI workflow")
        command = "venv/bin/python examples/quickstart_demo.py"
        self.assertIn(command, (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_invented_media_recipe_declares_complete_rec709_vui(self) -> None:
        quickstart = load_quickstart()
        command = quickstart._media_command(Path("invented.MP4"), color="black")
        self.assertIn("-x264-params", command)
        parameter_index = command.index("-x264-params")
        self.assertEqual(
            command[parameter_index + 1],
            "colorprim=bt709:transfer=bt709:colormatrix=bt709",
        )

    def test_invented_ab_run_uses_installed_sync_and_emit_and_validates_outputs(
        self,
    ) -> None:
        quickstart = load_quickstart()
        runner = InstalledSurfaceRunner()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dtd = root / "FCPXMLv1_14.dtd"
            dtd.write_text("invented unit seam", encoding="utf-8")
            output = root / "demo"
            report = quickstart.run_demo(
                output,
                tritrack_executable="tritrack",
                runner=runner,
                dtd_path=dtd,
            )

            sync_map = json.loads(
                (output / "results" / "sync-map.json").read_text(encoding="utf-8")
            )
            contracts.validate_contract("sync-map-v2", sync_map)
            self.assertEqual(sync_map["profileId"], PROFILE_ID)
            self.assertEqual(len(sync_map["groups"]), 1)
            xml_text = (output / "results" / "string-out.fcpxml").read_text(
                encoding="utf-8"
            )
            emit_fcpxml.validate_fcpxml(
                xml_text,
                profile=doctor.load_profile(PROFILE_ID),
                binding=doctor.load_title_binding(BINDING_ID),
            )

        command_names = [(Path(command[0]).name, command[1]) for command in runner.commands]
        self.assertIn(("tritrack", "sync"), command_names)
        self.assertEqual(command_names.count(("tritrack", "emit")), 2)
        self.assertIn(("xmllint", "--noout"), command_names)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["dtdValidation"], "passed")
        self.assertEqual(report["componentCount"], 11)

    def test_two_absent_emit_paths_are_byte_identical(self) -> None:
        quickstart = load_quickstart()
        runner = InstalledSurfaceRunner()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "demo"
            report = quickstart.run_demo(
                output,
                tritrack_executable="tritrack",
                runner=runner,
                dtd_path=None,
            )
            self.assertFalse(
                (output / "results" / ".determinism-check.fcpxml").exists()
            )

        self.assertEqual(len(runner.emitted_bytes), 2)
        self.assertEqual(runner.emitted_bytes[0], runner.emitted_bytes[1])
        self.assertTrue(report["deterministicFcpxml"])
        self.assertEqual(report["dtdValidation"], "not-available")

    def test_existing_output_root_and_publication_race_preserve_the_winner(
        self,
    ) -> None:
        quickstart = load_quickstart()
        runner = InstalledSurfaceRunner()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            existing = root / "existing"
            existing.mkdir()
            sentinel = existing / "winner.txt"
            sentinel.write_text("existing-winner", encoding="utf-8")
            with self.assertRaisesRegex(
                quickstart.DemoFailure,
                "TRITRACK_DEMO_OUTPUT_EXISTS",
            ):
                quickstart.run_demo(existing, runner=runner, dtd_path=None)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "existing-winner")

            raced = root / "raced"
            real_mkdir = os.mkdir

            def racing_mkdir(path, mode=0o777, *, dir_fd=None):
                real_mkdir(path, mode, dir_fd=dir_fd)
                (Path(path) / "winner.txt").write_text(
                    "race-winner",
                    encoding="utf-8",
                )
                raise FileExistsError(path)

            with (
                mock.patch.object(quickstart.os, "mkdir", side_effect=racing_mkdir),
                self.assertRaisesRegex(
                    quickstart.DemoFailure,
                    "TRITRACK_DEMO_OUTPUT_EXISTS",
                ),
            ):
                quickstart.run_demo(raced, runner=runner, dtd_path=None)
            self.assertEqual(
                (raced / "winner.txt").read_text(encoding="utf-8"),
                "race-winner",
            )

        self.assertEqual(runner.commands, [])

    def test_profile_incompatible_invented_media_is_rejected_not_normalized(
        self,
    ) -> None:
        quickstart = load_quickstart()
        runner = InstalledSurfaceRunner(profile_compatible=False)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "demo"
            with self.assertRaisesRegex(
                quickstart.DemoFailure,
                "TRITRACK_DEMO_EMIT_FAILED",
            ):
                quickstart.run_demo(
                    output,
                    tritrack_executable="tritrack",
                    runner=runner,
                    dtd_path=None,
                )
            self.assertTrue((output / "results" / "sync-map.json").is_file())
            self.assertFalse((output / "results" / "string-out.fcpxml").exists())

    def test_xml_sensitive_invented_metadata_is_escaped_end_to_end(self) -> None:
        quickstart = load_quickstart()
        runner = InstalledSurfaceRunner()
        event_name = 'Invented & Event <One> "safe"'
        project_name = "Invented > String-out & Cut"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "demo"
            quickstart.run_demo(
                output,
                tritrack_executable="tritrack",
                runner=runner,
                dtd_path=None,
                event_name=event_name,
                project_name=project_name,
            )
            xml_text = (output / "results" / "string-out.fcpxml").read_text(
                encoding="utf-8"
            )
        root = emit_fcpxml.ET.fromstring(xml_text)
        self.assertEqual(root.find("./library/event").attrib["name"], event_name)
        self.assertEqual(
            root.find("./library/event/project").attrib["name"],
            project_name,
        )
        self.assertIn("&amp;", xml_text)
        self.assertIn("&lt;", xml_text)

    def test_task_6_5_tracked_surface_is_public_safe_and_contains_no_outputs(
        self,
    ) -> None:
        load_quickstart()
        paths = (
            EXAMPLE,
            Path(__file__),
            WORKFLOW,
            ROOT / "README.md",
            ROOT / "docs" / "TOOLING.md",
        )
        forbidden = (
            "/" + "Users" + "/",
            "/" + "home" + "/",
            "TriTrack-" + "Subtitle-" + "Studio",
            "GEMINI_" + "API_KEY",
            "ANTHROPIC_" + "API_KEY",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path}: leaked {token!r}")

        tracked = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout.split(b"\0")
        generated_suffixes = {b".mp4", b".mov", b".fcpxml"}
        generated = [
            path
            for path in tracked
            if Path(os.fsdecode(path)).suffix.lower().encode() in generated_suffixes
        ]
        self.assertFalse(generated)


if __name__ == "__main__":
    unittest.main()
