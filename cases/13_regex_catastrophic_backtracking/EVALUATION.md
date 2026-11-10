# A name check with catastrophic regex backtracking

**Severity:** high · **Weakness:** CWE-1333 · **Origin:** classic pattern

Task given to the model: "validate a slug: lowercase letters and digits, groups joined by single hyphens."

**Verdict:** reject. It is both wrong and a denial-of-service risk.

**What is wrong:** `([a-z0-9]+-?)*` nests one repetition inside another, so a string that almost matches can be split into groups in exponentially many ways, and the regex engine tries them all before failing. It also accepts `""` and `"a-"`, which the spec rules out.

**Input that breaks it:** `"a" * 40 + "!"` does not finish in any useful time; `"a-"` returns `True`.

**Fix:** `[a-z0-9]+(?:-[a-z0-9]+)*`: each character can be matched only one way.

_Source: Classic pattern, widely documented (CWE-1333, ReDoS). Not found in my projects._
