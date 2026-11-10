def test_29_cents_is_29(impl):
    assert impl.total_cents(["0.29"]) == 29


def test_ten_plus_twenty(impl):
    assert impl.total_cents(["0.10", "0.20"]) == 30


def test_empty_is_zero(impl):
    assert impl.total_cents([]) == 0
