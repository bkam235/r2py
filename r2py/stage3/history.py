"""Per-script edit history for Stage 3 (§8.4).

Tracks which edits have been tried in the current translation loop so the
policy can exclude them from future proposals.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..types import Edit


def _edit_key(edit: Edit) -> tuple:
    """Normalised key for edit equality: (kind, sorted entity_ids, frozen params).

    pattern_id is deliberately excluded — the same mechanical edit attributed to
    a different pattern is still the same translation-state transition.
    """
    params_frozen = tuple(sorted((k, str(v)) for k, v in edit.params.items()))
    return (edit.kind, tuple(sorted(edit.entity_ids)), params_frozen)


@dataclass
class EditHistory:
    tried: list[Edit] = field(default_factory=list)
    # Counts ties + regressions per entity (not accepted edits).
    # Used for both the 3-attempt cap and the position-based rank adjustment in
    # _weak_first so that entities that repeatedly fail to improve are deprioritised.
    _rejected: dict[str, int] = field(default_factory=dict, init=False, repr=False)
    _rejection_notes: dict[tuple, str] = field(default_factory=dict, init=False, repr=False)

    def add(self, edit: Edit) -> None:
        """Record a tried edit."""
        self.tried.append(edit)

    def record_rejection(self, entity_id: str) -> None:
        """Increment the tie/regression count for entity_id.

        Called by the loop after a tie or regression is confirmed so that
        count_for_entity reflects only non-improving attempts.
        """
        self._rejected[entity_id] = self._rejected.get(entity_id, 0) + 1

    def record_rejection_note(self, edit: Edit, note: str) -> None:
        self._rejection_notes[_edit_key(edit)] = note

    def get_rejection_note(self, edit: Edit) -> str:
        return self._rejection_notes.get(_edit_key(edit), "")

    def was_tried(self, edit: Edit) -> bool:
        """True if an equivalent edit (same kind + entity_ids + params) was already tried."""
        key = _edit_key(edit)
        return any(_edit_key(e) == key for e in self.tried)

    def count_for_entity(self, entity_id: str) -> int:
        """Count tie/regression edits for this entity (used for the 3-attempt cap).

        Accepted edits are excluded — an entity that improved once should not
        be penalised when the loop revisits it to improve it further.
        """
        return self._rejected.get(entity_id, 0)

    def copy_to(self, other: "EditHistory") -> None:
        """Copy rejection notes to another history (used when inheriting history)."""
        other._rejection_notes.update(self._rejection_notes)

    def clear(self) -> None:
        """Reset for a new translation script."""
        self.tried.clear()
        self._rejected.clear()
        self._rejection_notes.clear()
