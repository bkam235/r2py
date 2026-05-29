"""Tests for loop.py data logging (edits.log.jsonl + library_diff.json, §12.3)."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from r2py.loop import run_loop
from r2py.types import (
    Candidate, Edit, EditKind, EntityScore, RetrievalEpisode, ScoreReport
)

_S2 = "r2py.stage2.translate"
_S3_PROPOSE = "r2py.stage3.propose_edit"
_S3_APPLY = "r2py.stage3.apply_edit"
_S4 = "r2py.stage4.verify"
_EP = "r2py.library.epistemology.review"


# ---------------------------------------------------------------------------
# Shared mock factories
# ---------------------------------------------------------------------------

def _mock_decomp(aggregate: float = 0.5) -> ScoreReport:
    return ScoreReport(
        aggregate=aggregate,
        by_entity={"e1": EntityScore(entity_id="e1", type_match=aggregate)},
    )


def _mock_script_map(source: str = "x <- 1") -> object:
    sm = MagicMock()
    sm.source = source
    sm.entities = {}
    return sm


def _mock_library(patterns: list = None) -> MagicMock:
    lib = MagicMock()
    lib.retrieve.return_value = patterns or []
    lib.learned_retrieval = False
    lib.learned_policy = False
    lib._bandit_model = None   # explicitly None so isinstance check fails
    lib._reranker_model = None
    lib._models_loaded = True
    return lib


def _stub_edit(kind: EditKind = EditKind.REPLACE_CALL) -> Edit:
    return Edit(kind=kind, entity_ids=["e1"], params={}, pattern_id="p1")


# ---------------------------------------------------------------------------
# Core logging tests
# ---------------------------------------------------------------------------

class TestLoopLogging:
    def _run_with_single_accepted_edit(self, output_dir: Path) -> None:
        """Run a minimal loop where one edit gets accepted (score improves)."""
        script_map = _mock_script_map()
        library = _mock_library()
        edit = _stub_edit()

        seed_src = "x = 1"
        improved_src = "x = 2"
        seed_decomp = _mock_decomp(0.4)
        improved_decomp = _mock_decomp(0.7)  # strictly better

        with (
            patch(_S2, return_value=seed_src),
            patch(_S4, side_effect=[seed_decomp, improved_decomp]),
            patch(_S3_PROPOSE, return_value=edit),
            patch(_S3_APPLY, return_value=improved_src),
            patch(_EP),
        ):
            run_loop(script_map, library, max_iters=1, output_dir=output_dir)

    def test_edits_log_written_when_output_dir_set(self, tmp_path):
        self._run_with_single_accepted_edit(tmp_path)
        log = tmp_path / "edits.log.jsonl"
        assert log.exists(), "edits.log.jsonl should be written when output_dir is set"

    def test_edits_log_is_valid_jsonl(self, tmp_path):
        self._run_with_single_accepted_edit(tmp_path)
        log = tmp_path / "edits.log.jsonl"
        lines = [l for l in log.read_text().splitlines() if l.strip()]
        # At minimum we should have the policy transition line.
        assert len(lines) >= 1
        for line in lines:
            json.loads(line)  # must parse without error

    def test_library_diff_written(self, tmp_path):
        self._run_with_single_accepted_edit(tmp_path)
        diff = tmp_path / "library_diff.json"
        assert diff.exists()
        data = json.loads(diff.read_text())
        assert "evidence_added" in data
        assert "contradictions_added" in data

    def test_library_diff_has_pattern_on_accepted(self, tmp_path):
        self._run_with_single_accepted_edit(tmp_path)
        diff = json.loads((tmp_path / "library_diff.json").read_text())
        assert "p1" in diff["evidence_added"]

    def test_no_files_without_output_dir(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        seed_decomp = _mock_decomp(0.9)

        with (
            patch(_S2, return_value="x = 1"),
            patch(_S4, return_value=seed_decomp),
            patch(_EP),
        ):
            run_loop(script_map, library, max_iters=0, output_dir=None)

        # No files should be created in tmp_path (which we'd only touch if output_dir set).
        assert not (tmp_path / "edits.log.jsonl").exists()
        assert not (tmp_path / "library_diff.json").exists()

    def test_policy_transition_outcome_stamped_accepted(self, tmp_path):
        self._run_with_single_accepted_edit(tmp_path)
        log = tmp_path / "edits.log.jsonl"
        lines = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
        transitions = [l for l in lines if "edit_kind" in l]
        assert len(transitions) >= 1
        assert transitions[0]["outcome"] == "accepted"

    def test_policy_transition_outcome_stamped_rejected(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        edit = _stub_edit()
        seed_src = "x = 1"
        worse_src = "x = 0"
        seed_decomp = _mock_decomp(0.6)
        worse_decomp = _mock_decomp(0.3)

        with (
            patch(_S2, return_value=seed_src),
            patch(_S4, side_effect=[seed_decomp, worse_decomp]),
            patch(_S3_PROPOSE, return_value=edit),
            patch(_S3_APPLY, return_value=worse_src),
            patch(_EP),
        ):
            run_loop(script_map, library, max_iters=1, output_dir=tmp_path)

        lines = [json.loads(l) for l in (tmp_path / "edits.log.jsonl").read_text().splitlines()
                 if l.strip()]
        transitions = [l for l in lines if "edit_kind" in l]
        assert transitions[0]["outcome"] == "rejected"


# ---------------------------------------------------------------------------
# Retrieval episode logging (requires _collector to be propagated)
# ---------------------------------------------------------------------------

class TestRetrievalEpisodeLogging:
    def test_episode_collected_when_patterns_retrieved(self, tmp_path):
        from r2py.types import EpisodeCollector, RetrievalEpisodeCandidate
        collector = EpisodeCollector()

        # Simulate policy.propose() appending an episode.
        from r2py.library.pattern import Pattern, EvidenceEntry
        pat = Pattern(
            id="dplyr.filter", package="dplyr", confidence="confirmed", seed=False,
            guidance="Use boolean mask.", evidence=[], contradictions=[],
        )

        entity = MagicMock()
        entity.id = "e1"
        entity.name = "filter_call"
        entity.package = "dplyr"
        entity.kind = MagicMock()
        entity.kind.value = "FunctionCall"

        from r2py.stage3.policy import _make_episode
        ep = _make_episode(entity, [pat], "dplyr.filter", exploit=True)
        collector.episodes.append(ep)

        assert len(collector.episodes) == 1
        ep = collector.episodes[0]
        assert ep.chosen_pattern_id == "dplyr.filter"
        assert ep.exploit_mode is True
        assert len(ep.candidates) == 1
        assert ep.candidates[0].pattern_id == "dplyr.filter"
        assert ep.outcome is None  # not yet stamped

    def test_episode_outcome_stamped_by_loop(self, tmp_path):
        """Episodes written to log have their outcome stamped (not None)."""
        from r2py.library.pattern import Pattern
        pat = Pattern(
            id="p1", package="dplyr", confidence="confirmed", seed=False,
            guidance="hint", evidence=[], contradictions=[],
        )

        script_map = _mock_script_map()
        library = _mock_library(patterns=[pat])
        edit = _stub_edit()
        seed_decomp = _mock_decomp(0.4)
        improved_decomp = _mock_decomp(0.7)

        # patch propose_edit to also append an episode to the collector.
        from r2py.types import RetrievalEpisode, RetrievalEpisodeCandidate

        def _fake_propose(candidate, lib, script_map=None, history=None, iteration=0,
                          _collector=None):
            if _collector is not None:
                _collector.episodes.append(RetrievalEpisode(
                    query_entity_id="e1", query_entity_kind="FunctionCall",
                    query_package="dplyr", query_entity_name="filter_call",
                    candidates=[RetrievalEpisodeCandidate(
                        pattern_id="p1", rank=0, package_match=True,
                        ast_shape_sim=0.5, token_sim=0.3, confidence="confirmed",
                        evidence_count=1, contradiction_count=0, last_review="2026-01-01",
                    )],
                    chosen_pattern_id="p1", exploit_mode=True,
                    outcome=None, score_delta=None, script_id="", iteration=0,
                ))
            return edit

        with (
            patch(_S2, return_value="x = 1"),
            patch(_S4, side_effect=[seed_decomp, improved_decomp]),
            patch(_S3_PROPOSE, side_effect=_fake_propose),
            patch(_S3_APPLY, return_value="x = 2"),
            patch(_EP),
        ):
            run_loop(script_map, library, max_iters=1, output_dir=tmp_path)

        log = tmp_path / "edits.log.jsonl"
        assert log.exists()
        lines = [json.loads(l) for l in log.read_text().splitlines() if l.strip()]
        episodes = [l for l in lines if "candidates" in l]
        assert len(episodes) >= 1
        assert episodes[0]["outcome"] == "accepted"
        assert episodes[0]["chosen_pattern_id"] == "p1"
