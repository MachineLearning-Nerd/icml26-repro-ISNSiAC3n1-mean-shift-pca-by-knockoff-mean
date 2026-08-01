# Claim 1 evaluation

Expected verdict: **FALSIFIED** for the imported universal spectral-separability wording. The exact theorem formula remains supported; only the stronger disjointness interpretation is contradicted.

Run: `uv sync --frozen && uv run --no-sync python reproduce.py`

The verifier exits nonzero unless the admissible equal-strength tuple collides exactly, the independent rational checker agrees, the distinct-strength negative control separates, and no GPU device is present.
