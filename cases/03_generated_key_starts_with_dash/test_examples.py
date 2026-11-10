def test_key_beginning_with_dash_parses(impl, monkeypatch):
    monkeypatch.setattr("secrets.token_urlsafe", lambda n=None: "-abc123")
    assert impl.parse(impl.make_argv()).key == "-abc123"


def test_real_keys_round_trip(impl):
    for _ in range(50):
        argv = impl.make_argv()
        assert impl.parse(argv).key
