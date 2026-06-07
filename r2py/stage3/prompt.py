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
- The current Python translation.
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
- Output ONLY the JSON line. No prose before or after it.
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

    # Already-tried edits to avoid — filtered to the current entity
    entity_tried = [e for e in history.tried if entity.id in e.entity_ids]
    if entity_tried:
        parts.append("")
        parts.append("### Already-tried edits on this entity (do NOT repeat these)")
        for e in entity_tried[-8:]:  # cap at 8 to keep prompt manageable
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
