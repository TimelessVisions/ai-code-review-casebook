# Path containment checked with startswith

**Severity:** high · **Weakness:** CWE-22 · **Origin:** classic pattern

Task given to the model: "allow only files inside the base directory."

**Verdict:** reject.

**What is wrong:** `startswith(base)` is a string test, not a path test. `/srv/data2/secret` starts with `/srv/data`, so a sibling directory with the same prefix counts as inside.

**Input that breaks it:** `is_inside("/srv/data", "../data2/secret")` returns `True`.

**Fix:** normalise, then require the target to equal the base or start with `base + "/"` (or compare with `os.path.commonpath` on resolved paths).

_Source: Classic pattern, widely documented (CWE-22). Not found in my projects._
