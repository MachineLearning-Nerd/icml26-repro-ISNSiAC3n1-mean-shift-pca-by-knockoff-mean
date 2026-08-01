# Current claim-by-claim verification

![Headline Section 4 result](artifacts/current/images/headline.svg)

Previous live judged score: `5/10`

Conservative projected score range after this candidate: `8/10–10/10`.

Best-supported possible new score: `10/10` — forecast only, not a judge result.

This page supersedes the earlier 6.3-second verifier. That page is retained under **Historical rejected baseline**; its missing `core.py` and undisclosed scale are not used here.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | FALSIFIED | Exact above-BBP collision at `c=1/2`, `ell=theta²=3`: both locations are `14/3`; distinct-strength control separates. Risk: only universal disjointness is falsified, not Theorem 3.5's union formula. |
| 2 | 1 | 2 | HIGH | FALSIFIED | Assumption-satisfying rank-one counterexample stays at residual 0.20 through `n=8000`; centered control decays with slope -0.503. Risk: an unstated centering condition would change the theorem. |
| 3 | 1 | 2 | HIGH | VERIFIED | Literal Algorithm 1 over 36 trials at `n=500,1000,2000`: mean removed 100%, covariance retained 91.7%; dense checker and zero-injection control pass. |
| 4 | 1 | 2 | MEDIUM | VERIFIED | Machine-checked Gaussian derivation joins the correct outlier CLT, Gaussian right invariance, Bernoulli norm CLT, delta method, and edge law; BBP-threshold control is rejected. Risk: bridge is Gaussian-specific. |
| 5 | 1 | 2 | MEDIUM | VERIFIED | Exact Section 4 model: MS-PCA 0.940 vs PCA 0.086; exact `rpca==0.1.6` subset 0.079. Risk: Robust PCA is 12 paired `n=500` trials and two MS-PCA trials selected the wrong stable component. |

## Reproduction contract

- Paper: arXiv `2605.25460`, retrieved 2026-08-01 from `https://ar5iv.labs.arxiv.org/html/2605.25460`, SHA-256 `02f4714097d3681f770d35ed958b53bc44cddac13d97916ea1510dd08e078399`.
- Fixed command on every node: `uv sync --frozen && uv run --no-sync python reproduce.py`.
- Environment: Python 3.12.12, repository `.venv`, committed `pyproject.toml` and `uv.lock`.
- Compute: Hugging Face `cpu-upgrade`, selected 8 vCPU/32 GB; actual cgroup quota 8; no GPU device; accepted cumulative run 472.83 seconds, estimated $0.00394.
- Seeds: `2605254602`, `2605254603`, `2605254605`; exact-algebra claims need no random seed.
- Winning scientific revision: `13b55da6455a15560c274deb9f06ce0a0214ebe0`.

## Direct evidence

- [Executable cumulative verifier](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/reproduce.py)
- [Raw cumulative JSON](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/evidence.json)
- [Claim 5 raw trial CSV](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/claim5_trials.csv)
- [Independent fail-closed bundle checker](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/verify_bundle.py)
- [Pinned uv lock](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/uv.lock)
- [Source and method audits](#/evidence-and-code)
- [Evaluator visibility matrix](#/visibility-matrix)

The exact planned publication action, after every release gate passes, is a text-only additive upload to the existing `DineshAI/ISNSiAC3n1` Space, followed by a hash-verified redownload. No second Space will be created.
