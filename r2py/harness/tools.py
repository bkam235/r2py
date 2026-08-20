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
        self._r_packages = _collect_r_packages(script_map)

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

        r_pkg_warning = ""
        top_level = package.split(".")[0]
        if top_level in self._r_packages:
            r_pkg_warning = (
                f"CAUTION: '{top_level}' is also an R package used in this "
                f"script. The Python package shown below may be completely "
                f"unrelated (e.g. R's 'bit' is boolean indexing, Python's "
                f"'bit' is a Bitcoin library). Verify that the API below "
                f"actually matches the R functionality before using it. "
                f"If unrelated, implement the R behavior with standard "
                f"Python or well-known libraries (numpy, pandas, etc.).\n\n"
            )

        def _pydoc(q: str) -> str:
            r = subprocess.run(
                [sys.executable, "-m", "pydoc", q],
                capture_output=True, text=True, timeout=15,
            )
            return (r.stdout or r.stderr or "(no output)").strip()

        def _overview(mod: str) -> str:
            """Compact listing: public names with brief signatures."""
            code = (
                "import importlib, inspect\n"
                f"_m = importlib.import_module({mod!r})\n"
                "_ns = sorted(getattr(_m, '__all__', None) or "
                "[n for n in dir(_m) if not n.startswith('_')])\n"
                "for _n in _ns:\n"
                "    _o = getattr(_m, _n, None)\n"
                "    try: print(_n + str(inspect.signature(_o))[:60])\n"
                "    except: print(_n)\n"
            )
            r = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True, timeout=10,
            )
            return r.stdout.strip() if r.returncode == 0 else ""

        # Always fetch the module overview — the model needs to know what's
        # available in the module, not just whether a specific name exists.
        overview = _overview(package)
        if not overview:
            # Package exists but exports nothing via __all__ / dir — fall back
            # to pydoc (e.g. Python's bslib is a battery-storage stub).
            pkg_pydoc = _pydoc(package)
            if "no python documentation found" not in pkg_pydoc.lower():
                overview = pkg_pydoc[:800]
        overview_block = (
            f"## {package} — available names:\n{overview[:1500]}" if overview else ""
        )

        if not topic:
            result = (overview_block or _pydoc(package))[:3000]
            return r_pkg_warning + result if r_pkg_warning else result

        # Specific function/class docs.
        specific = _pydoc(f"{package}.{topic}")
        if "no python documentation found" in specific.lower():
            if overview_block:
                specific = f"'{topic}' is not in '{package}'."
            else:
                specific += (
                    f"\n\nNote: '{package}' is not installed in this Python "
                    "environment. If this is an R package name, look for its "
                    "Python equivalent (e.g. R's bslib → shiny.ui)."
                )

        parts = [p for p in [overview_block, specific[:1500]] if p]
        result = "\n\n".join(parts)[:3000]
        return r_pkg_warning + result if r_pkg_warning else result

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


def _collect_r_packages(script_map: "ScriptMap") -> set[str]:
    """Return the set of R package names used by this script."""
    entities = getattr(script_map, "entities", {}) or {}
    pkgs = {
        getattr(e, "package", "")
        for e in entities.values()
        if getattr(e, "package", "")
    }
    pkgs.discard("")
    pkgs.discard("base")
    return pkgs

