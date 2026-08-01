"""Verify the exact published Space revision from a fresh download."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
from urllib.parse import quote
from urllib.request import Request, urlopen


SPACE = "DineshAI/ISNSiAC3n1"
REVISION = "6ab8e46c08a02600837174439705a816b5901952"
BASE_URL = f"https://huggingface.co/spaces/{SPACE}/resolve/{REVISION}"


def download(relative: str) -> bytes:
    request = Request(
        f"{BASE_URL}/{quote(relative, safe='/')}",
        headers={"User-Agent": "OpenResearch-post-publication-verifier/1.0"},
    )
    for attempt in range(5):
        try:
            with urlopen(request, timeout=60) as response:
                return response.read()
        except Exception:
            if attempt == 4:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def main() -> int:
    local_release = Path("space/artifacts/current/release")
    allowlist_relative = "artifacts/current/release/upload_allowlist.txt"
    upload_manifest_relative = "artifacts/current/release/upload_manifest.sha256"
    judged_manifest_relative = "artifacts/current/judged_manifest.sha256"

    remote_allowlist = download(allowlist_relative)
    remote_upload_manifest = download(upload_manifest_relative)
    remote_judged_manifest = download(judged_manifest_relative)
    failures = []
    if remote_allowlist != (local_release / "upload_allowlist.txt").read_bytes():
        failures.append("published allowlist differs from the gated candidate")
    if remote_upload_manifest != (local_release / "upload_manifest.sha256").read_bytes():
        failures.append("published upload manifest differs from the gated candidate")

    allowlist = remote_allowlist.decode().splitlines()
    expected_hashes = {}
    for line in remote_upload_manifest.decode().splitlines():
        expected_hash, relative = line.split("  ", 1)
        expected_hashes[relative] = expected_hash
    preserved_paths = []
    for line in remote_judged_manifest.decode().splitlines():
        _, historical_path = line.split("  ", 1)
        preserved_paths.append(historical_path.removeprefix("judged-space/"))

    with TemporaryDirectory() as temporary:
        root = Path(temporary)
        downloaded = {}
        for relative in sorted(set(allowlist + preserved_paths)):
            content = download(relative)
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            downloaded[relative] = sha256(content).hexdigest()

        for relative, expected_hash in expected_hashes.items():
            if downloaded.get(relative) != expected_hash:
                failures.append(f"published hash mismatch: {relative}")
        if not all((root / relative).is_file() for relative in allowlist):
            failures.append("an allowlisted path is absent from the published revision")

        bundle = subprocess.run(
            [sys.executable, root / "artifacts/current/verify_bundle.py", root],
            check=False,
        )
        red_team = subprocess.run(
            [sys.executable, root / "artifacts/current/red_team.py", root],
            check=False,
        )
        if bundle.returncode:
            failures.append("published bundle verifier failed")
        if red_team.returncode:
            failures.append("published evaluator-blind traversal failed")

    result = {
        "space": SPACE,
        "revision": REVISION,
        "allowlisted_text_paths": len(allowlist),
        "manifest_hashes_checked": len(expected_hashes),
        "preserved_judged_paths_checked": len(set(preserved_paths)),
        "bundle_checker_exit_code": bundle.returncode,
        "red_team_exit_code": red_team.returncode,
        "failures": failures,
        "passed": not failures,
    }
    print("POSTPUBLICATION_JSON_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("POSTPUBLICATION_JSON_END")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
