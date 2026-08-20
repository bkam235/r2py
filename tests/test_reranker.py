"""Tests for r2py/library/reranker.py (§12.6 A).

Feature extraction and save/load run without LightGBM. The full training path
is skipped when lightgbm is unavailable.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from r2py.library.reranker import (
    FEATURE_NAMES,
    _recency_norm,
    extract_features,
    load_model,
    rerank,
    save_model,
)
from r2py.library.pattern import EvidenceEntry, Pattern

try:
    import lightgbm  # noqa: F401
    HAS_LGB = True
except ImportError:
    HAS_LGB = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pattern(pid: str, package: str = "dplyr", confidence: str = "confirmed",
                  n_evidence: int = 3, n_contradictions: int = 0) -> Pattern:
    evidence = [
        EvidenceEntry(script_id="s1", score=0.5, verification_path="exact", variable="x")
        for _ in range(n_evidence)
    ]
    contradictions = [f"s{i}" for i in range(n_contradictions)]
    return Pattern(
        id=pid,
        package=package,
        confidence=confidence,
        seed=False,
        guidance="Use filter() with boolean mask.",
        evidence=evidence,
        contradictions=contradictions,
        created="2026-01-01",
        last_review="2026-01-15",
    )


class _MockEntity:
    def __init__(self, package: str = "dplyr", name: str = "filter_call",
                 kind_value: str = "FunctionCall"):
        self.package = package
        self.name = name
        self.kind = MagicMock()
        self.kind.value = kind_value


# ---------------------------------------------------------------------------
# Feature extraction tests
# ---------------------------------------------------------------------------

class TestExtractFeatures:
    def test_feature_vector_length(self):
        entity = _MockEntity()
        patterns = [_make_pattern("p1"), _make_pattern("p2")]
        rows = extract_features(entity, patterns)
        assert len(rows) == 2
        assert all(len(r) == len(FEATURE_NAMES) for r in rows)

    def test_package_match_flag(self):
        entity = _MockEntity(package="dplyr")
        same_pkg = _make_pattern("p1", package="dplyr")
        diff_pkg = _make_pattern("p2", package="tidyr")
        rows = extract_features(entity, [same_pkg, diff_pkg])
        assert rows[0][0] == 1.0   # package_match for same
        assert rows[1][0] == 0.0   # no match for different

    def test_confidence_int(self):
        entity = _MockEntity()
        confirmed = _make_pattern("p1", confidence="confirmed")
        tentative = _make_pattern("p2", confidence="tentative")
        rows = extract_features(entity, [confirmed, tentative])
        assert rows[0][3] == 1.0
        assert rows[1][3] == 0.0

    def test_accept_rate_laplace(self):
        entity = _MockEntity()
        pat = _make_pattern("p1", n_evidence=3, n_contradictions=1)
        rows = extract_features(entity, [pat])
        # accept_rate = 3 / (3 + 1 + 1) = 0.6
        assert abs(rows[0][6] - 3 / 5) < 1e-6

    def test_accept_rate_zero_evidence(self):
        entity = _MockEntity()
        pat = _make_pattern("p1", n_evidence=0, n_contradictions=0)
        rows = extract_features(entity, [pat])
        # accept_rate = 0 / (0 + 0 + 1) = 0.0
        assert rows[0][6] == 0.0

    def test_empty_patterns(self):
        entity = _MockEntity()
        assert extract_features(entity, []) == []

    def test_recency_norm_recent(self):
        from datetime import date
        today = date.today()
        val = _recency_norm(today.isoformat(), today)
        assert val == 1.0

    def test_recency_norm_old(self):
        from datetime import date, timedelta
        today = date.today()
        old = (today - timedelta(days=400)).isoformat()
        val = _recency_norm(old, today)
        assert val == 0.0

    def test_recency_norm_empty(self):
        from datetime import date
        assert _recency_norm("", date.today()) == 0.0


# ---------------------------------------------------------------------------
# Reranking tests
# ---------------------------------------------------------------------------

class TestRerank:
    def test_rerank_none_model_returns_unchanged(self):
        entity = _MockEntity()
        patterns = [_make_pattern("p1"), _make_pattern("p2")]
        result = rerank(entity, patterns, model=None)
        assert result == patterns

    def test_rerank_empty_returns_empty(self):
        entity = _MockEntity()
        assert rerank(entity, [], model=None) == []

    def test_rerank_with_mock_model(self):
        entity = _MockEntity()
        patterns = [_make_pattern("p1"), _make_pattern("p2"), _make_pattern("p3")]
        # Mock model that reverses the order (scores p3 highest).
        mock_model = MagicMock()
        mock_model.predict.return_value = [0.1, 0.5, 0.9]
        result = rerank(entity, patterns, model=mock_model)
        assert [p.id for p in result] == ["p3", "p2", "p1"]

    def test_rerank_model_exception_returns_unchanged(self):
        entity = _MockEntity()
        patterns = [_make_pattern("p1"), _make_pattern("p2")]
        mock_model = MagicMock()
        mock_model.predict.side_effect = RuntimeError("boom")
        result = rerank(entity, patterns, model=mock_model)
        assert result == patterns


# ---------------------------------------------------------------------------
# Save / load tests
# ---------------------------------------------------------------------------

class TestSaveLoadModel:
    def test_save_creates_files(self):
        if not HAS_LGB:
            pytest.skip("lightgbm not installed")
        import lightgbm as lgb
        import numpy as np

        X = np.array([[1.0, 0.5, 0.3, 1.0, 3.0, 0.0, 0.75, 0.9],
                      [0.0, 0.2, 0.1, 0.0, 1.0, 0.0, 0.5, 0.5]], dtype=np.float32)
        y = np.array([1.0, 0.0], dtype=np.float32)
        group = np.array([2], dtype=np.int32)
        ds = lgb.Dataset(X, label=y, group=group, feature_name=FEATURE_NAMES)
        params = dict(objective="lambdarank", metric="ndcg", ndcg_eval_at=[1],
                      num_leaves=4, verbosity=-1, max_position=2)
        model = lgb.train(params, ds, num_boost_round=5)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = save_model(model, tmpdir, ndcg3_learned=0.8, ndcg3_heuristic=0.6)
            assert path.exists()
            manifest = json.loads((path.parent / "manifest.json").read_text())
            assert "artifact_hash" in manifest
            assert manifest["ndcg3_learned"] == pytest.approx(0.8)

    def test_load_model_absent_dir_returns_none(self):
        result = load_model("/nonexistent/path/xyz")
        assert result is None

    def test_load_model_empty_dir_returns_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            assert load_model(tmpdir) is None


# ---------------------------------------------------------------------------
# Train function — data threshold refusal
# ---------------------------------------------------------------------------

class TestTrainThreshold:
    def test_refuses_below_min_episodes(self, tmp_path):
        # Write a log with only 3 episodes (well below 500).
        log_dir = tmp_path / "outputs" / "run1"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "edits.log.jsonl"
        ep = {
            "candidates": [{"pattern_id": "p1", "package_match": 1,
                             "ast_shape_sim": 0.5, "token_sim": 0.3,
                             "confidence": "confirmed", "evidence_count": 2,
                             "contradiction_count": 0}],
            "chosen_pattern_id": "p1",
            "outcome": "accepted",
            "score_delta": 0.1,
            "script_id": "s1",
            "iteration": 0,
        }
        log_file.write_text("\n".join(json.dumps(ep) for _ in range(3)))
        log_glob = str(log_dir / "edits.log.jsonl")

        from r2py.library.reranker import train
        rc = train(
            out_dir=str(tmp_path / "models"),
            min_episodes=500,
            log_glob=log_glob,
            library_dir=str(tmp_path / "library"),
        )
        assert rc == 1
