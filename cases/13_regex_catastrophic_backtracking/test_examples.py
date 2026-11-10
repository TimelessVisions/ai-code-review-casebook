import subprocess
import sys


def test_valid_names(impl):
    assert impl.is_valid_name("abc-123") is True
    assert impl.is_valid_name("a") is True


def test_invalid_names(impl):
    for bad in ("", "-a", "a-", "a--b", "A", "a b"):
        assert impl.is_valid_name(bad) is False, bad


def test_long_near_miss_finishes_quickly(impl):
    code = (
        "import importlib.util as u, sys\n"
        "s = u.spec_from_file_location('m', sys.argv[1]); m = u.module_from_spec(s); s.loader.exec_module(m)\n"
        "m.is_valid_name('a' * 40 + '!')\n"
    )
    try:
        subprocess.run([sys.executable, "-c", code, impl.__file__], timeout=5, check=True)
    except subprocess.TimeoutExpired:
        raise AssertionError("is_valid_name('a' * 40 + '!') ran for more than 5 seconds") from None
