"""Record the R row names of the inherited data frames in stored script maps (2026-11-21, `data_row_names`).

R's data capture keeps a data frame's columns only, so the data shim handed mtcars to Python without its car names
and a translation could only paste them (purrr attr_getter, threshold-095-e16 audit). Stage 1 now probes them
(`r2py.stage1.probe_row_names`); this adds them to maps captured before. Candidates: the data shim's names whose
captured value is a data frame and that no entity defines (built-in and package datasets). Nothing else in a map
changes; a map is rewritten only when its row names change.

    python scripts/refresh_row_names.py work/reverify/script_maps [--dry-run]
"""
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _is_frame(v) -> bool:
    return (isinstance(v, dict) and bool(v) and all(isinstance(c, list) for c in v.values())
            and len({len(c) for c in v.values()}) == 1)


def refresh(path: str, dry: bool = False) -> str:
    from r2py.stage1 import probe_row_names
    from r2py.stage2.stitch import collect_shim_needed_names
    from r2py.stage4.verifier import get_r_bundle
    from r2py.types import EntityKind
    f = Path(path)
    sm = pickle.loads(f.read_bytes())
    data = getattr(get_r_bundle(sm), "data", {}) or {}
    names = {n for n in collect_shim_needed_names(sm) if n not in sm.entities and _is_frame(data.get(n))}
    if not names:
        return ""
    pkgs = [e.package for e in sm.entities.values() if e.kind == EntityKind.LIBRARY_IMPORT and e.package]
    new = probe_row_names(names, 300, packages=pkgs)
    old = getattr(sm, "data_row_names", None) or {}
    if new == old:
        return f"{f.stem}: {sorted(names)} unchanged"
    if not dry:
        sm.data_row_names = new
        tmp = f.with_suffix(".tmp")
        tmp.write_bytes(pickle.dumps(sm))
        tmp.replace(f)
    return f"{f.stem}: {sorted(names)} -> " + ", ".join(f"{k} {len(v)} ({v[:2]})" for k, v in sorted(new.items()))


if __name__ == "__main__":
    d, dry = Path(sys.argv[1]), "--dry-run" in sys.argv
    files = sorted(str(p) for p in d.glob("*.pkl"))
    with ProcessPoolExecutor(6) as ex:
        for line in ex.map(refresh, files, [dry] * len(files)):
            if line:
                print(line, flush=True)
