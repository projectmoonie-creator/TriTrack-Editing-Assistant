# Task 11 closeout adjudication

Adjudication date: 2026-08-18

## Frozen review target and attempts

- Base: `b4e21d660170dfd000c99ba38f55f825565ab922`.
- Candidate: `d53deb28aa86ef1aba9f978f44456f71bc315e57`.
- Packet SHA-256:
  `ab64798a971fdddeb3f093a4c3d0053e9d0d5c71712c81710cc0bb96663a92e2`.
- Fix-forward commit:
  `0493a92f8257c8721e1a4564b1e43bfec44c01dc`.

The packet digest above identifies the exact provider input. The tracked public
packet is a path-sanitized copy as declared in its sanitation note; it preserves
all target bytes and review questions but intentionally has a different digest.
Its public-copy SHA-256 is
`589670cfc3691274d0725d4a13f3fce7f103954e20b22e2188d83c37b9ff92a1`.
The maintainer recorded the Codex review before reading an external answer.
Gemini completed with `NO FINDINGS`; requested, observed, and completed model
were `gemini-3.7-flash`. Its response SHA-256 is
`01cf0fdb94288328d0416618a65461f42db1045d3583c1ee7973ca3bf71726c8`
before the repository text convention added one final newline. The tracked
copy SHA-256 is
`f2224880b91ee20ddc3128b56cca6906b852f7872c0a54718cd14a12cbdc2dc4`,
and status-ledger SHA-256 is
`23477e1e5ea7956daf7567c08a82c80138f9f277c6ef3156e29ce30bdf0ac504`.
Its clean review does not override source-backed findings.

The one Claude subscription attempt
`67528669-94b0-4e39-87bd-ab903b2bd552` requested the dynamic `opus` alias and
ended `claude-timeout`. Observed／completed models and usage are null;
`modelRequestSent` is null because dispatch completion is ambiguous. The
status-ledger SHA-256 is
`8a9ad815258509d1d2898387ff48d54bdc65ed1caf7cee48d7022dc3827f06c0`.
There was no retry, downgrade, API credential, paid fallback, or provider
substitution. The incomplete attempt contributes no finding or pass claim.

## Finding-by-finding adjudication

### C-1 — `agree`／major: inspection and hashing used different reads

At the frozen candidate, `scripts/release_gate_core.py:481-490`, `:517-562`,
and `:1188` inspected metadata and members from a path, then used later
unbounded `Path.read_bytes()` calls for final digests and wheel comparison. A
replacement could make the digest describe uninspected or over-limit bytes.

Fix: one bounded `O_NOFOLLOW` regular-file read now supplies the same immutable
bytes to ZIP／TAR inspection, hashing, and reproducibility comparison. RED:
replacement during member scanning changed the returned digest. GREEN: the
digest remains bound to the inspected bytes.

### C-2 — `agree`／major: manifest-last did not re-bind linked archives

At `scripts/release_gate_core.py:946-955`, archives were hard-linked first, but
their linked bytes were not checked against manifest hashes before the final
manifest link.

Fix: publication reads only the validated size／digest facts, then verifies each
linked output's regular type, exact size, digest, and stable descriptor
signature before linking the manifest. RED: a post-fsync archive change still
published success. GREEN: `TRITRACK_RELEASE_ARCHIVE_CHANGED` is raised and no
manifest exists.

### C-3 — `agree`／minor: missing run directory used exit 65

At `src/tritrack_editing_assistant/run_workflow.py:302-309` and
`src/tritrack_editing_assistant/cli.py:610-625`, a missing run directory became
`TRITRACK_RUN_BUNDLE_INVALID`／65 instead of unreadable-input I/O.

Fix: missing, non-directory-parent, and permission failures at the run root now
become `TRITRACK_RUN_INPUT_UNREADABLE`／74. Invalid existing bundles remain data
errors. RED returned 65; GREEN returns 74 with a path-free code.

### C-4 — `agree`／major: bare credential shapes could pass

At `scripts/release_gate_core.py:244-317`, assignments and private-key headers
were rejected, but a bare token-shaped value passed despite the approved
high-entropy credential boundary.

Fix: conservative GitHub, AWS, Google, and Slack token shapes are rejected.
Test canaries are runtime fragments, so tracked source has no complete token.
RED accepted the bare canary; GREEN rejects it without echoing the value.

### C-5 — `upgrade` from note to `agree`／minor: policy was partly inert

Reproduction upgraded the drift note: code allowed fake secret `editor`, while
the checked-in policy did not, and the loader accepted unexpected nested keys.

Fix: code and policy allowlists now agree exactly; the loader closes the exact
limits, source, wheel, and sdist keys. RED accepted an expanded allowlist and
an extra wheel key; GREEN rejects both with
`TRITRACK_RELEASE_POLICY_INVALID`.

## Fix-forward verification

- The focused RED run produced four expected failures; the missing-run
  regression separately returned 65 instead of 74.
- The focused GREEN run passed 15 tests.
- The complete suite passed 238 tests.
- Ruff and `compileall` passed over all public Python surfaces.
- Packaging policy tests passed twice consecutively.
- `git diff --check` passed.

The first post-review release-gate attempt correctly rejected the initial
packet copy because its complete diff retained a historical local-home literal
inside removed lines. That commit was never pushed and is absent from the
public branch history. The public branch was rebuilt from the fix-forward
commit, the two removed-line path literals were replaced without changing any
candidate byte or review question, and the old username-specific packaging
regression became a generic invocation of the actual privacy scanner in commit
`33b44e30c54db23a1cbff325c7f4a7410980180e`. A scan of every tracked and pending
public file then passed.

The final clean gate, fast-forward, public push, and exact-SHA remote CI check
occur after this record is committed. Their transient identifiers belong in
the handoff rather than this frozen adjudication.
