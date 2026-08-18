---
name: tritrack-editing-assistant-maintainer
description: Use when developing, testing, documenting, reviewing, or resuming maintenance of the public TriTrack Editing Assistant repository, including its OSS lane, Tasks 5–13, clean-room intake, compatibility evidence, and pre-release gates. Do not use for the private TriTrack production system or for the end-user editing workflow skill.
---

# TriTrack Editing Assistant Maintainer

## Start only the public maintenance lane

The only cold-start command is:

```text
$tritrack-editing-assistant-maintainer OSS 開工
```

An optional bounded task suffix may follow, for example:

```text
$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 5
```

Bare `開工`, a missing `OSS`, or any other lane must fail closed. Do not infer
the lane from conversation history, a branch name, or a similarly named
TriTrack project.

1. Resolve the current Git toplevel.
2. From that root, run:

   ```text
   python3 .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root <git-toplevel>
   ```

   Continue only when it returns `ok: true`, project kind `public-engine`, and
   lane `OSS` from `.tritrack-project.json`.
3. Read `AGENTS.md`, `STATUS.md`, `PRODUCT-WISHES.md`, `docs/ROADMAP.md`,
   `docs/TOOLING.md`, and only the task-relevant public files.
4. Confirm the branch/worktree is isolated and clean enough for the requested
   task. Keep implementation off `main`; integrate a fully green candidate
   only under the recorded standing grant.
5. State the public candidate commit, active task, next action, applicable
   standing grants, and exact verification evidence to be produced.

## Hold the role firewall

- This skill owns public repository development and maintenance only.
- `skills/tritrack-editing-assistant/SKILL.md` is the separate installed
  end-user product skill. Keep maintainer state, task numbers, release
  authority, and application strategy out of it.
- Never browse another repository for source, status, media, transcripts,
  journals, templates, credentials, or history. Consume only a separately
  reviewed clean-room intake that has been deliberately handed to the public
  task with hashes and allowed transformations.
- If required intake is absent, stop and report the missing handoff. Do not
  cross the boundary to manufacture it.
- Keep product behavior in tested Python/JavaScript code. This skill owns
  orchestration and governance, not pairing thresholds, schemas, or FCPXML
  construction logic.

## Execute one public task at a time

- Treat `STATUS.md` as the current public-maintenance truth and
  `docs/ROADMAP.md` as the public task sequence.
- Follow test-driven development for behavior changes: red test, observed
  failure, minimal implementation, full verification.
- Use invented or explicitly cleared fixtures only. Keep media, transcripts,
  credentials, absolute home paths, proprietary templates, and private
  operational evidence out of tracked files and review packets.
- Keep generated outputs in absent ignored directories; never overwrite source
  media or an existing result.
- Keep the default workflow local. Provider use requires the exact explicit
  user request and the product's separate consent boundary.
- Consult the exact command help before naming flags. A planned command is not
  implemented merely because it appears in the component registry.

## Apply standing authorization

Producer authorization is a capability-scoped standing grant. Once a
capability is explicitly authorized or recorded in the public governance, it
remains authorized for the same target, visibility, scope, and risk.
The grant remains effective until the producer revokes it.
Do not request it again, pause at that gate, or treat a new task as implicit
revocation.

Request a new authorization only for a capability that has never been granted
or for a material change in target, visibility, scope, or risk. Destructive
history changes, credential or private-data disclosure, and a different remote
are material changes rather than repetitions.

The current standing grant covers closeout review, fix-forward of ordinary
in-scope findings, fast-forward integration of a fully green candidate, and
pushing `main` to the existing public `origin` with exact remote-SHA backup
verification. Force-push, tags, releases, pull requests, tester contact,
package publication, and application submission have not yet been granted.
Never manufacture issues, adoption, downloads, or maintenance activity.

## Close the OSS lane

Run focused tests, the full suite, lint, skill validation, boundary tests, and
`git diff --check`. Read back the resulting files and status. Update public
`STATUS.md` only after the coherent public package is green. Commit only files
owned by the public task. Treat requested implementation as including closeout
review and fix-forward until ordinary in-scope findings are resolved; stop only
for a true public-contract gap, unsafe scope expansion, or a separately gated
action.

For a release-readiness task, run the maintainer-only gate exactly as:

```text
python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

The source must be a clean public-engine／OSS Git toplevel and the output must
be absent. Treat only a canonical manifest linked after both inspected archives
as a complete local candidate. This gate does not grant any outward action
excluded by the standing authorization above.
