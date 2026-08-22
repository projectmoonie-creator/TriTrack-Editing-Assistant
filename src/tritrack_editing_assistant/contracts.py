"""Strict loaders for the public versioned JSON contracts."""

from __future__ import annotations

import json
from collections.abc import Mapping
from functools import cache
from importlib import resources
from types import MappingProxyType

import jsonschema

CONTRACT_NAMES = frozenset(
    {
        "compatibility-profile-v1",
        "sync-map-v1",
        "sync-map-v2",
        "transcript-bundle-v1",
        "transcription-report-v1",
        "transcription-result-manifest-v1",
        "text-revision-v1",
        "aligned-transcript-v1",
        "grouping-v1",
        "working-cut-v1",
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


@cache
def contract_names_by_schema_version() -> Mapping[str, str]:
    """Return the closed installed schema-version to contract-name registry."""

    mapping: dict[str, str] = {}
    for name in sorted(CONTRACT_NAMES):
        schema = load_schema(name)
        try:
            version = schema["properties"]["schemaVersion"]["const"]
        except (KeyError, TypeError) as error:
            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID") from error
        if not isinstance(version, str) or version in mapping:
            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID")
        mapping[version] = name
    return MappingProxyType(mapping)


def contract_name_for_schema_version(schema_version: object) -> str:
    """Resolve only an exact version declared by one installed contract."""

    if not isinstance(schema_version, str):
        # One stable data-error family covers absent, non-string, and unknown IDs.
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN")  # noqa: TRY004
    try:
        return contract_names_by_schema_version()[schema_version]
    except KeyError as error:
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN") from error
