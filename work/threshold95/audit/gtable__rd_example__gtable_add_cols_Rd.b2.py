# Translated from <R script> by r2py v0.3.0
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy

# ---- grid / gtable emulation -------------------------------------------
_GLOBAL_GROB_N = [0]

def gpar(**kwargs):
    gp = {}
    for k, v in kwargs.items():
        if v is not None:
            gp[k] = v
    return gp

def unit(x, units, data=None):
    if isinstance(x, (int, float)):
        x = [x]
    try:
        n = len(x)
    except TypeError:
        x = [x]
        n = 1
    return [float(x[i]) for i in range(n)]

# r2py:entity:rect
def rectGrob(x=0.5, y=0.5, width=1, height=1, just="centre", hjust=None,
             vjust=None, default_units="npc", name=None, gp=None, vp=None):
    _GLOBAL_GROB_N[0] += 1
    if name is None:
        name = "GRID.rect.%d" % _GLOBAL_GROB_N[0]
    return {
        "x": 0.5, "y": 0.5, "width": 1, "height": 1,
        "just": "centre", "hjust": {}, "vjust": {},
        "name": name,
        "gp": gp if gp is not None else {},
        "vp": vp if vp is not None else {},
    }

# r2py:entity:tab
def gtable(widths=None, heights=None, respect=False, name="layout",
           rownames=None, colnames=None, vp=None):
    return {
        "grobs": [],
        "layout": {"t": [], "l": [], "b": [], "r": [], "z": [],
                   "clip": [], "name": []},
        "widths": list(widths) if widths is not None else [],
        "heights": list(heights) if heights is not None else [],
        "respect": respect,
        "rownames": rownames if rownames is not None else {},
        "colnames": colnames if colnames is not None else {},
        "name": name,
        "gp": {},
        "vp": vp if vp is not None else {},
        "children": [],
        "childrenOrder": [],
    }

def _neg_to_pos(pos, n):
    if pos < 0:
        return n + 1 + pos
    return pos

def _rep1(val, n_grobs):
    if isinstance(val, (list, tuple)):
        vals = list(val)
        if len(vals) == 0:
            return [val] * n_grobs
        return (vals * ((n_grobs // len(vals)) + 1))[:n_grobs]
    return [val] * n_grobs

# r2py:entity:tab_1
def gtable_add_grob(x, grobs, t, l, b=None, r=None, z=None,
                    clip="on", name=None):
    x = copy.deepcopy(x)
    if b is None:
        b = t
    if r is None:
        r = l
    if isinstance(grobs, dict):
        grobs = [grobs]
    n_grobs = len(grobs)

    t = _rep1(t, n_grobs)
    b = _rep1(b, n_grobs)
    l = _rep1(l, n_grobs)
    r = _rep1(r, n_grobs)

    x_row = len(x["heights"])
    x_col = len(x["widths"])
    t = [_neg_to_pos(v, x_row) for v in t]
    b = [_neg_to_pos(v, x_row) for v in b]
    l = [_neg_to_pos(v, x_col) for v in l]
    r = [_neg_to_pos(v, x_col) for v in r]

    clip = _rep1(clip, n_grobs)
    if name is None:
        name = x["name"]
    name = _rep1(name, n_grobs)

    if z is None:
        z = [float("inf")] * n_grobs
    else:
        z = _rep1(z, n_grobs)

    lay = x["layout"]
    zval = [v for v in lay["z"] if v not in (float("inf"), float("-inf"))] + \
           [v for v in z if v not in (float("inf"), float("-inf"))]
    if len(zval) == 0:
        zmin, zmax = 1, 0
    else:
        zmin, zmax = min(zval), max(zval)
    n_neg = sum(1 for v in z if v == float("-inf"))
    n_pos = sum(1 for v in z if v == float("inf"))
    z_new = []
    i_neg = 0
    i_pos = 0
    for v in z:
        if v == float("-inf"):
            i_neg += 1
            z_new.append(zmin - (n_neg - i_neg + 1))
        elif v == float("inf"):
            i_pos += 1
            z_new.append(zmax + i_pos)
        else:
            z_new.append(v)

    x["grobs"] = x["grobs"] + [copy.deepcopy(g) for g in grobs]
    lay["t"] = lay["t"] + t
    lay["l"] = lay["l"] + l
    lay["b"] = lay["b"] + b
    lay["r"] = lay["r"] + r
    lay["z"] = lay["z"] + z_new
    lay["clip"] = lay["clip"] + clip
    lay["name"] = lay["name"] + name
    return x

# r2py:entity:tab2
def gtable_add_cols(x, widths, pos=-1):
    x = copy.deepcopy(x)
    if not isinstance(widths, (list, tuple)):
        widths = [widths]
    n = len(widths)
    ncols = len(x["widths"])
    pos = _neg_to_pos(pos, ncols)
    lay = x["layout"]
    lay["l"] = [v + n if v > pos else v for v in lay["l"]]
    lay["r"] = [v + n if v > pos else v for v in lay["r"]]
    w = x["widths"]
    x["widths"] = w[:pos] + list(widths) + w[pos:]
    return x

# r2py:entity:dim
def _dim_gtable(x):
    return (len(x["heights"]), len(x["widths"]))

# r2py:entity:plot
def _plot_gtable(x):
    nrow, ncol = _dim_gtable(x)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, ncol)
    ax.set_ylim(0, nrow)
    ax.axis("off")
    lay = x["layout"]
    for i in range(len(lay["t"])):
        c0 = lay["l"][i] - 1
        r0 = lay["r"][i]
        roww = lay["t"][i] - 1
        rowh = lay["b"][i]
        rect = patches.Rectangle((c0, nrow - rowh), r0 - c0, rowh - roww,
                                 color="#00000080")
        ax.add_patch(rect)
    return fig

# ---- example code ------------------------------------------------------
# r2py:entity:rect
rect = rectGrob(gp=gpar(fill="#00000080"))

# r2py:entity:tab
tab = gtable(unit([1, 1, 1], "null"), unit([1, 1, 1], "null"))
# r2py:entity:tab_1
tab = gtable_add_grob(tab, rect, t=1, l=1, r=3)
# r2py:entity:tab_2
tab = gtable_add_grob(tab, rect, t=1, b=3, l=1)
# r2py:entity:tab_3
tab = gtable_add_grob(tab, rect, t=1, b=3, l=3)

# r2py:entity:dim
print(_dim_gtable(tab))
# r2py:entity:plot
_plot_gtable(tab)

# r2py:entity:tab2
tab2 = gtable_add_cols(tab, unit(1, "null"), 1)
# r2py:entity:dim_1
print(_dim_gtable(tab2))
# r2py:entity:plot_1
_plot_gtable(tab2)

# r2py:entity:tab3
tab3 = gtable_add_cols(tab, unit(1, "null"))
# r2py:entity:tab3_1
tab3 = gtable_add_cols(tab3, unit(1, "null"), 0)
# r2py:entity:dim_2
print(_dim_gtable(tab3))
# r2py:entity:plot_2
_plot_gtable(tab3)