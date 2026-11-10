def is_subset(items, allowed):
    """Return True only if every item is in `allowed`."""
    return all(str(i) in {str(a) for a in allowed} for i in items)
