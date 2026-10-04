"""Harness tool interface for the reasoning loop.

These are Python functions (not LLM tool-use) that the orchestrator calls
based on model decisions. They wrap Stage 4 verification, R sandbox probing,
pattern library queries, and entity information retrieval.
"""
from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..library import PatternLibrary
    from ..library.pattern import Pattern
    from ..stage1.script_map import ScriptMap
    from ..types import ScoreReport


# Verification cache outcomes (hit / miss), per process; drained into each run's row.
cache_stats: Counter = Counter()

MAPPING_TRIES = 3  # a failed mapping is resampled before falling back to aggregate-only scoring


def drain_cache_stats() -> dict:
    out = dict(cache_stats)
    cache_stats.clear()
    return out


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
        # (source hash) -> (report, annotated source): the same source is verified once per run.
        # The agent resubmits identical candidates (3-5 times in a row in the entity-repair arm),
        # and a repeat should cost nothing and, because entity attribution is an LLM call, must
        # also score the same.
        self._verify_cache: dict[str, tuple] = {}
        # Entity ids the current best source maps (see note_reference); a candidate that keeps all
        # of their sentinels is attributed by reading them, with no model call.
        self._mapped_eids: set[str] = set()
        self._reference_source = ""   # the annotated source being improved (restores dropped sentinels)
        self._r_packages = _collect_r_packages(script_map)

    def note_reference(self, annotated_source: str) -> None:
        """Record which entities the (sentinel-annotated) source being improved maps, and its text."""
        from ..stage2.sentinel_mapper import ranges_from_sentinels
        self._mapped_eids = set(ranges_from_sentinels(annotated_source))
        self._reference_source = annotated_source

    def _restored_ranges(self, candidate: str):
        """Entity ranges of *candidate* with the reference's dropped sentinels restored; None if any
        entity of the reference still has no range."""
        from ..stage2.sentinel_mapper import ranges_from_sentinels, restore_sentinels

        if not self._mapped_eids or not getattr(self, "_reference_source", ""):
            return None
        ranges = ranges_from_sentinels(restore_sentinels(self._reference_source, candidate))
        if not self._mapped_eids <= set(ranges):
            return None
        return {e: r for e, r in ranges.items() if e in self._mapped_eids}

    def verify(self, python_source: str) -> "ScoreReport":
        """Run Stage 4 verification, return full ScoreReport with comparisons."""
        from ..stage2.sentinel_mapper import (
            map_entities_to_lines, strip_sentinels, insert_sentinels,
            flatten_entity_line_map, ranges_from_sentinels, SentinelMappingError,
        )
        from ..stage4 import verifier

        clean = strip_sentinels(python_source)
        key = hashlib.sha1(clean.encode("utf-8")).hexdigest()
        if key in self._verify_cache:
            cache_stats["hit"] += 1
            report, self.last_annotated_source = self._verify_cache[key]
            return report
        cache_stats["miss"] += 1
        kept = ranges_from_sentinels(python_source)
        if self._mapped_eids and self._mapped_eids <= set(kept):
            # Every entity's sentinel survived: read the mapping off them. Asking a model to re-derive
            # it each time gave the same source aggregates from 0.44 to 0.77 (attribution noise).
            entity_ranges = {e: r for e, r in kept.items() if e in self._mapped_eids}
            cache_stats["sentinel_reuse"] += 1
        elif (restored := self._restored_ranges(python_source)) is not None:
            # Some sentinels were dropped: put them back by aligning unchanged lines with the
            # reference, which is deterministic; a model is asked only if that cannot place them all.
            entity_ranges = restored
            cache_stats["sentinel_restored"] += 1
        else:
            entity_ranges = None
            for attempt in range(MAPPING_TRIES):
                try:
                    entity_ranges = map_entities_to_lines(self._script_map, clean, model=self._model)
                    cache_stats["mapping_ok"] += 1
                    self._mapped_eids = set(entity_ranges)
                    break
                except SentinelMappingError as exc:
                    print(f"r2py: sentinel mapping failed (attempt {attempt + 1}/{MAPPING_TRIES}): {exc}")
            if entity_ranges is None:
                # As on the seed path: score without per-entity attribution rather than lose the
                # step. This silently changes the score (0.44 instead of 0.77 on one script), so
                # it is counted.
                cache_stats["mapping_failed"] += 1
                entity_ranges = {}
        self.last_annotated_source = insert_sentinels(clean, entity_ranges)
        entity_line_map = flatten_entity_line_map(entity_ranges)
        kw = {k: v for k, v in self._verify_kwargs.items()
              if k not in ("data_compare", "entity_line_map",
                           "sidecar_filename", "timeout_s")}
        report = verifier.verify(
            self._script_map,
            clean,
            data_compare=self._data_compare,
            entity_line_map=entity_line_map,
            sidecar_filename=self._sidecar_filename,
            timeout_s=self._timeout_s,
            **kw,
        )
        self._verify_cache[key] = (report, self.last_annotated_source)
        return report

    def locate(self, annotated_source: str, eid: str) -> str | None:
        """Where inside entity *eid* does this Python first depart from R?  A sentence for the agent, or None.

        Every call of the entity is probed on both sides (see ``harness.locate``) in two extra sandbox runs; the
        result is cached per (entity, source).  Returns None when the entity cannot be probed (no span, a source
        that does not parse, a run that fails).
        """
        import tempfile

        from ..stage0.effects import data as _data_effects
        from ..stage0.sandbox.py_sandbox import PySandbox
        from ..stage0.sandbox.r_sandbox import RSandbox
        from ..stage1.runner import _CRAWLER_PKG_RE, strip_r_guards
        from ..stage2.sentinel_mapper import ranges_from_sentinels, strip_sentinels
        from ..stage4.verifier import _activate_data_shim, _build_sidecar_payload, _rng_replay, get_r_bundle
        from ..types import EffectClass
        from . import locate as _loc

        clean = strip_sentinels(annotated_source)
        key = ("locate", eid, hashlib.sha1(clean.encode("utf-8")).hexdigest())
        cache = self.__dict__.setdefault("_locate_cache", {})
        if key in cache:
            return cache[key]

        entity = self._script_map.entities.get(eid)
        span = getattr(entity, "source_span", None)
        spans = ranges_from_sentinels(annotated_source).get(eid)
        r_source = getattr(self._script_map, "source", "") or ""
        if span is None or not spans or not r_source:
            return None
        try:
            r_program = strip_r_guards(_loc.r_locate_program(r_source, (span.start_line, span.end_line)))
            m = _CRAWLER_PKG_RE.search(r_source)
            if m:
                r_program = f"suppressPackageStartupMessages(library({m.group(1)}))\n" + r_program
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                RSandbox().run(r_program, workdir=Path(tmp), capture=frozenset({EffectClass.STDOUT}),
                               preamble=_data_effects.build_r_serializer_fn() + _loc.R_PROBE_FUNCTIONS,
                               timeout_s=min(self._timeout_s, 60))
                f = Path(tmp) / "_r2py_probes.json"
                r_probes = _loc.load_probes(f.read_text(encoding="utf-8") if f.exists() else None)

            shimmed, has_shim = _activate_data_shim(clean)
            py_probes: list = []
            for lo, hi in spans:
                instrumented = _loc.instrument_python(shimmed, (lo, hi))
                if instrumented is None:
                    return None
                shimmed = instrumented if len(spans) == 1 else shimmed
                if len(spans) == 1:
                    break
            sidecar = ({self._sidecar_filename: _build_sidecar_payload(self._script_map)}
                       if has_shim and self._sidecar_filename else None)
            with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
                PySandbox().run(shimmed, workdir=Path(tmp), capture=frozenset({EffectClass.DATA, EffectClass.RNG}),
                                preamble=_loc.PY_PROBE_PREAMBLE, timeout_s=min(self._timeout_s, 60),
                                sidecar_files=sidecar, replay=_rng_replay(get_r_bundle(self._script_map)))
                f = Path(tmp) / "_r2py_probes.json"
                py_probes = _loc.load_probes(f.read_text(encoding="utf-8") if f.exists() else None)
        except Exception:
            return None
        if not r_probes:
            return None
        text = _loc.format_divergence(getattr(entity, "name", eid), _loc.find_divergence(r_probes, py_probes),
                                      len(r_probes), len(py_probes))
        cache[key] = text
        return text

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

