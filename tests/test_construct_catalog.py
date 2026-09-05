"""Tests for the pre-translation construct catalog (r2py/construct_catalog.py)."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from r2py.construct_catalog import R_SEMANTIC_GUIDANCE, format_construct_notes


def _entity(flags: list[str]) -> SimpleNamespace:
    return SimpleNamespace(r_semantic_flags=flags, name="x", kind=None)


class TestFormatConstructNotes:
    def test_empty_entities(self):
        assert format_construct_notes({}) == ""

    def test_no_flags(self):
        entities = {"e1": _entity([]), "e2": _entity([])}
        assert format_construct_notes(entities) == ""

    def test_single_flag(self):
        entities = {"e1": _entity(["indexing_1based"])}
        result = format_construct_notes(entities)
        assert "indexing_1based" in result
        assert "1-based" in result

    def test_multiple_flags(self):
        entities = {
            "e1": _entity(["na_semantics"]),
            "e2": _entity(["super_assign"]),
        }
        result = format_construct_notes(entities)
        assert "na_semantics" in result
        assert "super_assign" in result

    def test_deduplication(self):
        entities = {
            "e1": _entity(["indexing_1based"]),
            "e2": _entity(["indexing_1based"]),
            "e3": _entity(["indexing_1based"]),
        }
        result = format_construct_notes(entities)
        assert result.count("indexing_1based") == 1

    def test_python_keyword_arg_filtered(self):
        entities = {"e1": _entity(["python_keyword_arg:from"])}
        assert format_construct_notes(entities) == ""

    def test_mixed_flags_keyword_filtered(self):
        entities = {"e1": _entity(["na_semantics", "python_keyword_arg:in"])}
        result = format_construct_notes(entities)
        assert "na_semantics" in result
        assert "python_keyword_arg" not in result

    def test_unknown_flag_ignored(self):
        entities = {"e1": _entity(["some_future_flag"])}
        result = format_construct_notes(entities)
        assert result == ""

    def test_unknown_flag_with_known(self):
        entities = {"e1": _entity(["some_future_flag", "nse"])}
        result = format_construct_notes(entities)
        assert "nse" in result
        assert "some_future_flag" not in result

    def test_deterministic_ordering(self):
        entities = {
            "e1": _entity(["vector_recycling", "indexing_1based", "nse"]),
        }
        result = format_construct_notes(entities)
        keys = list(R_SEMANTIC_GUIDANCE.keys())
        idx_1based = keys.index("indexing_1based")
        idx_nse = keys.index("nse")
        idx_recycle = keys.index("vector_recycling")
        pos_1based = result.index("indexing_1based")
        pos_nse = result.index("nse")
        pos_recycle = result.index("vector_recycling")
        assert (idx_1based < idx_nse < idx_recycle) == (pos_1based < pos_nse < pos_recycle)

    def test_entity_without_flags_attr(self):
        entities = {"e1": SimpleNamespace(name="x", kind=None)}
        assert format_construct_notes(entities) == ""

    def test_all_known_flags_have_guidance(self):
        all_flags = [
            "indexing_1based", "super_assign", "na_semantics", "nse",
            "vector_recycling", "copy_on_modify", "platform_specific",
            "dispatch_s3s4r6", "scalar_vs_vector", "vector_constructor",
        ]
        for flag in all_flags:
            assert flag in R_SEMANTIC_GUIDANCE, f"Missing guidance for {flag}"
            entities = {"e1": _entity([flag])}
            result = format_construct_notes(entities)
            assert flag in result, f"Flag {flag} not in output"
