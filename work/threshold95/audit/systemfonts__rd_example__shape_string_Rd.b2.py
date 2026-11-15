# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import os
import pandas as pd
from matplotlib import font_manager as _fm
from fontTools.ttLib import TTFont as _TTFont

# r2py:data_shim managed by the harness -- loads input datasets

# r2py:entity:import_systemfonts
# systemfonts is approximated using a real font file read through fontTools.


def _find_font(candidates):
    for cand in candidates:
        try:
            path = _fm.findfont(cand, fallback_to_default=False)
            if path and os.path.exists(path):
                return path
        except Exception:
            pass
    fsdirs = [
        r"C:\Windows\Fonts",
        "/usr/share/fonts/truetype/liberation",
        "/usr/share/fonts/truetype/msttcorefonts",
        "/Library/Fonts",
        "/System/Library/Fonts",
    ]
    names = ["arial.ttf", "Arial.ttf", "LiberationSans-Regular.ttf",
             "Arimo-Regular.ttf", "Helvetica.ttf", "DejaVuSans.ttf"]
    for d in fsdirs:
        for nm in names:
            p = os.path.join(d, nm)
            if os.path.exists(p):
                return p
    return _fm.findfont("DejaVu Sans")


_FONT_PATH = _find_font(["Arial", "Liberation Sans", "Arimo",
                         "Nimbus Sans", "Helvetica", "DejaVu Sans"])
_FONT = _TTFont(_FONT_PATH)
_UPEM = float(_FONT["head"].unitsPerEm)
_CMAP = _FONT.getBestCmap()
_HMTX = _FONT["hmtx"]
_HHEA = _FONT["hhea"]
_ASCENT = float(_HHEA.ascent)
_DESCENT = float(_HHEA.descent)
_GLYF = _FONT["glyf"]
_MISSING = _CMAP.get(ord("?"))


def _glyph_name(ch):
    return _CMAP.get(ord(ch), _MISSING)


def _adv_px(ch, size, res):
    units = _HMTX[_glyph_name(ch)][0]
    return units / _UPEM * size * (res / 72.0)


def _glyph_index(ch):
    return _FONT.getGlyphID(_glyph_name(ch))


def _glyph_bbox(gname):
    try:
        g = _GLYF[gname]
        if g.numberOfContours == 0:
            return None
        return (float(g.yMin), float(g.yMax))
    except Exception:
        return None


# r2py:entity:shape_string
def shape_string(strings, id=None, size=12, res=72, lineheight=1):
    if isinstance(strings, str):
        strings = [strings]
    n = len(strings)

    if id is None:
        ids = list(range(1, n + 1))
    else:
        if not isinstance(id, (list, tuple)):
            id = [id]
        ids = [id[k % len(id)] for k in range(n)]
    uniq = []
    for v in ids:
        if v not in uniq:
            uniq.append(v)
    ids = [uniq.index(v) + 1 for v in ids]

    if not isinstance(size, (list, tuple)):
        size = [size]
    size = [size[k % len(size)] for k in range(n)]

    order = sorted(range(n), key=lambda k: ids[k])
    ids = [ids[k] for k in order]
    strings = [str(strings[k]) for k in order]
    size = [size[k] for k in order]

    groups = []
    for i in range(n):
        if groups and groups[-1][0] == ids[i]:
            groups[-1][1].append((strings[i], size[i]))
        else:
            groups.append((ids[i], [(strings[i], size[i])]))

    shape_rows = []
    metrics_rows = []

    for sid, elements in groups:
        lines = [[]]
        for text, sz in elements:
            for ch in text:
                if ch == "\n":
                    lines[-1].append({"glyph": "\\n", "size": sz, "isnl": True})
                    lines.append([])
                else:
                    adv = int(round(_adv_px(ch, sz, res)))
                    lines[-1].append({"glyph": ch, "size": sz,
                                      "adv": adv, "isnl": False})

        lmax = []
        for ln in lines:
            if ln:
                lmax.append(max(g["size"] for g in ln))
            else:
                lmax.append(elements[0][1] if elements else 12)

        lh = [(_ASCENT - _DESCENT) / _UPEM * m * (res / 72.0) * lineheight
              for m in lmax]
        cum = [0.0] * len(lines)
        for i in range(1, len(lines)):
            cum[i] = cum[i - 1] + lh[i - 1]

        line_widths = []
        bbox_y_maxs = []
        bbox_y_mins = []
        for li, ln in enumerate(lines):
            x = 0.0
            yoff = 0.0 - cum[li]
            for g in ln:
                if g["isnl"]:
                    nladv = 0.75 * g["size"] * (res / 72.0)
                    shape_rows.append({
                        "glyph": "\\n", "index": 0, "metric_id": 0,
                        "string_id": sid, "x_offset": float(x),
                        "y_offset": yoff, "x_midpoint": nladv / 2.0,
                    })
                else:
                    bb = _glyph_bbox(_glyph_name(g["glyph"]))
                    if bb is not None:
                        bbox_y_mins.append(bb[0])
                        bbox_y_maxs.append(bb[1])
                    shape_rows.append({
                        "glyph": g["glyph"], "index": _glyph_index(g["glyph"]),
                        "metric_id": 0, "string_id": sid,
                        "x_offset": float(x), "y_offset": yoff,
                        "x_midpoint": g["adv"] / 2.0,
                    })
                    x += g["adv"]
            line_widths.append(x)

        metrics_size = lmax[0]
        scale = metrics_size * (res / 72.0) / _UPEM
        top_border = _ASCENT * scale
        bottom_border = -_DESCENT * scale
        ymax = max(bbox_y_maxs) if bbox_y_maxs else 0.0
        ymin = min(bbox_y_mins) if bbox_y_mins else 0.0
        top_bearing = top_border - ymax * scale
        bottom_bearing = bottom_border + ymin * scale

        width = float(max(line_widths)) if line_widths else 0.0
        pen_x = line_widths[-1] if line_widths else 0.0
        pen_y = 0.0 - cum[-1]
        height = 2.0 * top_border + bottom_border + cum[-1]

        metrics_rows.append({
            "string": "".join(t for t, _ in elements).replace("\n", "\\n"),
            "width": width,
            "height": height,
            "left_bearing": 0.0,
            "right_bearing": 0.0,
            "top_bearing": top_bearing,
            "bottom_bearing": bottom_bearing,
            "left_border": 0.0,
            "top_border": top_border,
            "pen_x": pen_x,
            "pen_y": pen_y,
        })

    shape = pd.DataFrame(shape_rows,
                         columns=["glyph", "index", "metric_id", "string_id",
                                  "x_offset", "y_offset", "x_midpoint"])
    metrics = pd.DataFrame(metrics_rows,
                           columns=["string", "width", "height", "left_bearing",
                                    "right_bearing", "top_bearing",
                                    "bottom_bearing", "left_border",
                                    "top_border", "pen_x", "pen_y"])
    return {"shape": shape, "metrics": metrics}


def _fmt_numeric_col(values):
    maxd = 0
    for v in values:
        v = float(v)
        if v == int(v):
            d = 0
        else:
            s = format(v, ".7g")
            if "e" in s or "E" in s:
                d = 6
            elif "." in s:
                d = len(s.split(".")[1].rstrip())
            else:
                d = 0
        if d > maxd:
            maxd = d
    return [format(float(v), ".%df" % maxd) for v in values]


def _format_column(df, name):
    vals = df[name].tolist()
    if name in ("glyph", "string"):
        strs = [str(v) for v in vals]
    else:
        strs = _fmt_numeric_col(vals)
    w = len(name)
    for s in strs:
        if len(s) > w:
            w = len(s)
    return strs, w


def _render_df(df):
    n = len(df)
    cols = list(df.columns)
    data = {}
    widths = {}
    for c in cols:
        s, w = _format_column(df, c)
        data[c] = s
        widths[c] = w

    rnames = [str(i) for i in range(1, n + 1)]
    rw = max((len(x) for x in rnames), default=0)

    groups = []
    cur = []
    for c in cols:
        new = cur + [c]
        test = rw + 1 + sum(widths[x] for x in new) + (len(new) - 1)
        if cur and test > 80:
            groups.append(cur)
            cur = [c]
        else:
            cur = new
    if cur:
        groups.append(cur)

    lines = []
    for grp in groups:
        hdr_parts = [c.rjust(widths[c]) for c in grp]
        lines.append((" " * rw) + " " + " ".join(hdr_parts))
        for ri in range(n):
            rn = rnames[ri].ljust(rw)
            parts = [data[c][ri].rjust(widths[c]) for c in grp]
            lines.append(rn + " " + " ".join(parts))
    return "\n".join(lines)


def _rprint(obj):
    print("$shape")
    print(_render_df(obj["shape"]))
    print("")
    print("$metrics")
    print(_render_df(obj["metrics"]))


# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(systemfonts)) -- no-op in Python

# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"

# r2py:entity:shape_string
_rprint(shape_string(string))

# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle",
]

# r2py:entity:shape_string_1
_rprint(shape_string(string, id=[1, 1, 1], size=[12, 24, 12]))