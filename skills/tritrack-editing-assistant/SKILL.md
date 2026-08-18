---
name: tritrack-editing-assistant
description: Guide an editor or terminal-capable agent through TriTrack's installed, local Final Cut workflow. Use when preparing synchronized A/B interview media, reviewing cue-addressed transcript corrections, organizing an edit in the paper workbook, finishing a story-ordered FCPXML, or checking an immutable run bundle.
---

# TriTrack Editing Assistant

Guide the edit through explicit immutable stages. Keep media and editorial
artifacts local, preserve editor intent, and use only the installed `tritrack`
command surface.

## Start help-first

1. Run `tritrack run --help`.
2. Run the selected subcommand's `--help` before naming or using its flags:
   - `tritrack run prepare --help`
   - `tritrack run align --help`
   - `tritrack run finish --help`
   - `tritrack run status --help`
   - `tritrack validate --help`
   - `tritrack validate contract --help`
   - `tritrack validate fcpxml --help`
   - `tritrack validate paper --help`
   - `tritrack validate run --help`
3. Treat installed help as the command authority. Stop if a required command or
   flag is unavailable; do not guess a replacement.

## Preserve local custody

- Keep source media, the local speech model, JSON artifacts, workbook, and
  FCPXML on paths the editor explicitly places in scope.
- Require globally unique media basenames across camera A and camera B.
- Choose only declared camera sources for transcription.
- Use a new absent output directory for every mutating stage. Never overwrite,
  repair, resume, or add files inside an earlier bundle.
- Read sanitized command summaries by default. Inspect transcript or workbook
  content only when the editor explicitly puts that artifact in scope.

## Prepare the synchronized run

Help the editor choose camera roles, transcription sources, spoken language,
public profile and title binding, event and project names, a safe run ID, and an
absent prepared output directory. Then run the installed command in the shape
reported by:

```text
tritrack run prepare --help
```

Confirm that the summary reports `phase: prepared` and
`nextAction: provide-revision`. Do not claim that the string-out is a final
story edit.

## Hold the text-revision human gate

Pause for the editor to review `transcript-bundle.json`. Preserve every cue ID,
source hash, language, and timing. Help encode only corrections the editor
explicitly approves in one strict `tritrack.text-revision/v1` JSON artifact
bound to the exact transcript-bundle bytes.

Never infer approval. Use `takes: []` only after the editor explicitly confirms
that no text changes are wanted. Do not retime, split, merge, translate, or
invent cues.

Run the installed alignment command in the shape reported by:

```text
tritrack run align --help
```

Confirm `phase: aligned` and `nextAction: edit-paper-workbook`.

## Hold the paper-edit human gate

Pause for the editor to edit `paper-edit.xlsx`. Allow edits only in the
`Questions` and `Selections` tables. Keep cue addresses intact and require the
editor to decide active answers, story order, and reserve ranges.

Treat the workbook as transport, not authority. The strict aligned transcript
remains text and timing authority; grouping JSON records editor intent; the
working-cut JSON is the compiled selection authority.

## Finish the story projection

Reuse the exact prepared and aligned bundles, the editor-approved workbook, and
the same local camera sources. Choose a new absent finished output directory.
Run the installed command in the shape reported by:

```text
tritrack run finish --help
```

Confirm `phase: finished` and `nextAction: complete`. Describe
`story-cut.fcpxml` as a deterministic story-ordered projection. Do not claim a
GUI import, application round trip, or external DTD validation unless the
editor separately performs and records it.

## Inspect without mutation

Use the installed read-only command in the shape reported by:

```text
tritrack run status --help
```

Report only the run ID, phase, next action, stage names, logical artifact names,
and hashes. Do not expose local paths, transcript text, question text, notes, or
FCPXML content in a status summary.

## Validate an existing artifact without mutation

Choose one explicit mode from installed help. Do not guess a format or search
nearby paths.

- `contract` returns the exact `contract` scope for one registered JSON
  contract. It does not prove referenced files or cross-file hashes.
- `fcpxml` returns `structural-profile` for the selected installed profile and
  title binding. It does not check source media, a DTD, or a GUI import.
- `paper` returns `authority-bound` for one workbook checked against the exact
  supplied aligned transcript bytes. It does not publish editor intent.
- `run` returns `complete-run-bundle` for one complete immutable bundle and its
  manifest chain.

All four modes are read-only. Validation does not repair an artifact, create an
output, inspect unrelated content, or make a network request. Report success
only inside the returned scope.

## Stop on strict failures

Stop when compatibility, source custody, exact hashes, manifest chain, schema,
workbook integrity, media coverage, or absent-output checks fail. Preserve the
error code and existing files. Do not weaken validation, reconstruct a missing
manifest, or continue from an incomplete bundle.
