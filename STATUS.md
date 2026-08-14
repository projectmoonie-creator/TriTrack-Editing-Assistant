# Public maintenance status

Updated: 2026-08-14
Project kind: public engine
Lane: `OSS`
Release state: local pre-release; no remote, tag, package publication, or
tester outreach

## Current gate

Tasks 1–5 are complete in this local public candidate. Task 5 began from exact
public base `41d5034addcc1f870ec7b055f62b69c38cae415b`. Its clean-room intake
matched all six declared payload hashes; the public export receipt records
seven copied entries, zero transformed entries, and tree SHA-256
`92843afb703f8f5b832601122b3ed1c4a3b24763fe3ac7365a1450bc549fb2a3`.
The matching public transform worklist contains no entries.

Task 5 implements normalized audio correlation, sane time-hint narrowing with
stale fallback, reusable B recordings, strongest-candidate selection, bounded
public media processes, strict `sync-map-v1` output, source immutability, and
race-safe absent-output publication. Verification after the last
implementation edit passed 50 tests and Ruff; the closing gate also includes
skill validation, the identity probe, Python compilation, boundary tests, and
`git diff --check`.

## Next action

Task 6 implements profile-bound FCPXML emission and string-out. It remains a
separate public task and must not silently broaden Task 5 compatibility or
outward-action authority.

## Implemented surface

- clean Python package and eleven-component status registry;
- Draft 2020-12 contracts loaded from installed package resources;
- bounded argv-only subprocess execution and sanitized receipts;
- audio-verified A/B synchronization with atomic `sync-map-v1` publication;
- fail-closed `doctor` command;
- exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
- public Basic Title binding with invented-content Final Cut round-trip
  evidence.

Editing commands other than `sync`, `doctor`, and `components` remain planned
and must return non-success until implemented and tested.

## Custody

The repository intentionally has no remote during this gate. Local commits are
not off-device backups. Any remote creation, public push, tag, release, tester
contact, or package publication requires explicit producer approval.
