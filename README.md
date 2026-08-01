# Mean-Shift PCA by Knockoff Mean — claim-by-claim reproduction

This campaign tests all five judged claims of [arXiv 2605.25460](https://arxiv.org/abs/2605.25460). Claims 1–2 are falsified by assumption-satisfying counterexamples; Claims 3–5 are verified within explicit Gaussian and finite-grid scopes. The headline Section 4 result is MS-PCA alignment `0.940` versus PCA `0.086`; on the exact `rpca==0.1.6` subset, Robust PCA is `0.079`. The evidence is published at Hugging Face Space revision `6ab8e46c08a02600837174439705a816b5901952` and passed an exact-revision redownload check. It is awaiting a new live judge; the recorded score remains 5/10.

All research computation ran on Hugging Face `cpu-upgrade` (8-vCPU cgroup, 32 GB), never GPU. The fixed command on every experiment node was `uv sync --frozen && uv run --no-sync python reproduce.py`. The Section 4 reproduction uses 12 trials at `n=500,1000,2000`; exact Robust PCA is scoped to 12 paired `n=500` trials after a larger attempt exceeded one hour.

[Read the illustrated technical report](reports/mean-shift-pca/report.md) · [Read the release-gate report](space/artifacts/current/release/final_release_report.md) · [Open the tutorial notebook](notebooks/mean_shift_pca_reproduction.py) · [![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/blob/main/notebooks/mean_shift_pca_reproduction.py)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Publication surface | Not run as an experiment (publication surface) | README, report, notebook, and released evidence | n/a |
| [`orx/baseline-exact-claim-1-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/baseline-exact-claim-1-contract) | Exact Theorem 3.5 contract | `uv sync --frozen && uv run --no-sync python reproduce.py` | Claim 1 FALSIFIED by exact location collision | HF cpu-upgrade |
| [`orx/claim-2-exact-assumption-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/claim-2-exact-assumption-counterexample) | Theorem 3.11 assumption audit | `uv sync --frozen && uv run --no-sync python reproduce.py` | Claim 2 FALSIFIED; centered control decays at root-n | HF cpu-upgrade |
| [`orx/claim-3a-paper-text-eigenvalue-algorithm`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/claim-3a-paper-text-eigenvalue-algorithm) | Literal Algorithm 1 | `uv sync --frozen && uv run --no-sync python reproduce.py` | Claim 3 VERIFIED; 91.7% joint success | HF cpu-upgrade |
| [`orx/claim-4-calibrated-fluctuation-scaling`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/claim-4-calibrated-fluctuation-scaling) | Direct finite-size scaling | `uv sync --frozen && uv run --no-sync python reproduce.py` | BLOCKED route: edge interval and rate discriminator failed | HF cpu-upgrade |
| [`orx/claim-4-route-2-analytical-calibration`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/claim-4-route-2-analytical-calibration) | Corrected primary-source derivation | `uv sync --frozen && uv run --no-sync python reproduce.py` | Claim 4 VERIFIED in Gaussian supercritical regime | HF cpu-upgrade |
| [`orx/claim-5-exact-section-4-benchmark`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/claim-5-exact-section-4-benchmark) | Section 4 5% benchmark | `uv sync --frozen && uv run --no-sync python reproduce.py` | Claim 5 VERIFIED within disclosed grid | HF cpu-upgrade |
| [`orx/final-release-gates`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/final-release-gates) | Cumulative science and evaluator-blind release gates | `uv sync --frozen && uv run --no-sync python reproduce.py` | All science, bundle, notebook, and blind-review gates passed | HF cpu-upgrade |
| [`orx/post-publication-exact-revision-verification`](https://github.com/MachineLearning-Nerd/icml26-repro-ISNSiAC3n1-mean-shift-pca-by-knockoff-mean/tree/orx/post-publication-exact-revision-verification) | Verify exact published Space revision | `uv sync --frozen && uv run --no-sync python reproduce.py` | 83 paths, 82 hashes, 17 historical paths, bundle, and blind traversal passed | HF cpu-upgrade |

## Reproduce

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv sync --frozen
uv run --no-sync python reproduce.py
```

The command prints a complete `EVIDENCE_JSON` block and exits nonzero if any accepted claim checker or intended negative control fails. Full raw evidence and exact limitations are in the report and `.openresearch/artifacts/`.
