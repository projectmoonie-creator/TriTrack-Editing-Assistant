# Task 14 amendment v2 decision: sparse-source guard

**Status:** accepted clean-room amendment on 2026-08-22
**Authorized behavioral input:** `task13-parity-v2`
**Relationship:** amends: `task13-parity-v1`
**Public base:** `1c9334290e75d1cc70a31b4b86cc273fcc59b2ae`

## Hash-bound intake

The handoff declares that it supersedes only v1's
`contracts/voice-activity-default.md`. Nothing else in v1 is retracted. The
public consumer verified every declared payload before using it:

| Payload | SHA-256 |
| --- | --- |
| `HANDOFF.md` | `9f03607e571d17ef13e715b8ca845630280c59cdce12c91a8d4b038daaaf454f` |
| `TRANSFORMATIONS.md` | `406890cc11fd9fe5b0c808806ca8d55fcc120ea2972c57e52ee73ecd3ab0cd15` |
| `contracts/transcription-observability.md` | `da42b2457af120d0a4bee380ec42fefde1b7ef8a226df12ab138cb7700bc4f4d` |
| `contracts/voice-activity-default-v2.md` | `499cd8e043eb289ecc7ac70b0306d2c5bacd6ecc0af396c046144c1902148f72` |
| `reference/sparse_master.py` | `ea8299914d2601133ca10aded54662c0475272003dbd89fca986da6f670489a8` |
| `reference/test_sparse_master.py` | `c10abf9afcbcbe2d580dfb4bcdb79e80ff464b3c06c0a48e24c8284e20b23c9e` |

No private repository, source media, transcript, receipt, path, or identifier
is an implementation input. The reference module is behavioral evidence, not
source to copy.

## Corrected gate

Voice-activity detection remains off. A later default change requires all
three behavioral guards to be production-wired and tested:

1. **in-cue repetition detection** catches invented loop text;
2. **sparse-source verdict** catches a long source that retained too little
   content;
3. **alternative-source retry** is driven by both verdicts, and the consumer's
   adoption decision is driven by the same two verdicts.

The prior two-part gate was insufficient. On the clean-room aggregate
measurement, detection alone changed one source from 1,162 characters to 93,
and a second recognizer reproduced the shape at 923 versus 95. The alternative
source retained 1,934 characters. These numbers explain the missing guard;
they do not claim that the same thresholds fit every language, recognizer, or
recording practice.

## Public design

- Reimplement content-character density and source choice as one pure public
  policy module. Sparse and invalid remain distinct verdicts.
- Preserve `transcript-bundle-v1` as cue authority.
- Preserve exact v1 report, result-manifest, and run-manifest readers.
- Publish new versioned report/result/run authority for density evidence rather
  than silently changing v1 schema bytes.
- Record exact normalized frame count and sample rate, character counts, a
  rounded readable density, thresholds and recognition settings, the source
  the consumer selected, retry/rescue/unrescued counts, and shared-alternative
  warnings. Ceiling milliseconds remain separate cue-bound evidence and never
  decide the 30-second sparse boundary.
- Emit one deterministic human-readable density table beside the machine
  record, with both the rate and minimum-duration thresholds on its threshold
  row.

The clean-room starting constants are 1.0 content character per second and a
30-second minimum. They are explicit, observable policy inputs to be
re-derived from public users' own material; they are not an accuracy claim.

## Preserved behavior

Content is counted by characters rather than cues; punctuation, marks, and
spacing are formatting rather than content. Short or unknown-duration media is
never guessed sparse, and the density boundary is strictly below the rate.
A usable primary wins. A sparse primary yields to a usable alternative but
survives when nothing better exists. An invalid primary never survives and may
adopt a merely sparse alternative. Retry and adoption use one choice policy,
every decoded source records density evidence, unrescued retries remain
visible, and two takes selecting the same alternative announce each other.
Every non-final attempt must itself justify retry; the result validator rejects
a fabricated attempt after a usable source and rejects an empty bundle take
mislabelled as a selectable sparse source. Standalone and embedded-run readers
share one exact-byte family, canonicality, hash, density, and relationship
validator.

## Non-goals

This amendment does not enable VAD, add VAD CLI switches, accept a VAD model
path, select or pin a VAD model, claim recognition accuracy, run downstream
private parity, or authorize a tag, release, package publication, tester
contact, private integration, or application submission.
