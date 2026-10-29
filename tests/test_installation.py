"""Installation tests: the package and its main dependencies install and import.

These catch broken installs and dependency version clashes early, before any
unit test runs.
"""

from importlib.metadata import version

import pytest


def test_package_imports():
    try:
        import dask.array  # noqa: F401
        import ngff_zarr  # noqa: F401

        import vem_project  # noqa: F401
    except ImportError as e:
        pytest.fail(f"Failed to import a required module: {e}")


def test_version_comes_from_package_metadata():
    import vem_project

    assert vem_project.__version__ == version("vem-project")
