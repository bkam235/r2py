"""Graphics comparator — compares what pages *plot*, not how they render (§7.3).

Pages are paired in order and compared through their content fingerprints
(``stage0.effects.graphics``): the data behind points/lines/bars, and the text.  Rendered
PNGs are deliberately not compared: SSIM between an R and a matplotlib image measures
white space, not content (an empty axis scored higher than the correct plot, and wrong data
scored the same as right data).  Without fingerprints only the page count is compared.
"""
from __future__ import annotations

import re

from ...types import ComparatorResult, EffectClass

# A page passes only when its content matches (one wrong value in eight must not pass): the
# score stays graded, the verdict is strict.  Chosen on experiments/graphics_corpus.
_PASS_THRESHOLD = 0.99

# Credit for the right values in the wrong order (bars sorted, a line reversed).
_UNORDERED_CREDIT = 0.85

# (weight, ...) of each aspect of a page; data marks dominate, text is a weak signal because R's
# default axis labels are deparsed argument text a translation would not reproduce.
_W_POINTS, _W_BARS, _W_POLYS, _W_SEGS, _W_IMG, _W_TEXT = 3.0, 3.0, 1.0, 0.5, 1.0, 1.0


def _ordered_sim(a: list[float], b: list[float]) -> float:
    """Element-wise closeness of two equal-length sequences, in drawing order."""
    import numpy as np

    a, b = np.asarray(a, float), np.asarray(b, float)
    span = max(a.max(), b.max()) - min(a.min(), b.min())
    if span <= 0:
        return float(np.mean(a == b))
    return float(np.mean(np.clip(1.0 - np.abs(a - b) / (0.1 * span), 0.0, 1.0)))


def _series_sim(a: list[float], b: list[float]) -> float:
    """Like ``_seq_sim`` but drawing order counts: the right values in another order earn only
    ``_UNORDERED_CREDIT``.  Different lengths are order-free (the caller weighs the length gap)."""
    free = _seq_sim(a, b)
    if len(a) != len(b) or not a:
        return free
    return max(_ordered_sim(a, b), _UNORDERED_CREDIT * free)


def _x_sim(r: dict, p: dict) -> float:
    """x positions, allowing a constant shift (R indexes from 1, Python from 0) -- per series
    when both sides drew the same series, otherwise over all vertices."""
    def shifted(a, b):
        return max(_series_sim(a, b), _series_sim(_centred(a), _centred(b)))

    rs, ps = r.get("seg") or [], p.get("seg") or []
    if rs and rs == ps and sum(rs) == len(r["px"]) == len(p["px"]):
        out, i = 0.0, 0
        for n in rs:
            out += n * shifted(r["px"][i:i + n], p["px"][i:i + n])
            i += n
        return out / sum(rs)
    return shifted(r["px"], p["px"])


def _seq_sim(a: list[float], b: list[float]) -> float:
    """Similarity of two multisets of numbers in [0, 1]: order-free, tolerant of small error.
    Different lengths are compared on a common quantile grid; callers weigh the length gap."""
    import numpy as np

    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    a, b = np.sort(np.asarray(a, float)), np.sort(np.asarray(b, float))
    n = min(len(a), len(b))
    if len(a) != n:
        a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a)
    if len(b) != n:
        b = np.interp(np.linspace(0, len(b) - 1, n), np.arange(len(b)), b)
    span = max(a.max(), b.max()) - min(a.min(), b.min())
    if span <= 0:
        close = float(np.mean(a == b))
    else:
        close = float(np.mean(np.clip(1.0 - np.abs(a - b) / (0.1 * span), 0.0, 1.0)))
    return close


def _centred(a: list[float]) -> list[float]:
    m = sum(a) / len(a) if a else 0.0
    return [v - m for v in a]


def _ratio(a: float, b: float) -> float:
    return 1.0 if a == b else min(a, b) / max(a, b)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


# R fills in axis labels and titles from the deparsed call ("c(1, 2)", "1:10", "Histogram of x")
# or a stock word; a translation would not reproduce those, so they are not counted as content.
_DEFAULT_LABEL = re.compile(r"[()\[\]$:^]|^histogram of |^(index|x|y|frequency|density|count)$", re.I)


def _texts(fp: dict, drop_defaults: bool = False) -> set[str]:
    labels = [fp.get("title", ""), fp.get("xlab", ""), fp.get("ylab", "")]
    if drop_defaults:
        labels = [t for t in labels if not _DEFAULT_LABEL.search(str(t))]
    return {_norm(t) for t in labels + list(fp.get("texts") or []) if _norm(t)}


def _page_score(r: dict, p: dict) -> float:
    """Score one R page against one Python page from their fingerprints."""
    parts: list[tuple[float, float]] = []

    r_pts, p_pts = bool(r.get("py")), bool(p.get("py"))
    if r_pts or p_pts:
        if r_pts and p_pts:
            # x also up to a constant shift: R indexes from 1, Python from 0.
            s = 0.5 * _x_sim(r, p) + 0.5 * _series_sim(r["py"], p["py"])
            s *= _ratio(len(r["py"]), len(p["py"]))
        else:
            s = 0.0
        parts.append((_W_POINTS if r_pts else 1.0, s))

    r_bars, p_bars = bool(r.get("bars")), bool(p.get("bars"))
    if r_bars or p_bars:
        s = (_series_sim(r["bars"], p["bars"]) * _ratio(len(r["bars"]), len(p["bars"]))
             if r_bars and p_bars else 0.0)
        parts.append((_W_BARS if r_bars else 1.0, s))

    for key, w in (("n_polys", _W_POLYS), ("n_segs", _W_SEGS), ("n_img", _W_IMG)):
        rn, pn = r.get(key, 0), p.get(key, 0)
        if rn or pn:
            parts.append((w, _ratio(rn, pn)))

    r_text = _texts(r, drop_defaults=True)
    if r_text:
        parts.append((_W_TEXT, len(r_text & _texts(p)) / len(r_text)))

    if not parts:
        return 1.0  # nothing plotted on either side
    return sum(w * s for w, s in parts) / sum(w for w, _ in parts)


class GraphicsComparator:
    effect_class = EffectClass.GRAPHICS

    def compare(self, r_effect: list[bytes], py_effect: list[bytes],
                r_meta: list | None = None, py_meta: list | None = None) -> ComparatorResult:
        n_r = len(r_meta) if r_meta else len(r_effect)
        n_p = len(py_meta) if py_meta else len(py_effect)
        if n_r == 0 and n_p == 0:
            return ComparatorResult(effect_class=EffectClass.GRAPHICS, score=1.0, verdict="pass")
        if n_r == 0 or n_p == 0:
            return self._fail(0.0, f"figure count differs: R={n_r} Python={n_p}")

        scores: list[float] = []
        if r_meta and py_meta:
            # Pair pages in order; a page with no fingerprint on either side cannot be
            # judged and is left out rather than guessed at.
            for i in range(max(n_r, n_p)):
                if i >= min(n_r, n_p):
                    scores.append(0.0)  # a page only one side produced
                    continue
                rf, pf = r_meta[i], py_meta[i]
                if rf is not None and pf is not None:
                    scores.append(_page_score(rf, pf))
        if not scores:
            # No fingerprints to judge by: the page count is all that can be compared.
            score = _ratio(n_r, n_p)
            if score >= _PASS_THRESHOLD:
                return ComparatorResult(effect_class=EffectClass.GRAPHICS, score=score, verdict="pass")
            return self._fail(score, f"figure count differs: R={n_r} Python={n_p}")

        score = sum(scores) / len(scores)
        if score >= _PASS_THRESHOLD:
            return ComparatorResult(effect_class=EffectClass.GRAPHICS, score=score, verdict="pass")
        expl = f"plotted content similarity {score:.3f} < {_PASS_THRESHOLD}"
        if n_r != n_p:
            expl += f" (figure count differs: R={n_r} Python={n_p})"
        return self._fail(score, expl)

    @staticmethod
    def _fail(score: float, explanation: str) -> ComparatorResult:
        return ComparatorResult(effect_class=EffectClass.GRAPHICS, score=score, verdict="fail",
                                explanation=explanation, failure_tag="value")
