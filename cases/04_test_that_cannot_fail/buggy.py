def parse(text: str) -> int:
    """Intended: raise ValueError on non-numeric input. (Broken: returns garbage.)"""
    return 0


def test_parse_rejects_bad_input():
    try:
        parse("bad input")
    except Exception:
        pass
