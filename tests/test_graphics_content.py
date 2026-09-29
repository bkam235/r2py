"""Content-aware graphics comparison: fingerprint comparator + real R/matplotlib capture."""
import tempfile
import unittest
from pathlib import Path

from r2py.stage4.comparators.graphics import GraphicsComparator, _page_score, _seq_sim


def fp(**kw):
    base = {"src": "x", "title": "", "xlab": "", "ylab": "", "texts": [], "px": [], "py": [],
            "bars": [], "n_polys": 0, "n_segs": 0, "n_img": 0}
    base.update(kw)
    return base


class TestComparator(unittest.TestCase):
    cmp = GraphicsComparator()

    def test_same_data_passes_and_wrong_data_or_empty_does_not(self):
        r = fp(px=[1, 2, 3], py=[1, 4, 9])
        self.assertEqual(_page_score(r, fp(px=[0, 1, 2], py=[1, 4, 9])), 1.0)  # x shifted: index base
        self.assertLess(_page_score(r, fp(px=[1, 2, 3], py=[1, 2, 3])), 0.9)
        self.assertEqual(_page_score(r, fp()), 0.0)
        self.assertEqual(_page_score(r, fp(bars=[1, 4, 9])), 0.0)

    def test_r_default_labels_are_not_content(self):
        r = fp(py=[1], px=[1], xlab="c(1, 2)", ylab="Index", title="Histogram of x")
        self.assertEqual(_page_score(r, fp(py=[1], px=[1])), 1.0)
        r = fp(py=[1], px=[1], title="Growth")
        self.assertLess(_page_score(r, fp(py=[1], px=[1])), 1.0)

    def test_pages_pair_in_order_and_extras_score_zero(self):
        a, b = fp(bars=[1, 2]), fp(bars=[5, 6])
        self.assertEqual(self.cmp.compare([b"x"] * 2, [b"x"] * 2, [a, b], [a, b]).score, 1.0)
        self.assertAlmostEqual(self.cmp.compare([b"x"] * 2, [b"x"], [a, b], [a]).score, 0.5)
        self.assertEqual(self.cmp.compare([b"x"], [b"x"], [a], [b]).verdict, "fail")

    def test_unextractable_page_is_skipped_not_guessed(self):
        r = self.cmp.compare([b"x"] * 2, [b"x"] * 2, [None, fp(bars=[1])], [fp(bars=[9]), fp(bars=[1])])
        self.assertEqual(r.score, 1.0)

    def test_without_fingerprints_only_counts_are_compared(self):
        self.assertEqual(self.cmp.compare([b"a"], [b"b"]).verdict, "pass")  # no SSIM guess
        self.assertEqual(self.cmp.compare([b"a"], []).score, 0.0)

    def test_seq_sim(self):
        self.assertEqual(_seq_sim([3, 1, 2], [1, 2, 3]), 1.0)
        self.assertEqual(_seq_sim([1], []), 0.0)


class TestCaptureEndToEnd(unittest.TestCase):
    """R base plots, R multi-page and matplotlib through the real sandboxes."""

    def _run(self, r_src, py_src):
        from r2py.stage0.sandbox.py_sandbox import PySandbox
        from r2py.stage0.sandbox.r_sandbox import RSandbox
        from r2py.types import EffectClass
        cap = frozenset({EffectClass.GRAPHICS})
        m = "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\n"
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            rb = RSandbox().run(r_src, workdir=Path(a), capture=cap, timeout_s=120)
            pb = PySandbox().run(m + py_src, workdir=Path(b), capture=cap, timeout_s=120)
        return rb, pb, GraphicsComparator().compare(rb.graphics, pb.graphics, rb.graphics_meta, pb.graphics_meta)

    def test_every_r_page_is_recorded_and_right_plot_beats_wrong_plot(self):
        rb, pb, ok = self._run("plot(1:3);plot(3:1)",
                               "plt.figure();plt.plot([1,2,3]);plt.figure();plt.plot([3,2,1])")
        self.assertEqual((len(rb.graphics), len(rb.graphics_meta)), (2, 2))
        self.assertEqual(ok.score, 1.0)
        _, _, bad = self._run("barplot(c(3,7,2,9,4))", "plt.bar(range(5),[9,4,2,1,1])")
        _, _, empty = self._run("barplot(c(3,7,2,9,4))", "plt.plot([])")
        self.assertLess(bad.score, 0.5)
        self.assertEqual(empty.score, 0.0)


if __name__ == "__main__":
    unittest.main()
