"""Pasted R output check (2026-11-11): numeric literals a candidate adds that equal R's recorded values.

With probes that show R's results (`probe_state`), a model can copy R's output into the Python as literals, and the
LLM review passed such programs (`model-screen-stall2`: textshaping/systemfonts glyph metrics, caret accuracies). This check is
deterministic. A literal counts when its value has at least 4 significant digits (trailing zeros do not count), appears neither in the reference program
(the chain's start) nor in the R script, and equals a number in the script's recorded R ground truth (entity data
and printed output) to the literal's own precision. Only numbers in code count (Python NUMBER tokens), not numbers
inside strings: the review allows an HTML/SVG literal for a package Python lacks, and its coordinates match R's HTML
output (bslib value_box, about 50 per program). Pasted printed output inside a string is left to the LLM review.
Integers are left to it too (2026-11-12): offline, 3+-digit integers found 2 pastes but also matched by chance
(a seed 123 against R's resample indices, 2**24 against a black pixel), and a false rejection repeats on every later
step of its chain.
"""
from __future__ import annotations

import bisect
import io
import json
import math
import re
import tokenize

MIN_SIG = 4
REJECT_AT = 1   # one pasted value is hardcoding (2026-11-12; was 3)
_NUM = re.compile(r"(?<![\w.])-?(?:\d+\.\d+(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+)")


def _sig(lit: str) -> int:
    """Significant digits of the value: leading and trailing zeros carry none (100.00000 has 1)."""
    mant = re.split(r"[eE]", lit.lstrip("-"))[0]
    return len(mant.replace(".", "").strip("0"))


def _half_ulp(lit: str) -> float:
    """Half a unit in the literal's last printed digit."""
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?(?:[eE]([-+]?\d+))?", lit.lstrip("-"))
    return 0.5 * 10.0 ** (int(m.group(3) or 0) - len(m.group(2) or ""))


def truth_numbers(script_map) -> list[float]:
    """Every number in the script's recorded R ground truth, sorted."""
    out = []
    for b in (getattr(script_map, "entity_bundles", {}) or {}).values():
        texts = [getattr(b, "stdout", "") or ""]
        for v in (getattr(b, "data", {}) or {}).values():
            texts.append(v if isinstance(v, str) else json.dumps(v, default=str))
        for t in texts:
            for m in _NUM.findall(t):
                try:
                    x = float(m)
                except ValueError:
                    continue
                if math.isfinite(x):
                    out.append(x)
    return sorted(out)


def _code_numbers(source: str) -> list[str]:
    """Numeric literals in code (a unary minus before one is kept), in order."""
    out, prev = [], None
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.NUMBER:
                out.append(("-" if prev is not None and prev.string == "-" else "") + tok.string)
            if tok.type not in (tokenize.NL, tokenize.COMMENT):
                prev = tok
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return [n for n in out if _NUM.fullmatch(n)]


def pasted(candidate: str, reference: str, r_source: str, truth: list[float]) -> list[str]:
    """The candidate's new numeric literals in code that equal a recorded R value (each literal once)."""
    hits = []
    for lit in dict.fromkeys(_code_numbers(candidate)):
        bare = lit.lstrip("-")
        if _sig(lit) < MIN_SIG or bare in reference or bare in r_source:
            continue
        x, tol = abs(float(lit)), _half_ulp(lit) * (1 + 1e-9)
        for v in (x, -x):
            i = bisect.bisect_left(truth, v - tol)
            if i < len(truth) and truth[i] <= v + tol:
                hits.append(lit)
                break
    return hits


def check(candidate: str, reference: str, r_source: str, script_map) -> "str | None":
    """A rejection reason when the candidate pastes a recorded R value (REJECT_AT or more), else None."""
    hits = pasted(candidate, reference, r_source, truth_numbers(script_map))
    if len(hits) < REJECT_AT:
        return None
    return (f"{len(hits)} numeric literal{'s' if len(hits) > 1 else ''} equal to values R computed for this script "
            f"({', '.join(hits[:5])}{', ...' if len(hits) > 5 else ''}); compute them instead of copying them")
