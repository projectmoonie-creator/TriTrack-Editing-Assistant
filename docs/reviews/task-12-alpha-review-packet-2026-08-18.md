# Task 12 public alpha independent-review packet

## Review target and packet provenance

- Repository: projectmoonie-creator/TriTrack-Editing-Assistant
- Project identity: public-engine / OSS
- Exact review target: 283ec9f7018a497aa77ad54c53f380a4bc426031
- Starting public main: 71d719770f5b335ecd2f5f31ce98ea886e76b955
- Package version: 0.1.0a0
- Target tracked worktree: clean before packet construction
- Known local verification: 252 tests, Ruff, compileall, public identity, both
  canonical skills, and the maintainer release gate passed at the target.
- The packet SHA-256 is recorded by the maintainer after these exact bytes are
  closed. Do not infer it from this sentence.

## Objective

Independently review the complete public alpha composition at the exact target.
Find current actionable defects across Tasks 1–12, especially cross-task seams
that incremental reviews could miss. This is a read-only review. Make no edit,
provider call, build, test, network request, tag, release, or publication.

## Current alpha surface

The public engine implements local A/B sync, profile-bound deterministic
FCPXML, CPU-only whisper.cpp transcription, cue-addressed revision alignment,
offline Gemini-receipt conformance, XLSX paper-edit transport, grouping and
transcript-text-free working-cut compilation, immutable prepared/aligned/
finished run bundles, story-ordered FCPXML, four explicit read-only validator
modes, deterministic packaging, and fixed public CI. The component registry has
exactly eleven entries; the live Gemini transport remains planned.

## Authority and privacy invariants

- JSON authorities retain strict roles. Workbook and FCPXML are transports or
  projections, never replacement transcript/timing authorities.
- Exact-byte authority and artifact inputs use their documented bounded,
  regular-file, immutability, and cross-hash checks. Every publisher preserves
  existing outputs and race winners; media probing remains scoped as documented.
- The default path is local and offline. Provider receipt validation is
  offline; no live provider transport is shipped.
- Public summaries are path-free and content-limited. Tracked source, packets,
  and distributions contain no private media, transcript, credential, local
  home path, or proprietary template.
- Run and release outputs publish the manifest last; a missing manifest is an
  incomplete result and is never repaired in place.

## Package and release-gate facts

The canonical target release manifest is reproduced below in full. Its exact
tracked file was generated only after the source commit was clean. The wheel
was byte-identical across two builds. The sdist normalized member inventory was
identical across two builds; compressed sdist byte reproducibility is not
claimed. A fresh environment installed the selected local wheel, ran pip check,
confirmed eleven components, and exercised all five validator help surfaces.

--- BEGIN TARGET RELEASE MANIFEST ---
{"artifacts":{"sdist":{"memberCount":103,"memberInventorySha256":"f428677f07794ee9b10a06da8b2595843eb2af125a3362df3b41548d53d09ded","sha256":"75aba42a7017c7d2ab2b92e397fa94de55d6bec4ed1108ef5ef8a45d1e926b51","sizeBytes":181473},"wheel":{"memberCount":38,"memberInventorySha256":"4bc6644aa0dd1740783b4e26aadfab00a5a26d51233df6b54699a7df0a0f4384","sha256":"ab3a0c0ec66bcfe09a5500034250f4076e5ead1206bf90fa350f2949d9438643","sizeBytes":86062}},"gates":{"freshInstall":"pass","sdistArchive":"pass","sourceIdentity":"pass","sourcePrivacy":"pass","wheelArchive":"pass"},"nonClaims":["no-tag","no-release","no-package-publication","no-pull-request","no-tester-contact","no-signing","no-attestation","no-sbom","no-final-cut-gui","no-dtd","no-provider","no-application-submission"],"platform":{"machine":"arm64","system":"Darwin"},"project":{"commit":"283ec9f7018a497aa77ad54c53f380a4bc426031","name":"tritrack-editing-assistant","version":"0.1.0a0"},"reproducibility":{"sdistMembersMatch":true,"wheelBytesMatch":true},"schemaVersion":"tritrack.release-manifest/v1","sourceInventory":{"count":128,"sha256":"673717d4ff23e23cfe31fdcccfef35834c093ecb14ca395376e183633da3bf06"},"toolchain":{"build":"1.5.0","implementation":"CPython","pip":"26.2","python":"3.13.15","setuptools":"84.0.0","wheel":"0.48.0"}}
--- END TARGET RELEASE MANIFEST ---

## Fixed CI contract

The workflow is exactly Ubuntu 24.04 x64 and macOS 26 arm64 on Python 3.12 and
3.13, plus one Ubuntu/Python 3.13 quality job and one local candidate-gate job.
Official Actions are commit pinned, permissions are contents read-only, and no
artifact is uploaded or published.

The last baseline before this target was GitHub Actions run 32108409857 at
commit 71d719770f5b335ecd2f5f31ce98ea886e76b955; all six jobs passed. Task 12
will require a new exact-target-independent review and later exact-SHA CI; the
baseline is context, not proof for this target.

## Prior review state

Tasks 7–11 each retained Codex-first and provider review records. Gemini
completed their recent formal closeouts. Several formal Claude subscription
attempts ended claude-timeout and remain incomplete. A later producer-mediated
interactive Claude review of public main returned NO FINDINGS plus four
optional observations; two reproducible minor defects were fixed, one test gap
was covered, and one hypothetical token observation was rejected. No old
timeout has been converted into completion.

The first Task 12 target (7ec69bd0ef045c18eb7899e95ff1472ca5913d05) received an independent Codex review
with two source-backed major findings: one sync-map loader applied its size
limit after an unbounded read, and the maintainer gate applied its subprocess
output limit after capture. Gemini returned NO FINDINGS, which does not
override those reproductions. The single Claude subscription attempt ended
claude-timeout and remains incomplete. A second internal target fixed both,
then Codex found that descriptor readers could still block while opening a
FIFO before reaching their regular-file checks. That second target was not
sent to external reviewers because it was already known to be superseded.
An additional convergence pass found the same blocking-open risk in older
path-based readers used by transcription, normalized WAV inspection, and CLI
output hashing. Those intermediate targets were not sent to external reviewers
because they were already known to be superseded. This target contains all TDD
fixes: descriptor-bounded sync-map input, streaming bounded subprocess capture
with process-group termination, nonblocking opens before regular-file checks,
stable descriptor-bound hashes, and read-before/read-after identity checks.
The sdist-only Basic Title capture inputs now use the same bounded boundary.
The package policy also owns a fixed SOURCE_DATE_EPOCH instead of deriving it
from commit time, so a later package-excluded evidence commit can satisfy the
approved exact-wheel-equality proof without falsifying Git timestamps. Review
the fixes and the complete resulting alpha composition.

## Task 12 freeze boundary

The producer selected a two-layer Git design. alphaReviewTarget is the exact
commit reviewed here. A later alphaEvidenceRecord may add only package-excluded
review evidence, Task 12 verification, current status, and the status boundary
test. The later commit must prove exact wheel equality, normalized sdist
content equality, and equal src tree identity. Its release manifest will
correctly differ in commit and tracked-source inventory. No tag or release is
authorized.

## Requested review dimensions

1. registry and implemented/planned truth;
2. authority ownership across every strict artifact and projection;
3. offline/privacy/credential/subprocess/source-immutability boundaries;
4. determinism, canonical bytes, timing, exact hashing, and cross-binding;
5. validator scopes, stable errors, read-only behavior, and claim limits;
6. run-bundle chains and manifest-last interruption/race behavior;
7. source/archive/package privacy, reproducibility, and fresh installation;
8. fixed CI matrix, pins, permissions, wheel smoke, and no publication;
9. docs, compatibility, role firewall, skills, and outward-action boundary;
10. missing tests or cross-task seams not covered by incremental closeouts.

## Finding schema

Return:

- Summary: NO FINDINGS or count by severity.
- Findings, each with stable ID, blocker/major/minor severity, confidence,
  current file and line, exact failure mechanism, impact, smallest safe fix,
  and test or reproduction.
- Optional observations in a separate non-blocking section.
- Inspection record naming the target and files actually inspected.

A blocker requires current file-and-line evidence or a reproducible failing
contract. Do not treat a historical timeout as a finding. Do not broaden a
successful validator or gate beyond its documented scope.

## Explicit no-edit and non-goal boundary

Do not edit files. Do not invoke product commands, tests, builds, network,
providers, GUI applications, or credentials. Do not propose Task 13 private
integration as a Task 12 requirement. No tag, release, package upload, signing,
attestation, SBOM, PR, tester contact, application submission, Final Cut GUI,
DTD, live provider, force-push, remote change, or visibility change is in scope.

## Exact target inventory

--- BEGIN GIT LS-TREE INVENTORY ---
100644 blob cfe3349a5c3fc816d118da5552204e3316656be1    5487	.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md
100644 blob ce063cbdaaa20af6226932804bc2b99eed491eb9     320	.agents/skills/tritrack-editing-assistant-maintainer/agents/openai.yaml
100644 blob ead49d8efc3aac3a97ed1f1c98befb51b01c78a5    1815	.agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py
100644 blob cbbf8dbf6a1f3fbc25aadfdab1a1ce1e3609c830    4439	.github/workflows/ci.yml
100644 blob 6fbab3487be340501160d20f30933754dc155096     132	.gitignore
100644 blob f9e72a3f51bb881d936d2e2eaf0c30c0fb72ded8     212	.tritrack-project.json
100644 blob 3c0ad2e0ea44c6390c086025147ed74e87823deb    3868	AGENTS.md
100644 blob fa26dcbe8121453289e7b2044afd6fe19899326c    3110	CHANGELOG.md
100644 blob 74763d35fc86a83ea3bdd9a71ce38c72d347ad22    1721	CODE_OF_CONDUCT.md
100644 blob 053cf916a4b6ae3f96d54c1ac0f306d8ad9b587f    1476	CONTRIBUTING.md
100644 blob 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64   11357	LICENSE
100644 blob 6edd3aadad38ba50caf2f7e4e09e588830461684     986	MANIFEST.in
100644 blob c0e25cec57851f1124d3f7a10751c9ad844d5191     293	NOTICE
100644 blob 405c733fef76be09833011cbf6e702ebdf717836     537	PRODUCT-WISHES.md
100644 blob 392a6eaedd15949cc1b7be7f7586d9e3776e54e0   16086	README.md
100644 blob bd84102d761905cbfde093bcce8fdf3fcbc3b87c    1488	SECURITY.md
100644 blob 9024ff0ee14f2f747236eac55c7f5bd910a3dab6   13210	STATUS.md
100644 blob 6ca3bdde293d70acbf5c14d38dda0c0d19e04349    2909	docs/ROADMAP.md
100644 blob 260e21381a16aba8d44ded44be328ff2bbc3a6dd   11532	docs/TASK-10-DECISION.md
100644 blob ffbbb3e0f379fb3bb129ab0613abb12b69b8435c    5485	docs/TASK-10-VERIFICATION.md
100644 blob 4ee22551177c3374ffaf83a64d7e9cc7ca680928   10825	docs/TASK-11-VERIFICATION.md
100644 blob 257edd670e7c83543cf3690b9176ff9cc690ab87    9219	docs/TASK-6.5-HANDOFF.md
100644 blob bb44df2251acb99e2e4c7187ec1f4a88669689ed    3530	docs/TASK-6.5-VERIFICATION.md
100644 blob ac8bd238c61a5d8cb32b79c8b7e72d7b16ae3df9    4029	docs/TASK-7-DECISION.md
100644 blob b277d527b1218976bd8b6f4a7571dde3738e0828    5365	docs/TASK-7-VERIFICATION.md
100644 blob 02b40107ec0f8d11449cdd6c01cc29365a428ea2    4922	docs/TASK-8-DECISION.md
100644 blob 9ffc028f4a6e701006c29a1264163343da1262d5    6484	docs/TASK-8-VERIFICATION.md
100644 blob 4faf72913231ab1d5b909665fb20ba66a720fc5d   14589	docs/TASK-9-DECISION.md
100644 blob 28f767f643b618cb628b52dd0f5cf3c49a525dad    6887	docs/TASK-9-VERIFICATION.md
100644 blob d4ab477869bb0aeaac234584b876827e06e85505   16909	docs/TOOLING.md
100644 blob bc2c69a7829cc0fce16b2d8d21a29b09e7fe87ae    4825	docs/reviews/claude-incomplete-audit-2026-08-18.md
100644 blob 30bff0e2e3ea98f2ce96d85328280ac8da36667c    2445	docs/reviews/task-10-closeout-adjudication-2026-08-17.md
100644 blob b18abe7267545e7555e655ac9d2d4b2f7ac264b0    1284	docs/reviews/task-10-closeout-claude-2026-08-17.md.status.json
100644 blob 055f7b014368a630fd5d5b415b98e8ba9678188c    3561	docs/reviews/task-10-closeout-gemini-2026-08-17.md
100644 blob 481830d2b7dbb9be3260b9f356f6fc9ff8fb6bec     530	docs/reviews/task-10-closeout-gemini-2026-08-17.md.status.json
100644 blob c9a0a19fd386ac219b213a0f9929f0d4073a191c  235355	docs/reviews/task-10-closeout-packet-2026-08-17.md
100644 blob 4829272e987c3c504ed4f11804901fb3849a82f7    5742	docs/reviews/task-11-closeout-adjudication-2026-08-17.md
100644 blob 52ffe978a50ba50cc7bcf366f6e671090449c70e    1284	docs/reviews/task-11-closeout-claude-2026-08-17.md.status.json
100644 blob 1286328091eb09958c3513a5fabc367669beab18     904	docs/reviews/task-11-closeout-gemini-2026-08-17.md
100644 blob 12ab5f8829cdf60c23523db1769b19a761cbb368     530	docs/reviews/task-11-closeout-gemini-2026-08-17.md.status.json
100644 blob 48342481c9808d3b8784339d37a28619d5dcc195  259584	docs/reviews/task-11-closeout-packet-2026-08-17.md
100644 blob d5d3c52f78e06a4d9e91777b5f7643065085f13d    2021	docs/reviews/task-9-closeout-adjudication-2026-08-15.md
100644 blob 98600bb1787efb371d671eef172f01a4451b810d    1281	docs/reviews/task-9-closeout-claude-2026-08-15.md.status.json
100644 blob 05587af8187643b257fbcd47bac7d5f1836b309f    2674	docs/reviews/task-9-closeout-gemini-2026-08-15.md
100644 blob 82ec5d632742d78b09c9c41422b5c44c93971164     530	docs/reviews/task-9-closeout-gemini-2026-08-15.md.status.json
100644 blob 885dd1611d65c3f42268642d8f0d624e66cb77e4  186761	docs/reviews/task-9-closeout-packet-2026-08-15.md
100644 blob 153b34eef119d833501c4a21d77036a3e15c53f0    1756	docs/reviews/task-9-post-fix-adjudication-2026-08-16.md
100644 blob e8a03a3a1af66354edebca0596061e462d67329f    1281	docs/reviews/task-9-post-fix-claude-2026-08-16.md.status.json
100644 blob cc135f7952bdcf2dfe66b28871000ef05eed3d6a     753	docs/reviews/task-9-post-fix-gemini-2026-08-16.md
100644 blob 84c2b85114dcafadb6dbca287708c46bcea2f48f     530	docs/reviews/task-9-post-fix-gemini-2026-08-16.md.status.json
100644 blob 4a23cb6a3258969bc0d4fbee31ddef3197e36115    9521	docs/reviews/task-9-post-fix-packet-2026-08-16.md
100644 blob 8a97836d1ee867fdbd0d29ed46b7c10314d8f28c    3648	docs/reviews/tasks-7-11-claude-manual-adjudication-2026-08-18.md
100644 blob 1eac1cb861af0d089d7d057743cf8fbec08dd4a9    2986	docs/reviews/tasks-7-11-claude-manual-review-2026-08-18.md
100644 blob 9c6db3444ac975fea88d900312a591f6f632c5b9    1300	docs/reviews/tasks-7-11-claude-recovery-2026-08-18.md.status.json
100644 blob 7a3f237ad56bd419d1b5323b4004077ccc3dcb84    8373	docs/reviews/tasks-7-11-claude-recovery-packet-2026-08-18.md
100644 blob 7674c8667a369d061bce65dd4cef10a47519fe1f   15629	docs/superpowers/plans/2026-08-15-task-8-text-alignment.md
100644 blob 1739f7f53b31913f3b395e4663e0f98a9b52d53c   19295	docs/superpowers/plans/2026-08-15-task-9-organizer-paper-edit.md
100644 blob d2971d9927a6db0ab6ecd547610122c370e4df9c   21269	docs/superpowers/plans/2026-08-17-task-10-immutable-run.md
100644 blob 1a0aa1496c4b4c242c9da2f34d0ae1e7119f2467   44346	docs/superpowers/plans/2026-08-17-task-11-release-readiness.md
100644 blob dc7830aa04ec4e24216c67a5661d6ac173151dbc   21059	docs/superpowers/plans/2026-08-18-task-12-alpha-freeze.md
100644 blob 1c5c80ebeaff5a424101c0aa50a69c476f38e711   20294	docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
100644 blob f7215e96ec36e04980ba20184bed177285fddd58   12758	docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md
100644 blob 640909155abcd01a95b266cf79281dd66e3183f1    1556	evidence/basic-title-v1/roundtrip-report.json
100644 blob 746300406ac90798bf4c4c61bc18b1f7592d040b    9633	examples/quickstart_demo.py
100644 blob 978f27f9a722a430dda03048e2d735b5a242fc07     243	package.json
100644 blob 9659703b67a6993ae00ec6bea55bad660ff173b3    1054	pyproject.toml
100644 blob bba414acf839d7a75a858b46d8e4410fb009c589    7231	release/package-policy-v1.json
100644 blob 53c8c8da8fe3dd240d8e80caae956fbe08aba902    3983	release/release-manifest-v1.schema.json
100644 blob 194fc9274eb5986e02bb3a04be64014c7dc1aeb9     108	requirements/ci-constraints.txt
100755 blob f681b0cd3f4f72ab5294779ebc04f0ee276d8454   10147	scripts/capture_basic_title_binding.py
100644 blob 924ea76306755a8aab5e5950754ecd1cf6af4796    1951	scripts/release_gate.py
100644 blob 6236c4235e77fdaf5671c7931ae6f248e0b03a9a   52929	scripts/release_gate_core.py
100644 blob 210dcbaa33ce1ff58947ec4be5eb92e985a122f2    5371	skills/tritrack-editing-assistant/SKILL.md
100644 blob 169cb80650eaeb46f76e59a1b68cf044521975d4     240	skills/tritrack-editing-assistant/agents/openai.yaml
100644 blob c932b4e38ffd060537643450c32634d706a02974      74	src/tritrack_editing_assistant/__init__.py
100644 blob bbdf794b06789959916951368064f1b81314f5ce   10986	src/tritrack_editing_assistant/align_text.py
100644 blob ed6dfe42713caa2392f65e66c07db4f01216e72e   36355	src/tritrack_editing_assistant/cli.py
100644 blob 6403a6754a86c8aa5fbda0ba884f72839ba5e3bf    2528	src/tritrack_editing_assistant/contracts.py
100644 blob 8a02e5363acab6e958600c30ccddefff85da3aa7    8858	src/tritrack_editing_assistant/doctor.py
100644 blob a2ec2f148c8b239938796e88fc75da1079be1021   20531	src/tritrack_editing_assistant/emit_fcpxml.py
100644 blob c1d8be53504355e42e5b9ae0b2ad6494e56105ea    4517	src/tritrack_editing_assistant/gemini_hybrid.py
100644 blob 39d89ef8b0af947336f28363d40fd139998fefc6    1675	src/tritrack_editing_assistant/hallucination.py
100644 blob 773791b722bd1cc72920b0c88066e5554561a26c   16878	src/tritrack_editing_assistant/organizer.py
100644 blob 06bc13bec93fb5be8d7f710fec15190b5f1b8589   25207	src/tritrack_editing_assistant/paper_edit.py
100644 blob ddbe40717a1ede302a5e1ef3248779d301231f7f    9825	src/tritrack_editing_assistant/process.py
100644 blob eb6e3c4d2e11feebdf7795c8902a5a08e471c879      67	src/tritrack_editing_assistant/profiles/__init__.py
100644 blob 287353179c7fc8d78a5a0a2fa04813a63261a271     461	src/tritrack_editing_assistant/profiles/basic-title-v1.json
100644 blob 7954b6879cc68998be92a790f19e79f34186d55e     283	src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json
100644 blob 3415c2678bb2de9dd39b156eb3b15c5fcde105d3   34374	src/tritrack_editing_assistant/run_workflow.py
100644 blob 836f666077292a4b8864c0094f099bf7c48e3428      59	src/tritrack_editing_assistant/schemas/__init__.py
100644 blob d39f6901c4bfd26dfa29d618bca52604ccf93692    2256	src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json
100644 blob b28e5a443843e9da999b8f397241d1c2da8a4fca    1054	src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json
100644 blob ffec1424ec87220292ad6ae926f7aef17157440a    2887	src/tritrack_editing_assistant/schemas/grouping-v1.schema.json
100644 blob 66a6269bd183a76adf4c6e270175316d070d6de5    2268	src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json
100644 blob 6b20f42bdf64f38805eb51c8fb45506ebd36ebde    5986	src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json
100644 blob 2a2a6e13106765a8d5053755f3e6362e13cd2126    2155	src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json
100644 blob f005cc8f9c2d8e8bdca7a0e6488e06beec32196a    1462	src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json
100644 blob aae793bbfb547dd39eddd65d3f1e760ac0ac3d9f     968	src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json
100644 blob bd3764dc997ab9e0eaa5d542478ee61839ad7ed9    2369	src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json
100644 blob 6ef57c5b8d4f934854b3817f58bde49eaddc0e13    3556	src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json
100644 blob 5521e794788a635a6b4c5c9267a53079a7bea127   27621	src/tritrack_editing_assistant/story_fcpxml.py
100644 blob d4b1568e31da5412db9e86336647cebc632d43d5    9518	src/tritrack_editing_assistant/string_out.py
100644 blob c0a329c402ca049c772aad333cc1621cf497a3a2   17884	src/tritrack_editing_assistant/sync_scan.py
100644 blob de07a06fec1661a01a606af06525f26b0be065ea   17380	src/tritrack_editing_assistant/transcribe_takes.py
100644 blob 28d8c8202e6d00650381f6c056ebbd3188de8552    6420	src/tritrack_editing_assistant/validate_artifacts.py
100644 blob e161e0b9a731213e890333d16ddd1a76cb561d7f    3611	tests/task9_fixtures.py
100644 blob 4116dbb1983df797d65ba554f53a1ec0ba729964   17266	tests/test_align_text.py
100644 blob a11320c65ea0e30fa97b156b0c10bc1df8509238   47843	tests/test_cli.py
100644 blob ea341a249f4ba3e3777f6723add0b789df787b1d   14631	tests/test_contracts.py
100644 blob 5cdf2d7d790b5c6c39c664fde822e188d6b372d8    6735	tests/test_doctor.py
100644 blob 95667456984a88be23a4d7f4fe84df92d5e42385   15857	tests/test_emit_fcpxml.py
100644 blob d3a43fbf526c46eeb6aff219223989e7835fe4e9   13498	tests/test_gemini_hybrid.py
100644 blob 480fc44049a013acae0a390ea66a423779edbd9b    1270	tests/test_hallucination.py
100644 blob 06a219fdada72d1c4e13bc39953c59984404c293   10572	tests/test_maintainer_boundary.py
100644 blob 7c12d244ade918559baad4fce9fecac0d88d6689   14189	tests/test_organizer.py
100644 blob e3ba32465b04e69456cd0299d82d74b0e5b41b35    8880	tests/test_packaging.py
100644 blob e1722c0a54d49c255ae54d2e13d252b207e3e4c8   25126	tests/test_paper_edit.py
100644 blob 4861dec2eacc38acf021be6814e7e2fcaa60f4e2    4878	tests/test_process.py
100644 blob ddfad1bf8464e412714aa596c4c5a19aea11b24e   12417	tests/test_quickstart_demo.py
100644 blob 4f357db8438fdad0294bb1076dea26317893f2fc    3993	tests/test_release_ci.py
100644 blob 5c6bf3b5840355df441e47b840647146306de070   31837	tests/test_release_gate.py
100644 blob 56c58ae5ab78f9570c0badde0a7d89edb0ca970e   40808	tests/test_run_workflow.py
100644 blob 4d2f1aeaf1bc8dbfb075e969799596db92fff130   28219	tests/test_story_fcpxml.py
100644 blob 1929cd85b4b8d76cd0cd3c1a024c427141b7cb42    7693	tests/test_string_out.py
100644 blob 7e22ee5fbb1bb2204dd0c5a64835ff4a1495a960   12677	tests/test_sync_scan.py
100644 blob f85e6bc92d3830da810af6018f1923c71620df05    7867	tests/test_title_binding.py
100644 blob 742875431edb1110a65076fc2b5bbe24706f5f62   30777	tests/test_transcribe_takes.py
100644 blob 2bdd228178532e1ecfbffbe4db9308acbb9f8932   17207	tests/test_validate_artifacts.py
--- END GIT LS-TREE INVENTORY ---

## Exact fix-forward diff from the first Task 12 target

--- BEGIN FIX-FORWARD DIFF ---
diff --git a/release/package-policy-v1.json b/release/package-policy-v1.json
index 8e7d975..bba414a 100644
--- a/release/package-policy-v1.json
+++ b/release/package-policy-v1.json
@@ -1,82 +1,85 @@
 {
   "schemaVersion": "tritrack.package-policy/v1",
+  "build": {
+    "sourceDateEpoch": 1704067200
+  },
   "limits": {
     "sourceMaxFiles": 4096,
     "sourceMaxFileBytes": 2097152,
     "sourceMaxTotalBytes": 134217728,
     "archiveMaxBytes": 67108864,
     "archiveMaxMembers": 2048,
     "memberMaxBytes": 33554432,
     "expandedMaxBytes": 268435456
   },
   "source": {
     "allowedFakeHomeUsers": [
       "editor",
       "example",
       "fake",
       "test"
     ],
     "allowedFakeSecretValues": [
       "example",
       "fake",
       "placeholder",
       "redacted",
       "secret",
       "test"
     ],
     "forbiddenSuffixes": [
       ".aac",
       ".aif",
       ".aiff",
       ".avi",
       ".fcpxmld",
       ".m4a",
       ".m4v",
       ".mkv",
       ".mov",
       ".mp3",
       ".mp4",
       ".wav",
       ".xlsx"
     ]
   },
   "wheel": {
     "expectedMembers": [
       "tritrack_editing_assistant-0.1.0a0.dist-info/METADATA",
       "tritrack_editing_assistant-0.1.0a0.dist-info/RECORD",
       "tritrack_editing_assistant-0.1.0a0.dist-info/WHEEL",
       "tritrack_editing_assistant-0.1.0a0.dist-info/entry_points.txt",
       "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/LICENSE",
       "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/NOTICE",
       "tritrack_editing_assistant-0.1.0a0.dist-info/top_level.txt",
       "tritrack_editing_assistant/__init__.py",
       "tritrack_editing_assistant/align_text.py",
       "tritrack_editing_assistant/cli.py",
       "tritrack_editing_assistant/contracts.py",
       "tritrack_editing_assistant/doctor.py",
       "tritrack_editing_assistant/emit_fcpxml.py",
       "tritrack_editing_assistant/gemini_hybrid.py",
       "tritrack_editing_assistant/hallucination.py",
       "tritrack_editing_assistant/organizer.py",
       "tritrack_editing_assistant/paper_edit.py",
       "tritrack_editing_assistant/process.py",
       "tritrack_editing_assistant/profiles/__init__.py",
       "tritrack_editing_assistant/profiles/basic-title-v1.json",
       "tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
       "tritrack_editing_assistant/run_workflow.py",
       "tritrack_editing_assistant/schemas/__init__.py",
       "tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
       "tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
       "tritrack_editing_assistant/schemas/grouping-v1.schema.json",
       "tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
       "tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
       "tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
       "tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
       "tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
       "tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
       "tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
       "tritrack_editing_assistant/story_fcpxml.py",
       "tritrack_editing_assistant/string_out.py",
       "tritrack_editing_assistant/sync_scan.py",
       "tritrack_editing_assistant/transcribe_takes.py",
       "tritrack_editing_assistant/validate_artifacts.py"
diff --git a/scripts/capture_basic_title_binding.py b/scripts/capture_basic_title_binding.py
index 69e2824..f681b0c 100755
--- a/scripts/capture_basic_title_binding.py
+++ b/scripts/capture_basic_title_binding.py
@@ -1,112 +1,168 @@
 #!/usr/bin/env python3
 """Capture a public-safe Basic Title binding from invented FCPXML."""

 from __future__ import annotations

 import argparse
 import json
 import os
+import stat
 import xml.etree.ElementTree as ET
 from collections.abc import Mapping
 from pathlib import Path

 from tritrack_editing_assistant.contracts import validate_contract
 from tritrack_editing_assistant.doctor import load_profile
 from tritrack_editing_assistant.process import require_absent_output

 FORBIDDEN_TEXT = (
     "Artlist LT",
     "江城知音体",
     "Transcription Template",
     "/" + "Users" + "/",
     "/" + "Volumes" + "/HoneyPot/",
 )
 STYLE_ATTRIBUTES = ("alignment", "font", "fontColor", "fontFace", "fontSize")
 ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
+MAX_CAPTURE_XML_BYTES = 16 * 1024 * 1024
+MAX_BINDING_BYTES = 1024 * 1024
+
+
+def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError(code) from error
+    try:
+        before = os.fstat(descriptor)
+        if not stat.S_ISREG(before.st_mode) or not (0 < before.st_size <= limit):
+            raise ValueError(code)
+        chunks: list[bytes] = []
+        remaining = limit + 1
+        while remaining:
+            chunk = os.read(descriptor, min(1024 * 1024, remaining))
+            if not chunk:
+                break
+            chunks.append(chunk)
+            remaining -= len(chunk)
+        encoded = b"".join(chunks)
+        after = os.fstat(descriptor)
+        if (
+            len(encoded) != before.st_size
+            or len(encoded) > limit
+            or (
+                before.st_dev,
+                before.st_ino,
+                before.st_size,
+                before.st_mtime_ns,
+            )
+            != (
+                after.st_dev,
+                after.st_ino,
+                after.st_size,
+                after.st_mtime_ns,
+            )
+        ):
+            raise ValueError(code)
+        return encoded
+    except OSError as error:
+        raise ValueError(code) from error
+    finally:
+        os.close(descriptor)


 def _read_public_xml(path: Path) -> str:
-    data = path.read_bytes()
+    data = _read_regular_bytes(
+        path,
+        limit=MAX_CAPTURE_XML_BYTES,
+        code="TRITRACK_TITLE_BINDING_INVALID_XML",
+    )
     if b"\x00" in data:
         raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
-    text = data.decode("utf-8")
+    try:
+        text = data.decode("utf-8")
+    except UnicodeDecodeError as error:
+        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML") from error
     without_allowed_doctype = text.replace(ALLOWED_DOCTYPE, "", 1)
     if (
         "<!DOCTYPE" in without_allowed_doctype
         or "<!ENTITY" in text
         or text.count(ALLOWED_DOCTYPE) > 1
     ):
         raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
     if any(value in text for value in FORBIDDEN_TEXT):
         raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")
     return text


 def _parameter_value(value: str) -> str | int | float | bool:
     try:
         number = float(value)
     except ValueError:
         return value
     return int(number) if number.is_integer() else number


 def capture_binding(source: Path) -> dict[str, object]:
     """Extract only the referenced Basic Title effect and style attributes."""

     text = _read_public_xml(source)
     try:
         root = ET.fromstring(text)
     except ET.ParseError as error:
         raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML") from error

     for element in root.iter():
         source_value = element.attrib.get("src")
         if source_value:
             raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

     effects = {
         effect.attrib.get("id"): effect
         for effect in root.findall("./resources/effect")
         if effect.attrib.get("name") == "Basic Title"
     }
     titles = [
         title for title in root.iter("title") if title.attrib.get("ref") in effects
     ]
     if len(titles) != 1:
         raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")
     effect = effects[titles[0].attrib["ref"]]
     uid = effect.attrib.get("uid")
     if not uid or not uid.endswith("Basic Title.moti"):
         raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")

     style_elements = titles[0].findall("./text-style-def/text-style")
     if len(style_elements) != 1:
         raise ValueError("TRITRACK_TITLE_BINDING_STYLE_REQUIRED")
     style = style_elements[0]
     parameters = [
         {"name": name, "value": _parameter_value(style.attrib[name])}
         for name in STYLE_ATTRIBUTES
         if name in style.attrib
     ]
     binding: dict[str, object] = {
         "schemaVersion": "tritrack.title-binding/v1",
         "bindingId": "basic-title-v1",
         "effectName": "Basic Title",
         "effectUid": uid,
         "parameters": parameters,
     }
     validate_contract("title-binding-v1", binding)
     return binding


 def render_basic_title_fcpxml(binding: Mapping[str, object], *, text: str) -> str:
     """Render a minimal, public-safe NDF project from a reviewed binding."""

     validate_contract("title-binding-v1", dict(binding))
     if not text.strip() or "\n" in text or "\r" in text:
         raise ValueError("TRITRACK_TITLE_BINDING_TEXT_REQUIRED")
     if any(value in text for value in FORBIDDEN_TEXT):
         raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

     profile = load_profile("uhd-2997-ndf-fcpxml-1.14")
     style_values = {
@@ -134,106 +190,115 @@ def render_basic_title_fcpxml(binding: Mapping[str, object], *, text: str) -> st
     ET.SubElement(
         resources_element,
         "effect",
         {
             "id": "r2",
             "name": str(binding["effectName"]),
             "uid": str(binding["effectUid"]),
         },
     )

     event = ET.SubElement(root, "event", {"name": "TriTrack Public Evidence"})
     project = ET.SubElement(
         event, "project", {"name": "TriTrack Basic Title Roundtrip"}
     )
     sequence = ET.SubElement(
         project,
         "sequence",
         {
             "format": "r1",
             "duration": "180180/30000s",
             "tcStart": "0s",
             "tcFormat": str(profile["timecodeFormat"]),
             "audioLayout": "stereo",
             "audioRate": f"{int(profile['audioRate']) // 1000}k",
         },
     )
     spine = ET.SubElement(sequence, "spine")
     ET.SubElement(
         spine,
         "gap",
         {
             "name": "Gap",
             "offset": "0s",
             "start": "0s",
             "duration": "90090/30000s",
         },
     )
     title = ET.SubElement(
         spine,
         "title",
         {
             "ref": "r2",
             "offset": "90090/30000s",
             "name": f"{text} - Basic Title",
             "start": "0s",
             "duration": "90090/30000s",
         },
     )
     text_element = ET.SubElement(title, "text")
     text_style = ET.SubElement(text_element, "text-style", {"ref": "ts1"})
     text_style.text = text
     text_style_definition = ET.SubElement(title, "text-style-def", {"id": "ts1"})
     ET.SubElement(
         text_style_definition,
         "text-style",
         {attribute: style_values[attribute] for attribute in STYLE_ATTRIBUTES},
     )

     ET.indent(root, space="    ")
     body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
     return f'<?xml version="1.0" encoding="UTF-8"?>\n{ALLOWED_DOCTYPE}\n{body}\n'


 def _write_exclusive(output: Path, encoded: bytes) -> None:
     destination = require_absent_output(output)
     descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
     with os.fdopen(descriptor, "wb") as handle:
         handle.write(encoded)
         handle.flush()
         os.fsync(handle.fileno())


 def write_binding(source: Path, output: Path) -> dict[str, object]:
     binding = capture_binding(source)
     encoded = (json.dumps(binding, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
     _write_exclusive(output, encoded)
     return binding


 def write_rendered_fcpxml(binding_path: Path, output: Path, text: str) -> None:
-    binding = json.loads(binding_path.read_text(encoding="utf-8"))
+    try:
+        binding = json.loads(
+            _read_regular_bytes(
+                binding_path,
+                limit=MAX_BINDING_BYTES,
+                code="TRITRACK_TITLE_BINDING_INVALID",
+            ).decode("utf-8")
+        )
+    except (UnicodeDecodeError, json.JSONDecodeError) as error:
+        raise ValueError("TRITRACK_TITLE_BINDING_INVALID") from error
     rendered = render_basic_title_fcpxml(binding, text=text)
     _write_exclusive(output, rendered.encode("utf-8"))


 def main() -> int:
     parser = argparse.ArgumentParser()
     source = parser.add_mutually_exclusive_group(required=True)
     source.add_argument("--input", type=Path)
     source.add_argument("--binding", type=Path)
     parser.add_argument("--output", type=Path, required=True)
     parser.add_argument("--text")
     arguments = parser.parse_args()
     if arguments.input is not None:
         if arguments.text is not None:
             parser.error("--text is only valid with --binding")
         write_binding(arguments.input, arguments.output)
     else:
         if arguments.text is None:
             parser.error("--text is required with --binding")
         write_rendered_fcpxml(arguments.binding, arguments.output, arguments.text)
     return 0


 if __name__ == "__main__":
     raise SystemExit(main())
diff --git a/scripts/release_gate_core.py b/scripts/release_gate_core.py
index 1f2ac02..6236c42 100644
--- a/scripts/release_gate_core.py
+++ b/scripts/release_gate_core.py
@@ -1,257 +1,412 @@
 """Bounded, fail-closed primitives for the maintainer release gate."""

 from __future__ import annotations

 import hashlib
 import importlib.metadata
 import io
 import json
 import os
 import platform
 import re
+import selectors
+import signal
 import stat
 import subprocess
 import sys
 import tarfile
 import tempfile
+import time
 import tomllib
 import unicodedata
 import zipfile
 from collections.abc import Mapping
 from dataclasses import dataclass
 from email.parser import BytesParser
 from pathlib import Path, PurePosixPath

 import jsonschema

 _COMMAND_TIMEOUT_SECONDS = 30
 _COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
 _POLICY_LIMIT = 1024 * 1024
 _ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
 _ALLOWED_FAKE_SECRETS = frozenset(
     {b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
 )
+_READ_CHUNK_BYTES = 64 * 1024
+_TERMINATION_GRACE_SECONDS = 0.2


 class ReleaseGateError(Exception):
     """One stable public-safe release-gate failure code."""

     def __init__(self, code: str):
         self.code = code
         super().__init__(code)

     def __str__(self) -> str:
         return self.code


 @dataclass(frozen=True)
 class SourceInventory:
     count: int
     total_bytes: int
     sha256: str
     commit: str


 @dataclass(frozen=True)
 class DistributionInspection:
     sha256: str
     size_bytes: int
     member_count: int
     member_inventory_sha256: str


 @dataclass(frozen=True)
 class ReleaseContext:
     project_name: str
     version: str
     commit: str
     source_inventory: SourceInventory
     toolchain: Mapping[str, str]
     python_version: str
     implementation: str
     system: str
     machine: str
     wheel: DistributionInspection
     sdist: DistributionInspection


+@dataclass(frozen=True)
+class _BoundedCommandResult:
+    status: str
+    returncode: int | None
+    stdout: bytes
+    stderr: bytes
+
+
 def _fail(code: str) -> None:
     raise ReleaseGateError(code)


 def _safe_environment() -> dict[str, str]:
     return {
         "GIT_CONFIG_NOSYSTEM": "1",
         "GIT_OPTIONAL_LOCKS": "0",
         "LANG": "C",
         "LC_ALL": "C",
         "PATH": os.defpath,
     }


-def _run_git(source: Path, *arguments: str) -> bytes:
+def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
+    if os.name == "posix":
+        try:
+            os.killpg(process.pid, signal.SIGTERM)
+        except ProcessLookupError:
+            pass
+        except OSError:
+            if process.poll() is None:
+                process.terminate()
+    elif process.poll() is None:
+        process.terminate()
+
     try:
-        result = subprocess.run(
-            ["git", *arguments],
-            cwd=source,
-            env=_safe_environment(),
+        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
+    except subprocess.TimeoutExpired:
+        pass
+
+    if os.name == "posix":
+        try:
+            os.killpg(process.pid, signal.SIGKILL)
+        except ProcessLookupError:
+            pass
+        except OSError:
+            if process.poll() is None:
+                process.kill()
+    elif process.poll() is None:
+        process.kill()
+
+    if process.poll() is None:
+        process.wait()
+
+
+def _close_process_pipes(process: subprocess.Popen[bytes]) -> None:
+    if process.stdout is not None:
+        process.stdout.close()
+    if process.stderr is not None:
+        process.stderr.close()
+
+
+def _run_bounded_subprocess(
+    argv: list[str],
+    *,
+    cwd: Path,
+    env: Mapping[str, str],
+    timeout: int,
+    output_limit: int,
+) -> _BoundedCommandResult:
+    """Run one argv-only child while bounding combined retained output."""
+
+    if timeout < 1 or output_limit < 1:
+        return _BoundedCommandResult("invalid", None, b"", b"")
+    try:
+        process = subprocess.Popen(
+            argv,
+            cwd=cwd,
+            env=dict(env),
             shell=False,
             stdin=subprocess.DEVNULL,
-            capture_output=True,
-            timeout=_COMMAND_TIMEOUT_SECONDS,
-            check=False,
+            stdout=subprocess.PIPE,
+            stderr=subprocess.PIPE,
+            start_new_session=True,
         )
-    except (OSError, subprocess.TimeoutExpired):
-        _fail("TRITRACK_RELEASE_GIT_FAILED")
-    if result.returncode != 0:
-        _fail("TRITRACK_RELEASE_GIT_FAILED")
-    if len(result.stdout) > _COMMAND_OUTPUT_LIMIT:
+    except OSError:
+        return _BoundedCommandResult("spawn_error", None, b"", b"")
+
+    deadline = time.monotonic() + timeout
+    stdout_chunks: list[bytes] = []
+    stderr_chunks: list[bytes] = []
+    captured = 0
+    status = "ok"
+    try:
+        with selectors.DefaultSelector() as selector:
+            assert process.stdout is not None
+            assert process.stderr is not None
+            selector.register(process.stdout, selectors.EVENT_READ, stdout_chunks)
+            selector.register(process.stderr, selectors.EVENT_READ, stderr_chunks)
+            while selector.get_map():
+                remaining = deadline - time.monotonic()
+                if remaining <= 0:
+                    status = "timeout"
+                    break
+                for key, _mask in selector.select(timeout=min(remaining, 0.05)):
+                    allowed_read = output_limit - captured + 1
+                    chunk = os.read(
+                        key.fd,
+                        min(_READ_CHUNK_BYTES, max(1, allowed_read)),
+                    )
+                    if not chunk:
+                        selector.unregister(key.fileobj)
+                        continue
+                    captured += len(chunk)
+                    if captured > output_limit:
+                        status = "output_limit_exceeded"
+                        break
+                    key.data.append(chunk)
+                if status != "ok":
+                    break
+
+        if status == "ok":
+            remaining = deadline - time.monotonic()
+            if remaining <= 0 and process.poll() is None:
+                status = "timeout"
+            else:
+                try:
+                    process.wait(timeout=max(0.0, remaining))
+                except subprocess.TimeoutExpired:
+                    status = "timeout"
+        if status != "ok":
+            _terminate_process_group(process)
+            return _BoundedCommandResult(status, process.returncode, b"", b"")
+        return _BoundedCommandResult(
+            "ok" if process.returncode == 0 else "failed",
+            process.returncode,
+            b"".join(stdout_chunks),
+            b"".join(stderr_chunks),
+        )
+    except OSError:
+        _terminate_process_group(process)
+        return _BoundedCommandResult("capture_error", process.returncode, b"", b"")
+    except BaseException:
+        _terminate_process_group(process)
+        raise
+    finally:
+        _close_process_pipes(process)
+
+
+def _run_git(source: Path, *arguments: str) -> bytes:
+    result = _run_bounded_subprocess(
+        ["git", *arguments],
+        cwd=source,
+        env=_safe_environment(),
+        timeout=_COMMAND_TIMEOUT_SECONDS,
+        output_limit=_COMMAND_OUTPUT_LIMIT,
+    )
+    if result.status == "output_limit_exceeded":
         _fail("TRITRACK_RELEASE_GIT_LIMIT")
+    if result.status != "ok":
+        _fail("TRITRACK_RELEASE_GIT_FAILED")
     return result.stdout


 def _read_regular(path: Path, limit: int) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     flags |= getattr(os, "O_CLOEXEC", 0)
     flags |= getattr(os, "O_NOFOLLOW", 0)
     try:
         descriptor = os.open(path, flags)
     except OSError:
         _fail("TRITRACK_RELEASE_SOURCE_READ")
     try:
         details = os.fstat(descriptor)
         if not stat.S_ISREG(details.st_mode):
             _fail("TRITRACK_RELEASE_SOURCE_MODE")
         if details.st_size > limit:
             _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
         chunks: list[bytes] = []
         remaining = limit + 1
         while remaining:
             chunk = os.read(descriptor, min(remaining, 1024 * 1024))
             if not chunk:
                 break
             chunks.append(chunk)
             remaining -= len(chunk)
         encoded = b"".join(chunks)
         if len(encoded) > limit or len(encoded) != details.st_size:
             _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
         return encoded
     except OSError:
         _fail("TRITRACK_RELEASE_SOURCE_READ")
     finally:
         os.close(descriptor)


 def _mapping(value: object, code: str) -> Mapping[str, object]:
     if not isinstance(value, Mapping):
         _fail(code)
     return value


 def _positive_limit(policy: Mapping[str, object], name: str) -> int:
     limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
     value = limits.get(name)
     if not isinstance(value, int) or isinstance(value, bool) or value < 1:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     return value


+def _build_epoch(policy: Mapping[str, object]) -> int:
+    build = _mapping(policy.get("build"), "TRITRACK_RELEASE_POLICY_INVALID")
+    if set(build) != {"sourceDateEpoch"}:
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    value = build.get("sourceDateEpoch")
+    if (
+        not isinstance(value, int)
+        or isinstance(value, bool)
+        or value < 315532800
+    ):
+        _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    return value
+
+
 def _string_list(value: object) -> tuple[str, ...]:
     if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     if len(value) != len(set(value)):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     return tuple(value)


 def _load_policy(source: Path) -> Mapping[str, object]:
     encoded = _read_regular(source / "release" / "package-policy-v1.json", _POLICY_LIMIT)
     try:
         policy = json.loads(encoded.decode("utf-8"))
     except (UnicodeDecodeError, json.JSONDecodeError):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     policy = _mapping(policy, "TRITRACK_RELEASE_POLICY_INVALID")
     if policy.get("schemaVersion") != "tritrack.package-policy/v1":
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
-    if set(policy) != {"schemaVersion", "limits", "source", "wheel", "sdist"}:
+    if set(policy) != {
+        "schemaVersion",
+        "build",
+        "limits",
+        "source",
+        "wheel",
+        "sdist",
+    }:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
+    _build_epoch(policy)
     limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
     expected_limits = {
         "sourceMaxFiles",
         "sourceMaxFileBytes",
         "sourceMaxTotalBytes",
         "archiveMaxBytes",
         "archiveMaxMembers",
         "memberMaxBytes",
         "expandedMaxBytes",
     }
     if set(limits) != expected_limits:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     for name in expected_limits:
         _positive_limit(policy, name)

     source_policy = _mapping(
         policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID"
     )
     if set(source_policy) != {
         "allowedFakeHomeUsers",
         "allowedFakeSecretValues",
         "forbiddenSuffixes",
     }:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     allowed_users = frozenset(
         value.encode("utf-8")
         for value in _string_list(source_policy.get("allowedFakeHomeUsers"))
     )
     allowed_secrets = frozenset(
         value.encode("utf-8")
         for value in _string_list(source_policy.get("allowedFakeSecretValues"))
     )
     if (
         allowed_users != _ALLOWED_FAKE_USERS
         or allowed_secrets != _ALLOWED_FAKE_SECRETS
     ):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     _string_list(source_policy.get("forbiddenSuffixes"))

     wheel_policy = _mapping(
         policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID"
     )
     if set(wheel_policy) != {"expectedMembers"}:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     _string_list(wheel_policy.get("expectedMembers"))

     sdist_policy = _mapping(
         policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID"
     )
     if set(sdist_policy) != {"root", "expectedMembers"}:
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     root = sdist_policy.get("root")
     if not isinstance(root, str) or not root.endswith("/"):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     _string_list(sdist_policy.get("expectedMembers"))
     return policy


 def _status(source: Path) -> bytes:
     return _run_git(
         source,
         "status",
         "--porcelain=v1",
         "-z",
         "--untracked-files=all",
     )


 def _safe_source_path(encoded: bytes) -> str:
     try:
         name = encoded.decode("utf-8", "strict")
     except UnicodeDecodeError:
         _fail("TRITRACK_RELEASE_SOURCE_PATH")
     candidate = PurePosixPath(name)
     if (
         not name
         or "\\" in name
         or candidate.is_absolute()
         or any(part in {"", ".", ".."} for part in candidate.parts)
     ):
@@ -368,161 +523,161 @@ def scan_public_bytes(encoded: bytes) -> None:
         value = match.group(1).rstrip(b"'\"").lower()
         if value not in _ALLOWED_FAKE_SECRETS:
             _fail("TRITRACK_RELEASE_CREDENTIAL")

     credential_shapes = (
         rb"\bgh" + rb"[pousr]_[A-Za-z0-9]{36,255}\b",
         rb"\bAK" + rb"IA[0-9A-Z]{16}\b",
         rb"\bAI" + rb"za[0-9A-Za-z_-]{35}\b",
         rb"\bxox" + rb"[baprs]-[0-9A-Za-z-]{20,255}\b",
     )
     if any(re.search(pattern, encoded) for pattern in credential_shapes):
         _fail("TRITRACK_RELEASE_CREDENTIAL")


 def inventory_tracked_source(source: Path) -> SourceInventory:
     """Bind one clean Git index to the exact regular working-tree bytes."""

     source = source.resolve()
     policy = _load_policy(source)
     index_bytes = _run_git(source, "ls-files", "-s", "-z")
     entries = _parse_index(index_bytes)
     if _status(source):
         _fail("TRITRACK_RELEASE_SOURCE_DIRTY")
     max_files = _positive_limit(policy, "sourceMaxFiles")
     max_file_bytes = _positive_limit(policy, "sourceMaxFileBytes")
     max_total_bytes = _positive_limit(policy, "sourceMaxTotalBytes")
     if len(entries) > max_files:
         _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
     source_policy = _mapping(policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID")
     suffixes = tuple(item.casefold() for item in _string_list(source_policy.get("forbiddenSuffixes")))
     object_format = _run_git(source, "rev-parse", "--show-object-format").strip()
     try:
         algorithm = object_format.decode("ascii", "strict")
     except UnicodeDecodeError:
         _fail("TRITRACK_RELEASE_GIT_FORMAT")
     commit_bytes = _run_git(source, "rev-parse", "HEAD").strip()
     try:
         commit = commit_bytes.decode("ascii", "strict")
     except UnicodeDecodeError:
         _fail("TRITRACK_RELEASE_GIT_FAILED")
     if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
         _fail("TRITRACK_RELEASE_GIT_FAILED")

     total = 0
     inventory = hashlib.sha256()
     for name, mode, object_id in sorted(entries):
         if suffixes and name.casefold().endswith(suffixes):
             _fail("TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE")
         path = source / name
         before = _path_signature(path)
         if before[2] > max_file_bytes:
             _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
         total += before[2]
         if total > max_total_bytes:
             _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
         encoded = _read_regular(path, max_file_bytes)
         after = _path_signature(path)
         if before != after:
             _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
         if _git_blob_hash(encoded, algorithm) != object_id:
             _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
         scan_public_bytes(encoded)
         content_sha = hashlib.sha256(encoded).hexdigest()
         for value in (name, mode, str(len(encoded)), content_sha):
             inventory.update(value.encode("utf-8"))
             inventory.update(b"\0")
         inventory.update(b"\n")

     if _run_git(source, "ls-files", "-s", "-z") != index_bytes or _status(source):
         _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
     return SourceInventory(
         count=len(entries),
         total_bytes=total,
         sha256=inventory.hexdigest(),
         commit=commit,
     )


 def _read_archive_bytes(path: Path, policy: Mapping[str, object]) -> bytes:
     limit = _positive_limit(policy, "archiveMaxBytes")
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     flags |= getattr(os, "O_CLOEXEC", 0)
     flags |= getattr(os, "O_NOFOLLOW", 0)
     try:
         descriptor = os.open(path, flags)
     except OSError:
         _fail("TRITRACK_RELEASE_ARCHIVE_READ")
     try:
         before = os.fstat(descriptor)
         if not stat.S_ISREG(before.st_mode):
             _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
         if not 0 < before.st_size <= limit:
             _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
         chunks: list[bytes] = []
         remaining = limit + 1
         while remaining:
             chunk = os.read(descriptor, min(remaining, 1024 * 1024))
             if not chunk:
                 break
             chunks.append(chunk)
             remaining -= len(chunk)
         encoded = b"".join(chunks)
         after = os.fstat(descriptor)
         if (
             len(encoded) > limit
             or len(encoded) != before.st_size
             or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
             != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
         ):
             _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
         return encoded
     except OSError:
         _fail("TRITRACK_RELEASE_ARCHIVE_READ")
     finally:
         os.close(descriptor)


 def _safe_member_name(name: str) -> str:
     if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
         _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
     normalized = unicodedata.normalize("NFC", name)
     path = PurePosixPath(normalized)
     if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
         _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
     return normalized.rstrip("/")


 def _bounded_archive_read(stream, expected: int, limit: int) -> bytes:
     if expected > limit:
         _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
     encoded = stream.read(limit + 1)
     if len(encoded) != expected or len(encoded) > limit:
         _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
     return encoded


 def _member_digest(
     inventory: hashlib._Hash,
     name: str,
     member_type: str,
     mode: int,
     encoded: bytes,
 ) -> None:
     values = (
         name,
         member_type,
         f"{mode & 0o7777:o}",
         str(len(encoded)),
         hashlib.sha256(encoded).hexdigest(),
     )
     for value in values:
         inventory.update(value.encode("utf-8"))
         inventory.update(b"\0")
     inventory.update(b"\n")


 def _check_collision(name: str, exact: set[str], folded: set[str]) -> None:
     if name in exact:
         _fail("TRITRACK_RELEASE_ARCHIVE_DUPLICATE")
     collision = unicodedata.normalize("NFC", name).casefold()
     if collision in folded:
@@ -591,177 +746,171 @@ def inspect_sdist(
     path: Path, policy: Mapping[str, object]
 ) -> DistributionInspection:
     """Inspect a gzipped source distribution without extracting it."""

     archive_bytes = _read_archive_bytes(path, policy)
     size_bytes = len(archive_bytes)
     max_members = _positive_limit(policy, "archiveMaxMembers")
     max_member = _positive_limit(policy, "memberMaxBytes")
     max_expanded = _positive_limit(policy, "expandedMaxBytes")
     sdist_policy = _mapping(policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID")
     root = sdist_policy.get("root")
     if not isinstance(root, str) or not root.endswith("/"):
         _fail("TRITRACK_RELEASE_POLICY_INVALID")
     expected = set(_string_list(sdist_policy.get("expectedMembers")))
     exact: set[str] = set()
     folded: set[str] = set()
     files: list[tuple[tarfile.TarInfo, str]] = []
     all_members: list[tuple[tarfile.TarInfo, str, str]] = []
     expanded = 0
     try:
         with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
             members = archive.getmembers()
             if len(members) > max_members:
                 _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
             for member in members:
                 full_name = _safe_member_name(member.name)
                 if full_name == root.rstrip("/"):
                     relative = ""
                 elif full_name.startswith(root):
                     relative = full_name[len(root) :]
                 else:
                     _fail("TRITRACK_RELEASE_ARCHIVE_ROOT")
                 collision_name = relative or "."
                 _check_collision(collision_name, exact, folded)
                 if member.isdir():
                     all_members.append((member, relative, "directory"))
                     continue
                 if not member.isreg():
                     _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                 if not relative:
                     _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
                 expanded += member.size
                 if member.size > max_member or expanded > max_expanded:
                     _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                 files.append((member, relative))
                 all_members.append((member, relative, "file"))
             if {name for _, name in files} != expected:
                 _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
             inventory = hashlib.sha256()
             for member, name, member_type in sorted(all_members, key=lambda item: item[1]):
                 if member_type == "directory":
                     encoded = b""
                 else:
                     stream = archive.extractfile(member)
                     if stream is None:
                         _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
                     with stream:
                         encoded = _bounded_archive_read(stream, member.size, max_member)
                     scan_public_bytes(encoded)
                 _member_digest(inventory, name or ".", member_type, member.mode, encoded)
     except ReleaseGateError:
         raise
     except (OSError, ValueError, tarfile.TarError):
         _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
     return DistributionInspection(
         sha256=hashlib.sha256(archive_bytes).hexdigest(),
         size_bytes=size_bytes,
         member_count=len(all_members),
         member_inventory_sha256=inventory.hexdigest(),
     )


 def _run_command(
     argv: list[str],
     *,
     cwd: Path,
     env: Mapping[str, str],
     timeout: int = 300,
     output_limit: int = _COMMAND_OUTPUT_LIMIT,
 ) -> bytes:
-    try:
-        result = subprocess.run(
-            argv,
-            cwd=cwd,
-            env=dict(env),
-            shell=False,
-            stdin=subprocess.DEVNULL,
-            capture_output=True,
-            timeout=timeout,
-            check=False,
-        )
-    except (OSError, subprocess.TimeoutExpired):
-        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
-    if result.returncode != 0:
-        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
-    if len(result.stdout) > output_limit or len(result.stderr) > output_limit:
+    result = _run_bounded_subprocess(
+        argv,
+        cwd=cwd,
+        env=env,
+        timeout=timeout,
+        output_limit=output_limit,
+    )
+    if result.status == "output_limit_exceeded":
         _fail("TRITRACK_RELEASE_COMMAND_LIMIT")
+    if result.status != "ok":
+        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
     return result.stdout


 def _installed_tool_versions() -> dict[str, str]:
     versions: dict[str, str] = {}
     for distribution in ("pip", "build", "setuptools", "wheel"):
         try:
             versions[distribution] = importlib.metadata.version(distribution)
         except importlib.metadata.PackageNotFoundError:
             _fail("TRITRACK_RELEASE_TOOLCHAIN")
     return versions


 def _build_environment(epoch: int, temporary: Path) -> dict[str, str]:
     if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
         _fail("TRITRACK_RELEASE_EPOCH")
     environment = {
         "HOME": os.fspath(temporary),
         "LANG": "C.UTF-8",
         "LC_ALL": "C.UTF-8",
         "PATH": os.defpath,
         "PYTHONHASHSEED": "0",
         "SOURCE_DATE_EPOCH": str(epoch),
         "TMPDIR": os.fspath(temporary),
     }
     return environment


 def build_distributions(
     snapshot: Path, output: Path, *, epoch: int
 ) -> tuple[Path, Path]:
     """Build exactly one wheel and one sdist with the pinned local toolchain."""

     expected_tools = {
         "pip": "26.2",
         "build": "1.5.0",
         "setuptools": "84.0.0",
         "wheel": "0.48.0",
     }
     if _installed_tool_versions() != expected_tools:
         _fail("TRITRACK_RELEASE_TOOLCHAIN")
     if not snapshot.is_dir():
         _fail("TRITRACK_RELEASE_SNAPSHOT")
     try:
         os.mkdir(output)
     except FileExistsError:
         _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
     except OSError:
         _fail("TRITRACK_RELEASE_OUTPUT")
     _run_command(
         [
             os.fspath(Path(sys.executable)),
             "-m",
             "build",
             "--no-isolation",
             "--outdir",
             os.fspath(output),
         ],
         cwd=snapshot,
         env=_build_environment(epoch, output),
         timeout=300,
     )
     try:
         members = [
             child
             for child in output.iterdir()
             if child.is_file() and not child.is_symlink()
         ]
     except OSError:
         _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
     wheels = [child for child in members if child.suffix == ".whl"]
     sdists = [child for child in members if child.name.endswith(".tar.gz")]
     if len(members) != 2 or len(wheels) != 1 or len(sdists) != 1:
         _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
     return wheels[0], sdists[0]


 def _wheel_project_identity(wheel: Path) -> tuple[str, str]:
     try:
         with zipfile.ZipFile(wheel) as archive:
@@ -963,161 +1112,161 @@ def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
             "no-pull-request",
             "no-tester-contact",
             "no-signing",
             "no-attestation",
             "no-sbom",
             "no-final-cut-gui",
             "no-dtd",
             "no-provider",
             "no-application-submission",
         ],
     }
     schema_path = Path(__file__).resolve().parents[1] / "release" / "release-manifest-v1.schema.json"
     try:
         schema = json.loads(_read_regular(schema_path, _POLICY_LIMIT).decode("utf-8"))
         jsonschema.Draft202012Validator.check_schema(schema)
         jsonschema.validate(manifest, schema)
     except ReleaseGateError:
         raise
     except (UnicodeDecodeError, json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError):
         _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
     return manifest


 def _link_file(source: Path, destination: Path) -> None:
     try:
         os.link(source, destination, follow_symlinks=False)
     except FileExistsError:
         _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
     except OSError:
         _fail("TRITRACK_RELEASE_PUBLISH")


 def _fsync_directory(path: Path) -> None:
     flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
     try:
         descriptor = os.open(path, flags)
         try:
             os.fsync(descriptor)
         finally:
             os.close(descriptor)
     except OSError:
         _fail("TRITRACK_RELEASE_PUBLISH")


 def _publication_artifacts(manifest: bytes) -> dict[str, tuple[int, str]]:
     if not 0 < len(manifest) <= _POLICY_LIMIT:
         _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
     try:
         payload = _mapping(
             json.loads(manifest.decode("utf-8", errors="strict")),
             "TRITRACK_RELEASE_MANIFEST_INVALID",
         )
         artifacts = _mapping(
             payload.get("artifacts"), "TRITRACK_RELEASE_MANIFEST_INVALID"
         )
         result: dict[str, tuple[int, str]] = {}
         for kind in ("wheel", "sdist"):
             artifact = _mapping(
                 artifacts.get(kind), "TRITRACK_RELEASE_MANIFEST_INVALID"
             )
             size = artifact.get("sizeBytes")
             digest = artifact.get("sha256")
             if (
                 not isinstance(size, int)
                 or isinstance(size, bool)
                 or size < 1
                 or not isinstance(digest, str)
                 or re.fullmatch(r"[0-9a-f]{64}", digest) is None
             ):
                 _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
             result[kind] = (size, digest)
         return result
     except ReleaseGateError:
         raise
     except (UnicodeDecodeError, json.JSONDecodeError):
         _fail("TRITRACK_RELEASE_MANIFEST_INVALID")


 def _verify_published_archive(path: Path, expected: tuple[int, str]) -> None:
     expected_size, expected_sha256 = expected
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     flags |= getattr(os, "O_CLOEXEC", 0)
     flags |= getattr(os, "O_NOFOLLOW", 0)
     try:
         descriptor = os.open(path, flags)
         try:
             details = os.fstat(descriptor)
             if not stat.S_ISREG(details.st_mode) or details.st_size != expected_size:
                 _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
             digest = hashlib.sha256()
             observed_size = 0
             while observed_size <= expected_size:
                 chunk = os.read(
                     descriptor,
                     min(1024 * 1024, expected_size + 1 - observed_size),
                 )
                 if not chunk:
                     break
                 observed_size += len(chunk)
                 digest.update(chunk)
             after = os.fstat(descriptor)
         finally:
             os.close(descriptor)
     except ReleaseGateError:
         raise
     except OSError:
         _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
     if (
         observed_size != expected_size
         or digest.hexdigest() != expected_sha256
         or (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)
         != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
     ):
         _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")


 def publish_release(
     output: Path, wheel: Path, sdist: Path, manifest: bytes
 ) -> None:
     """Publish two archives first and the canonical success manifest last."""

     if (
         wheel.name in {"", ".", "..", "release-manifest.json"}
         or sdist.name in {"", ".", "..", "release-manifest.json"}
         or wheel.name != os.path.basename(wheel.name)
         or sdist.name != os.path.basename(sdist.name)
         or wheel.name == sdist.name
     ):
         _fail("TRITRACK_RELEASE_PUBLISH")
     expected_artifacts = _publication_artifacts(manifest)
     try:
         parent_details = output.parent.stat(follow_symlinks=False)
     except OSError:
         _fail("TRITRACK_RELEASE_OUTPUT")
     if not stat.S_ISDIR(parent_details.st_mode):
         _fail("TRITRACK_RELEASE_OUTPUT")

     temporary_manifest: Path | None = None
     try:
         with tempfile.NamedTemporaryFile(
             mode="wb",
             dir=wheel.parent,
             prefix=".release-manifest-",
             delete=False,
         ) as stream:
             temporary_manifest = Path(stream.name)
             stream.write(manifest)
             stream.flush()
             os.fsync(stream.fileno())
         try:
             os.mkdir(output)
         except FileExistsError:
             _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
         except OSError:
             _fail("TRITRACK_RELEASE_OUTPUT")
         _link_file(wheel, output / wheel.name)
         _link_file(sdist, output / sdist.name)
         _fsync_directory(output)
         _verify_published_archive(output / wheel.name, expected_artifacts["wheel"])
         _verify_published_archive(output / sdist.name, expected_artifacts["sdist"])
         _link_file(temporary_manifest, output / "release-manifest.json")
@@ -1247,143 +1396,139 @@ def _write_snapshot_file(root: Path, name: str, mode: int, encoded: bytes) -> No


 def _materialize_snapshot(
     source: Path,
     destination: Path,
     inventory: SourceInventory,
     policy: Mapping[str, object],
 ) -> None:
     try:
         os.mkdir(destination)
     except OSError:
         _fail("TRITRACK_RELEASE_SNAPSHOT")
     archive_path = destination.parent / f".{destination.name}.tar"
     _run_command(
         [
             "git",
             "archive",
             "--format=tar",
             "--output",
             os.fspath(archive_path),
             inventory.commit,
         ],
         cwd=source,
         env=_safe_environment(),
         timeout=120,
     )
     try:
         with tarfile.open(archive_path, mode="r:") as archive:
             files, digest = _snapshot_inventory(
                 archive,
                 _positive_limit(policy, "sourceMaxFileBytes"),
                 _positive_limit(policy, "sourceMaxTotalBytes"),
             )
         if len(files) != inventory.count or digest != inventory.sha256:
             _fail("TRITRACK_RELEASE_SNAPSHOT_MISMATCH")
         for name, mode, encoded in files:
             _write_snapshot_file(destination, name, mode, encoded)
     except ReleaseGateError:
         raise
     except (OSError, tarfile.TarError):
         _fail("TRITRACK_RELEASE_SNAPSHOT")
     finally:
         try:
             archive_path.unlink(missing_ok=True)
         except OSError:
             pass


 def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
     return (
         json.dumps(
             manifest,
             ensure_ascii=False,
             sort_keys=True,
             separators=(",", ":"),
         ).encode("utf-8")
         + b"\n"
     )


 def run_release_gate(source: Path, output: Path) -> dict[str, object]:
     """Run the complete local release-readiness gate and publish manifest last."""

     try:
         source = source.resolve(strict=True)
     except OSError:
         _fail("TRITRACK_RELEASE_SOURCE")
     if not source.is_dir():
         _fail("TRITRACK_RELEASE_SOURCE")
     _assert_git_toplevel(source)
     project_name, version = _assert_source_identity(source)
     inventory = inventory_tracked_source(source)
     policy = _load_policy(source)
     if output.exists() or output.is_symlink():
         _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
     try:
         output_parent = output.parent.resolve(strict=True)
     except OSError:
         _fail("TRITRACK_RELEASE_OUTPUT")
     output = output_parent / output.name
-    epoch_bytes = _run_git(source, "show", "-s", "--format=%ct", inventory.commit).strip()
-    try:
-        epoch = int(epoch_bytes.decode("ascii", "strict"))
-    except (UnicodeDecodeError, ValueError):
-        _fail("TRITRACK_RELEASE_EPOCH")
+    epoch = _build_epoch(policy)
     if _run_git(source, "rev-parse", "HEAD").strip().decode("ascii") != inventory.commit:
         _fail("TRITRACK_RELEASE_SOURCE_CHANGED")

     with tempfile.TemporaryDirectory(
         dir=output.parent, prefix=".tritrack-release-staging-"
     ) as temporary:
         staging = Path(temporary)
         snapshot_one = staging / "snapshot-one"
         snapshot_two = staging / "snapshot-two"
         _materialize_snapshot(source, snapshot_one, inventory, policy)
         _materialize_snapshot(source, snapshot_two, inventory, policy)
         wheel_one, sdist_one = build_distributions(
             snapshot_one, staging / "dist-one", epoch=epoch
         )
         wheel_two, sdist_two = build_distributions(
             snapshot_two, staging / "dist-two", epoch=epoch
         )
         identities = {
             _wheel_project_identity(wheel_one),
             _wheel_project_identity(wheel_two),
         }
         if identities != {(project_name, version)}:
             _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
         if wheel_one.name != wheel_two.name or sdist_one.name != sdist_two.name:
             _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
         wheel_inspection = inspect_wheel(wheel_one, policy)
         second_wheel_inspection = inspect_wheel(wheel_two, policy)
         sdist_inspection = inspect_sdist(sdist_one, policy)
         second_sdist_inspection = inspect_sdist(sdist_two, policy)
         if wheel_inspection != second_wheel_inspection:
             _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
         if (
             sdist_inspection.member_inventory_sha256
             != second_sdist_inspection.member_inventory_sha256
         ):
             _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
         fresh_install_smoke(wheel_one, staging / "fresh-install")
         context = ReleaseContext(
             project_name=project_name,
             version=version,
             commit=inventory.commit,
             source_inventory=inventory,
             toolchain=_installed_tool_versions(),
             python_version=platform.python_version(),
             implementation=platform.python_implementation(),
             system=platform.system(),
             machine=platform.machine(),
             wheel=wheel_inspection,
             sdist=sdist_inspection,
         )
         manifest = build_release_manifest(context)
         publish_release(
             output,
             wheel_one,
             sdist_one,
             _canonical_manifest(manifest),
         )
     return manifest
diff --git a/src/tritrack_editing_assistant/align_text.py b/src/tritrack_editing_assistant/align_text.py
index 2c0e15b..bbdf794 100644
--- a/src/tritrack_editing_assistant/align_text.py
+++ b/src/tritrack_editing_assistant/align_text.py
@@ -1,123 +1,123 @@
 """Deterministic cue-addressed transcript promotion."""

 from __future__ import annotations

 import hashlib
 import json
 import os
 import stat
 import tempfile
 from collections.abc import Mapping
 from dataclasses import dataclass
 from pathlib import Path

 from jsonschema import ValidationError

 from . import hallucination
 from .contracts import validate_contract
 from .process import require_absent_output

 ALIGNMENT_PROFILE_ID = "cue-addressed-v1"
 _ARTIFACT_LIMIT_BYTES = 16 * 1024 * 1024


 @dataclass(frozen=True)
 class LoadedJsonArtifact:
     """One validated exact-byte JSON input and its immutable provenance."""

     path: Path
     contract: str
     invalid_code: str
     payload: object
     sha256: str


 def _validate_input(contract: str, payload: object, code: str) -> None:
     try:
         validate_contract(contract, payload)
     except ValidationError as error:
         raise ValueError(code) from error


 def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError(invalid_code) from error
     try:
         metadata = os.fstat(descriptor)
         if (
             not stat.S_ISREG(metadata.st_mode)
             or not 0 < metadata.st_size <= _ARTIFACT_LIMIT_BYTES
         ):
             raise ValueError(invalid_code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(_ARTIFACT_LIMIT_BYTES + 1)
         if len(encoded) > _ARTIFACT_LIMIT_BYTES:
             raise ValueError(invalid_code)
         return encoded
     except OSError as error:
         raise ValueError(invalid_code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def load_json_artifact(
     path: Path,
     *,
     contract: str,
     invalid_code: str,
 ) -> LoadedJsonArtifact:
     """Load one bounded regular JSON file and validate its strict contract."""

     selected = Path(path)
     encoded = _read_regular_bytes(selected, invalid_code)
     try:
         payload = json.loads(encoded.decode("utf-8", errors="strict"))
         validate_contract(contract, payload)
     except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
         raise ValueError(invalid_code) from error
     return LoadedJsonArtifact(
         path=selected,
         contract=contract,
         invalid_code=invalid_code,
         payload=payload,
         sha256=hashlib.sha256(encoded).hexdigest(),
     )


 def verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
     """Fail closed when an exact input file changed after validated loading."""

     try:
         encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
     except ValueError as error:
         raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED") from error
     if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
         raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED")


 def _canonical_source_cues(take: Mapping[str, object]) -> list[dict[str, object]]:
     status = take["status"]
     cues = take["cues"]
     assert isinstance(cues, list)
     if status == "empty":
         return []

     canonical: list[dict[str, object]] = []
     cue_ids: set[str] = set()
     previous_end = 0
     for cue in cues:
         assert isinstance(cue, Mapping)
         cue_id = cue["cueId"]
         start_ms = cue["startMs"]
         end_ms = cue["endMs"]
         text = cue["text"]
         assert isinstance(cue_id, str)
         assert isinstance(start_ms, int)
         assert isinstance(end_ms, int)
diff --git a/src/tritrack_editing_assistant/cli.py b/src/tritrack_editing_assistant/cli.py
index e23b09a..ed6dfe4 100644
--- a/src/tritrack_editing_assistant/cli.py
+++ b/src/tritrack_editing_assistant/cli.py
@@ -1,87 +1,89 @@
 """Command-line boundary for the TriTrack Editing Assistant scaffold."""

 from __future__ import annotations

 import argparse
 import hashlib
 import json
+import os
+import stat
 from collections.abc import Sequence
 from pathlib import Path

 from . import __version__
 from . import align_text as align_module
 from . import doctor as doctor_module
 from . import emit_fcpxml as emit_module
 from . import gemini_hybrid as hybrid_module
 from . import organizer as organizer_module
 from . import paper_edit as paper_module
 from . import run_workflow as run_module
 from . import sync_scan as sync_module
 from . import transcribe_takes as transcribe_module
 from . import validate_artifacts as validate_module

 EXIT_OK = 0
 EXIT_USAGE = 64
 EXIT_DATA = 65
 EXIT_DEPENDENCY = 69
 EXIT_OUTPUT_EXISTS = 73
 EXIT_IO = 74
 EXIT_TEMPORARY = 75
 EXIT_POLICY = 78


 class CliUsageError(ValueError):
     """Private signal for sanitized command-line usage failures."""


 class TriTrackArgumentParser(argparse.ArgumentParser):
     """Argument parser that preserves the public exit-code contract."""

     def error(self, message: str) -> None:
         del message
         raise CliUsageError("TRITRACK_USAGE")


 COMPONENTS = (
     {
         "sourceComponent": "sync_scan.py",
         "command": "sync",
         "status": "implemented",
     },
     {
         "sourceComponent": "emit_fcpxml.py",
         "command": "emit",
         "status": "implemented",
     },
     {
         "sourceComponent": "transcribe_takes.py",
         "command": "transcribe",
         "status": "implemented",
     },
     {
         "sourceComponent": "string_out.py",
         "command": "emit",
         "status": "implemented",
     },
     {
         "sourceComponent": "hallucination.py",
         "command": "transcribe",
         "status": "implemented",
     },
     {
         "sourceComponent": "organizer.py",
         "command": "organize",
         "status": "implemented",
     },
     {
         "sourceComponent": "paper_edit.py",
         "command": "paper",
         "status": "implemented",
     },
     {
         "sourceComponent": "align_text.py",
         "command": "align",
         "status": "implemented",
     },
     {
         "sourceComponent": "gemini_hybrid.py",
@@ -174,316 +176,349 @@ def _run_sync(arguments: argparse.Namespace) -> int:
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code in {
             "TRITRACK_SYNC_PROBE_FAILED",
             "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
         }:
             return EXIT_DEPENDENCY
         return EXIT_DATA

     if arguments.json:
         print(json.dumps(payload, ensure_ascii=False, indent=2))
     return EXIT_OK


 def _run_emit(arguments: argparse.Namespace) -> int:
     camera_a = [
         sync_module.MediaSource(path.name, path) for path in arguments.camera_a
     ]
     camera_b = [
         sync_module.MediaSource(path.name, path) for path in arguments.camera_b
     ]
     try:
         metadata = emit_module.ProjectMetadata(
             event_name=arguments.event_name,
             project_name=arguments.project_name,
         )
         emit_module.emit_and_publish(
             camera_a,
             camera_b,
             sync_map_path=arguments.sync_map,
             profile_id=arguments.profile,
             binding_id=arguments.binding,
             metadata=metadata,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code == "TRITRACK_SYNC_PROBE_FAILED":
             return EXIT_DEPENDENCY
         if code == "TRITRACK_PROFILE_UNKNOWN":
             return EXIT_POLICY
         return EXIT_DATA
     return EXIT_OK


 def _run_transcribe(arguments: argparse.Namespace) -> int:
     try:
         payload = transcribe_module.transcribe_and_publish(
             arguments.media,
             model_path=arguments.model,
             language=arguments.language,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code == "TRITRACK_OUTPUT_PARENT_MISSING":
             return EXIT_IO
         if code in {
             "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
             "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
             "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
         }:
             return EXIT_DEPENDENCY
         if code in {
             "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
             "TRITRACK_TRANSCRIPT_MEDIA_REQUIRED",
         }:
             return EXIT_USAGE
         return EXIT_DATA

     if arguments.json:
         takes = payload["takes"]
         assert isinstance(takes, list)
-        with arguments.output.open("rb") as stream:
-            bundle_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
+        bundle_sha256 = _output_sha256(arguments.output)
         summary = {
             "schemaVersion": "tritrack.transcribe-summary/v1",
             "takeCount": len(takes),
             "completedCount": sum(take["status"] == "completed" for take in takes),
             "emptyCount": sum(take["status"] == "empty" for take in takes),
             "bundleSha256": bundle_sha256,
         }
         print(json.dumps(summary, ensure_ascii=False, indent=2))
     return EXIT_OK


 def _alignment_summary(
     payload: dict[str, object], output_path: Path
 ) -> dict[str, object]:
     takes = payload["takes"]
     assert isinstance(takes, list)
     cue_count = 0
     revised_cue_count = 0
     for take in takes:
         assert isinstance(take, dict)
         cues = take["cues"]
         assert isinstance(cues, list)
         cue_count += len(cues)
         revised_cue_count += sum(
             isinstance(cue, dict) and cue["disposition"] == "revised"
             for cue in cues
         )
-    with output_path.open("rb") as stream:
-        artifact_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
+    artifact_sha256 = _output_sha256(output_path)
     return {
         "schemaVersion": "tritrack.align-summary/v1",
         "takeCount": len(takes),
         "cueCount": cue_count,
         "revisedCueCount": revised_cue_count,
         "artifactSha256": artifact_sha256,
     }


 def _run_align(arguments: argparse.Namespace) -> int:
     try:
         payload = align_module.align_and_publish(
             arguments.transcript,
             arguments.revision,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code == "TRITRACK_OUTPUT_PARENT_MISSING":
             return EXIT_IO
         return EXIT_DATA

     if arguments.json:
         print(
             json.dumps(
                 _alignment_summary(payload, arguments.output),
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK


 def _run_hybrid(arguments: argparse.Namespace) -> int:
     try:
         payload = hybrid_module.hybrid_and_publish(
             arguments.transcript,
             arguments.proposal,
             arguments.receipt,
             exact_model=arguments.model,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code == "TRITRACK_OUTPUT_PARENT_MISSING":
             return EXIT_IO
         if code == "TRITRACK_HYBRID_MODEL_INVALID":
             return EXIT_USAGE
         return EXIT_DATA

     if arguments.json:
         print(
             json.dumps(
                 _alignment_summary(payload, arguments.output),
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK


 def _run_organize(arguments: argparse.Namespace) -> int:
     try:
         payload = organizer_module.organize_and_publish(
             arguments.aligned,
             arguments.grouping,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         if code == "TRITRACK_OUTPUT_EXISTS":
             return EXIT_OUTPUT_EXISTS
         if code in {
             "TRITRACK_OUTPUT_PARENT_MISSING",
             "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
         }:
             return EXIT_IO
         return EXIT_DATA

     if arguments.json:
         questions = payload["questions"]
         segments = payload["segments"]
         reserve = payload["reserve"]
         assert isinstance(questions, list)
         assert isinstance(segments, list)
         assert isinstance(reserve, list)
-        with arguments.output.open("rb") as stream:
-            artifact_sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
+        artifact_sha256 = _output_sha256(arguments.output)
         print(
             json.dumps(
                 {
                     "schemaVersion": "tritrack.organize-summary/v1",
                     "questionCount": len(questions),
                     "segmentCount": len(segments),
                     "reserveCount": len(reserve),
                     "artifactSha256": artifact_sha256,
                 },
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK


 def _paper_error_exit(code: str) -> int:
     if code == "TRITRACK_OUTPUT_EXISTS":
         return EXIT_OUTPUT_EXISTS
     if code in {
         "TRITRACK_OUTPUT_PARENT_MISSING",
         "TRITRACK_PAPER_INPUT_UNREADABLE",
     }:
         return EXIT_IO
     return EXIT_DATA


 def _output_sha256(output_path: Path) -> str:
-    with output_path.open("rb") as stream:
-        return hashlib.file_digest(stream, "sha256").hexdigest()
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
+    descriptor = os.open(output_path, flags)
+    try:
+        before = os.fstat(descriptor)
+        if not stat.S_ISREG(before.st_mode):
+            raise OSError("TRITRACK_OUTPUT_UNREADABLE")
+        digest = hashlib.sha256()
+        total = 0
+        remaining = before.st_size + 1
+        while remaining:
+            chunk = os.read(descriptor, min(1024 * 1024, remaining))
+            if not chunk:
+                break
+            digest.update(chunk)
+            total += len(chunk)
+            remaining -= len(chunk)
+        after = os.fstat(descriptor)
+        if (
+            total != before.st_size
+            or (
+                before.st_dev,
+                before.st_ino,
+                before.st_size,
+                before.st_mtime_ns,
+            )
+            != (
+                after.st_dev,
+                after.st_ino,
+                after.st_size,
+                after.st_mtime_ns,
+            )
+        ):
+            raise OSError("TRITRACK_OUTPUT_CHANGED")
+        return digest.hexdigest()
+    finally:
+        os.close(descriptor)


 def _run_paper_export(arguments: argparse.Namespace) -> int:
     try:
         summary = paper_module.export_workbook(
             arguments.aligned,
             grouping_path=arguments.grouping,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         return _paper_error_exit(code)
     if arguments.json:
         print(
             json.dumps(
                 {
                     "schemaVersion": "tritrack.paper-export-summary/v1",
                     **summary,
                     "artifactSha256": _output_sha256(arguments.output),
                 },
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK


 def _run_paper_apply(arguments: argparse.Namespace) -> int:
     try:
         grouping = paper_module.apply_workbook(
             arguments.aligned,
             arguments.workbook,
             output_path=arguments.output,
         )
     except (TypeError, ValueError) as error:
         code = str(error).split(":", 1)[0]
         print(json.dumps({"error": code}, ensure_ascii=False))
         return _paper_error_exit(code)
     if arguments.json:
         questions = grouping["questions"]
         reserve = grouping["reserve"]
         assert isinstance(questions, list)
         assert isinstance(reserve, list)
         answer_count = 0
         for question in questions:
             assert isinstance(question, dict)
             answers = question["answers"]
             assert isinstance(answers, list)
             answer_count += len(answers)
         print(
             json.dumps(
                 {
                     "schemaVersion": "tritrack.paper-apply-summary/v1",
                     "questionCount": len(questions),
                     "answerCount": answer_count,
                     "reserveCount": len(reserve),
                     "artifactSha256": _output_sha256(arguments.output),
                 },
                 ensure_ascii=False,
                 indent=2,
             )
         )
     return EXIT_OK


 def _run_error_exit(code: str) -> int:
     if code == "TRITRACK_OUTPUT_EXISTS":
         return EXIT_OUTPUT_EXISTS
     if code in {
         "TRITRACK_OUTPUT_PARENT_MISSING",
         "TRITRACK_RUN_INPUT_UNREADABLE",
         "TRITRACK_STORY_SOURCE_UNREADABLE",
         "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
         "TRITRACK_PAPER_INPUT_UNREADABLE",
     }:
         return EXIT_IO
     if code in {
         "TRITRACK_SYNC_PROBE_FAILED",
         "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
diff --git a/src/tritrack_editing_assistant/emit_fcpxml.py b/src/tritrack_editing_assistant/emit_fcpxml.py
index e6e6945..a2ec2f1 100644
--- a/src/tritrack_editing_assistant/emit_fcpxml.py
+++ b/src/tritrack_editing_assistant/emit_fcpxml.py
@@ -1,130 +1,151 @@
 """Profile-bound FCPXML rendering and no-overwrite publication."""

 from __future__ import annotations

 import json
 import os
 import re
+import stat
 import tempfile
 import xml.etree.ElementTree as ET
 from collections.abc import Mapping, Sequence
 from dataclasses import dataclass
 from decimal import Decimal
 from pathlib import Path

 from jsonschema import ValidationError

 from . import contracts, doctor, process, string_out, sync_scan

 ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
 MAX_SYNC_MAP_BYTES = 16 * 1024 * 1024
 FORMAT_NAME = "FFVideoFormat3840x2160p2997"


 @dataclass(frozen=True)
 class ProjectMetadata:
     """Caller-owned names copied into one public string-out project."""

     event_name: str
     project_name: str

     def __post_init__(self) -> None:
         for value in (self.event_name, self.project_name):
             if (
                 not isinstance(value, str)
                 or not value.strip()
                 or any(ord(character) < 32 for character in value)
             ):
                 raise ValueError("TRITRACK_EMIT_METADATA_INVALID")


 def load_sync_map(path: str | os.PathLike[str]) -> dict[str, object]:
     """Load one strict sync-map-v1 while preserving decimal spellings."""

     source = Path(path)
+    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
     try:
-        raw = source.read_bytes()
+        descriptor = os.open(source, flags)
+    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
+        raise ValueError("TRITRACK_EMIT_SYNC_MAP_UNREADABLE") from error
+    except OSError as error:
+        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
+    try:
+        details = os.fstat(descriptor)
+        if (
+            not stat.S_ISREG(details.st_mode)
+            or not 0 < details.st_size <= MAX_SYNC_MAP_BYTES
+        ):
+            raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            raw = stream.read(MAX_SYNC_MAP_BYTES + 1)
+        if len(raw) > MAX_SYNC_MAP_BYTES or b"\x00" in raw:
+            raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
     except OSError as error:
         raise ValueError("TRITRACK_EMIT_SYNC_MAP_UNREADABLE") from error
-    if len(raw) > MAX_SYNC_MAP_BYTES or b"\x00" in raw:
-        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
     try:
         payload = json.loads(raw.decode("utf-8"), parse_float=Decimal)
     except (UnicodeDecodeError, json.JSONDecodeError) as error:
         raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
     if not isinstance(payload, dict):
         raise TypeError("TRITRACK_EMIT_SYNC_MAP_INVALID")
     try:
         contracts.validate_contract("sync-map-v1", payload)
     except ValidationError as error:
         raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
     return payload


 def _frame_time(timeline: string_out.StringOut, frames: int) -> str:
     if frames == 0:
         return "0s"
     numerator = frames * timeline.frame_numerator
     return f"{numerator}/{timeline.frame_denominator}s"


 def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
     parameters = binding["parameters"]
     if not isinstance(parameters, list):
         raise TypeError("TRITRACK_FCPXML_BINDING_INVALID")
     values = {
         str(parameter["name"]): str(parameter["value"])
         for parameter in parameters
         if isinstance(parameter, Mapping)
     }
     expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
     if set(values) != expected:
         raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
     return values


 def _source_uri(path: Path) -> str:
     try:
         return path.absolute().as_uri()
     except ValueError as error:
         raise ValueError("TRITRACK_EMIT_SOURCE_INVALID") from error


 def render_fcpxml(
     sync_map: Mapping[str, object],
     sources: Sequence[Mapping[str, object]],
     *,
     profile_id: str,
     binding_id: str,
     metadata: ProjectMetadata,
 ) -> str:
     """Render deterministic FCPXML from the closed public inputs."""

     if not isinstance(metadata, ProjectMetadata):
         raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
     profile = doctor.load_profile(profile_id)
     binding = doctor.load_title_binding(binding_id)
     timeline = string_out.build_string_out(sync_map, sources, profile=profile)
     if timeline.profile_id != profile_id:
         raise ValueError("TRITRACK_PROFILE_MISMATCH")
     styles = _style_values(binding)

     root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
     resources_element = ET.SubElement(root, "resources")
     ET.SubElement(
         resources_element,
         "format",
         {
             "id": "r1",
             "name": FORMAT_NAME,
             "frameDuration": str(profile["frameDuration"]),
             "width": str(profile["width"]),
             "height": str(profile["height"]),
             "colorSpace": str(profile["colorSpace"]),
         },
     )
     ET.SubElement(
         resources_element,
         "effect",
         {
             "id": "r2",
diff --git a/src/tritrack_editing_assistant/organizer.py b/src/tritrack_editing_assistant/organizer.py
index 0a6b246..773791b 100644
--- a/src/tritrack_editing_assistant/organizer.py
+++ b/src/tritrack_editing_assistant/organizer.py
@@ -324,161 +324,161 @@ def build_working_cut(
         aligned_sha256=aligned_sha256,
     )
     questions = canonical_grouping["questions"]
     reserve = canonical_grouping["reserve"]
     assert isinstance(questions, list)
     assert isinstance(reserve, list)

     compiled_questions: list[dict[str, object]] = []
     segments: list[dict[str, object]] = []
     story_order = 0
     for question in sorted(questions, key=lambda item: item["order"]):
         assert isinstance(question, Mapping)
         compiled_questions.append(
             {
                 "id": question["id"],
                 "question": question["question"],
                 "order": question["order"],
             }
         )
         answers = question["answers"]
         assert isinstance(answers, list)
         for answer in sorted(answers, key=lambda item: item["order"]):
             assert isinstance(answer, Mapping)
             story_order += 1
             compiled = {
                 "id": answer["id"],
                 "storyOrder": story_order,
                 "questionId": question["id"],
                 **_compiled_span(answer, aligned_index=aligned_index),
             }
             if "note" in answer:
                 compiled["note"] = answer["note"]
             segments.append(compiled)

     compiled_reserve: list[dict[str, object]] = []
     for item in sorted(reserve, key=lambda candidate: candidate["order"]):
         assert isinstance(item, Mapping)
         compiled = {
             "id": item["id"],
             "order": item["order"],
             **_compiled_span(item, aligned_index=aligned_index),
             "reason": item["reason"],
         }
         if "note" in item:
             compiled["note"] = item["note"]
         compiled_reserve.append(compiled)

     working_cut: dict[str, object] = {
         "schemaVersion": "tritrack.working-cut/v1",
         "organizationProfileId": ORGANIZATION_PROFILE_ID,
         "alignedTranscriptSha256": aligned_sha256,
         "groupingSha256": grouping_sha256,
         "questions": compiled_questions,
         "segments": segments,
         "reserve": compiled_reserve,
     }
     validate_contract("working-cut-v1", working_cut)
     return working_cut


 def _encode_contract(name: str, payload: object) -> bytes:
     validate_contract(name, payload)
     return (
         json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
     ).encode("utf-8")


 def encode_grouping(payload: object) -> bytes:
     """Return canonical bytes for one schema-valid grouping."""

     return _encode_contract("grouping-v1", payload)


 def encode_working_cut(payload: object) -> bytes:
     """Return canonical bytes for one strict working cut."""

     return _encode_contract("working-cut-v1", payload)


 def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
         raise ValueError("TRITRACK_ORGANIZER_INPUT_UNREADABLE") from error
     except OSError as error:
         raise ValueError(invalid_code) from error
     try:
         metadata = os.fstat(descriptor)
         if (
             not stat.S_ISREG(metadata.st_mode)
             or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
         ):
             raise ValueError(invalid_code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(_JSON_LIMIT_BYTES + 1)
         if len(encoded) > _JSON_LIMIT_BYTES:
             raise ValueError(invalid_code)
         return encoded
     except OSError as error:
         raise ValueError(invalid_code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def _load_json_artifact(
     path: Path,
     *,
     contract: str,
     invalid_code: str,
 ) -> LoadedJsonArtifact:
     selected = Path(path)
     encoded = _read_regular_bytes(selected, invalid_code)
     try:
         payload = json.loads(encoded.decode("utf-8", errors="strict"))
         validate_contract(contract, payload)
     except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
         raise ValueError(invalid_code) from error
     return LoadedJsonArtifact(
         path=selected,
         payload=payload,
         encoded=encoded,
         sha256=hashlib.sha256(encoded).hexdigest(),
         invalid_code=invalid_code,
     )


 def _verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
     try:
         encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
     except ValueError as error:
         raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED") from error
     if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
         raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED")


 def _publish_working_cut(payload: object, output_path: Path) -> None:
     destination = require_absent_output(output_path)
     if not destination.parent.is_dir():
         raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     encoded = encode_working_cut(payload)
     descriptor, temporary_name = tempfile.mkstemp(
         prefix=f".{destination.name}.",
         suffix=".tmp",
         dir=destination.parent,
     )
     temporary_path = Path(temporary_name)
     try:
         with os.fdopen(descriptor, "wb") as stream:
             stream.write(encoded)
             stream.flush()
             os.fsync(stream.fileno())
         try:
             os.link(temporary_path, destination)
         except FileExistsError as error:
             raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
     finally:
diff --git a/src/tritrack_editing_assistant/paper_edit.py b/src/tritrack_editing_assistant/paper_edit.py
index d6feb95..06bc13b 100644
--- a/src/tritrack_editing_assistant/paper_edit.py
+++ b/src/tritrack_editing_assistant/paper_edit.py
@@ -1,160 +1,160 @@
 """Strict XLSX transport for the cue-addressed paper-edit round trip."""

 from __future__ import annotations

 import hashlib
 import io
 import json
 import os
 import stat
 import tempfile
 import xml.etree.ElementTree as element_tree
 import zipfile
 from collections.abc import Mapping, Sequence
 from dataclasses import dataclass
 from pathlib import Path, PurePosixPath

 from jsonschema import ValidationError
 from openpyxl import Workbook, load_workbook
 from openpyxl.cell.cell import Cell
 from openpyxl.utils.exceptions import InvalidFileException

 from . import __version__, organizer
 from .contracts import validate_contract
 from .process import require_absent_output

 WORKBOOK_SCHEMA_VERSION = "tritrack.paper-workbook/v1"
 CUES_HEADERS = (
     "TakeId",
     "SourceSha256",
     "CueId",
     "StartMs",
     "EndMs",
     "Text",
     "Disposition",
 )
 QUESTIONS_HEADERS = ("QuestionId", "Question", "Order")
 SELECTIONS_HEADERS = (
     "Placement",
     "SegmentId",
     "QuestionId",
     "Order",
     "TakeId",
     "StartCueId",
     "EndCueId",
     "ReserveReason",
     "EditorNote",
 )
 MANIFEST_HEADERS = ("Key", "Value")
 SHEET_NAMES = ("Cues", "Questions", "Selections", "_TriTrack")
 _JSON_LIMIT_BYTES = 16 * 1024 * 1024
 _WORKBOOK_LIMIT_BYTES = 64 * 1024 * 1024
 _WORKBOOK_MEMBER_LIMIT = 512
 _WORKBOOK_EXPANDED_LIMIT_BYTES = 256 * 1024 * 1024
 _WORKBOOK_SINGLE_MEMBER_LIMIT_BYTES = 128 * 1024 * 1024


 @dataclass(frozen=True)
 class LoadedArtifact:
     path: Path
     payload: object
     encoded: bytes
     sha256: str
     invalid_code: str
     limit: int


 @dataclass(frozen=True)
 class ValidatedWorkbook:
     aligned_sha256: str
     workbook_sha256: str
     workbook_schema_version: str
     cue_count: int
     question_count: int
     answer_count: int
     reserve_count: int
     grouping: dict[str, object]


 def _read_regular_bytes(path: Path, *, limit: int, invalid_code: str) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
         raise ValueError("TRITRACK_PAPER_INPUT_UNREADABLE") from error
     except OSError as error:
         raise ValueError(invalid_code) from error
     try:
         metadata = os.fstat(descriptor)
         if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
             raise ValueError(invalid_code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(limit + 1)
         if len(encoded) > limit:
             raise ValueError(invalid_code)
         return encoded
     except OSError as error:
         raise ValueError(invalid_code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def _load_json(
     path: Path,
     *,
     contract: str,
     invalid_code: str,
 ) -> LoadedArtifact:
     selected = Path(path)
     encoded = _read_regular_bytes(
         selected,
         limit=_JSON_LIMIT_BYTES,
         invalid_code=invalid_code,
     )
     try:
         payload = json.loads(encoded.decode("utf-8", errors="strict"))
         validate_contract(contract, payload)
     except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
         raise ValueError(invalid_code) from error
     return LoadedArtifact(
         selected,
         payload,
         encoded,
         hashlib.sha256(encoded).hexdigest(),
         invalid_code,
         _JSON_LIMIT_BYTES,
     )


 def _verify_unchanged(artifact: LoadedArtifact) -> None:
     try:
         encoded = _read_regular_bytes(
             artifact.path,
             limit=artifact.limit,
             invalid_code=artifact.invalid_code,
         )
     except ValueError as error:
         raise ValueError("TRITRACK_PAPER_INPUT_CHANGED") from error
     if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
         raise ValueError("TRITRACK_PAPER_INPUT_CHANGED")


 def _literal(cell: Cell, value: object, *, text_format: bool = False) -> None:
     cell.value = value
     if isinstance(value, str):
         cell.data_type = "s"
     if text_format:
         cell.number_format = "@"


 def _write_row(
     worksheet,
     row: int,
     values: Sequence[object],
     *,
     text_columns: frozenset[int] = frozenset(),
 ) -> None:
diff --git a/src/tritrack_editing_assistant/run_workflow.py b/src/tritrack_editing_assistant/run_workflow.py
index 9fd7ac7..3415c26 100644
--- a/src/tritrack_editing_assistant/run_workflow.py
+++ b/src/tritrack_editing_assistant/run_workflow.py
@@ -137,161 +137,161 @@ def _validate_manifest(payload: object) -> dict[str, object]:
         if not isinstance(artifact, Mapping) or artifact["fileName"] != file_name:
             raise _manifest_error()

     stages = payload["stages"]
     assert isinstance(stages, list)
     if [stage["name"] for stage in stages] != list(spec.stages):
         raise _manifest_error()
     for stage, expected_name in zip(stages, spec.stages, strict=True):
         assert isinstance(stage, Mapping)
         output_hashes = stage["outputHashes"]
         expected_logical = dict(zip(spec.stages, spec.artifacts, strict=True))[
             expected_name
         ][0]
         if output_hashes != {
             expected_logical: artifacts[expected_logical]["sha256"]
         }:
             raise _manifest_error()
     return payload


 def build_manifest(
     *,
     run_id: str,
     profile_id: str,
     binding_id: str,
     phase: str,
     manifest_chain: Sequence[str],
     sources: Sequence[Mapping[str, object]],
     stages: Sequence[Mapping[str, object]],
     artifacts: Mapping[str, Mapping[str, str]],
 ) -> dict[str, object]:
     """Build one path-free immutable run receipt from completed stage facts."""

     try:
         spec = PHASE_SPECS[phase]
         expected_artifacts = {logical_name for logical_name, _ in spec.artifacts}
         if set(artifacts) != expected_artifacts:
             raise ValueError
         source_copies = [copy.deepcopy(dict(source)) for source in sources]
         source_copies.sort(key=lambda source: (source["camera"], source["mediaId"]))
         stage_by_name = {
             stage["name"]: copy.deepcopy(dict(stage)) for stage in stages
         }
         if (
             len(stage_by_name) != len(stages)
             or set(stage_by_name) != set(spec.stages)
         ):
             raise ValueError
         artifact_copies = {
             logical_name: copy.deepcopy(dict(artifacts[logical_name]))
             for logical_name, _ in spec.artifacts
         }
         payload: dict[str, object] = {
             "schemaVersion": "tritrack.run-manifest/v1",
             "toolVersion": __version__,
             "runId": run_id,
             "profileId": profile_id,
             "bindingId": binding_id,
             "phase": phase,
             "nextAction": spec.next_action,
             "manifestChain": list(manifest_chain),
             "sources": source_copies,
             "artifacts": artifact_copies,
             "stages": [stage_by_name[name] for name in spec.stages],
         }
     except (KeyError, TypeError, ValueError) as error:
         raise _manifest_error(error)
     return _validate_manifest(payload)


 def encode_manifest(payload: object) -> bytes:
     """Return canonical UTF-8 bytes for one semantically strict manifest."""

     validated = _validate_manifest(payload)
     return (
         json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
     ).encode("utf-8")


 def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError(code) from error
     try:
         metadata = os.fstat(descriptor)
         if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
             raise ValueError(code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(limit + 1)
         if len(encoded) > limit:
             raise ValueError(code)
         return encoded
     except OSError as error:
         raise ValueError(code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def _validate_json_artifact(
     encoded: bytes, *, contract: str, code: str
 ) -> object:
     try:
         payload = json.loads(
             encoded.decode("utf-8", errors="strict"), parse_float=Decimal
         )
         contracts.validate_contract(contract, payload)
     except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
         raise ValueError(code) from error
     return payload


 def _validate_artifact(
     logical_name: str,
     encoded: bytes,
     *,
     manifest: Mapping[str, object],
 ) -> None:
     contracts_by_name = {
         "syncMap": "sync-map-v1",
         "transcriptBundle": "transcript-bundle-v1",
         "alignedTranscript": "aligned-transcript-v1",
         "grouping": "grouping-v1",
         "workingCut": "working-cut-v1",
     }
     contract = contracts_by_name.get(logical_name)
     if contract is not None:
         _validate_json_artifact(
             encoded, contract=contract, code="TRITRACK_RUN_ARTIFACT_INVALID"
         )
         return
     if logical_name == "doctorReceipt":
         try:
             payload = json.loads(encoded.decode("utf-8", errors="strict"))
         except (UnicodeError, json.JSONDecodeError) as error:
             raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
         if (
             not isinstance(payload, dict)
             or payload.get("schemaVersion") != "tritrack.doctor-receipt/v1"
             or payload.get("profileId") != manifest["profileId"]
             or payload.get("titleBindingId") != manifest["bindingId"]
             or not isinstance(payload.get("supported"), bool)
             or not isinstance(payload.get("checks"), list)
             or not isinstance(payload.get("remediation"), list)
         ):
             raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID")
         return
     if logical_name in {"stringOut", "storyCut"}:
         try:
             text = encoded.decode("utf-8", errors="strict")
             emit_fcpxml.validate_fcpxml(
                 text,
                 profile=doctor.load_profile(str(manifest["profileId"])),
                 binding=doctor.load_title_binding(str(manifest["bindingId"])),
             )
         except (UnicodeError, TypeError, ValueError, ValidationError) as error:
@@ -416,161 +416,161 @@ def _verify_staging(staging: Path, manifest: Mapping[str, object]) -> None:
     if observed != expected:
         raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
     for logical_name, artifact in artifacts.items():
         assert isinstance(artifact, Mapping)
         encoded = _read_regular_bytes(
             staging / str(artifact["fileName"]),
             limit=_ARTIFACT_LIMIT_BYTES,
             code="TRITRACK_RUN_ARTIFACT_INVALID",
         )
         if hashlib.sha256(encoded).hexdigest() != artifact["sha256"]:
             raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
         _validate_artifact(str(logical_name), encoded, manifest=manifest)


 def _fsync_directory(path: Path) -> None:
     flags = os.O_RDONLY
     if hasattr(os, "O_DIRECTORY"):
         flags |= os.O_DIRECTORY
     descriptor = os.open(path, flags)
     try:
         os.fsync(descriptor)
     finally:
         os.close(descriptor)


 def publish_bundle(
     output_dir: Path,
     builder: Callable[[Path], Mapping[str, object]],
 ) -> LoadedRunBundle:
     """Build privately, then hard-link a complete absent bundle manifest last."""

     destination = process.require_absent_output(output_dir)
     if not destination.parent.is_dir():
         raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     staging = Path(
         tempfile.mkdtemp(
             prefix=f".{destination.name}.staging-", dir=destination.parent
         )
     )
     reserved = False
     linked: list[Path] = []
     try:
         manifest = _validate_manifest(builder(staging))
         _verify_staging(staging, manifest)
         manifest_bytes = encode_manifest(manifest)
         _write_manifest(staging / MANIFEST_FILE_NAME, manifest_bytes)
         try:
             os.mkdir(destination, 0o755)
             reserved = True
         except FileExistsError as error:
             raise ValueError("TRITRACK_OUTPUT_EXISTS") from error

         artifacts = manifest["artifacts"]
         assert isinstance(artifacts, Mapping)
         file_names = sorted(
             str(artifact["fileName"]) for artifact in artifacts.values()
         )
         for file_name in (*file_names, MANIFEST_FILE_NAME):
             target = destination / file_name
             os.link(staging / file_name, target)
             linked.append(target)
         _fsync_directory(destination)
         return load_bundle(destination, expected_phase=str(manifest["phase"]))
     except BaseException:
         if reserved:
             for path in reversed(linked):
                 try:
                     path.unlink()
                 except OSError:
                     pass
             try:
                 destination.rmdir()
             except OSError:
                 pass
         raise
     finally:
         shutil.rmtree(staging, ignore_errors=True)


 def _hash_regular_path(path: Path, *, code: str) -> str:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError(code) from error
     digest = hashlib.sha256()
     try:
         metadata = os.fstat(descriptor)
         if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
             raise ValueError(code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             while chunk := stream.read(_HASH_CHUNK_BYTES):
                 digest.update(chunk)
     except OSError as error:
         raise ValueError(code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)
     return digest.hexdigest()


 def _hash_value(payload: object) -> str:
     encoded = json.dumps(
         payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
     ).encode("utf-8")
     return hashlib.sha256(encoded).hexdigest()


 def _artifact_records(
     staging: Path, phase: str
 ) -> dict[str, dict[str, str]]:
     return {
         logical_name: {
             "fileName": file_name,
             "sha256": _hash_regular_path(
                 staging / file_name, code="TRITRACK_RUN_ARTIFACT_INVALID"
             ),
         }
         for logical_name, file_name in PHASE_SPECS[phase].artifacts
     }


 def _source_inventory(
     camera_a_sources: Sequence[sync_scan.MediaSource],
     camera_b_sources: Sequence[sync_scan.MediaSource],
     transcribe_media: Sequence[Path],
 ) -> tuple[list[dict[str, object]], dict[Path, str]]:
     if not camera_a_sources or not camera_b_sources:
         raise ValueError("TRITRACK_RUN_SOURCE_REQUIRED")
     declared: list[tuple[str, sync_scan.MediaSource]] = [
         *(("A", source) for source in camera_a_sources),
         *(("B", source) for source in camera_b_sources),
     ]
     media_ids = [source.media_id for _, source in declared]
     if (
         len(media_ids) != len(set(media_ids))
         or any(source.media_id != source.path.name for _, source in declared)
     ):
         raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
     declared_paths = [source.path for _, source in declared]
     if len(declared_paths) != len(set(declared_paths)):
         raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
     selected_transcribe = [Path(path) for path in transcribe_media]
     if (
         not selected_transcribe
         or len(selected_transcribe) != len(set(selected_transcribe))
         or any(path not in declared_paths for path in selected_transcribe)
     ):
         raise ValueError("TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID")
     source_hashes = {
         source.path: _hash_regular_path(
             source.path, code="TRITRACK_RUN_INPUT_UNREADABLE"
         )
         for _, source in declared
     }
     selected_set = set(selected_transcribe)
     inventory = [
         {
diff --git a/src/tritrack_editing_assistant/story_fcpxml.py b/src/tritrack_editing_assistant/story_fcpxml.py
index a755325..5521e79 100644
--- a/src/tritrack_editing_assistant/story_fcpxml.py
+++ b/src/tritrack_editing_assistant/story_fcpxml.py
@@ -553,217 +553,217 @@ def render_story_fcpxml(
     sequence = ET.SubElement(
         project,
         "sequence",
         {
             "format": "r1",
             "duration": _frame_time(timeline, timeline.duration_frames),
             "tcStart": "0s",
             "tcFormat": str(profile["timecodeFormat"]),
             "audioLayout": "stereo",
             "audioRate": f"{int(profile['audioRate']) // 1000}k",
         },
     )
     spine = ET.SubElement(sequence, "spine")
     for index, segment in enumerate(timeline.segments, start=1):
         gap = ET.SubElement(
             spine,
             "gap",
             {
                 "name": segment.segment_id,
                 "offset": _frame_time(timeline, segment.offset_frames),
                 "start": "0s",
                 "duration": _frame_time(timeline, segment.duration_frames),
             },
         )
         for lane, clip in enumerate(segment.clips, start=1):
             attributes = {
                 "ref": source_ids[(clip.camera, clip.media_id)],
                 "lane": str(lane),
                 "offset": _frame_time(timeline, clip.offset_frames),
                 "name": clip.media_id,
                 "start": _frame_time(timeline, clip.start_frames),
                 "duration": _frame_time(timeline, clip.duration_frames),
                 "srcEnable": "all" if clip.audio_enabled else "video",
             }
             if clip.audio_enabled:
                 attributes["audioRole"] = "dialogue"
             ET.SubElement(gap, "asset-clip", attributes)
         title = ET.SubElement(
             gap,
             "title",
             {
                 "ref": "r2",
                 "lane": str(len(segment.clips) + 1),
                 "offset": _frame_time(timeline, segment.offset_frames),
                 "name": f"{segment.segment_id} - Basic Title",
                 "start": "0s",
                 "duration": _frame_time(timeline, segment.duration_frames),
             },
         )
         text_element = ET.SubElement(title, "text")
         style_id = f"ts{index:03d}"
         text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
         text_style.text = segment.title_text
         definition = ET.SubElement(title, "text-style-def", {"id": style_id})
         ET.SubElement(
             definition,
             "text-style",
             {
                 name: styles[name]
                 for name in (
                     "alignment",
                     "font",
                     "fontColor",
                     "fontFace",
                     "fontSize",
                 )
             },
         )

     ET.indent(root, space="    ")
     body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
     rendered = (
         '<?xml version="1.0" encoding="UTF-8"?>\n'
         f"{emit_fcpxml.ALLOWED_DOCTYPE}\n{body}\n"
     )
     emit_fcpxml.validate_fcpxml(rendered, profile=profile, binding=binding)
     return rendered


 def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError(invalid_code) from error
     try:
         metadata = os.fstat(descriptor)
         if (
             not stat.S_ISREG(metadata.st_mode)
             or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
         ):
             raise ValueError(invalid_code)
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(_JSON_LIMIT_BYTES + 1)
         if len(encoded) > _JSON_LIMIT_BYTES:
             raise ValueError(invalid_code)
         return encoded
     except OSError as error:
         raise ValueError(invalid_code) from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def _load_artifact(path: Path, *, contract: str, code: str) -> _LoadedArtifact:
     selected = Path(path)
     encoded = _read_regular_bytes(selected, code)
     try:
         payload = json.loads(
             encoded.decode("utf-8", errors="strict"), parse_float=Decimal
         )
         contracts.validate_contract(contract, payload)
     except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
         raise ValueError(code) from error
     return _LoadedArtifact(
         path=selected,
         payload=payload,
         encoded=encoded,
         sha256=hashlib.sha256(encoded).hexdigest(),
         invalid_code=code,
     )


 def _verify_artifact(artifact: _LoadedArtifact) -> None:
     try:
         encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
     except ValueError as error:
         raise ValueError("TRITRACK_STORY_INPUT_CHANGED") from error
     if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
         raise ValueError("TRITRACK_STORY_INPUT_CHANGED")


 def _hash_regular_media(path: Path) -> str:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
     digest = hashlib.sha256()
     try:
         metadata = os.fstat(descriptor)
         if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
             raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE")
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             while chunk := stream.read(_HASH_CHUNK_BYTES):
                 digest.update(chunk)
     except OSError as error:
         raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)
     return digest.hexdigest()


 def emit_story_and_publish(
     camera_a_sources: Sequence[sync_scan.MediaSource],
     camera_b_sources: Sequence[sync_scan.MediaSource],
     *,
     sync_map_path: Path,
     aligned_path: Path,
     grouping_path: Path,
     working_cut_path: Path,
     profile_id: str,
     binding_id: str,
     metadata: emit_fcpxml.ProjectMetadata,
     output_path: Path,
 ) -> str:
     """Load exact authorities, render a story cut, and publish without overwrite."""

     destination = process.require_absent_output(output_path)
     if not destination.parent.is_dir():
         raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     sync_map = _load_artifact(
         sync_map_path, contract="sync-map-v1", code="TRITRACK_STORY_SYNC_INVALID"
     )
     aligned = _load_artifact(
         aligned_path,
         contract="aligned-transcript-v1",
         code="TRITRACK_STORY_ALIGNED_INVALID",
     )
     grouping = _load_artifact(
         grouping_path,
         contract="grouping-v1",
         code="TRITRACK_STORY_GROUPING_INVALID",
     )
     working_cut = _load_artifact(
         working_cut_path,
         contract="working-cut-v1",
         code="TRITRACK_STORY_WORKING_CUT_INVALID",
     )
     if grouping.encoded != organizer.encode_grouping(grouping.payload):
         raise ValueError("TRITRACK_STORY_GROUPING_NONCANONICAL")
     if working_cut.encoded != organizer.encode_working_cut(working_cut.payload):
         raise ValueError("TRITRACK_STORY_WORKING_CUT_NONCANONICAL")

     profile = doctor.load_profile(profile_id)
     doctor.load_title_binding(binding_id)
     source_hashes = {
         (camera, source.media_id): _hash_regular_media(source.path)
         for camera, camera_sources in (
             ("A", camera_a_sources),
             ("B", camera_b_sources),
         )
         for source in camera_sources
     }
     probed = emit_fcpxml.probe_sources(
         camera_a_sources, camera_b_sources, profile=profile
     )
     sources = [
         {**source, "sha256": source_hashes[(source["camera"], source["media_id"])]}
         for source in probed
diff --git a/src/tritrack_editing_assistant/transcribe_takes.py b/src/tritrack_editing_assistant/transcribe_takes.py
index 4b135e3..de07a06 100644
--- a/src/tritrack_editing_assistant/transcribe_takes.py
+++ b/src/tritrack_editing_assistant/transcribe_takes.py
@@ -84,342 +84,445 @@ def canonicalize_whisper_evidence(
             raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID")
         offsets = _object(segment.get("offsets"))
         start_ms = _millisecond(offsets.get("from"))
         end_ms = _millisecond(offsets.get("to"))
         if end_ms > audio_duration_ms:
             if (
                 index != len(transcription)
                 or start_ms >= audio_duration_ms
                 or end_ms - audio_duration_ms > _MAX_FINAL_CUE_PADDING_MS
             ):
                 raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
             end_ms = audio_duration_ms
         if not (previous_end <= start_ms < end_ms <= audio_duration_ms):
             raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
         cues.append(
             {
                 "cueId": f"cue-{len(cues) + 1:06d}",
                 "startMs": start_ms,
                 "endMs": end_ms,
                 "text": text,
             }
         )
         previous_end = end_ms

     hallucination.reject_repeated_cues([str(cue["text"]) for cue in cues])
     return cues


 def build_transcript_bundle(
     takes: Sequence[TranscribedTake],
     *,
     language: str,
     model_sha256: str,
     engine_version: str,
 ) -> dict[str, object]:
     """Build and validate one stable, path-free local transcript bundle."""

     ordered = sorted(takes, key=lambda take: take.take_id)
     take_ids = [take.take_id for take in ordered]
     if len(take_ids) != len(set(take_ids)):
         raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")

     bundle: dict[str, object] = {
         "schemaVersion": "tritrack.transcript-bundle/v1",
         "profileId": TRANSCRIPTION_PROFILE_ID,
         "language": language,
         "modelSha256": model_sha256,
         "engine": {"name": "whisper-cli", "version": engine_version},
         "takes": [
             {
                 "takeId": take.take_id,
                 "sourceSha256": take.source_sha256,
                 "status": take.status,
                 "cues": [dict(cue) for cue in take.cues],
             }
             for take in ordered
         ],
     }
     validate_contract("transcript-bundle-v1", bundle)
     return bundle


 def encode_transcript_bundle(bundle: object) -> str:
     """Encode a validated bundle with stable key ordering and final newline."""

     validate_contract("transcript-bundle-v1", bundle)
     return json.dumps(
         bundle,
         ensure_ascii=False,
         indent=2,
         sort_keys=True,
     ) + "\n"


 def _require_readable_file(path: Path, code: str) -> Path:
     if not path.is_file() or not os.access(path, os.R_OK):
         raise ValueError(code)
     return path


-def _sha256_file(path: Path) -> str:
-    digest = hashlib.sha256()
-    with path.open("rb") as stream:
-        while chunk := stream.read(_HASH_CHUNK_BYTES):
+def _sha256_file(
+    path: Path, code: str = "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
+) -> str:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError(code) from error
+    try:
+        before = os.fstat(descriptor)
+        if not stat.S_ISREG(before.st_mode):
+            raise ValueError(code)
+        digest = hashlib.sha256()
+        total = 0
+        remaining = before.st_size + 1
+        while remaining:
+            chunk = os.read(descriptor, min(_HASH_CHUNK_BYTES, remaining))
+            if not chunk:
+                break
             digest.update(chunk)
-    return digest.hexdigest()
+            total += len(chunk)
+            remaining -= len(chunk)
+        after = os.fstat(descriptor)
+        if (
+            total != before.st_size
+            or (
+                before.st_dev,
+                before.st_ino,
+                before.st_size,
+                before.st_mtime_ns,
+            )
+            != (
+                after.st_dev,
+                after.st_ino,
+                after.st_size,
+                after.st_mtime_ns,
+            )
+        ):
+            raise ValueError(code)
+        return digest.hexdigest()
+    except OSError as error:
+        raise ValueError(code) from error
+    finally:
+        os.close(descriptor)


 def _require_process(result: ProcessResult, code: str) -> None:
     if not result.ok:
         raise ValueError(code)


 def _read_engine_version(executable: str) -> str:
     result = run_bounded(
         [executable, "--version"],
         timeout_seconds=5,
         max_captured_bytes=64 * 1024,
     )
     _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")
     try:
         lines = result.stdout.decode("utf-8", errors="strict").splitlines()
     except UnicodeError as error:
         raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID") from error
     if not lines:
         raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
     version = lines[0].strip()
     if (
         not version
         or len(version) > 256
         or "/" in version
         or "\\" in version
         or any(ord(character) < 32 for character in version)
     ):
         raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
     return version


 def _normalize_audio(
     source: Path,
     destination: Path,
     *,
     ffmpeg_executable: str,
 ) -> None:
     result = run_bounded(
         [
             ffmpeg_executable,
             "-nostdin",
             "-hide_banner",
             "-loglevel",
             "error",
             "-n",
             "-i",
             str(source),
             "-map",
             "0:a:0",
             "-vn",
             "-ac",
             "1",
             "-ar",
             "16000",
             "-c:a",
             "pcm_s16le",
             "-f",
             "wav",
             str(destination),
         ],
         timeout_seconds=_AUDIO_TIMEOUT_SECONDS,
         max_captured_bytes=_PROCESS_CAPTURE_BYTES,
     )
     _require_process(result, "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED")


 def _inspect_normalized_audio(path: Path) -> tuple[int, bool]:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
+    try:
+        descriptor = os.open(path, flags)
+    except OSError as error:
+        raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID") from error
     try:
-        with wave.open(str(path), "rb") as audio:
+        before = os.fstat(descriptor)
+        if not stat.S_ISREG(before.st_mode):
+            raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
+        with os.fdopen(descriptor, "rb") as stream:
+            descriptor = -1
+            with wave.open(stream, "rb") as audio:
+                if (
+                    audio.getnchannels() != 1
+                    or audio.getsampwidth() != 2
+                    or audio.getframerate() != 16000
+                    or audio.getnframes() < 1
+                ):
+                    raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
+                frame_count = audio.getnframes()
+                silent = True
+                while frames := audio.readframes(64 * 1024):
+                    if any(frames):
+                        silent = False
+            after = os.fstat(stream.fileno())
             if (
-                audio.getnchannels() != 1
-                or audio.getsampwidth() != 2
-                or audio.getframerate() != 16000
-                or audio.getnframes() < 1
+                before.st_dev,
+                before.st_ino,
+                before.st_size,
+                before.st_mtime_ns,
+            ) != (
+                after.st_dev,
+                after.st_ino,
+                after.st_size,
+                after.st_mtime_ns,
             ):
                 raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
-            frame_count = audio.getnframes()
-            silent = True
-            while frames := audio.readframes(64 * 1024):
-                if any(frames):
-                    silent = False
     except (OSError, EOFError, wave.Error) as error:
         raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID") from error
+    finally:
+        if descriptor >= 0:
+            os.close(descriptor)
     duration_ms = (frame_count * 1000 + 15999) // 16000
     return duration_ms, silent


 def _run_whisper(
     audio_path: Path,
     *,
     model_path: Path,
     language: str,
     output_prefix: Path,
     whisper_executable: str,
 ) -> None:
     result = run_bounded(
         [
             whisper_executable,
             "--model",
             str(model_path),
             "--file",
             str(audio_path),
             "--language",
             language,
             "--temperature",
             "0",
             "--temperature-inc",
             "0",
             "--no-fallback",
             "--no-gpu",
             "--output-json-full",
             "--output-file",
             str(output_prefix),
             "--no-prints",
         ],
         timeout_seconds=_ENGINE_TIMEOUT_SECONDS,
         max_captured_bytes=_PROCESS_CAPTURE_BYTES,
     )
     _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")


 def _load_engine_json(path: Path) -> object:
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
+    flags |= getattr(os, "O_CLOEXEC", 0)
+    flags |= getattr(os, "O_NOFOLLOW", 0)
     try:
-        metadata = path.lstat()
+        descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error
-    if (
-        stat.S_ISLNK(metadata.st_mode)
-        or not stat.S_ISREG(metadata.st_mode)
-        or not 0 < metadata.st_size <= _ENGINE_JSON_LIMIT_BYTES
-    ):
-        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
     try:
-        with path.open("rb") as stream:
-            encoded = stream.read(_ENGINE_JSON_LIMIT_BYTES + 1)
-        if len(encoded) > _ENGINE_JSON_LIMIT_BYTES:
+        before = os.fstat(descriptor)
+        if not stat.S_ISREG(before.st_mode) or not (
+            0 < before.st_size <= _ENGINE_JSON_LIMIT_BYTES
+        ):
+            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
+        chunks: list[bytes] = []
+        remaining = _ENGINE_JSON_LIMIT_BYTES + 1
+        while remaining:
+            chunk = os.read(descriptor, min(_HASH_CHUNK_BYTES, remaining))
+            if not chunk:
+                break
+            chunks.append(chunk)
+            remaining -= len(chunk)
+        encoded = b"".join(chunks)
+        after = os.fstat(descriptor)
+        if (
+            len(encoded) != before.st_size
+            or len(encoded) > _ENGINE_JSON_LIMIT_BYTES
+            or (
+                before.st_dev,
+                before.st_ino,
+                before.st_size,
+                before.st_mtime_ns,
+            )
+            != (
+                after.st_dev,
+                after.st_ino,
+                after.st_size,
+                after.st_mtime_ns,
+            )
+        ):
             raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
+    except OSError as error:
+        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error
+    finally:
+        os.close(descriptor)
+    try:
         return json.loads(encoded.decode("utf-8", errors="strict"))
-    except (OSError, UnicodeError, json.JSONDecodeError) as error:
+    except (UnicodeError, json.JSONDecodeError) as error:
         raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error


 def _publish_transcript_bundle(output_path: Path, bundle: object) -> None:
     destination = require_absent_output(output_path)
     if not destination.parent.is_dir():
         raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     encoded = encode_transcript_bundle(bundle).encode("utf-8")
     descriptor, temporary_name = tempfile.mkstemp(
         prefix=f".{destination.name}.",
         suffix=".tmp",
         dir=destination.parent,
     )
     temporary_path = Path(temporary_name)
     try:
         with os.fdopen(descriptor, "wb") as stream:
             stream.write(encoded)
             stream.flush()
             os.fsync(stream.fileno())
         try:
             os.link(temporary_path, destination)
         except FileExistsError as error:
             raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
     finally:
         temporary_path.unlink(missing_ok=True)


 def transcribe_and_publish(
     media_paths: Sequence[Path],
     *,
     model_path: Path,
     language: str,
     output_path: Path,
     ffmpeg_executable: str = "ffmpeg",
     whisper_executable: str = "whisper-cli",
 ) -> dict[str, object]:
     """Transcribe local takes once and atomically publish one canonical bundle."""

     destination = require_absent_output(output_path)
     if not destination.parent.is_dir():
         raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
     if not media_paths:
         raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
     if not isinstance(language, str) or _LANGUAGE.fullmatch(language) is None:
         raise ValueError("TRITRACK_TRANSCRIPT_LANGUAGE_INVALID")

     media = tuple(Path(path) for path in media_paths)
     take_ids = [path.name for path in media]
     if len(take_ids) != len(set(take_ids)):
         raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")
     for path in media:
         _require_readable_file(path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE")
     selected_model = _require_readable_file(
         Path(model_path), "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
     )

     engine_version = _read_engine_version(whisper_executable)
-    model_sha256 = _sha256_file(selected_model)
-    source_hashes = {path: _sha256_file(path) for path in media}
+    model_sha256 = _sha256_file(
+        selected_model, "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
+    )
+    source_hashes = {
+        path: _sha256_file(path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE")
+        for path in media
+    }
     takes: list[TranscribedTake] = []
     with tempfile.TemporaryDirectory(prefix="tritrack-transcribe-") as temporary:
         scratch = Path(temporary)
         for index, source in enumerate(sorted(media, key=lambda path: path.name), start=1):
             audio_path = scratch / f"audio-{index:06d}.wav"
             output_prefix = scratch / f"whisper-{index:06d}"
             _normalize_audio(
                 source,
                 audio_path,
                 ffmpeg_executable=ffmpeg_executable,
             )
             duration_ms, silent = _inspect_normalized_audio(audio_path)
             _run_whisper(
                 audio_path,
                 model_path=selected_model,
                 language=language,
                 output_prefix=output_prefix,
                 whisper_executable=whisper_executable,
             )
             evidence = _load_engine_json(Path(f"{output_prefix}.json"))
             cues = canonicalize_whisper_evidence(
                 evidence,
                 requested_language=language,
                 audio_duration_ms=duration_ms,
                 proven_silence=silent,
             )
             if (
                 _sha256_file(source) != source_hashes[source]
                 or _sha256_file(selected_model) != model_sha256
             ):
                 raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")
             if silent and cues:
                 raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_TEXT_DETECTED")
             if not silent and not cues:
                 raise ValueError("TRITRACK_TRANSCRIPT_EMPTY_UNPROVEN")
             takes.append(
                 TranscribedTake(
                     take_id=source.name,
                     source_sha256=source_hashes[source],
                     status="empty" if silent else "completed",
                     cues=tuple(cues),
                 )
             )

     if _sha256_file(selected_model) != model_sha256 or any(
         _sha256_file(source) != source_hashes[source] for source in media
     ):
         raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")

     bundle = build_transcript_bundle(
         takes,
         language=language,
         model_sha256=model_sha256,
         engine_version=engine_version,
     )
     _publish_transcript_bundle(destination, bundle)
     return bundle
diff --git a/src/tritrack_editing_assistant/validate_artifacts.py b/src/tritrack_editing_assistant/validate_artifacts.py
index 1e9896e..28d8c82 100644
--- a/src/tritrack_editing_assistant/validate_artifacts.py
+++ b/src/tritrack_editing_assistant/validate_artifacts.py
@@ -1,108 +1,108 @@
 """Read-only, offline validation of public TriTrack artifacts."""

 from __future__ import annotations

 import hashlib
 import json
 import os
 import stat
 from dataclasses import dataclass
 from decimal import Decimal
 from pathlib import Path

 from jsonschema import ValidationError

 from . import __version__, contracts, doctor, emit_fcpxml, paper_edit, run_workflow

 MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024


 @dataclass(frozen=True)
 class LoadedValidationArtifact:
     path: Path
     encoded: bytes
     sha256: str


 def _read_regular_bytes(path: Path) -> bytes:
-    flags = os.O_RDONLY
+    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
     if hasattr(os, "O_NOFOLLOW"):
         flags |= os.O_NOFOLLOW
     try:
         descriptor = os.open(path, flags)
     except OSError as error:
         raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
     try:
         metadata = os.fstat(descriptor)
         if not stat.S_ISREG(metadata.st_mode):
             raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE")
         if not 0 < metadata.st_size <= MAX_VALIDATION_ARTIFACT_BYTES:
             raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
         with os.fdopen(descriptor, "rb") as stream:
             descriptor = -1
             encoded = stream.read(MAX_VALIDATION_ARTIFACT_BYTES + 1)
         if len(encoded) > MAX_VALIDATION_ARTIFACT_BYTES:
             raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
         return encoded
     except OSError as error:
         raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
     finally:
         if descriptor >= 0:
             os.close(descriptor)


 def _load_regular_artifact(path: Path) -> LoadedValidationArtifact:
     selected = Path(path)
     encoded = _read_regular_bytes(selected)
     return LoadedValidationArtifact(
         path=selected,
         encoded=encoded,
         sha256=hashlib.sha256(encoded).hexdigest(),
     )


 def _verify_unchanged(artifact: LoadedValidationArtifact) -> None:
     try:
         encoded = _read_regular_bytes(artifact.path)
     except ValueError as error:
         raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED") from error
     if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
         raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED")


 def _validation_summary(
     *,
     kind: str,
     scope: str,
     hashes: dict[str, str],
     counts: dict[str, int],
     details: dict[str, object],
 ) -> dict[str, object]:
     return {
         "schemaVersion": "tritrack.validate-summary/v1",
         "toolVersion": __version__,
         "artifactKind": kind,
         "validationScope": scope,
         "hashes": hashes,
         "counts": counts,
         "details": details,
     }


 def validate_contract_artifact(path: Path) -> dict[str, object]:
     """Validate one JSON file against its exact installed closed contract."""

     artifact = _load_regular_artifact(path)
     try:
         payload = json.loads(
             artifact.encoded.decode("utf-8", errors="strict"),
             parse_float=Decimal,
         )
     except (UnicodeError, json.JSONDecodeError) as error:
         raise ValueError("TRITRACK_VALIDATE_JSON_INVALID") from error
     try:
         schema_version = payload["schemaVersion"]
     except (KeyError, TypeError) as error:
         raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
     try:
         contract_name = contracts.contract_name_for_schema_version(schema_version)
diff --git a/tests/test_cli.py b/tests/test_cli.py
index 69a2be1..a11320c 100644
--- a/tests/test_cli.py
+++ b/tests/test_cli.py
@@ -27,160 +27,177 @@ def write_alignment_inputs(root: Path) -> tuple[Path, Path]:
             "name": "whisper-cli",
             "version": "whisper.cpp version: invented-cli",
         },
         "takes": [
             {
                 "takeId": "Invented.wav",
                 "sourceSha256": "a" * 64,
                 "status": "completed",
                 "cues": [
                     {
                         "cueId": "cue-000001",
                         "startMs": 0,
                         "endMs": 500,
                         "text": "Invented private source text.",
                     }
                 ],
             }
         ],
     }
     transcript_path = root / "transcript.json"
     transcript_path.write_text(
         json.dumps(transcript, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
         encoding="utf-8",
     )
     revision = {
         "schemaVersion": "tritrack.text-revision/v1",
         "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
         "language": "en",
         "takes": [
             {
                 "takeId": "Invented.wav",
                 "sourceSha256": "a" * 64,
                 "revisions": [
                     {
                         "cueId": "cue-000001",
                         "text": "Invented private revised text.",
                     }
                 ],
             }
         ],
     }
     revision_path = root / "revision.json"
     revision_path.write_text(
         json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
         encoding="utf-8",
     )
     return transcript_path, revision_path


 def write_hybrid_receipt(root: Path, transcript_path: Path) -> Path:
     receipt = {
         "schemaVersion": "tritrack.provider-receipt/v1",
         "provider": "gemini",
         "operation": "audio-transcription",
         "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
         "takeId": "Invented.wav",
         "requestedModel": "gemini-invented-exact",
         "observedModel": "gemini-invented-exact",
         "audioSha256": "a" * 64,
         "requestStatus": "completed",
         "responseStatus": 200,
         "upload": {
             "status": "completed",
             "serverFileIdSha256": "e" * 64,
         },
         "serverFileDeletion": {
             "attempted": True,
             "confirmed": True,
             "statusCode": 200,
         },
     }
     receipt_path = root / "receipt.json"
     receipt_path.write_text(
         json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
         encoding="utf-8",
     )
     return receipt_path


 class CliSmokeTest(unittest.TestCase):
+    @unittest.skipUnless(
+        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
+    )
+    def test_output_hash_rejects_special_files_before_blocking(self) -> None:
+        observed: list[int] = []
+
+        def reject_special(_path, flags, *_args):
+            observed.append(flags)
+            raise OSError("invented special file")
+
+        with mock.patch.object(
+            cli.os, "open", side_effect=reject_special
+        ), self.assertRaises(OSError):
+            cli._output_sha256(Path("invented-special-file"))
+        self.assertEqual(len(observed), 1)
+        self.assertTrue(observed[0] & os.O_NONBLOCK)
+
     def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
         completed = self.run_cli_unchecked(*args)
         completed.check_returncode()
         return completed

     def run_cli_unchecked(
         self,
         *args: str,
         environment_overrides: dict[str, str] | None = None,
     ) -> subprocess.CompletedProcess[str]:
         environment = os.environ.copy()
         environment["PYTHONPATH"] = str(ROOT / "src")
         if environment_overrides is not None:
             environment.update(environment_overrides)
         return subprocess.run(
             [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
             cwd=ROOT,
             env=environment,
             text=True,
             capture_output=True,
             check=False,
         )

     def test_version(self):
         completed = self.run_cli("--version")
         self.assertEqual(completed.stdout.strip(), "tritrack 0.1.0a0")

     def test_version_and_component_list(self):
         completed = self.run_cli("components", "--json")
         payload = json.loads(completed.stdout)

         self.assertEqual(payload["schemaVersion"], "tritrack.components/v1")
         self.assertEqual(len(payload["components"]), 11)
         self.assertEqual(
             [component["sourceComponent"] for component in payload["components"]],
             [
                 "sync_scan.py",
                 "emit_fcpxml.py",
                 "transcribe_takes.py",
                 "string_out.py",
                 "hallucination.py",
                 "organizer.py",
                 "paper_edit.py",
                 "align_text.py",
                 "gemini_hybrid.py",
                 "gemini_transcribe.mjs",
                 "multicam-sync",
             ],
         )
         self.assertEqual(
             {
                 component["sourceComponent"]: component["status"]
                 for component in payload["components"]
             },
             {
                 "sync_scan.py": "implemented",
                 "emit_fcpxml.py": "implemented",
                 "transcribe_takes.py": "implemented",
                 "string_out.py": "implemented",
                 "hallucination.py": "implemented",
                 "organizer.py": "implemented",
                 "paper_edit.py": "implemented",
                 "align_text.py": "implemented",
                 "gemini_hybrid.py": "implemented",
                 "gemini_transcribe.mjs": "planned",
                 "multicam-sync": "implemented",
             },
         )

     def test_help_exposes_the_complete_scaffold(self):
         completed = self.run_cli("--help")
         for command in (
             "components",
             "doctor",
             "sync",
             "transcribe",
             "align",
             "hybrid",
             "emit",
             "validate",
diff --git a/tests/test_emit_fcpxml.py b/tests/test_emit_fcpxml.py
index e214dce..9566745 100644
--- a/tests/test_emit_fcpxml.py
+++ b/tests/test_emit_fcpxml.py
@@ -287,83 +287,122 @@ class FcpxmlRenderingTest(unittest.TestCase):
             with (
                 mock.patch.object(sync_scan, "probe_media") as probe,
                 self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
             ):
                 module.emit_and_publish(
                     [sync_scan.MediaSource("A.MP4", root_path / "missing-a")],
                     [sync_scan.MediaSource("B.MP4", root_path / "missing-b")],
                     sync_map_path=root_path / "missing-sync-map.json",
                     profile_id="uhd-2997-ndf-fcpxml-1.14",
                     binding_id="basic-title-v1",
                     metadata=module.ProjectMetadata("Event", "Project"),
                     output_path=output,
                 )
             probe.assert_not_called()
             self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

     def test_source_probe_must_match_the_closed_public_profile(self) -> None:
         module = self.module()
         profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
         with tempfile.TemporaryDirectory() as temporary:
             root_path = Path(temporary)
             source_a = sync_scan.MediaSource("A-001.MP4", root_path / "A-001.MP4")
             source_b = sync_scan.MediaSource("B-001.MP4", root_path / "B-001.MP4")
             before = copy.deepcopy((source_a, source_b, profile))

             probes = [compatible_probe("A-001.MP4"), compatible_probe("B-001.MP4")]
             with mock.patch.object(sync_scan, "probe_media", side_effect=probes):
                 normalized = module._probe_sources(
                     [source_a],
                     [source_b],
                     profile=profile,
                 )

             self.assertEqual([item["camera"] for item in normalized], ["A", "B"])
             self.assertEqual((source_a, source_b, profile), before)

             mismatches = {
                 "width": 1920,
                 "frameRate": "25/1",
                 "colorSpace": None,
                 "sampleRate": "44100",
                 "channels": 1,
                 "audioStreamCount": 0,
             }
             for field, value in mismatches.items():
                 with self.subTest(field=field):
                     changed = compatible_probe("A-001.MP4")
                     changed["compatibility"][field] = value
                     with (
                         mock.patch.object(
                             sync_scan,
                             "probe_media",
                             return_value=changed,
                         ),
                         self.assertRaisesRegex(
                             ValueError,
                             "TRITRACK_EMIT_SOURCE_PROFILE_MISMATCH",
                         ),
                     ):
                         module._probe_sources([source_a], [], profile=profile)

     def test_sync_map_loader_preserves_decimal_timing_and_rejects_drift(self):
         module = self.module()
         with tempfile.TemporaryDirectory() as temporary:
             source = Path(temporary) / "sync-map.json"
             source.write_text(
                 json.dumps(sync_payload(), default=float),
                 encoding="utf-8",
             )
             loaded = module.load_sync_map(source)
             self.assertIsInstance(
                 loaded["pairs"][0]["offsetBFromASeconds"],
                 Decimal,
             )
             changed = sync_payload()
             changed["schemaVersion"] = "tritrack.sync-map/v2"
             source.write_text(json.dumps(changed, default=float), encoding="utf-8")
             with self.assertRaisesRegex(ValueError, "TRITRACK_EMIT_SYNC_MAP_INVALID"):
                 module.load_sync_map(source)

+    def test_sync_map_loader_does_not_use_unbounded_path_read(self) -> None:
+        module = self.module()
+        with tempfile.TemporaryDirectory() as temporary:
+            source = Path(temporary) / "sync-map.json"
+            source.write_text(
+                json.dumps(sync_payload(), default=float),
+                encoding="utf-8",
+            )
+
+            with mock.patch.object(
+                Path,
+                "read_bytes",
+                side_effect=AssertionError("unbounded Path.read_bytes used"),
+            ):
+                loaded = module.load_sync_map(source)
+
+            self.assertEqual(loaded["schemaVersion"], "tritrack.sync-map/v1")
+
+    def test_sync_map_loader_rejects_symlink_and_oversized_file(self) -> None:
+        module = self.module()
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            source = root / "sync-map.json"
+            source.write_text(
+                json.dumps(sync_payload(), default=float),
+                encoding="utf-8",
+            )
+            linked = root / "linked.json"
+            linked.symlink_to(source)
+            oversized = root / "oversized.json"
+            with oversized.open("wb") as stream:
+                stream.truncate(module.MAX_SYNC_MAP_BYTES + 1)
+
+            for candidate in (linked, oversized):
+                with self.subTest(candidate=candidate.name), self.assertRaisesRegex(
+                    ValueError, "^TRITRACK_EMIT_SYNC_MAP_INVALID$"
+                ):
+                    module.load_sync_map(candidate)
+

 if __name__ == "__main__":
     unittest.main()
diff --git a/tests/test_packaging.py b/tests/test_packaging.py
index bf55250..e3ba324 100644
--- a/tests/test_packaging.py
+++ b/tests/test_packaging.py
@@ -6,162 +6,163 @@ import hashlib
 import json
 import os
 import shutil
 import subprocess
 import sys
 import tarfile
 import tempfile
 import tomllib
 import unittest
 import zipfile
 from pathlib import Path

 import jsonschema

 from scripts import release_gate_core

 ROOT = Path(__file__).resolve().parents[1]
 POLICY_PATH = ROOT / "release" / "package-policy-v1.json"
 MANIFEST_SCHEMA_PATH = ROOT / "release" / "release-manifest-v1.schema.json"
 SDIST_ROOT = "tritrack_editing_assistant-0.1.0a0/"


 def normalized_inventory(entries: dict[str, bytes]) -> str:
     digest = hashlib.sha256()
     for name in sorted(entries):
         encoded = entries[name]
         digest.update(name.encode("utf-8"))
         digest.update(b"\0")
         digest.update(str(len(encoded)).encode("ascii"))
         digest.update(b"\0")
         digest.update(hashlib.sha256(encoded).hexdigest().encode("ascii"))
         digest.update(b"\n")
     return digest.hexdigest()


 class PackagingPolicyTest(unittest.TestCase):
     def test_01_python_and_tool_constraints_are_exact(self) -> None:
         configuration = tomllib.loads((ROOT / "pyproject.toml").read_text())
         self.assertEqual(
             configuration["build-system"]["requires"],
             ["setuptools==84.0.0"],
         )
         self.assertEqual(configuration["project"]["requires-python"], ">=3.12,<3.14")
         self.assertEqual(
             configuration["project"]["optional-dependencies"]["dev"],
             ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"],
         )
         classifiers = configuration["project"]["classifiers"]
         versions = [
             value
             for value in classifiers
             if value.startswith("Programming Language :: Python :: 3.")
         ]
         self.assertEqual(
             versions,
             [
                 "Programming Language :: Python :: 3.12",
                 "Programming Language :: Python :: 3.13",
             ],
         )
         self.assertEqual(
             (ROOT / "requirements" / "ci-constraints.txt")
             .read_text(encoding="utf-8")
             .splitlines(),
             [
                 "build==1.5.0",
                 "packaging==26.3",
                 "pip==26.2",
                 "pyproject-hooks==1.2.0",
                 "ruff==0.16.2",
                 "setuptools==84.0.0",
                 "wheel==0.48.0",
             ],
         )

     def test_02_package_policy_and_manifest_schema_are_closed(self) -> None:
         policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
         self.assertEqual(policy["schemaVersion"], "tritrack.package-policy/v1")
         self.assertEqual(
             set(policy),
-            {"schemaVersion", "limits", "source", "wheel", "sdist"},
+            {"schemaVersion", "build", "limits", "source", "wheel", "sdist"},
         )
+        self.assertEqual(policy["build"], {"sourceDateEpoch": 1704067200})
         for required in (
             "docs/TASK-11-VERIFICATION.md",
             "scripts/release_gate.py",
             "scripts/release_gate_core.py",
         ):
             self.assertIn(required, policy["sdist"]["expectedMembers"])
         schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
         jsonschema.Draft202012Validator.check_schema(schema)
         sample = {
             "schemaVersion": "tritrack.release-manifest/v1",
             "project": {
                 "name": "tritrack-editing-assistant",
                 "version": "0.1.0a0",
                 "commit": "a" * 40,
             },
             "sourceInventory": {"count": 1, "sha256": "b" * 64},
             "toolchain": {
                 "python": "3.13.15",
                 "implementation": "CPython",
                 "pip": "26.2",
                 "build": "1.5.0",
                 "setuptools": "84.0.0",
                 "wheel": "0.48.0",
             },
             "platform": {"system": "Darwin", "machine": "arm64"},
             "artifacts": {
                 kind: {
                     "sha256": value * 64,
                     "sizeBytes": 1,
                     "memberCount": 1,
                     "memberInventorySha256": value * 64,
                 }
                 for kind, value in (("wheel", "c"), ("sdist", "d"))
             },
             "reproducibility": {
                 "wheelBytesMatch": True,
                 "sdistMembersMatch": True,
             },
             "gates": {
                 name: "pass"
                 for name in (
                     "sourceIdentity",
                     "sourcePrivacy",
                     "wheelArchive",
                     "sdistArchive",
                     "freshInstall",
                 )
             },
             "nonClaims": ["no-tag", "no-package-publication"],
         }
         jsonschema.validate(sample, schema)
         sample["unexpected"] = True
         with self.assertRaises(jsonschema.ValidationError):
             jsonschema.validate(sample, schema)

     def test_03_distribution_members_are_explicit_and_reproducible(self) -> None:
         policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             distributions: list[tuple[Path, Path]] = []
             for label in ("first", "second"):
                 source = root / label / "source"
                 shutil.copytree(
                     ROOT,
                     source,
                     ignore=shutil.ignore_patterns(
                         ".git",
                         ".release-evidence",
                         "__pycache__",
                         "*.egg-info",
                         "build",
                         "dist",
                     ),
                 )
                 output = root / label / "dist"
                 output.mkdir()
                 environment = os.environ.copy()
                 environment["SOURCE_DATE_EPOCH"] = "1704067200"
                 subprocess.run(
                     [
diff --git a/tests/test_release_gate.py b/tests/test_release_gate.py
index 2f90586..5c6bf3b 100644
--- a/tests/test_release_gate.py
+++ b/tests/test_release_gate.py
@@ -1,184 +1,223 @@
 """Task 11 maintainer release-gate tests."""

 from __future__ import annotations

 import contextlib
 import hashlib
 import importlib
 import io
 import json
 import os
 import stat
 import subprocess
 import tarfile
 import tempfile
 import unittest
 import warnings
 import zipfile
 from pathlib import Path
 from unittest import mock

 from scripts import release_gate_core


 def _policy(*, wheel: list[str] | None = None, sdist: list[str] | None = None):
     return {
         "schemaVersion": "tritrack.package-policy/v1",
+        "build": {"sourceDateEpoch": 1704067200},
         "limits": {
             "sourceMaxFiles": 32,
             "sourceMaxFileBytes": 4096,
             "sourceMaxTotalBytes": 32768,
             "archiveMaxBytes": 65536,
             "archiveMaxMembers": 32,
             "memberMaxBytes": 4096,
             "expandedMaxBytes": 32768,
         },
         "source": {
             "allowedFakeHomeUsers": ["editor", "example", "fake", "test"],
             "allowedFakeSecretValues": [
                 "example",
                 "fake",
                 "placeholder",
                 "redacted",
                 "secret",
                 "test",
             ],
             "forbiddenSuffixes": [".mov", ".xlsx"],
         },
         "wheel": {"expectedMembers": wheel or ["demo.py"]},
         "sdist": {
             "root": "demo-1.0/",
             "expectedMembers": sdist or ["README.md"],
         },
     }


 def _run(*argv: str, cwd: Path, input_bytes: bytes | None = None) -> bytes:
     return subprocess.run(
         argv,
         cwd=cwd,
         input=input_bytes,
         check=True,
         capture_output=True,
     ).stdout


 def _make_repo(root: Path, files: dict[str, bytes] | None = None) -> None:
     (root / "release").mkdir(parents=True)
     (root / "release" / "package-policy-v1.json").write_text(
         json.dumps(_policy()), encoding="utf-8"
     )
     for name, encoded in (files or {"public.txt": b"public\n"}).items():
         path = root / name
         path.parent.mkdir(parents=True, exist_ok=True)
         path.write_bytes(encoded)
     _run("git", "init", "-q", cwd=root)
     _run("git", "config", "user.name", "Invented Tester", cwd=root)
     _run("git", "config", "user.email", "test@example.invalid", cwd=root)
     _run("git", "add", ".", cwd=root)
     _run("git", "commit", "-qm", "fixture", cwd=root)


 def _zip(path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]) -> None:
     with (
         zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive,
         warnings.catch_warnings(),
     ):
         warnings.simplefilter("ignore", UserWarning)
         for name, encoded in entries:
             archive.writestr(name, encoded)


 def _tar(
     path: Path,
     entries: list[tuple[tarfile.TarInfo | str, bytes]],
 ) -> None:
     with tarfile.open(path, "w:gz") as archive:
         for name, encoded in entries:
             member = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
             if member.isreg():
                 member.size = len(encoded)
             archive.addfile(member, io.BytesIO(encoded) if member.isreg() else None)


 class SourceGateTest(unittest.TestCase):
+    def test_package_policy_owns_a_fixed_build_epoch(self) -> None:
+        self.assertEqual(release_gate_core._build_epoch(_policy()), 1704067200)
+        for invalid in (True, 0, -1, "1704067200"):
+            policy = _policy()
+            policy["build"]["sourceDateEpoch"] = invalid
+            with self.subTest(invalid=invalid), self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError,
+                "^TRITRACK_RELEASE_POLICY_INVALID$",
+            ):
+                release_gate_core._build_epoch(policy)
+
+    @unittest.skipUnless(
+        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
+    )
+    def test_gate_descriptor_readers_reject_special_files_before_blocking(self) -> None:
+        selected = Path("invented-special-file")
+        readers = (
+            lambda: release_gate_core._read_regular(selected, 1),
+            lambda: release_gate_core._read_archive_bytes(selected, _policy()),
+            lambda: release_gate_core._verify_published_archive(
+                selected, (1, "a" * 64)
+            ),
+        )
+
+        for reader in readers:
+            observed: list[int] = []
+
+            def reject_special(_path, flags, *_args, observed=observed):
+                observed.append(flags)
+                raise OSError("invented special file")
+
+            with self.subTest(reader=reader), mock.patch.object(
+                release_gate_core.os, "open", side_effect=reject_special
+            ), self.assertRaises(release_gate_core.ReleaseGateError):
+                reader()
+            self.assertEqual(len(observed), 1)
+            self.assertTrue(observed[0] & os.O_NONBLOCK)
+
     def test_clean_stage_zero_regular_source_is_inventory_bound(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             _make_repo(root)
             first = release_gate_core.inventory_tracked_source(root)
             second = release_gate_core.inventory_tracked_source(root)
         self.assertEqual(first, second)
         self.assertEqual(first.count, 2)
         self.assertEqual(len(first.sha256), 64)
         self.assertGreater(first.total_bytes, 0)

     def test_dirty_source_and_tracked_links_fail_closed(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             _make_repo(root)
             (root / "public.txt").write_text("changed\n", encoding="utf-8")
             with self.assertRaisesRegex(
                 release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_DIRTY$"
             ):
                 release_gate_core.inventory_tracked_source(root)

         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             _make_repo(root)
             (root / "public.txt").unlink()
             os.symlink("target", root / "public.txt")
             _run("git", "add", "public.txt", cwd=root)
             _run("git", "commit", "-qm", "link", cwd=root)
             with self.assertRaisesRegex(
                 release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
             ):
                 release_gate_core.inventory_tracked_source(root)

     def test_submodule_unmerged_and_late_change_fail_closed(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             _make_repo(root)
             head = _run("git", "rev-parse", "HEAD", cwd=root).strip().decode()
             _run(
                 "git",
                 "update-index",
                 "--add",
                 "--cacheinfo",
                 f"160000,{head},nested",
                 cwd=root,
             )
             _run("git", "commit", "-qm", "gitlink", cwd=root)
             with self.assertRaisesRegex(
                 release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
             ):
                 release_gate_core.inventory_tracked_source(root)

         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             _make_repo(root)
             original = release_gate_core._read_regular
             changed = False

             def mutate(path: Path, limit: int) -> bytes:
                 nonlocal changed
                 encoded = original(path, limit)
                 if path.name == "public.txt" and not changed:
                     changed = True
                     path.write_text("late change\n", encoding="utf-8")
                 return encoded

             with (
                 mock.patch.object(
                     release_gate_core, "_read_regular", side_effect=mutate
                 ),
                 self.assertRaisesRegex(
                     release_gate_core.ReleaseGateError,
                     "^TRITRACK_RELEASE_SOURCE_CHANGED$",
                 ),
             ):
                 release_gate_core.inventory_tracked_source(root)

     def test_source_bounds_and_forbidden_suffix_are_enforced(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
@@ -311,160 +350,180 @@ class ArchiveGateTest(unittest.TestCase):
         link = tarfile.TarInfo("demo-1.0/README.md")
         link.type = tarfile.SYMTYPE
         link.linkname = "target"
         fixtures = (
             ([("other/README.md", b"x")], _policy(sdist=["README.md"])),
             ([(link, b"")], _policy()),
             (
                 [("demo-1.0/README.md", b"x"), ("demo-1.0/extra", b"x")],
                 _policy(),
             ),
         )
         for entries, policy in fixtures:
             with self.subTest(), tempfile.TemporaryDirectory() as temporary:
                 path = Path(temporary) / "bad.tar.gz"
                 _tar(path, list(entries))
                 with self.assertRaises(release_gate_core.ReleaseGateError):
                     release_gate_core.inspect_sdist(path, policy)

     def test_archive_bounds_privacy_and_inventory_mode_binding(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             path = root / "large.whl"
             _zip(path, [("demo.py", b"x" * 5000)])
             with self.assertRaisesRegex(
                 release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_LIMIT$"
             ):
                 release_gate_core.inspect_wheel(path, _policy())

             private_home = b"/" + b"home" + b"/real-person/private"
             _zip(path, [("demo.py", private_home)])
             with self.assertRaisesRegex(
                 release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_PRIVATE_PATH$"
             ):
                 release_gate_core.inspect_wheel(path, _policy())

             executable = zipfile.ZipInfo("demo.py")
             executable.create_system = 3
             executable.external_attr = (stat.S_IFREG | 0o755) << 16
             _zip(path, [(executable, b"public\n")])
             first = release_gate_core.inspect_wheel(path, _policy())
             regular = zipfile.ZipInfo("demo.py")
             regular.create_system = 3
             regular.external_attr = (stat.S_IFREG | 0o644) << 16
             _zip(path, [(regular, b"public\n")])
             second = release_gate_core.inspect_wheel(path, _policy())
             self.assertNotEqual(
                 first.member_inventory_sha256,
                 second.member_inventory_sha256,
             )

     def test_archive_hash_is_bound_to_the_same_bounded_bytes_as_inspection(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             path = root / "demo.whl"
             replacement = root / "replacement.whl"
             _zip(path, [("demo.py", b"public\n")])
             original = path.read_bytes()
             replaced = False

             def replace_after_member_read(_encoded: bytes) -> None:
                 nonlocal replaced
                 if replaced:
                     return
                 replaced = True
                 replacement.write_bytes(b"x" * 70000)
                 os.replace(replacement, path)

             with mock.patch.object(
                 release_gate_core,
                 "scan_public_bytes",
                 side_effect=replace_after_member_read,
             ):
                 result = release_gate_core.inspect_wheel(path, _policy())

             self.assertTrue(replaced)
             self.assertEqual(result.size_bytes, len(original))
             self.assertEqual(result.sha256, hashlib.sha256(original).hexdigest())


 class OrchestrationTest(unittest.TestCase):
+    def test_command_output_limit_terminates_before_timeout(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            command = [
+                os.fspath(Path(os.sys.executable)),
+                "-c",
+                "import os,time; os.write(1,b'x'*65); time.sleep(2)",
+            ]
+            with self.assertRaisesRegex(
+                release_gate_core.ReleaseGateError,
+                "^TRITRACK_RELEASE_COMMAND_LIMIT$",
+            ):
+                release_gate_core._run_command(
+                    command,
+                    cwd=root,
+                    env={"PATH": os.defpath},
+                    timeout=1,
+                    output_limit=64,
+                )
+
     def test_build_uses_fixed_epoch_and_exact_local_toolchain(self) -> None:
         calls: list[tuple[str, ...]] = []
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             snapshot = root / "snapshot"
             snapshot.mkdir()
             output = root / "dist"

             def fake_command(argv, **_kwargs):
                 calls.append(tuple(str(value) for value in argv))
                 output.mkdir(exist_ok=True)
                 (output / "demo-1.0-py3-none-any.whl").write_bytes(b"wheel")
                 (output / "demo-1.0.tar.gz").write_bytes(b"sdist")
                 return b""

             with (
                 mock.patch.object(
                     release_gate_core,
                     "_installed_tool_versions",
                     return_value={
                         "pip": "26.2",
                         "build": "1.5.0",
                         "setuptools": "84.0.0",
                         "wheel": "0.48.0",
                     },
                 ),
                 mock.patch.object(
                     release_gate_core, "_run_command", side_effect=fake_command
                 ),
             ):
                 wheel, sdist = release_gate_core.build_distributions(
                     snapshot, output, epoch=1704067200
                 )

         self.assertEqual(wheel.name, "demo-1.0-py3-none-any.whl")
         self.assertEqual(sdist.name, "demo-1.0.tar.gz")
         self.assertEqual(
             calls,
             [
                 (
                     os.fspath(Path(os.sys.executable)),
                     "-m",
                     "build",
                     "--no-isolation",
                     "--outdir",
                     os.fspath(output),
                 )
             ],
         )

     def test_fresh_install_uses_only_local_wheel_and_smokes_all_help(self) -> None:
         calls: list[tuple[str, ...]] = []
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
             wheel.write_bytes(b"invented wheel")

             def fake_command(argv, **_kwargs):
                 normalized = tuple(str(value) for value in argv)
                 calls.append(normalized)
                 if normalized[-2:] == ("components", "--json"):
                     return json.dumps(
                         {
                             "schemaVersion": "tritrack.components/v1",
                             "components": [{}] * 11,
                         }
                     ).encode()
                 if "importlib.metadata" in " ".join(normalized):
                     return b"tritrack-editing-assistant\t0.1.0a0\n"
                 return b""

             with (
                 mock.patch.object(
                     release_gate_core,
                     "_wheel_project_identity",
                     return_value=("tritrack-editing-assistant", "0.1.0a0"),
                 ),
                 mock.patch.object(
                     release_gate_core, "_run_command", side_effect=fake_command
                 ),
diff --git a/tests/test_title_binding.py b/tests/test_title_binding.py
index 9968933..f85e6bc 100644
--- a/tests/test_title_binding.py
+++ b/tests/test_title_binding.py
@@ -1,122 +1,163 @@
 """Task 4 tests for packaged public profiles and Basic Title capture."""

 from __future__ import annotations

 import importlib.util
 import json
+import os
+import subprocess
 import tempfile
 import unittest
 from pathlib import Path

 from tritrack_editing_assistant import doctor

 SCRIPT = Path(__file__).parents[1] / "scripts" / "capture_basic_title_binding.py"


 def load_capture_module():
     spec = importlib.util.spec_from_file_location("capture_basic_title_binding", SCRIPT)
     if spec is None or spec.loader is None:
         raise RuntimeError("capture script loader unavailable")
     module = importlib.util.module_from_spec(spec)
     spec.loader.exec_module(module)
     return module


 SAFE_FCPXML = """<?xml version="1.0" encoding="UTF-8"?>
 <!DOCTYPE fcpxml>
 <fcpxml version="1.14">
   <resources>
     <effect id="r2" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>
     <format id="r1" name="FFVideoFormat3840x2160p2997" frameDuration="1001/30000s" width="3840" height="2160" colorSpace="1-1-1 (Rec. 709)"/>
   </resources>
   <library><event name="Invented"><project name="Invented Basic Title"><sequence format="r1" duration="3003/30000s" tcFormat="NDF"><spine>
     <title name="Invented subtitle" ref="r2" offset="0s" start="0s" duration="3003/30000s">
       <text><text-style ref="ts1">Invented subtitle</text-style></text>
       <text-style-def id="ts1"><text-style font="Helvetica" fontSize="72" fontFace="Regular" fontColor="1 1 1 1" alignment="center"/></text-style-def>
     </title>
   </spine></sequence></project></event></library>
 </fcpxml>
 """


 class TitleBindingTest(unittest.TestCase):
+    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
+    def test_capture_inputs_reject_fifos_without_waiting_for_a_writer(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            root = Path(temporary)
+            fifo = root / "input"
+            os.mkfifo(fifo)
+            cases = (
+                ("--input", os.fspath(fifo)),
+                ("--binding", os.fspath(fifo), "--text", "Invented title"),
+            )
+            for index, arguments in enumerate(cases):
+                with self.subTest(arguments=arguments):
+                    completed = subprocess.run(
+                        [
+                            os.fspath(Path(os.sys.executable)),
+                            os.fspath(SCRIPT),
+                            *arguments,
+                            "--output",
+                            os.fspath(root / f"output-{index}"),
+                        ],
+                        check=False,
+                        capture_output=True,
+                        text=True,
+                        timeout=3,
+                    )
+                    self.assertNotEqual(completed.returncode, 0)
+                    self.assertIn("TRITRACK_TITLE_BINDING_", completed.stderr)
+
+    def test_capture_rejects_oversized_xml_before_parsing(self) -> None:
+        capture = load_capture_module()
+        with tempfile.TemporaryDirectory() as temporary:
+            source = Path(temporary) / "oversized.fcpxml"
+            with source.open("wb") as stream:
+                stream.truncate(16 * 1024 * 1024 + 1)
+            with self.assertRaisesRegex(
+                ValueError, "TRITRACK_TITLE_BINDING_INVALID_XML"
+            ):
+                capture.capture_binding(source)
+
     def test_packaged_compatibility_profile_has_exact_alpha_values(self) -> None:
         profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
         self.assertEqual(profile["schemaVersion"], "tritrack.compatibility-profile/v1")
         self.assertEqual(profile["frameDuration"], "1001/30000s")
         self.assertEqual((profile["width"], profile["height"]), (3840, 2160))
         self.assertEqual(profile["timecodeFormat"], "NDF")
         self.assertEqual(profile["audioRate"], 48000)

     def test_packaged_basic_title_binding_validates(self) -> None:
         binding = doctor.load_title_binding("basic-title-v1")
         self.assertEqual(binding["schemaVersion"], "tritrack.title-binding/v1")
         self.assertEqual(binding["effectName"], "Basic Title")
         self.assertTrue(binding["effectUid"].endswith("Basic Title.moti"))

     def test_capture_extracts_only_public_effect_and_style_values(self) -> None:
         capture = load_capture_module()
         with tempfile.TemporaryDirectory() as temporary:
             source = Path(temporary) / "invented.fcpxml"
             source.write_text(SAFE_FCPXML, encoding="utf-8")

             binding = capture.capture_binding(source)

         self.assertEqual(binding["effectName"], "Basic Title")
         self.assertEqual(
             {parameter["name"] for parameter in binding["parameters"]},
             {"alignment", "font", "fontColor", "fontFace", "fontSize"},
         )
         self.assertNotIn("Invented subtitle", json.dumps(binding))

     def test_capture_rejects_doctype_subsets_and_entities(self) -> None:
         capture = load_capture_module()
         source_xml = SAFE_FCPXML.replace(
             "<!DOCTYPE fcpxml>",
             '<!DOCTYPE fcpxml [<!ENTITY private SYSTEM "file:///etc/passwd">]>',
         )
         with tempfile.TemporaryDirectory() as temporary:
             source = Path(temporary) / "entity.fcpxml"
             source.write_text(source_xml, encoding="utf-8")
             with self.assertRaisesRegex(
                 ValueError, "TRITRACK_TITLE_BINDING_INVALID_XML"
             ):
                 capture.capture_binding(source)

     def test_rendered_basic_title_roundtrips_through_public_binding(self) -> None:
         capture = load_capture_module()
         binding = doctor.load_title_binding("basic-title-v1")
         rendered = capture.render_basic_title_fcpxml(
             binding,
             text="TRITRACK GENERATED BASIC TITLE",
         )

         self.assertIn('<fcpxml version="1.14">', rendered)
         self.assertIn('frameDuration="1001/30000s"', rendered)
         self.assertIn('tcFormat="NDF"', rendered)
         self.assertIn('duration="180180/30000s"', rendered)
         self.assertEqual(rendered.count('duration="90090/30000s"'), 2)
         self.assertIn('offset="90090/30000s"', rendered)
         self.assertNotIn('duration="3s"', rendered)
         self.assertNotIn("src=", rendered)

         with tempfile.TemporaryDirectory() as temporary:
             source = Path(temporary) / "generated.fcpxml"
             source.write_text(rendered, encoding="utf-8")
             recaptured = capture.capture_binding(source)

         self.assertEqual(recaptured, binding)

     def test_capture_rejects_private_title_font_path_and_template(self) -> None:
         capture = load_capture_module()
         forbidden_variants = (
             SAFE_FCPXML.replace("Basic Title", "Artlist LT", 1),
             SAFE_FCPXML.replace("Helvetica", "江城知音体"),
             SAFE_FCPXML.replace(
                 ".../Titles.localized",
                 "/Users/editor/Movies/Motion Templates/Titles.localized",
             ),
             SAFE_FCPXML.replace(
                 '<title name="Invented subtitle"',
                 '<title src="relative/private.mov" name="Invented subtitle"',
             ),
diff --git a/tests/test_transcribe_takes.py b/tests/test_transcribe_takes.py
index 715f52e..7428754 100644
--- a/tests/test_transcribe_takes.py
+++ b/tests/test_transcribe_takes.py
@@ -1,90 +1,93 @@
 """Task 7 tests for local transcript evidence canonicalization."""

 from __future__ import annotations

 import hashlib
 import json
+import os
+import subprocess
 import tempfile
 import textwrap
 import unittest
 from pathlib import Path
+from unittest import mock

 from tritrack_editing_assistant import contracts, transcribe_takes


 class TranscriptCanonicalizationTest(unittest.TestCase):
     def evidence(self) -> dict[str, object]:
         return {
             "result": {"language": "zh"},
             "transcription": [
                 {
                     "offsets": {"from": 125, "to": 900},
                     "text": "  第一個 invented cue。 ",
                     "tokens": [{"id": 1}],
                 },
                 {
                     "offsets": {"from": 900, "to": 1500},
                     "text": "Cafe\u0301  cue",
                 },
             ],
             "systeminfo": "ignored engine detail",
         }

     def test_canonicalizes_supported_whisper_evidence(self) -> None:
         cues = transcribe_takes.canonicalize_whisper_evidence(
             self.evidence(),
             requested_language="zh",
             audio_duration_ms=2000,
         )

         self.assertEqual(
             cues,
             [
                 {
                     "cueId": "cue-000001",
                     "startMs": 125,
                     "endMs": 900,
                     "text": "第一個 invented cue。",
                 },
                 {
                     "cueId": "cue-000002",
                     "startMs": 900,
                     "endMs": 1500,
                     "text": "Café cue",
                 },
             ],
         )

     def test_rejects_language_mismatch_and_invalid_timing(self) -> None:
         cases = []

         wrong_language = self.evidence()
         wrong_language["result"] = {"language": "en"}
         cases.append(wrong_language)

         overlapping = self.evidence()
         transcription = overlapping["transcription"]
         assert isinstance(transcription, list)
         second = transcription[1]
         assert isinstance(second, dict)
         second["offsets"] = {"from": 899, "to": 1500}
         cases.append(overlapping)

         bool_offset = self.evidence()
         transcription = bool_offset["transcription"]
         assert isinstance(transcription, list)
         first = transcription[0]
         assert isinstance(first, dict)
         first["offsets"] = {"from": False, "to": 900}
         cases.append(bool_offset)

         beyond_audio = self.evidence()
         transcription = beyond_audio["transcription"]
         assert isinstance(transcription, list)
         second = transcription[1]
         assert isinstance(second, dict)
         second["offsets"] = {"from": 2000, "to": 2001}
         cases.append(beyond_audio)

         for payload in cases:
             with self.subTest(payload=payload), self.assertRaisesRegex(
@@ -146,160 +149,210 @@ class TranscriptCanonicalizationTest(unittest.TestCase):
             [],
         )
         with self.assertRaisesRegex(
             ValueError, "TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID"
         ):
             transcribe_takes.canonicalize_whisper_evidence(
                 evidence,
                 requested_language="en",
                 audio_duration_ms=2000,
             )

     def test_builds_strict_stably_sorted_bundle_and_bytes(self) -> None:
         take_a = transcribe_takes.TranscribedTake(
             take_id="A-001.MP4",
             source_sha256="a" * 64,
             status="completed",
             cues=(
                 {
                     "cueId": "cue-000001",
                     "startMs": 0,
                     "endMs": 500,
                     "text": "Invented A cue.",
                 },
             ),
         )
         take_b = transcribe_takes.TranscribedTake(
             take_id="B-001.MP4",
             source_sha256="b" * 64,
             status="empty",
             cues=(),
         )

         first = transcribe_takes.build_transcript_bundle(
             [take_b, take_a],
             language="zh",
             model_sha256="f" * 64,
             engine_version="whisper.cpp version: 1.9.1",
         )
         second = transcribe_takes.build_transcript_bundle(
             [take_a, take_b],
             language="zh",
             model_sha256="f" * 64,
             engine_version="whisper.cpp version: 1.9.1",
         )

         contracts.validate_contract("transcript-bundle-v1", first)
         self.assertEqual(first, second)
         self.assertEqual(first["profileId"], "whisper-cpp-cpu-no-fallback-v1")
         self.assertEqual(
             [take["takeId"] for take in first["takes"]],
             ["A-001.MP4", "B-001.MP4"],
         )
         self.assertEqual(
             transcribe_takes.encode_transcript_bundle(first),
             transcribe_takes.encode_transcript_bundle(second),
         )
         self.assertEqual(
             json.loads(transcribe_takes.encode_transcript_bundle(first)), first
         )

     def test_bundle_rejects_duplicate_take_ids(self) -> None:
         take = transcribe_takes.TranscribedTake(
             take_id="A-001.MP4",
             source_sha256="a" * 64,
             status="empty",
             cues=(),
         )

         with self.assertRaisesRegex(
             ValueError, "TRITRACK_TRANSCRIPT_DUPLICATE_TAKE"
         ):
             transcribe_takes.build_transcript_bundle(
                 [take, take],
                 language="zh",
                 model_sha256="f" * 64,
                 engine_version="whisper.cpp version: 1.9.1",
             )


 class LocalTranscriptionWorkflowTest(unittest.TestCase):
+    @unittest.skipUnless(
+        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
+    )
+    def test_descriptor_input_readers_reject_special_files_before_blocking(self) -> None:
+        selected = Path("invented-special-file")
+        readers = (
+            lambda: transcribe_takes._sha256_file(selected),
+            lambda: transcribe_takes._inspect_normalized_audio(selected),
+            lambda: transcribe_takes._load_engine_json(selected),
+        )
+
+        for reader in readers:
+            observed: list[int] = []
+
+            def reject_special(_path, flags, *_args, observed=observed):
+                observed.append(flags)
+                raise OSError("invented special file")
+
+            with self.subTest(reader=reader), mock.patch.object(
+                transcribe_takes.os, "open", side_effect=reject_special
+            ), self.assertRaises((OSError, ValueError)):
+                reader()
+            self.assertEqual(len(observed), 1)
+            self.assertTrue(observed[0] & os.O_NONBLOCK)
+
+    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
+    def test_transcript_hash_rejects_fifo_without_waiting_for_a_writer(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            fifo = Path(temporary) / "media.mov"
+            os.mkfifo(fifo)
+            code = (
+                "from pathlib import Path; import sys; "
+                "from tritrack_editing_assistant.transcribe_takes "
+                "import _sha256_file; "
+                "\ntry: _sha256_file(Path(sys.argv[1]))"
+                "\nexcept ValueError as error: print(error); raise SystemExit(0)"
+                "\nraise SystemExit(1)"
+            )
+            completed = subprocess.run(
+                [os.fspath(Path(os.sys.executable)), "-c", code, os.fspath(fifo)],
+                check=False,
+                capture_output=True,
+                text=True,
+                timeout=3,
+            )
+
+        self.assertEqual(completed.returncode, 0)
+        self.assertEqual(completed.stdout, "TRITRACK_TRANSCRIPT_INPUT_CHANGED\n")
+        self.assertEqual(completed.stderr, "")
+
     def write_executable(self, root: Path, name: str, body: str) -> Path:
         path = root / name
         path.write_text(
             "#!/usr/bin/env python3\n" + textwrap.dedent(body),
             encoding="utf-8",
         )
         path.chmod(0o755)
         return path

     def write_ffmpeg(self, root: Path, *, sample: int) -> Path:
         return self.write_executable(
             root,
             "invented-ffmpeg",
             f"""
             import sys
             import wave

             with wave.open(sys.argv[-1], "wb") as output:
                 output.setnchannels(1)
                 output.setsampwidth(2)
                 output.setframerate(16000)
                 output.writeframes(bytes([{sample & 255}, {(sample >> 8) & 255}]) * 16000)
             """,
         )

     def write_whisper(
         self,
         root: Path,
         *,
         transcription: list[dict[str, object]],
         log: Path | None = None,
     ) -> Path:
         payload = {
             "result": {"language": "zh"},
             "transcription": transcription,
         }
         return self.write_executable(
             root,
             "invented-whisper",
             f"""
             import json
             import sys

             log_path = {str(log) if log is not None else None!r}
             if log_path is not None:
                 with open(log_path, "a", encoding="utf-8") as handle:
                     handle.write(json.dumps(sys.argv[1:]) + "\\n")

             if "--version" in sys.argv:
                 print("whisper.cpp version: invented-1")
                 raise SystemExit(0)

             required = [
                 "--model",
                 "--file",
                 "--language",
                 "zh",
                 "--temperature",
                 "0",
                 "--temperature-inc",
                 "0",
                 "--no-fallback",
                 "--no-gpu",
                 "--output-json-full",
                 "--output-file",
                 "--no-prints",
             ]
             if any(value not in sys.argv for value in required):
                 raise SystemExit(9)
             if "--prompt" in sys.argv or "--translate" in sys.argv:
                 raise SystemExit(10)

             prefix = sys.argv[sys.argv.index("--output-file") + 1]
             with open(prefix + ".json", "w", encoding="utf-8") as handle:
                 json.dump({payload!r}, handle, ensure_ascii=False)
             """,
         )

     def test_single_pass_publishes_stable_path_free_bundle(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
diff --git a/tests/test_validate_artifacts.py b/tests/test_validate_artifacts.py
index e6076a1..2bdd228 100644
--- a/tests/test_validate_artifacts.py
+++ b/tests/test_validate_artifacts.py
@@ -1,110 +1,208 @@
 """Task 11 tests for read-only, offline artifact validation."""

 from __future__ import annotations

 import copy
 import hashlib
 import json
+import os
+import subprocess
 import tempfile
 import unittest
 from pathlib import Path
 from unittest import mock

 from tests.test_contracts import VALID_CONTRACTS
 from tests.test_emit_fcpxml import media, sync_payload
 from tests.test_run_workflow import aligned_bundle_files, aligned_manifest, sha256
 from tritrack_editing_assistant import (
+    align_text,
     contracts,
     emit_fcpxml,
+    organizer,
+    paper_edit,
     process,
     run_workflow,
+    story_fcpxml,
     validate_artifacts,
 )


 def encode_json(payload: object) -> bytes:
     return (
         json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
     ).encode("utf-8")


+class NonblockingRegularFileBoundaryTest(unittest.TestCase):
+    @unittest.skipUnless(hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required")
+    def test_all_descriptor_readers_reject_special_files_before_blocking(self) -> None:
+        selected = Path("invented-special-file")
+        readers = (
+            (
+                "alignment JSON",
+                align_text,
+                lambda: align_text._read_regular_bytes(selected, "INVENTED"),
+            ),
+            ("sync map", emit_fcpxml, lambda: emit_fcpxml.load_sync_map(selected)),
+            (
+                "organizer JSON",
+                organizer,
+                lambda: organizer._read_regular_bytes(selected, "INVENTED"),
+            ),
+            (
+                "paper artifact",
+                paper_edit,
+                lambda: paper_edit._read_regular_bytes(
+                    selected, limit=1, invalid_code="INVENTED"
+                ),
+            ),
+            (
+                "run artifact",
+                run_workflow,
+                lambda: run_workflow._read_regular_bytes(
+                    selected, limit=1, code="INVENTED"
+                ),
+            ),
+            (
+                "run source hash",
+                run_workflow,
+                lambda: run_workflow._hash_regular_path(selected, code="INVENTED"),
+            ),
+            (
+                "story artifact",
+                story_fcpxml,
+                lambda: story_fcpxml._read_regular_bytes(selected, "INVENTED"),
+            ),
+            (
+                "story media hash",
+                story_fcpxml,
+                lambda: story_fcpxml._hash_regular_media(selected),
+            ),
+            (
+                "validator artifact",
+                validate_artifacts,
+                lambda: validate_artifacts._read_regular_bytes(selected),
+            ),
+        )
+
+        for label, module, reader in readers:
+            observed: list[int] = []
+
+            def reject_special(_path, flags, *_args, observed=observed):
+                observed.append(flags)
+                raise OSError("invented special file")
+
+            with self.subTest(label=label), mock.patch.object(
+                module.os, "open", side_effect=reject_special
+            ), self.assertRaises(ValueError):
+                reader()
+            self.assertEqual(len(observed), 1)
+            self.assertTrue(observed[0] & os.O_NONBLOCK, label)
+
+    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
+    def test_validator_rejects_fifo_without_waiting_for_a_writer(self) -> None:
+        with tempfile.TemporaryDirectory() as temporary:
+            fifo = Path(temporary) / "artifact.json"
+            os.mkfifo(fifo)
+            code = (
+                "from pathlib import Path; import sys; "
+                "from tritrack_editing_assistant.validate_artifacts "
+                "import validate_contract_artifact; "
+                "\ntry: validate_contract_artifact(Path(sys.argv[1]))"
+                "\nexcept ValueError as error: print(error); raise SystemExit(0)"
+                "\nraise SystemExit(1)"
+            )
+            completed = subprocess.run(
+                [os.fspath(Path(os.sys.executable)), "-c", code, os.fspath(fifo)],
+                check=False,
+                capture_output=True,
+                text=True,
+                timeout=3,
+            )
+
+        self.assertEqual(completed.returncode, 0)
+        self.assertEqual(completed.stdout, "TRITRACK_VALIDATE_INPUT_UNREADABLE\n")
+        self.assertEqual(completed.stderr, "")
+
+
 class ContractValidationTest(unittest.TestCase):
     def setUp(self) -> None:
         contracts.contract_names_by_schema_version.cache_clear()

     def tearDown(self) -> None:
         contracts.contract_names_by_schema_version.cache_clear()

     def test_discovers_every_installed_contract_from_schema_version(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             for name, payload in VALID_CONTRACTS.items():
                 with self.subTest(name=name):
                     encoded = encode_json(payload)
                     artifact = root / f"{name}.json"
                     artifact.write_bytes(encoded)

                     summary = validate_artifacts.validate_contract_artifact(
                         artifact
                     )

                     self.assertEqual(
                         summary,
                         {
                             "schemaVersion": "tritrack.validate-summary/v1",
                             "toolVersion": "0.1.0a0",
                             "artifactKind": "contract",
                             "validationScope": "contract",
                             "hashes": {
                                 "artifact": hashlib.sha256(encoded).hexdigest()
                             },
                             "counts": {},
                             "details": {
                                 "contractName": name,
                                 "contractSchemaVersion": payload["schemaVersion"],
                             },
                         },
                     )
                     self.assertEqual(artifact.read_bytes(), encoded)

     def test_rejects_unknown_invalid_and_unreadable_contracts(self) -> None:
         with tempfile.TemporaryDirectory() as temporary:
             root = Path(temporary)
             unknown = root / "unknown.json"
             unknown.write_bytes(encode_json({"schemaVersion": "invented/v1"}))
             invalid = root / "invalid.json"
             payload = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
             payload["questions"][0]["unexpected"] = True
             invalid.write_bytes(encode_json(payload))
             malformed = root / "malformed.json"
             malformed.write_bytes(b"{not-json")
             empty = root / "empty.json"
             empty.write_bytes(b"")
             symlink = root / "symlink.json"
             symlink.symlink_to(unknown)

             cases = (
                 (unknown, "TRITRACK_VALIDATE_CONTRACT_UNKNOWN"),
                 (invalid, "TRITRACK_VALIDATE_CONTRACT_INVALID"),
                 (malformed, "TRITRACK_VALIDATE_JSON_INVALID"),
                 (empty, "TRITRACK_VALIDATE_INPUT_INVALID"),
                 (symlink, "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
                 (root / "missing.json", "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
             )
             for artifact, code in cases:
                 with self.subTest(code=code), self.assertRaisesRegex(
                     ValueError, rf"^{code}$"
                 ):
                     validate_artifacts.validate_contract_artifact(artifact)

     def test_rejects_duplicate_installed_schema_versions(self) -> None:
         profile = contracts.load_schema("compatibility-profile-v1")
         duplicate = copy.deepcopy(profile)
         with mock.patch.object(
             contracts,
             "load_schema",
             side_effect=lambda name: duplicate
             if name == "sync-map-v1"
             else profile,
         ), self.assertRaisesRegex(
             ValueError, "^TRITRACK_CONTRACT_REGISTRY_INVALID$"
--- END FIX-FORWARD DIFF ---

## Exact selected current files


--- BEGIN FILE .tritrack-project.json ---
{
  "schemaVersion": "tritrack.project-identity/v1",
  "projectId": "tritrack-editing-assistant",
  "projectKind": "public-engine",
  "maintainerSkill": "tritrack-editing-assistant-maintainer",
  "lane": "OSS"
}
--- END FILE .tritrack-project.json ---

--- BEGIN FILE AGENTS.md ---
# Public project agent instructions

This repository is the public-engine project. Its development lane is `OSS`.
It is not a production-media repository and it does not inherit state from a
similarly named project.

## Startup

Use `.agents/skills/tritrack-editing-assistant-maintainer/SKILL.md` for every
substantive maintenance session. The only cold-start command is:

```text
$tritrack-editing-assistant-maintainer OSS 開工
```

Before reading task state or changing files, resolve the Git toplevel and run
the skill's `scripts/check_project_identity.py`. A missing or mismatched
`.tritrack-project.json` fails closed.

Then read `STATUS.md`, `PRODUCT-WISHES.md`, `docs/ROADMAP.md`,
`docs/TOOLING.md`, `README.md`, and only the files relevant to the active task.
State the candidate commit, task, next action, applicable standing grants, and
planned evidence before mutating project state.

## Three-role boundary

- `tritrack-editing-assistant-maintainer` owns this repository's development
  and maintenance.
- `skills/tritrack-editing-assistant/SKILL.md` is the installed end-user
  product surface. It contains no maintainer task state or release authority.
- Private production orchestration is a different project. Do not scan its
  repositories or import its status, media, transcripts, journals, templates,
  credentials, or history. Accept only reviewed clean-room intake with exact
  hashes and declared transformations.

If required clean-room intake is missing, report the missing handoff and stop.
Do not search for another checkout or silently use a remembered path.

## Development rules

- Work in an isolated branch/worktree. Integrate a fully green candidate to
  `main` only under the standing grant below.
- Use test-driven development for behavior changes and preserve the observed
  red/green evidence.
- Use invented or explicitly cleared fixtures only.
- Keep media, transcripts, credentials, absolute home paths, proprietary
  assets, and private operational evidence out of Git, prompts, and issues.
- Keep the default workflow local and no-overwrite. Provider operations remain
  separate, explicit opt-in paths.
- Do not claim planned commands are implemented. Verify against `STATUS.md`,
  tests, and installed command behavior.
- Public `STATUS.md` is the only current maintenance status. Public
  `docs/ROADMAP.md` owns the public task sequence.

## Authorization model

Producer authorization is a capability-scoped standing grant. Once a
capability is explicitly authorized or recorded here, it remains authorized for
the same target, visibility, scope, and risk until the producer revokes it.
Do not request it again, pause at that gate, or reinterpret a new task as
revoking it.

A new authorization is needed only when the capability has never been granted,
or when the proposed action materially changes the target, visibility, scope,
or risk. Destructive history changes, credential or private-data disclosure,
and a different remote are material changes rather than repetitions.

The current standing grant covers closeout review, fix-forward of ordinary
in-scope findings, fast-forward integration of a fully green candidate, and
pushing `main` to the existing public `origin` with exact remote-SHA backup
verification. Force-push, tags, releases, pull requests, tester contact,
package publication, and application submission have not yet been granted.

## Close

Before closing, run focused and full tests, lint, the project-boundary tests,
skill validation, and `git diff --check`; then read back exact status and
changed files. Update `STATUS.md` only after the coherent package is green.
Commit only task-owned files. A requested implementation includes closeout
review and fix-forward until ordinary in-scope findings are resolved; stop only
for a true contract gap, unsafe expansion, or a separately gated action.
--- END FILE AGENTS.md ---

--- BEGIN FILE README.md ---
# TriTrack Editing Assistant

TriTrack Editing Assistant is a local-first command-line project for building
editable Final Cut Pro interview workflows from local A/B-camera media. It is
designed for editors working with a terminal-capable agent while keeping story
decisions with the editor.

> Development scaffold: `0.1.0a0` currently exposes the component registry,
> the fail-closed `doctor` command, local audio-verified `sync`, fixed-profile
> local `transcribe`, deterministic cue-addressed `align`, offline receipt-only
> `hybrid`, profile-bound deterministic `emit`, strict `paper export`／
> `paper apply`, deterministic `organize`, and immutable `run prepare`／
> `align`／`finish`／`status`, plus four-mode read-only `validate`. The optional
> live transport remains planned and fail closed. There is no public release
> yet.

## Target alpha compatibility

The first alpha targets only this profile; support is not claimed until the
profile's automated checks and invented-content Final Cut round trip pass:

- macOS 26.5.2
- Final Cut Pro 12.3
- FCPXML 1.14
- UHD 3840×2160 at 29.97 NDF
- Rec. 709 and stereo 48 kHz source audio
- Python 3.12 and 3.13

The tool will fail closed outside declared compatibility profiles. It is not
affiliated with, endorsed by, or sponsored by Apple Inc. Final Cut Pro is a
trademark of Apple Inc.

## Local-first boundary

The default workflow is intended to operate without a network call or paid
model. The implemented optional `hybrid` command only validates existing
provider receipts offline; it performs no request, upload, deletion,
subprocess, credential lookup, or network access. No live provider transport is
operational in this scaffold.

Do not place production clips, transcripts, credentials, private home paths,
or proprietary title templates in this repository or in a public issue.

## Development installation

This repository currently supports source installation for development:

```bash
python3.13 -m venv venv
venv/bin/pip install -e '.[dev]'
venv/bin/tritrack components --json
```

Run the implemented compatibility preflight with:

```bash
venv/bin/tritrack doctor \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --json
```

The command reports sanitized dependency and compatibility checks. It does not
claim that a manual Final Cut import occurred.

Run local A/B synchronization with one repeatable flag per source:

```bash
venv/bin/tritrack sync \
  --camera-a A-001.MP4 \
  --camera-a A-002.MP4 \
  --camera-b B-001.MP4 \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --output results/sync-map.json
```

The output path and its parent directory must already be absent and present,
respectively. The command reads local metadata and audio through bounded
`ffprobe`/`ffmpeg` argv calls, validates `sync-map-v1`, and publishes the map
atomically without modifying source media or overwriting an existing result.

Emit a deterministic string-out from that strict map with the same repeatable
source set:

```bash
venv/bin/tritrack emit \
  --camera-a A-001.MP4 \
  --camera-a A-002.MP4 \
  --camera-b B-001.MP4 \
  --sync-map results/sync-map.json \
  --profile uhd-2997-ndf-fcpxml-1.14 \
  --binding basic-title-v1 \
  --event-name "Invented Interview" \
  --project-name "Invented String-out" \
  --output results/string-out.fcpxml
```

The source basenames must exactly match the camera-specific media IDs in the
map, including its unpaired entries. The command validates the public schema,
profile, and title binding; checks the declared source video and audio profile
through the bounded probe boundary; honors each pair's `audioMaster`; quantizes
timing once to integer frames; and creates one absent FCPXML path atomically.
It does not mutate its inputs or overwrite a race winner. The FCPXML contains
local source file URIs and should remain under the same custody as the source
media. Automated FCPXML 1.14 DTD validation does not claim that a Final Cut GUI
import or round trip ran.

Run one fixed local whisper.cpp transcription pass with one repeatable flag per
source:

```bash
venv/bin/tritrack transcribe \
  --media A-001.MP4 \
  --media A-002.MP4 \
  --model models/ggml-model.bin \
  --language zh \
  --output results/transcript-bundle.json \
  --json
```

The model is caller-owned and is never bundled or downloaded by TriTrack. The
command normalizes each source to temporary mono 16 kHz PCM, runs the installed
`whisper-cli` once per take with the fixed
`whisper-cpp-cpu-no-fallback-v1` profile, and creates one absent strict
`transcript-bundle-v1` path atomically. Media basenames must be unique and the
two- or three-letter language code must be explicit. CPU-only decoding removes
the local GPU backend as a profile variable; it does not claim bit-identical
inference across engine versions, models, or machines.

Recognized cues are NFC-normalized, single-spaced, ordered, and bounded to
integer milliseconds. A bounded final whisper.cpp timestamp pad is clipped to
the real PCM duration. Exact digital silence may produce an empty take; the
observed `[BLANK_AUDIO]` engine sentinel is discarded only after the PCM has
independently been proven all-zero. Non-silent empty output, text over proven
silence, malformed timing, leaked control tokens, or repeated structural
artifacts fail closed without publishing. No retry ladder, prompt, translation,
provider call, upload, or network access is part of this command.

The bundle contains transcript text and source basenames, so keep it under the
same local custody as the media. `--json` prints only a path-free completion
summary and bundle hash; it does not print transcript text.

Promote strict cue-addressed revisions without changing source timing:

```bash
venv/bin/tritrack align \
  --transcript results/transcript-bundle.json \
  --revision results/text-revision.json \
  --output results/aligned-transcript.json \
  --json
```

The `text-revision-v1` file binds its changes to the SHA-256 of the exact source
bundle bytes and addresses existing take and cue IDs. The command preserves
take IDs, source hashes, status, cue IDs, and integer-millisecond timing;
unmentioned cues retain their original text. Empty takes cannot be revised.
The absent output is a deterministic `aligned-transcript-v1` artifact bound to
both exact input hashes. The source, revision, and aligned artifacts all contain
transcript text and remain under local-media custody.

Validate already-produced Gemini evidence before promoting the same revision:

```bash
venv/bin/tritrack hybrid \
  --transcript results/transcript-bundle.json \
  --proposal results/text-revision.json \
  --receipt results/provider-receipt-A-001.json \
  --model gemini-exact-model-id \
  --output results/hybrid-aligned-transcript.json \
  --json
```

Repeat `--receipt` once per revised take. This command is an offline conformance
adapter, not a provider client: it makes no network call and cannot create the
receipts it consumes. Every receipt must bind the exact bundle, take, source
audio hash, requested and observed model, completed upload and request, 2xx
response, and attempted plus confirmed 2xx server-file deletion. It then uses
the same local promotion core as `align`, producing byte-identical output for
the same transcript and revision bytes. `gemini_transcribe.mjs`, live upload,
and provider credentials remain unimplemented.

Export an editor-facing workbook from the strict aligned authority:

```bash
venv/bin/tritrack paper export \
  --aligned results/aligned-transcript.json \
  --output results/paper-edit.xlsx \
  --json
```

Add `--grouping results/grouping.json` to prefill a workbook from existing
canonical editor intent. The XLSX file is a transport, not an authority. Its
complete `Cues` reference grid and hidden public-safe manifest bind it to the
exact aligned bytes. Formula cells, reference/display changes, unexpected
sheets, macros, external workbook links, cell hyperlinks, merged cells, and
structural drift fail closed. Archive expansion and worksheet dimensions are
bounded before rectangular cell inspection. Formula-looking transcript text is
exported as a literal display string.

After editing only the `Questions` and `Selections` tables, apply the workbook
back to strict JSON authority:

```bash
venv/bin/tritrack paper apply \
  --aligned results/aligned-transcript.json \
  --workbook results/paper-edit.xlsx \
  --output results/grouping.json \
  --json
```

The resulting `grouping-v1` contains cue addresses and normalized editor text,
but no transcript text, source hash, or millisecond timing. Compile it into a
deterministic transcript-text-free working cut with timing copied only from
the exact aligned authority:

```bash
venv/bin/tritrack organize \
  --aligned results/aligned-transcript.json \
  --grouping results/grouping.json \
  --output results/working-cut.json \
  --json
```

All three Task 9 operations are local-only and make no network, provider,
credential, media-processing, subprocess, FCPXML, or orchestration request.
Every output path must be absent.

## Task 10 immutable run workflow

Task 10 connects the installed local commands through three immutable bundles
and two explicit editor gates. Start by reading the installed command help:

```bash
venv/bin/tritrack run --help
venv/bin/tritrack run prepare --help
venv/bin/tritrack run align --help
venv/bin/tritrack run finish --help
venv/bin/tritrack run status --help
```

`run prepare` accepts repeatable camera A／B paths, a repeatable transcription
subset, the caller-owned local model, explicit language, public profile and
title binding, caller-owned event／project names, a safe run ID, and one absent
output directory. It runs doctor → sync → transcribe → string-out and publishes
exactly `doctor.json`, `sync-map.json`, `transcript-bundle.json`,
`string-out.fcpxml`, and `run-manifest.json`.

Pause for the editor to provide one strict `text-revision-v1` bound to the
exact transcript bytes. An empty `takes: []` is accepted only as explicit
no-change approval. Then `run align` consumes the complete prepared bundle and
revision, publishing `aligned-transcript.json`, `paper-edit.xlsx`, and a new
manifest into another absent directory.

Pause again while the editor changes only the workbook's `Questions` and
`Selections` tables. The workbook is transport, not authority. `run finish`
consumes the exact prepared and aligned bundles, edited workbook, and original
camera sources; it publishes canonical `grouping.json`, transcript-text-free
`working-cut.json`, story-ordered `story-cut.fcpxml`, and a finished manifest.
The story renderer re-derives cue text and timing from strict JSON authorities,
honors sync offsets and the declared audio master, and excludes reserve ranges.

Every mutating stage requires a new absent directory and publishes its manifest
last. `run status` is read-only and returns only the run ID, phase, next action,
completed stage names, and logical artifact hashes. The workflow makes no
network call and does not claim a Final Cut GUI import, DTD validation, or
round trip.

The separate installed skill at
`skills/tritrack-editing-assistant/SKILL.md` guides editors through the two
human gates using help-first installed commands. It contains no repository
maintenance or publication authority.

## Read-only artifact validation

Read installed help before selecting one explicit validation mode:

```text
tritrack validate --help
tritrack validate contract --help
tritrack validate fcpxml --help
tritrack validate paper --help
tritrack validate run --help
```

| Mode | Exact `validationScope` | Success proves | Success does not prove |
| --- | --- | --- | --- |
| `contract` | `contract` | One exact JSON artifact satisfies its installed registered schema. | Referenced files, parent artifacts, or cross-file hashes exist or match. |
| `fcpxml` | `structural-profile` | Exact FCPXML bytes satisfy the explicit installed profile and title binding structural checks. | Source media is available, a DTD passed, or a Final Cut GUI import ran. |
| `paper` | `authority-bound` | The workbook is acceptable against the exact supplied aligned transcript bytes. | A grouping artifact was created or workbook intent was repaired. |
| `run` | `complete-run-bundle` | The complete immutable bundle, manifest chain, fixed filenames, contracts, and hashes agree. | Any missing bundle was reconstructed or changed. |

Every mode is read-only and writes no output. It does not repair inputs, guess
a format, search sibling paths, probe source media, consult a DTD, launch a
GUI, or make a network request. A passing result is evidence only inside the
reported scope.

## One-minute invented quickstart

After the development installation above, exercise the complete implemented
path with deterministic invented media and one absent, ignored output root:

```bash
venv/bin/python examples/quickstart_demo.py --output .fixture-runs
```

The example exercises the implemented synchronization-to-emission path. It
generates two four-second UHD 29.97 NDF Rec. 709 clips with stereo
48 kHz invented audio, calls the installed `tritrack sync` and `tritrack emit`
surfaces, validates the strict map and profile-bound XML, checks deterministic
FCPXML bytes, and uses the installed FCPXML 1.14 DTD when the declared Final Cut
application is available. It prints only a sanitized relative-path summary and
does not upload or publish anything. The output root must be absent; choose a
new ignored path for another run.

Choose the narrowest entry point that matches your goal:

1. Use the invented quickstart above to verify the implemented local path.
2. Use `tritrack sync` then `tritrack emit` with your own local compatible
   media when you need an editable string-out.
3. Use `tritrack transcribe` with a caller-owned local whisper.cpp model when
   you need the strict local cue bundle.
4. Use `tritrack align` to promote a strict cue-addressed revision while
   preserving local cue timing.
5. Use `tritrack hybrid` only to validate already-produced provider receipts
   offline before running the same local promotion.
6. Use `tritrack paper export` then `tritrack paper apply` to author durable
   cue-addressed grouping intent through a non-authoritative workbook.
7. Use `tritrack organize` to compile that intent into a deterministic
   transcript-text-free working cut.
8. Use `tritrack run` to carry the exact local artifacts through immutable
   prepared, aligned, and finished bundles with explicit editor approval.
9. Use one explicit `tritrack validate` mode to check an existing artifact
   without modifying it, and `tritrack components --json` to inspect the
   unchanged eleven-component registry.

## Eleven-component roadmap

The component registry is the machine-readable source for current status:

```bash
tritrack components --json
```

| # | Component | Public command | Current status |
| ---: | --- | --- | --- |
| 1 | `sync_scan.py` | `tritrack sync` | implemented |
| 2 | `emit_fcpxml.py` | `tritrack emit` | implemented |
| 3 | `transcribe_takes.py` | `tritrack transcribe` | implemented |
| 4 | `string_out.py` | `tritrack emit` | implemented |
| 5 | `hallucination.py` | `tritrack transcribe` | implemented |
| 6 | `organizer.py` | `tritrack organize` | implemented |
| 7 | `paper_edit.py` | `tritrack paper` | implemented |
| 8 | `align_text.py` | `tritrack align` | implemented |
| 9 | `gemini_hybrid.py` | `tritrack hybrid` | implemented, offline optional |
| 10 | `gemini_transcribe.mjs` | `tritrack hybrid` | planned, optional |
| 11 | `multicam-sync` | `tritrack run` | implemented |

`components`, `doctor`, schemas, packaging, fixtures, tests, and release
automation are supporting infrastructure and do not increase the component
count.

## Project policies

- [Contributing](CONTRIBUTING.md)
- [Security and private-media reporting](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
- [Public roadmap](docs/ROADMAP.md)
- [Current maintenance status](STATUS.md)

Licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE).
--- END FILE README.md ---

--- BEGIN FILE STATUS.md ---
# Public maintenance status

Updated: 2026-08-18
Project kind: public engine
Lane: `OSS`
Release state: public pre-release source; no tag, package publication, or
tester outreach

## Current gate

Tasks 1–11 are complete in this public candidate. Task 6 began from exact
Task 5 candidate `dc2aa78380749cc2787606cdb9702a71725cf21b` after `main` was
fast-forwarded from `41d5034addcc1f870ec7b055f62b69c38cae415b` with no history
rewrite or merge commit.

Task 6 implements strict `sync-map-v1` loading, exact public profile and Basic
Title binding checks, integer-frame pair alignment, deterministic pair-first
string-out ordering, stable XML identifiers and bytes, XML escaping, source
immutability, sync-map audio-master selection, source-profile probing, and
race-safe absent-output FCPXML publication. The implementation retains FCPXML
1.14, UHD 3840×2160, `1001/30000s`, NDF, Rec. 709, stereo, and 48 kHz profile
values. Closeout-review verification after the last implementation edit passed
67 tests and Ruff; invented temporary output also passed the declared Final Cut
Pro 12.3 FCPXML 1.14 DTD. This is automated DTD evidence, not a claim that a
Task 6 GUI import or round trip ran.

Task 6.5 implementation candidate
`0a99fb65979930385a6a267d596f0baa2ea5aaf3` adds one public invented-media
quickstart from installed `sync` through installed `emit`, exact repeat-output
determinism, strict profile／map／XML checks, conditional local DTD validation,
minimal Python 3.12／3.13 CI, and a three-choice public entry guide without
changing the eleven-component registry. Final verification passed 8 focused,
31 Task 5／6 regression, 77 complete-suite, and 9 boundary tests, plus Ruff,
compilation, identity, skill, installed CLI, and diff gates. One real invented
run passed FFmpeg／FFprobe generation, audio pairing, two deterministic emits,
and the installed FCPXML 1.14 DTD. GitHub Actions run `31848242516` passed the
Python 3.12／3.13 matrix at that exact candidate; its Linux jobs skipped the
Darwin-only real-environment doctor acceptance and made no Final Cut／DTD
claim. The local run did not open Final Cut and makes no GUI import or
round-trip claim. Sanitized evidence is in
`docs/TASK-6.5-VERIFICATION.md`.

Task 7 implementation candidate
`60811a7af117a6dfd70d470513676d87db0922bb` adds fixed-profile CPU-only local
whisper.cpp transcription, strict `transcript-bundle-v1` publication,
deterministic cue canonicalization and silence outcomes, full-batch input
change detection, and atomic no-overwrite output. Final verification passed 37
focused, 100 complete-suite, and 9 boundary tests, plus Ruff, compilation,
identity, skill, installed CLI, schema, real-engine determinism, privacy, and
diff gates. Real invented speech produced byte-identical bundles in two runs;
independently proven digital silence produced an empty zero-cue take. Gemini's
dynamic-model closeout review passed with no findings. The separately
requested Claude subscription review timed out and remains explicitly
incomplete, with no retry or fallback. Sanitized evidence is in
`docs/TASK-7-VERIFICATION.md`.

Task 8 implementation candidate
`4cc25b5248fe67a7cce656f0e810976f18565c16` adds strict cue-addressed
`text-revision-v1` promotion into
provider-neutral `aligned-transcript-v1`, exact-byte source and revision
binding, immutable take／cue timing, input-change detection, and atomic
no-overwrite publication. Its optional `hybrid` command validates one existing
Gemini receipt per revised take, including exact model, bundle／take／audio
binding, request and upload completion, and confirmed server-file deletion,
then invokes the same local promotion core. It performs no provider request,
upload, deletion, subprocess, credential lookup, or network access;
`gemini_transcribe.mjs` remains planned. Sanitized evidence is in
`docs/TASK-8-VERIFICATION.md`.
Local verification passed 43 focused, 126 complete-suite, and 9 boundary
tests, plus Ruff, compilation, identity, skill, installed CLI, registry, and
diff gates.
Gemini's dynamic-model closeout review passed with no findings, test gaps, or
documentation gaps. The separately requested Claude subscription review timed
out and remains explicitly incomplete, with no retry or fallback.

Task 9 post-fix implementation candidate
`cc813f01176c1a9c8d0a0409b2de112ffb9ca8a5` retains the original
`f4e8074936674407e21bab2928701b4c88e6216c` cue-addressed
`grouping-v1`, adds deterministic dual-bound `working-cut-v1` compilation, and
implements the local `paper export`, `paper apply`, and `organize` surfaces.
The XLSX workbook is a four-worksheet editor transport, not an authority:
apply re-derives its complete cue/display grid and public-safe manifest from
the exact aligned bytes, rejects formulas, hyperlinks, unsafe ZIP expansion,
extreme worksheet dimensions, and structural drift, normalizes only
editor-authored text, and returns canonical grouping JSON. Task 9 never
retimes, rewrites, splits, merges, or deletes aligned cues and performs no
network, provider, credential, media, subprocess, FCPXML, or orchestration
operation. Final post-fix local verification passed 53 focused, 155
complete-suite, and 9 boundary tests, plus Ruff, compilation, identity, skill,
installed CLI, round-trip, and diff gates. Both the original and post-fix
Gemini dynamic-model closeout reviews passed with no findings. Both separate
Claude subscription reviews timed out and remain explicitly incomplete, with
no retry or fallback.
The pre-fix review-record candidate
`2edb93e515a62e4f26a6d61f1447e5c605892ec2` matched public `origin/main`, and
GitHub Actions run `31881710301` passed its Python 3.12／3.13 test, lint, and
compile matrix. Post-fix review-record candidate
`f5dc9d5f849c2024fabd44470025ff1ad927ae1b` then matched public `origin/main`,
and GitHub Actions run `31907255236` passed its Python 3.12／3.13 test, lint,
and compile matrix. Sanitized evidence is in `docs/TASK-9-VERIFICATION.md`.

Task 10 implementation candidate
`5fe9a4531f8dbd23f98174023d61f66a359d461b` adds installed
`tritrack run prepare`, `align`, `finish`, and read-only `status` commands.
Each mutating transition publishes a new immutable absent directory with its
manifest hard-linked last; fixed artifact names, exact byte hashes,
phase-specific completed stages, and the prior-manifest chain are validated
before reuse. The final story renderer re-derives every active range and title
from exact aligned／grouping／working-cut authorities, quantizes once to profile
frames, honors paired-source offsets and the declared audio master, excludes
reserve, and emits strict story-ordered FCPXML. Task 10 also installs the
separate end-user `tritrack-editing-assistant` skill with help-first command
discovery and explicit text-revision and paper-edit human gates. The workbook
remains transport only. The workflow makes no network request and does not
claim a Final Cut GUI import, DTD result, or round trip. Sanitized evidence is
in `docs/TASK-10-VERIFICATION.md`.
Local verification passed 193 complete-suite and 9 maintainer-boundary tests,
plus Ruff, compilation, identity, both skill validators, non-editable wheel
help／status smoke, registry, and diff gates.
The frozen closeout target `08517f477ae263664f981c002cc974c77fba291a`
passed Codex's independent review and a completed Gemini review with no
findings. Gemini requested, observed, and completed `gemini-3.7-flash`. The
separate Claude subscription review requested the dynamic `opus` capability
alias, timed out, and remains explicitly incomplete with observed／completed
models null and no retry, downgrade, or fallback.

Task 11 implementation candidate
`ce562e995b63f3f1a29989de3e1ef202da27b5f2` adds the exact four-mode,
read-only `tritrack validate` surface with `contract`, `structural-profile`,
`authority-bound`, and `complete-run-bundle` claim scopes. It also adds a
maintainer-only clean-source privacy and archive-safety gate, two-snapshot
package reproducibility checks, fresh local-wheel installation smoke, a closed
manifest-last receipt, exact Python／build constraints, and fixed public CI on
Ubuntu 24.04 x64 and macOS 26 arm64 across Python 3.12／3.13. The eleven-entry
component registry is unchanged.
Local verification in a new Python 3.13 environment passed 69 focused and 235
complete-suite tests, Ruff, compilation, identity, both skill validators,
package-member policy, and Git cleanliness. The implementation gate passed
with byte-identical wheels, identical normalized sdist member inventories,
and an installed-wheel `pip check` plus five validator help smokes. Sanitized
evidence and exact hashes are in `docs/TASK-11-VERIFICATION.md`.
Task 11 made no tag, release, package publication, pull request, tester contact,
artifact upload, signing, attestation, SBOM, Final Cut GUI, DTD, live provider,
credential, or application-submission claim.

A 2026-08-18 Claude coverage audit found eight historical Task 7–11 attempts
that ended `claude-timeout` after preflight with ambiguous dispatch and no
usable result. The registered OAuth preflight repair is not the same failure:
a separate Task 9 design review completed through that repaired subscription
lane. One new concise recovery review against current public `main` was sent
once through the approved wrapper and also ended at its hard timeout, with no
observed／completed model or raw result. It was not retried, downgraded, or sent
through a paid／alternate route. The public inventory, comparison, packet, and
attempt ledger are preserved in
`docs/reviews/claude-incomplete-audit-2026-08-18.md` and the matching
`tasks-7-11-claude-recovery-*` records.

A later producer-mediated interactive Claude Code review against public
`main` commit `7ae540a1ab46de39b31d826ae99752b325e6e9e1` returned
`NO FINDINGS` plus four optional hardening observations. Fix-forward commit
`eaa17b49c9100bf92452106c1de23392a2831ae5` maps third-party workbook parser
`ValueError` failures to the stable public code, makes current working-cut
claims precisely `transcript-text-free`, and adds direct noncanonical
working-cut regression coverage. The hypothetical inner-pipe engine-token
observation was not accepted without a supported token or failing contract.
The complete suite passed 240 tests; Ruff, compilation, project identity, both
skill validators, and diff checks also passed. The interactive session's model
and usage provenance remain self-reported, and the result does not convert any
earlier wrapper timeout or ambiguous dispatch into formal completion. Public
review and adjudication records are in `docs/reviews/tasks-7-11-claude-manual-*`.

## Next action

Task 12 freezes and independently reviews the alpha candidate. Task 11 does
not authorize or claim tags, releases, package publication, tester contact, or
application submission.

## Implemented surface

- clean Python package and eleven-component status registry;
- Draft 2020-12 contracts loaded from installed package resources;
- bounded argv-only subprocess execution and sanitized receipts;
- audio-verified A/B synchronization with atomic `sync-map-v1` publication;
- profile-bound deterministic string-out and atomic FCPXML 1.14 publication;
- fixed-profile CPU-only local transcription with strict deterministic bundle
  canonicalization and atomic no-overwrite publication;
- deterministic cue-addressed text promotion with immutable local timing and
  exact-byte provenance;
- optional offline Gemini receipt conformance that shares the local promotion
  core and performs no network access;
- cue-addressed grouping with deterministic working-cut compilation;
- strict local paper-edit export/apply with complete aligned-grid
  re-derivation, semantic round trips, and atomic no-overwrite publication;
- immutable prepared／aligned／finished run bundles with exact manifest chains,
  fixed artifacts, manifest-last publication, and read-only status;
- deterministic story-ordered FCPXML projection from exact editor authorities;
- separate installed end-user editing skill with two explicit human gates;
- four-mode read-only artifact validation with scope-limited path-free
  summaries;
- clean tracked-source privacy, bounded archive inspection, reproducible
  packaging, fresh-wheel installation, and manifest-last local candidate gate;
- fixed Ubuntu／macOS and Python 3.12／3.13 release-grade public CI;
- fail-closed `doctor` command;
- exact UHD 29.97 NDF FCPXML 1.14 compatibility profile;
- public Basic Title binding with invented-content Final Cut round-trip
  evidence;
- public invented-media synchronization-to-FCPXML quickstart with deterministic
  repeat emission, conditional local DTD verification, and minimal CI.

The network-capable `gemini_transcribe.mjs` component remains planned.

## Custody

The public `origin` is
`https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`.
Closeout requires verifying that its `main` SHA exactly matches the local green
candidate, making the GitHub copy the off-device Git backup. Tags, releases,
pull requests, tester contact, package publication, and application submission
have not yet been granted. All grants follow the standing-authorization model
in `AGENTS.md`.
--- END FILE STATUS.md ---

--- BEGIN FILE docs/ROADMAP.md ---
# Public alpha roadmap

This file owns the public implementation sequence. `STATUS.md` records the
current gate. Private coordination and outward-action strategy do not belong
here.

## Completed base

- Tasks 1–4: clean-history scaffold, contracts, bounded process receipts,
  compatibility doctor, and public Basic Title evidence.
- Task 4.5: public-native maintainer governance and the three-role skill
  boundary are complete.
- Task 5: audio-verified A/B synchronization from the reviewed clean-room
  intake, with strict `sync-map-v1` and no-overwrite publication.
- Task 6: profile-bound FCPXML 1.14 emission and deterministic string-out, with
  integer-frame timing, strict public profile, source-probe and binding checks,
  sync-map audio-master selection, and atomic no-overwrite publication.
- Task 6.5: self-contained invented-media quickstart through installed
  synchronization and deterministic FCPXML emission, with minimal CI and
  public-safe readiness evidence. It remains supporting infrastructure, not a
  twelfth workflow component.
- Task 7: fixed-profile CPU-only local whisper.cpp transcription, strict
  provider-neutral cue bundles, deterministic canonicalization and silence
  outcomes, input-change detection, and atomic no-overwrite publication.
- Task 8: deterministic cue-addressed text promotion with immutable local
  timing, exact-byte provenance, and an isolated offline Gemini-receipt
  conformance adapter. No live provider transport is shipped.
- Task 9: strict cue-addressed grouping, deterministic working-cut compilation,
  and a local XLSX paper-edit round trip with complete reference-grid
  re-derivation. The workbook is a transport; JSON remains authoritative.
- Task 10: installed immutable `run prepare`／`align`／`finish` bundles,
  read-only `run status`, deterministic story-ordered FCPXML, and a separate
  end-user `tritrack-editing-assistant` skill with explicit human gates.
- Task 11: exact four-mode read-only artifact validation, closed source and
  archive privacy gates, reproducible wheel／sdist package contracts, a
  manifest-last local candidate receipt, and fixed Ubuntu／macOS CI across
  Python 3.12／3.13.

## Alpha-candidate sequence

- Task 12 freezes and independently reviews the alpha candidate. `STATUS.md`
  alone records whether this gate is pending or complete.
- Task 13 proves the public engine as the generic authority and defines a
  deliberate downstream integration seam after Task 12 is complete.

## Outward-action boundary

Repository publication, tags, releases, tester contact, and package
publication are not authorized merely by completing this roadmap. Authorization
follows the standing-authorization model in `AGENTS.md` and the public
maintainer skill: once a capability is explicitly granted for the same target,
visibility, scope, and risk, it remains valid until revoked and must not be
requested again.
--- END FILE docs/ROADMAP.md ---

--- BEGIN FILE docs/TOOLING.md ---
# Maintainer tooling facts

This file records stable, public-safe facts needed to reproduce local
maintenance. It must not contain credentials, private paths, transient tokens,
or another project's tool state.

## Python

- Supported runtime: Python 3.12 and 3.13.
- Clean gate environments install both `pip` and `setuptools` through the
  exact `requirements/ci-constraints.txt` pins before installing `.[dev]`.
- Full tests: `python -m unittest discover -s tests -v`
- Lint: `ruff check src tests examples scripts`
- Skill validation uses the current Codex `skill-creator` validator against
  both `.agents/skills/tritrack-editing-assistant-maintainer` and
  `skills/tritrack-editing-assistant`.

## Read-only artifact validation

The installed help authorities are:

```text
tritrack validate --help
tritrack validate contract --help
tritrack validate fcpxml --help
tritrack validate paper --help
tritrack validate run --help
```

- `contract` reports `validationScope: contract` and proves only that one exact
  JSON artifact satisfies its installed registered schema.
- `fcpxml` reports `validationScope: structural-profile` and proves only the
  installed profile and title-binding structural checks. It does not probe
  source media, validate against a DTD, or launch a Final Cut GUI.
- `paper` reports `validationScope: authority-bound` and proves that the
  workbook is acceptable against the exact supplied aligned transcript bytes.
- `run` reports `validationScope: complete-run-bundle` and proves the complete
  immutable artifact set, manifest chain, contracts, and hashes agree.

All four modes are read-only. The command does not repair an artifact, guess a
format, discover sibling inputs, write a result, use network access, or broaden
success beyond its exact scope.

## Maintainer release-readiness gate

The only maintainer entry point is:

```text
python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

The source must be one clean Git toplevel at `HEAD`. The output parent must
exist and the named output directory must be absent; an existing path or race
winner is preserved. The gate inventories every stage-zero tracked regular
file, rejects private-path／credential shapes and forbidden binary surfaces,
builds twice from separately verified `git archive` snapshots, and inspects
wheel／sdist metadata, paths, types, bounds, exact members, contents, and hashes
without generic extraction.

The gate requires byte-identical wheels. For sdists it requires identical
normalized member／content inventories while recording the chosen compressed
archive's exact SHA-256; it does not claim byte-identical gzip output. A new
external virtual environment installs only the selected local wheel, runs
`pip check`, confirms the eleven-component registry, and exercises all five
validator help authorities.

Publication hard-links the two archives first and canonical
`release-manifest.json` last. The closed manifest contains only project
name／version／commit, tracked-source count and digest, exact toolchain and
platform facts, artifact sizes／hashes／member counts／inventory hashes, passed
gate names, reproducibility facts, and explicit non-claims. It contains no
path, time, account, host, command, log, source content, or matched value.

Public CI uses exactly Ubuntu 24.04 x64 and macOS 26 arm64 with Python 3.12
and 3.13, plus one Ubuntu 24.04／Python 3.13 quality job and one local candidate
gate job. CI and the maintainer gate do not tag, publish, upload, sign, attest,
contact testers, operate a GUI, or submit an application.

## Local synchronization

- `tritrack sync --help` is the command authority for Task 5 flags.
- Media metadata and mono float audio are read through `ffprobe` and `ffmpeg`
  using the public bounded-process wrapper. No shell command is constructed.
- The command creates one absent `sync-map-v1` JSON path atomically and never
  rewrites source media or an existing output path.

## Local FCPXML emission

- `tritrack emit --help` is the command authority for Task 6 flags.
- The command consumes one strict `sync-map-v1`, repeatable local camera A/B
  paths, the exact public compatibility profile, the public Basic Title
  binding, and caller-owned event and project names.
- Source duration, video dimensions, frame rate, Rec. 709 fields, and stereo
  48 kHz audio fields are read through the existing bounded `ffprobe` boundary
  and must match the declared profile before emission. JSON decimal timing is
  converted to rational values and quantized once to integer frames; timeline
  accumulation never uses binary floating point.
- Each paired segment enables audio only for the sync map's declared
  `audioMaster`; unpaired source segments retain their own audio.
- The command creates one absent FCPXML path atomically. It never rewrites
  source media, the sync map, an existing output, profile data, binding data,
  or caller metadata.
- Generated FCPXML contains caller-supplied local source file URIs and should
  remain under the same local-media custody as those sources.
- Automated DTD verification uses the installed FCPXML 1.14 DTD through its
  percent-encoded `file:` URI. Passing an unescaped application path containing
  spaces to `xmllint --dtdvalid` does not resolve as a DTD URI.
- A passing structural and DTD check does not claim that a Final Cut GUI import
  or round trip ran.

## Local transcription

- `tritrack transcribe --help` is the command authority for Task 7 flags.
- The caller supplies repeatable local media paths, one readable local
  whisper.cpp model, an explicit lowercase two- or three-letter language code,
  and one absent output path. TriTrack does not bundle or download a model.
- The fixed `whisper-cpp-cpu-no-fallback-v1` profile normalizes each source to
  temporary mono 16 kHz signed 16-bit PCM through bounded FFmpeg, then invokes
  `whisper-cli` exactly once with zero temperature, zero temperature increment,
  engine fallback disabled, and GPU decoding disabled. It sends no prompt,
  translation request, provider request, or network request.
- Raw engine JSON is an untrusted temporary side effect with a 16 MiB limit.
  Only the observed language, integer offsets, and cue text enter the strict
  canonicalizer. The temporary directory is removed after success or failure.
- The canonical `transcript-bundle-v1` records the fixed profile ID, sanitized
  engine version, model SHA-256, source SHA-256, stable basename-scoped take
  identities, stable cue IDs, and integer-millisecond cue timing. It records no
  absolute paths, temporary paths, logs, execution duration, or credentials.
- Input hashes are checked before and after local processing. Any media or
  model change fails closed. Output publication uses the same absent-path,
  temporary-file, hard-link race boundary as synchronization and FCPXML output.
- A final cue may exceed the decoded PCM duration by at most 5,000 ms to match
  observed whisper.cpp tail padding; only that final end is clipped to the real
  duration. Other invalid or non-monotonic timing fails closed.
- Exact `[BLANK_AUDIO]` evidence becomes an empty take only after the normalized
  PCM has independently been proven byte-zero. Non-silent empty evidence and
  any text over proven silence fail closed. This is a deterministic outcome
  rule, not a semantic claim about transcription accuracy.
- The bundle contains local transcript text and media basenames. Keep it under
  the same custody as source media. `--json` prints only counts and the bundle
  SHA-256.

## Local text alignment

- `tritrack align --help` is the command authority for the local Task 8 flags.
- The command consumes one strict `transcript-bundle-v1`, one strict
  `text-revision-v1` bound to the exact source bytes, and one absent output
  path. It makes no subprocess or network request.
- Revisions address existing take and cue IDs. Promotion preserves take IDs,
  source hashes, status, cue IDs, and integer-millisecond timing. Unknown or
  duplicate addresses, source or language mismatch, invalid normalized text,
  and attempts to edit empty takes fail closed.
- `aligned-transcript-v1` records the exact source-bundle and revision-file
  SHA-256 values. Inputs are rehashed before atomic publication. Repeating the
  operation with the same exact inputs produces identical artifact bytes.
- All three artifacts contain transcript text and remain under the same local
  custody as the source media. `--json` prints only counts and the aligned
  artifact SHA-256.

## Offline provider conformance

- `tritrack hybrid --help` is the command authority for the optional Task 8
  flags. It performs offline validation only and has no network access.
- The caller supplies the same transcript and revision, one strict
  `provider-receipt-v1` per revised take, an exact provider model ID, and one
  absent output path. The command cannot create receipts and reads no
  credential or environment secret.
- Every receipt must uniquely bind the exact bundle, revised take, source audio
  hash, requested and observed Gemini model, completed request and upload, 2xx
  response, and attempted plus confirmed 2xx server-file deletion. Missing,
  extra, duplicate, malformed, changed, failed, or privacy-incomplete evidence
  fails closed before publication.
- Conformant evidence flows through the same local alignment builder and
  publisher, so local and offline-hybrid promotion are byte-identical for the
  same exact transcript and revision files. The live network-capable
  `gemini_transcribe.mjs` component remains planned.

## Local paper edit and organization

- `tritrack paper export --help`, `tritrack paper apply --help`, and
  `tritrack organize --help` are the command authorities for Task 9 flags.
- Export reads one strict `aligned-transcript-v1` and optionally one canonical
  `grouping-v1`, then creates one absent XLSX workbook. Apply reopens the exact
  aligned bytes and one bounded regular non-symlink workbook, re-derives every
  cue/display/manifest value, and creates one absent canonical grouping JSON.
- The workbook has exactly four worksheets: visible `Cues`, `Questions`, and
  `Selections`, plus hidden `_TriTrack`. Hidden state is a usability aid, not a
  security boundary. Formula cells anywhere in the accepted sheets fail
  closed; cell hyperlinks, external workbook links, macros, merged cells,
  defined names, and structural drift also fail closed. Formula-looking
  transcript text is stored as a literal string.
- `grouping-v1` is exact-byte bound to the aligned authority and contains only
  cue-addressed editor intent. `working-cut-v1` is exact-byte bound to both
  aligned and grouping inputs and copies source hashes and millisecond timing
  only from aligned cues. Neither artifact creates a second transcript
  authority.
- The grouping fixpoint is exact canonical JSON bytes. XLSX ZIP-byte identity
  is not promised; repeated export instead guarantees the same logical grids,
  and subsequent apply returns the same grouping bytes.
- Task 9 performs no network access, provider call, credential lookup, media
  processing, subprocess invocation, FCPXML emission, or Task 10 orchestration.
- JSON inputs are bounded to 16 MiB and compressed XLSX inputs to 64 MiB.
  Workbook ZIP preflight additionally caps 512 members, 256 MiB total expanded
  bytes, and 128 MiB per member before openpyxl parsing. Worksheet rows and
  columns are capped from the exact aligned cue count before rectangular cell
  inspection. Inputs are rehashed before temporary-file plus hard-link
  publication; existing outputs and race winners are never overwritten.

## Immutable local run workflow

- `tritrack run prepare --help`, `tritrack run align --help`,
  `tritrack run finish --help`, and `tritrack run status --help` are the
  installed command authorities for Task 10 flags.
- `prepare`, `align`, and `finish` each publish a new absent directory. A
  bundle is complete only when its canonical `run-manifest.json` is present,
  lists the exact phase-specific filenames and hashes, and chains the exact
  prior manifest hashes. Publication reserves the directory, hard-links
  artifacts, and links the manifest last. No command overwrites or repairs an
  earlier bundle.
- Prepared bundles contain doctor, sync-map, transcript-bundle, and string-out
  artifacts. Aligned bundles contain aligned-transcript and paper-workbook
  artifacts. Finished bundles contain grouping, working-cut, and story-cut
  artifacts. Manifests contain no timestamp, mutable stage status, absolute
  path, transcript text, editor text, command arguments, logs, or credentials.
- `prepare` calls the existing doctor → sync → transcribe → emit Python
  functions directly. A doctor receipt with `supported: false` stops before
  processing. Declared media basenames are globally unique, transcription
  inputs are a strict subset, and media plus model hashes are rechecked before
  publication.
- `align` requires a complete prepared bundle and one explicit
  `text-revision-v1`. `takes: []` is a valid no-change revision only when the
  editor deliberately supplies it. The emitted workbook remains transport,
  not text, timing, or selection authority.
- `finish` validates the prepared → aligned manifest chain, current media
  hashes, and workbook binding before applying paper intent, compiling the
  working cut, and rendering `story-cut.fcpxml`. Story order, cue text, timing,
  source hashes, sync offsets, and audio-master coverage are re-derived from
  exact strict artifacts; reserve does not enter the active timeline.
- `status` is read-only and reports only run ID, phase, next action, completed
  stage names, and logical artifact hashes. Task 10 makes no network access and
  does not claim a Final Cut GUI import, DTD result, or round trip.
- `skills/tritrack-editing-assistant/SKILL.md` is the separate end-user entry
  point. It uses installed help first and preserves explicit text-revision and
  paper-edit human gates; the repository-local maintainer skill retains all
  development and publication authority.

## Invented quickstart verification

From an editable development installation, run the public Task 6.5 example
with one caller-selected output root that does not already exist:

```bash
venv/bin/python examples/quickstart_demo.py --output .fixture-runs
```

The example creates all invented sources and results below that root, invokes
the installed `tritrack components`, `tritrack sync`, and `tritrack emit`
surfaces through bounded argv-only processes, performs a second emit to an
absent temporary result and compares exact bytes, then removes only that
temporary comparison. The retained output is one strict `sync-map-v1`, one
deterministic FCPXML string-out, and the invented source pair. The output-root
reservation and both public result writers fail closed without overwrite.

The summary reports `dtdValidation: passed` only when the declared perpetual
Final Cut FCPXML 1.14 DTD exists locally and `xmllint` accepts the output. On a
runner without that application it reports `not-available`; this is not DTD or
GUI evidence. Local Task 6.5 acceptance additionally runs:

```bash
venv/bin/python -m unittest tests.test_quickstart_demo -v
venv/bin/python -m unittest discover -s tests -v
venv/bin/ruff check src tests examples
venv/bin/python -m compileall -q src tests examples
```

## Final Cut Pro verification target

The current compatibility evidence targets:

- application: `/Applications/Final Cut Pro.app`
- bundle identifier: `com.apple.FinalCut`
- version: `12.3`

A separately installed subscription application may register bundle identifier
`com.apple.FinalCutApp`. It is outside the current compatibility evidence.
Never rely on Finder's default file association. For GUI verification, launch
the declared application explicitly by exact bundle identifier or exact
application path, and record that identity in the evidence.

The product doctor reads only the declared perpetual application bundle and
its installed FCPXML DTD. A successful version check does not claim that a GUI
round trip ran; manual Final Cut evidence remains a separate artifact.

## Public remote custody

- Authorization follows the capability-scoped standing-grant model in
  `AGENTS.md`; unchanged authorized actions are not re-approved per task.
- Public `origin`:
  `https://github.com/projectmoonie-creator/TriTrack-Editing-Assistant.git`
- After a coherent package is green, the standing authorization permits a
  fast-forward `main` push to this existing public `origin` and exact remote-SHA
  verification as the off-device Git backup.
- Remote changes, visibility changes, force-push, tags, releases, pull requests,
  tester contact, package publication, and application submission have not yet
  been granted. If later granted for an unchanged scope, that grant persists
  until revoked.
--- END FILE docs/TOOLING.md ---

--- BEGIN FILE docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md ---
# Task 12 alpha-freeze and independent-review design

Decision date: 2026-08-18

Decision owner: producer

Selected option: A — two-layer Git freeze with a package-neutral evidence
epilogue

Starting public candidate:
`71d719770f5b335ecd2f5f31ce98ea886e76b955`

## Decision

Task 12 freezes and independently reviews the public alpha without creating a
tag, release, package upload, signature, attestation, or second package
authority.

The design names two exact Git commits with different roles:

1. `alphaReviewTarget` is the clean immutable commit whose complete public
   engine, package, tests, contracts, CI, selected packaged documentation, and
   Task 12 review boundary are independently assessed.
2. `alphaEvidenceRecord` is a later commit that adds only public-safe review
   evidence, adjudication, verification, current status, and the status
   regression. It points back to `alphaReviewTarget` and never claims that an
   external reviewer saw its own answer.

The split is mandatory because a Git commit cannot contain the result of a
review of that same commit without changing its identity. The later evidence
record is not silently relabelled as the external review target.

Task 11's existing `scripts/release_gate.py` remains the only maintainer
packaging authority. Task 12 adds no runtime command, JSON contract, validator,
package format, CI job, component, tag, audit branch, Git note, or release
workflow.

## Freeze identities

### `alphaReviewTarget`

The review target is one exact clean commit on the isolated Task 12 branch. It
must contain:

- the complete Tasks 1–11 public implementation and tests;
- the selected Task 12 design and execution plan;
- the final intended Task 12-neutral bytes of every document that enters the
  wheel or sdist; and
- a status-neutral roadmap sequence that remains true before and after Task 12
  completion while `STATUS.md` continues to own the current gate.

Before the target is declared, the full suite, Ruff, compilation, project
identity, both canonical skill validators, package policy, `git diff --check`,
and the existing release gate must pass from the clean commit.

The target identity is its full Git commit SHA-1. The local release manifest
for that commit additionally records the exact project version, tracked-source
inventory, toolchain, wheel SHA-256 and member inventory, sdist SHA-256 and
normalized member inventory, passed gates, and explicit non-claims.

### `alphaEvidenceRecord`

The evidence record may add or change only package-excluded public evidence:

- `docs/reviews/task-12-*` public-safe packets, responses, ledgers, and
  adjudication;
- `docs/TASK-12-VERIFICATION.md`;
- `STATUS.md`; and
- `tests/test_maintainer_boundary.py`, solely to require Tasks 1–12 complete
  and Task 13 next.

Under the current package contract, `docs/reviews/` and
`docs/superpowers/plans/` are pruned, `docs/TASK-12-VERIFICATION.md` and
`STATUS.md` are not selected sdist members, and
`tests/test_maintainer_boundary.py` is explicitly excluded. None enters the
wheel.

If any post-review change touches runtime source, a packaged test, contract,
package policy, CI, README, changelog, tooling, roadmap, selected verification,
or another wheel／sdist member, it is not an evidence epilogue. The old target
is superseded, the changed commit becomes a new candidate, and the relevant
review and gate steps repeat.

## Package-neutrality proof

Run the release gate once at `alphaReviewTarget` and once at the clean
`alphaEvidenceRecord`. The evidence epilogue is package-neutral only when:

- the wheel SHA-256 values are exactly equal;
- the wheel member-inventory SHA-256 values are exactly equal;
- the sdist normalized member-inventory SHA-256 values are exactly equal;
- the sdist member counts are equal; and
- the selected runtime `src/` tree hash is equal.

Compressed sdist byte equality is not required because the existing project
does not claim it. The second `release-manifest.json` is expected to differ:
its candidate commit and tracked-source inventory honestly describe the later
evidence record. Task 12 must not mistake manifest inequality for package
drift, nor mistake package equality for Git-tree equality.

If the wheel or normalized sdist contents differ, the epilogue fails closed.
The final commit is then a new alpha candidate, not merely a record, and must be
reviewed as such.

## Frozen review packet

One path-safe packet is built after the review target commit exists. It names
the exact full target SHA and packet SHA-256 and includes:

- objective, scope, decision, non-goals, and requested finding schema;
- public project identity, version, clean-state facts, Git inventory digest,
  and selected current file contents;
- the Task 12 design and package-membership boundary;
- current release-manifest facts and the exact local gate result;
- exact fixed CI matrix, action pins, permissions, and last known baseline run;
- current public command／authority map and eleven-component registry;
- strict cross-task invariants and explicit claim／non-claim boundaries;
- prior independent-review outcomes, including incomplete provider lanes;
- targeted source, schema, package, CI, governance, and test excerpts needed to
  support file-and-line findings; and
- instructions for a read-only review of the exact checkout.

The packet does not include credentials, absolute home paths, ignored raw
artifacts, local media, transcripts, workbooks, FCPXML with private URIs,
provider prompts from another project, private repositories, or proprietary
templates. It is bounded for reviewer attention and focuses on compositional
seams rather than reproducing every historical packet.

The exact packet sent to providers is preserved publicly after adjudication.
Raw transport envelopes and transient local release artifacts remain ignored.

## Independent-review sequence

The first round is isolated:

1. Codex reviews the frozen target and records findings before reading an
   external answer.
2. Gemini receives the exact same frozen packet once through the controlled
   REST wrapper with dynamic highest-eligible released-model routing.
3. Claude receives the exact same frozen packet once through the registered
   subscription-only wrapper and dynamic `opus` capability request.

Every provider lane records requested, observed, and completed model IDs,
invocation lane, packet hash, attempt state, usage when available, result, and
failure class. A timeout, quota error, authentication failure, empty answer,
missing exact provenance, or ambiguous dispatch is `incomplete`, not a clean
review and not a finding.

There is no provider substitution. Claude never uses an API credential, PAYG,
Console credit, extra usage, direct standalone print mode, downgrade, or retry
after an ambiguous dispatch. Historical model IDs are provenance only.

## Review dimensions

The independent reviewers inspect the whole alpha composition across these
dimensions:

1. component registry and implemented／planned truth;
2. exact authority ownership across sync map, transcript, revision, aligned
   transcript, grouping, working cut, run manifests, workbook, and FCPXML;
3. local-first, no-network, credential, subprocess, source-immutability, and
   no-overwrite boundaries;
4. deterministic timing, ordering, canonical bytes, exact hashes, and
   cross-artifact binding;
5. four validator scopes, stable errors, read-only behavior, and claim limits;
6. run-bundle manifest chains, fixed members, manifest-last publication, and
   interruption／race behavior;
7. source privacy, archive safety, package membership, reproducibility, fresh
   wheel installation, and release-manifest authority;
8. fixed CI matrix, pinned Actions, permissions, installed-wheel smoke, and no
   artifact publication;
9. public documentation, role firewall, maintainer／end-user skill separation,
   compatibility claims, and outward-action boundary; and
10. test gaps and cross-task seams not already covered by incremental reviews.

Reviewers return only actionable findings with severity, confidence, current
file-and-line evidence, impact, and smallest safe fix. Optional observations
remain clearly separate from blockers.

## Adjudication and fix-forward

Codex checks every external statement against the frozen source, tests, and
reproducible behavior. Each item is classified exactly as `agree`, `upgrade`,
`downgrade`, `reject`, or `already-fixed`.

An ordinary agreed defect is fixed forward under the standing grant:

1. add or identify an observed failing regression;
2. record the RED behavior;
3. implement the smallest in-scope correction;
4. run the focused GREEN set and full public gates; and
5. determine whether the changed bytes supersede `alphaReviewTarget`.

A reviewer headline never overrides source-backed findings, and an optional
observation is not ignored merely because the headline says `NO FINDINGS`.

A true public-contract gap, private-data requirement, remote／visibility
change, or separately gated outward action stops the task for producer
direction. Ordinary code, test, and documentation fixes do not trigger another
authorization request.

## Public evidence record

The tracked Task 12 record contains:

- the exact provider packet;
- Codex's pre-external review;
- each usable public-safe provider answer;
- each machine-readable status ledger;
- an explicit incomplete ledger for every failed lane;
- finding-by-finding adjudication and RED／GREEN evidence;
- `alphaReviewTarget`, fix-forward commits, and `alphaEvidenceRecord` roles;
- both release-gate manifest facts and the package-neutrality comparison;
- complete local test, lint, compilation, identity, skill, and diff results;
  and
- explicit non-claims.

Ignored raw envelopes are never staged. Provider output is sanitized only for
public-path and credential safety; any transformation and resulting tracked
copy hash are disclosed.

## Final local, remote, and CI proof

After the evidence record is committed and the package-neutrality proof passes:

- run the complete suite, Ruff, compilation, identity, both skill validators,
  maintainer boundary, package policy, and `git diff --check`;
- require a clean worktree;
- run the final release gate into one fresh ignored absent directory;
- fast-forward local `main` without a merge commit;
- push only `main` to the existing public `origin`;
- prove local `HEAD`, `origin/main`, and remote `refs/heads/main` are identical;
  and
- require all six CI jobs at that exact pushed SHA to pass.

The final GitHub Actions run ID belongs in the handoff only. Editing a tracked
file to embed it would create another candidate and another CI run.

## Completion definition

Task 12 is complete when:

- one exact `alphaReviewTarget` is frozen from a clean full-gate commit;
- Codex completes first and both external lanes have truthful completed or
  incomplete ledgers;
- every finding is adjudicated and every ordinary agreed defect is fixed with
  regression evidence;
- one exact `alphaEvidenceRecord` preserves the public evidence without
  pretending to be the external review target;
- the evidence epilogue proves exact wheel and normalized sdist content
  invariance or supersedes and re-reviews the candidate;
- the final release gate passes;
- public `main` and the remote backup match the exact green evidence commit;
- all six exact-SHA CI jobs pass; and
- `STATUS.md` records Tasks 1–12 complete with Task 13 next.

## Explicit non-claims

Task 12 does not create or authorize a tag, GitHub Release, package
publication, tester outreach, signing, attestation, SBOM, PR, application
submission, Final Cut GUI operation, DTD claim, live provider transport,
private downstream integration, force-push, remote change, or visibility
change. It does not declare production stability or solve Task 13.

## Brainstorm provenance

The frozen problem-frame SHA-256 was
`afdcba263df1dfd2bd54f484e6638a8b52c33fe3dfe9240eab893cb38f474657`.
Codex completed before external output; response SHA-256 was
`eced0a2adc2fc2bf381013023483e04c712f2d41f4b29890e6bd6e51edeaa466`.

Gemini requested, observed, and completed `gemini-3.7-flash`; response SHA-256
was `9e54a5b8bdec883eda872b8933a1339f9a10a55b957e09e11748f7670f1b0f4c`.

Claude's subscription-only attempt
`2f5e3114-392c-48df-8f76-eea51b9bf033` requested dynamic `opus` and ended
`claude-timeout`. Observed／completed models, usage, raw output, and completion
time are null; `modelRequestSent` is unknown. There was no retry, downgrade,
paid credential, API／PAYG／extra-usage route, or provider substitution. Its
status-ledger SHA-256 is
`b32d0a4b177ccfe5d8e0978d8b6f4eed1c44bbcdbd2039a7614329ddf1844030`.

The producer selected Option A on 2026-08-18.
--- END FILE docs/superpowers/specs/2026-08-18-task-12-alpha-freeze-design.md ---

--- BEGIN FILE pyproject.toml ---
[build-system]
requires = ["setuptools==84.0.0"]
build-backend = "setuptools.build_meta"

[project]
name = "tritrack-editing-assistant"
version = "0.1.0a0"
description = "Local-first editing-assistant building blocks for Final Cut Pro workflows"
readme = "README.md"
requires-python = ">=3.12,<3.14"
license = "Apache-2.0"
authors = [
  { name = "Hsin-Hsin Yuan" },
]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Operating System :: MacOS",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
]
dependencies = [
  "jsonschema>=4.23,<5",
  "numpy>=2,<3",
  "openpyxl>=3.1,<4",
]

[project.scripts]
tritrack = "tritrack_editing_assistant.cli:main"

[project.optional-dependencies]
dev = ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
tritrack_editing_assistant = [
  "schemas/*.json",
  "profiles/*.json",
  "providers/*.mjs",
]

[tool.ruff]
line-length = 88
target-version = "py312"
--- END FILE pyproject.toml ---

--- BEGIN FILE MANIFEST.in ---
include README.md
include LICENSE
include NOTICE
include CHANGELOG.md
include CONTRIBUTING.md
include SECURITY.md
include CODE_OF_CONDUCT.md
include pyproject.toml
include MANIFEST.in
include .github/workflows/ci.yml
include docs/ROADMAP.md
include docs/TASK-11-VERIFICATION.md
include docs/TOOLING.md
include docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md
recursive-include examples *.py
recursive-include skills/tritrack-editing-assistant *.md *.yaml
include scripts/capture_basic_title_binding.py
include scripts/release_gate.py
include scripts/release_gate_core.py
recursive-include release *.json
recursive-include requirements *.txt
recursive-include src/tritrack_editing_assistant *.py *.json *.mjs
recursive-include tests *.py
exclude tests/test_maintainer_boundary.py
prune .agents
prune .release-evidence
prune build
prune dist
prune docs/reviews
prune docs/superpowers/plans
global-exclude *.py[cod]
global-exclude .DS_Store
global-exclude __pycache__
--- END FILE MANIFEST.in ---

--- BEGIN FILE release/package-policy-v1.json ---
{
  "schemaVersion": "tritrack.package-policy/v1",
  "build": {
    "sourceDateEpoch": 1704067200
  },
  "limits": {
    "sourceMaxFiles": 4096,
    "sourceMaxFileBytes": 2097152,
    "sourceMaxTotalBytes": 134217728,
    "archiveMaxBytes": 67108864,
    "archiveMaxMembers": 2048,
    "memberMaxBytes": 33554432,
    "expandedMaxBytes": 268435456
  },
  "source": {
    "allowedFakeHomeUsers": [
      "editor",
      "example",
      "fake",
      "test"
    ],
    "allowedFakeSecretValues": [
      "example",
      "fake",
      "placeholder",
      "redacted",
      "secret",
      "test"
    ],
    "forbiddenSuffixes": [
      ".aac",
      ".aif",
      ".aiff",
      ".avi",
      ".fcpxmld",
      ".m4a",
      ".m4v",
      ".mkv",
      ".mov",
      ".mp3",
      ".mp4",
      ".wav",
      ".xlsx"
    ]
  },
  "wheel": {
    "expectedMembers": [
      "tritrack_editing_assistant-0.1.0a0.dist-info/METADATA",
      "tritrack_editing_assistant-0.1.0a0.dist-info/RECORD",
      "tritrack_editing_assistant-0.1.0a0.dist-info/WHEEL",
      "tritrack_editing_assistant-0.1.0a0.dist-info/entry_points.txt",
      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/LICENSE",
      "tritrack_editing_assistant-0.1.0a0.dist-info/licenses/NOTICE",
      "tritrack_editing_assistant-0.1.0a0.dist-info/top_level.txt",
      "tritrack_editing_assistant/__init__.py",
      "tritrack_editing_assistant/align_text.py",
      "tritrack_editing_assistant/cli.py",
      "tritrack_editing_assistant/contracts.py",
      "tritrack_editing_assistant/doctor.py",
      "tritrack_editing_assistant/emit_fcpxml.py",
      "tritrack_editing_assistant/gemini_hybrid.py",
      "tritrack_editing_assistant/hallucination.py",
      "tritrack_editing_assistant/organizer.py",
      "tritrack_editing_assistant/paper_edit.py",
      "tritrack_editing_assistant/process.py",
      "tritrack_editing_assistant/profiles/__init__.py",
      "tritrack_editing_assistant/profiles/basic-title-v1.json",
      "tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
      "tritrack_editing_assistant/run_workflow.py",
      "tritrack_editing_assistant/schemas/__init__.py",
      "tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
      "tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
      "tritrack_editing_assistant/schemas/grouping-v1.schema.json",
      "tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
      "tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
      "tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
      "tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
      "tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
      "tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
      "tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
      "tritrack_editing_assistant/story_fcpxml.py",
      "tritrack_editing_assistant/string_out.py",
      "tritrack_editing_assistant/sync_scan.py",
      "tritrack_editing_assistant/transcribe_takes.py",
      "tritrack_editing_assistant/validate_artifacts.py"
    ]
  },
  "sdist": {
    "root": "tritrack_editing_assistant-0.1.0a0/",
    "expectedMembers": [
      ".github/workflows/ci.yml",
      "CHANGELOG.md",
      "CODE_OF_CONDUCT.md",
      "CONTRIBUTING.md",
      "LICENSE",
      "MANIFEST.in",
      "NOTICE",
      "PKG-INFO",
      "README.md",
      "SECURITY.md",
      "docs/ROADMAP.md",
      "docs/TASK-11-VERIFICATION.md",
      "docs/TOOLING.md",
      "docs/superpowers/specs/2026-08-17-task-11-release-readiness-design.md",
      "examples/quickstart_demo.py",
      "pyproject.toml",
      "release/package-policy-v1.json",
      "release/release-manifest-v1.schema.json",
      "requirements/ci-constraints.txt",
      "scripts/capture_basic_title_binding.py",
      "scripts/release_gate.py",
      "scripts/release_gate_core.py",
      "setup.cfg",
      "skills/tritrack-editing-assistant/SKILL.md",
      "skills/tritrack-editing-assistant/agents/openai.yaml",
      "src/tritrack_editing_assistant.egg-info/PKG-INFO",
      "src/tritrack_editing_assistant.egg-info/SOURCES.txt",
      "src/tritrack_editing_assistant.egg-info/dependency_links.txt",
      "src/tritrack_editing_assistant.egg-info/entry_points.txt",
      "src/tritrack_editing_assistant.egg-info/requires.txt",
      "src/tritrack_editing_assistant.egg-info/top_level.txt",
      "src/tritrack_editing_assistant/__init__.py",
      "src/tritrack_editing_assistant/align_text.py",
      "src/tritrack_editing_assistant/cli.py",
      "src/tritrack_editing_assistant/contracts.py",
      "src/tritrack_editing_assistant/doctor.py",
      "src/tritrack_editing_assistant/emit_fcpxml.py",
      "src/tritrack_editing_assistant/gemini_hybrid.py",
      "src/tritrack_editing_assistant/hallucination.py",
      "src/tritrack_editing_assistant/organizer.py",
      "src/tritrack_editing_assistant/paper_edit.py",
      "src/tritrack_editing_assistant/process.py",
      "src/tritrack_editing_assistant/profiles/__init__.py",
      "src/tritrack_editing_assistant/profiles/basic-title-v1.json",
      "src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json",
      "src/tritrack_editing_assistant/run_workflow.py",
      "src/tritrack_editing_assistant/schemas/__init__.py",
      "src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/grouping-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json",
      "src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json",
      "src/tritrack_editing_assistant/story_fcpxml.py",
      "src/tritrack_editing_assistant/string_out.py",
      "src/tritrack_editing_assistant/sync_scan.py",
      "src/tritrack_editing_assistant/transcribe_takes.py",
      "src/tritrack_editing_assistant/validate_artifacts.py",
      "tests/task9_fixtures.py",
      "tests/test_align_text.py",
      "tests/test_cli.py",
      "tests/test_contracts.py",
      "tests/test_doctor.py",
      "tests/test_emit_fcpxml.py",
      "tests/test_gemini_hybrid.py",
      "tests/test_hallucination.py",
      "tests/test_organizer.py",
      "tests/test_packaging.py",
      "tests/test_paper_edit.py",
      "tests/test_process.py",
      "tests/test_quickstart_demo.py",
      "tests/test_release_gate.py",
      "tests/test_release_ci.py",
      "tests/test_run_workflow.py",
      "tests/test_story_fcpxml.py",
      "tests/test_string_out.py",
      "tests/test_sync_scan.py",
      "tests/test_title_binding.py",
      "tests/test_transcribe_takes.py",
      "tests/test_validate_artifacts.py"
    ]
  }
}
--- END FILE release/package-policy-v1.json ---

--- BEGIN FILE release/release-manifest-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.example/schemas/release-manifest-v1.schema.json",
  "title": "TriTrack release manifest v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "project",
    "sourceInventory",
    "toolchain",
    "platform",
    "artifacts",
    "reproducibility",
    "gates",
    "nonClaims"
  ],
  "properties": {
    "schemaVersion": {
      "const": "tritrack.release-manifest/v1"
    },
    "project": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "version", "commit"],
      "properties": {
        "name": {"const": "tritrack-editing-assistant"},
        "version": {"type": "string", "minLength": 1},
        "commit": {"type": "string", "pattern": "^[0-9a-f]{40}$"}
      }
    },
    "sourceInventory": {
      "type": "object",
      "additionalProperties": false,
      "required": ["count", "sha256"],
      "properties": {
        "count": {"type": "integer", "minimum": 1},
        "sha256": {"$ref": "#/$defs/sha256"}
      }
    },
    "toolchain": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "python",
        "implementation",
        "pip",
        "build",
        "setuptools",
        "wheel"
      ],
      "properties": {
        "python": {"type": "string", "minLength": 1},
        "implementation": {"const": "CPython"},
        "pip": {"type": "string", "minLength": 1},
        "build": {"type": "string", "minLength": 1},
        "setuptools": {"type": "string", "minLength": 1},
        "wheel": {"type": "string", "minLength": 1}
      }
    },
    "platform": {
      "type": "object",
      "additionalProperties": false,
      "required": ["system", "machine"],
      "properties": {
        "system": {"enum": ["Darwin", "Linux"]},
        "machine": {"enum": ["arm64", "x86_64"]}
      }
    },
    "artifacts": {
      "type": "object",
      "additionalProperties": false,
      "required": ["wheel", "sdist"],
      "properties": {
        "wheel": {"$ref": "#/$defs/artifact"},
        "sdist": {"$ref": "#/$defs/artifact"}
      }
    },
    "reproducibility": {
      "type": "object",
      "additionalProperties": false,
      "required": ["wheelBytesMatch", "sdistMembersMatch"],
      "properties": {
        "wheelBytesMatch": {"const": true},
        "sdistMembersMatch": {"const": true}
      }
    },
    "gates": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sourceIdentity",
        "sourcePrivacy",
        "wheelArchive",
        "sdistArchive",
        "freshInstall"
      ],
      "properties": {
        "sourceIdentity": {"const": "pass"},
        "sourcePrivacy": {"const": "pass"},
        "wheelArchive": {"const": "pass"},
        "sdistArchive": {"const": "pass"},
        "freshInstall": {"const": "pass"}
      }
    },
    "nonClaims": {
      "type": "array",
      "minItems": 2,
      "uniqueItems": true,
      "items": {
        "enum": [
          "no-tag",
          "no-release",
          "no-package-publication",
          "no-pull-request",
          "no-tester-contact",
          "no-signing",
          "no-attestation",
          "no-sbom",
          "no-final-cut-gui",
          "no-dtd",
          "no-provider",
          "no-application-submission"
        ]
      }
    }
  },
  "$defs": {
    "sha256": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "artifact": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "sha256",
        "sizeBytes",
        "memberCount",
        "memberInventorySha256"
      ],
      "properties": {
        "sha256": {"$ref": "#/$defs/sha256"},
        "sizeBytes": {"type": "integer", "minimum": 1},
        "memberCount": {"type": "integer", "minimum": 1},
        "memberInventorySha256": {"$ref": "#/$defs/sha256"}
      }
    }
  }
}
--- END FILE release/release-manifest-v1.schema.json ---

--- BEGIN FILE .github/workflows/ci.yml ---
name: Release-grade public Python CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test-matrix:
    name: ${{ matrix.os }} / Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-24.04
            python-version: "3.12"
            architecture: x64
          - os: ubuntu-24.04
            python-version: "3.13"
            architecture: x64
          - os: macos-26
            python-version: "3.12"
            architecture: arm64
          - os: macos-26
            python-version: "3.13"
            architecture: arm64
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up fixed Python cell
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: ${{ matrix.python-version }}
          architecture: ${{ matrix.architecture }}
      - name: Install constrained source and development checks
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Run complete public tests
        run: python -m unittest discover -s tests -v
      - name: Compile public Python surfaces
        run: python -m compileall -q src tests examples scripts
      - name: Build and smoke the local wheel in a new environment
        shell: bash
        run: |
          wheel_dir="$RUNNER_TEMP/tritrack-wheel-dist"
          smoke_dir="$RUNNER_TEMP/tritrack-wheel-smoke"
          test ! -e "$wheel_dir"
          test ! -e "$smoke_dir"
          python -m build --wheel --no-isolation --outdir "$wheel_dir"
          python -m venv "$smoke_dir"
          smoke_python="$smoke_dir/bin/python"
          smoke_cli="$smoke_dir/bin/tritrack"
          "$smoke_python" -m pip install --constraint requirements/ci-constraints.txt pip
          wheels=("$wheel_dir"/*.whl)
          test "${#wheels[@]}" -eq 1
          "$smoke_python" -m pip install "${wheels[0]}"
          "$smoke_python" -m pip check
          "$smoke_cli" components --json
          "$smoke_cli" validate --help
          "$smoke_cli" validate contract --help
          "$smoke_cli" validate fcpxml --help
          "$smoke_cli" validate paper --help
          "$smoke_cli" validate run --help

  quality:
    name: Public quality and policy contracts
    runs-on: ubuntu-24.04
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python 3.13
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: "3.13"
          architecture: x64
      - name: Install constrained source and development checks
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Lint every public Python surface
        run: ruff check src tests examples scripts
      - name: Verify public role, package, and CI contracts
        run: python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v
      - name: Verify public project identity
        run: python .agents/skills/tritrack-editing-assistant-maintainer/scripts/check_project_identity.py --root .

  release-gate:
    name: Local candidate gate without publication
    runs-on: ubuntu-24.04
    steps:
      - name: Check out exact source
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - name: Set up Python 3.13
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0
        with:
          python-version: "3.13"
          architecture: x64
      - name: Install exact gate toolchain
        run: |
          python -m pip install --constraint requirements/ci-constraints.txt pip setuptools
          python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'
      - name: Run the maintainer release-readiness gate locally
        run: |
          mkdir -p .release-evidence
          python scripts/release_gate.py --source . --output .release-evidence/ci
--- END FILE .github/workflows/ci.yml ---

--- BEGIN FILE .agents/skills/tritrack-editing-assistant-maintainer/SKILL.md ---
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
   task. Keep implementation off `main`; integrate a fully green candidate
   only under the recorded standing grant.
5. State the public candidate commit, active task, next action, applicable
   standing grants, and exact verification evidence to be produced.

## Hold the role firewall

- This skill owns public repository development and maintenance only.
- `skills/tritrack-editing-assistant/SKILL.md` is the separate installed
  end-user product skill. Keep maintainer state, task numbers, release
  authority, and application strategy out of it.
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

## Apply standing authorization

Producer authorization is a capability-scoped standing grant. Once a
capability is explicitly authorized or recorded in the public governance, it
remains authorized for the same target, visibility, scope, and risk.
The grant remains effective until the producer revokes it.
Do not request it again, pause at that gate, or treat a new task as implicit
revocation.

Request a new authorization only for a capability that has never been granted
or for a material change in target, visibility, scope, or risk. Destructive
history changes, credential or private-data disclosure, and a different remote
are material changes rather than repetitions.

The current standing grant covers closeout review, fix-forward of ordinary
in-scope findings, fast-forward integration of a fully green candidate, and
pushing `main` to the existing public `origin` with exact remote-SHA backup
verification. Force-push, tags, releases, pull requests, tester contact,
package publication, and application submission have not yet been granted.
Never manufacture issues, adoption, downloads, or maintenance activity.

## Close the OSS lane

Run focused tests, the full suite, lint, skill validation, boundary tests, and
`git diff --check`. Read back the resulting files and status. Update public
`STATUS.md` only after the coherent public package is green. Commit only files
owned by the public task. Treat requested implementation as including closeout
review and fix-forward until ordinary in-scope findings are resolved; stop only
for a true public-contract gap, unsafe scope expansion, or a separately gated
action.

For a release-readiness task, run the maintainer-only gate exactly as:

```text
python scripts/release_gate.py --source . --output ABSENT_DIRECTORY
```

The source must be a clean public-engine／OSS Git toplevel and the output must
be absent. Treat only a canonical manifest linked after both inspected archives
as a complete local candidate. This gate does not grant any outward action
excluded by the standing authorization above.
--- END FILE .agents/skills/tritrack-editing-assistant-maintainer/SKILL.md ---

--- BEGIN FILE skills/tritrack-editing-assistant/SKILL.md ---
---
name: tritrack-editing-assistant
description: Guide an editor or terminal-capable agent through TriTrack's installed, local Final Cut workflow. Use when preparing synchronized A/B interview media, reviewing cue-addressed transcript corrections, organizing an edit in the paper workbook, finishing a story-ordered FCPXML, or checking an immutable run bundle.
---

# TriTrack Editing Assistant

Guide the edit through explicit immutable stages. Keep media and editorial
artifacts local, preserve editor intent, and use only the installed `tritrack`
command surface.

## Start help-first

1. Run `tritrack run --help`.
2. Run the selected subcommand's `--help` before naming or using its flags:
   - `tritrack run prepare --help`
   - `tritrack run align --help`
   - `tritrack run finish --help`
   - `tritrack run status --help`
   - `tritrack validate --help`
   - `tritrack validate contract --help`
   - `tritrack validate fcpxml --help`
   - `tritrack validate paper --help`
   - `tritrack validate run --help`
3. Treat installed help as the command authority. Stop if a required command or
   flag is unavailable; do not guess a replacement.

## Preserve local custody

- Keep source media, the local speech model, JSON artifacts, workbook, and
  FCPXML on paths the editor explicitly places in scope.
- Require globally unique media basenames across camera A and camera B.
- Choose only declared camera sources for transcription.
- Use a new absent output directory for every mutating stage. Never overwrite,
  repair, resume, or add files inside an earlier bundle.
- Read sanitized command summaries by default. Inspect transcript or workbook
  content only when the editor explicitly puts that artifact in scope.

## Prepare the synchronized run

Help the editor choose camera roles, transcription sources, spoken language,
public profile and title binding, event and project names, a safe run ID, and an
absent prepared output directory. Then run the installed command in the shape
reported by:

```text
tritrack run prepare --help
```

Confirm that the summary reports `phase: prepared` and
`nextAction: provide-revision`. Do not claim that the string-out is a final
story edit.

## Hold the text-revision human gate

Pause for the editor to review `transcript-bundle.json`. Preserve every cue ID,
source hash, language, and timing. Help encode only corrections the editor
explicitly approves in one strict `tritrack.text-revision/v1` JSON artifact
bound to the exact transcript-bundle bytes.

Never infer approval. Use `takes: []` only after the editor explicitly confirms
that no text changes are wanted. Do not retime, split, merge, translate, or
invent cues.

Run the installed alignment command in the shape reported by:

```text
tritrack run align --help
```

Confirm `phase: aligned` and `nextAction: edit-paper-workbook`.

## Hold the paper-edit human gate

Pause for the editor to edit `paper-edit.xlsx`. Allow edits only in the
`Questions` and `Selections` tables. Keep cue addresses intact and require the
editor to decide active answers, story order, and reserve ranges.

Treat the workbook as transport, not authority. The strict aligned transcript
remains text and timing authority; grouping JSON records editor intent; the
working-cut JSON is the compiled selection authority.

## Finish the story projection

Reuse the exact prepared and aligned bundles, the editor-approved workbook, and
the same local camera sources. Choose a new absent finished output directory.
Run the installed command in the shape reported by:

```text
tritrack run finish --help
```

Confirm `phase: finished` and `nextAction: complete`. Describe
`story-cut.fcpxml` as a deterministic story-ordered projection. Do not claim a
GUI import, application round trip, or external DTD validation unless the
editor separately performs and records it.

## Inspect without mutation

Use the installed read-only command in the shape reported by:

```text
tritrack run status --help
```

Report only the run ID, phase, next action, stage names, logical artifact names,
and hashes. Do not expose local paths, transcript text, question text, notes, or
FCPXML content in a status summary.

## Validate an existing artifact without mutation

Choose one explicit mode from installed help. Do not guess a format or search
nearby paths.

- `contract` returns the exact `contract` scope for one registered JSON
  contract. It does not prove referenced files or cross-file hashes.
- `fcpxml` returns `structural-profile` for the selected installed profile and
  title binding. It does not check source media, a DTD, or a GUI import.
- `paper` returns `authority-bound` for one workbook checked against the exact
  supplied aligned transcript bytes. It does not publish editor intent.
- `run` returns `complete-run-bundle` for one complete immutable bundle and its
  manifest chain.

All four modes are read-only. Validation does not repair an artifact, create an
output, inspect unrelated content, or make a network request. Report success
only inside the returned scope.

## Stop on strict failures

Stop when compatibility, source custody, exact hashes, manifest chain, schema,
workbook integrity, media coverage, or absent-output checks fail. Preserve the
error code and existing files. Do not weaken validation, reconstruct a missing
manifest, or continue from an incomplete bundle.
--- END FILE skills/tritrack-editing-assistant/SKILL.md ---

--- BEGIN FILE src/tritrack_editing_assistant/__init__.py ---
"""TriTrack Editing Assistant public package."""

__version__ = "0.1.0a0"
--- END FILE src/tritrack_editing_assistant/__init__.py ---

--- BEGIN FILE src/tritrack_editing_assistant/cli.py ---
"""Command-line boundary for the TriTrack Editing Assistant scaffold."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from . import align_text as align_module
from . import doctor as doctor_module
from . import emit_fcpxml as emit_module
from . import gemini_hybrid as hybrid_module
from . import organizer as organizer_module
from . import paper_edit as paper_module
from . import run_workflow as run_module
from . import sync_scan as sync_module
from . import transcribe_takes as transcribe_module
from . import validate_artifacts as validate_module

EXIT_OK = 0
EXIT_USAGE = 64
EXIT_DATA = 65
EXIT_DEPENDENCY = 69
EXIT_OUTPUT_EXISTS = 73
EXIT_IO = 74
EXIT_TEMPORARY = 75
EXIT_POLICY = 78


class CliUsageError(ValueError):
    """Private signal for sanitized command-line usage failures."""


class TriTrackArgumentParser(argparse.ArgumentParser):
    """Argument parser that preserves the public exit-code contract."""

    def error(self, message: str) -> None:
        del message
        raise CliUsageError("TRITRACK_USAGE")


COMPONENTS = (
    {
        "sourceComponent": "sync_scan.py",
        "command": "sync",
        "status": "implemented",
    },
    {
        "sourceComponent": "emit_fcpxml.py",
        "command": "emit",
        "status": "implemented",
    },
    {
        "sourceComponent": "transcribe_takes.py",
        "command": "transcribe",
        "status": "implemented",
    },
    {
        "sourceComponent": "string_out.py",
        "command": "emit",
        "status": "implemented",
    },
    {
        "sourceComponent": "hallucination.py",
        "command": "transcribe",
        "status": "implemented",
    },
    {
        "sourceComponent": "organizer.py",
        "command": "organize",
        "status": "implemented",
    },
    {
        "sourceComponent": "paper_edit.py",
        "command": "paper",
        "status": "implemented",
    },
    {
        "sourceComponent": "align_text.py",
        "command": "align",
        "status": "implemented",
    },
    {
        "sourceComponent": "gemini_hybrid.py",
        "command": "hybrid",
        "status": "implemented",
    },
    {
        "sourceComponent": "gemini_transcribe.mjs",
        "command": "hybrid",
        "status": "planned",
    },
    {
        "sourceComponent": "multicam-sync",
        "command": "run",
        "status": "implemented",
    },
)


def _print_components(arguments: argparse.Namespace) -> int:
    payload = {
        "schemaVersion": "tritrack.components/v1",
        "toolVersion": __version__,
        "components": list(COMPONENTS),
    }
    if arguments.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return EXIT_OK

    print("COMPONENT\tCOMMAND\tSTATUS")
    for component in COMPONENTS:
        print(
            f"{component['sourceComponent']}\t"
            f"{component['command']}\t{component['status']}"
        )
    return EXIT_OK


def _planned_command(arguments: argparse.Namespace) -> int:
    print(
        f"TRITRACK_COMMAND_NOT_IMPLEMENTED: {arguments.command}",
        flush=True,
    )
    return EXIT_USAGE


def _print_doctor(arguments: argparse.Namespace) -> int:
    try:
        doctor_arguments = {
            "profile_id": arguments.profile,
            "transcription_requested": arguments.transcription,
            "whisper_model": arguments.whisper_model,
        }
        if arguments.output is None:
            receipt = doctor_module.build_receipt(**doctor_arguments)
        else:
            receipt = doctor_module.write_receipt(arguments.output, **doctor_arguments)
    except ValueError as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return EXIT_OUTPUT_EXISTS if code == "TRITRACK_OUTPUT_EXISTS" else EXIT_POLICY

    if arguments.json or arguments.output is None:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    if receipt["supported"]:
        return EXIT_OK
    checks = receipt["checks"]
    assert isinstance(checks, list)
    if any(check["status"] in {"missing", "unreadable"} for check in checks):
        return EXIT_DEPENDENCY
    return EXIT_POLICY


def _run_sync(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        payload = sync_module.synchronize_and_publish(
            camera_a,
            camera_b,
            profile_id=arguments.profile,
            output_path=arguments.output,
        )
    except ValueError as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code in {
            "TRITRACK_SYNC_PROBE_FAILED",
            "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
        }:
            return EXIT_DEPENDENCY
        return EXIT_DATA

    if arguments.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return EXIT_OK


def _run_emit(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        metadata = emit_module.ProjectMetadata(
            event_name=arguments.event_name,
            project_name=arguments.project_name,
        )
        emit_module.emit_and_publish(
            camera_a,
            camera_b,
            sync_map_path=arguments.sync_map,
            profile_id=arguments.profile,
            binding_id=arguments.binding,
            metadata=metadata,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_SYNC_PROBE_FAILED":
            return EXIT_DEPENDENCY
        if code == "TRITRACK_PROFILE_UNKNOWN":
            return EXIT_POLICY
        return EXIT_DATA
    return EXIT_OK


def _run_transcribe(arguments: argparse.Namespace) -> int:
    try:
        payload = transcribe_module.transcribe_and_publish(
            arguments.media,
            model_path=arguments.model,
            language=arguments.language,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        if code in {
            "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
            "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
            "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
        }:
            return EXIT_DEPENDENCY
        if code in {
            "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
            "TRITRACK_TRANSCRIPT_MEDIA_REQUIRED",
        }:
            return EXIT_USAGE
        return EXIT_DATA

    if arguments.json:
        takes = payload["takes"]
        assert isinstance(takes, list)
        bundle_sha256 = _output_sha256(arguments.output)
        summary = {
            "schemaVersion": "tritrack.transcribe-summary/v1",
            "takeCount": len(takes),
            "completedCount": sum(take["status"] == "completed" for take in takes),
            "emptyCount": sum(take["status"] == "empty" for take in takes),
            "bundleSha256": bundle_sha256,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return EXIT_OK


def _alignment_summary(
    payload: dict[str, object], output_path: Path
) -> dict[str, object]:
    takes = payload["takes"]
    assert isinstance(takes, list)
    cue_count = 0
    revised_cue_count = 0
    for take in takes:
        assert isinstance(take, dict)
        cues = take["cues"]
        assert isinstance(cues, list)
        cue_count += len(cues)
        revised_cue_count += sum(
            isinstance(cue, dict) and cue["disposition"] == "revised"
            for cue in cues
        )
    artifact_sha256 = _output_sha256(output_path)
    return {
        "schemaVersion": "tritrack.align-summary/v1",
        "takeCount": len(takes),
        "cueCount": cue_count,
        "revisedCueCount": revised_cue_count,
        "artifactSha256": artifact_sha256,
    }


def _run_align(arguments: argparse.Namespace) -> int:
    try:
        payload = align_module.align_and_publish(
            arguments.transcript,
            arguments.revision,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        return EXIT_DATA

    if arguments.json:
        print(
            json.dumps(
                _alignment_summary(payload, arguments.output),
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_hybrid(arguments: argparse.Namespace) -> int:
    try:
        payload = hybrid_module.hybrid_and_publish(
            arguments.transcript,
            arguments.proposal,
            arguments.receipt,
            exact_model=arguments.model,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code == "TRITRACK_OUTPUT_PARENT_MISSING":
            return EXIT_IO
        if code == "TRITRACK_HYBRID_MODEL_INVALID":
            return EXIT_USAGE
        return EXIT_DATA

    if arguments.json:
        print(
            json.dumps(
                _alignment_summary(payload, arguments.output),
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_organize(arguments: argparse.Namespace) -> int:
    try:
        payload = organizer_module.organize_and_publish(
            arguments.aligned,
            arguments.grouping,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        if code == "TRITRACK_OUTPUT_EXISTS":
            return EXIT_OUTPUT_EXISTS
        if code in {
            "TRITRACK_OUTPUT_PARENT_MISSING",
            "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
        }:
            return EXIT_IO
        return EXIT_DATA

    if arguments.json:
        questions = payload["questions"]
        segments = payload["segments"]
        reserve = payload["reserve"]
        assert isinstance(questions, list)
        assert isinstance(segments, list)
        assert isinstance(reserve, list)
        artifact_sha256 = _output_sha256(arguments.output)
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.organize-summary/v1",
                    "questionCount": len(questions),
                    "segmentCount": len(segments),
                    "reserveCount": len(reserve),
                    "artifactSha256": artifact_sha256,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _paper_error_exit(code: str) -> int:
    if code == "TRITRACK_OUTPUT_EXISTS":
        return EXIT_OUTPUT_EXISTS
    if code in {
        "TRITRACK_OUTPUT_PARENT_MISSING",
        "TRITRACK_PAPER_INPUT_UNREADABLE",
    }:
        return EXIT_IO
    return EXIT_DATA


def _output_sha256(output_path: Path) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(output_path, flags)
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise OSError("TRITRACK_OUTPUT_UNREADABLE")
        digest = hashlib.sha256()
        total = 0
        remaining = before.st_size + 1
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
            remaining -= len(chunk)
        after = os.fstat(descriptor)
        if (
            total != before.st_size
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
        ):
            raise OSError("TRITRACK_OUTPUT_CHANGED")
        return digest.hexdigest()
    finally:
        os.close(descriptor)


def _run_paper_export(arguments: argparse.Namespace) -> int:
    try:
        summary = paper_module.export_workbook(
            arguments.aligned,
            grouping_path=arguments.grouping,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _paper_error_exit(code)
    if arguments.json:
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.paper-export-summary/v1",
                    **summary,
                    "artifactSha256": _output_sha256(arguments.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_paper_apply(arguments: argparse.Namespace) -> int:
    try:
        grouping = paper_module.apply_workbook(
            arguments.aligned,
            arguments.workbook,
            output_path=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _paper_error_exit(code)
    if arguments.json:
        questions = grouping["questions"]
        reserve = grouping["reserve"]
        assert isinstance(questions, list)
        assert isinstance(reserve, list)
        answer_count = 0
        for question in questions:
            assert isinstance(question, dict)
            answers = question["answers"]
            assert isinstance(answers, list)
            answer_count += len(answers)
        print(
            json.dumps(
                {
                    "schemaVersion": "tritrack.paper-apply-summary/v1",
                    "questionCount": len(questions),
                    "answerCount": answer_count,
                    "reserveCount": len(reserve),
                    "artifactSha256": _output_sha256(arguments.output),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return EXIT_OK


def _run_error_exit(code: str) -> int:
    if code == "TRITRACK_OUTPUT_EXISTS":
        return EXIT_OUTPUT_EXISTS
    if code in {
        "TRITRACK_OUTPUT_PARENT_MISSING",
        "TRITRACK_RUN_INPUT_UNREADABLE",
        "TRITRACK_STORY_SOURCE_UNREADABLE",
        "TRITRACK_ORGANIZER_INPUT_UNREADABLE",
        "TRITRACK_PAPER_INPUT_UNREADABLE",
    }:
        return EXIT_IO
    if code in {
        "TRITRACK_SYNC_PROBE_FAILED",
        "TRITRACK_SYNC_AUDIO_DECODE_FAILED",
        "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED",
        "TRITRACK_TRANSCRIBE_ENGINE_FAILED",
        "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE",
    }:
        return EXIT_DEPENDENCY
    if code in {
        "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED",
        "TRITRACK_PROFILE_UNKNOWN",
    }:
        return EXIT_POLICY
    if code in {
        "TRITRACK_RUN_SOURCE_REQUIRED",
        "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID",
        "TRITRACK_TRANSCRIPT_LANGUAGE_INVALID",
        "TRITRACK_EMIT_METADATA_INVALID",
    }:
        return EXIT_USAGE
    return EXIT_DATA


def _print_run_summary(summary: dict[str, object], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    print(f"RUN\t{summary['runId']}")
    print(f"PHASE\t{summary['phase']}")
    print(f"NEXT\t{summary['nextAction']}")
    print(f"STAGES\t{','.join(summary['stages'])}")
    artifacts = summary["artifacts"]
    assert isinstance(artifacts, dict)
    for logical_name, sha256 in artifacts.items():
        print(f"ARTIFACT\t{logical_name}\t{sha256}")


def _run_prepare(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        summary = run_module.prepare_run(
            camera_a,
            camera_b,
            arguments.transcribe_media,
            model_path=arguments.model,
            language=arguments.language,
            profile_id=arguments.profile,
            binding_id=arguments.binding,
            metadata=emit_module.ProjectMetadata(
                arguments.event_name, arguments.project_name
            ),
            run_id=arguments.run_id,
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_align_bundle(arguments: argparse.Namespace) -> int:
    try:
        summary = run_module.align_run(
            arguments.prepared,
            arguments.revision,
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_finish(arguments: argparse.Namespace) -> int:
    camera_a = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_a
    ]
    camera_b = [
        sync_module.MediaSource(path.name, path) for path in arguments.camera_b
    ]
    try:
        summary = run_module.finish_run(
            arguments.prepared,
            arguments.aligned,
            arguments.workbook,
            camera_a,
            camera_b,
            metadata=emit_module.ProjectMetadata(
                arguments.event_name, arguments.project_name
            ),
            output_dir=arguments.output,
        )
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    if arguments.json:
        _print_run_summary(summary, as_json=True)
    return EXIT_OK


def _run_status(arguments: argparse.Namespace) -> int:
    try:
        summary = run_module.status_run(arguments.run_dir)
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _run_error_exit(code)
    _print_run_summary(summary, as_json=arguments.json)
    return EXIT_OK


def _validate_error_exit(code: str) -> int:
    if code in {
        "TRITRACK_VALIDATE_INPUT_UNREADABLE",
        "TRITRACK_PAPER_INPUT_UNREADABLE",
        "TRITRACK_RUN_INPUT_UNREADABLE",
    }:
        return EXIT_IO
    if code in {
        "TRITRACK_CONTRACT_REGISTRY_INVALID",
        "TRITRACK_PROFILE_UNKNOWN",
        "TRITRACK_TITLE_BINDING_UNKNOWN",
    }:
        return EXIT_POLICY
    return EXIT_DATA


def _print_validation_summary(
    summary: dict[str, object], *, as_json: bool
) -> None:
    if as_json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    print(
        f"VALIDATION\t{summary['artifactKind']}\t"
        f"{summary['validationScope']}"
    )
    hashes = summary["hashes"]
    counts = summary["counts"]
    details = summary["details"]
    assert isinstance(hashes, dict)
    assert isinstance(counts, dict)
    assert isinstance(details, dict)
    for name in sorted(hashes):
        print(f"HASH\t{name}\t{hashes[name]}")
    for name in sorted(counts):
        print(f"COUNT\t{name}\t{counts[name]}")
    for name in sorted(details):
        encoded = json.dumps(
            details[name],
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        print(f"DETAIL\t{name}\t{encoded}")


def _run_validate(arguments: argparse.Namespace) -> int:
    try:
        if arguments.validate_command == "contract":
            summary = validate_module.validate_contract_artifact(
                arguments.artifact
            )
        elif arguments.validate_command == "fcpxml":
            summary = validate_module.validate_fcpxml_artifact(
                arguments.artifact,
                profile_id=arguments.profile,
                binding_id=arguments.binding,
            )
        elif arguments.validate_command == "paper":
            summary = validate_module.validate_paper_artifacts(
                arguments.aligned,
                arguments.workbook,
            )
        elif arguments.validate_command == "run":
            summary = validate_module.validate_run_bundle(arguments.run_dir)
        else:
            raise CliUsageError("TRITRACK_USAGE")
    except (TypeError, ValueError) as error:
        code = str(error).split(":", 1)[0]
        print(json.dumps({"error": code}, ensure_ascii=False))
        return _validate_error_exit(code)
    _print_validation_summary(summary, as_json=arguments.json)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = TriTrackArgumentParser(
        prog="tritrack",
        description="Local-first Final Cut editing-assistant workflow",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    components = subparsers.add_parser(
        "components",
        help="list the eleven workflow components and current status",
    )
    components.add_argument("--json", action="store_true", help="emit JSON")
    components.set_defaults(handler=_print_components)

    doctor = subparsers.add_parser(
        "doctor",
        help="inspect the local compatibility profile and dependencies",
    )
    doctor.add_argument("--profile", required=True, help="closed compatibility profile id")
    doctor.add_argument("--output", type=Path, help="create an absent receipt path")
    doctor.add_argument("--json", action="store_true", help="print the sanitized receipt")
    doctor.add_argument(
        "--transcription",
        action="store_true",
        help="also require a readable local whisper model",
    )
    doctor.add_argument("--whisper-model", type=Path)
    doctor.set_defaults(handler=_print_doctor)

    sync = subparsers.add_parser(
        "sync",
        help="discover and audio-verify A/B camera pairs",
    )
    sync.add_argument(
        "--camera-a",
        action="append",
        required=True,
        type=Path,
        help="local camera-A media path; repeat for each source",
    )
    sync.add_argument(
        "--camera-b",
        action="append",
        required=True,
        type=Path,
        help="local camera-B media path; repeat for each source",
    )
    sync.add_argument("--profile", required=True, help="public compatibility profile id")
    sync.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent sync-map-v1 JSON path",
    )
    sync.add_argument("--json", action="store_true", help="also print the sync map")
    sync.set_defaults(handler=_run_sync)

    emit = subparsers.add_parser(
        "emit",
        help="emit a profile-bound deterministic Final Cut XML string-out",
    )
    emit.add_argument(
        "--camera-a",
        action="append",
        required=True,
        type=Path,
        help="local camera-A media path; repeat for each source",
    )
    emit.add_argument(
        "--camera-b",
        action="append",
        required=True,
        type=Path,
        help="local camera-B media path; repeat for each source",
    )
    emit.add_argument(
        "--sync-map",
        required=True,
        type=Path,
        help="strict sync-map-v1 JSON path",
    )
    emit.add_argument("--profile", required=True, help="public compatibility profile id")
    emit.add_argument("--binding", required=True, help="public title binding id")
    emit.add_argument("--event-name", required=True, help="caller-owned event name")
    emit.add_argument("--project-name", required=True, help="caller-owned project name")
    emit.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent FCPXML path",
    )
    emit.set_defaults(handler=_run_emit)

    transcribe = subparsers.add_parser(
        "transcribe",
        help="transcribe local media with one fixed local decoding profile",
    )
    transcribe.add_argument(
        "--media",
        action="append",
        required=True,
        type=Path,
        help="local media path; repeat for each take",
    )
    transcribe.add_argument(
        "--model",
        required=True,
        type=Path,
        help="caller-owned readable local whisper.cpp model",
    )
    transcribe.add_argument(
        "--language",
        required=True,
        help="explicit two- or three-letter spoken-language code",
    )
    transcribe.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent transcript-bundle-v1 JSON path",
    )
    transcribe.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    transcribe.set_defaults(handler=_run_transcribe)

    align = subparsers.add_parser(
        "align",
        help="promote local cue-addressed text without changing source timing",
    )
    align.add_argument(
        "--transcript",
        required=True,
        type=Path,
        help="strict transcript-bundle-v1 JSON path",
    )
    align.add_argument(
        "--revision",
        required=True,
        type=Path,
        help="strict text-revision-v1 JSON path",
    )
    align.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent aligned-transcript-v1 JSON path",
    )
    align.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    align.set_defaults(handler=_run_align)

    hybrid = subparsers.add_parser(
        "hybrid",
        help="validate optional provider evidence offline",
        description="Offline receipt validation only; no network access.",
    )
    hybrid.add_argument(
        "--transcript",
        required=True,
        type=Path,
        help="strict transcript-bundle-v1 JSON path",
    )
    hybrid.add_argument(
        "--proposal",
        required=True,
        type=Path,
        help="strict text-revision-v1 JSON path",
    )
    hybrid.add_argument(
        "--receipt",
        action="append",
        required=True,
        type=Path,
        help="strict provider-receipt-v1 path; repeat per revised take",
    )
    hybrid.add_argument(
        "--model",
        required=True,
        help="exact provider model recorded in every receipt",
    )
    hybrid.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent aligned-transcript-v1 JSON path",
    )
    hybrid.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    hybrid.set_defaults(handler=_run_hybrid)

    organize = subparsers.add_parser(
        "organize",
        help="compile cue-addressed grouping into a working cut",
    )
    organize.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    organize.add_argument(
        "--grouping",
        required=True,
        type=Path,
        help="strict grouping-v1 JSON path",
    )
    organize.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent working-cut-v1 JSON path",
    )
    organize.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    organize.set_defaults(handler=_run_organize)

    paper = subparsers.add_parser(
        "paper",
        help="export or apply a cue-addressed paper-edit workbook",
    )
    paper_subparsers = paper.add_subparsers(
        dest="paper_command",
        required=True,
    )
    paper_export = paper_subparsers.add_parser(
        "export",
        help="export an editor-facing workbook",
    )
    paper_export.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    paper_export.add_argument(
        "--grouping",
        type=Path,
        help="optional strict grouping-v1 JSON path to prefill",
    )
    paper_export.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent paper-workbook-v1 XLSX path",
    )
    paper_export.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    paper_export.set_defaults(handler=_run_paper_export)

    paper_apply = paper_subparsers.add_parser(
        "apply",
        help="apply a strict workbook to grouping authority",
    )
    paper_apply.add_argument(
        "--aligned",
        required=True,
        type=Path,
        help="strict aligned-transcript-v1 JSON path",
    )
    paper_apply.add_argument(
        "--workbook",
        required=True,
        type=Path,
        help="strict paper-workbook-v1 XLSX path",
    )
    paper_apply.add_argument(
        "--output",
        required=True,
        type=Path,
        help="create an absent grouping-v1 JSON path",
    )
    paper_apply.add_argument(
        "--json",
        action="store_true",
        help="print only a sanitized completion summary",
    )
    paper_apply.set_defaults(handler=_run_paper_apply)

    run = subparsers.add_parser(
        "run",
        help="publish immutable local workflow stage bundles",
    )
    run_subparsers = run.add_subparsers(dest="run_command", required=True)

    run_prepare = run_subparsers.add_parser(
        "prepare", help="doctor, synchronize, transcribe, and emit a string-out"
    )
    run_prepare.add_argument(
        "--camera-a", action="append", required=True, type=Path
    )
    run_prepare.add_argument(
        "--camera-b", action="append", required=True, type=Path
    )
    run_prepare.add_argument(
        "--transcribe-media", action="append", required=True, type=Path
    )
    run_prepare.add_argument("--model", required=True, type=Path)
    run_prepare.add_argument("--language", required=True)
    run_prepare.add_argument("--profile", required=True)
    run_prepare.add_argument("--binding", required=True)
    run_prepare.add_argument("--event-name", required=True)
    run_prepare.add_argument("--project-name", required=True)
    run_prepare.add_argument("--run-id", required=True)
    run_prepare.add_argument("--output", required=True, type=Path)
    run_prepare.add_argument("--json", action="store_true")
    run_prepare.set_defaults(handler=_run_prepare)

    run_align = run_subparsers.add_parser(
        "align", help="apply one explicit text revision and export paper edit"
    )
    run_align.add_argument("--prepared", required=True, type=Path)
    run_align.add_argument("--revision", required=True, type=Path)
    run_align.add_argument("--output", required=True, type=Path)
    run_align.add_argument("--json", action="store_true")
    run_align.set_defaults(handler=_run_align_bundle)

    run_finish = run_subparsers.add_parser(
        "finish", help="apply paper intent and emit the story cut"
    )
    run_finish.add_argument("--prepared", required=True, type=Path)
    run_finish.add_argument("--aligned", required=True, type=Path)
    run_finish.add_argument("--workbook", required=True, type=Path)
    run_finish.add_argument(
        "--camera-a", action="append", required=True, type=Path
    )
    run_finish.add_argument(
        "--camera-b", action="append", required=True, type=Path
    )
    run_finish.add_argument("--event-name", required=True)
    run_finish.add_argument("--project-name", required=True)
    run_finish.add_argument("--output", required=True, type=Path)
    run_finish.add_argument("--json", action="store_true")
    run_finish.set_defaults(handler=_run_finish)

    run_status = run_subparsers.add_parser(
        "status", help="validate and summarize one complete run bundle"
    )
    run_status.add_argument("--run", dest="run_dir", required=True, type=Path)
    run_status.add_argument("--json", action="store_true")
    run_status.set_defaults(handler=_run_status)

    validate = subparsers.add_parser(
        "validate",
        help="validate one public artifact without writing",
    )
    validate_subparsers = validate.add_subparsers(
        dest="validate_command",
        required=True,
    )

    validate_contract = validate_subparsers.add_parser(
        "contract",
        help="check one JSON artifact against its installed contract",
    )
    validate_contract.add_argument("--artifact", required=True, type=Path)
    validate_contract.add_argument("--json", action="store_true")
    validate_contract.set_defaults(handler=_run_validate)

    validate_fcpxml = validate_subparsers.add_parser(
        "fcpxml",
        help="check one FCPXML artifact against installed authorities",
    )
    validate_fcpxml.add_argument("--artifact", required=True, type=Path)
    validate_fcpxml.add_argument("--profile", required=True)
    validate_fcpxml.add_argument("--binding", required=True)
    validate_fcpxml.add_argument("--json", action="store_true")
    validate_fcpxml.set_defaults(handler=_run_validate)

    validate_paper = validate_subparsers.add_parser(
        "paper",
        help="check one workbook against exact aligned authority",
    )
    validate_paper.add_argument("--aligned", required=True, type=Path)
    validate_paper.add_argument("--workbook", required=True, type=Path)
    validate_paper.add_argument("--json", action="store_true")
    validate_paper.set_defaults(handler=_run_validate)

    validate_run = validate_subparsers.add_parser(
        "run",
        help="check one complete immutable run bundle",
    )
    validate_run.add_argument(
        "--run", dest="run_dir", required=True, type=Path
    )
    validate_run.add_argument("--json", action="store_true")
    validate_run.set_defaults(handler=_run_validate)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        arguments = build_parser().parse_args(argv)
    except CliUsageError:
        print(json.dumps({"error": "TRITRACK_USAGE"}, ensure_ascii=False))
        return EXIT_USAGE
    return arguments.handler(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
--- END FILE src/tritrack_editing_assistant/cli.py ---

--- BEGIN FILE src/tritrack_editing_assistant/contracts.py ---
"""Strict loaders for the public versioned JSON contracts."""

from __future__ import annotations

import json
from collections.abc import Mapping
from functools import cache
from importlib import resources
from types import MappingProxyType

import jsonschema

CONTRACT_NAMES = frozenset(
    {
        "compatibility-profile-v1",
        "sync-map-v1",
        "transcript-bundle-v1",
        "text-revision-v1",
        "aligned-transcript-v1",
        "grouping-v1",
        "working-cut-v1",
        "title-binding-v1",
        "run-manifest-v1",
        "provider-receipt-v1",
    }
)


@cache
def load_schema(name: str) -> dict[str, object]:
    """Load and meta-validate one packaged schema by its closed public name."""

    if name not in CONTRACT_NAMES:
        raise ValueError(f"TRITRACK_CONTRACT_UNKNOWN: {name!r}")

    schema_text = (
        resources.files("tritrack_editing_assistant.schemas")
        .joinpath(f"{name}.schema.json")
        .read_text(encoding="utf-8")
    )
    schema = json.loads(schema_text)
    jsonschema.Draft202012Validator.check_schema(schema)
    return schema


def validate_contract(name: str, payload: object) -> None:
    """Fail closed unless *payload* exactly satisfies a packaged contract."""

    validator = jsonschema.Draft202012Validator(load_schema(name))
    validator.validate(payload)


@cache
def contract_names_by_schema_version() -> Mapping[str, str]:
    """Return the closed installed schema-version to contract-name registry."""

    mapping: dict[str, str] = {}
    for name in sorted(CONTRACT_NAMES):
        schema = load_schema(name)
        try:
            version = schema["properties"]["schemaVersion"]["const"]
        except (KeyError, TypeError) as error:
            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID") from error
        if not isinstance(version, str) or version in mapping:
            raise ValueError("TRITRACK_CONTRACT_REGISTRY_INVALID")
        mapping[version] = name
    return MappingProxyType(mapping)


def contract_name_for_schema_version(schema_version: object) -> str:
    """Resolve only an exact version declared by one installed contract."""

    if not isinstance(schema_version, str):
        # One stable data-error family covers absent, non-string, and unknown IDs.
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN")  # noqa: TRY004
    try:
        return contract_names_by_schema_version()[schema_version]
    except KeyError as error:
        raise ValueError("TRITRACK_CONTRACT_UNKNOWN") from error
--- END FILE src/tritrack_editing_assistant/contracts.py ---

--- BEGIN FILE src/tritrack_editing_assistant/doctor.py ---
"""Fail-closed, privacy-safe compatibility preflight."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import shutil
from importlib import resources
from pathlib import Path
from typing import Protocol

from .contracts import validate_contract
from .process import require_absent_output, run_bounded

PROFILE_NAMES = frozenset({"uhd-2997-ndf-fcpxml-1.14"})
TITLE_BINDING_NAMES = frozenset({"basic-title-v1"})
SUPPORTED_MACOS_VERSION = "26.5.2"
SUPPORTED_ARCHITECTURE = "arm64"
SUPPORTED_FINAL_CUT_VERSION = "12.3"
FINAL_CUT_INFO = Path("/Applications/Final Cut Pro.app/Contents/Info.plist")
FINAL_CUT_DTD_DIRECTORY = Path(
    "/Applications/Final Cut Pro.app/Contents/Frameworks/"
    "Interchange.framework/Versions/A/Resources"
)
MINIMUM_FREE_DISK_BYTES = 5 * 1024**3


class Probe(Protocol):
    system: str
    macos_version: str
    architecture: str
    python_version: str
    final_cut_version: str | None
    free_disk_bytes: int

    def executable_version(self, name: str) -> str | None: ...

    def final_cut_dtd_present(self, version: str) -> bool: ...

    def path_is_readable_file(self, path: Path) -> bool: ...


class SystemProbe:
    """Read only declared local compatibility facts."""

    def __init__(self) -> None:
        self.system = platform.system()
        self.macos_version = platform.mac_ver()[0]
        self.architecture = platform.machine()
        self.python_version = platform.python_version()
        self.final_cut_version = self._final_cut_version()
        self.free_disk_bytes = shutil.disk_usage(Path.cwd()).free

    @staticmethod
    def _final_cut_version() -> str | None:
        try:
            with FINAL_CUT_INFO.open("rb") as handle:
                value = plistlib.load(handle).get("CFBundleShortVersionString")
        except (OSError, plistlib.InvalidFileException):
            return None
        return value if isinstance(value, str) and value else None

    def executable_version(self, name: str) -> str | None:
        executable = shutil.which(name)
        if executable is None:
            return None
        arguments = (
            [executable, "-version"] if name != "xmllint" else [executable, "--version"]
        )
        result = run_bounded(
            arguments,
            timeout_seconds=5,
            max_captured_bytes=64 * 1024,
        )
        if not result.ok:
            return None
        output = result.stdout or result.stderr
        first_line = output.decode("utf-8", errors="replace").splitlines()
        return (
            _sanitize_detected(first_line[0]) if first_line else Path(executable).name
        )

    def final_cut_dtd_present(self, version: str) -> bool:
        return (
            FINAL_CUT_DTD_DIRECTORY / f"FCPXMLv{version.replace('.', '_')}.dtd"
        ).is_file()

    def path_is_readable_file(self, path: Path) -> bool:
        return path.is_file() and os.access(path, os.R_OK)


def _sanitize_detected(value: str) -> str:
    """Keep version text while refusing local path-shaped material."""

    private_home = "/" + "Users" + "/"
    mounted_volume = "/" + "Volumes" + "/"
    if private_home in value or mounted_volume in value or "\\" in value:
        return "detected-redacted"
    first, separator, remainder = value.partition(" ")
    if first.startswith("/"):
        first = Path(first.rstrip(":")).name + (":" if first.endswith(":") else "")
        value = first + (separator + remainder if separator else "")
    return value[:256]


def _load_packaged_json(name: str, allowed: frozenset[str]) -> dict[str, object]:
    if name not in allowed:
        raise ValueError(f"TRITRACK_PROFILE_UNKNOWN: {name!r}")
    payload = json.loads(
        resources.files("tritrack_editing_assistant.profiles")
        .joinpath(f"{name}.json")
        .read_text(encoding="utf-8")
    )
    if not isinstance(payload, dict):
        raise TypeError("TRITRACK_PROFILE_INVALID")
    return payload


def load_profile(profile_id: str) -> dict[str, object]:
    profile = _load_packaged_json(profile_id, PROFILE_NAMES)
    validate_contract("compatibility-profile-v1", profile)
    if profile.get("profileId") != profile_id:
        raise ValueError("TRITRACK_PROFILE_ID_MISMATCH")
    return profile


def load_title_binding(binding_id: str) -> dict[str, object]:
    binding = _load_packaged_json(binding_id, TITLE_BINDING_NAMES)
    validate_contract("title-binding-v1", binding)
    if binding.get("bindingId") != binding_id:
        raise ValueError("TRITRACK_PROFILE_ID_MISMATCH")
    return binding


def _check(code: str, status: str, *, detected: str | None = None) -> dict[str, object]:
    result: dict[str, object] = {"code": code, "status": status}
    if detected is not None:
        result["detected"] = _sanitize_detected(detected)
    return result


def build_receipt(
    *,
    profile_id: str,
    probe: Probe | None = None,
    transcription_requested: bool = False,
    whisper_model: Path | None = None,
) -> dict[str, object]:
    """Inspect the exact alpha environment without retaining private paths."""

    selected_probe = probe or SystemProbe()
    profile = load_profile(profile_id)
    binding = load_title_binding("basic-title-v1")
    checks: list[dict[str, object]] = []

    checks.append(
        _check(
            "operating-system",
            "ok" if selected_probe.system == "Darwin" else "unsupported",
            detected=selected_probe.system,
        )
    )
    checks.append(
        _check(
            "macos-version",
            "ok"
            if selected_probe.macos_version == SUPPORTED_MACOS_VERSION
            else "unsupported",
            detected=selected_probe.macos_version,
        )
    )
    checks.append(
        _check(
            "architecture",
            "ok"
            if selected_probe.architecture == SUPPORTED_ARCHITECTURE
            else "unsupported",
            detected=selected_probe.architecture,
        )
    )
    checks.append(_check("python", "ok", detected=selected_probe.python_version))
    checks.append(
        _check(
            "free-disk",
            "ok"
            if selected_probe.free_disk_bytes >= MINIMUM_FREE_DISK_BYTES
            else "insufficient",
            detected=str(selected_probe.free_disk_bytes),
        )
    )

    for executable in ("ffmpeg", "ffprobe", "xmllint"):
        detected = selected_probe.executable_version(executable)
        checks.append(
            _check(
                executable,
                "ok" if detected is not None else "missing",
                detected=detected,
            )
        )

    checks.append(
        _check(
            "final-cut",
            "ok"
            if selected_probe.final_cut_version == SUPPORTED_FINAL_CUT_VERSION
            else "unsupported",
            detected=selected_probe.final_cut_version,
        )
    )
    dtd_present = selected_probe.final_cut_dtd_present(str(profile["fcpxmlVersion"]))
    checks.append(_check("fcpxml-dtd", "ok" if dtd_present else "missing"))
    checks.append(_check("compatibility-profile", "ok", detected=profile_id))
    checks.append(_check("title-binding", "ok", detected=str(binding["bindingId"])))

    if transcription_requested:
        whisper_detected = selected_probe.executable_version("whisper-cli")
        checks.append(
            _check(
                "whisper-cli",
                "ok" if whisper_detected is not None else "missing",
                detected=whisper_detected,
            )
        )
        model_readable = (
            whisper_model is not None
            and selected_probe.path_is_readable_file(whisper_model)
        )
        checks.append(_check("whisper-model", "ok" if model_readable else "unreadable"))

    supported = all(check["status"] == "ok" for check in checks)
    return {
        "schemaVersion": "tritrack.doctor-receipt/v1",
        "profileId": profile_id,
        "titleBindingId": binding["bindingId"],
        "supported": supported,
        "checks": checks,
        "remediation": []
        if supported
        else ["Install or select only dependencies declared by the alpha profile."],
    }


def write_receipt(output: Path, **arguments: object) -> dict[str, object]:
    """Atomically create one absent doctor receipt."""

    destination = require_absent_output(output)
    receipt = build_receipt(**arguments)
    encoded = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(destination, flags, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return receipt
--- END FILE src/tritrack_editing_assistant/doctor.py ---

--- BEGIN FILE src/tritrack_editing_assistant/emit_fcpxml.py ---
"""Profile-bound FCPXML rendering and no-overwrite publication."""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import contracts, doctor, process, string_out, sync_scan

ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
MAX_SYNC_MAP_BYTES = 16 * 1024 * 1024
FORMAT_NAME = "FFVideoFormat3840x2160p2997"


@dataclass(frozen=True)
class ProjectMetadata:
    """Caller-owned names copied into one public string-out project."""

    event_name: str
    project_name: str

    def __post_init__(self) -> None:
        for value in (self.event_name, self.project_name):
            if (
                not isinstance(value, str)
                or not value.strip()
                or any(ord(character) < 32 for character in value)
            ):
                raise ValueError("TRITRACK_EMIT_METADATA_INVALID")


def load_sync_map(path: str | os.PathLike[str]) -> dict[str, object]:
    """Load one strict sync-map-v1 while preserving decimal spellings."""

    source = Path(path)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(source, flags)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_UNREADABLE") from error
    except OSError as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
    try:
        details = os.fstat(descriptor)
        if (
            not stat.S_ISREG(details.st_mode)
            or not 0 < details.st_size <= MAX_SYNC_MAP_BYTES
        ):
            raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            raw = stream.read(MAX_SYNC_MAP_BYTES + 1)
        if len(raw) > MAX_SYNC_MAP_BYTES or b"\x00" in raw:
            raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID")
    except OSError as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_UNREADABLE") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    try:
        payload = json.loads(raw.decode("utf-8"), parse_float=Decimal)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
    if not isinstance(payload, dict):
        raise TypeError("TRITRACK_EMIT_SYNC_MAP_INVALID")
    try:
        contracts.validate_contract("sync-map-v1", payload)
    except ValidationError as error:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_INVALID") from error
    return payload


def _frame_time(timeline: string_out.StringOut, frames: int) -> str:
    if frames == 0:
        return "0s"
    numerator = frames * timeline.frame_numerator
    return f"{numerator}/{timeline.frame_denominator}s"


def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
    parameters = binding["parameters"]
    if not isinstance(parameters, list):
        raise TypeError("TRITRACK_FCPXML_BINDING_INVALID")
    values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in parameters
        if isinstance(parameter, Mapping)
    }
    expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
    if set(values) != expected:
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
    return values


def _source_uri(path: Path) -> str:
    try:
        return path.absolute().as_uri()
    except ValueError as error:
        raise ValueError("TRITRACK_EMIT_SOURCE_INVALID") from error


def render_fcpxml(
    sync_map: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    profile_id: str,
    binding_id: str,
    metadata: ProjectMetadata,
) -> str:
    """Render deterministic FCPXML from the closed public inputs."""

    if not isinstance(metadata, ProjectMetadata):
        raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    timeline = string_out.build_string_out(sync_map, sources, profile=profile)
    if timeline.profile_id != profile_id:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    styles = _style_values(binding)

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": FORMAT_NAME,
            "frameDuration": str(profile["frameDuration"]),
            "width": str(profile["width"]),
            "height": str(profile["height"]),
            "colorSpace": str(profile["colorSpace"]),
        },
    )
    ET.SubElement(
        resources_element,
        "effect",
        {
            "id": "r2",
            "name": str(binding["effectName"]),
            "uid": str(binding["effectUid"]),
        },
    )

    source_ids: dict[tuple[str, str], str] = {}
    for index, source in enumerate(timeline.sources, start=3):
        resource_id = f"r{index}"
        source_ids[(source.camera, source.media_id)] = resource_id
        asset = ET.SubElement(
            resources_element,
            "asset",
            {
                "id": resource_id,
                "name": source.media_id,
                "start": "0s",
                "duration": _frame_time(timeline, source.duration_frames),
                "hasVideo": "1",
                "hasAudio": "1",
                "format": "r1",
                "audioSources": "1",
                "audioChannels": "2",
                "audioRate": f"{int(profile['audioRate']) // 1000}k",
            },
        )
        ET.SubElement(
            asset,
            "media-rep",
            {
                "kind": "original-media",
                "src": _source_uri(source.path),
            },
        )

    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", {"name": metadata.event_name})
    project = ET.SubElement(event, "project", {"name": metadata.project_name})
    sequence = ET.SubElement(
        project,
        "sequence",
        {
            "format": "r1",
            "duration": _frame_time(timeline, timeline.duration_frames),
            "tcStart": "0s",
            "tcFormat": str(profile["timecodeFormat"]),
            "audioLayout": "stereo",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        },
    )
    spine = ET.SubElement(sequence, "spine")
    for index, segment in enumerate(timeline.segments, start=1):
        gap = ET.SubElement(
            spine,
            "gap",
            {
                "name": segment.label,
                "offset": _frame_time(timeline, segment.offset_frames),
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        for lane, clip in enumerate(segment.clips, start=1):
            clip_attributes = {
                "ref": source_ids[(clip.camera, clip.media_id)],
                "lane": str(lane),
                "offset": _frame_time(timeline, clip.offset_frames),
                "name": clip.media_id,
                "start": "0s",
                "duration": _frame_time(timeline, clip.duration_frames),
                "srcEnable": "all" if clip.audio_enabled else "video",
            }
            if clip.audio_enabled:
                clip_attributes["audioRole"] = "dialogue"
            ET.SubElement(
                gap,
                "asset-clip",
                clip_attributes,
            )
        title = ET.SubElement(
            gap,
            "title",
            {
                "ref": "r2",
                "lane": str(len(segment.clips) + 1),
                "offset": _frame_time(timeline, segment.offset_frames),
                "name": f"{segment.label} - Basic Title",
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        text_element = ET.SubElement(title, "text")
        style_id = f"ts{index:03d}"
        text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
        text_style.text = segment.label
        style_definition = ET.SubElement(
            title,
            "text-style-def",
            {"id": style_id},
        )
        ET.SubElement(
            style_definition,
            "text-style",
            {
                name: styles[name]
                for name in (
                    "alignment",
                    "font",
                    "fontColor",
                    "fontFace",
                    "fontSize",
                )
            },
        )

    ET.indent(root, space="    ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    rendered = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"{ALLOWED_DOCTYPE}\n{body}\n"
    )
    validate_fcpxml(rendered, profile=profile, binding=binding)
    return rendered


def _profile_format_attributes(profile: Mapping[str, object]) -> dict[str, str]:
    return {
        "id": "r1",
        "name": FORMAT_NAME,
        "frameDuration": str(profile["frameDuration"]),
        "width": str(profile["width"]),
        "height": str(profile["height"]),
        "colorSpace": str(profile["colorSpace"]),
    }


def _validate_time_values(root: ET.Element, profile: Mapping[str, object]) -> None:
    frame_value = str(profile["frameDuration"])
    numerator_text, _, denominator_text = frame_value[:-1].partition("/")
    frame_numerator = int(numerator_text)
    denominator = int(denominator_text)
    pattern = re.compile(rf"^-?[0-9]+/{denominator}s$")
    for element in root.iter():
        for name in ("offset", "start", "duration"):
            value = element.attrib.get(name)
            if value is None or value == "0s":
                continue
            if not pattern.fullmatch(value):
                raise ValueError("TRITRACK_FCPXML_TIME_INVALID")
            value_numerator = int(value.split("/", 1)[0])
            if value_numerator % frame_numerator:
                raise ValueError("TRITRACK_FCPXML_TIME_INVALID")


def validate_fcpxml(
    text: str,
    *,
    profile: Mapping[str, object],
    binding: Mapping[str, object],
) -> None:
    """Fail closed unless generated XML exactly retains the public profile."""

    contracts.validate_contract("compatibility-profile-v1", profile)
    contracts.validate_contract("title-binding-v1", binding)
    if dict(profile) != doctor.load_profile(str(profile["profileId"])):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    if dict(binding) != doctor.load_title_binding(str(binding["bindingId"])):
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
    if (
        not isinstance(text, str)
        or text.count(ALLOWED_DOCTYPE) != 1
        or "<!ENTITY" in text
        or "<!DOCTYPE" in text.replace(ALLOWED_DOCTYPE, "", 1)
    ):
        raise ValueError("TRITRACK_FCPXML_INVALID")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError("TRITRACK_FCPXML_INVALID") from error
    if root.tag != "fcpxml" or root.attrib != {
        "version": str(profile["fcpxmlVersion"])
    }:
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")

    format_elements = root.findall("./resources/format")
    if (
        len(format_elements) != 1
        or format_elements[0].attrib != _profile_format_attributes(profile)
    ):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    effect_elements = root.findall("./resources/effect")
    if len(effect_elements) != 1 or effect_elements[0].attrib != {
        "id": "r2",
        "name": str(binding["effectName"]),
        "uid": str(binding["effectUid"]),
    }:
        raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")

    sequence = root.find("./library/event/project/sequence")
    if sequence is None:
        raise ValueError("TRITRACK_FCPXML_INVALID")
    expected_sequence = {
        "format": "r1",
        "tcStart": "0s",
        "tcFormat": str(profile["timecodeFormat"]),
        "audioLayout": "stereo",
        "audioRate": f"{int(profile['audioRate']) // 1000}k",
    }
    if any(sequence.attrib.get(key) != value for key, value in expected_sequence.items()):
        raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
    if not sequence.attrib.get("duration"):
        raise ValueError("TRITRACK_FCPXML_TIME_INVALID")

    resource_ids = [
        element.attrib.get("id")
        for element in root.findall("./resources/*")
    ]
    if None in resource_ids or len(resource_ids) != len(set(resource_ids)):
        raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")
    valid_refs = set(resource_ids)
    if any(
        element.attrib["ref"] not in valid_refs
        for element in root.iter()
        if "ref" in element.attrib and element.tag != "text-style"
    ):
        raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")

    for asset in root.findall("./resources/asset"):
        media_representations = asset.findall("./media-rep")
        expected_asset_profile = {
            "format": "r1",
            "hasVideo": "1",
            "hasAudio": "1",
            "audioSources": "1",
            "audioChannels": "2",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        }
        if any(
            asset.attrib.get(name) != value
            for name, value in expected_asset_profile.items()
        ):
            raise ValueError("TRITRACK_FCPXML_PROFILE_MISMATCH")
        if (
            "src" in asset.attrib
            or len(media_representations) != 1
            or media_representations[0].attrib.get("kind") != "original-media"
            or not media_representations[0].attrib.get("src", "").startswith("file:")
        ):
            raise ValueError("TRITRACK_FCPXML_SOURCE_INVALID")

    for gap in root.findall("./library/event/project/sequence/spine/gap"):
        clips = gap.findall("./asset-clip")
        if (
            not clips
            or sum(clip.attrib.get("srcEnable") == "all" for clip in clips) != 1
            or any(
                clip.attrib.get("srcEnable") not in {"all", "video"}
                or (
                    (clip.attrib.get("srcEnable") == "all")
                    != (clip.attrib.get("audioRole") == "dialogue")
                )
                for clip in clips
            )
        ):
            raise ValueError("TRITRACK_FCPXML_AUDIO_INVALID")

    expected_styles = _style_values(binding)
    style_ids: set[str] = set()
    for definition in root.iter("text-style-def"):
        style_id = definition.attrib.get("id")
        styles = definition.findall("./text-style")
        if (
            not style_id
            or style_id in style_ids
            or len(styles) != 1
            or styles[0].attrib != expected_styles
        ):
            raise ValueError("TRITRACK_FCPXML_BINDING_INVALID")
        style_ids.add(style_id)
    for text_style in root.iter("text-style"):
        if "ref" in text_style.attrib and text_style.attrib["ref"] not in style_ids:
            raise ValueError("TRITRACK_FCPXML_IDENTIFIER_INVALID")
    _validate_time_values(root, profile)


def publish_fcpxml(
    output_path: str | os.PathLike[str],
    text: str,
    *,
    profile: Mapping[str, object],
    binding: Mapping[str, object],
) -> Path:
    """Atomically create one validated FCPXML path without overwriting."""

    validate_fcpxml(text, profile=profile, binding=binding)
    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def _probe_sources(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    profile: Mapping[str, object],
) -> list[dict[str, object]]:
    contracts.validate_contract("compatibility-profile-v1", profile)
    if dict(profile) != doctor.load_profile(str(profile["profileId"])):
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    frame_duration = str(profile["frameDuration"])
    numerator, separator, denominator = frame_duration.removesuffix("s").partition("/")
    if not separator or str(profile["colorSpace"]) != "1-1-1 (Rec. 709)":
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    expected_fields = {
        "videoStreamCount",
        "audioStreamCount",
        "width",
        "height",
        "frameRate",
        "colorSpace",
        "colorTransfer",
        "colorPrimaries",
        "sampleRate",
        "channels",
    }
    expected_values = {
        "width": int(profile["width"]),
        "height": int(profile["height"]),
        "frameRate": f"{denominator}/{numerator}",
        "colorSpace": "bt709",
        "colorTransfer": "bt709",
        "colorPrimaries": "bt709",
        "sampleRate": str(profile["audioRate"]),
        "channels": 2,
    }
    media: list[dict[str, object]] = []
    for camera, sources in (("A", camera_a_sources), ("B", camera_b_sources)):
        for source in sources:
            probed = sync_scan.probe_media(source)
            compatibility = probed.get("compatibility")
            if (
                not isinstance(compatibility, Mapping)
                or set(compatibility) != expected_fields
                or not isinstance(compatibility["videoStreamCount"], int)
                or compatibility["videoStreamCount"] < 1
                or not isinstance(compatibility["audioStreamCount"], int)
                or compatibility["audioStreamCount"] < 1
                or any(
                    compatibility[field] != value
                    for field, value in expected_values.items()
                )
            ):
                raise ValueError("TRITRACK_EMIT_SOURCE_PROFILE_MISMATCH")
            media.append(
                {
                    "camera": camera,
                    "media_id": source.media_id,
                    "path": source.path,
                    "duration_seconds": Decimal(str(probed["duration_seconds"])),
                }
            )
    return media


def probe_sources(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    profile: Mapping[str, object],
) -> list[dict[str, object]]:
    """Probe public media inputs against one exact compatibility profile."""

    return _probe_sources(camera_a_sources, camera_b_sources, profile=profile)


def emit_and_publish(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    sync_map_path: str | os.PathLike[str],
    profile_id: str,
    binding_id: str,
    metadata: ProjectMetadata,
    output_path: str | os.PathLike[str],
) -> str:
    """Load, probe, render, validate, and atomically publish one FCPXML."""

    process.require_absent_output(output_path)
    sync_map = load_sync_map(sync_map_path)
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    if sync_map["profileId"] != profile_id:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")
    media = probe_sources(
        camera_a_sources,
        camera_b_sources,
        profile=profile,
    )
    rendered = render_fcpxml(
        sync_map,
        media,
        profile_id=profile_id,
        binding_id=binding_id,
        metadata=metadata,
    )
    publish_fcpxml(
        output_path,
        rendered,
        profile=profile,
        binding=binding,
    )
    return rendered
--- END FILE src/tritrack_editing_assistant/emit_fcpxml.py ---

--- BEGIN FILE src/tritrack_editing_assistant/process.py ---
"""Bounded subprocess execution with privacy-safe machine receipts."""

from __future__ import annotations

import hashlib
import json
import math
import os
import selectors
import signal
import subprocess
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

ALLOWED_ENVIRONMENT_KEYS = frozenset(
    {"LANG", "LC_ALL", "LC_CTYPE", "PATH", "TMPDIR", "TZ"}
)
_READ_CHUNK_BYTES = 64 * 1024
_TERMINATION_GRACE_SECONDS = 0.2


@dataclass(frozen=True)
class ProcessResult:
    """Raw bounded output kept separate from the sanitized public receipt."""

    status: str
    returncode: int | None
    stdout: bytes
    stderr: bytes
    receipt: dict[str, object]

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def require_absent_output(path: str | os.PathLike[str]) -> Path:
    """Return *path* only when no file, directory, or symlink exists there."""

    resolved = Path(path)
    if os.path.lexists(resolved):
        raise ValueError("TRITRACK_OUTPUT_EXISTS")
    return resolved


def _command_shape(command: Sequence[str]) -> list[str]:
    shape = [Path(command[0]).name]
    for argument in command[1:]:
        if argument.startswith("-"):
            option = argument.split("=", 1)[0]
            shape.append(f"option:{option}")
        elif os.path.isabs(argument) or "/" in argument or "\\" in argument:
            shape.append("path")
        else:
            shape.append("argument")
    return shape


def sanitized_receipt(
    *,
    command: Sequence[str],
    environment: Mapping[str, str],
    returncode: int | None,
    status: str | None = None,
    timed_out: bool = False,
    output_limit_exceeded: bool = False,
    observed_captured_bytes: int = 0,
    stdout: bytes | None = None,
    stderr: bytes | None = None,
    duration_ms: int | None = None,
    error_code: str | None = None,
) -> dict[str, object]:
    """Build a receipt without command arguments, paths, output, or env values."""

    if not command:
        raise ValueError("TRITRACK_PROCESS_COMMAND_INVALID")
    shape_bytes = json.dumps(
        _command_shape(command), ensure_ascii=True, separators=(",", ":")
    ).encode("utf-8")
    if status is None:
        status = "ok" if returncode == 0 else "failed"

    receipt: dict[str, object] = {
        "schemaVersion": "tritrack.process-receipt/v1",
        "status": status,
        "executable": Path(command[0]).name,
        "argumentCount": len(command) - 1,
        "argumentShapeSha256": hashlib.sha256(shape_bytes).hexdigest(),
        "environmentKeys": sorted(environment),
        "returncode": returncode,
        "timedOut": timed_out,
        "outputLimitExceeded": output_limit_exceeded,
        "observedCapturedBytes": observed_captured_bytes,
        "retainedStdoutBytes": len(stdout) if stdout is not None else 0,
        "retainedStderrBytes": len(stderr) if stderr is not None else 0,
        "stdoutSha256": hashlib.sha256(stdout).hexdigest()
        if stdout is not None
        else None,
        "stderrSha256": hashlib.sha256(stderr).hexdigest()
        if stderr is not None
        else None,
        "durationMs": duration_ms,
    }
    if error_code is not None:
        receipt["errorCode"] = error_code
    return receipt


def _validate_command(command: Sequence[str]) -> tuple[str, ...]:
    if isinstance(command, (str, bytes)) or not isinstance(command, Sequence):
        raise TypeError("TRITRACK_PROCESS_COMMAND_INVALID")
    if not command or any(
        not isinstance(argument, str) or not argument or "\x00" in argument
        for argument in command
    ):
        raise ValueError("TRITRACK_PROCESS_COMMAND_INVALID")
    return tuple(command)


def _validate_bounds(timeout_seconds: float, max_captured_bytes: int) -> None:
    if (
        isinstance(timeout_seconds, bool)
        or not isinstance(timeout_seconds, (int, float))
        or not math.isfinite(timeout_seconds)
        or timeout_seconds <= 0
    ):
        raise ValueError("TRITRACK_PROCESS_TIMEOUT_INVALID")
    if (
        isinstance(max_captured_bytes, bool)
        or not isinstance(max_captured_bytes, int)
        or max_captured_bytes < 1
    ):
        raise ValueError("TRITRACK_PROCESS_CAPTURE_LIMIT_INVALID")


def _validated_environment(
    environment: Mapping[str, str] | None,
) -> dict[str, str]:
    if environment is None:
        return {
            key: os.environ[key]
            for key in ALLOWED_ENVIRONMENT_KEYS
            if key in os.environ
        }
    if not isinstance(environment, Mapping):
        raise TypeError("TRITRACK_PROCESS_ENVIRONMENT_INVALID")

    validated: dict[str, str] = {}
    for key, value in environment.items():
        if key not in ALLOWED_ENVIRONMENT_KEYS:
            raise ValueError(f"TRITRACK_PROCESS_ENVIRONMENT_NOT_ALLOWED: {key}")
        if not isinstance(value, str) or "\x00" in value:
            raise ValueError("TRITRACK_PROCESS_ENVIRONMENT_INVALID")
        validated[key] = value
    return validated


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except OSError:
        process.terminate()

    try:
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except OSError:
        if process.poll() is None:
            process.kill()

    if process.poll() is None:
        process.wait()


def _close_pipes(process: subprocess.Popen[bytes]) -> None:
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()


def _capture_bounded(
    process: subprocess.Popen[bytes],
    *,
    deadline: float,
    max_captured_bytes: int,
) -> tuple[str, bytes, bytes, int]:
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    observed_bytes = 0

    with selectors.DefaultSelector() as selector:
        assert process.stdout is not None
        assert process.stderr is not None
        selector.register(process.stdout, selectors.EVENT_READ, stdout_chunks)
        selector.register(process.stderr, selectors.EVENT_READ, stderr_chunks)

        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return "timeout", b"", b"", observed_bytes

            events = selector.select(timeout=min(remaining, 0.05))
            for key, _mask in events:
                allowed_read = max_captured_bytes - observed_bytes + 1
                chunk = os.read(
                    key.fd,
                    min(_READ_CHUNK_BYTES, max(1, allowed_read)),
                )
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue

                observed_bytes += len(chunk)
                if observed_bytes > max_captured_bytes:
                    return "output_limit_exceeded", b"", b"", observed_bytes
                key.data.append(chunk)

    remaining = deadline - time.monotonic()
    if remaining <= 0 and process.poll() is None:
        return "timeout", b"", b"", observed_bytes
    try:
        process.wait(timeout=max(0.0, remaining))
    except subprocess.TimeoutExpired:
        return "timeout", b"", b"", observed_bytes

    return (
        "ok" if process.returncode == 0 else "failed",
        b"".join(stdout_chunks),
        b"".join(stderr_chunks),
        observed_bytes,
    )


def run_bounded(
    command: Sequence[str],
    *,
    timeout_seconds: float,
    max_captured_bytes: int,
    environment: Mapping[str, str] | None = None,
) -> ProcessResult:
    """Run one argv-only process with time, output, and environment bounds."""

    checked_command = _validate_command(command)
    _validate_bounds(timeout_seconds, max_captured_bytes)
    checked_environment = _validated_environment(environment)
    started = time.monotonic()

    try:
        child = subprocess.Popen(
            checked_command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            env=checked_environment,
            start_new_session=True,
        )
    except OSError as error:
        duration_ms = round((time.monotonic() - started) * 1000)
        receipt = sanitized_receipt(
            command=checked_command,
            environment=checked_environment,
            returncode=None,
            status="spawn_error",
            duration_ms=duration_ms,
            error_code=f"OS_ERROR_{error.errno}",
        )
        return ProcessResult("spawn_error", None, b"", b"", receipt)

    deadline = started + timeout_seconds
    status, stdout, stderr, observed_bytes = _capture_bounded(
        child,
        deadline=deadline,
        max_captured_bytes=max_captured_bytes,
    )
    if status in {"timeout", "output_limit_exceeded"}:
        _terminate_process_group(child)
        stdout = b""
        stderr = b""
    _close_pipes(child)

    duration_ms = round((time.monotonic() - started) * 1000)
    receipt = sanitized_receipt(
        command=checked_command,
        environment=checked_environment,
        returncode=child.returncode,
        status=status,
        timed_out=status == "timeout",
        output_limit_exceeded=status == "output_limit_exceeded",
        observed_captured_bytes=observed_bytes,
        stdout=stdout if status in {"ok", "failed"} else None,
        stderr=stderr if status in {"ok", "failed"} else None,
        duration_ms=duration_ms,
    )
    return ProcessResult(status, child.returncode, stdout, stderr, receipt)
--- END FILE src/tritrack_editing_assistant/process.py ---

--- BEGIN FILE src/tritrack_editing_assistant/align_text.py ---
"""Deterministic cue-addressed transcript promotion."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError

from . import hallucination
from .contracts import validate_contract
from .process import require_absent_output

ALIGNMENT_PROFILE_ID = "cue-addressed-v1"
_ARTIFACT_LIMIT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class LoadedJsonArtifact:
    """One validated exact-byte JSON input and its immutable provenance."""

    path: Path
    contract: str
    invalid_code: str
    payload: object
    sha256: str


def _validate_input(contract: str, payload: object, code: str) -> None:
    try:
        validate_contract(contract, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _ARTIFACT_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_ARTIFACT_LIMIT_BYTES + 1)
        if len(encoded) > _ARTIFACT_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def load_json_artifact(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedJsonArtifact:
    """Load one bounded regular JSON file and validate its strict contract."""

    selected = Path(path)
    encoded = _read_regular_bytes(selected, invalid_code)
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedJsonArtifact(
        path=selected,
        contract=contract,
        invalid_code=invalid_code,
        payload=payload,
        sha256=hashlib.sha256(encoded).hexdigest(),
    )


def verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
    """Fail closed when an exact input file changed after validated loading."""

    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_ALIGNMENT_INPUT_CHANGED")


def _canonical_source_cues(take: Mapping[str, object]) -> list[dict[str, object]]:
    status = take["status"]
    cues = take["cues"]
    assert isinstance(cues, list)
    if status == "empty":
        return []

    canonical: list[dict[str, object]] = []
    cue_ids: set[str] = set()
    previous_end = 0
    for cue in cues:
        assert isinstance(cue, Mapping)
        cue_id = cue["cueId"]
        start_ms = cue["startMs"]
        end_ms = cue["endMs"]
        text = cue["text"]
        assert isinstance(cue_id, str)
        assert isinstance(start_ms, int)
        assert isinstance(end_ms, int)
        assert isinstance(text, str)
        if cue_id in cue_ids:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_CUE")
        cue_ids.add(cue_id)
        try:
            normalized = hallucination.normalize_cue_text(text)
        except (TypeError, ValueError) as error:
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_INVALID") from error
        if normalized != text or not (previous_end <= start_ms < end_ms):
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_INVALID")
        canonical.append(
            {
                "cueId": cue_id,
                "startMs": start_ms,
                "endMs": end_ms,
                "text": text,
                "disposition": "original",
            }
        )
        previous_end = end_ms
    return canonical


def build_aligned_transcript(
    transcript: object,
    revision: object,
    *,
    source_bundle_sha256: str,
    revision_sha256: str,
) -> dict[str, object]:
    """Promote cue-addressed text while preserving canonical source timing."""

    _validate_input(
        "transcript-bundle-v1",
        transcript,
        "TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID",
    )
    _validate_input(
        "text-revision-v1",
        revision,
        "TRITRACK_ALIGNMENT_REVISION_INVALID",
    )
    assert isinstance(transcript, Mapping)
    assert isinstance(revision, Mapping)

    if revision["sourceBundleSha256"] != source_bundle_sha256:
        raise ValueError("TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH")
    if revision["language"] != transcript["language"]:
        raise ValueError("TRITRACK_ALIGNMENT_LANGUAGE_MISMATCH")

    source_takes = transcript["takes"]
    revision_takes = revision["takes"]
    assert isinstance(source_takes, list)
    assert isinstance(revision_takes, list)

    aligned_by_take: dict[str, dict[str, object]] = {}
    source_by_take: dict[str, Mapping[str, object]] = {}
    for take in source_takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        assert isinstance(take_id, str)
        if take_id in source_by_take:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_TAKE")
        source_by_take[take_id] = take
        aligned_by_take[take_id] = {
            "takeId": take_id,
            "sourceSha256": take["sourceSha256"],
            "status": take["status"],
            "cues": _canonical_source_cues(take),
        }

    revised_take_ids: set[str] = set()
    for revised_take in revision_takes:
        assert isinstance(revised_take, Mapping)
        take_id = revised_take["takeId"]
        assert isinstance(take_id, str)
        if take_id in revised_take_ids:
            raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_TAKE")
        revised_take_ids.add(take_id)
        source_take = source_by_take.get(take_id)
        if source_take is None:
            raise ValueError("TRITRACK_ALIGNMENT_TAKE_UNKNOWN")
        if revised_take["sourceSha256"] != source_take["sourceSha256"]:
            raise ValueError("TRITRACK_ALIGNMENT_SOURCE_HASH_MISMATCH")
        if source_take["status"] == "empty":
            raise ValueError("TRITRACK_ALIGNMENT_EMPTY_TAKE_IMMUTABLE")

        aligned_cues = aligned_by_take[take_id]["cues"]
        assert isinstance(aligned_cues, list)
        cues_by_id = {cue["cueId"]: cue for cue in aligned_cues}
        revised_cue_ids: set[str] = set()
        revisions = revised_take["revisions"]
        assert isinstance(revisions, list)
        for cue_revision in revisions:
            assert isinstance(cue_revision, Mapping)
            cue_id = cue_revision["cueId"]
            assert isinstance(cue_id, str)
            if cue_id in revised_cue_ids:
                raise ValueError("TRITRACK_ALIGNMENT_DUPLICATE_CUE")
            revised_cue_ids.add(cue_id)
            cue = cues_by_id.get(cue_id)
            if cue is None:
                raise ValueError("TRITRACK_ALIGNMENT_CUE_UNKNOWN")
            try:
                normalized = hallucination.normalize_cue_text(cue_revision["text"])
            except (TypeError, ValueError) as error:
                raise ValueError("TRITRACK_ALIGNMENT_TEXT_INVALID") from error
            cue["text"] = normalized
            cue["disposition"] = "revised"

    aligned: dict[str, object] = {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": ALIGNMENT_PROFILE_ID,
        "sourceBundleSha256": source_bundle_sha256,
        "revisionSha256": revision_sha256,
        "language": transcript["language"],
        "takes": [aligned_by_take[take_id] for take_id in sorted(aligned_by_take)],
    }
    validate_contract("aligned-transcript-v1", aligned)
    return aligned


def encode_aligned_transcript(payload: object) -> bytes:
    """Return stable UTF-8 bytes for one strict aligned transcript."""

    validate_contract("aligned-transcript-v1", payload)
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def publish_aligned_transcript(payload: object, output_path: Path) -> None:
    """Publish one aligned transcript without overwriting a race winner."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_aligned_transcript(payload)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)


def prepare_alignment(
    transcript_path: Path,
    revision_path: Path,
) -> tuple[dict[str, object], tuple[LoadedJsonArtifact, LoadedJsonArtifact]]:
    """Load exact inputs and build an unpublished deterministic alignment."""

    transcript = load_json_artifact(
        transcript_path,
        contract="transcript-bundle-v1",
        invalid_code="TRITRACK_ALIGNMENT_TRANSCRIPT_INVALID",
    )
    revision = load_json_artifact(
        revision_path,
        contract="text-revision-v1",
        invalid_code="TRITRACK_ALIGNMENT_REVISION_INVALID",
    )
    aligned = build_aligned_transcript(
        transcript.payload,
        revision.payload,
        source_bundle_sha256=transcript.sha256,
        revision_sha256=revision.sha256,
    )
    return aligned, (transcript, revision)


def align_and_publish(
    transcript_path: Path,
    revision_path: Path,
    *,
    output_path: Path,
) -> dict[str, object]:
    """Promote local cue revisions and atomically publish stable bytes."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned, inputs = prepare_alignment(transcript_path, revision_path)
    for artifact in inputs:
        verify_artifact_unchanged(artifact)
    publish_aligned_transcript(aligned, destination)
    return aligned
--- END FILE src/tritrack_editing_assistant/align_text.py ---

--- BEGIN FILE src/tritrack_editing_assistant/gemini_hybrid.py ---
"""Offline Gemini receipt conformance for deterministic cue promotion."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from . import align_text
from .process import require_absent_output


def _validate_exact_model(exact_model: str) -> None:
    if (
        not isinstance(exact_model, str)
        or not exact_model
        or len(exact_model) > 256
        or any(character.isspace() for character in exact_model)
    ):
        raise ValueError("TRITRACK_HYBRID_MODEL_INVALID")


def _revised_take_sources(revision: object) -> dict[str, str]:
    assert isinstance(revision, Mapping)
    takes = revision["takes"]
    assert isinstance(takes, list)
    sources: dict[str, str] = {}
    for take in takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        source_sha256 = take["sourceSha256"]
        assert isinstance(take_id, str)
        assert isinstance(source_sha256, str)
        sources[take_id] = source_sha256
    return sources


def _receipt_take_id(receipt: align_text.LoadedJsonArtifact) -> str:
    payload = receipt.payload
    assert isinstance(payload, Mapping)
    take_id = payload["takeId"]
    assert isinstance(take_id, str)
    return take_id


def _is_success_status(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 200 <= value < 300


def _validate_receipt(
    receipt: align_text.LoadedJsonArtifact,
    *,
    source_bundle_sha256: str,
    take_id: str,
    source_sha256: str,
    exact_model: str,
) -> None:
    payload = receipt.payload
    assert isinstance(payload, Mapping)
    upload = payload["upload"]
    deletion = payload["serverFileDeletion"]
    assert isinstance(upload, Mapping)
    assert isinstance(deletion, Mapping)

    if not (
        payload["provider"] == "gemini"
        and payload["sourceBundleSha256"] == source_bundle_sha256
        and payload["takeId"] == take_id
        and payload["audioSha256"] == source_sha256
        and payload["requestedModel"] == exact_model
        and payload["observedModel"] == exact_model
        and payload["requestStatus"] == "completed"
        and _is_success_status(payload["responseStatus"])
        and upload["status"] == "completed"
        and upload["serverFileIdSha256"] is not None
        and deletion["attempted"] is True
        and deletion["confirmed"] is True
        and _is_success_status(deletion["statusCode"])
    ):
        raise ValueError("TRITRACK_HYBRID_RECEIPT_REJECTED")


def hybrid_and_publish(
    transcript_path: Path,
    revision_path: Path,
    receipt_paths: Sequence[Path],
    *,
    exact_model: str,
    output_path: Path,
) -> dict[str, object]:
    """Validate offline receipts, then publish through the local aligner."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    _validate_exact_model(exact_model)
    if isinstance(receipt_paths, (str, bytes)) or not isinstance(
        receipt_paths, Sequence
    ):
        raise TypeError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")

    aligned, alignment_inputs = align_text.prepare_alignment(
        transcript_path, revision_path
    )
    transcript, revision = alignment_inputs
    revised_sources = _revised_take_sources(revision.payload)

    receipts = [
        align_text.load_json_artifact(
            Path(path),
            contract="provider-receipt-v1",
            invalid_code="TRITRACK_HYBRID_RECEIPT_INVALID",
        )
        for path in receipt_paths
    ]
    receipts_by_take: dict[str, align_text.LoadedJsonArtifact] = {}
    for receipt in receipts:
        take_id = _receipt_take_id(receipt)
        if take_id in receipts_by_take:
            raise ValueError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")
        receipts_by_take[take_id] = receipt
    if set(receipts_by_take) != set(revised_sources):
        raise ValueError("TRITRACK_HYBRID_RECEIPT_SET_INVALID")

    for take_id, source_sha256 in revised_sources.items():
        _validate_receipt(
            receipts_by_take[take_id],
            source_bundle_sha256=transcript.sha256,
            take_id=take_id,
            source_sha256=source_sha256,
            exact_model=exact_model,
        )

    for artifact in (*alignment_inputs, *receipts):
        align_text.verify_artifact_unchanged(artifact)
    align_text.publish_aligned_transcript(aligned, destination)
    return aligned
--- END FILE src/tritrack_editing_assistant/gemini_hybrid.py ---

--- BEGIN FILE src/tritrack_editing_assistant/hallucination.py ---
"""Deterministic structural guards for local transcript evidence."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Sequence

_WHISPER_TOKEN = re.compile(r"<\|[^|]*\|>")
_ALLOWED_CONTROLS = frozenset({"\t", "\n", "\r"})
MAX_ADJACENT_IDENTICAL_CUES = 2
BLANK_AUDIO_SENTINEL = "[BLANK_AUDIO]"


def normalize_cue_text(value: object) -> str:
    """Return NFC, single-spaced cue text without engine control tokens."""

    if not isinstance(value, str):
        raise TypeError("TRITRACK_TRANSCRIPT_TEXT_INVALID")
    if any(
        unicodedata.category(character) == "Cc"
        and character not in _ALLOWED_CONTROLS
        for character in value
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_TEXT_INVALID")

    normalized = unicodedata.normalize("NFC", " ".join(value.split()))
    if not normalized or _WHISPER_TOKEN.search(normalized):
        raise ValueError("TRITRACK_TRANSCRIPT_TEXT_INVALID")
    return normalized


def reject_repeated_cues(values: Sequence[str]) -> None:
    """Reject only an exact normalized three-cue adjacent repetition run."""

    previous: str | None = None
    run_length = 0
    for value in values:
        normalized = normalize_cue_text(value)
        if normalized == previous:
            run_length += 1
        else:
            previous = normalized
            run_length = 1
        if run_length > MAX_ADJACENT_IDENTICAL_CUES:
            raise ValueError("TRITRACK_TRANSCRIPT_REPETITION_DETECTED")


def is_blank_audio_sentinel(value: str) -> bool:
    """Return true only for whisper.cpp's observed exact blank-audio marker."""

    return value == BLANK_AUDIO_SENTINEL
--- END FILE src/tritrack_editing_assistant/hallucination.py ---

--- BEGIN FILE src/tritrack_editing_assistant/organizer.py ---
"""Deterministic cue-addressed editorial grouping and compilation."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import ValidationError

from . import hallucination
from .contracts import validate_contract
from .process import require_absent_output

ORGANIZATION_PROFILE_ID = "cue-addressed-question-groups-v1"
QUESTION_TEXT_LIMIT = 500
NOTE_TEXT_LIMIT = 2000
_JSON_LIMIT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class IndexedCue:
    cue_id: str
    start_ms: int
    end_ms: int


@dataclass(frozen=True)
class IndexedTake:
    take_id: str
    source_sha256: str
    status: str
    cues: tuple[IndexedCue, ...]
    cue_positions: Mapping[str, int]


@dataclass(frozen=True)
class AlignedIndex:
    takes: Mapping[str, IndexedTake]
    completed_take_order: tuple[str, ...]


@dataclass(frozen=True)
class LoadedJsonArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str


def _validate_contract(name: str, payload: object, code: str) -> None:
    try:
        validate_contract(name, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def canonical_editor_text(
    value: object,
    *,
    maximum: int,
    required: bool,
) -> str | None:
    """Normalize one bounded editor-authored field without interpreting it."""

    if value is None or value == "":
        if required:
            raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
        return None
    if not isinstance(value, str):
        raise TypeError("TRITRACK_ORGANIZER_TEXT_INVALID")
    if any(unicodedata.category(character).startswith("C") for character in value):
        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
    normalized = " ".join(unicodedata.normalize("NFC", value).split())
    if (required and not normalized) or not 0 < len(normalized) <= maximum:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_INVALID")
    return normalized


def index_aligned_transcript(payload: object) -> AlignedIndex:
    """Validate and index one canonical aligned transcript authority."""

    _validate_contract(
        "aligned-transcript-v1",
        payload,
        "TRITRACK_ORGANIZER_ALIGNED_INVALID",
    )
    assert isinstance(payload, Mapping)
    takes = payload["takes"]
    assert isinstance(takes, list)
    take_ids = [take["takeId"] for take in takes]
    if take_ids != sorted(take_ids) or len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")

    indexed: dict[str, IndexedTake] = {}
    completed_order: list[str] = []
    for take in takes:
        assert isinstance(take, Mapping)
        take_id = take["takeId"]
        source_sha256 = take["sourceSha256"]
        status = take["status"]
        cues = take["cues"]
        assert isinstance(take_id, str)
        assert isinstance(source_sha256, str)
        assert isinstance(status, str)
        assert isinstance(cues, list)

        indexed_cues: list[IndexedCue] = []
        positions: dict[str, int] = {}
        previous_end = 0
        for position, cue in enumerate(cues):
            assert isinstance(cue, Mapping)
            cue_id = cue["cueId"]
            start_ms = cue["startMs"]
            end_ms = cue["endMs"]
            text = cue["text"]
            assert isinstance(cue_id, str)
            assert isinstance(start_ms, int)
            assert isinstance(end_ms, int)
            assert isinstance(text, str)
            if cue_id in positions or not (previous_end <= start_ms < end_ms):
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
            try:
                normalized_text = hallucination.normalize_cue_text(text)
            except (TypeError, ValueError) as error:
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID") from error
            if normalized_text != text:
                raise ValueError("TRITRACK_ORGANIZER_ALIGNED_INVALID")
            positions[cue_id] = position
            indexed_cues.append(IndexedCue(cue_id, start_ms, end_ms))
            previous_end = end_ms

        if status == "completed":
            completed_order.append(take_id)
        indexed[take_id] = IndexedTake(
            take_id=take_id,
            source_sha256=source_sha256,
            status=status,
            cues=tuple(indexed_cues),
            cue_positions=positions,
        )
    return AlignedIndex(indexed, tuple(completed_order))


def _require_permutation(items: list[object], field: str) -> None:
    orders = [item[field] for item in items]
    if orders != list(range(1, len(items) + 1)):
        raise ValueError("TRITRACK_ORGANIZER_ORDER_INVALID")


def _resolve_span(
    selection: Mapping[str, object],
    *,
    aligned_index: AlignedIndex,
) -> tuple[IndexedTake, int, int]:
    take_id = selection["takeId"]
    start_cue_id = selection["startCueId"]
    end_cue_id = selection["endCueId"]
    assert isinstance(take_id, str)
    assert isinstance(start_cue_id, str)
    assert isinstance(end_cue_id, str)
    take = aligned_index.takes.get(take_id)
    if take is None:
        raise ValueError("TRITRACK_ORGANIZER_TAKE_UNKNOWN")
    if take.status != "completed":
        raise ValueError("TRITRACK_ORGANIZER_TAKE_NOT_COMPLETED")
    start_position = take.cue_positions.get(start_cue_id)
    end_position = take.cue_positions.get(end_cue_id)
    if start_position is None or end_position is None:
        raise ValueError("TRITRACK_ORGANIZER_CUE_UNKNOWN")
    if start_position > end_position:
        raise ValueError("TRITRACK_ORGANIZER_SPAN_INVALID")
    return take, start_position, end_position


def _require_canonical_text(
    item: Mapping[str, object],
    field: str,
    *,
    maximum: int,
    required: bool,
) -> None:
    original = item.get(field)
    try:
        canonical = canonical_editor_text(
            original,
            maximum=maximum,
            required=required,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL") from error
    if canonical != original:
        raise ValueError("TRITRACK_ORGANIZER_TEXT_NONCANONICAL")


def validate_grouping(
    payload: object,
    *,
    aligned_index: AlignedIndex,
    aligned_sha256: str,
) -> dict[str, object]:
    """Validate canonical editor intent against one exact aligned authority."""

    _validate_contract(
        "grouping-v1",
        payload,
        "TRITRACK_ORGANIZER_GROUPING_INVALID",
    )
    assert isinstance(payload, dict)
    if payload["alignedTranscriptSha256"] != aligned_sha256:
        raise ValueError("TRITRACK_ORGANIZER_ALIGNED_HASH_MISMATCH")

    questions = payload["questions"]
    reserve = payload["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)
    _require_permutation(questions, "order")
    _require_permutation(reserve, "order")

    all_ids: set[str] = set()
    assigned_cues: set[tuple[str, str]] = set()

    def require_unique_id(item: Mapping[str, object]) -> None:
        identifier = item["id"]
        assert isinstance(identifier, str)
        if identifier in all_ids:
            raise ValueError("TRITRACK_ORGANIZER_DUPLICATE_ID")
        all_ids.add(identifier)

    def assign_span(item: Mapping[str, object]) -> None:
        take, start_position, end_position = _resolve_span(
            item,
            aligned_index=aligned_index,
        )
        for cue in take.cues[start_position : end_position + 1]:
            address = (take.take_id, cue.cue_id)
            if address in assigned_cues:
                raise ValueError("TRITRACK_ORGANIZER_CUE_REUSED")
            assigned_cues.add(address)

    for question in questions:
        assert isinstance(question, Mapping)
        require_unique_id(question)
        _require_canonical_text(
            question,
            "question",
            maximum=QUESTION_TEXT_LIMIT,
            required=True,
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        _require_permutation(answers, "order")
        for answer in answers:
            assert isinstance(answer, Mapping)
            require_unique_id(answer)
            if "note" in answer:
                _require_canonical_text(
                    answer,
                    "note",
                    maximum=NOTE_TEXT_LIMIT,
                    required=False,
                )
            assign_span(answer)

    for item in reserve:
        assert isinstance(item, Mapping)
        require_unique_id(item)
        _require_canonical_text(
            item,
            "reason",
            maximum=QUESTION_TEXT_LIMIT,
            required=True,
        )
        if "note" in item:
            _require_canonical_text(
                item,
                "note",
                maximum=NOTE_TEXT_LIMIT,
                required=False,
            )
        assign_span(item)
    return payload


def _compiled_span(
    selection: Mapping[str, object],
    *,
    aligned_index: AlignedIndex,
) -> dict[str, object]:
    take, start_position, end_position = _resolve_span(
        selection,
        aligned_index=aligned_index,
    )
    return {
        "takeId": take.take_id,
        "sourceSha256": take.source_sha256,
        "startCueId": take.cues[start_position].cue_id,
        "endCueId": take.cues[end_position].cue_id,
        "startMs": take.cues[start_position].start_ms,
        "endMs": take.cues[end_position].end_ms,
    }


def build_working_cut(
    aligned: object,
    grouping: object,
    *,
    aligned_sha256: str,
    grouping_sha256: str,
) -> dict[str, object]:
    """Compile one grouping into a deterministic transcript-text-free working cut."""

    aligned_index = index_aligned_transcript(aligned)
    canonical_grouping = validate_grouping(
        grouping,
        aligned_index=aligned_index,
        aligned_sha256=aligned_sha256,
    )
    questions = canonical_grouping["questions"]
    reserve = canonical_grouping["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)

    compiled_questions: list[dict[str, object]] = []
    segments: list[dict[str, object]] = []
    story_order = 0
    for question in sorted(questions, key=lambda item: item["order"]):
        assert isinstance(question, Mapping)
        compiled_questions.append(
            {
                "id": question["id"],
                "question": question["question"],
                "order": question["order"],
            }
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        for answer in sorted(answers, key=lambda item: item["order"]):
            assert isinstance(answer, Mapping)
            story_order += 1
            compiled = {
                "id": answer["id"],
                "storyOrder": story_order,
                "questionId": question["id"],
                **_compiled_span(answer, aligned_index=aligned_index),
            }
            if "note" in answer:
                compiled["note"] = answer["note"]
            segments.append(compiled)

    compiled_reserve: list[dict[str, object]] = []
    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
        assert isinstance(item, Mapping)
        compiled = {
            "id": item["id"],
            "order": item["order"],
            **_compiled_span(item, aligned_index=aligned_index),
            "reason": item["reason"],
        }
        if "note" in item:
            compiled["note"] = item["note"]
        compiled_reserve.append(compiled)

    working_cut: dict[str, object] = {
        "schemaVersion": "tritrack.working-cut/v1",
        "organizationProfileId": ORGANIZATION_PROFILE_ID,
        "alignedTranscriptSha256": aligned_sha256,
        "groupingSha256": grouping_sha256,
        "questions": compiled_questions,
        "segments": segments,
        "reserve": compiled_reserve,
    }
    validate_contract("working-cut-v1", working_cut)
    return working_cut


def _encode_contract(name: str, payload: object) -> bytes:
    validate_contract(name, payload)
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def encode_grouping(payload: object) -> bytes:
    """Return canonical bytes for one schema-valid grouping."""

    return _encode_contract("grouping-v1", payload)


def encode_working_cut(payload: object) -> bytes:
    """Return canonical bytes for one strict working cut."""

    return _encode_contract("working-cut-v1", payload)


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_UNREADABLE") from error
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_JSON_LIMIT_BYTES + 1)
        if len(encoded) > _JSON_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_json_artifact(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedJsonArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected, invalid_code)
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedJsonArtifact(
        path=selected,
        payload=payload,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
        invalid_code=invalid_code,
    )


def _verify_artifact_unchanged(artifact: LoadedJsonArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_ORGANIZER_INPUT_CHANGED")


def _publish_working_cut(payload: object, output_path: Path) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_working_cut(payload)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)


def organize_and_publish(
    aligned_path: Path,
    grouping_path: Path,
    *,
    output_path: Path,
) -> dict[str, object]:
    """Compile exact local inputs and atomically publish a working cut."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned = _load_json_artifact(
        aligned_path,
        contract="aligned-transcript-v1",
        invalid_code="TRITRACK_ORGANIZER_ALIGNED_INVALID",
    )
    grouping = _load_json_artifact(
        grouping_path,
        contract="grouping-v1",
        invalid_code="TRITRACK_ORGANIZER_GROUPING_INVALID",
    )
    if grouping.encoded != encode_grouping(grouping.payload):
        raise ValueError("TRITRACK_ORGANIZER_GROUPING_NONCANONICAL")
    working_cut = build_working_cut(
        aligned.payload,
        grouping.payload,
        aligned_sha256=aligned.sha256,
        grouping_sha256=grouping.sha256,
    )
    _verify_artifact_unchanged(aligned)
    _verify_artifact_unchanged(grouping)
    _publish_working_cut(working_cut, destination)
    return working_cut
--- END FILE src/tritrack_editing_assistant/organizer.py ---

--- BEGIN FILE src/tritrack_editing_assistant/paper_edit.py ---
"""Strict XLSX transport for the cue-addressed paper-edit round trip."""

from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import tempfile
import xml.etree.ElementTree as element_tree
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from jsonschema import ValidationError
from openpyxl import Workbook, load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils.exceptions import InvalidFileException

from . import __version__, organizer
from .contracts import validate_contract
from .process import require_absent_output

WORKBOOK_SCHEMA_VERSION = "tritrack.paper-workbook/v1"
CUES_HEADERS = (
    "TakeId",
    "SourceSha256",
    "CueId",
    "StartMs",
    "EndMs",
    "Text",
    "Disposition",
)
QUESTIONS_HEADERS = ("QuestionId", "Question", "Order")
SELECTIONS_HEADERS = (
    "Placement",
    "SegmentId",
    "QuestionId",
    "Order",
    "TakeId",
    "StartCueId",
    "EndCueId",
    "ReserveReason",
    "EditorNote",
)
MANIFEST_HEADERS = ("Key", "Value")
SHEET_NAMES = ("Cues", "Questions", "Selections", "_TriTrack")
_JSON_LIMIT_BYTES = 16 * 1024 * 1024
_WORKBOOK_LIMIT_BYTES = 64 * 1024 * 1024
_WORKBOOK_MEMBER_LIMIT = 512
_WORKBOOK_EXPANDED_LIMIT_BYTES = 256 * 1024 * 1024
_WORKBOOK_SINGLE_MEMBER_LIMIT_BYTES = 128 * 1024 * 1024


@dataclass(frozen=True)
class LoadedArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str
    limit: int


@dataclass(frozen=True)
class ValidatedWorkbook:
    aligned_sha256: str
    workbook_sha256: str
    workbook_schema_version: str
    cue_count: int
    question_count: int
    answer_count: int
    reserve_count: int
    grouping: dict[str, object]


def _read_regular_bytes(path: Path, *, limit: int, invalid_code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_PAPER_INPUT_UNREADABLE") from error
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(limit + 1)
        if len(encoded) > limit:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_json(
    path: Path,
    *,
    contract: str,
    invalid_code: str,
) -> LoadedArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(
        selected,
        limit=_JSON_LIMIT_BYTES,
        invalid_code=invalid_code,
    )
    try:
        payload = json.loads(encoded.decode("utf-8", errors="strict"))
        validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(invalid_code) from error
    return LoadedArtifact(
        selected,
        payload,
        encoded,
        hashlib.sha256(encoded).hexdigest(),
        invalid_code,
        _JSON_LIMIT_BYTES,
    )


def _verify_unchanged(artifact: LoadedArtifact) -> None:
    try:
        encoded = _read_regular_bytes(
            artifact.path,
            limit=artifact.limit,
            invalid_code=artifact.invalid_code,
        )
    except ValueError as error:
        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_PAPER_INPUT_CHANGED")


def _literal(cell: Cell, value: object, *, text_format: bool = False) -> None:
    cell.value = value
    if isinstance(value, str):
        cell.data_type = "s"
    if text_format:
        cell.number_format = "@"


def _write_row(
    worksheet,
    row: int,
    values: Sequence[object],
    *,
    text_columns: frozenset[int] = frozenset(),
) -> None:
    for column, value in enumerate(values, start=1):
        _literal(
            worksheet.cell(row=row, column=column),
            value,
            text_format=column in text_columns,
        )


def _paper_aligned_index(aligned: object) -> organizer.AlignedIndex:
    try:
        aligned_index = organizer.index_aligned_transcript(aligned)
    except ValueError as error:
        raise ValueError("TRITRACK_PAPER_ALIGNED_INVALID") from error
    if any(
        not all(
            character in "\t\n\r"
            or 0x20 <= ord(character) <= 0xD7FF
            or 0xE000 <= ord(character) <= 0xFFFD
            or 0x10000 <= ord(character) <= 0x10FFFF
            for character in take_id
        )
        for take_id in aligned_index.takes
    ):
        raise ValueError("TRITRACK_PAPER_ALIGNED_INVALID")
    return aligned_index


def _cue_rows(aligned: Mapping[str, object]) -> list[tuple[object, ...]]:
    _paper_aligned_index(aligned)
    rows: list[tuple[object, ...]] = []
    takes = aligned["takes"]
    assert isinstance(takes, list)
    for take in takes:
        assert isinstance(take, Mapping)
        if take["status"] != "completed":
            continue
        cues = take["cues"]
        assert isinstance(cues, list)
        for cue in cues:
            assert isinstance(cue, Mapping)
            rows.append(
                (
                    take["takeId"],
                    take["sourceSha256"],
                    cue["cueId"],
                    cue["startMs"],
                    cue["endMs"],
                    cue["text"],
                    cue["disposition"],
                )
            )
    return rows


def _cues_grid_sha256(rows: Sequence[Sequence[object]]) -> str:
    encoded = json.dumps(
        [list(CUES_HEADERS), *[list(row) for row in rows]],
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _project_grouping(
    workbook: Workbook,
    grouping: Mapping[str, object] | None,
) -> tuple[int, int]:
    questions_sheet = workbook["Questions"]
    selections_sheet = workbook["Selections"]
    _write_row(questions_sheet, 1, QUESTIONS_HEADERS, text_columns=frozenset({1}))
    _write_row(
        selections_sheet,
        1,
        SELECTIONS_HEADERS,
        text_columns=frozenset({1, 2, 3, 5, 6, 7}),
    )
    if grouping is None:
        return 0, 0

    questions = grouping["questions"]
    reserve = grouping["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)
    question_count = 0
    selection_count = 0
    for question in sorted(questions, key=lambda item: item["order"]):
        assert isinstance(question, Mapping)
        question_count += 1
        _write_row(
            questions_sheet,
            question_count + 1,
            (question["id"], question["question"], question["order"]),
            text_columns=frozenset({1}),
        )
        answers = question["answers"]
        assert isinstance(answers, list)
        for answer in sorted(answers, key=lambda item: item["order"]):
            assert isinstance(answer, Mapping)
            selection_count += 1
            _write_row(
                selections_sheet,
                selection_count + 1,
                (
                    "ANSWER",
                    answer["id"],
                    question["id"],
                    answer["order"],
                    answer["takeId"],
                    answer["startCueId"],
                    answer["endCueId"],
                    None,
                    answer.get("note"),
                ),
                text_columns=frozenset({1, 2, 3, 5, 6, 7}),
            )
    for item in sorted(reserve, key=lambda candidate: candidate["order"]):
        assert isinstance(item, Mapping)
        selection_count += 1
        _write_row(
            selections_sheet,
            selection_count + 1,
            (
                "RESERVE",
                item["id"],
                None,
                item["order"],
                item["takeId"],
                item["startCueId"],
                item["endCueId"],
                item["reason"],
                item.get("note"),
            ),
            text_columns=frozenset({1, 2, 3, 5, 6, 7}),
        )
    return question_count, selection_count


def _build_workbook(
    aligned: Mapping[str, object],
    *,
    aligned_sha256: str,
    grouping: Mapping[str, object] | None,
) -> tuple[Workbook, dict[str, int]]:
    cue_rows = _cue_rows(aligned)
    workbook = Workbook()
    cues_sheet = workbook.active
    cues_sheet.title = "Cues"
    workbook.create_sheet("Questions")
    workbook.create_sheet("Selections")
    manifest_sheet = workbook.create_sheet("_TriTrack")
    manifest_sheet.sheet_state = "hidden"

    _write_row(cues_sheet, 1, CUES_HEADERS, text_columns=frozenset({1, 2, 3}))
    for row_number, row in enumerate(cue_rows, start=2):
        _write_row(
            cues_sheet,
            row_number,
            row,
            text_columns=frozenset({1, 2, 3}),
        )
    question_count, selection_count = _project_grouping(workbook, grouping)
    _write_row(manifest_sheet, 1, MANIFEST_HEADERS)
    manifest = (
        ("WorkbookSchemaVersion", WORKBOOK_SCHEMA_VERSION),
        ("ToolVersion", __version__),
        ("AlignedTranscriptSha256", aligned_sha256),
        ("CuesGridSha256", _cues_grid_sha256(cue_rows)),
    )
    for row_number, row in enumerate(manifest, start=2):
        _write_row(manifest_sheet, row_number, row, text_columns=frozenset({1, 2}))
    return workbook, {
        "cueCount": len(cue_rows),
        "questionCount": question_count,
        "selectionCount": selection_count,
    }


def _publish_bytes(encoded: bytes, output_path: Path) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)


def export_workbook(
    aligned_path: Path,
    *,
    grouping_path: Path | None,
    output_path: Path,
) -> dict[str, int]:
    """Export one strict aligned authority to an editor-facing workbook."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    aligned = _load_json(
        aligned_path,
        contract="aligned-transcript-v1",
        invalid_code="TRITRACK_PAPER_ALIGNED_INVALID",
    )
    assert isinstance(aligned.payload, Mapping)
    grouping: LoadedArtifact | None = None
    grouping_payload: Mapping[str, object] | None = None
    aligned_index = _paper_aligned_index(aligned.payload)
    if grouping_path is not None:
        grouping = _load_json(
            grouping_path,
            contract="grouping-v1",
            invalid_code="TRITRACK_PAPER_GROUPING_INVALID",
        )
        if grouping.encoded != organizer.encode_grouping(grouping.payload):
            raise ValueError("TRITRACK_PAPER_GROUPING_INVALID")
        grouping_payload = organizer.validate_grouping(
            grouping.payload,
            aligned_index=aligned_index,
            aligned_sha256=aligned.sha256,
        )

    workbook, summary = _build_workbook(
        aligned.payload,
        aligned_sha256=aligned.sha256,
        grouping=grouping_payload,
    )
    buffer = io.BytesIO()
    workbook.save(buffer)
    _verify_unchanged(aligned)
    if grouping is not None:
        _verify_unchanged(grouping)
    _publish_bytes(buffer.getvalue(), destination)
    return summary


def _load_workbook_artifact(path: Path) -> tuple[LoadedArtifact, Workbook]:
    selected = Path(path)
    encoded = _read_regular_bytes(
        selected,
        limit=_WORKBOOK_LIMIT_BYTES,
        invalid_code="TRITRACK_PAPER_WORKBOOK_INVALID",
    )
    artifact = LoadedArtifact(
        selected,
        None,
        encoded,
        hashlib.sha256(encoded).hexdigest(),
        "TRITRACK_PAPER_WORKBOOK_INVALID",
        _WORKBOOK_LIMIT_BYTES,
    )
    try:
        with zipfile.ZipFile(io.BytesIO(encoded)) as archive:
            members = archive.infolist()
            names = [member.filename for member in members]
            expanded_size = 0
            if (
                not members
                or len(members) > _WORKBOOK_MEMBER_LIMIT
                or len(names) != len(set(names))
            ):
                raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
            for member in members:
                member_path = PurePosixPath(member.filename)
                if (
                    member.flag_bits & 0x1
                    or member.filename.startswith(("/", "\\"))
                    or "\\" in member.filename
                    or ".." in member_path.parts
                    or member.filename.lower().endswith("vbaproject.bin")
                    or member.file_size > _WORKBOOK_SINGLE_MEMBER_LIMIT_BYTES
                ):
                    raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
                expanded_size += member.file_size
                if expanded_size > _WORKBOOK_EXPANDED_LIMIT_BYTES:
                    raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    except ValueError:
        raise
    except (
        OSError,
        KeyError,
        TypeError,
        zipfile.BadZipFile,
        InvalidFileException,
        element_tree.ParseError,
    ) as error:
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID") from error

    try:
        workbook = load_workbook(
            io.BytesIO(encoded),
            data_only=False,
            read_only=False,
            keep_links=True,
        )
    except (
        OSError,
        KeyError,
        TypeError,
        ValueError,
        zipfile.BadZipFile,
        InvalidFileException,
        element_tree.ParseError,
    ) as error:
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID") from error
    return artifact, workbook


def _reject_unsafe_workbook_state(
    workbook: Workbook,
    *,
    cue_row_count: int,
) -> None:
    if workbook.sheetnames != list(SHEET_NAMES):
        raise ValueError("TRITRACK_PAPER_SHEETS_INVALID")
    if workbook["_TriTrack"].sheet_state != "hidden" or any(
        workbook[name].sheet_state != "visible" for name in SHEET_NAMES[:-1]
    ):
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    if len(workbook.defined_names) or getattr(workbook, "_external_links", []):
        raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    maximum_dimensions = {
        "Cues": (cue_row_count + 1, len(CUES_HEADERS)),
        "Questions": (cue_row_count + 1, len(QUESTIONS_HEADERS)),
        "Selections": (cue_row_count + 1, len(SELECTIONS_HEADERS)),
        "_TriTrack": (5, len(MANIFEST_HEADERS)),
    }
    for worksheet in workbook.worksheets:
        maximum_rows, maximum_columns = maximum_dimensions[worksheet.title]
        if (
            worksheet.max_row > maximum_rows
            or worksheet.max_column > maximum_columns
        ):
            raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
    for worksheet in workbook.worksheets:
        if worksheet.merged_cells.ranges:
            raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.hyperlink is not None:
                    raise ValueError("TRITRACK_PAPER_WORKBOOK_INVALID")
                if cell.data_type == "f":
                    raise ValueError("TRITRACK_PAPER_FORMULA_FORBIDDEN")


def _sheet_rows(
    worksheet,
    headers: Sequence[str],
    *,
    invalid_code: str,
) -> list[tuple[object, ...]]:
    actual_headers = tuple(
        worksheet.cell(row=1, column=column).value
        for column in range(1, len(headers) + 1)
    )
    if actual_headers != tuple(headers):
        raise ValueError(invalid_code)
    if any(
        worksheet.cell(row=row, column=column).value is not None
        for row in range(1, worksheet.max_row + 1)
        for column in range(len(headers) + 1, worksheet.max_column + 1)
    ):
        raise ValueError(invalid_code)
    raw_rows = [
        tuple(
            worksheet.cell(row=row, column=column).value
            for column in range(1, len(headers) + 1)
        )
        for row in range(2, worksheet.max_row + 1)
    ]
    while raw_rows and all(value is None for value in raw_rows[-1]):
        raw_rows.pop()
    if any(all(value is None for value in row) for row in raw_rows):
        raise ValueError(invalid_code)
    return raw_rows


def _require_exact_row_types(
    actual: Sequence[object],
    expected: Sequence[object],
) -> None:
    if len(actual) != len(expected) or any(
        value != reference or type(value) is not type(reference)
        for value, reference in zip(actual, expected, strict=True)
    ):
        raise ValueError("TRITRACK_PAPER_REFERENCE_MISMATCH")


def _verify_cues_grid(
    workbook: Workbook,
    aligned: Mapping[str, object],
) -> list[tuple[object, ...]]:
    expected = _cue_rows(aligned)
    actual = _sheet_rows(
        workbook["Cues"],
        CUES_HEADERS,
        invalid_code="TRITRACK_PAPER_REFERENCE_MISMATCH",
    )
    if len(actual) != len(expected):
        raise ValueError("TRITRACK_PAPER_REFERENCE_MISMATCH")
    for actual_row, expected_row in zip(actual, expected, strict=True):
        _require_exact_row_types(actual_row, expected_row)
    return expected


def _verify_manifest(
    workbook: Workbook,
    *,
    aligned_sha256: str,
    cue_rows: Sequence[Sequence[object]],
) -> None:
    expected = [
        ("WorkbookSchemaVersion", WORKBOOK_SCHEMA_VERSION),
        ("ToolVersion", __version__),
        ("AlignedTranscriptSha256", aligned_sha256),
        ("CuesGridSha256", _cues_grid_sha256(cue_rows)),
    ]
    actual = _sheet_rows(
        workbook["_TriTrack"],
        MANIFEST_HEADERS,
        invalid_code="TRITRACK_PAPER_MANIFEST_MISMATCH",
    )
    if actual != expected:
        raise ValueError("TRITRACK_PAPER_MANIFEST_MISMATCH")


def _canonical_workbook_text(
    value: object,
    *,
    maximum: int,
    required: bool,
) -> str | None:
    try:
        return organizer.canonical_editor_text(
            value,
            maximum=maximum,
            required=required,
        )
    except (TypeError, ValueError) as error:
        raise ValueError("TRITRACK_PAPER_ROW_INVALID") from error


def _positive_integer(value: object) -> int:
    if type(value) is not int or value < 1:
        raise ValueError("TRITRACK_PAPER_ROW_INVALID")
    return value


def _required_string(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("TRITRACK_PAPER_ROW_INVALID")
    return value


def _grouping_from_workbook(
    workbook: Workbook,
    *,
    aligned_index: organizer.AlignedIndex,
    aligned_sha256: str,
) -> dict[str, object]:
    question_rows = _sheet_rows(
        workbook["Questions"],
        QUESTIONS_HEADERS,
        invalid_code="TRITRACK_PAPER_ROW_INVALID",
    )
    selection_rows = _sheet_rows(
        workbook["Selections"],
        SELECTIONS_HEADERS,
        invalid_code="TRITRACK_PAPER_ROW_INVALID",
    )
    questions: list[dict[str, object]] = []
    questions_by_id: dict[str, dict[str, object]] = {}
    for question_id, question_text, order in question_rows:
        identifier = _required_string(question_id)
        question = {
            "id": identifier,
            "question": _canonical_workbook_text(
                question_text,
                maximum=organizer.QUESTION_TEXT_LIMIT,
                required=True,
            ),
            "order": _positive_integer(order),
            "answers": [],
        }
        if identifier in questions_by_id:
            raise ValueError("TRITRACK_ORGANIZER_DUPLICATE_ID")
        questions.append(question)
        questions_by_id[identifier] = question

    reserve: list[dict[str, object]] = []
    for row in selection_rows:
        (
            placement,
            segment_id,
            question_id,
            order,
            take_id,
            start_cue_id,
            end_cue_id,
            reserve_reason,
            editor_note,
        ) = row
        placement = _required_string(placement)
        common: dict[str, object] = {
            "id": _required_string(segment_id),
            "order": _positive_integer(order),
            "takeId": _required_string(take_id),
            "startCueId": _required_string(start_cue_id),
            "endCueId": _required_string(end_cue_id),
        }
        note = _canonical_workbook_text(
            editor_note,
            maximum=organizer.NOTE_TEXT_LIMIT,
            required=False,
        )
        if note is not None:
            common["note"] = note
        if placement == "ANSWER":
            if reserve_reason not in {None, ""}:
                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
            selected_question = questions_by_id.get(_required_string(question_id))
            if selected_question is None:
                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
            answers = selected_question["answers"]
            assert isinstance(answers, list)
            answers.append(common)
        elif placement == "RESERVE":
            if question_id not in {None, ""}:
                raise ValueError("TRITRACK_PAPER_ROW_INVALID")
            common["reason"] = _canonical_workbook_text(
                reserve_reason,
                maximum=organizer.QUESTION_TEXT_LIMIT,
                required=True,
            )
            reserve.append(common)
        else:
            raise ValueError("TRITRACK_PAPER_ROW_INVALID")

    grouping: dict[str, object] = {
        "schemaVersion": "tritrack.grouping/v1",
        "alignedTranscriptSha256": aligned_sha256,
        "questions": questions,
        "reserve": reserve,
    }
    return organizer.validate_grouping(
        grouping,
        aligned_index=aligned_index,
        aligned_sha256=aligned_sha256,
    )


def validate_workbook(
    aligned_path: Path,
    workbook_path: Path,
) -> ValidatedWorkbook:
    """Validate and re-derive one workbook without publishing output."""

    aligned = _load_json(
        aligned_path,
        contract="aligned-transcript-v1",
        invalid_code="TRITRACK_PAPER_ALIGNED_INVALID",
    )
    workbook_artifact, workbook = _load_workbook_artifact(workbook_path)
    assert isinstance(aligned.payload, Mapping)
    aligned_index = _paper_aligned_index(aligned.payload)
    cue_rows = _cue_rows(aligned.payload)
    _reject_unsafe_workbook_state(workbook, cue_row_count=len(cue_rows))
    cue_rows = _verify_cues_grid(workbook, aligned.payload)
    _verify_manifest(
        workbook,
        aligned_sha256=aligned.sha256,
        cue_rows=cue_rows,
    )
    grouping = _grouping_from_workbook(
        workbook,
        aligned_index=aligned_index,
        aligned_sha256=aligned.sha256,
    )
    _verify_unchanged(aligned)
    _verify_unchanged(workbook_artifact)
    questions = grouping["questions"]
    reserve = grouping["reserve"]
    assert isinstance(questions, list)
    assert isinstance(reserve, list)
    answer_count = 0
    for question in questions:
        assert isinstance(question, Mapping)
        answers = question["answers"]
        assert isinstance(answers, list)
        answer_count += len(answers)
    return ValidatedWorkbook(
        aligned_sha256=aligned.sha256,
        workbook_sha256=workbook_artifact.sha256,
        workbook_schema_version=WORKBOOK_SCHEMA_VERSION,
        cue_count=len(cue_rows),
        question_count=len(questions),
        answer_count=answer_count,
        reserve_count=len(reserve),
        grouping=grouping,
    )


def apply_workbook(
    aligned_path: Path,
    workbook_path: Path,
    *,
    output_path: Path,
) -> dict[str, object]:
    """Apply strict workbook intent and publish canonical grouping JSON."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    validated = validate_workbook(aligned_path, workbook_path)
    _publish_bytes(organizer.encode_grouping(validated.grouping), destination)
    return validated.grouping
--- END FILE src/tritrack_editing_assistant/paper_edit.py ---

--- BEGIN FILE src/tritrack_editing_assistant/run_workflow.py ---
"""Immutable run manifests and complete bundle publication."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import stat
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import (
    __version__,
    align_text,
    contracts,
    doctor,
    emit_fcpxml,
    organizer,
    paper_edit,
    process,
    story_fcpxml,
    sync_scan,
    transcribe_takes,
)

MANIFEST_FILE_NAME = "run-manifest.json"
_MANIFEST_LIMIT_BYTES = 16 * 1024 * 1024
_ARTIFACT_LIMIT_BYTES = 512 * 1024 * 1024
_HASH_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class PhaseSpec:
    next_action: str
    chain_length: int
    artifacts: tuple[tuple[str, str], ...]
    stages: tuple[str, ...]


PHASE_SPECS = {
    "prepared": PhaseSpec(
        next_action="provide-revision",
        chain_length=0,
        artifacts=(
            ("doctorReceipt", "doctor.json"),
            ("syncMap", "sync-map.json"),
            ("transcriptBundle", "transcript-bundle.json"),
            ("stringOut", "string-out.fcpxml"),
        ),
        stages=("doctor", "sync", "transcribe", "emit"),
    ),
    "aligned": PhaseSpec(
        next_action="edit-paper-workbook",
        chain_length=1,
        artifacts=(
            ("alignedTranscript", "aligned-transcript.json"),
            ("paperWorkbook", "paper-edit.xlsx"),
        ),
        stages=("align", "paper"),
    ),
    "finished": PhaseSpec(
        next_action="complete",
        chain_length=2,
        artifacts=(
            ("grouping", "grouping.json"),
            ("workingCut", "working-cut.json"),
            ("storyCut", "story-cut.fcpxml"),
        ),
        stages=("paper", "organize", "emit"),
    ),
}


@dataclass(frozen=True)
class LoadedRunArtifact:
    logical_name: str
    file_name: str
    path: Path
    encoded: bytes
    sha256: str


@dataclass(frozen=True)
class LoadedRunBundle:
    root: Path
    manifest: dict[str, object]
    manifest_bytes: bytes
    manifest_sha256: str
    artifacts: Mapping[str, LoadedRunArtifact]


def _manifest_error(error: BaseException | None = None) -> ValueError:
    result = ValueError("TRITRACK_RUN_MANIFEST_INVALID")
    if error is not None:
        result.__cause__ = error
    return result


def _validate_manifest(payload: object) -> dict[str, object]:
    try:
        contracts.validate_contract("run-manifest-v1", payload)
    except (TypeError, ValueError, ValidationError) as error:
        raise _manifest_error(error)
    if not isinstance(payload, dict):
        raise _manifest_error()
    phase = payload["phase"]
    if not isinstance(phase, str) or phase not in PHASE_SPECS:
        raise _manifest_error()
    spec = PHASE_SPECS[phase]
    if (
        payload["nextAction"] != spec.next_action
        or len(payload["manifestChain"]) != spec.chain_length
    ):
        raise _manifest_error()

    sources = payload["sources"]
    assert isinstance(sources, list)
    source_order = [(source["camera"], source["mediaId"]) for source in sources]
    media_ids = [source["mediaId"] for source in sources]
    if source_order != sorted(source_order) or len(media_ids) != len(set(media_ids)):
        raise _manifest_error()

    artifacts = payload["artifacts"]
    assert isinstance(artifacts, dict)
    expected_artifacts = dict(spec.artifacts)
    if set(artifacts) != set(expected_artifacts):
        raise _manifest_error()
    for logical_name, file_name in spec.artifacts:
        artifact = artifacts[logical_name]
        if not isinstance(artifact, Mapping) or artifact["fileName"] != file_name:
            raise _manifest_error()

    stages = payload["stages"]
    assert isinstance(stages, list)
    if [stage["name"] for stage in stages] != list(spec.stages):
        raise _manifest_error()
    for stage, expected_name in zip(stages, spec.stages, strict=True):
        assert isinstance(stage, Mapping)
        output_hashes = stage["outputHashes"]
        expected_logical = dict(zip(spec.stages, spec.artifacts, strict=True))[
            expected_name
        ][0]
        if output_hashes != {
            expected_logical: artifacts[expected_logical]["sha256"]
        }:
            raise _manifest_error()
    return payload


def build_manifest(
    *,
    run_id: str,
    profile_id: str,
    binding_id: str,
    phase: str,
    manifest_chain: Sequence[str],
    sources: Sequence[Mapping[str, object]],
    stages: Sequence[Mapping[str, object]],
    artifacts: Mapping[str, Mapping[str, str]],
) -> dict[str, object]:
    """Build one path-free immutable run receipt from completed stage facts."""

    try:
        spec = PHASE_SPECS[phase]
        expected_artifacts = {logical_name for logical_name, _ in spec.artifacts}
        if set(artifacts) != expected_artifacts:
            raise ValueError
        source_copies = [copy.deepcopy(dict(source)) for source in sources]
        source_copies.sort(key=lambda source: (source["camera"], source["mediaId"]))
        stage_by_name = {
            stage["name"]: copy.deepcopy(dict(stage)) for stage in stages
        }
        if (
            len(stage_by_name) != len(stages)
            or set(stage_by_name) != set(spec.stages)
        ):
            raise ValueError
        artifact_copies = {
            logical_name: copy.deepcopy(dict(artifacts[logical_name]))
            for logical_name, _ in spec.artifacts
        }
        payload: dict[str, object] = {
            "schemaVersion": "tritrack.run-manifest/v1",
            "toolVersion": __version__,
            "runId": run_id,
            "profileId": profile_id,
            "bindingId": binding_id,
            "phase": phase,
            "nextAction": spec.next_action,
            "manifestChain": list(manifest_chain),
            "sources": source_copies,
            "artifacts": artifact_copies,
            "stages": [stage_by_name[name] for name in spec.stages],
        }
    except (KeyError, TypeError, ValueError) as error:
        raise _manifest_error(error)
    return _validate_manifest(payload)


def encode_manifest(payload: object) -> bytes:
    """Return canonical UTF-8 bytes for one semantically strict manifest."""

    validated = _validate_manifest(payload)
    return (
        json.dumps(validated, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= limit:
            raise ValueError(code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(limit + 1)
        if len(encoded) > limit:
            raise ValueError(code)
        return encoded
    except OSError as error:
        raise ValueError(code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _validate_json_artifact(
    encoded: bytes, *, contract: str, code: str
) -> object:
    try:
        payload = json.loads(
            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
        )
        contracts.validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(code) from error
    return payload


def _validate_artifact(
    logical_name: str,
    encoded: bytes,
    *,
    manifest: Mapping[str, object],
) -> None:
    contracts_by_name = {
        "syncMap": "sync-map-v1",
        "transcriptBundle": "transcript-bundle-v1",
        "alignedTranscript": "aligned-transcript-v1",
        "grouping": "grouping-v1",
        "workingCut": "working-cut-v1",
    }
    contract = contracts_by_name.get(logical_name)
    if contract is not None:
        _validate_json_artifact(
            encoded, contract=contract, code="TRITRACK_RUN_ARTIFACT_INVALID"
        )
        return
    if logical_name == "doctorReceipt":
        try:
            payload = json.loads(encoded.decode("utf-8", errors="strict"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error
        if (
            not isinstance(payload, dict)
            or payload.get("schemaVersion") != "tritrack.doctor-receipt/v1"
            or payload.get("profileId") != manifest["profileId"]
            or payload.get("titleBindingId") != manifest["bindingId"]
            or not isinstance(payload.get("supported"), bool)
            or not isinstance(payload.get("checks"), list)
            or not isinstance(payload.get("remediation"), list)
        ):
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID")
        return
    if logical_name in {"stringOut", "storyCut"}:
        try:
            text = encoded.decode("utf-8", errors="strict")
            emit_fcpxml.validate_fcpxml(
                text,
                profile=doctor.load_profile(str(manifest["profileId"])),
                binding=doctor.load_title_binding(str(manifest["bindingId"])),
            )
        except (UnicodeError, TypeError, ValueError, ValidationError) as error:
            raise ValueError("TRITRACK_RUN_ARTIFACT_INVALID") from error


def _bundle_directory(path: Path) -> Path:
    selected = Path(path)
    try:
        metadata = selected.lstat()
    except (FileNotFoundError, NotADirectoryError, PermissionError) as error:
        raise ValueError("TRITRACK_RUN_INPUT_UNREADABLE") from error
    except OSError as error:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
    return selected


def load_bundle(
    path: Path, *, expected_phase: str | None = None
) -> LoadedRunBundle:
    """Load and verify one complete immutable run bundle."""

    root = _bundle_directory(path)
    manifest_path = root / MANIFEST_FILE_NAME
    if not os.path.lexists(manifest_path):
        raise ValueError("TRITRACK_RUN_BUNDLE_INCOMPLETE")
    manifest_bytes = _read_regular_bytes(
        manifest_path,
        limit=_MANIFEST_LIMIT_BYTES,
        code="TRITRACK_RUN_MANIFEST_INVALID",
    )
    try:
        payload = json.loads(manifest_bytes.decode("utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_RUN_MANIFEST_INVALID") from error
    manifest = _validate_manifest(payload)
    if manifest_bytes != encode_manifest(manifest):
        raise ValueError("TRITRACK_RUN_MANIFEST_NONCANONICAL")
    if expected_phase is not None and manifest["phase"] != expected_phase:
        raise ValueError("TRITRACK_RUN_PHASE_MISMATCH")

    artifacts_payload = manifest["artifacts"]
    assert isinstance(artifacts_payload, Mapping)
    expected_entries = {MANIFEST_FILE_NAME}
    expected_entries.update(
        str(artifact["fileName"]) for artifact in artifacts_payload.values()
    )
    try:
        observed_entries = {entry.name for entry in os.scandir(root)}
    except OSError as error:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID") from error
    if observed_entries != expected_entries:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")

    loaded: dict[str, LoadedRunArtifact] = {}
    for logical_name, artifact_payload in artifacts_payload.items():
        assert isinstance(artifact_payload, Mapping)
        file_name = str(artifact_payload["fileName"])
        encoded = _read_regular_bytes(
            root / file_name,
            limit=_ARTIFACT_LIMIT_BYTES,
            code="TRITRACK_RUN_ARTIFACT_INVALID",
        )
        observed_hash = hashlib.sha256(encoded).hexdigest()
        if observed_hash != artifact_payload["sha256"]:
            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
        _validate_artifact(logical_name, encoded, manifest=manifest)
        loaded[logical_name] = LoadedRunArtifact(
            logical_name=logical_name,
            file_name=file_name,
            path=root / file_name,
            encoded=encoded,
            sha256=observed_hash,
        )
    return LoadedRunBundle(
        root=root,
        manifest=manifest,
        manifest_bytes=manifest_bytes,
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),
        artifacts=loaded,
    )


def summarize_bundle(bundle: LoadedRunBundle) -> dict[str, object]:
    """Return a path-free and text-free status projection."""

    if not isinstance(bundle, LoadedRunBundle):
        raise TypeError("TRITRACK_RUN_BUNDLE_INVALID")
    return {
        "schemaVersion": "tritrack.run-summary/v1",
        "runId": bundle.manifest["runId"],
        "phase": bundle.manifest["phase"],
        "nextAction": bundle.manifest["nextAction"],
        "stages": [stage["name"] for stage in bundle.manifest["stages"]],
        "artifacts": {
            logical_name: artifact.sha256
            for logical_name, artifact in bundle.artifacts.items()
        },
    }


def _write_manifest(path: Path, encoded: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _verify_staging(staging: Path, manifest: Mapping[str, object]) -> None:
    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, Mapping)
    expected = {str(artifact["fileName"]) for artifact in artifacts.values()}
    observed = {entry.name for entry in os.scandir(staging)}
    if observed != expected:
        raise ValueError("TRITRACK_RUN_BUNDLE_INVALID")
    for logical_name, artifact in artifacts.items():
        assert isinstance(artifact, Mapping)
        encoded = _read_regular_bytes(
            staging / str(artifact["fileName"]),
            limit=_ARTIFACT_LIMIT_BYTES,
            code="TRITRACK_RUN_ARTIFACT_INVALID",
        )
        if hashlib.sha256(encoded).hexdigest() != artifact["sha256"]:
            raise ValueError("TRITRACK_RUN_ARTIFACT_HASH_MISMATCH")
        _validate_artifact(str(logical_name), encoded, manifest=manifest)


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def publish_bundle(
    output_dir: Path,
    builder: Callable[[Path], Mapping[str, object]],
) -> LoadedRunBundle:
    """Build privately, then hard-link a complete absent bundle manifest last."""

    destination = process.require_absent_output(output_dir)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.staging-", dir=destination.parent
        )
    )
    reserved = False
    linked: list[Path] = []
    try:
        manifest = _validate_manifest(builder(staging))
        _verify_staging(staging, manifest)
        manifest_bytes = encode_manifest(manifest)
        _write_manifest(staging / MANIFEST_FILE_NAME, manifest_bytes)
        try:
            os.mkdir(destination, 0o755)
            reserved = True
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error

        artifacts = manifest["artifacts"]
        assert isinstance(artifacts, Mapping)
        file_names = sorted(
            str(artifact["fileName"]) for artifact in artifacts.values()
        )
        for file_name in (*file_names, MANIFEST_FILE_NAME):
            target = destination / file_name
            os.link(staging / file_name, target)
            linked.append(target)
        _fsync_directory(destination)
        return load_bundle(destination, expected_phase=str(manifest["phase"]))
    except BaseException:
        if reserved:
            for path in reversed(linked):
                try:
                    path.unlink()
                except OSError:
                    pass
            try:
                destination.rmdir()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def _hash_regular_path(path: Path, *, code: str) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    digest = hashlib.sha256()
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
            raise ValueError(code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            while chunk := stream.read(_HASH_CHUNK_BYTES):
                digest.update(chunk)
    except OSError as error:
        raise ValueError(code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return digest.hexdigest()


def _hash_value(payload: object) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _artifact_records(
    staging: Path, phase: str
) -> dict[str, dict[str, str]]:
    return {
        logical_name: {
            "fileName": file_name,
            "sha256": _hash_regular_path(
                staging / file_name, code="TRITRACK_RUN_ARTIFACT_INVALID"
            ),
        }
        for logical_name, file_name in PHASE_SPECS[phase].artifacts
    }


def _source_inventory(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    transcribe_media: Sequence[Path],
) -> tuple[list[dict[str, object]], dict[Path, str]]:
    if not camera_a_sources or not camera_b_sources:
        raise ValueError("TRITRACK_RUN_SOURCE_REQUIRED")
    declared: list[tuple[str, sync_scan.MediaSource]] = [
        *(("A", source) for source in camera_a_sources),
        *(("B", source) for source in camera_b_sources),
    ]
    media_ids = [source.media_id for _, source in declared]
    if (
        len(media_ids) != len(set(media_ids))
        or any(source.media_id != source.path.name for _, source in declared)
    ):
        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
    declared_paths = [source.path for _, source in declared]
    if len(declared_paths) != len(set(declared_paths)):
        raise ValueError("TRITRACK_RUN_SOURCE_ID_DUPLICATE")
    selected_transcribe = [Path(path) for path in transcribe_media]
    if (
        not selected_transcribe
        or len(selected_transcribe) != len(set(selected_transcribe))
        or any(path not in declared_paths for path in selected_transcribe)
    ):
        raise ValueError("TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID")
    source_hashes = {
        source.path: _hash_regular_path(
            source.path, code="TRITRACK_RUN_INPUT_UNREADABLE"
        )
        for _, source in declared
    }
    selected_set = set(selected_transcribe)
    inventory = [
        {
            "camera": camera,
            "mediaId": source.media_id,
            "sha256": source_hashes[source.path],
            "transcribed": source.path in selected_set,
        }
        for camera, source in declared
    ]
    return inventory, source_hashes


def _require_inputs_unchanged(
    source_hashes: Mapping[Path, str], *, model_path: Path, model_sha256: str
) -> None:
    if _hash_regular_path(
        model_path, code="TRITRACK_RUN_INPUT_CHANGED"
    ) != model_sha256 or any(
        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
        for path, expected in source_hashes.items()
    ):
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def prepare_run(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    transcribe_media: Sequence[Path],
    *,
    model_path: Path,
    language: str,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
    run_id: str,
    output_dir: Path,
) -> dict[str, object]:
    """Publish a doctor／sync／transcript／string-out prepared run bundle."""

    process.require_absent_output(output_dir)
    inventory, source_hashes = _source_inventory(
        camera_a_sources, camera_b_sources, transcribe_media
    )
    selected_model = Path(model_path)
    model_sha256 = _hash_regular_path(
        selected_model, code="TRITRACK_RUN_INPUT_UNREADABLE"
    )
    selected_transcribe = [Path(path) for path in transcribe_media]
    profile_hash = _hash_value(doctor.load_profile(profile_id))
    binding_hash = _hash_value(doctor.load_title_binding(binding_id))
    source_set_hash = _hash_value(inventory)
    transcribed_hash = _hash_value(
        [
            source
            for source in sorted(inventory, key=lambda item: item["mediaId"])
            if source["transcribed"]
        ]
    )

    def build(staging: Path) -> dict[str, object]:
        receipt = doctor.write_receipt(
            staging / "doctor.json",
            profile_id=profile_id,
            transcription_requested=True,
            whisper_model=selected_model,
        )
        if receipt.get("supported") is not True:
            raise ValueError("TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED")
        sync_scan.synchronize_and_publish(
            camera_a_sources,
            camera_b_sources,
            profile_id=profile_id,
            output_path=staging / "sync-map.json",
        )
        transcribe_takes.transcribe_and_publish(
            selected_transcribe,
            model_path=selected_model,
            language=language,
            output_path=staging / "transcript-bundle.json",
        )
        emit_fcpxml.emit_and_publish(
            camera_a_sources,
            camera_b_sources,
            sync_map_path=staging / "sync-map.json",
            profile_id=profile_id,
            binding_id=binding_id,
            metadata=metadata,
            output_path=staging / "string-out.fcpxml",
        )
        _require_inputs_unchanged(
            source_hashes, model_path=selected_model, model_sha256=model_sha256
        )
        artifacts = _artifact_records(staging, "prepared")
        stages = [
            {
                "name": "doctor",
                "inputHashes": {
                    "binding": binding_hash,
                    "model": model_sha256,
                    "profile": profile_hash,
                },
                "outputHashes": {
                    "doctorReceipt": artifacts["doctorReceipt"]["sha256"]
                },
            },
            {
                "name": "sync",
                "inputHashes": {"sourceSet": source_set_hash},
                "outputHashes": {"syncMap": artifacts["syncMap"]["sha256"]},
            },
            {
                "name": "transcribe",
                "inputHashes": {
                    "model": model_sha256,
                    "transcribedSources": transcribed_hash,
                },
                "outputHashes": {
                    "transcriptBundle": artifacts["transcriptBundle"]["sha256"]
                },
            },
            {
                "name": "emit",
                "inputHashes": {
                    "binding": binding_hash,
                    "profile": profile_hash,
                    "sourceSet": source_set_hash,
                    "syncMap": artifacts["syncMap"]["sha256"],
                },
                "outputHashes": {"stringOut": artifacts["stringOut"]["sha256"]},
            },
        ]
        return build_manifest(
            run_id=run_id,
            profile_id=profile_id,
            binding_id=binding_id,
            phase="prepared",
            manifest_chain=[],
            sources=inventory,
            stages=stages,
            artifacts=artifacts,
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def _require_bundle_unchanged(bundle: LoadedRunBundle) -> None:
    try:
        current = load_bundle(bundle.root, expected_phase=str(bundle.manifest["phase"]))
    except ValueError as error:
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED") from error
    if current.manifest_sha256 != bundle.manifest_sha256:
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def align_run(
    prepared_dir: Path,
    revision_path: Path,
    *,
    output_dir: Path,
) -> dict[str, object]:
    """Consume one complete prepared run and publish an aligned paper bundle."""

    process.require_absent_output(output_dir)
    prepared = load_bundle(prepared_dir, expected_phase="prepared")
    revision = align_text.load_json_artifact(
        Path(revision_path),
        contract="text-revision-v1",
        invalid_code="TRITRACK_ALIGNMENT_REVISION_INVALID",
    )

    def build(staging: Path) -> dict[str, object]:
        align_text.align_and_publish(
            prepared.artifacts["transcriptBundle"].path,
            revision.path,
            output_path=staging / "aligned-transcript.json",
        )
        paper_edit.export_workbook(
            staging / "aligned-transcript.json",
            grouping_path=None,
            output_path=staging / "paper-edit.xlsx",
        )
        align_text.verify_artifact_unchanged(revision)
        _require_bundle_unchanged(prepared)
        artifacts = _artifact_records(staging, "aligned")
        stages = [
            {
                "name": "align",
                "inputHashes": {
                    "preparedManifest": prepared.manifest_sha256,
                    "revision": revision.sha256,
                    "transcriptBundle": prepared.artifacts[
                        "transcriptBundle"
                    ].sha256,
                },
                "outputHashes": {
                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
                },
            },
            {
                "name": "paper",
                "inputHashes": {
                    "alignedTranscript": artifacts["alignedTranscript"]["sha256"]
                },
                "outputHashes": {
                    "paperWorkbook": artifacts["paperWorkbook"]["sha256"]
                },
            },
        ]
        return build_manifest(
            run_id=str(prepared.manifest["runId"]),
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            phase="aligned",
            manifest_chain=[prepared.manifest_sha256],
            sources=prepared.manifest["sources"],
            stages=stages,
            artifacts=artifacts,
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def _finish_source_hashes(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    expected_sources: object,
) -> dict[Path, str]:
    if not camera_a_sources or not camera_b_sources:
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    declared: list[tuple[str, sync_scan.MediaSource]] = [
        *(("A", source) for source in camera_a_sources),
        *(("B", source) for source in camera_b_sources),
    ]
    media_ids = [source.media_id for _, source in declared]
    paths = [source.path for _, source in declared]
    if (
        len(media_ids) != len(set(media_ids))
        or len(paths) != len(set(paths))
        or any(source.media_id != source.path.name for _, source in declared)
    ):
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    try:
        hashes = {
            source.path: _hash_regular_path(
                source.path, code="TRITRACK_RUN_SOURCE_MISMATCH"
            )
            for _, source in declared
        }
        expected_by_id = {
            str(source["mediaId"]): source for source in expected_sources
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH") from error
    if set(media_ids) != set(expected_by_id):
        raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    for camera, source in declared:
        expected = expected_by_id[source.media_id]
        if (
            expected["camera"] != camera
            or expected["sha256"] != hashes[source.path]
        ):
            raise ValueError("TRITRACK_RUN_SOURCE_MISMATCH")
    return hashes


def _require_path_hashes_unchanged(path_hashes: Mapping[Path, str]) -> None:
    if any(
        _hash_regular_path(path, code="TRITRACK_RUN_INPUT_CHANGED") != expected
        for path, expected in path_hashes.items()
    ):
        raise ValueError("TRITRACK_RUN_INPUT_CHANGED")


def _validate_finish_chain(
    prepared: LoadedRunBundle, aligned: LoadedRunBundle
) -> None:
    if aligned.manifest["manifestChain"] != [prepared.manifest_sha256]:
        raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")
    for field in ("runId", "profileId", "bindingId", "sources"):
        if aligned.manifest[field] != prepared.manifest[field]:
            raise ValueError("TRITRACK_RUN_CHAIN_MISMATCH")


def finish_run(
    prepared_dir: Path,
    aligned_dir: Path,
    workbook_path: Path,
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    metadata: emit_fcpxml.ProjectMetadata,
    output_dir: Path,
) -> dict[str, object]:
    """Apply paper intent and publish one exact story-cut result bundle."""

    process.require_absent_output(output_dir)
    prepared = load_bundle(prepared_dir, expected_phase="prepared")
    aligned = load_bundle(aligned_dir, expected_phase="aligned")
    _validate_finish_chain(prepared, aligned)
    source_hashes = _finish_source_hashes(
        camera_a_sources,
        camera_b_sources,
        expected_sources=prepared.manifest["sources"],
    )
    selected_workbook = Path(workbook_path)
    workbook_sha256 = _hash_regular_path(
        selected_workbook, code="TRITRACK_PAPER_WORKBOOK_INVALID"
    )
    source_set_hash = _hash_value(prepared.manifest["sources"])

    def build(staging: Path) -> dict[str, object]:
        paper_edit.apply_workbook(
            aligned.artifacts["alignedTranscript"].path,
            selected_workbook,
            output_path=staging / "grouping.json",
        )
        organizer.organize_and_publish(
            aligned.artifacts["alignedTranscript"].path,
            staging / "grouping.json",
            output_path=staging / "working-cut.json",
        )
        story_fcpxml.emit_story_and_publish(
            camera_a_sources,
            camera_b_sources,
            sync_map_path=prepared.artifacts["syncMap"].path,
            aligned_path=aligned.artifacts["alignedTranscript"].path,
            grouping_path=staging / "grouping.json",
            working_cut_path=staging / "working-cut.json",
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            metadata=metadata,
            output_path=staging / "story-cut.fcpxml",
        )
        _require_bundle_unchanged(prepared)
        _require_bundle_unchanged(aligned)
        _require_path_hashes_unchanged(
            {**source_hashes, selected_workbook: workbook_sha256}
        )
        artifacts = _artifact_records(staging, "finished")
        stages = [
            {
                "name": "paper",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "workbook": workbook_sha256,
                },
                "outputHashes": {"grouping": artifacts["grouping"]["sha256"]},
            },
            {
                "name": "organize",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "grouping": artifacts["grouping"]["sha256"],
                },
                "outputHashes": {
                    "workingCut": artifacts["workingCut"]["sha256"]
                },
            },
            {
                "name": "emit",
                "inputHashes": {
                    "alignedTranscript": aligned.artifacts[
                        "alignedTranscript"
                    ].sha256,
                    "grouping": artifacts["grouping"]["sha256"],
                    "sourceSet": source_set_hash,
                    "syncMap": prepared.artifacts["syncMap"].sha256,
                    "workingCut": artifacts["workingCut"]["sha256"],
                },
                "outputHashes": {"storyCut": artifacts["storyCut"]["sha256"]},
            },
        ]
        return build_manifest(
            run_id=str(prepared.manifest["runId"]),
            profile_id=str(prepared.manifest["profileId"]),
            binding_id=str(prepared.manifest["bindingId"]),
            phase="finished",
            manifest_chain=[prepared.manifest_sha256, aligned.manifest_sha256],
            sources=prepared.manifest["sources"],
            stages=stages,
            artifacts=artifacts,
        )

    return summarize_bundle(publish_bundle(Path(output_dir), build))


def inspect_run(
    run_dir: Path,
) -> tuple[LoadedRunBundle, dict[str, object]]:
    """Validate, recheck, and summarize one run without writing anything."""

    bundle = load_bundle(Path(run_dir))
    _require_bundle_unchanged(bundle)
    return bundle, summarize_bundle(bundle)


def status_run(run_dir: Path) -> dict[str, object]:
    """Validate and summarize one run bundle without writing anything."""

    return inspect_run(run_dir)[1]
--- END FILE src/tritrack_editing_assistant/run_workflow.py ---

--- BEGIN FILE src/tritrack_editing_assistant/story_fcpxml.py ---
"""Deterministic projection of exact editorial authorities into story time."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import xml.etree.ElementTree as ET
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from jsonschema import ValidationError

from . import (
    contracts,
    doctor,
    emit_fcpxml,
    organizer,
    process,
    string_out,
    sync_scan,
)

_SOURCE_FIELDS = frozenset(
    {"camera", "media_id", "path", "duration_seconds", "sha256"}
)
_JSON_LIMIT_BYTES = 16 * 1024 * 1024
_HASH_CHUNK_BYTES = 1024 * 1024


@dataclass(frozen=True)
class StorySource:
    """One exact local source available to the story projection."""

    camera: str
    media_id: str
    path: Path
    duration_frames: int
    sha256: str


@dataclass(frozen=True)
class StoryClip:
    """One source excerpt placed inside a story segment."""

    camera: str
    media_id: str
    path: Path
    offset_frames: int
    start_frames: int
    duration_frames: int
    audio_enabled: bool


@dataclass(frozen=True)
class StorySegment:
    """One selected cue range in final editor story order."""

    segment_id: str
    offset_frames: int
    duration_frames: int
    title_text: str
    clips: tuple[StoryClip, ...]


@dataclass(frozen=True)
class StoryTimeline:
    """A complete story projection expressed only in integer frames."""

    profile_id: str
    frame_numerator: int
    frame_denominator: int
    duration_frames: int
    sources: tuple[StorySource, ...]
    segments: tuple[StorySegment, ...]


@dataclass(frozen=True)
class _SourceRelationship:
    kind: str
    source_a: StorySource | None
    source_b: StorySource | None
    offset_b_from_a_frames: int
    audio_master: str


@dataclass(frozen=True)
class _LoadedArtifact:
    path: Path
    payload: object
    encoded: bytes
    sha256: str
    invalid_code: str


def _validate_contract(name: str, payload: object, code: str) -> None:
    try:
        contracts.validate_contract(name, payload)
    except ValidationError as error:
        raise ValueError(code) from error


def _seconds_from_ms(value: int) -> Decimal:
    return Decimal(value) / Decimal(1000)


def _normalize_working_cut(payload: Mapping[str, object]) -> dict[str, object]:
    segments = payload["segments"]
    assert isinstance(segments, list)
    return {
        **payload,
        "segments": sorted(segments, key=lambda item: item["storyOrder"]),
    }


def _normalize_sources(
    sync_map: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    profile: Mapping[str, object],
) -> tuple[tuple[StorySource, ...], string_out.StringOut]:
    stripped: list[dict[str, object]] = []
    hashes: dict[tuple[str, str], str] = {}
    media_ids: set[str] = set()
    for source in sources:
        if not isinstance(source, Mapping) or set(source) != _SOURCE_FIELDS:
            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
        camera = source["camera"]
        media_id = source["media_id"]
        sha256 = source["sha256"]
        if (
            camera not in {"A", "B"}
            or not isinstance(media_id, str)
            or not media_id
            or media_id in media_ids
            or not isinstance(sha256, str)
            or len(sha256) != 64
            or any(character not in "0123456789abcdef" for character in sha256)
        ):
            raise ValueError("TRITRACK_STORY_SOURCE_INVALID")
        media_ids.add(media_id)
        hashes[(camera, media_id)] = sha256
        stripped.append(
            {
                "camera": camera,
                "media_id": media_id,
                "path": source["path"],
                "duration_seconds": source["duration_seconds"],
            }
        )

    try:
        base = string_out.build_string_out(sync_map, stripped, profile=profile)
    except (TypeError, ValueError, ValidationError) as error:
        raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID") from error
    normalized = tuple(
        StorySource(
            camera=source.camera,
            media_id=source.media_id,
            path=source.path,
            duration_frames=source.duration_frames,
            sha256=hashes[(source.camera, source.media_id)],
        )
        for source in base.sources
    )
    return normalized, base


def _build_relationships(
    sync_map: Mapping[str, object],
    source_by_media: Mapping[str, StorySource],
    *,
    frame_duration: Fraction,
) -> dict[str, _SourceRelationship]:
    relationships: dict[str, _SourceRelationship] = {}

    def register(media_id: str, relationship: _SourceRelationship) -> None:
        if media_id in relationships:
            raise ValueError("TRITRACK_STORY_SYNC_CONFLICT")
        relationships[media_id] = relationship

    pairs = sync_map["pairs"]
    assert isinstance(pairs, list)
    for pair in pairs:
        assert isinstance(pair, Mapping)
        media_a = str(pair["mediaA"])
        media_b = str(pair["mediaB"])
        source_a = source_by_media.get(media_a)
        source_b = source_by_media.get(media_b)
        if (
            source_a is None
            or source_b is None
            or source_a.camera != "A"
            or source_b.camera != "B"
        ):
            raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
        offset_frames = string_out.seconds_to_frames(
            pair["offsetBFromASeconds"], frame_duration
        )
        relationship = _SourceRelationship(
            kind="pair",
            source_a=source_a,
            source_b=source_b,
            offset_b_from_a_frames=offset_frames,
            audio_master=str(pair["audioMaster"]),
        )
        register(media_a, relationship)
        register(media_b, relationship)

    for camera, field in (("A", "singleA"), ("B", "singleB")):
        singles = sync_map[field]
        assert isinstance(singles, list)
        for value in singles:
            media_id = str(value)
            source = source_by_media.get(media_id)
            if source is None or source.camera != camera:
                raise ValueError("TRITRACK_STORY_SOURCE_SET_INVALID")
            register(
                media_id,
                _SourceRelationship(
                    kind="single",
                    source_a=source if camera == "A" else None,
                    source_b=source if camera == "B" else None,
                    offset_b_from_a_frames=0,
                    audio_master=camera,
                ),
            )
    return relationships


def _paired_clips(
    relationship: _SourceRelationship,
    selected: StorySource,
    *,
    selected_start: int,
    selected_end: int,
    story_offset: int,
) -> tuple[StoryClip, ...]:
    assert relationship.source_a is not None
    assert relationship.source_b is not None
    global_starts = {
        "A": 0,
        "B": relationship.offset_b_from_a_frames,
    }
    selected_global_start = selected_start + global_starts[selected.camera]
    selected_global_end = selected_end + global_starts[selected.camera]
    master = (
        relationship.source_a
        if relationship.audio_master == "A"
        else relationship.source_b
    )
    master_start = global_starts[master.camera]
    master_end = master_start + master.duration_frames
    if master_start > selected_global_start or master_end < selected_global_end:
        raise ValueError("TRITRACK_STORY_AUDIO_MASTER_COVERAGE")

    clips: list[StoryClip] = []
    for source in (relationship.source_a, relationship.source_b):
        source_global_start = global_starts[source.camera]
        source_global_end = source_global_start + source.duration_frames
        intersection_start = max(selected_global_start, source_global_start)
        intersection_end = min(selected_global_end, source_global_end)
        if intersection_end <= intersection_start:
            continue
        clips.append(
            StoryClip(
                camera=source.camera,
                media_id=source.media_id,
                path=source.path,
                offset_frames=story_offset
                + intersection_start
                - selected_global_start,
                start_frames=intersection_start - source_global_start,
                duration_frames=intersection_end - intersection_start,
                audio_enabled=source.camera == relationship.audio_master,
            )
        )
    return tuple(clips)


def build_story_timeline(
    sync_map: Mapping[str, object],
    aligned: Mapping[str, object],
    grouping: Mapping[str, object],
    working_cut: Mapping[str, object],
    sources: Sequence[Mapping[str, object]],
    *,
    aligned_sha256: str,
    grouping_sha256: str,
    profile: Mapping[str, object],
) -> StoryTimeline:
    """Re-derive and project selected cue spans into deterministic story time."""

    _validate_contract("sync-map-v1", sync_map, "TRITRACK_STORY_SYNC_INVALID")
    _validate_contract(
        "aligned-transcript-v1", aligned, "TRITRACK_STORY_ALIGNED_INVALID"
    )
    _validate_contract("grouping-v1", grouping, "TRITRACK_STORY_GROUPING_INVALID")
    _validate_contract(
        "working-cut-v1", working_cut, "TRITRACK_STORY_WORKING_CUT_INVALID"
    )
    _validate_contract(
        "compatibility-profile-v1", profile, "TRITRACK_STORY_PROFILE_INVALID"
    )
    profile_id = str(profile["profileId"])
    if (
        dict(profile) != doctor.load_profile(profile_id)
        or sync_map["profileId"] != profile_id
    ):
        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")

    try:
        expected_working_cut = organizer.build_working_cut(
            aligned,
            grouping,
            aligned_sha256=aligned_sha256,
            grouping_sha256=grouping_sha256,
        )
    except (TypeError, ValueError, ValidationError) as error:
        raise ValueError("TRITRACK_STORY_AUTHORITY_INVALID") from error
    if _normalize_working_cut(working_cut) != expected_working_cut:
        raise ValueError("TRITRACK_STORY_WORKING_CUT_DRIFT")

    normalized_sources, base_timeline = _normalize_sources(
        sync_map, sources, profile=profile
    )
    source_by_media = {source.media_id: source for source in normalized_sources}
    frame_duration = Fraction(
        base_timeline.frame_numerator, base_timeline.frame_denominator
    )
    relationships = _build_relationships(
        sync_map,
        source_by_media,
        frame_duration=frame_duration,
    )

    takes = aligned["takes"]
    assert isinstance(takes, list)
    take_by_id = {str(take["takeId"]): take for take in takes}
    segments = expected_working_cut["segments"]
    assert isinstance(segments, list)
    story_segments: list[StorySegment] = []
    cursor = 0
    for segment in segments:
        assert isinstance(segment, Mapping)
        take_id = str(segment["takeId"])
        take = take_by_id.get(take_id)
        source = source_by_media.get(take_id)
        relationship = relationships.get(take_id)
        if take is None or source is None or relationship is None:
            raise ValueError("TRITRACK_STORY_TAKE_UNKNOWN")
        if take["sourceSha256"] != source.sha256:
            raise ValueError("TRITRACK_STORY_SOURCE_HASH_MISMATCH")

        cues = take["cues"]
        assert isinstance(cues, list)
        positions = {str(cue["cueId"]): index for index, cue in enumerate(cues)}
        start_position = positions.get(str(segment["startCueId"]))
        end_position = positions.get(str(segment["endCueId"]))
        if (
            start_position is None
            or end_position is None
            or start_position > end_position
        ):
            raise ValueError("TRITRACK_STORY_CUE_UNKNOWN")
        selected_cues = cues[start_position : end_position + 1]
        start_ms = int(selected_cues[0]["startMs"])
        end_ms = int(selected_cues[-1]["endMs"])
        start_frames = string_out.seconds_to_frames(
            _seconds_from_ms(start_ms), frame_duration
        )
        end_frames = string_out.seconds_to_frames(
            _seconds_from_ms(end_ms), frame_duration
        )
        if end_frames <= start_frames or end_frames > source.duration_frames:
            raise ValueError("TRITRACK_STORY_SELECTION_INVALID")
        duration_frames = end_frames - start_frames
        title_text = " ".join(str(cue["text"]) for cue in selected_cues)

        if relationship.kind == "single":
            clips = (
                StoryClip(
                    camera=source.camera,
                    media_id=source.media_id,
                    path=source.path,
                    offset_frames=cursor,
                    start_frames=start_frames,
                    duration_frames=duration_frames,
                    audio_enabled=True,
                ),
            )
        else:
            clips = _paired_clips(
                relationship,
                source,
                selected_start=start_frames,
                selected_end=end_frames,
                story_offset=cursor,
            )
        story_segments.append(
            StorySegment(
                segment_id=str(segment["id"]),
                offset_frames=cursor,
                duration_frames=duration_frames,
                title_text=title_text,
                clips=clips,
            )
        )
        cursor += duration_frames

    return StoryTimeline(
        profile_id=profile_id,
        frame_numerator=base_timeline.frame_numerator,
        frame_denominator=base_timeline.frame_denominator,
        duration_frames=cursor,
        sources=normalized_sources,
        segments=tuple(story_segments),
    )


def _frame_time(timeline: StoryTimeline, frames: int) -> str:
    if frames == 0:
        return "0s"
    return f"{frames * timeline.frame_numerator}/{timeline.frame_denominator}s"


def _style_values(binding: Mapping[str, object]) -> dict[str, str]:
    parameters = binding["parameters"]
    if not isinstance(parameters, list):
        raise TypeError("TRITRACK_STORY_BINDING_INVALID")
    values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in parameters
        if isinstance(parameter, Mapping)
    }
    expected = {"alignment", "font", "fontColor", "fontFace", "fontSize"}
    if set(values) != expected:
        raise ValueError("TRITRACK_STORY_BINDING_INVALID")
    return values


def _validate_timeline(timeline: StoryTimeline) -> None:
    if not isinstance(timeline, StoryTimeline) or timeline.duration_frames <= 0:
        raise TypeError("TRITRACK_STORY_TIMELINE_INVALID")
    source_keys = [(source.camera, source.media_id) for source in timeline.sources]
    if source_keys != sorted(source_keys) or len(source_keys) != len(set(source_keys)):
        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
    source_by_key = {
        (source.camera, source.media_id): source for source in timeline.sources
    }
    cursor = 0
    for segment in timeline.segments:
        if (
            segment.offset_frames != cursor
            or segment.duration_frames <= 0
            or not segment.title_text
            or not segment.clips
            or sum(clip.audio_enabled for clip in segment.clips) != 1
        ):
            raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
        for clip in segment.clips:
            source = source_by_key.get((clip.camera, clip.media_id))
            if (
                source is None
                or clip.path != source.path
                or clip.offset_frames < segment.offset_frames
                or clip.start_frames < 0
                or clip.duration_frames <= 0
                or clip.start_frames + clip.duration_frames > source.duration_frames
                or clip.offset_frames + clip.duration_frames
                > segment.offset_frames + segment.duration_frames
            ):
                raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")
        cursor += segment.duration_frames
    if cursor != timeline.duration_frames:
        raise ValueError("TRITRACK_STORY_TIMELINE_INVALID")


def render_story_fcpxml(
    timeline: StoryTimeline,
    *,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
) -> str:
    """Render one deterministic Final Cut XML projection of a story timeline."""

    _validate_timeline(timeline)
    if not isinstance(metadata, emit_fcpxml.ProjectMetadata):
        raise TypeError("TRITRACK_EMIT_METADATA_INVALID")
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    if timeline.profile_id != profile_id:
        raise ValueError("TRITRACK_STORY_PROFILE_MISMATCH")
    styles = _style_values(binding)

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": emit_fcpxml.FORMAT_NAME,
            "frameDuration": str(profile["frameDuration"]),
            "width": str(profile["width"]),
            "height": str(profile["height"]),
            "colorSpace": str(profile["colorSpace"]),
        },
    )
    ET.SubElement(
        resources_element,
        "effect",
        {
            "id": "r2",
            "name": str(binding["effectName"]),
            "uid": str(binding["effectUid"]),
        },
    )
    source_ids: dict[tuple[str, str], str] = {}
    for index, source in enumerate(timeline.sources, start=3):
        resource_id = f"r{index}"
        source_ids[(source.camera, source.media_id)] = resource_id
        asset = ET.SubElement(
            resources_element,
            "asset",
            {
                "id": resource_id,
                "name": source.media_id,
                "start": "0s",
                "duration": _frame_time(timeline, source.duration_frames),
                "hasVideo": "1",
                "hasAudio": "1",
                "format": "r1",
                "audioSources": "1",
                "audioChannels": "2",
                "audioRate": f"{int(profile['audioRate']) // 1000}k",
            },
        )
        ET.SubElement(
            asset,
            "media-rep",
            {"kind": "original-media", "src": source.path.absolute().as_uri()},
        )

    library = ET.SubElement(root, "library")
    event = ET.SubElement(library, "event", {"name": metadata.event_name})
    project = ET.SubElement(event, "project", {"name": metadata.project_name})
    sequence = ET.SubElement(
        project,
        "sequence",
        {
            "format": "r1",
            "duration": _frame_time(timeline, timeline.duration_frames),
            "tcStart": "0s",
            "tcFormat": str(profile["timecodeFormat"]),
            "audioLayout": "stereo",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        },
    )
    spine = ET.SubElement(sequence, "spine")
    for index, segment in enumerate(timeline.segments, start=1):
        gap = ET.SubElement(
            spine,
            "gap",
            {
                "name": segment.segment_id,
                "offset": _frame_time(timeline, segment.offset_frames),
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        for lane, clip in enumerate(segment.clips, start=1):
            attributes = {
                "ref": source_ids[(clip.camera, clip.media_id)],
                "lane": str(lane),
                "offset": _frame_time(timeline, clip.offset_frames),
                "name": clip.media_id,
                "start": _frame_time(timeline, clip.start_frames),
                "duration": _frame_time(timeline, clip.duration_frames),
                "srcEnable": "all" if clip.audio_enabled else "video",
            }
            if clip.audio_enabled:
                attributes["audioRole"] = "dialogue"
            ET.SubElement(gap, "asset-clip", attributes)
        title = ET.SubElement(
            gap,
            "title",
            {
                "ref": "r2",
                "lane": str(len(segment.clips) + 1),
                "offset": _frame_time(timeline, segment.offset_frames),
                "name": f"{segment.segment_id} - Basic Title",
                "start": "0s",
                "duration": _frame_time(timeline, segment.duration_frames),
            },
        )
        text_element = ET.SubElement(title, "text")
        style_id = f"ts{index:03d}"
        text_style = ET.SubElement(text_element, "text-style", {"ref": style_id})
        text_style.text = segment.title_text
        definition = ET.SubElement(title, "text-style-def", {"id": style_id})
        ET.SubElement(
            definition,
            "text-style",
            {
                name: styles[name]
                for name in (
                    "alignment",
                    "font",
                    "fontColor",
                    "fontFace",
                    "fontSize",
                )
            },
        )

    ET.indent(root, space="    ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    rendered = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f"{emit_fcpxml.ALLOWED_DOCTYPE}\n{body}\n"
    )
    emit_fcpxml.validate_fcpxml(rendered, profile=profile, binding=binding)
    return rendered


def _read_regular_bytes(path: Path, invalid_code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(invalid_code) from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or not 0 < metadata.st_size <= _JSON_LIMIT_BYTES
        ):
            raise ValueError(invalid_code)
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(_JSON_LIMIT_BYTES + 1)
        if len(encoded) > _JSON_LIMIT_BYTES:
            raise ValueError(invalid_code)
        return encoded
    except OSError as error:
        raise ValueError(invalid_code) from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_artifact(path: Path, *, contract: str, code: str) -> _LoadedArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected, code)
    try:
        payload = json.loads(
            encoded.decode("utf-8", errors="strict"), parse_float=Decimal
        )
        contracts.validate_contract(contract, payload)
    except (UnicodeError, json.JSONDecodeError, ValidationError) as error:
        raise ValueError(code) from error
    return _LoadedArtifact(
        path=selected,
        payload=payload,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
        invalid_code=code,
    )


def _verify_artifact(artifact: _LoadedArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path, artifact.invalid_code)
    except ValueError as error:
        raise ValueError("TRITRACK_STORY_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_STORY_INPUT_CHANGED")


def _hash_regular_media(path: Path) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
    digest = hashlib.sha256()
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size <= 0:
            raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            while chunk := stream.read(_HASH_CHUNK_BYTES):
                digest.update(chunk)
    except OSError as error:
        raise ValueError("TRITRACK_STORY_SOURCE_UNREADABLE") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return digest.hexdigest()


def emit_story_and_publish(
    camera_a_sources: Sequence[sync_scan.MediaSource],
    camera_b_sources: Sequence[sync_scan.MediaSource],
    *,
    sync_map_path: Path,
    aligned_path: Path,
    grouping_path: Path,
    working_cut_path: Path,
    profile_id: str,
    binding_id: str,
    metadata: emit_fcpxml.ProjectMetadata,
    output_path: Path,
) -> str:
    """Load exact authorities, render a story cut, and publish without overwrite."""

    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    sync_map = _load_artifact(
        sync_map_path, contract="sync-map-v1", code="TRITRACK_STORY_SYNC_INVALID"
    )
    aligned = _load_artifact(
        aligned_path,
        contract="aligned-transcript-v1",
        code="TRITRACK_STORY_ALIGNED_INVALID",
    )
    grouping = _load_artifact(
        grouping_path,
        contract="grouping-v1",
        code="TRITRACK_STORY_GROUPING_INVALID",
    )
    working_cut = _load_artifact(
        working_cut_path,
        contract="working-cut-v1",
        code="TRITRACK_STORY_WORKING_CUT_INVALID",
    )
    if grouping.encoded != organizer.encode_grouping(grouping.payload):
        raise ValueError("TRITRACK_STORY_GROUPING_NONCANONICAL")
    if working_cut.encoded != organizer.encode_working_cut(working_cut.payload):
        raise ValueError("TRITRACK_STORY_WORKING_CUT_NONCANONICAL")

    profile = doctor.load_profile(profile_id)
    doctor.load_title_binding(binding_id)
    source_hashes = {
        (camera, source.media_id): _hash_regular_media(source.path)
        for camera, camera_sources in (
            ("A", camera_a_sources),
            ("B", camera_b_sources),
        )
        for source in camera_sources
    }
    probed = emit_fcpxml.probe_sources(
        camera_a_sources, camera_b_sources, profile=profile
    )
    sources = [
        {**source, "sha256": source_hashes[(source["camera"], source["media_id"])]}
        for source in probed
    ]
    assert isinstance(sync_map.payload, Mapping)
    assert isinstance(aligned.payload, Mapping)
    assert isinstance(grouping.payload, Mapping)
    assert isinstance(working_cut.payload, Mapping)
    timeline = build_story_timeline(
        sync_map.payload,
        aligned.payload,
        grouping.payload,
        working_cut.payload,
        sources,
        aligned_sha256=aligned.sha256,
        grouping_sha256=grouping.sha256,
        profile=profile,
    )
    rendered = render_story_fcpxml(
        timeline,
        profile_id=profile_id,
        binding_id=binding_id,
        metadata=metadata,
    )
    for artifact in (sync_map, aligned, grouping, working_cut):
        _verify_artifact(artifact)
    for camera, camera_sources in (
        ("A", camera_a_sources),
        ("B", camera_b_sources),
    ):
        for source in camera_sources:
            if _hash_regular_media(source.path) != source_hashes[(camera, source.media_id)]:
                raise ValueError("TRITRACK_STORY_INPUT_CHANGED")
    emit_fcpxml.publish_fcpxml(
        destination,
        rendered,
        profile=profile,
        binding=doctor.load_title_binding(binding_id),
    )
    return rendered
--- END FILE src/tritrack_editing_assistant/story_fcpxml.py ---

--- BEGIN FILE src/tritrack_editing_assistant/string_out.py ---
"""Deterministic, frame-exact string-out construction."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from . import contracts, doctor

SOURCE_FIELDS = frozenset({"camera", "media_id", "path", "duration_seconds"})


@dataclass(frozen=True)
class SourceMedia:
    """One caller-owned media source normalized without changing the input."""

    camera: str
    media_id: str
    path: Path
    duration_frames: int


@dataclass(frozen=True)
class TimelineClip:
    """One source clip at an absolute, integer-frame timeline position."""

    camera: str
    media_id: str
    path: Path
    offset_frames: int
    duration_frames: int
    audio_enabled: bool


@dataclass(frozen=True)
class StringOutSegment:
    """One deterministic pair or single-source region."""

    label: str
    offset_frames: int
    duration_frames: int
    clips: tuple[TimelineClip, ...]


@dataclass(frozen=True)
class StringOut:
    """A complete string-out expressed only in integer frames."""

    profile_id: str
    frame_numerator: int
    frame_denominator: int
    duration_frames: int
    sources: tuple[SourceMedia, ...]
    segments: tuple[StringOutSegment, ...]


def _number_fraction(value: object) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("TRITRACK_EMIT_TIME_INVALID")
    if isinstance(value, Decimal):
        return Fraction(value)
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(Decimal(str(value)))
    raise ValueError("TRITRACK_EMIT_TIME_INVALID")


def _frame_duration(profile: Mapping[str, object]) -> Fraction:
    value = profile.get("frameDuration")
    if not isinstance(value, str) or not value.endswith("s"):
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    numerator, separator, denominator = value[:-1].partition("/")
    if not separator:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    try:
        result = Fraction(int(numerator), int(denominator))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID") from error
    if result <= 0:
        raise ValueError("TRITRACK_EMIT_FRAME_DURATION_INVALID")
    return result


def _round_fraction(value: Fraction) -> int:
    if value < 0:
        return -_round_fraction(-value)
    quotient, remainder = divmod(value.numerator, value.denominator)
    return quotient + (1 if remainder * 2 >= value.denominator else 0)


def seconds_to_frames(value: object, frame_duration: Fraction) -> int:
    """Quantize seconds once using deterministic half-away-from-zero rounding."""

    return _round_fraction(_number_fraction(value) / frame_duration)


def _normalize_sources(
    sources: Sequence[Mapping[str, object]],
    *,
    frame_duration: Fraction,
) -> tuple[SourceMedia, ...]:
    normalized: list[SourceMedia] = []
    seen: set[tuple[str, str]] = set()
    for source in sources:
        if not isinstance(source, Mapping) or set(source) != SOURCE_FIELDS:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        camera = source["camera"]
        media_id = source["media_id"]
        path = source["path"]
        if camera not in {"A", "B"}:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        if not isinstance(media_id, str) or not media_id:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        try:
            normalized_path = Path(path)  # type: ignore[arg-type]
        except TypeError as error:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID") from error
        duration_frames = seconds_to_frames(
            source["duration_seconds"],
            frame_duration,
        )
        if duration_frames <= 0:
            raise ValueError("TRITRACK_EMIT_SOURCE_INVALID")
        key = (camera, media_id)
        if key in seen:
            raise ValueError("TRITRACK_EMIT_SOURCE_DUPLICATE")
        seen.add(key)
        normalized.append(
            SourceMedia(camera, media_id, normalized_path, duration_frames)
        )
    return tuple(sorted(normalized, key=lambda item: (item.camera, item.media_id)))


def _expected_source_keys(sync_map: Mapping[str, Any]) -> set[tuple[str, str]]:
    expected: set[tuple[str, str]] = set()
    for pair in sync_map["pairs"]:
        expected.add(("A", str(pair["mediaA"])))
        expected.add(("B", str(pair["mediaB"])))
    expected.update(("A", str(media_id)) for media_id in sync_map["singleA"])
    expected.update(("B", str(media_id)) for media_id in sync_map["singleB"])
    return expected


def _validate_sync_relationships(sync_map: Mapping[str, Any]) -> None:
    pair_ids = [str(pair["pairId"]) for pair in sync_map["pairs"]]
    if len(pair_ids) != len(set(pair_ids)):
        raise ValueError("TRITRACK_EMIT_PAIR_ID_DUPLICATE")

    paired_a = [str(pair["mediaA"]) for pair in sync_map["pairs"]]
    if len(paired_a) != len(set(paired_a)):
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_CONFLICT")
    paired_keys = {
        *(("A", value) for value in paired_a),
        *(("B", str(pair["mediaB"])) for pair in sync_map["pairs"]),
    }
    single_keys = {
        *(("A", str(value)) for value in sync_map["singleA"]),
        *(("B", str(value)) for value in sync_map["singleB"]),
    }
    if paired_keys & single_keys:
        raise ValueError("TRITRACK_EMIT_SYNC_MAP_CONFLICT")


def build_string_out(
    sync_map: Mapping[str, Any],
    sources: Sequence[Mapping[str, object]],
    *,
    profile: Mapping[str, object],
) -> StringOut:
    """Validate inputs and build a stable pair-first string-out."""

    contracts.validate_contract("sync-map-v1", sync_map)
    sync_profile_id = str(sync_map["profileId"])
    packaged_profile = doctor.load_profile(sync_profile_id)
    contracts.validate_contract("compatibility-profile-v1", profile)
    if dict(profile) != packaged_profile:
        raise ValueError("TRITRACK_PROFILE_MISMATCH")

    frame_duration = _frame_duration(profile)
    normalized_sources = _normalize_sources(
        sources,
        frame_duration=frame_duration,
    )
    source_by_key = {
        (source.camera, source.media_id): source for source in normalized_sources
    }
    _validate_sync_relationships(sync_map)
    if set(source_by_key) != _expected_source_keys(sync_map):
        raise ValueError("TRITRACK_EMIT_SOURCE_SET_MISMATCH")

    segments: list[StringOutSegment] = []
    cursor = 0
    sorted_pairs = sorted(
        sync_map["pairs"],
        key=lambda pair: (
            str(pair["pairId"]),
            str(pair["mediaA"]),
            str(pair["mediaB"]),
        ),
    )
    for pair in sorted_pairs:
        source_a = source_by_key[("A", str(pair["mediaA"]))]
        source_b = source_by_key[("B", str(pair["mediaB"]))]
        declared_a = seconds_to_frames(
            pair["durationASeconds"],
            frame_duration,
        )
        declared_b = seconds_to_frames(
            pair["durationBSeconds"],
            frame_duration,
        )
        if (
            declared_a != source_a.duration_frames
            or declared_b != source_b.duration_frames
        ):
            raise ValueError("TRITRACK_EMIT_DURATION_MISMATCH")

        b_from_a = seconds_to_frames(
            pair["offsetBFromASeconds"],
            frame_duration,
        )
        local_start = min(0, b_from_a)
        a_offset = cursor - local_start
        b_offset = cursor + b_from_a - local_start
        segment_duration = max(
            a_offset + source_a.duration_frames,
            b_offset + source_b.duration_frames,
        ) - cursor
        clips = (
            TimelineClip(
                "A",
                source_a.media_id,
                source_a.path,
                a_offset,
                source_a.duration_frames,
                pair["audioMaster"] == "A",
            ),
            TimelineClip(
                "B",
                source_b.media_id,
                source_b.path,
                b_offset,
                source_b.duration_frames,
                pair["audioMaster"] == "B",
            ),
        )
        segments.append(
            StringOutSegment(
                str(pair["pairId"]),
                cursor,
                segment_duration,
                clips,
            )
        )
        cursor += segment_duration

    for camera, field in (("A", "singleA"), ("B", "singleB")):
        for media_id in sorted(str(value) for value in sync_map[field]):
            source = source_by_key[(camera, media_id)]
            segments.append(
                StringOutSegment(
                    f"single-{camera}-{media_id}",
                    cursor,
                    source.duration_frames,
                    (
                        TimelineClip(
                            camera,
                            media_id,
                            source.path,
                            cursor,
                            source.duration_frames,
                            True,
                        ),
                    ),
                )
            )
            cursor += source.duration_frames

    return StringOut(
        sync_profile_id,
        frame_duration.numerator,
        frame_duration.denominator,
        cursor,
        normalized_sources,
        tuple(segments),
    )
--- END FILE src/tritrack_editing_assistant/string_out.py ---

--- BEGIN FILE src/tritrack_editing_assistant/sync_scan.py ---
"""Audio-verified A/B synchronization with no-overwrite publication."""

from __future__ import annotations

import datetime as dt
import json
import math
import os
import struct
import tempfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from . import contracts, doctor, process

MIN_OVERLAP_SECONDS = 3.0
MIN_PEAK_RATIO = 6.0
CLOCK_SANITY_DAYS = 30
PAIR_TOLERANCE_SECONDS = 180.0
DEFAULT_SAMPLE_RATE = 1_000
PROBE_TIMEOUT_SECONDS = 30.0
AUDIO_TIMEOUT_SECONDS = 300.0
MAX_PROBE_BYTES = 1024 * 1024
MAX_AUDIO_BYTES = 512 * 1024 * 1024

Clip = Mapping[str, Any]
Evidence = Mapping[str, float]


@dataclass(frozen=True)
class MediaSource:
    """An opaque public media id and a local source path."""

    media_id: str
    path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.media_id, str) or not self.media_id:
            raise ValueError("TRITRACK_SYNC_MEDIA_ID_INVALID")
        object.__setattr__(self, "path", Path(self.path))


def parse_media_time(value: str) -> dt.datetime:
    """Return a timezone-aware timestamp from ISO-8601 metadata."""

    try:
        parsed = dt.datetime.fromisoformat(value)
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("TRITRACK_SYNC_TIME_INVALID") from error
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    return parsed


def _one_camera_hints_are_sane(
    clips: Iterable[Clip], *, today: dt.date, max_days: int
) -> bool:
    stamped = [clip["start"] for clip in clips if clip.get("start") is not None]
    if not stamped:
        return False
    nearest_days = min(abs((stamp.date() - today).days) for stamp in stamped)
    return nearest_days <= max_days


def time_hints_are_sane(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    today: dt.date | None = None,
    max_days: int = CLOCK_SANITY_DAYS,
) -> bool:
    """Accept time hints only when both camera sets have a plausible stamp."""

    observed_today = today or dt.datetime.now(dt.UTC).astimezone().date()
    return _one_camera_hints_are_sane(
        camera_a, today=observed_today, max_days=max_days
    ) and _one_camera_hints_are_sane(
        camera_b, today=observed_today, max_days=max_days
    )


def candidate_pairs(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    hints_ok: bool,
    tolerance_seconds: float = PAIR_TOLERANCE_SECONDS,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
):
    """Yield time-near candidates, or all candidates when hints are stale."""

    camera_b_items = tuple(camera_b)
    if not hints_ok:
        for a_clip in camera_a:
            for b_clip in camera_b_items:
                yield a_clip, b_clip
        return

    pad = dt.timedelta(seconds=tolerance_seconds)
    for a_clip in camera_a:
        a_start = a_clip.get("start")
        if a_start is None:
            continue
        a_end = a_start + dt.timedelta(seconds=a_clip["duration_seconds"])
        for b_clip in camera_b_items:
            b_start = b_clip.get("start")
            if b_start is None:
                continue
            b_end = b_start + dt.timedelta(seconds=b_clip["duration_seconds"])
            overlap = (min(a_end, b_end) + pad - max(a_start, b_start)).total_seconds()
            if overlap > min_overlap_seconds:
                yield a_clip, b_clip


def normalized_audio_correlation(
    a_samples: Sequence[float],
    b_samples: Sequence[float],
    *,
    sample_rate: int,
) -> tuple[float, float]:
    """Return the strongest normalized lag and separated-peak ratio."""

    if sample_rate <= 0 or len(a_samples) == 0 or len(b_samples) == 0:
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")

    def normalize(samples: Sequence[float]) -> np.ndarray:
        values = np.asarray(samples, dtype=np.float64)
        if values.ndim != 1 or not np.all(np.isfinite(values)):
            raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
        centered = values - values.mean()
        deviation = math.sqrt(float(np.mean(centered**2)))
        if deviation == 0:
            raise ValueError("TRITRACK_SYNC_AUDIO_FLAT")
        return centered / deviation

    normalized_a = normalize(a_samples)
    normalized_b = normalize(b_samples)
    score_count = len(normalized_a) + len(normalized_b) - 1
    fft_length = 1 << (score_count - 1).bit_length()
    scores = np.fft.irfft(
        np.fft.rfft(normalized_a, fft_length)
        * np.fft.rfft(normalized_b[::-1], fft_length),
        fft_length,
    )[:score_count]
    scores = np.abs(scores)
    strongest_index = int(np.argmax(scores))
    strongest_lag = strongest_index - (len(normalized_b) - 1)
    strongest_score = float(scores[strongest_index])
    lags = np.arange(-(len(normalized_b) - 1), len(normalized_a))
    separated_scores = scores[np.abs(lags - strongest_lag) > sample_rate]
    second_score = float(separated_scores.max()) if separated_scores.size else 0.0
    return strongest_lag / sample_rate, strongest_score / (second_score + 1e-9)


def select_strongest_pairs(
    camera_a: Iterable[Clip],
    camera_b: Iterable[Clip],
    *,
    evidence_for: Callable[[Clip, Clip], Evidence | None],
    hints_ok: bool,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> list[dict[str, float | str]]:
    """Select one strongest B per A without consuming a reusable B clip."""

    camera_a_items = tuple(camera_a)
    camera_b_items = tuple(camera_b)
    strongest_by_a: dict[str, dict[str, float | str]] = {}

    for a_clip, b_clip in candidate_pairs(
        camera_a_items,
        camera_b_items,
        hints_ok=hints_ok,
        min_overlap_seconds=min_overlap_seconds,
    ):
        if not (a_clip.get("has_audio") and b_clip.get("has_audio")):
            continue
        evidence = evidence_for(a_clip, b_clip)
        if evidence is None:
            continue
        peak_ratio = float(evidence["peak_ratio"])
        overlap_seconds = float(evidence["overlap_seconds"])
        if peak_ratio < min_peak_ratio or overlap_seconds < min_overlap_seconds:
            continue

        a_id = str(a_clip["id"])
        candidate: dict[str, float | str] = {
            "a": a_id,
            "b": str(b_clip["id"]),
            "offset_seconds": float(evidence["offset_seconds"]),
            "peak_ratio": peak_ratio,
            "overlap_seconds": overlap_seconds,
        }
        current = strongest_by_a.get(a_id)
        if current is None or float(current["peak_ratio"]) < peak_ratio:
            strongest_by_a[a_id] = candidate

    return [
        strongest_by_a[str(a_clip["id"])]
        for a_clip in camera_a_items
        if str(a_clip["id"]) in strongest_by_a
    ]


def _process_stdout(result: process.ProcessResult, error_code: str) -> bytes:
    if not result.ok:
        raise ValueError(error_code)
    return result.stdout


def probe_media(
    source: MediaSource,
    *,
    executable: str = "ffprobe",
    timeout_seconds: float = PROBE_TIMEOUT_SECONDS,
    max_captured_bytes: int = MAX_PROBE_BYTES,
) -> dict[str, object]:
    """Read one source's public probe fields through the bounded process API."""

    if not source.path.is_file():
        raise ValueError("TRITRACK_SYNC_SOURCE_MISSING")
    command = [
        executable,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_entries",
        (
            "format=duration:format_tags=creation_time:"
            "stream=codec_type,width,height,r_frame_rate,color_space,"
            "color_transfer,color_primaries,sample_rate,channels"
        ),
        str(source.path),
    ]
    result = process.run_bounded(
        command,
        timeout_seconds=timeout_seconds,
        max_captured_bytes=max_captured_bytes,
    )
    raw = _process_stdout(result, "TRITRACK_SYNC_PROBE_FAILED")
    try:
        payload = json.loads(raw)
        format_data = payload["format"]
        streams = payload["streams"]
        duration = float(format_data["duration"])
        tags = format_data.get("tags", {})
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID") from error
    if (
        not isinstance(payload, Mapping)
        or not isinstance(format_data, Mapping)
        or not isinstance(streams, list)
        or not isinstance(tags, Mapping)
        or not math.isfinite(duration)
        or duration <= 0
    ):
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID")
    creation_time = tags.get("creation_time")
    if creation_time is not None and not isinstance(creation_time, str):
        raise ValueError("TRITRACK_SYNC_PROBE_INVALID")
    start = parse_media_time(creation_time) if creation_time else None
    video_streams = [
        stream
        for stream in streams
        if isinstance(stream, Mapping) and stream.get("codec_type") == "video"
    ]
    audio_streams = [
        stream
        for stream in streams
        if isinstance(stream, Mapping) and stream.get("codec_type") == "audio"
    ]
    video_stream = video_streams[0] if video_streams else {}
    audio_stream = audio_streams[0] if audio_streams else {}
    return {
        "id": source.media_id,
        "duration_seconds": duration,
        "start": start,
        "has_audio": bool(audio_streams),
        "compatibility": {
            "videoStreamCount": len(video_streams),
            "audioStreamCount": len(audio_streams),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "frameRate": video_stream.get("r_frame_rate"),
            "colorSpace": video_stream.get("color_space"),
            "colorTransfer": video_stream.get("color_transfer"),
            "colorPrimaries": video_stream.get("color_primaries"),
            "sampleRate": audio_stream.get("sample_rate"),
            "channels": audio_stream.get("channels"),
        },
        "source": source,
    }


def extract_audio_samples(
    source: MediaSource,
    *,
    executable: str = "ffmpeg",
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    timeout_seconds: float = AUDIO_TIMEOUT_SECONDS,
    max_captured_bytes: int = MAX_AUDIO_BYTES,
) -> tuple[float, ...]:
    """Decode mono float samples through the bounded process API."""

    if sample_rate <= 0:
        raise ValueError("TRITRACK_SYNC_SAMPLE_RATE_INVALID")
    result = process.run_bounded(
        [
            executable,
            "-nostdin",
            "-v",
            "error",
            "-i",
            str(source.path),
            "-map",
            "0:a:0",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "f32le",
            "pipe:1",
        ],
        timeout_seconds=timeout_seconds,
        max_captured_bytes=max_captured_bytes,
    )
    raw = _process_stdout(result, "TRITRACK_SYNC_AUDIO_DECODE_FAILED")
    if not raw or len(raw) % 4:
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
    samples = tuple(value[0] for value in struct.iter_unpack("<f", raw))
    if any(not math.isfinite(value) for value in samples):
        raise ValueError("TRITRACK_SYNC_AUDIO_INVALID")
    return samples


def _audio_evidence(
    a_clip: Clip,
    b_clip: Clip,
    *,
    samples_for: Callable[[Clip], Sequence[float]],
    sample_rate: int,
) -> dict[str, float]:
    a_samples = samples_for(a_clip)
    b_samples = samples_for(b_clip)
    offset_seconds, peak_ratio = normalized_audio_correlation(
        a_samples,
        b_samples,
        sample_rate=sample_rate,
    )
    lag_samples = round(offset_seconds * sample_rate)
    first_b_index = max(0, -lag_samples)
    last_b_index = min(len(b_samples), len(a_samples) - lag_samples)
    overlap_samples = max(0, last_b_index - first_b_index)
    return {
        "offset_seconds": offset_seconds,
        "peak_ratio": peak_ratio,
        "overlap_seconds": overlap_samples / sample_rate,
    }


def _validate_unique_media(clips: Sequence[Clip]) -> None:
    identifiers = [str(clip["id"]) for clip in clips]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("TRITRACK_SYNC_MEDIA_ID_DUPLICATE")


def _started_at_text(value: object) -> str | None:
    if not isinstance(value, dt.datetime):
        return None
    return value.isoformat().replace("+00:00", "Z")


def build_sync_map(
    camera_a: Sequence[Clip],
    camera_b: Sequence[Clip],
    *,
    profile_id: str,
    evidence_for: Callable[[Clip, Clip], Evidence | None],
    today: dt.date | None = None,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> dict[str, object]:
    """Build and validate the public sync-map-v1 payload."""

    doctor.load_profile(profile_id)
    _validate_unique_media(camera_a)
    _validate_unique_media(camera_b)
    hints_ok = time_hints_are_sane(camera_a, camera_b, today=today)
    selected = select_strongest_pairs(
        camera_a,
        camera_b,
        evidence_for=evidence_for,
        hints_ok=hints_ok,
        min_peak_ratio=min_peak_ratio,
        min_overlap_seconds=min_overlap_seconds,
    )
    a_by_id = {str(clip["id"]): clip for clip in camera_a}
    selected_a = {str(pair["a"]) for pair in selected}
    selected_b = {str(pair["b"]) for pair in selected}

    pairs: list[dict[str, object]] = []
    for index, pair in enumerate(selected, start=1):
        a_clip = a_by_id[str(pair["a"])]
        b_clip = next(
            clip for clip in camera_b if str(clip["id"]) == str(pair["b"])
        )
        pairs.append(
            {
                "pairId": f"pair-{index:03d}",
                "mediaA": pair["a"],
                "mediaB": pair["b"],
                "offsetBFromASeconds": pair["offset_seconds"],
                "confidence": pair["peak_ratio"],
                "overlapSeconds": pair["overlap_seconds"],
                "audioMaster": "A",
                "durationASeconds": float(a_clip["duration_seconds"]),
                "durationBSeconds": float(b_clip["duration_seconds"]),
                "startedAt": _started_at_text(a_clip.get("start"))
                if hints_ok
                else None,
            }
        )

    warnings: list[dict[str, str]] = []
    if not hints_ok:
        warnings.append({"code": "SYNC_TIME_HINTS_STALE"})
    for clip in (*camera_a, *camera_b):
        if not clip.get("has_audio"):
            warnings.append(
                {"code": "SYNC_AUDIO_MISSING", "mediaId": str(clip["id"])}
            )

    payload: dict[str, object] = {
        "schemaVersion": "tritrack.sync-map/v1",
        "profileId": profile_id,
        "pairs": pairs,
        "singleA": [
            str(clip["id"]) for clip in camera_a if str(clip["id"]) not in selected_a
        ],
        "singleB": [
            str(clip["id"]) for clip in camera_b if str(clip["id"]) not in selected_b
        ],
        "warnings": warnings,
    }
    contracts.validate_contract("sync-map-v1", payload)
    return payload


def publish_sync_map(
    output_path: str | os.PathLike[str], payload: object
) -> Path:
    """Atomically create one validated map without overwriting any path."""

    contracts.validate_contract("sync-map-v1", payload)
    destination = process.require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def synchronize_and_publish(
    camera_a_sources: Sequence[MediaSource],
    camera_b_sources: Sequence[MediaSource],
    *,
    profile_id: str,
    output_path: str | os.PathLike[str],
    today: dt.date | None = None,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    min_peak_ratio: float = MIN_PEAK_RATIO,
    min_overlap_seconds: float = MIN_OVERLAP_SECONDS,
) -> dict[str, object]:
    """Probe, correlate, validate, and publish one local synchronization map."""

    process.require_absent_output(output_path)
    camera_a = tuple(probe_media(source) for source in camera_a_sources)
    camera_b = tuple(probe_media(source) for source in camera_b_sources)
    sample_cache: dict[MediaSource, tuple[float, ...]] = {}

    def samples_for(clip: Clip) -> Sequence[float]:
        source = clip["source"]
        if not isinstance(source, MediaSource):
            raise TypeError("TRITRACK_SYNC_SOURCE_INVALID")
        if source not in sample_cache:
            sample_cache[source] = extract_audio_samples(
                source,
                sample_rate=sample_rate,
            )
        return sample_cache[source]

    def evidence_for(a_clip: Clip, b_clip: Clip) -> Evidence:
        return _audio_evidence(
            a_clip,
            b_clip,
            samples_for=samples_for,
            sample_rate=sample_rate,
        )

    payload = build_sync_map(
        camera_a,
        camera_b,
        profile_id=profile_id,
        evidence_for=evidence_for,
        today=today,
        min_peak_ratio=min_peak_ratio,
        min_overlap_seconds=min_overlap_seconds,
    )
    publish_sync_map(output_path, payload)
    return payload
--- END FILE src/tritrack_editing_assistant/sync_scan.py ---

--- BEGIN FILE src/tritrack_editing_assistant/transcribe_takes.py ---
"""Local whisper.cpp evidence canonicalization and transcription workflow."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
import wave
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from . import hallucination
from .contracts import validate_contract
from .process import ProcessResult, require_absent_output, run_bounded

_LANGUAGE = re.compile(r"^[a-z]{2,3}$")
_HASH_CHUNK_BYTES = 1024 * 1024
_PROCESS_CAPTURE_BYTES = 512 * 1024
_ENGINE_JSON_LIMIT_BYTES = 16 * 1024 * 1024
_MAX_FINAL_CUE_PADDING_MS = 5000
_AUDIO_TIMEOUT_SECONDS = 900
_ENGINE_TIMEOUT_SECONDS = 3600
TRANSCRIPTION_PROFILE_ID = "whisper-cpp-cpu-no-fallback-v1"


@dataclass(frozen=True)
class TranscribedTake:
    """One source-bound local transcription result."""

    take_id: str
    source_sha256: str
    status: str
    cues: tuple[dict[str, object], ...]


def _object(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    return value


def _millisecond(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    return value


def canonicalize_whisper_evidence(
    payload: object,
    *,
    requested_language: str,
    audio_duration_ms: int,
    proven_silence: bool = False,
) -> list[dict[str, object]]:
    """Extract strict canonical cues from one supported whisper JSON result."""

    if (
        isinstance(audio_duration_ms, bool)
        or not isinstance(audio_duration_ms, int)
        or audio_duration_ms < 1
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")

    evidence = _object(payload)
    result = _object(evidence.get("result"))
    if result.get("language") != requested_language:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    transcription = evidence.get("transcription")
    if not isinstance(transcription, list):
        raise TypeError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")

    cues: list[dict[str, object]] = []
    previous_end = 0
    for index, value in enumerate(transcription, start=1):
        segment = _object(value)
        text = hallucination.normalize_cue_text(segment.get("text"))
        if hallucination.is_blank_audio_sentinel(text):
            if proven_silence:
                continue
            raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID")
        offsets = _object(segment.get("offsets"))
        start_ms = _millisecond(offsets.get("from"))
        end_ms = _millisecond(offsets.get("to"))
        if end_ms > audio_duration_ms:
            if (
                index != len(transcription)
                or start_ms >= audio_duration_ms
                or end_ms - audio_duration_ms > _MAX_FINAL_CUE_PADDING_MS
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
            end_ms = audio_duration_ms
        if not (previous_end <= start_ms < end_ms <= audio_duration_ms):
            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
        cues.append(
            {
                "cueId": f"cue-{len(cues) + 1:06d}",
                "startMs": start_ms,
                "endMs": end_ms,
                "text": text,
            }
        )
        previous_end = end_ms

    hallucination.reject_repeated_cues([str(cue["text"]) for cue in cues])
    return cues


def build_transcript_bundle(
    takes: Sequence[TranscribedTake],
    *,
    language: str,
    model_sha256: str,
    engine_version: str,
) -> dict[str, object]:
    """Build and validate one stable, path-free local transcript bundle."""

    ordered = sorted(takes, key=lambda take: take.take_id)
    take_ids = [take.take_id for take in ordered]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")

    bundle: dict[str, object] = {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": TRANSCRIPTION_PROFILE_ID,
        "language": language,
        "modelSha256": model_sha256,
        "engine": {"name": "whisper-cli", "version": engine_version},
        "takes": [
            {
                "takeId": take.take_id,
                "sourceSha256": take.source_sha256,
                "status": take.status,
                "cues": [dict(cue) for cue in take.cues],
            }
            for take in ordered
        ],
    }
    validate_contract("transcript-bundle-v1", bundle)
    return bundle


def encode_transcript_bundle(bundle: object) -> str:
    """Encode a validated bundle with stable key ordering and final newline."""

    validate_contract("transcript-bundle-v1", bundle)
    return json.dumps(
        bundle,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def _require_readable_file(path: Path, code: str) -> Path:
    if not path.is_file() or not os.access(path, os.R_OK):
        raise ValueError(code)
    return path


def _sha256_file(
    path: Path, code: str = "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(code)
        digest = hashlib.sha256()
        total = 0
        remaining = before.st_size + 1
        while remaining:
            chunk = os.read(descriptor, min(_HASH_CHUNK_BYTES, remaining))
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
            remaining -= len(chunk)
        after = os.fstat(descriptor)
        if (
            total != before.st_size
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
        ):
            raise ValueError(code)
        return digest.hexdigest()
    except OSError as error:
        raise ValueError(code) from error
    finally:
        os.close(descriptor)


def _require_process(result: ProcessResult, code: str) -> None:
    if not result.ok:
        raise ValueError(code)


def _read_engine_version(executable: str) -> str:
    result = run_bounded(
        [executable, "--version"],
        timeout_seconds=5,
        max_captured_bytes=64 * 1024,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")
    try:
        lines = result.stdout.decode("utf-8", errors="strict").splitlines()
    except UnicodeError as error:
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID") from error
    if not lines:
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
    version = lines[0].strip()
    if (
        not version
        or len(version) > 256
        or "/" in version
        or "\\" in version
        or any(ord(character) < 32 for character in version)
    ):
        raise ValueError("TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID")
    return version


def _normalize_audio(
    source: Path,
    destination: Path,
    *,
    ffmpeg_executable: str,
) -> None:
    result = run_bounded(
        [
            ffmpeg_executable,
            "-nostdin",
            "-hide_banner",
            "-loglevel",
            "error",
            "-n",
            "-i",
            str(source),
            "-map",
            "0:a:0",
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            "-f",
            "wav",
            str(destination),
        ],
        timeout_seconds=_AUDIO_TIMEOUT_SECONDS,
        max_captured_bytes=_PROCESS_CAPTURE_BYTES,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_AUDIO_DECODE_FAILED")


def _inspect_normalized_audio(path: Path) -> tuple[int, bool]:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID") from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            with wave.open(stream, "rb") as audio:
                if (
                    audio.getnchannels() != 1
                    or audio.getsampwidth() != 2
                    or audio.getframerate() != 16000
                    or audio.getnframes() < 1
                ):
                    raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
                frame_count = audio.getnframes()
                silent = True
                while frames := audio.readframes(64 * 1024):
                    if any(frames):
                        silent = False
            after = os.fstat(stream.fileno())
            if (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID")
    except (OSError, EOFError, wave.Error) as error:
        raise ValueError("TRITRACK_TRANSCRIBE_AUDIO_INVALID") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    duration_ms = (frame_count * 1000 + 15999) // 16000
    return duration_ms, silent


def _run_whisper(
    audio_path: Path,
    *,
    model_path: Path,
    language: str,
    output_prefix: Path,
    whisper_executable: str,
) -> None:
    result = run_bounded(
        [
            whisper_executable,
            "--model",
            str(model_path),
            "--file",
            str(audio_path),
            "--language",
            language,
            "--temperature",
            "0",
            "--temperature-inc",
            "0",
            "--no-fallback",
            "--no-gpu",
            "--output-json-full",
            "--output-file",
            str(output_prefix),
            "--no-prints",
        ],
        timeout_seconds=_ENGINE_TIMEOUT_SECONDS,
        max_captured_bytes=_PROCESS_CAPTURE_BYTES,
    )
    _require_process(result, "TRITRACK_TRANSCRIBE_ENGINE_FAILED")


def _load_engine_json(path: Path) -> object:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or not (
            0 < before.st_size <= _ENGINE_JSON_LIMIT_BYTES
        ):
            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
        chunks: list[bytes] = []
        remaining = _ENGINE_JSON_LIMIT_BYTES + 1
        while remaining:
            chunk = os.read(descriptor, min(_HASH_CHUNK_BYTES, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(encoded) != before.st_size
            or len(encoded) > _ENGINE_JSON_LIMIT_BYTES
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
        ):
            raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID")
    except OSError as error:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error
    finally:
        os.close(descriptor)
    try:
        return json.loads(encoded.decode("utf-8", errors="strict"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_TRANSCRIPT_EVIDENCE_INVALID") from error


def _publish_transcript_bundle(output_path: Path, bundle: object) -> None:
    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    encoded = encode_transcript_bundle(bundle).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError as error:
            raise ValueError("TRITRACK_OUTPUT_EXISTS") from error
    finally:
        temporary_path.unlink(missing_ok=True)


def transcribe_and_publish(
    media_paths: Sequence[Path],
    *,
    model_path: Path,
    language: str,
    output_path: Path,
    ffmpeg_executable: str = "ffmpeg",
    whisper_executable: str = "whisper-cli",
) -> dict[str, object]:
    """Transcribe local takes once and atomically publish one canonical bundle."""

    destination = require_absent_output(output_path)
    if not destination.parent.is_dir():
        raise ValueError("TRITRACK_OUTPUT_PARENT_MISSING")
    if not media_paths:
        raise ValueError("TRITRACK_TRANSCRIPT_MEDIA_REQUIRED")
    if not isinstance(language, str) or _LANGUAGE.fullmatch(language) is None:
        raise ValueError("TRITRACK_TRANSCRIPT_LANGUAGE_INVALID")

    media = tuple(Path(path) for path in media_paths)
    take_ids = [path.name for path in media]
    if len(take_ids) != len(set(take_ids)):
        raise ValueError("TRITRACK_TRANSCRIPT_DUPLICATE_TAKE")
    for path in media:
        _require_readable_file(path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE")
    selected_model = _require_readable_file(
        Path(model_path), "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
    )

    engine_version = _read_engine_version(whisper_executable)
    model_sha256 = _sha256_file(
        selected_model, "TRITRACK_TRANSCRIPT_MODEL_UNREADABLE"
    )
    source_hashes = {
        path: _sha256_file(path, "TRITRACK_TRANSCRIPT_MEDIA_UNREADABLE")
        for path in media
    }
    takes: list[TranscribedTake] = []
    with tempfile.TemporaryDirectory(prefix="tritrack-transcribe-") as temporary:
        scratch = Path(temporary)
        for index, source in enumerate(sorted(media, key=lambda path: path.name), start=1):
            audio_path = scratch / f"audio-{index:06d}.wav"
            output_prefix = scratch / f"whisper-{index:06d}"
            _normalize_audio(
                source,
                audio_path,
                ffmpeg_executable=ffmpeg_executable,
            )
            duration_ms, silent = _inspect_normalized_audio(audio_path)
            _run_whisper(
                audio_path,
                model_path=selected_model,
                language=language,
                output_prefix=output_prefix,
                whisper_executable=whisper_executable,
            )
            evidence = _load_engine_json(Path(f"{output_prefix}.json"))
            cues = canonicalize_whisper_evidence(
                evidence,
                requested_language=language,
                audio_duration_ms=duration_ms,
                proven_silence=silent,
            )
            if (
                _sha256_file(source) != source_hashes[source]
                or _sha256_file(selected_model) != model_sha256
            ):
                raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")
            if silent and cues:
                raise ValueError("TRITRACK_TRANSCRIPT_SILENCE_TEXT_DETECTED")
            if not silent and not cues:
                raise ValueError("TRITRACK_TRANSCRIPT_EMPTY_UNPROVEN")
            takes.append(
                TranscribedTake(
                    take_id=source.name,
                    source_sha256=source_hashes[source],
                    status="empty" if silent else "completed",
                    cues=tuple(cues),
                )
            )

    if _sha256_file(selected_model) != model_sha256 or any(
        _sha256_file(source) != source_hashes[source] for source in media
    ):
        raise ValueError("TRITRACK_TRANSCRIPT_INPUT_CHANGED")

    bundle = build_transcript_bundle(
        takes,
        language=language,
        model_sha256=model_sha256,
        engine_version=engine_version,
    )
    _publish_transcript_bundle(destination, bundle)
    return bundle
--- END FILE src/tritrack_editing_assistant/transcribe_takes.py ---

--- BEGIN FILE src/tritrack_editing_assistant/validate_artifacts.py ---
"""Read-only, offline validation of public TriTrack artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from jsonschema import ValidationError

from . import __version__, contracts, doctor, emit_fcpxml, paper_edit, run_workflow

MAX_VALIDATION_ARTIFACT_BYTES = 16 * 1024 * 1024


@dataclass(frozen=True)
class LoadedValidationArtifact:
    path: Path
    encoded: bytes
    sha256: str


def _read_regular_bytes(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE")
        if not 0 < metadata.st_size <= MAX_VALIDATION_ARTIFACT_BYTES:
            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            encoded = stream.read(MAX_VALIDATION_ARTIFACT_BYTES + 1)
        if len(encoded) > MAX_VALIDATION_ARTIFACT_BYTES:
            raise ValueError("TRITRACK_VALIDATE_INPUT_INVALID")
        return encoded
    except OSError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_UNREADABLE") from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _load_regular_artifact(path: Path) -> LoadedValidationArtifact:
    selected = Path(path)
    encoded = _read_regular_bytes(selected)
    return LoadedValidationArtifact(
        path=selected,
        encoded=encoded,
        sha256=hashlib.sha256(encoded).hexdigest(),
    )


def _verify_unchanged(artifact: LoadedValidationArtifact) -> None:
    try:
        encoded = _read_regular_bytes(artifact.path)
    except ValueError as error:
        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED") from error
    if hashlib.sha256(encoded).hexdigest() != artifact.sha256:
        raise ValueError("TRITRACK_VALIDATE_INPUT_CHANGED")


def _validation_summary(
    *,
    kind: str,
    scope: str,
    hashes: dict[str, str],
    counts: dict[str, int],
    details: dict[str, object],
) -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.validate-summary/v1",
        "toolVersion": __version__,
        "artifactKind": kind,
        "validationScope": scope,
        "hashes": hashes,
        "counts": counts,
        "details": details,
    }


def validate_contract_artifact(path: Path) -> dict[str, object]:
    """Validate one JSON file against its exact installed closed contract."""

    artifact = _load_regular_artifact(path)
    try:
        payload = json.loads(
            artifact.encoded.decode("utf-8", errors="strict"),
            parse_float=Decimal,
        )
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_VALIDATE_JSON_INVALID") from error
    try:
        schema_version = payload["schemaVersion"]
    except (KeyError, TypeError) as error:
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
    try:
        contract_name = contracts.contract_name_for_schema_version(schema_version)
    except ValueError as error:
        if str(error) == "TRITRACK_CONTRACT_REGISTRY_INVALID":
            raise
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_UNKNOWN") from error
    try:
        contracts.validate_contract(contract_name, payload)
    except (TypeError, ValidationError) as error:
        raise ValueError("TRITRACK_VALIDATE_CONTRACT_INVALID") from error
    _verify_unchanged(artifact)
    return _validation_summary(
        kind="contract",
        scope="contract",
        hashes={"artifact": artifact.sha256},
        counts={},
        details={
            "contractName": contract_name,
            "contractSchemaVersion": schema_version,
        },
    )


def validate_fcpxml_artifact(
    path: Path,
    *,
    profile_id: str,
    binding_id: str,
) -> dict[str, object]:
    """Validate one FCPXML file against exact installed profile authorities."""

    artifact = _load_regular_artifact(path)
    try:
        text = artifact.encoded.decode("utf-8", errors="strict")
    except UnicodeError as error:
        raise ValueError("TRITRACK_VALIDATE_FCPXML_INVALID") from error
    profile = doctor.load_profile(profile_id)
    binding = doctor.load_title_binding(binding_id)
    emit_fcpxml.validate_fcpxml(text, profile=profile, binding=binding)
    _verify_unchanged(artifact)
    return _validation_summary(
        kind="fcpxml",
        scope="structural-profile",
        hashes={"artifact": artifact.sha256},
        counts={},
        details={"profileId": profile_id, "bindingId": binding_id},
    )


def validate_paper_artifacts(
    aligned_path: Path,
    workbook_path: Path,
) -> dict[str, object]:
    """Validate one workbook against the exact aligned JSON authority."""

    validated = paper_edit.validate_workbook(aligned_path, workbook_path)
    return _validation_summary(
        kind="paper",
        scope="authority-bound",
        hashes={
            "aligned": validated.aligned_sha256,
            "workbook": validated.workbook_sha256,
        },
        counts={
            "answerCount": validated.answer_count,
            "cueCount": validated.cue_count,
            "questionCount": validated.question_count,
            "reserveCount": validated.reserve_count,
        },
        details={
            "workbookSchemaVersion": validated.workbook_schema_version,
        },
    )


def validate_run_bundle(run_dir: Path) -> dict[str, object]:
    """Validate and summarize one complete immutable run bundle."""

    bundle, run_summary = run_workflow.inspect_run(run_dir)
    stages = run_summary["stages"]
    artifacts = run_summary["artifacts"]
    assert isinstance(stages, list)
    assert isinstance(artifacts, dict)
    return _validation_summary(
        kind="run",
        scope="complete-run-bundle",
        hashes={"manifest": bundle.manifest_sha256},
        counts={
            "artifactCount": len(artifacts),
            "stageCount": len(stages),
        },
        details={"runSummary": run_summary},
    )
--- END FILE src/tritrack_editing_assistant/validate_artifacts.py ---

--- BEGIN FILE src/tritrack_editing_assistant/profiles/__init__.py ---
"""Packaged, reviewed compatibility and title-binding profiles."""
--- END FILE src/tritrack_editing_assistant/profiles/__init__.py ---

--- BEGIN FILE src/tritrack_editing_assistant/profiles/basic-title-v1.json ---
{
  "schemaVersion": "tritrack.title-binding/v1",
  "bindingId": "basic-title-v1",
  "effectName": "Basic Title",
  "effectUid": ".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti",
  "parameters": [
    {"name": "alignment", "value": "center"},
    {"name": "font", "value": "Helvetica"},
    {"name": "fontColor", "value": "1 1 1 1"},
    {"name": "fontFace", "value": "Regular"},
    {"name": "fontSize", "value": 96}
  ]
}
--- END FILE src/tritrack_editing_assistant/profiles/basic-title-v1.json ---

--- BEGIN FILE src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json ---
{
  "schemaVersion": "tritrack.compatibility-profile/v1",
  "profileId": "uhd-2997-ndf-fcpxml-1.14",
  "fcpxmlVersion": "1.14",
  "frameDuration": "1001/30000s",
  "width": 3840,
  "height": 2160,
  "timecodeFormat": "NDF",
  "audioRate": 48000,
  "colorSpace": "1-1-1 (Rec. 709)"
}
--- END FILE src/tritrack_editing_assistant/profiles/uhd-2997-ndf-fcpxml-1.14.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/__init__.py ---
"""Packaged JSON schemas for TriTrack public contracts."""
--- END FILE src/tritrack_editing_assistant/schemas/__init__.py ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/aligned-transcript-v1.schema.json",
  "title": "TriTrack cue-addressed aligned transcript v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "alignmentProfileId",
    "sourceBundleSha256",
    "revisionSha256",
    "language",
    "takes"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.aligned-transcript/v1"},
    "alignmentProfileId": {"const": "cue-addressed-v1"},
    "sourceBundleSha256": {"$ref": "#/$defs/sha256"},
    "revisionSha256": {"$ref": "#/$defs/sha256"},
    "language": {"type": "string", "pattern": "^[a-z]{2,3}$"},
    "takes": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/$defs/take"}
    }
  },
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "cue": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "cueId",
        "startMs",
        "endMs",
        "text",
        "disposition"
      ],
      "properties": {
        "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
        "startMs": {"type": "integer", "minimum": 0},
        "endMs": {"type": "integer", "minimum": 1},
        "text": {"type": "string", "minLength": 1},
        "disposition": {"enum": ["original", "revised"]}
      }
    },
    "take": {
      "type": "object",
      "additionalProperties": false,
      "required": ["takeId", "sourceSha256", "status", "cues"],
      "properties": {
        "takeId": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[^/\\\\\\r\\n]+$"
        },
        "sourceSha256": {"$ref": "#/$defs/sha256"},
        "status": {"enum": ["completed", "empty"]},
        "cues": {
          "type": "array",
          "items": {"$ref": "#/$defs/cue"}
        }
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "completed"}}},
          "then": {"properties": {"cues": {"minItems": 1}}}
        },
        {
          "if": {"properties": {"status": {"const": "empty"}}},
          "then": {"properties": {"cues": {"maxItems": 0}}}
        }
      ]
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/aligned-transcript-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/compatibility-profile-v1.schema.json",
  "title": "TriTrack compatibility profile v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "profileId",
    "fcpxmlVersion",
    "frameDuration",
    "width",
    "height",
    "timecodeFormat",
    "audioRate",
    "colorSpace"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.compatibility-profile/v1"},
    "profileId": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9.-]*$",
      "minLength": 1
    },
    "fcpxmlVersion": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+$"},
    "frameDuration": {
      "type": "string",
      "pattern": "^[1-9][0-9]*/[1-9][0-9]*s$"
    },
    "width": {"type": "integer", "minimum": 1},
    "height": {"type": "integer", "minimum": 1},
    "timecodeFormat": {"enum": ["DF", "NDF"]},
    "audioRate": {"type": "integer", "minimum": 1},
    "colorSpace": {"type": "string", "minLength": 1}
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/compatibility-profile-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/grouping-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/grouping-v1.schema.json",
  "title": "TriTrack cue-addressed editorial grouping v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "alignedTranscriptSha256",
    "questions",
    "reserve"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.grouping/v1"},
    "alignedTranscriptSha256": {"$ref": "#/$defs/sha256"},
    "questions": {
      "type": "array",
      "minItems": 1,
      "maxItems": 10000,
      "items": {"$ref": "#/$defs/question"}
    },
    "reserve": {
      "type": "array",
      "maxItems": 10000,
      "items": {"$ref": "#/$defs/reserveRange"}
    }
  },
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "safeId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
    },
    "takeId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "pattern": "^[^/\\\\\\r\\n]+$"
    },
    "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
    "questionText": {"type": "string", "minLength": 1, "maxLength": 500},
    "note": {"type": "string", "minLength": 1, "maxLength": 2000},
    "answerRange": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "order",
        "takeId",
        "startCueId",
        "endCueId"
      ],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "order": {"type": "integer", "minimum": 1},
        "takeId": {"$ref": "#/$defs/takeId"},
        "startCueId": {"$ref": "#/$defs/cueId"},
        "endCueId": {"$ref": "#/$defs/cueId"},
        "note": {"$ref": "#/$defs/note"}
      }
    },
    "question": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "question", "order", "answers"],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "question": {"$ref": "#/$defs/questionText"},
        "order": {"type": "integer", "minimum": 1},
        "answers": {
          "type": "array",
          "minItems": 1,
          "maxItems": 10000,
          "items": {"$ref": "#/$defs/answerRange"}
        }
      }
    },
    "reserveRange": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "order",
        "takeId",
        "startCueId",
        "endCueId",
        "reason"
      ],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "order": {"type": "integer", "minimum": 1},
        "takeId": {"$ref": "#/$defs/takeId"},
        "startCueId": {"$ref": "#/$defs/cueId"},
        "endCueId": {"$ref": "#/$defs/cueId"},
        "reason": {"$ref": "#/$defs/questionText"},
        "note": {"$ref": "#/$defs/note"}
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/grouping-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/provider-receipt-v1.schema.json",
  "title": "TriTrack optional provider receipt v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "provider",
    "operation",
    "sourceBundleSha256",
    "takeId",
    "requestedModel",
    "observedModel",
    "audioSha256",
    "requestStatus",
    "responseStatus",
    "upload",
    "serverFileDeletion"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.provider-receipt/v1"},
    "provider": {"type": "string", "minLength": 1},
    "operation": {"const": "audio-transcription"},
    "sourceBundleSha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "takeId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "pattern": "^[^/\\\\\\r\\n]+$"
    },
    "requestedModel": {"type": "string", "minLength": 1},
    "observedModel": {"type": ["string", "null"], "minLength": 1},
    "audioSha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "requestStatus": {"enum": ["completed", "failed", "privacy-incomplete"]},
    "responseStatus": {"type": ["integer", "null"], "minimum": 100, "maximum": 599},
    "upload": {
      "type": "object",
      "additionalProperties": false,
      "required": ["status", "serverFileIdSha256"],
      "properties": {
        "status": {"enum": ["not-started", "completed", "failed"]},
        "serverFileIdSha256": {
          "type": ["string", "null"],
          "pattern": "^[0-9a-f]{64}$"
        }
      }
    },
    "serverFileDeletion": {
      "type": "object",
      "additionalProperties": false,
      "required": ["attempted", "confirmed", "statusCode"],
      "properties": {
        "attempted": {"type": "boolean"},
        "confirmed": {"type": "boolean"},
        "statusCode": {"type": ["integer", "null"], "minimum": 100, "maximum": 599}
      }
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "serverFileDeletion": {
            "properties": {"confirmed": {"const": false}},
            "required": ["confirmed"]
          }
        }
      },
      "then": {"properties": {"requestStatus": {"const": "privacy-incomplete"}}}
    }
  ]
}
--- END FILE src/tritrack_editing_assistant/schemas/provider-receipt-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/run-manifest-v1.schema.json",
  "title": "TriTrack immutable run manifest v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "toolVersion",
    "runId",
    "profileId",
    "bindingId",
    "phase",
    "nextAction",
    "manifestChain",
    "sources",
    "artifacts",
    "stages"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.run-manifest/v1"},
    "toolVersion": {"const": "0.1.0a0"},
    "runId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
    },
    "profileId": {"const": "uhd-2997-ndf-fcpxml-1.14"},
    "bindingId": {"const": "basic-title-v1"},
    "phase": {"enum": ["prepared", "aligned", "finished"]},
    "nextAction": {
      "enum": ["provide-revision", "edit-paper-workbook", "complete"]
    },
    "manifestChain": {
      "type": "array",
      "uniqueItems": true,
      "items": {"$ref": "#/$defs/sha256"}
    },
    "sources": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {"$ref": "#/$defs/source"}
    },
    "artifacts": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "doctorReceipt": {"$ref": "#/$defs/artifact"},
        "syncMap": {"$ref": "#/$defs/artifact"},
        "transcriptBundle": {"$ref": "#/$defs/artifact"},
        "stringOut": {"$ref": "#/$defs/artifact"},
        "alignedTranscript": {"$ref": "#/$defs/artifact"},
        "paperWorkbook": {"$ref": "#/$defs/artifact"},
        "grouping": {"$ref": "#/$defs/artifact"},
        "workingCut": {"$ref": "#/$defs/artifact"},
        "storyCut": {"$ref": "#/$defs/artifact"}
      }
    },
    "stages": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/$defs/stage"}
    }
  },
  "allOf": [
    {
      "if": {"properties": {"phase": {"const": "prepared"}}},
      "then": {
        "properties": {
          "nextAction": {"const": "provide-revision"},
          "manifestChain": {"maxItems": 0},
          "artifacts": {
            "required": [
              "doctorReceipt",
              "syncMap",
              "transcriptBundle",
              "stringOut"
            ],
            "propertyNames": {
              "enum": [
                "doctorReceipt",
                "syncMap",
                "transcriptBundle",
                "stringOut"
              ]
            }
          },
          "stages": {
            "minItems": 4,
            "maxItems": 4,
            "prefixItems": [
              {"properties": {"name": {"const": "doctor"}}},
              {"properties": {"name": {"const": "sync"}}},
              {"properties": {"name": {"const": "transcribe"}}},
              {"properties": {"name": {"const": "emit"}}}
            ]
          }
        }
      }
    },
    {
      "if": {"properties": {"phase": {"const": "aligned"}}},
      "then": {
        "properties": {
          "nextAction": {"const": "edit-paper-workbook"},
          "manifestChain": {"minItems": 1, "maxItems": 1},
          "artifacts": {
            "required": ["alignedTranscript", "paperWorkbook"],
            "propertyNames": {
              "enum": ["alignedTranscript", "paperWorkbook"]
            }
          },
          "stages": {
            "minItems": 2,
            "maxItems": 2,
            "prefixItems": [
              {"properties": {"name": {"const": "align"}}},
              {"properties": {"name": {"const": "paper"}}}
            ]
          }
        }
      }
    },
    {
      "if": {"properties": {"phase": {"const": "finished"}}},
      "then": {
        "properties": {
          "nextAction": {"const": "complete"},
          "manifestChain": {"minItems": 2, "maxItems": 2},
          "artifacts": {
            "required": ["grouping", "workingCut", "storyCut"],
            "propertyNames": {"enum": ["grouping", "workingCut", "storyCut"]}
          },
          "stages": {
            "minItems": 3,
            "maxItems": 3,
            "prefixItems": [
              {"properties": {"name": {"const": "paper"}}},
              {"properties": {"name": {"const": "organize"}}},
              {"properties": {"name": {"const": "emit"}}}
            ]
          }
        }
      }
    }
  ],
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "hashMap": {
      "type": "object",
      "minProperties": 1,
      "propertyNames": {"pattern": "^[A-Za-z][A-Za-z0-9]*$"},
      "additionalProperties": {"$ref": "#/$defs/sha256"}
    },
    "source": {
      "type": "object",
      "additionalProperties": false,
      "required": ["camera", "mediaId", "sha256", "transcribed"],
      "properties": {
        "camera": {"enum": ["A", "B"]},
        "mediaId": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[^/\\\\\\r\\n]+$"
        },
        "sha256": {"$ref": "#/$defs/sha256"},
        "transcribed": {"type": "boolean"}
      }
    },
    "artifact": {
      "type": "object",
      "additionalProperties": false,
      "required": ["fileName", "sha256"],
      "properties": {
        "fileName": {
          "type": "string",
          "minLength": 1,
          "maxLength": 128,
          "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
        },
        "sha256": {"$ref": "#/$defs/sha256"}
      }
    },
    "stage": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "inputHashes", "outputHashes"],
      "properties": {
        "name": {
          "enum": [
            "doctor",
            "sync",
            "transcribe",
            "align",
            "emit",
            "organize",
            "paper"
          ]
        },
        "inputHashes": {"$ref": "#/$defs/hashMap"},
        "outputHashes": {"$ref": "#/$defs/hashMap"}
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/run-manifest-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/sync-map-v1.schema.json",
  "title": "TriTrack synchronization map v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "profileId", "pairs", "singleA", "singleB", "warnings"],
  "properties": {
    "schemaVersion": {"const": "tritrack.sync-map/v1"},
    "profileId": {"type": "string", "minLength": 1},
    "pairs": {
      "type": "array",
      "items": {"$ref": "#/$defs/pair"}
    },
    "singleA": {
      "type": "array",
      "items": {"type": "string", "minLength": 1},
      "uniqueItems": true
    },
    "singleB": {
      "type": "array",
      "items": {"type": "string", "minLength": 1},
      "uniqueItems": true
    },
    "warnings": {
      "type": "array",
      "items": {"$ref": "#/$defs/warning"}
    }
  },
  "$defs": {
    "pair": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "pairId",
        "mediaA",
        "mediaB",
        "offsetBFromASeconds",
        "confidence",
        "overlapSeconds",
        "audioMaster",
        "durationASeconds",
        "durationBSeconds",
        "startedAt"
      ],
      "properties": {
        "pairId": {"type": "string", "minLength": 1},
        "mediaA": {"type": "string", "minLength": 1},
        "mediaB": {"type": "string", "minLength": 1},
        "offsetBFromASeconds": {"type": "number"},
        "confidence": {"type": "number", "minimum": 0},
        "overlapSeconds": {"type": "number", "exclusiveMinimum": 0},
        "audioMaster": {"enum": ["A", "B"]},
        "durationASeconds": {"type": "number", "exclusiveMinimum": 0},
        "durationBSeconds": {"type": "number", "exclusiveMinimum": 0},
        "startedAt": {
          "type": ["string", "null"],
          "format": "date-time"
        }
      }
    },
    "warning": {
      "type": "object",
      "additionalProperties": false,
      "required": ["code"],
      "properties": {
        "code": {"type": "string", "pattern": "^[A-Z][A-Z0-9_]*$"},
        "mediaId": {"type": "string", "minLength": 1}
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/sync-map-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/text-revision-v1.schema.json",
  "title": "TriTrack cue-addressed text revision v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "sourceBundleSha256", "language", "takes"],
  "properties": {
    "schemaVersion": {"const": "tritrack.text-revision/v1"},
    "sourceBundleSha256": {"$ref": "#/$defs/sha256"},
    "language": {"type": "string", "pattern": "^[a-z]{2,3}$"},
    "takes": {
      "type": "array",
      "items": {"$ref": "#/$defs/take"}
    }
  },
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "revision": {
      "type": "object",
      "additionalProperties": false,
      "required": ["cueId", "text"],
      "properties": {
        "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
        "text": {"type": "string", "minLength": 1}
      }
    },
    "take": {
      "type": "object",
      "additionalProperties": false,
      "required": ["takeId", "sourceSha256", "revisions"],
      "properties": {
        "takeId": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[^/\\\\\\r\\n]+$"
        },
        "sourceSha256": {"$ref": "#/$defs/sha256"},
        "revisions": {
          "type": "array",
          "minItems": 1,
          "items": {"$ref": "#/$defs/revision"}
        }
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/text-revision-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/title-binding-v1.schema.json",
  "title": "TriTrack public title binding v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "bindingId", "effectName", "effectUid", "parameters"],
  "properties": {
    "schemaVersion": {"const": "tritrack.title-binding/v1"},
    "bindingId": {"type": "string", "minLength": 1},
    "effectName": {"type": "string", "minLength": 1},
    "effectUid": {"type": "string", "minLength": 1},
    "parameters": {
      "type": "array",
      "items": {"$ref": "#/$defs/parameter"},
      "uniqueItems": true
    }
  },
  "$defs": {
    "parameter": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "value"],
      "properties": {
        "name": {"type": "string", "minLength": 1},
        "value": {"type": ["string", "number", "boolean"]}
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/title-binding-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/transcript-bundle-v1.schema.json",
  "title": "TriTrack local transcript bundle v1",
  "type": "object",
  "additionalProperties": false,
  "required": ["schemaVersion", "profileId", "language", "modelSha256", "engine", "takes"],
  "properties": {
    "schemaVersion": {"const": "tritrack.transcript-bundle/v1"},
    "profileId": {"const": "whisper-cpp-cpu-no-fallback-v1"},
    "language": {"type": "string", "pattern": "^[a-z]{2,3}$"},
    "modelSha256": {"$ref": "#/$defs/sha256"},
    "engine": {
      "type": "object",
      "additionalProperties": false,
      "required": ["name", "version"],
      "properties": {
        "name": {"const": "whisper-cli"},
        "version": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "pattern": "^[^/\\\\\\r\\n]+$"
        }
      }
    },
    "takes": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/$defs/take"}
    }
  },
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "cue": {
      "type": "object",
      "additionalProperties": false,
      "required": ["cueId", "startMs", "endMs", "text"],
      "properties": {
        "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
        "startMs": {"type": "integer", "minimum": 0},
        "endMs": {"type": "integer", "minimum": 1},
        "text": {"type": "string", "minLength": 1}
      }
    },
    "take": {
      "type": "object",
      "additionalProperties": false,
      "required": ["takeId", "sourceSha256", "status", "cues"],
      "properties": {
        "takeId": {
          "type": "string",
          "minLength": 1,
          "maxLength": 255,
          "pattern": "^[^/\\\\\\r\\n]+$"
        },
        "sourceSha256": {"$ref": "#/$defs/sha256"},
        "status": {"enum": ["completed", "empty"]},
        "cues": {
          "type": "array",
          "items": {"$ref": "#/$defs/cue"}
        }
      },
      "allOf": [
        {
          "if": {"properties": {"status": {"const": "completed"}}},
          "then": {"properties": {"cues": {"minItems": 1}}}
        },
        {
          "if": {"properties": {"status": {"const": "empty"}}},
          "then": {"properties": {"cues": {"maxItems": 0}}}
        }
      ]
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/transcript-bundle-v1.schema.json ---

--- BEGIN FILE src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json ---
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tritrack.dev/schemas/working-cut-v1.schema.json",
  "title": "TriTrack compiled working cut v1",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schemaVersion",
    "organizationProfileId",
    "alignedTranscriptSha256",
    "groupingSha256",
    "questions",
    "segments",
    "reserve"
  ],
  "properties": {
    "schemaVersion": {"const": "tritrack.working-cut/v1"},
    "organizationProfileId": {
      "const": "cue-addressed-question-groups-v1"
    },
    "alignedTranscriptSha256": {"$ref": "#/$defs/sha256"},
    "groupingSha256": {"$ref": "#/$defs/sha256"},
    "questions": {
      "type": "array",
      "minItems": 1,
      "maxItems": 10000,
      "items": {"$ref": "#/$defs/question"}
    },
    "segments": {
      "type": "array",
      "minItems": 1,
      "maxItems": 10000,
      "items": {"$ref": "#/$defs/segment"}
    },
    "reserve": {
      "type": "array",
      "maxItems": 10000,
      "items": {"$ref": "#/$defs/reserveRange"}
    }
  },
  "$defs": {
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "safeId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$"
    },
    "takeId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "pattern": "^[^/\\\\\\r\\n]+$"
    },
    "cueId": {"type": "string", "pattern": "^cue-[0-9]{6}$"},
    "editorText": {"type": "string", "minLength": 1, "maxLength": 500},
    "note": {"type": "string", "minLength": 1, "maxLength": 2000},
    "question": {
      "type": "object",
      "additionalProperties": false,
      "required": ["id", "question", "order"],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "question": {"$ref": "#/$defs/editorText"},
        "order": {"type": "integer", "minimum": 1}
      }
    },
    "segment": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "storyOrder",
        "questionId",
        "takeId",
        "sourceSha256",
        "startCueId",
        "endCueId",
        "startMs",
        "endMs"
      ],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "storyOrder": {"type": "integer", "minimum": 1},
        "questionId": {"$ref": "#/$defs/safeId"},
        "takeId": {"$ref": "#/$defs/takeId"},
        "sourceSha256": {"$ref": "#/$defs/sha256"},
        "startCueId": {"$ref": "#/$defs/cueId"},
        "endCueId": {"$ref": "#/$defs/cueId"},
        "startMs": {"type": "integer", "minimum": 0},
        "endMs": {"type": "integer", "minimum": 1},
        "note": {"$ref": "#/$defs/note"}
      }
    },
    "reserveRange": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id",
        "order",
        "takeId",
        "sourceSha256",
        "startCueId",
        "endCueId",
        "startMs",
        "endMs",
        "reason"
      ],
      "properties": {
        "id": {"$ref": "#/$defs/safeId"},
        "order": {"type": "integer", "minimum": 1},
        "takeId": {"$ref": "#/$defs/takeId"},
        "sourceSha256": {"$ref": "#/$defs/sha256"},
        "startCueId": {"$ref": "#/$defs/cueId"},
        "endCueId": {"$ref": "#/$defs/cueId"},
        "startMs": {"type": "integer", "minimum": 0},
        "endMs": {"type": "integer", "minimum": 1},
        "reason": {"$ref": "#/$defs/editorText"},
        "note": {"$ref": "#/$defs/note"}
      }
    }
  }
}
--- END FILE src/tritrack_editing_assistant/schemas/working-cut-v1.schema.json ---

--- BEGIN FILE scripts/release_gate.py ---
"""Maintainer-only Task 11 release-readiness command."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if __package__:
    from scripts import release_gate_core
else:
    import release_gate_core


class _UsageError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise _UsageError from None


def _error(code: str) -> None:
    print(json.dumps({"error": code}, separators=(",", ":")), file=sys.stderr)


def _parser() -> argparse.ArgumentParser:
    parser = _Parser(add_help=True, allow_abbrev=False)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        arguments = _parser().parse_args(argv)
    except _UsageError:
        _error("TRITRACK_RELEASE_USAGE")
        return 64
    try:
        manifest = release_gate_core.run_release_gate(
            Path(arguments.source), Path(arguments.output)
        )
        manifest_sha = hashlib.sha256(
            release_gate_core._canonical_manifest(manifest)
        ).hexdigest()
        project = manifest["project"]
        artifacts = manifest["artifacts"]
        lines = (
            "RELEASE_GATE\tPASS",
            f"commit\t{project['commit']}",
            f"version\t{project['version']}",
            f"wheelSha256\t{artifacts['wheel']['sha256']}",
            f"sdistSha256\t{artifacts['sdist']['sha256']}",
            f"manifestSha256\t{manifest_sha}",
        )
    except release_gate_core.ReleaseGateError as error:
        _error(error.code)
        return 1
    except Exception:  # noqa: BLE001 - the public boundary must never emit a traceback
        _error("TRITRACK_RELEASE_INTERNAL")
        return 1
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
--- END FILE scripts/release_gate.py ---

--- BEGIN FILE scripts/release_gate_core.py ---
"""Bounded, fail-closed primitives for the maintainer release gate."""

from __future__ import annotations

import hashlib
import importlib.metadata
import io
import json
import os
import platform
import re
import selectors
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import unicodedata
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

import jsonschema

_COMMAND_TIMEOUT_SECONDS = 30
_COMMAND_OUTPUT_LIMIT = 8 * 1024 * 1024
_POLICY_LIMIT = 1024 * 1024
_ALLOWED_FAKE_USERS = frozenset({b"editor", b"example", b"fake", b"test"})
_ALLOWED_FAKE_SECRETS = frozenset(
    {b"example", b"fake", b"placeholder", b"redacted", b"secret", b"test"}
)
_READ_CHUNK_BYTES = 64 * 1024
_TERMINATION_GRACE_SECONDS = 0.2


class ReleaseGateError(Exception):
    """One stable public-safe release-gate failure code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True)
class SourceInventory:
    count: int
    total_bytes: int
    sha256: str
    commit: str


@dataclass(frozen=True)
class DistributionInspection:
    sha256: str
    size_bytes: int
    member_count: int
    member_inventory_sha256: str


@dataclass(frozen=True)
class ReleaseContext:
    project_name: str
    version: str
    commit: str
    source_inventory: SourceInventory
    toolchain: Mapping[str, str]
    python_version: str
    implementation: str
    system: str
    machine: str
    wheel: DistributionInspection
    sdist: DistributionInspection


@dataclass(frozen=True)
class _BoundedCommandResult:
    status: str
    returncode: int | None
    stdout: bytes
    stderr: bytes


def _fail(code: str) -> None:
    raise ReleaseGateError(code)


def _safe_environment() -> dict[str, str]:
    return {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": os.defpath,
    }


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        except OSError:
            if process.poll() is None:
                process.terminate()
    elif process.poll() is None:
        process.terminate()

    try:
        process.wait(timeout=_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        pass

    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            if process.poll() is None:
                process.kill()
    elif process.poll() is None:
        process.kill()

    if process.poll() is None:
        process.wait()


def _close_process_pipes(process: subprocess.Popen[bytes]) -> None:
    if process.stdout is not None:
        process.stdout.close()
    if process.stderr is not None:
        process.stderr.close()


def _run_bounded_subprocess(
    argv: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout: int,
    output_limit: int,
) -> _BoundedCommandResult:
    """Run one argv-only child while bounding combined retained output."""

    if timeout < 1 or output_limit < 1:
        return _BoundedCommandResult("invalid", None, b"", b"")
    try:
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=dict(env),
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError:
        return _BoundedCommandResult("spawn_error", None, b"", b"")

    deadline = time.monotonic() + timeout
    stdout_chunks: list[bytes] = []
    stderr_chunks: list[bytes] = []
    captured = 0
    status = "ok"
    try:
        with selectors.DefaultSelector() as selector:
            assert process.stdout is not None
            assert process.stderr is not None
            selector.register(process.stdout, selectors.EVENT_READ, stdout_chunks)
            selector.register(process.stderr, selectors.EVENT_READ, stderr_chunks)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    status = "timeout"
                    break
                for key, _mask in selector.select(timeout=min(remaining, 0.05)):
                    allowed_read = output_limit - captured + 1
                    chunk = os.read(
                        key.fd,
                        min(_READ_CHUNK_BYTES, max(1, allowed_read)),
                    )
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    captured += len(chunk)
                    if captured > output_limit:
                        status = "output_limit_exceeded"
                        break
                    key.data.append(chunk)
                if status != "ok":
                    break

        if status == "ok":
            remaining = deadline - time.monotonic()
            if remaining <= 0 and process.poll() is None:
                status = "timeout"
            else:
                try:
                    process.wait(timeout=max(0.0, remaining))
                except subprocess.TimeoutExpired:
                    status = "timeout"
        if status != "ok":
            _terminate_process_group(process)
            return _BoundedCommandResult(status, process.returncode, b"", b"")
        return _BoundedCommandResult(
            "ok" if process.returncode == 0 else "failed",
            process.returncode,
            b"".join(stdout_chunks),
            b"".join(stderr_chunks),
        )
    except OSError:
        _terminate_process_group(process)
        return _BoundedCommandResult("capture_error", process.returncode, b"", b"")
    except BaseException:
        _terminate_process_group(process)
        raise
    finally:
        _close_process_pipes(process)


def _run_git(source: Path, *arguments: str) -> bytes:
    result = _run_bounded_subprocess(
        ["git", *arguments],
        cwd=source,
        env=_safe_environment(),
        timeout=_COMMAND_TIMEOUT_SECONDS,
        output_limit=_COMMAND_OUTPUT_LIMIT,
    )
    if result.status == "output_limit_exceeded":
        _fail("TRITRACK_RELEASE_GIT_LIMIT")
    if result.status != "ok":
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    return result.stdout


def _read_regular(path: Path, limit: int) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if details.st_size > limit:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        if len(encoded) > limit or len(encoded) != details.st_size:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_READ")
    finally:
        os.close(descriptor)


def _mapping(value: object, code: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        _fail(code)
    return value


def _positive_limit(policy: Mapping[str, object], name: str) -> int:
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    value = limits.get(name)
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return value


def _build_epoch(policy: Mapping[str, object]) -> int:
    build = _mapping(policy.get("build"), "TRITRACK_RELEASE_POLICY_INVALID")
    if set(build) != {"sourceDateEpoch"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    value = build.get("sourceDateEpoch")
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value < 315532800
    ):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return value


def _string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if len(value) != len(set(value)):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    return tuple(value)


def _load_policy(source: Path) -> Mapping[str, object]:
    encoded = _read_regular(source / "release" / "package-policy-v1.json", _POLICY_LIMIT)
    try:
        policy = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    policy = _mapping(policy, "TRITRACK_RELEASE_POLICY_INVALID")
    if policy.get("schemaVersion") != "tritrack.package-policy/v1":
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    if set(policy) != {
        "schemaVersion",
        "build",
        "limits",
        "source",
        "wheel",
        "sdist",
    }:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _build_epoch(policy)
    limits = _mapping(policy.get("limits"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected_limits = {
        "sourceMaxFiles",
        "sourceMaxFileBytes",
        "sourceMaxTotalBytes",
        "archiveMaxBytes",
        "archiveMaxMembers",
        "memberMaxBytes",
        "expandedMaxBytes",
    }
    if set(limits) != expected_limits:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    for name in expected_limits:
        _positive_limit(policy, name)

    source_policy = _mapping(
        policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(source_policy) != {
        "allowedFakeHomeUsers",
        "allowedFakeSecretValues",
        "forbiddenSuffixes",
    }:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    allowed_users = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeHomeUsers"))
    )
    allowed_secrets = frozenset(
        value.encode("utf-8")
        for value in _string_list(source_policy.get("allowedFakeSecretValues"))
    )
    if (
        allowed_users != _ALLOWED_FAKE_USERS
        or allowed_secrets != _ALLOWED_FAKE_SECRETS
    ):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(source_policy.get("forbiddenSuffixes"))

    wheel_policy = _mapping(
        policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(wheel_policy) != {"expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(wheel_policy.get("expectedMembers"))

    sdist_policy = _mapping(
        policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID"
    )
    if set(sdist_policy) != {"root", "expectedMembers"}:
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    _string_list(sdist_policy.get("expectedMembers"))
    return policy


def _status(source: Path) -> bytes:
    return _run_git(
        source,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )


def _safe_source_path(encoded: bytes) -> str:
    try:
        name = encoded.decode("utf-8", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    candidate = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or candidate.is_absolute()
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        _fail("TRITRACK_RELEASE_SOURCE_PATH")
    return name


def _parse_index(encoded: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    for raw in encoded.split(b"\0"):
        if not raw:
            continue
        try:
            prefix, raw_path = raw.split(b"\t", 1)
            mode, object_id, stage = prefix.decode("ascii").split(" ")
        except (ValueError, UnicodeDecodeError):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        if stage != "0":
            _fail("TRITRACK_RELEASE_SOURCE_STAGE")
        if mode not in {"100644", "100755"}:
            _fail("TRITRACK_RELEASE_SOURCE_MODE")
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id):
            _fail("TRITRACK_RELEASE_INDEX_INVALID")
        entries.append((_safe_source_path(raw_path), mode, object_id))
    if not entries:
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    if len({entry[0] for entry in entries}) != len(entries):
        _fail("TRITRACK_RELEASE_INDEX_INVALID")
    return entries


def _git_blob_hash(encoded: bytes, algorithm: str) -> str:
    if algorithm not in {"sha1", "sha256"}:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    digest = hashlib.new(algorithm)
    digest.update(f"blob {len(encoded)}\0".encode("ascii"))
    digest.update(encoded)
    return digest.hexdigest()


def _path_signature(path: Path) -> tuple[int, int, int, int]:
    try:
        details = path.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)


def _home_user_after(encoded: bytes, marker: bytes, separator: bytes) -> bytes | None:
    lowered = encoded.lower()
    offset = 0
    lowered_marker = marker.lower()
    while True:
        found = lowered.find(lowered_marker, offset)
        if found < 0:
            return None
        start = found + len(marker)
        end = start
        while end < len(encoded) and encoded[end : end + 1] not in (
            separator,
            b"/",
            b"\\",
            b"\0",
            b"\t",
            b"\r",
            b"\n",
            b" ",
            b'"',
            b"'",
        ):
            end += 1
        user = lowered[start:end]
        if user and user not in _ALLOWED_FAKE_USERS:
            return user
        offset = max(end, start + 1)


def scan_public_bytes(encoded: bytes) -> None:
    """Reject public-source privacy canaries without returning matched bytes."""

    mac_home = b"/" + b"Users" + b"/"
    linux_home = b"/" + b"home" + b"/"
    windows_home = b"\\" + b"Users" + b"\\"
    mounted_volume = b"/" + b"Volumes" + b"/"
    for marker, separator in (
        (mac_home, b"/"),
        (linux_home, b"/"),
        (windows_home, b"\\"),
    ):
        if _home_user_after(encoded, marker, separator) is not None:
            _fail("TRITRACK_RELEASE_PRIVATE_PATH")
    if mounted_volume.lower() in encoded.lower():
        _fail("TRITRACK_RELEASE_PRIVATE_PATH")

    private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
    rsa_private_key = b"-----BEGIN RSA " + b"PRIVATE KEY-----"
    if private_key in encoded or rsa_private_key in encoded:
        _fail("TRITRACK_RELEASE_PRIVATE_KEY")

    terms = (
        b"api" + b"[_-]?key",
        b"auth" + b"[_-]?token",
        b"access" + b"[_-]?token",
        b"password",
        b"passwd",
        b"secret",
    )
    assignment = re.compile(
        rb"(?im)\b(?:"
        + b"|".join(terms)
        + rb")\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+${}\-]{1,256})"
    )
    for match in assignment.finditer(encoded):
        value = match.group(1).rstrip(b"'\"").lower()
        if value not in _ALLOWED_FAKE_SECRETS:
            _fail("TRITRACK_RELEASE_CREDENTIAL")

    credential_shapes = (
        rb"\bgh" + rb"[pousr]_[A-Za-z0-9]{36,255}\b",
        rb"\bAK" + rb"IA[0-9A-Z]{16}\b",
        rb"\bAI" + rb"za[0-9A-Za-z_-]{35}\b",
        rb"\bxox" + rb"[baprs]-[0-9A-Za-z-]{20,255}\b",
    )
    if any(re.search(pattern, encoded) for pattern in credential_shapes):
        _fail("TRITRACK_RELEASE_CREDENTIAL")


def inventory_tracked_source(source: Path) -> SourceInventory:
    """Bind one clean Git index to the exact regular working-tree bytes."""

    source = source.resolve()
    policy = _load_policy(source)
    index_bytes = _run_git(source, "ls-files", "-s", "-z")
    entries = _parse_index(index_bytes)
    if _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_DIRTY")
    max_files = _positive_limit(policy, "sourceMaxFiles")
    max_file_bytes = _positive_limit(policy, "sourceMaxFileBytes")
    max_total_bytes = _positive_limit(policy, "sourceMaxTotalBytes")
    if len(entries) > max_files:
        _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
    source_policy = _mapping(policy.get("source"), "TRITRACK_RELEASE_POLICY_INVALID")
    suffixes = tuple(item.casefold() for item in _string_list(source_policy.get("forbiddenSuffixes")))
    object_format = _run_git(source, "rev-parse", "--show-object-format").strip()
    try:
        algorithm = object_format.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FORMAT")
    commit_bytes = _run_git(source, "rev-parse", "HEAD").strip()
    try:
        commit = commit_bytes.decode("ascii", "strict")
    except UnicodeDecodeError:
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        _fail("TRITRACK_RELEASE_GIT_FAILED")

    total = 0
    inventory = hashlib.sha256()
    for name, mode, object_id in sorted(entries):
        if suffixes and name.casefold().endswith(suffixes):
            _fail("TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE")
        path = source / name
        before = _path_signature(path)
        if before[2] > max_file_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += before[2]
        if total > max_total_bytes:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        encoded = _read_regular(path, max_file_bytes)
        after = _path_signature(path)
        if before != after:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        if _git_blob_hash(encoded, algorithm) != object_id:
            _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
        scan_public_bytes(encoded)
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, mode, str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")

    if _run_git(source, "ls-files", "-s", "-z") != index_bytes or _status(source):
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")
    return SourceInventory(
        count=len(entries),
        total_bytes=total,
        sha256=inventory.hexdigest(),
        commit=commit,
    )


def _read_archive_bytes(path: Path, policy: Mapping[str, object]) -> bytes:
    limit = _positive_limit(policy, "archiveMaxBytes")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
        if not 0 < before.st_size <= limit:
            _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(encoded) > limit
            or len(encoded) != before.st_size
            or (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        ):
            _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
        return encoded
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_READ")
    finally:
        os.close(descriptor)


def _safe_member_name(name: str) -> str:
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    normalized = unicodedata.normalize("NFC", name)
    path = PurePosixPath(normalized)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
    return normalized.rstrip("/")


def _bounded_archive_read(stream, expected: int, limit: int) -> bytes:
    if expected > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    encoded = stream.read(limit + 1)
    if len(encoded) != expected or len(encoded) > limit:
        _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
    return encoded


def _member_digest(
    inventory: hashlib._Hash,
    name: str,
    member_type: str,
    mode: int,
    encoded: bytes,
) -> None:
    values = (
        name,
        member_type,
        f"{mode & 0o7777:o}",
        str(len(encoded)),
        hashlib.sha256(encoded).hexdigest(),
    )
    for value in values:
        inventory.update(value.encode("utf-8"))
        inventory.update(b"\0")
    inventory.update(b"\n")


def _check_collision(name: str, exact: set[str], folded: set[str]) -> None:
    if name in exact:
        _fail("TRITRACK_RELEASE_ARCHIVE_DUPLICATE")
    collision = unicodedata.normalize("NFC", name).casefold()
    if collision in folded:
        _fail("TRITRACK_RELEASE_ARCHIVE_COLLISION")
    exact.add(name)
    folded.add(collision)


def inspect_wheel(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a wheel without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    wheel_policy = _mapping(policy.get("wheel"), "TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(wheel_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[zipfile.ZipInfo, str, int]] = []
    expanded = 0
    try:
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
            members = archive.infolist()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                name = _safe_member_name(member.filename)
                _check_collision(name, exact, folded)
                if member.flag_bits & 1:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ENCRYPTED")
                if member.is_dir():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                raw_mode = member.external_attr >> 16
                member_type = stat.S_IFMT(raw_mode)
                if member_type not in {0, stat.S_IFREG}:
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                expanded += member.file_size
                if member.file_size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, name, raw_mode))
            if {name for _, name, _ in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, raw_mode in sorted(files, key=lambda item: item[1]):
                with archive.open(member) as stream:
                    encoded = _bounded_archive_read(stream, member.file_size, max_member)
                scan_public_bytes(encoded)
                _member_digest(inventory, name, "file", raw_mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(files),
        member_inventory_sha256=inventory.hexdigest(),
    )


def inspect_sdist(
    path: Path, policy: Mapping[str, object]
) -> DistributionInspection:
    """Inspect a gzipped source distribution without extracting it."""

    archive_bytes = _read_archive_bytes(path, policy)
    size_bytes = len(archive_bytes)
    max_members = _positive_limit(policy, "archiveMaxMembers")
    max_member = _positive_limit(policy, "memberMaxBytes")
    max_expanded = _positive_limit(policy, "expandedMaxBytes")
    sdist_policy = _mapping(policy.get("sdist"), "TRITRACK_RELEASE_POLICY_INVALID")
    root = sdist_policy.get("root")
    if not isinstance(root, str) or not root.endswith("/"):
        _fail("TRITRACK_RELEASE_POLICY_INVALID")
    expected = set(_string_list(sdist_policy.get("expectedMembers")))
    exact: set[str] = set()
    folded: set[str] = set()
    files: list[tuple[tarfile.TarInfo, str]] = []
    all_members: list[tuple[tarfile.TarInfo, str, str]] = []
    expanded = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            if len(members) > max_members:
                _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
            for member in members:
                full_name = _safe_member_name(member.name)
                if full_name == root.rstrip("/"):
                    relative = ""
                elif full_name.startswith(root):
                    relative = full_name[len(root) :]
                else:
                    _fail("TRITRACK_RELEASE_ARCHIVE_ROOT")
                collision_name = relative or "."
                _check_collision(collision_name, exact, folded)
                if member.isdir():
                    all_members.append((member, relative, "directory"))
                    continue
                if not member.isreg():
                    _fail("TRITRACK_RELEASE_ARCHIVE_TYPE")
                if not relative:
                    _fail("TRITRACK_RELEASE_ARCHIVE_PATH")
                expanded += member.size
                if member.size > max_member or expanded > max_expanded:
                    _fail("TRITRACK_RELEASE_ARCHIVE_LIMIT")
                files.append((member, relative))
                all_members.append((member, relative, "file"))
            if {name for _, name in files} != expected:
                _fail("TRITRACK_RELEASE_ARCHIVE_CONTENT")
            inventory = hashlib.sha256()
            for member, name, member_type in sorted(all_members, key=lambda item: item[1]):
                if member_type == "directory":
                    encoded = b""
                else:
                    stream = archive.extractfile(member)
                    if stream is None:
                        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
                    with stream:
                        encoded = _bounded_archive_read(stream, member.size, max_member)
                    scan_public_bytes(encoded)
                _member_digest(inventory, name or ".", member_type, member.mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, ValueError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_ARCHIVE_INVALID")
    return DistributionInspection(
        sha256=hashlib.sha256(archive_bytes).hexdigest(),
        size_bytes=size_bytes,
        member_count=len(all_members),
        member_inventory_sha256=inventory.hexdigest(),
    )


def _run_command(
    argv: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    timeout: int = 300,
    output_limit: int = _COMMAND_OUTPUT_LIMIT,
) -> bytes:
    result = _run_bounded_subprocess(
        argv,
        cwd=cwd,
        env=env,
        timeout=timeout,
        output_limit=output_limit,
    )
    if result.status == "output_limit_exceeded":
        _fail("TRITRACK_RELEASE_COMMAND_LIMIT")
    if result.status != "ok":
        _fail("TRITRACK_RELEASE_COMMAND_FAILED")
    return result.stdout


def _installed_tool_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for distribution in ("pip", "build", "setuptools", "wheel"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            _fail("TRITRACK_RELEASE_TOOLCHAIN")
    return versions


def _build_environment(epoch: int, temporary: Path) -> dict[str, str]:
    if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 0:
        _fail("TRITRACK_RELEASE_EPOCH")
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.defpath,
        "PYTHONHASHSEED": "0",
        "SOURCE_DATE_EPOCH": str(epoch),
        "TMPDIR": os.fspath(temporary),
    }
    return environment


def build_distributions(
    snapshot: Path, output: Path, *, epoch: int
) -> tuple[Path, Path]:
    """Build exactly one wheel and one sdist with the pinned local toolchain."""

    expected_tools = {
        "pip": "26.2",
        "build": "1.5.0",
        "setuptools": "84.0.0",
        "wheel": "0.48.0",
    }
    if _installed_tool_versions() != expected_tools:
        _fail("TRITRACK_RELEASE_TOOLCHAIN")
    if not snapshot.is_dir():
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    try:
        os.mkdir(output)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [
            os.fspath(Path(sys.executable)),
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            os.fspath(output),
        ],
        cwd=snapshot,
        env=_build_environment(epoch, output),
        timeout=300,
    )
    try:
        members = [
            child
            for child in output.iterdir()
            if child.is_file() and not child.is_symlink()
        ]
    except OSError:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    wheels = [child for child in members if child.suffix == ".whl"]
    sdists = [child for child in members if child.name.endswith(".tar.gz")]
    if len(members) != 2 or len(wheels) != 1 or len(sdists) != 1:
        _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
    return wheels[0], sdists[0]


def _wheel_project_identity(wheel: Path) -> tuple[str, str]:
    try:
        with zipfile.ZipFile(wheel) as archive:
            candidates = [
                member
                for member in archive.infolist()
                if member.filename.endswith(".dist-info/METADATA")
                and not member.is_dir()
            ]
            if len(candidates) != 1 or candidates[0].file_size > _POLICY_LIMIT:
                _fail("TRITRACK_RELEASE_WHEEL_METADATA")
            with archive.open(candidates[0]) as stream:
                encoded = _bounded_archive_read(
                    stream, candidates[0].file_size, _POLICY_LIMIT
                )
    except ReleaseGateError:
        raise
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError):
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    message = BytesParser().parsebytes(encoded)
    name = message.get("Name")
    version = message.get("Version")
    if not name or not version or "\n" in name or "\n" in version:
        _fail("TRITRACK_RELEASE_WHEEL_METADATA")
    return name, version


def _install_environment(temporary: Path, binary: Path) -> dict[str, str]:
    environment = {
        "HOME": os.fspath(temporary),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PATH": os.fspath(binary) + os.pathsep + os.defpath,
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PYTHONHASHSEED": "0",
        "TMPDIR": os.fspath(temporary),
    }
    for name in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "NO_PROXY",
        "PIP_INDEX_URL",
        "PIP_TRUSTED_HOST",
    ):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    return environment


def fresh_install_smoke(wheel: Path, temporary: Path) -> None:
    """Install only the chosen local wheel into a new external environment."""

    project_name, project_version = _wheel_project_identity(wheel)
    if project_name != "tritrack-editing-assistant":
        _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
    try:
        os.mkdir(temporary)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    _run_command(
        [os.fspath(Path(sys.executable)), "-m", "venv", os.fspath(temporary)],
        cwd=temporary.parent,
        env=_build_environment(0, temporary),
        timeout=180,
    )
    if os.name == "nt":
        binary = temporary / "Scripts"
        python = binary / "python.exe"
        tritrack = binary / "tritrack.exe"
    else:
        binary = temporary / "bin"
        python = binary / "python"
        tritrack = binary / "tritrack"
    environment = _install_environment(temporary, binary)
    pip_base = [
        os.fspath(python),
        "-m",
        "pip",
        "--disable-pip-version-check",
        "--no-input",
    ]
    _run_command(
        [*pip_base, "install", "pip==26.2"],
        cwd=temporary,
        env=environment,
        timeout=300,
    )
    _run_command(
        [*pip_base, "install", os.fspath(wheel.resolve())],
        cwd=temporary,
        env=environment,
        timeout=600,
    )
    _run_command(
        [*pip_base, "check"], cwd=temporary, env=environment, timeout=120
    )
    metadata_code = (
        "import importlib.metadata as m; "
        "d=m.distribution('tritrack-editing-assistant'); "
        "print(d.metadata['Name']+'\\t'+d.version)"
    )
    installed = _run_command(
        [os.fspath(python), "-I", "-c", metadata_code],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    expected = f"{project_name}\t{project_version}\n".encode()
    if installed != expected:
        _fail("TRITRACK_RELEASE_INSTALLED_IDENTITY")
    components = _run_command(
        [os.fspath(tritrack), "components", "--json"],
        cwd=temporary,
        env=environment,
        timeout=60,
    )
    try:
        component_summary = json.loads(components.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    if (
        not isinstance(component_summary, Mapping)
        or component_summary.get("schemaVersion") != "tritrack.components/v1"
        or not isinstance(component_summary.get("components"), list)
        or len(component_summary["components"]) != 11
    ):
        _fail("TRITRACK_RELEASE_INSTALLED_SMOKE")
    for arguments in (
        ("validate", "--help"),
        ("validate", "contract", "--help"),
        ("validate", "fcpxml", "--help"),
        ("validate", "paper", "--help"),
        ("validate", "run", "--help"),
    ):
        _run_command(
            [os.fspath(tritrack), *arguments],
            cwd=temporary,
            env=environment,
            timeout=60,
        )


def build_release_manifest(context: ReleaseContext) -> dict[str, object]:
    """Build and validate the deterministic, closed public release receipt."""

    manifest: dict[str, object] = {
        "schemaVersion": "tritrack.release-manifest/v1",
        "project": {
            "name": context.project_name,
            "version": context.version,
            "commit": context.commit,
        },
        "sourceInventory": {
            "count": context.source_inventory.count,
            "sha256": context.source_inventory.sha256,
        },
        "toolchain": {
            "python": context.python_version,
            "implementation": context.implementation,
            "pip": context.toolchain["pip"],
            "build": context.toolchain["build"],
            "setuptools": context.toolchain["setuptools"],
            "wheel": context.toolchain["wheel"],
        },
        "platform": {"system": context.system, "machine": context.machine},
        "artifacts": {
            "wheel": {
                "sha256": context.wheel.sha256,
                "sizeBytes": context.wheel.size_bytes,
                "memberCount": context.wheel.member_count,
                "memberInventorySha256": context.wheel.member_inventory_sha256,
            },
            "sdist": {
                "sha256": context.sdist.sha256,
                "sizeBytes": context.sdist.size_bytes,
                "memberCount": context.sdist.member_count,
                "memberInventorySha256": context.sdist.member_inventory_sha256,
            },
        },
        "reproducibility": {
            "wheelBytesMatch": True,
            "sdistMembersMatch": True,
        },
        "gates": {
            "sourceIdentity": "pass",
            "sourcePrivacy": "pass",
            "wheelArchive": "pass",
            "sdistArchive": "pass",
            "freshInstall": "pass",
        },
        "nonClaims": [
            "no-tag",
            "no-release",
            "no-package-publication",
            "no-pull-request",
            "no-tester-contact",
            "no-signing",
            "no-attestation",
            "no-sbom",
            "no-final-cut-gui",
            "no-dtd",
            "no-provider",
            "no-application-submission",
        ],
    }
    schema_path = Path(__file__).resolve().parents[1] / "release" / "release-manifest-v1.schema.json"
    try:
        schema = json.loads(_read_regular(schema_path, _POLICY_LIMIT).decode("utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(manifest, schema)
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    return manifest


def _link_file(source: Path, destination: Path) -> None:
    try:
        os.link(source, destination, follow_symlinks=False)
    except FileExistsError:
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        _fail("TRITRACK_RELEASE_PUBLISH")


def _publication_artifacts(manifest: bytes) -> dict[str, tuple[int, str]]:
    if not 0 < len(manifest) <= _POLICY_LIMIT:
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
    try:
        payload = _mapping(
            json.loads(manifest.decode("utf-8", errors="strict")),
            "TRITRACK_RELEASE_MANIFEST_INVALID",
        )
        artifacts = _mapping(
            payload.get("artifacts"), "TRITRACK_RELEASE_MANIFEST_INVALID"
        )
        result: dict[str, tuple[int, str]] = {}
        for kind in ("wheel", "sdist"):
            artifact = _mapping(
                artifacts.get(kind), "TRITRACK_RELEASE_MANIFEST_INVALID"
            )
            size = artifact.get("sizeBytes")
            digest = artifact.get("sha256")
            if (
                not isinstance(size, int)
                or isinstance(size, bool)
                or size < 1
                or not isinstance(digest, str)
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
            ):
                _fail("TRITRACK_RELEASE_MANIFEST_INVALID")
            result[kind] = (size, digest)
        return result
    except ReleaseGateError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_MANIFEST_INVALID")


def _verify_published_archive(path: Path, expected: tuple[int, str]) -> None:
    expected_size, expected_sha256 = expected
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
        try:
            details = os.fstat(descriptor)
            if not stat.S_ISREG(details.st_mode) or details.st_size != expected_size:
                _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
            digest = hashlib.sha256()
            observed_size = 0
            while observed_size <= expected_size:
                chunk = os.read(
                    descriptor,
                    min(1024 * 1024, expected_size + 1 - observed_size),
                )
                if not chunk:
                    break
                observed_size += len(chunk)
                digest.update(chunk)
            after = os.fstat(descriptor)
        finally:
            os.close(descriptor)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")
    if (
        observed_size != expected_size
        or digest.hexdigest() != expected_sha256
        or (details.st_dev, details.st_ino, details.st_size, details.st_mtime_ns)
        != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    ):
        _fail("TRITRACK_RELEASE_ARCHIVE_CHANGED")


def publish_release(
    output: Path, wheel: Path, sdist: Path, manifest: bytes
) -> None:
    """Publish two archives first and the canonical success manifest last."""

    if (
        wheel.name in {"", ".", "..", "release-manifest.json"}
        or sdist.name in {"", ".", "..", "release-manifest.json"}
        or wheel.name != os.path.basename(wheel.name)
        or sdist.name != os.path.basename(sdist.name)
        or wheel.name == sdist.name
    ):
        _fail("TRITRACK_RELEASE_PUBLISH")
    expected_artifacts = _publication_artifacts(manifest)
    try:
        parent_details = output.parent.stat(follow_symlinks=False)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    if not stat.S_ISDIR(parent_details.st_mode):
        _fail("TRITRACK_RELEASE_OUTPUT")

    temporary_manifest: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=wheel.parent,
            prefix=".release-manifest-",
            delete=False,
        ) as stream:
            temporary_manifest = Path(stream.name)
            stream.write(manifest)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.mkdir(output)
        except FileExistsError:
            _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
        except OSError:
            _fail("TRITRACK_RELEASE_OUTPUT")
        _link_file(wheel, output / wheel.name)
        _link_file(sdist, output / sdist.name)
        _fsync_directory(output)
        _verify_published_archive(output / wheel.name, expected_artifacts["wheel"])
        _verify_published_archive(output / sdist.name, expected_artifacts["sdist"])
        _link_file(temporary_manifest, output / "release-manifest.json")
        _fsync_directory(output)
        _fsync_directory(output.parent)
    finally:
        if temporary_manifest is not None:
            try:
                temporary_manifest.unlink(missing_ok=True)
            except OSError:
                pass


def _assert_source_identity(source: Path) -> tuple[str, str]:
    encoded = _read_regular(source / ".tritrack-project.json", _POLICY_LIMIT)
    try:
        identity = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")
    expected = {
        "schemaVersion": "tritrack.project-identity/v1",
        "projectId": "tritrack-editing-assistant",
        "projectKind": "public-engine",
        "maintainerSkill": "tritrack-editing-assistant-maintainer",
        "lane": "OSS",
    }
    if identity != expected:
        _fail("TRITRACK_RELEASE_SOURCE_IDENTITY")

    try:
        configuration = tomllib.loads(
            _read_regular(source / "pyproject.toml", _POLICY_LIMIT).decode("utf-8")
        )
        project = configuration["project"]
        project_name = project["name"]
        version = project["version"]
    except (UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    if project_name != "tritrack-editing-assistant" or not isinstance(version, str):
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    init_bytes = _read_regular(
        source / "src" / "tritrack_editing_assistant" / "__init__.py",
        _POLICY_LIMIT,
    )
    match = re.fullmatch(
        rb'"""TriTrack Editing Assistant public package\."""\n\n__version__ = "([^"\r\n]+)"\n',
        init_bytes,
    )
    if match is None or match.group(1).decode("utf-8", "strict") != version:
        _fail("TRITRACK_RELEASE_PROJECT_METADATA")
    return project_name, version


def _assert_git_toplevel(source: Path) -> None:
    try:
        top = Path(
            _run_git(source, "rev-parse", "--show-toplevel").decode("utf-8", "strict").strip()
        ).resolve()
    except (UnicodeDecodeError, OSError):
        _fail("TRITRACK_RELEASE_GIT_FAILED")
    if top != source:
        _fail("TRITRACK_RELEASE_GIT_TOPLEVEL")


def _snapshot_inventory(
    archive: tarfile.TarFile,
    max_file: int,
    max_total: int,
) -> tuple[list[tuple[str, int, bytes]], str]:
    files: list[tuple[str, int, bytes]] = []
    seen: set[str] = set()
    total = 0
    for member in archive.getmembers():
        name = _safe_member_name(member.name)
        if name in seen:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        seen.add(name)
        if member.isdir():
            continue
        if not member.isreg():
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        if member.size > max_file:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        total += member.size
        if total > max_total:
            _fail("TRITRACK_RELEASE_SOURCE_LIMIT")
        stream = archive.extractfile(member)
        if stream is None:
            _fail("TRITRACK_RELEASE_SNAPSHOT")
        with stream:
            encoded = _bounded_archive_read(stream, member.size, max_file)
        mode = 0o755 if member.mode & 0o111 else 0o644
        files.append((name, mode, encoded))
    inventory = hashlib.sha256()
    for name, mode, encoded in sorted(files):
        content_sha = hashlib.sha256(encoded).hexdigest()
        for value in (name, f"100{mode:o}"[-6:], str(len(encoded)), content_sha):
            inventory.update(value.encode("utf-8"))
            inventory.update(b"\0")
        inventory.update(b"\n")
    return files, inventory.hexdigest()


def _write_snapshot_file(root: Path, name: str, mode: int, encoded: bytes) -> None:
    path = root.joinpath(*PurePosixPath(name).parts)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            mode,
        )
        try:
            view = memoryview(encoded)
            while view:
                written = os.write(descriptor, view)
                if written < 1:
                    _fail("TRITRACK_RELEASE_SNAPSHOT")
                view = view[written:]
        finally:
            os.close(descriptor)
        os.chmod(path, mode, follow_symlinks=False)
    except ReleaseGateError:
        raise
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")


def _materialize_snapshot(
    source: Path,
    destination: Path,
    inventory: SourceInventory,
    policy: Mapping[str, object],
) -> None:
    try:
        os.mkdir(destination)
    except OSError:
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    archive_path = destination.parent / f".{destination.name}.tar"
    _run_command(
        [
            "git",
            "archive",
            "--format=tar",
            "--output",
            os.fspath(archive_path),
            inventory.commit,
        ],
        cwd=source,
        env=_safe_environment(),
        timeout=120,
    )
    try:
        with tarfile.open(archive_path, mode="r:") as archive:
            files, digest = _snapshot_inventory(
                archive,
                _positive_limit(policy, "sourceMaxFileBytes"),
                _positive_limit(policy, "sourceMaxTotalBytes"),
            )
        if len(files) != inventory.count or digest != inventory.sha256:
            _fail("TRITRACK_RELEASE_SNAPSHOT_MISMATCH")
        for name, mode, encoded in files:
            _write_snapshot_file(destination, name, mode, encoded)
    except ReleaseGateError:
        raise
    except (OSError, tarfile.TarError):
        _fail("TRITRACK_RELEASE_SNAPSHOT")
    finally:
        try:
            archive_path.unlink(missing_ok=True)
        except OSError:
            pass


def _canonical_manifest(manifest: Mapping[str, object]) -> bytes:
    return (
        json.dumps(
            manifest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )


def run_release_gate(source: Path, output: Path) -> dict[str, object]:
    """Run the complete local release-readiness gate and publish manifest last."""

    try:
        source = source.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_SOURCE")
    if not source.is_dir():
        _fail("TRITRACK_RELEASE_SOURCE")
    _assert_git_toplevel(source)
    project_name, version = _assert_source_identity(source)
    inventory = inventory_tracked_source(source)
    policy = _load_policy(source)
    if output.exists() or output.is_symlink():
        _fail("TRITRACK_RELEASE_OUTPUT_EXISTS")
    try:
        output_parent = output.parent.resolve(strict=True)
    except OSError:
        _fail("TRITRACK_RELEASE_OUTPUT")
    output = output_parent / output.name
    epoch = _build_epoch(policy)
    if _run_git(source, "rev-parse", "HEAD").strip().decode("ascii") != inventory.commit:
        _fail("TRITRACK_RELEASE_SOURCE_CHANGED")

    with tempfile.TemporaryDirectory(
        dir=output.parent, prefix=".tritrack-release-staging-"
    ) as temporary:
        staging = Path(temporary)
        snapshot_one = staging / "snapshot-one"
        snapshot_two = staging / "snapshot-two"
        _materialize_snapshot(source, snapshot_one, inventory, policy)
        _materialize_snapshot(source, snapshot_two, inventory, policy)
        wheel_one, sdist_one = build_distributions(
            snapshot_one, staging / "dist-one", epoch=epoch
        )
        wheel_two, sdist_two = build_distributions(
            snapshot_two, staging / "dist-two", epoch=epoch
        )
        identities = {
            _wheel_project_identity(wheel_one),
            _wheel_project_identity(wheel_two),
        }
        if identities != {(project_name, version)}:
            _fail("TRITRACK_RELEASE_WHEEL_IDENTITY")
        if wheel_one.name != wheel_two.name or sdist_one.name != sdist_two.name:
            _fail("TRITRACK_RELEASE_BUILD_OUTPUT")
        wheel_inspection = inspect_wheel(wheel_one, policy)
        second_wheel_inspection = inspect_wheel(wheel_two, policy)
        sdist_inspection = inspect_sdist(sdist_one, policy)
        second_sdist_inspection = inspect_sdist(sdist_two, policy)
        if wheel_inspection != second_wheel_inspection:
            _fail("TRITRACK_RELEASE_WHEEL_REPRODUCIBILITY")
        if (
            sdist_inspection.member_inventory_sha256
            != second_sdist_inspection.member_inventory_sha256
        ):
            _fail("TRITRACK_RELEASE_SDIST_REPRODUCIBILITY")
        fresh_install_smoke(wheel_one, staging / "fresh-install")
        context = ReleaseContext(
            project_name=project_name,
            version=version,
            commit=inventory.commit,
            source_inventory=inventory,
            toolchain=_installed_tool_versions(),
            python_version=platform.python_version(),
            implementation=platform.python_implementation(),
            system=platform.system(),
            machine=platform.machine(),
            wheel=wheel_inspection,
            sdist=sdist_inspection,
        )
        manifest = build_release_manifest(context)
        publish_release(
            output,
            wheel_one,
            sdist_one,
            _canonical_manifest(manifest),
        )
    return manifest
--- END FILE scripts/release_gate_core.py ---

--- BEGIN FILE scripts/capture_basic_title_binding.py ---
#!/usr/bin/env python3
"""Capture a public-safe Basic Title binding from invented FCPXML."""

from __future__ import annotations

import argparse
import json
import os
import stat
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from pathlib import Path

from tritrack_editing_assistant.contracts import validate_contract
from tritrack_editing_assistant.doctor import load_profile
from tritrack_editing_assistant.process import require_absent_output

FORBIDDEN_TEXT = (
    "Artlist LT",
    "江城知音体",
    "Transcription Template",
    "/" + "Users" + "/",
    "/" + "Volumes" + "/HoneyPot/",
)
STYLE_ATTRIBUTES = ("alignment", "font", "fontColor", "fontFace", "fontSize")
ALLOWED_DOCTYPE = "<!DOCTYPE fcpxml>"
MAX_CAPTURE_XML_BYTES = 16 * 1024 * 1024
MAX_BINDING_BYTES = 1024 * 1024


def _read_regular_bytes(path: Path, *, limit: int, code: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ValueError(code) from error
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or not (0 < before.st_size <= limit):
            raise ValueError(code)
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        encoded = b"".join(chunks)
        after = os.fstat(descriptor)
        if (
            len(encoded) != before.st_size
            or len(encoded) > limit
            or (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            )
            != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            )
        ):
            raise ValueError(code)
        return encoded
    except OSError as error:
        raise ValueError(code) from error
    finally:
        os.close(descriptor)


def _read_public_xml(path: Path) -> str:
    data = _read_regular_bytes(
        path,
        limit=MAX_CAPTURE_XML_BYTES,
        code="TRITRACK_TITLE_BINDING_INVALID_XML",
    )
    if b"\x00" in data:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML") from error
    without_allowed_doctype = text.replace(ALLOWED_DOCTYPE, "", 1)
    if (
        "<!DOCTYPE" in without_allowed_doctype
        or "<!ENTITY" in text
        or text.count(ALLOWED_DOCTYPE) > 1
    ):
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML")
    if any(value in text for value in FORBIDDEN_TEXT):
        raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")
    return text


def _parameter_value(value: str) -> str | int | float | bool:
    try:
        number = float(value)
    except ValueError:
        return value
    return int(number) if number.is_integer() else number


def capture_binding(source: Path) -> dict[str, object]:
    """Extract only the referenced Basic Title effect and style attributes."""

    text = _read_public_xml(source)
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID_XML") from error

    for element in root.iter():
        source_value = element.attrib.get("src")
        if source_value:
            raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

    effects = {
        effect.attrib.get("id"): effect
        for effect in root.findall("./resources/effect")
        if effect.attrib.get("name") == "Basic Title"
    }
    titles = [
        title for title in root.iter("title") if title.attrib.get("ref") in effects
    ]
    if len(titles) != 1:
        raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")
    effect = effects[titles[0].attrib["ref"]]
    uid = effect.attrib.get("uid")
    if not uid or not uid.endswith("Basic Title.moti"):
        raise ValueError("TRITRACK_TITLE_BINDING_BASIC_TITLE_REQUIRED")

    style_elements = titles[0].findall("./text-style-def/text-style")
    if len(style_elements) != 1:
        raise ValueError("TRITRACK_TITLE_BINDING_STYLE_REQUIRED")
    style = style_elements[0]
    parameters = [
        {"name": name, "value": _parameter_value(style.attrib[name])}
        for name in STYLE_ATTRIBUTES
        if name in style.attrib
    ]
    binding: dict[str, object] = {
        "schemaVersion": "tritrack.title-binding/v1",
        "bindingId": "basic-title-v1",
        "effectName": "Basic Title",
        "effectUid": uid,
        "parameters": parameters,
    }
    validate_contract("title-binding-v1", binding)
    return binding


def render_basic_title_fcpxml(binding: Mapping[str, object], *, text: str) -> str:
    """Render a minimal, public-safe NDF project from a reviewed binding."""

    validate_contract("title-binding-v1", dict(binding))
    if not text.strip() or "\n" in text or "\r" in text:
        raise ValueError("TRITRACK_TITLE_BINDING_TEXT_REQUIRED")
    if any(value in text for value in FORBIDDEN_TEXT):
        raise ValueError("TRITRACK_TITLE_BINDING_FORBIDDEN")

    profile = load_profile("uhd-2997-ndf-fcpxml-1.14")
    style_values = {
        str(parameter["name"]): str(parameter["value"])
        for parameter in binding["parameters"]  # type: ignore[index]
    }
    missing_styles = set(STYLE_ATTRIBUTES) - style_values.keys()
    if missing_styles:
        raise ValueError("TRITRACK_TITLE_BINDING_STYLE_REQUIRED")

    root = ET.Element("fcpxml", {"version": str(profile["fcpxmlVersion"])})
    resources_element = ET.SubElement(root, "resources")
    ET.SubElement(
        resources_element,
        "format",
        {
            "id": "r1",
            "name": "FFVideoFormat3840x2160p2997",
            "frameDuration": str(profile["frameDuration"]),
            "width": str(profile["width"]),
            "height": str(profile["height"]),
            "colorSpace": str(profile["colorSpace"]),
        },
    )
    ET.SubElement(
        resources_element,
        "effect",
        {
            "id": "r2",
            "name": str(binding["effectName"]),
            "uid": str(binding["effectUid"]),
        },
    )

    event = ET.SubElement(root, "event", {"name": "TriTrack Public Evidence"})
    project = ET.SubElement(
        event, "project", {"name": "TriTrack Basic Title Roundtrip"}
    )
    sequence = ET.SubElement(
        project,
        "sequence",
        {
            "format": "r1",
            "duration": "180180/30000s",
            "tcStart": "0s",
            "tcFormat": str(profile["timecodeFormat"]),
            "audioLayout": "stereo",
            "audioRate": f"{int(profile['audioRate']) // 1000}k",
        },
    )
    spine = ET.SubElement(sequence, "spine")
    ET.SubElement(
        spine,
        "gap",
        {
            "name": "Gap",
            "offset": "0s",
            "start": "0s",
            "duration": "90090/30000s",
        },
    )
    title = ET.SubElement(
        spine,
        "title",
        {
            "ref": "r2",
            "offset": "90090/30000s",
            "name": f"{text} - Basic Title",
            "start": "0s",
            "duration": "90090/30000s",
        },
    )
    text_element = ET.SubElement(title, "text")
    text_style = ET.SubElement(text_element, "text-style", {"ref": "ts1"})
    text_style.text = text
    text_style_definition = ET.SubElement(title, "text-style-def", {"id": "ts1"})
    ET.SubElement(
        text_style_definition,
        "text-style",
        {attribute: style_values[attribute] for attribute in STYLE_ATTRIBUTES},
    )

    ET.indent(root, space="    ")
    body = ET.tostring(root, encoding="unicode", short_empty_elements=True)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{ALLOWED_DOCTYPE}\n{body}\n'


def _write_exclusive(output: Path, encoded: bytes) -> None:
    destination = require_absent_output(output)
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def write_binding(source: Path, output: Path) -> dict[str, object]:
    binding = capture_binding(source)
    encoded = (json.dumps(binding, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _write_exclusive(output, encoded)
    return binding


def write_rendered_fcpxml(binding_path: Path, output: Path, text: str) -> None:
    try:
        binding = json.loads(
            _read_regular_bytes(
                binding_path,
                limit=MAX_BINDING_BYTES,
                code="TRITRACK_TITLE_BINDING_INVALID",
            ).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("TRITRACK_TITLE_BINDING_INVALID") from error
    rendered = render_basic_title_fcpxml(binding, text=text)
    _write_exclusive(output, rendered.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--binding", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--text")
    arguments = parser.parse_args()
    if arguments.input is not None:
        if arguments.text is not None:
            parser.error("--text is only valid with --binding")
        write_binding(arguments.input, arguments.output)
    else:
        if arguments.text is None:
            parser.error("--text is required with --binding")
        write_rendered_fcpxml(arguments.binding, arguments.output, arguments.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
--- END FILE scripts/capture_basic_title_binding.py ---

--- BEGIN FILE tests/test_maintainer_boundary.py ---
"""Task 4.5 tests for the public-maintainer project boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = (
    ROOT / ".agents" / "skills" / "tritrack-editing-assistant-maintainer"
)
VALIDATOR = SKILL_ROOT / "scripts" / "check_project_identity.py"
PUBLIC_GOVERNANCE = (
    ROOT / "AGENTS.md",
    ROOT / "STATUS.md",
    ROOT / "PRODUCT-WISHES.md",
    ROOT / "docs" / "ROADMAP.md",
    ROOT / "docs" / "TOOLING.md",
    SKILL_ROOT / "SKILL.md",
)


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )


class MaintainerBoundaryTest(unittest.TestCase):
    def test_public_project_identity_is_accepted(self) -> None:
        result = run_validator(ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "lane": "OSS",
                "ok": True,
                "projectId": "tritrack-editing-assistant",
                "projectKind": "public-engine",
            },
        )

    def test_missing_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run_validator(Path(temporary))
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISSING", result.stderr)

    def test_private_project_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".tritrack-project.json").write_text(
                json.dumps(
                    {
                        "schemaVersion": "tritrack.project-identity/v1",
                        "projectId": "some-private-production",
                        "projectKind": "private-production",
                        "maintainerSkill": "some-private-skill",
                        "lane": "MAIN",
                    }
                ),
                encoding="utf-8",
            )
            result = run_validator(root)
        self.assertEqual(result.returncode, 2)
        self.assertIn("TRITRACK_PROJECT_IDENTITY_MISMATCH", result.stderr)

    def test_public_governance_is_self_contained_and_public_safe(self) -> None:
        forbidden = (
            "/" + "Users" + "/",
            "TriTrack-" + "worktrees",
            "TriTrack-" + "Subtitle-" + "Studio",
            "Codex for " + "Open Source",
            "six " + "months",
            "六" + "個月",
        )
        for path in PUBLIC_GOVERNANCE:
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, f"{path}: leaked {token!r}")

    def test_maintainer_and_end_user_skills_are_distinct(self) -> None:
        maintainer = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        end_user_root = ROOT / "skills" / "tritrack-editing-assistant"
        end_user = (end_user_root / "SKILL.md").read_text(encoding="utf-8")
        metadata = (end_user_root / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: tritrack-editing-assistant-maintainer", maintainer)
        self.assertIn("$tritrack-editing-assistant-maintainer OSS 開工", maintainer)
        self.assertIn("name: tritrack-editing-assistant\n", end_user)
        self.assertIn("$tritrack-editing-assistant", metadata)
        self.assertIn('display_name: "TriTrack Editing Assistant"', metadata)

        for command in (
            "tritrack run --help",
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
            "tritrack validate --help",
            "tritrack validate contract --help",
            "tritrack validate fcpxml --help",
            "tritrack validate paper --help",
            "tritrack validate run --help",
        ):
            self.assertIn(command, end_user)
        for required in (
            "text-revision human gate",
            "paper-edit human gate",
            "takes: []",
            "Questions",
            "Selections",
            "transport, not authority",
            "absent output directory",
            "Keep media",
            "strict aligned transcript",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(required, end_user)

        lowered = end_user.lower()
        forbidden = (
            "tritrack-editing-assistant-maintainer",
            "task 10",
            "standing grant",
            "branch",
            "release",
            "tester",
            "moonie",
            "subtitle studio",
            "/" + "users" + "/",
            "api_key",
            "credential",
            "provider",
            "upload",
            "run_workflow",
            ".py",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)

    def test_public_status_records_task_11_and_schedules_task_12(self) -> None:
        status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        decision = (ROOT / "docs" / "TASK-10-DECISION.md").read_text(
            encoding="utf-8"
        )
        verification = (ROOT / "docs" / "TASK-10-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        task_11_verification = (ROOT / "docs" / "TASK-11-VERIFICATION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Tasks 1–11", status)
        self.assertIn("Task 6.5", status)
        self.assertLess(status.index("Task 6.5"), status.index("Task 7"))
        self.assertLess(status.index("Task 7"), status.index("Task 8"))
        self.assertLess(status.index("Task 8"), status.index("Task 9"))
        self.assertLess(status.index("Task 9"), status.index("Task 10"))
        self.assertLess(status.index("Task 10"), status.index("Task 11"))
        self.assertLess(status.index("Task 11"), status.index("Task 12"))
        self.assertIn("Task 10", roadmap)
        self.assertLess(roadmap.index("Task 10"), roadmap.index("Task 11"))
        for authority in (
            "tritrack run prepare --help",
            "tritrack run align --help",
            "tritrack run finish --help",
            "tritrack run status --help",
        ):
            self.assertIn(authority, tooling)
        for text in (status, roadmap, tooling, readme, verification):
            self.assertIn("Task 10", text)
        self.assertIn("Selected option: A", decision)
        self.assertIn("immutable", verification)
        self.assertIn("story-cut.fcpxml", verification)
        self.assertIn("tritrack-editing-assistant", verification)
        self.assertIn("no network", verification)
        self.assertIn("Task 11", status)
        self.assertIn("Task 11", roadmap)
        self.assertIn("Task 12", status)
        self.assertIn("Task 12", roadmap)
        self.assertIn("ce562e995b63f3f1a29989de3e1ef202da27b5f2", task_11_verification)
        for scope in (
            "contract",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        ):
            self.assertIn(scope, task_11_verification)
        self.assertNotIn("`validate` and `run` remain planned", status)
        self.assertNotIn("`validate` remains planned", status)
        self.assertNotIn("`tritrack run` | planned", readme)

    def test_task_6_5_handoff_is_public_safe_and_bounded(self) -> None:
        handoff = (ROOT / "docs" / "TASK-6.5-HANDOFF.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "$tritrack-editing-assistant-maintainer OSS 開工，執行 Task 6.5",
            handoff,
        )
        self.assertIn("242e8b5406e92049ce60c654c3c8fca11be4b596", handoff)
        self.assertIn("codex/task6-5-public-demo-readiness", handoff)
        self.assertIn("RED", handoff)
        self.assertIn("GREEN", handoff)
        self.assertIn("application submission", handoff)
        self.assertNotIn("/" + "Users" + "/", handoff)

    def test_tooling_pins_the_perpetual_final_cut_identity(self) -> None:
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        self.assertIn("/Applications/Final Cut Pro.app", tooling)
        self.assertIn("com.apple.FinalCut", tooling)
        self.assertIn("com.apple.FinalCutApp", tooling)
        self.assertIn("default file association", tooling)

    def test_working_cut_claims_distinguish_transcript_from_editor_text(self) -> None:
        for path in (
            ROOT / "README.md",
            ROOT / "docs" / "TASK-9-VERIFICATION.md",
        ):
            text = path.read_text(encoding="utf-8")
            self.assertIn("transcript-text-free", text, str(path))
            self.assertNotRegex(
                text,
                r"(?<!transcript-)text-free\s+(?:working cut|`working-cut)",
                str(path),
            )

        organizer = (
            ROOT / "src" / "tritrack_editing_assistant" / "organizer.py"
        ).read_text(encoding="utf-8")
        self.assertIn("transcript-text-free working cut", organizer)

    def test_authorization_is_a_capability_scoped_standing_grant(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        for text in (agents, skill):
            self.assertIn("capability-scoped standing grant", text)
            self.assertIn("same target, visibility, scope, and risk", text)
            self.assertIn("until the producer revokes it", text)
            self.assertIn("Do not request it again", text)
            self.assertNotIn("without explicit producer", text)

        roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("standing-authorization model", roadmap)
        self.assertNotIn("Each requires an explicit producer-approved gate", roadmap)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_maintainer_boundary.py ---

--- BEGIN FILE tests/test_packaging.py ---
"""Task 11 distribution policy and reproducibility tests."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path

import jsonschema

from scripts import release_gate_core

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "release" / "package-policy-v1.json"
MANIFEST_SCHEMA_PATH = ROOT / "release" / "release-manifest-v1.schema.json"
SDIST_ROOT = "tritrack_editing_assistant-0.1.0a0/"


def normalized_inventory(entries: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for name in sorted(entries):
        encoded = entries[name]
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(encoded)).encode("ascii"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(encoded).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


class PackagingPolicyTest(unittest.TestCase):
    def test_01_python_and_tool_constraints_are_exact(self) -> None:
        configuration = tomllib.loads((ROOT / "pyproject.toml").read_text())
        self.assertEqual(
            configuration["build-system"]["requires"],
            ["setuptools==84.0.0"],
        )
        self.assertEqual(configuration["project"]["requires-python"], ">=3.12,<3.14")
        self.assertEqual(
            configuration["project"]["optional-dependencies"]["dev"],
            ["build==1.5.0", "ruff==0.16.2", "wheel==0.48.0"],
        )
        classifiers = configuration["project"]["classifiers"]
        versions = [
            value
            for value in classifiers
            if value.startswith("Programming Language :: Python :: 3.")
        ]
        self.assertEqual(
            versions,
            [
                "Programming Language :: Python :: 3.12",
                "Programming Language :: Python :: 3.13",
            ],
        )
        self.assertEqual(
            (ROOT / "requirements" / "ci-constraints.txt")
            .read_text(encoding="utf-8")
            .splitlines(),
            [
                "build==1.5.0",
                "packaging==26.3",
                "pip==26.2",
                "pyproject-hooks==1.2.0",
                "ruff==0.16.2",
                "setuptools==84.0.0",
                "wheel==0.48.0",
            ],
        )

    def test_02_package_policy_and_manifest_schema_are_closed(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        self.assertEqual(policy["schemaVersion"], "tritrack.package-policy/v1")
        self.assertEqual(
            set(policy),
            {"schemaVersion", "build", "limits", "source", "wheel", "sdist"},
        )
        self.assertEqual(policy["build"], {"sourceDateEpoch": 1704067200})
        for required in (
            "docs/TASK-11-VERIFICATION.md",
            "scripts/release_gate.py",
            "scripts/release_gate_core.py",
        ):
            self.assertIn(required, policy["sdist"]["expectedMembers"])
        schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        sample = {
            "schemaVersion": "tritrack.release-manifest/v1",
            "project": {
                "name": "tritrack-editing-assistant",
                "version": "0.1.0a0",
                "commit": "a" * 40,
            },
            "sourceInventory": {"count": 1, "sha256": "b" * 64},
            "toolchain": {
                "python": "3.13.15",
                "implementation": "CPython",
                "pip": "26.2",
                "build": "1.5.0",
                "setuptools": "84.0.0",
                "wheel": "0.48.0",
            },
            "platform": {"system": "Darwin", "machine": "arm64"},
            "artifacts": {
                kind: {
                    "sha256": value * 64,
                    "sizeBytes": 1,
                    "memberCount": 1,
                    "memberInventorySha256": value * 64,
                }
                for kind, value in (("wheel", "c"), ("sdist", "d"))
            },
            "reproducibility": {
                "wheelBytesMatch": True,
                "sdistMembersMatch": True,
            },
            "gates": {
                name: "pass"
                for name in (
                    "sourceIdentity",
                    "sourcePrivacy",
                    "wheelArchive",
                    "sdistArchive",
                    "freshInstall",
                )
            },
            "nonClaims": ["no-tag", "no-package-publication"],
        }
        jsonschema.validate(sample, schema)
        sample["unexpected"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(sample, schema)

    def test_03_distribution_members_are_explicit_and_reproducible(self) -> None:
        policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distributions: list[tuple[Path, Path]] = []
            for label in ("first", "second"):
                source = root / label / "source"
                shutil.copytree(
                    ROOT,
                    source,
                    ignore=shutil.ignore_patterns(
                        ".git",
                        ".release-evidence",
                        "__pycache__",
                        "*.egg-info",
                        "build",
                        "dist",
                    ),
                )
                output = root / label / "dist"
                output.mkdir()
                environment = os.environ.copy()
                environment["SOURCE_DATE_EPOCH"] = "1704067200"
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "build",
                        "--no-isolation",
                        "--outdir",
                        str(output),
                    ],
                    cwd=source,
                    env=environment,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                wheel = next(output.glob("*.whl"))
                sdist = next(output.glob("*.tar.gz"))
                distributions.append((wheel, sdist))

            first_wheel, first_sdist = distributions[0]
            second_wheel, second_sdist = distributions[1]
            self.assertEqual(first_wheel.read_bytes(), second_wheel.read_bytes())

            with zipfile.ZipFile(first_wheel) as archive:
                wheel_entries = {
                    member.filename: archive.read(member)
                    for member in archive.infolist()
                    if not member.is_dir()
                }
            self.assertEqual(
                set(wheel_entries),
                set(policy["wheel"]["expectedMembers"]),
            )
            for forbidden in ("tests/", "docs/", "skills/", "scripts/", ".github/"):
                self.assertFalse(any(forbidden in name for name in wheel_entries))

            sdist_inventories: list[str] = []
            for sdist in (first_sdist, second_sdist):
                with tarfile.open(sdist, mode="r:gz") as archive:
                    entries = {
                        member.name.removeprefix(SDIST_ROOT): archive.extractfile(
                            member
                        ).read()
                        for member in archive.getmembers()
                        if member.isfile()
                    }
                self.assertTrue(all(name and not name.startswith("/") for name in entries))
                self.assertEqual(
                    set(entries),
                    set(policy["sdist"]["expectedMembers"]),
                )
                sdist_inventories.append(normalized_inventory(entries))
                for forbidden in (
                    ".agents/",
                    "docs/reviews/",
                    "docs/superpowers/plans/",
                    "tests/test_maintainer_boundary.py",
                ):
                    self.assertFalse(any(name.startswith(forbidden) for name in entries))
            self.assertEqual(sdist_inventories[0], sdist_inventories[1])

    def test_04_historical_records_have_no_machine_specific_home(self) -> None:
        for relative in (
            "docs/reviews/task-10-closeout-packet-2026-08-17.md",
            "docs/superpowers/plans/2026-08-17-task-10-immutable-run.md",
        ):
            release_gate_core.scan_public_bytes((ROOT / relative).read_bytes())


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_packaging.py ---

--- BEGIN FILE tests/test_release_ci.py ---
"""Task 11 public release-grade CI configuration contract."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "ci.yml"
CHECKOUT_SHA = "3d3c42e5aac5ba805825da76410c181273ba90b1"
SETUP_PYTHON_SHA = "5fda3b95a4ea91299a34e894583c3862153e4b97"


class ReleaseCiContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.lowered = cls.workflow.casefold()

    def test_exact_fixed_four_cell_matrix(self) -> None:
        cells = re.findall(
            r"- os: (ubuntu-24\.04|macos-26)\n"
            r'\s+python-version: "(3\.12|3\.13)"\n'
            r"\s+architecture: (x64|arm64)",
            self.workflow,
        )
        self.assertEqual(
            cells,
            [
                ("ubuntu-24.04", "3.12", "x64"),
                ("ubuntu-24.04", "3.13", "x64"),
                ("macos-26", "3.12", "arm64"),
                ("macos-26", "3.13", "arm64"),
            ],
        )
        self.assertIn("runs-on: ${{ matrix.os }}", self.workflow)
        self.assertIn("fail-fast: false", self.workflow)
        self.assertNotIn("-latest", self.workflow)

    def test_matrix_runs_complete_build_and_installed_smoke(self) -> None:
        required = (
            "python -m pip install --constraint requirements/ci-constraints.txt pip setuptools",
            "python -m pip install --constraint requirements/ci-constraints.txt -e '.[dev]'",
            "python -m unittest discover -s tests -v",
            "python -m compileall -q src tests examples scripts",
            "python -m build --wheel --no-isolation",
            "python -m venv",
            "pip check",
            "components --json",
            "validate --help",
            "validate contract --help",
            "validate fcpxml --help",
            "validate paper --help",
            "validate run --help",
        )
        for command in required:
            self.assertIn(command, self.workflow)

    def test_quality_and_release_jobs_are_single_fixed_cells(self) -> None:
        self.assertRegex(
            self.workflow,
            r"quality:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
        )
        self.assertRegex(
            self.workflow,
            r"release-gate:\n(?:.|\n)*?runs-on: ubuntu-24\.04",
        )
        self.assertGreaterEqual(self.workflow.count('python-version: "3.13"'), 4)
        self.assertIn("ruff check src tests examples scripts", self.workflow)
        self.assertIn(
            "python -m unittest tests.test_maintainer_boundary tests.test_packaging tests.test_release_ci -v",
            self.workflow,
        )
        self.assertIn(
            "python scripts/release_gate.py --source . --output .release-evidence/ci",
            self.workflow,
        )

    def test_actions_permissions_and_negative_authority_are_closed(self) -> None:
        uses = re.findall(r"uses:\s*([^\s#]+)", self.workflow)
        self.assertTrue(uses)
        self.assertEqual(
            set(uses),
            {
                f"actions/checkout@{CHECKOUT_SHA}",
                f"actions/setup-python@{SETUP_PYTHON_SHA}",
            },
        )
        for action in uses:
            self.assertRegex(action, r"@[0-9a-f]{40}$")
        self.assertRegex(
            self.workflow,
            r"permissions:\n  contents: read\n\njobs:",
        )
        self.assertNotIn("cache:", self.workflow)
        for forbidden in (
            "upload-artifact",
            "download-artifact",
            "gh release",
            "git tag",
            "twine",
            "pypi",
            "sigstore",
            "attest",
            "sbom",
            "secrets.",
            "xmllint",
            "xcodebuild",
        ):
            self.assertNotIn(forbidden, self.lowered)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_release_ci.py ---

--- BEGIN FILE tests/test_release_gate.py ---
"""Task 11 maintainer release-gate tests."""

from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import os
import stat
import subprocess
import tarfile
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock

from scripts import release_gate_core


def _policy(*, wheel: list[str] | None = None, sdist: list[str] | None = None):
    return {
        "schemaVersion": "tritrack.package-policy/v1",
        "build": {"sourceDateEpoch": 1704067200},
        "limits": {
            "sourceMaxFiles": 32,
            "sourceMaxFileBytes": 4096,
            "sourceMaxTotalBytes": 32768,
            "archiveMaxBytes": 65536,
            "archiveMaxMembers": 32,
            "memberMaxBytes": 4096,
            "expandedMaxBytes": 32768,
        },
        "source": {
            "allowedFakeHomeUsers": ["editor", "example", "fake", "test"],
            "allowedFakeSecretValues": [
                "example",
                "fake",
                "placeholder",
                "redacted",
                "secret",
                "test",
            ],
            "forbiddenSuffixes": [".mov", ".xlsx"],
        },
        "wheel": {"expectedMembers": wheel or ["demo.py"]},
        "sdist": {
            "root": "demo-1.0/",
            "expectedMembers": sdist or ["README.md"],
        },
    }


def _run(*argv: str, cwd: Path, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        argv,
        cwd=cwd,
        input=input_bytes,
        check=True,
        capture_output=True,
    ).stdout


def _make_repo(root: Path, files: dict[str, bytes] | None = None) -> None:
    (root / "release").mkdir(parents=True)
    (root / "release" / "package-policy-v1.json").write_text(
        json.dumps(_policy()), encoding="utf-8"
    )
    for name, encoded in (files or {"public.txt": b"public\n"}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(encoded)
    _run("git", "init", "-q", cwd=root)
    _run("git", "config", "user.name", "Invented Tester", cwd=root)
    _run("git", "config", "user.email", "test@example.invalid", cwd=root)
    _run("git", "add", ".", cwd=root)
    _run("git", "commit", "-qm", "fixture", cwd=root)


def _zip(path: Path, entries: list[tuple[zipfile.ZipInfo | str, bytes]]) -> None:
    with (
        zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive,
        warnings.catch_warnings(),
    ):
        warnings.simplefilter("ignore", UserWarning)
        for name, encoded in entries:
            archive.writestr(name, encoded)


def _tar(
    path: Path,
    entries: list[tuple[tarfile.TarInfo | str, bytes]],
) -> None:
    with tarfile.open(path, "w:gz") as archive:
        for name, encoded in entries:
            member = name if isinstance(name, tarfile.TarInfo) else tarfile.TarInfo(name)
            if member.isreg():
                member.size = len(encoded)
            archive.addfile(member, io.BytesIO(encoded) if member.isreg() else None)


class SourceGateTest(unittest.TestCase):
    def test_package_policy_owns_a_fixed_build_epoch(self) -> None:
        self.assertEqual(release_gate_core._build_epoch(_policy()), 1704067200)
        for invalid in (True, 0, -1, "1704067200"):
            policy = _policy()
            policy["build"]["sourceDateEpoch"] = invalid
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core._build_epoch(policy)

    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_gate_descriptor_readers_reject_special_files_before_blocking(self) -> None:
        selected = Path("invented-special-file")
        readers = (
            lambda: release_gate_core._read_regular(selected, 1),
            lambda: release_gate_core._read_archive_bytes(selected, _policy()),
            lambda: release_gate_core._verify_published_archive(
                selected, (1, "a" * 64)
            ),
        )

        for reader in readers:
            observed: list[int] = []

            def reject_special(_path, flags, *_args, observed=observed):
                observed.append(flags)
                raise OSError("invented special file")

            with self.subTest(reader=reader), mock.patch.object(
                release_gate_core.os, "open", side_effect=reject_special
            ), self.assertRaises(release_gate_core.ReleaseGateError):
                reader()
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_NONBLOCK)

    def test_clean_stage_zero_regular_source_is_inventory_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            first = release_gate_core.inventory_tracked_source(root)
            second = release_gate_core.inventory_tracked_source(root)
        self.assertEqual(first, second)
        self.assertEqual(first.count, 2)
        self.assertEqual(len(first.sha256), 64)
        self.assertGreater(first.total_bytes, 0)

    def test_dirty_source_and_tracked_links_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_DIRTY$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            (root / "public.txt").unlink()
            os.symlink("target", root / "public.txt")
            _run("git", "add", "public.txt", cwd=root)
            _run("git", "commit", "-qm", "link", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_submodule_unmerged_and_late_change_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            head = _run("git", "rev-parse", "HEAD", cwd=root).strip().decode()
            _run(
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{head},nested",
                cwd=root,
            )
            _run("git", "commit", "-qm", "gitlink", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_MODE$"
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            original = release_gate_core._read_regular
            changed = False

            def mutate(path: Path, limit: int) -> bytes:
                nonlocal changed
                encoded = original(path, limit)
                if path.name == "public.txt" and not changed:
                    changed = True
                    path.write_text("late change\n", encoding="utf-8")
                return encoded

            with (
                mock.patch.object(
                    release_gate_core, "_read_regular", side_effect=mutate
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_SOURCE_CHANGED$",
                ),
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_source_bounds_and_forbidden_suffix_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"clip.mov": b"invented"})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_SOURCE_FORBIDDEN_TYPE$",
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root, {"large.txt": b"x" * 5000})
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_SOURCE_LIMIT$"
            ):
                release_gate_core.inventory_tracked_source(root)

    def test_privacy_scanner_redacts_paths_and_credentials(self) -> None:
        private_home = b"/" + b"Users" + b"/real-person/project"
        credential = b"API" + b"_KEY=" + b"A" * 36
        bare_token = b"gh" + b"p_" + b"A" * 36
        private_key = b"-----BEGIN " + b"PRIVATE KEY-----"
        for encoded in (private_home, credential, bare_token, private_key):
            with self.subTest(kind=hashlib.sha256(encoded).hexdigest()[:8]):
                with self.assertRaises(release_gate_core.ReleaseGateError) as caught:
                    release_gate_core.scan_public_bytes(encoded)
                message = str(caught.exception)
                self.assertRegex(message, r"^TRITRACK_RELEASE_[A-Z_]+$")
                self.assertNotIn(encoded.decode(), message)

        for public in (
            b"/Users/editor/invented",
            b"/home/example/demo",
            b"password=placeholder",
            b"secret=test",
        ):
            release_gate_core.scan_public_bytes(public)

    def test_policy_allowlists_and_nested_keys_cannot_drift_from_scanner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            policy_path = root / "release" / "package-policy-v1.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["source"]["allowedFakeHomeUsers"].append("real-person")
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            _run("git", "add", ".", cwd=root)
            _run("git", "commit", "-qm", "policy drift", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core.inventory_tracked_source(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _make_repo(root)
            policy_path = root / "release" / "package-policy-v1.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["wheel"]["unexpected"] = True
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            _run("git", "add", ".", cwd=root)
            _run("git", "commit", "-qm", "policy extension", cwd=root)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_POLICY_INVALID$",
            ):
                release_gate_core.inventory_tracked_source(root)


class ArchiveGateTest(unittest.TestCase):
    def test_safe_wheel_and_sdist_return_only_counts_and_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            _zip(wheel, [("demo.py", b"print('public')\n")])
            _tar(sdist, [("demo-1.0/README.md", b"public\n")])
            wheel_result = release_gate_core.inspect_wheel(wheel, _policy())
            sdist_result = release_gate_core.inspect_sdist(sdist, _policy())
        for result in (wheel_result, sdist_result):
            self.assertEqual(result.member_count, 1)
            self.assertEqual(len(result.sha256), 64)
            self.assertEqual(len(result.member_inventory_sha256), 64)
            self.assertNotIn("demo", repr(result))

    def test_zip_rejects_traversal_duplicates_casefold_links_and_encryption(self) -> None:
        fixtures: list[tuple[list[tuple[zipfile.ZipInfo | str, bytes]], dict]] = []
        fixtures.append(([("../demo.py", b"x")], _policy(wheel=["../demo.py"])))
        fixtures.append(
            (
                [("demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["demo.py"]),
            )
        )
        fixtures.append(
            (
                [("Demo.py", b"x"), ("demo.py", b"y")],
                _policy(wheel=["Demo.py", "demo.py"]),
            )
        )
        link = zipfile.ZipInfo("demo.py")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        fixtures.append(([(link, b"target")], _policy()))

        for entries, policy in fixtures:
            with self.subTest(size=len(entries)), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "bad.whl"
                _zip(path, entries)
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_wheel(path, policy)

        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "encrypted.whl"
            _zip(path, [("demo.py", b"x")])
            encoded = bytearray(path.read_bytes())
            local = encoded.find(b"PK\x03\x04")
            central = encoded.find(b"PK\x01\x02")
            encoded[local + 6] |= 1
            encoded[central + 8] |= 1
            path.write_bytes(encoded)
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_ENCRYPTED$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

    def test_tar_rejects_wrong_root_links_and_unexpected_members(self) -> None:
        link = tarfile.TarInfo("demo-1.0/README.md")
        link.type = tarfile.SYMTYPE
        link.linkname = "target"
        fixtures = (
            ([("other/README.md", b"x")], _policy(sdist=["README.md"])),
            ([(link, b"")], _policy()),
            (
                [("demo-1.0/README.md", b"x"), ("demo-1.0/extra", b"x")],
                _policy(),
            ),
        )
        for entries, policy in fixtures:
            with self.subTest(), tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "bad.tar.gz"
                _tar(path, list(entries))
                with self.assertRaises(release_gate_core.ReleaseGateError):
                    release_gate_core.inspect_sdist(path, policy)

    def test_archive_bounds_privacy_and_inventory_mode_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "large.whl"
            _zip(path, [("demo.py", b"x" * 5000)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_ARCHIVE_LIMIT$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            private_home = b"/" + b"home" + b"/real-person/private"
            _zip(path, [("demo.py", private_home)])
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError, "^TRITRACK_RELEASE_PRIVATE_PATH$"
            ):
                release_gate_core.inspect_wheel(path, _policy())

            executable = zipfile.ZipInfo("demo.py")
            executable.create_system = 3
            executable.external_attr = (stat.S_IFREG | 0o755) << 16
            _zip(path, [(executable, b"public\n")])
            first = release_gate_core.inspect_wheel(path, _policy())
            regular = zipfile.ZipInfo("demo.py")
            regular.create_system = 3
            regular.external_attr = (stat.S_IFREG | 0o644) << 16
            _zip(path, [(regular, b"public\n")])
            second = release_gate_core.inspect_wheel(path, _policy())
            self.assertNotEqual(
                first.member_inventory_sha256,
                second.member_inventory_sha256,
            )

    def test_archive_hash_is_bound_to_the_same_bounded_bytes_as_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "demo.whl"
            replacement = root / "replacement.whl"
            _zip(path, [("demo.py", b"public\n")])
            original = path.read_bytes()
            replaced = False

            def replace_after_member_read(_encoded: bytes) -> None:
                nonlocal replaced
                if replaced:
                    return
                replaced = True
                replacement.write_bytes(b"x" * 70000)
                os.replace(replacement, path)

            with mock.patch.object(
                release_gate_core,
                "scan_public_bytes",
                side_effect=replace_after_member_read,
            ):
                result = release_gate_core.inspect_wheel(path, _policy())

            self.assertTrue(replaced)
            self.assertEqual(result.size_bytes, len(original))
            self.assertEqual(result.sha256, hashlib.sha256(original).hexdigest())


class OrchestrationTest(unittest.TestCase):
    def test_command_output_limit_terminates_before_timeout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            command = [
                os.fspath(Path(os.sys.executable)),
                "-c",
                "import os,time; os.write(1,b'x'*65); time.sleep(2)",
            ]
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_COMMAND_LIMIT$",
            ):
                release_gate_core._run_command(
                    command,
                    cwd=root,
                    env={"PATH": os.defpath},
                    timeout=1,
                    output_limit=64,
                )

    def test_build_uses_fixed_epoch_and_exact_local_toolchain(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot"
            snapshot.mkdir()
            output = root / "dist"

            def fake_command(argv, **_kwargs):
                calls.append(tuple(str(value) for value in argv))
                output.mkdir(exist_ok=True)
                (output / "demo-1.0-py3-none-any.whl").write_bytes(b"wheel")
                (output / "demo-1.0.tar.gz").write_bytes(b"sdist")
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_installed_tool_versions",
                    return_value={
                        "pip": "26.2",
                        "build": "1.5.0",
                        "setuptools": "84.0.0",
                        "wheel": "0.48.0",
                    },
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                wheel, sdist = release_gate_core.build_distributions(
                    snapshot, output, epoch=1704067200
                )

        self.assertEqual(wheel.name, "demo-1.0-py3-none-any.whl")
        self.assertEqual(sdist.name, "demo-1.0.tar.gz")
        self.assertEqual(
            calls,
            [
                (
                    os.fspath(Path(os.sys.executable)),
                    "-m",
                    "build",
                    "--no-isolation",
                    "--outdir",
                    os.fspath(output),
                )
            ],
        )

    def test_fresh_install_uses_only_local_wheel_and_smokes_all_help(self) -> None:
        calls: list[tuple[str, ...]] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "tritrack_editing_assistant-0.1.0a0-py3-none-any.whl"
            wheel.write_bytes(b"invented wheel")

            def fake_command(argv, **_kwargs):
                normalized = tuple(str(value) for value in argv)
                calls.append(normalized)
                if normalized[-2:] == ("components", "--json"):
                    return json.dumps(
                        {
                            "schemaVersion": "tritrack.components/v1",
                            "components": [{}] * 11,
                        }
                    ).encode()
                if "importlib.metadata" in " ".join(normalized):
                    return b"tritrack-editing-assistant\t0.1.0a0\n"
                return b""

            with (
                mock.patch.object(
                    release_gate_core,
                    "_wheel_project_identity",
                    return_value=("tritrack-editing-assistant", "0.1.0a0"),
                ),
                mock.patch.object(
                    release_gate_core, "_run_command", side_effect=fake_command
                ),
            ):
                release_gate_core.fresh_install_smoke(wheel, root / "smoke")

        flattened = [" ".join(call) for call in calls]
        install = [
            call
            for call in flattened
            if "pip" in call.split() and "install" in call.split()
        ]
        self.assertTrue(any("pip==26.2" in call for call in install))
        self.assertTrue(any(os.fspath(wheel) in call for call in install))
        self.assertFalse(any("-e" in call.split() for call in install))
        for mode in ("contract", "fcpxml", "paper", "run"):
            self.assertTrue(
                any(f"validate {mode} --help" in call for call in flattened), mode
            )

    def test_manifest_is_closed_deterministic_and_schema_valid(self) -> None:
        inspection = release_gate_core.DistributionInspection(
            sha256="c" * 64,
            size_bytes=10,
            member_count=2,
            member_inventory_sha256="d" * 64,
        )
        context = release_gate_core.ReleaseContext(
            project_name="tritrack-editing-assistant",
            version="0.1.0a0",
            commit="a" * 40,
            source_inventory=release_gate_core.SourceInventory(
                count=3,
                total_bytes=30,
                sha256="b" * 64,
                commit="a" * 40,
            ),
            toolchain={
                "pip": "26.2",
                "build": "1.5.0",
                "setuptools": "84.0.0",
                "wheel": "0.48.0",
            },
            python_version="3.13.15",
            implementation="CPython",
            system="Darwin",
            machine="arm64",
            wheel=inspection,
            sdist=inspection,
        )
        first = release_gate_core.build_release_manifest(context)
        second = release_gate_core.build_release_manifest(context)
        self.assertEqual(first, second)
        self.assertEqual(
            set(first),
            {
                "schemaVersion",
                "project",
                "sourceInventory",
                "toolchain",
                "platform",
                "artifacts",
                "reproducibility",
                "gates",
                "nonClaims",
            },
        )
        serialized = json.dumps(first, sort_keys=True)
        for forbidden in ("path", "time", "duration", "command", "log", "content"):
            self.assertNotIn(forbidden, serialized.casefold())

    def test_pipeline_failure_never_calls_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with (
                mock.patch.object(
                    release_gate_core,
                    "inventory_tracked_source",
                    side_effect=release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_SOURCE_DIRTY"
                    ),
                ),
                mock.patch.object(release_gate_core, "publish_release") as publish,
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.run_release_gate(root, root / "absent")
            publish.assert_not_called()


class PublicationTest(unittest.TestCase):
    @staticmethod
    def manifest(wheel: bytes, sdist: bytes) -> bytes:
        return (
            json.dumps(
                {
                    "artifacts": {
                        "wheel": {
                            "sha256": hashlib.sha256(wheel).hexdigest(),
                            "sizeBytes": len(wheel),
                        },
                        "sdist": {
                            "sha256": hashlib.sha256(sdist).hexdigest(),
                            "sizeBytes": len(sdist),
                        },
                    }
                },
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
            + b"\n"
        )

    def test_artifacts_are_linked_before_manifest_and_existing_output_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            manifest = self.manifest(b"wheel", b"sdist")
            release_gate_core.publish_release(output, wheel, sdist, manifest)
            self.assertEqual((output / wheel.name).read_bytes(), b"wheel")
            self.assertEqual((output / sdist.name).read_bytes(), b"sdist")
            self.assertEqual((output / "release-manifest.json").read_bytes(), manifest)

            sentinel = root / "existing"
            sentinel.mkdir()
            (sentinel / "keep").write_text("untouched", encoding="utf-8")
            with self.assertRaisesRegex(
                release_gate_core.ReleaseGateError,
                "^TRITRACK_RELEASE_OUTPUT_EXISTS$",
            ):
                release_gate_core.publish_release(sentinel, wheel, sdist, manifest)
            self.assertEqual((sentinel / "keep").read_text(), "untouched")

    def test_interruption_before_last_link_leaves_no_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            real_link = os.link
            calls = 0

            def interrupted(source: Path, destination: Path) -> None:
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise release_gate_core.ReleaseGateError(
                        "TRITRACK_RELEASE_INTERRUPTED"
                    )
                real_link(source, destination)

            with (
                mock.patch.object(
                    release_gate_core, "_link_file", side_effect=interrupted
                ),
                self.assertRaises(release_gate_core.ReleaseGateError),
            ):
                release_gate_core.publish_release(
                    output,
                    wheel,
                    sdist,
                    self.manifest(b"wheel", b"sdist"),
                )
            self.assertTrue(output.is_dir())
            self.assertFalse((output / "release-manifest.json").exists())

    def test_late_archive_change_before_manifest_link_fails_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "demo.whl"
            sdist = root / "demo.tar.gz"
            wheel.write_bytes(b"wheel")
            sdist.write_bytes(b"sdist")
            output = root / "candidate"
            real_fsync = release_gate_core._fsync_directory
            calls = 0

            def mutate_after_archive_links(path: Path) -> None:
                nonlocal calls
                calls += 1
                real_fsync(path)
                if calls == 1:
                    wheel.write_bytes(b"changed")

            with (
                mock.patch.object(
                    release_gate_core,
                    "_fsync_directory",
                    side_effect=mutate_after_archive_links,
                ),
                self.assertRaisesRegex(
                    release_gate_core.ReleaseGateError,
                    "^TRITRACK_RELEASE_ARCHIVE_CHANGED$",
                ),
            ):
                release_gate_core.publish_release(
                    output,
                    wheel,
                    sdist,
                    self.manifest(b"wheel", b"sdist"),
                )
            self.assertTrue(output.is_dir())
            self.assertFalse((output / "release-manifest.json").exists())


class ReleaseCliTest(unittest.TestCase):
    def test_cli_success_prints_only_bounded_receipt_facts(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        manifest = {
            "project": {"commit": "a" * 40, "version": "0.1.0a0"},
            "artifacts": {
                "wheel": {"sha256": "b" * 64},
                "sdist": {"sha256": "c" * 64},
            },
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                return_value=manifest,
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", "invented-source", "--output", "invented-output"]
            )
        self.assertEqual(result, 0)
        self.assertEqual(stderr.getvalue(), "")
        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "RELEASE_GATE\tPASS")
        self.assertEqual(len(lines), 6)
        self.assertFalse(any("invented" in line for line in lines))

    def test_cli_usage_and_gate_failures_are_json_codes_only(self) -> None:
        release_gate = importlib.import_module("scripts.release_gate")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = release_gate.main([])
        self.assertEqual(result, 64)
        self.assertEqual(
            json.loads(stderr.getvalue()), {"error": "TRITRACK_RELEASE_USAGE"}
        )

        stderr = io.StringIO()
        private = "/" + "Users" + "/real-person/private"
        with (
            mock.patch.object(
                release_gate.release_gate_core,
                "run_release_gate",
                side_effect=release_gate_core.ReleaseGateError(
                    "TRITRACK_RELEASE_PRIVATE_PATH"
                ),
            ),
            contextlib.redirect_stderr(stderr),
        ):
            result = release_gate.main(
                ["--source", private, "--output", "invented-output"]
            )
        self.assertEqual(result, 1)
        self.assertEqual(
            json.loads(stderr.getvalue()),
            {"error": "TRITRACK_RELEASE_PRIVATE_PATH"},
        )
        self.assertNotIn(private, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_release_gate.py ---

--- BEGIN FILE tests/test_run_workflow.py ---
import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from openpyxl import load_workbook

from tritrack_editing_assistant import (
    align_text,
    doctor,
    emit_fcpxml,
    organizer,
    paper_edit,
    run_workflow,
    story_fcpxml,
    sync_scan,
    transcribe_takes,
)


def sha256(encoded: bytes) -> str:
    return hashlib.sha256(encoded).hexdigest()


def invented_sources() -> list[dict[str, object]]:
    return [
        {
            "camera": "B",
            "mediaId": "B-001.MP4",
            "sha256": "b" * 64,
            "transcribed": False,
        },
        {
            "camera": "A",
            "mediaId": "A-001.MP4",
            "sha256": "a" * 64,
            "transcribed": True,
        },
    ]


def prepared_artifacts() -> dict[str, dict[str, str]]:
    return {
        "transcriptBundle": {
            "fileName": "transcript-bundle.json",
            "sha256": "d" * 64,
        },
        "doctorReceipt": {"fileName": "doctor.json", "sha256": "b" * 64},
        "stringOut": {"fileName": "string-out.fcpxml", "sha256": "e" * 64},
        "syncMap": {"fileName": "sync-map.json", "sha256": "c" * 64},
    }


def prepared_stages() -> list[dict[str, object]]:
    return [
        {
            "name": "emit",
            "inputHashes": {"syncMap": "c" * 64},
            "outputHashes": {"stringOut": "e" * 64},
        },
        {
            "name": "transcribe",
            "inputHashes": {"sourceSet": "2" * 64},
            "outputHashes": {"transcriptBundle": "d" * 64},
        },
        {
            "name": "sync",
            "inputHashes": {"sourceSet": "1" * 64},
            "outputHashes": {"syncMap": "c" * 64},
        },
        {
            "name": "doctor",
            "inputHashes": {"profile": "f" * 64},
            "outputHashes": {"doctorReceipt": "b" * 64},
        },
    ]


def invented_aligned() -> dict[str, object]:
    return {
        "schemaVersion": "tritrack.aligned-transcript/v1",
        "alignmentProfileId": "cue-addressed-v1",
        "sourceBundleSha256": "1" * 64,
        "revisionSha256": "2" * 64,
        "language": "en",
        "takes": [
            {
                "takeId": "A-001.MP4",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented words.",
                        "disposition": "original",
                    }
                ],
            }
        ],
    }


def aligned_bundle_files() -> dict[str, bytes]:
    aligned = (
        json.dumps(invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    return {
        "aligned-transcript.json": aligned,
        "paper-edit.xlsx": b"PK\x03\x04invented-workbook",
    }


def aligned_manifest(files: dict[str, bytes]) -> dict[str, object]:
    artifacts = {
        "alignedTranscript": {
            "fileName": "aligned-transcript.json",
            "sha256": sha256(files["aligned-transcript.json"]),
        },
        "paperWorkbook": {
            "fileName": "paper-edit.xlsx",
            "sha256": sha256(files["paper-edit.xlsx"]),
        },
    }
    return run_workflow.build_manifest(
        run_id="run-001",
        profile_id="uhd-2997-ndf-fcpxml-1.14",
        binding_id="basic-title-v1",
        phase="aligned",
        manifest_chain=["9" * 64],
        sources=invented_sources(),
        stages=[
            {
                "name": "paper",
                "inputHashes": {"alignedTranscript": sha256(files["aligned-transcript.json"])},
                "outputHashes": {"paperWorkbook": sha256(files["paper-edit.xlsx"])},
            },
            {
                "name": "align",
                "inputHashes": {"revision": "8" * 64},
                "outputHashes": {
                    "alignedTranscript": sha256(files["aligned-transcript.json"])
                },
            },
        ],
        artifacts=artifacts,
    )


class RunManifestTest(unittest.TestCase):
    def build(self, **changes) -> dict[str, object]:
        arguments = {
            "run_id": "run-001",
            "profile_id": "uhd-2997-ndf-fcpxml-1.14",
            "binding_id": "basic-title-v1",
            "phase": "prepared",
            "manifest_chain": [],
            "sources": invented_sources(),
            "stages": prepared_stages(),
            "artifacts": prepared_artifacts(),
        }
        arguments.update(changes)
        return run_workflow.build_manifest(**arguments)

    def test_builds_sorted_immutable_canonical_manifest(self) -> None:
        sources = invented_sources()
        stages = prepared_stages()
        artifacts = prepared_artifacts()
        before = copy.deepcopy((sources, stages, artifacts))

        manifest = self.build(sources=sources, stages=stages, artifacts=artifacts)
        first = run_workflow.encode_manifest(manifest)
        second = run_workflow.encode_manifest(copy.deepcopy(manifest))

        self.assertEqual((sources, stages, artifacts), before)
        self.assertEqual(first, second)
        self.assertTrue(first.endswith(b"\n"))
        self.assertEqual(
            [(source["camera"], source["mediaId"]) for source in manifest["sources"]],
            [("A", "A-001.MP4"), ("B", "B-001.MP4")],
        )
        self.assertEqual(
            [stage["name"] for stage in manifest["stages"]],
            ["doctor", "sync", "transcribe", "emit"],
        )
        self.assertNotIn(b"createdAt", first)
        self.assertNotIn(b"status", first)
        self.assertNotIn(b"/Users/", first)

    def test_rejects_unsafe_duplicate_and_phase_drift(self) -> None:
        duplicate = invented_sources()
        duplicate.append(
            {
                "camera": "B",
                "mediaId": "A-001.MP4",
                "sha256": "9" * 64,
                "transcribed": False,
            }
        )
        invalid = [
            {"run_id": "../run"},
            {"phase": "running"},
            {"manifest_chain": ["1" * 64]},
            {"sources": duplicate},
        ]
        for changes in invalid:
            with (
                self.subTest(changes=changes),
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_MANIFEST_INVALID"
                ),
            ):
                self.build(**changes)

    def test_rejects_foreign_artifact_filename_stage_and_hash(self) -> None:
        artifacts = prepared_artifacts()
        artifacts["syncMap"]["fileName"] = "foreign.json"
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(artifacts=artifacts)

        stages = prepared_stages()
        stages[0]["name"] = "validate"
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(stages=stages)

    def test_rejects_extra_artifact_and_stage_facts(self) -> None:
        artifacts = prepared_artifacts()
        artifacts["foreign"] = {
            "fileName": "foreign.json",
            "sha256": "9" * 64,
        }
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(artifacts=artifacts)

        stages = prepared_stages()
        stages.append(
            {
                "name": "foreign",
                "action": "foreign",
                "outputHashes": {"foreign": "9" * 64},
            }
        )
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(stages=stages)

        stages = prepared_stages()
        stages[0]["outputHashes"]["stringOut"] = "9" * 64
        with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_MANIFEST_INVALID"):
            self.build(stages=stages)

    def test_loads_complete_bundle_and_returns_sanitized_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "aligned-run"
            root.mkdir()
            files = aligned_bundle_files()
            for name, encoded in files.items():
                (root / name).write_bytes(encoded)
            manifest = aligned_manifest(files)
            manifest_bytes = run_workflow.encode_manifest(manifest)
            (root / "run-manifest.json").write_bytes(manifest_bytes)

            bundle = run_workflow.load_bundle(root, expected_phase="aligned")
            summary = run_workflow.summarize_bundle(bundle)

            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.run-summary/v1",
                    "runId": "run-001",
                    "phase": "aligned",
                    "nextAction": "edit-paper-workbook",
                    "stages": ["align", "paper"],
                    "artifacts": {
                        "alignedTranscript": sha256(
                            files["aligned-transcript.json"]
                        ),
                        "paperWorkbook": sha256(files["paper-edit.xlsx"]),
                    },
                },
            )
            self.assertNotIn(str(root), json.dumps(summary))
            self.assertNotIn("Invented words", json.dumps(summary))

    def test_load_rejects_noncanonical_changed_unlisted_and_incomplete(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            files = aligned_bundle_files()
            for name, encoded in files.items():
                (root / name).write_bytes(encoded)
            manifest = aligned_manifest(files)
            (root / "run-manifest.json").write_text(
                json.dumps(manifest, separators=(",", ":")), encoding="utf-8"
            )
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_MANIFEST_NONCANONICAL"
            ):
                run_workflow.load_bundle(root)

            (root / "run-manifest.json").write_bytes(
                run_workflow.encode_manifest(manifest)
            )
            (root / "paper-edit.xlsx").write_bytes(b"changed")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
            ):
                run_workflow.load_bundle(root)

            (root / "paper-edit.xlsx").write_bytes(files["paper-edit.xlsx"])
            (root / "foreign.txt").write_text("foreign", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "TRITRACK_RUN_BUNDLE_INVALID"):
                run_workflow.load_bundle(root)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "incomplete"
            root.mkdir()
            (root / "aligned-transcript.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
            ):
                run_workflow.load_bundle(root)


class BundlePublicationTest(unittest.TestCase):
    def builder(self, files: dict[str, bytes], calls: list[Path] | None = None):
        def build(staging: Path) -> dict[str, object]:
            if calls is not None:
                calls.append(staging)
            for name, encoded in files.items():
                (staging / name).write_bytes(encoded)
            return aligned_manifest(files)

        return build

    def test_publishes_manifest_last_and_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = aligned_bundle_files()
            linked: list[str] = []
            real_link = os.link

            def recording_link(source, destination):
                linked.append(Path(destination).name)
                return real_link(source, destination)

            with mock.patch.object(
                run_workflow.os, "link", side_effect=recording_link
            ):
                first = run_workflow.publish_bundle(
                    root / "first", self.builder(files)
                )
            second = run_workflow.publish_bundle(root / "second", self.builder(files))

            self.assertEqual(linked[-1], "run-manifest.json")
            self.assertEqual(first.manifest, second.manifest)
            self.assertEqual(
                (root / "first" / "run-manifest.json").read_bytes(),
                (root / "second" / "run-manifest.json").read_bytes(),
            )
            self.assertEqual(list(root.glob(".*.staging-*")), [])

    def test_rejects_missing_existing_and_dangling_outputs_before_builder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = aligned_bundle_files()
            calls: list[Path] = []
            builder = self.builder(files, calls)
            existing = root / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                run_workflow.publish_bundle(existing, builder)

            dangling = root / "dangling"
            dangling.symlink_to(root / "missing")
            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                run_workflow.publish_bundle(dangling, builder)

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_OUTPUT_PARENT_MISSING"
            ):
                run_workflow.publish_bundle(root / "missing" / "run", builder)
            self.assertEqual(calls, [])

    def test_builder_and_link_failures_clean_only_owned_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            caller_input = root / "caller-input"
            caller_input.write_text("keep", encoding="utf-8")

            def failing_builder(staging: Path):
                (staging / "partial").write_text("partial", encoding="utf-8")
                raise RuntimeError("invented failure")

            with self.assertRaisesRegex(RuntimeError, "invented failure"):
                run_workflow.publish_bundle(root / "builder-failed", failing_builder)
            self.assertFalse((root / "builder-failed").exists())
            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(root.glob(".*.staging-*")), [])

            real_link = os.link
            link_count = 0

            def failing_link(source, destination):
                nonlocal link_count
                link_count += 1
                if link_count == 2:
                    raise OSError("invented link failure")
                return real_link(source, destination)

            with (
                mock.patch.object(
                    run_workflow.os, "link", side_effect=failing_link
                ),
                self.assertRaisesRegex(OSError, "invented link failure"),
            ):
                run_workflow.publish_bundle(
                    root / "link-failed", self.builder(aligned_bundle_files())
                )
            self.assertFalse((root / "link-failed").exists())
            self.assertEqual(caller_input.read_text(encoding="utf-8"), "keep")

    def test_directory_reservation_race_preserves_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "race"
            real_mkdir = os.mkdir

            def racing_mkdir(path, mode=0o777, *, dir_fd=None):
                if Path(path) == output:
                    real_mkdir(path, mode)
                    (output / "winner").write_text("keep", encoding="utf-8")
                    raise FileExistsError
                return real_mkdir(path, mode, dir_fd=dir_fd)

            with (
                mock.patch.object(
                    run_workflow.os, "mkdir", side_effect=racing_mkdir
                ),
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                run_workflow.publish_bundle(
                    output, self.builder(aligned_bundle_files())
                )
            self.assertEqual((output / "winner").read_text(encoding="utf-8"), "keep")


class PrepareAlignTransitionTest(unittest.TestCase):
    def write_sources(
        self, root: Path
    ) -> tuple[list[sync_scan.MediaSource], list[sync_scan.MediaSource], Path]:
        source_a = root / "A-001.MP4"
        source_b = root / "B-001.MP4"
        model = root / "ggml-model.bin"
        source_a.write_bytes(b"invented-source-a")
        source_b.write_bytes(b"invented-source-b")
        model.write_bytes(b"invented-model")
        return (
            [sync_scan.MediaSource(source_a.name, source_a)],
            [sync_scan.MediaSource(source_b.name, source_b)],
            model,
        )

    @staticmethod
    def sync_payload() -> dict[str, object]:
        return {
            "schemaVersion": "tritrack.sync-map/v1",
            "profileId": "uhd-2997-ndf-fcpxml-1.14",
            "pairs": [
                {
                    "pairId": "pair-001",
                    "mediaA": "A-001.MP4",
                    "mediaB": "B-001.MP4",
                    "offsetBFromASeconds": 1.0,
                    "confidence": 20.0,
                    "overlapSeconds": 8.0,
                    "audioMaster": "A",
                    "durationASeconds": 10.0,
                    "durationBSeconds": 8.0,
                    "startedAt": None,
                }
            ],
            "singleA": [],
            "singleB": [],
            "warnings": [],
        }

    def fakes(self, calls: list[str], *, supported: bool = True):
        def fake_doctor(output: Path, **_arguments):
            calls.append("doctor")
            receipt = {
                "schemaVersion": "tritrack.doctor-receipt/v1",
                "profileId": "uhd-2997-ndf-fcpxml-1.14",
                "titleBindingId": "basic-title-v1",
                "supported": supported,
                "checks": [],
                "remediation": [] if supported else ["Invented remediation"],
            }
            output.write_text(
                json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return receipt

        def fake_sync(_camera_a, _camera_b, *, output_path, **_arguments):
            calls.append("sync")
            payload = self.sync_payload()
            output_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return payload

        def fake_transcribe(media_paths, *, model_path, language, output_path, **_):
            calls.append("transcribe")
            source = Path(media_paths[0])
            bundle = {
                "schemaVersion": "tritrack.transcript-bundle/v1",
                "profileId": "whisper-cpp-cpu-no-fallback-v1",
                "language": language,
                "modelSha256": sha256(Path(model_path).read_bytes()),
                "engine": {
                    "name": "whisper-cli",
                    "version": "whisper.cpp version: invented",
                },
                "takes": [
                    {
                        "takeId": source.name,
                        "sourceSha256": sha256(source.read_bytes()),
                        "status": "completed",
                        "cues": [
                            {
                                "cueId": "cue-000001",
                                "startMs": 0,
                                "endMs": 500,
                                "text": "Invented words.",
                            }
                        ],
                    }
                ],
            }
            output_path.write_text(
                transcribe_takes.encode_transcript_bundle(bundle), encoding="utf-8"
            )
            return bundle

        def fake_emit(
            camera_a,
            camera_b,
            *,
            sync_map_path,
            profile_id,
            binding_id,
            metadata,
            output_path,
        ):
            calls.append("emit")
            sources = [
                {
                    "camera": "A",
                    "media_id": camera_a[0].media_id,
                    "path": camera_a[0].path,
                    "duration_seconds": 10.0,
                },
                {
                    "camera": "B",
                    "media_id": camera_b[0].media_id,
                    "path": camera_b[0].path,
                    "duration_seconds": 8.0,
                },
            ]
            rendered = emit_fcpxml.render_fcpxml(
                json.loads(Path(sync_map_path).read_text(encoding="utf-8")),
                sources,
                profile_id=profile_id,
                binding_id=binding_id,
                metadata=metadata,
            )
            output_path.write_text(rendered, encoding="utf-8")
            return rendered

        return fake_doctor, fake_sync, fake_transcribe, fake_emit

    def prepare(
        self, root: Path, *, calls: list[str] | None = None
    ) -> tuple[run_workflow.LoadedRunBundle, list[sync_scan.MediaSource], Path]:
        camera_a, camera_b, model = self.write_sources(root)
        observed_calls = [] if calls is None else calls
        fake_doctor, fake_sync, fake_transcribe, fake_emit = self.fakes(
            observed_calls
        )
        output = root / "prepared-run"
        with (
            mock.patch.object(doctor, "write_receipt", side_effect=fake_doctor),
            mock.patch.object(
                sync_scan, "synchronize_and_publish", side_effect=fake_sync
            ),
            mock.patch.object(
                transcribe_takes,
                "transcribe_and_publish",
                side_effect=fake_transcribe,
            ),
            mock.patch.object(
                emit_fcpxml, "emit_and_publish", side_effect=fake_emit
            ),
        ):
            summary = run_workflow.prepare_run(
                camera_a,
                camera_b,
                [camera_a[0].path],
                model_path=model,
                language="en",
                profile_id="uhd-2997-ndf-fcpxml-1.14",
                binding_id="basic-title-v1",
                metadata=emit_fcpxml.ProjectMetadata("Interview", "String-out"),
                run_id="run-001",
                output_dir=output,
            )
        self.assertEqual(summary["phase"], "prepared")
        return run_workflow.load_bundle(output), [*camera_a, *camera_b], model

    def test_prepare_calls_existing_engines_in_order_and_binds_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            calls: list[str] = []
            bundle, sources, model = self.prepare(root, calls=calls)

            self.assertEqual(calls, ["doctor", "sync", "transcribe", "emit"])
            self.assertEqual(bundle.manifest["phase"], "prepared")
            self.assertEqual(
                [source["mediaId"] for source in bundle.manifest["sources"]],
                ["A-001.MP4", "B-001.MP4"],
            )
            self.assertEqual(
                [source["transcribed"] for source in bundle.manifest["sources"]],
                [True, False],
            )
            for source in sources:
                manifest_source = next(
                    item
                    for item in bundle.manifest["sources"]
                    if item["mediaId"] == source.media_id
                )
                self.assertEqual(
                    manifest_source["sha256"], sha256(source.path.read_bytes())
                )
            encoded = bundle.manifest_bytes
            self.assertNotIn(str(root).encode(), encoded)
            self.assertNotIn(model.name.encode(), encoded)
            self.assertNotIn(b"Invented words", encoded)

    def test_prepare_rejects_unsupported_subset_duplicate_and_late_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, model = self.write_sources(root)
            calls: list[str] = []
            fakes = self.fakes(calls, supported=False)
            with (
                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
                mock.patch.object(
                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
                ) as sync,
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED"
                ),
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-unsupported",
                    output_dir=root / "unsupported",
                )
            sync.assert_not_called()
            self.assertFalse((root / "unsupported").exists())

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_TRANSCRIBE_SOURCE_INVALID"
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [root / "foreign.MP4"],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-foreign",
                    output_dir=root / "foreign",
                )

            duplicate_path = root / "other" / "A-001.MP4"
            duplicate_path.parent.mkdir()
            duplicate_path.write_bytes(b"duplicate")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_SOURCE_ID_DUPLICATE"
            ):
                run_workflow.prepare_run(
                    camera_a,
                    [sync_scan.MediaSource("A-001.MP4", duplicate_path)],
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-duplicate",
                    output_dir=root / "duplicate",
                )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a, camera_b, model = self.write_sources(root)
            calls: list[str] = []
            fakes = list(self.fakes(calls))
            original_emit = fakes[3]

            def changing_emit(*args, **kwargs):
                rendered = original_emit(*args, **kwargs)
                model.write_bytes(b"changed-model")
                return rendered

            with (
                mock.patch.object(doctor, "write_receipt", side_effect=fakes[0]),
                mock.patch.object(
                    sync_scan, "synchronize_and_publish", side_effect=fakes[1]
                ),
                mock.patch.object(
                    transcribe_takes,
                    "transcribe_and_publish",
                    side_effect=fakes[2],
                ),
                mock.patch.object(
                    emit_fcpxml, "emit_and_publish", side_effect=changing_emit
                ),
                self.assertRaisesRegex(ValueError, "TRITRACK_RUN_INPUT_CHANGED"),
            ):
                run_workflow.prepare_run(
                    camera_a,
                    camera_b,
                    [camera_a[0].path],
                    model_path=model,
                    language="en",
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    run_id="run-changed",
                    output_dir=root / "changed",
                )
            self.assertFalse((root / "changed").exists())

    def test_align_accepts_no_change_revision_and_chains_prepared(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, _, _ = self.prepare(root)
            transcript = prepared.artifacts["transcriptBundle"]
            revision = {
                "schemaVersion": "tritrack.text-revision/v1",
                "sourceBundleSha256": transcript.sha256,
                "language": "en",
                "takes": [],
            }
            revision_path = root / "revision.json"
            revision_bytes = (
                json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True)
                + "\n"
            ).encode("utf-8")
            revision_path.write_bytes(revision_bytes)
            output = root / "aligned-run"

            with (
                mock.patch.object(
                    align_text,
                    "align_and_publish",
                    wraps=align_text.align_and_publish,
                ) as align,
                mock.patch.object(
                    paper_edit,
                    "export_workbook",
                    wraps=paper_edit.export_workbook,
                ) as paper,
            ):
                summary = run_workflow.align_run(
                    prepared.root, revision_path, output_dir=output
                )

            self.assertEqual([align.call_count, paper.call_count], [1, 1])
            self.assertEqual(summary["phase"], "aligned")
            aligned_bundle = run_workflow.load_bundle(output)
            self.assertEqual(
                aligned_bundle.manifest["manifestChain"],
                [prepared.manifest_sha256],
            )
            self.assertEqual(
                aligned_bundle.manifest["sources"], prepared.manifest["sources"]
            )
            aligned_payload = json.loads(
                aligned_bundle.artifacts["alignedTranscript"].encoded
            )
            self.assertTrue(
                all(
                    cue["disposition"] == "original"
                    for take in aligned_payload["takes"]
                    for cue in take["cues"]
                )
            )
            self.assertEqual(revision_path.read_bytes(), revision_bytes)

    def test_align_validates_prepared_bundle_before_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            incomplete = root / "incomplete"
            incomplete.mkdir()
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_BUNDLE_INCOMPLETE"
            ):
                run_workflow.align_run(
                    incomplete,
                    root / "missing-revision.json",
                    output_dir=root / "aligned",
                )


class FinishStatusTransitionTest(PrepareAlignTransitionTest):
    def prepare_and_align(
        self, root: Path
    ) -> tuple[
        run_workflow.LoadedRunBundle,
        run_workflow.LoadedRunBundle,
        list[sync_scan.MediaSource],
    ]:
        prepared, sources, _ = self.prepare(root)
        transcript = prepared.artifacts["transcriptBundle"]
        revision = {
            "schemaVersion": "tritrack.text-revision/v1",
            "sourceBundleSha256": transcript.sha256,
            "language": "en",
            "takes": [],
        }
        revision_path = root / "revision.json"
        revision_path.write_text(
            json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        aligned_path = root / "aligned-run"
        run_workflow.align_run(
            prepared.root, revision_path, output_dir=aligned_path
        )
        return prepared, run_workflow.load_bundle(aligned_path), sources

    @staticmethod
    def edit_workbook(aligned: run_workflow.LoadedRunBundle, output: Path) -> None:
        output.write_bytes(aligned.artifacts["paperWorkbook"].encoded)
        workbook = load_workbook(output, data_only=False)
        workbook["Questions"].append(["question-001", "What happened?", 1])
        workbook["Selections"].append(
            [
                "ANSWER",
                "answer-001",
                "question-001",
                1,
                "A-001.MP4",
                "cue-000001",
                "cue-000001",
                None,
                None,
            ]
        )
        workbook.save(output)

    @staticmethod
    def probe(source: sync_scan.MediaSource) -> dict[str, object]:
        durations = {"A-001.MP4": 10.0, "B-001.MP4": 8.0}
        return {
            "duration_seconds": durations[source.media_id],
            "compatibility": {
                "videoStreamCount": 1,
                "audioStreamCount": 1,
                "width": 3840,
                "height": 2160,
                "frameRate": "30000/1001",
                "colorSpace": "bt709",
                "colorTransfer": "bt709",
                "colorPrimaries": "bt709",
                "sampleRate": "48000",
                "channels": 2,
            },
        }

    def finish(
        self,
        root: Path,
        prepared: run_workflow.LoadedRunBundle,
        aligned: run_workflow.LoadedRunBundle,
        sources: list[sync_scan.MediaSource],
        *,
        calls: list[str] | None = None,
    ) -> tuple[dict[str, object], Path]:
        workbook = root / "edited-paper.xlsx"
        self.edit_workbook(aligned, workbook)
        output = root / "finished-run"
        camera_a = [source for source in sources if source.media_id.startswith("A-")]
        camera_b = [source for source in sources if source.media_id.startswith("B-")]
        observed = [] if calls is None else calls
        real_apply = paper_edit.apply_workbook
        real_organize = organizer.organize_and_publish
        real_story = story_fcpxml.emit_story_and_publish

        def apply(*args, **kwargs):
            observed.append("paper")
            return real_apply(*args, **kwargs)

        def organize(*args, **kwargs):
            observed.append("organize")
            return real_organize(*args, **kwargs)

        def story(*args, **kwargs):
            observed.append("emit")
            return real_story(*args, **kwargs)

        with (
            mock.patch.object(paper_edit, "apply_workbook", side_effect=apply),
            mock.patch.object(
                organizer, "organize_and_publish", side_effect=organize
            ),
            mock.patch.object(
                story_fcpxml, "emit_story_and_publish", side_effect=story
            ),
            mock.patch.object(sync_scan, "probe_media", side_effect=self.probe),
        ):
            summary = run_workflow.finish_run(
                prepared.root,
                aligned.root,
                workbook,
                camera_a,
                camera_b,
                metadata=emit_fcpxml.ProjectMetadata("Interview", "Story cut"),
                output_dir=output,
            )
        return summary, output

    def test_finish_applies_organizes_emits_and_chains_exact_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            calls: list[str] = []

            summary, output = self.finish(
                root, prepared, aligned, sources, calls=calls
            )

            self.assertEqual(calls, ["paper", "organize", "emit"])
            self.assertEqual(summary["phase"], "finished")
            finished = run_workflow.load_bundle(output, expected_phase="finished")
            self.assertEqual(
                finished.manifest["manifestChain"],
                [prepared.manifest_sha256, aligned.manifest_sha256],
            )
            self.assertEqual(
                finished.manifest["sources"], prepared.manifest["sources"]
            )
            self.assertEqual(
                set(finished.artifacts), {"grouping", "workingCut", "storyCut"}
            )
            self.assertNotIn("What happened?", json.dumps(summary))
            self.assertNotIn(str(root), json.dumps(summary))

    def test_finish_rejects_chain_source_and_existing_output_before_engines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            workbook = root / "edited.xlsx"
            self.edit_workbook(aligned, workbook)
            camera_a = [sources[0]]
            camera_b = [sources[1]]
            existing = root / "existing"
            existing.mkdir()
            with (
                mock.patch.object(paper_edit, "apply_workbook") as apply,
                self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"),
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    camera_a,
                    camera_b,
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=existing,
                )
            apply.assert_not_called()

            sources[0].path.write_bytes(b"changed-source")
            with (
                mock.patch.object(paper_edit, "apply_workbook") as apply,
                self.assertRaisesRegex(
                    ValueError, "TRITRACK_RUN_SOURCE_MISMATCH"
                ),
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    camera_a,
                    camera_b,
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=root / "source-mismatch",
                )
            apply.assert_not_called()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            changed = copy.deepcopy(aligned.manifest)
            changed["manifestChain"] = ["8" * 64]
            (aligned.root / "run-manifest.json").write_bytes(
                run_workflow.encode_manifest(changed)
            )
            workbook = root / "edited.xlsx"
            self.edit_workbook(aligned, workbook)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_CHAIN_MISMATCH"
            ):
                run_workflow.finish_run(
                    prepared.root,
                    aligned.root,
                    workbook,
                    [sources[0]],
                    [sources[1]],
                    metadata=emit_fcpxml.ProjectMetadata("Event", "Project"),
                    output_dir=root / "bad-chain",
                )

    def test_status_is_read_only_and_rejects_changed_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared, aligned, sources = self.prepare_and_align(root)
            _, output = self.finish(root, prepared, aligned, sources)
            before = {
                path.name: path.read_bytes() for path in output.iterdir()
            }

            summary = run_workflow.status_run(output)

            self.assertEqual(summary["phase"], "finished")
            self.assertEqual(summary["nextAction"], "complete")
            self.assertEqual(
                before,
                {path.name: path.read_bytes() for path in output.iterdir()},
            )
            self.assertNotIn("What happened?", json.dumps(summary))

            (output / "story-cut.fcpxml").write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_RUN_ARTIFACT_HASH_MISMATCH"
            ):
                run_workflow.status_run(output)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_run_workflow.py ---

--- BEGIN FILE tests/test_cli.py ---
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from tests.test_contracts import VALID_CONTRACTS
from tritrack_editing_assistant import cli, run_workflow

ROOT = Path(__file__).resolve().parents[1]


def write_alignment_inputs(root: Path) -> tuple[Path, Path]:
    transcript = {
        "schemaVersion": "tritrack.transcript-bundle/v1",
        "profileId": "whisper-cpp-cpu-no-fallback-v1",
        "language": "en",
        "modelSha256": "3" * 64,
        "engine": {
            "name": "whisper-cli",
            "version": "whisper.cpp version: invented-cli",
        },
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "status": "completed",
                "cues": [
                    {
                        "cueId": "cue-000001",
                        "startMs": 0,
                        "endMs": 500,
                        "text": "Invented private source text.",
                    }
                ],
            }
        ],
    }
    transcript_path = root / "transcript.json"
    transcript_path.write_text(
        json.dumps(transcript, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    revision = {
        "schemaVersion": "tritrack.text-revision/v1",
        "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
        "language": "en",
        "takes": [
            {
                "takeId": "Invented.wav",
                "sourceSha256": "a" * 64,
                "revisions": [
                    {
                        "cueId": "cue-000001",
                        "text": "Invented private revised text.",
                    }
                ],
            }
        ],
    }
    revision_path = root / "revision.json"
    revision_path.write_text(
        json.dumps(revision, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return transcript_path, revision_path


def write_hybrid_receipt(root: Path, transcript_path: Path) -> Path:
    receipt = {
        "schemaVersion": "tritrack.provider-receipt/v1",
        "provider": "gemini",
        "operation": "audio-transcription",
        "sourceBundleSha256": hashlib.sha256(transcript_path.read_bytes()).hexdigest(),
        "takeId": "Invented.wav",
        "requestedModel": "gemini-invented-exact",
        "observedModel": "gemini-invented-exact",
        "audioSha256": "a" * 64,
        "requestStatus": "completed",
        "responseStatus": 200,
        "upload": {
            "status": "completed",
            "serverFileIdSha256": "e" * 64,
        },
        "serverFileDeletion": {
            "attempted": True,
            "confirmed": True,
            "statusCode": 200,
        },
    }
    receipt_path = root / "receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt_path


class CliSmokeTest(unittest.TestCase):
    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_output_hash_rejects_special_files_before_blocking(self) -> None:
        observed: list[int] = []

        def reject_special(_path, flags, *_args):
            observed.append(flags)
            raise OSError("invented special file")

        with mock.patch.object(
            cli.os, "open", side_effect=reject_special
        ), self.assertRaises(OSError):
            cli._output_sha256(Path("invented-special-file"))
        self.assertEqual(len(observed), 1)
        self.assertTrue(observed[0] & os.O_NONBLOCK)

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        completed = self.run_cli_unchecked(*args)
        completed.check_returncode()
        return completed

    def run_cli_unchecked(
        self,
        *args: str,
        environment_overrides: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        if environment_overrides is not None:
            environment.update(environment_overrides)
        return subprocess.run(
            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_version(self):
        completed = self.run_cli("--version")
        self.assertEqual(completed.stdout.strip(), "tritrack 0.1.0a0")

    def test_version_and_component_list(self):
        completed = self.run_cli("components", "--json")
        payload = json.loads(completed.stdout)

        self.assertEqual(payload["schemaVersion"], "tritrack.components/v1")
        self.assertEqual(len(payload["components"]), 11)
        self.assertEqual(
            [component["sourceComponent"] for component in payload["components"]],
            [
                "sync_scan.py",
                "emit_fcpxml.py",
                "transcribe_takes.py",
                "string_out.py",
                "hallucination.py",
                "organizer.py",
                "paper_edit.py",
                "align_text.py",
                "gemini_hybrid.py",
                "gemini_transcribe.mjs",
                "multicam-sync",
            ],
        )
        self.assertEqual(
            {
                component["sourceComponent"]: component["status"]
                for component in payload["components"]
            },
            {
                "sync_scan.py": "implemented",
                "emit_fcpxml.py": "implemented",
                "transcribe_takes.py": "implemented",
                "string_out.py": "implemented",
                "hallucination.py": "implemented",
                "organizer.py": "implemented",
                "paper_edit.py": "implemented",
                "align_text.py": "implemented",
                "gemini_hybrid.py": "implemented",
                "gemini_transcribe.mjs": "planned",
                "multicam-sync": "implemented",
            },
        )

    def test_help_exposes_the_complete_scaffold(self):
        completed = self.run_cli("--help")
        for command in (
            "components",
            "doctor",
            "sync",
            "transcribe",
            "align",
            "hybrid",
            "emit",
            "validate",
            "organize",
            "paper",
            "run",
        ):
            self.assertIn(command, completed.stdout)

    def test_sync_help_exposes_only_the_public_task_5_boundary(self):
        completed = self.run_cli("sync", "--help")
        for option in ("--camera-a", "--camera-b", "--profile", "--output"):
            self.assertIn(option, completed.stdout)

    def test_emit_help_exposes_only_the_public_task_6_boundary(self):
        completed = self.run_cli("emit", "--help")
        for option in (
            "--camera-a",
            "--camera-b",
            "--sync-map",
            "--profile",
            "--binding",
            "--event-name",
            "--project-name",
            "--output",
        ):
            self.assertIn(option, completed.stdout)

    def test_transcribe_help_exposes_only_the_local_task_7_boundary(self):
        completed = self.run_cli("transcribe", "--help")
        for option in ("--media", "--model", "--language", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "prompt", "fallback"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_align_help_exposes_only_the_local_cue_addressed_boundary(self):
        completed = self.run_cli("align", "--help")
        for option in ("--transcript", "--revision", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "prompt", "model", "retime"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_run_help_exposes_exact_immutable_local_transitions(self):
        run = self.run_cli("run", "--help")
        for command in ("prepare", "align", "finish", "status"):
            self.assertIn(command, run.stdout)

        prepare = self.run_cli("run", "prepare", "--help")
        for option in (
            "--camera-a",
            "--camera-b",
            "--transcribe-media",
            "--model",
            "--language",
            "--profile",
            "--binding",
            "--event-name",
            "--project-name",
            "--run-id",
            "--output",
            "--json",
        ):
            self.assertIn(option, prepare.stdout)

        align = self.run_cli("run", "align", "--help")
        for option in ("--prepared", "--revision", "--output", "--json"):
            self.assertIn(option, align.stdout)

        finish = self.run_cli("run", "finish", "--help")
        for option in (
            "--prepared",
            "--aligned",
            "--workbook",
            "--camera-a",
            "--camera-b",
            "--event-name",
            "--project-name",
            "--output",
            "--json",
        ):
            self.assertIn(option, finish.stdout)

        status = self.run_cli("run", "status", "--help")
        for option in ("--run", "--json"):
            self.assertIn(option, status.stdout)
        for completed in (run, prepare, align, finish, status):
            for excluded in (
                "provider",
                "upload",
                "credential",
                "overwrite",
                "resume",
                "release",
            ):
                self.assertNotIn(excluded, completed.stdout.lower())

    def test_run_handlers_forward_only_public_inputs_and_print_summary(self):
        summary = {
            "schemaVersion": "tritrack.run-summary/v1",
            "runId": "run-001",
            "phase": "prepared",
            "nextAction": "provide-revision",
            "stages": ["doctor", "sync", "transcribe", "emit"],
            "artifacts": {"syncMap": "a" * 64},
        }
        standard_output = io.StringIO()
        with (
            mock.patch.object(
                run_workflow, "prepare_run", return_value=summary
            ) as prepare,
            contextlib.redirect_stdout(standard_output),
        ):
            returncode = cli.main(
                [
                    "run",
                    "prepare",
                    "--camera-a",
                    "A-001.MP4",
                    "--camera-b",
                    "B-001.MP4",
                    "--transcribe-media",
                    "A-001.MP4",
                    "--model",
                    "model.bin",
                    "--language",
                    "en",
                    "--profile",
                    "uhd-2997-ndf-fcpxml-1.14",
                    "--binding",
                    "basic-title-v1",
                    "--event-name",
                    "Interview",
                    "--project-name",
                    "String-out",
                    "--run-id",
                    "run-001",
                    "--output",
                    "prepared-run",
                    "--json",
                ]
            )
        self.assertEqual(returncode, 0)
        self.assertEqual(json.loads(standard_output.getvalue()), summary)
        positional = prepare.call_args.args
        self.assertEqual(positional[0][0].media_id, "A-001.MP4")
        self.assertEqual(positional[1][0].media_id, "B-001.MP4")
        self.assertEqual(positional[2], [Path("A-001.MP4")])
        self.assertEqual(prepare.call_args.kwargs["run_id"], "run-001")

    def test_run_status_and_failure_codes_are_sanitized(self):
        summary = {
            "schemaVersion": "tritrack.run-summary/v1",
            "runId": "run-001",
            "phase": "finished",
            "nextAction": "complete",
            "stages": ["paper", "organize", "emit"],
            "artifacts": {"storyCut": "a" * 64},
        }
        standard_output = io.StringIO()
        with (
            mock.patch.object(run_workflow, "status_run", return_value=summary),
            contextlib.redirect_stdout(standard_output),
        ):
            returncode = cli.main(["run", "status", "--run", "finished", "--json"])
        self.assertEqual(returncode, 0)
        self.assertEqual(json.loads(standard_output.getvalue()), summary)

        cases = {
            "TRITRACK_OUTPUT_EXISTS": 73,
            "TRITRACK_OUTPUT_PARENT_MISSING": 74,
            "TRITRACK_RUN_ENVIRONMENT_UNSUPPORTED": 78,
            "TRITRACK_TRANSCRIBE_ENGINE_FAILED": 69,
            "TRITRACK_RUN_BUNDLE_INCOMPLETE": 65,
        }
        for code, expected in cases.items():
            standard_output = io.StringIO()
            with (
                self.subTest(code=code),
                mock.patch.object(
                    run_workflow, "status_run", side_effect=ValueError(code)
                ),
                contextlib.redirect_stdout(standard_output),
            ):
                returncode = cli.main(
                    ["run", "status", "--run", "invented", "--json"]
                )
            self.assertEqual(returncode, expected)
            self.assertEqual(json.loads(standard_output.getvalue()), {"error": code})
            self.assertNotIn("Traceback", standard_output.getvalue())

    def test_align_cli_publishes_and_prints_only_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision = write_alignment_inputs(root)
            output = root / "aligned.json"

            completed = self.run_cli_unchecked(
                "align",
                "--transcript",
                str(transcript),
                "--revision",
                str(revision),
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.align-summary/v1",
                    "takeCount": 1,
                    "cueCount": 1,
                    "revisedCueCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private", encoded_summary)

    def test_align_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "aligned.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "align",
                "--transcript",
                str(root / "missing-transcript.json"),
                "--revision",
                str(root / "missing-revision.json"),
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_organize_help_exposes_only_the_local_cue_addressed_boundary(self):
        completed = self.run_cli("organize", "--help")
        for option in ("--aligned", "--grouping", "--output", "--json"):
            self.assertIn(option, completed.stdout)
        for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_organize_cli_publishes_only_a_sanitized_summary(self):
        from tests.task9_fixtures import invented_aligned, invented_grouping

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned = root / "aligned.json"
            grouping = root / "grouping.json"
            output = root / "working-cut.json"
            aligned.write_text(
                json.dumps(
                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
                )
                + "\n",
                encoding="utf-8",
            )
            grouping_payload = invented_grouping()
            grouping_payload["alignedTranscriptSha256"] = hashlib.sha256(
                aligned.read_bytes()
            ).hexdigest()
            grouping.write_text(
                json.dumps(
                    grouping_payload,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(aligned),
                "--grouping",
                str(grouping),
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.organize-summary/v1",
                    "questionCount": 2,
                    "segmentCount": 2,
                    "reserveCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded = json.dumps(summary)
            self.assertNotIn(str(root), encoded)
            self.assertNotIn("What changed", encoded)

    def test_organize_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "working-cut.json"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(root / "missing-aligned.json"),
                "--grouping",
                str(root / "missing-grouping.json"),
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_organize_maps_missing_input_to_io_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed = self.run_cli_unchecked(
                "organize",
                "--aligned",
                str(root / "missing-aligned.json"),
                "--grouping",
                str(root / "missing-grouping.json"),
                "--output",
                str(root / "working-cut.json"),
            )
            self.assertEqual(completed.returncode, 74)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_ORGANIZER_INPUT_UNREADABLE"},
            )
            self.assertNotIn("Traceback", completed.stderr)

    def test_paper_help_exposes_exact_nested_local_commands(self):
        paper = self.run_cli("paper", "--help")
        self.assertIn("export", paper.stdout)
        self.assertIn("apply", paper.stdout)

        export = self.run_cli("paper", "export", "--help")
        for option in ("--aligned", "--grouping", "--output", "--json"):
            self.assertIn(option, export.stdout)
        self.assertNotIn("--workbook", export.stdout)

        apply = self.run_cli("paper", "apply", "--help")
        for option in ("--aligned", "--workbook", "--output", "--json"):
            self.assertIn(option, apply.stdout)
        self.assertNotIn("--grouping", apply.stdout)
        for completed in (paper, export, apply):
            for excluded in ("provider", "upload", "model", "retime", "fcpxml"):
                self.assertNotIn(excluded, completed.stdout.lower())

    def test_paper_export_and_apply_print_only_sanitized_summaries(self):
        from openpyxl import load_workbook

        from tests.task9_fixtures import invented_aligned

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            aligned = root / "aligned.json"
            workbook = root / "paper.xlsx"
            grouping = root / "grouping.json"
            aligned.write_text(
                json.dumps(
                    invented_aligned(), ensure_ascii=False, indent=2, sort_keys=True
                )
                + "\n",
                encoding="utf-8",
            )

            exported = self.run_cli_unchecked(
                "paper",
                "export",
                "--aligned",
                str(aligned),
                "--output",
                str(workbook),
                "--json",
            )
            self.assertEqual(exported.returncode, 0, exported.stderr)
            export_summary = json.loads(exported.stdout)
            self.assertEqual(
                export_summary,
                {
                    "schemaVersion": "tritrack.paper-export-summary/v1",
                    "cueCount": 4,
                    "questionCount": 0,
                    "selectionCount": 0,
                    "artifactSha256": hashlib.sha256(
                        workbook.read_bytes()
                    ).hexdigest(),
                },
            )

            editable = load_workbook(workbook, data_only=False)
            editable["Questions"].append(
                ["question-001", "  Invented   question?  ", 1]
            )
            editable["Selections"].append(
                [
                    "ANSWER",
                    "answer-001",
                    "question-001",
                    1,
                    "A.wav",
                    "cue-000001",
                    "cue-000001",
                    None,
                    None,
                ]
            )
            editable.save(workbook)

            applied = self.run_cli_unchecked(
                "paper",
                "apply",
                "--aligned",
                str(aligned),
                "--workbook",
                str(workbook),
                "--output",
                str(grouping),
                "--json",
            )
            self.assertEqual(applied.returncode, 0, applied.stderr)
            apply_summary = json.loads(applied.stdout)
            self.assertEqual(
                apply_summary,
                {
                    "schemaVersion": "tritrack.paper-apply-summary/v1",
                    "questionCount": 1,
                    "answerCount": 1,
                    "reserveCount": 0,
                    "artifactSha256": hashlib.sha256(
                        grouping.read_bytes()
                    ).hexdigest(),
                },
            )
            summaries = json.dumps([export_summary, apply_summary])
            self.assertNotIn(str(root), summaries)
            self.assertNotIn("Invented question", summaries)

    def test_paper_cli_maps_output_and_input_failures(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "paper.xlsx"
            output.write_text("winner", encoding="utf-8")
            exists = self.run_cli_unchecked(
                "paper",
                "export",
                "--aligned",
                str(root / "missing.json"),
                "--output",
                str(output),
            )
            self.assertEqual(exists.returncode, 73)
            self.assertEqual(
                json.loads(exists.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"}
            )

            missing = self.run_cli_unchecked(
                "paper",
                "apply",
                "--aligned",
                str(root / "missing.json"),
                "--workbook",
                str(root / "missing.xlsx"),
                "--output",
                str(root / "grouping.json"),
            )
            self.assertEqual(missing.returncode, 74)
            self.assertEqual(
                json.loads(missing.stdout),
                {"error": "TRITRACK_PAPER_INPUT_UNREADABLE"},
            )
            self.assertNotIn("Traceback", missing.stderr)

    def test_hybrid_help_exposes_only_offline_receipt_validation(self):
        completed = self.run_cli("hybrid", "--help")
        for option in (
            "--transcript",
            "--proposal",
            "--receipt",
            "--model",
            "--output",
            "--json",
        ):
            self.assertIn(option, completed.stdout)
        self.assertIn("offline", completed.stdout.lower())
        self.assertIn("no network", completed.stdout.lower())
        for excluded in ("api-key", "credential", "fallback", "upload-file"):
            self.assertNotIn(excluded, completed.stdout.lower())

    def test_hybrid_cli_validates_receipt_and_prints_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            transcript, revision = write_alignment_inputs(root)
            receipt = write_hybrid_receipt(root, transcript)
            output = root / "hybrid.json"

            completed = self.run_cli_unchecked(
                "hybrid",
                "--transcript",
                str(transcript),
                "--proposal",
                str(revision),
                "--receipt",
                str(receipt),
                "--model",
                "gemini-invented-exact",
                "--output",
                str(output),
                "--json",
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.align-summary/v1",
                    "takeCount": 1,
                    "cueCount": 1,
                    "revisedCueCount": 1,
                    "artifactSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private", encoded_summary)

    def test_hybrid_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "hybrid.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "hybrid",
                "--transcript",
                str(root / "missing-transcript.json"),
                "--proposal",
                str(root / "missing-revision.json"),
                "--receipt",
                str(root / "missing-receipt.json"),
                "--model",
                "gemini-invented-exact",
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_transcribe_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "transcript.json"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "transcribe",
                "--media",
                str(root / "missing.MP4"),
                "--model",
                str(root / "missing-model.bin"),
                "--language",
                "zh",
                "--output",
                str(output),
            )

            self.assertEqual(completed.returncode, 73)
            self.assertEqual(json.loads(completed.stdout), {"error": "TRITRACK_OUTPUT_EXISTS"})
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_transcribe_cli_runs_local_tools_and_prints_only_sanitized_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Invented.MP4"
            model = root / "model.bin"
            output = root / "transcript.json"
            media.write_bytes(b"invented-media")
            model.write_bytes(b"invented-model")

            ffmpeg = root / "ffmpeg"
            ffmpeg.write_text(
                "#!/usr/bin/env python3\n"
                + textwrap.dedent(
                    """
                    import sys
                    import wave

                    with wave.open(sys.argv[-1], "wb") as output:
                        output.setnchannels(1)
                        output.setsampwidth(2)
                        output.setframerate(16000)
                        output.writeframes(bytes([1, 0]) * 16000)
                    """
                ),
                encoding="utf-8",
            )
            ffmpeg.chmod(0o755)

            whisper = root / "whisper-cli"
            whisper.write_text(
                "#!/usr/bin/env python3\n"
                + textwrap.dedent(
                    """
                    import json
                    import sys

                    if "--version" in sys.argv:
                        print("whisper.cpp version: invented-cli")
                        raise SystemExit(0)
                    prefix = sys.argv[sys.argv.index("--output-file") + 1]
                    payload = {
                        "result": {"language": "zh"},
                        "transcription": [
                            {
                                "offsets": {"from": 0, "to": 500},
                                "text": "Invented private transcript text.",
                            }
                        ],
                    }
                    with open(prefix + ".json", "w", encoding="utf-8") as handle:
                        json.dump(payload, handle)
                    """
                ),
                encoding="utf-8",
            )
            whisper.chmod(0o755)
            path = str(root) + os.pathsep + os.environ.get("PATH", "")

            completed = self.run_cli_unchecked(
                "transcribe",
                "--media",
                str(media),
                "--model",
                str(model),
                "--language",
                "zh",
                "--output",
                str(output),
                "--json",
                environment_overrides={"PATH": path},
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.transcribe-summary/v1",
                    "takeCount": 1,
                    "completedCount": 1,
                    "emptyCount": 0,
                    "bundleSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
                },
            )
            encoded_summary = json.dumps(summary)
            self.assertNotIn(str(root), encoded_summary)
            self.assertNotIn("Invented private transcript text", encoded_summary)

    def test_emit_rejects_existing_output_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "string-out.fcpxml"
            output.write_text("sentinel", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(root / "missing-sync-map.json"),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "Invented Event",
                "--project-name",
                "Invented String-out",
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_OUTPUT_EXISTS"},
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

    def test_emit_rejects_invalid_caller_metadata_at_the_cli_boundary(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(root / "missing-sync-map.json"),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "\n",
                "--project-name",
                "Invented String-out",
                "--output",
                str(root / "string-out.fcpxml"),
            )
            self.assertEqual(completed.returncode, 65)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_EMIT_METADATA_INVALID"},
            )
            self.assertEqual(completed.stderr, "")

    def test_emit_rejects_non_object_sync_map_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sync_map = root / "sync-map.json"
            sync_map.write_text("[]", encoding="utf-8")
            completed = self.run_cli_unchecked(
                "emit",
                "--camera-a",
                str(root / "missing-a.MP4"),
                "--camera-b",
                str(root / "missing-b.MP4"),
                "--sync-map",
                str(sync_map),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--binding",
                "basic-title-v1",
                "--event-name",
                "Invented Event",
                "--project-name",
                "Invented String-out",
                "--output",
                str(root / "string-out.fcpxml"),
            )

            self.assertEqual(completed.returncode, 65)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_EMIT_SYNC_MAP_INVALID"},
            )
            self.assertEqual(completed.stderr, "")

    def test_sync_rejects_existing_output_before_running_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            camera_a = root / "A-001.MP4"
            camera_b = root / "B-001.MP4"
            camera_a.write_bytes(b"invented-a")
            camera_b.write_bytes(b"invented-b")
            output = root / "sync-map.json"
            output.write_text("sentinel", encoding="utf-8")

            completed = self.run_cli_unchecked(
                "sync",
                "--camera-a",
                str(camera_a),
                "--camera-b",
                str(camera_b),
                "--profile",
                "uhd-2997-ndf-fcpxml-1.14",
                "--output",
                str(output),
            )
            self.assertEqual(completed.returncode, 73)
            self.assertEqual(
                json.loads(completed.stdout),
                {"error": "TRITRACK_OUTPUT_EXISTS"},
            )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")


class ValidateCliTest(unittest.TestCase):
    def run_cli_unchecked(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "tritrack_editing_assistant.cli", *args],
            check=False,
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=environment,
        )

    def test_help_exposes_exact_four_read_only_modes(self) -> None:
        expected = {
            "contract": ("--artifact", "--json"),
            "fcpxml": ("--artifact", "--profile", "--binding", "--json"),
            "paper": ("--aligned", "--workbook", "--json"),
            "run": ("--run", "--json"),
        }
        parent = self.run_cli_unchecked("validate", "--help")
        self.assertEqual(parent.returncode, 0, parent.stderr)
        for mode in expected:
            self.assertIn(mode, parent.stdout)
        for mode, flags in expected.items():
            with self.subTest(mode=mode):
                completed = self.run_cli_unchecked("validate", mode, "--help")
                self.assertEqual(completed.returncode, 0, completed.stderr)
                for flag in flags:
                    self.assertIn(flag, completed.stdout)
                for forbidden in (
                    "output",
                    "repair",
                    "network",
                    "provider",
                    "credential",
                    "dtd",
                    "media-probe",
                ):
                    self.assertNotIn(forbidden, completed.stdout.lower())

    def test_contract_json_and_human_summaries_are_path_free(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "private-name.json"
            encoded = (
                json.dumps(
                    VALID_CONTRACTS["grouping-v1"],
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
            artifact.write_bytes(encoded)

            as_json = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(artifact), "--json"
            )
            human = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(artifact)
            )

            self.assertEqual(as_json.returncode, 0, as_json.stderr)
            summary = json.loads(as_json.stdout)
            self.assertEqual(summary["artifactKind"], "contract")
            self.assertEqual(summary["validationScope"], "contract")
            self.assertEqual(
                summary["hashes"]["artifact"],
                hashlib.sha256(encoded).hexdigest(),
            )
            self.assertEqual(human.returncode, 0, human.stderr)
            self.assertEqual(
                human.stdout.splitlines(),
                [
                    "VALIDATION\tcontract\tcontract",
                    f"HASH\tartifact\t{hashlib.sha256(encoded).hexdigest()}",
                    "DETAIL\tcontractName\t\"grouping-v1\"",
                    "DETAIL\tcontractSchemaVersion\t\"tritrack.grouping/v1\"",
                ],
            )
            for output in (as_json.stdout, human.stdout):
                self.assertNotIn(str(root), output)
                self.assertNotIn("What changed?", output)

    def test_dispatches_fcpxml_paper_and_run_with_exact_arguments(self) -> None:
        base_summary = {
            "schemaVersion": "tritrack.validate-summary/v1",
            "toolVersion": "0.1.0a0",
            "artifactKind": "invented",
            "validationScope": "invented-scope",
            "hashes": {},
            "counts": {},
            "details": {},
        }
        with (
            mock.patch.object(
                cli.validate_module,
                "validate_fcpxml_artifact",
                return_value=base_summary,
            ) as fcpxml,
            mock.patch.object(
                cli.validate_module,
                "validate_paper_artifacts",
                return_value=base_summary,
            ) as paper,
            mock.patch.object(
                cli.validate_module,
                "validate_run_bundle",
                return_value=base_summary,
            ) as run,
        ):
            for arguments in (
                [
                    "validate",
                    "fcpxml",
                    "--artifact",
                    "story.fcpxml",
                    "--profile",
                    "profile-id",
                    "--binding",
                    "binding-id",
                    "--json",
                ],
                [
                    "validate",
                    "paper",
                    "--aligned",
                    "aligned.json",
                    "--workbook",
                    "paper.xlsx",
                    "--json",
                ],
                ["validate", "run", "--run", "finished-run", "--json"],
            ):
                with self.subTest(arguments=arguments):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        self.assertEqual(cli.main(arguments), 0)
                    self.assertEqual(json.loads(output.getvalue()), base_summary)

        fcpxml.assert_called_once_with(
            Path("story.fcpxml"),
            profile_id="profile-id",
            binding_id="binding-id",
        )
        paper.assert_called_once_with(Path("aligned.json"), Path("paper.xlsx"))
        run.assert_called_once_with(Path("finished-run"))

    def test_usage_data_io_and_policy_failures_are_stable_and_sanitized(self) -> None:
        usage = self.run_cli_unchecked("validate", "contract")
        self.assertEqual(usage.returncode, 64)
        self.assertEqual(json.loads(usage.stdout), {"error": "TRITRACK_USAGE"})
        self.assertEqual(usage.stderr, "")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            malformed = root / "private-name.json"
            malformed.write_text("{private text", encoding="utf-8")
            data = self.run_cli_unchecked(
                "validate", "contract", "--artifact", str(malformed)
            )
            missing = self.run_cli_unchecked(
                "validate",
                "contract",
                "--artifact",
                str(root / "missing.json"),
            )
            missing_run = self.run_cli_unchecked(
                "validate",
                "run",
                "--run",
                str(root / "missing-run"),
            )
            xml = root / "story.fcpxml"
            xml.write_text("invented", encoding="utf-8")
            policy = self.run_cli_unchecked(
                "validate",
                "fcpxml",
                "--artifact",
                str(xml),
                "--profile",
                "unknown-profile",
                "--binding",
                "basic-title-v1",
            )

            self.assertEqual(data.returncode, 65)
            self.assertEqual(
                json.loads(data.stdout), {"error": "TRITRACK_VALIDATE_JSON_INVALID"}
            )
            self.assertEqual(missing.returncode, 74)
            self.assertEqual(
                json.loads(missing.stdout),
                {"error": "TRITRACK_VALIDATE_INPUT_UNREADABLE"},
            )
            self.assertEqual(missing_run.returncode, 74)
            self.assertEqual(
                json.loads(missing_run.stdout),
                {"error": "TRITRACK_RUN_INPUT_UNREADABLE"},
            )
            self.assertEqual(policy.returncode, 78)
            self.assertEqual(
                json.loads(policy.stdout), {"error": "TRITRACK_PROFILE_UNKNOWN"}
            )
            for completed in (data, missing, missing_run, policy):
                self.assertEqual(completed.stderr, "")
                self.assertNotIn(str(root), completed.stdout)
                self.assertNotIn("private text", completed.stdout)
                self.assertNotIn("Traceback", completed.stdout)

    def test_validate_does_not_change_component_registry(self) -> None:
        self.assertEqual(len(cli.COMPONENTS), 11)
        self.assertFalse(
            any(component["command"] == "validate" for component in cli.COMPONENTS)
        )


class ValidateDocumentationTest(unittest.TestCase):
    def test_public_docs_name_all_help_authorities_and_scope_boundaries(self) -> None:
        paths = (
            ROOT / "README.md",
            ROOT / "docs" / "TOOLING.md",
            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md",
        )
        commands = (
            "tritrack validate --help",
            "tritrack validate contract --help",
            "tritrack validate fcpxml --help",
            "tritrack validate paper --help",
            "tritrack validate run --help",
        )
        scopes = (
            "contract",
            "structural-profile",
            "authority-bound",
            "complete-run-bundle",
        )
        for path in paths:
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for command in commands:
                    self.assertIn(command, text)
                for scope in scopes:
                    self.assertIn(scope, text)
                self.assertIn("read-only", text)
                self.assertIn("does not repair", text)
                self.assertIn("source media", text)
                self.assertIn("DTD", text)
                self.assertIn("GUI", text)

    def test_release_gate_is_maintainer_only_and_python_support_is_exact(self) -> None:
        release_command = (
            "python scripts/release_gate.py --source . --output ABSENT_DIRECTORY"
        )
        tooling = (ROOT / "docs" / "TOOLING.md").read_text(encoding="utf-8")
        maintainer = (
            ROOT
            / ".agents"
            / "skills"
            / "tritrack-editing-assistant-maintainer"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        end_user = (
            ROOT / "skills" / "tritrack-editing-assistant" / "SKILL.md"
        ).read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(release_command, tooling)
        self.assertIn(release_command, maintainer)
        for text in (readme, end_user):
            self.assertNotIn(release_command, text)
        self.assertNotIn("release", end_user.casefold())
        self.assertNotIn(".py", end_user.casefold())

        for relative in ("README.md", "docs/TOOLING.md", "CONTRIBUTING.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("Python 3.12 and 3.13", text, relative)
            self.assertNotIn("Python 3.12 or newer", text, relative)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_cli.py ---

--- BEGIN FILE tests/test_title_binding.py ---
"""Task 4 tests for packaged public profiles and Basic Title capture."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tritrack_editing_assistant import doctor

SCRIPT = Path(__file__).parents[1] / "scripts" / "capture_basic_title_binding.py"


def load_capture_module():
    spec = importlib.util.spec_from_file_location("capture_basic_title_binding", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("capture script loader unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SAFE_FCPXML = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.14">
  <resources>
    <effect id="r2" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>
    <format id="r1" name="FFVideoFormat3840x2160p2997" frameDuration="1001/30000s" width="3840" height="2160" colorSpace="1-1-1 (Rec. 709)"/>
  </resources>
  <library><event name="Invented"><project name="Invented Basic Title"><sequence format="r1" duration="3003/30000s" tcFormat="NDF"><spine>
    <title name="Invented subtitle" ref="r2" offset="0s" start="0s" duration="3003/30000s">
      <text><text-style ref="ts1">Invented subtitle</text-style></text>
      <text-style-def id="ts1"><text-style font="Helvetica" fontSize="72" fontFace="Regular" fontColor="1 1 1 1" alignment="center"/></text-style-def>
    </title>
  </spine></sequence></project></event></library>
</fcpxml>
"""


class TitleBindingTest(unittest.TestCase):
    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
    def test_capture_inputs_reject_fifos_without_waiting_for_a_writer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fifo = root / "input"
            os.mkfifo(fifo)
            cases = (
                ("--input", os.fspath(fifo)),
                ("--binding", os.fspath(fifo), "--text", "Invented title"),
            )
            for index, arguments in enumerate(cases):
                with self.subTest(arguments=arguments):
                    completed = subprocess.run(
                        [
                            os.fspath(Path(os.sys.executable)),
                            os.fspath(SCRIPT),
                            *arguments,
                            "--output",
                            os.fspath(root / f"output-{index}"),
                        ],
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=3,
                    )
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertIn("TRITRACK_TITLE_BINDING_", completed.stderr)

    def test_capture_rejects_oversized_xml_before_parsing(self) -> None:
        capture = load_capture_module()
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "oversized.fcpxml"
            with source.open("wb") as stream:
                stream.truncate(16 * 1024 * 1024 + 1)
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TITLE_BINDING_INVALID_XML"
            ):
                capture.capture_binding(source)

    def test_packaged_compatibility_profile_has_exact_alpha_values(self) -> None:
        profile = doctor.load_profile("uhd-2997-ndf-fcpxml-1.14")
        self.assertEqual(profile["schemaVersion"], "tritrack.compatibility-profile/v1")
        self.assertEqual(profile["frameDuration"], "1001/30000s")
        self.assertEqual((profile["width"], profile["height"]), (3840, 2160))
        self.assertEqual(profile["timecodeFormat"], "NDF")
        self.assertEqual(profile["audioRate"], 48000)

    def test_packaged_basic_title_binding_validates(self) -> None:
        binding = doctor.load_title_binding("basic-title-v1")
        self.assertEqual(binding["schemaVersion"], "tritrack.title-binding/v1")
        self.assertEqual(binding["effectName"], "Basic Title")
        self.assertTrue(binding["effectUid"].endswith("Basic Title.moti"))

    def test_capture_extracts_only_public_effect_and_style_values(self) -> None:
        capture = load_capture_module()
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "invented.fcpxml"
            source.write_text(SAFE_FCPXML, encoding="utf-8")

            binding = capture.capture_binding(source)

        self.assertEqual(binding["effectName"], "Basic Title")
        self.assertEqual(
            {parameter["name"] for parameter in binding["parameters"]},
            {"alignment", "font", "fontColor", "fontFace", "fontSize"},
        )
        self.assertNotIn("Invented subtitle", json.dumps(binding))

    def test_capture_rejects_doctype_subsets_and_entities(self) -> None:
        capture = load_capture_module()
        source_xml = SAFE_FCPXML.replace(
            "<!DOCTYPE fcpxml>",
            '<!DOCTYPE fcpxml [<!ENTITY private SYSTEM "file:///etc/passwd">]>',
        )
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "entity.fcpxml"
            source.write_text(source_xml, encoding="utf-8")
            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TITLE_BINDING_INVALID_XML"
            ):
                capture.capture_binding(source)

    def test_rendered_basic_title_roundtrips_through_public_binding(self) -> None:
        capture = load_capture_module()
        binding = doctor.load_title_binding("basic-title-v1")
        rendered = capture.render_basic_title_fcpxml(
            binding,
            text="TRITRACK GENERATED BASIC TITLE",
        )

        self.assertIn('<fcpxml version="1.14">', rendered)
        self.assertIn('frameDuration="1001/30000s"', rendered)
        self.assertIn('tcFormat="NDF"', rendered)
        self.assertIn('duration="180180/30000s"', rendered)
        self.assertEqual(rendered.count('duration="90090/30000s"'), 2)
        self.assertIn('offset="90090/30000s"', rendered)
        self.assertNotIn('duration="3s"', rendered)
        self.assertNotIn("src=", rendered)

        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "generated.fcpxml"
            source.write_text(rendered, encoding="utf-8")
            recaptured = capture.capture_binding(source)

        self.assertEqual(recaptured, binding)

    def test_capture_rejects_private_title_font_path_and_template(self) -> None:
        capture = load_capture_module()
        forbidden_variants = (
            SAFE_FCPXML.replace("Basic Title", "Artlist LT", 1),
            SAFE_FCPXML.replace("Helvetica", "江城知音体"),
            SAFE_FCPXML.replace(
                ".../Titles.localized",
                "/Users/editor/Movies/Motion Templates/Titles.localized",
            ),
            SAFE_FCPXML.replace(
                '<title name="Invented subtitle"',
                '<title src="relative/private.mov" name="Invented subtitle"',
            ),
            SAFE_FCPXML.replace("Basic Title.moti", "Transcription Template.moti"),
        )
        with tempfile.TemporaryDirectory() as temporary:
            for index, xml in enumerate(forbidden_variants):
                with self.subTest(index=index):
                    source = Path(temporary) / f"forbidden-{index}.fcpxml"
                    source.write_text(xml, encoding="utf-8")
                    with self.assertRaisesRegex(
                        ValueError, "TRITRACK_TITLE_BINDING_FORBIDDEN"
                    ):
                        capture.capture_binding(source)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_title_binding.py ---

--- BEGIN FILE tests/test_transcribe_takes.py ---
"""Task 7 tests for local transcript evidence canonicalization."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from tritrack_editing_assistant import contracts, transcribe_takes


class TranscriptCanonicalizationTest(unittest.TestCase):
    def evidence(self) -> dict[str, object]:
        return {
            "result": {"language": "zh"},
            "transcription": [
                {
                    "offsets": {"from": 125, "to": 900},
                    "text": "  第一個 invented cue。 ",
                    "tokens": [{"id": 1}],
                },
                {
                    "offsets": {"from": 900, "to": 1500},
                    "text": "Cafe\u0301  cue",
                },
            ],
            "systeminfo": "ignored engine detail",
        }

    def test_canonicalizes_supported_whisper_evidence(self) -> None:
        cues = transcribe_takes.canonicalize_whisper_evidence(
            self.evidence(),
            requested_language="zh",
            audio_duration_ms=2000,
        )

        self.assertEqual(
            cues,
            [
                {
                    "cueId": "cue-000001",
                    "startMs": 125,
                    "endMs": 900,
                    "text": "第一個 invented cue。",
                },
                {
                    "cueId": "cue-000002",
                    "startMs": 900,
                    "endMs": 1500,
                    "text": "Café cue",
                },
            ],
        )

    def test_rejects_language_mismatch_and_invalid_timing(self) -> None:
        cases = []

        wrong_language = self.evidence()
        wrong_language["result"] = {"language": "en"}
        cases.append(wrong_language)

        overlapping = self.evidence()
        transcription = overlapping["transcription"]
        assert isinstance(transcription, list)
        second = transcription[1]
        assert isinstance(second, dict)
        second["offsets"] = {"from": 899, "to": 1500}
        cases.append(overlapping)

        bool_offset = self.evidence()
        transcription = bool_offset["transcription"]
        assert isinstance(transcription, list)
        first = transcription[0]
        assert isinstance(first, dict)
        first["offsets"] = {"from": False, "to": 900}
        cases.append(bool_offset)

        beyond_audio = self.evidence()
        transcription = beyond_audio["transcription"]
        assert isinstance(transcription, list)
        second = transcription[1]
        assert isinstance(second, dict)
        second["offsets"] = {"from": 2000, "to": 2001}
        cases.append(beyond_audio)

        for payload in cases:
            with self.subTest(payload=payload), self.assertRaisesRegex(
                (TypeError, ValueError), "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
            ):
                transcribe_takes.canonicalize_whisper_evidence(
                    payload,
                    requested_language="zh",
                    audio_duration_ms=2000,
                )

    def test_clamps_only_bounded_final_whisper_padding_to_audio_duration(self) -> None:
        evidence = {
            "result": {"language": "en"},
            "transcription": [
                {
                    "offsets": {"from": 0, "to": 5000},
                    "text": "Invented short cue.",
                }
            ],
        }

        cues = transcribe_takes.canonicalize_whisper_evidence(
            evidence,
            requested_language="en",
            audio_duration_ms=3424,
        )

        self.assertEqual(cues[0]["endMs"], 3424)

        evidence["transcription"][0]["offsets"] = {"from": 0, "to": 9000}
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
        ):
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=3424,
            )

    def test_accepts_exact_blank_audio_sentinel_only_for_proven_silence(self) -> None:
        evidence = {
            "result": {"language": "en"},
            "transcription": [
                {
                    "offsets": {"from": 0, "to": 10000},
                    "text": " [BLANK_AUDIO]",
                }
            ],
        }

        self.assertEqual(
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=2000,
                proven_silence=True,
            ),
            [],
        )
        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_SILENCE_SENTINEL_INVALID"
        ):
            transcribe_takes.canonicalize_whisper_evidence(
                evidence,
                requested_language="en",
                audio_duration_ms=2000,
            )

    def test_builds_strict_stably_sorted_bundle_and_bytes(self) -> None:
        take_a = transcribe_takes.TranscribedTake(
            take_id="A-001.MP4",
            source_sha256="a" * 64,
            status="completed",
            cues=(
                {
                    "cueId": "cue-000001",
                    "startMs": 0,
                    "endMs": 500,
                    "text": "Invented A cue.",
                },
            ),
        )
        take_b = transcribe_takes.TranscribedTake(
            take_id="B-001.MP4",
            source_sha256="b" * 64,
            status="empty",
            cues=(),
        )

        first = transcribe_takes.build_transcript_bundle(
            [take_b, take_a],
            language="zh",
            model_sha256="f" * 64,
            engine_version="whisper.cpp version: 1.9.1",
        )
        second = transcribe_takes.build_transcript_bundle(
            [take_a, take_b],
            language="zh",
            model_sha256="f" * 64,
            engine_version="whisper.cpp version: 1.9.1",
        )

        contracts.validate_contract("transcript-bundle-v1", first)
        self.assertEqual(first, second)
        self.assertEqual(first["profileId"], "whisper-cpp-cpu-no-fallback-v1")
        self.assertEqual(
            [take["takeId"] for take in first["takes"]],
            ["A-001.MP4", "B-001.MP4"],
        )
        self.assertEqual(
            transcribe_takes.encode_transcript_bundle(first),
            transcribe_takes.encode_transcript_bundle(second),
        )
        self.assertEqual(
            json.loads(transcribe_takes.encode_transcript_bundle(first)), first
        )

    def test_bundle_rejects_duplicate_take_ids(self) -> None:
        take = transcribe_takes.TranscribedTake(
            take_id="A-001.MP4",
            source_sha256="a" * 64,
            status="empty",
            cues=(),
        )

        with self.assertRaisesRegex(
            ValueError, "TRITRACK_TRANSCRIPT_DUPLICATE_TAKE"
        ):
            transcribe_takes.build_transcript_bundle(
                [take, take],
                language="zh",
                model_sha256="f" * 64,
                engine_version="whisper.cpp version: 1.9.1",
            )


class LocalTranscriptionWorkflowTest(unittest.TestCase):
    @unittest.skipUnless(
        hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required"
    )
    def test_descriptor_input_readers_reject_special_files_before_blocking(self) -> None:
        selected = Path("invented-special-file")
        readers = (
            lambda: transcribe_takes._sha256_file(selected),
            lambda: transcribe_takes._inspect_normalized_audio(selected),
            lambda: transcribe_takes._load_engine_json(selected),
        )

        for reader in readers:
            observed: list[int] = []

            def reject_special(_path, flags, *_args, observed=observed):
                observed.append(flags)
                raise OSError("invented special file")

            with self.subTest(reader=reader), mock.patch.object(
                transcribe_takes.os, "open", side_effect=reject_special
            ), self.assertRaises((OSError, ValueError)):
                reader()
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_NONBLOCK)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
    def test_transcript_hash_rejects_fifo_without_waiting_for_a_writer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fifo = Path(temporary) / "media.mov"
            os.mkfifo(fifo)
            code = (
                "from pathlib import Path; import sys; "
                "from tritrack_editing_assistant.transcribe_takes "
                "import _sha256_file; "
                "\ntry: _sha256_file(Path(sys.argv[1]))"
                "\nexcept ValueError as error: print(error); raise SystemExit(0)"
                "\nraise SystemExit(1)"
            )
            completed = subprocess.run(
                [os.fspath(Path(os.sys.executable)), "-c", code, os.fspath(fifo)],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "TRITRACK_TRANSCRIPT_INPUT_CHANGED\n")
        self.assertEqual(completed.stderr, "")

    def write_executable(self, root: Path, name: str, body: str) -> Path:
        path = root / name
        path.write_text(
            "#!/usr/bin/env python3\n" + textwrap.dedent(body),
            encoding="utf-8",
        )
        path.chmod(0o755)
        return path

    def write_ffmpeg(self, root: Path, *, sample: int) -> Path:
        return self.write_executable(
            root,
            "invented-ffmpeg",
            f"""
            import sys
            import wave

            with wave.open(sys.argv[-1], "wb") as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(16000)
                output.writeframes(bytes([{sample & 255}, {(sample >> 8) & 255}]) * 16000)
            """,
        )

    def write_whisper(
        self,
        root: Path,
        *,
        transcription: list[dict[str, object]],
        log: Path | None = None,
    ) -> Path:
        payload = {
            "result": {"language": "zh"},
            "transcription": transcription,
        }
        return self.write_executable(
            root,
            "invented-whisper",
            f"""
            import json
            import sys

            log_path = {str(log) if log is not None else None!r}
            if log_path is not None:
                with open(log_path, "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(sys.argv[1:]) + "\\n")

            if "--version" in sys.argv:
                print("whisper.cpp version: invented-1")
                raise SystemExit(0)

            required = [
                "--model",
                "--file",
                "--language",
                "zh",
                "--temperature",
                "0",
                "--temperature-inc",
                "0",
                "--no-fallback",
                "--no-gpu",
                "--output-json-full",
                "--output-file",
                "--no-prints",
            ]
            if any(value not in sys.argv for value in required):
                raise SystemExit(9)
            if "--prompt" in sys.argv or "--translate" in sys.argv:
                raise SystemExit(10)

            prefix = sys.argv[sys.argv.index("--output-file") + 1]
            with open(prefix + ".json", "w", encoding="utf-8") as handle:
                json.dump({payload!r}, handle, ensure_ascii=False)
            """,
        )

    def test_single_pass_publishes_stable_path_free_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media_a = root / "A-001.MP4"
            media_b = root / "B-001.MP4"
            model = root / "invented-model.bin"
            media_a.write_bytes(b"invented-source-a")
            media_b.write_bytes(b"invented-source-b")
            model.write_bytes(b"invented-local-model")
            ffmpeg = self.write_ffmpeg(root, sample=1)
            log = root / "whisper-argv.jsonl"
            whisper = self.write_whisper(
                root,
                transcription=[
                    {
                        "offsets": {"from": 0, "to": 500},
                        "text": " Invented local cue. ",
                    }
                ],
                log=log,
            )
            first_output = root / "first.json"
            second_output = root / "second.json"

            first = transcribe_takes.transcribe_and_publish(
                [media_b, media_a],
                model_path=model,
                language="zh",
                output_path=first_output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )
            second = transcribe_takes.transcribe_and_publish(
                [media_a, media_b],
                model_path=model,
                language="zh",
                output_path=second_output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )

            self.assertEqual(first, second)
            self.assertEqual(first_output.read_bytes(), second_output.read_bytes())
            self.assertEqual(
                first["modelSha256"], hashlib.sha256(model.read_bytes()).hexdigest()
            )
            self.assertEqual(
                [take["takeId"] for take in first["takes"]],
                ["A-001.MP4", "B-001.MP4"],
            )
            encoded = first_output.read_text(encoding="utf-8")
            self.assertNotIn(str(root), encoded)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            inference_calls = [call for call in calls if "--version" not in call]
            self.assertEqual(len(inference_calls), 4)
            self.assertTrue(all(call.count("--no-fallback") == 1 for call in inference_calls))

    def test_digital_silence_is_the_only_empty_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Silent.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-silent-source")
            model.write_bytes(b"invented-model")
            ffmpeg = self.write_ffmpeg(root, sample=0)
            whisper = self.write_whisper(
                root,
                transcription=[
                    {
                        "offsets": {"from": 0, "to": 10000},
                        "text": " [BLANK_AUDIO]",
                    }
                ],
            )
            output = root / "transcript.json"

            payload = transcribe_takes.transcribe_and_publish(
                [media],
                model_path=model,
                language="zh",
                output_path=output,
                ffmpeg_executable=str(ffmpeg),
                whisper_executable=str(whisper),
            )

            self.assertEqual(payload["takes"][0]["status"], "empty")
            self.assertEqual(payload["takes"][0]["cues"], [])

    def test_non_silent_empty_and_silent_text_fail_without_output(self) -> None:
        cases = ((1, []), (0, [{"offsets": {"from": 0, "to": 500}, "text": "Invented"}]))
        for sample, transcription in cases:
            with (
                self.subTest(sample=sample, transcription=transcription),
                tempfile.TemporaryDirectory() as temporary,
            ):
                    root = Path(temporary)
                    media = root / "Take.MP4"
                    model = root / "model.bin"
                    media.write_bytes(b"invented-source")
                    model.write_bytes(b"invented-model")
                    output = root / "transcript.json"

                    with self.assertRaisesRegex(
                        ValueError, "TRITRACK_TRANSCRIPT_(EMPTY_UNPROVEN|SILENCE_TEXT_DETECTED)"
                    ):
                        transcribe_takes.transcribe_and_publish(
                            [media],
                            model_path=model,
                            language="zh",
                            output_path=output,
                            ffmpeg_executable=str(self.write_ffmpeg(root, sample=sample)),
                            whisper_executable=str(
                                self.write_whisper(root, transcription=transcription)
                            ),
                        )
                    self.assertFalse(output.exists())

    def test_existing_output_and_duplicate_basenames_fail_before_processes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "transcript.json"
            output.write_text("sentinel", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                transcribe_takes.transcribe_and_publish(
                    [root / "missing.MP4"],
                    model_path=root / "missing-model.bin",
                    language="zh",
                    output_path=output,
                    ffmpeg_executable="missing-ffmpeg",
                    whisper_executable="missing-whisper",
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "sentinel")

            (root / "one").mkdir()
            (root / "two").mkdir()
            first = root / "one" / "Take.MP4"
            second = root / "two" / "Take.MP4"
            first.write_bytes(b"one")
            second.write_bytes(b"two")
            model = root / "model.bin"
            model.write_bytes(b"model")

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_DUPLICATE_TAKE"
            ):
                transcribe_takes.transcribe_and_publish(
                    [first, second],
                    model_path=model,
                    language="zh",
                    output_path=root / "new.json",
                    ffmpeg_executable="missing-ffmpeg",
                    whisper_executable="missing-whisper",
                )

    def test_detects_source_changes_during_audio_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source-before")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            ffmpeg = self.write_executable(
                root,
                "mutating-ffmpeg",
                """
                import sys
                import wave

                source = sys.argv[sys.argv.index("-i") + 1]
                with open(source, "ab") as handle:
                    handle.write(b"-changed")
                with wave.open(sys.argv[-1], "wb") as audio:
                    audio.setnchannels(1)
                    audio.setsampwidth(2)
                    audio.setframerate(16000)
                    audio.writeframes(bytes([1, 0]) * 16000)
                """,
            )
            whisper = self.write_whisper(
                root,
                transcription=[
                    {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                ],
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(ffmpeg),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_detects_model_changes_during_inference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model-before")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "mutating-whisper",
                """
                import json
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                model = sys.argv[sys.argv.index("--model") + 1]
                with open(model, "ab") as handle:
                    handle.write(b"-changed")
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {
                    "result": {"language": "zh"},
                    "transcription": [
                        {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                    ],
                }
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_rechecks_all_sources_after_the_complete_batch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = root / "A.MP4"
            second = root / "B.MP4"
            model = root / "model.bin"
            first.write_bytes(b"invented-source-a")
            second.write_bytes(b"invented-source-b")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "late-mutating-whisper",
                """
                import json
                import sys
                from pathlib import Path

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                state = Path(__file__).with_suffix(".state")
                if state.exists():
                    with (Path(__file__).parent / "A.MP4").open("ab") as handle:
                        handle.write(b"-changed-after-first-take")
                else:
                    state.write_text("first", encoding="utf-8")
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {
                    "result": {"language": "zh"},
                    "transcription": [
                        {"offsets": {"from": 0, "to": 500}, "text": "Invented"}
                    ],
                }
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIPT_INPUT_CHANGED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [first, second],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_invalid_engine_version_bytes_fail_with_stable_code(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "invalid-version-whisper",
                """
                import sys

                if "--version" in sys.argv:
                    sys.stdout.buffer.write(bytes([255]))
                    raise SystemExit(0)
                raise SystemExit(91)
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIBE_ENGINE_VERSION_INVALID"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_malformed_or_oversized_engine_output_never_publishes(self) -> None:
        scripts = {
            "malformed": """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    handle.write("{")
            """,
            "oversized": """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                with open(prefix + ".json", "wb") as handle:
                    handle.truncate(16 * 1024 * 1024 + 1)
            """,
        }
        for name, script in scripts.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                media = root / "Take.MP4"
                model = root / "model.bin"
                media.write_bytes(b"invented-source")
                model.write_bytes(b"invented-model")
                output = root / "transcript.json"

                with self.assertRaisesRegex(
                    ValueError, "TRITRACK_TRANSCRIPT_EVIDENCE_INVALID"
                ):
                    transcribe_takes.transcribe_and_publish(
                        [media],
                        model_path=model,
                        language="zh",
                        output_path=output,
                        ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                        whisper_executable=str(
                            self.write_executable(root, f"{name}-whisper", script)
                        ),
                    )
                self.assertFalse(output.exists())

    def test_engine_capture_overflow_never_publishes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "noisy-whisper",
                """
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                sys.stdout.write("x" * (600 * 1024))
                """,
            )

            with self.assertRaisesRegex(
                ValueError, "TRITRACK_TRANSCRIBE_ENGINE_FAILED"
            ):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertFalse(output.exists())

    def test_publication_race_preserves_the_winner(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            media = root / "Take.MP4"
            model = root / "model.bin"
            media.write_bytes(b"invented-source")
            model.write_bytes(b"invented-model")
            output = root / "transcript.json"
            whisper = self.write_executable(
                root,
                "racing-whisper",
                f"""
                import json
                import sys

                if "--version" in sys.argv:
                    print("whisper.cpp version: invented-1")
                    raise SystemExit(0)
                prefix = sys.argv[sys.argv.index("--output-file") + 1]
                payload = {{
                    "result": {{"language": "zh"}},
                    "transcription": [
                        {{"offsets": {{"from": 0, "to": 500}}, "text": "Invented"}}
                    ],
                }}
                with open(prefix + ".json", "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                with open({str(output)!r}, "w", encoding="utf-8") as handle:
                    handle.write("race-winner")
                """,
            )

            with self.assertRaisesRegex(ValueError, "TRITRACK_OUTPUT_EXISTS"):
                transcribe_takes.transcribe_and_publish(
                    [media],
                    model_path=model,
                    language="zh",
                    output_path=output,
                    ffmpeg_executable=str(self.write_ffmpeg(root, sample=1)),
                    whisper_executable=str(whisper),
                )
            self.assertEqual(output.read_text(encoding="utf-8"), "race-winner")


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_transcribe_takes.py ---

--- BEGIN FILE tests/test_validate_artifacts.py ---
"""Task 11 tests for read-only, offline artifact validation."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.test_contracts import VALID_CONTRACTS
from tests.test_emit_fcpxml import media, sync_payload
from tests.test_run_workflow import aligned_bundle_files, aligned_manifest, sha256
from tritrack_editing_assistant import (
    align_text,
    contracts,
    emit_fcpxml,
    organizer,
    paper_edit,
    process,
    run_workflow,
    story_fcpxml,
    validate_artifacts,
)


def encode_json(payload: object) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


class NonblockingRegularFileBoundaryTest(unittest.TestCase):
    @unittest.skipUnless(hasattr(os, "O_NONBLOCK"), "POSIX nonblocking flag required")
    def test_all_descriptor_readers_reject_special_files_before_blocking(self) -> None:
        selected = Path("invented-special-file")
        readers = (
            (
                "alignment JSON",
                align_text,
                lambda: align_text._read_regular_bytes(selected, "INVENTED"),
            ),
            ("sync map", emit_fcpxml, lambda: emit_fcpxml.load_sync_map(selected)),
            (
                "organizer JSON",
                organizer,
                lambda: organizer._read_regular_bytes(selected, "INVENTED"),
            ),
            (
                "paper artifact",
                paper_edit,
                lambda: paper_edit._read_regular_bytes(
                    selected, limit=1, invalid_code="INVENTED"
                ),
            ),
            (
                "run artifact",
                run_workflow,
                lambda: run_workflow._read_regular_bytes(
                    selected, limit=1, code="INVENTED"
                ),
            ),
            (
                "run source hash",
                run_workflow,
                lambda: run_workflow._hash_regular_path(selected, code="INVENTED"),
            ),
            (
                "story artifact",
                story_fcpxml,
                lambda: story_fcpxml._read_regular_bytes(selected, "INVENTED"),
            ),
            (
                "story media hash",
                story_fcpxml,
                lambda: story_fcpxml._hash_regular_media(selected),
            ),
            (
                "validator artifact",
                validate_artifacts,
                lambda: validate_artifacts._read_regular_bytes(selected),
            ),
        )

        for label, module, reader in readers:
            observed: list[int] = []

            def reject_special(_path, flags, *_args, observed=observed):
                observed.append(flags)
                raise OSError("invented special file")

            with self.subTest(label=label), mock.patch.object(
                module.os, "open", side_effect=reject_special
            ), self.assertRaises(ValueError):
                reader()
            self.assertEqual(len(observed), 1)
            self.assertTrue(observed[0] & os.O_NONBLOCK, label)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO required")
    def test_validator_rejects_fifo_without_waiting_for_a_writer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fifo = Path(temporary) / "artifact.json"
            os.mkfifo(fifo)
            code = (
                "from pathlib import Path; import sys; "
                "from tritrack_editing_assistant.validate_artifacts "
                "import validate_contract_artifact; "
                "\ntry: validate_contract_artifact(Path(sys.argv[1]))"
                "\nexcept ValueError as error: print(error); raise SystemExit(0)"
                "\nraise SystemExit(1)"
            )
            completed = subprocess.run(
                [os.fspath(Path(os.sys.executable)), "-c", code, os.fspath(fifo)],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "TRITRACK_VALIDATE_INPUT_UNREADABLE\n")
        self.assertEqual(completed.stderr, "")


class ContractValidationTest(unittest.TestCase):
    def setUp(self) -> None:
        contracts.contract_names_by_schema_version.cache_clear()

    def tearDown(self) -> None:
        contracts.contract_names_by_schema_version.cache_clear()

    def test_discovers_every_installed_contract_from_schema_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, payload in VALID_CONTRACTS.items():
                with self.subTest(name=name):
                    encoded = encode_json(payload)
                    artifact = root / f"{name}.json"
                    artifact.write_bytes(encoded)

                    summary = validate_artifacts.validate_contract_artifact(
                        artifact
                    )

                    self.assertEqual(
                        summary,
                        {
                            "schemaVersion": "tritrack.validate-summary/v1",
                            "toolVersion": "0.1.0a0",
                            "artifactKind": "contract",
                            "validationScope": "contract",
                            "hashes": {
                                "artifact": hashlib.sha256(encoded).hexdigest()
                            },
                            "counts": {},
                            "details": {
                                "contractName": name,
                                "contractSchemaVersion": payload["schemaVersion"],
                            },
                        },
                    )
                    self.assertEqual(artifact.read_bytes(), encoded)

    def test_rejects_unknown_invalid_and_unreadable_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            unknown = root / "unknown.json"
            unknown.write_bytes(encode_json({"schemaVersion": "invented/v1"}))
            invalid = root / "invalid.json"
            payload = copy.deepcopy(VALID_CONTRACTS["grouping-v1"])
            payload["questions"][0]["unexpected"] = True
            invalid.write_bytes(encode_json(payload))
            malformed = root / "malformed.json"
            malformed.write_bytes(b"{not-json")
            empty = root / "empty.json"
            empty.write_bytes(b"")
            symlink = root / "symlink.json"
            symlink.symlink_to(unknown)

            cases = (
                (unknown, "TRITRACK_VALIDATE_CONTRACT_UNKNOWN"),
                (invalid, "TRITRACK_VALIDATE_CONTRACT_INVALID"),
                (malformed, "TRITRACK_VALIDATE_JSON_INVALID"),
                (empty, "TRITRACK_VALIDATE_INPUT_INVALID"),
                (symlink, "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
                (root / "missing.json", "TRITRACK_VALIDATE_INPUT_UNREADABLE"),
            )
            for artifact, code in cases:
                with self.subTest(code=code), self.assertRaisesRegex(
                    ValueError, rf"^{code}$"
                ):
                    validate_artifacts.validate_contract_artifact(artifact)

    def test_rejects_duplicate_installed_schema_versions(self) -> None:
        profile = contracts.load_schema("compatibility-profile-v1")
        duplicate = copy.deepcopy(profile)
        with mock.patch.object(
            contracts,
            "load_schema",
            side_effect=lambda name: duplicate
            if name == "sync-map-v1"
            else profile,
        ), self.assertRaisesRegex(
            ValueError, "^TRITRACK_CONTRACT_REGISTRY_INVALID$"
        ):
            contracts.contract_names_by_schema_version()

    def test_detects_late_contract_change_without_leaking_path_or_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "private-name.json"
            encoded = encode_json(VALID_CONTRACTS["grouping-v1"])
            artifact.write_bytes(encoded)
            real_validate = contracts.validate_contract

            def changing_validate(name: str, payload: object) -> None:
                real_validate(name, payload)
                artifact.write_bytes(encoded + b" ")

            with mock.patch.object(
                contracts, "validate_contract", side_effect=changing_validate
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
            ) as raised:
                validate_artifacts.validate_contract_artifact(artifact)

            message = str(raised.exception)
            self.assertNotIn(str(root), message)
            self.assertNotIn("What changed?", message)


class FcpxmlValidationTest(unittest.TestCase):
    def render(self, root: Path) -> str:
        return emit_fcpxml.render_fcpxml(
            sync_payload(),
            media(root),
            profile_id="uhd-2997-ndf-fcpxml-1.14",
            binding_id="basic-title-v1",
            metadata=emit_fcpxml.ProjectMetadata("Invented Event", "Invented Cut"),
        )

    def test_validates_exact_bytes_with_installed_profile_and_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "story.fcpxml"
            encoded = self.render(root).encode("utf-8")
            artifact.write_bytes(encoded)

            with mock.patch.object(process, "run_bounded") as subprocess_call:
                summary = validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            subprocess_call.assert_not_called()
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.validate-summary/v1",
                    "toolVersion": "0.1.0a0",
                    "artifactKind": "fcpxml",
                    "validationScope": "structural-profile",
                    "hashes": {"artifact": hashlib.sha256(encoded).hexdigest()},
                    "counts": {},
                    "details": {
                        "profileId": "uhd-2997-ndf-fcpxml-1.14",
                        "bindingId": "basic-title-v1",
                    },
                },
            )
            self.assertEqual(artifact.read_bytes(), encoded)
            self.assertNotIn(str(root), json.dumps(summary))

    def test_rejects_profile_binding_xml_and_file_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            valid = self.render(root)
            artifact = root / "story.fcpxml"
            artifact.write_text(valid, encoding="utf-8")

            for keyword, value in (
                ("profile_id", "unknown-profile"),
                ("binding_id", "unknown-binding"),
            ):
                arguments = {
                    "profile_id": "uhd-2997-ndf-fcpxml-1.14",
                    "binding_id": "basic-title-v1",
                }
                arguments[keyword] = value
                with self.subTest(keyword=keyword), self.assertRaisesRegex(
                    ValueError, "^TRITRACK_PROFILE_UNKNOWN"
                ):
                    validate_artifacts.validate_fcpxml_artifact(
                        artifact, **arguments
                    )

            artifact.write_text(
                valid.replace('width="3840"', 'width="1920"'),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_FCPXML_PROFILE_MISMATCH$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            artifact.write_bytes(b"\xff\xfe")
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_FCPXML_INVALID$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

            symlink = root / "link.fcpxml"
            symlink.symlink_to(artifact)
            with self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_UNREADABLE$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    symlink,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )

    def test_detects_late_fcpxml_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact = root / "story.fcpxml"
            valid = self.render(root)
            artifact.write_text(valid, encoding="utf-8")
            real_validate = emit_fcpxml.validate_fcpxml

            def changing_validate(*args, **kwargs) -> None:
                real_validate(*args, **kwargs)
                artifact.write_text(valid + " ", encoding="utf-8")

            with mock.patch.object(
                emit_fcpxml, "validate_fcpxml", side_effect=changing_validate
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_VALIDATE_INPUT_CHANGED$"
            ):
                validate_artifacts.validate_fcpxml_artifact(
                    artifact,
                    profile_id="uhd-2997-ndf-fcpxml-1.14",
                    binding_id="basic-title-v1",
                )


class RunValidationTest(unittest.TestCase):
    def write_aligned_bundle(self, root: Path) -> tuple[Path, bytes, dict[str, bytes]]:
        run = root / "aligned-run"
        run.mkdir()
        files = aligned_bundle_files()
        for name, encoded in files.items():
            (run / name).write_bytes(encoded)
        manifest_bytes = run_workflow.encode_manifest(aligned_manifest(files))
        (run / "run-manifest.json").write_bytes(manifest_bytes)
        return run, manifest_bytes, files

    def test_shares_complete_run_authority_and_exact_status_facts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, manifest_bytes, files = self.write_aligned_bundle(root)
            entries_before = {path.name: path.read_bytes() for path in run.iterdir()}

            bundle, status = run_workflow.inspect_run(run)
            summary = validate_artifacts.validate_run_bundle(run)

            self.assertEqual(status, run_workflow.status_run(run))
            self.assertEqual(bundle.manifest_sha256, sha256(manifest_bytes))
            self.assertEqual(
                summary,
                {
                    "schemaVersion": "tritrack.validate-summary/v1",
                    "toolVersion": "0.1.0a0",
                    "artifactKind": "run",
                    "validationScope": "complete-run-bundle",
                    "hashes": {"manifest": sha256(manifest_bytes)},
                    "counts": {"artifactCount": 2, "stageCount": 2},
                    "details": {"runSummary": status},
                },
            )
            self.assertEqual(
                entries_before,
                {path.name: path.read_bytes() for path in run.iterdir()},
            )
            self.assertEqual(
                summary["details"]["runSummary"]["artifacts"],
                {
                    "alignedTranscript": sha256(files["aligned-transcript.json"]),
                    "paperWorkbook": sha256(files["paper-edit.xlsx"]),
                },
            )
            self.assertNotIn(str(root), json.dumps(summary))
            self.assertNotIn("Invented words", json.dumps(summary))

    def test_inspection_detects_change_between_initial_load_and_recheck(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run, _, _ = self.write_aligned_bundle(root)
            real_load = run_workflow.load_bundle
            load_count = 0

            def changing_load(*args, **kwargs):
                nonlocal load_count
                loaded = real_load(*args, **kwargs)
                load_count += 1
                if load_count == 1:
                    (run / "paper-edit.xlsx").write_bytes(b"changed")
                return loaded

            with mock.patch.object(
                run_workflow, "load_bundle", side_effect=changing_load
            ), self.assertRaisesRegex(
                ValueError, "^TRITRACK_RUN_INPUT_CHANGED$"
            ):
                run_workflow.inspect_run(run)


if __name__ == "__main__":
    unittest.main()
--- END FILE tests/test_validate_artifacts.py ---

## End of frozen source evidence

Review only the exact target above.
