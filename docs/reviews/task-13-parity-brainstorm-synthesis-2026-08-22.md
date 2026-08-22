# Task 13 parity mechanisms — multi-AI brainstorm synthesis

Date: 2026-08-22

Decision owner: producer

No production implementation began before this synthesis and producer
decision.

## Frozen evidence

- packet SHA-256:
  `3004b7a90946a514389865b30f2fbcb001ac387d792a512edfb7664b45fed674`
- Codex independent response SHA-256:
  `96b0732dcadbd0fdc3ad6a03dedb09f6291e25f6e6bc26b449e22abbd7bc0a1b`
- Gemini wrapper-output SHA-256 before one trailing-space cleanup:
  `d2c272c29fbc0f12095587c90b9be5d6c3608b852312c6abd994837d2b07eb42`
- tracked Gemini response SHA-256 after removing that one trailing space:
  `9591bbf53bd4d7aa0445c91950acba499b72ff44453ed0d4342b7f84c3db8247`
- Gemini status SHA-256:
  `b7d53374ba962d3a3258eb8a17ea924ed83c591ce119aa5281b43f14cd3e992f`
- Claude status SHA-256:
  `d8bc89f398daf72d3b14099893e847cd76abeb195c6f0f659ac764eaa063635c`

## Consensus

- This is an artifact-contract lifecycle decision, not a request to paste two
  algorithms into existing modules.
- The existing v1 process seam must remain exact. Relay topology, failure
  status, attempts, retry, and settings cannot silently acquire new meanings
  under `sync-map-v1` or `transcript-bundle-v1`.
- One shared orchestration core should serve standalone transcription and
  `run prepare`; otherwise the public engine would have two contradictory
  definitions of transcription behavior.
- Anomaly verdict and alternative-source retry must be production-wired and
  tested before voice activity becomes the default.
- Explicit `--vad` may exist earlier, but default-on is the last milestone.
- Reused work must never be stamped with the current run's settings.
- Take-level anomaly failures may degrade; infrastructure and dependency
  failures must still abort rather than being mislabeled as bad takes.
- The historical public Task 13 authority-seam decision should not be
  rewritten. Both completed lanes recommend naming this public work Task 14.

## Complementary ideas

- Codex separated the two authority problems: relay selection changes sync
  authority itself, while transcription attempts explain cue authority but do
  not own cue text or timing.
- Gemini emphasized one layered transcription core: a single-stream engine
  under a take orchestrator that owns retry and degradation.
- Together these support an asymmetric design: a new version of the sync
  authority, plus a manifest-like transcription result around the unchanged
  cue authority.
- Both lanes require distinct validation classes for public registry pins and
  caller-owned model paths, so a caller's bytes are never falsely described by
  somebody else's size／hash pin.

## Provider-unique ideas

### Codex

- Keep `transcript-bundle-v1` as the only cue-text／timing authority. Put
  requested-source completeness, settings, attempts, selected retry, failures,
  and reuse markers in a text-free `transcription-report-v1`, with a
  manifest-last result directory binding both exact artifacts.
- Use `sync-map-v2` because relay topology changes authoritative sync facts and
  must reach FCPXML without placing the A take twice.
- Treat the absence of a verified public VAD model pin as a true contract gap:
  anomaly, retry, provenance, and explicit plumbing can land, but default-on
  must not invent operational evidence.
- Keep editorial take identity separate from physical attempt-source identity
  so retry does not break later cue-addressed revisions.
- Flag greedy coverage order, drift-coordinate definition, stable tie-breaking,
  interval clipping, and zero-success batches as explicit design risks.

### Gemini

- Proposed `TranscriptEngine` plus `TakeOrchestrator` as explicit layering.
- Proposed an additive `sync-report-v1`／`transcription-report-v1` family and a
  v1 projection facade as the smallest compatibility change.
- Called out the difference between take-level anomaly failures and systemic
  subprocess failures.
- Suggested an end-to-end invented VAD loop experiment. The useful portion is
  the deterministic one-cue loop fixture and retry assertion; relying on a real
  decoder to reproduce the loop from synthetic HVAC noise would be flaky and
  is not required for contract coverage.

## Contradictions and adjudication

### Relay authority

Codex recommends `sync-map-v2` as the production authority. Gemini's pragmatic
path keeps the full relay only in `sync-report-v1`, projects one dominant B into
v1, and leaves legacy FCPXML on that projection.

The Gemini projection is not a completion path for the current handoff: the
coverage-selected relay would be computed and documented but not applied by
the installed editing output. That fails the public rule that a mechanism is
not complete until it is fixed, pinned, and connected. It remains a legitimate
scope-reduction option only if the producer explicitly defers relay application
to a later task.

### Failed takes in v1 cue bundles

Gemini suggested that failed takes might be excluded or projected as empty.
Projecting a judged-invalid take as `empty` contradicts the preserved invariant
that an empty transcript is not the same as judged bad. Exclusion can be
truthful only when an enclosing exact manifest records the requested source set
and failed outcome. The synthesis therefore rejects `failed -> empty` and keeps
manifest-bound exclusion as the only v1-compatible projection.

### Model registry

Gemini proposed two selectors, a named registry and a custom model path. The
handoff says selectable public pins are closed, but also warns not to assert a
project pin against caller-owned bytes. The reconciled rule is:

- arbitrary VAD paths are not accepted once public VAD selection exists;
- a public VAD registry entry is name + exact size + exact hash;
- existing caller-owned recognition paths remain a distinct unregistered
  input class and record their observed hash without inheriting a registry
  name; and
- if named recognition selection is added later, it is mutually exclusive with
  the caller-owned path.

## Experiments

### Experiment 1 — relay authority RED

Use invented measurements for one 600-second A source and two sequential
300-second B sources. The public command-level test must prove all of these:

- A appears once in the produced timeline;
- both B relays appear over their covered intervals;
- a simultaneous duplicate B adds zero coverage and is absent;
- correlation outranks drift-prior acceptance; and
- input ordering cannot change chosen bytes.

If a proposed artifact cannot drive this installed FCPXML behavior without
duplicating A, it is not a viable relay authority.

### Experiment 2 — transcription result RED

Use invented engine JSON: primary source produces one four-token stuttering
cue, the synchronized alternative produces clean cues. Prove the result binds
both attempts, identical settings, selected alternative, and one cue authority
without copying cue text into the report.

Then use a no-alternative failure followed by a clean second take. Prove the
first is reported failed, the second ships, and infrastructure failures still
abort the batch.

### Experiment 3 — authority-shape comparison

Express Experiment 2 with both direct `transcript-bundle-v2` and a
bundle／report／manifest. Count changed existing schemas and consumers and test
TOCTOU binding. Falsify the manifest form if completeness cannot be proven
without duplicating cue authority or if validation requires race-prone
unbound reads.

## Risks

- Drift needs a precise coordinate system and an independent evidence source;
  otherwise a prior can accidentally vouch for the same noisy measurement it
  is supposed to supplement.
- Greedy coverage selection needs deterministic ordering and tie-breaking.
- Relay placement needs interval clipping, not just a second raw-offset clip.
- Report samples or error prose can leak transcript text; report reasons should
  be closed codes.
- A zero-success batch must not look like a valid empty transcript.
- Boolean-switch parser tests must cover wrapper forwarding, not only unit
  parser state.
- New packaged schema／registry resources intentionally change exact package
  inventories and require a new candidate record.
- The current downstream example proves aligned-transcript-v1 only; preserving
  it does not prove new contracts are discoverable or correctly validated.
- A VAD default needs one verified public model pin and installed-engine flag
  behavior. The clean-room handoff supplies the behavioral contract but does
  not itself supply that operational pin.

## Options

### Option A — asymmetric authorities (recommended)

Add `sync-map-v2` for authoritative relay topology. Add a manifest-last
`transcription-result-v1` directory containing an unchanged
`transcript-bundle-v1`, text-free `transcription-report-v1`, and exact manifest.
Normalize v1 pairs and v2 groups into one internal FCPXML relationship model.
Standalone and prepared-run transcription use the same orchestrator.

Tradeoff: sync consumers gain v2 support, but alignment and cue-edit consumers
avoid a version cascade because cue authority remains v1. The result has more
than one transcription file, so manifest binding and read-order tests are
mandatory.

### Option B — full v2 authority cascade

Add `sync-map-v2` and `transcript-bundle-v2`, representing relay, settings,
attempts, retry, failed status, and provenance directly. Propagate v2 through
alignment, paper edit, organization, story projection, run manifests,
validators, packaging, and the downstream seam while retaining v1 readers.

Tradeoff: cleanest single-artifact domain model and strongest atomicity, but
largest migration and regression surface. Attempt facts force unrelated cue
editing contracts to migrate.

### Option C — orchestration overlays around frozen v1

Add manifest-last `sync-result-v1` and `transcription-result-v1` directories.
Each binds a frozen v1 projection plus a new text-free report. New FCPXML paths
consume the complete sync result to apply relays; legacy v1 consumers retain
only the primary projection.

Tradeoff: smallest change to direct v1 validators and examples, but the sync
result risks overlapping authority between its projection and relay report.
Every consumer must be explicit about whether it has only legacy primary facts
or the complete relay authority.

The narrower Gemini variant that computes relays but never applies them to
FCPXML is not a completion option unless relay application is explicitly
deferred.

## Recommendation

Choose Option A and name the public work `Task 14 — parity prerequisites`.

Use this hard milestone order:

1. production-wire anomaly detection and verdict; VAD remains off by default;
2. production-wire manifest／report, degradation, and alternative-source retry;
   VAD remains off by default;
3. wire a verified closed VAD registry and explicit `--vad` behavior;
4. retain a mechanical test proving default-off until steps 1–3 are green;
5. flip VAD default and test default-on, explicit-on, opt-out, contradictions,
   no-audio misuse, early model rejection, and retry-setting equality; and
6. land `sync-map-v2` relay, drift, coverage, forced audio master, and installed
   FCPXML consumption as the independent sync work package.

Stop before step 5 if no verified public VAD registry pin exists. That is a
truthful contract gap, not permission to manufacture a model identity.

## Provider status

| Lane | Requested | Observed | Completed | Result |
| --- | --- | --- | --- | --- |
| Codex | current primary model | `gpt-5.6-sol` | `gpt-5.6-sol` | completed independently before external outputs |
| Gemini controlled REST | `gemini-3.7-flash` | `gemini-3.7-flash` | `gemini-3.7-flash` | completed; input 2,469, output 2,825, total 5,752 tokens |
| Claude subscription wrapper | dynamic `opus` capability alias | null | null | incomplete: `claude-timeout`; dispatch ambiguous; no retry or fallback |

Claude attempt ID:
`1e764fbd-d3cf-4aa6-af88-dbdd62c857df`.
