"""The value the search climbs (Stage 7), kept apart from the official score.

The official score forces the aggregate to exactly 0.0 whenever Python crashes and R did not.  A loop
that climbs it cannot tell a rewrite that fixed one of two crash sites from one that fixed nothing:
about half of the agent runs in the smoke arms started on that plateau, and 14-16 of 68 rewrites per arm
ended in a crash.  The search therefore ranks candidates by ``search_key`` instead.  Reported scores, the
pass threshold and every analysis keep using ``report.aggregate``.
"""
from __future__ import annotations

EPS = 1e-6


def entity_score(es) -> float:
    """An entity's score as the verifier averages it; 0 if it did not run."""
    if not es.executed_ok:
        return 0.0
    dims = [getattr(es, d) for d in es.active_dims]
    return sum(dims) / len(dims) if dims else 1.0


def entity_status(report, eid: str) -> str:
    """``ran`` | ``crashed`` (the crash happened here) | ``blocked`` (never reached: the program crashed
    earlier) | ``not_run`` (the program ran, the entity did not) | ``unknown`` (not scored).

    For analyses: a blocked entity's score says nothing about what was done to it. The prompt-load runs
    read 137 such outcomes as "guidance adopted, no gain" (2026-10-11). Without traceback attribution
    the first entity, in script order, that did not run is taken as the crash site.
    """
    es = report.by_entity.get(eid)
    if es is None:
        return "unknown"
    if es.executed_ok:
        return "ran"
    if report.py_exit_code == 0:
        return "not_run"
    culprits = list(getattr(report, "crash_entities", None) or [])
    if not culprits:
        culprits = [next(e for e, s in report.by_entity.items() if not s.executed_ok)]
    return "crashed" if eid in culprits else "blocked"


def search_key(report) -> tuple[int, float]:
    """``(runs_to_completion, shaped)``, compared lexicographically.

    A candidate that runs always beats one that crashes.  Among crashing candidates the value is the
    mean score of the entities that ran, weighted by the fraction of entities reached, so getting
    further, or fixing the entities already reached, is visible progress.  Without a per-entity table
    (attribution failed) there is no gradient and the value is 0.
    """
    if report.py_exit_code == 0:
        return 1, report.aggregate
    entities = list(report.by_entity.values())
    ran = [e for e in entities if e.executed_ok]
    if not entities or not ran:
        return 0, 0.0
    return 0, (sum(entity_score(e) for e in ran) / len(ran)) * (len(ran) / len(entities))


def better(new, old) -> bool:
    """True if the key of ``new`` improves on ``old`` (strictly, beyond float noise)."""
    (nr, ns), (orr, os_) = search_key(new), search_key(old)
    return nr > orr or (nr == orr and ns > os_ + EPS)
