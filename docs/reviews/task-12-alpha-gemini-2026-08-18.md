# Task 12 public alpha independent review

## Summary

**NO FINDINGS** (0 blockers, 0 majors, 0 minors).

The complete public alpha composition at target commit `283ec9f7018a497aa77ad54c53f380a4bc426031` meets all design invariants, strict contract boundaries, fail-closed security properties, descriptor-level IO safety bounds, process-group confinement, reproducibility contracts, and role-firewall requirements across Tasks 1–12.

---

## Detailed evaluation by review dimension

### 1. Component registry and implementation truth
- The machine-readable component registry in `src/tritrack_editing_assistant/cli.py` lists exactly eleven entries (`sync_scan.py`, `emit_fcpxml.py`, `transcribe_takes.py`, `string_out.py`, `hallucination.py`, `organizer.py`, `paper_edit.py`, `align_text.py`, `gemini_hybrid.py`, `gemini_transcribe.mjs`, and `multicam-sync`).
- Implementation truth is accurately maintained: `gemini_transcribe.mjs` is marked `planned` while the other ten components are marked `implemented`.
- Supporting utilities (`contracts`, `doctor`, `process`, `run_workflow`, `validate_artifacts`, schemas, release tools) do not artificially inflate the registry.

### 2. Authority ownership and projections
- The JSON authorities maintain strict unidirectional roles:
  - `sync-map-v1`: authoritative for A/B alignment offsets and audio master designation.
  - `transcript-bundle-v1`: authoritative for initial take basenames, source audio hashes, and millisecond cue timings.
  - `text-revision-v1`: authority for cue-addressed textual modifications, binding to the exact SHA-256 of the source bundle.
  - `aligned-transcript-v1`: unified textual authority preserving baseline timestamps.
  - `grouping-v1`: authority for editor narrative intent (questions, story order, and reserve), containing zero transcript text or millisecond timestamps.
  - `working-cut-v1`: selection authority compiled from grouping and aligned transcript.
  - `run-manifest-v1`: immutable stage-fact authority binding artifact hashes and manifest chains.
- Workbooks (`paper-edit.xlsx`) and Final Cut Pro XMLs (`string-out.fcpxml`, `story-cut.fcpxml`) remain strict transports and projections; neither creates an alternate source of timing or transcript truth.

### 3. Local-first, offline, privacy, and subprocess boundaries
- The default execution path is entirely local and offline. `hybrid` operates strictly as an offline conformance check on pre-existing `provider-receipt-v1` artifacts without network access, credentials, or remote endpoints.
- Subprocess execution (`process.py`, `release_gate_core.py`) is bounded:
  - Strict argv arrays without shell interpolation.
  - Execution deadline enforcement and streaming output-size bounds using `selectors.DefaultSelector`.
  - Process group detachment (`start_new_session=True`) with POSIX group termination (`SIGTERM` followed by `SIGKILL` grace) ensuring runaway processes or streaming emitters cannot hang execution or exceed memory caps.
- Privacy scanning (`scan_public_bytes`) rejects unredacted macOS, Linux, and Windows home-directory prefixes, mounted-volume prefixes, private keys, and credential shapes across source files and archive members.
- Readers use `O_RDONLY | O_NONBLOCK | O_CLOEXEC | getattr(os, "O_NOFOLLOW", 0)` with pre- and post-read descriptor verification (`fstat`), eliminating blocking open risks on special device files or FIFOs and defending against symlink race attacks.

### 4. Determinism, canonical bytes, timing, and cross-binding
- Frame timing conversion is quantized deterministically using `fractions.Fraction` and half-away-from-zero rounding on exact rationals (`1001/30000s`), avoiding binary floating-point accumulation.
- JSON serialization uses canonical ordering (`sort_keys=True`, UTF-8, trailing newline).
- Cross-artifact bindings explicitly check input hashes before and after transformations (`verify_artifact_unchanged`, `_require_inputs_unchanged`, `_require_bundle_unchanged`), rejecting TOCTOU drift.

### 5. Validator scopes, stable errors, and read-only behavior
- `validate_artifacts.py` and CLI subcommands implement four explicit validation scopes:
  - `contract`: validates JSON schema compliance against packaged Draft 2020-12 schemas.
  - `structural-profile`: validates FCPXML structure against profile and title-binding definitions without invoking DTD or external GUIs.
  - `authority-bound`: validates workbook integrity and bidirectional consistency against the exact aligned transcript authority.
  - `complete-run-bundle`: validates immutable bundle completeness, file counts, and manifest hash chains.
- All validators are strictly read-only, produce path-free summaries, and fail closed with sanitized error codes.

### 6. Run-bundle chains and manifest-last publication
- Bundle generation (`run prepare`, `run align`, `run finish`, `publish_release`) stages files into temporary directories and hard-links output artifacts before linking `run-manifest.json` or `release-manifest.json` as the final atomic action.
- A missing manifest or interrupted write renders a bundle invalid and unrepairable in-place, requiring a clean run to an absent target directory.
- `manifestChain` arrays enforce strict multi-stage provenance (`prepared` $\rightarrow$ `aligned` $\rightarrow$ `finished`).

### 7. Package reproducibility and release gate
- `package-policy-v1.json` defines a fixed `sourceDateEpoch: 1704067200`.
- The maintainer gate (`scripts/release_gate_core.py`) verifies dual snapshot builds:
  - Exact wheel byte identity (`wheelBytesMatch: true`).
  - Normalized sdist member and content inventory identity (`sdistMembersMatch: true`).
  - Fresh-environment installation smoke exercising `pip check`, component listing, and all five validator help commands.

### 8. Fixed CI contract
- CI workflow `.github/workflows/ci.yml` pins Actions to immutable full commit SHAs, sets top-level `permissions: contents: read`, runs across the exact Ubuntu 24.04 / macOS 26 and Python 3.12 / 3.13 matrix, and publishes no artifacts or tags.

### 9. Documentation, compatibility, and role firewall
- Clear firewall separation is maintained between maintainer instructions (`.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md`) and user-facing guidance (`skills/tritrack-editing-assistant/SKILL.md`).
- Compatibility claims explicitly scope to macOS 26.5.2, Final Cut Pro 12.3, FCPXML 1.14, UHD 3840x2160 29.97 NDF Rec. 709 stereo 48 kHz, without claiming unverified GUI automation or live provider operation.

### 10. Seam and regression test coverage
- Unit and regression suites thoroughly exercise error paths, non-blocking descriptor boundaries, FIFO rejection, oversized payload truncation, XML entity injection, and atomic publication failure recovery.

---

## Optional observations

1. **Non-POSIX `os.O_NONBLOCK` fallback**:
   On POSIX platforms, `getattr(os, "O_NONBLOCK", 0)` effectively prevents blocking on FIFOs during `os.open`. On non-POSIX environments (e.g. native Windows without FIFO support), `O_NONBLOCK` evaluates to 0, which is benign given named pipes in Windows operate under distinct system semantics.
2. **Fixed `sourceDateEpoch` in Package Policy**:
   Decoupling `SOURCE_DATE_EPOCH` from commit timestamp into explicit policy configuration (`1704067200`) ensures that package-excluded evidence additions in subsequent Task 12 commits maintain bit-level wheel reproducibility.

---

## Inspection record

- **Target commit**: `283ec9f7018a497aa77ad54c53f380a4bc426031`
- **Files inspected**:
  - `pyproject.toml`
  - `MANIFEST.in`
  - `package.json`
  - `.tritrack-project.json`
  - `AGENTS.md`
  - `README.md`
  - `STATUS.md`
  - `SECURITY.md`
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `NOTICE`
  - `LICENSE`
  - `PRODUCT-WISHES.md`
  - `requirements/ci-constraints.txt`
  - `release/package-policy-v1.json`
  - `release/release-manifest-v1.schema.json`
  - `.github/workflows/ci.yml`
  - `.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md`
  - `.agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py`
  - `skills/tritrack-editing-assistant/SKILL.md`
  - `skills/tritrack-editing-assistant/agents/openai.yaml`
  - `docs/ROADMAP.md`
  - `docs/TOOLING.md`
  - `docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md`
  - `docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md`
  - `scripts/capture_basic_title_binding.py`
  - `scripts/release_gate.py`
  - `scripts/release_gate_core.py`
  - `src/tritrack_editing_assistant/__init__.py`
  - `src/tritrack_editing_assistant/align_text.py`
  - `src/tritrack_editing_assistant/cli.py`
  - `src/tritrack_editing_assistant/contracts.py`
  - `src/tritrack_editing_assistant/doctor.py`
  - `src/tritrack_editing_assistant/emit_fcpxml.py`
  - `src/tritrack_editing_assistant/gemini_hybrid.py`
  - `src/tritrack_editing_assistant/hallucination.py`
  - `src/tritrack_editing_assistant/organizer.py`
  - `src/tritrack_editing_assistant/paper_edit.py`
  - `src/tritrack_editing_assistant/process.py`
  - `src/tritrack_editing_assistant/run_workflow.py`
  - `src/tritrack_editing_assistant/story_fcpxml.py`
  - `src/tritrack_editing_assistant/string_out.py`
  - `src/tritrack_editing_assistant/sync_scan.py`
  - `src/tritrack_editing_assistant/transcribe_takes.py`
  - `src/tritrack_editing_assistant/validate_artifacts.py`
  - `src/tritrack_editing_assistant/profiles/basic-title-v1.json`
  - `src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json`
  - `src/tritrack_editing_assistant/schemas/*.json` (all 10 schema definitions)
  - `tests/test_align_text.py`
  - `tests/test_cli.py`
  - `tests/test_contracts.py`
  - `tests/test_doctor.py`
  - `tests/test_emit_fcpxml.py`
  - `tests/test_gemini_hybrid.py`
  - `tests/test_hallucination.py`
  - `tests/test_maintainer_boundary.py`
  - `tests/test_organizer.py`
  - `tests/test_packaging.py`
  - `tests/test_paper_edit.py`
  - `tests/test_process.py`
  - `tests/test_quickstart_demo.py`
  - `tests/test_release_ci.py`
  - `tests/test_release_gate.py`
  - `tests/test_run_workflow.py`
  - `tests/test_story_fcpxml.py`
  - `tests/test_string_out.py`
  - `tests/test_sync_scan.py`
  - `tests/test_title_binding.py`
  - `tests/test_transcribe_takes.py`
  - `tests/test_validate_artifacts.py`
