"""Build the labelled graphics corpus: R plots paired with equivalent and mutated Python plots.

Each *case* is one R snippet.  Its Python variants are labelled ``same`` (a correct translation,
however styled) or ``different`` (a wrong one: wrong data, wrong chart type, missing points,
empty, wrong labels).  Both sides are run through the real sandboxes and only the resulting
fingerprints are stored, so evaluating a comparator needs neither R nor matplotlib:

    python experiments/graphics_corpus/build_corpus.py     # slow: runs R and Python
    python experiments/graphics_corpus/evaluate.py         # fast: scores corpus.json

A variant with a ``limitation`` note is a wrong plot the comparator is *known* unable to tell
apart (it compares order-free multisets, and treats labels as a weak signal); it is kept so the
report shows the gap instead of hiding it.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from r2py.stage0.sandbox.py_sandbox import PySandbox  # noqa: E402
from r2py.stage0.sandbox.r_sandbox import RSandbox  # noqa: E402
from r2py.types import EffectClass  # noqa: E402

OUT = Path(__file__).with_name("corpus.json")
CAP = frozenset({EffectClass.GRAPHICS})
MPL = "import matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nimport numpy as np\n"
GG = "suppressPackageStartupMessages(library(ggplot2))\n"

XS = [1, 2, 3, 4, 5, 6, 7, 8]
YS = [2.0, 3.5, 1.0, 7.0, 4.5, 9.0, 6.0, 8.5]
BARS = [3, 7, 2, 9, 4]
HIST = [1.2, 1.7, 2.2, 2.4, 2.6, 3.1, 3.3, 3.4, 3.8, 4.4]
EDGES = [1, 2, 3, 4, 5]

ORDER = "same multiset of values, wrong order"
LABELS = "labels are the only difference"


def v(xs):
    return "[" + ",".join(repr(x) for x in xs) + "]"


def c(xs):
    return "c(" + ",".join(repr(x) for x in xs) + ")"


def perturbed(ys):          # last value far off
    return ys[:-1] + [ys[-1] * 3 + 5]


def dropped(ys):            # half the points missing
    return ys[: len(ys) // 2]


def cases():
    """(case name, R source, {variant: (Python source, label[, limitation note])})"""
    yield "line", f"plot({c(XS)}, {c(YS)}, type='l')", {
        "correct": (f"plt.plot({v(XS)}, {v(YS)})", "same"),
        "as_markers": (f"plt.plot({v(XS)}, {v(YS)}, 'o-', color='red', lw=3)", "same"),
        "zero_based_x": (f"plt.plot({v([x - 1 for x in XS])}, {v(YS)})", "same"),
        "float_noise": (f"plt.plot({v(XS)}, {v([y + 1e-9 for y in YS])})", "same"),
        "one_value_off": (f"plt.plot({v(XS)}, {v(perturbed(YS))})", "different"),
        "half_points": (f"plt.plot({v(XS[:4])}, {v(dropped(YS))})", "different"),
        "y_equals_x": (f"plt.plot({v(XS)}, {v(XS)})", "different"),
        "as_bars": (f"plt.bar({v(XS)}, {v(YS)})", "different"),
        "empty": ("plt.plot([])", "different"),
        "y_reversed_in_order": (f"plt.plot({v(XS)}, {v(YS[::-1])})", "different", ORDER),
    }
    yield "scatter", f"plot({c(XS)}, {c(YS)})", {
        "correct": (f"plt.scatter({v(XS)}, {v(YS)})", "same"),
        "as_line": (f"plt.plot({v(XS)}, {v(YS)}, 'o')", "same"),
        "one_value_off": (f"plt.scatter({v(XS)}, {v(perturbed(YS))})", "different"),
        "swapped_axes": (f"plt.scatter({v(YS)}, {v(XS)})", "different"),
        "empty": ("plt.scatter([], [])", "different"),
    }
    yield "barplot", f"barplot({c(BARS)})", {
        "correct": (f"plt.bar(range({len(BARS)}), {v(BARS)})", "same"),
        "styled": (f"plt.bar(range({len(BARS)}), {v(BARS)}, color='green', width=0.4)", "same"),
        "one_bar_off": (f"plt.bar(range({len(BARS)}), {v(perturbed(BARS))})", "different"),
        "sorted": (f"plt.bar(range({len(BARS)}), {v(sorted(BARS))})", "different", ORDER),
        "missing_bar": (f"plt.bar(range({len(BARS) - 1}), {v(BARS[:-1])})", "different"),
        "as_line": (f"plt.plot({v(BARS)})", "different"),
    }
    yield "hist", f"hist({c(HIST)}, breaks={c(EDGES)})", {
        "correct": (f"plt.hist({v(HIST)}, bins={v(EDGES)})", "same"),
        "wrong_bins": (f"plt.hist({v(HIST)}, bins=[1, 3, 5])", "different"),
        "wrong_data": (f"plt.hist({v([h + 1 for h in HIST])}, bins={v(EDGES)})", "different"),
    }
    yield "two_figures", f"plot({c(YS)}); plot({c(YS[::-1])})", {
        "correct": (f"plt.figure(); plt.plot({v(YS)}); plt.figure(); plt.plot({v(YS[::-1])})", "same"),
        "one_figure_missing": (f"plt.plot({v(YS)})", "different"),
        "second_wrong": (f"plt.figure(); plt.plot({v(YS)}); plt.figure(); plt.plot({v(perturbed(YS))})",
                         "different"),
        "extra_figure": (f"plt.figure(); plt.plot({v(YS)}); plt.figure(); plt.plot({v(YS[::-1])}); "
                         f"plt.figure(); plt.plot({v(YS)})", "different"),
    }
    yield "panels", f"par(mfrow=c(1,2)); plot({c(YS)}); plot({c(XS)}, {c(YS)})", {
        "correct": (f"f, a = plt.subplots(1, 2); a[0].plot({v(YS)}); a[1].plot({v(XS)}, {v(YS)})", "same"),
        "one_panel_wrong": (f"f, a = plt.subplots(1, 2); a[0].plot({v(YS)}); "
                            f"a[1].plot({v(XS)}, {v(perturbed(YS))})", "different"),
    }
    yield "labelled", f"plot({c(XS)}, {c(YS)}, main='Growth', xlab='Week', ylab='Height (cm)')", {
        "correct": (f"plt.plot({v(XS)}, {v(YS)}); plt.title('Growth'); plt.xlabel('Week'); "
                    "plt.ylabel('Height (cm)')", "same"),
        "no_labels": (f"plt.plot({v(XS)}, {v(YS)})", "different", LABELS),
        "wrong_labels": (f"plt.plot({v(XS)}, {v(YS)}); plt.title('Decline'); plt.xlabel('Day'); "
                         "plt.ylabel('Weight')", "different", LABELS),
    }
    yield "curve", "curve(sin, 0, pi)", {
        "correct": ("x = np.linspace(0, np.pi, 101); plt.plot(x, np.sin(x))", "same"),
        "cosine": ("x = np.linspace(0, np.pi, 101); plt.plot(x, np.cos(x))", "different"),
    }
    yield "gg_point", GG + f"print(ggplot(data.frame(x={c(XS)}, y={c(YS)}), aes(x, y)) + geom_point())", {
        "correct": (f"plt.scatter({v(XS)}, {v(YS)})", "same"),
        "one_value_off": (f"plt.scatter({v(XS)}, {v(perturbed(YS))})", "different"),
        "empty": ("plt.scatter([], [])", "different"),
    }
    yield "gg_col", GG + (f"print(ggplot(data.frame(x=factor(1:{len(BARS)}), y={c(BARS)}), "
                          "aes(x, y)) + geom_col())"), {
        "correct": (f"plt.bar(range({len(BARS)}), {v(BARS)})", "same"),
        "one_bar_off": (f"plt.bar(range({len(BARS)}), {v(perturbed(BARS))})", "different"),
        "as_scatter": (f"plt.scatter(range({len(BARS)}), {v(BARS)})", "different"),
    }
    yield "gg_line_titled", GG + (f"print(ggplot(data.frame(x={c(XS)}, y={c(YS)}), aes(x, y)) + "
                                  "geom_line() + ggtitle('Growth'))"), {
        "correct": (f"plt.plot({v(XS)}, {v(YS)}); plt.title('Growth')", "same"),
        "one_value_off": (f"plt.plot({v(XS)}, {v(perturbed(YS))}); plt.title('Growth')", "different"),
    }


def fingerprints(sandbox, src: str) -> tuple[list, int]:
    with tempfile.TemporaryDirectory() as d:
        b = sandbox.run(src, workdir=Path(d), capture=CAP, timeout_s=180)
    return b.graphics_meta, len(b.graphics)


def main() -> None:
    entries = []
    for case, r_src, variants in cases():
        print(f"[{case}] R", flush=True)
        r_meta, r_pages = fingerprints(RSandbox(), r_src)
        for name, spec in variants.items():
            py_src, label = spec[0], spec[1]
            note = spec[2] if len(spec) > 2 else ""
            py_meta, py_pages = fingerprints(PySandbox(), MPL + py_src)
            entries.append({
                "case": case, "variant": name, "label": label, "limitation": note,
                "r_meta": r_meta, "py_meta": py_meta, "r_pages": r_pages, "py_pages": py_pages,
            })
            print(f"   {name:22s} {label:9s} R={r_pages}/{len(r_meta)} Py={py_pages}/{len(py_meta)}",
                  flush=True)
    OUT.write_text(json.dumps(entries, indent=1), encoding="utf-8")
    print(f"wrote {len(entries)} entries -> {OUT}")


if __name__ == "__main__":
    main()
