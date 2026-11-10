from hypothesis import given, strategies as st

# Mostly multi-byte characters, long enough to reach the 200 cap, so a byte-based cut is found reliably.
texts = st.text(alphabet="aé€😀", min_size=190, max_size=400)


@given(texts)
def test_is_a_prefix_of_at_most_200_characters(impl, s):
    out = impl.cap(s)
    assert s.startswith(out)
    assert len(out) == min(len(s), 200)
