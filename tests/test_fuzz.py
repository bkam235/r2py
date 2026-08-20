"""Tests for Stage 4 generators and fuzz harness (§7.8)."""
from __future__ import annotations

import random

import pytest

from r2py.stage4.generators import (
    ScalarGenerator,
    VectorGenerator,
    DataFrameGenerator,
    generator_from_observed,
    boundary_cases,
)
from r2py.stage4.fuzz import FuzzConfig, run_fuzz, _inject_input, _inject_py_input
from r2py.types import EffectBundle, EffectClass


# ---------------------------------------------------------------------------
# ScalarGenerator
# ---------------------------------------------------------------------------

class TestScalarGenerator:
    def test_int_sample_stays_int(self):
        g = ScalarGenerator(42)
        rng = random.Random(0)
        for _ in range(20):
            v = g.sample(rng)
            assert isinstance(v, int)

    def test_float_sample_stays_float(self):
        g = ScalarGenerator(3.14)
        rng = random.Random(0)
        v = g.sample(rng)
        assert isinstance(v, float)

    def test_bool_sample_is_bool(self):
        g = ScalarGenerator(True)
        rng = random.Random(0)
        samples = {g.sample(rng) for _ in range(20)}
        assert samples == {True, False}

    def test_str_sample_is_str(self):
        g = ScalarGenerator("hello")
        rng = random.Random(0)
        v = g.sample(rng)
        assert isinstance(v, str)

    def test_none_sample_is_none(self):
        g = ScalarGenerator(None)
        rng = random.Random(0)
        assert g.sample(rng) is None

    def test_int_boundary_cases_include_zero(self):
        g = ScalarGenerator(5)
        cases = g.boundary_cases()
        assert 0 in cases

    def test_float_boundary_cases_include_extreme(self):
        g = ScalarGenerator(1.0)
        cases = g.boundary_cases()
        assert any(abs(c) >= 1e14 for c in cases if isinstance(c, float))

    def test_float_boundary_cases_include_none(self):
        g = ScalarGenerator(1.0)
        cases = g.boundary_cases()
        assert None in cases

    def test_str_boundary_cases_include_empty(self):
        g = ScalarGenerator("hello")
        cases = g.boundary_cases()
        assert "" in cases


# ---------------------------------------------------------------------------
# VectorGenerator
# ---------------------------------------------------------------------------

class TestVectorGenerator:
    def test_sample_returns_list(self):
        g = VectorGenerator([1, 2, 3])
        rng = random.Random(0)
        v = g.sample(rng)
        assert isinstance(v, list)

    def test_boundary_includes_empty(self):
        g = VectorGenerator([1, 2, 3])
        cases = g.boundary_cases()
        assert [] in cases

    def test_boundary_includes_length_one(self):
        # The R scalar-vs-vector trap §3.7
        g = VectorGenerator([10, 20, 30])
        cases = g.boundary_cases()
        assert any(isinstance(c, list) and len(c) == 1 for c in cases)

    def test_boundary_includes_na_present(self):
        g = VectorGenerator([1, 2, 3])
        cases = g.boundary_cases()
        assert any(isinstance(c, list) and None in c for c in cases)

    def test_empty_observed_still_works(self):
        g = VectorGenerator([])
        rng = random.Random(0)
        v = g.sample(rng)
        assert isinstance(v, list)


# ---------------------------------------------------------------------------
# DataFrameGenerator
# ---------------------------------------------------------------------------

class TestDataFrameGenerator:
    def test_sample_preserves_columns(self):
        df = {"a": [1, 2], "b": ["x", "y"]}
        g = DataFrameGenerator(df)
        rng = random.Random(0)
        result = g.sample(rng)
        assert set(result.keys()) == {"a", "b"}

    def test_boundary_includes_zero_rows(self):
        df = {"a": [1, 2]}
        g = DataFrameGenerator(df)
        cases = g.boundary_cases()
        assert any(all(len(v) == 0 for v in c.values()) for c in cases)

    def test_boundary_includes_one_row(self):
        df = {"a": [1, 2]}
        g = DataFrameGenerator(df)
        cases = g.boundary_cases()
        assert any(all(len(v) == 1 for v in c.values() if isinstance(v, list)) for c in cases)


# ---------------------------------------------------------------------------
# generator_from_observed + boundary_cases factory
# ---------------------------------------------------------------------------

class TestGeneratorFactory:
    def test_int_gets_scalar_gen(self):
        g = generator_from_observed(42)
        assert isinstance(g, ScalarGenerator)

    def test_float_gets_scalar_gen(self):
        g = generator_from_observed(3.14)
        assert isinstance(g, ScalarGenerator)

    def test_list_gets_vector_gen(self):
        g = generator_from_observed([1, 2, 3])
        assert isinstance(g, VectorGenerator)

    def test_dict_gets_dataframe_gen(self):
        g = generator_from_observed({"a": [1]})
        assert isinstance(g, DataFrameGenerator)

    def test_none_gets_scalar_gen(self):
        g = generator_from_observed(None)
        assert isinstance(g, ScalarGenerator)

    def test_boundary_cases_int(self):
        cases = boundary_cases(5)
        assert 0 in cases

    def test_boundary_cases_list(self):
        cases = boundary_cases([1, 2])
        assert [] in cases

    def test_boundary_cases_dict(self):
        cases = boundary_cases({"x": [1, 2]})
        assert any(isinstance(c, dict) for c in cases)


# ---------------------------------------------------------------------------
# _inject_input / _inject_py_input
# ---------------------------------------------------------------------------

class TestInjectInput:
    def test_inject_int_r(self):
        result = _inject_input("print(x)", "x", 42)
        assert "x <- 42" in result
        assert "print(x)" in result

    def test_inject_none_r(self):
        result = _inject_input("print(x)", "x", None)
        assert "x <- NULL" in result

    def test_inject_bool_true_r(self):
        result = _inject_input("", "x", True)
        assert "x <- TRUE" in result

    def test_inject_list_r(self):
        result = _inject_input("", "x", [1, 2, 3])
        assert "c(1, 2, 3)" in result

    def test_inject_int_python(self):
        result = _inject_py_input("print(x)", "x", 42)
        assert "x = 42" in result

    def test_inject_str_python(self):
        result = _inject_py_input("", "x", "hello")
        assert "x = 'hello'" in result


# ---------------------------------------------------------------------------
# run_fuzz smoke test (no R runtime — entities without actual_bundle are skipped)
# ---------------------------------------------------------------------------

class TestRunFuzzSmoke:
    def test_no_entities_returns_empty(self):
        from r2py.types import ScriptMap
        sm = ScriptMap(source="x <- 1")
        # Base ScriptMap has no entities, so fuzz returns []
        result = run_fuzz(sm, "x = 1", config=FuzzConfig(n_inputs=2))
        assert result == []

    def test_fuzz_config_defaults(self):
        cfg = FuzzConfig()
        assert cfg.n_inputs == 10
        assert cfg.seed == 42
        assert cfg.timeout_s == 30
