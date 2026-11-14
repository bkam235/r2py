"""Why do GLM's rewrites crash more often than DeepSeek's? (offline, no model calls; reads saved trajectories only)

Follows `rewrite_scope.py` (2026-11-12): same rewrites, same bases. For every candidate that crashed, from its
traceback and the base/candidate diff:
  where      the deepest frame in the script: is its code line new (not in the base) or old; in which entity
             (verified / failing / unscored in the base); innermost frame in a library (site-packages) or the script
  what       exception type; for NameError, is the name defined in the base but not in the candidate (dropped code)
  elision    does the candidate carry a placeholder for omitted code ("... unchanged", "rest as before", a bare ...)
Plus, for every verified candidate: crash rate by rewrite size (share of the base's lines changed), and per chain,
how often a crash follows a crash (does the model fix its own crash from the feedback?).

    python scripts/rewrite_crashes.py screen | full
"""
from __future__ import annotations

import collections
import contextlib
import io
import re
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import rewrite_scope as rs  # noqa: E402
from r2py.stage2.sentinel_mapper import strip_sentinels  # noqa: E402

FRAME = re.compile(r'File "([^"]+)", line \d+, in (\S+)\r?\n(?:\s*\r?\n)?([^\r\n]*)')
EXC = re.compile(r"^(\w+(?:\.\w+)*(?:Error|Exception|Exit|Interrupt|Warning)\w*):?\s*(.*)$", re.M)
ELISION = re.compile(r"^\s*(#.*\b(unchanged|as before|same as (above|before)|omitted|rest of|remains? the same|"
                     r"previous (code|implementation)|existing code)\b.*|\.\.\.|pass\s*#.*)\s*$", re.I | re.M)


def parse(crash: str) -> dict:
    frames = FRAME.findall(crash or "")
    script = [f for f in frames if f[0].endswith("_r2py_script.py")]
    exc = EXC.findall(crash or "")
    return dict(exc=exc[-1][0] if exc else ("timeout" if "imeout" in (crash or "") else "other"),
                msg=exc[-1][1] if exc else "",
                line=script[-1][2].strip() if script else None,
                func=script[-1][1] if script else None,
                in_library=bool(frames) and not frames[-1][0].endswith("_r2py_script.py"))


def defined(name: str, src: str) -> bool:
    n = re.escape(name)
    return bool(re.search(rf"^\s*(def|class)\s+{n}\b|^\s*{n}\s*(:[^=]*)?=[^=]|^\s*(from\s+\S+\s+)?import\s.*\b{n}\b|"
                          rf"\bas\s+{n}\b|^\s*for\s+.*\b{n}\b.*\bin\b", src, re.M))


def classify(row: dict) -> dict:
    p = parse(row["crash"])
    base_lines = {l.strip() for _, l in rs.owned_lines(row["base_src"])}
    owner = None
    if p["line"]:
        for o, l in rs.owned_lines(rs.restore_sentinels(row["base_src"], row["cand_src"])):
            if l.strip() == p["line"]:
                owner = o
                break
    where = ("no script frame" if p["line"] is None else
             "new line" if p["line"] not in base_lines else "old line")
    out = dict(exc=p["exc"], where=where, in_library=p["in_library"],
               elision=bool(ELISION.search(strip_sentinels(row["cand_src"]))))
    out["owner"] = owner
    if p["exc"] in ("NameError", "UnboundLocalError"):
        m = re.search(r"name '([^']+)'|variable '([^']+)'", p["msg"])
        name = m and (m.group(1) or m.group(2))
        out["name_dropped"] = bool(name) and defined(name, row["base_src"]) and not defined(name, row["cand_src"])
    return out


def share(rows, key, val=True) -> str:
    n = sum(1 for r in rows if r.get(key) == val)
    return f"{n:3d}/{len(rows):3d} ({n / len(rows):.0%})" if rows else "  -"


def main(kind: str) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        data = rs.screen()[0] if kind == "screen" else rs.full()
    arms = tuple(data)
    print(f"Crashing rewrites, {kind}: {' vs '.join(arms)}")
    for arm in arms:
        rows = [r for rows in data[arm].values() for r in rows if "crashed" in r]
        crashed = [dict(r, **classify(r)) for r in rows if r["crashed"]]
        print(f"\n== {arm}: {len(crashed)} of {len(rows)} verified candidates crashed ({len(crashed) / len(rows):.0%})")
        print("  exception      ", dict(collections.Counter(c["exc"] for c in crashed).most_common(8)))
        print("  crash line     ", dict(collections.Counter(c["where"] for c in crashed)))
        print("  innermost frame in a library:", share(crashed, "in_library"))
        own = collections.Counter("preamble/helpers" if c["owner"] == rs.PRE else
                                  "unknown" if c["owner"] is None else "entity" for c in crashed)
        print("  crash line owner", dict(own))
        names = [c for c in crashed if "name_dropped" in c]
        print("  Name/UnboundLocal errors whose name the base defines and the candidate dropped:", share(names, "name_dropped"))
        ok = [r for r in rows if not r["crashed"]]
        el = [dict(r, elision=bool(ELISION.search(strip_sentinels(r["cand_src"])))) for r in rows]
        print("  elision marker: crashed", share(crashed, "elision"), " ran", share([e for e in el if not e["crashed"]], "elision"))
        print("  crash rate by share of the base's lines changed:")
        for lo, hi in ((0, .1), (.1, .3), (.3, .6), (.6, 1.01)):
            b = [r for r in rows if lo <= r["base_lines_changed_share"] < hi]
            if b:
                print(f"    [{lo:.1f}, {min(hi, 1):.1f})  {sum(r['crashed'] for r in b):3.0f}/{len(b):3d} "
                      f"({st.mean(r['crashed'] for r in b):.0%})")
        # crash after crash, within a chain (rows are in step order per state; a chain is a (state, branch) run of rows)
        after = collections.Counter()
        for rows_s in data[arm].values():
            prev = {}
            for r in rows_s:
                if "crashed" not in r:
                    continue
                k = r["branch"]
                if r["first"]:
                    prev.pop(k, None)
                if k in prev:
                    after[(prev[k], bool(r["crashed"]))] += 1
                prev[k] = bool(r["crashed"])
        for p in (True, False):
            n = after[(p, True)] + after[(p, False)]
            if n:
                print(f"  after a {'crash' if p else 'run  '}: next candidate crashes {after[(p, True)]}/{n} "
                      f"({after[(p, True)] / n:.0%})")
        for c in [c for c in crashed if c["where"] == "old line"][:3]:
            print("    old-line example:", c["exc"], "|", parse(c["crash"])["line"][:100])


if __name__ == "__main__":
    main(sys.argv[1])
