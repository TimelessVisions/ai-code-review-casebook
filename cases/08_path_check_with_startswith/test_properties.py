from hypothesis import given, strategies as st

seg = st.text(alphabet="abcxyz019_", min_size=1, max_size=8)


@given(st.lists(seg, min_size=1, max_size=4))
def test_plain_relative_paths_are_inside(impl, parts):
    assert impl.is_inside("/srv/data", "/".join(parts)) is True


@given(seg)
def test_same_prefix_siblings_are_outside(impl, suffix):
    assert impl.is_inside("/srv/data", f"../data{suffix}/f") is False
