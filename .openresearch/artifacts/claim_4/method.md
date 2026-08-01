# Claim 4 method

At fixed `c=0.5`, independently generate 24 Gaussian trials at each of six precommitted sizes `n=300,500,800,1250,2000,3200`. From common noise per trial, form: a covariance spike of strength 2; a Bernoulli mean spike of strength 2 with `pi=0.2`; and an unspiked edge control. Estimate the standard deviation of the largest covariance eigenvalue at each size and regress log dispersion on log size.

Use 1,000 within-size bootstrap resamples for each slope interval. Require each target exponent to lie inside its interval, scaled dispersions to remain within a factor of three, and each observed slope to be closer to its intended exponent than the deliberately wrong exponent. A dense eigensolver checks the iterative solver on all three first instances.
