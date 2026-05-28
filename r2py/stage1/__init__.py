"""Stage 1 — Script analysis: AST walk, branch extraction, ScriptMap (§3)."""
from __future__ import annotations

from pathlib import Path

from ..types import ScriptMap


def analyze(r_path: Path) -> ScriptMap:
    """Parse and analyze an R script, returning its ScriptMap."""
    raise NotImplementedError("Stage 1 not yet implemented (architecture step 2)")
