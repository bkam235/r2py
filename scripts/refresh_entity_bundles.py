"""Re-run R's checkpointed capture for stored script maps and replace their per-entity bundles (2026-10-17).

The checkpoint injection was fixed (statement boundaries, deferred graphics flush, quote escaping); the stored
maps of the scripts it affected still hold the old per-entity bundles (none at all for 34 of 249). Only the
per-entity bundles and types are replaced; everything else in the map is kept.

    python scripts/refresh_entity_bundles.py work/reverify/script_maps STEMS_FILE [--main]

``--main`` also replaces the whole-script values the new run captured (2026-10-18: tag lists are now serialised as
rendered HTML); values only the stored map has (inherited datasets probed separately) are kept.
"""
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def refresh(path: str, main: bool = False) -> str:
    from r2py.stage1.runner import run_script_checkpointed
    f = Path(path)
    sm = pickle.loads(f.read_bytes())
    before = len(sm.entity_bundles or {})
    try:
        full, bundles, types = run_script_checkpointed(sm.source, sm.entities, timeout_s=600)
    except Exception as exc:
        return f"{f.stem}: R failed, kept ({type(exc).__name__})"
    sm.entity_bundles, sm.entity_types = bundles, types
    if main:
        mains = {id(e.actual_bundle): e.actual_bundle for e in sm.entities.values() if getattr(e, "actual_bundle", None) is not None}
        for b in mains.values():
            b.data.update({k: v for k, v in full.data.items() if k in b.data})
    tmp = f.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(sm))
    tmp.replace(f)
    return f"{f.stem}: entity bundles {before} -> {len(bundles)}"


if __name__ == "__main__":
    maps, stems = Path(sys.argv[1]), [s.strip() for s in open(sys.argv[2]) if s.strip()]
    main = "--main" in sys.argv[3:]
    with ProcessPoolExecutor(6) as ex:
        for line in ex.map(refresh, [str(maps / f"{s}.pkl") for s in stems], [main] * len(stems)):
            print(line, flush=True)
