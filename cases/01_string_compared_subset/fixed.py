def is_subset(items, allowed):
    """Return True only if every item is in `allowed` (same type and equal)."""
    return all(any(type(i) is type(a) and i == a for a in allowed) for i in items)
