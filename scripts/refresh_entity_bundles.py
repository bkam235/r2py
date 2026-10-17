"""Re-run R's checkpointed capture for stored script maps and replace their per-entity bundles (2026-10-17).

The checkpoint injection was fixed (statement boundaries, deferred graphics flush, quote escaping); the stored
maps of the scripts it affected still hold the old per-entity bundles (none at all for 34 of 249). Only the
per-entity bundles and types are replaced; everything else in the map is kept.

    python scripts/refresh_entity_bundles.py work/reverify/script_maps STEMS_FILE
"""
import pickle
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def refresh(path: str) -> str:
    from r2py.stage1.runner import run_script_checkpointed
    f = Path(path)
    sm = pickle.loads(f.read_bytes())
    before = len(sm.entity_bundles or {})
    try:
        _, bundles, types = run_script_checkpointed(sm.source, sm.entities, timeout_s=600)
    except Exception as exc:
        return f"{f.stem}: R failed, kept ({type(exc).__name__})"
    sm.entity_bundles, sm.entity_types = bundles, types
    tmp = f.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(sm))
    tmp.replace(f)
    return f"{f.stem}: entity bundles {before} -> {len(bundles)}"


if __name__ == "__main__":
    maps, stems = Path(sys.argv[1]), [s.strip() for s in open(sys.argv[2]) if s.strip()]
    with ProcessPoolExecutor(6) as ex:
        for line in ex.map(refresh, [str(maps / f"{s}.pkl") for s in stems]):
            print(line, flush=True)
