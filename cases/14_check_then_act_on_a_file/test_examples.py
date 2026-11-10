import os


def test_creates_a_new_file(impl, tmp_path):
    p = tmp_path / "f.txt"
    assert impl.write_if_absent(str(p), "hello") is True
    assert p.read_text(encoding="utf-8") == "hello"


def test_never_overwrites_even_if_the_file_appears_after_the_check(impl, tmp_path, monkeypatch):
    p = tmp_path / "f.txt"
    p.write_text("someone else's data", encoding="utf-8")
    # Simulate the race: the existence check runs before the other writer creates the file.
    monkeypatch.setattr(os.path, "exists", lambda _p: False)
    assert impl.write_if_absent(str(p), "mine") is False
    assert p.read_text(encoding="utf-8") == "someone else's data"
