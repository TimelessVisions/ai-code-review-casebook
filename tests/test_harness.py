"""Tests for the harness itself: registry, grading, mutation, CLI."""

import json
import pathlib
import subprocess
import sys

import pytest

from casebook import cli
from casebook.grading import run_tests, verdict
from casebook.mutation import mutants
from casebook.registry import all_cases, find_case, load_case

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_there_are_fifteen_cases_with_unique_ids():
    cases = all_cases()
    assert len(cases) == 15
    assert len({c.id for c in cases}) == 15


def test_every_case_has_the_full_set_of_files():
    for c in all_cases():
        for name in ("buggy.py", "fixed.py", "test_examples.py", "test_properties.py", "EVALUATION.md", "case.toml"):
            assert (c.path / name).is_file(), f"{c.path.name} lacks {name}"


def test_origin_labels_are_honest():
    by_origin = {c.origin for c in all_cases()}
    assert by_origin == {"real", "classic"}
    real = [c for c in all_cases() if c.origin == "real"]
    assert [c.id for c in real] == ["01", "02", "03", "04", "05", "06"]
    for c in all_cases():
        if c.origin == "classic":
            assert "Not found in my projects" in c.source


def test_find_case_by_id_and_name():
    assert find_case("02").title.startswith("Cap a message")
    assert find_case("02_slice_bytes_then_decode").id == "02"
    with pytest.raises(KeyError):
        find_case("99")


def test_load_case_rejects_bad_metadata(tmp_path):
    (tmp_path / "case.toml").write_text('id = "x"\n', encoding="utf-8")
    with pytest.raises(ValueError, match="missing"):
        load_case(tmp_path)


def test_a_wrong_fix_is_rejected_with_a_review():
    case = find_case("02")
    result = run_tests(case, case.buggy, profile="fast")
    assert not result.passed and result.failures
    text = verdict(result)
    assert "**Verdict:** reject" in text and "CWE-135" in text
    assert "smallest breaking input found" in text


def test_a_correct_fix_is_accepted():
    case = find_case("02")
    result = run_tests(case, case.fixed, profile="fast")
    assert result.passed and result.tests >= 3
    assert "**Verdict:** accept" in verdict(result)


def test_an_alternative_correct_fix_is_accepted(tmp_path):
    alt = tmp_path / "alt.py"
    alt.write_text('def cap(data):\n    return "".join(list(data)[:200])\n', encoding="utf-8")
    assert run_tests(find_case("02"), alt, profile="fast").passed


def test_a_plausible_but_wrong_fix_is_caught_by_the_property_test(tmp_path):
    """Passes the examples (é*150 fits) but caps at 199, not 200."""
    off_by_one = tmp_path / "off.py"
    off_by_one.write_text("def cap(data):\n    return data[:199]\n", encoding="utf-8")
    result = run_tests(find_case("02"), off_by_one, profile="fast")
    assert not result.passed
    failing = {f.test: f for f in result.failures}
    assert "test_is_a_prefix_of_at_most_200_characters" in failing
    assert failing["test_is_a_prefix_of_at_most_200_characters"].falsifying, "the breaking input must be reported"


def test_a_missing_file_is_an_error_not_a_pass(tmp_path):
    result = run_tests(find_case("02"), tmp_path / "nope.py")
    assert not result.passed and result.error


def test_a_candidate_without_the_function_fails(tmp_path):
    empty = tmp_path / "empty.py"
    empty.write_text("x = 1\n", encoding="utf-8")
    assert not run_tests(find_case("02"), empty, profile="fast").passed


def test_mutants_change_the_code_and_skip_noops():
    src = "def f(a, b):\n    if a == b:\n        return 1\n    return a + b\n"
    found = mutants(src)
    assert len(found) >= 4
    assert all(new != src for _, new in found)
    assert len({new for _, new in found}) == len(found)


def test_mutants_leave_docstrings_alone():
    src = 'def f():\n    """hello"""\n    return 1\n'
    for _, new in mutants(src):
        assert "hello" in new


def test_cli_list_and_grade(capsys, tmp_path):
    assert cli.main(["list"]) == 0
    assert "SQL query built with an f-string" in capsys.readouterr().out
    good = tmp_path / "good.py"
    good.write_text(find_case("10").fixed.read_text(encoding="utf-8"), encoding="utf-8")
    assert cli.main(["grade", "10", str(good), "--profile", "fast"]) == 0
    assert cli.main(["grade", "10", str(find_case("10").buggy), "--profile", "fast"]) == 1


def test_cli_grade_json(capsys):
    code = cli.main(["grade", "05", str(find_case("05").buggy), "--json", "--profile", "fast"])
    data = json.loads(capsys.readouterr().out)
    assert code == 1 and data["passed"] is False and data["failures"]


def test_cli_unknown_case_is_exit_2(capsys):
    assert cli.main(["grade", "99", "x.py"]) == 2


def test_console_script_runs():
    r = subprocess.run([sys.executable, "-m", "casebook.cli", "--version"], capture_output=True, text=True)
    assert r.returncode == 0 and "casebook" in r.stdout
