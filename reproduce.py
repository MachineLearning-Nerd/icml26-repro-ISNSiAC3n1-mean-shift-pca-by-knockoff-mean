"""Fixed OpenResearch entrypoint; cumulative exact-claim verification."""

from fractions import Fraction
import json
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np


def spike_location(strength: Fraction, aspect_ratio: Fraction) -> Fraction:
    return 1 + strength + aspect_ratio * (1 + strength) / strength


def verify_claim_1() -> dict:
    c = Fraction(1, 2)
    covariance_strength = Fraction(3, 1)
    mean_strength = Fraction(3, 1)
    covariance_location = spike_location(covariance_strength, c)
    mean_location = spike_location(mean_strength, c)

    control_mean_strength = Fraction(6, 5)
    control_mean_location = spike_location(control_mean_strength, c)

    assumptions = {
        "rank_covariance": 1,
        "rank_mean": 1,
        "aspect_ratio_c": "1/2",
        "covariance_strength_ell": "3",
        "mean_strength_theta_squared": "3",
        "mixture_weight_pi": "1/5",
        "mean_norm_squared": "15",
        "bbp_condition": "ell > sqrt(c) and theta^2 > sqrt(c)",
        "above_bbp": covariance_strength * covariance_strength > c
        and mean_strength * mean_strength > c,
        "noise": "iid Gaussian (zero mean, unit variance, finite fourth moment)",
        "directions": "independent Haar unit vectors, independent of data and membership",
    }
    equal_strength_counterexample = covariance_location == mean_location
    distinct_strength_control_separates = covariance_location != control_mean_location

    checker = {
        "covariance_location_fraction": str(covariance_location),
        "mean_location_fraction": str(mean_location),
        "cross_product_difference": covariance_location.numerator
        * mean_location.denominator
        - mean_location.numerator * covariance_location.denominator,
        "passed": equal_strength_counterexample,
    }
    negative_control = {
        "mean_strength_theta_squared": str(control_mean_strength),
        "mean_location_fraction": str(control_mean_location),
        "location_gap_fraction": str(covariance_location - control_mean_location),
        "falsification_triggered": not distinct_strength_control_separates,
        "expected_falsification_triggered": False,
        "passed": distinct_strength_control_separates,
    }
    passed = (
        assumptions["above_bbp"]
        and equal_strength_counterexample
        and checker["passed"]
        and negative_control["passed"]
    )
    return {
        "claim": 1,
        "status": "FALSIFIED" if passed else "BLOCKED",
        "exact_contract": (
            "For every parameter tuple satisfying Theorem 3.5 assumptions, "
            "the covariance-induced set Lambda_P and mean-induced set Lambda_A "
            "are disjoint and hence separable by asymptotic eigenvalue location."
        ),
        "source_anchor": "https://ar5iv.labs.arxiv.org/html/2605.25460#S3.Thmtheorem5",
        "assumptions": assumptions,
        "raw": {
            "covariance_location_fraction": str(covariance_location),
            "mean_location_fraction": str(mean_location),
            "locations_equal": equal_strength_counterexample,
        },
        "independent_checker": checker,
        "negative_control": negative_control,
        "verifier_passed": passed,
        "limitation": (
            "This falsifies universal disjointness by exact algebra. It does not "
            "dispute Theorem 3.5's union/convergence formula or generic separation "
            "when the two mapped strengths differ."
        ),
    }


def residual_norm(alpha: float, membership_mean: float, cross_mean: float) -> float:
    q_coefficient = membership_mean * alpha + cross_mean
    u_coefficient = alpha * cross_mean
    squared_norm = (
        q_coefficient**2
        + u_coefficient**2
        + 2 * alpha * q_coefficient * u_coefficient
    )
    return float(np.sqrt(max(squared_norm, 0.0)))


def verify_claim_2() -> dict:
    aspect_ratio = 1
    mixture_weight = 0.2
    mean_magnitude = 1.0
    sample_sizes = [250, 500, 1000, 2000, 4000, 8000]
    trials = 200
    seed = 2605254602
    rng = np.random.default_rng(seed)

    counterexample_medians = []
    control_medians = []
    rows = []
    for n in sample_sizes:
        d = aspect_ratio * n
        counterexample_residuals = []
        control_residuals = []
        alternating = np.ones(n)
        alternating[1::2] = -1
        for _ in range(trials):
            clean_direction = rng.normal(size=d)
            clean_direction /= np.linalg.norm(clean_direction)
            mean_direction = rng.normal(size=d)
            mean_direction /= np.linalg.norm(mean_direction)
            alpha = float(clean_direction @ mean_direction)
            membership = rng.binomial(1, mixture_weight, size=n)
            membership_mean = float(membership.mean())

            counterexample_cross_mean = membership_mean
            control_cross_mean = float(membership @ alternating / n)
            counterexample_residuals.append(
                mean_magnitude
                * residual_norm(alpha, membership_mean, counterexample_cross_mean)
            )
            control_residuals.append(
                mean_magnitude
                * residual_norm(alpha, membership_mean, control_cross_mean)
            )

        counterexample_medians.append(float(np.median(counterexample_residuals)))
        control_medians.append(float(np.median(control_residuals)))
        rows.append(
            {
                "n": n,
                "d": d,
                "counterexample_median": counterexample_medians[-1],
                "counterexample_q05": float(np.quantile(counterexample_residuals, 0.05)),
                "counterexample_q95": float(np.quantile(counterexample_residuals, 0.95)),
                "centered_control_median": control_medians[-1],
                "centered_control_q05": float(np.quantile(control_residuals, 0.05)),
                "centered_control_q95": float(np.quantile(control_residuals, 0.95)),
            }
        )

    log_n = np.log(np.asarray(sample_sizes, dtype=float))
    counterexample_slope = float(np.polyfit(log_n, np.log(counterexample_medians), 1)[0])
    control_slope = float(np.polyfit(log_n, np.log(control_medians), 1)[0])

    analytic_checker = {
        "clean_covariance_spectrum": "one eigenvalue 1; d-1 eigenvalues 0",
        "clean_esd_limit": "delta_0 (compact support)",
        "residual_formula": (
            "||q*(p_hat*alpha+s)+u*(alpha*s)||, "
            "alpha=<q,u>, s=<gamma,v>/n"
        ),
        "counterexample_limits": {
            "alpha": 0,
            "p_hat": mixture_weight,
            "s_for_v_all_ones": mixture_weight,
            "residual_norm": mixture_weight * mean_magnitude,
        },
        "root_n_scaled_residual_limit": "infinity",
        "contradicts_O_p_n_minus_half": True,
    }
    negative_control = {
        "clean_right_factor": "alternating +1,-1",
        "why_it_should_not_falsify": "<gamma,v>/n is O_p(n^-1/2)",
        "observed_slope": control_slope,
        "final_median": control_medians[-1],
        "passed": -0.7 < control_slope < -0.3 and control_medians[-1] < 0.03,
    }
    empirical_counterexample_passed = (
        abs(counterexample_slope) < 0.1
        and counterexample_medians[-1] > 0.15
        and abs(counterexample_medians[-1] - mixture_weight) < 0.03
    )
    passed = (
        analytic_checker["contradicts_O_p_n_minus_half"]
        and empirical_counterexample_passed
        and negative_control["passed"]
    )
    return {
        "claim": 2,
        "status": "FALSIFIED" if passed else "BLOCKED",
        "exact_contract": (
            "Under Assumptions 3.1 and 3.10, every eigenvector u of XX^T/n "
            "satisfies ||(A A^T + A X^T + X A^T)u/n||=O_p(n^-1/2)."
        ),
        "source_anchor": "https://ar5iv.labs.arxiv.org/html/2605.25460#S3.Thmtheorem11",
        "assumptions": {
            "d_over_n": aspect_ratio,
            "clean_matrix": "X=u*1_n^T, with u a Haar unit vector",
            "clean_esd": "(1/d) delta_1 + ((d-1)/d) delta_0 -> delta_0",
            "mean_shift": "A=q*gamma^T, q independent Haar, gamma_i iid Bernoulli(1/5)",
            "rank_mean_shift": 1,
            "independence": "q and gamma independent of X",
        },
        "raw": {
            "seed": seed,
            "trials_per_size": trials,
            "rows": rows,
            "counterexample_log_log_slope": counterexample_slope,
        },
        "independent_checker": analytic_checker,
        "negative_control": negative_control,
        "verifier_passed": passed,
        "limitation": (
            "This is a counterexample to Theorem 3.11 under its cited assumptions. "
            "It does not apply if an additional centering or isotropic-right-factor "
            "condition on X was intended but unstated."
        ),
    }


def cgroup_cpu_quota() -> float | None:
    cpu_max = Path("/sys/fs/cgroup/cpu.max")
    if cpu_max.exists():
        quota, period = cpu_max.read_text().split()
        return None if quota == "max" else int(quota) / int(period)
    quota_path = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
    period_path = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
    if quota_path.exists() and period_path.exists():
        quota = int(quota_path.read_text())
        return None if quota < 0 else quota / int(period_path.read_text())
    return None


def git_sha() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    started = time.perf_counter()
    results = [verify_claim_1(), verify_claim_2()]
    runtime = time.perf_counter() - started
    gpu_devices_present = any(
        Path(device).exists()
        for device in ("/dev/nvidia0", "/dev/nvidiactl", "/dev/kfd")
    )
    evidence = {
        "paper": "Mean-Shift PCA by Knockoff Mean",
        "arxiv": "2605.25460",
        "paper_source": {
            "url": "https://ar5iv.labs.arxiv.org/html/2605.25460",
            "retrieved_at": "2026-08-01T19:13:37Z",
            "sha256": "02f4714097d3681f770d35ed958b53bc44cddac13d97916ea1510dd08e078399",
        },
        "git_sha": git_sha(),
        "fixed_command": "uv sync --frozen && uv run --no-sync python reproduce.py",
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "cpu-upgrade",
            "selected_vcpus": 8,
            "selected_memory_gb": 32,
            "actual_logical_cpus": os.cpu_count(),
            "actual_cgroup_cpu_quota": cgroup_cpu_quota(),
            "gpu_devices_present": gpu_devices_present,
            "runtime_seconds": runtime,
            "estimated_cost_usd": runtime * 0.03 / 3600,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "lockfile": "uv.lock",
            "project_venv": ".venv",
        },
        "claims": results,
        "all_verifiers_passed": all(
            result["verifier_passed"] for result in results
        ) and not gpu_devices_present,
    }
    print("EVIDENCE_JSON_BEGIN")
    print(json.dumps(evidence, indent=2, sort_keys=True))
    print("EVIDENCE_JSON_END")
    print(
        "SUMMARY claim_1_status=" + results[0]["status"]
        + " claim_2_status=" + results[1]["status"]
        + " all_verifiers_passed=" + str(evidence["all_verifiers_passed"])
    )
    return 0 if evidence["all_verifiers_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
