# Historical rejected baseline

This 6.3-second verifier is preserved only as historical evidence. It is rejected as the current verifier because its imported `core.py` was missing and its dimensions and methods were not visible. Current verification: [Current claim-by-claim verification](#/current-verification).


---
<!-- trackio-cell
{"type": "code", "id": "cell_3144d189170b", "created_at": "2026-07-31T15:55:22+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 6.293}
-->
````bash
$ .venv/bin/python repro/src/verify.py
````

exit 0 · 6.3s


````python title=verify.py
"""verify.py - 5 anchored claims for ISNSiAC3n1 (arXiv 2605.25460, Mean-Shift PCA)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import core as C
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs"); os.makedirs(OUT, exist_ok=True)
v = {"paper": "ISNSiAC3n1", "arxiv": "2605.25460", "checks": {}}

r = C.claim0_thm35_spectral_separability()
v["checks"]["C0_thm35_spectral_separability"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.5 / [0]: mean-shift spikes Lambda_A and covariance spikes Lambda_P are spectrally separable (above MP bulk, disjoint)",
 "precision": f"cases (spikes above MP bulk): {r['cases']}"}

r = C.claim1_thm311_eigenspace_invariance()
v["checks"]["C1_thm311_eigenspace_invariance"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Theorem 3.11 / [1]: covariance eigenspace invariant under mean-shift contamination",
 "precision": f"alignment contaminated={r['mean_alignment_contaminated']} vs clean={r['mean_alignment_clean']} (diff {r['invariance_diff']})"}

r = C.claim2_mspca_knockoff()
v["checks"]["C2_algo1_mspca_recovers_PC"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "Algorithm 1 / [2]: MS-PCA removes the mean-shift spike, recovers the covariance PC; standard PCA biased",
 "precision": f"removed {r['mean_shift_spikes_removed']} mean-shift spike(s); MS-PCA align {r['mspca_alignment_with_true_PC']} vs PCA {r['standard_PCA_alignment_with_true_PC']}; knockoff displaces top eig {r['knockoff_displaces_top_eigenvalue_beyond_eps']}"}

r = C.claim3_fluctuations()
v["checks"]["C3_fluctuation_orders"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "[3]: Lambda_A,Lambda_P spikes fluctuate O(n^{-1/2}); spectral edge O(n^{-2/3})",
 "precision": f"spike log-log slope {r['spike_loglog_slope']} (~ -1/2); edge slope {r['edge_loglog_slope']} (< spike, ~ -2/3)"}

r = C.claim4_rpca_vs_mspca()
v["checks"]["C4_rpca_fails_mspca_recovers"] = {"status": "PASS" if r["passed"] else "FAIL",
 "anchor": "[4]: at 5% outliers d/n=1, standard & sparse-RPCA fail; MS-PCA recovers the true PC",
 "precision": f"MS-PCA align {r['mspca_alignment_5pct_outlier']} vs PCA {r['standard_PCA_alignment_5pct_outlier']} vs sparse-RPCA {r['sparse_RPCA_alignment_5pct_outlier']}"}

v["n_claims_passed"] = sum(1 for c in v["checks"].values() if c["status"] == "PASS")
v["n_claims_total"] = 5
v["all_passed"] = all(c["status"] == "PASS" for c in v["checks"].values())
json.dump(v, open(os.path.join(OUT, "verdict.json"), "w"), indent=2)
print(json.dumps(v, indent=2))
print(f"\nSUMMARY: {v['n_claims_passed']}/{v['n_claims_total']} passed, all_passed={v['all_passed']}")

````


````output
{
  "paper": "ISNSiAC3n1",
  "arxiv": "2605.25460",
  "checks": {
    "C0_thm35_spectral_separability": {
      "status": "PASS",
      "anchor": "Theorem 3.5 / [0]: mean-shift spikes Lambda_A and covariance spikes Lambda_P are spectrally separable (above MP bulk, disjoint)",
      "precision": "cases (spikes above MP bulk): [{'d/n': 1.0, 'top_spikes_above_bulk': [14.16, 10.3, 6.79], 'bulk_edge_hi': np.float64(4.0)}, {'d/n': 1.0, 'top_spikes_above_bulk': [11.35, 9.31, 6.66], 'bulk_edge_hi': np.float64(4.0)}, {'d/n': 0.5, 'top_spikes_above_bulk': [9.06, 6.17], 'bulk_edge_hi': np.float64(2.914)}]"
    },
    "C1_thm311_eigenspace_invariance": {
      "status": "PASS",
      "anchor": "Theorem 3.11 / [1]: covariance eigenspace invariant under mean-shift contamination",
      "precision": "alignment contaminated=0.903 vs clean=0.915 (diff 0.012)"
    },
    "C2_algo1_mspca_recovers_PC": {
      "status": "PASS",
      "anchor": "Algorithm 1 / [2]: MS-PCA removes the mean-shift spike, recovers the covariance PC; standard PCA biased",
      "precision": "removed 1 mean-shift spike(s); MS-PCA align 0.907 vs PCA 0.046; knockoff displaces top eig True"
    },
    "C3_fluctuation_orders": {
      "status": "PASS",
      "anchor": "[3]: Lambda_A,Lambda_P spikes fluctuate O(n^{-1/2}); spectral edge O(n^{-2/3})",
      "precision": "spike log-log slope -0.511 (~ -1/2); edge slope -0.674 (< spike, ~ -2/3)"
    },
    "C4_rpca_fails_mspca_recovers": {
      "status": "PASS",
      "anchor": "[4]: at 5% outliers d/n=1, standard & sparse-RPCA fail; MS-PCA recovers the true PC",
      "precision": "MS-PCA align 0.73 vs PCA 0.168 vs sparse-RPCA 0.161"
    }
  },
  "n_claims_passed": 5,
  "n_claims_total": 5,
  "all_passed": true
}

SUMMARY: 5/5 passed, all_passed=True

````
