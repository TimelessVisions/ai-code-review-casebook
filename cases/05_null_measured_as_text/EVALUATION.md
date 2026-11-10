# Measuring null as a short string

Task given to the model: "deny an argument longer than `limit` characters."

**Verdict:** reject.

**What is wrong:** `str(None)` is `"None"` (4 characters, `"null"` in JSON), so a missing or null argument passes every limit of 4 or more. A security rule should fail closed on input it cannot measure.

**Input that breaks it:** `within_max_length(None, 4)` returns `True`.

**Fix:** reject non-strings explicitly (or, if the argument is optional, treat `None` as "absent" on purpose and test that).

_Origin: Fixed in agent-trust-plane 0.4.0 (`argument_max_length` measured an explicit null as the string "null")._
