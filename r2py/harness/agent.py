"""Reasoning agent — adaptive translation loop driven by model decisions."""
from __future__ import annotations

import ast
import json
import re
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm
from ..stage2.llm import TruncatedResponseError
from . import prompt as _prompt
from .review import review_translation
from ..stage2.stitch import (
    DATA_SHIM_BEGIN as _SHIM_MARKER,
    reorder_positional_before_kwargs,
    sanitize_keyword_args,
)

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import ScoreReport
    from .tools import HarnessTools


def reason(
    current_source: str,
    score_report: "ScoreReport",
    harness: "HarnessTools",
    script_map: "ScriptMap",
    *,
    model: str = _llm._DEFAULT_MODEL,
    max_steps: int = 20,
    score_threshold: float = 0.9,
    max_stalls: int = 3,
    audit_feedback: str = "",
) -> "tuple[str, ScoreReport] | None":
    """Run the reasoning loop until the score reaches threshold or budget is exhausted.

    Returns (improved_source, score_report) or None if no improvement was achieved.
    """
    from ..stage1.runner import strip_r_guards
    r_source = strip_r_guards(getattr(script_map, "source", "") or "")
    best_source = current_source
    best_score = score_report.aggregate
    report = score_report
    history: list[str] = []
    if audit_feedback:
        history.append(audit_feedback)

    patterns_by_entity = _prefetch_patterns(harness, score_report)
    r_function_sources, entity_metadata = _prefetch_r_sources(script_map)
    unavailable_packages = _get_unavailable_packages(script_map)

    is_openrouter = model.startswith("openrouter:")
    system_prompt = (
        _prompt.AGENT_SYSTEM_PROMPT_OPENROUTER if is_openrouter
        else _prompt.AGENT_SYSTEM_PROMPT
    )

    print(f"[Agent]   Starting reasoning loop (model={model}, score={best_score:.3f}, "
          f"threshold={score_threshold}, max_steps={max_steps})")

    stall_count = 0

    for step in range(1, max_steps + 1):
        if report.aggregate >= score_threshold:
            print(f"[Agent]   Score {report.aggregate:.3f} >= threshold, stopping")
            break

        if stall_count >= max_stalls:
            print(f"[Agent]   {max_stalls} consecutive non-improving rewrites, stopping")
            break

        if stall_count > 0 and stall_count >= max_stalls - 1:
            history.append(
                "SYSTEM: You have rewritten twice without improving the score. "
                "Try probe_r to investigate what R actually produces for the "
                "failing entities, or action:done if you cannot improve further."
            )

        messages = _prompt.build_agent_turn(
            r_source=r_source,
            python_source=best_source,
            report=report,
            script_map=script_map,
            step=step,
            max_steps=max_steps,
            probe_budget_remaining=max(0, 10 - harness._probe_count),
            history=history,
            patterns_by_entity=patterns_by_entity,
            r_function_sources=r_function_sources,
            entity_metadata=entity_metadata,
        )

        truncated = False
        try:
            raw = _llm.call(
                messages, system_prompt,
                model=model, max_tokens=16384,
            )
        except TruncatedResponseError as exc:
            raw = exc.partial_text
            truncated = True
            print(f"[Agent]   Response truncated at max_tokens — attempting recovery")
        except Exception as exc:
            print(f"[Agent]   LLM call failed: {exc}")
            break

        action = _parse_action(raw)
        if action is None:
            snippet = raw[:300].replace('\n', '\\n')
            print(f"[Agent]   Could not parse action from response: {snippet!r}")
            # Retry with assistant prefill to force JSON output
            try:
                retry_messages = messages + [
                    {"role": "assistant", "content": raw},
                    {"role": "user", "content": (
                        "Now output ONLY your action as a JSON object. "
                        "No analysis, no explanation."
                    )},
                    {"role": "assistant", "content": '{"action": "'},
                ]
                continuation = _llm.call(
                    retry_messages,
                    system_prompt,
                    model=model, max_tokens=16384,
                )
                action = _parse_action('{"action": "' + continuation)
                if action:
                    print(f"[Agent]   Continuation retry succeeded: {action.get('action', '?')}")
            except TruncatedResponseError as exc:
                action = _parse_action('{"action": "' + exc.partial_text)
                if action:
                    print(f"[Agent]   Continuation retry succeeded (truncated): {action.get('action', '?')}")
            except Exception as exc:
                print(f"[Agent]   Continuation retry failed: {exc}")
            if action is None:
                history.append(
                    f"Step {step}: (your response was analysis only, no action was taken. "
                    "You MUST include an action in your response.)"
                )
                continue

        action_type = action.get("action", "")
        print(f"[Agent]   Step {step}: {action_type}")

        if action_type == "done":
            history.append(f"Step {step}: done")
            break

        elif action_type == "probe_r":
            expression = action.get("expression", "")
            if not expression:
                history.append(f"Step {step}: probe_r (empty expression)")
                continue
            try:
                result = harness.probe_r(expression)
            except Exception as exc:
                result = f"ERROR: {exc}"
            print(f"[Agent]   Probe result: {result[:200]!r}")
            history.append(f"Step {step}: probe_r -> {result[:100]!r}")
            stall_count += 1

        elif action_type == "lookup_docs":
            package = action.get("package", "")
            topic = action.get("topic", "")
            language = action.get("language", "python")
            if not package:
                history.append(f"Step {step}: lookup_docs (missing package)")
                continue
            docs_before = harness._docs_count
            try:
                result = harness.lookup_docs(package, topic, language)
            except Exception as exc:
                result = f"ERROR: {exc}"
            was_cached = harness._docs_count == docs_before
            label = f"{language}::{package}" + (f"::{topic}" if topic else "")
            print(f"[Agent]   Docs {label}: {result[:200]!r}")
            cache_note = " (cached — you already looked this up; try a different query)" if was_cached else ""
            history.append(f"Step {step}: lookup_docs {label}{cache_note} ->\n{result[:800]}")
            stall_count += 1

        elif action_type == "rewrite":
            new_source = action.get("new_source", "")
            if not new_source.strip():
                history.append(f"Step {step}: rewrite (empty source)")
                continue

            if _SHIM_MARKER in best_source and _SHIM_MARKER not in new_source:
                print(f"[Agent]   Rewrite dropped data shim block — rejecting")
                history.append(
                    f"Step {step}: rewrite REJECTED — you deleted the "
                    "# r2py:data_shim block. Preserve it exactly as-is."
                )
                stall_count += 1
                continue

            source_lines = len(new_source.splitlines())
            print(f"[Agent]   Rewrite: {source_lines} lines")

            # Auto-fix Python reserved keywords used as argument names before
            # syntax-checking — the model frequently renames in definitions but
            # forgets call sites (e.g. chunk(from=1) where `from` is a keyword).
            new_source, kw_renamed = sanitize_keyword_args(new_source)
            if kw_renamed:
                print(f"[Agent]   Auto-fixed Python keywords as arg names: {kw_renamed}")
            new_source, reordered = reorder_positional_before_kwargs(new_source)
            if reordered:
                print(f"[Agent]   Auto-fixed positional-after-keyword arg ordering")

            syntax_error = _check_syntax(new_source)
            if syntax_error:
                print(f"[Agent]   Syntax error: {syntax_error}")
                stall_count += 1
                # Give targeted hints for the two common R->Python syntax errors.
                hint = ""
                if "positional argument follows keyword argument" in syntax_error:
                    hint = (" NOTE: In Python ALL positional arguments must come "
                            "BEFORE keyword arguments in a function call. "
                            "Move all non-`name=value` arguments to the front "
                            "of every call, before any `name=value` pairs.")
                elif "invalid syntax" in syntax_error:
                    hint = (" NOTE: Python reserved keywords (from, in, as, class, "
                            "return, import, for, while, if, else, lambda, ...) "
                            "cannot be used as argument names. Rename them "
                            "consistently in definitions AND call sites "
                            "(e.g. `from` -> `from_val`).")
                history.append(
                    f"Step {step}: rewrite REJECTED — Python syntax error: "
                    f"{syntax_error}.{hint} Fix the error and rewrite."
                )
                continue

            try:
                new_report = harness.verify(new_source)
            except Exception as exc:
                print(f"[Agent]   Verification failed: {exc}")
                history.append(f"Step {step}: rewrite -> verification error")
                continue

            print(f"[Agent]   Rewrite scored: {new_report.aggregate:.3f} "
                  f"(was {best_score:.3f}), "
                  f"exit_code={new_report.py_exit_code}")
            crash_msg = ""
            if new_report.py_exit_code != 0 and new_report.feedback:
                crash_fb = [fb for fb in new_report.feedback if fb.effect_class.value == "syntax"]
                if crash_fb:
                    detailed = [fb for fb in crash_fb
                                if "Python crashed" in fb.message and len(fb.message) > 60]
                    crash_msg = (detailed[0] if detailed else crash_fb[0]).message
                    print(f"[Agent]   Crash: {crash_msg[:300]}")

            if new_report.aggregate > best_score:
                # Code review gate: check for rule violations before adopting
                passed, reason = review_translation(
                    r_source, new_source, script_map, model=model,
                    unavailable_packages=unavailable_packages,
                )
                if not passed:
                    print(f"[Review]  FAILED: {reason}")
                    stall_count += 1
                    # Include a trimmed copy of the rejected source so the
                    # agent can see exactly what was hardcoded and avoid
                    # re-inventing the same approach.
                    rejected_snippet = new_source
                    if len(rejected_snippet) > 1500:
                        rejected_snippet = rejected_snippet[:1500] + "\n... (truncated)"
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} "
                        f"(REJECTED by review: {reason}). "
                        "Your code contains hardcoded values — you must COMPUTE "
                        "results, not copy expected output as literals.\n"
                        "Rejected code:\n```python\n"
                        f"{rejected_snippet}\n```"
                    )
                    # Show the rejected rewrite's comparisons on the next
                    # turn so the agent sees which parts were correct vs.
                    # hardcoded, rather than falling back to the stale seed
                    # comparisons.
                    report = new_report
                else:
                    print(f"[Review]  PASSED")
                    best_source = harness.last_annotated_source or new_source
                    best_score = new_report.aggregate
                    report = new_report
                    stall_count = 0
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} (ACCEPTED)")
            else:
                stall_count += 1
                crash_detail = f" Python error: {crash_msg}" if crash_msg else ""
                crash_detail += _auto_lookup_on_crash(crash_msg, harness, new_source)
                history.append(
                    f"Step {step}: rewrite -> {new_report.aggregate:.3f} (rejected, stall {stall_count}).{crash_detail}")
                report = new_report if new_report.aggregate == best_score else report

        else:
            history.append(f"Step {step}: unknown action {action_type!r}")

    if best_score > score_report.aggregate:
        print(f"[Agent]   Improved: {score_report.aggregate:.3f} -> {best_score:.3f}")
        return best_source, report

    print(f"[Agent]   No improvement achieved (score={best_score:.3f})")
    return None


_PKG_COLON_RE = re.compile(r"\b(\w+)::")


def _get_unavailable_packages(script_map: "ScriptMap") -> list[str]:
    """Return R package names used by this script that have no Python equivalent."""
    try:
        from ..stage0.sandbox.py_sandbox import _SKIP_PACKAGES
    except Exception:
        return []
    # Collect from entity metadata
    entities = getattr(script_map, "entities", {}) or {}
    r_packages = {
        getattr(e, "package", "")
        for e in entities.values()
        if getattr(e, "package", "")
    }
    # Also scan R source for pkg::func calls (covers packages used without library())
    r_source = getattr(script_map, "source", "") or ""
    r_packages.update(_PKG_COLON_RE.findall(r_source))
    r_packages.discard("")
    return sorted(r_packages & _SKIP_PACKAGES)


def _prefetch_patterns(harness: "HarnessTools", report: "ScoreReport") -> dict:
    """Pre-fetch pattern library matches for entities in the score report."""
    result = {}
    for eid in report.by_entity:
        patterns = harness.lookup_patterns(eid, k=2)
        if patterns:
            result[eid] = patterns
    return result


def _prefetch_r_sources(
    script_map: "ScriptMap",
) -> "tuple[list[str], str]":
    """Compute R source lookups and entity metadata once before the agent loop."""
    from ..types import EntityKind
    from ..seed import collect_source_lookups, format_entity_metadata

    entities = getattr(script_map, "entities", {}) or {}
    imported_pkgs: list[str] = [
        e.package
        for e in entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]

    source_parts: list[str] = []
    if imported_pkgs:
        try:
            source_parts = collect_source_lookups(entities, imported_pkgs)
        except Exception:
            pass

    metadata = format_entity_metadata(entities)
    return source_parts, metadata


_ACTION_RE = re.compile(r'\{[^{}]*"action"\s*:', re.DOTALL)
_FENCE_RE = re.compile(r'```(?:json)?\s*\n(.*?)```', re.DOTALL)
_PY_FENCE_RE = re.compile(r'```python\s*\n(.*?)```', re.DOTALL)
_PY_FENCE_OPEN_RE = re.compile(r'```python\s*\n(.*)', re.DOTALL)
_R_FENCE_RE = re.compile(r'```r\s*\n(.*?)```', re.DOTALL)
_ACTION_TAG_RE = re.compile(r'ACTION\s*:\s*(\w+)', re.IGNORECASE)


def _parse_action(raw: str) -> dict | None:
    """Extract the action JSON from the agent's response text.

    Handles single-line JSON, markdown-fenced blocks, and embedded JSON.
    """
    # 0) Try ACTION: tag format (structured format for smaller models)
    tag_match = _ACTION_TAG_RE.search(raw)
    if tag_match:
        action_type = tag_match.group(1).lower()
        if action_type == "rewrite":
            py_match = _PY_FENCE_RE.search(raw) or _PY_FENCE_OPEN_RE.search(raw)
            if py_match:
                code = py_match.group(1).rstrip("`").rstrip()
                if code.strip():
                    return {"action": "rewrite", "new_source": code}
        elif action_type == "done":
            return {"action": "done"}
        elif action_type in ("probe_r", "probe"):
            r_match = _R_FENCE_RE.search(raw) or _FENCE_RE.search(raw)
            if r_match:
                return {"action": "probe_r", "expression": r_match.group(1).strip()}
        elif action_type in ("lookup_docs", "docs"):
            # Accept JSON on its own line or in a fenced block after the tag
            after_tag = raw[tag_match.end():]
            for line in after_tag.splitlines():
                line = line.strip()
                if line.startswith("{"):
                    try:
                        params = json.loads(line)
                        if isinstance(params, dict):
                            return {
                                "action": "lookup_docs",
                                "package": params.get("package", ""),
                                "topic": params.get("topic", ""),
                                "language": params.get("language", "python"),
                            }
                    except json.JSONDecodeError:
                        continue
            json_match = _FENCE_RE.search(after_tag)
            if json_match:
                try:
                    params = json.loads(json_match.group(1))
                    if isinstance(params, dict):
                        return {
                            "action": "lookup_docs",
                            "package": params.get("package", ""),
                            "topic": params.get("topic", ""),
                            "language": params.get("language", "python"),
                        }
                except json.JSONDecodeError:
                    pass

    # 1) Try single-line JSON (fast path for well-behaved models)
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
            if "action" in obj:
                return obj
        except json.JSONDecodeError:
            continue

    # 2) Try markdown-fenced code blocks (common pattern for smaller models)
    for fence_match in _FENCE_RE.finditer(raw):
        block = fence_match.group(1).strip()
        try:
            obj = json.loads(block)
            if isinstance(obj, dict) and "action" in obj:
                return obj
        except json.JSONDecodeError:
            continue

    # 3) Try parsing contiguous lines that look like a multi-line JSON object
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("{"):
            accumulated = []
            for j in range(i, len(lines)):
                accumulated.append(lines[j])
                candidate = "\n".join(accumulated)
                try:
                    obj = json.loads(candidate)
                    if isinstance(obj, dict) and "action" in obj:
                        return obj
                except json.JSONDecodeError:
                    if lines[j].strip().endswith("}"):
                        break
                    continue

    # 4) Regex fallback for deeply embedded JSON
    match = _ACTION_RE.search(raw)
    if match:
        start = match.start()
        depth = 0
        for i in range(start, len(raw)):
            if raw[i] == "{":
                depth += 1
            elif raw[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw[start:i + 1])
                    except json.JSONDecodeError:
                        break

    # 5) Relaxed fallback: detect rewrite intent + python code fence (closed or unclosed)
    raw_lower = raw.lower()
    if "rewrite" in raw_lower or "```python" in raw:
        py_match = _PY_FENCE_RE.search(raw) or _PY_FENCE_OPEN_RE.search(raw)
        if py_match:
            code = py_match.group(1).rstrip("`").rstrip()
            if code.strip():
                return {"action": "rewrite", "new_source": code}
    if '"action"' in raw_lower or "'action'" in raw_lower:
        if "done" in raw_lower and "rewrite" not in raw_lower:
            return {"action": "done"}
        if "probe_r" in raw_lower:
            py_match = _PY_FENCE_RE.search(raw) or _FENCE_RE.search(raw)
            if py_match:
                return {"action": "probe_r", "expression": py_match.group(1).strip()}

    # 6) Last resort: bare python fence without any action keyword
    py_match = _PY_FENCE_RE.search(raw) or _PY_FENCE_OPEN_RE.search(raw)
    if py_match:
        code = py_match.group(1).rstrip("`").rstrip()
        if code.strip() and ("import " in code or "def " in code or "r2py:entity" in code):
            return {"action": "rewrite", "new_source": code}

    return None


_IMPORT_ERROR_RE = re.compile(
    r"(?:ImportError|ModuleNotFoundError): (?:cannot import name '(\w+)' from '([\w.]+)'|No module named '([\w.]+)')"
)
_ATTR_ERROR_RE = re.compile(
    r"AttributeError: module '([\w.]+)' has no attribute '(\w+)'"
)


def _search_module_names(module: str, query: str) -> str:
    """Search a Python module's public names for fuzzy matches against *query*.

    Returns a compact string listing matches, or empty string on failure.
    Uses substring and word-boundary matching so e.g. 'action_button' finds
    'input_action_button'.
    """
    import subprocess
    import sys
    code = (
        "import importlib\n"
        f"_m = importlib.import_module({module!r})\n"
        "_ns = getattr(_m, '__all__', None) or "
        "[n for n in dir(_m) if not n.startswith('_')]\n"
        f"_q = {query!r}.lower()\n"
        "_qwords = set(_q.replace('-','_').split('_'))\n"
        "hits = []\n"
        "for n in sorted(_ns):\n"
        "    nl = n.lower()\n"
        "    nwords = set(nl.replace('-','_').split('_'))\n"
        "    if _q in nl or _qwords & nwords:\n"
        "        hits.append(n)\n"
        "print('\\n'.join(hits[:30]))\n"
    )
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=15,
        )
    except subprocess.TimeoutExpired:
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def _search_alternative_module(module: str, name: str, py_source: str = "") -> str:
    """When module has no match, search other modules the script uses.

    Extracts import targets from the Python source and searches those.
    Falls back to common submodules of top-level packages already imported.
    """
    # Extract all modules mentioned in import statements
    candidates: set[str] = set()
    for line in py_source.splitlines():
        line = line.strip()
        if line.startswith("from "):
            parts = line.split()
            if len(parts) >= 2:
                candidates.add(parts[1])
        elif line.startswith("import "):
            for part in line[7:].split(","):
                mod = part.strip().split(" as ")[0].strip()
                if mod:
                    candidates.add(mod)

    # Also try common submodules of top-level packages
    top_pkgs = {c.split(".")[0] for c in candidates}
    for pkg in top_pkgs:
        candidates.update([f"{pkg}.ui", f"{pkg}.render", f"{pkg}.reactive"])

    candidates.discard(module)

    for alt_mod in sorted(candidates):
        matches = _search_module_names(alt_mod, name)
        if matches:
            return (
                f"\n  [Auto-lookup] '{name}' not in {module}. "
                f"Found in {alt_mod}: {matches.replace(chr(10), ', ')}"
            )
    return ""


_FROM_IMPORT_RE = re.compile(
    r"from\s+([\w.]+)\s+import\s+(.+)"
)


def _auto_lookup_on_crash(crash_msg: str, harness: "HarnessTools", py_source: str = "") -> str:
    """When a crash is an import/attribute error, auto-lookup the module's docs.

    Returns a docs string to append to the history, or empty string.
    """
    if not crash_msg:
        return ""
    m = _IMPORT_ERROR_RE.search(crash_msg)
    if m:
        name, module, missing_module = m.group(1), m.group(2), m.group(3)
        if module and name:
            # Check ALL names in the import line, not just the one that failed.
            corrections = _check_all_import_names(crash_msg, module, py_source)
            if corrections:
                return "\n  [Auto-lookup] Import corrections for " + module + ":\n" + corrections
            # Fallback: search for the single failing name
            matches = _search_module_names(module, name)
            if matches:
                return (
                    f"\n  [Auto-lookup] '{name}' not in {module}. "
                    f"Similar names: {matches.replace(chr(10), ', ')}"
                )
            alt = _search_alternative_module(module, name, py_source)
            if alt:
                return alt
            return f"\n  [Auto-lookup] '{name}' not in {module}, and no similar names found."
        elif missing_module:
            parent = missing_module.rsplit(".", 1)[0] if "." in missing_module else ""
            if parent:
                docs = harness.lookup_docs(parent, "", "python")
                return f"\n  [Auto-lookup] '{missing_module}' not found. Parent '{parent}' exports:\n{docs[:1200]}"
            return f"\n  [Auto-lookup] '{missing_module}' is not installed."
    m = _ATTR_ERROR_RE.search(crash_msg)
    if m:
        module, attr = m.group(1), m.group(2)
        matches = _search_module_names(module, attr)
        if matches:
            return (
                f"\n  [Auto-lookup] '{attr}' not in {module}. "
                f"Similar names: {matches.replace(chr(10), ', ')}"
            )
        alt = _search_alternative_module(module, attr, py_source)
        if alt:
            return alt
        return f"\n  [Auto-lookup] '{attr}' not in {module}, no similar names found."
    return ""


def _check_all_import_names(crash_msg: str, module: str, py_source: str = "") -> str:
    """Parse the import line from the traceback or source, check all names.

    Returns a formatted string with corrections for wrong names, or empty string.
    """
    import subprocess, sys
    # Try extracting from the traceback first
    names: list[str] = []
    im = _FROM_IMPORT_RE.search(crash_msg)
    if im and im.group(1) == module:
        names_str = im.group(2).strip().rstrip("\\")
        names_str = names_str.strip("()")
        names = [n.strip().rstrip(",") for n in names_str.split(",") if n.strip()]
    # If traceback had a multi-line import (just "("), parse the Python source
    if not names and py_source:
        _imp_re = re.compile(
            r"from\s+" + re.escape(module) + r"\s+import\s+\(([^)]+)\)",
            re.DOTALL,
        )
        m2 = _imp_re.search(py_source)
        if m2:
            names = [n.strip().rstrip(",") for n in m2.group(1).replace("\n", ",").split(",") if n.strip()]
        elif im and im.group(1) == module:
            # Single-line fallback: re-search py_source for single-line import
            m3 = re.search(r"from\s+" + re.escape(module) + r"\s+import\s+(.+)", py_source)
            if m3:
                names_str = m3.group(1).strip().rstrip("\\").strip("()")
                names = [n.strip().rstrip(",") for n in names_str.split(",") if n.strip()]
    if not names:
        return ""
    # Check which names exist; rank matches by word-set similarity
    code = (
        "import importlib, json\n"
        f"_m = importlib.import_module({module!r})\n"
        "_ns = set(getattr(_m, '__all__', None) or "
        "[n for n in dir(_m) if not n.startswith('_')])\n"
        f"names = {names!r}\n"
        "result = {}\n"
        "for n in names:\n"
        "    if n not in _ns:\n"
        "        q = n.lower()\n"
        "        qwords = set(q.replace('-','_').split('_'))\n"
        "        scored = []\n"
        "        for x in _ns:\n"
        "            xl = x.lower()\n"
        "            xwords = set(xl.replace('-','_').split('_'))\n"
        "            if qwords == xwords:\n"
        "                scored.append((0, x))\n"
        "            elif q in xl:\n"
        "                scored.append((1, x))\n"
        "            elif qwords & xwords and len(qwords & xwords) >= len(qwords) // 2 + 1:\n"
        "                scored.append((2, x))\n"
        "        scored.sort()\n"
        "        result[n] = [x for _, x in scored[:5]]\n"
        "print(json.dumps(result))\n"
    )
    try:
        r = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=20,
        )
        if r.returncode != 0:
            return ""
        import json
        wrong_names = json.loads(r.stdout.strip())
    except Exception:
        return ""
    if not wrong_names:
        return ""
    parts = []
    for wrong, suggestions in wrong_names.items():
        if suggestions:
            parts.append(f"    {wrong} -> try: {', '.join(suggestions)}")
        else:
            parts.append(f"    {wrong} -> NOT FOUND in {module}")
    return "\n".join(parts)


def _check_syntax(source: str) -> str | None:
    """Parse *source* with the AST and return a one-line error or None."""
    # Strip lines that start with r2py sentinel comments — they can appear
    # between arguments in some placements and confuse the parser.
    clean = "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith("# r2py:")
    )
    try:
        ast.parse(clean)
    except SyntaxError as exc:
        return f"line {exc.lineno}: {exc.msg}"
    return None


