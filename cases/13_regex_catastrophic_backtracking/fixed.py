import re

_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def is_valid_name(name: str) -> bool:
    """Lowercase letters and digits, in groups joined by single hyphens."""
    return _NAME.fullmatch(name) is not None
