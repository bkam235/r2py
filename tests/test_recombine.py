"""Seed recombination: donor entities spliced into the best seed, kept only if the objective improves."""
import unittest
from types import SimpleNamespace

from r2py.harness import recombine as R


def _es(score, ok=True):
    return SimpleNamespace(executed_ok=ok, active_dims=("d",), d=score)


def _rep(entities: dict, exit_code=0, aggregate=None):
    by = {k: _es(*v) if isinstance(v, tuple) else _es(v) for k, v in entities.items()}
    agg = aggregate if aggregate is not None else (sum(R._obj.entity_score(e) for e in by.values()) / len(by))
    return SimpleNamespace(aggregate=agg, py_exit_code=exit_code, by_entity=by, crash_entities=[])


A = "import os\n# r2py:entity:a\nx = 1\n# r2py:entity:b\ny = bad(x)\n"
B = "import os\nimport json\n# r2py:entity:a\nx = bad2()\n# r2py:entity:b\ny = json.dumps(x)\n"


class FakeHarness:
    def __init__(self, scorer):
        self.scorer, self.verified, self.last_annotated_source = scorer, [], None

    def verify(self, source):
        self.verified.append(source)
        return self.scorer(source)


class TestRecombine(unittest.TestCase):
    def test_better_entity_is_spliced_in_with_its_imports(self):
        seen = {}

        def scorer(src):
            seen["src"] = src
            return _rep({"a": 0.9, "b": 0.9})

        pool = [(A, _rep({"a": 0.9, "b": 0.1})), (B, _rep({"a": 0.2, "b": 0.8}))]
        out = R.recombine(pool, FakeHarness(scorer))
        self.assertIsNotNone(out)
        src, rep = out
        self.assertIn("x = 1", src)                     # a kept from the base
        self.assertIn("y = json.dumps(x)", src)         # b taken from the donor
        self.assertIn("import json", src)              # and the import it needs
        self.assertGreater(rep.aggregate, 0.5)

    def test_not_kept_when_the_objective_does_not_improve(self):
        pool = [(A, _rep({"a": 0.9, "b": 0.1})), (B, _rep({"a": 0.2, "b": 0.8}))]
        self.assertIsNone(R.recombine(pool, FakeHarness(lambda s: _rep({"a": 0.9, "b": 0.05}))))

    def test_small_advantage_is_not_worth_a_verification(self):
        h = FakeHarness(lambda s: _rep({"a": 0.9, "b": 0.9}))
        pool = [(A, _rep({"a": 0.9, "b": 0.5})), (B, _rep({"a": 0.2, "b": 0.52}))]
        self.assertIsNone(R.recombine(pool, h))
        self.assertEqual(h.verified, [])

    def test_donor_that_did_not_run_the_entity_is_ignored(self):
        h = FakeHarness(lambda s: _rep({"a": 0.9, "b": 0.9}))
        pool = [(A, _rep({"a": 0.9, "b": 0.1})), (B, _rep({"a": 0.2, "b": (0.9, False)}))]
        self.assertIsNone(R.recombine(pool, h))

    def test_a_crashing_base_improves_through_a_donor(self):
        crashed = _rep({"a": 0.9, "b": (0.0, False)}, exit_code=1, aggregate=0.0)
        out = R.recombine([(A, crashed), (B, _rep({"a": 0.2, "b": 0.8}))],
                          FakeHarness(lambda s: _rep({"a": 0.9, "b": 0.8})))
        self.assertIsNotNone(out)
        self.assertEqual(out[1].py_exit_code, 0)

    def test_single_seed_pool_has_nothing_to_do(self):
        self.assertIsNone(R.recombine([(A, _rep({"a": 0.5, "b": 0.5}))], FakeHarness(lambda s: None)))

    def test_import_union_places_missing_imports_after_existing_ones(self):
        out = R._with_donor_imports(A, B)
        self.assertEqual(out.splitlines()[:2], ["import os", "import json"])
        self.assertEqual(R._with_donor_imports(A, A), A)


if __name__ == "__main__":
    unittest.main()
