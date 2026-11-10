import pytest


def test_the_models_test_passes_even_though_parse_is_broken(buggy_mod):
    buggy_mod.test_parse_rejects_bad_input()  # cannot fail: proves nothing


def test_bad_input_raises(impl):
    with pytest.raises(ValueError):
        impl.parse("bad input")


def test_numbers_parse(impl):
    assert impl.parse("42") == 42
    assert impl.parse("-7") == -7
