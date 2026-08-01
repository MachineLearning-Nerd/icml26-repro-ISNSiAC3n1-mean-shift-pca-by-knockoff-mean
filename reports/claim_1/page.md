# Claim 1 — exact spectral-separability audit

**Current result: FALSIFIED** for the universal claim that `Lambda_P` and `Lambda_A` are always disjoint under Theorem 3.5 assumptions.

The theorem maps both origins through `g(s)=1+s+c(1+s)/s`. At admissible `c=1/2`, `ell=theta^2=3`, both locations equal `14/3`. The assumptions are satisfied by rank-one covariance and mean shifts, i.i.d. Gaussian noise, independent Haar directions, `pi=1/5`, and `||m||^2=15`. A distinct-strength negative control at `theta^2=6/5` maps to `187/60`, leaving gap `31/20`.

This does not dispute the theorem's union/convergence formula or generic separation for unequal mapped strengths. It falsifies the stronger universal wording in the judged claim.

- Contract: `.openresearch/artifacts/claim_1/claim_contract.json`
- Source audit: `.openresearch/artifacts/claim_1/source_audit.md`
- Executable verifier: `reproduce.py`
- Fixed command: `uv sync --frozen && uv run --no-sync python reproduce.py`
- Compute: Hugging Face `cpu-upgrade`; estimated 1 core, selected 8 vCPU/32 GB; actual allocation and runtime are printed by the verifier.
