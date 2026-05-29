"""Edit attribution validation for Stage 3 (§8.5).

Every proposed edit must be attributed to a pattern (existing ID or new slug)
before it can be returned. Edits without attribution are rejected.
"""
from __future__ import annotations

from ..types import Edit


class AttributionError(ValueError):
    """Raised when a proposed edit has no pattern attribution (§8.5)."""


def attribute(edit: Edit, proposed_pattern_id: str | None) -> Edit:
    """Return a copy of edit with pattern_id set and validated.

    In exploit mode, pass the retrieved pattern's .id as proposed_pattern_id.
    In explore mode, pass whatever slug the LLM put in the pattern_id field.
    Raises AttributionError if proposed_pattern_id is None or empty.
    """
    if not proposed_pattern_id or not proposed_pattern_id.strip():
        raise AttributionError(
            f"Edit of kind {edit.kind.value} has no pattern attribution. "
            "Every edit must reference an existing pattern ID or propose a new slug (§8.5)."
        )
    return Edit(
        kind=edit.kind,
        entity_ids=list(edit.entity_ids),
        params=dict(edit.params),
        pattern_id=proposed_pattern_id.strip(),
    )
