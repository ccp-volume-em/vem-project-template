"""Check whether the CCP-volumeEM guide has changed since guidance/ was written.

Compares the guide pages recorded in guidance/source.json with the current
guide on GitHub and reports pages that are new, changed or removed. With
--diff it also prints what changed in each page.

Usage:
    python tools/check_guidance.py           # summary
    python tools/check_guidance.py --diff    # summary plus the changes

Exit status: 0 up to date, 1 the guide has changed, 2 the check failed.

Uses only the Python standard library. Set GITHUB_TOKEN (or GH_TOKEN) to
avoid GitHub's low limit on anonymous requests.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SOURCE_FILE = Path(__file__).resolve().parent.parent / "guidance" / "source.json"
API = "https://api.github.com"


def github_get(url: str) -> dict:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def current_pages(repo: str, branch: str) -> tuple[str, dict[str, str]]:
    """Return the latest commit on `branch` and {page path: blob sha}."""
    commit = github_get(f"{API}/repos/{repo}/commits/{branch}")["sha"]
    tree = github_get(f"{API}/repos/{repo}/git/trees/{commit}?recursive=1")["tree"]
    pages = {
        item["path"]: item["sha"]
        for item in tree
        if item["type"] == "blob"
        and item["path"].startswith("docs/")
        and item["path"].endswith(".md")
    }
    return commit, pages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--diff", action="store_true", help="print the changes to each page")
    args = parser.parse_args(argv)

    source = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    repo, branch = source["repository"], source["branch"]
    recorded = {path: info["sha"] for path, info in source["pages"].items()}

    try:
        commit, latest = current_pages(repo, branch)
    except (urllib.error.URLError, KeyError) as e:
        print(f"Could not read the guide from GitHub: {e}", file=sys.stderr)
        return 2

    new = sorted(latest.keys() - recorded.keys())
    removed = sorted(recorded.keys() - latest.keys())
    changed = sorted(p for p in latest.keys() & recorded.keys() if latest[p] != recorded[p])

    print(f"Guide: https://github.com/{repo} ({branch})")
    print(f"Recorded commit: {source['commit'][:7]} ({source['commit_date']})")
    print(f"Latest commit:   {commit[:7]}")
    if not (new or removed or changed):
        print("\nThe guidance is up to date.")
        return 0

    for label, paths in (("Changed", changed), ("New", new), ("Removed", removed)):
        for path in paths:
            used_in = source["pages"].get(path, {}).get("used_in", [])
            where = f"  -> update {', '.join(used_in)}" if used_in else ""
            print(f"  {label}: {path}{where}")

    if args.diff:
        try:
            compare = github_get(f"{API}/repos/{repo}/compare/{source['commit']}...{commit}")
        except urllib.error.URLError as e:
            # e.g. the recorded commit no longer exists after a history rewrite
            print(f"\nCould not fetch the diff ({e}); read the pages listed above instead.")
            return 1
        for f in compare.get("files", []):
            if f["filename"] in changed or f["filename"] in new:
                print(f"\n===== {f['filename']} ({f['status']}) =====")
                print(f.get("patch", "(no text diff available; read the page itself)"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
