"""Task 11 maintainer release-gate tests."""

from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import os
import stat
import subprocess
import tarfile
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock

from scripts import release_gate_core


def _policy(*, wheel: list[str] | None = None, sdist: list[str] | None = None):
    return {
        "schemaVersion": "tritrack.package-policy/v1",
        "limits": {
            "sourceMaxFiles": 32,
            "sourceMaxFileBytes": 4096,
            "sourceMaxTotalBytes": 32768,
            "archiveMaxBytes": 65536,
            "archiveMaxMembers": 32,
            "memberMaxBytes": 4096,
            "expandedMaxBytes": 32768,
        },
        "source": {
            "allowedFakeHomeUsers": ["editor", "example", "fake", "test"],
            "allowedFakeSecretValues": [
                "example",
                "fake",
                "placeholder",
                "redacted",
                "secret",
                "test",
            ],
            "forbiddenSuffixes": [".mov", ".xlsx"],
        },
        "wheel": {"expectedMembers": wheel or ["demo.py"]},
        "sdist": {
            "root": "demo-1.0/",
            "expectedMembers": sdist or ["README.md"],
        },
    }


def _run(*argv: str, cwd: Path, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        argv,
        cwd=cwd,
        input=input_bytes,
        check=True,
        capture_output=True,
    ).stdout


def _make_repo(root: Path, files: dict[str, bytes] | None = None) -> None:
    (root / "release").mkdir(parents=True)
    (root / "release" / "package-policy-v1.json").write_text(
        json.dumps(_policy()), encoding="utf-8"
    )
    for name, encoded in (files or {"public.txt": b"public\n"}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encoded)
    _run("git", "init", "-q", cwd=root)
    _run("git", "config", "user.name", "Invented Tester", cwd=root)
    _run("git", "config", "user.email", "test@example.invalid", cwd=root)
    _run("git", "add", ".", cwd=root)
    _run("git", "commit", "-qm", "fixture", cwd=root)


def _zip(path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]) -> None:
    with (
        zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive,
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore", UserWarning)
        for name, encoded in entries:
            archive.writestr(name, encoded)


def _tar(
    path: Path,
    entries: list[tuple[tarfile.TarInfo | str, bytes]],
) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name, encoded in entries:
            member = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
            if member.isreg():
                member.size = len(encoded)
            archive.addfile(member, io.BytesIO(encoded) if member.isreg() else None)


class SourceGateTest(unittest.TestCase):
    def test_clean_stage_zero_regular_source_is_inventory_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            first = release_gate_core.inventory_tracked_source(root)
            second = release_gate_core.inventory_tracked_source(root)
        self.assertEqual(first, second)
        self.assertEqual(first.count, 2)
        self.assertEqual(len(first.sha256), 64)
        self.assertGreater(first.total_bytes, 0)

    def test_dirty_source_and_tracked_links_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_DIRTY$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").unlink()
            os.symlink("target", root / "public.txt")
            _run("git", "add", "public.txt", cwd=root)
            _run("git", "commit", "-qm", "link", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_submodule_unmerged_and_late_change_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            head = _run("git", "rev-parse", "HEAD", cwd=root).strip().decode()
            _run(
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{head},nested",
                cwd=root,
            )
            _run("git", "commit", "-qm", "gitlink", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            original = release_gate_core._read_regular
            changed = False

            def mutate(path: Path, limit: int) -> bytes:
                nonlocal changed
                encoded = original(path, limit)
                if path.name == "public.txt" and not changed:
                    changed = True
                    path.write_text("late change\n", encoding="utf-8")
                return encoded

            with (
                mock.patch.object(
                    release_gate_core, "_read_regular", side_effect=mutate
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_SOURCE_CHANGED$",
                ),
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_source_bounds_and_forbidden_suffix_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"clip.mov": b"invented"})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE$",
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"large.txt": b"x" * 5000})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_LIMIT$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_privacy_scanner_redacts_paths_and_credentials(self) -> None:
        private_home = b"/" + b"Users" + b"/real-person/project"
        credential = b"API" + b"_KEY=" + b"A" * 36
        private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
        for encoded in (private_home, credential, private_key):
            with self.subTest(kind=hashlib.sha256(encoded).hexdigest()[:8]):
                with self.assertRaises(release_gate_core.ReleaseGateError) as caught:
                    release_gate_core.scan_public_bytes(encoded)
                message = str(caught.exception)
                self.assertRegex(message, r"^TRITRACK_RELEASE_[A-Z_]+$")
                self.assertNotIn(encoded.decode(), message)

        for public in (
            b"/Users/editor/invented",
            b"/home/example/demo",
            b"password=placeholder",
            b"secret=test",
        ):
            release_gate_core.scan_public_bytes(public)


class ArchiveGateTest(unittest.TestCase):
    def test_safe_wheel_and_sdist_return_only_counts_and_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            _zip(wheel, [("demo.py", b"print('public')\n")])
            _tar(sdist, [("demo-1.0/README.md", b"public\n")])
            wheel_result = release_gate_core.inspect_wheel(wheel, _policy())
            sdist_result = release_gate_core.inspect_sdist(sdist, _policy())
        for result in (wheel_result, sdist_result):
            self.assertEqual(result.member_count, 1)
            self.assertEqual(len(result.sha256), 64)
            self.assertEqual(len(result.member_inventory_sha256), 64)
            self.assertNotIn("demo", repr(result))

    def test_zip_rejects_traversal_duplicates_casefold_links_and_encryption(self) -> None:
        fixtures: list[tuple[list[tuple[zipfile.ZipInfo | str, bytes]], dict]] = []
        fixtures.append(([("../demo.py", b"x")], _policy(wheel=["../demo.py"])))
        fixtures.append(
            (
                [("demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["demo.py"]),
            )
        )
        fixtures.append(
            (
                [("Demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["Demo.py", "demo.py"]),
            )
        )
        link = zipfile.ZipInfo("demo.py")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        fixtures.append(([(link, b"target")], _policy()))

        for entries, policy in fixtures:
            with self.subTest(size=len(entries)), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "bad.whl"
                _zip(path, entries)
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_wheel(path, policy)

        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "encrypted.whl"
            _zip(path, [("demo.py", b"x")])
            encoded = bytearray(path.read_bytes())
            local = encoded.find(b"PK\x03\x04")
            central = encoded.find(b"PK\x01\x02")
            encoded[local + 6] |= 1
            encoded[central + 8] |= 1
            path.write_bytes(encoded)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_ENCRYPTED$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

    def test_tar_rejects_wrong_root_links_and_unexpected_members(self) -> None:
        link = tarfile.TarInfo("demo-1.0/README.md")
        link.type = tarfile.SYMTYPE
        link.linkname = "target"
        fixtures = (
            ([("other/README.md", b"x")], _policy(sdist=["README.md"])),
            ([(link, b"")], _policy()),
            (
                [("demo-1.0/README.md", b"x"), ("demo-1.0/extra", b"x")],
                _policy(),
            ),
        )
        for entries, policy in fixtures:
            with self.subTest(), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "bad.tar.gz"
                _tar(path, list(entries))
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_sdist(path, policy)

    def test_archive_bounds_privacy_and_inventory_mode_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "large.whl"
            _zip(path, [("demo.py", b"x" * 5000)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_LIMIT$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            private_home = b"/" + b"home" + b"/real-person/private"
            _zip(path, [("demo.py", private_home)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_PRIVATE_PATH$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            executable = zipfile.ZipInfo("demo.py")
            executable.create_system = 3
            executable.external_attr = (stat.S_IFREG | 0o755) << 16
            _zip(path, [(executable, b"public\n")])
            first = release_gate_core.inspect_wheel(path, _policy())
            regular = zipfile.ZipInfo("demo.py")
            regular.create_system = 3
            regular.external_attr = (stat.S_IFREG | 0o644) << 16
            _zip(path, [(regular, b"public\n")])
            second = release_gate_core.inspect_wheel(path, _policy())
            self.assertNotEqual(
                first.member_inventory_sha256,
                second.member_inventory_sha256,
            )


class OrchestrationTest(unittest.TestCase):
    def test_build_uses_fixed_epoch_and_exact_local_toolchain(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot"
            snapshot.mkdir()
            output = root / "dist"

            def fake_command(argv, **_kwargs):
                calls.append(tuple(str(value) for value in argv))
                output.mkdir(exist_ok=True)
                (output / "demo-1.0-py3-none-any.whl").write_bytes(b"wheel")
                (output / "demo-1.0.tar.gz").write_bytes(b"sdist")
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_installed_tool_versions",
                    return_value={
                        "pip": "26.2",
                        "build": "1.5.0",
                        "setuptools": "84.0.0",
                        "wheel": "0.48.0",
                    },
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                wheel, sdist = release_gate_core.build_distributions(
                    snapshot, output, epoch=1704067200
                )

        self.assertEqual(wheel.name, "demo-1.0-py3-none-any.whl")
        self.assertEqual(sdist.name, "demo-1.0.tar.gz")
        self.assertEqual(
            calls,
            [
                (
                    os.fspath(Path(os.sys.executable)),
                    "-m",
                    "build",
                    "--no-isolation",
                    "--outdir",
                    os.fspath(output),
                )
            ],
        )

    def test_fresh_install_uses_only_local_wheel_and_smokes_all_help(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
            wheel.write_bytes(b"invented wheel")

            def fake_command(argv, **_kwargs):
                normalized = tuple(str(value) for value in argv)
                calls.append(normalized)
                if normalized[-2:] == ("components", "--json"):
                    return json.dumps(
                        {
                            "schemaVersion": "tritrack.components/v1",
                            "components": [{}] * 11,
                        }
                    ).encode()
                if "importlib.metadata" in " ".join(normalized):
                    return b"tritrack-editing-assistant\t0.1.0a0\n"
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_wheel_project_identity",
                    return_value=("tritrack-editing-assistant", "0.1.0a0"),
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                release_gate_core.fresh_install_smoke(wheel, root / "smoke")

        flattened = [" ".join(call) for call in calls]
        install = [
            call
            for call in flattened
            if "pip" in call.split() and "install" in call.split()
        ]
        self.assertTrue(any("pip==26.2" in call for call in install))
        self.assertTrue(any(os.fspath(wheel) in call for call in install))
        self.assertFalse(any("-e" in call.split() for call in install))
        for mode in ("contract", "fcpxml", "paper", "run"):
            self.assertTrue(
                any(f"validate {mode} --help" in call for call in flattened), mode
            )

    def test_manifest_is_closed_deterministic_and_schema_valid(self) -> None:
        inspection = release_gate_core.DistributionInspection(
            sha256="c" * 64,
            size_bytes=10,
            member_count=2,
            member_inventory_sha256="d" * 64,
        )
        context = release_gate_core.ReleaseContext(
            project_name="tritrack-editing-assistant",
            version="0.1.0a0",
            commit="a" * 40,
            source_inventory=release_gate_core.SourceInventory(
                count=3,
                total_bytes=30,
                sha256="b" * 64,
                commit="a" * 40,
            ),
            toolchain={
                "pip": "26.2",
                "build": "1.5.0",
                "setuptools": "84.0.0",
                "wheel": "0.48.0",
            },
            python_version="3.13.15",
            implementation="CPython",
            system="Darwin",
            machine="arm64",
            wheel=inspection,
            sdist=inspection,
        )
        first = release_gate_core.build_release_manifest(context)
        second = release_gate_core.build_release_manifest(context)
        self.assertEqual(first, second)
        self.assertEqual(
            set(first),
            {
                "schemaVersion",
                "project",
                "sourceInventory",
                "toolchain",
                "platform",
                "artifacts",
                "reproducibility",
                "gates",
                "nonClaims",
            },
        )
        serialized = json.dumps(first, sort_keys=True)
        for forbidden in ("path", "time", "duration", "command", "log", "content"):
            self.assertNotIn(forbidden, serialized.casefold())

    def test_pipeline_failure_never_calls_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(
                    release_gate_core,
                    "inventory_tracked_source",
                    side_effect=release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_SOURCE_DIRTY"
                    ),
                ),
                mock.patch.object(release_gate_core, "publish_release") as publish,
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.run_release_gate(root, root / "absent")
            publish.assert_not_called()


class PublicationTest(unittest.TestCase):
    def test_artifacts_are_linked_before_manifest_and_existing_output_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            release_gate_core.publish_release(output, wheel, sdist, b"{}\n")
            self.assertEqual((output / wheel.name).read_bytes(), b"wheel")
            self.assertEqual((output / sdist.name).read_bytes(), b"sdist")
            self.assertEqual((output / "release-manifest.json").read_bytes(), b"{}\n")

            sentinel = root / "existing"
            sentinel.mkdir()
            (sentinel / "keep").write_text("untouched", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_OUTPUT_EXISTS$",
            ):
                release_gate_core.publish_release(sentinel, wheel, sdist, b"{}\n")
            self.assertEqual((sentinel / "keep").read_text(), "untouched")

    def test_interruption_before_last_link_leaves_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            real_link = os.link
            calls = 0

            def interrupted(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_INTERRUPTED"
                    )
                real_link(source, destination)

            with (
                mock.patch.object(
                    release_gate_core, "_link_file", side_effect=interrupted
                ),
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.publish_release(output, wheel, sdist, b"{}\n")
            self.assertTrue(output.is_dir())
            self.assertFalse((output / "release-manifest.json").exists())


class ReleaseCliTest(unittest.TestCase):
    def test_cli_success_prints_only_bounded_receipt_facts(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        manifest = {
            "project": {"commit": "a" * 40, "version": "0.1.0a0"},
            "artifacts": {
                "wheel": {"sha256": "b" * 64},
                "sdist": {"sha256": "c" * 64},
            },
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                return_value=manifest,
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", "invented-source", "--output", "invented-output"]
            )
        self.assertEqual(result, 0)
        self.assertEqual(stderr.getvalue(), "")
        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "RELEASE_GATE\tPASS")
        self.assertEqual(len(lines), 6)
        self.assertFalse(any("invented" in line for line in lines))

    def test_cli_usage_and_gate_failures_are_json_codes_only(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = release_gate.main([])
        self.assertEqual(result, 64)
        self.assertEqual(
            json.loads(stderr.getvalue()), {"error": "TRITRACK_RELEASE_USAGE"}
        )

        stderr = io.StringIO()
        private = "/" + "Users" + "/real-person/private"
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                side_effect=release_gate_core.ReleaseGateError(
                    "TRITRACK_RELEASE_PRIVATE_PATH"
                ),
            ),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", private, "--output", "invented-output"]
            )
        self.assertEqual(result, 1)
        self.assertEqual(
            json.loads(stderr.getvalue()),
            {"error": "TRITRACK_RELEASE_PRIVATE_PATH"},
        )
        self.assertNotIn(private, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
