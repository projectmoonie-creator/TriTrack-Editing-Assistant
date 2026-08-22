# Task 14 decision: parity prerequisites

**Status:** accepted by the producer on 2026-08-22  
**Public base:** `d952c1fe41563c38c7859250b3f95b3d93e8929f`  
**Working branch:** `codex/task13-parity-mechanisms`  
**Authorized behavioral input:** clean-room handoff `task13-parity-v1`

## Decision

Adopt the asymmetric Option A from the Task 13 parity brainstorm and name the
public work **Task 14 — parity prerequisites**.

- Introduce `sync-map-v2` as the authoritative representation for a temporal
  relay, drift-prior acceptance, coverage-selected extra sources, and an
  explicit audio master.
- Keep `transcript-bundle-v1` byte-for-byte compatible as the cue-bearing
  authority for successful and proven-empty takes.
- Publish transcription as a manifest-last result directory containing that
  bundle plus a text-free `transcription-report-v1` and an exact
  `transcription-result-manifest-v1`.
- Introduce `run-manifest-v2` for newly prepared immutable runs so those three
  transcription artifacts are first-class run authority. Existing v1 run
  manifests remain readable and are not retroactively redefined.
- Make standalone `transcribe` and `run prepare` call the same orchestration
  seam. An invalid primary is retried with a synchronized alternative under
  identical settings; a take with no valid source is reported as failed and
  omitted from the cue bundle without aborting the batch.
- Preserve the current caller-owned recognition-model path as an observed,
  hashed input. It is not relabelled as a closed-registry model.

## Voice-activity hard gate

Voice-activity detection remains **off by default** in the Task 14 candidate.
The clean-room handoff deliberately provides the model-pinning rule but no
publicly verifiable model byte length or SHA-256. Consequently Task 14 must not
invent a pin, accept an unpinned caller path, expose a misleading default, or
claim the `voice-activity-default` contract is complete.

The default may flip only in a later coherent change after all of these facts
are simultaneously true:

1. in-cue stutter detection is green;
2. alternative-source retry and degrade-to-failed are green at both the
   orchestrator and CLI/run boundaries;
3. a non-rejected VAD model is present in a closed public registry with exact
   byte length and SHA-256;
4. model validation happens before media decode;
5. `--vad`, `--no-vad`, contradictory switches, no-audio use, and model-choice
   argument rules are covered by wrapper-level tests.

Until then the public report states voice activity as `off` for new attempts
and `unknown` for reused evidence. The command surface exposes no VAD switch.

## Compatibility boundary

`sync-map-v1` remains readable for existing public artifacts. New sync output
uses v2. The relay claim is intentionally narrow: v2 supports sources relaying
in time and continues to discard simultaneous duplicate coverage. It does not
claim arbitrary simultaneous N-camera support.

No private repository, private media, private transcript, or private runtime
receipt is an implementation or verification input.
