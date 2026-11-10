import importlib.util
import pathlib

import pytest


def _load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(f"{path.parent.name}_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def buggy_mod(request):
    return _load(pathlib.Path(request.fspath).parent / "buggy.py")


@pytest.fixture
def fixed_mod(request):
    return _load(pathlib.Path(request.fspath).parent / "fixed.py")


@pytest.fixture
def impl(fixed_mod):
    """Case tests run against the fixed implementation."""
    return fixed_mod
