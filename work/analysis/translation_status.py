"""Show which R scripts have been translated and their highest scores.

Reads from work/analysis/run_history.jsonl (appended by each translate() call).
Shows the best score per script across all runs.

Usage:
    python work/analysis/translation_status.py [--all] [--sort COLUMN] [--asc]

Flags:
    --all       Include untranslated scripts (default: only show translated)
    --sort COL  Sort by: score, name, iterations, entities, runs (default: score)
    --asc       Sort ascending instead of descending
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
INPUTS_DIR = ROOT / "work" / "inputs" / "harvested"
HISTORY_PATH = ROOT / "work" / "analysis" / "run_history.jsonl"


def load_history() -> list[dict]:
    if not HISTORY_PATH.exists():
        return []
    records = []
    for line in HISTORY_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def best_per_script(records: list[dict]) -> dict[str, dict]:
    """Keep the best run (by final_score) per script, plus run count."""
    best: dict[str, dict] = {}
    counts: dict[str, int] = {}
    for r in records:
        name = r["script"]
        counts[name] = counts.get(name, 0) + 1
        prev = best.get(name)
        if prev is None or r.get("final_score", 0) > prev.get("final_score", 0):
            best[name] = r
    for name, row in best.items():
        row["run_count"] = counts[name]
    return best


def collect_status(include_untranslated: bool) -> list[dict]:
    input_scripts = {p.stem for p in INPUTS_DIR.glob("*.R")}
    records = load_history()
    best = best_per_script(records)

    rows = []
    for name, r in best.items():
        by_effect = r.get("by_effect", {})
        rows.append({
            "script": name,
            "translated": True,
            "has_input": name in input_scripts,
            "final_score": r.get("final_score"),
            "data_score": by_effect.get("data"),
            "files_score": by_effect.get("files"),
            "iterations": r.get("iterations"),
            "entity_count": r.get("entity_count", 0),
            "run_count": r.get("run_count", 1),
            "model": r.get("model", ""),
            "timestamp": r.get("timestamp", ""),
        })

    if include_untranslated:
        translated_stems = {r["script"] for r in rows}
        for stem in sorted(input_scripts):
            if stem not in translated_stems:
                rows.append({
                    "script": stem,
                    "translated": False,
                    "has_input": True,
                    "final_score": None,
                    "data_score": None,
                    "files_score": None,
                    "iterations": None,
                    "entity_count": 0,
                    "run_count": 0,
                    "model": "",
                    "timestamp": "",
                })

    return rows


SORT_KEYS = {
    "score": lambda r: (r["final_score"] if r["final_score"] is not None else -1),
    "name": lambda r: r["script"],
    "iterations": lambda r: (r["iterations"] if r["iterations"] is not None else -1),
    "entities": lambda r: r["entity_count"],
    "runs": lambda r: r["run_count"],
}


def fmt(val, width, decimals=3):
    if val is None:
        return "-".rjust(width)
    if isinstance(val, float):
        return f"{val:.{decimals}f}".rjust(width)
    return str(val).rjust(width)


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("No translation history found.")
        return

    header = f"{'Script':<60} {'Score':>7} {'Data':>7} {'Files':>7} {'Iters':>5} {'Ents':>5} {'Runs':>5}"
    print(header)
    print("-" * len(header))
    for r in rows:
        line = f"{r['script']:<60} {fmt(r['final_score'], 7)} {fmt(r['data_score'], 7)} {fmt(r['files_score'], 7)} {fmt(r['iterations'], 5, 0)} {fmt(r['entity_count'] or None, 5, 0)} {fmt(r['run_count'] or None, 5, 0)}"
        print(line)

    translated = [r for r in rows if r["translated"]]
    total_input = sum(1 for r in rows if r["has_input"])
    print()
    print(f"Translated: {len(translated)} / {total_input} input scripts")
    if translated:
        scores = [r["final_score"] for r in translated if r["final_score"] is not None]
        if scores:
            print(f"Score range: {min(scores):.3f} - {max(scores):.3f}  (mean {sum(scores)/len(scores):.3f})")


def main():
    parser = argparse.ArgumentParser(description="R-to-Python translation status table")
    parser.add_argument("--all", action="store_true", help="Include untranslated scripts")
    parser.add_argument("--sort", choices=list(SORT_KEYS), default="score", help="Sort column")
    parser.add_argument("--asc", action="store_true", help="Sort ascending")
    args = parser.parse_args()

    rows = collect_status(include_untranslated=args.all)
    rows.sort(key=SORT_KEYS[args.sort], reverse=not args.asc)
    print_table(rows)


if __name__ == "__main__":
    main()
