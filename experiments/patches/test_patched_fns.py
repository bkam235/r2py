"""Functional test of the patched agent.py behaviour, in isolation.

Pulls the relevant functions out of the ORIGINAL and PATCHED agent.py by AST and
execs them in a bare namespace, so nothing imports r2py or touches the live tree.

Asserts:
  * _check_syntax now reports the offending source line (patch 02)
  * _parse_action is byte-identical to the original (patch 03 changes no parser)
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENT = Path("r2py") / "harness" / "agent.py"
WANT_FN = {"_check_syntax", "_parse_action"}
WANT_ASSIGN_RE = re.compile(r"^(_\w+_RE|CATASTROPHIC_DROP)$")


def load(path: Path) -> tuple[dict, dict[str, str]]:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    keep: list[ast.stmt] = []
    sources: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in WANT_FN:
            keep.append(node)
            sources[node.name] = ast.get_source_segment(src, node) or ""
        elif isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and WANT_ASSIGN_RE.match(t.id) for t in node.targets
        ):
            keep.append(node)
    ns: dict = {"ast": ast, "re": re, "json": __import__("json")}
    exec(compile(ast.Module(body=keep, type_ignores=[]), str(path), "exec"), ns)
    return ns, sources


old, old_src = load(HERE / "orig" / AGENT)
new, new_src = load(HERE / "new" / AGENT)
fails: list[str] = []


def check(label: str, got, expected) -> None:
    ok = expected(got) if callable(expected) else got == expected
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if not ok:
        print(f"          got: {got!r}")
        fails.append(label)


print("=== patch 03 must not touch the parser ===")
check("_parse_action source identical", new_src["_parse_action"] == old_src["_parse_action"], True)

print("\n=== _check_syntax: valid code still passes ===")
for name, mod in (("old", old), ("new", new)):
    check(f"{name}: valid -> None", mod["_check_syntax"]("import os\nx = 1\n"), None)
    check(f"{name}: valid class/def -> None",
          mod["_check_syntax"]("def f(a, b=2):\n    return a + b\n"), None)

print("\n=== _check_syntax: reserved keyword as kwarg ===")
bad = "import os\nresult = foo(from=1, to=2)\nprint(result)\n"
check("old: message only, no source shown",
      old["_check_syntax"](bad), lambda g: "invalid syntax" in g and "from=1" not in g)
check("new: shows offending line + caret",
      new["_check_syntax"](bad), lambda g: "from=1" in g and "^" in g)
print(f"        old -> {old['_check_syntax'](bad)!r}")
print(f"        new -> {new['_check_syntax'](bad)!r}")

print("\n=== _check_syntax: f-string backslash (CPython 3.10 only) ===")
fs = 'lines = f"{ text.split(chr(92) + \'n\') }"\n'
fs_bad = 'lines = f"{ text.split(\'\\\\n\') }"\n'
got_old, got_new = old["_check_syntax"](fs_bad), new["_check_syntax"](fs_bad)
check("new: reports f-string backslash", got_new, lambda g: g and "backslash" in g)
check("new: shows the source line", got_new, lambda g: g and "split" in g)
print(f"        new -> {got_new!r}")

print("\n=== _check_syntax: unterminated string ===")
check("new: reports and shows line",
      new["_check_syntax"]('x = "abc\ny = 2\n'), lambda g: g and ("unterminated" in g or "EOL" in g))

print("\n=== _check_syntax: r2py sentinel lines are still stripped ===")
check("new: sentinel-only file parses",
      new["_check_syntax"]("# r2py:entity:e1\nx = 1\n"), None)

print("\n=== parser sanity (identical behaviour, both modules) ===")
cases = {
    "ACTION: rewrite + fence": 'ACTION: rewrite\n```python\nx = 1\n```\n',
    "ACTION: probe_r + r fence": 'ACTION: probe_r\n```r\nlag(1:5)\n```\n',
    "ACTION: done": 'Nothing left.\n\nACTION: done\n',
    "json rewrite": '{"action": "rewrite", "new_source": "x = 1"}',
    "bare python fence": '```python\nimport os\nx = 1\n```\n',
}
for label, raw in cases.items():
    a, b = old["_parse_action"](raw), new["_parse_action"](raw)
    check(f"{label}: old == new", a == b, True)
    print(f"        -> {(b or {}).get('action', None)!r}")

print("\n" + ("FAILURES: " + ", ".join(fails) if fails else "ALL CHECKS PASSED"))
raise SystemExit(1 if fails else 0)
