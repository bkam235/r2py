"""AST node coverage tracking for Stage 1."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

CoverageStatus = Literal["analyzed", "dynamic", "branch-extracted", "unreachable"]

_STATUS_ORDER = ("analyzed", "dynamic", "branch-extracted", "unreachable")
_ANALYZED_STATUSES = frozenset({"analyzed", "dynamic", "branch-extracted"})


@dataclass
class CoverageReport:
    total_nodes: int
    by_status: dict[str, int] = field(default_factory=dict)
    fraction_analyzed: float = 0.0


class CoverageTracker:
    def __init__(self) -> None:
        self._status: dict[str, CoverageStatus] = {}

    def register(self, node_id: str) -> None:
        """Register a node as known but not yet analyzed."""
        if node_id not in self._status:
            self._status[node_id] = "unreachable"

    def mark(self, node_id: str, status: CoverageStatus) -> None:
        """Mark a node with a coverage status. Only upgrades (never downgrades)."""
        current = self._status.get(node_id, "unreachable")
        # upgrade priority: analyzed > dynamic > branch-extracted > unreachable
        if _STATUS_ORDER.index(status) < _STATUS_ORDER.index(current):
            self._status[node_id] = status

    def report(self) -> CoverageReport:
        total = len(self._status)
        by_status: dict[str, int] = {s: 0 for s in _STATUS_ORDER}
        for s in self._status.values():
            by_status[s] += 1
        analyzed_count = sum(by_status[s] for s in _ANALYZED_STATUSES)
        fraction = analyzed_count / total if total > 0 else 1.0
        return CoverageReport(
            total_nodes=total,
            by_status=by_status,
            fraction_analyzed=fraction,
        )

    def reachable_uncovered(self) -> list[str]:
        """Return node_ids still marked 'unreachable' (not yet analyzed)."""
        return [nid for nid, s in self._status.items() if s == "unreachable"]
