# Claim 3A method

Generate the paper's one-spike Gaussian model at `c=1`, population spike `ell=2`, contamination weight `pi=0.05`, and mean norm `2 sqrt(sqrt(c)/pi)`. For each of 12 seeds at `n=500,1000,2000`, compute the five largest covariance eigenpairs, construct the exact Algorithm 1 knockoff with `pi'=1` and `theta'^2=2 g^-1(lambda_tilde_1)`, and match covariance eigenvalues within `1/sqrt(n)`.

The true covariance and mean directions identify which observed components must respectively remain and move. A dense symmetric eigensolver independently checks the iterative top-PCA result on the first instance. The negative control sets the knockoff to zero; it must retain the mean component, showing that removal is caused by the specified intervention.
