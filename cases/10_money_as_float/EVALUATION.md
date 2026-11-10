# Money converted to cents through a float

**Severity:** medium · **Weakness:** CWE-1339 · **Origin:** classic pattern

Task given to the model: "sum the prices and return cents."

**Verdict:** reject.

**What is wrong:** `0.29` has no exact binary float. `0.29 * 100` is `28.999999999999996`, and `int()` truncates it to `28`. The error is a cent here and there, which is exactly the kind of bug nobody notices until reconciliation.

**Input that breaks it:** `["0.29"]` gives `28`.

**Fix:** `decimal.Decimal` from the string, or integer cents end to end.

_Source: Classic pattern, widely documented (CWE-1339). Not found in my projects._
