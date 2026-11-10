from decimal import Decimal


def total_cents(prices: list[str]) -> int:
    """Sum prices like "0.29" and return the total in cents."""
    return int(sum((Decimal(p) for p in prices), Decimal(0)) * 100)
