# Claim 1 — FALSIFIED

Exact contract: for every tuple satisfying Theorem 3.5's assumptions, the covariance-induced set `Lambda_P` and mean-induced set `Lambda_A` are disjoint and therefore separable by asymptotic location.

At `c=1/2`, choose covariance strength `ell=3`, mean strength `theta²=3`, mixture weight `pi=1/5`, and mean norm squared 15. Both strengths are strictly above the BBP threshold. Exact rational evaluation of `g(x)=1+x+c(1+x)/x` gives

`g(ell)=g(theta²)=14/3`.

The independent cross-product checker is exactly zero. A negative control with `theta²=6/5` gives `187/60`, separated from `14/3` by `31/20`; it does not trigger falsification.

Verdict: **FALSIFIED** for universal disjointness. This does not dispute Theorem 3.5's union/convergence formula or generic separation at unequal mapped strengths.

Source: Theorem 3.5. Code: `verify_claim_1` in the [current verifier](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/reproduce.py). Raw output: Claim 1 in [evidence.json](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/evidence.json).

![Exact location collision](artifacts/current/images/claim1_collision.svg)
