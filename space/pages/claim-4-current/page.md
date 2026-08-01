# Claim 4 — VERIFIED

Exact contract: in the paper's supercritical Gaussian covariance and Bernoulli mean-shift models, isolated eigenvalues fluctuate at order `n^-1/2`, while the unspiked upper edge fluctuates at `n^-2/3`.

The first empirical route was inconclusive: fitted slopes were -0.440 (covariance), -0.608 (mean), and -0.806 (edge); the edge interval narrowly missed -2/3 and the mean wrong-rate discriminator failed. It is retained as a rejected route, not upgraded to a pass.

The accepted route machine-checks the exact Gaussian chain:

1. Strength 2 is strictly above `sqrt(1/2)` and `g(2)=15/4` is separated from the edge 2.9142.
2. The spiked-Wishart outlier CLT gives the covariance root-n rate.
3. Conditional Gaussian right-orthogonal invariance makes normalized Bernoulli membership distributionally compatible with the additive outlier CLT.
4. Its random norm contributes another root-n term; a smooth delta method preserves that rate for the eigenvalue.
5. The white-Wishart upper-edge law gives the `n^-2/3` rate.

The paper cites Benaych-Georges–Nadakuditi Theorem 2.19, but 2.19 is an assumption for the smallest singular value. The applicable largest-outlier result is Theorem 2.18. At the BBP threshold, strict supercriticality fails and the map derivative is zero; the negative control is correctly rejected.

Verdict: **VERIFIED** for the paper's Gaussian supercritical regime. The derivation does not extend this conclusion to arbitrary non-Gaussian noise or critical spikes.
