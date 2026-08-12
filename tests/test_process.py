import gc
import json
import sys
import tempfile
import time
import unittest
import warnings
from pathlib import Path

from tritrack_editing_assistant import process


class SanitizedReceiptTest(unittest.TestCase):
    def test_receipt_redacts_paths_and_environment_values(self):
        private_home = Path("/").joinpath("Users", "editor", "Secret", "C0001.MP4")
        receipt = process.sanitized_receipt(
            command=["ffprobe", str(private_home)],
            environment={"GEMINI_API_KEY": "secret"},
            returncode=1,
        )
        encoded = json.dumps(receipt)
        self.assertNotIn(str(private_home.parent.parent), encoded)
        self.assertNotIn("C0001.MP4", encoded)
        self.assertNotIn("secret", encoded)
        self.assertEqual(receipt["executable"], "ffprobe")
        self.assertEqual(receipt["argumentCount"], 1)

    def test_output_path_must_be_absent_including_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            existing = root / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                process.require_absent_output(existing)

            dangling = root / "dangling"
            dangling.symlink_to(root / "missing")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                process.require_absent_output(dangling)

            self.assertEqual(
                process.require_absent_output(root / "new-output"),
                root / "new-output",
            )


class BoundedProcessTest(unittest.TestCase):
    def test_success_returns_raw_output_separate_from_sanitized_receipt(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ResourceWarning)
            result = process.run_bounded(
                [sys.executable, "-c", "print('ready')"],
                timeout_seconds=2,
                max_captured_bytes=1024,
                environment={},
            )
            gc.collect()
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"ready\n")
        self.assertNotIn("ready", json.dumps(result.receipt))
        self.assertEqual(
            [warning for warning in caught if warning.category is ResourceWarning],
            [],
        )

    def test_string_command_is_rejected_instead_of_using_a_shell(self):
        with self.assertRaisesRegex(TypeError, "TRITRACK_PROCESS_COMMAND_INVALID"):
            process.run_bounded(
                "printf unsafe",  # type: ignore[arg-type]
                timeout_seconds=1,
                max_captured_bytes=100,
                environment={},
            )

    def test_non_allowlisted_environment_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_PROCESS_ENVIRONMENT_NOT_ALLOWED"
        ):
            process.run_bounded(
                [sys.executable, "-c", "pass"],
                timeout_seconds=1,
                max_captured_bytes=100,
                environment={"GEMINI_API_KEY": "secret"},
            )

    def test_timeout_terminates_the_entire_process_group(self):
        with tempfile.TemporaryDirectory() as temporary:
            marker = Path(temporary) / "orphan-ran"
            child = (
                "import pathlib,time;"
                "time.sleep(0.5);"
                f"pathlib.Path({str(marker)!r}).write_text('alive')"
            )
            parent = (
                "import subprocess,sys,time;"
                f"subprocess.Popen([sys.executable, '-c', {child!r}]);"
                "time.sleep(10)"
            )
            result = process.run_bounded(
                [sys.executable, "-c", parent],
                timeout_seconds=0.1,
                max_captured_bytes=1024,
                environment={},
            )
            self.assertEqual(result.status, "timeout")
            self.assertEqual(result.stdout, b"")
            self.assertEqual(result.stderr, b"")
            time.sleep(0.7)
            self.assertFalse(marker.exists(), "a grandchild escaped the process group")

    def test_oversized_output_is_killed_and_not_returned(self):
        result = process.run_bounded(
            [
                sys.executable,
                "-c",
                "import os,time; os.write(1, b'x' * 8192); time.sleep(10)",
            ],
            timeout_seconds=2,
            max_captured_bytes=64,
            environment={},
        )
        self.assertEqual(result.status, "output_limit_exceeded")
        self.assertEqual(result.stdout, b"")
        self.assertEqual(result.stderr, b"")
        self.assertNotIn("x" * 16, json.dumps(result.receipt))


if __name__ == "__main__":
    unittest.main()
