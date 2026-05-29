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

    def add(self, edit: Edit) -> None:
        """Record a tried edit."""
        self.tried.append(edit)

    def was_tried(self, edit: Edit) -> bool:
        """True if an equivalent edit (same kind + entity_ids + params) was already tried."""
        key = _edit_key(edit)
        return any(_edit_key(e) == key for e in self.tried)

    def clear(self) -> None:
        """Reset for a new translation script."""
        self.tried.clear()
