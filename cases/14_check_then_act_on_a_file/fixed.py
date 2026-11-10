def write_if_absent(path: str, data: str) -> bool:
    """Create `path` with `data` unless it exists. Return True if written."""
    try:
        with open(path, "x", encoding="utf-8", newline="") as f:
            f.write(data)
    except FileExistsError:
        return False
    return True
