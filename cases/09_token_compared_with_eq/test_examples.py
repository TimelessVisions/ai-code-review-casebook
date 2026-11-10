import hmac


def test_uses_a_constant_time_comparison(impl, monkeypatch):
    calls = []
    real = hmac.compare_digest

    def spy(a, b):
        calls.append((a, b))
        return real(a, b)

    monkeypatch.setattr(hmac, "compare_digest", spy)
    assert impl.check_token("abc", "abc") is True
    assert calls, "the comparison must go through hmac.compare_digest"


def test_wrong_token_is_rejected(impl):
    assert impl.check_token("abd", "abc") is False
