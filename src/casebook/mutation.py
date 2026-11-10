"""Small AST mutation testing: break a fix in small ways and check the tests notice."""

from __future__ import annotations

import ast
import copy
import pathlib
import tempfile
from dataclasses import dataclass, field

from .grading import run_tests
from .registry import Case

_CMP_SWAP = {
    ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
    ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
    ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In,
}
_BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.FloorDiv, ast.FloorDiv: ast.Mult}


def _sites(tree: ast.AST) -> list[tuple[int, str, int]]:
    """(node index in walk order, kind, sub-index) for every mutation point."""
    docstrings = {
        id(n.body[0].value)
        for n in ast.walk(tree)
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)
    }
    out = []
    for i, n in enumerate(ast.walk(tree)):
        if isinstance(n, ast.Compare):
            out += [(i, "cmp", k) for k, op in enumerate(n.ops) if type(op) in _CMP_SWAP]
        elif isinstance(n, ast.BoolOp):
            out.append((i, "bool", 0))
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            out.append((i, "not", 0))
        elif isinstance(n, ast.BinOp) and type(n.op) in _BIN_SWAP:
            out.append((i, "bin", 0))
        elif isinstance(n, ast.Constant) and id(n) not in docstrings:
            if isinstance(n.value, bool) or (isinstance(n.value, int)) or (isinstance(n.value, str) and n.value):
                out.append((i, "const", 0))
        elif isinstance(n, ast.Return) and n.value is not None:
            out.append((i, "return", 0))
        elif isinstance(n, ast.If):
            out.append((i, "if", 0))
    return out


def _apply(n: ast.AST, kind: str, k: int) -> str:
    if kind == "cmp":
        old = type(n.ops[k]); n.ops[k] = _CMP_SWAP[old]()
        return f"{old.__name__} -> {type(n.ops[k]).__name__}"
    if kind == "bool":
        n.op = ast.Or() if isinstance(n.op, ast.And) else ast.And()
        return f"boolean operator -> {type(n.op).__name__}"
    if kind == "not":
        n.operand = ast.UnaryOp(op=ast.Not(), operand=n.operand)
        return "removed `not`"
    if kind == "bin":
        old = type(n.op); n.op = _BIN_SWAP[old]()
        return f"{old.__name__} -> {type(n.op).__name__}"
    if kind == "const":
        v = n.value
        n.value = (not v) if isinstance(v, bool) else (v + 1 if isinstance(v, int) else "")
        return f"constant {v!r} -> {n.value!r}"
    if kind == "return":
        n.value = ast.Constant(value=None)
        return "return value -> None"
    if kind == "if":
        n.test = ast.UnaryOp(op=ast.Not(), operand=n.test)
        return "negated if-condition"
    raise ValueError(kind)


def mutants(source: str) -> list[tuple[str, str]]:
    """Every single-point mutant of `source`, as (description, new source); no-ops are dropped."""
    tree = ast.parse(source)
    original = ast.unparse(tree)
    out, seen = [], {original}
    for idx, kind, k in _sites(tree):
        t = copy.deepcopy(tree)
        node = next(n for i, n in enumerate(ast.walk(t)) if i == idx)
        desc = _apply(node, kind, k)
        ast.fix_missing_locations(t)
        new = ast.unparse(t)
        if new not in seen:
            seen.add(new)
            line = getattr(node, "lineno", "?")
            out.append((f"line {line}: {desc}", new))
    return out


@dataclass
class MutationResult:
    case: Case
    total: int = 0
    killed: int = 0
    survivors: list[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        return self.killed / self.total if self.total else 1.0


def mutate_case(case: Case, *, profile: str = "fast", timeout: float = 120) -> MutationResult:
    result = MutationResult(case=case)
    source = case.fixed.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="casebook-mut-") as tmp:
        for n, (desc, src) in enumerate(mutants(source)):
            path = pathlib.Path(tmp) / f"mutant_{n}.py"
            path.write_text(src, encoding="utf-8")
            graded = run_tests(case, path, profile=profile, timeout=timeout)
            result.total += 1
            if graded.passed:
                result.survivors.append(desc)
            else:
                result.killed += 1
    return result
