# SQL query built with an f-string

**Severity:** critical · **Weakness:** CWE-89 · **Origin:** classic pattern

Task given to the model: "return the ids of users with this name."

**Verdict:** reject. Critical.

**What is wrong:** the name is pasted into the SQL text, so the caller controls the query. A quote ends the string literal and the rest runs as SQL.

**Input that breaks it:** `x' OR '1'='1` returns every user; `o'brien` raises a syntax error.

**Fix:** a parameterised query: `conn.execute("... WHERE name = ?", (name,))`.

_Source: Classic pattern, widely documented (OWASP, CWE-89). Not found in my projects._
