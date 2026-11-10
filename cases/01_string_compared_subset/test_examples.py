def test_int_is_not_the_string(impl):
    assert impl.is_subset([1], ["1"]) is False


def test_bool_is_not_its_text(impl):
    assert impl.is_subset([True], ["True"]) is False


def test_exact_members_pass(impl):
    assert impl.is_subset([1, "a"], [1, "a", "b"]) is True
    assert impl.is_subset([], ["x"]) is True
