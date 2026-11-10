import os


def write_if_absent(path: str, data: str) -> bool:
    """Create `path` with `data` unless it exists. Return True if written."""
    if os.path.exists(path):
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    return True
