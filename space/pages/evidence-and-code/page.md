# Evidence, code, and environment

The fixed reproduction command is:

`uv sync --frozen && uv run --no-sync python reproduce.py`

Run it from the repository root. It regenerates every claim, prints the complete machine-readable evidence block, records CPU/GPU state and runtime, and exits nonzero if any scientific verifier or control fails.

Current files:

- [reproduce.py](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/reproduce.py) — complete implementation, data generation, dimensions, algorithms, thresholds, independent checkers, and controls.
- [evidence.json](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/evidence.json) — raw output from scientific commit `13b55da6455a15560c274deb9f06ce0a0214ebe0`.
- [claim5_trials.csv](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/claim5_trials.csv) — all Section 4 trial rows.
- [verify_bundle.py](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/verify_bundle.py) — independent fail-closed evidence, navigation, historical-subset, and secret checker.
- [pyproject.toml](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/pyproject.toml), [uv.lock](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/uv.lock), and [.python-version](https://huggingface.co/spaces/DineshAI/ISNSiAC3n1/resolve/main/artifacts/current/.python-version) — pinned environment.
- `artifacts/current/claims/claim_1` through `claim_5` — claim contracts, source audits, methods, limitations, and evaluator notes.

The accepted cumulative run used Hugging Face `cpu-upgrade`: estimated and selected 8 vCPUs/32 GB, actual cgroup quota 8, 64 logical CPUs visible, GPU devices absent, 472.83 seconds of scientific runtime, estimated $0.00394. The cancelled calibration run is disclosed separately and contributes no scientific result.
