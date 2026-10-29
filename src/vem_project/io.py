"""Read and write volumes as OME-Zarr, keeping their physical metadata.

OME-Zarr (also called NGFF) is the community format for large bioimaging
data. Reading is lazy: you get a dask array, and voxels are only loaded from
disk when a calculation needs them, so volumes larger than memory still work.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import dask.array as da
import ngff_zarr as nz
import numpy as np


@dataclass
class Volume:
    """Image or label data together with the metadata needed to interpret it.

    Keeping voxel size and units next to the data means measurements can be
    reported in physical units, and the metadata is not lost when results
    are written back out.

    Parameters
    ----------
    data : dask.array.Array or numpy.ndarray
        Voxel values, with axes in the order given by `dims`.
    dims : tuple of str
        Axis names, e.g. ``("z", "y", "x")``.
    voxel_size : dict of str to float
        Size of one voxel along each spatial axis, in `unit`.
    unit : str
        Physical unit of `voxel_size`, as an OME-Zarr unit name such as
        ``"nanometer"``.
    name : str
        Short name stored in the OME-Zarr metadata.
    """

    data: da.Array | np.ndarray
    dims: tuple[str, ...]
    voxel_size: dict[str, float]
    unit: str = "nanometer"
    name: str = "image"


def read_ome_zarr(path: str | Path, level: int = 0) -> Volume:
    """Open one resolution level of an OME-Zarr image without loading it.

    Parameters
    ----------
    path : str or pathlib.Path
        Local path or URL of the ``.ome.zarr`` store.
    level : int
        Pyramid level, where 0 is full resolution and higher levels are
        progressively downsampled.

    Returns
    -------
    Volume
        Lazy (dask) data with the voxel size and unit of that level.
    """
    multiscales = nz.from_ngff_zarr(str(path))
    image = multiscales.images[level]
    spatial = [d for d in image.dims if d in ("z", "y", "x")]
    units = {image.axes_units[d] for d in spatial} if image.axes_units else {None}
    if len(units) != 1:
        # Mixed units would silently corrupt volume calculations downstream.
        raise ValueError(f"Spatial axes use different units: {image.axes_units}")
    return Volume(
        data=image.data,
        dims=tuple(image.dims),
        voxel_size={d: float(image.scale[d]) for d in spatial},
        unit=units.pop() or "unknown",
        name=image.name,
    )


def write_ome_zarr(
    volume: Volume,
    path: str | Path,
    scale_factors: list[int] | None = None,
    labels: bool = False,
) -> None:
    """Write a volume as OME-Zarr with a multiscale pyramid.

    Parameters
    ----------
    volume : Volume
        Data and metadata to write.
    path : str or pathlib.Path
        Destination ``.ome.zarr`` path. It must not already exist.
    scale_factors : list of int, optional
        Downsampling factor of each extra pyramid level relative to full
        resolution, e.g. ``[2, 4]``. By default one level per halving until
        the image is small.
    labels : bool
        Set to True for segmentations, so downsampling keeps label values
        rather than averaging them into values that are not labels.
    """
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"{path} already exists; refusing to overwrite it")
    image = nz.to_ngff_image(
        volume.data,
        dims=list(volume.dims),
        scale=volume.voxel_size,
        axes_units={d: volume.unit for d in volume.voxel_size},
        name=volume.name,
    )
    method = nz.Methods.ITKWASM_LABEL_IMAGE if labels else nz.Methods.ITKWASM_GAUSSIAN
    multiscales = nz.to_multiscales(image, scale_factors=scale_factors or [2], method=method)
    nz.to_ngff_zarr(str(path), multiscales)
