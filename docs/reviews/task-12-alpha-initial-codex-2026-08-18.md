# Task 12 Codex independent alpha review

## Review identity

- Review target: `7ec69bd0ef045c18eb7899e95ff1472ca5913d05`
- Frozen packet: `task12-alpha-review-packet-v4-2026-08-18.md`
- Packet SHA-256:
  `38873ec0d33715d2e7f162f4cafbbad78994fc9b4cd0fb88d7320ab33985c8d1`
- Independence: this response was closed before either Task 12 external
  closeout response was requested or read.

## Summary

Two major findings. Both are localized resource-boundary defects. No blocker
was found, and no finding changes the authority model, validator mode count,
package contents, or Task 12 two-layer freeze design.

## Findings

### T12-CX-001 — major — high confidence

- Current location: `src/tritrack_editing_assistant/emit_fcpxml.py:41-50`
- Failure mechanism: `load_sync_map` calls `Path.read_bytes()` before comparing
  the result with `MAX_SYNC_MAP_BYTES`. The advertised 16 MiB limit therefore
  does not bound the read: an arbitrarily large regular file is first retained
  in memory and is rejected only afterwards. The same path also follows a
  symlink because this loader does not use the repository's descriptor-based
  `O_NOFOLLOW` regular-file boundary.
- Impact: a caller-selected malformed sync-map path can cause excessive memory
  use or process termination instead of the stable
  `TRITRACK_EMIT_SYNC_MAP_INVALID` result. This defeats the current local input
  safety boundary before FCPXML validation begins.
- Smallest safe fix: load at most `MAX_SYNC_MAP_BYTES + 1` bytes from an
  `O_NOFOLLOW` descriptor after an `fstat` regular-file and size check, then
  preserve the existing unreadable/invalid error split.
- Regression: supply an oversized sparse regular file and a symlink to a valid
  map; prove both fail through the stable code without calling
  `Path.read_bytes`, while a valid exact-limit-or-smaller file still loads.

### T12-CX-002 — major — high confidence

- Current locations: `scripts/release_gate_core.py:92-110` and
  `scripts/release_gate_core.py:663-688`
- Failure mechanism: `_run_git` and `_run_command` use
  `subprocess.run(..., capture_output=True)` and compare output length only
  after the child has exited. `subprocess.run` has already accumulated all
  stdout and stderr in memory at that point, so `_COMMAND_OUTPUT_LIMIT` is a
  post-hoc acceptance check rather than a capture bound. A noisy or stalled
  Git/build/install subprocess can consume memory until completion or timeout.
- Impact: the maintainer gate can be killed or delayed rather than failing
  promptly and deterministically at its declared output boundary. This is
  particularly material because the gate evaluates source-controlled build
  behavior and describes its primitives as bounded and fail closed.
- Smallest safe fix: stream stdout and stderr under one explicit byte budget,
  terminate the complete child process group on limit or timeout, and retain
  the current sanitized public error codes. Apply the same primitive to Git
  and build/install commands.
- Regression: run a child that writes just over a tiny injected limit and then
  sleeps. The bounded implementation must terminate it and return
  `TRITRACK_RELEASE_COMMAND_LIMIT` before timeout; the frozen implementation
  instead waits for timeout and returns `TRITRACK_RELEASE_COMMAND_FAILED`.

## Optional observations

None.

## Inspection record

Inspected the packet header, exact Git inventory, complete packaged runtime
source and data set, CLI registry and validator dispatch, authority schemas,
run-bundle publication and loading, sync／transcribe／align／hybrid／paper／organize
／story seams, FCPXML rendering and structural validation, release policy,
wheel／sdist inspection and publication, fixed CI, Task 12 design, current
README／status／roadmap／tooling claims, and focused tests for the affected
loaders and gate seams. No provider answer was available during this review.
