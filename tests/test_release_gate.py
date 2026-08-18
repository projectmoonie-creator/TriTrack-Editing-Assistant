"""Task 11 maintainer release-gate tests."""

from __future__ import annotations

import hashlib
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


if __name__ == "__main__":
    unittest.main()
