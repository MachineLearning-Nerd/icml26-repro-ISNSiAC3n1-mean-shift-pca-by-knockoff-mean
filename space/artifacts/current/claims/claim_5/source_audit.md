# Claim 5 source audit

Paper source: arXiv 2605.25460, Section 4 and Figure 2. Retrieved from `https://ar5iv.labs.arxiv.org/html/2605.25460` on 2026-08-01; SHA-256 `02f4714097d3681f770d35ed958b53bc44cddac13d97916ea1510dd08e078399`.

The source experiment uses one Gaussian covariance spike of strength `2*sqrt(c)`, a mean vector of norm `2*sqrt(sqrt(c)/pi)`, Bernoulli mixture membership, `C=1/c`, and knockoff weight `pi'=1`. Figure 2 varies sample size and reports alignment with the uncontaminated sample's top left singular vector. The 5% claim is tested here at `c=1`, hence covariance strength 2 and mean norm `sqrt(80)`.

The official code was inspected at `Mengda-Li/ms-pca@540d660761af1d168813e6c80c6bdefcf2557217`. It specifies 25 trials and 15 logarithmic sizes from 100 through 10000, across 16 `(c, pi)` settings. Its active implementation matches singular values and passes a singular value to an inverse eigenvalue map, whereas Algorithm 1 is written in eigenvalues. The experiment therefore uses the literal paper-text Algorithm 1 already independently checked in Claim 3, and records this deviation explicitly.
