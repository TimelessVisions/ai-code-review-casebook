def total_cents(prices: list[str]) -> int:
    """Sum prices like "0.29" and return the total in cents."""
    return int(sum(float(p) for p in prices) * 100)
