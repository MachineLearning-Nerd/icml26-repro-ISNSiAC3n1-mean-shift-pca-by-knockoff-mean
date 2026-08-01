# Claim 3A evaluator contract

Run `uv sync --frozen && uv run --no-sync python reproduce.py` on Hugging Face `cpu-upgrade`. The verifier prints per-size success rates, shift-to-threshold ratios, the independent eigensolver error, control output, runtime, CPU quota, Git SHA, and seed. It exits nonzero if Claim 3A or either cumulative prior verifier fails.
