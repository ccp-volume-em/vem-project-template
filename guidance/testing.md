# Testing

From the guide: [Writing Tests For Plugins](https://ccp-volume-em.github.io/guide/plugin_testing/)
and [Container Testing](https://ccp-volume-em.github.io/guide/container_testing/).
The advice applies to any Python package, not only plugins.

Well-written tests keep the code maintainable for future developers and help
locate the source of problems users report. Use
[pytest](https://docs.pytest.org/en/stable/getting-started.html).

## Kinds of test

**Installation tests** check that the package is installed and imports
without errors, together with its main dependencies. They catch broken
installs and version clashes between packages.

```python
def test_module_imports():
    try:
        import napari
        import my_package
    except ImportError as e:
        pytest.fail(f"Failed to import required module: {e}")
```

**Unit tests** check that each function returns the expected output for a
given input. Write them so that *any correct implementation* passes: test the
behaviour, not the implementation. Use `@pytest.mark.parametrize` to cover
several scenarios, including edge cases (e.g. overlapping, separate and
touching ranges), and give each case a readable `id`.

**Integration tests** check that components work together. For napari
plugins, test each widget. In CI, use a mock viewer such as
`napari.components.ViewerModel` instead of opening the GUI.

## Hardware-dependent tests

- Mark tests that need a GPU (e.g. `@pytest.mark.gpu`) and skip them
  automatically when no GPU is available, by overriding
  `pytest_collection_modifyitems` in `tests/conftest.py`.
- Within a GPU test, `pytest.skip` with a clear reason if the framework wasn't
  built with CUDA or CUDA isn't available.
- Check that the GPU actually computes something, not just that it's detected.

## Coverage

```bash
pip install pytest-cov
pytest --cov=<your_package> --cov-report=html
```

Open `htmlcov/index.html` to see which lines are tested. Aim to cover
everything. Exclude lines that never need testing (e.g. debugging code) with
`# pragma: no cover`.

## Automated testing (GitHub Actions)

- Run the tests automatically in a workflow in `.github/workflows/`.
- Test on Linux, macOS and Windows, and on each supported Python version.
- Install the package with its test extras (`pip install .[test]`).
- Tests designed for containers (e.g. installation checks) can be excluded from
  the normal CI run.

## Containers

- In CI, it's normally enough to check that the container image builds and,
  if possible, runs without error. Use a virtual display such as `Xvfb` for
  GUI applications.
- Build the container locally and check the software works inside it at least
  once after initial development, and ideally periodically: paths,
  directories and user permissions differ from a direct install.
- Add **start-up checks** to the container's entrypoint: `DISPLAY` is set,
  host data mounts are readable and writable, GPU/CUDA is available, expected
  executables are on `PATH`, shared libraries load (`ldd`).
- A failed start-up check should **warn**, not stop the container: the
  problem may not affect everything, and the user can often fix it with a
  simple option (e.g. `--gpus all`).
