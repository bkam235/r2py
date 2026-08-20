"""JSON index for fast Pattern Library retrieval (§6.6)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from ..types import PatternId

if TYPE_CHECKING:
    from .store import PatternStore


class PatternIndex:
    """
    Backed by library_dir/index.json.

    Structure::

        {
          "by_key": {
            "<package>:<ast_shape_hash>": ["pattern_id", ...]
          },
          "meta": {
            "<pattern_id>": {
              "confidence": "...",
              "evidence_count": N,
              "contradictions_count": N,
              "seed": bool,
              "package": "...",
              "ast_shape_hash": "..."
            }
          }
        }
    """

    def __init__(self, library_dir: Path) -> None:
        self._path = library_dir / "index.json"
        self._data: dict = {"by_key": {}, "meta": {}, "total_runs": 0}
        if self._path.exists():
            self._load()

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def total_runs(self) -> int:
        return int(self._data.get("total_runs", 0))

    def increment_runs(self) -> int:
        """Increment the global translation run counter and return the new value."""
        n = self.total_runs() + 1
        self._data["total_runs"] = n
        self._save()
        return n

    def rebuild(self, store: "PatternStore") -> None:
        """Regenerate the index from all patterns in the store.

        Each pattern is indexed under the wildcard key ``(package, "")``.
        Exact-shape keys (``(package, ast_shape_hash)``) are only populated
        via ``upsert_meta`` once a real shape hash is known (Stage 2 supplies
        this at retrieval time).  Populating exact-shape keys during rebuild
        would require guessing the hash from pattern metadata, which is not
        available here.
        """
        by_key: dict[str, list[PatternId]] = {}
        meta: dict[PatternId, dict] = {}

        for pid, pat in store.load_all().items():
            pkg_key = _make_key(pat.package, "")
            by_key.setdefault(pkg_key, [])
            if pid not in by_key[pkg_key]:
                by_key[pkg_key].append(pid)

            meta[pid] = {
                "confidence": pat.confidence,
                "evidence_count": len(pat.evidence),
                "contradictions_count": len(pat.contradictions),
                "seed": pat.seed,
                "package": pat.package,
                "ast_shape_hash": "",
            }

        self._data = {"by_key": by_key, "meta": meta}
        self._save()

    def lookup(self, package: str, ast_shape_hash: str = "") -> list[PatternId]:
        """Return pattern IDs matching (package, ast_shape_hash).

        Tries exact key first, then falls back to package wildcard (empty hash).
        """
        exact = self._data["by_key"].get(_make_key(package, ast_shape_hash), [])
        if exact:
            return list(exact)
        return list(self._data["by_key"].get(_make_key(package, ""), []))

    def get_meta(self, pattern_id: PatternId) -> dict:
        return dict(self._data["meta"].get(pattern_id, {}))

    def all_ids(self) -> list[PatternId]:
        return list(self._data["meta"].keys())

    def upsert_meta(self, pattern_id: PatternId, package: str, confidence: str,
                    evidence_count: int, contradictions_count: int, seed: bool,
                    ast_shape_hash: str = "",
                    contradicted_at_run: int | None = None) -> None:
        """Update metadata for a single pattern without a full rebuild."""
        existing = self._data["meta"].get(pattern_id, {})
        entry: dict = {
            "confidence": confidence,
            "evidence_count": evidence_count,
            "contradictions_count": contradictions_count,
            "seed": seed,
            "package": package,
            "ast_shape_hash": ast_shape_hash,
            "contradicted_at_run": existing.get("contradicted_at_run", 0),
        }
        if contradicted_at_run is not None:
            entry["contradicted_at_run"] = contradicted_at_run
        self._data["meta"][pattern_id] = entry
        key = _make_key(package, ast_shape_hash)
        ids = self._data["by_key"].setdefault(key, [])
        if pattern_id not in ids:
            ids.append(pattern_id)
        pkg_key = _make_key(package, "")
        pkg_ids = self._data["by_key"].setdefault(pkg_key, [])
        if pattern_id not in pkg_ids:
            pkg_ids.append(pattern_id)
        self._save()

    def remove(self, pattern_id: PatternId) -> None:
        """Remove a pattern from the index (used by archival)."""
        self._data["meta"].pop(pattern_id, None)
        for ids in self._data["by_key"].values():
            if pattern_id in ids:
                ids.remove(pattern_id)
        self._save()

    # ------------------------------------------------------------------ #
    # Private                                                              #
    # ------------------------------------------------------------------ #

    def _load(self) -> None:
        self._data = json.loads(self._path.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self._path.write_text(
            json.dumps(self._data, indent=2), encoding="utf-8"
        )


def _make_key(package: str, ast_shape_hash: str) -> str:
    return f"{package}:{ast_shape_hash}"
