# Claim 2 — exact-assumption audit

**Provisional verdict before the HF run:** BLOCKED.

Theorem 3.11 cites only Assumptions 3.1 and 3.10. The verifier constructs `X=u 1_n^T`, whose sample covariance has eigenvalues `1,0,...,0` and whose empirical spectral distribution converges to compactly supported `delta_0`. An independent Bernoulli rank-one mean shift gives a residual for `u` that converges to `pi=1/5`, contradicting the stated `O_p(n^-1/2)` bound. A centered-right-factor version is the negative control.

The fixed Hugging Face run will determine whether the analytic checker, size sweep, and negative control jointly support `FALSIFIED`; otherwise the status remains `BLOCKED`.
