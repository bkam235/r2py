"""Reasoning agent — adaptive translation loop driven by model decisions."""
from __future__ import annotations

import ast
from collections import Counter
import json
import re
import time
from typing import TYPE_CHECKING

from ..stage0.env.module_check import unavailable_imports
from ..stage2.argorder import repair_argument_order
from ..stage2 import llm as _llm
from ..stage2.llm import TruncatedResponseError
from . import prompt as _prompt
from .review import REVIEW_UNAVAILABLE, review_translation
from ..stage2.stitch import (
    DATA_SHIM_BEGIN as _SHIM_MARKER,
    DATA_SHIM_RE as _SHIM_RE,
    rebuild_entity_line_map,
    shadow_autofix,
    splice_entity,
)

# What the agent did, per process, drained into each run's row (see heldout._drain_diagnostics):
# {"action": {rewrite: n, ...}, "outcome": {"rewrite:worse": n, ...}, "stop": {"budget": n, ...}}
agent_stats: dict[str, Counter] = {"action": Counter(), "outcome": Counter(), "stop": Counter()}


def _stat(kind: str, key: str) -> None:
    agent_stats[kind][key] += 1


def drain_agent_stats() -> dict:
    out = {k: dict(v) for k, v in agent_stats.items()}
    for v in agent_stats.values():
        v.clear()
    return out


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
    budget_s: float | None = None,
    audit_feedback: str = "",
    replace_entity: bool = True,
    entity_repair: bool = False,
) -> "tuple[str, ScoreReport] | None":
    """Run the reasoning loop until the score reaches threshold or budget is exhausted.

    Returns (improved_source, score_report) or None if no improvement was achieved.
    """
    from ..stage1.runner import strip_r_guards
    from ..seed import expand_echoed_calls
    r_source = strip_r_guards(getattr(script_map, "source", "") or "")
    entities = getattr(script_map, "entities", {}) or {}
    entity_bundles = getattr(script_map, "entity_bundles", {}) or {}
    r_source, expanded_eids = expand_echoed_calls(
        r_source, entities, entity_bundles,
    )
    best_source = current_source
    best_score = score_report.aggregate
    report = score_report
    history: list[str] = []
    if audit_feedback:
        history.append(audit_feedback)

    patterns_by_entity = _prefetch_patterns(harness, score_report)
    r_function_sources, entity_metadata = _prefetch_r_sources(
        script_map, skip_eids=expanded_eids,
    )
    unavailable_packages = _get_unavailable_packages(script_map)

    is_openrouter = model.startswith("openrouter:")
    system_prompt = _prompt.with_runtime_note(
        _prompt.AGENT_SYSTEM_PROMPT_OPENROUTER if is_openrouter
        else _prompt.AGENT_SYSTEM_PROMPT
    )
    if not replace_entity:
        system_prompt = _prompt.without_replace_entity(system_prompt)

    print(f"[Agent]   Starting reasoning loop (model={model}, score={best_score:.3f}, "
          f"threshold={score_threshold}, max_steps={max_steps})")

    stall_count = 0
    entity_tries: dict[str, int] = {}          # entity repairs attempted, per entity
    entity_notes: dict[str, list[str]] = {}    # what each failed attempt looked like
    # Wall-clock, not step count: the worst script of the first training run burned
    # 10.7h in only 6 rewrites, so a step limit never reached it.
    deadline = time.monotonic() + budget_s if budget_s else None

    for step in range(1, max_steps + 1):
        if deadline is not None and time.monotonic() >= deadline:
            print(f"[Agent]   Wall-clock budget ({budget_s / 60:.0f} min) exhausted "
                  f"after {step - 1} steps, stopping with score {best_score:.3f}")
            _stat("stop", "budget")
            break

        if report.aggregate >= score_threshold:
            print(f"[Agent]   Score {report.aggregate:.3f} >= threshold, stopping")
            _stat("stop", "threshold")
            break

        if stall_count >= max_stalls:
            print(f"[Agent]   {max_stalls} consecutive non-improving rewrites, stopping")
            _stat("stop", "stalled")
            break

        if stall_count > 0 and stall_count >= max_stalls - 1:
            history.append(
                "SYSTEM: You have rewritten twice without improving the score. "
                "Try probe_r to investigate what R actually produces for the "
                "failing entities, or action:done if you cannot improve further."
            )

        # Harness-driven targeted repair: the model does not choose replace_entity on its own
        # (1 use in 84 actions), so the harness picks the failing entity and asks for just that.
        repair_eid = None
        if entity_repair and not (step == 1 and best_score == 0.0):
            repair_eid = _pick_repair_entity(report, best_source, entity_tries)
        turn_system = system_prompt

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
            sidecar_filename=getattr(harness, "_sidecar_filename", ""),
        )

        if repair_eid is not None:
            entity_tries[repair_eid] = entity_tries.get(repair_eid, 0) + 1
            messages = _build_entity_repair(
                script_map, r_source, best_source, report, repair_eid, entity_notes.get(repair_eid, []))
            turn_system = _prompt.ENTITY_REPAIR_SYSTEM
            print(f"[Agent]   Targeting entity {repair_eid} for repair")

        truncated = False
        try:
            raw = _llm.call(
                messages, turn_system,
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
        if repair_eid is not None:
            # Whatever shape the answer took, it is a fragment for this entity.
            frag = action.get("new_source") if action and action.get("action") in ("rewrite", "replace_entity") else None
            if not frag:
                history.append(f"Step {step}: entity repair of {repair_eid}: no usable code in the response")
                _stat("outcome", "entity_repair:no_code")
                stall_count += 1
                continue
            action = {"action": "entity_repair", "entity": repair_eid, "new_source": frag}
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
        _stat("action", action_type)

        if action_type == "done":
            history.append(f"Step {step}: done")
            _stat("stop", "done")
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

        elif action_type in ("rewrite", "replace_entity", "entity_repair"):
            new_source = action.get("new_source", "")
            if not new_source.strip():
                history.append(f"Step {step}: {action_type} (empty source)")
                continue

            if action_type == "replace_entity" and not replace_entity:
                _stat("outcome", "replace_entity:disabled")
                history.append(f"Step {step}: replace_entity is not available; use rewrite.")
                stall_count += 1
                continue

            if action_type in ("replace_entity", "entity_repair"):
                # Splice into the best version so untouched lines stay byte-identical.
                new_source, splice_err = splice_entity(best_source, action.get("entity", ""), new_source)
                if new_source is None:
                    print(f"[Agent]   replace_entity refused: {splice_err}")
                    _stat("outcome", "replace_entity:refused")
                    history.append(f"Step {step}: replace_entity REFUSED — {splice_err}.")
                    continue  # not a stall: nothing was verified

            if _SHIM_MARKER in best_source and _SHIM_MARKER not in new_source:
                print(f"[Agent]   Rewrite dropped data shim block — rejecting")
                history.append(
                    f"Step {step}: rewrite REJECTED — you deleted the "
                    "# r2py:data_shim block. Preserve it exactly as-is."
                )
                stall_count += 1
                continue

            # The data shim is harness-owned, and the prompt says to keep it exactly. Models
            # keep un-commenting it or writing prose inside it ("Simulating highr internal
            # tables"), which is a syntax error once the shim is activated. Put the original back.
            new_source, shim_restored = restore_data_shim(best_source, new_source)
            if shim_restored:
                print("[Agent]   Data shim block was altered; restored the original")
                _stat("outcome", f"{action_type}:shim_restored")

            # R allows named arguments before positional ones; Python does not, and the model
            # keeps writing it. Reordering is meaning-preserving, so do it -- and say so, so the
            # agent still learns the rule instead of having the mistake hidden from it.
            new_source, n_reordered = repair_argument_order(new_source)
            if n_reordered:
                print(f"[Agent]   Reordered arguments in {n_reordered} call(s) (positional first)")
                _stat("outcome", f"{action_type}:arg_order_repaired")
                history.append(
                    f"Step {step}: NOTE — {n_reordered} call(s) had positional arguments after keyword "
                    "arguments (legal in R, a SyntaxError in Python). The harness reordered them "
                    "(positional first). Write positional arguments first yourself.")

            source_lines = len(new_source.splitlines())
            print(f"[Agent]   Rewrite: {source_lines} lines")

            # The auto-fixers are observed, not applied: a silent fix is feedback the
            # agent never sees. Their would-be effect goes to the run record.
            shadow_autofix(new_source, "agent")

            syntax_error = _check_syntax(new_source)
            if syntax_error:
                print(f"[Agent]   Syntax error: {syntax_error}")
                _stat("outcome", f"{action_type}:syntax_rejected")
                stall_count += 1
                # Give targeted hints for the two common R->Python syntax errors.
                hint = ""
                if "positional argument follows keyword argument" in syntax_error:
                    hint = (" NOTE: In Python ALL positional arguments must come "
                            "BEFORE keyword arguments in a function call. "
                            "Move all non-`name=value` arguments to the front "
                            "of every call, before any `name=value` pairs.")
                elif "f-string" in syntax_error and "backslash" in syntax_error:
                    hint = (" NOTE: The target runtime is CPython " + _runtime_version() + ", where an "
                            "f-string expression may not contain a backslash. "
                            "Bind the value first (e.g. `nl = chr(10)` then "
                            "`f\"{s.split(nl)}\"`) instead of inlining the escape.")
                elif "invalid syntax" in syntax_error and "data shim" not in syntax_error:
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

            # Imports that cannot resolve (R package names such as `import magrittr`): tell the
            # agent now instead of spending a verification to learn it from the crash.
            from ..stage0.sandbox.py_sandbox import _SKIP_PACKAGES
            bad_imports = unavailable_imports(new_source, _SKIP_PACKAGES)
            if bad_imports:
                print(f"[Agent]   Unavailable imports: {bad_imports}")
                _stat("outcome", f"{action_type}:import_rejected")
                stall_count += 1
                history.append(
                    f"Step {step}: {action_type} REJECTED before running — these imports cannot be "
                    f"resolved (not installed and not on PyPI): {', '.join(bad_imports)}. They are "
                    "R package names, not Python modules. Do not import them; translate the calls "
                    "with the Python libraries that provide the same function (or implement it)."
                )
                continue

            try:
                new_report = harness.verify(new_source)
            except Exception as exc:
                print(f"[Agent]   Verification failed: {exc}")
                _stat("outcome", f"{action_type}:verify_error")
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

            _stat("outcome", f"{action_type}:" + (
                "improved" if new_report.aggregate > best_score + 1e-9 else
                "catastrophic" if (best_score - new_report.aggregate) >= CATASTROPHIC_DROP
                or (new_report.aggregate == 0.0 and best_score > 0.0) else
                "worse" if new_report.aggregate < best_score - 1e-9 else "unchanged"))
            if new_report.aggregate > best_score:
                # Code review gate: check for rule violations before adopting
                passed, reason = review_translation(
                    r_source, new_source, script_map, model=model,
                    unavailable_packages=unavailable_packages,
                )
                if not passed:
                    print(f"[Review]  FAILED: {reason}")
                    _stat("outcome", f"{action_type}:review_rejected")
                    stall_count += 1
                    # Include a trimmed copy of the rejected source so the
                    # agent can see exactly what was hardcoded and avoid
                    # re-inventing the same approach.
                    rejected_snippet = new_source
                    if len(rejected_snippet) > 1500:
                        rejected_snippet = rejected_snippet[:1500] + "\n... (truncated)"
                    if reason == REVIEW_UNAVAILABLE:
                        history.append(
                            f"Step {step}: rewrite -> {new_report.aggregate:.3f} "
                            "(not adopted: the anti-hardcoding review could not run). "
                            "Resubmit the same approach."
                        )
                        report = new_report
                        continue
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
                if action_type == "entity_repair":
                    entity_notes.setdefault(action["entity"], []).append(
                        f"aggregate went {best_score:.3f} -> {new_report.aggregate:.3f}"
                        + (f"; {crash_msg[:200]}" if crash_msg else ""))
                catastrophic = (best_score - new_report.aggregate) >= CATASTROPHIC_DROP or (
                    new_report.aggregate == 0.0 and best_score > 0.0
                )
                if catastrophic:
                    # The loop always prompts with best_source, so the bad rewrite is
                    # already discarded — but the agent could not tell, and kept
                    # iterating on the broken variant it thought was current.
                    print(f"[Agent]   Catastrophic rewrite ({best_score:.3f} -> "
                          f"{new_report.aggregate:.3f}) — discarded, reverted to best")
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} DISCARDED "
                        f"(score fell from {best_score:.3f}). It has been REVERTED: the "
                        "Python source shown above is the previous, better version, NOT "
                        "your last rewrite. Do not resend that rewrite. Change ONLY the "
                        "statements named as failing and keep every other line "
                        f"byte-identical.{crash_detail}"
                    )
                else:
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


# A rewrite that loses this much score (or crashes a working translation) is
# reported to the agent as discarded, so it stops iterating on a broken variant.
CATASTROPHIC_DROP = 0.25

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
    skip_eids: set[str] | None = None,
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
            source_parts = collect_source_lookups(
                entities, imported_pkgs,
                entity_bundles=getattr(script_map, "entity_bundles", {}),
                skip_eids=skip_eids,
            )
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
_ENTITY_LINE_RE = re.compile(r'^\s*entity\s*:\s*`?([\w:.\-]+)`?\s*$', re.IGNORECASE | re.MULTILINE)


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
        elif action_type == "replace_entity":
            eid_match = _ENTITY_LINE_RE.search(raw[tag_match.end():])
            py_match = _PY_FENCE_RE.search(raw) or _PY_FENCE_OPEN_RE.search(raw)
            if py_match:
                # Missing entity line: still a replace_entity (refused by the loop),
                # never a fragment mistaken for a full rewrite by the fallbacks below.
                code = py_match.group(1).rstrip("`").rstrip()
                if code.strip():
                    return {"action": "replace_entity",
                            "entity": eid_match.group(1) if eid_match else "",
                            "new_source": code}
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
    # The sandbox runs the source with the data shim un-commented, so bare prose
    # left inside the shim block only breaks once activated.
    from ..stage4.verifier import _activate_data_shim
    activated, has_shim = _activate_data_shim(source)
    # Strip lines that start with r2py sentinel comments — they can appear
    # between arguments in some placements and confuse the parser.
    clean = "\n".join(
        line for line in activated.splitlines()
        if not line.lstrip().startswith("# r2py:")
    )
    # Parsed by the interpreter that will run it: the harness's own may be older and reject
    # valid newer syntax (nested f-string quotes).
    from ..stage0.env.py_runtime import syntax_error_in_sandbox_python
    exc = syntax_error_in_sandbox_python(clean)
    if exc:
        detail = f"line {exc['lineno']}: {exc['msg']}" + (" (in the source as executed, data shim active)" if has_shim else "")
        # Show the offending source line: "line 9: invalid syntax" alone told the
        # model nothing, and the line number refers to `clean` (r2py comment lines
        # stripped), so it need not match the source the model sent.
        text = (exc.get("text") or "").rstrip("\n")
        if text.strip():
            caret = " " * max(0, (exc.get("offset") or 1) - 1) + "^"
            detail += f"\n    {text}\n    {caret}"
        return detail
    return None


def _entity_score(es) -> float:
    if not es.executed_ok:
        return 0.0
    dims = [getattr(es, d) for d in es.active_dims]
    return sum(dims) / len(dims) if dims else 1.0


def _pick_repair_entity(report, best_source: str, tries: dict[str, int], max_tries: int = 2) -> str | None:
    """The entity to repair next: the first one that did not run (the root of a crash), else the
    lowest-scoring.  Only entities with one span in the source (``splice_entity`` refuses the rest),
    with something to verify, and not already tried ``max_tries`` times."""
    spans = rebuild_entity_line_map(best_source)
    crashed, weak = [], []
    for eid, es in report.by_entity.items():
        if not es.active_dims or tries.get(eid, 0) >= max_tries or len(spans.get(eid, [])) != 1:
            continue
        sc = _entity_score(es)
        if not es.executed_ok:
            crashed.append((spans[eid][0][0], eid))
        elif sc < 0.9:
            weak.append((sc, eid))
    if crashed:
        return min(crashed)[1]
    return min(weak)[1] if weak else None


def _build_entity_repair(script_map, r_source, best_source, report, eid, notes) -> list[dict]:
    entity = script_map.entities[eid]
    sp = entity.source_span
    r_lines = (getattr(script_map, "source", "") or "").splitlines()
    r_entity = "\n".join(r_lines[sp.start_line:sp.end_line + 1])
    (start, end), = rebuild_entity_line_map(best_source)[eid]
    py_entity = "\n".join(best_source.splitlines()[start:end])  # drops the sentinel line itself
    return _prompt.build_entity_repair_turn(
        r_source, best_source, report, eid, getattr(entity, "name", eid), r_entity, py_entity, notes)


def restore_data_shim(best_source: str, new_source: str) -> tuple[str, bool]:
    """Replace the data-shim block of ``new_source`` with the one from ``best_source``.

    Returns ``(source, changed)``.  Leaves the source alone when either side has no block.
    """
    old, new = _SHIM_RE.search(best_source), _SHIM_RE.search(new_source)
    if new and not old:
        # No shim was generated for this script, so any block is the model's own invention
        # ("No data shim needed for this script" inside the markers was a syntax error).
        return _SHIM_RE.sub("", new_source, count=1), True
    if not old or not new or old.group(0) == new.group(0):
        return new_source, False
    return new_source[:new.start()] + old.group(0) + new_source[new.end():], True


def _runtime_version() -> str:
    from ..stage0.env.py_runtime import python_version
    return python_version()


