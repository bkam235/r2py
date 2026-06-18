"""ε-greedy edit proposal policy for Stage 3 (§8.4).

EXPLOIT: follow the best retrieved Pattern's guidance.
EXPLORE: propose freely, guided only by the verifier's feedback.
"""
from __future__ import annotations

import re
import random
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm
from ..types import Edit, EditKind, EntityScore
from . import prompt as _prompt
from .attributor import attribute, AttributionError
from .edit_types import dict_to_edit

if TYPE_CHECKING:
    from ..library import PatternLibrary
    from ..stage1.script_map import ScriptMap
    from ..types import Candidate
    from .history import EditHistory


def propose(
    candidate: "Candidate",
    script_map: "ScriptMap",
    library: "PatternLibrary",
    history: "EditHistory",
    epsilon: float = 0.2,
    model: str = _llm._DEFAULT_MODEL,
    meta_model: str = _llm._DEFAULT_MODEL,
    _collector: object = None,
    harness: object = None,
) -> Edit:
    """Propose a typed edit targeting the weakest entity in the candidate.

    Tries each entity in ascending score order, skipping already-tried edits.
    Raises RuntimeError if all entities are exhausted or the LLM fails.
    """
    if script_map is None or not getattr(script_map, "entities", {}):
        raise RuntimeError(
            "propose() requires a ScriptMap with populated entities; "
            "pass script_map to stage3.propose_edit() (§4.1 loop)"
        )

    ordered = _weak_first(candidate, script_map, history=history)
    if not ordered:
        raise RuntimeError("no entities to edit: ScoreReport.by_entity is empty")

    from ..library.bandit import BanditModel as _BanditModel
    from ..library import bandit as _bandit

    # Max edits tried for any single entity before moving on (prevents cycling when
    # the LLM generates slight param variations that all produce the same bad score).
    _MAX_ATTEMPTS_PER_ENTITY = 5

    # Scan ALL entities for stubs before the score-ordered loop.
    # Stub entities fall back to the global data score in stage 4 (because `pass`
    # produces no checkpoints and no variable assignment), so they appear to score
    # well and never rise to the top of the weak-first ordering. We must find them
    # by inspecting the translation directly.
    all_entity_ids = list(getattr(script_map, "entities", {}).keys())
    stub_eids_for_llm: list[str] = []  # stubs where retranslation failed; hand to LLM loop
    for eid in all_entity_ids:
        if history.count_for_entity(eid) >= _MAX_ATTEMPTS_PER_ENTITY:
            continue
        if not _entity_is_stub(candidate.translation, eid):
            continue
        from ..stage2.translator import retranslate_entity as _retranslate
        new_snippet = _retranslate(
            eid, script_map, library, model=model,
            current_source=candidate.translation,
        )
        if new_snippet is not None:
            stub_edit = Edit(
                kind=EditKind.RETRANSLATE_ENTITY,
                entity_ids=[eid],
                params={"new_snippet": new_snippet},
                pattern_id="retranslate-stub-entity",
            )
            try:
                attributed = attribute(stub_edit, stub_edit.pattern_id)
            except AttributionError:
                attributed = None
            if attributed is not None and not history.was_tried(attributed):
                return attributed
        # Retranslation returned None (LLM produced invalid Python again) or was
        # already tried. Fall back to the LLM edit loop which can propose a
        # RestructureControlFlow to replace the stub line directly.
        stub_eids_for_llm.append(eid)

    # Promote stubs that couldn't be retranslated to the front of the edit order
    # so the LLM edit prompt can attempt a direct RestructureControlFlow fix.
    if stub_eids_for_llm:
        ordered_set = set(ordered)
        ordered = (
            [eid for eid in stub_eids_for_llm if eid in ordered_set]
            + [eid for eid in ordered if eid not in set(stub_eids_for_llm)]
        )

    bandit_model = getattr(library, "_bandit_model", None)

    for eid in ordered:
        if history.count_for_entity(eid) >= _MAX_ATTEMPTS_PER_ENTITY:
            continue

        entity = _get_entity(script_map, eid)
        if entity is None:
            continue

        # --- Deterministic data-pinning (no LLM) ---
        # If this entity references R built-in datasets or other inherited values
        # whose exact data is captured in actual_bundle.data, embed them directly
        # rather than relying on the LLM to guess or approximate.
        pin_edit = _try_pin_free_variables(entity, candidate)
        if pin_edit is not None:
            try:
                attributed_pin = attribute(pin_edit, pin_edit.pattern_id)
            except AttributionError:
                attributed_pin = None
            if attributed_pin is not None and not history.was_tried(attributed_pin):
                return attributed_pin
        # --- End data-pinning ---

        entity_score = candidate.decomp.by_entity.get(eid, EntityScore(entity_id=eid))
        feedback = [f for f in candidate.decomp.feedback if f.entity_id == eid]

        patterns = library.retrieve(entity, k=3) if hasattr(library, "retrieve") else []
        exploit = bool(patterns) and random.random() > epsilon

        # D6: if a trained bandit model is available, use it to choose the preferred
        # edit kind and pass that hint to the prompt (bandit handles exploration itself).
        bandit_hint: str | None = None
        if isinstance(bandit_model, _BanditModel):
            context = _bandit.extract_context(
                entity_score,
                getattr(getattr(entity, "kind", None), "value", ""),
                getattr(entity, "package", None) or "",
            )
            all_arms = [e.value for e in EditKind]
            bandit_hint = _bandit.choose_action(bandit_model, context, all_arms)

        failure_class = _dominant_failure_class_from_feedback(feedback)

        # Gap 3: extract per-entity R expected output (ground truth).
        # Probe R sandbox whenever entity bundles lack stdout — no longer gated
        # behind 2+ rejections since concrete output is the primary feedback signal.
        r_expected = _entity_r_expected_output(eid, script_map)
        if not r_expected and harness is not None:
            r_src_for_probe = _entity_r_source(entity, script_map)
            if r_src_for_probe:
                r_expected = harness.probe_r(r_src_for_probe)
        if not r_expected:
            r_expected = _diagnostic_r_probe(entity, script_map)

        # Gap 4: extract called function context from prior entities
        called_ctx = _called_function_context(entity, candidate.translation, script_map)

        # Gap 4 extension: R source of the called function
        r_fn_source = _called_function_r_source(entity, script_map)

        # Gap 2/5: extract print-format hint from the first entity that used this name
        fmt_hint = _format_hint_for_entity(entity, candidate.translation, script_map)

        # Resolved positional arg binding from Stage 1's match.call() probe
        resolved_call = getattr(entity, "resolved_call", None) or ""

        # Actual Python output for this entity (from previous verification run)
        py_bundles = getattr(candidate.decomp, "py_entity_bundles", {})
        py_eb = py_bundles.get(eid)
        py_actual_output = (getattr(py_eb, "stdout", "") or "").strip() if py_eb else ""

        # R type/class info for variables produced by this entity
        r_type_info = getattr(script_map, "entity_types", {}).get(eid, {})

        # Meta-diagnosis: reserve the LLM meta-diagnosis call for genuinely stuck
        # entities (3+ rejections). Structured output comparisons (Phase 1) now
        # provide concrete evidence on every iteration, so the LLM meta-call is
        # only needed for complex structural failures the comparison alone can't diagnose.
        _r_src = _entity_r_source(entity, script_map)
        meta_diag = ""
        if history.count_for_entity(eid) >= 3:
            _rej_count = history.count_for_entity(eid)
            print(f"[Meta]    Diagnosing stuck entity {eid!r} ({_rej_count} rejections) via {meta_model}")
            try:
                meta_msgs = _prompt.build_meta_diagnosis_prompt(
                    entity=entity,
                    entity_score=entity_score,
                    history=history,
                    translation=candidate.translation,
                    r_source=_r_src,
                    r_expected_output=r_expected,
                    py_actual_output=py_actual_output,
                    resolved_call=resolved_call,
                    called_function_context=called_ctx,
                )
                meta_diag = _llm.call(
                    meta_msgs, _prompt.METADIAG_SYSTEM_PROMPT,
                    model=meta_model, max_tokens=1024,
                )
                print(f"[Meta]    Diagnosis: {meta_diag[:200]}")
            except Exception as _meta_exc:
                print(f"[Meta]    Diagnosis failed: {_meta_exc}")
                meta_diag = ""

        all_comparisons = getattr(candidate.decomp, "comparisons", [])
        entity_comparisons = [
            c for c in all_comparisons
            if c.entity_id == eid or c.entity_id == ""
        ]
        if entity_comparisons:
            print(f"[Compare] {len(entity_comparisons)} comparison(s) for {eid!r}:")
            for c in entity_comparisons[:3]:
                print(f"          [{c.effect_class.value}] score={c.score:.3f}: R={c.r_value[:80]!r} Py={c.py_value[:80]!r}")
        elif all_comparisons:
            print(f"[Compare] {len(all_comparisons)} comparison(s) total but none match entity {eid!r}")
        else:
            print(f"[Compare] No comparisons in ScoreReport for this candidate")

        messages = _prompt.build_edit_prompt(
            entity=entity,
            entity_score=entity_score,
            feedback=feedback,
            translation=candidate.translation,
            patterns=patterns if exploit else [],
            history=history,
            exploit=exploit,
            preferred_edit_kind=bandit_hint,
            r_source=_r_src,
            failure_class=failure_class,
            r_expected_output=r_expected,
            called_function_context=called_ctx,
            r_function_source=r_fn_source,
            format_hint=fmt_hint,
            resolved_call=resolved_call,
            r_type_info=r_type_info,
            py_actual_output=py_actual_output,
            meta_diagnosis=meta_diag,
            comparisons=entity_comparisons,
        )

        raw = _llm.call(messages, _prompt.STAGE3_SYSTEM_PROMPT, model=model)

        d = _prompt.parse_edit_response(raw)
        if d is None:
            continue

        try:
            edit = dict_to_edit(d)
        except (ValueError, KeyError):
            continue

        # Use pattern_id from the LLM response; in exploit mode also accept the retrieved id.
        pid = d.get("pattern_id") or (patterns[0].id if exploit and patterns else None)

        if _collector is not None and patterns:
            _collector.episodes.append(_make_episode(entity, patterns, pid, exploit))

        try:
            attributed = attribute(edit, pid)
        except AttributionError:
            continue

        if history.was_tried(attributed):
            continue

        # Redirect edits that target a completely different entity than the one
        # we asked the LLM to fix. Redirect rather than reject so the edit
        # still gets applied — the LLM's mechanical params are usually correct,
        # only the entity_ids field is wrong.
        if attributed.entity_ids and eid not in attributed.entity_ids:
            attributed = Edit(
                kind=attributed.kind,
                entity_ids=[eid],
                params=attributed.params,
                pattern_id=attributed.pattern_id,
            )

        return attributed

    raise RuntimeError("no untried edits could be proposed for any entity")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_STUB_SNIPPET = "pass  # r2py: translation failed for entity (LLM response not valid Python)"


def _entity_is_stub(translation: str, eid: str) -> bool:
    """Return True if the entity's section in the assembled translation is the failure stub."""
    sentinel = f"# r2py:entity:{eid}\n"
    idx = translation.find(sentinel)
    if idx == -1:
        return False
    after = translation[idx + len(sentinel):]
    for line in after.splitlines():
        if line.strip():
            return line.strip() == _STUB_SNIPPET
    return False


def _weak_first(
    candidate: "Candidate",
    script_map: object = None,
    history: "EditHistory | None" = None,
) -> list[str]:
    """Return entity IDs sorted by ascending average score, adjusted for past failures.

    Base order (ascending):
      (avg_score, has_no_feedback, is_not_callable)

    Then a position-based rank adjustment is applied: each entity's position in
    the base order is shifted forward by the number of tie/regression edits it
    has received so far (history.count_for_entity).  Entities with the same
    adjusted position are ordered by rejection count ascending then original
    position ascending, so a freshly-tried entity loses to an untried peer at
    the same adjusted rank.

    Example with 3 entities at base ranks [0, 1, 2] and SMM(rank=0) having
    2 rejections: SMM adjusted rank = 2, others unchanged → SMM moves to last.
    """
    from ..types import EntityKind
    scores = candidate.decomp.by_entity
    entities = getattr(script_map, "entities", {}) if script_map is not None else {}
    feedback_eids = {f.entity_id for f in candidate.decomp.feedback}

    def _sort_key(eid: str) -> tuple:
        es = scores[eid]
        entity = entities.get(eid)
        kind_val = getattr(entity, "kind", None) if entity else None
        avg = _avg_score(es, kind=kind_val)
        has_feedback = 0 if eid in feedback_eids else 1
        is_callable = kind_val in (EntityKind.FUNCTION_CALL, EntityKind.EXTERNAL_SYMBOL,
                                   EntityKind.FUNCTION_DEF)
        priority = 0 if is_callable else 1
        return (avg, has_feedback, priority)

    base_order = sorted(scores.keys(), key=_sort_key)

    if history is None:
        return base_order

    # Position-based adjustment: shifted_rank = base_rank + rejection_count.
    # Secondary key: rejection_count ascending (fewer rejections wins ties at
    # same shifted rank).  Tertiary: base_rank ascending (original ordering).
    ranked = [
        (i, eid, history.count_for_entity(eid))
        for i, eid in enumerate(base_order)
    ]
    ranked.sort(key=lambda t: (t[0] + t[2], t[2], t[0]))
    return [eid for _, eid, _ in ranked]


def _avg_score(es: EntityScore, kind=None) -> float:
    # Use only execution-outcome fields for edit priority. type_match, control_flow_match,
    # and callable_output include kind-specific 1.0 constants for non-callable entities
    # (e.g. LIBRARY_IMPORT always gets callable_output=1.0) which would inflate the
    # apparent score of a failed entity and deprioritize it from editing.
    vals = [es.data_output, es.variable_output, es.side_effects]
    # For FUNCTION_DEF, control_flow_match holds stdout_score — the only field that
    # captures whether the function's output matches R. Include it so a function
    # with correct data but wrong stdout is still prioritised for editing.
    # Other kinds use control_flow_match as a binary executed_ok proxy, so we
    # exclude it there to avoid inflating scores for already-running entities.
    from ..types import EntityKind
    if kind == EntityKind.FUNCTION_DEF:
        vals.append(es.control_flow_match)
    base = sum(vals) / len(vals)
    # Penalise entities that did not execute (crash or post-crash): they are more
    # likely to be causing the failure and should rank ahead of pre-crash entities
    # that already ran successfully (crash attribution via §7.4 decompose).
    return base if es.executed_ok else max(0.0, base - 0.1)


def _dominant_failure_class_from_feedback(feedback: list) -> str:
    """Return the EffectClass.value of the worst-scoring feedback item.

    feedback is already filtered to the current entity by the caller.
    Returns "" when there is no feedback (no retrieval key available).
    """
    if not feedback:
        return ""
    worst = min(feedback, key=lambda f: getattr(f, "score", 1.0))
    ec = getattr(worst, "effect_class", None)
    return getattr(ec, "value", str(ec)) if ec is not None else ""


def _entity_r_source(entity: object, script_map: object) -> str:
    """Extract the R source lines for an entity from the ScriptMap."""
    source = getattr(script_map, "source", "") or ""
    if not source:
        return ""
    span = getattr(entity, "source_span", None)
    if span is None:
        return ""
    lines = source.splitlines()
    start = getattr(span, "start_line", 0)
    end = getattr(span, "end_line", start)
    return "\n".join(lines[start:end + 1])


def _get_entity(script_map: "ScriptMap", eid: str) -> object | None:
    """Return the Entity for eid, or None if script_map has no entities dict."""
    entities = getattr(script_map, "entities", {})
    return entities.get(eid)


# ---------------------------------------------------------------------------
# Gap 3: Per-entity R expected output
# ---------------------------------------------------------------------------

def _entity_r_expected_output(eid: str, script_map: object) -> str:
    """Return the R stdout for an entity from Stage 1's per-entity bundles."""
    entity_bundles = getattr(script_map, "entity_bundles", {})
    bundle = entity_bundles.get(eid)
    if bundle is None:
        return ""
    return (getattr(bundle, "stdout", "") or "").strip()


# ---------------------------------------------------------------------------
# Gap 5: Diagnostic R sandbox probe for stuck entities
# ---------------------------------------------------------------------------

def _diagnostic_r_probe(entity: object, script_map: object) -> str:
    """Run the entity's R source in the Stage 0 sandbox to get ground truth output.

    Invoked as a last resort when entity_bundles lack stdout for this entity
    and multiple edit attempts have already failed.  Builds a minimal R script
    from the full script source up to and including this entity, runs it, and
    returns the captured stdout.
    """
    source = getattr(script_map, "source", "") or ""
    if not source:
        return ""
    entity_span = getattr(entity, "source_span", None)
    if entity_span is None:
        return ""

    # Build a script from the beginning through this entity's end line.
    lines = source.splitlines()
    end = min(len(lines), entity_span.end_line + 1)
    r_script = "\n".join(lines[:end])
    if not r_script.strip():
        return ""

    try:
        from ..stage0.sandbox.r_sandbox import RSandbox
        sandbox = RSandbox()
        bundle = sandbox.run(r_script, capture={"stdout"}, timeout_s=30)
        stdout = (getattr(bundle, "stdout", "") or "").strip()
        # The full-script stdout includes all prior entities' output too.
        # Try to isolate this entity's contribution by subtracting prior output.
        prior_stdout = ""
        entity_bundles = getattr(script_map, "entity_bundles", {})
        entities = getattr(script_map, "entities", {})
        for eid, ent in entities.items():
            ent_span = getattr(ent, "source_span", None)
            if ent_span is not None and ent_span.end_line < entity_span.start_line:
                eb = entity_bundles.get(eid)
                if eb is not None:
                    prior_stdout += (getattr(eb, "stdout", "") or "")
        # Rough isolation: if total stdout starts with prior stdout, take the rest
        prior_stripped = prior_stdout.strip()
        if prior_stripped and stdout.startswith(prior_stripped):
            stdout = stdout[len(prior_stripped):].strip()
        return stdout
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Gap 4: Cross-entity context (function/name definitions from prior entities)
# ---------------------------------------------------------------------------

def _called_function_context(entity: object, translation: str, script_map: object) -> str:
    """Extract the Python definition of a function/name the target entity calls.

    When the target entity is a FUNCTION_CALL and the function was defined by a
    prior entity, return the function's signature + first few lines from the
    current translation.  Also works for VARIABLE and other entity kinds that
    reference names defined by prior entities.
    """
    name = getattr(entity, "name", "") or ""
    if not name:
        return ""

    entities = getattr(script_map, "entities", {})
    entity_span = getattr(entity, "source_span", None)
    if entity_span is None:
        return ""

    # Find a prior entity that defines this name
    definer_eid = None
    for eid, ent in entities.items():
        ent_name = getattr(ent, "name", "")
        ent_span = getattr(ent, "source_span", None)
        if ent_name == name and ent_span is not None:
            if ent_span.start_line < entity_span.start_line:
                definer_eid = eid
                break

    if definer_eid is None:
        return ""

    # Extract the full entity code then find the specific function definition
    full_code = _extract_entity_code(translation, definer_eid, max_lines=200)
    if not full_code:
        return ""

    # Look for `def name(` in the entity code and extract that function
    fn_code = _extract_function_def(full_code, name)
    if fn_code:
        return fn_code

    # Fallback: return first 30 lines if no function def found
    lines = full_code.splitlines()
    if len(lines) > 30:
        lines = lines[:30] + [f"... ({len(lines) - 30} more lines)"]
    return "\n".join(lines)


def _extract_entity_code(translation: str, eid: str, max_lines: int = 30) -> str:
    """Extract the Python code for a given entity from the assembled translation."""
    sentinel = f"# r2py:entity:{eid}\n"
    idx = translation.find(sentinel)
    if idx == -1:
        return ""
    after = translation[idx + len(sentinel):]

    # Find the next entity sentinel or end of file
    next_sentinel = re.search(r"^# r2py:entity:", after, re.MULTILINE)
    if next_sentinel:
        code = after[:next_sentinel.start()]
    else:
        code = after

    lines = code.strip().splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"... ({len(lines) - max_lines} more lines)"]
    return "\n".join(lines)


def _extract_function_def(code: str, name: str, max_lines: int = 30) -> str:
    """Extract a `def name(...)` block from a larger code string."""
    lines = code.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        if re.match(rf"^def\s+{re.escape(name)}\s*\(", line):
            start_idx = i
            break
    if start_idx is None:
        return ""
    # Collect the function body (indented lines after the def line)
    end_idx = start_idx + 1
    for j in range(start_idx + 1, len(lines)):
        stripped = lines[j].strip()
        if stripped == "":
            end_idx = j + 1
            continue
        if lines[j][0] != " " and lines[j][0] != "\t":
            break
        end_idx = j + 1
    result_lines = lines[start_idx:end_idx]
    if len(result_lines) > max_lines:
        result_lines = result_lines[:max_lines] + [f"... ({len(result_lines) - max_lines} more lines)"]
    return "\n".join(result_lines)


def _called_function_r_source(entity: object, script_map: object) -> str:
    """Return the R source of the function this entity calls, via package_lookup.

    Only for FUNCTION_CALL entities where the function source is available.
    """
    from ..types import EntityKind

    kind = getattr(entity, "kind", None)
    if kind != EntityKind.FUNCTION_CALL:
        return ""

    name = getattr(entity, "name", "") or ""
    if not name:
        return ""

    # Check if this function was defined by a prior entity (in-script definition)
    # — if so, the R source is already in the ScriptMap, not a package.
    # Only match FUNCTION_DEF entities, not FUNCTION_CALL entities that happen
    # to share the same name (those are call sites, not definitions).
    entities = getattr(script_map, "entities", {})
    entity_span = getattr(entity, "source_span", None)
    for eid, ent in entities.items():
        ent_name = getattr(ent, "name", "")
        ent_kind = getattr(ent, "kind", None)
        ent_span = getattr(ent, "source_span", None)
        if (ent_name == name and ent_kind == EntityKind.FUNCTION_DEF
                and ent_span is not None and entity_span is not None):
            if ent_span.start_line < entity_span.start_line:
                source = getattr(script_map, "source", "") or ""
                if source:
                    lines = source.splitlines()
                    start = ent_span.start_line
                    end = min(len(lines), ent_span.end_line + 1)
                    r_code = "\n".join(lines[start:end])
                    if len(r_code) > 2000:
                        r_code = r_code[:2000] + "\n... (truncated)"
                    return r_code
                return ""

    # Not in-script — try package_lookup
    imported_pkgs: list[str] = [
        e.package
        for e in entities.values()
        if getattr(e, "kind", None) == EntityKind.LIBRARY_IMPORT and e.package
    ]
    if not imported_pkgs:
        return ""

    try:
        from ..stage1.package_lookup import get_function_source_recursive
        source = get_function_source_recursive(imported_pkgs, name)
        if source and len(source) > 2000:
            source = source[:2000] + "\n... (truncated)"
        return source or ""
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Gap 2: Format hint from prior entity's print pattern
# ---------------------------------------------------------------------------

def _format_hint_for_entity(entity: object, translation: str, script_map: object) -> str:
    """Extract a print-formatting pattern from the first entity that used this name.

    When multiple entities call the same function (e.g. chunk, chunk_1, chunk_2),
    the first entity's translation typically includes a print-formatting loop.
    Later entities should reuse that format, not fall back to print(result).
    """
    name = getattr(entity, "name", "") or ""
    if not name:
        return ""

    entities = getattr(script_map, "entities", {})
    entity_span = getattr(entity, "source_span", None)
    if entity_span is None:
        return ""

    # Find the first entity with the same name that was translated earlier
    first_eid = None
    first_start = entity_span.start_line
    for eid, ent in entities.items():
        ent_name = getattr(ent, "name", "")
        ent_span = getattr(ent, "source_span", None)
        if ent_name == name and ent_span is not None:
            if ent_span.start_line < first_start:
                first_start = ent_span.start_line
                first_eid = eid

    if first_eid is None:
        return ""

    # Extract the first entity's FULL code to find print-formatting pattern
    first_code = _extract_entity_code(translation, first_eid, max_lines=500)
    if not first_code:
        return ""

    # Look for a print loop (for key in result: ... print(...))
    lines = first_code.splitlines()
    format_lines: list[str] = []
    in_format = False
    for line in lines:
        stripped = line.strip()
        if "for " in stripped and " in " in stripped and ("result" in stripped or "ret" in stripped):
            in_format = True
        if in_format:
            format_lines.append(line)
            if stripped and not stripped.startswith("#") and not stripped.startswith("for "):
                # Check if we've left the loop body (non-indented line after loop start)
                if format_lines and len(format_lines) > 1 and not line.startswith(" ") and not line.startswith("\t"):
                    break
    if not format_lines:
        return ""

    return "\n".join(format_lines).strip()


# ---------------------------------------------------------------------------
# Data-pinning helpers (deterministic, no LLM)
# ---------------------------------------------------------------------------

_PIN_PATTERN_DATA = "r_builtin_data_pin"
_PIN_MAX_ELEMENTS = 50_000


def _try_pin_free_variables(entity: object, candidate: "Candidate") -> "Edit | None":
    """Return a deterministic edit embedding captured R data into the translation.

    Checks entity.free_variable_refs against entity.actual_bundle.data (which
    is the full-script bundle, populated by Stage 1 step 3b for inherited vars).

    Returns RestructureControlFlow if the variable is already assigned wrongly,
    InsertPreamble if it is absent entirely, or None if nothing to pin.
    """
    from ..types import Edit, EditKind

    free_refs = getattr(entity, "free_variable_refs", [])
    if not free_refs:
        return None

    bundle = getattr(entity, "actual_bundle", None)
    bundle_data: dict = bundle.data if bundle is not None else {}
    if not bundle_data:
        return None

    source = candidate.translation

    to_pin: list[tuple[str, str]] = []
    for name in free_refs:
        if name not in bundle_data:
            continue
        code = _pin_value(name, bundle_data[name])
        if code is not None:
            to_pin.append((name, code))

    if not to_pin:
        return None

    # Replace the first wrongly-assigned variable we find.
    for name, code in to_pin:
        existing = _find_assignment_line(name, source)
        if existing is not None:
            return Edit(
                kind=EditKind.RESTRUCTURE_CONTROL_FLOW,
                entity_ids=[getattr(entity, "id", "")],
                params={"old_code": existing, "new_code": code},
                pattern_id=_PIN_PATTERN_DATA,
            )

    # No wrong assignments — insert all absent variables as a single preamble.
    imports = _pin_imports(bundle_data, [n for n, _ in to_pin])
    preamble = "\n".join(imports + [code for _, code in to_pin])
    return Edit(
        kind=EditKind.INSERT_PREAMBLE,
        entity_ids=[getattr(entity, "id", "")],
        params={"code": preamble},
        pattern_id=_PIN_PATTERN_DATA,
    )


def _find_assignment_line(name: str, source: str) -> "str | None":
    """Return the full source text of the first top-level assignment to *name*.

    Uses the AST to capture multi-line statements (e.g. np.array([\\n...\\n]))
    so that RESTRUCTURE_CONTROL_FLOW replaces the whole expression, not just
    the opening line.  Falls back to a single-line regex if parsing fails.
    """
    import ast as _ast_mod
    lines = source.splitlines(keepends=True)
    try:
        tree = _ast_mod.parse(source)
        for node in tree.body:
            if isinstance(node, _ast_mod.Assign):
                for target in node.targets:
                    if isinstance(target, _ast_mod.Name) and target.id == name:
                        start = node.lineno - 1       # ast uses 1-based lines
                        end = node.end_lineno          # inclusive; slice is exclusive
                        return "".join(lines[start:end])
    except SyntaxError:
        pass
    # Fallback: single-line match only (may leave multi-line tail in place)
    m = re.search(rf"^{re.escape(name)}\s*=.*$", source, re.MULTILINE)
    return m.group(0) if m else None


def _pin_value(name: str, val: object) -> "str | None":
    """Serialise *val* to ``name = <literal>``, or None if too large."""
    try:
        import numpy as np  # type: ignore[import]
        if isinstance(val, np.ndarray):
            if val.size <= _PIN_MAX_ELEMENTS:
                return f"{name} = np.array({val.tolist()!r})"
            return None
    except Exception:
        pass
    try:
        import pandas as pd  # type: ignore[import]
        if isinstance(val, pd.DataFrame):
            if val.size <= _PIN_MAX_ELEMENTS:
                return f"{name} = pd.DataFrame({val.to_dict(orient='list')!r})"
            return None
    except Exception:
        pass
    if isinstance(val, list):
        if len(val) <= _PIN_MAX_ELEMENTS:
            return f"{name} = {val!r}"
        return None
    if isinstance(val, (int, float, bool, str)):
        return f"{name} = {val!r}"
    return None


def _pin_imports(bundle_data: dict, names: list[str]) -> list[str]:
    imports: list[str] = []
    for name in names:
        val = bundle_data.get(name)
        try:
            import numpy as np  # type: ignore[import]
            if isinstance(val, np.ndarray) and "import numpy as np" not in imports:
                imports.append("import numpy as np")
        except Exception:
            pass
        try:
            import pandas as pd  # type: ignore[import]
            if isinstance(val, pd.DataFrame) and "import pandas as pd" not in imports:
                imports.append("import pandas as pd")
        except Exception:
            pass
    return imports


def _make_episode(entity: object, patterns: list, chosen_id: "str | None", exploit: bool) -> object:
    """Build a RetrievalEpisode (outcome/score_delta stamped later by the loop)."""
    from ..types import RetrievalEpisode, RetrievalEpisodeCandidate
    from ..library.retrieval import _token_overlap, _entity_kind_str

    package = getattr(entity, "package", None) or ""
    entity_name = getattr(entity, "name", "") or ""
    entity_kind = _entity_kind_str(entity)

    candidates = []
    for rank, pat in enumerate(patterns):
        pkg_match = pat.package == package
        ast_sim = _token_overlap(entity_kind, pat.id)
        tok_sim = _token_overlap(entity_name, pat.guidance)
        candidates.append(RetrievalEpisodeCandidate(
            pattern_id=pat.id,
            rank=rank,
            package_match=pkg_match,
            ast_shape_sim=ast_sim,
            token_sim=tok_sim,
            confidence=pat.confidence,
            evidence_count=len(pat.evidence),
            contradiction_count=len(pat.contradictions),
            last_review=pat.last_review or "",
        ))

    return RetrievalEpisode(
        query_entity_id=getattr(entity, "id", ""),
        query_entity_kind=entity_kind,
        query_package=package,
        query_entity_name=entity_name,
        candidates=candidates,
        chosen_pattern_id=chosen_id,
        exploit_mode=exploit,
        outcome=None,
        score_delta=None,
        script_id="",
        iteration=0,
    )
