"""Whole-file seed translation: translate an R script to Python in one LLM call."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from .stage2 import llm as _llm
from .stage2.argorder import repair_argument_order
from .stage2.stitch import (
    build_data_shim,
    collect_shim_needed_names,
    remove_shim_overrides,
    shadow_autofix,
)
from collections import Counter

from . import __version__ as _r2py_version

if TYPE_CHECKING:
    from .stage1.script_map import ScriptMap
    from .library import PatternLibrary


_SYSTEM_PROMPT = """\
You are an R-to-Python translator. Translate the given R script into clean, \
idiomatic Python that produces equivalent output.

Rules:
1. Use the standard Python equivalents for R packages (e.g. shiny for Python, \
pandas for data frames, numpy for arrays, plotnine for ggplot2).
2. Do not create stub classes or fake implementations. Use real Python libraries.
3. Drop R documentation scaffolding (withAutoprint, examplesIf, rlang::is_interactive, \
rlang::is_installed wrappers) — translate the actual example code inside them. \
These are guards for optional/interactive examples; in our pipeline the guarded \
code always executes in R, so Python must execute it unconditionally too.
4. When Pattern Library guidance is provided, follow it.
5. In Python, positional arguments must come before keyword arguments in \
every function call. R allows named arguments before positional ones — \
reorder them when translating.
6. Python reserved keywords (from, in, as, for, while, if, else, class, \
return, import, lambda, pass, yield, del, not, and, or, is, with, try, \
except, raise, finally, global, nonlocal, async, await, break, continue, \
def, elif, assert) CANNOT be used as function parameter names or keyword \
argument names. R commonly uses `from`, `in`, `as` as parameter names \
(e.g., chunk(from=1, to=100, by=10), seq(from=1, to=10)). Rename them \
consistently in BOTH function definitions AND all call sites \
(e.g., `from` → `from_val`, `in` → `in_val`, `as` → `as_val`).
7. Output ONLY the Python code — no explanation, no markdown fences.
8. Write ALL code at the top/module level. Do NOT wrap the translation inside \
function definitions (def ...) or class definitions. The R original executes \
at the top level, so your Python must too — every variable assignment must \
be a module-level statement, not hidden inside a function body.
9. Preserve R variable names in your translation. If R assigns `d <- sim(m, 1000)`, \
Python must use `d = ...` (same name), not `data` or `df`.
10. Translate ALL sections of the R source — do not skip any part. If an R \
package has no Python equivalent, use numpy/pandas/scipy to approximate the \
computation and produce variables with the same names and similar types \
(DataFrames for data frames, dicts for named lists, etc.).
"""

# Third style: the bare input, but the model first plans each statement.  The styles fail on different
# scripts (best of 4 seeds: 0.49 bare, 0.52 structured, 0.61 for two of each), so a new style is worth more
# than another sample of an old one.  The plan names what differs between R and Python; the plan lines
# are stripped from the code.
_PLANNED_SYSTEM_PROMPT = """\
Translate the R code to Python. Use real libraries (shiny, pandas, numpy, \
plotnine). If a function has no Python equivalent, use numpy/pandas/scipy to \
approximate it. Write all code at the top/module level - do NOT wrap in \
function definitions. Preserve R variable names (d, m, g, etc.). Translate \
ALL sections - do not skip any.

Before the code, write a plan: one line per top-level R statement, each starting \
with "# plan:", naming the Python function you will call and anything that \
differs between the R call and the Python one (argument order and names, \
0-based versus 1-based indexing, data frame versus dict or array, NA handling, \
return type). Then write the Python code. Output only the plan lines and the \
code, nothing else.\
"""

_PLAN_LINE_RE = re.compile(r"^[ \t]*#[ \t]*plan:.*\n?", re.MULTILINE | re.IGNORECASE)

_BARE_SYSTEM_PROMPT = """\
Translate the R code to Python. Use real libraries (shiny, pandas, numpy, \
plotnine). If a function has no Python equivalent, use numpy/pandas/scipy to \
approximate it. Write all code at the top/module level — do NOT wrap in \
function definitions. Preserve R variable names (d, m, g, etc.). Translate \
ALL sections — do not skip any. Output only the Python code, nothing else.\
"""

# At most this many verified fixes are shown per script (the highest score gains).
_MAX_FIXES_IN_PROMPT = 5
# At most this many base-R usage examples are shown per script (the most focused ones).
_MAX_BASE_PATTERNS_IN_PROMPT = 8

_COMMENT_RE = re.compile(r"^#[^\n]*\n", re.MULTILINE)

# Outcomes of the seed gate in this process: found / fixed / still_broken (drained into run rows).
seed_gate_stats: Counter = Counter()


def seed_problems(code: str, runtime=None) -> list[str]:
    """What is wrong with a seed before it is run: the checks the agent loop already applies to
    its rewrites (syntax under the interpreter that will run it, imports that cannot resolve).
    In 255 logged seeds 7 failed on syntax and 56 on an import."""
    from .stage0.env.module_check import unavailable_imports
    from .stage0.env.py_runtime import syntax_error_in_sandbox_python
    from .stage0.sandbox.py_sandbox import _SKIP_PACKAGES

    problems: list[str] = []
    err = syntax_error_in_sandbox_python(code)
    if err:
        problems.append(f"syntax error on line {err['lineno']}: {err['msg']}")
        return problems  # imports of unparseable code are not meaningful
    bad = unavailable_imports(code, _SKIP_PACKAGES)
    if bad:
        problems.append(
            "these imports cannot be resolved (not installed, not on PyPI; they are R package names, "
            f"not Python modules): {', '.join(bad)}. Do not import them; use the Python libraries that "
            "provide the same function, or implement it")
    if runtime is not None:
        unknown = runtime.unknown_references(code)
        if unknown:
            problems.append(
                f"{', '.join(unknown)} {'does' if len(unknown) == 1 else 'do'} not exist: only the verified functions listed in the prompt "
                "exist (r_<name>); implement the other R calls yourself")
    return problems


def _corrective_round(messages: list[dict], system_prompt: str, raw: str, code: str, model: str,
                      lessons: list | None = None, runtime=None) -> str:
    """One corrective turn if the seed has a problem the gates can see, or imports a library the lesson
    store (``r2py.lessons``) has pitfalls for; keep the better version."""
    from .lessons import format_lessons, lessons_for

    problems = seed_problems(code, runtime)
    matched = lessons_for(code, lessons) if lessons else []
    if not problems and not matched:
        return code
    request = ""
    if problems:
        seed_gate_stats["found"] += 1
        print(f"[Seed]    Gate: {'; '.join(problems)[:200]} -- asking for a corrected version", file=sys.stderr)
        request += "This Python cannot run:\n- " + "\n- ".join(problems) + "\n"
    if matched:
        seed_gate_stats["lessons_offered"] += 1
        request += ("Earlier runs of translated scripts hit these problems with libraries you use:\n"
                    + format_lessons(matched) + "\nChange your code where it is affected.\n")
    try:
        fixed_raw = _llm.call(
            messages + [{"role": "assistant", "content": raw},
                        {"role": "user", "content": request + "Return the complete corrected Python code only."}],
            system_prompt, model=model)
    except Exception as exc:
        print(f"[Seed]    corrective round failed: {exc}", file=sys.stderr)
        if problems:
            seed_gate_stats["still_broken"] += 1
        return code
    fixed = _extract_python(fixed_raw)
    remaining = seed_problems(fixed, runtime)
    if not problems:   # lessons only: take the revision unless it broke what ran
        if remaining:
            return code
        seed_gate_stats["lessons_applied"] += 1
        return fixed
    if not remaining:
        seed_gate_stats["fixed"] += 1
        return fixed
    seed_gate_stats["still_broken"] += 1
    return fixed if len(remaining) < len(problems) else code


def translate(
    script_map: "ScriptMap",
    library: "PatternLibrary",
    *,
    model: str = _llm._DEFAULT_MODEL,
    sidecar_filename: str | None = None,
    script_relpath: str | None = None,
    no_seeds: bool = False,
    r_path: str = "",
    bare: bool = False,
    gate: bool = True,
    style: str | None = None,
    runtime=None,
    lessons: list | None = None,
) -> tuple[str, dict[str, tuple[int, int]]]:
    """Translate an R script to Python via a single whole-file LLM call.

    When bare=True, uses a minimal prompt with just the clean R code
    (no pattern library, no metadata, no function source lookups).
    Returns (python_source, entity_line_map).
    """
    from .stage1.runner import strip_r_guards

    style = style or ("bare" if bare else "structured")
    if style in ("bare", "planned"):
        r_clean = strip_r_guards(script_map.source or "")
        r_clean = _COMMENT_RE.sub("", r_clean).strip()
        messages = [{"role": "user", "content": f"```r\n{r_clean}\n```"}]
        system_prompt = _BARE_SYSTEM_PROMPT if style == "bare" else _PLANNED_SYSTEM_PROMPT
    else:
        prompt_parts = _build_prompt(script_map, library, no_seeds=no_seeds, runtime=runtime)
        messages = [{"role": "user", "content": "\n\n".join(prompt_parts)}]
        system_prompt = _SYSTEM_PROMPT

    try:
        raw = _llm.call(messages, system_prompt, model=model)
    except Exception as exc:
        print(f"r2py: seed LLM call failed: {exc}", file=sys.stderr)
        raw = "# r2py: seed translation failed"

    python_code = _extract_python(raw)
    if style == "planned":
        python_code = _PLAN_LINE_RE.sub("", python_code)
    if gate:
        python_code = _corrective_round(messages, system_prompt, raw, python_code, model, lessons, runtime)
    shadow_autofix(python_code, "seed")
    python_code, n_reordered = repair_argument_order(python_code)
    if n_reordered:
        print(f"[Seed]    Reordered arguments in {n_reordered} call(s) (positional first)", file=sys.stderr)
    python_source = _assemble(
        python_code, script_map, model,
        r_path=r_path,
        sidecar_filename=sidecar_filename,
        script_relpath=script_relpath,
    )
    if runtime is not None:
        python_source = runtime.sync(python_source)      # the managed block of the verified functions the code calls
    from .stage2.sentinel_mapper import (
        map_entities_to_lines, insert_sentinels, flatten_entity_line_map,
        SentinelMappingError,
    )
    from .stage2.stitch import rebuild_entity_line_map as _rebuild
    try:
        entity_ranges = map_entities_to_lines(script_map, python_source, model=model)
    except SentinelMappingError as exc:
        # Mapping failed even after retry + overlap resolution.  Continue without
        # sentinels so the translation still runs; per-entity scoring will fall
        # back to aggregate-only mode.
        print(f"r2py: sentinel mapping failed, using aggregate-only scoring: {exc}",
              file=sys.stderr)
        entity_ranges = {}
    python_source = insert_sentinels(python_source, entity_ranges)
    # Re-derive map from sentinel-inserted source so line numbers match.
    return python_source, flatten_entity_line_map(_rebuild(python_source))


def expand_echoed_calls(
    r_source: str,
    entities: dict,
    entity_bundles: dict,
) -> tuple[str, set[str]]:
    """Replace example()/demo() calls with their actual recovered R source.

    Returns (expanded_source, set_of_expanded_entity_ids).  Processes
    entities bottom-up so line-number shifts don't affect earlier entities.
    """
    from .stage1.runner import extract_echoed_source as _extract

    expanded_eids: set[str] = set()
    r_lines = r_source.splitlines()
    for eid, entity in reversed(list(entities.items())):
        eb = entity_bundles.get(eid)
        if eb is None:
            continue
        echoed = _extract(getattr(eb, "stdout", "") or "")
        if not echoed:
            continue
        span = getattr(entity, "source_span", None)
        if span is None:
            continue
        start = max(0, span.start_line)
        end = min(len(r_lines), span.end_line + 1)
        topics = getattr(entity, "free_variable_refs", None) or []
        label = f"{entity.name}({', '.join(topics)})" if topics else entity.name
        header = f"# -- {label}: actual code executed --"
        r_lines[start:end] = [header] + echoed.splitlines()
        expanded_eids.add(eid)
    return "\n".join(r_lines), expanded_eids


def _build_prompt(
    script_map: "ScriptMap",
    library: "PatternLibrary",
    no_seeds: bool = False,
    runtime=None,
) -> list[str]:
    """Build the user prompt for whole-file translation."""
    from .types import EntityKind
    from .stage1.runner import strip_r_guards

    parts: list[str] = []
    r_source = strip_r_guards(script_map.source or "")
    entities = getattr(script_map, "entities", {}) or {}

    entity_bundles = getattr(script_map, "entity_bundles", {}) or {}
    r_source_expanded, expanded_eids = expand_echoed_calls(
        r_source, entities, entity_bundles,
    )

    parts.append(
        f"Translate this R script into Python:\n\n```r\n{r_source_expanded}\n```"
    )

    # Collect pattern library guidance for entities in this script.
    patterns_seen: set[str] = set()
    pattern_parts: list[str] = []
    for entity in entities.values():
        # A pattern that holds only corrections has nothing to show here (see below).
        matches = [p for p in library.retrieve(entity, k=2, no_seeds=no_seeds)
                   if getattr(p, "translation_examples", [])]
        for pat in matches:
            if pat.id in patterns_seen:
                continue
            patterns_seen.add(pat.id)
            entry = f"**{pat.id}** ({pat.confidence}): {pat.guidance.strip()}"
            for ex in getattr(pat, "translation_examples", [])[:1]:
                entry += (
                    f"\n  R: `{ex.r_snippet}`"
                    f"\n  Python: `{ex.py_snippet}`"
                )
            pattern_parts.append(entry)
    if pattern_parts:
        parts.append(
            "## Translation patterns (follow these):\n" + "\n\n".join(pattern_parts)
        )

    # Base-R usage: for base-R functions called inside this script's statements, a verified
    # statement from any script that used the function (the most focused one). Base R is
    # shared by every package, so this transfers across packages.
    if getattr(library, "show_base_patterns", False) is True:
        base_patterns: dict = {}
        for entity in entities.values():
            if getattr(entity, "kind", None) == EntityKind.LIBRARY_IMPORT:
                continue
            for pat in library.retrieve_base_patterns(entity, no_seeds=no_seeds):
                if pat.id not in patterns_seen:
                    base_patterns.setdefault(pat.id, pat)
        best_patterns = sorted(base_patterns.values(),
                               key=lambda p: (p.translation_examples[0].n_calls, p.id))
        best_patterns = best_patterns[:_MAX_BASE_PATTERNS_IN_PROMPT]
        if best_patterns:
            patterns_seen.update(p.id for p in best_patterns)
            parts.append(
                "## Base-R usage (verified statements that use these functions; they may call "
                "other functions too):\n"
                + "\n\n".join(
                    f"**{p.id}**\n  R: `{p.translation_examples[0].r_snippet}`\n"
                    f"  Python: `{p.translation_examples[0].py_snippet}`"
                    for p in best_patterns
                )
            )

    # Verified fixes: for base-R functions this script calls, cases where a first translation
    # was wrong and a corrected one scored higher. Base R is shared by every package, so a fix
    # found in one package's script applies here.
    if getattr(library, "show_corrections", False) is True:
        fixes: dict = {}
        for entity in entities.values():
            if getattr(entity, "kind", None) == EntityKind.LIBRARY_IMPORT:
                continue
            for fix in library.retrieve_corrections(entity, k=1, no_seeds=no_seeds):
                fixes.setdefault((fix.script_id, fix.r_snippet, fix.new_code), fix)
        best = sorted(fixes.values(), key=lambda f: -f.score_delta)[:_MAX_FIXES_IN_PROMPT]
        if best:
            parts.append(
                "## Verified fixes (a first translation of similar R code was wrong; the corrected "
                "version scored higher — avoid the same mistake):\n"
                + "\n\n".join(
                    f"**R** (calls {', '.join(f.functions)}; fixed: {f.failure_class}):\n"
                    f"`{f.r_snippet}`\n  First attempt (wrong): `{f.old_code}`\n"
                    f"  Corrected: `{f.new_code}`"
                    for f in best
                )
            )

    # Collect R source lookups for all package symbols referenced by entities.
    imported_pkgs: list[str] = [
        e.package
        for e in entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]
    if imported_pkgs:
        source_parts = collect_source_lookups(
            entities, imported_pkgs,
            entity_bundles=entity_bundles,
            skip_eids=expanded_eids,
        )
        if source_parts:
            parts.append(
                "## R function source (for reference — translate the logic, "
                "don't hardcode values):\n" + "\n\n".join(source_parts)
            )

    # Surface resolved_call and function_metadata from Stage 1 probes.
    metadata_text = format_entity_metadata(entities)
    if metadata_text:
        parts.append(
            "## Function metadata (from R introspection):\n" + metadata_text
        )

    # Surface R-semantic construct warnings for pitfalls in this script.
    from .construct_catalog import format_construct_notes
    construct_notes = format_construct_notes(entities)
    if construct_notes:
        parts.append(
            "## R construct warnings (language-level pitfalls in this script):\n"
            + construct_notes
        )

    section = runtime.prompt_section(script_map.source or "") if runtime is not None else ""
    if section:
        parts.append("### Verified Python implementations of R functions this script calls\n" + section)

    return parts


def collect_source_lookups(
    entities: dict,
    imported_pkgs: list[str],
    entity_bundles: dict | None = None,
    skip_eids: set[str] | None = None,
) -> list[str]:
    """Look up R source for all package symbols referenced by entities.

    Collects function names from:
    - entity.name for FUNCTION_CALL and EXTERNAL_SYMBOL entities
    - entity.free_variable_refs for ALL entity kinds (captures nested function
      calls inside assignments, arguments, function bodies, etc.)

    When an entity has entity.package set, looks up source in that specific
    package first before searching all imported packages.

    entity_bundles: per-entity EffectBundle deltas (ScriptMap.entity_bundles).
    When an entity's captured stdout contains real R source echoed by a
    construct like example()/demo() (see stage1.runner.extract_echoed_source),
    that recovered source is used instead of a generic function-definition
    lookup for its free_variable_refs -- the actual worked example, not the
    package's (often huge and unhelpful) implementation of the referenced
    symbol.
    """
    from .types import EntityKind
    from .stage1.runner import extract_echoed_source

    try:
        from .stage1.package_lookup import (
            get_function_source_recursive, _BASE_R_NAMES,
        )
    except ImportError:
        return []

    # Entity names that define local variables/functions — skip these for
    # source lookup since they're script-defined, not package symbols.
    local_defs = {
        eid for eid, e in entities.items()
        if getattr(e, "kind", None) in (
            EntityKind.VARIABLE, EntityKind.FUNCTION_DEF, EntityKind.LIBRARY_IMPORT,
        )
    }
    seen: set[str] = set()
    # (name, packages_to_search) pairs — package-specific lookups first
    lookups: list[tuple[str, list[str]]] = []

    # Recover real source for example()/demo()/similar echoing calls first,
    # so their free_variable_refs (the topic(s) they were called with) are
    # marked `seen` before the generic loop below tries to look them up as
    # ordinary function definitions.
    echo_parts: list[str] = []
    for eid, entity in entities.items():
        if skip_eids and eid in skip_eids:
            # Already expanded inline in the R source shown to the model;
            # still mark topic refs as seen to suppress generic lookups.
            seen.add(entity.name)
            for ref in getattr(entity, "free_variable_refs", []) or []:
                seen.add(ref)
            continue
        eb = (entity_bundles or {}).get(eid)
        if eb is None:
            continue
        echoed = extract_echoed_source(getattr(eb, "stdout", "") or "")
        if not echoed:
            continue
        # Label with the call's topic argument(s), not just its name -- a
        # script commonly has several calls sharing the same name (e.g.
        # example(estimate), example(constrain), example(zigreg) all being
        # entities named "example"). Without the topic, multiple recovered
        # blocks are indistinguishable and the model can't reliably map each
        # one back to its specific call site in the visible R source.
        topics = getattr(entity, "free_variable_refs", None) or []
        label = f"{entity.name}({', '.join(topics)})" if topics else entity.name
        echo_parts.append(
            f"### `{label}` (real source, captured during execution)\n"
            f"```r\n{echoed}\n```"
        )
        # Suppress the generic loop's lookups for both this call itself (e.g.
        # `example` -- otherwise it would separately fetch utils::example's
        # own unhelpful implementation) and its topic argument(s) (e.g.
        # `estimate` -- otherwise it would fetch that function's generic
        # definition instead of the worked example we just recovered).
        seen.add(entity.name)
        for ref in getattr(entity, "free_variable_refs", []) or []:
            seen.add(ref)

    # Collect all identifiers from the script as S3 class hints — when a
    # UseMethod generic is found, only fetch methods whose class suffix
    # matches one of these names (avoids fetching 100+ methods for tidy/glance).
    all_refs: set[str] = set()

    for entity in entities.values():
        kind = getattr(entity, "kind", None)
        all_refs.add(entity.name)

        # For FUNCTION_CALL and EXTERNAL_SYMBOL, the entity name is a function.
        if kind in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL):
            name = entity.name
            if name not in seen and name not in _BASE_R_NAMES:
                seen.add(name)
                pkg = getattr(entity, "package", None)
                if pkg and pkg not in imported_pkgs:
                    lookups.append((name, [pkg] + imported_pkgs))
                else:
                    lookups.append((name, imported_pkgs))

        # For ALL entity kinds, free_variable_refs captures identifiers from
        # RHS expressions / arguments — includes nested function calls.
        for ref in getattr(entity, "free_variable_refs", []):
            all_refs.add(ref)
            if ref not in seen and ref not in local_defs and ref not in _BASE_R_NAMES:
                seen.add(ref)
                lookups.append((ref, imported_pkgs))

    s3_class_hints = frozenset(all_refs)

    parts: list[str] = []
    for name, pkgs in lookups:
        try:
            source = get_function_source_recursive(
                pkgs, name, s3_class_hints=s3_class_hints,
            )
        except Exception:
            source = None
        if source:
            parts.append(f"### `{name}`\n```r\n{source}\n```")
    return echo_parts + parts


def format_entity_metadata(entities: dict) -> str:
    """Format resolved_call and function_metadata for the LLM prompt."""
    # Pre-collect all python_keyword_arg flags per name across ALL entities so
    # the dedup-by-name loop below still surfaces warnings even when the flag
    # lives on a later entity with the same name.
    kw_flags_by_name: dict[str, set[str]] = {}
    for entity in entities.values():
        flags = getattr(entity, "r_semantic_flags", [])
        for f in flags:
            if f.startswith("python_keyword_arg:"):
                kw = f[len("python_keyword_arg:"):]
                kw_flags_by_name.setdefault(entity.name, set()).add(kw)

    parts: list[str] = []
    seen_names: set[str] = set()
    for entity in entities.values():
        name = entity.name
        if name in seen_names:
            continue

        lines: list[str] = []

        resolved = getattr(entity, "resolved_call", None)
        if resolved:
            lines.append(f"  Resolved call: {resolved}")

        fm = getattr(entity, "function_metadata", None)
        if fm:
            if fm.formals:
                formals_str = ", ".join(
                    f"{k}={v}" if v else k
                    for k, v in fm.formals.items()
                )
                lines.append(f"  Formals: {formals_str}")
            if fm.methods:
                lines.append(f"  S3 methods: {', '.join(fm.methods)}")

        # Surface python_keyword_arg flags so the LLM knows which argument
        # names clash with Python keywords before it even starts translating.
        kw_flags = kw_flags_by_name.get(name, set())
        if kw_flags:
            unique_kws = sorted(kw_flags)
            lines.append(
                f"  WARNING: R uses Python keyword(s) as arg names: "
                + ", ".join(f"`{k}` -> rename to `{k}_val`" for k in unique_kws)
            )

        if lines:
            seen_names.add(name)
            parts.append(f"  {name}:\n" + "\n".join(lines))

    return "\n".join(parts)


def _extract_python(raw: str) -> str:
    """Extract Python code from LLM response, stripping markdown fences if present."""
    m = re.search(r"```python\s*\n(.*?)```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*\n(.*?)```", raw, re.DOTALL)
    if m:
        return m.group(1).strip()
    return raw.strip()


def _assemble(
    python_code: str,
    script_map: "ScriptMap",
    model: str,
    r_path: str = "",
    sidecar_filename: str | None = None,
    script_relpath: str | None = None,
) -> str:
    """Add header and data shim to the raw translation."""
    entities = getattr(script_map, "entities", {}) or {}
    n_entities = len(entities)
    r_label = r_path or getattr(script_map, "source_file", "<R script>")

    header = (
        f"# Translated from {r_label} by r2py v{_r2py_version}\n"
        f"# Model: {model}  ScriptMap entities: {n_entities}"
    )

    # Build data shim if needed.
    shim_needed = collect_shim_needed_names(script_map) if sidecar_filename else []
    shim_text = ""
    if sidecar_filename and shim_needed:
        shim_text = build_data_shim(
            shim_needed, sidecar_filename, script_relpath=script_relpath
        )
        # Strip assignments to shim-loaded names.
        python_code = remove_shim_overrides(python_code, set(shim_needed))

    parts = [header]
    if shim_text:
        parts.append(shim_text)
    parts.append(python_code)

    return "\n\n".join(parts) + "\n"


