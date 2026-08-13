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
   task. Never start implementation on `main` without explicit producer
   authorization.
5. State the public candidate commit, active task, next action, outward-action
   gate, and exact verification evidence to be produced.

## Hold the role firewall

- This skill owns public repository development and maintenance only.
- The future `skills/tritrack-editing-assistant/SKILL.md` is the end-user
  product skill. Do not create it before its roadmap task or put maintainer
  state, task numbers, release authority, or application strategy inside it.
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

## Stop at outward actions

Creating a remote, pushing public bytes, tagging or publishing a release,
contacting testers, and submitting any application are separate outward
actions. Stop and obtain explicit producer approval at the applicable gate.
Never manufacture issues, adoption, downloads, or maintenance activity.

## Close the OSS lane

Run focused tests, the full suite, lint, skill validation, boundary tests, and
`git diff --check`. Read back the resulting files and status. Update public
`STATUS.md` only after the coherent public package is green. Commit only files
owned by the public task, and report explicitly when the local repository has
no remote or off-device backup.
