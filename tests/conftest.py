import pytest


def _gpu_available() -> bool:
    # This template has no GPU code. If you add some, check for it here, e.g.
    #     import torch
    #     return torch.cuda.is_available()
    return False


def pytest_collection_modifyitems(config, items):
    """Skip tests marked ``@pytest.mark.gpu`` on machines without a usable GPU."""
    if _gpu_available():
        return
    skip_gpu = pytest.mark.skip(reason="No GPU available")
    for item in items:
        if "gpu" in item.keywords:
            item.add_marker(skip_gpu)
