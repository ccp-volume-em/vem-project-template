"""Example volume EM / CLEM analysis package.

Replace this description with what your package does.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    # pyproject.toml is the single source of truth for the version.
    __version__ = version("vem-project")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "unknown"
