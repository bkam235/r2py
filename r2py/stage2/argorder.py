"""Reorder call arguments so positional ones come before keyword ones.

R accepts ``f(data = d, aes(x, y))``; Python rejects it at parse time ("positional argument
follows keyword argument"), and the translator keeps writing it.  The source does not parse, so
the AST cannot locate the arguments: this works on the token stream instead, which still exists.

It replaces ``stitch.reorder_positional_before_kwargs``, whose text surgery corrupted valid
source (23 ``valid -> invalid`` against 5 real saves over two smoke runs).  The differences:
only calls are touched (not tuples, subscripts, ``def`` or ``class`` parameter lists), arguments
are moved as exact source slices, and a call whose argument list contains a comment is left
alone (a sentinel comment inside it would be lost).  Callers report the repair to the agent
instead of making it silently.
"""
from __future__ import annotations

import io
import keyword
import tokenize

_SKIP = {tokenize.NL, tokenize.COMMENT, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
         tokenize.ENDMARKER}
_NOT_CALLEES = set(keyword.kwlist) - {"True", "False", "None"}
_OPEN, _CLOSE = "([{", ")]}"


def _offsets(source: str) -> list[int]:
    starts, pos = [0], 0
    for line in source.splitlines(keepends=True):
        pos += len(line)
        starts.append(pos)
    return starts


def _arg_kind(toks: list, first: int) -> str:
    """'star' | 'dstar' | 'kw' | 'pos' for the argument starting at token index ``first``."""
    t = toks[first]
    if t.type == tokenize.OP and t.string == "**":
        return "dstar"
    if t.type == tokenize.OP and t.string == "*":
        return "star"
    if t.type == tokenize.NAME:
        j = first + 1
        while j < len(toks) and toks[j].type in _SKIP:
            j += 1
        if j < len(toks) and toks[j].type == tokenize.OP and toks[j].string == "=":
            return "kw"
    return "pos"


def _repair_first(source: str) -> str | None:
    """Fix the first call with a misordered argument list; None if there is nothing to fix."""
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None
    starts = _offsets(source)

    def off(pos: tuple[int, int]) -> int:
        return starts[pos[0] - 1] + pos[1]

    stack: list[dict] = []
    prev = prev2 = None  # last two significant tokens
    for i, t in enumerate(toks):
        if t.type == tokenize.COMMENT:
            for fr in stack:
                fr["comment"] = True
        if t.type in _SKIP:
            continue
        if t.type == tokenize.OP and t.string in _OPEN:
            is_call = False
            if t.string == "(" and prev is not None:
                after_def = prev2 is not None and prev2.type == tokenize.NAME and prev2.string in ("def", "class")
                is_call = (not after_def and (
                    (prev.type == tokenize.NAME and prev.string not in _NOT_CALLEES)
                    or (prev.type == tokenize.OP and prev.string in (")", "]"))))
            if stack:
                _touch(stack[-1], i)
            stack.append({"call": is_call, "comment": False,
                          "args": [{"first": None, "last": None}] if is_call else []})
        elif t.type == tokenize.OP and t.string in _CLOSE:
            if not stack:
                return None
            fr = stack.pop()
            if fr["call"]:
                fixed = _fix_call(source, toks, fr, off)
                if fixed is not None:
                    return fixed
            if stack:
                _touch(stack[-1], i)
        elif t.type == tokenize.OP and t.string == "," and stack and stack[-1]["call"]:
            stack[-1]["args"].append({"first": None, "last": None})
        elif stack:
            _touch(stack[-1], i)
        prev2, prev = prev, t
    return None


def _touch(frame: dict, i: int) -> None:
    if not frame["args"]:
        return
    arg = frame["args"][-1]
    if arg["first"] is None:
        arg["first"] = i
    arg["last"] = i


def _fix_call(source: str, toks: list, fr: dict, off) -> str | None:
    args = [a for a in fr["args"] if a["first"] is not None]  # drops the empty slot after a trailing comma
    if len(args) < 2 or fr["comment"]:
        return None
    kinds = [_arg_kind(toks, a["first"]) for a in args]
    seen_kw = False
    misordered = False
    for k in kinds:
        if k in ("kw", "dstar"):
            seen_kw = True
        elif k == "pos" and seen_kw:
            misordered = True
    if not misordered:
        return None
    texts = [source[off(toks[a["first"]].start):off(toks[a["last"]].end)] for a in args]
    order = ([t for t, k in zip(texts, kinds) if k in ("pos", "star")]
             + [t for t, k in zip(texts, kinds) if k == "kw"]
             + [t for t, k in zip(texts, kinds) if k == "dstar"])
    start = off(toks[args[0]["first"]].start)
    end = off(toks[args[-1]["last"]].end)
    return source[:start] + ", ".join(order) + source[end:]


def repair_argument_order(source: str, max_calls: int = 50) -> tuple[str, int]:
    """Return ``(source, n)``: ``source`` with ``n`` calls' arguments reordered (positional first)."""
    n = 0
    while n < max_calls:
        fixed = _repair_first(source)
        if fixed is None or fixed == source:
            break
        source, n = fixed, n + 1
    return source, n
