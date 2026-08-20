"""Tests for loop.py data logging (effect bundles + score reports)."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from r2py.loop import run_loop
from r2py.types import EffectBundle, EntityScore, ScoreReport


def _make_verify_side_effect(*decomps):
    decomp_iter = iter(decomps)

    def _side_effect(*args, return_bundle=False, **kwargs):
        d = next(decomp_iter)
        return (d, EffectBundle()) if return_bundle else d

    return _side_effect


_S4_GET_R_BUNDLE = "r2py.stage4.get_r_bundle"
_S2 = "r2py.seed.translate"
_S4 = "r2py.stage4.verify"
_EP = "r2py.library.epistemology.review"
_AGENT = "r2py.harness.agent.reason"


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


def _mock_library() -> MagicMock:
    lib = MagicMock()
    lib.retrieve.return_value = []
    lib.store = MagicMock()
    lib.index = MagicMock()
    return lib


class TestEffectBundleWriting:
    def test_effect_bundle_r_written_when_output_dir_set(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        seed_decomp = _mock_decomp(0.9)

        with (
            patch(_S2, return_value=("x = 1", {})),
            patch(_S4, side_effect=_make_verify_side_effect(seed_decomp)),
            patch(_S4_GET_R_BUNDLE, return_value=EffectBundle()),
            patch(_EP),
            patch(_AGENT, return_value=None),
        ):
            run_loop(script_map, library, score_threshold=0.85, output_dir=tmp_path)

        assert (tmp_path / "effect_bundle.r.json").exists()

    def test_effect_bundle_py0_written_when_output_dir_set(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        seed_decomp = _mock_decomp(0.9)

        with (
            patch(_S2, return_value=("x = 1", {})),
            patch(_S4, side_effect=_make_verify_side_effect(seed_decomp)),
            patch(_S4_GET_R_BUNDLE, return_value=EffectBundle()),
            patch(_EP),
            patch(_AGENT, return_value=None),
        ):
            run_loop(script_map, library, score_threshold=0.85, output_dir=tmp_path)

        assert (tmp_path / "effect_bundle.py.0.json").exists()

    def test_effect_bundle_files_are_valid_json(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        seed_decomp = _mock_decomp(0.9)

        with (
            patch(_S2, return_value=("x = 1", {})),
            patch(_S4, side_effect=_make_verify_side_effect(seed_decomp)),
            patch(_S4_GET_R_BUNDLE, return_value=EffectBundle()),
            patch(_EP),
            patch(_AGENT, return_value=None),
        ):
            run_loop(script_map, library, score_threshold=0.85, output_dir=tmp_path)

        for fname in ["effect_bundle.r.json", "effect_bundle.py.0.json"]:
            data = json.loads((tmp_path / fname).read_text())
            assert "stdout" in data
            assert "exit_code" in data

    def test_no_bundle_files_without_output_dir(self, tmp_path):
        script_map = _mock_script_map()
        library = _mock_library()
        seed_decomp = _mock_decomp(0.9)

        with (
            patch(_S2, return_value=("x = 1", {})),
            patch(_S4, return_value=seed_decomp),
            patch(_EP),
            patch(_AGENT, return_value=None),
        ):
            run_loop(script_map, library, score_threshold=0.85, output_dir=None)

        assert not list(tmp_path.glob("effect_bundle*.json"))
