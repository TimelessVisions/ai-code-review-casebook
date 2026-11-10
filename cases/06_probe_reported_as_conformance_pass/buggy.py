def status(results: dict[str, bool], required_total: int) -> str:
    return "PASS" if all(results.values()) else "FAIL"
