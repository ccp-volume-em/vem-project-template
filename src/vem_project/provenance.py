"""Record how an output was produced, so results can be traced and reproduced.

A provenance file sits next to each output and records the software version,
the parameters and the inputs. For sharing complete datasets, the CCP-volumeEM
guide recommends packaging this information as an RO-Crate
(https://www.researchobject.org/ro-crate/); this simple JSON record is a
starting point that can be converted later.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import vem_project

# Versions of the libraries that can change results.
_TRACKED_PACKAGES = ("dask", "ngff-zarr", "numpy")


def write_provenance(
    path: str | Path,
    parameters: dict,
    inputs: list[str | Path],
    outputs: list[str | Path],
) -> dict:
    """Write a JSON provenance record and return its contents.

    Parameters
    ----------
    path : str or pathlib.Path
        Where to write the record, usually next to the outputs.
    parameters : dict
        Every parameter that affects the result.
    inputs, outputs : list of str or pathlib.Path
        Files or folders read and written.

    Returns
    -------
    dict
        The record that was written.
    """
    record = {
        "software": {"name": "vem-project", "version": vem_project.__version__},
        "created": datetime.now(UTC).isoformat(timespec="seconds"),
        "parameters": parameters,
        "inputs": [str(p) for p in inputs],
        "outputs": [str(p) for p in outputs],
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "packages": {name: _installed_version(name) for name in _TRACKED_PACKAGES},
        },
    }
    Path(path).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


def _installed_version(package: str) -> str | None:
    try:
        return version(package)
    except PackageNotFoundError:
        return None
