"""Task 4 tests for the fail-closed environment doctor."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tritrack_editing_assistant import cli, doctor


class FakeProbe:
    def __init__(self) -> None:
        self.system = "Darwin"
        self.macos_version = "26.5.2"
        self.architecture = "arm64"
        self.python_version = "3.13.15"
        self.final_cut_version = "12.3"
        self.executables = {
            "ffmpeg": "ffmpeg version 7.1",
            "ffprobe": "ffprobe version 7.1",
            "xmllint": "/usr/bin/xmllint: using libxml version 21107",
            "whisper-cli": "whisper.cpp version 1.9.1",
        }
        self.dtd_present = True
        self.free_disk_bytes = 20_000_000_000
        self.readable_paths: set[Path] = set()

    def executable_version(self, name: str) -> str | None:
        return self.executables.get(name)

    def final_cut_dtd_present(self, _version: str) -> bool:
        return self.dtd_present

    def path_is_readable_file(self, path: Path) -> bool:
        return path in self.readable_paths


class DoctorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.probe = FakeProbe()

    def run_doctor(self, **overrides: object) -> dict[str, object]:
        arguments: dict[str, object] = {
            "profile_id": "uhd-2997-ndf-fcpxml-1.14",
            "probe": self.probe,
        }
        arguments.update(overrides)
        return doctor.build_receipt(**arguments)

    def check_code(self, receipt: dict[str, object], code: str) -> dict[str, object]:
        checks = receipt["checks"]
        assert isinstance(checks, list)
        return next(check for check in checks if check["code"] == code)

    def test_missing_ffmpeg_is_an_unsupported_dependency(self) -> None:
        self.probe.executables.pop("ffmpeg")

        receipt = self.run_doctor()

        self.assertFalse(receipt["supported"])
        self.assertEqual(self.check_code(receipt, "ffmpeg")["status"], "missing")

    def test_unsupported_os_fails_policy_without_guessing(self) -> None:
        self.probe.system = "Linux"

        receipt = self.run_doctor()

        self.assertFalse(receipt["supported"])
        self.assertEqual(
            self.check_code(receipt, "operating-system")["status"], "unsupported"
        )

    def test_unsupported_macos_and_final_cut_versions_fail_policy(self) -> None:
        self.probe.macos_version = "26.6"
        self.probe.final_cut_version = "12.4"

        receipt = self.run_doctor()

        self.assertFalse(receipt["supported"])
        self.assertEqual(
            self.check_code(receipt, "macos-version")["status"], "unsupported"
        )
        self.assertEqual(self.check_code(receipt, "final-cut")["status"], "unsupported")

    def test_unknown_profile_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "TRITRACK_PROFILE_UNKNOWN"):
            self.run_doctor(profile_id="some-other-profile")

    def test_missing_dtd_is_an_unsupported_dependency(self) -> None:
        self.probe.dtd_present = False

        receipt = self.run_doctor()

        self.assertFalse(receipt["supported"])
        self.assertEqual(self.check_code(receipt, "fcpxml-dtd")["status"], "missing")

    def test_existing_output_is_rejected_before_probe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "doctor.json"
            output.write_text("existing", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                doctor.write_receipt(
                    output,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    probe=self.probe,
                )

    def test_transcription_requires_a_readable_whisper_model(self) -> None:
        receipt = self.run_doctor(
            transcription_requested=True,
            whisper_model=Path("/Users/editor/private/model.bin"),
        )

        self.assertFalse(receipt["supported"])
        self.assertEqual(
            self.check_code(receipt, "whisper-model")["status"], "unreadable"
        )

    def test_transcription_requires_the_whisper_executable(self) -> None:
        self.probe.executables.pop("whisper-cli")
        model = Path("model.bin")
        self.probe.readable_paths.add(model)

        receipt = self.run_doctor(
            transcription_requested=True,
            whisper_model=model,
        )

        self.assertFalse(receipt["supported"])
        self.assertEqual(self.check_code(receipt, "whisper-cli")["status"], "missing")

    def test_insufficient_free_disk_is_unsupported(self) -> None:
        self.probe.free_disk_bytes = 0

        receipt = self.run_doctor()

        self.assertFalse(receipt["supported"])
        self.assertEqual(
            self.check_code(receipt, "free-disk")["status"], "insufficient"
        )

    def test_receipt_json_omits_paths_filenames_and_credentials(self) -> None:
        receipt = self.run_doctor(
            transcription_requested=True,
            whisper_model=Path("/Users/editor/Secret/model.bin"),
        )

        encoded = json.dumps(receipt, ensure_ascii=False)
        self.assertNotIn("/Users/", encoded)
        self.assertNotIn("/usr/bin/", encoded)
        self.assertNotIn("model.bin", encoded)
        self.assertNotIn("Secret", encoded)
        self.assertEqual(receipt["schemaVersion"], "tritrack.doctor-receipt/v1")

    @unittest.skipUnless(
        sys.platform == "darwin",
        "requires the declared local Final Cut and FCPXML DTD environment",
    )
    def test_cli_doctor_emits_the_real_supported_receipt(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            returncode = cli.main(
                [
                    "doctor",
                    "--profile",
                    "uhd-2997-ndf-fcpxml-1.14",
                    "--json",
                ]
            )

        payload = json.loads(output.getvalue())
        self.assertEqual(returncode, cli.EXIT_OK)
        self.assertTrue(payload["supported"])
        self.assertEqual(payload["schemaVersion"], "tritrack.doctor-receipt/v1")


if __name__ == "__main__":
    unittest.main()
