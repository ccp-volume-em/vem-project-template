# Getting started

## Install

You need Python 3.11 or newer. Use a virtual environment, so this project's
packages don't interfere with others:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install "vem-project @ git+https://github.com/ccp-volume-em/vem-project"
```

<!-- Once released on PyPI: python -m pip install vem-project -->

Check it worked:

```bash
vem-project --version
```

## Try it on example data

From a copy of the repository:

```bash
python examples/make_example_data.py
vem-project measure examples/params.yml
```

The first command writes a small synthetic label volume to
`data/example_labels.ome.zarr`: two box-shaped objects with 8 × 8 × 16 nm
voxels. The second measures them and writes:

- `results/example/object_volumes.csv`: the volume of each object in nm³;
- `results/example/provenance.json`: the software version, parameters and
  inputs that produced it.

Object 1 is 8 × 20 × 20 voxels of 1,024 nm³ each, so its volume should be
3,276,800 nm³.
