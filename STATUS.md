# Public maintenance status

Updated: 2026-08-14
Project kind: public engine
Lane: `OSS`
Release state: public pre-release source; no tag, package publication, or
tester outreach

## Current gate

Tasks 1–6 are complete in this public candidate. Task 6 began from exact
Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
rewrite or merge commit.

Task 6 implements strict `sync-map-v1` loading, exact public profile and Basic
Title binding checks, integer-frame pair alignment, deterministic pair-first
string-out ordering, stable XML identifiers and bytes, XML escaping, source
immutability, sync-map audio-master selection, source-profile probing, and
race-safe absent-output FCPXML publication. The implementation retains FCPXML
1.14, UHD 3840×2160, `1001/30000s`, NDF, Rec. 709, stereo, and 48 kHz profile
values. Closeout-review verification after the last implementation edit passed
67 tests and Ruff; invented temporary output also passed the declared Final Cut
Pro 12.3 FCPXML 1.14 DTD. This is automated DTD evidence, not a claim that a
Task 6 GUI import or round trip ran.

## Next action

Task 7 adds local transcription and deterministic fallbacks. It remains a
separate public task and must not silently broaden Task 6 compatibility or
outward-action authority.

## Implemented surface

- clean Python package and eleven-component status registry;
- Draft 2020-12 contracts loaded from installed package resources;
- bounded argv-only subprocess execution and sanitized receipts;
- audio-verified A/B synchronization with atomic `sync-map-v1` publication;
- profile-bound deterministic string-out and atomic FCPXML 1.14 publication;
- fail-closed `doctor` command;
- exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
- public Basic Title binding with invented-content Final Cut round-trip
  evidence.

Editing commands other than `sync`, `emit`, `doctor`, and `components` remain
planned and must return non-success until implemented and tested.

## Custody

The public `origin` is
`https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`.
Closeout requires verifying that its `main` SHA exactly matches the local green
candidate, making the GitHub copy the off-device Git backup. Tags, releases,
pull requests, tester contact, and package publication remain separate gates.
