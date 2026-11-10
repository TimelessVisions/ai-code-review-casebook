import sqlite3


def find_user(conn: sqlite3.Connection, name: str) -> list[int]:
    rows = conn.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchall()
    return [r[0] for r in rows]
