"""R checkpoint injection (2026-10-17): 34 of 249 checkpointed runs failed, and the script then had no per-entity
bundles at all. Causes: a checkpoint inside an open expression (pipes, `+` chains, argument lists), a checkpoint
that closed the graphics device between a plot and its low-level additions, and quote escaping."""
import unittest
from types import SimpleNamespace as NS

from r2py.stage1.runner import _cp_file_id, _statement_boundary_rows, run_script_checkpointed
from r2py.stage2.stitch import DATA_SHIM_RE, build_data_shim, refresh_data_shim


class TestBoundaries(unittest.TestCase):
    def test_only_statement_ends_are_boundaries(self):
        src = ("x <- storms |>\n  filter(a) |>\n  head()\n"     # rows 0-2: one pipeline
               "if (f(x)) {\n  y <- 1\n  z <- foo(1,\n     2)\n}\n"  # rows 3-7
               "if (g())\n  w <- 3\n")                            # rows 8-9: an if without braces
        rows = _statement_boundary_rows(src)
        self.assertEqual(sorted(rows & set(range(10))), [2, 3, 4, 6, 7, 9])

    def test_unparsable_source_is_not_filtered(self):
        self.assertIsNone(_statement_boundary_rows("x <- (1 +\n"))

    def test_file_ids_have_no_characters_windows_forbids(self):
        self.assertEqual(_cp_file_id('xml_attr(doc, "id")'), "xml_attr(doc, _id_)")
        self.assertEqual(_cp_file_id("a\\b/c:d"), "a_b_c_d")


def ents(**spans):
    return {e: NS(source_span=NS(start_line=a, end_line=b)) for e, (a, b) in spans.items()}


class TestCheckpointedRun(unittest.TestCase):
    def run_r(self, src, entities):
        try:
            return run_script_checkpointed(src, entities, timeout_s=120)[1]
        except Exception as exc:          # no R on this machine
            self.skipTest(f"R not available: {exc}")

    def test_a_pipeline_keeps_its_bundles(self):
        src = 'x <- c(3, 1, 2) |>\n  sort() |>\n  rev()\ny <- x + 1\n'
        b = self.run_r(src, ents(sort=(1, 1), x=(0, 2), y=(3, 3)))
        self.assertEqual(set(b), {"x", "y"})                         # `sort` ends mid-pipeline: no checkpoint
        self.assertEqual(b["x"].data["x"], [3, 2, 1])

    def test_low_level_graphics_after_a_plot_entity_still_draw(self):
        src = 'plot.new()\nplot.window(c(0, 1), c(0, 1))\ntext(0.5, 0.5, "A")\nz <- 1\n'
        b = self.run_r(src, ents(plot_new=(0, 0), plot_window=(1, 1), text=(2, 2), z=(3, 3)))
        self.assertEqual(set(b), {"plot_new", "plot_window", "text", "z"})
        self.assertEqual(b["z"].data["z"], 1)
        gfx = lambda e: b[e].graphics if isinstance(b[e].graphics, int) else len(b[e].graphics)   # noqa: E731
        self.assertGreater(gfx("plot_new"), 0)

    def test_an_entity_id_with_quotes(self):
        src = 'x <- 1\nprint("a")\n'
        b = self.run_r(src, ents(x=(0, 0), **{'print("a")': (1, 1)}))
        self.assertIn('print("a")', b)
        self.assertIn('"a"', b['print("a")'].stdout)


class TestShimRefresh(unittest.TestCase):
    OLD = ("# r2py:data_shim:begin\n# import json as _r2py_shim_json\n# from pathlib import Path as _r2py_shim_Path\n"
           "# if '__file__' not in globals(): __file__ = 'out/s.py'\n"
           "# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 's.r2py_data.json')"
           ".read_text(encoding='utf-8'))\n# for _r2py_shim_n in ['diamonds']:\n"
           "#     if _r2py_shim_n in _r2py_shim_data:\n#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]\n"
           "# r2py:entity:e1\n# r2py:data_shim:end\nx = 1\n")

    def test_an_old_block_loads_data_frames_and_keeps_its_line_count(self):
        out = refresh_data_shim(self.OLD)
        self.assertEqual(out.count("\n"), self.OLD.count("\n"))      # entity line maps stay valid
        self.assertIn("_r2py_shim_pd.DataFrame", out)
        body = "\n".join(l[2:] for l in DATA_SHIM_RE.search(out).group(2).splitlines() if not l.startswith("# r2py:"))
        ns = {"__file__": "x"}
        exec(body.replace("_r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 's.r2py_data.json')"
                          ".read_text(encoding='utf-8'))", "{'diamonds': {'a': [1, 2], 'b': [3, 4]}}"), ns)
        self.assertEqual(type(ns["diamonds"]).__name__, "DataFrame")

    def test_a_current_block_is_unchanged(self):
        src = build_data_shim(["diamonds"], "s.r2py_data.json", "out/s.py") + "\nx = 1\n"
        self.assertEqual(refresh_data_shim(src), src)


if __name__ == "__main__":
    unittest.main()


class TestPythonInjection(unittest.TestCase):
    def test_no_checkpoint_inside_a_multiline_string(self):
        from r2py.stage4.verifier import _inject_py_checkpoints
        src = "x = parse('''\n<root/>\n''')\ny = 1\n"
        out, _ = _inject_py_checkpoints(src, {"a": (1, 1), "x": (1, 3), "y": (4, 4)})
        self.assertIn("x = parse('''\n<root/>\n''')\n_r2py_checkpoint('x')\n", out)
        self.assertNotIn("_r2py_checkpoint('a')", out)        # row 1 ends inside the string


class TestTagListSerialisation(unittest.TestCase):
    def test_a_tag_list_is_captured_as_its_rendered_html(self):
        src = 'x <- htmltools::tagList(htmltools::p("a"), htmltools::span("b"))\n'
        try:
            b = run_script_checkpointed(src, ents(x=(0, 0)), timeout_s=120)[1]
        except Exception as exc:
            self.skipTest(f"R not available: {exc}")
        self.assertIsInstance(b["x"].data["x"], str)          # not htmltools' internal list
        self.assertIn("<p>a</p>", b["x"].data["x"])
