"""Create a small synthetic label volume to try the tool on.

Usage:  python examples/make_example_data.py
Writes data/example_labels.ome.zarr (the data/ folder is not tracked by git).
"""

from pathlib import Path

import numpy as np

from vem_project.io import Volume, write_ome_zarr

labels = np.zeros((32, 128, 128), dtype=np.uint16)
labels[4:12, 10:30, 10:30] = 1  # 8 x 20 x 20 voxels
labels[16:28, 60:100, 60:100] = 2  # 12 x 40 x 40 voxels

out = Path(__file__).resolve().parent.parent / "data" / "example_labels.ome.zarr"
out.parent.mkdir(exist_ok=True)
# Typical anisotropic FIB-SEM voxels: 8 nm in-plane, 16 nm slice thickness.
volume = Volume(labels, ("z", "y", "x"), {"z": 16.0, "y": 8.0, "x": 8.0}, name="example labels")
write_ome_zarr(volume, out, labels=True)
print(f"Wrote {out}")
