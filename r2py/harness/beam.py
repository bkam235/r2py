"""Width with shared progress: rounds of parallel chains that restart from the best states found (Stage 11e).

``reason_wide`` runs independent chains; each spends its depth on its own dead ends, and most runs end by
stalling, not by budget.  Here a round runs ``width`` short chains (``max_steps`` each); the next round
restarts them from the best distinct states found so far, so a chain that got furthest is built on
instead of being thrown away.  The search value (``harness.objective``) is deterministic, so the best
states can be ranked directly; no exploration bonus is needed.
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from . import objective as _obj

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import ScoreReport


def _top_distinct(pool: list, k: int) -> list:
    """The k best distinct states, best first; the best one repeated if fewer than k exist."""
    ranked: list = []
    for item in pool:
        pos = len(ranked)
        for i, other in enumerate(ranked):
            if _obj.better(item[1], other[1]):
                pos = i
                break
        ranked.insert(pos, item)
    ranked = ranked[:k]
    while len(ranked) < k:
        ranked.append(ranked[0])
    return ranked


def reason_beam(harnesses: list, *, current_source: str, score_report: "ScoreReport", script_map: "ScriptMap",
                max_rounds: int = 3, budget_s: float | None = None, score_threshold: float = 0.9,
                **kwargs) -> "tuple[str, ScoreReport] | None":
    """``kwargs`` go to ``agent.reason``; its ``max_steps`` is the length of one chain in one round."""
    from . import agent

    deadline = time.monotonic() + budget_s if budget_s else None
    width = len(harnesses)
    pool = [(current_source, score_report)]
    seen = {current_source}
    for rnd in range(max_rounds):
        best_rep = _top_distinct(pool, 1)[0][1]
        if best_rep.aggregate >= score_threshold or (deadline and time.monotonic() >= deadline):
            break
        starts = _top_distinct(pool, width)
        remaining = max(1.0, deadline - time.monotonic()) if deadline else None

        def chain(i: int):
            src, rep = starts[i]
            try:
                return agent.reason(current_source=src, score_report=rep, harness=harnesses[i],
                                    script_map=script_map, branch=i, budget_s=remaining,
                                    score_threshold=score_threshold, **kwargs)
            except Exception as exc:   # one failing chain must not lose the others
                print(f"[Beam]    chain {i} failed: {type(exc).__name__}: {exc}")
                return None

        with ThreadPoolExecutor(width) as ex:
            results = [r for r in ex.map(chain, range(width)) if r is not None]
        fresh = [r for r in results if r[0] not in seen]
        print(f"[Beam]    round {rnd + 1}: " + (", ".join(f"{r[1].aggregate:.3f}" for r in results) or "no chain improved"))
        if not fresh:
            break
        pool += fresh
        seen.update(r[0] for r in fresh)
    best_src, best_rep = _top_distinct(pool, 1)[0]
    return (best_src, best_rep) if _obj.better(best_rep, score_report) else None
