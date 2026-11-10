"""`casebook`: list cases, grade a fix, check the casebook, run mutation testing."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from . import __version__
from .grading import run_tests, verdict
from .mutation import mutate_case
from .registry import all_cases, cases_root, find_case

REPORT_START = "<!-- casebook:cases:start -->"
REPORT_END = "<!-- casebook:cases:end -->"


def _cmd_list(args: argparse.Namespace) -> int:
    for c in all_cases():
        print(f"{c.id}  {c.severity:<8} {c.cwe:<10} {c.origin:<7} {c.title}")
    return 0


def _cmd_grade(args: argparse.Namespace) -> int:
    case = find_case(args.case)
    result = run_tests(case, pathlib.Path(args.file), profile=args.profile)
    if args.json:
        print(json.dumps({
            "case": case.id, "passed": result.passed, "tests": result.tests,
            "timed_out": result.timed_out, "error": result.error,
            "failures": [vars(f) for f in result.failures],
        }, indent=2))
    else:
        print(verdict(result))
    return 0 if result.passed else 1


def _cmd_check(args: argparse.Namespace) -> int:
    """Every fixed.py must pass its case and every buggy.py must fail it."""
    bad = 0
    for c in all_cases():
        fixed = run_tests(c, c.fixed, profile=args.profile)
        buggy = run_tests(c, c.buggy, profile=args.profile)
        ok = fixed.passed and not buggy.passed and not buggy.error
        bad += not ok
        note = "" if ok else f"  <- fixed passed={fixed.passed} buggy passed={buggy.passed} {fixed.error or buggy.error or ''}"
        print(f"{'ok  ' if ok else 'FAIL'} {c.id} fixed {fixed.tests} tests pass={fixed.passed}; buggy fails {len(buggy.failures)}{note}")
    print(f"\n{'all cases demonstrate their bug' if not bad else f'{bad} case(s) broken'}")
    return 1 if bad else 0


def _cmd_mutate(args: argparse.Namespace) -> int:
    cases = [find_case(args.case)] if args.case else all_cases()
    results = {}
    for c in cases:
        r = mutate_case(c, profile=args.profile)
        results[c.id] = {"killed": r.killed, "total": r.total, "survivors": r.survivors}
        print(f"{c.id}  {r.killed}/{r.total} mutants killed ({r.score:.0%})")
        for s in r.survivors:
            print(f"      survived: {s}")
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    """Write the case table into README.md (mutation scores from a `mutate --out` JSON file)."""
    scores = json.loads(pathlib.Path(args.scores).read_text(encoding="utf-8")) if args.scores else {}
    rows = ["| # | Case | Severity | Weakness | Origin | Mutants killed |", "|---|---|---|---|---|---|"]
    for c in all_cases():
        rel = c.path.relative_to(cases_root().parent).as_posix()
        s = scores.get(c.id)
        score = f"{s['killed']}/{s['total']}" if s else "not run"
        origin = "found in my projects" if c.origin == "real" else "classic pattern"
        rows.append(f"| {c.id} | [{c.title}]({rel}/EVALUATION.md) | {c.severity} | {c.cwe} | {origin} | {score} |")
    table = "\n".join(rows)
    readme = cases_root().parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    a, b = text.index(REPORT_START) + len(REPORT_START), text.index(REPORT_END)
    readme.write_text(text[:a] + "\n" + table + "\n" + text[b:], encoding="utf-8")
    print(f"updated {readme}")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser(prog="casebook", description=__doc__)
    p.add_argument("--version", action="version", version=f"casebook {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list the cases").set_defaults(fn=_cmd_list)
    g = sub.add_parser("grade", help="grade a candidate fix for one case")
    g.add_argument("case", help="case id, e.g. 02")
    g.add_argument("file", help="Python file that defines the case's function")
    g.add_argument("--json", action="store_true")
    g.add_argument("--profile", default="default", choices=["default", "fast"])
    g.set_defaults(fn=_cmd_grade)
    c = sub.add_parser("check", help="every fix passes and every bug fails")
    c.add_argument("--profile", default="fast", choices=["default", "fast"])
    c.set_defaults(fn=_cmd_check)
    m = sub.add_parser("mutate", help="mutation-test the fixes")
    m.add_argument("case", nargs="?")
    m.add_argument("--out", help="write scores as JSON")
    m.add_argument("--profile", default="fast", choices=["default", "fast"])
    m.set_defaults(fn=_cmd_mutate)
    r = sub.add_parser("report", help="write the case table into README.md")
    r.add_argument("--scores", help="JSON from `casebook mutate --out`")
    r.set_defaults(fn=_cmd_report)
    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except (KeyError, ValueError) as e:
        print(f"casebook: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
