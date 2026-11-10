def test_key_beginning_with_dash_parses(impl, monkeypatch):
    monkeypatch.setattr("secrets.token_urlsafe", lambda n=None: "-abc123")
    ns = impl.parse(impl.make_argv())
    assert ns.key == "-abc123"
