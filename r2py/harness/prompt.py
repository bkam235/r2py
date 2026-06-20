"""Prompt construction for the reasoning agent."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap
    from ..types import ScoreReport


AGENT_SYSTEM_PROMPT = """\
You are an R→Python translation agent. Your goal is to produce a Python \
translation that is execution-equivalent to the R source.

You work in a loop. Each turn you see:
- The R source code
- Your current Python translation
- The verification result: per-entity scores and concrete R-vs-Python \
output comparisons showing exactly where the translation diverges
- Known translation patterns from the pattern library (when available)

You respond with ONE action per turn as a JSON object on a single line:

{"action": "rewrite", "new_source": "..."}
  Replace the entire Python translation. This is your primary action. \
Use the R source, output comparisons, and pattern library to write correct Python. \
Include # r2py:entity:<id> sentinel comments to preserve entity boundaries.

{"action": "probe_r", "expression": "..."}
  Run an R expression to understand specific behavior you cannot determine \
from the source or patterns alone. Include library() calls for any packages \
the script uses. Only probe when you have a specific question — never to \
explore generally.

{"action": "done"}
  Stop. Use when satisfied with the score or when further progress is unlikely.

Before your JSON action, reason in 2-5 sentences about what the comparisons \
reveal and what you should do next. Then output your action JSON on its own line.

Rules:
- REWRITE FIRST. When the score is low, rewrite the full translation immediately. \
Do not probe before your first rewrite attempt.
- Focus on the WORST-scoring entities first.
- Use the pattern library guidance and translation examples to inform your rewrite.
- Probe only to debug specific mismatches AFTER a rewrite attempt, not before.
- If a rewrite does not improve the score, DO NOT rewrite again with minor changes. \
Instead, probe_r to understand what R actually outputs for the failing entities, \
then rewrite with that knowledge. If you cannot improve further, use action "done".
- When rewriting, preserve ALL entity sentinel comments (# r2py:entity:<id>).
- Each step costs budget. Be action-oriented: rewrite, verify, iterate.
"""

AGENT_SYSTEM_PROMPT_OLLAMA = """\
You are an R-to-Python translation agent. Produce Python code that is \
execution-equivalent to the R source.

Each turn you see the R source, your current Python translation, and a \
verification result showing where R and Python outputs diverge.

## Response format

Respond with a SHORT analysis (1-2 sentences max), then ONE action.

To REWRITE the translation, output the COMPLETE Python file in a fenced block. \
You MUST include ALL entities from the current translation — do not stop early \
or omit entities. The fenced block must contain the ENTIRE file, not a partial \
snippet. If the current translation is 300 lines, your rewrite should be \
roughly 300 lines too.

ACTION: rewrite
```python
# the COMPLETE Python translation — ALL entities, from first import to last call
```

To PROBE R behavior:

ACTION: probe_r
```r
expression_to_evaluate
```

To STOP:

ACTION: done

## Rules
- REWRITE FIRST. When the score is low, rewrite immediately.
- Keep your analysis to 1-2 sentences. ALL your output tokens should go to code.
- The rewrite MUST be the COMPLETE file. Never output just the first few entities.
- Preserve ALL entity sentinel comments (# r2py:entity:<id>).
- Focus on the WORST-scoring entities first, but include ALL entities in the rewrite.
- If a rewrite does not improve the score, DO NOT rewrite again blindly. \
Use probe_r to check what R actually outputs, then rewrite with that knowledge. \
If you cannot improve further, use ACTION: done.
- Each step costs budget. Be action-oriented.
"""


def format_score_report(report: "ScoreReport") -> str:
    """Format a ScoreReport as human-readable text for the agent prompt."""
    parts = [f"Aggregate score: {report.aggregate:.3f}"]

    if report.py_exit_code != 0:
        parts.append(f"Python exit code: {report.py_exit_code} (CRASHED)")

    if report.by_entity:
        parts.append("")
        parts.append("Per-entity scores:")
        for eid, es in sorted(report.by_entity.items(),
                              key=lambda x: _entity_avg(x[1])):
            avg = _entity_avg(es)
            ok = "OK" if es.executed_ok else "CRASH"
            parts.append(f"  {eid}: {avg:.3f} ({ok})")

    if report.comparisons:
        parts.append("")
        parts.append("Output comparisons (R vs Python):")
        for c in report.comparisons:
            eid_label = f" [{c.entity_id}]" if c.entity_id else ""
            parts.append(f"  [{c.effect_class.value}]{eid_label} score={c.score:.3f}")
            parts.append(f"    R produced:      {c.r_value}")
            parts.append(f"    Python produced: {c.py_value}")
            if c.diff_summary:
                parts.append(f"    Diff: {c.diff_summary}")

    if report.feedback:
        parts.append("")
        parts.append("Verifier feedback:")
        for f in report.feedback[:10]:
            parts.append(f"  [{f.entity_id}] {f.effect_class.value}: {f.message}")

    return "\n".join(parts)


def format_entity_list(script_map: "ScriptMap") -> str:
    """Format the entity IDs and names for the agent's reference."""
    entities = getattr(script_map, "entities", {})
    if not entities:
        return "(no entities)"
    parts = []
    for eid, entity in entities.items():
        name = getattr(entity, "name", eid)
        kind = getattr(getattr(entity, "kind", None), "value", "?")
        parts.append(f"  {eid}: {name} ({kind})")
    return "\n".join(parts)


def format_patterns(patterns_by_entity: dict[str, list]) -> str:
    """Format pre-fetched pattern library matches for the agent prompt."""
    if not patterns_by_entity:
        return "(no patterns available)"
    parts = []
    for eid, patterns in patterns_by_entity.items():
        if not patterns:
            continue
        parts.append(f"  Entity {eid}:")
        for pat in patterns[:2]:
            parts.append(f"    Pattern: {pat.id} ({pat.confidence})")
            if pat.guidance:
                parts.append(f"    Guidance: {pat.guidance[:300]}")
            for ex in pat.translation_examples[:2]:
                parts.append(f"    Example R:  {ex.r_snippet[:200]}")
                parts.append(f"    Example Py: {ex.py_snippet[:300]}")
    return "\n".join(parts) if parts else "(no patterns matched)"


def build_agent_turn(
    r_source: str,
    python_source: str,
    report: "ScoreReport",
    script_map: "ScriptMap",
    step: int,
    max_steps: int,
    probe_budget_remaining: int,
    history: list[str] | None = None,
    patterns_by_entity: dict[str, list] | None = None,
) -> list[dict]:
    """Build the messages for one agent reasoning turn."""
    parts = []

    parts.append(f"## Step {step}/{max_steps} (probe budget: {probe_budget_remaining})")
    parts.append("")

    parts.append("### R source")
    parts.append("```r")
    parts.append(r_source)
    parts.append("```")
    parts.append("")

    py_line_count = len(python_source.splitlines())
    parts.append(f"### Current Python translation ({py_line_count} lines — rewrite must include ALL lines)")
    parts.append("```python")
    parts.append(python_source)
    parts.append("```")
    parts.append("")

    parts.append("### Verification result")
    parts.append(format_score_report(report))
    parts.append("")

    parts.append("### Entities")
    parts.append(format_entity_list(script_map))
    parts.append("")

    if patterns_by_entity:
        parts.append("### Pattern library (known translation patterns)")
        parts.append(format_patterns(patterns_by_entity))
        parts.append("")

    if history:
        parts.append("### Previous actions this session")
        for h in history[-5:]:
            parts.append(h)
        parts.append("")

    parts.append("What is your next action? (brief analysis, then action JSON)")

    return [{"role": "user", "content": "\n".join(parts)}]


def _entity_avg(es) -> float:
    return (es.type_match + es.control_flow_match + es.data_output
            + es.variable_output + es.callable_output + es.side_effects) / 6
