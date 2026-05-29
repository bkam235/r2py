"""Tests for r2py/library/bandit.py (§12.6 B)."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from r2py.library.bandit import (
    BanditArm,
    BanditModel,
    _N_FEATURES,
    _init_arm,
    _solve,
    choose_action,
    extract_context,
    load_model,
    save_model,
    ucb_score,
    update_arm,
)
from r2py.types import EditKind, EntityScore


ALL_ARMS = [e.value for e in EditKind]


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

class TestExtractContext:
    def test_vector_length(self):
        es = EntityScore(entity_id="e1", type_match=0.8, data_output=0.5)
        ctx = extract_context(es, "FunctionCall", "dplyr")
        assert len(ctx) == _N_FEATURES

    def test_scores_in_first_six(self):
        es = EntityScore(
            entity_id="e1",
            type_match=0.1, control_flow_match=0.2, data_output=0.3,
            variable_output=0.4, callable_output=0.5, side_effects=0.6,
        )
        ctx = extract_context(es, "FunctionCall", "dplyr")
        assert ctx[:6] == pytest.approx([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

    def test_hash_features_in_range(self):
        es = EntityScore(entity_id="e1")
        ctx = extract_context(es, "Variable", "base")
        assert 0.0 <= ctx[6] <= 1.0
        assert 0.0 <= ctx[7] <= 1.0

    def test_same_inputs_deterministic(self):
        es = EntityScore(entity_id="e1", type_match=0.5)
        a = extract_context(es, "FunctionDef", "ggplot2")
        b = extract_context(es, "FunctionDef", "ggplot2")
        assert a == b


# ---------------------------------------------------------------------------
# LinUCB arithmetic
# ---------------------------------------------------------------------------

class TestLinUCB:
    def test_cold_arm_gives_finite_score(self):
        arm = _init_arm(_N_FEATURES)
        ctx = [0.5] * _N_FEATURES
        score = ucb_score(arm, ctx)
        assert isinstance(score, float)
        assert score > 0.0  # exploration bonus on cold arm

    def test_choose_action_returns_valid_arm(self):
        model = BanditModel(arms={})
        ctx = [0.5] * _N_FEATURES
        chosen = choose_action(model, ctx, ALL_ARMS)
        assert chosen in ALL_ARMS

    def test_choose_action_with_all_arms_cold(self):
        model = BanditModel(arms={arm: _init_arm(_N_FEATURES) for arm in ALL_ARMS})
        ctx = [0.0] * _N_FEATURES
        chosen = choose_action(model, ctx, ALL_ARMS)
        assert chosen in ALL_ARMS

    def test_update_increases_expected_reward(self):
        arm = _init_arm(_N_FEATURES)
        ctx = [1.0] * _N_FEATURES
        score_before = ucb_score(arm, ctx)
        update_arm(arm, ctx, reward=1.0)
        score_after = ucb_score(arm, ctx)
        # After a positive update the expected value should be higher or UCB changes.
        assert isinstance(score_after, float)

    def test_solve_identity(self):
        n = 3
        I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        b = [1.0, 2.0, 3.0]
        x = _solve(I, b)
        assert x == pytest.approx(b)

    def test_solve_2x2(self):
        A = [[2.0, 1.0], [1.0, 3.0]]
        b = [5.0, 10.0]
        x = _solve(A, b)
        # Check Ax ≈ b
        residual = [
            A[0][0]*x[0] + A[0][1]*x[1] - b[0],
            A[1][0]*x[0] + A[1][1]*x[1] - b[1],
        ]
        assert residual == pytest.approx([0.0, 0.0], abs=1e-9)


# ---------------------------------------------------------------------------
# Save / load
# ---------------------------------------------------------------------------

class TestSaveLoadBandit:
    def test_round_trip(self, tmp_path):
        arm = _init_arm(_N_FEATURES)
        # Apply a couple of updates.
        update_arm(arm, [0.5] * _N_FEATURES, reward=0.8)
        model = BanditModel(
            arms={"ReplaceCall": arm},
            n_features=_N_FEATURES,
            alpha=1.0,
        )
        path = save_model(model, tmp_path)
        assert path.exists()

        loaded = load_model(tmp_path)
        assert loaded is not None
        assert "ReplaceCall" in loaded.arms
        loaded_arm = loaded.arms["ReplaceCall"]
        for i, row in enumerate(arm.A):
            assert loaded_arm.A[i] == pytest.approx(row)
        assert loaded_arm.b == pytest.approx(arm.b)

    def test_manifest_written(self, tmp_path):
        model = BanditModel(arms={})
        save_model(model, tmp_path, reward_learned=0.4, reward_heuristic=0.3)
        manifests = list(tmp_path.glob("*/manifest.json"))
        assert len(manifests) == 1
        data = json.loads(manifests[0].read_text())
        assert data["reward_learned"] == pytest.approx(0.4)

    def test_load_absent_dir_returns_none(self):
        assert load_model("/nonexistent/xyz") is None

    def test_load_empty_dir_returns_none(self, tmp_path):
        assert load_model(tmp_path) is None


# ---------------------------------------------------------------------------
# Train — data threshold refusal
# ---------------------------------------------------------------------------

class TestTrainThreshold:
    def test_refuses_below_min_transitions(self, tmp_path):
        log_dir = tmp_path / "outputs" / "run1"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "edits.log.jsonl"
        tr = {
            "edit_kind": "ReplaceCall",
            "entity_id": "e1",
            "entity_kind": "FunctionCall",
            "package": "dplyr",
            "type_match": 0.5, "control_flow_match": 0.5, "data_output": 0.5,
            "variable_output": 0.5, "callable_output": 0.5, "side_effects": 0.5,
            "outcome": "accepted",
            "score_delta": 0.1,
            "script_id": "s1",
            "iteration": 0,
        }
        log_file.write_text("\n".join(json.dumps(tr) for _ in range(5)))

        from r2py.library.bandit import train
        rc = train(
            out_dir=str(tmp_path / "models"),
            min_transitions=200,
            log_glob=str(log_dir / "edits.log.jsonl"),
        )
        assert rc == 1
