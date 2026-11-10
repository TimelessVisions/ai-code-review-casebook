def cap(data: str) -> str:
    """Cap a log message at 200 characters."""
    return data.encode("utf-8")[:200].decode()
