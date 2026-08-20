"""Topological ordering of ScriptMap entities for Stage 2 translation (§5.3)."""
from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stage1.entities import Entity
    from ..types import EntityId


def topological_order(entities: dict[str, "Entity"]) -> list[str]:
    """Return entity IDs in dependency-first (topological) order.

    Uses Kahn's algorithm. On a cycle, appends the remaining cycle members in
    their insertion order (graceful fallback; cycles are rare in R top-level
    scripts where most assignments are to independent names).
    """
    if not entities:
        return []

    # Build adjacency: dep_id → set of entity_ids that depend on it.
    in_degree: dict[str, int] = {eid: 0 for eid in entities}
    dependents: dict[str, list[str]] = {eid: [] for eid in entities}

    for eid, entity in entities.items():
        seen_deps: set[str] = set()
        for ref in entity.dependencies:
            dep_id = ref.entity_id
            if dep_id in entities and dep_id != eid and dep_id not in seen_deps:
                in_degree[eid] += 1
                dependents[dep_id].append(eid)
                seen_deps.add(dep_id)

    # Kahn's BFS: start with all nodes that have no unresolved dependencies.
    queue: deque[str] = deque(
        eid for eid in entities if in_degree[eid] == 0
    )
    order: list[str] = []

    while queue:
        eid = queue.popleft()
        order.append(eid)
        for dependent in dependents[eid]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Cycle fallback: append remaining nodes in insertion order.
    if len(order) < len(entities):
        remaining = [eid for eid in entities if eid not in set(order)]
        order.extend(remaining)

    return order
