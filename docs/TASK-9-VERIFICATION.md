# Task 9 verification

Date: 2026-08-15

Candidate implementation: `f4e8074936674407e21bab2928701b4c88e6216c`

## Public scope proven

Task 9 implements three local-only commands:

- `tritrack paper export` creates a strict four-worksheet XLSX transport from
  exact aligned transcript bytes, optionally prefilled from canonical grouping
  intent;
- `tritrack paper apply` re-derives the complete cue reference grid and hidden
  manifest before publishing canonical `grouping-v1`; and
- `tritrack organize` compiles exact aligned and grouping bytes into a
  deterministic, dual-bound, text-free `working-cut-v1`.

The commands make no network access, provider request, credential lookup,
media-processing call, subprocess invocation, FCPXML emission, or Task 10
orchestration call. All tracked fixtures and tests use invented content.

## Preserved RED-to-GREEN evidence

- Contract RED: the tightened grouping fixture failed against the old schema
  and `working-cut-v1` returned `TRITRACK_CONTRACT_UNKNOWN`. GREEN added the
  strict Draft 2020-12 resources and package registry entry.
- Organizer RED: `organizer.py` was absent. GREEN covers canonical aligned
  indexing, exact hash binding, unique IDs, order permutations, completed-take
  spans, single cue assignment, copied timing/source hashes, deterministic
  bytes, late mutation, output conflicts, and hard-link races.
- Paper export RED: `paper_edit.py` was absent. GREEN covers the exact four
  worksheets, complete cue grid, hidden manifest, grouping projection, literal
  formula-looking transcript display, and absent-output publication.
- Paper apply RED: `apply_workbook()` was absent. GREEN covers formula and
  structural rejection, complete grid/manifest re-derivation, editor-text
  normalization, reference immutability, symlink/ZIP/input-change boundaries,
  deterministic grouping bytes, and publication races.
- CLI RED: `paper` had no nested commands and both Task 9 components remained
  planned. GREEN exposes the three exact help authorities, stable exit classes,
  sanitized summaries, and an unchanged eleven-component registry.

## Semantic round trips

1. **Grouping fixpoint:** applying a workbook exported from one canonical
   grouping publishes bytes identical to that grouping.
2. **Edited workbook normalization:** two exports from the normalized grouping
   have identical logical cell grids even though XLSX ZIP bytes are not claimed
   deterministic; applying either returns the same grouping bytes.
3. **Structural transcript immutability:** grouping contains no transcript,
   source-hash, or timing authority, and organizer copies every emitted source
   hash and millisecond boundary only from the exact aligned artifact.

## Local verification state

The coherent implementation and governance package passed:

- 49 focused contract, organizer, paper-edit, and CLI tests;
- 151 complete-suite tests;
- Ruff over `src`, `tests`, and `examples`;
- Python compilation over `src`, `tests`, and `examples`;
- project identity with `ok: true`, kind `public-engine`, and lane `OSS`;
- the current Codex skill validator for the public maintainer skill; and
- `git diff --check`.

A non-editable local wheel installation exposed all three installed help
surfaces and the unchanged eleven-component registry. One invented installed
round trip exported two cues including literal formula-looking display text,
normalized one question and selection into grouping, compiled one working-cut
segment, produced equal re-exported logical grids, and returned the same
grouping bytes from both re-applies. Its grouping SHA-256 was
`6b6b0736391ca349ea2d3453557c58dc9facb84bbe312f7e2b5f83664ddad145`.

## Independent closeout review

The frozen full-diff packet has SHA-256
`4c764db444dd2df246f3cc86ec03cc710e650013ec9981825c19cd25d8122630`.
Gemini dynamically requested, observed, and completed
`gemini-3.7-flash`; it returned `PASS` with no findings, test gaps, or
documentation gaps across all seven requested dimensions.

The separate Claude Code subscription lane requested the dynamic `opus`
capability alias but hit its hard timeout. Its observed and completed model
fields are null and its result remains explicitly incomplete. It was not
retried, downgraded, or replaced by a paid credential/API fallback. The
provider ledgers and local adjudication are preserved under `docs/reviews/`;
this record does not claim two completed reviews.

Remote CI and exact remote-main custody are not claimed in this local-evidence
section; they are recorded only after those separate gates actually complete.
No Final Cut GUI import, DTD validation, tag, release, package publication,
tester contact, or application submission is claimed by Task 9.
