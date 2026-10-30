"""Check whether the project template has changed since this project used it.

A project made from the template doesn't receive the template's later
improvements (new rules, skills, checks) by itself. This script finds which
template version the project is based on, compares it with the template's
latest release (or its main branch, before the first release), and lists the
files that changed. The update-from-template skill then merges them in.

Usage:
    python tools/check_template.py               # what changed?
    python tools/check_template.py --fetch DIR   # also save the old and new
                                                 # versions of shared files
    python tools/check_template.py --init        # note the template version
                                                 # this project was made from
    python tools/check_template.py --record      # note the latest template
                                                 # version as merged

The template version in use is kept in .github/template.json. Without it, the
script asks GitHub which template the repository was made from and when.

Exit status: 0 up to date, 1 the template has changed, 2 the check failed.

Uses only the Python standard library. Set GITHUB_TOKEN (or GH_TOKEN), e.g.
GITHUB_TOKEN=$(gh auth token), to read a private template.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORD = ROOT / ".github" / "template.json"
PARTS = ROOT / ".github" / "template-parts.toml"
API = "https://api.github.com"

# Files the template maintains for every project. Everything else (code,
# README, pyproject.toml, changelog, docs) belongs to the project, so changes
# to it in the template are shown for information only.
SHARED = (
    ".agents/",
    ".github/ISSUE_TEMPLATE/",
    ".github/workflows/",
    ".github/dependabot.yml",
    ".github/pull_request_template.md",
    ".github/template-parts.toml",
    ".github/rulesets/",
    ".gitignore",
    ".dockerignore",
    ".pre-commit-config.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "REVIEWING.md",
    "SECURITY.md",
    "START_HERE.md",
    "data/README.md",
    "fiji/README.md",
    "guidance/",
    "notebooks/README.md",
    "tests/conftest.py",
    "tests/repository/",
    "tools/",
)


def is_shared(path: str) -> bool:
    return any(path == s or (s.endswith("/") and path.startswith(s)) for s in SHARED)


def left_out_files(base: dict) -> list[str]:
    """Files of the optional parts this project left out (see tools/parts.py)."""
    if not base.get("left_out") or not PARTS.exists():
        return []
    parts = tomllib.loads(PARTS.read_text(encoding="utf-8"))["parts"]
    return [f for name in base["left_out"] if name in parts for f in parts[name]["files"]]


def is_left_out(path: str, left_out: list[str]) -> bool:
    return any(path == f or path.startswith(f + "/") for f in left_out)


def github_get(path: str, raw: bool = False):
    accept = "application/vnd.github.raw" if raw else "application/vnd.github+json"
    request = urllib.request.Request(f"{API}/{path}", headers={"Accept": accept})
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    return body if raw else json.loads(body)


def repo_slug(remote_url: str) -> str:
    """owner/repo from an SSH or HTTPS GitHub remote URL."""
    match = re.search(r"github\.com[:/](.+?/.+?)(?:\.git)?/?$", remote_url)
    if not match:
        raise ValueError(f"Not a GitHub remote: {remote_url}")
    return match.group(1)


def own_slug() -> str:
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    return repo_slug(url)


def find_base() -> dict | None:
    """The template version this project is based on, or None for the template itself."""
    if RECORD.exists():
        return json.loads(RECORD.read_text(encoding="utf-8"))
    repo = github_get(f"repos/{own_slug()}")
    if not repo.get("template_repository"):
        return None
    template = repo["template_repository"]["full_name"]
    # The template's newest commit when this repository was created from it.
    commits = github_get(f"repos/{template}/commits?until={repo['created_at']}&per_page=1")
    return {"repository": template, "commit": commits[0]["sha"], "version": None}


def find_latest(template: str) -> dict:
    """The template's latest release, or its newest commit if it has none."""
    try:
        release = github_get(f"repos/{template}/releases/latest")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        commit = github_get(f"repos/{template}/commits/HEAD")["sha"]
        return {"commit": commit, "version": None}
    tag = release["tag_name"]
    commit = github_get(f"repos/{template}/commits/{tag}")["sha"]
    return {"commit": commit, "version": tag}


def describe(version: dict) -> str:
    return f"{version['version'] or 'unreleased'} ({version['commit'][:7]})"


def save(template: str, ref: str, path: str, dest: Path) -> None:
    try:
        content = github_get(f"repos/{template}/contents/{path}?ref={ref}", raw=True)
    except urllib.error.HTTPError as e:
        if e.code == 404:  # added or removed in this update
            return
        raise
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content if isinstance(content, bytes) else base64.b64decode(content))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--fetch",
        type=Path,
        metavar="DIR",
        help="save old and new template versions of shared files in DIR",
    )
    parser.add_argument(
        "--init", action="store_true", help="record the template version this project came from"
    )
    parser.add_argument(
        "--record", action="store_true", help="record the latest template version as merged"
    )
    args = parser.parse_args(argv)  # fmt: skip

    try:
        base = find_base()
        if base is None:
            print("This repository isn't made from a template (or is the template itself).")
            return 0
        template = base["repository"]
        latest = find_latest(template)
    except (urllib.error.URLError, subprocess.CalledProcessError, ValueError, KeyError) as e:
        print(f"Could not check the template: {e}", file=sys.stderr)
        return 2

    if args.init or args.record:
        version = latest if args.record else base
        record = {**version, "repository": template, "recorded": date.today().isoformat()}
        if base.get("left_out"):
            record["left_out"] = base["left_out"]
        RECORD.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(f"Recorded {template} {describe(version)} in {RECORD.relative_to(ROOT)}")
        return 0

    print(f"Template: https://github.com/{template}")
    print(f"This project is based on: {describe(base)}")
    print(f"Latest template version:  {describe(latest)}")
    if base["commit"] == latest["commit"]:
        print("\nThe project is up to date with the template.")
        return 0

    compare = github_get(f"repos/{template}/compare/{base['commit']}...{latest['commit']}")
    left_out = left_out_files(base)
    files = compare.get("files", [])
    skipped = [f for f in files if is_left_out(f["filename"], left_out)]
    files = [f for f in files if f not in skipped]
    shared = [f for f in files if is_shared(f["filename"])]
    own = [f for f in files if not is_shared(f["filename"])]

    print(f"\nShared files changed ({len(shared)}), to merge into this project:")
    for f in shared:
        print(f"  {f['status']:<9} {f['filename']}")
    print(f"\nProject files changed in the template ({len(own)}), for information only:")
    for f in own:
        print(f"  {f['status']:<9} {f['filename']}")
    if skipped:
        print(f"\nFiles of parts this project left out ({len(skipped)}), skipped:")
        for f in skipped:
            print(f"  {f['status']:<9} {f['filename']}")
    print(f"\nWhat changed: https://github.com/{template}/compare/"
          f"{base['commit'][:7]}...{latest['commit'][:7]}")  # fmt: skip

    if args.fetch:
        for f in shared:
            save(template, base["commit"], f["filename"], args.fetch / "base" / f["filename"])
            save(template, latest["commit"], f["filename"], args.fetch / "latest" / f["filename"])
        print(f"\nSaved old and new versions of the shared files in {args.fetch}/base and"
              f" {args.fetch}/latest")  # fmt: skip
    return 1


if __name__ == "__main__":
    sys.exit(main())
