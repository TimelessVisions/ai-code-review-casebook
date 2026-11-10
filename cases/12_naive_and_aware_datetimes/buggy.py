from datetime import datetime


def is_expired(expires_at: str, now: datetime | None = None) -> bool:
    return datetime.fromisoformat(expires_at) < (now or datetime.now())
