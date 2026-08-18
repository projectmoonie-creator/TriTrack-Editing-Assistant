# Tasks 7–11 Claude coverage recovery review packet

Packet date: 2026-08-18

## Objective

Perform one new, read-only review of the current integrated public alpha to
recover the useful Claude coverage that older Task 7–11 attempts did not
produce. Review current source, tests, and public contracts only. Produce
findings; do not edit files.

This is a new review request against the integrated candidate. It is not a
replay of any historical provider request and must not claim that an older
ambiguous attempt was never dispatched.

## Frozen target

- Repository: `projectmoonie-creator/TriTrack-Editing-Assistant`
- Lane: `OSS`
- Target branch: public `main`
- Exact target commit: `54f5f2c1dade34ae5fa7a7dc070b7dcc2d27c37d`
- Package version: `0.1.0a0`
- Project kind: public engine

The review packet itself may be present as an uncommitted documentation file.
It is not part of the source target. Limit source findings to the exact target
commit and cite repository-relative file paths and current line numbers.

## Why this recovery review exists

The public record contains eight older Claude attempts with no usable result:

| Area | Attempt | Recorded result |
| --- | --- | --- |
| Task 7 closeout | `b5479357-f27c-4930-a51c-d5bbbb14092c` | `claude-timeout`; dispatch unknown |
| Task 8 design | `ba290d4b-2867-4241-ac13-e9f288c10914` | `claude-timeout`; dispatch unknown |
| Task 8 closeout | `b35fb467-7046-424d-816e-dd497096f170` | `claude-timeout`; dispatch unknown |
| Task 9 closeout | `5d9d13e2-007c-41ec-8623-3c0cbe086c4a` | `claude-timeout`; dispatch unknown |
| Task 9 post-fix | `9f8ea635-bf56-4ca1-91ec-f2e57cda71e0` | `claude-timeout`; dispatch unknown |
| Task 10 closeout | `aad06b61-ac4b-49bd-805f-ef7df23bd747` | `claude-timeout`; dispatch unknown |
| Task 11 design | `637f7c3a-cf72-4e97-9d42-ef7ef0d1400e` | `claude-timeout`; dispatch unknown |
| Task 11 closeout | `67528669-94b0-4e39-87bd-ab903b2bd552` | `claude-timeout`; dispatch unknown |

Do not treat those failures as findings or as completed reviews. A separate
Task 9 design review completed through the approved subscription lane with
`claude-opus-5`, proving that the subscription preflight repair and these
later hard timeouts are different conditions.

## Public behavior to review

### Task 7 — local transcription

The fixed local profile converts each caller-supplied source to bounded mono
16 kHz PCM, invokes caller-installed whisper.cpp CPU-only without fallback,
canonicalizes strict cues, binds source/model hashes, and atomically publishes
one absent `transcript-bundle-v1`. It must remain local, deterministic at the
canonicalization boundary, fail closed on malformed or changed evidence, and
emit path-free summaries.

Primary paths:

- `src/tritrack_editing_assistant/transcribe_takes.py`
- `src/tritrack_editing_assistant/hallucination.py`
- `src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json`
- `tests/test_transcribe_takes.py`
- `tests/test_hallucination.py`

### Task 8 — immutable text promotion and offline receipt conformance

`align` promotes cue-addressed text only while preserving IDs, hashes, status,
and integer timing. `hybrid` validates already-produced provider receipts
offline and must make no provider request, upload, deletion, credential lookup,
or network call. Both routes use the same promotion core and exact-byte input
binding.

Primary paths:

- `src/tritrack_editing_assistant/align_text.py`
- `src/tritrack_editing_assistant/gemini_hybrid.py`
- `src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json`
- `src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json`
- `src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json`
- `tests/test_align_text.py`
- `tests/test_gemini_hybrid.py`

### Task 9 — paper edit and organization

The XLSX workbook is non-authoritative transport. Apply must re-derive its
complete cue/display grid and hidden manifest from exact aligned bytes, reject
active content and structural drift, and publish canonical cue-addressed
grouping only. Organization must copy timing solely from aligned authority and
produce deterministic text-free `working-cut-v1`.

Primary paths:

- `src/tritrack_editing_assistant/paper_edit.py`
- `src/tritrack_editing_assistant/organizer.py`
- `src/tritrack_editing_assistant/schemas/grouping-v1.schema.json`
- `src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json`
- `tests/test_paper_edit.py`
- `tests/test_organizer.py`

### Task 10 — immutable run workflow

`prepare`, `align`, and `finish` each publish a new absent directory with a
strict manifest linked last. Fixed artifacts, exact hashes, prior-manifest
chains, media/model immutability, and editor gates must be revalidated before
reuse. Final story FCPXML must derive order, text, timing, source offsets, and
audio-master coverage only from the strict authorities. `status` is read-only.

Primary paths:

- `src/tritrack_editing_assistant/run_workflow.py`
- `src/tritrack_editing_assistant/story_fcpxml.py`
- `src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json`
- `src/tritrack_editing_assistant/cli.py`
- `tests/test_run_workflow.py`
- `tests/test_story_fcpxml.py`
- `tests/test_cli.py`

### Task 11 — scoped validation and release-readiness gate

`validate contract|fcpxml|paper|run` is read-only, local, exact-scope, and
path-free. The maintainer gate binds one clean tracked source, scans privacy,
builds and inspects two archive snapshots without generic extraction, verifies
package policy and reproducibility, installs only the chosen local wheel, then
hard-links validated archives before a canonical manifest last. Public CI is
fixed to the declared OS/Python cells and performs no publication.

Primary paths:

- `src/tritrack_editing_assistant/validate_artifacts.py`
- `scripts/release_gate.py`
- `scripts/release_gate_core.py`
- `.github/workflows/ci.yml`
- `tests/test_validate_artifacts.py`
- `tests/test_release_gate.py`
- `tests/test_release_ci.py`
- `tests/test_packaging.py`

## Shared boundaries across all five tasks

Also inspect these shared authorities where needed:

- `src/tritrack_editing_assistant/contracts.py`
- `src/tritrack_editing_assistant/process.py`
- `src/tritrack_editing_assistant/emit_fcpxml.py`
- `src/tritrack_editing_assistant/cli.py`
- `README.md`
- `docs/TOOLING.md`
- `STATUS.md`

Prioritize defects that can violate source immutability, exact-byte binding,
schema closure, no-overwrite publication, symlink/TOCTOU defenses, bounded
reads, offline/privacy claims, deterministic outputs, or manifest authority.
Check whether tests actually exercise the claimed failure boundaries. Do not
report a future feature merely because it is out of scope.

## Known verification

At the target commit:

- 238 complete-suite tests passed locally;
- Ruff, compileall, project identity, both skill validators, public-boundary
  checks, and `git diff --check` passed;
- the local candidate gate passed two-snapshot archive inspection,
  reproducibility policy, fresh-wheel installation, `pip check`, component
  registry, and validator-help smoke checks;
- GitHub Actions run `32095722258` passed all six jobs on Ubuntu 24.04 x64 and
  macOS 26 arm64 across Python 3.12 and 3.13;
- Gemini's Task 7–11 reviews completed without unresolved findings; historical
  Claude timeout attempts are not counted as review evidence.

Known passing tests are context, not proof that no defect exists.

## Non-goals and safety boundary

Do not edit files, execute product operations, inspect another repository,
access credentials or private media, use network services, create a tag,
release, pull request, package publication, artifact upload, tester contact,
Final Cut GUI operation, or application submission.

## Required response

Return `NO FINDINGS` if no actionable current defect is supported. Otherwise
return a concise numbered list. Every finding must contain:

1. severity: `blocker`, `major`, `minor`, or `note`;
2. exact repository-relative file and current line;
3. violated current requirement;
4. concrete reasoning or reproduction path;
5. smallest bounded fix;
6. the test that should fail before and pass after.

Separate optional hardening and future work from current defects. Do not infer
that an old timeout request was or was not delivered, and do not edit files.
