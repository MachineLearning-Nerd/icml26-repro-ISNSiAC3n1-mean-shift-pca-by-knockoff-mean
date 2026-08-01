# Claim 5: Section 4 benchmark

This experiment tests the paper's headline 5% contamination regime at `d/n=1` using 25 trials at `n=500,1000,2000`. It compares literal Algorithm 1 against ordinary PCA and the paper's pinned `rpca==0.1.6` baseline, with paired uncertainty, an independent eigensolver, and a contamination-off control.

The fixed command is `uv sync --frozen && uv run --no-sync python reproduce.py`; all research compute runs on Hugging Face `cpu-upgrade`, with a runtime check that no GPU device is present.

This candidate node deliberately records the scale limitation: it does not execute the official code's full 15-size, 16-setting grid through `n=10000`.
