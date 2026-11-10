# AI code review casebook

Six bugs that AI coding agents actually shipped while I was building developer tools, each reduced to a small, runnable case: the buggy code, the fix, a test that fails on the bug and passes on the fix, and a short written evaluation in the form a reviewer would write (verdict first, then the evidence, the input that breaks it, and the fix).

The cases come from my work on [agent-trust-plane](https://github.com/TimelessVisions/agent-trust-plane) (on PyPI) and a protocol fault-injection harness. They are reduced for clarity; each evaluation states where the bug came from.

| # | Case | Verdict |
|---|---|---|
| 01 | [A security check that compares values as strings](cases/01_string_compared_subset/EVALUATION.md) | Reject. A correctness bug inside a security check. |
| 02 | [Cap a message at 200 characters by slicing bytes](cases/02_slice_bytes_then_decode/EVALUATION.md) | Reject. Crashes on ordinary non-ASCII input. |
| 03 | [A generated key passed as a CLI argument](cases/03_generated_key_starts_with_dash/EVALUATION.md) | Reject as written. About 1 key in 64 fails. |
| 04 | ["All tests pass" from a test that cannot fail](cases/04_test_that_cannot_fail/EVALUATION.md) | Reject the claim. The test proves nothing. |
| 05 | [Measuring null as a short string](cases/05_null_measured_as_text/EVALUATION.md) | Reject. `None` silently passes any limit of 4 or more. |
| 06 | [A 3-check probe reported as a full conformance pass](cases/06_probe_reported_as_conformance_pass/EVALUATION.md) | Reject. The status claims more than was measured. |

## Run it

```bash
python -m pip install pytest
python -m pytest -q
```

The suite checks two things: the fixed code passes each case's tests, and the buggy code *fails* them (`test_buggy_versions_fail.py`), so no case can quietly stop demonstrating its bug.

## How I review AI-written code

1. Run or trace it. Correctness comes first; style never outranks a wrong answer.
2. Name the exact input that breaks it.
3. Write the failing test before the fix.
4. Distrust green: a test that cannot fail, a probe reported as a full pass, and a CI job that never ran all look like success.
5. Say what was not measured.

MIT licensed.
