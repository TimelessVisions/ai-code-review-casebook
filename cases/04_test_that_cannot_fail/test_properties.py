import pytest
from hypothesis import given, strategies as st


@given(st.integers())
def test_round_trips_any_integer(impl, n):
    assert impl.parse(str(n)) == n


@given(st.text(alphabet="abcxyz!?", min_size=1, max_size=10))
def test_letters_are_rejected(impl, s):
    with pytest.raises(ValueError):
        impl.parse(s)
