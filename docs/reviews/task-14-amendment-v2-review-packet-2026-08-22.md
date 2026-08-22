# Read-only review: Task 14 amendment v2 sparse-source guard

You are an independent reviewer. Produce findings only; do not edit files.
Review only the evidence in this packet. Do not claim repository inspection
beyond the included excerpts.

## Frozen target

- Repository: public `TriTrack-Editing-Assistant`
- Branch: `codex/task13-parity-mechanisms`
- Base: `1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`
- Target: `7232267a236cbb35f210d5088cb02ca69201d473`
- Objective: add the missing sparse-source guard while keeping VAD off and
  preserving exact v1 readers.

## Authoritative behavioral requirements

The hash-bound public clean-room amendment requires all three guards before a
future VAD default: in-cue invention detection, sparse-source detection, and
alternative retry driven by both. Retry triggering and adoption must consult
the same verdicts. The sparse starting policy is strictly below 1.0 Unicode
letter／number／symbol per second on media at least 30 seconds long. Unknown,
non-positive, and short durations are not judged. A usable primary wins; a
sparse primary yields to a usable alternative but survives when nothing is
better; invalid primary text never survives and may adopt a sparse
alternative. Per-source machine evidence, per-job retry／rescue／unrescued
counts, active thresholds／settings, a sorted human table with a threshold row,
and shared-alternative warnings are required. Existing cue bundle v1 remains
authority and old readers remain supported. VAD must stay off.

## Implementation shape

1. `sparse_source.py` is pure and owns both verdict and source choice.
2. Successful decoding now carries exact normalized PCM duration in
   milliseconds.
3. New output is additive: `transcription-report-v2`,
   `transcription-result-manifest-v2`, and `run-manifest-v3`; v1 result and
   v1／v2 run loaders remain.
4. `transcription-density.txt` is deterministic, path-free, text-free, sorted
   by exact rational density, and hash-bound by both the result and run
   manifests.
5. Standalone and run orchestration use the same result builder. One
   alternative path may be shared across takes, while any primary-as-
   alternative mapping and duplicates within one take remain invalid.

## Critical source excerpts

Pure policy:

```python
SPARSE_CHARACTERS_PER_SECOND = 1.0
SPARSE_MINIMUM_DURATION_MS = 30_000

def transcript_characters(cues):
    total = 0
    for cue in cues or ():
        text = "" if cue is None else cue.get("text") or ""
        if not isinstance(text, str):
            raise TypeError("TRITRACK_TRANSCRIPT_CONTENT_INVALID")
        for character in text:
            if unicodedata.category(character)[0] in {"L", "N", "S"}:
                total += 1
    return total

def characters_per_second(cues, duration_ms):
    if (isinstance(duration_ms, bool)
            or not isinstance(duration_ms, (int, float))
            or duration_ms <= 0):
        return None
    return transcript_characters(cues) * 1000 / duration_ms

def is_sparse(cues, duration_ms):
    if (isinstance(duration_ms, bool)
            or not isinstance(duration_ms, (int, float))
            or duration_ms < SPARSE_MINIMUM_DURATION_MS):
        return False
    measured = characters_per_second(cues, duration_ms)
    return measured is not None and measured < SPARSE_CHARACTERS_PER_SECOND

def source_problem(candidate):
    if candidate.invalid:
        return "invalid"
    if not candidate.cues:
        return "empty"
    if is_sparse(candidate.cues, candidate.duration_ms):
        return "sparse"
    return None

def requires_retry(candidate):
    return source_problem(candidate) is not None

def choose_source(candidates):
    if not candidates:
        return SourceChoice(None, "empty")
    primary_problem = source_problem(candidates[0])
    if primary_problem is None:
        return SourceChoice(0, "primary-usable")
    for index, candidate in enumerate(candidates[1:], start=1):
        if source_problem(candidate) is None:
            return SourceChoice(index, f"primary-{primary_problem}")
    if primary_problem == "sparse":
        return SourceChoice(0, "no-better-source")
    for index, candidate in enumerate(candidates[1:], start=1):
        if source_problem(candidate) == "sparse":
            return SourceChoice(index, f"primary-{primary_problem}")
    return SourceChoice(None, primary_problem)
```

Builder control flow (error attempts carry unknown metrics and an invalid
candidate; successful attempts carry exact metrics):

```python
for ordinal, source in enumerate(request.sources, start=1):
    try:
        take = decoder(source, request.take_id, settings)
    except ValueError as error:
        code = _error_code(error)
        if code in _FATAL_TAKE_ERRORS:
            raise
        attempts.append(AttemptRecord(
            ordinal=ordinal,
            source_sha256=source.sha256,
            outcome="invalid" if code in {
                "TRITRACK_TRANSCRIPT_ANOMALY_INVALID",
                "TRITRACK_TRANSCRIPT_REPEATED_CUES",
            } else "failed",
            failure_code=code,
            settings=settings,
            metrics=_unknown_metrics(),
        ))
        decoded.append(None)
        candidates.append(_candidate_for_error())
        continue
    metrics = _measured_metrics(take)
    candidate = _candidate_for_take(take)
    problem = sparse_source.source_problem(candidate)
    attempts.append(AttemptRecord(
        ordinal=ordinal,
        source_sha256=source.sha256,
        outcome="sparse" if problem == "sparse" else take.status,
        failure_code=None,
        settings=settings,
        metrics=metrics,
    ))
    decoded.append(take)
    candidates.append(candidate)
    if not sparse_source.requires_retry(candidate):
        break

choice = sparse_source.choose_source(candidates)
selected = decoded[choice.index] if choice.index is not None else None
```

Machine report facts:

```python
"sparsePolicy": {
    "charactersPerSecond": 1.0,
    "minimumDurationMs": 30000,
    "contentDefinition": "unicode-letters-numbers-symbols-v1",
},
"summary": {
    "sourceAttemptCount": sum(len(take["attempts"]) for take in reports),
    "sparseSourceCount": sum(
        1 for take in reports for attempt in take["attempts"]
        if attempt["metrics"]["sparse"] is True
    ),
    "retryAttemptCount": sum(
        max(0, len(take["attempts"]) - 1) for take in reports
    ),
    "rescuedTakeCount": rescued_take_count,
    "unrescuedTakeCount": unrescued_take_count,
}
```

Load-time v2 verification validates canonical report／manifest bytes; all three
artifact hashes; exact regenerated density table bytes; report-to-bundle take,
source, status, settings, selection, attempt-order, summary, and
shared-alternative relationships; every attempt's rate and sparse boolean
against exact duration／character counts; and selected-source counts against
the cue bundle. v1 loading dispatches to untouched v1 contracts and the
three-file directory shape.

Run v3 adds logical `transcriptionDensity` to the prepared artifact set and
transcribe stage outputs. Its authority validator requires density only for
result-manifest v2, verifies the result hash, and regenerates exact table bytes.
Result-manifest v1 rejects an unexpected density artifact. Aligned and finished
phase shapes are unchanged and retain the prepared manifest's schema version.

## Test evidence

TDD RED checkpoints were observed for each absent seam. The fixed target then
passed:

- 337 complete unit tests;
- Ruff over `src tests examples scripts`;
- Python compilation over `src tests examples scripts`;
- package wheel／sdist exact member and reproducibility checks;
- public maintainer-boundary and project-identity checks;
- `git diff --check`.

Invented tests cover Unicode counting, strict thresholds, unknown／short
duration, primary／alternative choice ordering, sparse retry and adoption,
invalid-to-sparse adoption, unrescued sparse primary, exact duration capture,
per-source metrics and summaries, deterministic threshold table, shared
alternatives across takes, v1 result loading, v1／v2 run compatibility, v3
artifact binding, and re-signed relationship drift.

## Known boundaries and non-goals

- VAD remains hardcoded off; no VAD switch, path, model pin, or download was
  added.
- The initial threshold is observable and must be re-derived for public users'
  own language, recognizer model, and material; it is not an accuracy claim.
- No private repository or media was read.
- No tag, Release, package publication, external tester contact, private
  integration, application submission, or production-stability claim.
- The separate historical Task 14 Claude convergence supplement used its
  original byte-identical packet and remains incomplete after timeout; it is
  not evidence for this amendment review.

## Requested review

Look specifically for policy divergence, a retry/adoption split, incorrect
sparse counting or threshold arithmetic, report/schema/loader contradictions,
unsafe backward compatibility, semantic cross-binding gaps, deterministic
table errors, path/text leakage, or tests that falsely pass. Return either
`NO FINDINGS` or a list with: ID, severity (`blocker|major|minor`), exact packet
excerpt, concrete counterexample, and bounded correction. Distinguish required
findings from optional hardening.
