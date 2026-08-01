# Claim 2 — FALSIFIED

Exact contract: under Assumptions 3.1 and 3.10, every eigenvector `u` of `XX^T/n` has mean-shift perturbation residual `O_p(n^-1/2)`.

Take `X=u 1_n^T`, independent Haar mean direction `q`, and Bernoulli(1/5) membership `gamma`. The clean covariance has one eigenvalue 1 and `d-1` zeros, so its empirical spectral distribution converges to compactly supported `delta_0`. All cited assumptions hold. The exact residual converges to 0.2, so multiplying it by `sqrt(n)` diverges.

Across 200 trials per size from `n=250` to `8000`, the counterexample median stays near 0.20 with log-log slope `0.000052`. The centered alternating-right-factor control decays to `0.00323` with slope `-0.5027`.

Verdict: **FALSIFIED** under the assumptions actually cited by Theorem 3.11. If centering or isotropic right factors were intended, those are material unstated assumptions.

Code: `verify_claim_2` in the [current verifier](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/reproduce.py). Raw quantiles: Claim 2 in [evidence.json](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/evidence.json).

![Counterexample and centered control](artifacts/current/images/claim2_counterexample.svg)
