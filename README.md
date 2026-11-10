# AI code review casebook

[![ci](https://github.com/TimelessVisions/ai-code-review-casebook/actions/workflows/ci.yml/badge.svg)](https://github.com/TimelessVisions/ai-code-review-casebook/actions/workflows/ci.yml)

A small tool for grading AI-written fixes, and a set of 15 bug cases to grade them on.

Give `casebook` a candidate fix (from any model, or from you) and it returns a review in reviewer format: **verdict first, then the smallest input that breaks it**. It judges the fix with example tests plus property-based tests that try hundreds of generated inputs, so a fix that only works for the example in the prompt does not pass.

```console
$ casebook grade 02 candidate.py
# Case 02: Cap a message at 200 characters by slicing bytes

Candidate: `candidate.py`
Severity if wrong: medium · CWE-135

**Verdict:** reject. 1 of 3 tests fail.
- `test_multibyte_text_does_not_crash`: UnicodeDecodeError: 'utf-8' codec can't decode byte ...
```

## Try it

```bash
git clone https://github.com/TimelessVisions/ai-code-review-casebook && cd ai-code-review-casebook
uv sync
uv run casebook list
uv run casebook grade 02 cases/02_slice_bytes_then_decode/buggy.py     # rejected
uv run casebook grade 02 cases/02_slice_bytes_then_decode/fixed.py     # accepted
```

Write your own `candidate.py` that defines the case's function (see `function` in each `case.toml`) and grade it.

## The cases

Cases 01–06 are bugs that AI coding agents actually shipped while I was building [agent-trust-plane](https://github.com/TimelessVisions/agent-trust-plane) and [mcp-failure-lab](https://github.com/TimelessVisions/mcp-failure-lab), reduced to a small runnable form. Cases 07–15 are well-known weakness patterns (OWASP / CWE) that AI-written code often repeats. They are labelled **classic pattern** and I do not claim to have found them: the origin of every case is in its `case.toml` and `EVALUATION.md`.

<!-- casebook:cases:start -->
| # | Case | Severity | Weakness | Origin | Mutants killed |
|---|---|---|---|---|---|
| 01 | [A security check that compares values as strings](cases/01_string_compared_subset/EVALUATION.md) | high | CWE-1025 | found in my projects | 4/4 |
| 02 | [Cap a message at 200 characters by slicing bytes](cases/02_slice_bytes_then_decode/EVALUATION.md) | medium | CWE-135 | found in my projects | 2/2 |
| 03 | [A generated key passed as a CLI argument](cases/03_generated_key_starts_with_dash/EVALUATION.md) | low | CWE-88 | found in my projects | 5/8 |
| 04 | ["All tests pass" from a test that cannot fail](cases/04_test_that_cannot_fail/EVALUATION.md) | medium | CWE-1164 | found in my projects | 1/1 |
| 05 | [Measuring null as a short string](cases/05_null_measured_as_text/EVALUATION.md) | high | CWE-20 | found in my projects | 5/5 |
| 06 | [A 3-check probe reported as a full conformance pass](cases/06_probe_reported_as_conformance_pass/EVALUATION.md) | high | CWE-1164 | found in my projects | 7/7 |
| 07 | [SQL query built with an f-string](cases/07_sql_built_with_fstring/EVALUATION.md) | critical | CWE-89 | classic pattern | 3/3 |
| 08 | [Path containment checked with startswith](cases/08_path_check_with_startswith/EVALUATION.md) | high | CWE-22 | classic pattern | 5/6 |
| 09 | [Secret token compared with ==](cases/09_token_compared_with_eq/EVALUATION.md) | medium | CWE-208 | classic pattern | 1/1 |
| 10 | [Money converted to cents through a float](cases/10_money_as_float/EVALUATION.md) | medium | CWE-1339 | classic pattern | 4/4 |
| 11 | [A mutable default argument shared between calls](cases/11_mutable_default_argument/EVALUATION.md) | medium | CWE-1188 | classic pattern | 2/2 |
| 12 | [Comparing a timezone-aware expiry with a naive now](cases/12_naive_and_aware_datetimes/EVALUATION.md) | medium | CWE-1025 | classic pattern | 5/6 |
| 13 | [A name check with catastrophic regex backtracking](cases/13_regex_catastrophic_backtracking/EVALUATION.md) | high | CWE-1333 | classic pattern | 3/3 |
| 14 | [Check-then-act when creating a file](cases/14_check_then_act_on_a_file/EVALUATION.md) | high | CWE-367 | classic pattern | 6/6 |
| 15 | [A config loader that swallows every error](cases/15_swallowed_exception/EVALUATION.md) | medium | CWE-390 | classic pattern | 3/3 |
<!-- casebook:cases:end -->

## What is in each case

| File | Purpose |
|---|---|
| `buggy.py` | The plausible-looking wrong answer |
| `fixed.py` | A correct fix |
| `test_examples.py` | Readable examples, including the breaking input |
| `test_properties.py` | [Hypothesis](https://hypothesis.readthedocs.io/) property tests: hundreds of generated inputs, shrunk to the smallest failure |
| `EVALUATION.md` | The written review: verdict, what is wrong, breaking input, fix |
| `case.toml` | Function name, severity, CWE and where the case came from |

## How the cases are checked

- `casebook check` requires that every `fixed.py` **passes** and every `buggy.py` **fails** its case. A case that no longer demonstrates its bug breaks CI.
- `casebook mutate` breaks each fix in small ways (flip a comparison, change a constant, drop a return value) and reports how many of those mutants the tests catch. The column above is **mutants killed / mutants made**. A survivor means the tests do not pin that behaviour down, and the survivors are listed by `casebook mutate`.
- CI runs on Linux, macOS and Windows, Python 3.12 and 3.13.

## Limits

- Property tests sample inputs; a pass is strong evidence, not a proof.
- Mutation testing is a rough measure. Some surviving mutants are equivalent to the original code (the same behaviour written differently).
- Case 09 (timing leak) cannot be unit-tested by timing; its test checks that the comparison goes through `hmac.compare_digest`.
- No model is run by this repository. It does not publish model pass rates.

## How I review AI-written code

1. Run or trace it. Correctness comes first; style never outranks a wrong answer.
2. Name the exact input that breaks it.
3. Write the failing test before the fix.
4. Distrust green: a test that cannot fail, a probe reported as a full pass, and a CI job that never ran all look like success.
5. Say what was not measured.

MIT licensed.
