"""Comparator protocol and shared helpers (§7.3)."""
from __future__ import annotations

import os
import re as _re
from difflib import SequenceMatcher
from typing import Protocol

from ...types import ComparatorResult, EffectClass


class Comparator(Protocol):
    effect_class: EffectClass

    def compare(self, r_effect: object, py_effect: object) -> ComparatorResult: ...


# Module-level singleton for the embedding model (loaded lazily).
_embed_model = None


def _get_embed_model():
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer  # type: ignore
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embed_model


def _difflib_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _normalize_printed_output(s: str) -> str:
    """Strip R/Python print-format decoration to bare whitespace-separated tokens.

    Handles:
    - R vector indices: ``[1]``, ``[7]``, etc. at line start
    - Surrounding quotes (both ``"`` and ``'``)
    - Python list/tuple brackets and commas
    """
    # Remove R vector line-index markers like "[1]" or " [7]"
    s = _re.sub(r'^\s*\[\d+\]\s*', '', s, flags=_re.MULTILINE)
    # Strip quote characters and list punctuation
    s = s.translate(str.maketrans('', '', '"\'[](),'))
    return ' '.join(s.split())


def _embedding_similarity(a: str, b: str) -> float:
    """Cosine similarity via sentence-transformers (falls back to difflib on error)."""
    try:
        from sentence_transformers import util  # type: ignore
        model = _get_embed_model()
        vecs = model.encode([a, b], convert_to_tensor=True)
        return float(util.cos_sim(vecs[0], vecs[1]))
    except Exception:
        return _difflib_similarity(a, b)


def text_similarity(a: str, b: str) -> float:
    """Return a [0, 1] similarity score for two strings.

    Default: difflib.SequenceMatcher (stdlib, no ML deps).
    Set R2PY_EMBED=1 to use sentence-transformers cosine similarity instead
    (requires ``pip install r2py[embed]``).

    Always takes the max of raw and normalised similarity so that R auto-print
    format (``[1] "January" ...``) and Python list repr (``['January', ...]``)
    score as equivalent when they contain the same tokens.
    """
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    if os.getenv("R2PY_EMBED"):
        return _embedding_similarity(a, b)
    raw = _difflib_similarity(a, b)
    norm = _difflib_similarity(_normalize_printed_output(a), _normalize_printed_output(b))
    return max(raw, norm)
