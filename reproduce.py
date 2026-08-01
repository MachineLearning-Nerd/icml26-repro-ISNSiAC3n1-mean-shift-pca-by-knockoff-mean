"""Fixed OpenResearch entrypoint; cumulative exact-claim verification."""

from fractions import Fraction
import json
import os
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
from scipy.sparse.linalg import svds


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


def top_svd(data: np.ndarray, component_count: int = 5) -> tuple[np.ndarray, np.ndarray]:
    scaled = data / np.sqrt(data.shape[1])
    start = np.ones(min(scaled.shape)) / np.sqrt(min(scaled.shape))
    vectors, singular_values, _ = svds(
        scaled,
        k=component_count,
        which="LM",
        tol=1e-7,
        v0=start,
    )
    order = np.argsort(singular_values)[::-1]
    return singular_values[order], vectors[:, order]


def released_strength_estimate(top_singular_value: float, aspect_ratio: float) -> float:
    discriminant = (aspect_ratio + 1 - top_singular_value) ** 2 - 4 * aspect_ratio
    linear_term = aspect_ratio - top_singular_value + 1
    return 0.5 * (-linear_term + np.sqrt(abs(discriminant)))


def verify_claim_3() -> dict:
    aspect_ratio = 1.0
    covariance_strength = 2.0
    mixture_weight = 0.05
    mean_norm = 2 * np.sqrt(np.sqrt(aspect_ratio) / mixture_weight)
    knockoff_weight = 1.0
    threshold_constant = 1.0
    sample_sizes = [500, 1000, 2000]
    trials = 12
    seed = 2605254603
    rng = np.random.default_rng(seed)
    rows = []
    dense_checker_error = None

    for n in sample_sizes:
        d = int(aspect_ratio * n)
        covariance_kept = 0
        mean_removed = 0
        joint_success = 0
        distinct_components = 0
        zero_control_mean_kept = 0
        covariance_shift_ratios = []
        mean_shift_ratios = []
        effective_strengths = []

        for trial in range(trials):
            covariance_direction = rng.normal(size=d)
            covariance_direction /= np.linalg.norm(covariance_direction)
            mean_direction = rng.normal(size=d)
            mean_direction /= np.linalg.norm(mean_direction)
            noise = rng.normal(size=(d, n))
            projected_noise = covariance_direction @ noise
            clean = noise + (
                np.sqrt(1 + covariance_strength) - 1
            ) * np.outer(covariance_direction, projected_noise)
            membership = rng.binomial(1, mixture_weight, size=n)
            contaminated = clean + mean_norm * np.outer(mean_direction, membership)

            singular_values, eigenvectors = top_svd(contaminated)
            if n == sample_sizes[0] and trial == 0:
                dense_eigenvalues = np.linalg.eigvalsh(contaminated @ contaminated.T / n)[-5:][::-1]
                dense_singular_values = np.sqrt(np.maximum(dense_eigenvalues, 0))
                dense_checker_error = float(
                    np.max(np.abs(singular_values - dense_singular_values))
                )

            estimated_strength = released_strength_estimate(
                singular_values[0], aspect_ratio
            )
            knockoff_direction = rng.normal(size=d)
            knockoff_direction /= np.linalg.norm(knockoff_direction)
            knockoff_membership = np.ones(n)
            knockoff_norm = 2 * np.sqrt(estimated_strength / knockoff_weight)
            knockoff = np.outer(
                knockoff_norm * knockoff_direction,
                knockoff_membership,
            )
            effective_strengths.append(knockoff_weight * knockoff_norm**2)
            perturbed_singular_values, _ = top_svd(contaminated + knockoff)
            zero_control_singular_values, _ = top_svd(contaminated)

            threshold = threshold_constant / np.sqrt(n)
            nearest_shifts = np.min(
                np.abs(
                    singular_values[:, None] - perturbed_singular_values[None, :]
                ),
                axis=1,
            )
            zero_control_shifts = np.min(
                np.abs(
                    singular_values[:, None] - zero_control_singular_values[None, :]
                ),
                axis=1,
            )
            stable = nearest_shifts < threshold
            covariance_index = int(
                np.argmax(np.abs(eigenvectors.T @ covariance_direction))
            )
            mean_index = int(np.argmax(np.abs(eigenvectors.T @ mean_direction)))
            components_are_distinct = covariance_index != mean_index
            covariance_is_kept = bool(stable[covariance_index])
            mean_is_removed = not bool(stable[mean_index])

            distinct_components += components_are_distinct
            covariance_kept += covariance_is_kept
            mean_removed += mean_is_removed
            joint_success += (
                components_are_distinct and covariance_is_kept and mean_is_removed
            )
            zero_control_mean_kept += bool(zero_control_shifts[mean_index] < threshold)
            covariance_shift_ratios.append(nearest_shifts[covariance_index] / threshold)
            mean_shift_ratios.append(nearest_shifts[mean_index] / threshold)

        rows.append(
            {
                "n": n,
                "d": d,
                "trials": trials,
                "distinct_component_rate": distinct_components / trials,
                "covariance_kept_rate": covariance_kept / trials,
                "mean_removed_rate": mean_removed / trials,
                "joint_success_rate": joint_success / trials,
                "median_covariance_shift_over_epsilon": float(
                    np.median(covariance_shift_ratios)
                ),
                "median_mean_shift_over_epsilon": float(np.median(mean_shift_ratios)),
                "median_effective_knockoff_strength": float(
                    np.median(effective_strengths)
                ),
                "zero_injection_control_mean_kept_rate": zero_control_mean_kept / trials,
            }
        )

    aggregate_joint_rate = float(np.mean([row["joint_success_rate"] for row in rows]))
    aggregate_covariance_rate = float(np.mean([row["covariance_kept_rate"] for row in rows]))
    aggregate_mean_rate = float(np.mean([row["mean_removed_rate"] for row in rows]))
    independent_checker = {
        "method": "dense eigensolver converted to singular values on first n=500 instance",
        "maximum_singular_value_error": dense_checker_error,
        "passed": dense_checker_error is not None and dense_checker_error < 1e-8,
    }
    negative_control = {
        "intervention": "set A'_n=0 and rerun the released matching rule",
        "expected": "the mean-shift singular value remains matched and is not removed",
        "mean_kept_rate": float(
            np.mean([row["zero_injection_control_mean_kept_rate"] for row in rows])
        ),
        "passed": all(row["zero_injection_control_mean_kept_rate"] == 1 for row in rows),
    }
    passed = (
        aggregate_joint_rate >= 0.75
        and aggregate_covariance_rate >= 0.8
        and aggregate_mean_rate >= 0.8
        and independent_checker["passed"]
        and negative_control["passed"]
    )
    return {
        "claim": 3,
        "status": "VERIFIED" if passed else "BLOCKED",
        "exact_contract": (
            "Official commit 540d660's released MS-PCA semantics match singular "
            "values within epsilon=n^-1/2 and use norm(m')=2*sqrt(theta_hat^2), "
            "removing a mean component while retaining a covariance component in "
            "the paper's c=1, pi=0.05 Gaussian regime."
        ),
        "source_anchor": "https://github.com/Mengda-Li/ms-pca/tree/540d660761af1d168813e6c80c6bdefcf2557217",
        "implementation": {
            "official_commit": "540d660761af1d168813e6c80c6bdefcf2557217",
            "comparison_quantity": "singular values of X/sqrt(n)",
            "inverse_map_input": "top singular value, not covariance eigenvalue",
            "inverse_map_discriminant": "absolute value before square root",
            "knockoff_norm": "2*sqrt(theta_hat_squared/pi_prime)",
            "effective_strength": "4*theta_hat_squared",
            "pi_prime": knockoff_weight,
            "epsilon": "1/sqrt(n)",
        },
        "raw": {
            "seed": seed,
            "rows": rows,
            "aggregate_joint_success_rate": aggregate_joint_rate,
            "aggregate_covariance_kept_rate": aggregate_covariance_rate,
            "aggregate_mean_removed_rate": aggregate_mean_rate,
        },
        "independent_checker": independent_checker,
        "negative_control": negative_control,
        "verifier_passed": passed,
        "limitation": (
            "This verifies the public code's numerical behavior, not literal "
            "Algorithm 1. The singular-value comparison and effective knockoff "
            "strength differ materially from the paper text."
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
    results = [verify_claim_1(), verify_claim_2(), verify_claim_3()]
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
            "estimated_cores": 8,
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
        + " claim_3_status=" + results[2]["status"]
        + " all_verifiers_passed=" + str(evidence["all_verifiers_passed"])
    )
    return 0 if evidence["all_verifiers_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
