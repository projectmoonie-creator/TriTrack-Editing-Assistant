# Tasks 7–11 Claude manual-review adjudication

Adjudication date: 2026-08-18

## Review boundary

The producer-mediated Claude Code review completed against public `main`
commit `7ae540a1ab46de39b31d826ae99752b325e6e9e1` and returned `NO FINDINGS`.
Its exact response SHA-256 is
`ffd6a408fd755ede13c5e1c5946f9aeef09a4449737edcba8416c0870ca47d09`.
The response reports `claude-opus-5[1m]`; the formatting residue is retained,
usage is unverified, and neither field is upgraded to audit-wrapper proof.

The review is independent useful evidence, but it is not a replay or
completion of any prior wrapper attempt. All historical `claude-timeout`
records keep their original incomplete and ambiguous-dispatch state.

## Observation-by-observation adjudication

### M-1 — `upgrade`／minor: third-party workbook errors could escape the stable code

Reproduction replaced `openpyxl.load_workbook` with a function that raises
`ValueError("untrusted parser detail")`. The frozen implementation propagated
that raw value, allowing a non-`TRITRACK_` string to become the CLI code.

Fix: ZIP preflight validation remains in its own exception boundary so its
stable sentinel passes unchanged. `load_workbook` now has a separate boundary
that maps its `ValueError` to `TRITRACK_PAPER_WORKBOOK_INVALID`.

RED: `test_maps_openpyxl_value_errors_to_the_stable_workbook_code` received
the raw parser detail. GREEN: it receives only the stable workbook code.

### M-2 — `agree`／test gap: noncanonical working-cut behavior lacked direct coverage

The implementation already applies the same canonical-byte check to grouping
and working-cut authorities. A new regression supplies noncanonical
`working-cut-v1` bytes and proves that story validation returns
`TRITRACK_STORY_WORKING_CUT_NONCANONICAL`.

This test was green before any product-code edit, so the item remains a
coverage gap rather than an implementation defect.

### M-3 — `upgrade`／minor: “text-free” overstated the artifact guarantee

The working cut intentionally excludes transcript text but retains
editor-authored question, reason, and note fields. The old phrase was therefore
broader than the schema and implementation contract.

Fix: current public working-cut claims in the organizer docstring, README, and
Task 9 verification record now say `transcript-text-free`. A maintainer-boundary
test prevents the broader current claim from returning.

RED: the boundary test found current “text-free working cut” wording. GREEN:
all current claims use the precise transcript-qualified form.

### M-4 — `reject`: no supported inner-pipe engine token is known

The observation is hypothetical and identifies no whisper.cpp token, current
input, failing behavior, or upstream contract requiring an inner pipe. A wider
pattern could also reject legitimate transcript text. The current exact known
token boundary therefore remains unchanged. A concrete supported token or
source-backed engine contract would justify reopening this decision.

## Verification state

The focused RED／GREEN evidence and complete repository verification are
recorded in the final Task 11 closeout. No optional observation was accepted
without either a reproduction or a narrowly scoped coverage assertion.
