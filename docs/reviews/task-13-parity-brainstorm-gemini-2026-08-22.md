### 1. problem_reframe

The core challenge is not merely porting discrete digital signal processing or string-filtering heuristics into Python; it is an **artifact contract lifecycle problem**.

The public base (`d952c1f`) froze `sync-map-v1` and `transcript-bundle-v1` as exact, immutable downstream seams consumed by validators, string-out, and story projections. The clean-room handoff (`task13-parity-v1`) introduces behaviors that cannot be fully expressed within those frozen v1 schemas:
1. **Relayed B-coverage over a single A-take** violates the v1 assumption of at most one `mediaB` partner per `mediaA`.
2. **Take degradation, retry history, bidirectional hearing settings, and reuse markers** violate the v1 transcript bundle model, which requires all non-silent takes to be `completed` and lacks retry/receipt fields.
3. **Voice-activity detection (VAD) defaults** introduce a causal failure mode (single-cue token loops) that requires stutter detection and alternative-source retry to land *before* the VAD default flips.

The problem must be framed as: **How to upgrade the internal decision engines and emit rich orchestration metadata immediately while preserving zero-breakage compatibility for frozen v1 downstream consumers, without branching the engine into two unmaintainable pipelines.**

---

### 2. pragmatic_path

**Architecture: Additive Sidecar Execution Reports + v1 Projection Facades**

#### A. Versioning & Schema Strategy
- Keep `sync-map-v1` and `transcript-bundle-v1` schemas valid and strictly enforced for downstream tools (`string_out.py`, `story_projection.py`, downstream proofs).
- Introduce a parallel, non-breaking execution report format: `transcription-report-v1` and `sync-report-v1` (or aggregate into a unified `run-execution-report-v1`).
- `transcript-bundle-v1` remains the consumable artifact for downstream story generation, containing only valid/completed takes and silent empty takes. Takes that degraded to `failed` after retry are excluded or marked empty in the v1 bundle projection, while their full failure logs, attempt history, and raw outputs reside in `transcription-report-v1`.

#### B. Relay Selection & FCPXML Mapping
- In `sync_scan`, calculate the clock-drift prior and multi-segment relay coverage.
- When generating `sync-map-v1`, project the relay selection down to the single dominant primary `mediaB` (highest valid overlap + drift agreement) to satisfy the existing 1:1 invariant in `string_out.py` and story projection.
- Record the full discontinuous relay chain in `sync-report-v1` for timeline assemblers capable of multi-clip compound syncing, preventing duplicate `mediaA` IDs in legacy v1 consumers.

#### C. Standalone `transcribe` vs. `run prepare`
- Refactor the transcription pipeline into a layered core:
  - `TranscriptEngine`: Pure transcription on a single stream with VAD, hallucination/stutter detection, and verdict generation.
  - `TakeOrchestrator`: Manages retry loops across candidate sources, provenance receipts, and degrade-to-failed fallback.
- `tritrack transcribe` operates `TakeOrchestrator` on caller-supplied single files (no alternative sources available; a failed take logs verdict reasons and degrades without aborting the batch).
- `tritrack run prepare` passes the sync-graph's candidate alternative audio tracks into `TakeOrchestrator`, enabling automatic failover to the alternative synchronized source.

#### D. Registry vs. Caller-Owned Models
- Split model validation into two explicit discriminators:
  1. `NamedRegistry`: Closed, SHA-256 and byte-length pinned set (e.g., standard Silero VAD, fixed Whisper pins).
  2. `CustomModelPath`: Explicit `--model-path <path>` flag. When used, the receipt records `type: "custom"`, computes the real on-disk SHA-256 and byte length at runtime, and explicitly avoids checking against the closed registry pins.

#### E. Strict Milestone Rollout Sequence
1. **Milestone 1: Pure Decision Engines (Red/Green)**
   - In-cue stutter detector (4-token repetition threshold, delimiter-free limitation documented).
   - Boilerplate & cross-cue repetition analyzers.
   - Clock-drift prior estimator (minimum sample, max-spread refusal).
2. **Milestone 2: Anomaly Verdicts & Standalone CLI Support**
   - Whole-transcript verdict generator (distinguish empty vs. invalid).
   - Additive `transcription-report-v1`.
   - Explicit `--vad` and `--no-vad` flags (VAD default remains **OFF**).
   - Custom model path vs. closed registry hash-checking separation.
3. **Milestone 3: Alternative-Source Retry Engine**
   - Wire `TakeOrchestrator` into `run prepare` with alternative source candidate retry.
   - Provenance recording (bidirectional settings, reuse tracking marked `unknown`).
4. **Milestone 4: Parity Flip & Safety Release**
   - Flip VAD default to **ON** (now protected by Milestones 1 and 3).
   - Run verification suite against clean-room handoff invariants.

#### F. Roadmap Naming
- Record this as **Task 14: Engine Parity & Extended Orchestration**, explicitly referencing the Task 13 authority seam as a frozen prerequisite rather than rewriting Task 13 history.

---

### 3. alternative_architecture

**Architecture: Clean-Break `v2` Artifact Pipeline (`sync-map-v2` & `transcript-bundle-v2`)**

Instead of projecting downward to legacy v1 contracts, declare an atomic transition to v2 schemas across the public engine:

- **Schema Evolution**:
  - `sync-map-v2`: Replaces `pairs: list[Pair]` with `takes: list[TakeMapping]`, where each `take` contains `mediaA` and an array of `relayedSources: list[RelayedSource]` with time-slice offsets.
  - `transcript-bundle-v2`: Natively includes `status: "completed" | "empty" | "failed"`, `receipts`, `attempts: list[Attempt]`, and `provenance`.
- **Downstream Migration**:
  - Update `string_out.py`, `story_projection.py`, and CLI validators to parse both v1 and v2, using an adapter layer (`v2_to_v1_downgrade_adapter`).
- **Tradeoffs**:
  - *Pros*: Completely clean domain model; zero sidecar files; no dual-schema cognitive overhead in the core engine.
  - *Cons*: High blast radius across all downstream validators, packaging tests, and downstream integration proofs; requires simultaneous updates across story projection and FCPXML generators; increases risk of subtle regressions in frozen v1 consumers.

---

### 4. low_cost_experiment

**Experiment: The Isolated Single-Cue VAD Loop Safety Trap**
- **Hypothesis**: Enabling VAD on an audio track containing low-level background HVAC hum causes Whisper to hallucinate a single repeated token loop (e.g., `" Thank you. Thank you. Thank you. Thank you."`) inside a single continuous cue, which passes legacy 3-cue cross-repetition checks but is caught 100% of the time by the 4-token in-cue stutter detector.
- **Method**:
  1. Synthesize a 15-second audio fixture with 40dB SNR ambient noise.
  2. Run transcription with VAD enabled without in-cue stutter detection -> verify it yields a 1-cue hallucination loop.
  3. Execute `detect_in_cue_stutter()` on the output -> assert it flags the cue as invalid with reason `stutter_repetition`.
  4. Pass the invalid verdict to `TakeOrchestrator` -> assert it triggers retry on the secondary sync source.
- **Falsification Metric**: If the in-cue detector fails to catch a 4-token identical sequence within a single cue, or if it erroneously flags natural speech with 3 identical tokens, the experiment fails.

---

### 5. contrarian_challenge

**Thesis: Multi-track relay in `sync_scan` is a premature optimization that does not belong in the synchronization core.**

- In practical field production, an A-camera continuous take spanning two discontinuous B-audio files is an edge case compared to single-file drift. Attempting to solve discontinuous time relays in `sync_scan` forces the synchronization map to act as an edit decision list (EDL).
- If `sync-map-v1` remains 1:1, building a multi-segment relay selector whose outputs must immediately be flattened down to a single dominant B-source creates phantom complexity.
- **Alternative Stance**: Keep `sync_scan` strictly pairwise (file-to-file correlation + clock drift prior). Move relay assembly to a dedicated timeline stitching stage prior to string-out.

---

### 6. unconstrained_possibility

**Zero-Schema Runtime: Content-Addressed Execution DAG**

If backwards compatibility constraints were entirely removed:
- Eliminate `sync-map` and `transcript-bundle` JSON files as static artifacts.
- Represent the entire pipeline as a pure, content-addressed derivation graph (similar to Nix/Bazel).
- Every audio track slice, VAD segment, transcription attempt, and drift correlation is an immutable CAS (Content-Addressed Storage) object identified by `hash(input_bytes + exact_engine_version + settings_receipt)`.
- Downstream tools query the graph via a local SQLite/DuckDB index. Retries, relays, and multi-angle takes resolve dynamically via SQL views rather than rigid JSON schemas.

---

### 7. overlooked_risks

1. **Delimiter-Free Token Loops**: The in-cue detector relies on token/word boundaries. Delimiter-free hallucinations (common in non-segmented or character-based decodes like `"haahahahahahaha"`) will bypass the 4-token stutter check. *Mitigation*: Strictly document this known limit in CLI help and receipt diagnostics; do not advertise regex-based substring safety.
2. **Deterministic Hash Incompatibilities across Platforms**: Model hash verification (byte length + SHA-256) can fail on Windows vs. POSIX if model files undergo CRLF conversion or sparse file allocation. *Mitigation*: Read raw binary chunks (`rb`) using explicit 64KB buffers for hash calculation.
3. **Receipt Provenance Leakage in Reused Work**: Caching engines often accidentally copy the *current* execution receipt onto cached outputs. If cached work is reused, stenciling current `--vad` flags onto previous non-VAD transcripts creates corrupt scientific provenance. *Mitigation*: Mark provenance as `unknown` whenever a cache hit occurs without a full cryptographic settings receipt match.
4. **Degraded Batch Behavior under Subprocess Timeouts**: Degrading a take to `failed` instead of aborting the batch must not mask systematic failures (such as a missing `ffmpeg` binary or a corrupted CUDA/Metal driver). *Mitigation*: Distinguish *take-level anomaly verdicts* (retryable/degradable) from *engine-level infrastructure failures* (which must still abort the batch immediately).

---

### 8. assumptions_to_verify

1. **Overlap Precedence**: Verify that `minimum shared-audio overlap` rejection triggers *before* running cross-correlation or clock-drift prior calculations to avoid expensive FFTs on non-overlapping media.
2. **Drift Prior Bounds**: Verify that the handoff’s "maximum-spread refusal" accurately rejects clock drift calculations when sample points are clustered within < 30 seconds of total span.
3. **Model Validation Timing**: Verify that registry and model-path checks execute strictly before audio loading/decoding begins, ensuring fast CLI failure on typos.
4. **CLI Mutual Exclusion**: Verify that passing both `--vad` and `--no-vad` immediately yields an exit code `2` argument error rather than one silently overriding the other.

---

### 9. recommended_next_decision

**Approve the Pragmatic Path (Section 2) under a new "Task 14" Milestone Container.**

1. **Action**: Authorize the creation of Task 14 work packages following the 4-milestone rollout order.
2. **Schema Policy**: Preserve `sync-map-v1` and `transcript-bundle-v1` as the immutable downstream public interfaces; emit extended metadata via sidecar execution receipts (`transcription-report-v1`).
3. **Rollout Guard**: Enforce by test assertion that the default flag for voice activity detection remains `False` until the test suite verifies that both `detect_in_cue_stutter` and alternative-source retry are wired into `run prepare`.
