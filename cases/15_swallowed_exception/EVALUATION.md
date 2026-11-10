# A config loader that swallows every error

**Severity:** medium · **Weakness:** CWE-390 · **Origin:** classic pattern

Task given to the model: "load the config; if there is no config file, use defaults."

**Verdict:** reject.

**What is wrong:** `except Exception` turns every failure into "use defaults": a typo in the JSON, a permissions error, a disk error. If a default is less safe (here, `require_auth` falls back to off), a broken config silently weakens the system.

**Input that breaks it:** a config file containing `{"require_auth": true,` (invalid JSON) loads as `{}`.

**Fix:** catch only the case the spec names, `FileNotFoundError`; let everything else raise.

_Source: Classic pattern, widely documented (CWE-390). Not found in my projects._
