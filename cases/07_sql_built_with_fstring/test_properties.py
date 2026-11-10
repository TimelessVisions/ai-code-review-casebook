import sqlite3

from hypothesis import given, strategies as st

names = st.text(st.characters(blacklist_categories=("Cs",), blacklist_characters="\x00"), max_size=30)


@given(names)
def test_only_exact_matches_come_back(impl, name):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    c.executemany("INSERT INTO users (name) VALUES (?)", [("alice",), ("bob",)])
    expected = {"alice": [1], "bob": [2]}.get(name, [])
    assert impl.find_user(c, name) == expected
    c.close()
