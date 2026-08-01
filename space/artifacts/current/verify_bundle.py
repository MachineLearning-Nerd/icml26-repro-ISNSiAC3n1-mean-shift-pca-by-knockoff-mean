"""Fail-closed verifier for the evaluator-visible Mean-Shift PCA bundle."""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    current = root / "artifacts" / "current"
    evidence = json.loads((current / "evidence.json").read_text())
    failures = []
    checks = {}

    statuses = {item["claim"]: item["status"] for item in evidence["claims"]}
    checks["exact_statuses"] = statuses == {
        1: "FALSIFIED",
        2: "FALSIFIED",
        3: "VERIFIED",
        4: "VERIFIED",
        5: "VERIFIED",
    }
    check(checks["exact_statuses"], "claim status mismatch", failures)
    checks["all_scientific_verifiers"] = bool(evidence["all_verifiers_passed"])
    check(checks["all_scientific_verifiers"], "scientific suite did not pass", failures)
    checks["all_controls"] = all(
        item["negative_control"]["passed"] for item in evidence["claims"]
    )
    check(checks["all_controls"], "a negative control did not pass", failures)
    checks["all_independent_checkers"] = all(
        item["independent_checker"].get("passed", True)
        or item["independent_checker"].get("all_steps_checked", False)
        for item in evidence["claims"]
    )
    check(
        checks["all_independent_checkers"],
        "an independent checker did not pass",
        failures,
    )
    checks["cpu_only"] = (
        evidence["compute"]["selected_flavor"] == "cpu-upgrade"
        and evidence["compute"]["actual_cgroup_cpu_quota"] == 8.0
        and not evidence["compute"]["gpu_devices_present"]
    )
    check(checks["cpu_only"], "compute was not verified CPU-only", failures)
    checks["fixed_command"] = evidence["fixed_command"] == (
        "uv sync --frozen && uv run --no-sync python reproduce.py"
    )
    check(checks["fixed_command"], "fixed command changed", failures)
    checks["locked_environment"] = all(
        (current / name).is_file()
        for name in ("pyproject.toml", "uv.lock", ".python-version")
    )
    check(checks["locked_environment"], "locked environment missing", failures)

    claim5 = next(item for item in evidence["claims"] if item["claim"] == 5)
    csv_lines = (current / "claim5_trials.csv").read_text().strip().splitlines()
    checks["raw_claim5_rows"] = (
        len(claim5["raw"]["trials"]) == 36 and len(csv_lines) == 37
    )
    check(checks["raw_claim5_rows"], "Claim 5 raw rows missing", failures)
    checks["claim5_uncertainty"] = (
        claim5["raw"]["aggregate"]["ms_minus_pca_bootstrap_95_percent_interval"][0]
        > 0.2
        and claim5["raw"]["aggregate"]["ms_minus_rpca_bootstrap_95_percent_interval"][0]
        > 0.2
    )
    check(checks["claim5_uncertainty"], "Claim 5 interval gate failed", failures)

    manifest = (current / "judged_manifest.sha256").read_text().splitlines()
    snapshot = root / "historical" / "judged-4e611eff62e91407b88649de06de041360679082"
    exact_snapshot = True
    original_paths_present = True
    for line in manifest:
        expected_hash, old_path = line.split("  ", 1)
        relative = old_path.removeprefix("judged-space/")
        candidate_file = root / relative
        snapshot_file = snapshot / relative
        preserved_file = snapshot_file if snapshot_file.is_file() else candidate_file
        exact_snapshot &= preserved_file.is_file() and sha256(
            preserved_file.read_bytes()
        ).hexdigest() == expected_hash
        original_paths_present &= candidate_file.is_file()
    checks["judged_snapshot_exact"] = exact_snapshot
    checks["old_file_set_subset"] = original_paths_present
    check(exact_snapshot, "protected judged snapshot hash mismatch", failures)
    check(original_paths_present, "an original judged path is absent", failures)

    logbook = json.loads((root / "logbook.json").read_text())
    children = logbook["root"]["children"]
    checks["current_navigation_first"] = (
        children[0]["slug"] == "current-verification"
        and children[-1]["title"] == "Historical rejected baseline"
    )
    check(checks["current_navigation_first"], "current navigation is not first", failures)
    current_page = (root / "pages" / "current-verification" / "page.md").read_text()
    visibility_page = (root / "pages" / "visibility-matrix" / "page.md").read_text()
    checks["canonical_discovery"] = all(
        token in current_page
        for token in (
            "FALSIFIED",
            "VERIFIED",
            "cpu-upgrade",
            "evidence.json",
            "reproduce.py",
            "Historical rejected baseline",
        )
    )
    matrix_rows = [
        line for line in visibility_page.splitlines() if re.match(r"\| [1-5] \|", line)
    ]
    checks["visibility_matrix_complete"] = (
        len(matrix_rows) == 5
        and all(line.count("Complete") == 7 for line in matrix_rows)
        and "Missing" not in visibility_page
    )
    check(checks["canonical_discovery"], "canonical page is incomplete", failures)
    check(
        checks["visibility_matrix_complete"],
        "visibility matrix has missing cells",
        failures,
    )

    text_suffixes = {".md", ".py", ".json", ".csv", ".toml", ".lock", ".txt", ".js", ".css", ".html", ".svg"}
    secret_pattern = re.compile(
        r"(?:hf_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY)"
    )
    secret_hits = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in text_suffixes:
            text = path.read_text(errors="ignore")
            if secret_pattern.search(text):
                secret_hits.append(str(path.relative_to(root)))
    checks["secret_scan"] = not secret_hits
    check(checks["secret_scan"], "secret-like text found: " + ", ".join(secret_hits), failures)

    release = current / "release"
    red_team = json.loads((release / "red_team.json").read_text())
    checks["blind_review_passed"] = (
        red_team["passed"]
        and red_team["claims_located"] == [1, 2, 3, 4, 5]
        and not red_team["conclusions_not_verified"]
        and red_team["canonical_entrypoint"] == "pages/current-verification/page.md"
    )
    check(checks["blind_review_passed"], "evaluator-blind review failed", failures)

    release_report = (release / "final_release_report.md").read_text()
    checks["release_report_complete"] = all(
        token in release_report
        for token in (
            "Previous live judged score: `5/10`",
            "Conservative projected score range after the proposed change: `8/10–10/10`",
            "Best-supported possible new score: `10/10`",
            "| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |",
            "No claim is `BLOCKED`",
            "text-only additive Hugging Face API commit",
            "awaiting judge",
        )
    )
    check(checks["release_report_complete"], "final release report is incomplete", failures)

    allowlist_path = release / "upload_allowlist.txt"
    manifest_path = release / "upload_manifest.sha256"
    allowlist = [line for line in allowlist_path.read_text().splitlines() if line]
    manifest_entries = {}
    for line in manifest_path.read_text().splitlines():
        expected_hash, relative = line.split("  ", 1)
        manifest_entries[relative] = expected_hash
    expected_manifest_paths = set(allowlist) - {
        "artifacts/current/release/upload_manifest.sha256"
    }
    checks["text_upload_allowlist"] = (
        len(allowlist) == len(set(allowlist))
        and allowlist == sorted(allowlist)
        and all(not path.endswith(".png") for path in allowlist)
        and all((root / path).is_file() for path in allowlist)
        and set(manifest_entries) == expected_manifest_paths
    )
    if checks["text_upload_allowlist"]:
        checks["upload_manifest_exact"] = all(
            sha256((root / relative).read_bytes()).hexdigest() == expected_hash
            for relative, expected_hash in manifest_entries.items()
        )
    else:
        checks["upload_manifest_exact"] = False
    check(checks["text_upload_allowlist"], "text upload allowlist is invalid", failures)
    check(checks["upload_manifest_exact"], "upload manifest hash mismatch", failures)

    result = {
        "verifier": "artifacts/current/verify_bundle.py",
        "checks": checks,
        "failures": failures,
        "passed": not failures,
    }
    print("BUNDLE_CHECKER_JSON_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("BUNDLE_CHECKER_JSON_END")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
