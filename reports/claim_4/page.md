# Claim 4 — calibrated fluctuation scaling

**Provisional verdict before the HF run:** BLOCKED.

The verifier measures dispersion for covariance spikes, Bernoulli mean spikes, and the unspiked upper edge at six independently chosen sizes from `n=300` to `3200`, with 24 trials per size. It precommits target-covering bootstrap intervals, scaled-dispersion stability, a wrong-exponent control, and dense-eigensolver agreement.

The source audit also corrects a paper citation: the relevant largest-outlier CLT is Theorem 2.18 of arXiv:1103.2221, not “Theorem 2.19,” and its right-vector assumptions do not directly include Bernoulli membership. The empirical result therefore cannot erase that theorem-level limitation.
