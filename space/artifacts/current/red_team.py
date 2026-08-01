"""Evaluator-blind traversal: inspect only the downloaded candidate bundle."""

import json
from pathlib import Path
import sys
from xml.etree import ElementTree


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    opened = []
    failures = []

    def read(relative: str) -> str:
        path = root / relative
        opened.append(relative)
        if not path.is_file():
            failures.append(f"missing: {relative}")
            return ""
        return path.read_text(errors="strict")

    manifest = json.loads(read("logbook.json"))
    first = manifest["root"]["children"][0]
    if first["slug"] != "current-verification":
        failures.append("current verifier is not the first navigation item")
    canonical = read(first["file"])
    required_canonical = [
        "Previous live judged score",
        "FALSIFIED",
        "VERIFIED",
        "Conservative projected score range",
        "cpu-upgrade",
        "Historical rejected baseline",
    ]
    for token in required_canonical:
        if token not in canonical:
            failures.append(f"canonical page omits: {token}")

    claim_pages = []
    for child in first["children"]:
        text = read(child["file"])
        if child["slug"].startswith("claim-"):
            claim_pages.append((child["slug"], text))
    if len(claim_pages) != 5:
        failures.append("five current claim pages were not discoverable")
    for slug, text in claim_pages:
        for token in ("Exact contract", "Verdict", "control"):
            if token.lower() not in text.lower():
                failures.append(f"{slug} omits {token}")

    evidence = json.loads(read("artifacts/current/evidence.json"))
    read("artifacts/current/reproduce.py")
    read("artifacts/current/verify_bundle.py")
    read("artifacts/current/claim5_trials.csv")
    read("artifacts/current/pyproject.toml")
    read("artifacts/current/uv.lock")
    read("artifacts/current/.python-version")
    read("artifacts/current/release/checker_output.json")
    for claim in range(1, 6):
        for name in (
            "claim_contract.json",
            "source_audit.md",
            "method.md",
            "limitations.md",
            "EVAL.md",
        ):
            read(f"artifacts/current/claims/claim_{claim}/{name}")
    for name in (
        "headline.svg",
        "claim1_collision.svg",
        "claim2_counterexample.svg",
        "claim3_matching.svg",
    ):
        svg = read(f"artifacts/current/images/{name}")
        try:
            root_element = ElementTree.fromstring(svg)
            if not root_element.tag.endswith("svg"):
                failures.append(f"image is not SVG: {name}")
        except ElementTree.ParseError:
            failures.append(f"image does not parse: {name}")

    statuses = {item["claim"]: item["status"] for item in evidence["claims"]}
    expected = {1: "FALSIFIED", 2: "FALSIFIED", 3: "VERIFIED", 4: "VERIFIED", 5: "VERIFIED"}
    if statuses != expected:
        failures.append("raw statuses disagree with canonical verdicts")
    if not all(item["verifier_passed"] for item in evidence["claims"]):
        failures.append("a raw claim verifier is false")

    result = {
        "review_mode": "candidate bundle and evaluator rubric only",
        "canonical_entrypoint": first["file"],
        "files_opened": opened,
        "claims_located": sorted(statuses),
        "conclusions_not_verified": failures,
        "passed": not failures,
    }
    print("RED_TEAM_JSON_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("RED_TEAM_JSON_END")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
