def test_multibyte_text_does_not_crash(impl):
    assert len(impl.cap("é" * 150)) <= 200


def test_caps_characters_not_bytes(impl):
    assert impl.cap("é" * 150) == "é" * 150
    assert len(impl.cap("a" * 500)) == 200
