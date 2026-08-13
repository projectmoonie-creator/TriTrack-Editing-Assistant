# Public maintenance status

Updated: 2026-08-13
Project kind: public engine
Lane: `OSS`
Release state: local pre-release; no remote, tag, package publication, or
tester outreach

## Current gate

Tasks 1–4 are complete in the clean public history. The current accepted base
is commit `9b0d02b08ca83b198556a42dedababc83fe0f38f`, tree
`4d9bbd593370b4f776eac8dac1f8a87e675da2ee`.

Task 4.5 is CLOSED in this status-bearing candidate. It separates public
maintenance from both private production orchestration and the future
end-user product skill. Verification after the last implementation edit
passed 39 tests including seven boundary cases, Ruff, skill validation, the
identity probe, Python compilation, and `git diff --check`.

## Next action

Task 5 extracts and hardens the synchronization engine. The `OSS` lane may
consume only a separately reviewed clean-room handoff; it must not browse
another repository to obtain source or context. Until that handoff exists,
Task 5 is waiting on its private-side source preparation rather than silently
crossing the boundary.

## Implemented surface

- clean Python package and eleven-component status registry;
- Draft 2020-12 contracts loaded from installed package resources;
- bounded argv-only subprocess execution and sanitized receipts;
- fail-closed `doctor` command;
- exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
- public Basic Title binding with invented-content Final Cut round-trip
  evidence.

Editing commands other than `doctor` and `components` remain planned and must
return non-success until implemented and tested.

## Custody

The repository intentionally has no remote during this gate. Local commits are
not off-device backups. Any remote creation, public push, tag, release, tester
contact, or package publication requires explicit producer approval.
