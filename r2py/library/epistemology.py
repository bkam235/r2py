"""Confidence transitions and archival rules for the Pattern Library (§6.5)."""
from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .store import PatternStore
    from .index import PatternIndex

_ARCHIVE_AFTER_RUNS = 30
# Patterns with no real improvement evidence are archived after this many
# non-improvement interactions (ties + contradictions combined).
_NO_IMPROVEMENT_RUN_THRESHOLD = 100
_DEMOTION_MAP = {"confirmed": "tentative", "tentative": "contradicted"}


def review(store: "PatternStore", index: "PatternIndex") -> list[str]:
    """Apply all §6.5 confidence rules.  Returns a list of human-readable log lines."""
    patterns = store.load_all()
    log: list[str] = []

    # Rule 0: promote tentative → confirmed (§6.5, amended).
    # Original rule required ≥2 *distinct* script IDs.  Amended: requires ≥2
    # genuine improvement evidence entries regardless of script identity.
    # Rationale: the distinct-script requirement prevented promotion entirely when
    # the corpus is a single script or a small fixed set — the system could never
    # learn regardless of how many confirmed runs accumulated (see architecture.md
    # §6.5 departure note).
    for pid, pat in list(patterns.items()):
        if pat.confidence != "tentative":
            continue
        real_evidence = [e for e in pat.evidence if e.score > 0.0]
        if len(real_evidence) >= 2:
            pat.confidence = "confirmed"
            pat.last_review = date.today().isoformat()
            store.save(pat)
            index.upsert_meta(
                pattern_id=pid,
                package=pat.package,
                confidence="confirmed",
                evidence_count=len(pat.evidence),
                contradictions_count=len(pat.contradictions),
                seed=pat.seed,
                ast_shape_hash=index.get_meta(pid).get("ast_shape_hash", ""),
            )
            log.append(
                f"promoted {pid}: {len(real_evidence)} genuine improvement entries"
            )

    # Reload after mutations
    patterns = store.load_all()

    # Rule 1: contradiction-threshold demotion
    for pid, pat in list(patterns.items()):
        if pat.confidence == "contradicted":
            continue
        threshold = pat.demotion_threshold()
        if len(pat.contradictions) >= threshold:
            new_conf = _DEMOTION_MAP[pat.confidence]
            pat.confidence = new_conf  # type: ignore[assignment]
            pat.last_review = date.today().isoformat()
            store.save(pat)
            log.append(
                f"demoted {pid}: contradictions({len(pat.contradictions)})"
                f" >= threshold({threshold}) → {new_conf}"
            )

    # Reload after mutations
    patterns = store.load_all()

    # Rule 2: conflict detection — two `confirmed` patterns with the same
    # (package, ast_shape_hash) and differing guidance.
    # Only fires when ast_shape_hash is non-empty: patterns indexed under the
    # wildcard ("") bucket cannot be compared for specificity, so we skip them
    # to avoid false-positive demotions between patterns covering different
    # R constructs in the same package.
    pkg_shape_confirmed: dict[tuple[str, str], list[str]] = defaultdict(list)
    for pid, pat in patterns.items():
        if pat.confidence == "confirmed":
            meta = index.get_meta(pid)
            shape = meta.get("ast_shape_hash", "")
            if shape:  # only group patterns with a real shape hash
                pkg_shape_confirmed[(pat.package, shape)].append(pid)

    for (pkg, shape), pids in pkg_shape_confirmed.items():
        if len(pids) < 2:
            continue
        guidances = {pid: patterns[pid].guidance for pid in pids}
        for pid_a in pids:
            for pid_b in pids:
                if pid_a >= pid_b:
                    continue
                if _normalized(guidances[pid_a]) == _normalized(guidances[pid_b]):
                    continue
                for demote_id in (pid_a, pid_b):
                    p = patterns[demote_id]
                    if p.confidence == "confirmed":
                        p.confidence = "tentative"  # type: ignore[assignment]
                        p.last_review = date.today().isoformat()
                        store.save(p)
                        other = pid_a if demote_id == pid_b else pid_b
                        log.append(
                            f"demoted {demote_id}: conflicting confirmed"
                            f" guidance with {other}"
                        )
                _write_conflict_note(store, pid_a, pid_b)

    # Rule 3: archive contradicted patterns after enough translation runs.
    current_run = index.total_runs()
    patterns = store.load_all()
    for pid, pat in patterns.items():
        if pat.confidence != "contradicted":
            continue
        meta = index.get_meta(pid)
        contradicted_at = meta.get("contradicted_at_run", 0)
        if current_run - contradicted_at >= _ARCHIVE_AFTER_RUNS:
            index.remove(pid)
            log.append(
                f"archived {pid}: contradicted for"
                f" {current_run - contradicted_at} runs (>{_ARCHIVE_AFTER_RUNS})"
            )

    # Rule 4: archive patterns tried many times without any improvement.
    # Seeds are always kept.
    patterns = store.load_all()
    for pid, pat in patterns.items():
        if pat.confidence == "contradicted" or pat.seed:
            continue
        real_evidence = [e for e in pat.evidence if e.score > 0.0]
        if real_evidence:
            continue  # has at least one genuine improvement — keep
        non_improvements = pat.tie_count + len(pat.contradictions)
        if non_improvements >= _NO_IMPROVEMENT_RUN_THRESHOLD:
            index.remove(pid)
            log.append(
                f"archived {pid}: {non_improvements} non-improvement runs, no improvement"
            )

    return log


def prune_unimproved(store: "PatternStore", index: "PatternIndex") -> list[str]:
    """Immediately archive ALL non-seed patterns with zero genuine improvement evidence.

    One-time cleanup of patterns accumulated before the tie-counting and
    guidance-requirement fixes. Preserves seed patterns and any pattern that
    has at least one evidence entry with score > 0.
    """
    patterns = store.load_all()
    log: list[str] = []
    indexed = set(index.all_ids())
    for pid, pat in patterns.items():
        if pid not in indexed:
            continue
        if pat.confidence == "contradicted" or pat.seed:
            continue
        real_evidence = [e for e in pat.evidence if e.score > 0.0]
        if real_evidence:
            continue
        index.remove(pid)
        log.append(f"pruned {pid}: no improvement evidence")
    return log


def _normalized(text: str) -> str:
    return " ".join(text.lower().split())


def _write_conflict_note(store: "PatternStore", pid_a: str, pid_b: str) -> None:
    from .pattern import Pattern
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
        created=date.today().isoformat(),
        last_review=date.today().isoformat(),
    )
    store.save(note)
