import pytest


def test_past_expiry_is_expired(impl):
    assert impl.is_expired("2000-01-01T00:00:00+00:00") is True


def test_future_expiry_is_not(impl):
    assert impl.is_expired("2999-01-01T00:00:00+00:00") is False


def test_expiry_without_timezone_is_refused(impl):
    with pytest.raises(ValueError):
        impl.is_expired("2000-01-01T00:00:00")
