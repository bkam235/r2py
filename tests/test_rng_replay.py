"""R's random draws are inputs: recorded on the R side, served to Python's random functions at verification."""
import json
import tempfile
from pathlib import Path

import pytest

from r2py.stage0.effects import rng
from r2py.stage0.sandbox.base import ReplayLog

np = pytest.importorskip("numpy")


def _install(draws):
    ns = {}
    exec(rng._py_replay_preamble(ReplayLog(rng_draws=draws)), ns)


def _script(src: str) -> dict:
    """Run *src* the way the sandbox runs a translation: as ``__main__``."""
    ns = {"__name__": "__main__"}
    exec(src, ns)
    return ns


def test_numpy_legacy_functions_are_served_in_order_and_shape():
    _install([("rnorm", [], [0.5, -1.5, 2.5, 0.25]), ("runif", [], [0.75]), ("rbinom", [], [1, 0, 1])])
    ns = _script("import numpy as np\n"
                 "a = np.random.normal(0, 1, 4).tolist()\n"
                 "b = np.random.uniform()\n"
                 "c = np.random.binomial(1, 0.5, 3)\n")
    assert ns["a"] == [0.5, -1.5, 2.5, 0.25]          # R's values, whatever the arguments
    assert ns["b"] == 0.75                             # a scalar draw is a scalar
    assert ns["c"].tolist() == [1, 0, 1] and ns["c"].dtype.kind == "i"


def test_dims_style_and_numpy_integer_sizes():
    _install([("rnorm", [], [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]), ("runif", [], [0.1, 0.2, 0.3])])
    ns = _script("import numpy as np\na = np.random.randn(2, 3)\nb = np.random.uniform(size=np.int64(3))\n")
    assert ns["a"].shape == (2, 3)
    assert ns["b"].tolist() == [0.1, 0.2, 0.3]


def test_generator_is_served_and_keeps_its_type():
    _install([("rnorm", [], [9.0, 8.0]), ("sample", [], [3, 1, 2])])
    ns = _script("import numpy as np\n"
                 "g = np.random.default_rng(1)\n"
                 "a = g.normal(size=2).tolist()\n"
                 "c = g.choice([1, 2, 3], 3, replace=False).tolist()\n"
                 "same = np.random.default_rng(g) is g\n"
                 "rs = np.random.RandomState(0)\n"
                 "rs_untouched = isinstance(np.random.mtrand._rand, np.random.RandomState) and isinstance(rs, np.random.RandomState)\n")
    assert (ns["a"], ns["c"]) == ([9.0, 8.0], [3, 1, 2])
    assert isinstance(ns["g"], np.random.Generator)
    assert ns["same"]                                  # libraries pass generators back into default_rng
    assert ns["rs_untouched"]                          # RandomState is left alone: sklearn checks isinstance


def test_stdlib_random_is_served():
    _install([("runif", [], [0.125]), ("rnorm", [], [1.5]), ("sample", [], [4, 2])])
    ns = _script("import random\na = random.random()\nb = random.gauss(0, 1)\nc = random.sample(range(10), 2)\n")
    assert (ns["a"], ns["b"], ns["c"]) == (0.125, 1.5, [4, 2])


def test_a_different_count_or_no_draw_left_falls_through_to_the_real_generator():
    _install([("rnorm", [], [1.0, 2.0])])
    ns = _script("import numpy as np\na = len(np.random.normal(size=5))\nb = np.random.normal(size=2).tolist()\n"
                 "c = len(np.random.normal(size=2))\n")
    assert ns["a"] == 5                                # R drew 2, Python wants 5: not served
    assert ns["b"] == [1.0, 2.0]                       # the draw of 2 is still there
    assert ns["c"] == 2                                # exhausted: real numbers


def test_library_internal_draws_do_not_use_up_the_scripts_draws():
    _install([("rnorm", [], [1.0, 2.0])])
    lib = {"__name__": "some_library"}                 # a call whose caller is not the script
    exec("import numpy as np\nlib_draw = np.random.normal(size=2).tolist()\n", lib)
    assert lib["lib_draw"] != [1.0, 2.0]
    ns = _script("import numpy as np\nmine = np.random.normal(size=2).tolist()\n")
    assert ns["mine"] == [1.0, 2.0]


def test_no_draws_leaves_numpy_working():
    _install([])
    assert _script("import numpy as np\na = np.random.normal(size=3)\n")["a"].shape == (3,)


def test_r_log_entries_are_decoded_to_fn_args_values():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "_r2py_rng.json").write_text(json.dumps(
            [{"fn": "rnorm", "value": [0.1, 0.2]}, {"fn": "runif", "value": 0.5}]), encoding="utf-8")
        log = rng.collect(Path(d))["rng_log"]
    assert log == [("rnorm", [], [0.1, 0.2]), ("runif", [], [0.5])]


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_translation_that_draws_its_own_numbers_matches_r():
    from r2py.stage1 import analyze
    from r2py.stage4 import verifier

    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "draws.R"
        r.write_text("set.seed(1)\nx <- rnorm(5)\ny <- runif(3, 1, 2)\nz <- sample(1:10)\n", encoding="utf-8")
        sm = analyze(r)
        legacy = "import numpy as np\nx = np.random.normal(size=5)\ny = np.random.uniform(1, 2, 3)\nz = np.random.choice(np.arange(1, 11), 10, replace=False)\n"
        gen = "import numpy as np\nrng = np.random.default_rng(7)\nx = rng.normal(size=5)\ny = rng.uniform(1, 2, 3)\nz = rng.choice(np.arange(1, 11), 10, replace=False)\n"
        for src in (legacy, gen):
            assert verifier.verify(sm, src, data_compare="exact", timeout_s=60).aggregate == 1.0
        hardcoded = "x = [1.0] * 5\ny = [1.5] * 3\nz = list(range(1, 11))\n"
        assert verifier.verify(sm, hardcoded, data_compare="exact", timeout_s=60).aggregate < 0.5
