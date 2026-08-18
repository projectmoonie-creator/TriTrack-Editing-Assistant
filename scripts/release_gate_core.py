"""Bounded, fail-closed primitives for the maintainer release gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import io
import json
import os
import platform
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unicodedata
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

import jsonschema

_COMMAND_TIMEOUT_SECONDS = 30
_COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
_POLICY_LIMIT = 1024 * 1024
_ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
_ALLOWED_FAKE_SECRETS = frozenset(
    {b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
)


class ReleaseGateError(Exception):
    """One stable public-safe release-gate failure code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class SourceInventory:
    count: int
    total_bytes: int
    sha256: str
    commit: str


@dataclass(frozen=True)
class DistributionInspection:
    sha256: str
    size_bytes: int
    member_count: int
    member_inventory_sha256: str


@dataclass(frozen=True)
class ReleaseContext:
    project_name: str
    version: str
    commit: str
    source_inventory: SourceInventory
    toolchain: Mapping[str, str]
    python_version: str
    implementation: str
    system: str
    machine: str
    wheel: DistributionInspection
    sdist: DistributionInspection


def _fail(code: str) -> None:
    raise ReleaseGateError(code)


def _safe_environment() -> dict[str, str]:
    return {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }


def _run_git(source: Path, *arguments: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=source,
            env=_safe_environment(),
            shell=False,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=_COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if result.returncode != 0:
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if len(result.stdout) > _COMMAND_OUTPUT_LIMIT:
        _fail("TRITRACK_RELEASE_GIT_LIMIT")
    return result.stdout


def _read_regular(path: Path, limit: int) -> bytes:
    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if details.st_size > limit:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        if len(encoded) > limit or len(encoded) != details.st_size:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    finally:
        os.close(descriptor)


def _mapping(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        _fail(code)
    return value


def _positive_limit(policy: Mapping[str, object], name: str) -> int:
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    value = limits.get(name)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return value


def _string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if len(value) != len(set(value)):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return tuple(value)


def _load_policy(source: Path) -> Mapping[str, object]:
    encoded = _read_regular(source / "release" / "package-policy-v1.json", _POLICY_LIMIT)
    try:
        policy = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    policy = _mapping(policy, "TRITRACK_RELEASE_POLICY_INVALID")
    if policy.get("schemaVersion") != "tritrack.package-policy/v1":
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if set(policy) != {"schemaVersion", "limits", "source", "wheel", "sdist"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected_limits = {
        "sourceMaxFiles",
        "sourceMaxFileBytes",
        "sourceMaxTotalBytes",
        "archiveMaxBytes",
        "archiveMaxMembers",
        "memberMaxBytes",
        "expandedMaxBytes",
    }
    if set(limits) != expected_limits:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    for name in expected_limits:
        _positive_limit(policy, name)

    source_policy = _mapping(
        policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(source_policy) != {
        "allowedFakeHomeUsers",
        "allowedFakeSecretValues",
        "forbiddenSuffixes",
    }:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    allowed_users = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeHomeUsers"))
    )
    allowed_secrets = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeSecretValues"))
    )
    if (
        allowed_users != _ALLOWED_FAKE_USERS
        or allowed_secrets != _ALLOWED_FAKE_SECRETS
    ):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(source_policy.get("forbiddenSuffixes"))

    wheel_policy = _mapping(
        policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(wheel_policy) != {"expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(wheel_policy.get("expectedMembers"))

    sdist_policy = _mapping(
        policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(sdist_policy) != {"root", "expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(sdist_policy.get("expectedMembers"))
    return policy


def _status(source: Path) -> bytes:
    return _run_git(
        source,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )


def _safe_source_path(encoded: bytes) -> str:
    try:
        name = encoded.decode("utf-8", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    candidate = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or candidate.is_absolute()
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    return name


def _parse_index(encoded: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for raw in encoded.split(b"\0"):
        if not raw:
            continue
        try:
            prefix, raw_path = raw.split(b"\t", 1)
            mode, object_id, stage = prefix.decode("ascii").split(" ")
        except (ValueError, UnicodeDecodeError):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        if stage != "0":
            _fail("TRITRACK_RELEASE_SOURCE_STAGE")
        if mode not in {"100644", "100755"}:
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        entries.append((_safe_source_path(raw_path), mode, object_id))
    if not entries:
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    if len({entry[0] for entry in entries}) != len(entries):
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    return entries


def _git_blob_hash(encoded: bytes, algorithm: str) -> str:
    if algorithm not in {"sha1", "sha256"}:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    digest = hashlib.new(algorithm)
    digest.update(f"blob {len(encoded)}\0".encode("ascii"))
    digest.update(encoded)
    return digest.hexdigest()


def _path_signature(path: Path) -> tuple[int, int, int, int]:
    try:
        details = path.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)


def _home_user_after(encoded: bytes, marker: bytes, separator: bytes) -> bytes | None:
    lowered = encoded.lower()
    offset = 0
    lowered_marker = marker.lower()
    while True:
        found = lowered.find(lowered_marker, offset)
        if found < 0:
            return None
        start = found + len(marker)
        end = start
        while end < len(encoded) and encoded[end : end + 1] not in (
            separator,
            b"/",
            b"\\",
            b"\0",
            b"\t",
            b"\r",
            b"\n",
            b" ",
            b'"',
            b"'",
        ):
            end += 1
        user = lowered[start:end]
        if user and user not in _ALLOWED_FAKE_USERS:
            return user
        offset = max(end, start + 1)


def scan_public_bytes(encoded: bytes) -> None:
    """Reject public-source privacy canaries without returning matched bytes."""

    mac_home = b"/" + b"Users" + b"/"
    linux_home = b"/" + b"home" + b"/"
    windows_home = b"\\" + b"Users" + b"\\"
    mounted_volume = b"/" + b"Volumes" + b"/"
    for marker, separator in (
        (mac_home, b"/"),
        (linux_home, b"/"),
        (windows_home, b"\\"),
    ):
        if _home_user_after(encoded, marker, separator) is not None:
            _fail("TRITRACK_RELEASE_PRIVATE_PATH")
    if mounted_volume.lower() in encoded.lower():
        _fail("TRITRACK_RELEASE_PRIVATE_PATH")

    private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
    rsa_private_key = b"-----BEGIN RSA " + b"PRIVATE KEY-----"
    if private_key in encoded or rsa_private_key in encoded:
        _fail("TRITRACK_RELEASE_PRIVATE_KEY")

    terms = (
        b"api" + b"[_-]?key",
        b"auth" + b"[_-]?token",
        b"access" + b"[_-]?token",
        b"password",
        b"passwd",
        b"secret",
    )
    assignment = re.compile(
        rb"(?im)\b(?:"
        + b"|".join(terms)
        + rb")\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+${}\-]{1,256})"
    )
    for match in assignment.finditer(encoded):
        value = match.group(1).rstrip(b"'\"").lower()
        if value not in _ALLOWED_FAKE_SECRETS:
            _fail("TRITRACK_RELEASE_CREDENTIAL")

    credential_shapes = (
        rb"\bgh" + rb"[pousr]_[A-Za-z0-9]{36,255}\b",
        rb"\bAK" + rb"IA[0-9A-Z]{16}\b",
        rb"\bAI" + rb"za[0-9A-Za-z_-]{35}\b",
        rb"\bxox" + rb"[baprs]-[0-9A-Za-z-]{20,255}\b",
    )
    if any(re.search(pattern, encoded) for pattern in credential_shapes):
        _fail("TRITRACK_RELEASE_CREDENTIAL")


def inventory_tracked_source(source: Path) -> SourceInventory:
    """Bind one clean Git index to the exact regular working-tree bytes."""

    source = source.resolve()
    policy = _load_policy(source)
    index_bytes = _run_git(source, "ls-files", "-s", "-z")
    entries = _parse_index(index_bytes)
    if _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_DIRTY")
    max_files = _positive_limit(policy, "sourceMaxFiles")
    max_file_bytes = _positive_limit(policy, "sourceMaxFileBytes")
    max_total_bytes = _positive_limit(policy, "sourceMaxTotalBytes")
    if len(entries) > max_files:
        _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
    source_policy = _mapping(policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID")
    suffixes = tuple(item.casefold() for item in _string_list(source_policy.get("forbiddenSuffixes")))
    object_format = _run_git(source, "rev-parse", "--show-object-format").strip()
    try:
        algorithm = object_format.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    commit_bytes = _run_git(source, "rev-parse", "HEAD").strip()
    try:
        commit = commit_bytes.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        _fail("TRITRACK_RELEASE_GIT_FAILED")

    total = 0
    inventory = hashlib.sha256()
    for name, mode, object_id in sorted(entries):
        if suffixes and name.casefold().endswith(suffixes):
            _fail("TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE")
        path = source / name
        before = _path_signature(path)
        if before[2] > max_file_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += before[2]
        if total > max_total_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        encoded = _read_regular(path, max_file_bytes)
        after = _path_signature(path)
        if before != after:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        if _git_blob_hash(encoded, algorithm) != object_id:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        scan_public_bytes(encoded)
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, mode, str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")

    if _run_git(source, "ls-files", "-s", "-z") != index_bytes or _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return SourceInventory(
        count=len(entries),
        total_bytes=total,
        sha256=inventory.hexdigest(),
        commit=commit,
    )


def _read_archive_bytes(path: Path, policy: Mapping[str, object]) -> bytes:
    limit = _positive_limit(policy, "archiveMaxBytes")
    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
        if not 0 < before.st_size <= limit:
            _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(encoded) > limit
            or len(encoded) != before.st_size
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        ):
            _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    finally:
        os.close(descriptor)


def _safe_member_name(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    normalized = unicodedata.normalize("NFC", name)
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    return normalized.rstrip("/")


def _bounded_archive_read(stream, expected: int, limit: int) -> bytes:
    if expected > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    encoded = stream.read(limit + 1)
    if len(encoded) != expected or len(encoded) > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    return encoded


def _member_digest(
    inventory: hashlib._Hash,
    name: str,
    member_type: str,
    mode: int,
    encoded: bytes,
) -> None:
    values = (
        name,
        member_type,
        f"{mode & 0o7777:o}",
        str(len(encoded)),
        hashlib.sha256(encoded).hexdigest(),
    )
    for value in values:
        inventory.update(value.encode("utf-8"))
        inventory.update(b"\0")
    inventory.update(b"\n")


def _check_collision(name: str, exact: set[str], folded: set[str]) -> None:
    if name in exact:
        _fail("TRITRACK_RELEASE_ARCHIVE_DUPLICATE")
    collision = unicodedata.normalize("NFC", name).casefold()
    if collision in folded:
        _fail("TRITRACK_RELEASE_ARCHIVE_COLLISION")
    exact.add(name)
    folded.add(collision)


def inspect_wheel(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a wheel without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    wheel_policy = _mapping(policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(wheel_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[zipfile.ZipInfo, str, int]] = []
    expanded = 0
    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            members = archive.infolist()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                name = _safe_member_name(member.filename)
                _check_collision(name, exact, folded)
                if member.flag_bits & 1:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ENCRYPTED")
                if member.is_dir():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                raw_mode = member.external_attr >> 16
                member_type = stat.S_IFMT(raw_mode)
                if member_type not in {0, stat.S_IFREG}:
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                expanded += member.file_size
                if member.file_size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, name, raw_mode))
            if {name for _, name, _ in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, raw_mode in sorted(files, key=lambda item: item[1]):
                with archive.open(member) as stream:
                    encoded = _bounded_archive_read(stream, member.file_size, max_member)
                scan_public_bytes(encoded)
                _member_digest(inventory, name, "file", raw_mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(files),
        member_inventory_sha256=inventory.hexdigest(),
    )


def inspect_sdist(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a gzipped source distribution without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    sdist_policy = _mapping(policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(sdist_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[tarfile.TarInfo, str]] = []
    all_members: list[tuple[tarfile.TarInfo, str, str]] = []
    expanded = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                full_name = _safe_member_name(member.name)
                if full_name == root.rstrip("/"):
                    relative = ""
                elif full_name.startswith(root):
                    relative = full_name[len(root) :]
                else:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ROOT")
                collision_name = relative or "."
                _check_collision(collision_name, exact, folded)
                if member.isdir():
                    all_members.append((member, relative, "directory"))
                    continue
                if not member.isreg():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                if not relative:
                    _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
                expanded += member.size
                if member.size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, relative))
                all_members.append((member, relative, "file"))
            if {name for _, name in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, member_type in sorted(all_members, key=lambda item: item[1]):
                if member_type == "directory":
                    encoded = b""
                else:
                    stream = archive.extractfile(member)
                    if stream is None:
                        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
                    with stream:
                        encoded = _bounded_archive_read(stream, member.size, max_member)
                    scan_public_bytes(encoded)
                _member_digest(inventory, name or ".", member_type, member.mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(all_members),
        member_inventory_sha256=inventory.hexdigest(),
    )


def _run_command(
    argv: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout: int = 300,
    output_limit: int = _COMMAND_OUTPUT_LIMIT,
) -> bytes:
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            env=dict(env),
            shell=False,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
    if result.returncode != 0:
        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
    if len(result.stdout) > output_limit or len(result.stderr) > output_limit:
        _fail("TRITRACK_RELEASE_COMMAND_LIMIT")
    return result.stdout


def _installed_tool_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("pip", "build", "setuptools", "wheel"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            _fail("TRITRACK_RELEASE_TOOLCHAIN")
    return versions


def _build_environment(epoch: int, temporary: Path) -> dict[str, str]:
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        _fail("TRITRACK_RELEASE_EPOCH")
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.defpath,
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": str(epoch),
        "TMPDIR": os.fspath(temporary),
    }
    return environment


def build_distributions(
    snapshot: Path, output: Path, *, epoch: int
) -> tuple[Path, Path]:
    """Build exactly one wheel and one sdist with the pinned local toolchain."""

    expected_tools = {
        "pip": "26.2",
        "build": "1.5.0",
        "setuptools": "84.0.0",
        "wheel": "0.48.0",
    }
    if _installed_tool_versions() != expected_tools:
        _fail("TRITRACK_RELEASE_TOOLCHAIN")
    if not snapshot.is_dir():
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    try:
        os.mkdir(output)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [
            os.fspath(Path(sys.executable)),
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            os.fspath(output),
        ],
        cwd=snapshot,
        env=_build_environment(epoch, output),
        timeout=300,
    )
    try:
        members = [
            child
            for child in output.iterdir()
            if child.is_file() and not child.is_symlink()
        ]
    except OSError:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    wheels = [child for child in members if child.suffix == ".whl"]
    sdists = [child for child in members if child.name.endswith(".tar.gz")]
    if len(members) != 2 or len(wheels) != 1 or len(sdists) != 1:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    return wheels[0], sdists[0]


def _wheel_project_identity(wheel: Path) -> tuple[str, str]:
    try:
        with zipfile.ZipFile(wheel) as archive:
            candidates = [
                member
                for member in archive.infolist()
                if member.filename.endswith(".dist-info/METADATA")
                and not member.is_dir()
            ]
            if len(candidates) != 1 or candidates[0].file_size > _POLICY_LIMIT:
                _fail("TRITRACK_RELEASE_WHEEL_METADATA")
            with archive.open(candidates[0]) as stream:
                encoded = _bounded_archive_read(
                    stream, candidates[0].file_size, _POLICY_LIMIT
                )
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    message = BytesParser().parsebytes(encoded)
    name = message.get("Name")
    version = message.get("Version")
    if not name or not version or "\n" in name or "\n" in version:
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    return name, version


def _install_environment(temporary: Path, binary: Path) -> dict[str, str]:
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.fspath(binary) + os.pathsep + os.defpath,
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PYTHONHASHSEED": "0",
        "TMPDIR": os.fspath(temporary),
    }
    for name in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "PIP_INDEX_URL",
        "PIP_TRUSTED_HOST",
    ):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    return environment


def fresh_install_smoke(wheel: Path, temporary: Path) -> None:
    """Install only the chosen local wheel into a new external environment."""

    project_name, project_version = _wheel_project_identity(wheel)
    if project_name != "tritrack-editing-assistant":
        _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
    try:
        os.mkdir(temporary)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [os.fspath(Path(sys.executable)), "-m", "venv", os.fspath(temporary)],
        cwd=temporary.parent,
        env=_build_environment(0, temporary),
        timeout=180,
    )
    if os.name == "nt":
        binary = temporary / "Scripts"
        python = binary / "python.exe"
        tritrack = binary / "tritrack.exe"
    else:
        binary = temporary / "bin"
        python = binary / "python"
        tritrack = binary / "tritrack"
    environment = _install_environment(temporary, binary)
    pip_base = [
        os.fspath(python),
        "-m",
        "pip",
        "--disable-pip-version-check",
        "--no-input",
    ]
    _run_command(
        [*pip_base, "install", "pip==26.2"],
        cwd=temporary,
        env=environment,
        timeout=300,
    )
    _run_command(
        [*pip_base, "install", os.fspath(wheel.resolve())],
        cwd=temporary,
        env=environment,
        timeout=600,
    )
    _run_command(
        [*pip_base, "check"], cwd=temporary, env=environment, timeout=120
    )
    metadata_code = (
        "import importlib.metadata as m; "
        "d=m.distribution('tritrack-editing-assistant'); "
        "print(d.metadata['Name']+'\\t'+d.version)"
    )
    installed = _run_command(
        [os.fspath(python), "-I", "-c", metadata_code],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    expected = f"{project_name}\t{project_version}\n".encode()
    if installed != expected:
        _fail("TRITRACK_RELEASE_INSTALLED_IDENTITY")
    components = _run_command(
        [os.fspath(tritrack), "components", "--json"],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    try:
        component_summary = json.loads(components.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    if (
        not isinstance(component_summary, Mapping)
        or component_summary.get("schemaVersion") != "tritrack.components/v1"
        or not isinstance(component_summary.get("components"), list)
        or len(component_summary["components"]) != 11
    ):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    for arguments in (
        ("validate", "--help"),
        ("validate", "contract", "--help"),
        ("validate", "fcpxml", "--help"),
        ("validate", "paper", "--help"),
        ("validate", "run", "--help"),
    ):
        _run_command(
            [os.fspath(tritrack), *arguments],
            cwd=temporary,
            env=environment,
            timeout=60,
        )


def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
    """Build and validate the deterministic, closed public release receipt."""

    manifest: dict[str, object] = {
        "schemaVersion": "tritrack.release-manifest/v1",
        "project": {
            "name": context.project_name,
            "version": context.version,
            "commit": context.commit,
        },
        "sourceInventory": {
            "count": context.source_inventory.count,
            "sha256": context.source_inventory.sha256,
        },
        "toolchain": {
            "python": context.python_version,
            "implementation": context.implementation,
            "pip": context.toolchain["pip"],
            "build": context.toolchain["build"],
            "setuptools": context.toolchain["setuptools"],
            "wheel": context.toolchain["wheel"],
        },
        "platform": {"system": context.system, "machine": context.machine},
        "artifacts": {
            "wheel": {
                "sha256": context.wheel.sha256,
                "sizeBytes": context.wheel.size_bytes,
                "memberCount": context.wheel.member_count,
                "memberInventorySha256": context.wheel.member_inventory_sha256,
            },
            "sdist": {
                "sha256": context.sdist.sha256,
                "sizeBytes": context.sdist.size_bytes,
                "memberCount": context.sdist.member_count,
                "memberInventorySha256": context.sdist.member_inventory_sha256,
            },
        },
        "reproducibility": {
            "wheelBytesMatch": True,
            "sdistMembersMatch": True,
        },
        "gates": {
            "sourceIdentity": "pass",
            "sourcePrivacy": "pass",
            "wheelArchive": "pass",
            "sdistArchive": "pass",
            "freshInstall": "pass",
        },
        "nonClaims": [
            "no-tag",
            "no-release",
            "no-package-publication",
            "no-pull-request",
            "no-tester-contact",
            "no-signing",
            "no-attestation",
            "no-sbom",
            "no-final-cut-gui",
            "no-dtd",
            "no-provider",
            "no-application-submission",
        ],
    }
    schema_path = Path(__file__).resolve().parents[1] / "release" / "release-manifest-v1.schema.json"
    try:
        schema = json.loads(_read_regular(schema_path, _POLICY_LIMIT).decode("utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(manifest, schema)
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    return manifest


def _link_file(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination, follow_symlinks=False)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _publication_artifacts(manifest: bytes) -> dict[str, tuple[int, str]]:
    if not 0 < len(manifest) <= _POLICY_LIMIT:
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    try:
        payload = _mapping(
            json.loads(manifest.decode("utf-8", errors="strict")),
            "TRITRACK_RELEASE_MANIFEST_INVALID",
        )
        artifacts = _mapping(
            payload.get("artifacts"), "TRITRACK_RELEASE_MANIFEST_INVALID"
        )
        result: dict[str, tuple[int, str]] = {}
        for kind in ("wheel", "sdist"):
            artifact = _mapping(
                artifacts.get(kind), "TRITRACK_RELEASE_MANIFEST_INVALID"
            )
            size = artifact.get("sizeBytes")
            digest = artifact.get("sha256")
            if (
                not isinstance(size, int)
                or isinstance(size, bool)
                or size < 1
                or not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
            result[kind] = (size, digest)
        return result
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")


def _verify_published_archive(path: Path, expected: tuple[int, str]) -> None:
    expected_size, expected_sha256 = expected
    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            details = os.fstat(descriptor)
            if not stat.S_ISREG(details.st_mode) or details.st_size != expected_size:
                _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
            digest = hashlib.sha256()
            observed_size = 0
            while observed_size <= expected_size:
                chunk = os.read(
                    descriptor,
                    min(1024 * 1024, expected_size + 1 - observed_size),
                )
                if not chunk:
                    break
                observed_size += len(chunk)
                digest.update(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
    if (
        observed_size != expected_size
        or digest.hexdigest() != expected_sha256
        or (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    ):
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")


def publish_release(
    output: Path, wheel: Path, sdist: Path, manifest: bytes
) -> None:
    """Publish two archives first and the canonical success manifest last."""

    if (
        wheel.name in {"", ".", "..", "release-manifest.json"}
        or sdist.name in {"", ".", "..", "release-manifest.json"}
        or wheel.name != os.path.basename(wheel.name)
        or sdist.name != os.path.basename(sdist.name)
        or wheel.name == sdist.name
    ):
        _fail("TRITRACK_RELEASE_PUBLISH")
    expected_artifacts = _publication_artifacts(manifest)
    try:
        parent_details = output.parent.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    if not stat.S_ISDIR(parent_details.st_mode):
        _fail("TRITRACK_RELEASE_OUTPUT")

    temporary_manifest: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=wheel.parent,
            prefix=".release-manifest-",
            delete=False,
        ) as stream:
            temporary_manifest = Path(stream.name)
            stream.write(manifest)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.mkdir(output)
        except FileExistsError:
            _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
        except OSError:
            _fail("TRITRACK_RELEASE_OUTPUT")
        _link_file(wheel, output / wheel.name)
        _link_file(sdist, output / sdist.name)
        _fsync_directory(output)
        _verify_published_archive(output / wheel.name, expected_artifacts["wheel"])
        _verify_published_archive(output / sdist.name, expected_artifacts["sdist"])
        _link_file(temporary_manifest, output / "release-manifest.json")
        _fsync_directory(output)
        _fsync_directory(output.parent)
    finally:
        if temporary_manifest is not None:
            try:
                temporary_manifest.unlink(missing_ok=True)
            except OSError:
                pass


def _assert_source_identity(source: Path) -> tuple[str, str]:
    encoded = _read_regular(source / ".tritrack-project.json", _POLICY_LIMIT)
    try:
        identity = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")
    expected = {
        "schemaVersion": "tritrack.project-identity/v1",
        "projectId": "tritrack-editing-assistant",
        "projectKind": "public-engine",
        "maintainerSkill": "tritrack-editing-assistant-maintainer",
        "lane": "OSS",
    }
    if identity != expected:
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")

    try:
        configuration = tomllib.loads(
            _read_regular(source / "pyproject.toml", _POLICY_LIMIT).decode("utf-8")
        )
        project = configuration["project"]
        project_name = project["name"]
        version = project["version"]
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    if project_name != "tritrack-editing-assistant" or not isinstance(version, str):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    init_bytes = _read_regular(
        source / "src" / "tritrack_editing_assistant" / "__init__.py",
        _POLICY_LIMIT,
    )
    match = re.fullmatch(
        rb'"""TriTrack Editing Assistant public package\."""\n\n__version__ = "([^"\r\n]+)"\n',
        init_bytes,
    )
    if match is None or match.group(1).decode("utf-8", "strict") != version:
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    return project_name, version


def _assert_git_toplevel(source: Path) -> None:
    try:
        top = Path(
            _run_git(source, "rev-parse", "--show-toplevel").decode("utf-8", "strict").strip()
        ).resolve()
    except (UnicodeDecodeError, OSError):
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if top != source:
        _fail("TRITRACK_RELEASE_GIT_TOPLEVEL")


def _snapshot_inventory(
    archive: tarfile.TarFile,
    max_file: int,
    max_total: int,
) -> tuple[list[tuple[str, int, bytes]], str]:
    files: list[tuple[str, int, bytes]] = []
    seen: set[str] = set()
    total = 0
    for member in archive.getmembers():
        name = _safe_member_name(member.name)
        if name in seen:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        seen.add(name)
        if member.isdir():
            continue
        if not member.isreg():
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        if member.size > max_file:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += member.size
        if total > max_total:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        stream = archive.extractfile(member)
        if stream is None:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        with stream:
            encoded = _bounded_archive_read(stream, member.size, max_file)
        mode = 0o755 if member.mode & 0o111 else 0o644
        files.append((name, mode, encoded))
    inventory = hashlib.sha256()
    for name, mode, encoded in sorted(files):
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, f"100{mode:o}"[-6:], str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")
    return files, inventory.hexdigest()


def _write_snapshot_file(root: Path, name: str, mode: int, encoded: bytes) -> None:
    path = root.joinpath(*PurePosixPath(name).parts)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            mode,
        )
        try:
            view = memoryview(encoded)
            while view:
                written = os.write(descriptor, view)
                if written < 1:
                    _fail("TRITRACK_RELEASE_SNAPSHOT")
                view = view[written:]
        finally:
            os.close(descriptor)
        os.chmod(path, mode, follow_symlinks=False)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")


def _materialize_snapshot(
    source: Path,
    destination: Path,
    inventory: SourceInventory,
    policy: Mapping[str, object],
) -> None:
    try:
        os.mkdir(destination)
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    archive_path = destination.parent / f".{destination.name}.tar"
    _run_command(
        [
            "git",
            "archive",
            "--format=tar",
            "--output",
            os.fspath(archive_path),
            inventory.commit,
        ],
        cwd=source,
        env=_safe_environment(),
        timeout=120,
    )
    try:
        with tarfile.open(archive_path, mode="r:") as archive:
            files, digest = _snapshot_inventory(
                archive,
                _positive_limit(policy, "sourceMaxFileBytes"),
                _positive_limit(policy, "sourceMaxTotalBytes"),
            )
        if len(files) != inventory.count or digest != inventory.sha256:
            _fail("TRITRACK_RELEASE_SNAPSHOT_MISMATCH")
        for name, mode, encoded in files:
            _write_snapshot_file(destination, name, mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    finally:
        try:
            archive_path.unlink(missing_ok=True)
        except OSError:
            pass


def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
    return (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )


def run_release_gate(source: Path, output: Path) -> dict[str, object]:
    """Run the complete local release-readiness gate and publish manifest last."""

    try:
        source = source.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE")
    if not source.is_dir():
        _fail("TRITRACK_RELEASE_SOURCE")
    _assert_git_toplevel(source)
    project_name, version = _assert_source_identity(source)
    inventory = inventory_tracked_source(source)
    policy = _load_policy(source)
    if output.exists() or output.is_symlink():
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    try:
        output_parent = output.parent.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    output = output_parent / output.name
    epoch_bytes = _run_git(source, "show", "-s", "--format=%ct", inventory.commit).strip()
    try:
        epoch = int(epoch_bytes.decode("ascii", "strict"))
    except (UnicodeDecodeError, ValueError):
        _fail("TRITRACK_RELEASE_EPOCH")
    if _run_git(source, "rev-parse", "HEAD").strip().decode("ascii") != inventory.commit:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")

    with tempfile.TemporaryDirectory(
        dir=output.parent, prefix=".tritrack-release-staging-"
    ) as temporary:
        staging = Path(temporary)
        snapshot_one = staging / "snapshot-one"
        snapshot_two = staging / "snapshot-two"
        _materialize_snapshot(source, snapshot_one, inventory, policy)
        _materialize_snapshot(source, snapshot_two, inventory, policy)
        wheel_one, sdist_one = build_distributions(
            snapshot_one, staging / "dist-one", epoch=epoch
        )
        wheel_two, sdist_two = build_distributions(
            snapshot_two, staging / "dist-two", epoch=epoch
        )
        identities = {
            _wheel_project_identity(wheel_one),
            _wheel_project_identity(wheel_two),
        }
        if identities != {(project_name, version)}:
            _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
        if wheel_one.name != wheel_two.name or sdist_one.name != sdist_two.name:
            _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
        wheel_inspection = inspect_wheel(wheel_one, policy)
        second_wheel_inspection = inspect_wheel(wheel_two, policy)
        sdist_inspection = inspect_sdist(sdist_one, policy)
        second_sdist_inspection = inspect_sdist(sdist_two, policy)
        if wheel_inspection != second_wheel_inspection:
            _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
        if (
            sdist_inspection.member_inventory_sha256
            != second_sdist_inspection.member_inventory_sha256
        ):
            _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
        fresh_install_smoke(wheel_one, staging / "fresh-install")
        context = ReleaseContext(
            project_name=project_name,
            version=version,
            commit=inventory.commit,
            source_inventory=inventory,
            toolchain=_installed_tool_versions(),
            python_version=platform.python_version(),
            implementation=platform.python_implementation(),
            system=platform.system(),
            machine=platform.machine(),
            wheel=wheel_inspection,
            sdist=sdist_inspection,
        )
        manifest = build_release_manifest(context)
        publish_release(
            output,
            wheel_one,
            sdist_one,
            _canonical_manifest(manifest),
        )
    return manifest
