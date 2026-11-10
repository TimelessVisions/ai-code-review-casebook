from hypothesis import given, strategies as st

cents = st.integers(0, 10_000_000)


@given(st.lists(cents, max_size=20))
def test_matches_integer_cents(impl, amounts):
    prices = [f"{c // 100}.{c % 100:02d}" for c in amounts]
    assert impl.total_cents(prices) == sum(amounts)
