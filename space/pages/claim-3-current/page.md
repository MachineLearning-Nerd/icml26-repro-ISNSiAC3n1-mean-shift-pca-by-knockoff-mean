# Claim 3 — VERIFIED

Exact contract: literal Algorithm 1 adds `A'=m' gamma'^T` with `pi'=1`, sets `theta'²=2 g^-1(lambda_tilde_1)`, and matches covariance eigenvalues within `epsilon=n^-1/2`, removing the mean spike while retaining the covariance spike.

The paper's one-spike Gaussian regime was run at `c=1`, `pi=0.05`, covariance strength 2, and mean norm `sqrt(80)`, with 12 trials at each `n=500,1000,2000`.

| n | Covariance kept | Mean removed | Joint success | Median covariance shift / epsilon | Median mean shift / epsilon |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 500 | 75% | 100% | 75% | 0.484 | 6.696 |
| 1000 | 100% | 100% | 100% | 0.174 | 11.371 |
| 2000 | 100% | 100% | 100% | 0.103 | 14.714 |

Aggregate joint success is 91.7%. A dense eigensolver agrees within `1.64e-14`. With the artificial injection set to zero, the mean eigenvalue stays matched in 100% of trials, the intended failing control.

Verdict: **VERIFIED** for the literal eigenvalue algorithm in this regime. The released repository instead matches singular values and scales the injection differently; that behavior was audited separately and is not silently substituted.

![Knockoff matching diagnostic](artifacts/current/images/claim3_matching.svg)
