"""The example notebook runs from top to bottom and gives the expected volumes."""

from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")

NOTEBOOK = Path(__file__).resolve().parent.parent / "notebooks" / "example_measure.ipynb"


def test_example_notebook_runs(tmp_path):
    nb = nbformat.read(NOTEBOOK, as_version=4)
    # Point the parameters cell at a temporary folder, so the test doesn't
    # write example data into the repository.
    params = next(c for c in nb.cells if c.cell_type == "code" and "DATA_DIR =" in c.source)
    params.source = params.source.replace('Path("../data")', f"Path({str(tmp_path)!r})")

    nbclient.NotebookClient(
        nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": NOTEBOOK.parent}}
    ).execute()

    text = "\n".join(
        str(output.get("data", {}).get("text/plain", output.get("text", "")))
        for cell in nb.cells
        for output in cell.get("outputs", [])
    )
    assert "{1: 3276800.0, 2: 19660800.0}" in text
    assert (tmp_path / "example_labels.ome.zarr").exists()
