"""Stage 4 — Verification: execution equivalence testing (§7)."""
from __future__ import annotations

from ..types import ScoreReport, ScriptMap
from .verifier import verify as _verify, get_r_bundle


def verify(
    script_map: ScriptMap,
    candidate: str,
    changed: "list[str] | None" = None,
    **kwargs,
) -> "ScoreReport | tuple[ScoreReport, object]":
    """Score a candidate Python translation against the R ScriptMap.

    changed: entity_ids touched by the last edit; if provided, only those
    entities are re-verified (incremental verification, §7.4).

    Additional keyword arguments are forwarded to verifier.verify():
      data_compare: "auto" | "exact" | "embedding" (default "auto")
      rtol, atol: numeric tolerances for data comparison (§7.3.1)
      use_fuzz: enable differential fuzzing (§7.8)
      fuzz_n: number of fuzz inputs per entity
      use_judge: enable LLM judge fallback (D4, disabled by default)
      workdir: explicit Path for sandbox workdir (temp dir by default)
      timeout_s: per-run sandbox timeout in seconds
    """
    return _verify(script_map, candidate, changed=changed, **kwargs)
