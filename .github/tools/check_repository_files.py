"""Stop data, images, model weights and large files from being committed.

Once a file is committed it stays in the history, even after it's deleted, so
this check runs before each commit (pre-commit) and on every pull request.

Usage:
    python .github/tools/check_repository_files.py            # every tracked file
    python .github/tools/check_repository_files.py FILE ...   # just these files

Exit status: 0 all fine, 1 problems found.

A file that genuinely belongs in the repository (e.g. a small documentation
image) can be allowed by adding a glob pattern, with a comment saying why, to
.github/allowed-files.txt.
"""

from __future__ import annotations

import fnmatch
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = ROOT / ".github" / "allowed-files.txt"
MAX_BYTES = 1_000_000

# Microscopy images and volumes, array stores, and model weights.
DATA_SUFFIXES = {
    ".tif", ".tiff", ".czi", ".nd2", ".lif", ".lsm", ".ims", ".oib", ".oif",
    ".mrc", ".rec", ".st", ".ali", ".am", ".dm3", ".dm4",
    ".h5", ".hdf5", ".npy", ".npz",
    ".pt", ".pth", ".ckpt", ".onnx", ".safetensors",
}  # fmt: skip
# Array stores are folders, so any file inside one is data.
DATA_FOLDER_SUFFIXES = (".zarr", ".n5")


def allowed_patterns() -> list[str]:
    if not ALLOWLIST.exists():
        return []
    lines = ALLOWLIST.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def problem(path: Path, patterns: list[str], root: Path = ROOT) -> str | None:
    """Why `path` shouldn't be committed, or None if it's fine."""
    rel = path.as_posix()
    if any(fnmatch.fnmatch(rel, pattern) for pattern in patterns):
        return None
    if path.suffix.lower() in DATA_SUFFIXES:
        return "looks like image, volume or model data"
    if any(part.lower().endswith(DATA_FOLDER_SUFFIXES) for part in path.parts[:-1]):
        return "is inside a Zarr or N5 data folder"
    full = root / path
    if full.is_file() and full.stat().st_size > MAX_BYTES:
        return f"is larger than {MAX_BYTES // 1_000_000} MB"
    return None


def tracked_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    return [Path(name) for name in output.split("\0") if name]


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    paths = [Path(arg) for arg in argv] if argv else tracked_files()
    patterns = allowed_patterns()
    problems = [(path, why) for path in paths if (why := problem(path, patterns))]
    if not problems:
        return 0

    print("These files shouldn't be in the repository:\n")
    for path, why in problems:
        print(f"  {path.as_posix()}: {why}")
    print(
        "\nKeep data and large files outside git and link to them instead (see"
        " data/README.md).\nIf this is a commit you haven't made yet, unstage the"
        " file: git restore --staged <file>.\nIf it's already committed, deleting"
        " it isn't enough, because it stays in the history: ask a maintainer, or"
        " your AI assistant, to make a fresh branch without that commit.\nIf the"
        " file really belongs here, add a pattern for it to"
        " .github/allowed-files.txt, with a comment saying why."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
