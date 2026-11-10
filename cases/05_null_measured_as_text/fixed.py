def within_max_length(value, limit: int) -> bool:
    if not isinstance(value, str):
        return False  # null/numbers cannot be measured by a length rule: fail closed
    return len(value) <= limit
