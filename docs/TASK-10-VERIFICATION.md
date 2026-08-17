# Task 10 verification

Date: 2026-08-17

Implementation candidate: `5fe9a4531f8dbd23f98174023d61f66a359d461b`

## Public scope proven

Task 10 implements the installed `tritrack run prepare`, `run align`, `run
finish`, and read-only `run status` commands. Every mutating transition creates
a new immutable absent directory with a canonical phase-specific manifest,
fixed artifact names, exact SHA-256 values, completed stage records, and the
ordered hashes of prior manifests. The manifest is published last.

The finished bundle contains canonical grouping and working-cut JSON plus
`story-cut.fcpxml`. The story renderer reopens the exact aligned, grouping, and
working-cut authorities; re-derives each active cue span, text, timing, source
hash, and story order; converts boundaries once to profile frames; layers
paired sources through the sync offset; requires full declared audio-master
coverage; and excludes reserve ranges.

The separate `skills/tritrack-editing-assistant/SKILL.md` is the installed
end-user editing entry point. It consults installed help before flags, preserves
the explicit text-revision and paper-edit human gates, requires absent outputs,
and states that the workbook is transport rather than authority. Maintainer
task state and publication authority remain in the repository-local maintainer
skill.

The workflow performs no network request, credential lookup, provider
transport, live upload, Final Cut automation, or private-project operation. It
makes no claim of a Final Cut GUI import, DTD validation, or round trip.

## Architecture decision and consultation

The producer selected option A: three explicit immutable stage bundles plus a
final story-ordered FCPXML projection. The frozen brainstorm packet SHA-256 was
`80af43be795fc7638b7ecd49c26b6f7525ab7e97239f9d9b71b804caf0cf06c5`.
Codex completed its independent analysis before external results. Gemini
dynamically requested, observed, and completed `gemini-3.7-flash`. The separate
Claude subscription wrapper requested the dynamic `opus` capability alias but
timed out; observed and completed models are null and that attempt remains
explicitly incomplete without retry, downgrade, paid credential, or provider
fallback. The selected contract is frozen in `docs/TASK-10-DECISION.md`.

## Preserved RED-to-GREEN evidence

- Manifest／revision RED: the old mutable run manifest rejected immutable
  bundle fields and `text-revision-v1` rejected explicit `takes: []`. GREEN
  closes phase artifacts, actions, chains, sources, and completed stages while
  retaining non-empty revisions inside any listed take.
- Story projection RED: `story_fcpxml.py` and its renderer did not exist. GREEN
  covers authority rebinding, story-order permutations, exact frame timing,
  paired and single sources, one dialogue master, title text, reserve exclusion,
  deterministic XML, source starts, XML escaping, late mutation, symlinks, and
  publication races.
- Bundle RED: `run_workflow.py` did not exist. GREEN covers canonical manifests,
  fixed filenames, exact hashes, sanitized summaries, complete-bundle loading,
  manifest-last hard links, directory races, incomplete bundles, and cleanup of
  invocation-owned state only.
- Transition RED: prepare／align／finish／status interfaces were absent. GREEN
  covers installed engine order, unsupported-doctor fail-fast, source and model
  custody, explicit no-change revision, workbook application, exact chain
  matching, story emission, and read-only status.
- CLI RED: `run` was a planned placeholder and component 11 was planned. GREEN
  exposes four nested help surfaces, sanitized exit mappings, and exactly eleven
  components with `multicam-sync` implemented.
- Skill RED: no separate end-user skill existed. GREEN passes the canonical
  skill validator and a role-firewall test that rejects maintenance, private,
  credential, transport, and source-module content.

## Local verification state

The coherent implementation and governance package passed:

- 193 complete-suite tests;
- 9 maintainer-boundary tests;
- Ruff over `src`, `tests`, and `examples`;
- Python compilation over `src`, `tests`, and `examples`;
- project identity with `ok: true`, kind `public-engine`, and lane `OSS`;
- the current canonical validator for both the maintainer and end-user skills;
- `git diff --check`; and
- a non-editable wheel build and install with `run --help`, the eleven-item
  component registry, and read-only `run status` against a complete invented
  aligned bundle.

The wheel SHA-256 was
`078c8761a663baca1b567ef9978bf07cfbf092537d504574811e4418ffc5a534`.
All run-workflow fixtures use invented content.

Closeout-review provenance is recorded in the Task 10 closeout packet and
provider status／adjudication files under `docs/reviews/`.

No tag, release, pull request, tester contact, package publication, application
submission, Final Cut GUI evidence, or DTD evidence is claimed by Task 10.
