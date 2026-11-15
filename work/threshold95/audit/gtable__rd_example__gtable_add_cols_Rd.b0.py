# Translated from <R script> by r2py v0.3.0
import math
import copy

import numpy as np
import pandas as pd

# r2py:data_shim managed by the harness

# ---- minimal 'grid' / 'gtable' emulation -------------------------------

def unit(x, units=None):
    vals = np.atleast_1d(np.asarray(x, dtype=float))
    return [float(v) for v in vals]


def gpar(**kwargs):
    gp = {}
    for k, v in kwargs.items():
        if v is not None:
            gp[k] = v
    return gp


def rectGrob(x=0.5, y=0.5, width=1.0, height=1.0, just="centre",
             hjust=None, vjust=None, name=None, gp=None, vp=None):
    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "just": just,
        "hjust": hjust if hjust is not None else {},
        "vjust": vjust if vjust is not None else {},
        "name": name if name is not None else "GRID.rect.1",
        "gp": gp if gp is not None else {},
        "vp": vp if vp is not None else {},
    }


def gtable(widths=None, heights=None, respect=False, name="layout",
           rownames=None, colnames=None, vp=None):
    if widths is None:
        widths = []
    if heights is None:
        heights = []
    layout = {
        "t": [], "l": [], "b": [], "r": [],
        "z": [], "clip": [], "name": [],
    }
    return {
        "grobs": [],
        "layout": layout,
        "widths": list(widths),
        "heights": list(heights),
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
    return n + pos + 1 if pos < 0 else pos


def gtable_add_grob(x, grobs, t, l, b=None, r=None, z=None, clip="on", name=None):
    x = copy.deepcopy(x)
    if isinstance(grobs, dict):
        grobs = [grobs]
    n_grobs = len(grobs)

    if b is None:
        b = t
    if r is None:
        r = l
    if z is None:
        z = [math.inf] * n_grobs
    if name is None:
        name = x["name"]

    t = list(np.atleast_1d(t))
    l = list(np.atleast_1d(l))
    b = list(np.atleast_1d(b))
    r = list(np.atleast_1d(r))
    z = list(np.atleast_1d(z))
    clip = list(np.atleast_1d(clip))
    name = list(np.atleast_1d(name))

    def rep_to(vals, n):
        vals = list(vals)
        if len(vals) == 0:
            return vals
        return [vals[i % len(vals)] for i in range(n)]

    layout = x["layout"]
    zval = list(layout["z"]) + [zz for zz in z if not math.isinf(zz)]
    if len(zval) == 0:
        zmin, zmax = 1, 0
    else:
        zmin, zmax = min(zval), max(zval)

    n_neg_inf = sum(1 for zz in z if zz == -math.inf)
    n_pos_inf = sum(1 for zz in z if zz == math.inf)

    x_row = len(x["heights"])
    x_col = len(x["widths"])

    t = [_neg_to_pos(v, x_row) for v in rep_to(t, n_grobs)]
    b = [_neg_to_pos(v, x_row) for v in rep_to(b, n_grobs)]
    l = [_neg_to_pos(v, x_col) for v in rep_to(l, n_grobs)]
    r = [_neg_to_pos(v, x_col) for v in rep_to(r, n_grobs)]
    z = rep_to(z, n_grobs)
    clip = rep_to(clip, n_grobs)
    name = rep_to(name, n_grobs)

    neg_counter = n_neg_inf
    pos_counter = 0
    for i, zz in enumerate(z):
        if zz == -math.inf:
            z[i] = zmin - (n_neg_inf - neg_counter + 1)
            neg_counter -= 1
        elif zz == math.inf:
            pos_counter += 1
            z[i] = zmax + pos_counter

    x["grobs"] = list(x["grobs"]) + grobs
    layout["t"] = list(layout["t"]) + t
    layout["l"] = list(layout["l"]) + l
    layout["b"] = list(layout["b"]) + b
    layout["r"] = list(layout["r"]) + r
    layout["z"] = list(layout["z"]) + z
    layout["clip"] = list(layout["clip"]) + clip
    layout["name"] = list(layout["name"]) + name
    return x


def gtable_add_cols(x, widths, pos=-1):
    x = copy.deepcopy(x)
    if isinstance(widths, (dict, float, int)):
        widths = [widths]
    n = len(widths)
    pos = _neg_to_pos(pos, len(x["widths"]))

    old = list(x["widths"])
    x["widths"] = old[:pos] + list(widths) + old[pos:]

    layout = x["layout"]
    layout["l"] = [v + n if v > pos else v for v in layout["l"]]
    layout["r"] = [v + n if v > pos else v for v in layout["r"]]
    return x


def dim(x):
    return (len(x["heights"]), len(x["widths"]))


# r2py:entity:plot
def plot(x, *args, **kwargs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    nrow = len(x["heights"])
    ncol = len(x["widths"])
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, max(ncol, 1))
    ax.set_ylim(0, max(nrow, 1))
    ax.axis("off")
    for i in range(len(x["layout"]["t"])):
        t = x["layout"]["t"][i]
        b = x["layout"]["b"][i]
        l = x["layout"]["l"][i]
        r = x["layout"]["r"][i]
        rect = patches.Rectangle((l - 1, nrow - b), r - l + 1, b - t + 1)
        ax.add_patch(rect)
    return None


def suppressPackageStartupMessages(expr=None):
    return expr


# ---- example -----------------------------------------------------------

# r2py:entity:suppressPackageStartupMessages
suppressPackageStartupMessages(expr=True)


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
print(dim(tab))
# r2py:entity:plot
plot(tab)

# r2py:entity:tab2
tab2 = gtable_add_cols(tab, unit(1, "null"), 1)
# r2py:entity:dim_1
print(dim(tab2))
# r2py:entity:plot_1
plot(tab2)

# r2py:entity:tab3
tab3 = gtable_add_cols(tab, unit(1, "null"))
# r2py:entity:tab3_1
tab3 = gtable_add_cols(tab3, unit(1, "null"), 0)
# r2py:entity:dim_2
print(dim(tab3))
# r2py:entity:plot_2
plot(tab3)