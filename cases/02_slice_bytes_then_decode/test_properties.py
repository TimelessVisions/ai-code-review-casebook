from hypothesis import given, strategies as st


@given(st.text(max_size=400))
def test_is_a_prefix_of_at_most_200_characters(impl, s):
    out = impl.cap(s)
    assert s.startswith(out)
    assert len(out) == min(len(s), 200)
