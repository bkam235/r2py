"""Offline retrieval reranker trainer — §12.6 A.

Consumes logged outcomes from work/outputs/*/edits.log.jsonl + library_diff.json,
trains a LightGBM lambdarank model, and writes a versioned artifact to
work/models/reranker/ only on a held-out win against the heuristic baseline.

CLI: r2py library train-reranker
Not yet implemented. See architecture.md §12.6 A.
"""
raise NotImplementedError
