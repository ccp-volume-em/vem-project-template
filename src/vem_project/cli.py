"""Command-line interface, for batch runs and HPC jobs.

Parameters come from a YAML file rather than many command-line flags, so a
run can be repeated exactly and the file can be kept with the results.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml

from vem_project import __version__
from vem_project.io import read_ome_zarr
from vem_project.measure import object_volumes
from vem_project.provenance import write_provenance


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vem-project", description="Measure objects in volume EM label images."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)
    measure = sub.add_parser("measure", help="measure the volume of each labelled object")
    measure.add_argument("params", type=Path, help="YAML parameter file, see examples/params.yml")
    args = parser.parse_args(argv)

    if args.command == "measure":
        run_measure(args.params)
    return 0


def run_measure(params_path: Path) -> Path:
    """Measure object volumes as described by a parameter file.

    Parameters
    ----------
    params_path : pathlib.Path
        YAML file with ``labels`` (input OME-Zarr), ``output_dir`` and
        optionally ``level`` (pyramid level, default 0). Relative paths are
        resolved against the parameter file's folder.

    Returns
    -------
    pathlib.Path
        The CSV file of measurements.
    """
    params = yaml.safe_load(params_path.read_text(encoding="utf-8"))
    base = params_path.parent
    labels_path = base / params["labels"]
    output_dir = base / params["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    labels = read_ome_zarr(labels_path, level=params.get("level", 0))
    volumes = object_volumes(labels)

    csv_path = output_dir / "object_volumes.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", f"volume_{labels.unit}3"])
        writer.writerows(volumes.items())

    write_provenance(output_dir / "provenance.json", params, [labels_path], [csv_path])
    print(f"Measured {len(volumes)} objects; results in {csv_path}")
    return csv_path


if __name__ == "__main__":
    raise SystemExit(main())
