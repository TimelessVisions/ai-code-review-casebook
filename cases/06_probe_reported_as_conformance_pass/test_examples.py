def test_three_of_177_is_not_a_pass(impl):
    probe = {f"check{i}": True for i in range(3)}
    assert impl.status(probe, 177) == "NOT_MEASURED"


def test_full_run_can_pass_or_fail(impl):
    ok = {f"c{i}": True for i in range(177)}
    assert impl.status(ok, 177) == "PASS"
    ok["c5"] = False
    assert impl.status(ok, 177) == "FAIL"
