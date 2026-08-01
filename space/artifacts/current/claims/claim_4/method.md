# Claim 4 route 1 — empirical method

At fixed `c=0.5`, independently generate 24 Gaussian trials at each of six precommitted sizes `n=300,500,800,1250,2000,3200`. From common noise per trial, form: a covariance spike of strength 2; a Bernoulli mean spike of strength 2 with `pi=0.2`; and an unspiked edge control. Estimate the standard deviation of the largest covariance eigenvalue at each size and regress log dispersion on log size.

Use 1,000 within-size bootstrap resamples for each slope interval. Require each target exponent to lie inside its interval, scaled dispersions to remain within a factor of three, and each observed slope to be closer to its intended exponent than the deliberately wrong exponent. A dense eigensolver checks the iterative solver on all three first instances.

This route was BLOCKED: the edge interval narrowly missed `-2/3` and the mean wrong-rate discriminator failed.

# Claim 4 route 2 — analytical method

Reconstruct the result from primary theorems. Check strict supercriticality and a nonzero spike-map derivative. For the Bernoulli mean shift, condition on membership and use Gaussian right orthogonal invariance to satisfy the additive outlier CLT; then include the root-n membership-norm fluctuation and square the singular value by the delta method. Use the spiked-Wishart CLT for covariance outliers and the white-Wishart upper-edge law for the edge. The negative control places the spike exactly at the BBP threshold, where strict supercriticality and the derivative check both fail.
