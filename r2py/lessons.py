"""Lessons learned from the pipeline's own crash-and-fix history (pilot).

A trajectory log (``harness/trajectory.py``) shows, for every agent step, the traceback of the script
it ran and the source that did or did not fix it.  A *pair* is a step whose traceback disappeared in the
next candidate without the score dropping.  The model distils each distinct pair into one lesson (the
libraries it concerns, the symptom, what to do instead); a lesson is kept only because a verified run
followed the fix.  Seeds then get the lessons for the libraries they import, in the seed gate's corrective
turn.  Nothing here is written by hand: the store is rebuilt from trajectories.

    python scripts/mine_lessons.py --arms work/smoke/<arm> ... --out work/lessons/pilot.json
"""
from __future__ import annotations

import ast
import difflib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .harness import trajectory
from .stage2.sentinel_mapper import strip_sentinels

_EXC_RE = re.compile(r"^([A-Za-z_][\w.]*(?:Error|Exception|Exit|Warning))\b:?\s*(.*)$")
MAX_DIFF_LINES = 80
PAIRS_PER_SIGNATURE = 2


@dataclass
class Pair:
    script: str
    traceback: str
    diff: str
    signature: str


@dataclass
class Lesson:
    signature: str
    libs: list[str]
    symptom: str
    lesson: str
    support: int = 1
    scripts: list[str] = field(default_factory=list)


def exception_line(traceback: str) -> str:
    """The line that names the exception ('' when the text holds none)."""
    for line in reversed((traceback or "").replace("\r", "").splitlines()):
        if _EXC_RE.match(line.strip()):
            return line.strip()
    return ""


def signature(traceback: str) -> str:
    """Exception type and message with numbers and quoted object reprs normalised."""
    line = exception_line(traceback)
    line = re.sub(r"0x[0-9a-f]+|\d+", "N", line)
    return line[:110]


def _changed_lines(before: str, after: str) -> str:
    diff = list(difflib.unified_diff(strip_sentinels(before).splitlines(), strip_sentinels(after).splitlines(),
                                     lineterm="", n=1))
    return "\n".join(diff[2:])


def mine_pairs(files: list[Path], exclude_scripts: set[str] = frozenset()) -> list[Pair]:
    """Crash -> fix pairs from trajectory files, at most PAIRS_PER_SIGNATURE per signature (smallest diffs)."""
    found: dict[str, list[Pair]] = {}
    for f in files:
        recs = trajectory.read(f)
        if not recs:
            continue
        script = recs[0].get("script", "")
        if script in exclude_scripts:
            continue
        prev = None   # (source, traceback, aggregate)
        for r in recs:
            if r["kind"] not in ("step", "accepted") or not r.get("source"):
                continue
            tb, agg = r.get("crash") or "", r.get("aggregate") or 0.0
            if prev and signature(prev[1]) and signature(prev[1]) != signature(tb) and agg >= prev[2] \
                    and strip_sentinels(prev[0]) != strip_sentinels(r["source"]):
                diff = _changed_lines(prev[0], r["source"])
                if diff and diff.count("\n") <= MAX_DIFF_LINES:
                    found.setdefault(signature(prev[1]), []).append(Pair(script, prev[1], diff, signature(prev[1])))
            prev = (r["source"], tb, agg)
    out: list[Pair] = []
    for pairs in found.values():
        out += sorted(pairs, key=lambda p: len(p.diff))[:PAIRS_PER_SIGNATURE]
    return out


_DISTILL_SYSTEM = (
    "You write short, reusable lessons for a system that translates R scripts to Python. You are shown a "
    "Python traceback and the lines that were changed to make it go away. Reply with one JSON object and "
    'nothing else: {"libs": [top-level Python modules the lesson concerns, e.g. "lxml", "numpy"], '
    '"symptom": "the error in one line, without file paths", '
    '"lesson": "one or two sentences: what to do instead, as a general rule for any script using these libraries"}. '
    'If the fix is specific to one script (a variable name, a data detail) or concerns no library, reply {"libs": []}.')


def distill(pair: Pair, model: str) -> Lesson | None:
    """One model call per pair; None when the fix is script-specific or the reply is not usable."""
    from .stage2 import llm

    tail = "\n".join(pair.traceback.replace("\r", "").splitlines()[-25:])
    raw = llm.call([{"role": "user", "content": f"Traceback:\n{tail}\n\nChanged lines (unified diff):\n{pair.diff}"}],
                   _DISTILL_SYSTEM, model=model, max_tokens=600)
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        d = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        return None
    libs = [x for x in d.get("libs", []) if isinstance(x, str) and re.fullmatch(r"[A-Za-z_]\w*", x)]
    if not libs or not d.get("lesson") or not d.get("symptom"):
        return None
    return Lesson(pair.signature, libs, str(d["symptom"])[:200], str(d["lesson"])[:400], 1, [pair.script])


def merge(lessons: list[Lesson]) -> list[Lesson]:
    """Lessons with the same signature (several pairs, several scripts) become one with support counted."""
    by: dict[str, Lesson] = {}
    for les in lessons:
        cur = by.get(les.signature)
        if cur is None:
            by[les.signature] = les
        else:
            cur.support += les.support
            cur.scripts = sorted(set(cur.scripts) | set(les.scripts))
            cur.libs = sorted(set(cur.libs) | set(les.libs))
    return sorted(by.values(), key=lambda x: -x.support)


def save(lessons: list[Lesson], path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps([asdict(x) for x in lessons], indent=1), encoding="utf-8")


def load(path: str | Path) -> list[Lesson]:
    return [Lesson(**d) for d in json.loads(Path(path).read_text(encoding="utf-8"))]


def imported_modules(code: str) -> set[str]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return set()
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            mods.add(node.module.split(".")[0])
    return mods


def lessons_for(code: str, lessons: list[Lesson], k: int = 6) -> list[Lesson]:
    """The lessons about libraries this code imports, best supported first."""
    mods = imported_modules(code)
    return [x for x in lessons if mods & set(x.libs)][:k]


def format_lessons(lessons: list[Lesson]) -> str:
    return "\n".join(f"- {x.lesson} (seen as: {x.symptom})" for x in lessons)
