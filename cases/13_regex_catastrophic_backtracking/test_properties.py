from hypothesis import given, strategies as st

group = st.text(alphabet="abc019", min_size=1, max_size=6)


@given(st.lists(group, min_size=1, max_size=5))
def test_hyphen_joined_groups_are_valid(impl, groups):
    assert impl.is_valid_name("-".join(groups)) is True


@given(st.lists(group, min_size=1, max_size=5))
def test_trailing_hyphen_is_invalid(impl, groups):
    assert impl.is_valid_name("-".join(groups) + "-") is False
