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
  {"kind": "<EditKind>", "entity_ids": ["<id>", ...], "params": {...}, "pattern_id": "<slug>"}

Valid kind values (use exactly these strings):
  ReplaceCall           params: {"old_call": "...", "new_call": "..."}
  WrapValue             params: {"name": "...", "wrapper": "..."}
  ChangeImport          params: {"old_import": "...", "new_import": "..."}
  InsertPreamble        params: {"code": "..."}
  RenameVariable        params: {"old": "...", "new": "..."}
  RestructureControlFlow  params: {"old_code": "...", "new_code": "..."}
  ReplaceLibrary        params: {"old_name": "...", "new_name": "...", "old_import": "...", "new_import": "..."}

Rules:
- "pattern_id" is REQUIRED. Use an existing pattern slug (provided below) or propose
  a new short kebab-case slug that names the rule (e.g. "dplyr.filter-to-mask").
- "entity_ids" MUST contain the ID shown after "## Target entity:" — do not target a different entity.
- Target the specific entity that is scoring poorly; set entity_ids to its ID.
- Make the smallest change that addresses the failure.
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
    parts.append("")
    parts.append("### Score breakdown")
    parts.append(f"- executed_ok: {entity_score.executed_ok}")
    parts.append(f"- type_match: {entity_score.type_match:.3f}")
    parts.append(f"- control_flow_match: {entity_score.control_flow_match:.3f}")
    parts.append(f"- data_output: {entity_score.data_output:.3f}")
    parts.append(f"- variable_output: {entity_score.variable_output:.3f}")
    parts.append(f"- callable_output: {entity_score.callable_output:.3f}")
    parts.append(f"- side_effects: {entity_score.side_effects:.3f}")

    # Verifier feedback
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

    # Already-tried edits to avoid
    if history.tried:
        parts.append("")
        parts.append("### Already-tried edits (do NOT repeat these)")
        for e in history.tried[-5:]:  # show last 5 to keep prompt short
            parts.append(f"- kind={e.kind.value} entity_ids={e.entity_ids} params={e.params}")

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
