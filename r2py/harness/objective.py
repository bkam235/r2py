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
