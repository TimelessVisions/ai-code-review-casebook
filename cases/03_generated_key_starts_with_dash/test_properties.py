import string
from unittest import mock

from hypothesis import given, strategies as st

ALPHABET = string.ascii_letters + string.digits + "-_"


@given(st.text(alphabet=ALPHABET, min_size=1, max_size=64))
def test_any_url_safe_key_round_trips(impl, key):
    with mock.patch("secrets.token_urlsafe", lambda n=None: key):
        assert impl.parse(impl.make_argv()).key == key
