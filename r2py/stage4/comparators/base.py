"""Comparator protocol and shared helpers (§7.3)."""
from __future__ import annotations

from difflib import SequenceMatcher
from typing import Protocol

from ...types import ComparatorResult, EffectClass


class Comparator(Protocol):
    effect_class: EffectClass

    def compare(self, r_effect: object, py_effect: object) -> ComparatorResult: ...


def text_similarity(a: str, b: str) -> float:
    """Return a [0, 1] similarity score for two strings.

    Uses difflib.SequenceMatcher — stdlib, no ML deps, injection point for a
    real cosine-over-embedding later at the same call site.
    """
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()
