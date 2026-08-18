"""Bounded, fail-closed primitives for the maintainer release gate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import tarfile
import unicodedata
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

_COMMAND_TIMEOUT_SECONDS = 30
_COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
_POLICY_LIMIT = 1024 * 1024
_ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
_ALLOWED_FAKE_SECRETS = frozenset(
    {b"editor", b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
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


def _archive_size(path: Path, policy: Mapping[str, object]) -> int:
    try:
        details = path.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    if not stat.S_ISREG(details.st_mode):
        _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
    if details.st_size > _positive_limit(policy, "archiveMaxBytes"):
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    return details.st_size


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

    size_bytes = _archive_size(path, policy)
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
        with zipfile.ZipFile(path) as archive:
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
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(files),
        member_inventory_sha256=inventory.hexdigest(),
    )


def inspect_sdist(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a gzipped source distribution without extracting it."""

    size_bytes = _archive_size(path, policy)
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
        with tarfile.open(path, mode="r:gz") as archive:
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
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(all_members),
        member_inventory_sha256=inventory.hexdigest(),
    )
