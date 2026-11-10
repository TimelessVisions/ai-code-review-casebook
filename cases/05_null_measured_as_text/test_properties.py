from hypothesis import given, strategies as st


@given(st.text(max_size=50), st.integers(0, 60))
def test_strings_compare_by_length(impl, s, limit):
    assert impl.within_max_length(s, limit) is (len(s) <= limit)


@given(st.one_of(st.none(), st.integers(), st.floats(allow_nan=False), st.lists(st.integers())), st.integers(0, 60))
def test_non_strings_fail_closed(impl, v, limit):
    assert impl.within_max_length(v, limit) is False
