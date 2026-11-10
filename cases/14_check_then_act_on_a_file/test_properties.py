import pathlib
import tempfile

from hypothesis import given, strategies as st


@given(st.text(max_size=50), st.text(max_size=50))
def test_second_write_never_changes_the_file(impl, first, second):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "f.txt"
        assert impl.write_if_absent(str(p), first) is True
        assert impl.write_if_absent(str(p), second) is False
        assert p.read_text(encoding="utf-8") == first
