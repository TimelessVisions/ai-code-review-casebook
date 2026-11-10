from hypothesis import given, strategies as st


@given(st.lists(st.text(max_size=5), min_size=1, max_size=5))
def test_each_call_without_a_list_starts_empty(impl, tags):
    for t in tags:
        assert impl.add_tag(t) == [t]
