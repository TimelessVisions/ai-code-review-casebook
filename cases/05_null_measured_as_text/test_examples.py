def test_none_is_not_a_short_string(impl):
    assert impl.within_max_length(None, 4) is False


def test_strings_still_measured(impl):
    assert impl.within_max_length("abcd", 4) is True
    assert impl.within_max_length("abcde", 4) is False
