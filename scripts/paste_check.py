"""Deterministic check for R output pasted into a translation (2026-10-16).

Pasting R's printed output or computed values as literals was a major flaw in earlier versions of the project:
a translation that hardcodes results scores without computing anything. The harness's hardcoding review is a
model call and can err either way, so this is a fixed check to judge it by. A literal in the candidate counts
only if it matches something R *computed* (a printed line, a value of an entity) and occurs neither in the R
script nor in the Python the candidate was written from (literals R itself writes, like `c(1.5, 2.25)`, are
legitimate in Python too).
"""
from __future__ import annotations

import ast
import json
import re

MIN_LINE = 12        # printed lines shorter than this are too generic to count ("[1] TRUE")
MIN_STRING = 8


def _flatten(v, out: list) -> None:
    if isinstance(v, dict):
        for x in v.values():
            _flatten(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v:
            _flatten(x, out)
    else:
        out.append(v)


def _informative_number(x) -> bool:
    """A number unlikely to be typed by chance: a float with >= 4 significant decimals, or an int >= 10000."""
    if isinstance(x, bool):
        return False
    if isinstance(x, float):
        s = repr(x).split("e")[0]
        return "." in s and len(s.split(".")[1].rstrip("0")) >= 4
    return isinstance(x, int) and abs(x) >= 10000


def r_results(entity_bundles: dict) -> tuple[set[str], set[float], set[str]]:
    """(printed lines, informative numbers, long strings) that R computed, over every entity of the script."""
    from r2py.stage1.runner import strip_echoed_source
    lines, numbers, strings = set(), set(), set()
    for eb in (entity_bundles or {}).values():
        out = strip_echoed_source(getattr(eb, "stdout", "") or "")
        lines |= {l.strip() for l in out.splitlines() if len(l.strip()) >= MIN_LINE}
        vals: list = []
        _flatten(getattr(eb, "data", None) or {}, vals)
        for v in vals:
            if isinstance(v, (int, float)) and _informative_number(v):
                numbers.add(round(float(v), 9))
            elif isinstance(v, str) and len(v) >= MIN_STRING:
                strings.add(v)
    return lines, numbers, strings


def _literals(code: str) -> tuple[list[float], list[str]]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return [], []
    nums, strs = [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
                nums.append(n.value)
            elif isinstance(n.value, str):
                strs.append(n.value)
    return nums, strs


def check(candidate: str, previous: str, r_source: str, entity_bundles: dict) -> dict:
    """Counts of pasted R results in ``candidate`` that are new relative to ``previous`` and absent from ``r_source``."""
    lines, numbers, strings = r_results(entity_bundles)
    prev_nums, prev_strs = _literals(previous)
    prev_num_set = {round(float(x), 9) for x in prev_nums}
    r_text = r_source or ""
    nums, strs = _literals(candidate)
    pasted_numbers = sorted({round(float(x), 9) for x in nums if _informative_number(x)
                             and round(float(x), 9) in numbers and round(float(x), 9) not in prev_num_set
                             and repr(x) not in r_text})
    pasted_lines = sorted({l for l in lines
                           if any(l in s for s in strs) and not any(l in s for s in prev_strs) and l not in r_text})
    pasted_strings = sorted({s for s in strs if s in strings and s not in prev_strs and s not in r_text})
    return {"numbers": len(pasted_numbers), "lines": len(pasted_lines), "strings": len(pasted_strings),
            "examples": [str(x) for x in pasted_numbers[:3]] + pasted_lines[:2] + pasted_strings[:2],
            "pasted": len(pasted_numbers) >= 3 or len(pasted_lines) >= 1 or len(pasted_strings) >= 2}
