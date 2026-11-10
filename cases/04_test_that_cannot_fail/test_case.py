import pytest


def test_the_weak_test_passes_even_though_parse_is_broken(buggy_mod):
    buggy_mod.test_parse_rejects_bad_input()  # passes: it cannot fail


def test_the_real_test_catches_the_broken_parse(buggy_mod, fixed_mod):
    assert buggy_mod.parse("bad input") == 0  # the broken parse does not raise
    with pytest.raises(ValueError):
        fixed_mod.parse("bad input")
    assert fixed_mod.parse("42") == 42
