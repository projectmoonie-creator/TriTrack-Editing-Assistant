"""Strict loaders for the public versioned JSON contracts."""

from __future__ import annotations

import json
from functools import cache
from importlib import resources

import jsonschema

CONTRACT_NAMES = frozenset(
    {
        "compatibility-profile-v1",
        "sync-map-v1",
        "transcript-bundle-v1",
        "text-revision-v1",
        "aligned-transcript-v1",
        "grouping-v1",
        "title-binding-v1",
        "run-manifest-v1",
        "provider-receipt-v1",
    }
)


@cache
def load_schema(name: str) -> dict[str, object]:
    """Load and meta-validate one packaged schema by its closed public name."""

    if name not in CONTRACT_NAMES:
        raise ValueError(f"TRITRACK_CONTRACT_UNKNOWN: {name!r}")

    schema_text = (
        resources.files("tritrack_editing_assistant.schemas")
        .joinpath(f"{name}.schema.json")
        .read_text(encoding="utf-8")
    )
    schema = json.loads(schema_text)
    jsonschema.Draft202012Validator.check_schema(schema)
    return schema


def validate_contract(name: str, payload: object) -> None:
    """Fail closed unless *payload* exactly satisfies a packaged contract."""

    validator = jsonschema.Draft202012Validator(load_schema(name))
    validator.validate(payload)
