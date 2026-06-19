"""Reasoning agent — adaptive translation loop driven by model decisions."""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING

from ..stage2 import llm as _llm
from . import prompt as _prompt

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
) -> "tuple[str, ScoreReport] | None":
    """Run the reasoning loop until the score reaches threshold or budget is exhausted.

    Returns (improved_source, score_report) or None if no improvement was achieved.
    """
    r_source = getattr(script_map, "source", "") or ""
    best_source = current_source
    best_score = score_report.aggregate
    report = score_report
    history: list[str] = []

    patterns_by_entity = _prefetch_patterns(harness, score_report)

    is_ollama = model.startswith("ollama:")
    system_prompt = (
        _prompt.AGENT_SYSTEM_PROMPT_OLLAMA if is_ollama
        else _prompt.AGENT_SYSTEM_PROMPT
    )

    print(f"[Agent]   Starting reasoning loop (model={model}, score={best_score:.3f}, "
          f"threshold={score_threshold}, max_steps={max_steps})")

    stall_count = 0

    for step in range(1, max_steps + 1):
        if report.aggregate >= score_threshold:
            print(f"[Agent]   Score {report.aggregate:.3f} >= threshold, stopping")
            break

        if stall_count >= 3:
            print(f"[Agent]   3 consecutive non-improving rewrites, stopping")
            break

        if stall_count >= 2:
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
        )

        try:
            raw = _llm.call(
                messages, system_prompt,
                model=model, max_tokens=16384,
            )
        except Exception as exc:
            print(f"[Agent]   LLM call failed: {exc}")
            break

        action = _parse_action(raw)
        if action is None:
            print(f"[Agent]   Could not parse action from response")
            history.append(f"Step {step}: (parse error)")
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
            stall_count = 0

        elif action_type == "rewrite":
            new_source = action.get("new_source", "")
            if not new_source.strip():
                history.append(f"Step {step}: rewrite (empty source)")
                continue

            sentinel_count = new_source.count("# r2py:entity:")
            source_lines = len(new_source.splitlines())
            print(f"[Agent]   Rewrite: {source_lines} lines, {sentinel_count} entity sentinels")

            try:
                new_report = harness.verify(new_source)
            except Exception as exc:
                print(f"[Agent]   Verification failed: {exc}")
                history.append(f"Step {step}: rewrite -> verification error")
                continue

            print(f"[Agent]   Rewrite scored: {new_report.aggregate:.3f} "
                  f"(was {best_score:.3f}), "
                  f"exit_code={new_report.py_exit_code}")
            if new_report.py_exit_code != 0 and new_report.feedback:
                crash_fb = [fb for fb in new_report.feedback if fb.effect_class.value == "syntax"]
                if crash_fb:
                    print(f"[Agent]   Crash: {crash_fb[0].message[:200]}")

            if new_report.aggregate > best_score:
                best_source = new_source
                best_score = new_report.aggregate
                report = new_report
                stall_count = 0
                history.append(
                    f"Step {step}: rewrite -> {new_report.aggregate:.3f} (ACCEPTED)")
            else:
                stall_count += 1
                history.append(
                    f"Step {step}: rewrite -> {new_report.aggregate:.3f} (rejected, stall {stall_count})")
                report = new_report if new_report.aggregate == best_score else report

        else:
            history.append(f"Step {step}: unknown action {action_type!r}")

    if best_score > score_report.aggregate:
        print(f"[Agent]   Improved: {score_report.aggregate:.3f} -> {best_score:.3f}")
        return best_source, report

    print(f"[Agent]   No improvement achieved (score={best_score:.3f})")
    return None


def _prefetch_patterns(harness: "HarnessTools", report: "ScoreReport") -> dict:
    """Pre-fetch pattern library matches for entities in the score report."""
    result = {}
    for eid in report.by_entity:
        patterns = harness.lookup_patterns(eid, k=2)
        if patterns:
            result[eid] = patterns
    return result


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
    # 0) Try ACTION: tag format (Ollama-friendly structured format)
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

    # 2) Try markdown-fenced code blocks (common Ollama pattern)
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

    return None


_INSIGHT_PROMPT = """\
You are a translation-rule extractor. Given the R source, the original broken Python \
translation, and the corrected Python translation, extract 1–3 reusable translation \
rules that would help translate similar R code in the future.

Each rule should:
- Name the R construct (function, idiom, or pattern)
- Describe the correct Python equivalent
- Be concise (1–2 sentences)

Return a JSON array of objects: [{{"name": "rule_name", "guidance": "description"}}]
Return ONLY the JSON array, no other text.

## R source
```r
{r_source}
```

## Original (broken) Python
```python
{original}
```

## Corrected Python
```python
{improved}
```
"""


def extract_insights(
    r_source: str,
    original: str,
    improved: str,
    *,
    model: str = _llm._DEFAULT_MODEL,
) -> list[tuple[str, str]]:
    """Ask the model to articulate reusable translation rules from a successful fix.

    Returns list of (rule_name, guidance_text) tuples.
    """
    user_msg = _INSIGHT_PROMPT.format(
        r_source=r_source, original=original, improved=improved,
    )
    try:
        raw = _llm.call(
            [{"role": "user", "content": user_msg}],
            system="You extract translation rules as JSON.",
            model=model, max_tokens=2048,
        )
    except Exception:
        return []

    raw = raw.strip()
    if raw.startswith("```"):
        m = re.search(r'```(?:json)?\s*\n(.*?)```', raw, re.DOTALL)
        if m:
            raw = m.group(1).strip()

    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        return []

    if not isinstance(items, list):
        return []

    results: list[tuple[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = item.get("name", "")
        guidance = item.get("guidance", "")
        if name and guidance:
            results.append((str(name), str(guidance)))
    return results
