# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/pROC__rd_example__coords_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'pROC__rd_example__coords_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['aSAH']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(pROC))

# r2py:entity:import_pROC
# library(pROC) -- reimplemented below

# r2py:entity:data
# data(aSAH) -- aSAH is provided by the shim

# ---------------------------------------------------------------------------
# Minimal reimplementation of the pROC API
# ---------------------------------------------------------------------------
_VALID_COORDS = ["specificity", "sensitivity", "accuracy", "tn", "tp", "fn", "fp",
                 "npv", "ppv", "fdr", "fpr", "tpr", "tnr", "fnr",
                 "1-specificity", "1-sensitivity", "1-accuracy", "1-npv", "1-ppv",
                 "precision", "recall", "lr_pos", "lr_neg", "youden",
                 "closest.topleft"]

_DECREASING = {"sensitivity", "tpr", "recall", "1-specificity", "fpr"}

_ALIASES = {"t": "threshold", "topleft": "closest.topleft",
            "npe": "1-npv", "ppe": "1-ppv", "se": "sensitivity",
            "sp": "specificity"}


def _match_arg(x, candidates):
    if x in candidates:
        return x
    hits = [c for c in candidates if c.startswith(x)]
    if not hits:
        raise ValueError("'arg' should be one of " + ", ".join(candidates))
    return hits[0]


def _match_ret(ret):
    if isinstance(ret, str):
        ret = [ret]
    ret = list(ret)
    if "all" in ret:
        return ["threshold"] + list(_VALID_COORDS)
    out = []
    for r in ret:
        r = _ALIASES.get(r, r)
        out.append("threshold" if r == "threshold" else _match_arg(r, _VALID_COORDS))
    return out


def _safe(v):
    """Plain JSON-friendly float (None for non-finite)."""
    v = float(v)
    if not np.isfinite(v):
        return None
    return v


# --- R-style output helpers -------------------------------------------------
def _fmt(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if not np.isfinite(v):
        return "NA"
    return f"{v:.7g}"


def _fmt6(x):
    v = float(x)
    if not np.isfinite(v):
        return "NA"
    return f"{v:.6f}"


def print_df(df):
    """Approximate R's print.data.frame layout."""
    labels = [str(i) for i in df.index]
    names = [str(c) for c in df.columns]
    cell = [[_fmt(df.iat[r, c]) for c in range(len(names))] for r in range(len(df))]
    lblw = max([len(l) for l in labels] + [0])
    widths = [max([len(names[j])] + [len(cell[r][j]) for r in range(len(df))])
              for j in range(len(names))]
    avail = max(80 - lblw - 1, 20)
    groups = []
    cur = []
    curw = 0
    for j in range(len(names)):
        add = widths[j] + (1 if cur else 0)
        if cur and curw + add > avail:
            groups.append(cur)
            cur = [j]
            curw = widths[j]
        else:
            cur.append(j)
            curw += add
    if cur:
        groups.append(cur)
    out = []
    for g in groups:
        out.append(" " * lblw + " " +
                   " ".join(names[j].rjust(widths[j]) for j in g))
        for r in range(len(df)):
            out.append(labels[r].rjust(lblw) + " " +
                       " ".join(cell[r][j].rjust(widths[j]) for j in g))
    print("\n".join(out))


def print_vector(v):
    vals = [_fmt6(x) for x in np.asarray(v, dtype=float).ravel()]
    if not vals:
        return
    width = max(len(s) for s in vals)
    nlab = len(str(len(vals)))
    lines = []
    for start in range(0, len(vals), 6):
        chunk = vals[start:start + 6]
        lab = f"[{start + 1}]".rjust(nlab + 2)
        lines.append(lab + " " + " ".join(s.rjust(width) for s in chunk))
    print("\n".join(lines))


# --- pROC core ---------------------------------------------------------------
def _roc_impl(response, predictor, percent=True):
    """pROC::roc(response, predictor, percent=...) (algorithm 2)."""
    y = np.asarray(response)
    x = np.asarray(predictor, dtype=float)
    yv = y.astype(str)
    levs = np.array(sorted(pd.unique(yv)))
    controls = x[yv == levs[0]]
    cases = x[yv == levs[1]]
    neg = bool((np.median(cases) - np.median(controls)) < 0)
    direction = "<" if neg else ">"
    c_ = -controls if neg else controls.copy()
    k_ = -cases if neg else cases.copy()

    vals = np.unique(np.concatenate([c_, k_]))
    mids = (vals[:-1] + vals[1:]) / 2.0
    th = np.concatenate(([-np.inf], mids, [np.inf]))

    scale = 100.0 if percent else 1.0
    kk = np.sort(k_)
    cc = np.sort(c_)
    se = np.asarray((len(kk) - np.searchsorted(kk, th, side="right"))
                    / len(kk) * scale, dtype=float)
    sp = np.asarray(np.searchsorted(cc, th, side="right") / len(cc) * scale,
                    dtype=float)

    return {
        "class": ["roc"],
        "__r2py_fp__": True,
        "numbers": {
            "sensitivities": [_safe(v) for v in se],
            "specificities": [_safe(v) for v in sp],
            "thresholds": [_safe(v) for v in th],
            "cases": [_safe(v) for v in k_],
            "controls": [_safe(v) for v in c_],
        },
        "strings": {"direction": direction},
        "se": [float(v) for v in se],
        "sp": [float(v) for v in sp],
        "th": [float(v) for v in th],
        "controls": [float(v) for v in c_],
        "cases": [float(v) for v in k_],
        "percent": bool(percent),
        "neg": neg,
        "is_smooth": False,
    }


def smooth(rocr, n=512):
    """pROC::smooth.roc, default binormal method."""
    scale = 100.0 if rocr["percent"] else 1.0
    sp = norm.ppf(np.asarray(rocr["sp"], dtype=float) / scale)
    se = norm.ppf(np.asarray(rocr["se"], dtype=float) / scale)
    keep = np.isfinite(sp) & np.isfinite(se)
    sp, se = sp[keep], se[keep]
    A = np.vstack([se, np.ones_like(se)]).T
    coef = np.linalg.lstsq(A, sp, rcond=None)[0]
    se_new = norm.ppf(np.linspace(0.0, 1.0, n))
    sens = norm.cdf(se_new) * scale
    spec = norm.cdf(coef[0] * se_new + coef[1]) * scale
    order = np.argsort(spec, kind="stable")
    sens = np.asarray(sens[order], dtype=float)
    spec = np.asarray(spec[order], dtype=float)
    th = np.full(n, np.nan)
    return {
        "class": ["smooth.roc"],
        "__r2py_fp__": True,
        "numbers": {
            "sensitivities": [_safe(v) for v in sens],
            "specificities": [_safe(v) for v in spec],
        },
        "strings": {"direction": rocr["strings"]["direction"]},
        "se": [float(v) for v in sens],
        "sp": [float(v) for v in spec],
        "th": [float("nan")] * n,
        "controls": list(rocr["controls"]),
        "cases": list(rocr["cases"]),
        "percent": rocr["percent"],
        "neg": rocr["neg"],
        "is_smooth": True,
    }


def _all_columns(th, se, sp, rocr, weights=(1, 0.5)):
    """pROC::roc_utils_calc_coords."""
    th = np.asarray(th, dtype=float)
    se = np.asarray(se, dtype=float)
    sp = np.asarray(sp, dtype=float)
    scale = 100.0 if rocr["percent"] else 1.0
    nc = len(rocr["controls"])
    nk = len(rocr["cases"])
    n = nc + nk
    tp = np.round(se / scale * nk)
    tn = np.round(sp / scale * nc)
    fn = nk - tp
    fp = nc - tn
    acc = (tp + tn) / n * scale
    npv = np.where((tn + fn) > 0, tn / np.where((tn + fn) > 0, tn + fn, 1) * scale, np.nan)
    ppv = np.where((tp + fp) > 0, tp / np.where((tp + fp) > 0, tp + fp, 1) * scale, np.nan)
    fpr = scale - sp
    fnr = scale - se
    w1, w2 = float(weights[0]), float(weights[1])
    r = (1 - w2) / (w1 * w2)
    return {
        "threshold": th,
        "specificity": sp,
        "sensitivity": se,
        "accuracy": acc,
        "tn": tn, "tp": tp, "fn": fn, "fp": fp,
        "npv": npv, "ppv": ppv, "fdr": scale - ppv,
        "fpr": fpr, "tpr": se, "tnr": sp, "fnr": fnr,
        "1-specificity": fpr, "1-sensitivity": fnr, "1-accuracy": scale - acc,
        "1-npv": scale - npv, "1-ppv": scale - ppv,
        "precision": ppv, "recall": se,
        "lr_pos": np.where(fpr != 0, se / np.where(fpr != 0, fpr, 1), np.inf),
        "lr_neg": np.where(sp != 0, fnr / np.where(sp != 0, sp, 1), np.inf),
        "youden": se + r * sp,
        "closest.topleft": scale * ((1 - se / scale) ** 2 + r * (1 - sp / scale) ** 2),
    }


def _optim_crit(se, sp, maxv, weights, method):
    """pROC::roc_utils_optim_crit"""
    w1, w2 = float(weights[0]), float(weights[1])
    r = (1 - w2) / (w1 * w2)
    if method == "youden":
        return se + r * sp
    return -((maxv - se) ** 2 + r * (maxv - sp) ** 2)


def coords(rocr, x=None, input="threshold", ret=None,
           best_method="youden", best_weights=(1, 0.5)):
    """pROC::coords."""
    is_smooth = bool(rocr.get("is_smooth", False))
    if ret is None:
        ret = ["specificity", "sensitivity"] if is_smooth else \
            ["threshold", "specificity", "sensitivity"]
    ret = _match_ret(ret)
    input = _match_arg(input, ["threshold"] + _VALID_COORDS)
    if x is None:
        x = "all"

    scale = 100.0 if rocr["percent"] else 1.0
    th0 = np.asarray(rocr["th"], dtype=float)
    se0 = np.asarray(rocr["se"], dtype=float)
    sp0 = np.asarray(rocr["sp"], dtype=float)
    rownames = None

    if isinstance(x, str):
        key = _match_arg(x, ["all", "best"])
        if key == "all":
            th, se, sp = th0, se0, sp0
            rownames = [f"{v:.15g}".replace("inf", "Inf").replace("nan", "NA")
                        for v in th]
        else:
            crit = _optim_crit(se0, sp0, scale, best_weights, best_method)
            good = crit == np.nanmax(crit)
            th, se, sp = th0[good], se0[good], sp0[good]
            n = int(len(th))
            rownames = ["threshold"] * n if len(ret) > 1 else [str(i + 1) for i in range(n)]
    else:
        xs = np.atleast_1d(np.asarray(x, dtype=float)).ravel()
        if input == "threshold":
            xn = -xs if rocr["neg"] else xs
            k_ = np.asarray(rocr["cases"], dtype=float)
            c_ = np.asarray(rocr["controls"], dtype=float)
            se = np.array([np.mean(k_ > t) for t in xn]) * scale
            sp = np.array([np.mean(c_ <= t) for t in xn]) * scale
            th = xs.astype(float)
        else:
            cols = _all_columns(th0, se0, sp0, rocr)
            iv = np.asarray(cols[input], dtype=float)
            decreasing = input in _DECREASING
            se = np.full(len(xs), np.nan)
            sp = np.full(len(xs), np.nan)
            th = np.full(len(xs), np.nan)
            for j, value in enumerate(xs):
                idx = np.where(iv == value)[0]
                if len(idx) > 1:
                    idx = np.array([idx[-1] if decreasing else idx[0]])
                if len(idx) == 1:
                    i0 = int(idx[0])
                    th[j], se[j], sp[j] = th0[i0], se0[i0], sp0[i0]
                else:
                    cand = np.where(iv < value)[0] if decreasing \
                        else np.where(iv > value)[0]
                    if len(cand) == 0 or cand[0] == 0:
                        continue
                    nxt = int(cand[0])
                    denom = iv[nxt - 1] - iv[nxt]
                    prop = 0.0 if denom == 0 else (value - iv[nxt]) / denom
                    se[j] = se0[nxt] + prop * (se0[nxt - 1] - se0[nxt])
                    sp[j] = sp0[nxt] + prop * (sp0[nxt - 1] - sp0[nxt])
        rownames = [str(k + 1) for k in range(len(xs))]

    cols = _all_columns(th, se, sp, rocr, weights=best_weights)
    df = pd.DataFrame({k: cols[k] for k in ret})
    if rownames is not None and len(rownames) == len(df):
        df.index = rownames
    return df


# ---------------------------------------------------------------------------
# Example body
# ---------------------------------------------------------------------------
# r2py:entity:roc.s100b
# roc.s100b <- roc(aSAH$outcome, aSAH$s100b, percent = TRUE)
globals()["roc.s100b"] = _roc_impl(aSAH["outcome"].to_numpy(),
                                   aSAH["s100b"].to_numpy(), percent=True)
_roc_s100b = globals()["roc.s100b"]

# r2py:entity:coords
# coords(roc.s100b, 0.55)
print_df(coords(_roc_s100b, 0.55))

# r2py:entity:coords_1
# coords(roc=roc.s100b, x=50, input="sensitivity")
print_df(coords(_roc_s100b, 50, "sensitivity"))

# r2py:entity:coords_2
# coords(roc.s100b, 50, "se")
print_df(coords(_roc_s100b, 50, "sensitivity"))

# r2py:entity:coords_3
# coords(smooth(roc.s100b), 90, "specificity")
print_df(coords(smooth(_roc_s100b), 90, "specificity"))

# r2py:entity:cc
# cc <- coords(roc.s100b, "all", ret="sensitivity")
cc = coords(_roc_s100b, "all", ret="sensitivity")

# r2py:entity:print
# print(cc$sensitivity)
print_vector(cc["sensitivity"].to_numpy())

# r2py:entity:coords_4
# coords(roc.s100b, "best", ret="threshold")
print_df(coords(_roc_s100b, "best", ret="threshold"))

# r2py:entity:roc.ndka
# roc.ndka <- roc(aSAH$outcome, aSAH$ndka, percent=TRUE)
globals()["roc.ndka"] = _roc_impl(aSAH["outcome"].to_numpy(),
                                  aSAH["ndka"].to_numpy(), percent=True)
_roc_ndka = globals()["roc.ndka"]

# r2py:entity:coords_5
# coords(roc.ndka, "best", ret="threshold", best.method="youden")
print_df(coords(_roc_ndka, "best", ret="threshold", best_method="youden"))

# r2py:entity:coords_6
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft")
print_df(coords(_roc_ndka, "best", ret="threshold", best_method="closest.topleft"))

# r2py:entity:coords_7
# coords(roc.ndka, "best", ret="threshold", best.method="youden", best.weights=c(50, 0.2))
print_df(coords(_roc_ndka, "best", ret="threshold", best_method="youden",
                best_weights=(50, 0.2)))

# r2py:entity:coords_8
# coords(roc.ndka, "best", ret="threshold", best.method="closest.topleft", best.weights=c(5, 0.2))
print_df(coords(_roc_ndka, "best", ret="threshold", best_method="closest.topleft",
                best_weights=(5, 0.2)))

# r2py:entity:plot
# plot(roc.ndka, print.thres="best", print.thres.best.method="youden",
#      print.thres.best.weights=c(50, 0.2))
_all_ndka = _all_columns(_roc_ndka["th"], _roc_ndka["se"], _roc_ndka["sp"], _roc_ndka)
_best_ndka = coords(_roc_ndka, "best",
                    ret=["threshold", "specificity", "sensitivity"],
                    best_method="youden", best_weights=(50, 0.2))
_fig_roc = plt.figure()
_ax = _fig_roc.add_subplot(111)
_ax.plot(np.concatenate(([100.0], _all_ndka["specificity"], [0.0])),
         np.concatenate(([0.0], _all_ndka["sensitivity"], [100.0])),
         color="black", linewidth=1)
for _, row in _best_ndka.iterrows():
    _ax.plot([row["specificity"]], [row["sensitivity"]], marker="o", color="black")
    _ax.text(row["specificity"] + 2, row["sensitivity"] - 5,
             f"{row['threshold']:.2f}", color="black")
_ax.set_xlim(100, 0)
_ax.set_ylim(0, 100)
_ax.set_xlabel("Specificity")
_ax.set_ylabel("Sensitivity")
plot = _fig_roc

# r2py:entity:coords_9
# coords(roc.s100b, "best", ret=c("threshold","specificity","sensitivity","accuracy","precision","recall"))
print_df(coords(_roc_s100b, "best",
                ret=["threshold", "specificity", "sensitivity", "accuracy",
                     "precision", "recall"]))

# r2py:entity:coords_10
# coords(roc.s100b, "best", ret = "all")
print_df(coords(_roc_s100b, "best", ret="all"))

# r2py:entity:plot_1
# plot(specificity + sensitivity ~ threshold, coords(roc.ndka, "all"), type="l", log="x",
#      subset = is.finite(threshold))
_c_all = coords(_roc_ndka, "all")
_sel = np.isfinite(_c_all["threshold"].to_numpy())
_fig1 = plt.figure()
_ax1 = _fig1.add_subplot(111)
_ax1.plot(_c_all["threshold"].to_numpy()[_sel],
          (_c_all["specificity"] + _c_all["sensitivity"]).to_numpy()[_sel])
_ax1.set_xscale("log")
_ax1.set_xlabel("threshold")
_ax1.set_ylabel("specificity + sensitivity")
plot_1 = _fig1

# r2py:entity:plot_2
# plot(precision ~ recall, coords(roc.ndka, "all", ret=c("recall","precision")),
#      type="l", ylim=c(0, 100))
_c_pr = coords(_roc_ndka, "all", ret=["recall", "precision"])
_fig2 = plt.figure()
_ax2 = _fig2.add_subplot(111)
_ax2.plot(_c_pr["recall"].to_numpy(), _c_pr["precision"].to_numpy())
_ax2.set_ylim(0, 100)
_ax2.set_xlabel("recall")
_ax2.set_ylabel("precision")
plot_2 = _fig2

# r2py:entity:plot_3
# plot(tpr ~ fpr, coords(roc.ndka, "all", ret=c("tpr","fpr")), type="l")
_c_tf = coords(_roc_ndka, "all", ret=["tpr", "fpr"])
_fig3 = plt.figure()
_ax3 = _fig3.add_subplot(111)
_ax3.plot(_c_tf["fpr"].to_numpy(), _c_tf["tpr"].to_numpy())
_ax3.set_xlabel("fpr")
_ax3.set_ylabel("tpr")
plot_3 = _fig3