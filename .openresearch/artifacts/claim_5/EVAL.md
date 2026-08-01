# Claim 5 evaluator contract

Status before the run: PENDING.

The current verifier is `verify_claim_5` in `reproduce.py`. It emits raw per-trial JSON, summaries, confidence intervals, checker and control output between `EVIDENCE_JSON_BEGIN` and `EVIDENCE_JSON_END`. It returns nonzero if Claim 5 or any cumulative accepted claim fails.

Reviewer checklist:

- exact Section 4 `c=1`, `pi=0.05` model and parameters visible;
- 25 deterministic trials at each disclosed size;
- literal Algorithm 1, PCA, and pinned Robust PCA implementation visible;
- paired uncertainty, dense checker, and zero-contamination control visible;
- CPU quota, GPU absence, runtime, environment lock and Git SHA emitted;
- limitation against extrapolating beyond the tested grid visible.
