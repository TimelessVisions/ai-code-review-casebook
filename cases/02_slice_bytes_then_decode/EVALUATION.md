# Cap a message at 200 characters by slicing bytes

**Severity:** medium · **Weakness:** CWE-135 · **Origin:** found in my projects

Task given to the model: "cap a log message at 200 characters."

**Verdict:** reject.

**What is wrong:** it slices the UTF-8 bytes and then decodes. A multi-byte character (`é`, an emoji) that straddles byte 200 is cut in half and `decode()` raises `UnicodeDecodeError`. It also caps bytes, not characters, so it is not what was asked.

**Input that breaks it:** `"é" * 150` (300 bytes; byte 200 is mid-character).

**Fix:** slice the string: `data[:200]`. If a byte limit is genuinely required, decode with `errors="ignore"` after slicing, and say so.

_Source: Found in AI-written code in agent-trust-plane (also present in released 0.3.2); fixed in 0.4.0._
