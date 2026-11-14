"""Census (2026-11-14): programs that import a module name above the first entity sentinel and rebind it later."""
import ast, json, glob, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]; sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import health_report as hr

def rebinds(src):
    try: tree = ast.parse(src)
    except SyntaxError: return []
    lines = src.splitlines()
    first = next((i + 1 for i, l in enumerate(lines) if l.strip().startswith("# r2py:entity:")), None)
    if first is None: return []
    mods = {}
    for n in tree.body:
        if n.lineno >= first: continue
        if isinstance(n, ast.Import):
            for a in n.names: mods[a.asname or a.name.split(".")[0]] = n.lineno
        elif isinstance(n, ast.ImportFrom):
            for a in n.names: mods[a.asname or a.name] = n.lineno   # may be a module or not; checked at run time
    hits = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and getattr(n, "lineno", 0) >= first:
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id in mods: hits.add(t.id)
    return sorted(hits)

def runs(run_dir):
    fin = {}
    for f in sorted(glob.glob(f"{run_dir}/trajectories/*.jsonl")):
        stem = os.path.basename(f).split(".")[0]
        recs = [json.loads(l) for l in open(f, encoding="utf-8")]
        src = hr._final_program(recs) or (hr.SOURCES / f"{stem}.py").read_text(encoding="utf-8")
        h = rebinds(src)
        if h: print(f"  {run_dir} final  {stem}: {h}")

for rd in ["work/dsflash_default", "work/dsflash_heldout"]:
    runs(rd)
n = 0
for p in sorted(hr.SOURCES.glob("*.py")):
    h = rebinds(p.read_text(encoding="utf-8")); n += 1
    if h: print(f"  start  {p.stem}: {h}")
print("starts scanned", n)
