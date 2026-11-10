"""Find and describe the cases on disk."""

from __future__ import annotations

import os
import pathlib
import tomllib
from dataclasses import dataclass

REQUIRED = ("id", "title", "function", "severity", "cwe", "origin", "source")
SEVERITIES = ("low", "medium", "high", "critical")
ORIGINS = ("real", "classic")


@dataclass(frozen=True)
class Case:
    id: str
    title: str
    function: str
    severity: str
    cwe: str
    origin: str
    source: str
    path: pathlib.Path

    @property
    def fixed(self) -> pathlib.Path:
        return self.path / "fixed.py"

    @property
    def buggy(self) -> pathlib.Path:
        return self.path / "buggy.py"


def cases_root() -> pathlib.Path:
    """The `cases/` directory: $CASEBOOK_CASES, else the nearest one above the cwd, else the repo's."""
    env = os.environ.get("CASEBOOK_CASES")
    if env:
        return pathlib.Path(env).resolve()
    here = pathlib.Path.cwd().resolve()
    for d in (here, *here.parents):
        if (d / "cases").is_dir() and any((d / "cases").glob("*/case.toml")):
            return d / "cases"
    return (pathlib.Path(__file__).resolve().parents[2] / "cases").resolve()


def load_case(path: pathlib.Path) -> Case:
    data = tomllib.loads((path / "case.toml").read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if not str(data.get(k, "")).strip()]
    if missing:
        raise ValueError(f"{path.name}/case.toml is missing {', '.join(missing)}")
    if data["severity"] not in SEVERITIES:
        raise ValueError(f"{path.name}: severity must be one of {SEVERITIES}")
    if data["origin"] not in ORIGINS:
        raise ValueError(f"{path.name}: origin must be one of {ORIGINS}")
    return Case(path=path, **{k: str(data[k]) for k in REQUIRED})


def all_cases(root: pathlib.Path | None = None) -> list[Case]:
    root = root or cases_root()
    return [load_case(p.parent) for p in sorted(root.glob("*/case.toml"))]


def find_case(key: str, root: pathlib.Path | None = None) -> Case:
    """Look a case up by id (`02`) or by directory name."""
    for case in all_cases(root):
        if key in (case.id, case.path.name) or case.path.name.startswith(f"{key}_"):
            return case
    raise KeyError(f"no case {key!r}; run `casebook list`")
