def test_plain_file_is_inside(impl):
    assert impl.is_inside("/srv/data", "report.txt") is True


def test_sibling_with_same_prefix_is_outside(impl):
    assert impl.is_inside("/srv/data", "../data2/secret") is False


def test_parent_escape_is_outside(impl):
    assert impl.is_inside("/srv/data", "../../etc/passwd") is False


def test_absolute_path_is_outside(impl):
    assert impl.is_inside("/srv/data", "/etc/passwd") is False


def test_dotdot_that_comes_back_is_inside(impl):
    assert impl.is_inside("/srv/data", "a/../b.txt") is True
