# Claim 5 — VERIFIED

Exact contract: in the Section 4 one-spike Gaussian experiment at `d/n=1` and 5% mean-shift contamination, literal MS-PCA recovers the uncontaminated sample PC substantially better than ordinary PCA and Robust PCA (AAP).

| n | Trials | MS-PCA mean | PCA mean | Robust PCA mean |
| ---: | ---: | ---: | ---: | ---: |
| 500 | 12 | 0.915 | 0.084 | 0.079 |
| 1000 | 12 | 0.910 | 0.110 | not run |
| 2000 | 12 | 0.996 | 0.064 | not run |

Across all 36 MS-PCA/PCA pairs, means are 0.940 and 0.086; the paired bootstrap 95% difference interval is `[0.759,0.926]`, and MS-PCA wins 94.4%. On 12 exact `rpca==0.1.6` pairs at `n=500`, Robust PCA averages 0.079; the MS-PCA difference interval is `[0.637,0.955]`, with a 91.7% win rate.

The dense eigensolver error is at most `1.51e-14`. Negative control: removing the mean shift restores PCA alignment to 1.0, so the baseline failure disappears as intended.

Verdict: **VERIFIED** within the disclosed grid. Two MS-PCA trials selected the wrong stable component, so this supports strong aggregate recovery rather than perfect per-trial consistency. The first 75-fit Robust PCA design was cancelled after more than an hour and 26 fits; the accepted exact Robust PCA comparison is therefore scoped to the 12 paired `n=500` trials.

Raw rows: [claim5_trials.csv](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/claim5_trials.csv).
