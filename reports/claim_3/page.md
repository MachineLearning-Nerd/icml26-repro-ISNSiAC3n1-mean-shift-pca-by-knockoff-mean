# Claim 3B — released-code semantics

**Provisional verdict before the HF run:** BLOCKED.

The official code at commit `540d660` differs from Algorithm 1: it matches singular values, feeds a singular value into the covariance-eigenvalue inverse map, takes an absolute discriminant, and injects four times the estimated strength. This sibling reruns those semantics on the same seeded `c=1`, 5% contamination sweep used for the literal paper algorithm.

The result is diagnostic: even if the public implementation behaves well, the final exact-claim verdict remains grounded in Claim 3A's literal eigenvalue implementation.
