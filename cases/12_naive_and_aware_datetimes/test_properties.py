from datetime import datetime, timedelta, timezone

from hypothesis import given, strategies as st

aware = st.datetimes(
    min_value=datetime(1990, 1, 1), max_value=datetime(2100, 1, 1),
    timezones=st.sampled_from([timezone.utc, timezone(timedelta(hours=5)), timezone(timedelta(hours=-8))]),
)


@given(aware, aware)
def test_compares_instants_across_offsets(impl, expiry, now):
    assert impl.is_expired(expiry.isoformat(), now) is (expiry < now)
