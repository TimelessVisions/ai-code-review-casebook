"""Each buggy.py must fail its own case's tests, or the case proves nothing."""
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).parent
CASES = sorted(p for p in (HERE / "cases").iterdir() if p.is_dir())
META = {"04_test_that_cannot_fail"}  # this case's test exercises both modules itself


@pytest.mark.parametrize("case", [c for c in CASES if c.name not in META], ids=lambda c: c.name)
def test_buggy_implementation_fails_the_case_tests(case, tmp_path):
    (tmp_path / "test_case.py").write_text((case / "test_case.py").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "fixed.py").write_text((case / "buggy.py").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "conftest.py").write_text((HERE / "conftest.py").read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--import-mode=importlib", "test_case.py"],
        capture_output=True, text=True, cwd=tmp_path,
    )
    assert r.returncode != 0, "buggy version passed its own tests:\n" + r.stdout
