"""Build patch 05: let analyze/status work on a restricted checkpoint set.

Same method as build_patches.py — exact-anchor edits against pristine copies, asserted
unique, AST-validated, emitted as a unified diff. Touches r2py/heldout.py (the experiment
runner, excluded from harness_hash by design) and scripts/run_heldout.py only.
"""
from __future__ import annotations

import ast
import difflib
import shutil
from pathlib import Path

REPO = Path(r"C:\Users\bened\Desktop\r2py_v0.3")
HERE = Path(__file__).resolve().parent
ORIG, NEW = HERE / "orig05", HERE / "new05"
FILES = ["r2py/heldout.py", "scripts/run_heldout.py"]

EDITS: list[tuple[str, str, str]] = [
    # 1) analyze takes an explicit checkpoint list
    (
        "r2py/heldout.py",
        '''def analyze(manifest: dict, scores_path: str | Path, library_dir: str | Path | None = None) -> dict:
''',
        '''def analyze(manifest: dict, scores_path: str | Path, library_dir: str | Path | None = None,
            checkpoints: list[str] | None = None) -> dict:
''',
    ),
    # 2) resolve it once, next to the other locals
    (
        "r2py/heldout.py",
        '''    spec = manifest["protocol"]["primary_test"]
    before, after = spec["before"], spec["after"]
    rows = read_scores(scores_path)
''',
        '''    spec = manifest["protocol"]["primary_test"]
    before, after = spec["before"], spec["after"]
    # Which checkpoints this analysis covers. Defaults to the manifest, but a run that
    # scored only a subset must say so: _trend keeps a checkpoint as soon as ANY row
    # mentions it, then keeps only scripts present in EVERY one — so leftover rows from a
    # dropped checkpoint would silently shrink the trend's n instead of being ignored.
    order_all = [c for c in (checkpoints or manifest["checkpoints"]) if c in manifest["checkpoints"]]
    rows = read_scores(scores_path)
    rows = [r for r in rows if r["checkpoint"] in order_all]
''',
    ),
    # 3) secondary trend
    (
        "r2py/heldout.py",
        '''            "trend": _trend(script_means, list(manifest["checkpoints"])),
''',
        '''            "trend": _trend(script_means, order_all),
''',
    ),
    # 4) primary trend
    (
        "r2py/heldout.py",
        '''    order = [c for c in manifest["checkpoints"] if c in ent_means]
''',
        '''    order = [c for c in order_all if c in ent_means]
''',
    ),
    # 5) record what was analysed, so the report cannot be misread later
    (
        "r2py/heldout.py",
        '''        "n_heldout": len(manifest["heldout"]),
''',
        '''        "n_heldout": len(manifest["heldout"]),
        "checkpoints_analyzed": order_all,
''',
    ),
    # 6) progress(): same restriction, so status shows the right denominator
    (
        "r2py/heldout.py",
        '''def progress(manifest: dict, workdir: str | Path) -> dict:
''',
        '''def progress(manifest: dict, workdir: str | Path, checkpoints: list[str] | None = None) -> dict:
''',
    ),
    (
        "r2py/heldout.py",
        '''    checkpoints = list(manifest["checkpoints"])
''',
        '''    checkpoints = [c for c in (checkpoints or manifest["checkpoints"])
                   if c in manifest["checkpoints"]]
''',
    ),
    (
        "r2py/heldout.py",
        '''            "done": len({(r["checkpoint"], r["script"], r["rep"]) for r in s_rows}),
''',
        '''            "done": len({(r["checkpoint"], r["script"], r["rep"]) for r in s_rows
                         if r["checkpoint"] in checkpoints}),
''',
    ),
    (
        "r2py/heldout.py",
        '''                              for c, v in by_cp.items() if c in manifest["checkpoints"]},
''',
        '''                              for c, v in by_cp.items() if c in checkpoints},
''',
    ),
    # 7) CLI: --checkpoints on analyze and status
    (
        "scripts/run_heldout.py",
        '''    sub.add_parser("analyze", help="run the pre-specified tests on scores.jsonl")

    sub.add_parser("status", help="show training and scoring progress")
''',
        '''    p = sub.add_parser("analyze", help="run the pre-specified tests on scores.jsonl")
    p.add_argument("--checkpoints", nargs="+", default=None,
                   help="restrict the analysis to these checkpoints "
                        "(default: every checkpoint in the manifest)")

    p = sub.add_parser("status", help="show training and scoring progress")
    p.add_argument("--checkpoints", nargs="+", default=None,
                   help="restrict progress to these checkpoints")
''',
    ),
    (
        "scripts/run_heldout.py",
        '''        result = ho.analyze(manifest, workdir / "scores.jsonl", workdir / "checkpoints" / "full")
''',
        '''        result = ho.analyze(manifest, workdir / "scores.jsonl", workdir / "checkpoints" / "full",
                            checkpoints=args.checkpoints)
''',
    ),
    (
        "scripts/run_heldout.py",
        '''        print(ho.format_progress(ho.progress(manifest, workdir)))
''',
        '''        print(ho.format_progress(ho.progress(manifest, workdir, args.checkpoints)))
''',
    ),
]


def main() -> int:
    for d in (ORIG, NEW):
        if d.exists():
            shutil.rmtree(d)
    for rel in FILES:
        for d in (ORIG, NEW):
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / rel, d / rel)

    for rel, old, new in EDITS:
        path = NEW / rel
        src = path.read_text(encoding="utf-8")
        n = src.count(old)
        if n != 1:
            raise SystemExit(f"{rel}: anchor matched {n} times, expected 1\n--- anchor ---\n{old}")
        path.write_text(src.replace(old, new), encoding="utf-8")

    chunks: list[str] = []
    for rel in FILES:
        before = (ORIG / rel).read_text(encoding="utf-8")
        after = (NEW / rel).read_text(encoding="utf-8")
        try:
            ast.parse(after)
        except SyntaxError as exc:
            raise SystemExit(f"{rel} no longer parses: line {exc.lineno}: {exc.msg}")
        chunks.extend(difflib.unified_diff(
            before.splitlines(keepends=True), after.splitlines(keepends=True),
            fromfile=f"a/{rel}", tofile=f"b/{rel}", n=3))
    out = HERE / "05-analyze-restricted-checkpoints.patch"
    out.write_text("".join(chunks), encoding="utf-8")
    added = sum(1 for l in chunks if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in chunks if l.startswith("-") and not l.startswith("---"))
    print(f"{out.name}   {', '.join(FILES)}   +{added} -{removed}")
    print("both files parse")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
