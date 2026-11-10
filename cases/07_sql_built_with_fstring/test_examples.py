import sqlite3

import pytest


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    c.executemany("INSERT INTO users (name) VALUES (?)", [("alice",), ("bob",)])
    yield c
    c.close()


def test_finds_exact_name(impl, conn):
    assert impl.find_user(conn, "alice") == [1]


def test_injection_returns_nothing(impl, conn):
    assert impl.find_user(conn, "x' OR '1'='1") == []


def test_quote_in_a_name_is_just_data(impl, conn):
    conn.execute("INSERT INTO users (name) VALUES (?)", ("o'brien",))
    assert impl.find_user(conn, "o'brien") == [3]
