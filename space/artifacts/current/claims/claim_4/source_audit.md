# Claim 4 source audit

The paper's “Order of Fluctuation” paragraph asserts `n^-1/2` for mean-shift and covariance outliers and `n^-2/3` for the upper edge. Its mean-spike citation to Benaych-Georges and Nadakuditi (2012), “Theorem 2.19,” is inaccurate: 2.19 is an assumption for smallest-singular-value fluctuations. The relevant largest-outlier CLT is Theorem 2.18, under Assumptions 2.1, 2.3, 2.4, 2.16, and 2.17. Those assumptions require an isotropic zero-mean right spike direction and do not directly cover Bernoulli membership.

Sources: paper ar5iv HTML retrieved 2026-08-01, SHA-256 `02f4714097d3681f770d35ed958b53bc44cddac13d97916ea1510dd08e078399`; primary reference arXiv:1103.2221v2, Sections 2.6–2.7.

Route 2 closes the Gaussian-model applicability gap by conditioning on the Bernoulli membership vector. Gaussian noise is right orthogonally invariant, so its distribution relative to a fixed normalized membership vector is the isotropic model required by the additive CLT. The membership norm itself fluctuates at root-n order; smooth spike and squaring maps preserve that order for the covariance eigenvalue.
