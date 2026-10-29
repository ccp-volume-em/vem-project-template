"""Tests for tools/check_repository_files.py, which keeps data out of git."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_repository_files", ROOT / "tools" / "check_repository_files.py"
)
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)


def test_this_repository_has_no_data_files():
    assert checker.main([]) == 0


@pytest.mark.parametrize(
    "path",
    ["data/stack.tif", "raw/cells.OME.TIFF", "scan.mrc", "weights/model.pth", "a/b.h5"],
)
def test_data_files_are_blocked(path, tmp_path):
    assert checker.problem(Path(path), [], root=tmp_path)


@pytest.mark.parametrize("path", ["out/labels.ome.zarr/zarr.json", "x.n5/s0/attributes.json"])
def test_files_inside_array_stores_are_blocked(path, tmp_path):
    assert "Zarr or N5" in checker.problem(Path(path), [], root=tmp_path)


def test_large_files_are_blocked(tmp_path):
    (tmp_path / "big.csv").write_bytes(b"0" * (checker.MAX_BYTES + 1))
    (tmp_path / "small.csv").write_bytes(b"0" * 100)
    assert "larger than" in checker.problem(Path("big.csv"), [], root=tmp_path)
    assert checker.problem(Path("small.csv"), [], root=tmp_path) is None


def test_code_and_docs_are_allowed(tmp_path):
    for path in ["src/vem_project/io.py", "README.md", "fiji/measure.groovy"]:
        assert checker.problem(Path(path), [], root=tmp_path) is None


def test_allowlist_patterns_override(tmp_path):
    assert checker.problem(Path("docs/images/figure.tif"), ["docs/images/*"], root=tmp_path) is None


def test_named_files_are_reported(capsys):
    assert checker.main(["data/stack.tif", "README.md"]) == 1
    output = capsys.readouterr().out
    assert "  data/stack.tif: " in output
    assert "  README.md: " not in output
