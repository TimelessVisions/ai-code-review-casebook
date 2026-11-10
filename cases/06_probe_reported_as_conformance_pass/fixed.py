def status(results: dict[str, bool], required_total: int) -> str:
    if len(results) < required_total:
        return "NOT_MEASURED"  # never a pass for checks that did not run
    return "PASS" if all(results.values()) else "FAIL"
