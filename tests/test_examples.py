"""The example data script makes the volume both the Python tool and Fiji read."""

import importlib.util
from pathlib import Path

import numpy as np
import tifffile

from vem_project.io import read_ome_zarr

_path = Path(__file__).resolve().parent.parent / "examples" / "make_example_data.py"
_spec = importlib.util.spec_from_file_location("make_example_data", _path)
example = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(example)


def test_writes_ome_zarr_and_tiff_with_the_same_voxel_size(tmp_path):
    example.main(tmp_path)

    volume = read_ome_zarr(tmp_path / "example_labels.ome.zarr")
    assert volume.voxel_size == {"z": 16.0, "y": 8.0, "x": 8.0}
    assert volume.unit == "nanometer"

    with tifffile.TiffFile(tmp_path / "example_labels.tif") as tif:
        assert tif.imagej_metadata["spacing"] == 16.0
        assert tif.imagej_metadata["unit"] == "nm"
        np.testing.assert_array_equal(tif.asarray(), volume.data.compute())


def test_documented_object_sizes():
    labels = example.make_labels()
    # The docstring promises these voxel counts, for checking results by hand.
    assert (labels == 1).sum() == 8 * 20 * 20
    assert (labels == 2).sum() == 12 * 40 * 40


def test_existing_files_are_left_alone(tmp_path, capsys):
    example.main(tmp_path)
    example.main(tmp_path)
    assert "already exists" in capsys.readouterr().out
