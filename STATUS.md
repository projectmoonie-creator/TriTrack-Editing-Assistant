# Public maintenance status

Updated: 2026-08-18
Project kind: public engine
Lane: `OSS`
Release state: public pre-release source; no tag, package publication, or
tester outreach

## Current gate

Tasks 1–12 are complete in this public candidate. Task 6 began from exact
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

Task 6.5 implementation candidate
`0a99fb65979930385a6a267d596f0baa2ea5aaf3` adds one public invented-media
quickstart from installed `sync` through installed `emit`, exact repeat-output
determinism, strict profile／map／XML checks, conditional local DTD validation,
minimal Python 3.12／3.13 CI, and a three-choice public entry guide without
changing the eleven-component registry. Final verification passed 8 focused,
31 Task 5／6 regression, 77 complete-suite, and 9 boundary tests, plus Ruff,
compilation, identity, skill, installed CLI, and diff gates. One real invented
run passed FFmpeg／FFprobe generation, audio pairing, two deterministic emits,
and the installed FCPXML 1.14 DTD. GitHub Actions run `31848242516` passed the
Python 3.12／3.13 matrix at that exact candidate; its Linux jobs skipped the
Darwin-only real-environment doctor acceptance and made no Final Cut／DTD
claim. The local run did not open Final Cut and makes no GUI import or
round-trip claim. Sanitized evidence is in
`docs/TASK-6.5-VERIFICATION.md`.

Task 7 implementation candidate
`60811a7af117a6dfd70d470513676d87db0922bb` adds fixed-profile CPU-only local
whisper.cpp transcription, strict `transcript-bundle-v1` publication,
deterministic cue canonicalization and silence outcomes, full-batch input
change detection, and atomic no-overwrite output. Final verification passed 37
focused, 100 complete-suite, and 9 boundary tests, plus Ruff, compilation,
identity, skill, installed CLI, schema, real-engine determinism, privacy, and
diff gates. Real invented speech produced byte-identical bundles in two runs;
independently proven digital silence produced an empty zero-cue take. Gemini's
dynamic-model closeout review passed with no findings. The separately
requested Claude subscription review timed out and remains explicitly
incomplete, with no retry or fallback. Sanitized evidence is in
`docs/TASK-7-VERIFICATION.md`.

Task 8 implementation candidate
`4cc25b5248fe67a7cce656f0e810976f18565c16` adds strict cue-addressed
`text-revision-v1` promotion into
provider-neutral `aligned-transcript-v1`, exact-byte source and revision
binding, immutable take／cue timing, input-change detection, and atomic
no-overwrite publication. Its optional `hybrid` command validates one existing
Gemini receipt per revised take, including exact model, bundle／take／audio
binding, request and upload completion, and confirmed server-file deletion,
then invokes the same local promotion core. It performs no provider request,
upload, deletion, subprocess, credential lookup, or network access;
`gemini_transcribe.mjs` remains planned. Sanitized evidence is in
`docs/TASK-8-VERIFICATION.md`.
Local verification passed 43 focused, 126 complete-suite, and 9 boundary
tests, plus Ruff, compilation, identity, skill, installed CLI, registry, and
diff gates.
Gemini's dynamic-model closeout review passed with no findings, test gaps, or
documentation gaps. The separately requested Claude subscription review timed
out and remains explicitly incomplete, with no retry or fallback.

Task 9 post-fix implementation candidate
`cc813f01176c1a9c8d0a0409b2de112ffb9ca8a5` retains the original
`f4e8074936674407e21bab2928701b4c88e6216c` cue-addressed
`grouping-v1`, adds deterministic dual-bound `working-cut-v1` compilation, and
implements the local `paper export`, `paper apply`, and `organize` surfaces.
The XLSX workbook is a four-worksheet editor transport, not an authority:
apply re-derives its complete cue/display grid and public-safe manifest from
the exact aligned bytes, rejects formulas, hyperlinks, unsafe ZIP expansion,
extreme worksheet dimensions, and structural drift, normalizes only
editor-authored text, and returns canonical grouping JSON. Task 9 never
retimes, rewrites, splits, merges, or deletes aligned cues and performs no
network, provider, credential, media, subprocess, FCPXML, or orchestration
operation. Final post-fix local verification passed 53 focused, 155
complete-suite, and 9 boundary tests, plus Ruff, compilation, identity, skill,
installed CLI, round-trip, and diff gates. Both the original and post-fix
Gemini dynamic-model closeout reviews passed with no findings. Both separate
Claude subscription reviews timed out and remain explicitly incomplete, with
no retry or fallback.
The pre-fix review-record candidate
`2edb93e515a62e4f26a6d61f1447e5c605892ec2` matched public `origin/main`, and
GitHub Actions run `31881710301` passed its Python 3.12／3.13 test, lint, and
compile matrix. Post-fix review-record candidate
`f5dc9d5f849c2024fabd44470025ff1ad927ae1b` then matched public `origin/main`,
and GitHub Actions run `31907255236` passed its Python 3.12／3.13 test, lint,
and compile matrix. Sanitized evidence is in `docs/TASK-9-VERIFICATION.md`.

Task 10 implementation candidate
`5fe9a4531f8dbd23f98174023d61f66a359d461b` adds installed
`tritrack run prepare`, `align`, `finish`, and read-only `status` commands.
Each mutating transition publishes a new immutable absent directory with its
manifest hard-linked last; fixed artifact names, exact byte hashes,
phase-specific completed stages, and the prior-manifest chain are validated
before reuse. The final story renderer re-derives every active range and title
from exact aligned／grouping／working-cut authorities, quantizes once to profile
frames, honors paired-source offsets and the declared audio master, excludes
reserve, and emits strict story-ordered FCPXML. Task 10 also installs the
separate end-user `tritrack-editing-assistant` skill with help-first command
discovery and explicit text-revision and paper-edit human gates. The workbook
remains transport only. The workflow makes no network request and does not
claim a Final Cut GUI import, DTD result, or round trip. Sanitized evidence is
in `docs/TASK-10-VERIFICATION.md`.
Local verification passed 193 complete-suite and 9 maintainer-boundary tests,
plus Ruff, compilation, identity, both skill validators, non-editable wheel
help／status smoke, registry, and diff gates.
The frozen closeout target `08517f477ae263664f981c002cc974c77fba291a`
passed Codex's independent review and a completed Gemini review with no
findings. Gemini requested, observed, and completed `gemini-3.7-flash`. The
separate Claude subscription review requested the dynamic `opus` capability
alias, timed out, and remains explicitly incomplete with observed／completed
models null and no retry, downgrade, or fallback.

Task 11 implementation candidate
`ce562e995b63f3f1a29989de3e1ef202da27b5f2` adds the exact four-mode,
read-only `tritrack validate` surface with `contract`, `structural-profile`,
`authority-bound`, and `complete-run-bundle` claim scopes. It also adds a
maintainer-only clean-source privacy and archive-safety gate, two-snapshot
package reproducibility checks, fresh local-wheel installation smoke, a closed
manifest-last receipt, exact Python／build constraints, and fixed public CI on
Ubuntu 24.04 x64 and macOS 26 arm64 across Python 3.12／3.13. The eleven-entry
component registry is unchanged.
Local verification in a new Python 3.13 environment passed 69 focused and 235
complete-suite tests, Ruff, compilation, identity, both skill validators,
package-member policy, and Git cleanliness. The implementation gate passed
with byte-identical wheels, identical normalized sdist member inventories,
and an installed-wheel `pip check` plus five validator help smokes. Sanitized
evidence and exact hashes are in `docs/TASK-11-VERIFICATION.md`.
Task 11 made no tag, release, package publication, pull request, tester contact,
artifact upload, signing, attestation, SBOM, Final Cut GUI, DTD, live provider,
credential, or application-submission claim.

Task 12 `alphaReviewTarget`
`283ec9f7018a497aa77ad54c53f380a4bc426031` freezes the complete public alpha
composition under the producer-approved two-layer Git design. Fix-forward
review added bounded sync-map loading, streaming release-command capture,
nonblocking regular-file validation across runtime and distributed scripts,
descriptor-bound transcription／WAV／CLI hashing, bounded Basic Title inputs,
and a policy-owned fixed package epoch. The final clean target passed 252
tests, Ruff, compilation, identity, both skill validators, public-content and
package gates, plus the full release gate with reproducible wheel bytes and
normalized sdist contents.

Codex's final independent review returned no current finding. Gemini requested,
observed, and completed `gemini-3.7-flash` and returned no product finding; its
overbroad inspection-record claims are not used as evidence. Claude's single
final subscription-only attempt requested the dynamic `opus` capability alias
and ended `claude-timeout`; observed／completed model, output, and usage remain
absent. It was not retried, downgraded, substituted, or sent through a paid
route. The later `alphaEvidenceRecord` contains only package-excluded public
evidence, verification, this status, and the maintainer-boundary regression;
its exact identity is supplied by Git rather than self-referenced inside its
own bytes. Complete evidence is in `docs/TASK-12-VERIFICATION.md`.

Task 12 makes no tag, GitHub Release, package publication, pull request, tester
contact, signing, attestation, SBOM, Final Cut GUI, DTD, live provider,
application-submission, production-stability, or Task 13 claim.

A 2026-08-18 Claude coverage audit found eight historical Task 7–11 attempts
that ended `claude-timeout` after preflight with ambiguous dispatch and no
usable result. The registered OAuth preflight repair is not the same failure:
a separate Task 9 design review completed through that repaired subscription
lane. One new concise recovery review against current public `main` was sent
once through the approved wrapper and also ended at its hard timeout, with no
observed／completed model or raw result. It was not retried, downgraded, or sent
through a paid／alternate route. The public inventory, comparison, packet, and
attempt ledger are preserved in
`docs/reviews/claude-incomplete-audit-2026-08-18.md` and the matching
`tasks-7-11-claude-recovery-*` records.

A later producer-mediated interactive Claude Code review against public
`main` commit `7ae540a1ab46de39b31d826ae99752b325e6e9e1` returned
`NO FINDINGS` plus four optional hardening observations. Fix-forward commit
`eaa17b49c9100bf92452106c1de23392a2831ae5` maps third-party workbook parser
`ValueError` failures to the stable public code, makes current working-cut
claims precisely `transcript-text-free`, and adds direct noncanonical
working-cut regression coverage. The hypothetical inner-pipe engine-token
observation was not accepted without a supported token or failing contract.
The complete suite passed 240 tests; Ruff, compilation, project identity, both
skill validators, and diff checks also passed. The interactive session's model
and usage provenance remain self-reported, and the result does not convert any
earlier wrapper timeout or ambiguous dispatch into formal completion. Public
review and adjudication records are in `docs/reviews/tasks-7-11-claude-manual-*`.

## Next action

Task 13 proves the public engine as the generic authority and defines a
deliberate downstream integration seam. Task 12 does not authorize or claim
tags, releases, package publication, tester contact, private integration, or
application submission.

## Implemented surface

- clean Python package and eleven-component status registry;
- Draft 2020-12 contracts loaded from installed package resources;
- bounded argv-only subprocess execution and sanitized receipts;
- audio-verified A/B synchronization with atomic `sync-map-v1` publication;
- profile-bound deterministic string-out and atomic FCPXML 1.14 publication;
- fixed-profile CPU-only local transcription with strict deterministic bundle
  canonicalization and atomic no-overwrite publication;
- deterministic cue-addressed text promotion with immutable local timing and
  exact-byte provenance;
- optional offline Gemini receipt conformance that shares the local promotion
  core and performs no network access;
- cue-addressed grouping with deterministic working-cut compilation;
- strict local paper-edit export/apply with complete aligned-grid
  re-derivation, semantic round trips, and atomic no-overwrite publication;
- immutable prepared／aligned／finished run bundles with exact manifest chains,
  fixed artifacts, manifest-last publication, and read-only status;
- deterministic story-ordered FCPXML projection from exact editor authorities;
- separate installed end-user editing skill with two explicit human gates;
- four-mode read-only artifact validation with scope-limited path-free
  summaries;
- clean tracked-source privacy, bounded archive inspection, reproducible
  packaging, fresh-wheel installation, and manifest-last local candidate gate;
- fixed Ubuntu／macOS and Python 3.12／3.13 release-grade public CI;
- fail-closed `doctor` command;
- exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
- public Basic Title binding with invented-content Final Cut round-trip
  evidence;
- public invented-media synchronization-to-FCPXML quickstart with deterministic
  repeat emission, conditional local DTD verification, and minimal CI.

The network-capable `gemini_transcribe.mjs` component remains planned.

## Custody

The public `origin` is
`https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`.
Closeout requires verifying that its `main` SHA exactly matches the local green
candidate, making the GitHub copy the off-device Git backup. Tags, releases,
pull requests, tester contact, package publication, and application submission
have not yet been granted. All grants follow the standing-authorization model
in `AGENTS.md`.
