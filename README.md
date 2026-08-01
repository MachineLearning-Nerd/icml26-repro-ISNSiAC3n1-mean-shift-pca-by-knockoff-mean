# Mean-Shift PCA by Knockoff Mean — reproduction

Current research branch: cumulative exact-claim verification. Claims 1 and 2 have proof-level counterexamples; Claim 3A implements the paper's Algorithm 1 literally with covariance eigenvalue matching. See `reports/claim_1/page.md`, `reports/claim_2/page.md`, `reports/claim_3/page.md`, and `audits/logbook_gap_analysis.md`.

Fixed experiment command: `uv sync --frozen && uv run --no-sync python reproduce.py`.

All scientific execution is restricted to Hugging Face `cpu-upgrade`; GPU hardware is prohibited.
