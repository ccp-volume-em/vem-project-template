"""List, remove or add the optional parts of a project.

Projects made from the template start small: the documentation site, the
container, Fiji scripts and notebooks are optional parts, described in
.github/template-parts.toml. This script handles their files the same way for
every part, and records the choice so updates from the template skip parts a
project has left out. The edits each part needs in other files (listed in
template-parts.toml) are made by hand, or by an AI assistant with the
start-project or add-part skill.

Usage:
    python tools/parts.py list             # which parts this project has
    python tools/parts.py remove container # delete a part's files
    python tools/parts.py add container    # copy them back from the template

`add` copies the files from the template version this project is based on
(recorded in .github/template.json), with the template's example names
replaced by this project's. It never overwrites a file that exists.

Uses only the Python standard library. Set GITHUB_TOKEN (or GH_TOKEN), e.g.
GITHUB_TOKEN=$(gh auth token), to read a private template.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tomllib
import urllib.error
import urllib.request
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
PARTS = Path(".github/template-parts.toml")
RECORD = Path(".github/template.json")
NOTES_HEADING = "## Project-specific notes"

# The template's example names, replaced by the project's own in added files.
TEMPLATE_SLUG = "ccp-volume-em/vem-project"
TEMPLATE_NAME = "vem-project"
TEMPLATE_PACKAGE = "vem_project"
# Text that only makes sense in the template itself (see start-project).
TEMPLATE_ONLY = re.compile(
    r"<!-- template-(?:status|example):start -->.*?<!-- template-(?:status|example):end -->\n\n?",
    re.DOTALL,
)


def load_parts(root: Path) -> dict:
    return tomllib.loads((root / PARTS).read_text(encoding="utf-8"))["parts"]


def load_record(root: Path) -> dict:
    if not (root / RECORD).exists():
        raise SystemExit(
            f"{RECORD} is missing. In a project made from the template, run "
            "`python tools/check_template.py --init` first. (Parts aren't "
            "removed from the template itself.)"
        )
    return json.loads((root / RECORD).read_text(encoding="utf-8"))


def save_record(root: Path, record: dict) -> None:
    (root / RECORD).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def status(root: Path, part: dict) -> str:
    present = [(root / f).exists() for f in part["files"]]
    return "included" if all(present) else "left out" if not any(present) else "partly"


def note_line(name: str, part: dict) -> str:
    return f"- Left out: {part['title']} (`{name}`). Add it with the add-part skill."


def set_note(root: Path, name: str, part: dict, left_out: bool) -> None:
    """Add or remove the AGENTS.md note saying the part was left out on purpose."""
    agents = root / "AGENTS.md"
    if not agents.exists():
        return
    text = agents.read_text(encoding="utf-8")
    line = note_line(name, part)
    if left_out and line not in text:
        if NOTES_HEADING in text:
            text = text.rstrip("\n")
            # A blank line before the first list item, none between items.
            gap = "\n" if text.splitlines()[-1].startswith("- ") else "\n\n"
            text = text + gap + line + "\n"
        else:
            text = text.rstrip("\n") + f"\n\n{NOTES_HEADING}\n\n{line}\n"
    elif not left_out:
        text = text.replace(line + "\n", "")
    agents.write_text(text, encoding="utf-8")


def set_left_out(root: Path, name: str, part: dict, left_out: bool) -> None:
    record = load_record(root)
    names = set(record.get("left_out", []))
    names = names | {name} if left_out else names - {name}
    record["left_out"] = sorted(names)
    save_record(root, record)
    set_note(root, name, part, left_out)


def print_edits(part: dict, adding: bool) -> None:
    verb = "Undo these edits, using the template's version" if adding else "Now make these edits"
    print(f"\n{verb}:")
    for edit in part["edits"]:
        print(f"  - {edit}")
    if adding and part.get("after_add"):
        print(f"\nThen: {part['after_add']}")


def remove(root: Path, name: str) -> None:
    part = load_parts(root)[name]
    load_record(root)  # fail before deleting anything
    for f in part["files"]:
        path = root / f
        if path.is_dir():
            shutil.rmtree(path)
            print(f"Deleted {f}/")
        elif path.exists():
            path.unlink()
            print(f"Deleted {f}")
    set_left_out(root, name, part, left_out=True)
    print(f"Recorded {name} as left out in {RECORD} and AGENTS.md.")
    print_edits(part, adding=False)


def project_names(root: Path) -> dict[str, str]:
    """The project's own names, to replace the template's examples with."""
    pyproject = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    name = pyproject["project"]["name"]
    packages = [p.parent.name for p in (root / "src").glob("*/__init__.py")]
    names = {
        TEMPLATE_NAME: name,
        TEMPLATE_PACKAGE: packages[0] if len(packages) == 1 else name.replace("-", "_"),
    }
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        slug = re.search(r"github\.com[:/](.+?/.+?)(?:\.git)?/?$", url)
        if slug:
            names[TEMPLATE_SLUG] = slug.group(1)
    except (OSError, subprocess.CalledProcessError):
        pass
    return names


def adapt(content: bytes, names: dict[str, str]) -> bytes:
    """Replace the template's example names, and drop template-only notes."""
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return content
    text = TEMPLATE_ONLY.sub("", text)
    # Longest first, and never inside a link to the template itself.
    for old in sorted(names, key=len, reverse=True):
        text = re.sub(re.escape(old) + r"(?!-template)", names[old], text)
    return text.encode("utf-8")


def download(repository: str, commit: str) -> bytes:
    request = urllib.request.Request(f"https://codeload.github.com/{repository}/tar.gz/{commit}")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def add(root: Path, name: str, archive: bytes | None = None) -> None:
    part = load_parts(root)[name]
    record = load_record(root)
    if archive is None:
        try:
            archive = download(record["repository"], record["commit"])
        except (urllib.error.URLError, KeyError) as e:
            raise SystemExit(f"Could not download the template: {e}") from e
    names = project_names(root)
    wanted = [PurePosixPath(f) for f in part["files"]]
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        for member in tar.getmembers():
            # Paths in GitHub's archive start with a <repo>-<commit>/ folder.
            rel = PurePosixPath(*PurePosixPath(member.name).parts[1:])
            if not member.isfile() or ".." in rel.parts:
                continue
            if not any(rel == w or w in rel.parents for w in wanted):
                continue
            dest = root / rel
            if dest.exists():
                print(f"Kept {rel} (it already exists)")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(adapt(tar.extractfile(member).read(), names))
            print(f"Added {rel}")
    set_left_out(root, name, part, left_out=False)
    print_edits(part, adding=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="list the optional parts and whether this project has them")
    for command in ("remove", "add"):
        sub.add_parser(command, help=f"{command} a part").add_argument("part")
    args = parser.parse_args(argv)

    parts = load_parts(ROOT)
    if args.command == "list":
        for name, part in parts.items():
            print(f"{name:<10} {status(ROOT, part):<9} {part['title']}")
        return 0
    if args.part not in parts:
        print(f"No part called {args.part!r}. Parts: {', '.join(parts)}", file=sys.stderr)
        return 2
    (remove if args.command == "remove" else add)(ROOT, args.part)
    return 0


if __name__ == "__main__":
    sys.exit(main())
