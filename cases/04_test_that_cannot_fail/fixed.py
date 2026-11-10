import pytest


def parse(text: str) -> int:
    return int(text)  # raises ValueError on "bad input"


def test_parse_rejects_bad_input():
    with pytest.raises(ValueError):
        parse("bad input")
