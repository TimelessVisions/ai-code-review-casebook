"""Fixtures shared by every case. `impl` is the implementation under test."""
import hashlib
import importlib.util
import os
import pathlib

import pytest
from hypothesis import HealthCheck, settings

_common = dict(deadline=None, database=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
settings.register_profile("default", max_examples=200, **_common)
settings.register_profile("fast", max_examples=40, **_common)
settings.load_profile(os.environ.get("CASEBOOK_HYPOTHESIS_PROFILE", "default"))


def _load(path: pathlib.Path):
    path = path.resolve()
    name = "casebook_impl_" + hashlib.sha256(str(path).encode()).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _case_dir(request) -> pathlib.Path:
    return pathlib.Path(str(request.node.fspath)).parent


@pytest.fixture
def impl(request):
    """$CASEBOOK_IMPL if set (a candidate being graded), else the case's fixed.py."""
    candidate = os.environ.get("CASEBOOK_IMPL")
    return _load(pathlib.Path(candidate) if candidate else _case_dir(request) / "fixed.py")


@pytest.fixture
def buggy_mod(request):
    return _load(_case_dir(request) / "buggy.py")
