"""The intra-script runtime step: which functions a failing script needs, and what gets admitted."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from r2py.runtime import ondemand
from r2py.runtime.store import RuntimeStore
from r2py.types import EntityKind


def entity(name, package="pkg", rhs=None, rhs_pkg=None, kind=EntityKind.FUNCTION_CALL, line=0):
    return SimpleNamespace(name=name, package=package, rhs_call_name=rhs, rhs_call_package=rhs_pkg, kind=kind,
                           source_span=SimpleNamespace(start_line=line, end_line=line))


def score(value, ran=True):
    return SimpleNamespace(executed_ok=ran, active_dims=["data_output"], data_output=value)


class TestWhichFunctionsAScriptNeeds(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = RuntimeStore(self._tmp.name)
        self.sm = SimpleNamespace(source="", entities={
            "a": entity("a", rhs="time_add", rhs_pkg="timechange", line=1),
            "b": entity("b", rhs="time_add", rhs_pkg="timechange", line=2),
            "c": entity("plot", package="graphics", line=3),
            "ok": entity("median", package="stats", line=4),
            "boiler": entity("suppressPackageStartupMessages", package="base", line=5),
            "lib": entity("timechange", kind=EntityKind.LIBRARY_IMPORT, line=0),
        })
        self.report = SimpleNamespace(by_entity={
            "a": score(0.0), "b": score(0.5), "c": score(0.2), "ok": score(1.0), "boiler": score(0.0),
            "lib": score(0.0)})

    def tearDown(self):
        self._tmp.cleanup()

    def test_failing_entities_are_grouped_by_the_function_behind_them_biggest_loss_first(self):
        needs = ondemand.failing_functions(self.sm, self.report, self.store)
        self.assertEqual([(n.function, n.package) for n in needs], [("time_add", "timechange"), ("plot", "graphics")])
        self.assertAlmostEqual(needs[0].loss, 1.5)
        self.assertEqual(needs[0].spans, [(1, 1), (2, 2)])

    def test_a_function_the_store_already_has_is_not_needed(self):
        self.store.add({"function": "time_add", "package": "timechange", "status": "passed"},
                       "def r_time_add(x):\n    return x\n")
        needs = ondemand.failing_functions(self.sm, self.report, self.store)
        self.assertEqual([n.function for n in needs], ["plot"])


class TestVerifyNeeded(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.store = RuntimeStore(self._tmp.name)
        self.sm = SimpleNamespace(source="", entities={
            "a": entity("a", rhs="good", rhs_pkg="pkg", line=1),
            "b": entity("b", rhs="nearly", rhs_pkg="pkg", line=2),
            "c": entity("plot", package="graphics", line=3)})
        self.report = SimpleNamespace(by_entity={"a": score(0.0), "b": score(0.1), "c": score(0.2)})

    def tearDown(self):
        self._tmp.cleanup()

    def run_step(self, attempt, assess=None, **kw):
        probe = lambda specs: {s: {"found": True, "kind": "closure", "impure": []} for s in specs}  # noqa: E731
        cases = [{"call": f"f({i})", "args": [[None, i]], "expected": i} for i in range(5)]
        with patch("r2py.runtime.purity.probe", probe), \
                patch.object(ondemand, "cases_for", lambda need, src: (cases, "")), \
                patch("r2py.runtime.propose.attempt", attempt), \
                patch("r2py.runtime.admit.assess", assess or (lambda rec, cs: {"verdict": "not admissible"})):
            return ondemand.verify_needed(self.sm, self.report, self.store, model="m", log=lambda *_: None, **kw)

    def test_a_passing_function_is_added_and_a_graphics_function_never_attempted(self):
        def attempt(fname, package, model, **kw):
            return {"function": fname, "package": package, "status": "passed",
                    "code": f"def r_{fname}(x):\n    return x\n"}
        recs = self.run_step(attempt, max_functions=5)
        self.assertEqual(sorted(r["function"] for r in recs), ["good", "nearly"])
        self.assertEqual(sorted(self.store.entries), ["r_good", "r_nearly"])

    def test_a_near_miss_enters_restricted_and_a_plain_failure_not_at_all(self):
        def attempt(fname, package, model, **kw):
            return {"function": fname, "package": package, "status": "failed", "code": f"def r_{fname}(x): ..."}

        def assess(rec, cases):
            if rec["function"] == "nearly":
                return {"verdict": "admitted, restricted", "fenced": {"roll": ["wrap"]},
                        "code": "def r_nearly(x):\n    return x\n"}
            return {"verdict": "not admissible: a bug, not a regime"}
        recs = {r["function"]: r for r in self.run_step(attempt, assess, max_functions=5)}
        self.assertEqual(recs["nearly"]["admitted"], "restricted")
        self.assertNotIn("admitted", recs["good"])
        self.assertEqual(list(self.store.entries), ["r_nearly"])
        self.assertEqual(self.store.entries["r_nearly"].unverified, {"roll": ["wrap"]})

    def test_the_cap_on_functions_per_script_holds(self):
        calls = []

        def attempt(fname, package, model, **kw):
            calls.append(fname)
            return {"function": fname, "package": package, "status": "failed"}
        self.run_step(attempt, max_functions=1)
        self.assertEqual(calls, ["good"])                     # the bigger loss first

    def test_it_never_raises(self):
        def attempt(*a, **k):
            raise RuntimeError("provider down")
        recs = self.run_step(attempt)
        self.assertTrue(recs and recs[-1]["status"].startswith("error"))


class TestStoreAdd(unittest.TestCase):
    def test_add_writes_code_and_record_and_reloads(self):
        with tempfile.TemporaryDirectory() as d:
            store = RuntimeStore(d)
            e = store.add({"function": "f", "package": None, "status": "passed"}, "def r_f(x):\n    return x\n")
            self.assertEqual(e.py, "r_f")
            self.assertTrue((Path(d) / "base__f.py").exists())
            self.assertEqual(sorted(p.name for p in Path(d).iterdir()), ["base__f.json", "base__f.py"])
            self.assertIn("r_f", RuntimeStore(d).entries)          # another reader sees it too

    def test_add_refuses_a_failed_record(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(RuntimeStore(d).add({"function": "f", "status": "failed"}, "x = 1"))


if __name__ == "__main__":
    unittest.main()
