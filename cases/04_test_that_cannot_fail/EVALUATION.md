# "All tests pass" from a test that cannot fail

Claim from the model: "all tests pass", shown with `try: parse("bad input") except Exception: pass`.

**Verdict:** the claim is meaningless.

**What is wrong:** the test catches every exception, so it passes whether `parse` raises, returns garbage, or works. A test that cannot fail verifies nothing.

**How to show it:** replace `parse` with a function that returns `0` for everything; the test still passes.

**Fix:** `with pytest.raises(ValueError): parse("bad input")`, plus a positive case (`parse("42") == 42`).

_Origin: The pattern behind a false green found in a protocol fault-injection harness, where checks asserted nothing._
