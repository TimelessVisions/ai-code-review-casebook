# A generated key passed as a CLI argument

**Severity:** low · **Weakness:** CWE-88 · **Origin:** found in my projects

Task given to the model: "generate a key and pass it to the tool as --key KEY."

**Verdict:** reject as written; it fails intermittently, which is worse than failing always.

**What is wrong:** the URL-safe alphabet has 64 characters and `-` is one of them, so about 1 key in 64 starts with `-`. `argparse` then reads the key as an option and errors with "expected one argument".

**Input that breaks it:** any key beginning with `-`. The tests pin the random value so the failure is deterministic.

**Fix:** pass `--key=KEY`, or regenerate until the key does not start with `-`.

_Source: A 1-in-64 CLI failure fixed in agent-trust-plane: generated keys starting with '-'._
