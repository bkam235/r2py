"""Tests for Stage 1 — Script analysis (§3).

Coverage:
- AST parse round-trip (ast.py)
- CoverageTracker (coverage.py)
- Walker entity classification (walker.py)
- §3.7 R-semantic annotation detection (walker.py)
- ScriptMap JSON round-trip (script_map.py)
- to_annotated_r output (script_map.py)
- branch_extractor slice building (branch_extractor.py)
- runner._py_to_r helper (runner.py)
- package_lookup._find_symbol_in_file (package_lookup.py)
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from r2py.types import EffectClass, EntityKind
from r2py.stage1.ast import parse
from r2py.stage1.coverage import CoverageTracker
from r2py.stage1.effects import SideEffect, STATIC_PREDICTIONS
from r2py.stage1.entities import AstNode, Entity, EntityRef, SourceLocation
from r2py.stage1.script_map import (
    BranchAnalysis, ScriptMap, from_json, to_annotated_r, to_json,
)
from r2py.stage1.walker import walk

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SIMPLE_R = "x <- 1\nprint(x)\n"
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "simple.R"


# ---------------------------------------------------------------------------
# ast.py — parse()
# ---------------------------------------------------------------------------

class TestParse:
    def test_root_kind_is_program(self):
        root = parse(SIMPLE_R)
        assert root.kind == "program"

    def test_has_children(self):
        root = parse(SIMPLE_R)
        assert len(root.children) > 0

    def test_named_children_only_named(self):
        root = parse(SIMPLE_R)
        for c in root.named_children():
            assert c.is_named

    def test_text_roundtrip(self):
        src = "x <- 42L\n"
        root = parse(src)
        # Root text should be the whole source
        assert root.text.strip() == src.strip()

    def test_start_end_positions(self):
        root = parse("x <- 1\n")
        child = root.named_children()[0]  # binary_operator
        assert child.start == (0, 0)
        assert child.end[0] == 0  # same line

    def test_child_by_field_assignment(self):
        root = parse("x <- 1\n")
        assign = root.named_children()[0]
        lhs = assign.child_by_field("lhs")
        assert lhs is not None
        assert lhs.text == "x"
        rhs = assign.child_by_field("rhs")
        assert rhs is not None
        assert rhs.text == "1"

    def test_parse_empty_source(self):
        root = parse("")
        assert root.kind == "program"

    def test_parse_multiline(self):
        src = "a <- 1\nb <- 2\nc <- a + b\n"
        root = parse(src)
        assert root.start == (0, 0)
        named = root.named_children()
        assert len(named) == 3


# ---------------------------------------------------------------------------
# coverage.py — CoverageTracker
# ---------------------------------------------------------------------------

class TestCoverageTracker:
    def test_empty_report(self):
        t = CoverageTracker()
        r = t.report()
        assert r.total_nodes == 0
        assert r.fraction_analyzed == 1.0

    def test_register_and_mark(self):
        t = CoverageTracker()
        t.register("n1")
        t.register("n2")
        t.mark("n1", "dynamic")
        r = t.report()
        assert r.total_nodes == 2
        assert r.by_status["dynamic"] == 1
        assert r.by_status["unreachable"] == 1
        assert r.fraction_analyzed == pytest.approx(0.5)

    def test_mark_upgrades_only(self):
        t = CoverageTracker()
        t.register("n1")
        t.mark("n1", "dynamic")
        t.mark("n1", "unreachable")  # should not downgrade
        r = t.report()
        assert r.by_status["dynamic"] == 1
        assert r.by_status["unreachable"] == 0

    def test_analyzed_is_top_priority(self):
        t = CoverageTracker()
        t.register("n1")
        t.mark("n1", "branch-extracted")
        t.mark("n1", "analyzed")   # upgrade
        t.mark("n1", "dynamic")    # no further upgrade (analyzed > dynamic)
        assert t._status["n1"] == "analyzed"

    def test_reachable_uncovered(self):
        t = CoverageTracker()
        t.register("n1")
        t.register("n2")
        t.mark("n1", "analyzed")
        assert t.reachable_uncovered() == ["n2"]

    def test_fraction_all_analyzed(self):
        t = CoverageTracker()
        for i in range(5):
            t.register(f"n{i}")
            t.mark(f"n{i}", "dynamic")
        assert t.report().fraction_analyzed == 1.0


# ---------------------------------------------------------------------------
# walker.py — entity classification
# ---------------------------------------------------------------------------

class TestWalkerEntityClassification:
    def _walk(self, src: str) -> dict:
        root = parse(src)
        entities, _ = walk(root, "test.R")
        return entities

    def test_variable_assignment(self):
        # RHS is a non-literal expression → VARIABLE (not CONSTANT)
        entities = self._walk("a <- 1\nb <- 2\nx <- a + b\n")
        assert "x" in entities
        assert entities["x"].kind == EntityKind.VARIABLE

    def test_constant_integer_literal(self):
        entities = self._walk("N <- 10L\n")
        assert entities["N"].kind == EntityKind.CONSTANT

    def test_constant_float_literal(self):
        entities = self._walk("PI <- 3.14\n")
        assert entities["PI"].kind == EntityKind.CONSTANT

    def test_function_def(self):
        entities = self._walk("f <- function(x) x + 1\n")
        assert "f" in entities
        assert entities["f"].kind == EntityKind.FUNCTION_DEF

    def test_library_import(self):
        entities = self._walk("library(dplyr)\n")
        assert "import_dplyr" in entities
        e = entities["import_dplyr"]
        assert e.kind == EntityKind.LIBRARY_IMPORT
        assert e.package == "dplyr"

    def test_require_import(self):
        entities = self._walk("require(ggplot2)\n")
        assert "import_ggplot2" in entities

    def test_function_call(self):
        entities = self._walk("x <- 1\nprint(x)\n")
        assert "print" in entities
        assert entities["print"].kind == EntityKind.FUNCTION_CALL

    def test_multiple_entities(self):
        entities = self._walk("a <- 1\nb <- 2\ncat(a + b)\n")
        assert "a" in entities
        assert "b" in entities
        assert "cat" in entities

    def test_nested_function_body(self):
        src = "f <- function(x) {\n  y <- x * 2\n  y\n}\n"
        entities = self._walk(src)
        assert "f" in entities
        assert entities["f"].kind == EntityKind.FUNCTION_DEF

    def test_if_else_entities(self):
        src = "x <- 5\nif (x > 0) print(x) else cat('no')\n"
        entities = self._walk(src)
        assert "x" in entities

    def test_formula_assignment(self):
        entities = self._walk("f <- y ~ x + z\n")
        assert "f" in entities
        assert entities["f"].kind == EntityKind.FORMULA

    def test_external_symbol_namespace(self):
        entities = self._walk("dplyr::filter(df, x > 0)\n")
        filter_ent = next((e for e in entities.values() if e.name == "filter"), None)
        assert filter_ent is not None
        assert filter_ent.kind == EntityKind.EXTERNAL_SYMBOL
        assert filter_ent.package == "dplyr"

    def test_external_symbol_triple_colon(self):
        entities = self._walk("rlang:::sym('x')\n")
        sym_ent = next((e for e in entities.values() if e.name == "sym"), None)
        assert sym_ent is not None
        assert sym_ent.kind == EntityKind.EXTERNAL_SYMBOL
        assert sym_ent.package == "rlang"

    def test_if_condition_does_not_create_entity(self):
        """The condition expression of an if-statement must not produce its own entity."""
        # 'x > y' is just the condition text — the walker should not register it as an entity.
        entities = self._walk("x <- 5\ny <- 3\nif (x > y) print(x)\n")
        entity_names = {e.name for e in entities.values()}
        # No entity whose name is the raw condition text or an operator
        assert "x > y" not in entity_names
        assert ">" not in entity_names


# ---------------------------------------------------------------------------
# walker.py — §3.7 R-semantic annotations
# ---------------------------------------------------------------------------

class TestRSemanticAnnotations:
    def _flags(self, src: str) -> set[str]:
        """Return the union of all r_semantic_flags across all entities."""
        root = parse(src)
        entities, _ = walk(root, "test.R")
        flags: set[str] = set()
        for e in entities.values():
            flags.update(e.r_semantic_flags)
        return flags

    def test_na_semantics_na_literal(self):
        flags = self._flags("x <- NA\n")
        assert "na_semantics" in flags

    def test_na_semantics_na_integer(self):
        flags = self._flags("x <- NA_integer_\n")
        assert "na_semantics" in flags

    def test_super_assign(self):
        flags = self._flags("f <- function() { x <<- 1 }\n")
        assert "super_assign" in flags

    def test_indexing_1based(self):
        # Subscript access triggers the flag
        flags = self._flags("v <- c(1,2,3)\nx <- v[1]\n")
        # The subscript is inside the assignment rhs; the enclosing entity gets flagged
        assert "indexing_1based" in flags

    def test_nse_dplyr_filter(self):
        flags = self._flags("library(dplyr)\ndf2 <- filter(df, x > 0)\n")
        assert "nse" in flags

    def test_nse_subset(self):
        flags = self._flags("df2 <- subset(df, x > 0)\n")
        assert "nse" in flags

    def test_copy_on_modify(self):
        flags = self._flags("a <- 1\nb <- a\n")
        assert "copy_on_modify" in flags

    def test_vector_recycling(self):
        flags = self._flags("a <- c(1,2)\nb <- c(1,2,3)\nx <- a + b\n")
        assert "vector_recycling" in flags

    def test_dispatch_r6class(self):
        src = "MyClass <- R6Class('MyClass', public=list(x=NULL))\n"
        flags = self._flags(src)
        assert "dispatch_s3s4r6" in flags

    def test_formula_tilde_flags_nse(self):
        # y ~ x should flag 'nse' via the ~ binary_operator detection
        flags = self._flags("model <- lm(y ~ x, data=df)\n")
        assert "nse" in flags

    def test_no_false_positives_simple(self):
        # A plain assignment with no R-semantic quirks should have no flags.
        flags = self._flags("x <- 1\ny <- 2\nz <- x + y\n")
        # vector_recycling is expected here (arithmetic on two identifiers)
        assert "na_semantics" not in flags
        assert "super_assign" not in flags


# ---------------------------------------------------------------------------
# walker.py — predicted effects
# ---------------------------------------------------------------------------

class TestPredictedEffects:
    def _effects(self, src: str) -> list[SideEffect]:
        root = parse(src)
        _, effects = walk(root, "test.R")
        return effects

    def test_print_predicts_stdout(self):
        effects = self._effects("print('hello')\n")
        assert any(e.kind == EffectClass.STDOUT for e in effects)

    def test_library_predicts_env(self):
        effects = self._effects("library(ggplot2)\n")
        assert any(e.kind == EffectClass.ENV for e in effects)

    def test_write_csv_predicts_files(self):
        effects = self._effects("write.csv(df, 'out.csv')\n")
        assert any(e.kind == EffectClass.FILES for e in effects)

    def test_set_seed_predicts_rng(self):
        effects = self._effects("set.seed(42)\n")
        assert any(e.kind == EffectClass.RNG for e in effects)

    def test_message_predicts_warnings(self):
        effects = self._effects("message('hi')\n")
        assert any(e.kind == EffectClass.WARNINGS for e in effects)

    def test_no_effects_for_pure_assignment(self):
        effects = self._effects("x <- 1\n")
        assert effects == []

    def test_all_effects_are_predicted(self):
        effects = self._effects("write.csv(df, 'out.csv')\nprint(x)\n")
        for e in effects:
            assert e.is_predicted is True


# ---------------------------------------------------------------------------
# script_map.py — JSON round-trip
# ---------------------------------------------------------------------------

class TestScriptMapSerialization:
    def _make_sm(self, src: str = SIMPLE_R) -> ScriptMap:
        root = parse(src)
        tracker = CoverageTracker()
        entities, effects = walk(root, "test.R", tracker)
        return ScriptMap(
            source=src, ast_root=root, entities=entities,
            effects=effects, coverage=tracker.report(),
        )

    def test_roundtrip_source(self):
        sm = self._make_sm()
        sm2 = from_json(to_json(sm))
        assert sm2.source == sm.source

    def test_roundtrip_entity_ids(self):
        sm = self._make_sm()
        sm2 = from_json(to_json(sm))
        assert set(sm2.entities.keys()) == set(sm.entities.keys())

    def test_roundtrip_entity_kind(self):
        sm = self._make_sm()
        sm2 = from_json(to_json(sm))
        for eid in sm.entities:
            assert sm2.entities[eid].kind == sm.entities[eid].kind

    def test_roundtrip_effects(self):
        sm = self._make_sm()
        sm2 = from_json(to_json(sm))
        assert len(sm2.effects) == len(sm.effects)

    def test_roundtrip_coverage(self):
        sm = self._make_sm()
        sm2 = from_json(to_json(sm))
        assert sm2.coverage.fraction_analyzed == pytest.approx(sm.coverage.fraction_analyzed)

    def test_roundtrip_no_ast_root(self):
        """ScriptMap without ast_root serializes fine."""
        sm = self._make_sm()
        sm.ast_root = None
        sm2 = from_json(to_json(sm))
        assert sm2.ast_root is None

    def test_save_and_load(self):
        sm = self._make_sm()
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "test.map.json"
            from r2py.stage1.script_map import save, load
            save(sm, p)
            sm2 = load(p)
        assert sm2.source == sm.source
        assert set(sm2.entities.keys()) == set(sm.entities.keys())

    def test_json_is_valid(self):
        sm = self._make_sm()
        d = to_json(sm)
        # Must survive json.dumps → json.loads round-trip
        assert json.loads(json.dumps(d)) == d


# ---------------------------------------------------------------------------
# script_map.py — to_annotated_r
# ---------------------------------------------------------------------------

class TestAnnotatedR:
    def test_annotation_inserted_after_entity_line(self):
        src = "x <- 1\nprint(x)\n"
        root = parse(src)
        entities, _ = walk(root, "test.R")
        sm = ScriptMap(source=src, ast_root=root, entities=entities, effects=[])
        ann = to_annotated_r(sm)
        assert "# r2py: x" in ann
        assert "# r2py: print" in ann

    def test_annotation_preserves_source_lines(self):
        src = "a <- 1\nb <- 2\n"
        root = parse(src)
        entities, _ = walk(root, "test.R")
        sm = ScriptMap(source=src, ast_root=root, entities=entities, effects=[])
        ann = to_annotated_r(sm)
        # Original lines still present
        assert "a <- 1" in ann
        assert "b <- 2" in ann

    def test_annotation_order(self):
        src = "x <- 1\nprint(x)\n"
        root = parse(src)
        entities, _ = walk(root, "test.R")
        sm = ScriptMap(source=src, ast_root=root, entities=entities, effects=[])
        ann = to_annotated_r(sm)
        x_pos = ann.index("# r2py: x")
        print_pos = ann.index("# r2py: print")
        assert x_pos < print_pos


# ---------------------------------------------------------------------------
# branch_extractor.py
# ---------------------------------------------------------------------------

class TestBranchExtractor:
    def test_extract_branch_with_known_vars(self):
        from r2py.stage1.branch_extractor import extract_branch
        from r2py.types import EffectBundle

        # Branch body uses variable 'x' which is in parent_bundle.data
        branch_node = parse("cat(x)\n").named_children()[0]
        root_full = parse("x <- 42\n")
        entities, _ = walk(root_full, "test.R")
        parent_bundle = EffectBundle(data={"x": 42})
        slice_src = extract_branch(branch_node, entities, parent_bundle)
        assert "x <- 42" in slice_src
        assert "cat" in slice_src

    def test_extract_branch_no_parent_data(self):
        from r2py.stage1.branch_extractor import extract_branch
        from r2py.types import EffectBundle

        branch_node = parse("print('hello')\n").named_children()[0]
        slice_src = extract_branch(branch_node, {}, EffectBundle())
        assert "print" in slice_src

    def test_extract_branch_float_value(self):
        from r2py.stage1.branch_extractor import extract_branch
        from r2py.types import EffectBundle

        branch_node = parse("y <- x * 2\n").named_children()[0]
        root_full = parse("x <- 3.5\n")
        entities, _ = walk(root_full, "test.R")
        parent_bundle = EffectBundle(data={"x": 3.5})
        slice_src = extract_branch(branch_node, entities, parent_bundle)
        assert "x <- 3.5" in slice_src

    def test_extract_for_branch_basic(self):
        from r2py.stage1.branch_extractor import extract_for_branch
        from r2py.types import EffectBundle

        source = "for (n in nums) { total <- total + n }"
        for_node = parse(source).named_children()[0]
        parent_bundle = EffectBundle(data={"nums": [1, 2, 3], "total": 0})
        entities, _ = walk(parse("nums <- c(1,2,3)\ntotal <- 0\n"), "test.R")
        result = extract_for_branch(for_node, entities, parent_bundle)
        assert result is not None
        # Should contain the for header with a single element from nums
        assert "for (n in" in result
        assert "total" in result

    def test_extract_for_branch_fallback_no_seq(self):
        """With no sequence data available, falls back to iterating over 1."""
        from r2py.stage1.branch_extractor import extract_for_branch
        from r2py.types import EffectBundle

        source = "for (x in unknown_var) { print(x) }"
        for_node = parse(source).named_children()[0]
        result = extract_for_branch(for_node, {}, EffectBundle())
        assert result is not None
        assert "for (x in" in result

    def test_collect_for_branch_nodes(self):
        """_collect_branch_nodes_rec should surface for_statement as a branch."""
        from r2py.stage1 import _collect_branch_nodes

        source = "nums <- c(1, 2)\nfor (n in nums) { print(n) }\n"
        root = parse(source)
        entities, _ = walk(root, "test.R")
        branch_list = _collect_branch_nodes(root, entities)
        branch_kinds = [node.kind for _, node, *_ in branch_list]
        assert "for_statement" in branch_kinds

    def test_while_branch_marked_not_executed(self):
        """while_statement body should be collected with was_executed=False."""
        from r2py.stage1 import _collect_branch_nodes

        source = "x <- 5\nwhile (x > 0) { x <- x - 1 }\n"
        root = parse(source)
        entities, _ = walk(root, "test.R")
        branch_list = _collect_branch_nodes(root, entities)
        while_branches = [entry for entry in branch_list if entry[0].startswith("while_branch")]
        assert len(while_branches) == 1, "Expected exactly one while branch"
        _id, _node, _parent, _cond, was_executed = while_branches[0]
        assert was_executed is False, "while body should not be pre-marked as executed"

    def test_while_condition_text_captured(self):
        """Condition text for while branch should include 'while('."""
        from r2py.stage1 import _collect_branch_nodes

        source = "x <- 5\nwhile (x > 0) { x <- x - 1 }\n"
        root = parse(source)
        entities, _ = walk(root, "test.R")
        branch_list = _collect_branch_nodes(root, entities)
        while_branches = [e for e in branch_list if e[0].startswith("while_branch")]
        _id, _node, _parent, condition_text, _exec = while_branches[0]
        assert condition_text.startswith("while(")

    def test_extract_branch_on_while_body(self):
        """extract_branch handles while body node and restores free variables."""
        from r2py.stage1.branch_extractor import extract_branch
        from r2py.types import EffectBundle

        source = "x <- 5\nwhile (x > 0) { x <- x - 1 }\n"
        root = parse(source)
        entities, _ = walk(root, "test.R")
        while_node = None
        for node in root.children:
            if node.kind == "while_statement":
                while_node = node
                break
        assert while_node is not None
        body_node = while_node.child_by_field("body")
        assert body_node is not None
        parent_bundle = EffectBundle(data={"x": 5})
        slice_src = extract_branch(body_node, entities, parent_bundle)
        assert "x <- 5" in slice_src
        assert "x - 1" in slice_src


# ---------------------------------------------------------------------------
# runner.py — _py_to_r helper
# ---------------------------------------------------------------------------

class TestPyToR:
    def _convert(self, value):
        from r2py.stage1.runner import _py_to_r
        return _py_to_r(value)

    def test_none(self):
        assert self._convert(None) == "NULL"

    def test_true(self):
        assert self._convert(True) == "TRUE"

    def test_false(self):
        assert self._convert(False) == "FALSE"

    def test_int(self):
        assert self._convert(5) == "5L"

    def test_float(self):
        assert self._convert(3.14) == "3.14"

    def test_nan(self):
        assert self._convert(float("nan")) == "NaN"

    def test_inf(self):
        assert self._convert(float("inf")) == "Inf"

    def test_neg_inf(self):
        assert self._convert(float("-inf")) == "-Inf"

    def test_string(self):
        assert self._convert("hello") == '"hello"'

    def test_string_with_quotes(self):
        result = self._convert('say "hi"')
        assert '\\"' in result

    def test_list_single(self):
        assert self._convert([1]) == "1L"

    def test_list_multiple(self):
        result = self._convert([1, 2, 3])
        assert result == "c(1L, 2L, 3L)"

    def test_dict_simple(self):
        result = self._convert({"a": 1, "b": 2})
        assert result == "list(a=1L, b=2L)"

    def test_dict_empty(self):
        assert self._convert({}) == "list()"

    def test_dict_with_nested_complex_returns_none(self):
        # If a nested value is too complex, give up
        assert self._convert({"a": object()}) is None

    def test_dict_mixed_types(self):
        result = self._convert({"x": 1.5, "y": True, "z": "hi"})
        assert "x=1.5" in result
        assert "y=TRUE" in result
        assert 'z="hi"' in result

    def test_dataframe_produces_jsonlite_call(self):
        pytest.importorskip("pandas")
        import pandas as pd
        df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
        result = self._convert(df)
        assert result is not None
        assert "jsonlite::fromJSON" in result


# ---------------------------------------------------------------------------
# package_lookup.py — _find_symbol_in_file
# ---------------------------------------------------------------------------

class TestFindSymbolInFile:
    def test_finds_function_definition(self):
        from r2py.stage1.package_lookup import _find_symbol_in_file

        with tempfile.NamedTemporaryFile(suffix=".R", mode="w",
                                         delete=False, encoding="utf-8") as f:
            f.write("# some comment\nmyFn <- function(x) x + 1\n")
            fpath = Path(f.name)

        try:
            loc = _find_symbol_in_file(fpath, "myFn")
            assert loc is not None
            assert loc.start_line == 1
            assert "myFn" in fpath.read_text()
        finally:
            fpath.unlink()

    def test_returns_none_when_not_found(self):
        from r2py.stage1.package_lookup import _find_symbol_in_file

        with tempfile.NamedTemporaryFile(suffix=".R", mode="w",
                                         delete=False, encoding="utf-8") as f:
            f.write("x <- 1\n")
            fpath = Path(f.name)

        try:
            loc = _find_symbol_in_file(fpath, "myFn")
            assert loc is None
        finally:
            fpath.unlink()

    def test_returns_none_for_missing_file(self):
        from r2py.stage1.package_lookup import _find_symbol_in_file
        loc = _find_symbol_in_file(Path("/nonexistent/path/file.R"), "fn")
        assert loc is None


# ---------------------------------------------------------------------------
# Integration: analyze() on fixture (static path, no Rscript needed)
# ---------------------------------------------------------------------------

class TestAnalyzeFixture:
    def test_fixture_r_file_exists(self):
        assert FIXTURE_PATH.exists(), f"Missing fixture: {FIXTURE_PATH}"

    def test_analyze_returns_scriptmap(self):
        """analyze() in static-only mode (sandbox skipped gracefully) returns ScriptMap."""
        # We monkey-patch run_script to raise so the test doesn't need Rscript.
        import r2py.stage1 as s1
        import r2py.stage1.runner as runner_mod
        original = runner_mod.run_script

        def _fail(*args, **kwargs):
            raise RuntimeError("no Rscript in test environment")

        runner_mod.run_script = _fail
        try:
            sm = s1.analyze(FIXTURE_PATH)
        finally:
            runner_mod.run_script = original

        assert sm.source != ""
        assert len(sm.entities) > 0
        assert sm.coverage is not None
        assert sm.coverage.fraction_analyzed > 0

    def test_analyze_finds_library_import(self):
        import r2py.stage1 as s1
        import r2py.stage1.runner as runner_mod
        original = runner_mod.run_script
        runner_mod.run_script = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("no Rscript"))

        try:
            sm = s1.analyze(FIXTURE_PATH)
        finally:
            runner_mod.run_script = original

        kinds = {e.kind for e in sm.entities.values()}
        assert EntityKind.LIBRARY_IMPORT in kinds

    def test_analyze_detects_super_assign_flag(self):
        import r2py.stage1 as s1
        import r2py.stage1.runner as runner_mod
        original = runner_mod.run_script
        runner_mod.run_script = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("no Rscript"))

        try:
            sm = s1.analyze(FIXTURE_PATH)
        finally:
            runner_mod.run_script = original

        all_flags = {f for e in sm.entities.values() for f in e.r_semantic_flags}
        assert "super_assign" in all_flags

    def test_top_level_analyze_api(self):
        """r2py.analyze() (top-level) delegates to stage1 correctly."""
        import r2py
        import r2py.stage1.runner as runner_mod
        original = runner_mod.run_script
        runner_mod.run_script = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("no Rscript"))

        try:
            sm = r2py.analyze(FIXTURE_PATH)
        finally:
            runner_mod.run_script = original

        assert hasattr(sm, "entities")
        assert hasattr(sm, "coverage")

    def test_static_fallback_effects_survive_sandbox_failure(self):
        """When run_script raises, statically predicted effects are still in the ScriptMap."""
        import r2py.stage1 as s1
        import r2py.stage1.runner as runner_mod
        import tempfile
        original = runner_mod.run_script
        runner_mod.run_script = lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("no Rscript"))

        fpath = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".R", mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.write("print('hello')\n")
                fpath = Path(f.name)
            sm = s1.analyze(fpath)
            # Static prediction for print() → STDOUT must survive the sandbox failure
            assert any(e.kind == EffectClass.STDOUT for e in sm.effects)
        finally:
            runner_mod.run_script = original
            if fpath and fpath.exists():
                fpath.unlink()


# ---------------------------------------------------------------------------
# package_lookup.py — backtick-quoted symbol forms
# ---------------------------------------------------------------------------

class TestFindSymbolBacktick:
    def test_finds_backtick_quoted_function(self):
        """`_find_symbol_in_file` matches backtick-quoted function definitions."""
        from r2py.stage1.package_lookup import _find_symbol_in_file

        with tempfile.NamedTemporaryFile(
            suffix=".R", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("`my.fn` <- function(x) x + 1\n")
            fpath = Path(f.name)

        try:
            loc = _find_symbol_in_file(fpath, "my.fn")
            assert loc is not None
            assert loc.start_line == 0
        finally:
            fpath.unlink()

    def test_finds_no_space_function_assignment(self):
        """`_find_symbol_in_file` matches `fn=function(` (no spaces) style."""
        from r2py.stage1.package_lookup import _find_symbol_in_file

        with tempfile.NamedTemporaryFile(
            suffix=".R", mode="w", delete=False, encoding="utf-8"
        ) as f:
            f.write("myFn=function(x) x\n")
            fpath = Path(f.name)

        try:
            loc = _find_symbol_in_file(fpath, "myFn")
            assert loc is not None
        finally:
            fpath.unlink()


# ---------------------------------------------------------------------------
# script_map.py — to_annotated_r edge cases
# ---------------------------------------------------------------------------

class TestAnnotatedREdgeCases:
    def test_function_def_is_single_entity(self):
        """Walker produces only the FUNCTION_DEF entity for a one-liner function.

        Calls inside a function body are NOT extracted as separate entities —
        the entire function (body included) is translated as one unit.
        """
        src = "f <- function(x) print(x)\n"
        root = parse(src)
        entities, _ = walk(root, "test.R")
        # Only 'f' — 'print' inside the body must not become a separate entity.
        assert list(entities.keys()) == ["f"]
        sm = ScriptMap(source=src, ast_root=root, entities=entities, effects=[])
        ann = to_annotated_r(sm)
        assert "# r2py: f" in ann
        assert "# r2py: print" not in ann
        # Original source line appears exactly once
        assert ann.count("f <- function(x) print(x)") == 1
