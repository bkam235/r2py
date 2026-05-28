"""Confidence transitions and archival rules for the Pattern Library (§6.5)."""
from __future__ import annotations

import math
from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .store import PatternStore
    from .index import PatternIndex

_ARCHIVE_AFTER_DAYS = 30
_DEMOTION_MAP = {"confirmed": "tentative", "tentative": "contradicted"}


def review(store: "PatternStore", index: "PatternIndex") -> list[str]:
    """Apply all §6.5 demotion rules.  Returns a list of human-readable log lines."""
    patterns = store.load_all()
    log: list[str] = []

    # Rule 1: contradiction-threshold demotion
    for pid, pat in list(patterns.items()):
        if pat.confidence == "contradicted":
            continue
        threshold = math.ceil(len(pat.evidence) / 2) if pat.evidence else 1
        if len(pat.contradictions) >= threshold:
            new_conf = _DEMOTION_MAP[pat.confidence]
            pat.confidence = new_conf  # type: ignore[assignment]
            pat.last_review = date.today().isoformat()
            store.save(pat)
            log.append(f"demoted {pid}: contradictions({len(pat.contradictions)}) >= threshold({threshold}) → {new_conf}")

    # Reload after mutations
    patterns = store.load_all()

    # Rule 2: conflict detection (two confirmed patterns on same package)
    from collections import defaultdict
    pkg_confirmed: dict[str, list[str]] = defaultdict(list)
    for pid, pat in patterns.items():
        if pat.confidence == "confirmed":
            pkg_confirmed[pat.package].append(pid)

    for pkg, pids in pkg_confirmed.items():
        if len(pids) < 2:
            continue
        # Check for guidance conflicts (different guidance on same package — conservative)
        guidances = {pid: patterns[pid].guidance for pid in pids}
        # We flag all pairs with diverging guidance (non-identical normalized text)
        seen: set[str] = set()
        for pid_a in pids:
            for pid_b in pids:
                if pid_a >= pid_b:
                    continue
                pair = frozenset({pid_a, pid_b})
                pair_key = "|".join(sorted(pair))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                if _normalized(guidances[pid_a]) != _normalized(guidances[pid_b]):
                    for demote_id in (pid_a, pid_b):
                        p = patterns[demote_id]
                        if p.confidence == "confirmed":
                            p.confidence = "tentative"  # type: ignore[assignment]
                            p.last_review = date.today().isoformat()
                            store.save(p)
                            log.append(f"demoted {demote_id}: conflicting confirmed guidance with {pid_a if demote_id == pid_b else pid_b}")
                    _write_conflict_note(store, pid_a, pid_b)

    # Rule 3: archive stale contradicted patterns
    cutoff = date.today() - timedelta(days=_ARCHIVE_AFTER_DAYS)
    patterns = store.load_all()
    for pid, pat in patterns.items():
        if pat.confidence != "contradicted":
            continue
        review_date = _parse_date(pat.last_review or pat.created)
        if review_date and review_date < cutoff:
            index.remove(pid)
            log.append(f"archived {pid}: contradicted and unchanged for >{_ARCHIVE_AFTER_DAYS} days")

    return log


def _normalized(text: str) -> str:
    return " ".join(text.lower().split())


def _parse_date(s: str) -> date | None:
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def _write_conflict_note(store: "PatternStore", pid_a: str, pid_b: str) -> None:
    from .pattern import Pattern
    from datetime import date as _date
    note_id = f"conflict_{pid_a}_vs_{pid_b}"
    note = Pattern(
        id=note_id,
        package="",
        confidence="tentative",
        seed=False,
        guidance=(
            f"Conflict detected between `{pid_a}` and `{pid_b}`. "
            "Both have been demoted to tentative. Human review required."
        ),
        created=_date.today().isoformat(),
        last_review=_date.today().isoformat(),
    )
    store.save(note)
