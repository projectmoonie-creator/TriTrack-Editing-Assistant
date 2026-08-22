Based on a thorough review of the provided evidence, implementation excerpts, and requirements:

- **Pure policy & arithmetic:** Character counting correctly includes Unicode categories `L`, `N`, and `S`. `is_sparse` correctly guards against boolean/invalid/non-positive/short (`< 30_000` ms) durations and enforces the strict `< 1.0` chars/sec threshold.
- **Retry/Adoption convergence:** `requires_retry` and `choose_source` both evaluate candidates via `source_problem()`. Usable primaries win; sparse primaries retry and yield to usable alternatives but survive as fallback (`no-better-source`); invalid/empty primaries never survive but can adopt a sparse alternative if no usable alternative exists.
- **Builder control flow:** Decoding failures and anomalies are properly classified as invalid candidates with unknown metrics, while successful decodes record exact PCM duration metrics and break early on usable takes.
- **Backward compatibility & contracts:** Additive artifact versioning (`transcription-report-v2`, `transcription-result-manifest-v2`, `run-manifest-v3`) preserves exact v1 readers while binding the deterministic density table. VAD remains hardcoded off.

NO FINDINGS