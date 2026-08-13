"""Fail closed unless a root is the public TriTrack maintenance project."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED = {
    "schemaVersion": "tritrack.project-identity/v1",
    "projectId": "tritrack-editing-assistant",
    "projectKind": "public-engine",
    "maintainerSkill": "tritrack-editing-assistant-maintainer",
    "lane": "OSS",
}
MAX_IDENTITY_BYTES = 16 * 1024


def validate(root: Path) -> dict[str, object]:
    identity_path = root / ".tritrack-project.json"
    if not identity_path.is_file() or identity_path.is_symlink():
        raise ValueError("TRITRACK_PROJECT_IDENTITY_MISSING")
    try:
        raw = identity_path.read_bytes()
    except OSError as error:
        raise ValueError("TRITRACK_PROJECT_IDENTITY_UNREADABLE") from error
    if len(raw) > MAX_IDENTITY_BYTES:
        raise ValueError("TRITRACK_PROJECT_IDENTITY_INVALID")
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_PROJECT_IDENTITY_INVALID") from error
    if payload != EXPECTED:
        raise ValueError("TRITRACK_PROJECT_IDENTITY_MISMATCH")
    return {
        "lane": EXPECTED["lane"],
        "ok": True,
        "projectId": EXPECTED["projectId"],
        "projectKind": EXPECTED["projectKind"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        result = validate(arguments.root)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
