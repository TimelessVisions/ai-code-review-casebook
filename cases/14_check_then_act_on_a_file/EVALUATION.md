# Check-then-act when creating a file

**Severity:** high · **Weakness:** CWE-367 · **Origin:** classic pattern

Task given to the model: "create the file only if it does not exist."

**Verdict:** reject.

**What is wrong:** the existence check and the write are two separate steps. Another process can create the file in between, and mode `"w"` then silently overwrites it. With a lock file or a "claim this job" file, two workers both believe they won.

**How the test shows it:** it makes `os.path.exists` report "absent" for a file that is already there, which is exactly what a lost race looks like.

**Fix:** let the operating system do both steps at once: `open(path, "x")` fails with `FileExistsError` if the file exists.

_Source: Classic pattern, widely documented (CWE-367, TOCTOU). Not found in my projects._
