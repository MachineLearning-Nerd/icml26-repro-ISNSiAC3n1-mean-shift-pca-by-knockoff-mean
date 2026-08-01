# Claim 3A — literal Algorithm 1

**Provisional verdict before the HF run:** BLOCKED.

This branch implements Algorithm 1 as printed: covariance eigenvalues before and after `A'_n=m' gamma'^T`, `pi'=1`, `theta'^2=2g^-1(lambda_tilde_1)`, and `epsilon=n^-1/2`. It tests the paper's `c=1`, 5% contamination, one-spike Gaussian regime at `n=500,1000,2000`, with 12 trials per size.

The verifier requires the covariance component to remain matched and the mean component to become unmatched. A dense eigensolver checks the top eigenvalues independently; a zero-knockoff control must keep the mean component.
