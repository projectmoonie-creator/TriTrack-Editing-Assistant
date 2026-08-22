# Task 14 amendment v2 Codex review and adjudication

Review date: 2026-08-22

## Frozen review identity

- Exact reviewed target: `7232267a236cbb35f210d5088cb02ca69201d473`
- Frozen packet: `task-14-amendment-v2-review-packet-2026-08-22.md`
- Packet SHA-256:
  `f6c530b5886a13b1b14284d636ec8457e3c9545e91aeb4e82c6013deae9efc55`
- Requested／observed／completed model: `gpt-5.6-sol`
- Reasoning effort: `xhigh`
- Codex session:
  `01a02963-37df-7f12-88db-68dba69e255f`
- Reported token use: `223620`
- Review mode: read-only source inspection plus in-memory adversarial checks

The shutdown log contained localhost MCP initialization warnings after the
review result was complete. They did not affect source access, the reproduced
counterexamples, or the final finding list. The reviewer changed no repository
file.

## Required findings

| ID | Severity | Finding | Adjudication |
| --- | --- | --- | --- |
| `T14V2-001` | major | A fully resigned report could append a retry after a usable primary because the validator recomputed adoption but did not prove that every non-final attempt justified retry. | Accepted. The validator now calls the shared retry verdict for every non-final candidate. A fully resigned loader regression proves rejection. |
| `T14V2-002` | major | A valid empty bundle take could be labelled `sparse` and selected, even though the shared policy classifies empty before sparse and selects no empty source. | Accepted. Non-reused selection now cross-binds the selected attempt outcome to a completed, non-empty bundle take. |
| `T14V2-003` | major | Embedded run validation accepted a v1 result manifest around a v2 report and accepted noncanonical report bytes when hashes were updated. | Accepted. Standalone and embedded-run paths now call the same exact-byte family, canonicality, hash, density, and semantic validator. |
| `T14V2-004` | major | Ceiling milliseconds turned 479,999 frames at 16 kHz (29.9999375 seconds) into 30,000 ms and incorrectly subjected short media to the sparse threshold. | Accepted. Normalized frame count and sample rate are preserved and used as an exact rational duration; ceiling milliseconds are retained only for cue bounds. |
| `T14V2-005` | minor | The human threshold row exposed 30 seconds but omitted the 1.000 characters／second threshold. | Accepted. The table now has an explicit row kind and serializes both threshold values on the threshold row. |
| `T14V2-006` | minor | Two semantic-drift loader tests kept stale density bytes, so they failed before reaching relationship validation. | Accepted. The tests now regenerate density, update its hash, and rebuild canonical manifest bytes before asserting semantic rejection. |

There were no optional-hardening notes.

## RED／GREEN disposition

Each accepted finding received a test that failed for the reproduced reason
before production code changed. Corrected focused suites passed 92 tests; the
complete suite then passed 344 tests. Ruff, compilation, and diff hygiene also
passed.

The exact bounded fix target is
`f8b77e65ac0a51d19efbda159d7441cb3be870e4`. The review did not authorize or
perform any tag, Release, package publication, tester contact, private
integration, or application submission.
