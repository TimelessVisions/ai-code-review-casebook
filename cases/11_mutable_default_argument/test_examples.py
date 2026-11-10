def test_calls_do_not_share_state(impl):
    assert impl.add_tag("a") == ["a"]
    assert impl.add_tag("b") == ["b"]


def test_given_list_is_extended(impl):
    mine = ["x"]
    assert impl.add_tag("y", mine) == ["x", "y"]
