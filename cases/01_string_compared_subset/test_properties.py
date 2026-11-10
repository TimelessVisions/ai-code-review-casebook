from hypothesis import given, strategies as st

scalars = st.one_of(st.integers(-1000, 1000), st.text(max_size=8), st.booleans())


@given(st.lists(scalars, max_size=8))
def test_a_list_is_a_subset_of_itself(impl, xs):
    assert impl.is_subset(xs, xs) is True


@given(st.integers(-1000, 1000))
def test_an_int_never_matches_its_text(impl, n):
    assert impl.is_subset([n], [str(n)]) is False


@given(st.lists(scalars, max_size=6), st.lists(scalars, max_size=6))
def test_matches_exact_type_membership(impl, items, allowed):
    expected = all(any(type(i) is type(a) and i == a for a in allowed) for i in items)
    assert impl.is_subset(items, allowed) is expected
