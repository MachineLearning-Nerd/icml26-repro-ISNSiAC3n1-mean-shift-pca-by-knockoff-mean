# Claim 3B method

Recreate the released numerical semantics with a converged sparse top-SVD solver on the same precommitted `c=1`, 5% contamination, one-spike Gaussian sweep as Claim 3A: 12 trials each at `n=500,1000,2000`. Classify observed components by their alignment with the true covariance and mean directions. Record retention/removal and shift-to-threshold ratios.

A dense eigensolver independently reconstructs singular values for the first instance. The executed negative control reruns the matching rule with zero injection and must retain the mean component.
