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
        self._docs_count = 0
        self._docs_cache: dict[str, str] = {}
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

    def lookup_docs(self, package: str, topic: str, language: str = "python") -> str:
        """Look up offline documentation for a package symbol.

        language: "python" or "r"
        package: dotted module path for Python (e.g. "shiny.ui") or package name for R
        topic:   function/class name; empty string → list the module's public API
        """
        cache_key = f"{language.lower()}:{package}:{topic}"
        if cache_key in self._docs_cache:
            return self._docs_cache[cache_key]
        if self._docs_count >= 5:
            return "(docs lookup limit reached)"
        self._docs_count += 1
        if language.lower() == "r":
            result = self._lookup_r_docs(package, topic)
        else:
            result = self._lookup_python_docs(package, topic)
        self._docs_cache[cache_key] = result
        return result

    def _lookup_python_docs(self, package: str, topic: str) -> str:
        import subprocess
        import sys

        def _pydoc(q: str) -> str:
            r = subprocess.run(
                [sys.executable, "-m", "pydoc", q],
                capture_output=True, text=True, timeout=15,
            )
            return (r.stdout or r.stderr or "(no output)").strip()

        query = f"{package}.{topic}".rstrip(".") if topic else package
        out = _pydoc(query)

        # When the exact query isn't found, probe the parent module so the model
        # gets actionable context (e.g. bslib.popover fails → show bslib or shiny.ui).
        if "no python documentation found" in out.lower() and "." in query:
            parent = query.rsplit(".", 1)[0]
            parent_out = _pydoc(parent)
            if "no python documentation found" in parent_out.lower():
                out += (
                    f"\nPackage '{parent}' is also not installed in this Python "
                    "environment. If this is an R package name, look for its Python "
                    "equivalent — e.g. R's bslib → Python's shiny.ui; "
                    "R's shiny → Python's shiny."
                )
            else:
                out += f"\n\n--- '{parent}' is installed. Partial listing: ---\n{parent_out[:800]}"

        return out[:3000]

    def _lookup_r_docs(self, package: str, topic: str) -> str:
        if topic:
            expr = (
                f'suppressPackageStartupMessages(library({package}))\n'
                f'tryCatch(\n'
                f'  paste(capture.output('
                f'tools::Rd2txt(utils::help("{topic}", package="{package}")'
                f')), collapse="\\n"),\n'
                f'  error=function(e) paste("Error:", conditionMessage(e))\n'
                f')'
            )
        else:
            expr = (
                f'suppressPackageStartupMessages(library({package}))\n'
                f'cat(paste(sort(getNamespaceExports("{package}")), collapse=", "))\n'
            )
        import tempfile
        from ..stage0.sandbox.r_sandbox import RSandbox
        from ..types import EffectClass
        sandbox = RSandbox()
        with tempfile.TemporaryDirectory() as tmpdir:
            bundle = sandbox.run(
                expr,
                workdir=Path(tmpdir),
                capture=frozenset({EffectClass.STDOUT}),
                timeout_s=min(self._timeout_s, 20),
            )
        return (bundle.stdout or "(no output)").strip()[:3000]

    def lookup_patterns(self, entity_id: str, k: int = 3) -> list["Pattern"]:
        """Query pattern library for the given entity."""
        entity = self._script_map.entities.get(entity_id)
        if entity is None:
            return []
        return self._library.retrieve(entity, k=k)

