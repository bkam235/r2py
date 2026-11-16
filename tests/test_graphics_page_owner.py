"""Epoch 15 (2026-11-16): a page belongs to the entity that started it, on both sides.

R's checkpoints keep a page open across entities and give it, with everything later entities add to it, to the
entity that started it (``stage1/runner.py``, ``.r2py_gfx_flush``). The Python checkpoints snapshotted and closed
every figure at each checkpoint, so the opener entity had only its own drawing and each addition became a page of
its own (shape filledmultigonal: R 458 polygons at ``emptyplot``, Python 0; getellipse, Arrows, prodlim backGround).
And R's fingerprints are written with ``auto_unbox``, so a one-point series arrived as a scalar the comparator read
as "nothing plotted" (backGround: ``plot(0, 0)``)."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

from r2py.stage4.comparators.graphics import GraphicsComparator
from r2py.stage4.decompose import _compare_entity_bundles
from r2py.types import EffectClass


def _ents(**spans):
    return {e: NS(source_span=NS(start_line=a, end_line=b)) for e, (a, b) in spans.items()}


def _py_checkpointed(src: str, eids: list[str]):
    """Run a Python program with a checkpoint after each line (one entity per line) and collect its bundles."""
    from r2py.stage0.sandbox.py_sandbox import PySandbox
    from r2py.stage1.runner import DEFAULT_CAPTURE
    from r2py.stage4.verifier import _PY_CHECKPOINT_PREAMBLE, _collect_py_checkpoints
    lines = src.strip().splitlines()
    body = "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n"
    for eid, line in zip(eids, lines):
        body += f"{line}\n_r2py_checkpoint('{eid}')\n"
    with tempfile.TemporaryDirectory() as d:
        b = PySandbox().run(body, workdir=Path(d), capture=DEFAULT_CAPTURE, preamble=_PY_CHECKPOINT_PREAMBLE,
                            timeout_s=120)
        assert b.exit_code == 0, b.stderr[-600:]
        return _collect_py_checkpoints(Path(d), eids)


def _n_pages(eb):
    if eb.graphics_meta:
        return len(eb.graphics_meta)
    return eb.graphics if isinstance(eb.graphics, int) else len(eb.graphics or [])


class TestPythonPageOwner(unittest.TestCase):
    def test_additions_by_later_entities_land_on_the_opener_page(self):
        pb = _py_checkpointed("fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 2, 3])\n"
                              "ax.plot([1, 2, 3], [3, 2, 1])\n"
                              "x = 1\n",
                              ["plot", "lines", "x"])
        self.assertEqual(_n_pages(pb["plot"]), 1)
        self.assertEqual(pb["plot"].graphics_meta[0]["seg"], [3, 3])     # both lines on the opener's page
        self.assertEqual(_n_pages(pb["lines"]), 0)                        # an addition is no page of its own

    def test_a_new_figure_is_a_new_page_of_its_entity(self):
        pb = _py_checkpointed("plt.figure(); plt.plot([1, 2, 3])\n"
                              "plt.figure(); plt.plot([3, 2, 1])\n",
                              ["p1", "p2"])
        self.assertEqual((_n_pages(pb["p1"]), _n_pages(pb["p2"])), (1, 1))
        self.assertEqual(pb["p1"].graphics_meta[0]["py"], [1.0, 2.0, 3.0])
        self.assertEqual(pb["p2"].graphics_meta[0]["py"], [3.0, 2.0, 1.0])


    def test_an_empty_figure_is_a_page_as_plot_new_is(self):
        pb = _py_checkpointed("plt.figure()\n"
                              "plt.xlim(0, 150)\n"
                              "plt.plot([1, 2, 3])\n",
                              ["plot.new", "plot.window", "lines"])
        self.assertEqual([_n_pages(pb[e]) for e in ("plot.new", "plot.window", "lines")], [1, 0, 0])
        self.assertEqual(pb["plot.new"].graphics_meta[0]["py"], [1.0, 2.0, 3.0])

    def test_the_checkpoint_leaves_the_current_figure_and_its_size_alone(self):
        pb = _py_checkpointed("f1 = plt.figure(figsize=(3, 2)); plt.plot([1, 2])\n"
                              "f0 = plt.figure(); g = plt.figure(); plt.plot([5, 6]); plt.figure(g.number)\n"
                              "plt.plot([7, 8]); s = list(g.get_size_inches())\n",
                              ["a", "b", "c"])
        self.assertEqual(pb["b"].graphics_meta[1]["py"], [5.0, 6.0, 7.0, 8.0])   # c drew on b's current figure g
        self.assertEqual(pb["c"].data["s"], [6.4, 4.8])                           # matplotlib's default size kept


class TestBothSides(unittest.TestCase):
    def test_a_faithful_plot_with_additions_matches_r_per_entity(self):
        from r2py.stage1.runner import run_script_checkpointed
        r_src = "plot(1:3, 1:3, type = 'l')\nlines(1:3, 3:1)\nx <- 1\n"
        try:
            rb = run_script_checkpointed(r_src, _ents(plot=(0, 0), lines=(1, 1), x=(2, 2)), timeout_s=120)[1]
        except Exception as exc:          # no R on this machine
            self.skipTest(f"R not available: {exc}")
        pb = _py_checkpointed("fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 2, 3])\n"
                              "ax.plot([1, 2, 3], [3, 2, 1])\n"
                              "x = 1\n",
                              ["plot", "lines", "x"])
        res = _compare_entity_bundles(rb["plot"], pb["plot"])[EffectClass.GRAPHICS]
        self.assertGreaterEqual(res.score, 0.99, res.explanation)
        self.assertEqual(_n_pages(rb["lines"]), _n_pages(pb["lines"]))


class TestUnboxedScalars(unittest.TestCase):
    def test_a_one_point_r_series_is_a_series(self):
        r = {"src": "base", "title": "", "xlab": "0", "ylab": "0", "texts": [], "px": 0, "py": 0, "seg": 1,
             "bars": [], "n_polys": 0, "n_segs": 0, "n_img": 0}
        p = {"src": "mpl", "title": "", "xlab": "", "ylab": "", "texts": [], "px": [0.0], "py": [0.0], "seg": [1],
             "bars": [], "n_polys": 0, "n_segs": 0, "n_img": 0}
        res = GraphicsComparator().compare([b""], [b""], [r], [p])
        self.assertEqual(res.score, 1.0, res.explanation)


if __name__ == "__main__":
    unittest.main()
