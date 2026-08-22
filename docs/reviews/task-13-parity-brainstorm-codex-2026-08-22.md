# Task 13 parity mechanisms — Codex independent brainstorm

Date: 2026-08-22

This response was completed before Claude or Gemini output was read.

## 1. `problem_reframe`

The core decision is not where to paste five algorithms. It is which new facts
become public authorities, and how they cross the already-frozen v1 process
seam without turning old artifact versions into moving targets.

There are two different ownership problems:

- relay selection changes the authoritative topology of synchronization, so it
  cannot be a diagnostic sidecar that FCPXML is free to ignore; and
- transcription attempts and settings explain how cue authority was obtained,
  but do not themselves become a second authority for cue text or timing.

The architecture should therefore be asymmetric rather than forcing both
domains into the same versioning device.

## 2. `pragmatic_path`

Use a new synchronization authority version plus a manifest-like transcription
result bundle.

For synchronization, add `sync-map-v2`. Represent each time-domain take as one
group with one A anchor, one primary B relationship, zero or more relay B
relationships, explicit match reasons, timing, coverage, and one forced or
automatic audio-master policy. V1 remains loadable and valid but never gains
new meanings. FCPXML loaders normalize v1 pairs and v2 groups into one internal
relationship model; v2 groups place the A source once and add each relay only
over its covered interval. A source with zero new coverage never enters the
group. This makes coverage a production fact rather than a test-only helper.

For transcription, keep `transcript-bundle-v1` as cue authority and add a new
manifest-last `transcription-result-v1` directory containing:

- one canonical `transcript-bundle-v1` with successful and proven-empty takes;
- one `transcription-report-v1` with run settings, per-take attempts, source
  hashes, selected attempt, invalid／failed codes, retry relationship, and
  explicit unknown markers for reused work; and
- one small manifest binding the exact hashes of both files and the requested
  source set.

The report does not copy cue text or timing. A failed take is present in the
report and absent from the cue bundle. The manifest makes that absence
unambiguous instead of overloading the bundle's `empty` status. Alignment can
continue consuming exact v1 cue bundles; the run workflow additionally requires
the report and manifest when it needs completeness claims.

Make one orchestration function own both standalone and `run prepare`
transcription. The standalone installed command publishes the result directory;
`run prepare` calls the same function with alternate relationships derived from
the just-created sync map. If compatibility requires retaining the old
single-file command, preserve it under an explicit `legacy-v1` mode whose help
states that it cannot make retry or complete-source-set claims. Do not let the
legacy mode be the default after this work lands.

Use a packaged closed registry only for public-engine-owned selectable pins,
especially the VAD model. Each entry has name, expected basename, exact size,
and SHA-256. Resolve a caller-supplied absolute model directory plus registry
name to the pinned file, validate it before decode, and never accept an
arbitrary VAD path. Keep the existing caller-owned recognition model path as a
separate input class: record its observed SHA-256 but do not label it with a
registry name or compare it with somebody else's pin. If recognition registry
selection is later offered, it must be a separate mutually exclusive flag.

Milestones are mechanical:

1. anomaly detector and invalid verdict are production-wired while VAD remains
   opt-in;
2. report／manifest and alternative-source retry are production-wired with
   invented tests while VAD remains opt-in;
3. VAD model registry and explicit `--vad` path are production-wired;
4. one source assertion and CLI integration test prove the default is still
   off until milestones 1–3 are green;
5. flip the default and add tests for default-on, explicit-on, opt-out,
   contradictions, no-audio misuse, early model failure, and matching retry
   settings; and
6. land sync-map-v2 relay behavior independently, then make the prepared run
   bind both the v2 sync authority and transcription result manifest.

Roadmap naming should be `Task 14 — parity prerequisites`. The old public Task
13 decision remains true history. The private-side parity proof can still be a
Task 13 activity elsewhere without forcing the public roadmap to reuse a
completed number.

## 3. `alternative_architecture`

Version both domains directly: `sync-map-v2` and `transcript-bundle-v2`, then
propagate aligned, grouping, working-cut, run-manifest, validator, and example
support for both versions.

This has the cleanest theoretical authority graph: every take, failed status,
setting, attempt, retry, and relay lives in a single versioned domain artifact.
It avoids a separate transcription manifest. The tradeoff is a broad migration
whose risk is dominated by downstream surfaces unrelated to recognition. A
failed take forces changes through alignment and paper-edit contracts even
though those tools cannot edit failed evidence. Supporting v1 and v2 in every
consumer also doubles compatibility cases during the pre-release phase.

Falsify the pragmatic hybrid if consumers routinely need attempt facts and cue
facts atomically inside one JSON value, or if manifest binding makes common
validation require multiple race-prone reads. In that case direct v2 is worth
the blast radius.

## 4. `low_cost_experiment`

Write three public command-level RED tests without implementation:

1. A sync fixture where one 600-second A source correlates with two 300-second
   B sources in sequence. Assert that the selected public artifact allows the
   string-out builder to place A once and both B relays, while a simultaneous B
   duplicate is absent.
2. A transcription fixture where the primary produces one stuttering cue and
   the synchronized alternative produces clean cues. Assert one output
   directory records both attempts, selects the alternative, and keeps cue text
   only in the transcript bundle.
3. A no-alternative fixture followed by a clean second take. Assert the first
   is reported failed, the second ships, and the batch command succeeds.

Try to express these tests with (a) direct v2 transcript JSON and (b) a
bundle／report／manifest. Compare the number of existing contract and consumer
files that must change before either RED can become semantically correct. The
experiment is falsifiable: if the manifest form cannot make completeness and
TOCTOU binding precise without duplicating cue authority, choose direct v2.

## 5. `contrarian_challenge`

Do not assume the measured VAD benefit obligates an immediate public default.
The handoff proves a default is defensible only under its measured conditions;
it does not supply a public model pin, exact current whisper.cpp switch
contract, or an invented end-to-end public fixture proving the installed engine
supports the selected VAD model. A closed registry with zero verified public
entries is honest; a default that names an unverified model is not.

If no publicly reviewable model pin can be established from authorized public
sources, complete anomaly detection, retry, provenance, and explicit VAD
plumbing, but stop before the default flip and report the exact missing pin as
a true contract gap. The ordering constraint is a lower bound on safety, not a
license to invent configuration evidence.

## 6. `unconstrained_possibility`

Replace A/B pair artifacts with a general time-coverage graph: sources are
nodes, measured offsets are edges with evidence classes, and take groups are
connected components projected into one timeline. Audio-master selection is a
group policy, and transcription attempts point to graph nodes. Relays and
simultaneous cameras become different constraints over the same graph.

This could eventually support N cameras and independent audio, but it violates
the current two-folder identity limit, has a much larger proof burden, and
should not be smuggled into the bounded handoff. It is useful only as a future
direction that explains why v2 should not hard-code an `extraB1`／`extraB2`
shape.

## 7. `overlooked_risks`

- Drift values need a precisely documented coordinate system. The reference
  accepts a `drift` scalar but the public correlation path currently exposes
  an offset; conflating them could make the prior self-validate the same noisy
  measurement it is meant to supplement.
- Selection order can make coverage greedy and non-optimal. Stable tie-breaking
  is required or input order will change extras and artifact bytes.
- A relay FCPXML group needs interval clipping; merely adding a second B clip at
  its raw offset can extend or duplicate the A segment.
- The transcription report can leak text through samples or error prose. Keep
  reasons as closed codes and cue text exclusively in the cue authority.
- A retry source may correspond to a different media basename. Take identity
  must remain the editorial take, while attempt identity records the physical
  source, or later cue-addressed revisions will drift.
- Degrading one take must not accidentally make a zero-success batch look like
  a valid empty transcript. Define whether the result can contain an empty cue
  bundle or must use a nullable bundle member plus report-only failure.
- Registering boolean switches is not enough; wrapper forwarding tests must
  prove standalone flags do not shift neighboring values.
- The release package policy has exact wheel members. New schema resources and
  registry data intentionally change those counts and must update the policy
  as a new candidate fact, not as a regression exception.
- The existing downstream example proves only aligned-transcript-v1. New
  contracts need validator discovery coverage without pretending the example
  has migrated.

## 8. `assumptions_to_verify`

- The producer accepts a new public roadmap task number even though the
  downstream need is still called Task 13 elsewhere.
- The public command may add a new manifest-last output-directory mode while
  keeping the old exact single-file command available.
- The installed whisper.cpp version exposes stable VAD and VAD-model switches
  that can be invoked through the bounded process wrapper.
- A public, legally distributable registry entry can identify at least one VAD
  model by exact size and SHA-256 without bundling it.
- The clean-room definition of `drift` can be derived from current public
  timestamps／offset evidence without any further non-public input.
- The public sync schema may introduce a source-neutral group shape even though
  the current CLI still scans two camera folders.
- Excluding failed takes from `transcript-bundle-v1` does not violate an existing
  documented completeness promise once the enclosing manifest records the
  exact requested set.

## 9. `recommended_next_decision`

Approve the asymmetric architecture:

- `sync-map-v2` for new authoritative relay topology;
- `transcription-result-v1` as a manifest-last bundle around the unchanged cue
  authority and a text-free provenance／attempt report;
- one shared orchestration path for standalone and prepared-run transcription;
- a closed registry only for engine-owned selectable pins, with caller-owned
  recognition models kept explicitly unregistered; and
- roadmap label `Task 14 — parity prerequisites`.

Also approve a hard stop before the VAD default flip unless a public registry
pin and installed-engine invocation are independently verified. This preserves
the handoff's ordering constraint without manufacturing the missing operational
evidence.
