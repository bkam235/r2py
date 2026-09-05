"""Static structural audit — LLM-based pre-execution equivalence check."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm

if TYPE_CHECKING:
    from ..stage1.script_map import ScriptMap

CATEGORIES = (
    "control_flow",
    "function_signature",
    "error_handling",
    "return_structure",
    "side_effects",
    "library_mapping",
)

_SEVERITIES = ("high", "medium", "low")


@dataclass
class AuditFinding:
    category: str
    entity_id: str
    severity: str
    description: str


_AUDIT_SYSTEM = "You are a code equivalence auditor. Compare R source to its Python translation and identify structural divergences. Answer with JSON only."

_AUDIT_PROMPT = """\
You are auditing a Python translation of R code for structural equivalence. \
Do NOT execute either program — compare them by reading the source only.

{entity_section}\
## R source
```r
{r_source}
```

## Python translation
```python
{py_source}
```

## Check categories

1. **control_flow** — Missing or inverted if/else branches, missing loops, \
missing early returns. Do NOT flag stylistic differences (for-loop vs. list \
comprehension) if they produce the same result.

2. **function_signature** — Missing parameters, wrong default values, R's \
`...` not mapped to `*args`/`**kwargs`. Do NOT flag parameter renaming \
(R keywords like `from` → `from_val` is correct).

3. **error_handling** — `tryCatch` without `try/except`, `stop()` without \
`raise`, `warning()` without `warnings.warn()`. Do NOT flag trivial R \
scaffolding guards (withAutoprint, examplesIf, rlang::is_interactive).

4. **return_structure** — Named list vs. dict key mismatches, data.frame vs. \
DataFrame column mismatches, wrong return type. Do NOT flag minor type \
differences (R integer vs. Python int).

5. **side_effects** — Missing `print()` calls, missing file writes, missing \
global state modifications that R performs. Do NOT flag R's implicit \
last-expression printing.

6. **library_mapping** — R library calls mapped to Python packages that do \
not exist or do not have the used function/class. Do NOT flag reasonable \
alternatives (e.g. plotnine for ggplot2, siuba for dplyr).

## Response format

Return a JSON object:

```json
{{"findings": [
  {{
    "category": "control_flow",
    "entity_id": "entity_3",
    "severity": "high",
    "description": "R has tryCatch on lines 15-20 but Python has no try/except"
  }}
]}}
```

- Return `{{"findings": []}}` if no structural issues are found.
- At most 10 findings, sorted by severity (high first).
- `entity_id` should match an entity ID from the listing above, or "" for \
script-level issues.
- Each description must be actionable — state what Python should do differently.

Return ONLY the JSON object, nothing else.
"""


def _build_entity_section(script_map: "ScriptMap | None") -> str:
    if script_map is None:
        return ""
    entities = getattr(script_map, "entities", {})
    if not entities:
        return ""
    lines = ["## Entities\n"]
    for eid, entity in entities.items():
        name = getattr(entity, "name", eid)
        kind = getattr(getattr(entity, "kind", None), "value", "?")
        pkg = getattr(entity, "package", "")
        pkg_note = f" ({pkg})" if pkg else ""
        lines.append(f"- `{eid}`: {name} ({kind}){pkg_note}")
    lines.append("\n")
    return "\n".join(lines)


def static_audit(
    r_source: str,
    py_source: str,
    script_map: "ScriptMap | None" = None,
    *,
    model: str = _llm._DEFAULT_MODEL,
) -> list[AuditFinding]:
    """Structural audit comparing R source to Python translation.

    Single LLM call, fail-open: returns [] on any error.
    """
    entity_section = _build_entity_section(script_map)
    prompt = _AUDIT_PROMPT.format(
        r_source=r_source,
        py_source=py_source,
        entity_section=entity_section,
    )

    try:
        raw = _llm.call(
            [{"role": "user", "content": prompt}],
            _AUDIT_SYSTEM,
            model=model,
            max_tokens=2048,
        )
    except Exception as exc:
        print(f"[Audit]   LLM call failed: {exc}")
        return []

    return _parse_response(raw)


def _parse_response(raw: str) -> list[AuditFinding]:
    raw = raw.strip()
    if raw.startswith("```"):
        m = re.search(r"```(?:json)?\s*\n(.*?)```", raw, re.DOTALL)
        if m:
            raw = m.group(1).strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        print(f"[Audit]   Could not parse audit response: {raw[:200]!r}")
        return []

    if not isinstance(result, dict) or "findings" not in result:
        return []

    findings: list[AuditFinding] = []
    for item in result["findings"]:
        if not isinstance(item, dict):
            continue
        cat = item.get("category", "")
        if cat not in CATEGORIES:
            continue
        sev = item.get("severity", "medium")
        if sev not in _SEVERITIES:
            sev = "medium"
        desc = item.get("description", "")
        if not desc:
            continue
        findings.append(AuditFinding(
            category=cat,
            entity_id=str(item.get("entity_id", "")),
            severity=sev,
            description=desc,
        ))

    return findings[:10]


def format_audit_for_agent(findings: list[AuditFinding]) -> str:
    if not findings:
        return ""
    severity_order = {"high": 0, "medium": 1, "low": 2}
    ordered = sorted(findings, key=lambda f: severity_order.get(f.severity, 1))
    lines = [
        f"SYSTEM: Static structural audit found {len(ordered)} issue(s) "
        f"in the seed translation:"
    ]
    for f in ordered:
        eid = f" {f.entity_id}" if f.entity_id else ""
        lines.append(
            f"  [{f.severity.upper()}]{eid} ({f.category}): {f.description}"
        )
    lines.append(
        "Address these in your rewrites. These are structural issues that "
        "execution-based verification may not catch."
    )
    return "\n".join(lines)
