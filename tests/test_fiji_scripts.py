"""Tests for the Fiji scripts in fiji/.

The checks on the script text run everywhere. Running a script needs Fiji,
so those tests only run when the FIJI environment variable points at the Fiji
launcher, e.g.  FIJI=/Applications/Fiji.app/fiji pytest -m fiji
"""

import csv
import json
import os
import re
import subprocess
from pathlib import Path

import numpy as np
import pytest

FIJI_DIR = Path(__file__).resolve().parent.parent / "fiji"
SCRIPTS = sorted([*FIJI_DIR.glob("*.groovy"), *FIJI_DIR.glob("*.ijm")])
FIJI = os.environ.get("FIJI")

# Dialogs that wait for a person break headless and batch runs; Script
# Parameters (#@) build the dialog instead.
BLOCKING_UI = re.compile(
    r"\b(GenericDialog|WaitForUserDialog|waitForUser|NonBlockingGenericDialog)\b"
)
# The ImageJ macro language's own dialogs and prompts.
MACRO_BLOCKING_UI = re.compile(
    r"\b(Dialog\.create|File\.openDialog|getNumber|getString|getBoolean|waitForUser)\s*\("
)


def uses_hand_built_dialogs(text, suffix):
    """Whether a script asks for input itself instead of through Script Parameters."""
    if suffix == ".ijm" and MACRO_BLOCKING_UI.search(text):
        return True
    return bool(BLOCKING_UI.search(text))


def test_there_are_fiji_scripts():
    assert SCRIPTS, "fiji/ has no .groovy or .ijm scripts"


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_inputs_are_script_parameters(script):
    lines = script.read_text().splitlines()
    assert lines[0].startswith("#@"), "inputs should be declared as #@ Script Parameters first"
    assert not uses_hand_built_dialogs(script.read_text(), script.suffix), (
        "use Script Parameters, not dialogs"
    )


@pytest.mark.parametrize(
    ("text", "suffix", "expected"),
    [
        ('#@ Double (label = "Sigma", value = 2) sigma\nrun("Gaussian Blur...");', ".ijm", False),
        ('Dialog.create("Settings");\nDialog.addNumber("Sigma", 2);', ".ijm", True),
        ('path = File.openDialog("Choose an image");', ".ijm", True),
        ('sigma = getNumber("Sigma", 2);', ".ijm", True),
        ("def gd = new GenericDialog('Settings')", ".groovy", True),
        ("#@ File inputFile\ndef props = new Properties()", ".groovy", False),
    ],
)
def test_hand_built_dialogs_are_caught(text, suffix, expected):
    assert uses_hand_built_dialogs(text, suffix) is expected


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_has_a_header_comment(script):
    assert "/*" in script.read_text(), "start with a comment saying what the script does"


def run_fiji(script, **params):
    """Run a script headless. Returns Fiji's combined output."""
    # Script errors don't change Fiji's exit status, so callers check outputs.
    args = ",".join(
        f'{k}="{v}"' if isinstance(v, str | Path) else f"{k}={str(v).lower()}"
        for k, v in params.items()
    )
    # Naming the main class works around a launcher quirk in recent Fiji that
    # reads "--run" as a macro name in headless mode; see fiji/README.md.
    cmd = [
        FIJI,
        "--headless",
        "--main-class=net.imagej.Main",
        "--",
        "--headless",
        "--run",
        str(script),
        args,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.stdout + result.stderr


@pytest.fixture
def labels_tif(tmp_path):
    import tifffile

    labels = np.zeros((10, 20, 20), dtype=np.uint16)
    labels[0:2, 0:3, 0:4] = 1  # 2 * 3 * 4 = 24 voxels
    labels[5:10, 10:20, 10:20] = 7  # 5 * 10 * 10 = 500 voxels
    path = tmp_path / "labels.tif"
    # 8 x 8 nm in-plane, 16 nm slices: one voxel is 1024 nm³.
    tifffile.imwrite(
        path,
        labels,
        imagej=True,
        resolution=(1 / 8, 1 / 8),
        metadata={"spacing": 16.0, "unit": "nm", "axes": "ZYX"},
    )
    return path


@pytest.mark.fiji
@pytest.mark.skipif(not FIJI, reason="set FIJI to the Fiji launcher to run Fiji scripts")
def test_measure_object_volumes(tmp_path, labels_tif):
    out = tmp_path / "out"
    log = run_fiji(
        FIJI_DIR / "measure_object_volumes.groovy",
        labelFile=labels_tif,
        outputDir=out,
        requireCalibration=True,
    )

    assert (out / "object_volumes.csv").exists(), log
    with open(out / "object_volumes.csv", newline="") as f:
        rows = list(csv.reader(f))
    assert rows == [["label", "volume_nm3"], ["1", "24576.0"], ["7", "512000.0"]]

    provenance = json.loads((out / "provenance.json").read_text())
    assert provenance["voxelSize"] == {"x": 8.0, "y": 8.0, "z": 16.0, "unit": "nm"}
    assert provenance["sha256"]


@pytest.mark.fiji
@pytest.mark.skipif(not FIJI, reason="set FIJI to the Fiji launcher to run Fiji scripts")
def test_uncalibrated_image_is_refused(tmp_path):
    import tifffile

    path = tmp_path / "uncalibrated.tif"
    tifffile.imwrite(
        path, np.ones((2, 8, 8), dtype=np.uint8), imagej=True, metadata={"axes": "ZYX"}
    )
    log = run_fiji(
        FIJI_DIR / "measure_object_volumes.groovy",
        labelFile=path,
        outputDir=tmp_path / "out",
        requireCalibration=True,
    )

    assert "has no voxel size" in log
    assert not (tmp_path / "out" / "object_volumes.csv").exists()


@pytest.mark.fiji
@pytest.mark.skipif(not FIJI, reason="set FIJI to the Fiji launcher to run Fiji scripts")
def test_fiji_and_python_agree_on_the_example_data(tmp_path):
    import importlib.util

    from vem_project.io import read_ome_zarr
    from vem_project.measure import object_volumes

    script = FIJI_DIR.parent / "examples" / "make_example_data.py"
    spec = importlib.util.spec_from_file_location("make_example_data", script)
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    example.main(tmp_path)

    out = tmp_path / "fiji-out"
    log = run_fiji(
        FIJI_DIR / "measure_object_volumes.groovy",
        labelFile=tmp_path / "example_labels.tif",
        outputDir=out,
        requireCalibration=True,
    )
    assert (out / "object_volumes.csv").exists(), log
    with open(out / "object_volumes.csv", newline="") as f:
        fiji = {int(row["label"]): float(row["volume_nm3"]) for row in csv.DictReader(f)}

    python = object_volumes(read_ome_zarr(tmp_path / "example_labels.ome.zarr"))
    assert fiji == python == {1: 3_276_800.0, 2: 19_660_800.0}
