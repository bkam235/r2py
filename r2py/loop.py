"""Beam/strict-improvement translation loop (§4.1).

W=1 reduces to strict hill-climbing. W>1 holds a population of candidates and
accepts only strict improvements, preventing neutral drift and cycling.
"""
from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from .types import Candidate, Proposal, TranslateResult

if TYPE_CHECKING:
    from .types import ScriptMap


def _state_hash(translation: str) -> str:
    """SHA-256 of the Python source text — tabu key for the visited set."""
    return hashlib.sha256(translation.encode()).hexdigest()


def _top_k(candidates: list[Candidate], k: int) -> list[Candidate]:
    """Return the k highest-scoring candidates.

    sorted() is stable, so incumbents (appearing earlier in the input list)
    beat survivors at equal scores — implements 'prefer_incumbent_on_tie'.
    """
    return sorted(candidates, key=lambda c: c.score, reverse=True)[:k]


def run_loop(
    script_map: "ScriptMap",
    library,
    *,
    max_iters: int = 8,
    score_threshold: float = 0.85,
    beam_width: int = 4,
    use_judge: bool = False,
    data_compare: str = "auto",
    no_seeds: bool = False,
    **verify_kwargs,
) -> TranslateResult:
    """Run the beam/strict-improvement loop (§4.1).

    Args:
        script_map: Stage 1 ScriptMap for the R source.
        library: PatternLibrary (read by Stage 2, written on evidence/contradiction).
        max_iters: Maximum number of edit iterations.
        score_threshold: Stop early when best beam score reaches this value.
        beam_width: Number of candidates to keep in the beam (W=1 = hill-climbing).
        use_judge: Enable LLM judge fallback (D4, off by default).
        data_compare: "auto" | "exact" | "embedding" (§7.3.1).
        no_seeds: Ignore seed:true patterns (§6.7 transfer experiment).
        **verify_kwargs: Forwarded to stage4.verify() (e.g. rtol, atol, timeout_s).
    """
    from . import stage2, stage3, stage4
    from .stage3.history import EditHistory
    from .library.epistemology import review as _ep_review

    script_id = hashlib.sha1(script_map.source.encode()).hexdigest()[:12]

    # --- seed translation -------------------------------------------------- #
    seed = stage2.translate(script_map, library, no_seeds=no_seeds)
    seed_decomp = stage4.verify(
        script_map, seed,
        data_compare=data_compare, use_judge=use_judge,
        **verify_kwargs,
    )

    beam: list[Candidate] = [Candidate(seed, seed_decomp.aggregate, seed_decomp)]
    visited: set[str] = {_state_hash(seed)}
    score_history = [seed_decomp]
    evidence_added: list[str] = []
    contradictions_added: list[str] = []
    # Per-parent edit histories keyed by state hash so beam members A and B
    # can independently propose the same edit kind (applying it to their
    # different translations produces different states; the tabu set catches
    # actual duplicates).
    histories: dict[str, EditHistory] = {}

    i = 0
    for i in range(max_iters):
        best = max(beam, key=lambda c: c.score)
        if best.score >= score_threshold:
            break

        proposals: list[Proposal] = []

        for parent in beam:
            parent_history = histories.setdefault(
                _state_hash(parent.translation), EditHistory()
            )
            try:
                edit = stage3.propose_edit(
                    parent, library,
                    script_map=script_map,
                    history=parent_history,
                    iteration=i,
                )
            except RuntimeError:
                continue  # all entities exhausted for this parent

            # Record before the tabu check so Stage 3 won't re-propose an edit
            # that leads to an already-visited state.
            parent_history.add(edit)

            candidate_src = stage3.apply_edit(parent.translation, edit)
            h = _state_hash(candidate_src)
            if h in visited:
                continue
            visited.add(h)

            new_decomp = stage4.verify(
                script_map, candidate_src,
                changed=edit.entity_ids,
                data_compare=data_compare,
                use_judge=use_judge,
                **verify_kwargs,
            )
            proposals.append(
                Proposal(candidate_src, new_decomp.aggregate, new_decomp, edit, parent.score)
            )

        if not proposals:
            break

        score_history.extend(p.new_decomp for p in proposals)

        for p in proposals:
            if p.new_score > p.parent_score:
                library.record_evidence(
                    p.edit,
                    score_delta=p.new_score - p.parent_score,
                    script_id=script_id,
                )
                if p.edit.pattern_id:
                    evidence_added.append(p.edit.pattern_id)
            elif p.new_score == p.parent_score:
                library.record_tie(p.edit, script_id=script_id)
            else:
                library.record_contradiction(
                    p.edit, observed=p.new_score, script_id=script_id,
                )
                if p.edit.pattern_id:
                    contradictions_added.append(p.edit.pattern_id)

        beam_min = min(c.score for c in beam)
        survivors = [
            Candidate(p.candidate, p.new_score, p.new_decomp)
            for p in proposals
            if p.new_score > beam_min
        ]
        beam = _top_k(beam + survivors, beam_width)

    # Epistemology review only when the library was actually mutated — avoids
    # unnecessary I/O on no-op runs and aligns with the "every N" intent (§7.7).
    if evidence_added or contradictions_added:
        try:
            _ep_review(library.store, library.index)
        except Exception:
            pass

    best = max(beam, key=lambda c: c.score)
    return TranslateResult(
        python_source=best.translation,
        final_score=best.score,
        iterations=i + 1,
        score_history=score_history,
        pattern_evidence_added=list(dict.fromkeys(evidence_added)),
        pattern_contradictions_added=list(dict.fromkeys(contradictions_added)),
    )
