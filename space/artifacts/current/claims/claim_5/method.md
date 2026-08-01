# Claim 5 method

For each of 12 deterministic trials at `n=d` in `{500,1000,2000}`, generate the paper's exact one-spike Gaussian sample, add an independent rank-one Bernoulli mean shift with `pi=0.05`, and measure alignment to the uncontaminated sample PC. Run the exact Robust PCA baseline on all 12 paired `n=500` trials; MS-PCA and PCA run at every size.

Methods are literal Algorithm 1 eigenvalue matching (`pi'=1`, `C=1`), ordinary contaminated-sample PCA, and `rpca==0.1.6` `RobustPCA(n_components=1)` using `low_rank_[:,0]`, exactly as the official comparison code. Report every trial, per-size means, medians and 5–95% intervals, paired win rates, and paired bootstrap 95% confidence intervals. The Robust PCA subset was calibrated after the initial 75-fit design completed only 26 fits in over one hour and emitted no claim result.

The independent checker compares the iterative top eigensolver with a dense symmetric eigensolver on the first `n=500` case. The negative control removes the mean shift; ordinary PCA must then equal the clean reference PC, so the reported baseline failure must disappear.

Fixed command: `uv sync --frozen && uv run --no-sync python reproduce.py`.

Compute estimate: 8 CPU cores, 32 GB RAM, up to one hour. Selected target: Hugging Face `cpu-upgrade` (8 vCPU); GPU devices are prohibited and checked at runtime.
