"""Harness-located errors: probes on both sides, value-aligned, first divergence reported."""
import ast
import tempfile
import unittest
from pathlib import Path

import pytest

from r2py.harness import locate as L


def _p(i, expr, value):
    return {"id": i, "expr": expr, "value": value}


class TestPythonInstrumentation(unittest.TestCase):
    SRC = "import numpy as np\nx = [1.0, 2.0]\nq = np.percentile(x, 90)\nm = np.mean(x) + q\nprint(m)\n"

    def test_only_calls_and_operators_in_the_range_are_wrapped_inner_first(self):
        out = L.instrument_python(self.SRC, (4, 4))
        self.assertIn("_r2py_probe(", out)
        body = out.splitlines()
        self.assertNotIn("_r2py_probe", body[2])                 # line 3 is outside the range
        self.assertNotIn("_r2py_probe", body[4])                 # so is the print
        line = [b for b in body if b.startswith("m =")][0]
        self.assertLess(line.index("np.mean"), line.index("+ q"))
        self.assertEqual(out.count("_r2py_probe(1,"), 1)         # np.mean(x) is probe 1, the sum probe 2
        self.assertIn("_r2py_probe(2, 'np.mean(x) + q'", out)    # labels are the original code, not the rewritten

    def test_instrumented_source_still_computes_the_same_values(self):
        out = L.instrument_python(self.SRC.replace("print(m)\n", ""), (1, 4))
        ns = {"__name__": "__main__", "_r2py_probe": lambda i, label, v: v}
        exec(out, ns)
        self.assertAlmostEqual(ns["m"], 1.5 + 1.9)

    def test_store_targets_and_unparseable_source(self):
        out = L.instrument_python("x = [0, 0]\nx[1] = 5\n", (1, 2))
        ast.parse(out)
        self.assertIn("x[1] = 5", out)                           # a subscript on the left is not an expression to probe
        self.assertIsNone(L.instrument_python("def (:\n", (1, 1)))


class TestRProgram(unittest.TestCase):
    def test_program_runs_the_script_up_to_the_entity_and_drops_the_rest(self):
        src = "a <- 1\nb <- sd(a)\nc <- 3\n"
        prog = L.r_locate_program(src, (1, 1))
        self.assertTrue(prog.startswith("a <- 1\n"))
        self.assertIn("b <- sd(a)", prog)
        self.assertNotIn("c <- 3", prog)
        self.assertIn("_r2py_probes.json", prog)

    def test_a_delimiter_collision_in_the_entity_text_is_avoided(self):
        entity = 'x <- ")------"\n'                     # contains the closing sequence of a six-dash raw string
        prog = L.r_locate_program(entity, (0, 0))
        self.assertIn('r"-------(x <- ")------"', prog)   # so the delimiter is longer than anything the text holds


class TestDivergence(unittest.TestCase):
    def test_first_unreproduced_r_call_is_reported_with_the_nearest_python_value(self):
        r = [_p(1, "mean(x)", 6.25), _p(2, "sd(x)", 2.89923), _p(3, "round(sd(x) * 2, 3)", 5.798)]
        py = [_p(1, "np.mean(x)", 6.25), _p(2, "np.std(x)", 2.71198), _p(3, "round(...)", 5.424)]
        d = L.find_divergence(r, py)
        self.assertEqual(d["expr"], "sd(x)")
        self.assertEqual(d["closest"]["expr"], "np.std(x)")
        self.assertAlmostEqual(d["closest"]["error"], 0.0646, places=3)
        self.assertIn("`sd(x)`", L.format_divergence("r", d, 3, 3))

    def test_alignment_is_by_value_not_by_name_or_order(self):
        r = [_p(1, "quantile(x, 0.9)", 9.73), _p(2, "mean(x)", 6.4375)]
        py = [_p(5, "np.mean(x)", 6.4375), _p(9, "np.percentile(x, 90)", 9.73)]
        self.assertIsNone(L.find_divergence(r, py))
        self.assertIn("also appears", L.format_divergence("m", None, 2, 2))

    def test_trivial_constants_are_not_divergences(self):
        self.assertIsNone(L.find_divergence([_p(1, "length(x)", 3)], [_p(1, "len(x)", 4.0)]))

    def test_vectors_match_as_a_whole_and_text_values_compare_canonically(self):
        r = [_p(1, "f(x)", [1.234567, 2.345678, 3.456789]), _p(2, "g(y)", "<a> <b/> </a>")]
        self.assertIsNone(L.find_divergence(r, [_p(1, "h", [3.456789, 1.234567, 2.345678]), _p(2, "t", "<a><b/></a>")]))
        self.assertEqual(L.find_divergence(r[:1], [_p(1, "h", [1.234567, 2.345678, 9.9])])["expr"], "f(x)")

    def test_load_probes_tolerates_garbage(self):
        self.assertEqual(L.load_probes(None), [])
        self.assertEqual(L.load_probes("not json"), [])
        self.assertEqual(len(L.load_probes('[{"id": 1, "expr": "f()", "value": 2}, {"x": 1}]')), 1)


def _has_r() -> bool:
    try:
        from r2py.stage0.env.r_runtime import find_rscript
        return find_rscript() is not None
    except Exception:
        return False


@pytest.mark.skipif(not _has_r(), reason="R not available")
def test_end_to_end_locates_the_population_standard_deviation_bug():
    from r2py.harness.tools import HarnessTools
    from r2py.library import PatternLibrary
    from r2py.stage1 import analyze

    with tempfile.TemporaryDirectory() as d:
        r = Path(d) / "loc.R"
        r.write_text("x <- c(2.5, 3.1, 4.7, 5.2, 6.8, 7.4, 9.9, 10.3)\nr <- round(sd(x) * 2, 3)\n", encoding="utf-8")
        sm = analyze(r)
        eids = {e.name: k for k, e in sm.entities.items()}
        src = ("# r2py:entity:%s\nx = [2.5, 3.1, 4.7, 5.2, 6.8, 7.4, 9.9, 10.3]\n# r2py:entity:%s\n"
               "import numpy as np\nr = round(float(np.std(x)) * 2, 3)\n") % (eids["x"], eids["r"])
        (Path(d) / "lib").mkdir()
        h = HarnessTools(sm, PatternLibrary(Path(d) / "lib"), model="m", data_compare="exact", timeout_s=60,
                         sidecar_filename="x.r2py_data.json")
        h.note_reference(src)
        h.verify(src)
        text = h.locate(h.last_annotated_source, eids["r"])
        assert "`sd(x)`" in text and "np.std(x)" in text
        assert h.locate(h.last_annotated_source, eids["r"]) == text        # cached


if __name__ == "__main__":
    unittest.main()
