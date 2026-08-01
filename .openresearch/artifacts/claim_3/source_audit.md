# Claim 3B source audit

Official commit `540d660761af1d168813e6c80c6bdefcf2557217` computes singular values of `X_tilde/sqrt(n)`, passes the largest singular value to an inverse map written for covariance eigenvalues, takes the absolute value of a negative discriminant, sets `pi'=1`, and uses `norm(m')=2 sqrt(theta_hat^2/pi')`. Consequently, the injected strength is `pi'||m'||^2=4 theta_hat^2`, rather than the paper guidance `2 g^-1(lambda_tilde_1)`. It also matches singular values within `C/sqrt(n)`, whereas Algorithm 1 matches covariance eigenvalues.
