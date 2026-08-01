# Command ledger

Every scientific node inherited this exact command:

```bash
uv sync --frozen && uv run --no-sync python reproduce.py
```

Every research launch used Hugging Face `cpu-upgrade`, the same CPU image, and no GPU:

```bash
orx exp run <experiment-id> --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim --timeout 1h
```

## Startup and evidence inspection

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx projects
orx runs d1aa1e8e-ddab-4e35-b65c-9f4568c43a06
orx project view d1aa1e8e-ddab-4e35-b65c-9f4568c43a06
git branch -a
git status --short
git rev-parse HEAD
git rev-parse main
df -h .
env | sed 's/=.*//' | sort
orx paper 2605.25460 --full
```

The paper HTML was retrieved with an explicit browser User-Agent and hashed with SHA-256. The verdict dataset was filtered by the exact `space_id == "DineshAI/ISNSiAC3n1"`. The judged Space revision `4e611eff62e91407b88649de06de041360679082` and the public reference logbook were cloned read-only for the protected manifest and gap audit.

## Experiment creation and launches

The campaign used `orx create-experiment ... --parent <parent-id>` for each node, then `git fetch`, `git checkout`, `git add`, `git commit`, and `git push` before launch. The exact launched experiment IDs were:

```text
2640ed80-455d-412c-8cf1-ccf797f7aa9e  baseline / Claim 1
6ebcfa39-c279-4596-941f-cfa2656afbbe  Claim 2
c947d7e2-1ad2-4232-bb1f-aa0da1460b1a  Claim 3A literal algorithm
f632dd49-5bac-4dd6-8c73-57911a8709cf  Claim 3B released-code diagnostic
8d70dce0-cdf9-4484-96d3-e533bd13f388  Claim 4 direct scaling route
96b485c6-9f47-4ee8-b1ae-d7ed2bdf38f0  Claim 4 analytical route
e38c698b-c8d5-400b-9233-2d282392b3c4  Claim 5 benchmark
e050abcb-6fcc-4dcc-88a0-359503c42818  evaluator-visible candidate
d76f1cf9-3dd3-4e82-ac7b-6f695f7a28dd  final evaluator gate
821d197d-2b4c-4103-bfd0-24af378e4428  publication manifest gate
```

After each launch:

```bash
orx exp wait <experiment-id> --timeout 480
orx logs <run-id> --bytes 200000
orx exp desc <experiment-id> --set <evidence-summary>
```

Run IDs, statuses, SHAs, and durations remain visible in the OpenResearch experiment tree and are summarized in the release report. The cancelled 75-fit Robust PCA run was stopped with `orx exp cancel e38c698b-c8d5-400b-9233-2d282392b3c4` after it yielded no complete claim evidence.
