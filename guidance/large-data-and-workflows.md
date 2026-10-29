# Large data and workflows

Patterns the guide shows in [muvis-align](https://ccp-volume-em.github.io/guide/muvis-align/)
([source code](https://github.com/ccp-volume-em/muvis-align)), a registration
package with a napari plugin, notebooks, a CLI and containers.

## Larger-than-memory data

- Read lazily: open TIFF (via tifffile's Zarr store, `aszarr`) and OME-Zarr as
  [dask](https://www.dask.org/) arrays, one per pyramid level, so the full
  volume is never loaded at once.
- Read metadata first (e.g. from consolidated Zarr metadata), and only touch
  the arrays when the data is needed.
- Write results directly to OME-Zarr level by level and block by block,
  instead of building the whole output in memory first.
- Raise a clear error for unsupported file types.

## One workflow, several interfaces

- Offer the same workflow as a napari plugin, notebooks, and a command-line
  interface for batch and HPC runs.
- Drive the CLI from a YAML parameter file, so a run can be repeated exactly.
- Describe parameters declaratively (muvis-align uses the Bilayers schema,
  validated with [Pydantic](https://docs.pydantic.dev/)) and generate the
  user interface from that description, so the plugin, CLI and containers
  share one definition.

## Provenance and FAIR outputs

- Write each run's parameters, source images and results as a Workflow Run
  [RO-Crate](https://www.researchobject.org/ro-crate/).
- Give OME-Zarr outputs their own RO-Crate recording sources, acquisition,
  quality metrics and processing steps.
- See [fair-data.md](fair-data.md).

## Quality metrics

- Compute several complementary metrics to judge results rather than relying
  on one. For registration: NCC (intensity correlation), SSIM (local
  structure) and ONMI (shared information, robust across modalities).
- Save the metrics alongside the results.

## Resumable workflows

- Save intermediate state (e.g. pairwise and global registration mappings,
  metrics) to files as each expensive step finishes.
- On a re-run, detect existing outputs and continue from the last completed
  step instead of recomputing.
- Track progress explicitly, e.g. with a state enum.

## Interactive use on remote machines

- A container variant with [Xpra](https://xpra.org/) lets users run a napari
  GUI on a remote machine or cluster from a web browser. See
  [containers.md](containers.md).
