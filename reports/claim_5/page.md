# Claim 5: Section 4 benchmark

This experiment tests the paper's headline 5% contamination regime at `d/n=1` using 12 trials at `n=500,1000,2000`. It compares literal Algorithm 1 against ordinary PCA at every size and the paper's pinned `rpca==0.1.6` baseline on the 12 paired `n=500` trials, with paired uncertainty, an independent eigensolver, and a contamination-off control.

The fixed command is `uv sync --frozen && uv run --no-sync python reproduce.py`; all research compute runs on Hugging Face `cpu-upgrade`, with a runtime check that no GPU device is present.

This candidate node deliberately records the scale limitation: the initial 75-fit Robust PCA design completed only 26 fits in over an hour, so the repaired design uses a calibrated subset and does not execute the official code's full 15-size, 25-trial, 16-setting grid through `n=10000`.
