"""Fail-closed, privacy-safe compatibility preflight."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import shutil
from importlib import resources
from pathlib import Path
from typing import Protocol

from .contracts import validate_contract
from .process import require_absent_output, run_bounded

PROFILE_NAMES = frozenset({"uhd-2997-ndf-fcpxml-1.14"})
TITLE_BINDING_NAMES = frozenset({"basic-title-v1"})
SUPPORTED_MACOS_VERSION = "26.5.2"
SUPPORTED_ARCHITECTURE = "arm64"
SUPPORTED_FINAL_CUT_VERSION = "12.3"
FINAL_CUT_INFO = Path("/Applications/Final Cut Pro.app/Contents/Info.plist")
FINAL_CUT_DTD_DIRECTORY = Path(
    "/Applications/Final Cut Pro.app/Contents/Frameworks/"
    "Interchange.framework/Versions/A/Resources"
)
MINIMUM_FREE_DISK_BYTES = 5 * 1024**3


class Probe(Protocol):
    system: str
    macos_version: str
    architecture: str
    python_version: str
    final_cut_version: str | None
    free_disk_bytes: int

    def executable_version(self, name: str) -> str | None: ...

    def final_cut_dtd_present(self, version: str) -> bool: ...

    def path_is_readable_file(self, path: Path) -> bool: ...


class SystemProbe:
    """Read only declared local compatibility facts."""

    def __init__(self) -> None:
        self.system = platform.system()
        self.macos_version = platform.mac_ver()[0]
        self.architecture = platform.machine()
        self.python_version = platform.python_version()
        self.final_cut_version = self._final_cut_version()
        self.free_disk_bytes = shutil.disk_usage(Path.cwd()).free

    @staticmethod
    def _final_cut_version() -> str | None:
        try:
            with FINAL_CUT_INFO.open("rb") as handle:
                value = plistlib.load(handle).get("CFBundleShortVersionString")
        except (OSError, plistlib.InvalidFileException):
            return None
        return value if isinstance(value, str) and value else None

    def executable_version(self, name: str) -> str | None:
        executable = shutil.which(name)
        if executable is None:
            return None
        arguments = (
            [executable, "-version"] if name != "xmllint" else [executable, "--version"]
        )
        result = run_bounded(
            arguments,
            timeout_seconds=5,
            max_captured_bytes=64 * 1024,
        )
        if not result.ok:
            return None
        output = result.stdout or result.stderr
        first_line = output.decode("utf-8", errors="replace").splitlines()
        return (
            _sanitize_detected(first_line[0]) if first_line else Path(executable).name
        )

    def final_cut_dtd_present(self, version: str) -> bool:
        return (
            FINAL_CUT_DTD_DIRECTORY / f"FCPXMLv{version.replace('.', '_')}.dtd"
        ).is_file()

    def path_is_readable_file(self, path: Path) -> bool:
        return path.is_file() and os.access(path, os.R_OK)


def _sanitize_detected(value: str) -> str:
    """Keep version text while refusing local path-shaped material."""

    private_home = "/" + "Users" + "/"
    mounted_volume = "/" + "Volumes" + "/"
    if private_home in value or mounted_volume in value or "\\" in value:
        return "detected-redacted"
    first, separator, remainder = value.partition(" ")
    if first.startswith("/"):
        first = Path(first.rstrip(":")).name + (":" if first.endswith(":") else "")
        value = first + (separator + remainder if separator else "")
    return value[:256]


def _load_packaged_json(name: str, allowed: frozenset[str]) -> dict[str, object]:
    if name not in allowed:
        raise ValueError(f"TRITRACK_PROFILE_UNKNOWN: {name!r}")
    payload = json.loads(
        resources.files("tritrack_editing_assistant.profiles")
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    if not isinstance(payload, dict):
        raise TypeError("TRITRACK_PROFILE_INVALID")
    return payload


def load_profile(profile_id: str) -> dict[str, object]:
    profile = _load_packaged_json(profile_id, PROFILE_NAMES)
    validate_contract("compatibility-profile-v1", profile)
    if profile.get("profileId") != profile_id:
        raise ValueError("TRITRACK_PROFILE_ID_MISMATCH")
    return profile


def load_title_binding(binding_id: str) -> dict[str, object]:
    binding = _load_packaged_json(binding_id, TITLE_BINDING_NAMES)
    validate_contract("title-binding-v1", binding)
    if binding.get("bindingId") != binding_id:
        raise ValueError("TRITRACK_PROFILE_ID_MISMATCH")
    return binding


def _check(code: str, status: str, *, detected: str | None = None) -> dict[str, object]:
    result: dict[str, object] = {"code": code, "status": status}
    if detected is not None:
        result["detected"] = _sanitize_detected(detected)
    return result


def build_receipt(
    *,
    profile_id: str,
    probe: Probe | None = None,
    transcription_requested: bool = False,
    whisper_model: Path | None = None,
) -> dict[str, object]:
    """Inspect the exact alpha environment without retaining private paths."""

    selected_probe = probe or SystemProbe()
    profile = load_profile(profile_id)
    binding = load_title_binding("basic-title-v1")
    checks: list[dict[str, object]] = []

    checks.append(
        _check(
            "operating-system",
            "ok" if selected_probe.system == "Darwin" else "unsupported",
            detected=selected_probe.system,
        )
    )
    checks.append(
        _check(
            "macos-version",
            "ok"
            if selected_probe.macos_version == SUPPORTED_MACOS_VERSION
            else "unsupported",
            detected=selected_probe.macos_version,
        )
    )
    checks.append(
        _check(
            "architecture",
            "ok"
            if selected_probe.architecture == SUPPORTED_ARCHITECTURE
            else "unsupported",
            detected=selected_probe.architecture,
        )
    )
    checks.append(_check("python", "ok", detected=selected_probe.python_version))
    checks.append(
        _check(
            "free-disk",
            "ok"
            if selected_probe.free_disk_bytes >= MINIMUM_FREE_DISK_BYTES
            else "insufficient",
            detected=str(selected_probe.free_disk_bytes),
        )
    )

    for executable in ("ffmpeg", "ffprobe", "xmllint"):
        detected = selected_probe.executable_version(executable)
        checks.append(
            _check(
                executable,
                "ok" if detected is not None else "missing",
                detected=detected,
            )
        )

    checks.append(
        _check(
            "final-cut",
            "ok"
            if selected_probe.final_cut_version == SUPPORTED_FINAL_CUT_VERSION
            else "unsupported",
            detected=selected_probe.final_cut_version,
        )
    )
    dtd_present = selected_probe.final_cut_dtd_present(str(profile["fcpxmlVersion"]))
    checks.append(_check("fcpxml-dtd", "ok" if dtd_present else "missing"))
    checks.append(_check("compatibility-profile", "ok", detected=profile_id))
    checks.append(_check("title-binding", "ok", detected=str(binding["bindingId"])))

    if transcription_requested:
        whisper_detected = selected_probe.executable_version("whisper-cli")
        checks.append(
            _check(
                "whisper-cli",
                "ok" if whisper_detected is not None else "missing",
                detected=whisper_detected,
            )
        )
        model_readable = (
            whisper_model is not None
            and selected_probe.path_is_readable_file(whisper_model)
        )
        checks.append(_check("whisper-model", "ok" if model_readable else "unreadable"))

    supported = all(check["status"] == "ok" for check in checks)
    return {
        "schemaVersion": "tritrack.doctor-receipt/v1",
        "profileId": profile_id,
        "titleBindingId": binding["bindingId"],
        "supported": supported,
        "checks": checks,
        "remediation": []
        if supported
        else ["Install or select only dependencies declared by the alpha profile."],
    }


def write_receipt(output: Path, **arguments: object) -> dict[str, object]:
    """Atomically create one absent doctor receipt."""

    destination = require_absent_output(output)
    receipt = build_receipt(**arguments)
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(destination, flags, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return receipt
