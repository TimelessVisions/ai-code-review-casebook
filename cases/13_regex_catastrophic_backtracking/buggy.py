import re


def is_valid_name(name: str) -> bool:
    """Lowercase letters and digits, in groups joined by single hyphens."""
    return re.fullmatch(r"([a-z0-9]+-?)*", name) is not None
