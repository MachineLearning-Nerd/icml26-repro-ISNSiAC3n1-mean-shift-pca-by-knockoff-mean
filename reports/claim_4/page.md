# Claim 4 — analytical calibration after an inconclusive sweep

**Provisional verdict before the HF run:** BLOCKED.

Route 1 measured dispersion for covariance spikes, Bernoulli mean spikes, and the unspiked upper edge at six independently chosen sizes from `n=300` to `3200`, with 24 trials per size. It was honestly BLOCKED: the edge interval narrowly missed `-2/3` and the mean wrong-exponent control failed.

Route 2 is independent and analytical. It corrects the paper citation to Theorem 2.18 of arXiv:1103.2221, conditions on Bernoulli membership, uses Gaussian right orthogonal invariance to meet the isotropic-direction premise, incorporates root-n membership-norm variation, and applies the delta method to covariance eigenvalues. A BBP-threshold control must be rejected because strict supercriticality and the spike-map derivative fail there.
