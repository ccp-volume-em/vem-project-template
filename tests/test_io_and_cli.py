"""Integration tests: OME-Zarr round trip and a full command-line run."""

import csv
import json

import numpy as np
import pytest

from vem_project import __version__
from vem_project.cli import main
from vem_project.io import Volume, read_ome_zarr, write_ome_zarr


@pytest.fixture
def labels_zarr(tmp_path):
    labels = np.zeros((8, 32, 32), dtype=np.uint16)
    labels[0:4, 0:8, 0:8] = 1  # 256 voxels
    path = tmp_path / "labels.ome.zarr"
    write_ome_zarr(
        Volume(labels, ("z", "y", "x"), {"z": 30.0, "y": 5.0, "x": 5.0}), path, labels=True
    )
    return path, labels


def test_round_trip_keeps_data_and_voxel_size(labels_zarr):
    path, labels = labels_zarr
    volume = read_ome_zarr(path)
    np.testing.assert_array_equal(volume.data.compute(), labels)
    assert volume.dims == ("z", "y", "x")
    assert volume.voxel_size == {"z": 30.0, "y": 5.0, "x": 5.0}
    assert volume.unit == "nanometer"


def test_pyramid_level_has_larger_voxels(labels_zarr):
    path, _ = labels_zarr
    assert read_ome_zarr(path, level=1).voxel_size == {"z": 60.0, "y": 10.0, "x": 10.0}


def test_refuses_to_overwrite(labels_zarr):
    path, labels = labels_zarr
    with pytest.raises(FileExistsError):
        write_ome_zarr(Volume(labels, ("z", "y", "x"), {"z": 1, "y": 1, "x": 1}), path)


def test_measure_command_writes_results_and_provenance(tmp_path, labels_zarr):
    params = tmp_path / "params.yml"
    params.write_text("labels: labels.ome.zarr\noutput_dir: out\n")

    assert main(["measure", str(params)]) == 0

    with open(tmp_path / "out" / "object_volumes.csv", newline="") as f:
        rows = list(csv.reader(f))
    assert rows == [["label", "volume_nanometer3"], ["1", str(256 * 30.0 * 5.0 * 5.0)]]

    provenance = json.loads((tmp_path / "out" / "provenance.json").read_text())
    assert provenance["software"]["version"] == __version__
    assert provenance["parameters"] == {"labels": "labels.ome.zarr", "output_dir": "out"}


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert __version__ in capsys.readouterr().out
