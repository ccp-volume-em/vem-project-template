"""Unit tests for object volume measurement.

Each expected value is worked out by hand from the test image, not by running
the code, so the tests check the answer rather than the implementation.
"""

import dask.array as da
import numpy as np
import pytest

from vem_project.io import Volume
from vem_project.measure import object_volumes

ZYX = ("z", "y", "x")


@pytest.fixture
def two_cubes():
    labels = np.zeros((10, 20, 20), dtype=np.uint16)
    labels[0:2, 0:3, 0:4] = 1  # 2 * 3 * 4 = 24 voxels
    labels[5:10, 10:20, 10:20] = 7  # 5 * 10 * 10 = 500 voxels
    return labels


def test_known_volumes_isotropic(two_cubes):
    volume = Volume(two_cubes, ZYX, {"z": 1.0, "y": 1.0, "x": 1.0})
    assert object_volumes(volume) == {1: 24.0, 7: 500.0}


def test_anisotropic_voxels_scale_volume(two_cubes):
    # One voxel is 16 * 8 * 8 = 1024 nm³.
    volume = Volume(two_cubes, ZYX, {"z": 16.0, "y": 8.0, "x": 8.0})
    assert object_volumes(volume) == {1: 24 * 1024.0, 7: 500 * 1024.0}


def test_same_answer_across_chunks(two_cubes):
    # Object 7 spans several chunks, so its counts must be summed correctly.
    lazy = da.from_array(two_cubes, chunks=(3, 7, 7))
    volume = Volume(lazy, ZYX, {"z": 1.0, "y": 1.0, "x": 1.0})
    assert object_volumes(volume) == {1: 24.0, 7: 500.0}


def test_background_only_gives_no_objects():
    volume = Volume(np.zeros((3, 3, 3), dtype=np.uint8), ZYX, {"z": 1, "y": 1, "x": 1})
    assert object_volumes(volume) == {}


def test_float_labels_are_rejected():
    volume = Volume(np.zeros((3, 3, 3), dtype=float), ZYX, {"z": 1, "y": 1, "x": 1})
    with pytest.raises(TypeError, match="integers"):
        object_volumes(volume)


def test_missing_voxel_size_is_rejected(two_cubes):
    volume = Volume(two_cubes, ZYX, {"y": 1.0, "x": 1.0})
    with pytest.raises(ValueError, match="missing"):
        object_volumes(volume)
