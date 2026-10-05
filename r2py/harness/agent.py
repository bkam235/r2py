"""Reasoning agent — adaptive translation loop driven by model decisions."""
from __future__ import annotations

import ast
from collections import Counter
import json
import re
import threading
import time
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from ..stage0.env.module_check import unavailable_imports
from ..stage2.argorder import repair_argument_order
from ..stage2.sentinel_mapper import ranges_from_sentinels
from . import objective as _obj
from . import trajectory as _trajectory
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
agent_stats: dict[str, Counter] = {"action": Counter(), "outcome": Counter(), "stop": Counter(),
                                   "entity_width": Counter(), "locate": Counter()}


class _StepContext(MutableMapping):
    """The step being run: filled in as the step progresses, logged with each outcome.  One per thread,
    because width runs several loops of this module at once."""

    def __init__(self) -> None:
        self._local = threading.local()

    @property
    def _d(self) -> dict:
        if not hasattr(self._local, "d"):
            self._local.d = {}
        return self._local.d

    def __getitem__(self, k):
        return self._d[k]

    def __setitem__(self, k, v) -> None:
        self._d[k] = v

    def __delitem__(self, k) -> None:
        del self._d[k]

    def __iter__(self):
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)


_ctx = _StepContext()


def _stat(kind: str, key: str) -> None:
    agent_stats[kind][key] += 1
    if kind == "outcome":
        _trajectory.log("step", outcome=key, **_ctx)


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
    escalate_after: "int | None" = None,
    branch: "int | None" = None,
    entity_width: int = 1,
    locate: bool = False,
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
    if hasattr(harness, "note_reference"):
        harness.note_reference(current_source)
    best_score = score_report.aggregate
    report = score_report
    history: list[str] = []   # the audit findings are pinned in the turn (build_agent_turn), not kept here
    runtime = getattr(harness, "runtime", None)
    runtime_section = runtime.prompt_section(getattr(script_map, "source", "") or "") if runtime is not None else ""
    located: set[str] = set()  # entities already probed for the point where Python departs from R
    if locate:
        _loc_note = _locate_note(harness, best_source, report, located)
        if _loc_note:
            history.append(f"Step 0: LOCATED (the harness probed every call of the worst entity in R and in your Python). {_loc_note}")

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
    if runtime_section:
        system_prompt += ("\n\nVerified R functions: when the turn lists Python implementations of R functions, call them "
                          "(`r_<name>(...)`) instead of reimplementing the R function. The harness keeps their code in a block "
                          "between `# r2py:runtime:begin` and `# r2py:runtime:end`; never edit, define or import them.")

    print(f"[Agent]   Starting reasoning loop (model={model}, score={best_score:.3f}, "
          f"threshold={score_threshold}, max_steps={max_steps})")

    # Entity repairs are cheap and each targets a different entity, so three misses in a row
    # is too early to give up on the approach (all 3 scripts of the first live check stopped there).
    if entity_repair:
        max_stalls = max(max_stalls, ENTITY_REPAIR_MAX_STALLS)

    stall_count = 0
    entity_tries: dict[str, int] = {}          # entity repairs attempted, per entity
    entity_notes: dict[str, list[str]] = {}    # what each failed attempt looked like
    repair_misses = 0                          # consecutive non-improving attempts in entity-repair mode
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
        # Escalation: two failed repairs in a row, then one full rewrite (the two approaches won on
        # different scripts in the smoke arms: best-of-two 0.794 against 0.71 / 0.695 each).
        escalate = repair_misses >= (ENTITY_REPAIR_ESCALATE_AFTER if escalate_after is None else escalate_after)
        if escalate:
            print("[Agent]   Escalating to a full rewrite after failed entity repairs")
            _stat("outcome", "escalated_to_rewrite")
            repair_misses = 0
        if entity_repair and not escalate and not (step == 1 and best_score == 0.0):
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
            audit_feedback=audit_feedback,
            runtime_section=runtime_section,
        )

        if repair_eid is not None:
            entity_tries[repair_eid] = entity_tries.get(repair_eid, 0) + 1
            repair_misses += 1   # assume a miss; acceptance resets it
            messages = _build_entity_repair(
                script_map, r_source, best_source, report, repair_eid, entity_notes.get(repair_eid, []))
            turn_system = _prompt.ENTITY_REPAIR_SYSTEM
            print(f"[Agent]   Targeting entity {repair_eid} for repair")

        _ctx.clear()
        _ctx.update(step=step, best_score=round(best_score, 4), best_hash=_trajectory.source_hash(best_source),
                    prompt_hash=_trajectory.source_hash(json.dumps(messages, default=str)),
                    entity_repair=repair_eid, branch=branch)
        t_llm = time.monotonic()
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
            if entity_width > 1:
                action = _widen_entity_repair(action, messages, turn_system, model, entity_width, best_source, harness)
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
        _ctx.update(action=action_type, entity=action.get("entity"), llm_s=round(time.monotonic() - t_llm, 1))
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
            if runtime is not None:   # the managed block of verified functions follows what the code references
                synced = runtime.sync(new_source)
                if synced != new_source:
                    _stat("outcome", f"{action_type}:runtime_block_synced")
                new_source = synced

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

            _ctx.update(source=new_source, source_hash=_trajectory.source_hash(new_source))
            source_lines = len(new_source.splitlines())
            print(f"[Agent]   Rewrite: {source_lines} lines")

            # The auto-fixers are observed, not applied: a silent fix is feedback the
            # agent never sees. Their would-be effect goes to the run record.
            shadow_autofix(new_source, "agent")

            syntax_error = _check_syntax(new_source)
            if syntax_error:
                print(f"[Agent]   Syntax error: {syntax_error}")
                _stat("outcome", f"{action_type}:syntax_rejected")
                _note_rejection(entity_notes, action_type, action, f"syntax error: {syntax_error.splitlines()[0]}")
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
                _note_rejection(entity_notes, action_type, action,
                                f"imported {', '.join(bad_imports)}, which cannot be installed; do not import them")
                stall_count += 1
                history.append(
                    f"Step {step}: {action_type} REJECTED before running — these imports cannot be "
                    f"resolved (not installed and not on PyPI): {', '.join(bad_imports)}. They are "
                    "R package names, not Python modules. Do not import them; translate the calls "
                    "with the Python libraries that provide the same function (or implement it)."
                )
                continue

            # Attribution is read off the entity sentinels when they all survive; tell the agent when
            # some did not, because then a model has to re-derive the mapping (less reliable).
            lost = sorted(getattr(harness, "_mapped_eids", set()) - set(ranges_from_sentinels(new_source)))
            if lost:
                print(f"[Agent]   {len(lost)} entity sentinel(s) missing: {lost[:6]}")
                _stat("outcome", f"{action_type}:sentinels_missing")
                history.append(
                    f"Step {step}: NOTE — {len(lost)} `# r2py:entity:` comment(s) were dropped "
                    f"({', '.join(lost[:6])}). Entity attribution then has to be re-derived by a model, "
                    "which is less reliable. Keep every `# r2py:entity:` line.")

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

            _ctx.update(
                aggregate=round(new_report.aggregate, 4), exit_code=new_report.py_exit_code,
                crash=crash_msg[:600],
                per_entity={eid: round(_entity_score(es), 3) for eid, es in new_report.by_entity.items()})
            _stat("outcome", f"{action_type}:" + (
                "improved" if new_report.aggregate > best_score + 1e-9 else
                "catastrophic" if (best_score - new_report.aggregate) >= CATASTROPHIC_DROP
                or (new_report.aggregate == 0.0 and best_score > 0.0) else
                "worse" if new_report.aggregate < best_score - 1e-9 else "unchanged"))
            if _obj.better(new_report, report):
                # Code review gate: check for rule violations before adopting. A candidate that
                # still crashes is only a stepping stone (Stage 7); the review judges what runs.
                if new_report.py_exit_code == 0:
                    passed, reason = review_translation(
                        r_source, new_source, script_map, model=model,
                        unavailable_packages=unavailable_packages,
                    )
                else:
                    passed, reason = True, ""
                if not passed:
                    print(f"[Review]  FAILED: {reason}")
                    _stat("outcome", f"{action_type}:review_rejected")
                    _note_rejection(entity_notes, action_type, action, f"rejected for hardcoding: {reason[:200]}")
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
                        continue
                    history.append(
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} "
                        f"(REJECTED by review: {reason}). "
                        "Your code contains hardcoded values — you must COMPUTE "
                        "results, not copy expected output as literals.\n"
                        "Rejected code:\n```python\n"
                        f"{rejected_snippet}\n```" + _scores_note(new_report)
                    )
                    # `report` stays the report of the source the agent is shown (best_source):
                    # showing a rejected candidate's comparisons next to a different program
                    # misleads. Its per-entity scores are in the history entry instead.
                else:
                    print(f"[Review]  PASSED")
                    _trajectory.log("accepted", **_ctx)
                    best_source = harness.last_annotated_source or new_source
                    if hasattr(harness, "note_reference"):
                        harness.note_reference(best_source)
                    repair_misses = 0
                    progress_only = new_report.aggregate <= best_score + 1e-9
                    best_score = new_report.aggregate
                    report = new_report
                    stall_count = 0
                    if progress_only:
                        _stat("outcome", f"{action_type}:shaped_progress")
                        history.append(
                            f"Step {step}: rewrite -> {new_report.aggregate:.3f} (ACCEPTED as progress: it "
                            "still crashes, but more of the script now runs or the entities that run score "
                            f"better).{_scores_note(new_report)}")
                    else:
                        history.append(
                            f"Step {step}: rewrite -> {new_report.aggregate:.3f} (ACCEPTED)")
                    if locate:
                        _loc_note = _locate_note(harness, best_source, report, located)
                        if _loc_note:
                            history.append(f"Step {step}: LOCATED. {_loc_note}")
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
                        f"Step {step}: rewrite -> {new_report.aggregate:.3f} (rejected, stall {stall_count})."
                        f"{crash_detail}{_scores_note(new_report)}")
                # `report` is NOT replaced here: it must keep belonging to best_source.

        else:
            history.append(f"Step {step}: unknown action {action_type!r}")

    if _obj.better(report, score_report):
        print(f"[Agent]   Improved: {score_report.aggregate:.3f} -> {best_score:.3f}")
        return best_source, report

    print(f"[Agent]   No improvement achieved (score={best_score:.3f})")
    return None


def _prepare_fragment(best_source: str, eid: str, fragment: str) -> str | None:
    """The source an entity repair would produce, through the gates that need no run; None when refused."""
    from ..stage0.sandbox.py_sandbox import _SKIP_PACKAGES

    new_source, _err = splice_entity(best_source, eid, fragment)
    if new_source is None:
        return None
    new_source, _ = restore_data_shim(best_source, new_source)
    new_source, _ = repair_argument_order(new_source)
    if _check_syntax(new_source) or unavailable_imports(new_source, _SKIP_PACKAGES):
        return None
    return new_source


def _widen_entity_repair(action: dict, messages: list, system: str, model: str, width: int,
                         best_source: str, harness: "HarnessTools") -> dict:
    """Entity-level width (Stage 11a): ``width`` independent repairs of the same entity are sampled in
    parallel, spliced and verified; the best by the search objective replaces the first fragment."""
    eid = action["entity"]

    def sample(_i):
        try:
            a = _parse_action(_llm.call(messages, system, model=model, max_tokens=16384))
        except Exception:
            return None
        return a.get("new_source") if a and a.get("action") in ("rewrite", "replace_entity") else None

    with ThreadPoolExecutor(width - 1) as pool:
        fragments = [action["new_source"]] + [f for f in pool.map(sample, range(width - 1)) if f]
    best_frag, best_rep, seen = action["new_source"], None, set()
    for frag in fragments:
        source = _prepare_fragment(best_source, eid, frag)
        if source is None or source in seen:
            continue
        seen.add(source)
        try:
            rep = harness.verify(source)
        except Exception:
            continue
        if best_rep is None or _obj.better(rep, best_rep):
            best_frag, best_rep = frag, rep
    _stat("entity_width", f"{len(fragments)}_sampled_{len(seen)}_distinct")
    return {**action, "new_source": best_frag}


def reason_wide(harnesses: list, *, current_source: str, score_report: "ScoreReport", script_map: "ScriptMap",
                **kwargs) -> "tuple[str, ScoreReport] | None":
    """Width: one independent agent loop per harness, run in parallel from the same state; the verifier
    picks the best result.  Replays of 20 frozen states gave a mean final score of 0.654 for one loop and
    0.726 / 0.755 for the best of 2 / 3 (selection by the official score, which is computable at
    translation time).  Each loop needs its own harness: verification cache, probe budget and annotated
    source are per-harness state."""
    if len(harnesses) == 1:
        return reason(current_source=current_source, score_report=score_report, harness=harnesses[0],
                      script_map=script_map, **kwargs)

    def one(i: int):
        try:
            return reason(current_source=current_source, score_report=score_report, harness=harnesses[i],
                          script_map=script_map, branch=i, **kwargs)
        except Exception as exc:   # one failing branch must not lose the others
            print(f"[Agent]   Branch {i} failed: {type(exc).__name__}: {exc}")
            return None

    with ThreadPoolExecutor(len(harnesses)) as pool:
        results = [r for r in pool.map(one, range(len(harnesses))) if r is not None]
    best = None
    for r in results:
        if best is None or _obj.better(r[1], best[1]):
            best = r
    print(f"[Agent]   Width {len(harnesses)}: " + (
        "branch scores " + ", ".join(f"{r[1].aggregate:.3f}" for r in results) if results else "no branch improved"))
    return best


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


ENTITY_REPAIR_MAX_STALLS = 6
ENTITY_REPAIR_ESCALATE_AFTER = 2


_entity_score = _obj.entity_score


LOCATE_MAX = 8            # probe runs per agent loop (each is two extra sandbox runs)
LOCATE_BELOW = 0.95       # an entity scoring under this, that ran, is worth locating


def _locate_note(harness: "HarnessTools", annotated_source: str, report: "ScoreReport", tried: set) -> str | None:
    """Where inside the worst-scoring entity that ran does the Python first depart from R?  See ``harness.locate``."""
    if len(tried) >= LOCATE_MAX or not hasattr(harness, "locate"):
        return None
    crashed = set(getattr(report, "crash_entities", []) or [])
    pool = [(eid, _entity_score(es)) for eid, es in report.by_entity.items()
            if es.executed_ok and eid not in crashed and eid not in tried and _entity_score(es) < LOCATE_BELOW]
    for eid, _score in sorted(pool, key=lambda kv: kv[1]):
        tried.add(eid)
        note = harness.locate(annotated_source, eid)
        _stat("locate", "found" if note else "none")
        if note:
            return note
        if len(tried) >= LOCATE_MAX:
            break
    return None


def _scores_note(rep, limit: int = 12) -> str:
    """One line with a candidate's per-entity scores (worst first), for the history entry."""
    items = sorted(((eid, _entity_score(es)) for eid, es in rep.by_entity.items()), key=lambda kv: kv[1])
    if not items:
        return ""
    return " Per-entity scores of that version: " + ", ".join(f"{e}={v:.2f}" for e, v in items[:limit]) + "."


def _note_rejection(notes: dict, action_type: str, action: dict, text: str) -> None:
    """Remember why a harness gate refused an entity repair, so the next attempt on that entity can
    avoid it (before this, only score outcomes reached the notes and the model repeated gated mistakes)."""
    if action_type == "entity_repair" and action.get("entity"):
        notes.setdefault(action["entity"], []).append(text)


def _pick_repair_entity(report, best_source: str, tries: dict[str, int], max_tries: int = 2) -> str | None:
    """The entity to repair next: the first one that did not run (the root of a crash), else the
    lowest-scoring.  Only entities with one span in the source (``splice_entity`` refuses the rest),
    with something to verify, and not already tried ``max_tries`` times."""
    spans = rebuild_entity_line_map(best_source)
    # A crash names its own culprit: the entity whose statement was executing (outermost frame of
    # the traceback), then the entity where the exception was raised. Use that rather than guessing
    # from which entities "did not run" (on googledrive that picked a stub defined far from the crash).
    for eid in getattr(report, "crash_entities", None) or []:
        if tries.get(eid, 0) < max_tries and len(spans.get(eid, [])) == 1 and eid in report.by_entity:
            return eid
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


