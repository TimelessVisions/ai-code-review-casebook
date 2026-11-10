import hmac


def check_token(given: str, expected: str) -> bool:
    return hmac.compare_digest(given.encode(), expected.encode())
