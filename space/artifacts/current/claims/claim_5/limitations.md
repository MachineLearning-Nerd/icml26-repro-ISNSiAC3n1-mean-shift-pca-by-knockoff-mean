# Claim 5 limitations and deviations

The reproduction directly tests the headline `c=1`, `pi=5%` setting with 12 trials at three substantial sizes. Exact `rpca==0.1.6` is evaluated on the 12 paired `n=500` cases only. The initial 75-fit design was cancelled after over an hour with only 26 fits complete and no evidence block. The accepted design does not run the full 15-size, 25-trial, 16-setting grid or `n=10000` endpoint.

It uses literal Algorithm 1 eigenvalue matching. The released `main.py` instead matches singular values, applies the inverse eigenvalue map to a singular value, and scales the injected mean differently. That released-code behavior was separately audited in Claim 3B and is not silently substituted here.

Finite simulation can verify the reported Section 4 experiment within the tested grid; it cannot establish universal performance for every robust PCA method or distribution.
