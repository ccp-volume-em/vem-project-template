"""Measurements on segmented volumes, in physical units."""

from __future__ import annotations

import math

import dask.array as da
import numpy as np

from vem_project.io import Volume


def object_volumes(labels: Volume) -> dict[int, float]:
    """Physical volume of every labelled object.

    Works chunk by chunk on dask arrays, so the label image never has to fit
    in memory.

    Parameters
    ----------
    labels : Volume
        Integer label image where 0 is background and each other value is one
        object. Must have ``z``, ``y`` and ``x`` voxel sizes.

    Returns
    -------
    dict of int to float
        Object label mapped to its volume in cubic `labels.unit`, e.g. nm³
        for ``"nanometer"``. Background (0) is not included.

    Examples
    --------
    >>> import numpy as np
    >>> cube = np.zeros((4, 4, 4), dtype=np.uint8)
    >>> cube[:2, :2, :2] = 1
    >>> object_volumes(Volume(cube, ("z", "y", "x"), {"z": 10, "y": 5, "x": 5}))
    {1: 2000.0}
    """
    if not np.issubdtype(labels.data.dtype, np.integer):
        raise TypeError(f"Labels must be integers, got {labels.data.dtype}")
    missing = {"z", "y", "x"} - labels.voxel_size.keys()
    if missing:
        raise ValueError(f"Voxel size is missing for axes {sorted(missing)}")

    data = da.asarray(labels.data)
    # Count voxels per label within each chunk, then sum the counts: this
    # avoids da.unique, which would gather all voxels into one task.
    per_chunk = data.map_blocks(_label_counts, dtype=object, chunks=(1,) * data.ndim)
    totals: dict[int, int] = {}
    for counts in per_chunk.compute().ravel():
        for label, n in counts.items():
            totals[label] = totals.get(label, 0) + n

    voxel_volume = float(math.prod(labels.voxel_size[d] for d in ("z", "y", "x")))
    return {label: n * voxel_volume for label, n in sorted(totals.items()) if label != 0}


def _label_counts(block: np.ndarray) -> np.ndarray:
    values, counts = np.unique(block, return_counts=True)
    out = np.empty((1,) * block.ndim, dtype=object)
    out.flat[0] = dict(zip(values.tolist(), counts.tolist(), strict=True))
    return out
