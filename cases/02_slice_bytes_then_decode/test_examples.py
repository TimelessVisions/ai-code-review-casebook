def test_multibyte_character_at_the_cut_does_not_crash(impl):
    # "a" shifts every 2-byte "é" by one, so byte 200 falls inside a character.
    s = "a" + "é" * 150
    assert impl.cap(s) == s  # 151 characters: under the cap, returned whole


def test_caps_characters_not_bytes(impl):
    assert impl.cap("é" * 150) == "é" * 150
    assert len(impl.cap("a" * 500)) == 200
