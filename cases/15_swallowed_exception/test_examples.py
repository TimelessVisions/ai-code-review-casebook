import pytest


def test_missing_file_is_empty_config(impl, tmp_path):
    assert impl.load_config(str(tmp_path / "nope.json")) == {}


def test_broken_json_is_an_error_not_defaults(impl, tmp_path):
    p = tmp_path / "c.json"
    p.write_text('{"require_auth": true,', encoding="utf-8")
    with pytest.raises(ValueError):
        impl.load_config(str(p))
