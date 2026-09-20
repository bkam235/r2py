"""Tests for seed_from_translation: one pattern per (package, function)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import r2py
from r2py.library import get_library
from r2py.types import EntityKind

R_SOURCE = "\n".join([
    "x <- paste('a', 'b')",       # 0  base::paste
    "y <- lapply(1:3, sqrt)",     # 1  base::lapply
    "z <- mutate(df, a = 1)",     # 2  dplyr::mutate
    "w <- filter(df, a > 1)",     # 3  dplyr::filter
    "v <- filter(ts, 1)",         # 4  stats::filter (same name, other package)
    "u <- 1",                     # 5  package-less variable
    "library(dplyr)",             # 6  library import
])

PY_SOURCE = "\n".join([
    "# r2py:entity:e_paste", "x = ' '.join(['a', 'b'])",
    "# r2py:entity:e_lapply", "y = [sqrt(i) for i in range(1, 4)]",
    "# r2py:entity:e_mutate", "z = df.assign(a=1)",
    "# r2py:entity:e_dfilter", "w = df[df.a > 1]",
    "# r2py:entity:e_sfilter", "v = scipy_filter(ts, 1)",
    "# r2py:entity:e_var", "u = 1",
    "# r2py:entity:e_lib", "import pandas as pd",
]) + "\n"


def _entity(name, package, line, kind=EntityKind.FUNCTION_CALL):
    return SimpleNamespace(name=name, package=package, kind=kind,
                           source_span=SimpleNamespace(start_line=line, end_line=line))


ENTITIES = {
    "e_paste": _entity("paste", "base", 0),
    "e_lapply": _entity("lapply", "base", 1),
    "e_mutate": _entity("mutate", "dplyr", 2),
    "e_dfilter": _entity("filter", "dplyr", 3),
    "e_sfilter": _entity("filter", "stats", 4),
    "e_var": _entity("u", "", 5, EntityKind.VARIABLE),
    "e_lib": _entity("dplyr", "dplyr", 6, EntityKind.LIBRARY_IMPORT),
}


class TestSeedFromTranslation(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.lib = get_library(root / "lib")
        self.r_path, self.py_path = root / "s.R", root / "s.py"
        self.r_path.write_text(R_SOURCE, encoding="utf-8")
        self.py_path.write_text(PY_SOURCE, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _seed(self, entities=ENTITIES, script_id="s1"):
        script_map = SimpleNamespace(entities=entities, source=R_SOURCE)
        with patch("r2py.stage1.analyze", return_value=script_map):
            return r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib,
                                              script_id=script_id)

    def test_creates_one_pattern_per_package_and_function(self):
        touched = self._seed()
        self.assertEqual(sorted(touched),
                         ["base.lapply", "base.paste", "dplyr.filter", "dplyr.mutate", "stats.filter"])

    def test_same_name_in_two_packages_are_separate_patterns(self):
        self._seed()
        self.assertIn("filter", self.lib.store.get("dplyr.filter").translation_examples[0].r_snippet)
        self.assertIn("ts", self.lib.store.get("stats.filter").translation_examples[0].r_snippet)

    def test_skips_packageless_entities_and_library_imports(self):
        touched = self._seed()
        self.assertFalse([t for t in touched if t.endswith(".u") or t == "dplyr.dplyr"])

    def test_new_function_in_a_seen_package_gets_its_own_pattern(self):
        """The bug being fixed: it used to be attached to the package's first pattern."""
        self._seed({k: v for k, v in ENTITIES.items() if k == "e_paste"})
        self.assertEqual(self.lib.store.list_ids(), ["base.paste"])
        self._seed({k: v for k, v in ENTITIES.items() if k == "e_lapply"})
        self.assertEqual(sorted(self.lib.store.list_ids()), ["base.lapply", "base.paste"])
        # each holds only its own example
        self.assertEqual(len(self.lib.store.get("base.paste").translation_examples), 1)
        self.assertIn("lapply", self.lib.store.get("base.lapply").translation_examples[0].r_snippet)

    def test_same_function_again_adds_an_example_to_the_same_pattern(self):
        self._seed(script_id="s1")
        self.r_path.write_text(R_SOURCE.replace("'a', 'b'", "'c', 'd'"), encoding="utf-8")
        script_map = SimpleNamespace(entities=ENTITIES, source=R_SOURCE.replace("'a', 'b'", "'c', 'd'"))
        with patch("r2py.stage1.analyze", return_value=script_map):
            r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib, script_id="s2")
        ex = self.lib.store.get("base.paste").translation_examples
        self.assertEqual(sorted(e.script_id for e in ex), ["s1", "s2"])
        self.assertEqual(len(self.lib.store.list_ids()), 5)  # no duplicates created

    def test_seeded_patterns_are_retrievable_by_the_same_entity(self):
        self._seed()
        for eid in ("e_paste", "e_lapply", "e_mutate", "e_dfilter", "e_sfilter"):
            got = self.lib.retrieve(ENTITIES[eid], k=3)
            self.assertEqual(len(got), 1, eid)
            self.assertEqual(got[0].package, ENTITIES[eid].package)
        self.assertEqual(self.lib.retrieve(ENTITIES["e_var"], k=3), [])
        # an unseen function in a seen package gets nothing, not a neighbour
        self.assertEqual(self.lib.retrieve(_entity("paste0", "base", 0), k=3), [])

    def test_index_is_rebuilt_so_new_patterns_are_listed(self):
        self._seed()
        self.assertEqual(sorted(self.lib.index.all_ids()), sorted(self.lib.store.list_ids()))


class TestSnippetLimits(unittest.TestCase):
    """Examples are stored and shown whole up to MAX_*_SNIPPET, clipped at a line boundary."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        root = Path(self._tmp.name)
        self.lib = get_library(root / "lib")
        self.r_path, self.py_path = root / "s.R", root / "s.py"
        self.r_path.write_text("z <- mutate(df, a = 1)\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _seed_with_python(self, body: str) -> "Pattern":
        self.py_path.write_text("# r2py:entity:e1\n" + body + "\n", encoding="utf-8")
        entities = {"e1": _entity("mutate", "dplyr", 0)}
        script_map = SimpleNamespace(entities=entities, source="z <- mutate(df, a = 1)\n")
        with patch("r2py.stage1.analyze", return_value=script_map):
            r2py.seed_from_translation(self.r_path, self.py_path, library=self.lib)
        return self.lib.store.get("dplyr.mutate").translation_examples[0]

    def test_clip_snippet(self):
        from r2py.library.pattern import clip_snippet
        self.assertEqual(clip_snippet("abc", 10), "abc")
        self.assertEqual(clip_snippet("a" * 10, 10), "a" * 10)
        clipped = clip_snippet("line1\nline2\nline3\nline4", 13)  # room for 2 full lines + part of 3
        self.assertEqual(clipped, "line1\nline2\n# ...")
        self.assertEqual(clip_snippet("x" * 50, 10), "x" * 10 + "\n# ...")  # no newline to cut at

    def test_a_1500_char_translation_is_stored_whole(self):
        """Used to be cut at 600 characters, often mid-statement."""
        body = "\n".join(f"df['c{i}'] = df['a'] + {i}" for i in range(50))
        self.assertGreater(len(body), 1000)
        ex = self._seed_with_python(body)
        self.assertIn(body, ex.py_snippet)
        self.assertNotIn("# ...", ex.py_snippet)

    def test_oversized_translation_is_clipped_at_a_line_boundary(self):
        from r2py.library.pattern import MAX_PY_SNIPPET
        body = "\n".join(f"df['col_{i:04d}'] = df['a'] + {i}" for i in range(200))
        self.assertGreater(len(body), MAX_PY_SNIPPET)
        ex = self._seed_with_python(body)
        self.assertLessEqual(len(ex.py_snippet), MAX_PY_SNIPPET + len("\n# ..."))
        self.assertTrue(ex.py_snippet.endswith("\n# ..."))
        last_line = ex.py_snippet.splitlines()[-2]
        self.assertIn(last_line, body.splitlines())  # a whole source line, not a fragment

    def test_prompt_shows_the_whole_stored_example(self):
        """The seed prompt used to show only the first 300 characters of the Python."""
        from r2py.seed import _build_prompt
        body = "\n".join(f"df['c{i}'] = df['a'] + {i}" for i in range(40))
        self.assertGreater(len(body), 600)
        self._seed_with_python(body)
        script_map = SimpleNamespace(source="z <- mutate(df, a = 1)\n", entity_bundles={},
                                     entities={"e1": _entity("mutate", "dplyr", 0)})
        prompt = "\n".join(_build_prompt(script_map, self.lib))
        self.assertIn(body, prompt)


if __name__ == "__main__":
    unittest.main()
