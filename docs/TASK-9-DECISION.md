# Task 9 organizer and paper-edit decision

Decision date: 2026-08-15

Decision owner: producer

Selected option: A — paper-first compiler with JSON authority

## Decision

Task 9 adds a local, cue-addressed paper-edit round trip and a separate
organizer compiler. The workbook is an editor-facing transport, not an
authority. Strict JSON artifacts remain the deterministic, versioned authority
for editor intent and the compiled working cut.

The accepted flow is:

```text
aligned-transcript-v1
        │
        ├── paper export ──> paper-workbook-v1.xlsx
        │                         │
        │                    editor changes
        │                         │
        └── paper apply  <────────┘
                 │
                 v
            grouping-v1
                 │
                 └── organize ──> working-cut-v1
```

`paper export` may also consume an existing `grouping-v1` to prefill a
workbook. This closes the round trip without requiring an editor to hand-write
cue identifiers before a workbook exists.

Task 8 remains the immutable timing and transcript authority. Task 9 does not
retime, split, merge, delete, rewrite, or align cues. A Task 9 segment is an
inclusive, contiguous cue span inside one completed take. Mid-cue trims and
word-level selections remain outside the public alpha.

## Public command surface

Task 9 implements these exact local commands:

```text
tritrack paper export \
  --aligned ALIGNED.json \
  [--grouping GROUPING.json] \
  --output PAPER.xlsx \
  [--json]

tritrack paper apply \
  --aligned ALIGNED.json \
  --workbook PAPER.xlsx \
  --output GROUPING.json \
  [--json]

tritrack organize \
  --aligned ALIGNED.json \
  --grouping GROUPING.json \
  --output WORKING-CUT.json \
  [--json]
```

Nested `export` and `apply` subcommands are required because their inputs and
outputs are disjoint. A mode flag would permit nonsensical argument
combinations and make the help surface ambiguous.

All three commands are local and network-free. They perform no provider call,
credential lookup, media processing, subprocess invocation, transcript
generation, FCPXML emission, or Task 10 orchestration.

## `grouping-v1` editor-intent authority

The existing pre-release `grouping-v1` contract is tightened in place. It has
no implemented consumer and Task 8 established the same in-place tightening
precedent for another unused pre-release contract. A fictitious migration to
`grouping-v2` is therefore not introduced.

The contract binds to the SHA-256 of the exact `aligned-transcript-v1` bytes and
contains only editor intent:

```json
{
  "schemaVersion": "tritrack.grouping/v1",
  "alignedTranscriptSha256": "<64 lowercase hex>",
  "questions": [
    {
      "id": "question-001",
      "question": "What changed?",
      "order": 1,
      "answers": [
        {
          "id": "answer-001",
          "order": 1,
          "takeId": "Take-A.wav",
          "startCueId": "cue-000001",
          "endCueId": "cue-000003",
          "note": "Optional editor note"
        }
      ]
    }
  ],
  "reserve": [
    {
      "id": "reserve-001",
      "order": 1,
      "takeId": "Take-B.wav",
      "startCueId": "cue-000004",
      "endCueId": "cue-000004",
      "reason": "Alternate answer",
      "note": "Optional editor note"
    }
  ]
}
```

The JSON Schema uses Draft 2020-12, rejects unknown fields, requires safe
path-free identifiers and lowercase SHA-256 values, bounds all editor-authored
text, and makes `note` optional. Millisecond values and transcript text do not
appear in this intent artifact, so the editor cannot create a second timing or
transcript authority.

Semantic validation additionally requires:

- the exact aligned artifact hash to match;
- unique question, answer, and reserve IDs;
- question orders to be the permutation `1..N`;
- answer orders to be `1..N` inside each question;
- reserve orders to be `1..N` globally;
- at least one question and at least one answer per question;
- every span to address one completed take by `(takeId, cueId)`;
- `startCueId` through `endCueId` to be inclusive and contiguous in the take's
  canonical cue-array order;
- no cue to appear in more than one answer or reserve span; and
- omitted aligned cues to remain valid and unchanged.

The single-assignment rule deliberately prevents duplicated source material in
the first public working-cut contract. Cue reuse is deferred rather than
silently inferred.

Question text, reserve reasons, and notes are NFC-normalized, have leading and
trailing whitespace removed, collapse internal whitespace, reject control
characters, and obey explicit length limits. Directly authored grouping JSON
must already be canonical; `organize` validates it without rewriting it.

## `working-cut-v1` compiled authority

`organize` validates the exact aligned and grouping bytes, resolves every cue
span, and publishes a new deterministic `working-cut-v1` JSON artifact. It is
dual-bound to both exact inputs:

```json
{
  "schemaVersion": "tritrack.working-cut/v1",
  "organizationProfileId": "cue-addressed-question-groups-v1",
  "alignedTranscriptSha256": "<64 lowercase hex>",
  "groupingSha256": "<64 lowercase hex>",
  "questions": [
    {"id": "question-001", "question": "What changed?", "order": 1}
  ],
  "segments": [
    {
      "id": "answer-001",
      "storyOrder": 1,
      "questionId": "question-001",
      "takeId": "Take-A.wav",
      "sourceSha256": "<64 lowercase hex>",
      "startCueId": "cue-000001",
      "endCueId": "cue-000003",
      "startMs": 0,
      "endMs": 3200,
      "note": "Optional editor note"
    }
  ],
  "reserve": [
    {
      "id": "reserve-001",
      "order": 1,
      "takeId": "Take-B.wav",
      "sourceSha256": "<64 lowercase hex>",
      "startCueId": "cue-000004",
      "endCueId": "cue-000004",
      "startMs": 4500,
      "endMs": 5200,
      "reason": "Alternate answer",
      "note": "Optional editor note"
    }
  ]
}
```

Active `segments` are flattened in question order and then answer order;
`storyOrder` is the derived global permutation `1..N`. Millisecond boundaries
and source hashes are copied only from the aligned authority. Transcript text
is not copied, preventing a second text authority. Task 10 can consume the flat
ordered seam while reopening the exact aligned artifact for authoritative cue
text.

The same exact aligned and grouping bytes must produce byte-identical canonical
JSON, using sorted keys and one final newline. Inputs are rehashed before atomic
publication. Existing outputs and race winners are never overwritten.

## Workbook contract

`paper-workbook-v1` is an `.xlsx` transport with exactly four worksheets:

### `Cues`

One row per cue from completed aligned takes, ordered by canonical take order
and cue order.

| Column | Class | Apply behavior |
| --- | --- | --- |
| `TakeId` | identity | must exactly match the re-derived grid |
| `SourceSha256` | identity | must exactly match the aligned take |
| `CueId` | identity | must exactly match `(takeId, cueId)` |
| `StartMs` | identity | must exactly match aligned timing |
| `EndMs` | identity | must exactly match aligned timing |
| `Text` | immutable display | must match aligned text; never imported |
| `Disposition` | immutable display | must match aligned disposition; never imported |

Full reference-grid equality detects row insertion, deletion, reordering,
identity edits, and misleading display edits. Display columns help the editor
make decisions but never enter JSON authority; they are compared only to the
aligned authority. Workbook sheet protection, if present for usability, is
never described or relied upon as a security control.

### `Questions`

The editor authors `QuestionId`, `Question`, and `Order`. Blank trailing rows
are ignored. Nonblank partial rows fail closed.

### `Selections`

Each row describes one answer or reserve segment. Editable columns are:

| Column | Required behavior |
| --- | --- |
| `Placement` | exact enum `ANSWER` or `RESERVE` |
| `SegmentId` | safe unique ID |
| `QuestionId` | required for `ANSWER`; empty for `RESERVE` |
| `Order` | positive integer, validated in its question or reserve list |
| `TakeId` | must address one completed aligned take |
| `StartCueId` | inclusive start cue in the declared take |
| `EndCueId` | inclusive end cue in the declared take |
| `ReserveReason` | required for `RESERVE`; empty for `ANSWER` |
| `EditorNote` | optional canonical editor text |

Blank trailing rows are ignored; partially populated rows fail closed. A
prefilled export is a direct projection of one strict grouping artifact.

### `_TriTrack`

The hidden manifest records only public-safe identity metadata:

- workbook schema version `tritrack.paper-workbook/v1`;
- tool version;
- exact aligned-transcript SHA-256; and
- SHA-256 of the canonical complete `Cues` reference grid.

The hidden state is a usability aid, not a security boundary. `paper apply`
re-derives and verifies all values from the supplied aligned artifact.

## Workbook safety and failure behavior

Workbook parsing uses formulas as formulas (`data_only=False`) and rejects any
formula cell anywhere in the accepted sheets. It also rejects unexpected or
missing sheets, merged cells, unexpected defined names, external links,
cell hyperlinks, macros, malformed cell types, duplicate IDs, duplicate or
gapped ordering, foreign cue addresses, non-contiguous spans, overlapping
assignments, noncanonical text, and a manifest or reference-grid mismatch.

Export writes text cells explicitly as strings and uses text number formats for
identifiers to reduce spreadsheet coercion. Formula-looking transcript text is
display-only and must be serialized as a literal string, never as a formula.

Workbook and JSON inputs have independent declared size limits, must be regular
non-symlink files, and are hashed before and after parsing. Workbook ZIP member
count and expanded sizes are bounded before openpyxl parsing. Worksheet rows
and columns are capped from the exact aligned cue count before rectangular
cell inspection. Any change before publication fails closed. Workbook export
and both JSON writers publish only to absent paths through the existing
temporary-file plus hard-link race boundary, with cleanup after success or
failure.

Command summaries contain only schema version, bounded counts, and artifact
SHA-256. They never print transcript text, question text, notes, filenames, or
absolute paths.

## Round-trip invariants

XLSX byte identity is explicitly not promised. A scratch openpyxl probe on the
selected dependency produced different ZIP bytes for two logically identical
workbooks while all cell grids remained equal; 11 ZIP members differed.
Formula cells loaded as formula strings with `data_only=False` and as null
without a cached result under `data_only=True`, so apply must use the former and
reject formulas rather than trusting cached values.

Task 9 instead proves three semantic invariants:

1. **Grouping fixpoint:** for every canonical grouping `G` valid against exact
   aligned bytes `A`, `paper apply(A, paper export(A, G))` publishes bytes
   identical to `G`.
2. **Edited-workbook normalization:** for every human-edited workbook `W` that
   apply accepts, if `G = paper apply(A, W)`, then repeated
   `paper export(A, G)` operations have identical logical grids and every
   subsequent apply publishes bytes identical to `G`.
3. **Structural transcript immutability:** apply and organize cannot publish a
   take, cue, source hash, or millisecond boundary not re-derived from `A`.

## Error boundaries

The commands retain the project's stable CLI exit classes:

- malformed CLI intent returns usage;
- invalid schema, workbook state, foreign identity, or semantic conflict
  returns data;
- missing or unreadable parents and file I/O failures return I/O;
- an existing output or publication race returns output-exists; and
- no failure prints a traceback or creates a partial output.

Validation errors use stable `TRITRACK_*` prefixes. Exact codes are frozen in
the implementation plan and tests, not invented ad hoc by individual call
sites.

## Deferred alternatives and non-goals

- organize-first hand-authored JSON as the only way to bootstrap a workbook;
- direct workbook-to-working-cut compilation with no durable grouping intent;
- XLSX as an authoritative or byte-deterministic artifact;
- mid-cue, word-level, or frame-level trims;
- cue reuse in multiple story positions;
- transcript text editing, cue retiming, merge, split, or deletion;
- automatic semantic question classification;
- provider calls, credentials, upload, or model selection;
- FCPXML emission from the working cut;
- Task 10 orchestration or end-user skill creation; and
- tags, releases, pull requests, tester contact, package publication, or
  application submission.

## Verification target

Implementation acceptance must preserve observed RED-to-GREEN evidence for:

- tightened grouping and new working-cut contracts;
- pure organizer compilation and every semantic rejection above;
- workbook export, apply, prefill, literal formula-looking display text,
  formula rejection, complete reference-grid re-derivation, and exact grouping
  fixpoint;
- logical-grid idempotence without XLSX byte claims;
- regular-file and size boundaries, exact input hashes, late input mutation,
  absent-output publication, races, cleanup, source immutability, and sanitized
  summaries;
- installed CLI help and the unchanged eleven-component registry; and
- invented fixtures only.

Closeout additionally requires focused and complete tests, Ruff, compilation,
project identity, maintainer-skill validation, public-boundary tests,
`git diff --check`, installed invented acceptance, convergent independent
review with fix-forward, minimal CI, and exact public remote-main SHA backup
verification.

## Brainstorm provenance

The frozen public problem packet SHA-256 was
`992b621a93955277455b99aa9005ae4250f0727397b9ed9dfe30091e9be95727`.

Codex froze its independent first round before reading other answers. Gemini
requested, observed, and completed `gemini-3.7-flash`; its response SHA-256 was
`c05d6967ef4ffe4a1b56f1c4cccb62ff52c397d9806700d7ee18bc9415ac26b9`.
Claude requested the dynamic `opus` capability alias and completed with
`claude-opus-5`; attempt `a68cdd57-889f-4cdc-8f5e-46383c8ec356` and response
SHA-256
`e71764b0ce60caf3503865bbce1293a171e69f8c11f5821451564895ac2a761c`
record the exact completed lane. The producer selected option A on
2026-08-15.
