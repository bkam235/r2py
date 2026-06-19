"""Tests for Stage 3 — edit_types (apply_edit, serialization).

Tests for deleted Stage 3 modules (editor, policy, history, prompt,
attributor) were removed alongside the modules they tested.
"""
from __future__ import annotations

import unittest

from r2py.types import (
    Edit,
    EditKind,
)


# ---------------------------------------------------------------------------
# T1 — TestApplyEdit
# ---------------------------------------------------------------------------

class TestApplyEdit(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.edit_types import apply_edit
        self.apply = apply_edit

    def test_insert_preamble_before_first_code_line(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "import numpy as np"})
        result = self.apply(source, e)
        self.assertIn("import numpy as np\n", result)
        self.assertTrue(result.index("import numpy") < result.index("x = 1"))

    def test_insert_preamble_skips_comments(self):
        source = "# header\nx = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "import os"})
        result = self.apply(source, e)
        self.assertIn("import os", result)

    def test_insert_preamble_empty_code_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={"code": "   "})
        self.assertEqual(self.apply(source, e), source)

    def test_rename_variable(self):
        source = "foo = 1\nbar = foo + 2\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "foo", "new": "baz"})
        result = self.apply(source, e)
        self.assertNotIn("foo", result)
        self.assertIn("baz", result)

    def test_rename_variable_whole_word_only(self):
        source = "foobar = 1\nfoo = 2\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "foo", "new": "x"})
        result = self.apply(source, e)
        self.assertIn("foobar", result)  # not renamed
        self.assertIn("x = 2", result)

    def test_rename_variable_empty_params_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.RENAME_VARIABLE, params={"old": "", "new": "y"})
        self.assertEqual(self.apply(source, e), source)

    def test_change_import(self):
        source = "import pandas\nx = 1\n"
        e = Edit(kind=EditKind.CHANGE_IMPORT,
                 params={"old_import": "import pandas", "new_import": "import pandas as pd"})
        result = self.apply(source, e)
        self.assertIn("import pandas as pd", result)
        self.assertNotIn("import pandas\n", result)

    def test_change_import_no_match_noop(self):
        source = "import numpy\n"
        e = Edit(kind=EditKind.CHANGE_IMPORT,
                 params={"old_import": "import pandas", "new_import": "import polars"})
        self.assertEqual(self.apply(source, e), source)

    def test_wrap_value(self):
        source = "result = compute(x)\nprint(result)\n"
        e = Edit(kind=EditKind.WRAP_VALUE, params={"name": "result", "wrapper": "str"})
        result = self.apply(source, e)
        self.assertIn("str(result)", result)

    def test_wrap_value_empty_name_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.WRAP_VALUE, params={"name": "", "wrapper": "str"})
        self.assertEqual(self.apply(source, e), source)

    def test_replace_call(self):
        source = "y = old_fn(x)\n"
        e = Edit(kind=EditKind.REPLACE_CALL,
                 params={"old_call": "old_fn(x)", "new_call": "new_fn(x)"})
        result = self.apply(source, e)
        self.assertIn("new_fn(x)", result)
        self.assertNotIn("old_fn(x)", result)

    def test_replace_call_empty_old_noop(self):
        source = "y = old_fn(x)\n"
        e = Edit(kind=EditKind.REPLACE_CALL, params={"old_call": "", "new_call": "new_fn(x)"})
        self.assertEqual(self.apply(source, e), source)

    def test_restructure_control_flow(self):
        old = "if x > 0:\n    y = 1\nelse:\n    y = 0\n"
        new = "y = 1 if x > 0 else 0\n"
        source = old + "z = y\n"
        e = Edit(kind=EditKind.RESTRUCTURE_CONTROL_FLOW,
                 params={"old_code": old, "new_code": new})
        result = self.apply(source, e)
        self.assertIn("y = 1 if x > 0 else 0", result)

    def test_restructure_control_flow_empty_old_noop(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.RESTRUCTURE_CONTROL_FLOW,
                 params={"old_code": "", "new_code": "y = 2\n"})
        self.assertEqual(self.apply(source, e), source)

    def test_replace_library_name_and_import(self):
        source = "import pandas as pd\ndf = pd.DataFrame({'a': [1]})\n"
        e = Edit(kind=EditKind.REPLACE_LIBRARY,
                 params={
                     "old_name": "pd",
                     "new_name": "pl",
                     "old_import": "import pandas as pd",
                     "new_import": "import polars as pl",
                 })
        result = self.apply(source, e)
        self.assertIn("import polars as pl", result)
        self.assertIn("pl.DataFrame", result)
        self.assertNotIn("pd.DataFrame", result)

    def test_replace_library_empty_names_noop(self):
        source = "import pandas as pd\n"
        e = Edit(kind=EditKind.REPLACE_LIBRARY, params={"old_name": "", "new_name": "pl"})
        self.assertEqual(self.apply(source, e), source)

    def test_bad_params_returns_source_unchanged(self):
        source = "x = 1\n"
        e = Edit(kind=EditKind.INSERT_PREAMBLE, params={})  # no "code" key
        # Returns source unchanged (empty code -> noop)
        self.assertEqual(self.apply(source, e), source)


# ---------------------------------------------------------------------------
# T2 — TestEditTypesHelpers
# ---------------------------------------------------------------------------

class TestEditTypesHelpers(unittest.TestCase):

    def setUp(self):
        from r2py.stage3.edit_types import edit_to_dict, dict_to_edit
        self.to_dict = edit_to_dict
        self.from_dict = dict_to_edit

    def test_round_trip(self):
        e = Edit(kind=EditKind.REPLACE_CALL, entity_ids=["e1"],
                 params={"old_call": "foo()", "new_call": "bar()"},
                 pattern_id="my.pat")
        d = self.to_dict(e)
        e2 = self.from_dict(d)
        self.assertEqual(e.kind, e2.kind)
        self.assertEqual(e.entity_ids, e2.entity_ids)
        self.assertEqual(e.params, e2.params)
        self.assertEqual(e.pattern_id, e2.pattern_id)

    def test_invalid_kind_raises(self):
        with self.assertRaises(ValueError):
            self.from_dict({"kind": "NotAKind", "entity_ids": [], "params": {}})

    def test_missing_kind_raises(self):
        with self.assertRaises(KeyError):
            self.from_dict({"entity_ids": [], "params": {}})


if __name__ == "__main__":
    unittest.main()
