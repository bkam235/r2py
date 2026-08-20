"""Tests for the Pattern Library (§6): pattern, store, index, retrieval,
epistemology, writer, and PatternLibrary facade."""
from __future__ import annotations

import json
import math
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest

from r2py.library.pattern import (
    EvidenceEntry, Pattern, from_markdown, to_markdown,
)
from r2py.library.store import PatternStore
from r2py.library.index import PatternIndex
from r2py.library.retrieval import retrieve, _token_overlap
from r2py.library import epistemology, writer
from r2py.library import get_library
from r2py.types import Edit, EditKind


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pattern(pid: str, package: str = "base",
                  confidence: str = "tentative", seed: bool = False) -> Pattern:
    return Pattern(
        id=pid, package=package, confidence=confidence, seed=seed,  # type: ignore
        guidance=f"Guidance for {pid}.",
        created=date.today().isoformat(),
        last_review=date.today().isoformat(),
    )


def _make_edit(pattern_id: str, package: str = "", guidance: str = "Use this pattern.") -> Edit:
    return Edit(kind=EditKind.REPLACE_CALL, pattern_id=pattern_id,
                params={"package": package}, guidance=guidance)


class _FakeEntity:
    def __init__(self, package: str = "base", name: str = "x", kind_value: str = "Variable"):
        self.package = package
        self.name = name

        class _Kind:
            value = kind_value
        self.kind = _Kind()


# ---------------------------------------------------------------------------
# 3.1 Pattern round-trip
# ---------------------------------------------------------------------------

class TestPatternRoundTrip:
    def test_minimal_pattern(self):
        p = _make_pattern("test.foo")
        text = to_markdown(p)
        p2 = from_markdown(text)
        assert p2.id == "test.foo"
        assert p2.package == "base"
        assert p2.confidence == "tentative"
        assert p2.seed is False
        assert "Guidance for test.foo" in p2.guidance

    def test_with_evidence(self):
        p = _make_pattern("test.bar")
        p.evidence.append(EvidenceEntry(
            script_id="script1.R", score=0.92,
            verification_path="exact", variable="result",
        ))
        text = to_markdown(p)
        p2 = from_markdown(text)
        assert len(p2.evidence) == 1
        assert p2.evidence[0].script_id == "script1.R"
        assert abs(p2.evidence[0].score - 0.92) < 1e-3
        assert p2.evidence[0].verification_path == "exact"
        assert p2.evidence[0].variable == "result"

    def test_with_contradictions(self):
        p = _make_pattern("test.baz")
        p.contradictions.append("script2.R/entity_x: score regressed to 0.400")
        text = to_markdown(p)
        p2 = from_markdown(text)
        assert len(p2.contradictions) == 1
        assert "script2.R" in p2.contradictions[0]

    def test_seed_true(self):
        p = _make_pattern("test.seed", seed=True)
        text = to_markdown(p)
        p2 = from_markdown(text)
        assert p2.seed is True

    def test_confirmed_confidence(self):
        p = _make_pattern("test.conf", confidence="confirmed")
        text = to_markdown(p)
        p2 = from_markdown(text)
        assert p2.confidence == "confirmed"

    def test_invalid_front_matter_raises(self):
        with pytest.raises(ValueError, match="front-matter"):
            from_markdown("no front matter here")

    def test_unknown_confidence_defaults_to_tentative(self):
        text = "---\nid: x\npackage: base\nconfidence: unknown\nseed: false\ncreated: 2026-01-01\nlast_review: 2026-01-01\n---\n\n# x\n\n## Guidance\ng\n\n## Evidence\n(none)\n\n## Contradictions\n(none)\n"
        p = from_markdown(text)
        assert p.confidence == "tentative"

    def test_demotion_threshold(self):
        p = _make_pattern("t")
        assert p.demotion_threshold() == 1  # no evidence → threshold = 1
        p.evidence = [EvidenceEntry("s", 0.9, "exact", "v")] * 4
        assert p.demotion_threshold() == max(3, math.ceil(4 * 0.75))  # = 3


# ---------------------------------------------------------------------------
# 3.2 PatternStore CRUD
# ---------------------------------------------------------------------------

class TestPatternStore:
    def test_save_and_get(self, tmp_path):
        store = PatternStore(tmp_path)
        p = _make_pattern("base.foo")
        store.save(p)
        p2 = store.get("base.foo")
        assert p2 is not None
        assert p2.id == "base.foo"

    def test_get_missing_returns_none(self, tmp_path):
        store = PatternStore(tmp_path)
        assert store.get("nonexistent") is None

    def test_list_ids(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("p1"))
        store.save(_make_pattern("p2"))
        ids = store.list_ids()
        assert "p1" in ids
        assert "p2" in ids

    def test_load_all(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("a"))
        store.save(_make_pattern("b"))
        all_pats = store.load_all()
        assert "a" in all_pats
        assert "b" in all_pats

    def test_overwrite_on_save(self, tmp_path):
        store = PatternStore(tmp_path)
        p = _make_pattern("x")
        store.save(p)
        p.guidance = "Updated guidance."
        store.save(p)
        p2 = store.get("x")
        assert p2.guidance == "Updated guidance."

    def test_delete(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("del_me"))
        store.delete("del_me")
        assert store.get("del_me") is None

    def test_delete_nonexistent_no_error(self, tmp_path):
        store = PatternStore(tmp_path)
        store.delete("ghost")  # should not raise


# ---------------------------------------------------------------------------
# 3.3 PatternIndex rebuild + lookup
# ---------------------------------------------------------------------------

class TestPatternIndex:
    def test_rebuild_and_lookup(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("dplyr.filter", package="dplyr"))
        store.save(_make_pattern("base.foo", package="base"))
        index = PatternIndex(tmp_path)
        index.rebuild(store)
        ids = index.lookup("dplyr")
        assert "dplyr.filter" in ids

    def test_lookup_missing_package_returns_empty(self, tmp_path):
        index = PatternIndex(tmp_path)
        assert index.lookup("unknownpkg") == []

    def test_get_meta(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("base.x", package="base", confidence="confirmed"))
        index = PatternIndex(tmp_path)
        index.rebuild(store)
        meta = index.get_meta("base.x")
        assert meta["confidence"] == "confirmed"
        assert meta["package"] == "base"

    def test_upsert_meta(self, tmp_path):
        index = PatternIndex(tmp_path)
        index.upsert_meta("new.pat", "newpkg", "tentative", 0, 0, False)
        assert "new.pat" in index.lookup("newpkg")

    def test_remove(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("rem.me", package="rem"))
        index = PatternIndex(tmp_path)
        index.rebuild(store)
        assert "rem.me" in index.lookup("rem")
        index.remove("rem.me")
        assert "rem.me" not in index.lookup("rem")

    def test_persisted_to_disk(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("base.y", package="base"))
        index = PatternIndex(tmp_path)
        index.rebuild(store)
        # Re-load from disk
        index2 = PatternIndex(tmp_path)
        assert "base.y" in index2.lookup("base")


# ---------------------------------------------------------------------------
# 3.4 Retrieval ordering
# ---------------------------------------------------------------------------

class TestRetrieval:
    def _setup(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        return store, index

    def test_package_first(self, tmp_path):
        store, index = self._setup(tmp_path)
        store.save(_make_pattern("dplyr.a", package="dplyr", seed=True))
        store.save(_make_pattern("base.a", package="base", seed=True))
        index.rebuild(store)
        entity = _FakeEntity(package="dplyr")
        results = retrieve(entity, k=5, store=store, index=index)
        ids = [p.id for p in results]
        assert "dplyr.a" in ids
        if "base.a" in ids:
            assert ids.index("dplyr.a") < ids.index("base.a")

    def test_excludes_contradicted(self, tmp_path):
        store, index = self._setup(tmp_path)
        store.save(_make_pattern("base.bad", package="base", confidence="contradicted"))
        store.save(_make_pattern("base.good", package="base", seed=True))
        index.rebuild(store)
        entity = _FakeEntity(package="base")
        results = retrieve(entity, k=5, store=store, index=index)
        ids = [p.id for p in results]
        assert "base.bad" not in ids
        assert "base.good" in ids

    def test_no_seeds_filter(self, tmp_path):
        store, index = self._setup(tmp_path)
        store.save(_make_pattern("base.seed", package="base", seed=True))
        # Non-seed tentative patterns need ≥2 genuine improvement entries to be retrieved.
        learned = _make_pattern("base.learned", package="base", seed=False)
        learned.evidence = [EvidenceEntry("s1", 0.9, "exact", "v"),
                            EvidenceEntry("s2", 0.8, "exact", "v")]
        store.save(learned)
        index.rebuild(store)
        entity = _FakeEntity(package="base")
        results = retrieve(entity, k=5, store=store, index=index, no_seeds=True)
        ids = [p.id for p in results]
        assert "base.seed" not in ids
        assert "base.learned" in ids

    def test_k_limit(self, tmp_path):
        store, index = self._setup(tmp_path)
        for i in range(10):
            store.save(_make_pattern(f"base.p{i}", package="base"))
        index.rebuild(store)
        entity = _FakeEntity(package="base")
        results = retrieve(entity, k=3, store=store, index=index)
        assert len(results) <= 3

    def test_empty_library_returns_empty(self, tmp_path):
        store, index = self._setup(tmp_path)
        entity = _FakeEntity(package="base")
        results = retrieve(entity, k=3, store=store, index=index)
        assert results == []

    def test_token_overlap(self):
        assert _token_overlap("hello world", "hello there") > 0
        assert _token_overlap("", "hello") == 0.0
        assert _token_overlap("abc", "abc") == 1.0


# ---------------------------------------------------------------------------
# 3.5 Epistemology transitions
# ---------------------------------------------------------------------------

class TestEpistemology:
    def test_contradiction_threshold_demotes_tentative_to_contradicted(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.x", package="base", confidence="tentative")
        # threshold = 1 when evidence is empty
        p.contradictions = ["s1/e1: regressed"]
        store.save(p)
        index.rebuild(store)
        log = epistemology.review(store, index)
        p2 = store.get("base.x")
        assert p2.confidence == "contradicted"
        assert any("demoted" in l for l in log)

    def test_contradiction_threshold_demotes_confirmed_to_tentative(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.y", package="base", confidence="confirmed")
        # 2 evidence entries → threshold = max(3, ceil(2*0.75)) = 3; need ≥3 contradictions
        p.evidence = [EvidenceEntry("s1", 0.9, "exact", "v")] * 2
        p.contradictions = ["s2/e2: regressed", "s3/e3: regressed", "s4/e4: regressed"]
        store.save(p)
        index.rebuild(store)
        epistemology.review(store, index)
        p2 = store.get("base.y")
        assert p2.confidence == "tentative"

    def test_below_threshold_no_demotion(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.z", package="base", confidence="confirmed")
        # 4 evidence entries → threshold = 2; 1 contradiction → no demotion
        p.evidence = [EvidenceEntry("s", 0.9, "exact", "v")] * 4
        p.contradictions = ["one"]
        store.save(p)
        index.rebuild(store)
        epistemology.review(store, index)
        p2 = store.get("base.z")
        assert p2.confidence == "confirmed"

    def test_conflict_between_confirmed_demotes_both(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p1 = _make_pattern("pkg.a", package="pkg", confidence="confirmed")
        p1.guidance = "Use method A."
        p2 = _make_pattern("pkg.b", package="pkg", confidence="confirmed")
        p2.guidance = "Use method B."
        store.save(p1)
        store.save(p2)
        index.rebuild(store)
        # Conflict detection requires a non-empty ast_shape_hash so it can
        # distinguish patterns that target the same (package, AST shape).
        # Without a shape hash, two patterns on the same package might cover
        # entirely different R constructs and should not conflict.
        index.upsert_meta("pkg.a", "pkg", "confirmed", 0, 0, False, ast_shape_hash="abc123")
        index.upsert_meta("pkg.b", "pkg", "confirmed", 0, 0, False, ast_shape_hash="abc123")
        log = epistemology.review(store, index)
        r1 = store.get("pkg.a")
        r2 = store.get("pkg.b")
        assert r1.confidence == "tentative"
        assert r2.confidence == "tentative"
        assert any("conflict" in l or "demoted" in l for l in log)

    def test_no_conflict_without_shape_hash(self, tmp_path):
        """Two confirmed patterns on the same package must NOT conflict when
        ast_shape_hash is empty — they may cover different R constructs."""
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p1 = _make_pattern("pkg.x", package="pkg", confidence="confirmed")
        p1.guidance = "Use method X."
        p2 = _make_pattern("pkg.y", package="pkg", confidence="confirmed")
        p2.guidance = "Use method Y."
        store.save(p1)
        store.save(p2)
        index.rebuild(store)  # ast_shape_hash stays "" for both
        log = epistemology.review(store, index)
        r1 = store.get("pkg.x")
        r2 = store.get("pkg.y")
        assert r1.confidence == "confirmed"
        assert r2.confidence == "confirmed"
        assert not any("demoted" in l for l in log)

    def test_stale_contradicted_archived(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.old", package="base", confidence="contradicted")
        store.save(p)
        index.rebuild(store)
        # Archival is run-count based: contradicted_at_run=0, total_runs must be ≥30.
        index.upsert_meta("base.old", "base", "contradicted", 0, 1, False,
                          contradicted_at_run=0)
        for _ in range(30):
            index.increment_runs()
        log = epistemology.review(store, index)
        # Pattern should no longer be in index
        assert "base.old" not in index.lookup("base")
        assert any("archived" in l for l in log)

    def test_recent_contradicted_not_archived(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.new", package="base", confidence="contradicted")
        p.last_review = date.today().isoformat()
        store.save(p)
        index.rebuild(store)
        log = epistemology.review(store, index)
        assert not any("archived" in l and "base.new" in l for l in log)


# ---------------------------------------------------------------------------
# 3.6 Writer: record_evidence / record_contradiction
# ---------------------------------------------------------------------------

class TestWriter:
    def test_record_evidence_creates_new_pattern(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        edit = _make_edit("new.pattern", package="base")
        writer.record_evidence(edit, 0.15, "script.R", "entity1", "exact", store, index)
        p = store.get("new.pattern")
        assert p is not None
        assert p.confidence == "tentative"
        assert len(p.evidence) == 1
        assert p.evidence[0].score == 0.15

    def test_record_evidence_appends_to_existing(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        store.save(_make_pattern("base.x", package="base"))
        edit = _make_edit("base.x")
        writer.record_evidence(edit, 0.1, "s1.R", "e1", "exact", store, index)
        writer.record_evidence(edit, 0.2, "s2.R", "e2", "exact", store, index)
        p = store.get("base.x")
        assert len(p.evidence) == 2

    def test_record_contradiction_appends(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        store.save(_make_pattern("base.y", package="base"))
        edit = _make_edit("base.y")
        writer.record_contradiction(edit, 0.3, "s1.R", "e1", store, index)
        p = store.get("base.y")
        assert len(p.contradictions) == 1

    def test_contradiction_triggers_demotion(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.z", package="base", confidence="tentative")
        # threshold = 1 (no evidence); one contradiction should demote
        store.save(p)
        index.rebuild(store)
        edit = _make_edit("base.z")
        writer.record_contradiction(edit, 0.2, "s1.R", "e1", store, index)
        p2 = store.get("base.z")
        assert p2.confidence == "contradicted"

    def test_record_tie_does_not_demote(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        p = _make_pattern("base.w", package="base", confidence="tentative")
        store.save(p)
        index.rebuild(store)
        edit = _make_edit("base.w")
        writer.record_tie(edit, "s.R", "e", store, index)
        p2 = store.get("base.w")
        # tie: tracked in tie_count only, evidence unchanged, confidence unchanged
        assert p2.confidence == "tentative"
        assert p2.tie_count == 1
        assert len(p2.evidence) == 0

    def test_no_pattern_id_is_noop(self, tmp_path):
        store = PatternStore(tmp_path)
        index = PatternIndex(tmp_path)
        edit = Edit(kind=EditKind.REPLACE_CALL, pattern_id=None)
        # Should not raise; no pattern created
        writer.record_evidence(edit, 0.1, "s.R", "e", "exact", store, index)
        assert store.list_ids() == []


# ---------------------------------------------------------------------------
# 3.7 PatternLibrary facade + get_library
# ---------------------------------------------------------------------------

class TestPatternLibrary:
    def test_get_library_creates_dir(self, tmp_path):
        lib_dir = tmp_path / "lib"
        lib = get_library(lib_dir)
        assert lib_dir.exists()
        assert repr(lib).startswith("PatternLibrary(")

    def test_retrieve_via_facade(self, tmp_path):
        lib = get_library(tmp_path)
        lib.store.save(_make_pattern("base.foo", package="base", seed=True))
        lib.index.rebuild(lib.store)
        entity = _FakeEntity(package="base")
        results = lib.retrieve(entity, k=3)
        assert any(p.id == "base.foo" for p in results)

    def test_record_evidence_via_facade(self, tmp_path):
        lib = get_library(tmp_path)
        edit = _make_edit("base.new", package="base")
        lib.record_evidence(edit, 0.2, script_id="s.R", entity_id="e1")
        p = lib.store.get("base.new")
        assert p is not None
        assert len(p.evidence) == 1

    def test_record_contradiction_via_facade(self, tmp_path):
        lib = get_library(tmp_path)
        lib.store.save(_make_pattern("base.p", package="base"))
        lib.index.rebuild(lib.store)
        edit = _make_edit("base.p")
        lib.record_contradiction(edit, 0.1, script_id="s.R", entity_id="e1")
        p = lib.store.get("base.p")
        assert len(p.contradictions) == 1

    def test_index_auto_rebuilt_if_empty(self, tmp_path):
        store = PatternStore(tmp_path)
        store.save(_make_pattern("base.q", package="base"))
        # Create library AFTER patterns exist; index should be built
        lib = get_library(tmp_path)
        assert "base.q" in lib.index.lookup("base")
