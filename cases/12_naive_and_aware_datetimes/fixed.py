from datetime import datetime, timezone


def is_expired(expires_at: str, now: datetime | None = None) -> bool:
    expiry = datetime.fromisoformat(expires_at)
    if expiry.tzinfo is None:
        raise ValueError("expiry must include a timezone offset")
    return expiry < (now or datetime.now(timezone.utc))
