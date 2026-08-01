# Claim-by-claim logbook gap analysis

Compared revisions: judged `DineshAI/ISNSiAC3n1@4e611eff62e91407b88649de06de041360679082` and reference `arvkevi/mean-shift-pca-repro@3152498837c3abea63bef7bcc2ff7e4294341117`.

| Area | Judged DineshAI artifact | Sound reference pattern to rerun independently | Campaign requirement |
|---|---|---|---|
| Navigation | Five generic pages; weak verifier is the default | Judge-first scorecard | Put current verification first; label old pages `Historical rejected baseline` |
| Code | `verify.py` shown, but imported `core.py` absent | Downloadable source bundle and official snapshot | Show all current source inline and link individual raw files |
| Claim 1 | Unspecified dimensions; three unexplained spikes | Controlled theorem-specific model and BBP locations | Audit exact quantifier; add proof/counterexample, checker, and control |
| Claim 2 | Alignment only; no model or dimensions | 400 direct oracle-stable cases | Add exact residual contract, mixture-weight sweep, proof reconstruction, and violating-independence control |
| Claim 3 | Algorithm hidden | Released-code audit and low-`c` falsification | Run paper-text and released semantics separately; expose knockoff, threshold, and selection trace |
| Claim 4 | Slopes only; hidden horizons/trials | Explicit `n` grid and raw standard deviations | Add both spike types, edge, confidence intervals, scaled-statistic checks, and wrong-rate controls |
| Claim 5 | One aggregate number; RPCA implementation hidden | Official commit, paper grid, RPCA-AAP package | Run exact `c=1`, `pi=5%` Figure 2 regime with 25 seeds and disclosed dimensions |
| Raw evidence | Evidence page says `(no verify_run.log)` | Raw JSON with SHA-256 | Inline decisive rows plus separate CSV/JSON links and hashes |
| Reproducibility | No lock, seeds, Git SHA, CPU allocation, or cost | Protocol, official SHA, seeds, runtimes | One `uv.lock`, one fixed command, HF `cpu-upgrade`, actual CPU/runtime/cost in every run |
| Controls | None visible | Mechanistic selector failure checks | Independent checker and negative control for every claim |

Reference conclusions are not imported. Every adopted method must be reimplemented or inspected and rerun against this repository on HF CPU.
