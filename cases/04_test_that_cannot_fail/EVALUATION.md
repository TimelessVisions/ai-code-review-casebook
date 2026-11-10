# "All tests pass" from a test that cannot fail

**Severity:** medium · **Weakness:** CWE-1164 · **Origin:** found in my projects

Claim from the model: "all tests pass", shown with `try: parse("bad input") except Exception: pass`.

**Verdict:** the claim is meaningless.

**What is wrong:** the test catches every exception, so it passes whether `parse` raises, returns garbage, or works. A test that cannot fail verifies nothing.

**How to show it:** `buggy.py` has a `parse` that returns `0` for everything, and the model's test still passes (`test_the_models_test_passes_even_though_parse_is_broken`).

**Fix:** `with pytest.raises(ValueError): parse("bad input")`, plus positive cases.

_Source: The pattern behind a false green in mcp-failure-lab, where checks asserted nothing._
