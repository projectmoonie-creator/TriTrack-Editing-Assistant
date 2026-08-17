# Public project agent instructions

This repository is the public-engine project. Its development lane is `OSS`.
It is not a production-media repository and it does not inherit state from a
similarly named project.

## Startup

Use `.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md` for every
substantive maintenance session. The only cold-start command is:

```text
$tritrack-editing-assistant-maintainer OSS 開工
```

Before reading task state or changing files, resolve the Git toplevel and run
the skill's `scripts/check_project_identity.py`. A missing or mismatched
`.tritrack-project.json` fails closed.

Then read `STATUS.md`, `PRODUCT-WISHES.md`, `docs/ROADMAP.md`,
`docs/TOOLING.md`, `README.md`, and only the files relevant to the active task.
State the candidate commit, task, next action, applicable standing grants, and
planned evidence before mutating project state.

## Three-role boundary

- `tritrack-editing-assistant-maintainer` owns this repository's development
  and maintenance.
- `skills/tritrack-editing-assistant/SKILL.md` is the installed end-user
  product surface. It contains no maintainer task state or release authority.
- Private production orchestration is a different project. Do not scan its
  repositories or import its status, media, transcripts, journals, templates,
  credentials, or history. Accept only reviewed clean-room intake with exact
  hashes and declared transformations.

If required clean-room intake is missing, report the missing handoff and stop.
Do not search for another checkout or silently use a remembered path.

## Development rules

- Work in an isolated branch/worktree. Integrate a fully green candidate to
  `main` only under the standing grant below.
- Use test-driven development for behavior changes and preserve the observed
  red/green evidence.
- Use invented or explicitly cleared fixtures only.
- Keep media, transcripts, credentials, absolute home paths, proprietary
  assets, and private operational evidence out of Git, prompts, and issues.
- Keep the default workflow local and no-overwrite. Provider operations remain
  separate, explicit opt-in paths.
- Do not claim planned commands are implemented. Verify against `STATUS.md`,
  tests, and installed command behavior.
- Public `STATUS.md` is the only current maintenance status. Public
  `docs/ROADMAP.md` owns the public task sequence.

## Authorization model

Producer authorization is a capability-scoped standing grant. Once a
capability is explicitly authorized or recorded here, it remains authorized for
the same target, visibility, scope, and risk until the producer revokes it.
Do not request it again, pause at that gate, or reinterpret a new task as
revoking it.

A new authorization is needed only when the capability has never been granted,
or when the proposed action materially changes the target, visibility, scope,
or risk. Destructive history changes, credential or private-data disclosure,
and a different remote are material changes rather than repetitions.

The current standing grant covers closeout review, fix-forward of ordinary
in-scope findings, fast-forward integration of a fully green candidate, and
pushing `main` to the existing public `origin` with exact remote-SHA backup
verification. Force-push, tags, releases, pull requests, tester contact,
package publication, and application submission have not yet been granted.

## Close

Before closing, run focused and full tests, lint, the project-boundary tests,
skill validation, and `git diff --check`; then read back exact status and
changed files. Update `STATUS.md` only after the coherent package is green.
Commit only task-owned files. A requested implementation includes closeout
review and fix-forward until ordinary in-scope findings are resolved; stop only
for a true contract gap, unsafe expansion, or a separately gated action.
