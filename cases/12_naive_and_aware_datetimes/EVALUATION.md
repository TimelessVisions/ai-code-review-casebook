# Comparing a timezone-aware expiry with a naive now

**Severity:** medium · **Weakness:** CWE-1025 · **Origin:** classic pattern

Task given to the model: "return True if the token has expired."

**Verdict:** reject.

**What is wrong:** the expiry string carries an offset (`+00:00`), so it parses to an aware datetime; `datetime.now()` is naive. Python refuses to compare them and raises `TypeError` on every call that does not pass `now`. If both were naive, the server's local timezone would silently shift every expiry.

**Input that breaks it:** `is_expired("2000-01-01T00:00:00+00:00")` raises `TypeError`.

**Fix:** use `datetime.now(timezone.utc)`, and refuse expiries without an offset.

_Source: Classic pattern with Python datetimes, widely documented. Not found in my projects._
