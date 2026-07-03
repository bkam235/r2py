"""Harness tool interface for the reasoning loop.

These are Python functions (not LLM tool-use) that the orchestrator calls
based on model decisions. They wrap Stage 4 verification, R sandbox probing,
pattern library queries, and entity information retrieval.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..library import PatternLibrary
    from ..library.pattern import Pattern
    from ..stage1.script_map import ScriptMap
    from ..types import ScoreReport


class HarnessTools:
    """Stateful tool bag bound to a specific translation context."""

    def __init__(
        self,
        script_map: "ScriptMap",
        library: "PatternLibrary",
        *,
        model: str = "",
        data_compare: str = "auto",
        timeout_s: float = 60,
        sidecar_filename: str = "",
        verify_kwargs: dict | None = None,
    ):
        self._script_map = script_map
        self._library = library
        self._model = model
        self._data_compare = data_compare
        self._timeout_s = timeout_s
        self._sidecar_filename = sidecar_filename
        self._verify_kwargs = verify_kwargs or {}
        self._probe_count = 0
        self._probe_history: list[tuple[str, str]] = []
        self.last_annotated_source: str = ""

    def verify(self, python_source: str) -> "ScoreReport":
        """Run Stage 4 verification, return full ScoreReport with comparisons."""
        from ..stage2.sentinel_mapper import (
            map_entities_to_lines, strip_sentinels, insert_sentinels,
            flatten_entity_line_map,
        )
        from ..stage4 import verifier

        clean = strip_sentinels(python_source)
        entity_ranges = map_entities_to_lines(
            self._script_map, clean, model=self._model,
        )
        self.last_annotated_source = insert_sentinels(clean, entity_ranges)
        entity_line_map = flatten_entity_line_map(entity_ranges)
        kw = {k: v for k, v in self._verify_kwargs.items()
              if k not in ("data_compare", "entity_line_map",
                           "sidecar_filename", "timeout_s")}
        return verifier.verify(
            self._script_map,
            clean,
            data_compare=self._data_compare,
            entity_line_map=entity_line_map,
            sidecar_filename=self._sidecar_filename,
            timeout_s=self._timeout_s,
            **kw,
        )

    def probe_r(self, r_expression: str) -> str:
        """Run an R expression in sandbox and return its stdout.

        Bounded to prevent runaway costs: max 10 probes per HarnessTools instance.
        """
        if self._probe_count >= 10:
            return "(probe limit reached)"
        self._probe_count += 1

        import tempfile
        from ..stage0.sandbox.r_sandbox import RSandbox
        from ..types import EffectClass

        sandbox = RSandbox()
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle = sandbox.run(
                r_expression,
                workdir=Path(tmpdir),
                capture=frozenset({EffectClass.STDOUT}),
                timeout_s=min(self._timeout_s, 15),
            )
        result = (bundle.stdout or "").strip()
        self._probe_history.append((r_expression, result))
        return result

    def lookup_patterns(self, entity_id: str, k: int = 3) -> list["Pattern"]:
        """Query pattern library for the given entity."""
        entity = self._script_map.entities.get(entity_id)
        if entity is None:
            return []
        return self._library.retrieve(entity, k=k)

