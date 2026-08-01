# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_68c26388ac33", "created_at": "2026-07-31T15:55:14+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 3.5 proves that mean-shift-induced spiked eigenvalues (set Λ_A) are spectrally separable from the covariance-induced spikes (set Λ_P) in high dimensions, using tools from Random Matrix Theory under the additive low-rank perturbation model (Section 3, Theorem 3.5).
2. Theorem 3.11 (Eigenspace Invariance) shows that the eigenspace of the uncontaminated sample covariance matrix remains asymptotically invariant under mean-shift mixture contamination, regardless of the mixture weight π (Section 3, Theorem 3.11).
3. The proposed two-stage Mean-Shift PCA (MS-PCA, Algorithm 1) deliberately injects an artificial knockoff mean-shift perturbation A'_n = m'γ'^T with mixture weight π' (e.g., π'=0.5 or π'=1) and threshold ϵ=Cn^(-1/2) to identify and remove the mean-shift eigenvalues while leaving covariance-induced eigenvalues invariant (Section 2, Algorithm 1).
4. Both mean-shift-induced spikes and covariance-induced spikes fluctuate at order O(n^-1/2), except the largest eigenvalue at the spectral edge which fluctuates at order O(n^-2/3), as used to set the matching threshold in the algorithm (Section 2, citing Theorem 2.19/2.16/2.15 of prior RMT results).
5. Section 4 numerical experiments show that existing Robust PCA methods fail to recover the true principal component even with only 5% outlier proportion when the aspect ratio d/n does not vanish (e.g., d/n=1), whereas MS-PCA consistently recovers it (Figure 2, Section 4).
