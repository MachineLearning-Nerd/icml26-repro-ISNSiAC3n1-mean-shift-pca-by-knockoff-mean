# Claim 3 source audit

Algorithm 1 computes eigenvalues of the contaminated sample covariance, adds `A'_n=m' gamma'^T`, recomputes eigenvalues, and retains an original eigenvalue if a perturbed eigenvalue lies within `epsilon=C n^-1/2`. The perturbation guidance recommends `theta'^2=2 g^-1(lambda_tilde_1)`, `pi'=0.5` or `1`, a Haar/Gaussian direction, `||m'||^2=theta'^2/pi'`, and `C=1` for large `d` (or `1/c` for small aspect ratio).

Source: ar5iv HTML retrieved 2026-08-01, SHA-256 `02f4714097d3681f770d35ed958b53bc44cddac13d97916ea1510dd08e078399`, Section 2, Algorithm 1, and the perturbation-generation guidance immediately following it.
