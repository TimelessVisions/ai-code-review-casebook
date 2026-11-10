# A 3-check probe reported as a full conformance pass

**Severity:** high · **Weakness:** CWE-1164 · **Origin:** found in my projects

Behaviour reported by the tool: `OFFICIAL_CONFORMANCE_PASS`.

**Verdict:** reject. The pass covers only the checks that ran.

**What is wrong:** `all()` over three passing checks is `True`, but the real requirement set has 177. The code never compares what ran with what was required, so a tiny probe is recorded as a full pass.

**Input that breaks it:** three passing checks out of 177 returns `PASS`.

**Fix:** if fewer checks ran than required, return `NOT_MEASURED`. A result you did not measure is never a pass.

_Source: Found in mcp-failure-lab: a 3-check probe was recorded as an official pass while the real set fails 88 of 177 checks._
