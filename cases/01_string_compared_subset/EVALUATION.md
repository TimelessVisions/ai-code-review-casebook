# A security check that compares values as strings

**Severity:** high · **Weakness:** CWE-1025 · **Origin:** found in my projects

Task given to the model: "return True only if every item is in allowed."

**Verdict:** reject.

**What is wrong:** `str()` on both sides makes `1` match `"1"` and `True` match `"True"`; a dict matches by its text form. The task said "in allowed", not "looks like something in allowed". In an authorization rule this lets a value of the wrong type through.

**Input that breaks it:** `is_subset([1], ["1"])` returns `True`; it should be `False`.

**Also:** it rebuilds the set of strings for every item (quadratic work).

**Fix:** compare type and value: `type(i) is type(a) and i == a`.

_Source: Found reviewing AI-written code for agent-trust-plane's argument_subset_of rule; fixed before v0.4.0._
