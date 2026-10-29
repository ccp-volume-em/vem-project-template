# OME-Zarr (NGFF) and image metadata

From the guide: [Next Generation File Format](https://ccp-volume-em.github.io/guide/ngff/),
with examples from [muvis-align](https://ccp-volume-em.github.io/guide/muvis-align/).

OME-Zarr, also called NGFF (Next Generation File Format), is the Open
Microscopy Environment community format for storing and sharing large
bioimaging datasets.

## Choosing a library

- Several Python packages support OME-Zarr well. See the
  [comparison of OME-Zarr libraries](https://github.com/ome/ome-zarr-py/issues/407),
  which has examples for each.
- [An Introduction to OME-Zarr for Big Bioimaging Data](https://ome-zarr-book.readthedocs.io/)
  is a good overview (using ome-zarr-models, pydantic-ome-ngff and zarr-python).
- [ome-zarr-py](https://github.com/ome/ome-zarr-py) reads local or remote
  (URL) data into a list of dask arrays, one per pyramid level, plus a
  metadata dictionary. `write_image` writes data with metadata and pyramid
  levels created automatically.
- [ngff-zarr](https://pypi.org/project/ngff-zarr/) (`to_ngff_image`,
  `to_multiscales`, `to_ngff_zarr`) writes images with physical scale,
  translation and units, and generates the multiscale pyramid.

## Persistent metadata

- Keep metadata *with* the image data throughout processing, not in separate
  variables that can get out of step: pixel/voxel size, coordinates and
  transforms.
- Hold image data as [dask](https://docs.dask.org/) arrays, and the metadata
  in memory with [spatial-image](https://github.com/spatial-image/spatial-image)
  / multiscale spatial images, which are based on
  [xarray](https://docs.xarray.dev/) (labelled dimensions, with coordinates and
  attributes).
- Propagate the metadata through every operation and write it back out, so
  the physical meaning of the output is preserved.
- Read input metadata (axes, units, voxel scale, translations, channels,
  transforms) from OME-TIFF or OME-Zarr and convert it to physical units.

## Coordinate transforms (e.g. registration, CLEM)

- Store registration transforms in the
  [OME-NGFF RFC 6 coordinate-transform format](https://github.com/ome/ngff-spec/blob/main/index.md#coordinatetransformations-metadata)
  rather than as application-specific matrices.
- Name each transform's input and output coordinate systems (e.g.
  `source_metadata` → `registered`) and the image it applies to.
- Validate and serialise transforms with a model library (e.g.
  `ome-zarr-models`), so other tools that implement NGFF can use them.
