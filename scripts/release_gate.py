"""Maintainer-only Task 11 release-readiness command."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__:
    from scripts import release_gate_core
else:
    import release_gate_core


class _UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _UsageError from None


def _error(code: str) -> None:
    print(json.dumps({"error": code}, separators=(",", ":")), file=sys.stderr)


def _parser() -> argparse.ArgumentParser:
    parser = _Parser(add_help=True, allow_abbrev=False)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _parser().parse_args(argv)
    except _UsageError:
        _error("TRITRACK_RELEASE_USAGE")
        return 64
    try:
        manifest = release_gate_core.run_release_gate(
            Path(arguments.source), Path(arguments.output)
        )
        manifest_sha = hashlib.sha256(
            release_gate_core._canonical_manifest(manifest)
        ).hexdigest()
        project = manifest["project"]
        artifacts = manifest["artifacts"]
        lines = (
            "RELEASE_GATE\tPASS",
            f"commit\t{project['commit']}",
            f"version\t{project['version']}",
            f"wheelSha256\t{artifacts['wheel']['sha256']}",
            f"sdistSha256\t{artifacts['sdist']['sha256']}",
            f"manifestSha256\t{manifest_sha}",
        )
    except release_gate_core.ReleaseGateError as error:
        _error(error.code)
        return 1
    except Exception:  # noqa: BLE001 - the public boundary must never emit a traceback
        _error("TRITRACK_RELEASE_INTERNAL")
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
