from hypothesis import given, strategies as st

tok = st.text(st.characters(blacklist_categories=("Cs",)), max_size=20)


@given(tok, tok)
def test_equal_exactly_when_the_strings_are_equal(impl, a, b):
    assert impl.check_token(a, b) is (a == b)
