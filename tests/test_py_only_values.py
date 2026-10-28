"""A Python variable R has no data for is recorded by its type, not serialized (2026-10-28).

The checkpoints serialized every global; ragg agg_webp_anim kept a list of image frames that R never had and ran
20-90 s instead of 1.3 s, past the 60 s sandbox limit."""
import numpy as np

from r2py.stage0.effects.data import build_py_preamble
from r2py.stage4.verifier import _py_only_preamble
from r2py.types import EffectBundle


def _serializer(r_names, entity_names):
    ns = {}
    exec(build_py_preamble(), ns)
    exec(_py_only_preamble(EffectBundle(data={n: 1 for n in r_names}),
                           {"e": EffectBundle(data={n: 1 for n in entity_names})}), ns)
    return ns["_r2py_try_serialize"]


def test_names_r_has_are_serialized_and_others_get_a_placeholder():
    ser = _serializer(["x"], ["y"])
    assert ser("x", np.arange(3)) == ([0, 1, 2], True)
    assert ser("y", {"a": 1}) == ({"a": 1}, True)
    assert ser("frames", [np.zeros((400, 500, 4), dtype="uint8")] * 10) == ({"__r2py_py_only__": "list"}, True)


def test_no_r_data_means_every_value_is_a_placeholder():
    assert _serializer([], [])("x", 1.5) == ({"__r2py_py_only__": "float"}, True)
