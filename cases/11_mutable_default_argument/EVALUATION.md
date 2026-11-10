# A mutable default argument shared between calls

**Severity:** medium · **Weakness:** CWE-1188 · **Origin:** classic pattern

Task given to the model: "add a tag to a list, creating the list if none is given."

**Verdict:** reject.

**What is wrong:** the default `[]` is created once, when the function is defined, and every call without a list appends to that same object. Tags leak from one caller (or one user's request) into the next.

**Input that breaks it:** `add_tag("a")` then `add_tag("b")` returns `["a", "b"]`.

**Fix:** default to `None` and create the list inside the function.

_Source: Classic Python pitfall, widely documented. Not found in my projects._
