"""LLM prompt construction and response parsing for Stage 3 (§8.4).

The system prompt is version-controlled and never mutated at runtime (§5.7).
"""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stage1.entities import Entity
    from ..library.pattern import Pattern
    from ..types import EntityScore, FeedbackItem
    from .history import EditHistory


STAGE3_SYSTEM_PROMPT = """\
You are Stage 3 of an R→Python translator. Your job is to propose ONE typed edit
that is likely to improve the Python translation's equivalence score.

You will be shown:
- The target entity (weakest-scoring R entity) and its score breakdown.
- Feedback from the verifier explaining what went wrong.
- The EXPECTED R output — this is the ground truth your edit must match.
- The current Python translation.
- Optionally: the Python definition of functions/names the entity calls.
- Optionally: Pattern Library guidance to follow (exploit mode).

You MUST output exactly ONE JSON object on a single line with these fields:
  {"kind": "<EditKind>", "entity_ids": ["<id>", ...], "params": {...}, "pattern_id": "<slug>", "guidance": "<rule>"}

Valid kind values (use exactly these strings):
  ReplaceCall           params: {"old_call": "...", "new_call": "..."}
  WrapValue             params: {"name": "...", "wrapper": "..."}
  ChangeImport          params: {"old_import": "...", "new_import": "..."}
  InsertPreamble        params: {"code": "..."}
  RenameVariable        params: {"old": "...", "new": "..."}
  RestructureControlFlow  params: {"old_code": "...", "new_code": "...", "start_line": N, "end_line": N}
  ReplaceLibrary        params: {"old_name": "...", "new_name": "...", "old_import": "...", "new_import": "..."}

Rules:
- "pattern_id" is REQUIRED. Use an existing pattern slug (provided below) or propose
  a new short kebab-case slug that names the rule (e.g. "dplyr.filter-to-mask").
- "guidance" is REQUIRED when proposing a NEW pattern_id (one not listed in the Pattern
  Library). Write 1–3 sentences describing the general R→Python translation rule: what
  R construct is being translated, what Python equivalent to use, and any gotchas.
  For an EXISTING pattern_id, omit "guidance" or set it to "".
- "entity_ids" MUST contain the ID shown after "## Target entity:".
- Make the smallest change that addresses the failure.
- When "Expected R output" is provided, your edit MUST make the Python produce output
  matching that format EXACTLY. If the current code uses print(result) but the expected
  output shows a specific format (e.g. named list elements with $`key`), replace the
  print(result) with a formatting loop that matches the expected output.
- When "Called function context" is provided showing a Python function definition, your
  edit should fix the CALL SITE (arguments, print formatting) — not redefine the function.
  Read the function signature carefully to determine correct argument names and types.
- RestructureControlFlow replaces any substring of the FULL script — use it to amend
  earlier shared code (helpers, imports, module-level variables) when that is what the
  target entity needs. You are not limited to editing only the target entity's section.
  start_line and end_line are 1-indexed line numbers (inclusive start, exclusive end).
  PREFER start_line/end_line over old_code whenever the target line contains non-ASCII
  characters (e.g. Unicode in a string literal or comment) — use old_code only for
  ASCII-only targets. When using line numbers, omit old_code entirely.
  IMPORTANT: if the entity's current translation is the stub line
  `pass  # r2py: translation failed for entity (LLM response not valid Python)`, use
  RestructureControlFlow with old_code set to that exact stub line and new_code set to
  a correct Python translation of the R source shown above.
- InsertPreamble is for NEW helpers not yet in the script. If the helper already exists,
  use RestructureControlFlow to amend it instead of inserting a duplicate.
- Before your JSON edit, reason through the failure in 2-4 sentences:
  (1) What the score breakdown and verifier feedback reveal about the root cause.
  (2) What specific change would fix it and why.
  Then output your JSON edit on a single line.

"""


def build_edit_prompt(
    entity: "Entity",
    entity_score: "EntityScore",
    feedback: list["FeedbackItem"],
    translation: str,
    patterns: list["Pattern"],
    history: "EditHistory",
    exploit: bool,
    preferred_edit_kind: "str | None" = None,
    r_source: str = "",
    failure_class: str = "",
    r_expected_output: str = "",
    called_function_context: str = "",
    r_function_source: str = "",
    format_hint: str = "",
    resolved_call: str = "",
    r_type_info: dict | None = None,
    py_actual_output: str = "",
    meta_diagnosis: str = "",
) -> list[dict]:
    """Build the user-turn message for the edit-proposal LLM call."""
    parts: list[str] = []

    # Entity and score breakdown
    parts.append(f"## Target entity: {entity.id} ({_kind_str(entity)})")
    parts.append(f"Name: `{entity.name}`")
    if getattr(entity, "package", None):
        parts.append(f"Package: {entity.package}")
    flags = getattr(entity, "r_semantic_flags", [])
    if flags:
        parts.append(f"R semantic flags: {', '.join(flags)}")
    if r_source:
        parts.append("")
        parts.append("### R source")
        parts.append(f"```r\n{r_source}\n```")
    if resolved_call:
        parts.append("")
        parts.append("### R positional arg binding (from match.call)")
        parts.append(f"R resolves this call to: `{resolved_call}`")
        bound, unbound = _parse_resolved_args(resolved_call)
        if bound:
            for formal, val in bound:
                parts.append(f"- `{formal}` = `{val}` (bound to formal parameter)")
        if unbound:
            for val in unbound:
                parts.append(f"- `{val}` (unmatched → goes to `...` dots, NOT a named parameter)")
            parts.append(
                "IMPORTANT: dots args are passed via `...` in R and are often IGNORED "
                "by the method implementation. Do NOT pass them as named keyword arguments "
                "like from_val, to, by, etc. If the expected output differs drastically "
                "from the actual output, try calling with ONLY the bound formal parameters."
            )
        else:
            parts.append(
                "Your Python translation MUST bind arguments accordingly."
            )
    parts.append("")
    parts.append("### Score breakdown")
    parts.append(f"- executed_ok: {entity_score.executed_ok}")
    parts.append(f"- type_match: {entity_score.type_match:.3f}")
    parts.append(f"- control_flow_match: {entity_score.control_flow_match:.3f}")
    parts.append(f"- data_output: {entity_score.data_output:.3f}")
    parts.append(f"- variable_output: {entity_score.variable_output:.3f}")
    parts.append(f"- callable_output: {entity_score.callable_output:.3f}")
    parts.append(f"- side_effects: {entity_score.side_effects:.3f}")

    # Verifier feedback (text portion; images appended as separate content blocks below)
    entity_feedback = [f for f in feedback if f.entity_id == entity.id]
    if entity_feedback:
        parts.append("")
        parts.append("### Verifier feedback")
        for fb in entity_feedback:
            parts.append(f"- [{fb.effect_class.value}] score={fb.score:.3f}: {fb.message}")

    # Gap 3: Expected R output — ground truth for what the Python should produce
    if r_expected_output:
        _r_out_lines = r_expected_output.splitlines()
        if len(_r_out_lines) > 40:
            r_expected_output = "\n".join(_r_out_lines[:40]) + f"\n... ({len(_r_out_lines) - 40} more lines)"
        parts.append("")
        parts.append("### Expected R output (ground truth)")
        parts.append(
            "The R script produced this EXACT output for this entity. "
            "Your edit MUST make the Python produce output matching this format:"
        )
        parts.append(f"```\n{r_expected_output}\n```")

    # Actual Python output — side-by-side with expected R output
    if py_actual_output:
        _py_out_lines = py_actual_output.splitlines()
        if len(_py_out_lines) > 40:
            py_actual_output = "\n".join(_py_out_lines[:40]) + f"\n... ({len(_py_out_lines) - 40} more lines)"
        parts.append("")
        parts.append("### Actual Python output (current)")
        parts.append(
            "The Python translation currently produces this output for this entity. "
            "Compare it with the expected R output above to identify what needs to change:"
        )
        parts.append(f"```\n{py_actual_output}\n```")
    elif r_expected_output:
        parts.append("")
        parts.append("### Actual Python output (current)")
        parts.append("The Python translation produces NO output for this entity.")

    # R type/class info for variables produced by this entity
    if r_type_info:
        parts.append("")
        parts.append("### R object types for this entity")
        for var_name, info in r_type_info.items():
            if isinstance(info, dict):
                cls = info.get("class", "?")
                tp = info.get("typeof", "?")
                parts.append(f"- `{var_name}`: class={cls}, typeof={tp}")

    # Gap 4: Called function/name context from prior entities
    if called_function_context:
        parts.append("")
        parts.append("### Called function context (defined by a prior entity)")
        parts.append(
            "The function/name this entity uses is ALREADY DEFINED in the translation. "
            "Do NOT redefine it. Fix the CALL SITE — check argument names, types, and "
            "output formatting against this signature:"
        )
        parts.append(f"```python\n{called_function_context}\n```")

    # Gap 4 extension: R source of the called function for semantic understanding
    if r_function_source:
        _r_fn_lines = r_function_source.splitlines()
        if len(_r_fn_lines) > 60:
            r_function_source = "\n".join(_r_fn_lines[:60]) + "\n... (truncated)"
        parts.append("")
        parts.append("### R source of the called function")
        parts.append(
            "This is the R implementation. Use it to understand argument binding, "
            "default values, and the function's actual behaviour:"
        )
        parts.append(f"```r\n{r_function_source}\n```")

    # Gap 2/5: Format hint — reusable print format from a prior entity
    if format_hint:
        parts.append("")
        parts.append("### Output format to reuse")
        parts.append(
            "A prior entity already formatted this function's output. "
            "You MUST use this same format — do NOT use print(result):"
        )
        parts.append(f"```python\n{format_hint}\n```")

    # Current Python translation (trimmed to keep context manageable)
    parts.append("")
    parts.append("### Current Python translation")
    trimmed = translation if len(translation) <= 3000 else translation[:3000] + "\n... (truncated)"
    parts.append(f"```python\n{trimmed}\n```")

    # Pattern guidance (exploit mode only)
    if exploit and patterns:
        parts.append("")
        parts.append("### Pattern Library guidance (apply the most relevant one)")
        for pat in patterns:
            parts.append(f"**Pattern `{pat.id}`** (confidence: {pat.confidence})")
            parts.append(pat.guidance)
            if pat.evidence:
                ev = pat.evidence[0]
                parts.append(f"Evidence: {ev.script_id} → score {ev.score:.3f}")
            parts.append("")
        # Show the best edit example matching the current failure class, if any.
        if failure_class:
            ex = _best_edit_example(patterns, failure_class)
            if ex is not None:
                parts.append(f"### How this pattern fixed a `{failure_class}` failure before")
                parts.append(f"Score delta: +{ex.score_delta:.3f}")
                parts.append(f"Before:\n```python\n{ex.old_code}\n```")
                parts.append(f"After:\n```python\n{ex.new_code}\n```")
                parts.append("")
    elif not exploit:
        parts.append("")
        parts.append("### Mode: explore")
        parts.append(
            "No pattern guidance is provided. Reason from the score breakdown and "
            "feedback to propose any typed edit that is likely to help. You must "
            "still propose a new pattern_id slug that names the rule you are applying."
        )

    # Bandit hint (D6, §12.6 B): suggest a preferred edit kind when a trained policy is active.
    if preferred_edit_kind is not None:
        parts.append("")
        parts.append(f"### Suggested edit kind (learned policy): `{preferred_edit_kind}`")
        parts.append(
            "The learned edit policy suggests this edit kind is most likely to help. "
            "Use it unless a pattern-guided or feedback-driven choice is clearly better."
        )

    # Meta-diagnosis from a stronger model about why previous edits failed
    if meta_diagnosis:
        parts.append("")
        parts.append("### Meta-diagnosis: why previous edits failed")
        parts.append(meta_diagnosis)
        parts.append(
            "Follow this diagnosis. Make ONLY the surgical change described above."
        )

    # Already-tried edits to avoid — filtered to the current entity
    entity_tried = [e for e in history.tried if entity.id in e.entity_ids]
    if entity_tried:
        parts.append("")
        parts.append("### Already-tried edits on this entity (do NOT repeat these)")
        for e in entity_tried[-8:]:  # cap at 8 to keep prompt manageable
            note = history.get_rejection_note(e) if hasattr(history, "get_rejection_note") else ""
            if note:
                parts.append(f"- kind={e.kind.value} params={e.params}")
                parts.append(f"  ↳ {note}")
                if "regressed" in note:
                    parts.append(
                        "  ↳ Your edit broke OTHER entities. Make a more surgical change: "
                        "modify ONLY the call site for this entity, do NOT change shared "
                        "function/class definitions."
                    )
            else:
                parts.append(f"- kind={e.kind.value} params={e.params}")

    return [{"role": "user", "content": "\n".join(parts)}]


def parse_edit_response(raw: str) -> dict | None:
    """Extract the first valid JSON object from the LLM response.

    Returns None if no parseable JSON object is found.
    """
    # Try each line for a single-line JSON object
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = json.loads(line)
                if "kind" in obj:
                    return obj
            except json.JSONDecodeError:
                continue

    # Fallback: extract the outermost {...} block using brace-counting so that
    # multi-line or nested-brace JSON (e.g. params: {"a": "b"}) is handled.
    start = raw.find("{")
    if start != -1:
        depth = 0
        for i, ch in enumerate(raw[start:], start=start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        obj = json.loads(raw[start : i + 1])
                        if "kind" in obj:
                            return obj
                    except json.JSONDecodeError:
                        pass
                    break

    return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_resolved_args(resolved_call: str) -> tuple[list[tuple[str, str]], list[str]]:
    """Parse a resolved call like 'chunk(x = 1, 100, 10)' into bound and unbound args."""
    m = re.match(r'^[\w.]+\((.*)\)$', resolved_call.strip(), re.DOTALL)
    if not m:
        return [], []
    body = m.group(1)
    bound: list[tuple[str, str]] = []
    unbound: list[str] = []
    depth = 0
    current = ""
    for ch in body:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            _classify_arg(current.strip(), bound, unbound)
            current = ""
        else:
            current += ch
    if current.strip():
        _classify_arg(current.strip(), bound, unbound)
    return bound, unbound


def _classify_arg(arg: str, bound: list, unbound: list) -> None:
    eq = arg.find("=")
    if eq > 0 and re.match(r'^[\w.]+\s*$', arg[:eq]):
        formal = arg[:eq].strip()
        val = arg[eq + 1:].strip()
        bound.append((formal, val))
    else:
        unbound.append(arg)


METADIAG_SYSTEM_PROMPT = """\
You are a debugging advisor for an R→Python translation pipeline.

An entity has been edited multiple times but every edit was rejected because it
regressed OTHER entities in the same script. You must diagnose WHY the edits keep
failing and prescribe exactly what to do differently.

Focus on:
1. Which part of the code the previous edits changed (shared function vs. call site).
2. Why that caused regressions in other entities.
3. What the correct surgical fix is — which specific line(s) to change and what to
   change them to, without touching any shared definitions.

Be concrete: name the exact line, the exact old code, and the exact new code.
Keep your response to 3-6 sentences.
"""


def build_meta_diagnosis_prompt(
    entity: "Entity",
    entity_score: "EntityScore",
    history: "EditHistory",
    translation: str,
    r_source: str = "",
    r_expected_output: str = "",
    py_actual_output: str = "",
    resolved_call: str = "",
    called_function_context: str = "",
) -> list[dict]:
    """Build a prompt for the meta-diagnosis LLM call."""
    parts: list[str] = []

    parts.append(f"## Stuck entity: {entity.id} (name: `{entity.name}`)")

    if r_source:
        parts.append(f"\n### R source\n```r\n{r_source}\n```")

    if resolved_call:
        parts.append(f"\n### Resolved call (from match.call)\n`{resolved_call}`")

    if r_expected_output:
        lines = r_expected_output.splitlines()
        if len(lines) > 20:
            r_expected_output = "\n".join(lines[:20]) + f"\n... ({len(lines) - 20} more lines)"
        parts.append(f"\n### Expected R output\n```\n{r_expected_output}\n```")

    if py_actual_output:
        lines = py_actual_output.splitlines()
        if len(lines) > 20:
            py_actual_output = "\n".join(lines[:20]) + f"\n... ({len(lines) - 20} more lines)"
        parts.append(f"\n### Actual Python output\n```\n{py_actual_output}\n```")

    if called_function_context:
        ctx_lines = called_function_context.splitlines()
        if len(ctx_lines) > 30:
            called_function_context = "\n".join(ctx_lines[:30]) + "\n... (truncated)"
        parts.append(f"\n### Shared function definition (used by many entities)\n```python\n{called_function_context}\n```")

    trimmed = translation if len(translation) <= 2000 else translation[:2000] + "\n... (truncated)"
    parts.append(f"\n### Current full translation\n```python\n{trimmed}\n```")

    entity_tried = [e for e in history.tried if entity.id in e.entity_ids]
    if entity_tried:
        parts.append("\n### Previous edit attempts (all rejected)")
        for e in entity_tried[-6:]:
            note = history.get_rejection_note(e) if hasattr(history, "get_rejection_note") else ""
            parts.append(f"- kind={e.kind.value} params={e.params}")
            if note:
                parts.append(f"  {note}")

    parts.append("\nDiagnose why every edit failed and prescribe the correct surgical fix.")

    return [{"role": "user", "content": "\n".join(parts)}]


def _kind_str(entity: "Entity") -> str:
    kind = getattr(entity, "kind", None)
    return getattr(kind, "value", str(kind)) if kind is not None else "unknown"


def _best_edit_example(patterns: list["Pattern"], failure_class: str) -> "object | None":
    """Return the EditExample with the highest score_delta matching failure_class.

    Scans edit_examples on all retrieved patterns; returns None when the library
    has no verified examples for this failure class yet (graceful no-op).
    """
    best = None
    best_delta = -1.0
    for pat in patterns:
        for ex in getattr(pat, "edit_examples", []):
            if ex.failure_class == failure_class and ex.score_delta > best_delta:
                best = ex
                best_delta = ex.score_delta
    return best
