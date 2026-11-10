import posixpath


def is_inside(base: str, user_path: str) -> bool:
    """True if base/user_path stays inside base (POSIX paths)."""
    base = posixpath.normpath(base)
    target = posixpath.normpath(posixpath.join(base, user_path))
    return target == base or target.startswith(base.rstrip("/") + "/")
