"""Stage 4 — Verification: execution equivalence testing (§7)."""
from __future__ import annotations

from ..types import ScoreReport, ScriptMap


def verify(
    script_map: ScriptMap,
    candidate: str,
    changed: "list[str] | None" = None,
) -> ScoreReport:
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).
    """
    raise NotImplementedError("Stage 4 not yet implemented (architecture step 4)")
