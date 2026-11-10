"""Run a case's example and property tests against a candidate implementation."""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from .registry import Case


@dataclass
class Failure:
    test: str
    message: str
    falsifying: str | None = None


@dataclass
class GradeResult:
    case: Case
    candidate: pathlib.Path
    passed: bool
    tests: int = 0
    failures: list[Failure] = field(default_factory=list)
    timed_out: bool = False
    error: str | None = None


def _falsifying(text: str) -> str | None:
    """Hypothesis reports the shrunk breaking input as 'Falsifying example:' or 'Failing test case:'."""
    m = re.search(r"(?:Falsifying example|Failing test case):[^\n]*\n(.*)", text, re.S)
    if not m:
        return None
    args = []
    for raw in m.group(1).splitlines():
        line = re.sub(r"^[E|\s]+", "", raw).strip()
        if not line or line == ")" or line.startswith(")"):
            break
        if re.match(r"^[A-Za-z_]\w*=", line) and not line.startswith(("impl=", "buggy_mod=", "fixed_mod=")):
            args.append(re.sub(r"\s+#.*$", "", line).rstrip(","))
    return ", ".join(args)[:600] or None


def _short_message(message: str, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("E "):
            return line[1:].strip()[:300]
    return (message or "failed").strip().splitlines()[0][:300]


def run_tests(
    case: Case,
    candidate: pathlib.Path,
    *,
    profile: str = "default",
    timeout: float = 300,
) -> GradeResult:
    candidate = candidate.resolve()
    result = GradeResult(case=case, candidate=candidate, passed=False)
    if not candidate.is_file():
        result.error = f"no such file: {candidate}"
        return result
    with tempfile.TemporaryDirectory(prefix="casebook-") as tmp:
        junit = pathlib.Path(tmp) / "junit.xml"
        env = dict(os.environ, CASEBOOK_IMPL=str(candidate), CASEBOOK_HYPOTHESIS_PROFILE=profile)
        env.pop("PYTEST_ADDOPTS", None)
        cmd = [
            sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
            "--import-mode=importlib", f"--junitxml={junit}", "-o", "addopts=",
            str(case.path),
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, env=env, timeout=timeout, cwd=case.path.parent.parent
            )
        except subprocess.TimeoutExpired:
            result.timed_out = True
            result.failures.append(Failure("(whole run)", f"timed out after {timeout:g}s"))
            return result
        if not junit.exists():
            result.error = (proc.stdout + proc.stderr).strip()[-2000:] or "pytest produced no report"
            return result
        root = ET.parse(junit).getroot()
        for tc in root.iter("testcase"):
            result.tests += 1
            bad = tc.find("failure")
            if bad is None:
                bad = tc.find("error")
            if bad is not None:
                text = bad.text or ""
                result.failures.append(
                    Failure(
                        test=tc.get("name", "?"),
                        message=_short_message(bad.get("message", ""), text),
                        falsifying=_falsifying(text),
                    )
                )
        result.passed = proc.returncode == 0 and result.tests > 0 and not result.failures
        if proc.returncode not in (0, 1) and not result.failures:
            result.error = (proc.stdout + proc.stderr).strip()[-2000:]
    return result


def verdict(result: GradeResult) -> str:
    """A review in the casebook format: verdict first, then the evidence."""
    c = result.case
    head = f"# Case {c.id}: {c.title}\n\nCandidate: `{result.candidate.name}`  \nSeverity if wrong: {c.severity} · {c.cwe}\n\n"
    if result.error:
        return head + f"**Verdict:** could not grade.\n\n```\n{result.error}\n```\n"
    if result.passed:
        return head + (
            f"**Verdict:** accept. All {result.tests} example and property tests pass.\n\n"
            "Property tests sample many inputs; a pass is strong evidence, not a proof.\n"
        )
    lines = [head + f"**Verdict:** reject. {len(result.failures)} of {result.tests or '?'} tests fail.\n"]
    for f in result.failures:
        lines.append(f"- `{f.test}`: {f.message}")
        if f.falsifying:
            lines.append(f"  - smallest breaking input found: `{f.falsifying}`")
    return "\n".join(lines) + "\n"
