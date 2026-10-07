"""Imported names that do not exist in their (installed) modules are found before the script runs."""
import unittest

from r2py.stage0.env.module_check import imported_names, missing_import_names


class TestImportedNames(unittest.TestCase):
    def test_names_are_read_from_absolute_from_imports_only(self):
        src = "import os\nfrom os import path, sep\nfrom . import local\nfrom json import *\nfrom __future__ import annotations\n"
        self.assertEqual(imported_names(src), [("os", "path"), ("os", "sep")])
        self.assertEqual(imported_names("def (:\n"), [])

    def test_missing_names_are_found_with_near_spellings(self):
        bad = missing_import_names("from os import path, nonexistent_name\nfrom pandas import DataFrame, dataframe\n")
        self.assertEqual({(m, n) for m, n, _ in bad}, {("os", "nonexistent_name"), ("pandas", "dataframe")})
        near = {n: near for _m, n, near in bad}
        self.assertEqual(near["dataframe"][0], "DataFrame")

    def test_existing_names_and_submodules_pass(self):
        self.assertEqual(missing_import_names("from os import path\nfrom json import decoder, loads\nfrom numpy.random import default_rng\n"), [])

    def test_modules_that_cannot_be_imported_are_the_other_checks_business(self):
        self.assertEqual(missing_import_names("from definitely_not_a_module_xyz import thing\n"), [])


if __name__ == "__main__":
    unittest.main()
