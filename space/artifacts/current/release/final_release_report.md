Previous live judged score: `5/10`

Conservative projected score range after the proposed change: `8/10–10/10`

Best-supported possible new score: `10/10` — forecast only, not a judge result

# Final release report

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | FALSIFIED | Exact assumption-satisfying collision at `14/3`; the union formula itself is not disputed. |
| 2 | 1 | 2 | HIGH | FALSIFIED | Residual stays at 0.20 through `n=8000`; an unstated centering condition would exclude the counterexample. |
| 3 | 1 | 2 | HIGH | VERIFIED | Literal Algorithm 1 removes 100% of mean spikes and jointly succeeds in 91.7% of 36 trials. |
| 4 | 1 | 2 | MEDIUM | VERIFIED | Independently reconstructed Gaussian supercritical rate derivation; the bridge is not claimed outside that scope. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | MS-PCA 0.940 versus PCA 0.086; exact Robust PCA 0.079 on 12 paired `n=500` trials. Two MS-PCA trials selected the wrong component. |

The current total remains the live judge's `5/10`. All five claims changed from historical `TOY` evidence to exact `FALSIFIED` or scoped `VERIFIED` evidence. No claim is `BLOCKED`; no claim has LOW confidence, so the mandatory three-route/fourth-falsification procedure is not triggered.

## Reproduction and compute

- Fixed command: `uv sync --frozen && uv run --no-sync python reproduce.py`.
- Environment: Python 3.12.12, one repository `.venv`, committed `pyproject.toml` and `uv.lock`.
- Compute: Hugging Face `cpu-upgrade`, estimated and selected 8 vCPU/32 GB; actual cgroup quota 8; GPU absent.
- Campaign job duration through the successful evaluator-blind gate: 7,496 seconds (2:04:56), estimated at `$0.06247` using `$0.03/hour`. This includes cancelled and failed diagnostic/setup jobs; the final packaging-gate job is reported separately with its run evidence.
- Winning scientific branch: `orx/claim-5-exact-section-4-benchmark`, Git SHA `13b55da6455a15560c274deb9f06ce0a0214ebe0`.
- Cumulative evaluator gate: `orx/final-release-gates`, Git SHA `484f586443166b8edd475e6a019f8f45cfcd5ef4`.

## Release gates

All scientific verifiers, independent checkers, and negative controls pass. Raw data regenerates from the fixed command. The exact judged 17-file tree at revision `4e611eff62e91407b88649de06de041360679082` is hash-preserved, and every old path remains present. The candidate visibility matrix has five complete rows. The evaluator-blind traversal starts only at `pages/current-verification/page.md`, locates all claims, and reports no unverifiable conclusion. The secret scan passes.

The exact publication action is a text-only additive Hugging Face API commit to the existing `DineshAI/ISNSiAC3n1` Space using `upload_allowlist.txt`; no second Space will be created. The published revision will then be downloaded afresh, every uploaded hash checked, and the canonical traversal rerun before the GitHub `main` mirror is fast-forwarded and confirmed with `git ls-remote`.

The live status after publication will be **awaiting judge**. No score increase is claimed unless the live evaluator records one.
