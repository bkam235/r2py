"""Stage 2 — shared translation infrastructure (LLM client, stitching helpers, walker).

Whole-file translation lives in ``r2py/seed.py``; this package holds the
pieces it (and the reasoning agent) share: the LLM client (``llm.py``), the
data-shim / sentinel utilities (``stitch.py``), and the entity dependency
walker (``walker.py``).
"""
from __future__ import annotations
