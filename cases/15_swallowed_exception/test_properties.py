import json
import pathlib
import tempfile

from hypothesis import given, strategies as st

values = st.recursive(st.none() | st.booleans() | st.integers() | st.text(max_size=5),
                      lambda c: st.lists(c, max_size=3) | st.dictionaries(st.text(max_size=5), c, max_size=3),
                      max_leaves=8)


@given(st.dictionaries(st.text(max_size=8), values, max_size=5))
def test_valid_config_round_trips(impl, cfg):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "c.json"
        p.write_text(json.dumps(cfg), encoding="utf-8")
        assert impl.load_config(str(p)) == cfg
