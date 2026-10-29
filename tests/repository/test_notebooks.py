"""Notebooks are committed without outputs.

Outputs (plots, tables, printed values) can be large and can show unpublished
data. The nbstripout pre-commit hook removes them; this check catches any
committed without it.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKIP = {".venv", "venv", ".git", ".tox", "site", ".ipynb_checkpoints"}
NOTEBOOKS = sorted(p for p in ROOT.rglob("*.ipynb") if not SKIP & set(p.relative_to(ROOT).parts))


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_notebook_has_no_outputs(notebook):
    cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
    with_outputs = [
        i for i, cell in enumerate(cells, 1)
        if cell.get("outputs") or cell.get("execution_count") is not None
    ]  # fmt: skip
    assert not with_outputs, (
        f"cells {with_outputs} have saved outputs: run `pre-commit install`, or "
        f"`nbstripout {notebook.relative_to(ROOT).as_posix()}`"
    )
