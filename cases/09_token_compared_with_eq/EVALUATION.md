# Secret token compared with ==

**Severity:** medium · **Weakness:** CWE-208 · **Origin:** classic pattern

Task given to the model: "check the API token."

**Verdict:** reject for a secret; fine for anything else.

**What is wrong:** `==` stops at the first differing character, so the time it takes leaks how much of the guess is right. Over many requests an attacker can recover the token one character at a time.

**How the test shows it:** timing is too noisy for a unit test, so the test checks that the comparison goes through `hmac.compare_digest`; the property test checks the result is still correct for any pair of strings.

**Fix:** `hmac.compare_digest(given.encode(), expected.encode())`.

_Source: Classic pattern, widely documented (CWE-208). Not found in my projects._
