from hypothesis import given, strategies as st


@given(st.lists(st.booleans(), max_size=30), st.integers(0, 30))
def test_status_reflects_coverage_then_results(impl, outcomes, required):
    results = {f"c{i}": ok for i, ok in enumerate(outcomes)}
    got = impl.status(results, required)
    if len(results) < required:
        assert got == "NOT_MEASURED"
    else:
        assert got == ("PASS" if all(outcomes) else "FAIL")
