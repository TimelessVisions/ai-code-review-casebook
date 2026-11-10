import posixpath


def is_inside(base: str, user_path: str) -> bool:
    """True if base/user_path stays inside base (POSIX paths)."""
    return posixpath.normpath(posixpath.join(base, user_path)).startswith(base)
