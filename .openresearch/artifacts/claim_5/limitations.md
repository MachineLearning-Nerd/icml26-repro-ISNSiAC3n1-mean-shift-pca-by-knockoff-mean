# Claim 5 limitations and deviations

The reproduction directly tests the headline `c=1`, `pi=5%` setting with the paper's 25 trials at three substantial sizes, but does not run the full 15-size, 16-setting grid or `n=10000` endpoint.

It uses literal Algorithm 1 eigenvalue matching. The released `main.py` instead matches singular values, applies the inverse eigenvalue map to a singular value, and scales the injected mean differently. That released-code behavior was separately audited in Claim 3B and is not silently substituted here.

Finite simulation can verify the reported Section 4 experiment within the tested grid; it cannot establish universal performance for every robust PCA method or distribution.
