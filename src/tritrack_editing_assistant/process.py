"""Bounded subprocess execution with privacy-safe machine receipts."""

from __future__ import annotations

import hashlib
import json
import math
import os
import selectors
import signal
import subprocess
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

ALLOWED_ENVIRONMENT_KEYS = frozenset(
    {"LANG", "LC_ALL", "LC_CTYPE", "PATH", "TMPDIR", "TZ"}
)
_READ_CHUNK_BYTES = 64 * 1024
_TERMINATION_GRACE_SECONDS = 0.2


@dataclass(frozen=True)
class ProcessResult:
    """Raw bounded output kept separate from the sanitized public receipt."""

    status: str
    returncode: int | None
    stdout: bytes
    stderr: bytes
    receipt: dict[str, object]

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def require_absent_output(path: str | os.PathLike[str]) -> Path:
    """Return *path* only when no file, directory, or symlink exists there."""

    resolved = Path(path)
    if os.path.lexists(resolved):
        raise ValueError("TRITRACK_OUTPUT_EXISTS")
    return resolved


def _command_shape(command: Sequence[str]) -> list[str]:
    shape = [Path(command[0]).name]
    for argument in command[1:]:
        if argument.startswith("-"):
            option = argument.split("=", 1)[0]
            shape.append(f"option:{option}")
        elif os.path.isabs(argument) or "/" in argument or "\\" in argument:
            shape.append("path")
        else:
            shape.append("argument")
    return shape


def sanitized_receipt(
    *,
    command: Sequence[str],
    environment: Mapping[str, str],
    returncode: int | None,
    status: str | None = None,
    timed_out: bool = False,
    output_limit_exceeded: bool = False,
    observed_captured_bytes: int = 0,
    stdout: bytes | None = None,
    stderr: bytes | None = None,
    duration_ms: int | None = None,
    error_code: str | None = None,
) -> dict[str, object]:
    """Build a receipt without command arguments, paths, output, or env values."""

    if not command:
        raise ValueError("TRITRACK_PROCESS_COMMAND_INVALID")
    shape_bytes = json.dumps(
        _command_shape(command), ensure_ascii=True, separators=(",", ":")
    ).encode("utf-8")
    if status is None:
        status = "ok" if returncode == 0 else "failed"

    receipt: dict[str, object] = {
        "schemaVersion": "tritrack.process-receipt/v1",
        "status": status,
        "executable": Path(command[0]).name,
        "argumentCount": len(command) - 1,
        "argumentShapeSha256": hashlib.sha256(shape_bytes).hexdigest(),
        "environmentKeys": sorted(environment),
        "returncode": returncode,
        "timedOut": timed_out,
        "outputLimitExceeded": output_limit_exceeded,
        "observedCapturedBytes": observed_captured_bytes,
        "retainedStdoutBytes": len(stdout) if stdout is not None else 0,
        "retainedStderrBytes": len(stderr) if stderr is not None else 0,
        "stdoutSha256": hashlib.sha256(stdout).hexdigest()
        if stdout is not None
        else None,
        "stderrSha256": hashlib.sha256(stderr).hexdigest()
        if stderr is not None
        else None,
        "durationMs": duration_ms,
    }
    if error_code is not None:
        receipt["errorCode"] = error_code
    return receipt


def _validate_command(command: Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, (str, bytes)) or not isinstance(command, Sequence):
        raise TypeError("TRITRACK_PROCESS_COMMAND_INVALID")
    if not command or any(
        not isinstance(argument, str) or not argument or "\x00" in argument
        for argument in command
    ):
        raise ValueError("TRITRACK_PROCESS_COMMAND_INVALID")
    return tuple(command)


def _validate_bounds(timeout_seconds: float, max_captured_bytes: int) -> None:
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("TRITRACK_PROCESS_TIMEOUT_INVALID")
    if (
        isinstance(max_captured_bytes, bool)
        or not isinstance(max_captured_bytes, int)
        or max_captured_bytes < 1
    ):
        raise ValueError("TRITRACK_PROCESS_CAPTURE_LIMIT_INVALID")


def _validated_environment(
    environment: Mapping[str, str] | None,
) -> dict[str, str]:
    if environment is None:
        return {
            key: os.environ[key]
            for key in ALLOWED_ENVIRONMENT_KEYS
            if key in os.environ
        }
    if not isinstance(environment, Mapping):
        raise TypeError("TRITRACK_PROCESS_ENVIRONMENT_INVALID")

    validated: dict[str, str] = {}
    for key, value in environment.items():
        if key not in ALLOWED_ENVIRONMENT_KEYS:
            raise ValueError(f"TRITRACK_PROCESS_ENVIRONMENT_NOT_ALLOWED: {key}")
        if not isinstance(value, str) or "\x00" in value:
            raise ValueError("TRITRACK_PROCESS_ENVIRONMENT_INVALID")
        validated[key] = value
    return validated


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except OSError:
        process.terminate()

    try:
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        if process.poll() is None:
            process.kill()

    if process.poll() is None:
        process.wait()


def _close_pipes(process: subprocess.Popen[bytes]) -> None:
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()


def _capture_bounded(
    process: subprocess.Popen[bytes],
    *,
    deadline: float,
    max_captured_bytes: int,
) -> tuple[str, bytes, bytes, int]:
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    observed_bytes = 0

    with selectors.DefaultSelector() as selector:
        assert process.stdout is not None
        assert process.stderr is not None
        selector.register(process.stdout, selectors.EVENT_READ, stdout_chunks)
        selector.register(process.stderr, selectors.EVENT_READ, stderr_chunks)

        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return "timeout", b"", b"", observed_bytes

            events = selector.select(timeout=min(remaining, 0.05))
            for key, _mask in events:
                allowed_read = max_captured_bytes - observed_bytes + 1
                chunk = os.read(
                    key.fd,
                    min(_READ_CHUNK_BYTES, max(1, allowed_read)),
                )
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue

                observed_bytes += len(chunk)
                if observed_bytes > max_captured_bytes:
                    return "output_limit_exceeded", b"", b"", observed_bytes
                key.data.append(chunk)

    remaining = deadline - time.monotonic()
    if remaining <= 0 and process.poll() is None:
        return "timeout", b"", b"", observed_bytes
    try:
        process.wait(timeout=max(0.0, remaining))
    except subprocess.TimeoutExpired:
        return "timeout", b"", b"", observed_bytes

    return (
        "ok" if process.returncode == 0 else "failed",
        b"".join(stdout_chunks),
        b"".join(stderr_chunks),
        observed_bytes,
    )


def run_bounded(
    command: Sequence[str],
    *,
    timeout_seconds: float,
    max_captured_bytes: int,
    environment: Mapping[str, str] | None = None,
) -> ProcessResult:
    """Run one argv-only process with time, output, and environment bounds."""

    checked_command = _validate_command(command)
    _validate_bounds(timeout_seconds, max_captured_bytes)
    checked_environment = _validated_environment(environment)
    started = time.monotonic()

    try:
        child = subprocess.Popen(
            checked_command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            env=checked_environment,
            start_new_session=True,
        )
    except OSError as error:
        duration_ms = round((time.monotonic() - started) * 1000)
        receipt = sanitized_receipt(
            command=checked_command,
            environment=checked_environment,
            returncode=None,
            status="spawn_error",
            duration_ms=duration_ms,
            error_code=f"OS_ERROR_{error.errno}",
        )
        return ProcessResult("spawn_error", None, b"", b"", receipt)

    deadline = started + timeout_seconds
    status, stdout, stderr, observed_bytes = _capture_bounded(
        child,
        deadline=deadline,
        max_captured_bytes=max_captured_bytes,
    )
    if status in {"timeout", "output_limit_exceeded"}:
        _terminate_process_group(child)
        stdout = b""
        stderr = b""
    _close_pipes(child)

    duration_ms = round((time.monotonic() - started) * 1000)
    receipt = sanitized_receipt(
        command=checked_command,
        environment=checked_environment,
        returncode=child.returncode,
        status=status,
        timed_out=status == "timeout",
        output_limit_exceeded=status == "output_limit_exceeded",
        observed_captured_bytes=observed_bytes,
        stdout=stdout if status in {"ok", "failed"} else None,
        stderr=stderr if status in {"ok", "failed"} else None,
        duration_ms=duration_ms,
    )
    return ProcessResult(status, child.returncode, stdout, stderr, receipt)
