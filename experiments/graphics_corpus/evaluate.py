"""Score the graphics corpus with the current comparator and report how well it separates
correct from wrong plots.  Needs neither R nor matplotlib (fingerprints are stored).

    python experiments/graphics_corpus/evaluate.py [-v]

Exit status is 1 if a wrong plot without a documented limitation scores as a pass, or a correct
plot fails -- so the same check can guard changes to the comparator or the extractors.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from r2py.stage4.comparators.graphics import _PASS_THRESHOLD, GraphicsComparator  # noqa: E402

CORPUS = Path(__file__).with_name("corpus.json")


def score_entries(entries: list[dict]) -> list[dict]:
    cmp = GraphicsComparator()
    rows = []
    for e in entries:
        s = cmp.compare([b""] * e["r_pages"], [b""] * e["py_pages"], e["r_meta"], e["py_meta"]).score
        rows.append({**e, "score": s})
    return rows


def auc(pos: list[float], neg: list[float]) -> float:
    """P(a correct plot outscores a wrong one); ties count half."""
    if not pos or not neg:
        return float("nan")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def errors(rows: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """(correct plots that fail, wrong plots that pass, of those the documented limitations)."""
    false_fail = [r for r in rows if r["label"] == "same" and r["score"] < _PASS_THRESHOLD]
    false_pass = [r for r in rows if r["label"] == "different" and r["score"] >= _PASS_THRESHOLD]
    known = [r for r in false_pass if r["limitation"]]
    return false_fail, [r for r in false_pass if not r["limitation"]], known


def report(rows: list[dict], verbose: bool = False) -> str:
    same = [r["score"] for r in rows if r["label"] == "same"]
    diff = [r["score"] for r in rows if r["label"] == "different"]
    false_fail, false_pass, known = errors(rows)
    lines = [f"corpus: {len(rows)} pairs ({len(same)} correct, {len(diff)} wrong), "
             f"pass threshold {_PASS_THRESHOLD}", ""]
    for name, xs in (("correct", same), ("wrong", diff)):
        lines.append(f"{name:8s} n={len(xs):3d} mean={sum(xs) / len(xs):.3f} min={min(xs):.3f} max={max(xs):.3f}")
    lines += ["", f"AUC (correct outscores wrong): {auc(same, diff):.3f}   "
                  f"excluding documented limitations: "
                  f"{auc(same, [r['score'] for r in rows if r['label'] == 'different' and not r['limitation']]):.3f}",
              f"correct plots failing:            {len(false_fail)}/{len(same)}",
              f"wrong plots passing (unexpected): {len(false_pass)}/{len(diff)}",
              f"wrong plots passing (documented limitations): {len(known)}"]
    for title, group in (("CORRECT PLOTS THAT FAIL", false_fail), ("WRONG PLOTS THAT PASS", false_pass),
                         ("KNOWN LIMITATIONS THAT PASS", known)):
        if group:
            lines += ["", title]
            lines += [f"  {r['case']}/{r['variant']}: {r['score']:.3f}"
                      + (f"  ({r['limitation']})" if r["limitation"] else "") for r in group]
    if verbose:
        lines += ["", "ALL"]
        lines += [f"  {r['case']:16s} {r['variant']:22s} {r['label']:9s} {r['score']:.3f}"
                  for r in sorted(rows, key=lambda r: (r["case"], r["label"]))]
    return "\n".join(lines)


def main() -> int:
    rows = score_entries(json.loads(CORPUS.read_text(encoding="utf-8")))
    print(report(rows, verbose="-v" in sys.argv))
    false_fail, false_pass, _ = errors(rows)
    return 1 if (false_fail or false_pass) else 0


if __name__ == "__main__":
    sys.exit(main())
