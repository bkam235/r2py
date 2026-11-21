# Translated from <R script> by r2py v0.3.0

import os
import math
import pandas as pd
import numpy as np

try:
    import uharfbuzz as hb
    _HB = True
except Exception:
    _HB = False

DIGITS = 7
WRAP_WIDTH = 78


# r2py:entity:suppressPackageStartupMessages
def suppressPackageStartupMessages(expr=None):
    return None


suppressPackageStartupMessages()

# r2py:entity:import_textshaping
# textshaping functionality approximated with uharfbuzz


def _find_font(family="arial"):
    fam = (family or "arial").lower()
    candidates = {
        "arial": [
            r"C:\WINDOWS\Fonts\arial.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ],
    }
    paths = candidates.get(fam, [])
    paths += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def _sig_decimals(v, digits=DIGITS):
    """Decimals needed so that signif(v, digits) is shown exactly."""
    if v == 0:
        return 0
    ax = abs(v)
    e = math.floor(math.log10(ax))
    dec = digits - 1 - e
    if dec < 0:
        dec = 0
    rv = round(v, dec)
    for d in range(0, 17):
        if round(rv, d) == rv:
            return d
    return dec


def _round_away(x):
    if x >= 0:
        return math.floor(x + 0.5)
    return math.ceil(x - 0.5)


# r2py:entity:shape_text
def shape_text(strings, id=None, family="", italic=False, weight="normal",
               width="undefined", features=None, size=12, res=72,
               lineheight=1, align="auto", hjust=0, vjust=0, max_width=np.nan,
               tracking=0, indent=0, hanging=0, space_before=0, space_after=0,
               direction="auto", path=None, index=0, bold=None):

    if isinstance(strings, str):
        strings = [strings]
    strings = [str(s) for s in strings]
    n = len(strings)

    if id is None:
        id = list(range(1, n + 1))
    id = list(id)
    id = [id[i % len(id)] for i in range(n)]
    uniq = []
    for v in id:
        if v not in uniq:
            uniq.append(v)
    id = [uniq.index(v) + 1 for v in id]

    def rep_len(x, m):
        if not isinstance(x, (list, tuple, np.ndarray)):
            x = [x]
        x = list(x)
        if len(x) == 0:
            x = [0]
        return [x[i % len(x)] for i in range(m)]

    order = sorted(range(n), key=lambda i: id[i])
    ids_sorted = [id[i] for i in order]
    strings_sorted = [strings[i] for i in order]

    size_v = [float(v) for v in rep_len(size, n)]
    size_s = [size_v[i] for i in order]

    font_path = path if path is not None else _find_font(family if family else "arial")

    face = hb.Face(hb.Blob.from_file_path(font_path)) if (_HB and font_path) else None

    font_cache = {}
    asc_cache = {}
    desc_cache = {}
    ratio_cache = {}

    def get_font(fs):
        if not _HB or face is None:
            return None
        if fs not in font_cache:
            f = hb.Font(face)
            f.scale = (int(round(fs * 64)), int(round(fs * 64)))
            font_cache[fs] = f
        return font_cache[fs]

    def design_ratios():
        if "asc" in ratio_cache:
            return ratio_cache["asc"], ratio_cache["desc"]
        H = 1 << 24
        f = hb.Font(face)
        f.scale = (H, H)
        ext = f.get_font_extents("ltr")
        ra = ext.ascender / float(H)
        rd = ext.descender / float(H)
        ratio_cache["asc"] = ra
        ratio_cache["desc"] = rd
        return ra, rd

    def get_asc_desc(fs):
        if fs in asc_cache:
            return asc_cache[fs], desc_cache[fs]
        if _HB and face is not None:
            ra, rd = design_ratios()
            a = _round_away(ra * fs * 64) / 64.0
            d = _round_away(rd * fs * 64) / 64.0
        else:
            a = fs * 0.905
            d = -fs * 0.212
        asc_cache[fs] = a
        desc_cache[fs] = d
        return a, d

    groups = []
    cur = None
    cur_id = None
    for k in range(len(ids_sorted)):
        sid = ids_sorted[k]
        if sid != cur_id:
            if cur is not None:
                groups.append(cur)
            cur = {"id": sid, "chars": []}
            cur_id = sid
        for ch in strings_sorted[k]:
            cur["chars"].append((ch, size_s[k]))
    if cur is not None:
        groups.append(cur)

    shape_rows = []
    metric_rows = []

    for g in groups:
        chars = g["chars"]
        sid = g["id"]

        chars = [(c, sz, pos + 1) for pos, (c, sz) in enumerate(chars)]

        lines = []
        line = []
        for (ch, sz, pos) in chars:
            if ch == "\n":
                lines.append(line)
                line = []
            else:
                line.append((ch, sz, pos))
        lines.append(line)

        line_data = []
        for line in lines:
            gl = []
            i = 0
            while i < len(line):
                sz = line[i][1]
                j = i
                while j < len(line) and line[j][1] == sz:
                    j += 1
                run = line[i:j]
                runstr = "".join(c for (c, _, _) in run)
                positions = [p for (_, _, p) in run]
                f = get_font(sz)
                if f is not None and len(runstr) > 0:
                    buf = hb.Buffer()
                    buf.add_str(runstr)
                    buf.guess_segment_properties()
                    hb.shape(f, buf)
                    shaped = [(info.codepoint, pos.x_advance / 64.0)
                              for info, pos in zip(buf.glyph_infos, buf.glyph_positions)]
                    for idx, (gid, adv) in enumerate(shaped):
                        if idx < len(positions):
                            ap = positions[idx]
                        else:
                            ap = positions[-1] + (idx - len(positions) + 1)
                        gl.append((gid, adv, sz, ap))
                else:
                    for (c, _, p) in run:
                        gl.append((ord(c), sz * 0.6, sz, p))
                i = j

            sizes_in_line = set(sz for (c, sz, _) in line) if line else {12}
            asc_line = max(get_asc_desc(s)[0] for s in sizes_in_line)
            desc_line = min(get_asc_desc(s)[1] for s in sizes_in_line)
            line_data.append((gl, asc_line, desc_line))

        nlines = len(line_data)
        asc_lines = [ld[1] for ld in line_data]
        desc_lines = [ld[2] for ld in line_data]

        baselines = [0.0] * nlines
        baselines[nlines - 1] = -min(desc_lines)
        for i in range(nlines - 1, 0, -1):
            baselines[i - 1] = baselines[i] + (asc_lines[i] - desc_lines[i - 1])
        height = baselines[0] + asc_lines[0]
        pen_y = baselines[nlines - 1]

        line_widths = []
        ink_left = None
        ink_right = None
        ink_top = None
        ink_bottom = None
        for li, (gl, asc, desc) in enumerate(line_data):
            xpos = 0.0
            ybase = baselines[li]
            for (gid, adv, sz, ap) in gl:
                a_sz, d_sz = get_asc_desc(sz)
                shape_rows.append({
                    "glyph": ap,
                    "index": gid,
                    "metric_id": sid,
                    "string_id": sid,
                    "x_offset": xpos,
                    "y_offset": ybase,
                    "font_path": font_path if font_path else "",
                    "font_index": 0,
                    "font_size": sz,
                    "advance": adv,
                    "ascender": a_sz,
                    "descender": d_sz,
                })
                f = get_font(sz)
                if f is not None:
                    try:
                        ge = f.get_glyph_extents(gid)
                        bx = ge.x_bearing / 64.0
                        by = ge.y_bearing / 64.0
                        bw = ge.width / 64.0
                        bh = ge.height / 64.0
                        g_left = xpos + bx
                        g_right = xpos + bx + bw
                        g_top = ybase + by
                        g_bot = ybase + by - bh
                        ink_left = g_left if ink_left is None else min(ink_left, g_left)
                        ink_right = g_right if ink_right is None else max(ink_right, g_right)
                        ink_top = g_top if ink_top is None else max(ink_top, g_top)
                        ink_bottom = g_bot if ink_bottom is None else min(ink_bottom, g_bot)
                    except Exception:
                        pass
                xpos += adv
            line_widths.append(xpos)

        w = max(line_widths) if line_widths else 0.0
        pen_x = line_widths[-1] if line_widths else 0.0

        if ink_left is not None:
            left_bearing = ink_left
            right_bearing = w - ink_right
            top_bearing = height - ink_top
            bottom_bearing = ink_bottom
        else:
            left_bearing = 0.0
            right_bearing = 0.0
            top_bearing = asc_lines[0]
            bottom_bearing = 0.0

        metric_rows.append({
            "string": "".join(c for (c, _, _) in chars),
            "width": w,
            "height": height,
            "left_bearing": left_bearing,
            "right_bearing": right_bearing,
            "top_bearing": top_bearing,
            "bottom_bearing": bottom_bearing,
            "left_border": 0.0,
            "top_border": height,
            "pen_x": pen_x,
            "pen_y": pen_y,
            "ltr": True,
        })

    shape_df = pd.DataFrame(shape_rows, columns=[
        "glyph", "index", "metric_id", "string_id", "x_offset", "y_offset",
        "font_path", "font_index", "font_size", "advance", "ascender", "descender"])
    metrics_df = pd.DataFrame(metric_rows, columns=[
        "string", "width", "height", "left_bearing", "right_bearing",
        "top_bearing", "bottom_bearing", "left_border", "top_border",
        "pen_x", "pen_y", "ltr"])

    return {"shape": shape_df, "metrics": metrics_df}


def _escape_char(s):
    return str(s).replace("\\", "\\\\").replace("\n", "\\n")


def _format_columns(df):
    headers = []
    colvals = []
    widths = []
    for name in df.columns:
        col = list(df[name])
        headers.append(str(name))
        is_char = (len(col) > 0 and isinstance(col[0], str))
        is_bool = (len(col) > 0 and isinstance(col[0], (bool, np.bool_)))
        if is_bool:
            vals = ["TRUE" if bool(v) else "FALSE" for v in col]
        elif is_char:
            vals = [_escape_char(v) for v in col]
        else:
            nums = [float(v) for v in col]
            D = 0
            for x in nums:
                D = max(D, _sig_decimals(x))
            fmt = "%." + str(D) + "f"
            vals = [fmt % x for x in nums]
        w = max([len(str(name))] + [len(v) for v in vals]) if vals else len(str(name))
        colvals.append(vals)
        widths.append(w)
    return headers, colvals, widths


def _print_df(df):
    nrow = df.shape[0]
    if nrow == 0:
        return
    headers, colvals, widths = _format_columns(df)
    rnw = len(str(nrow))
    ncol = len(headers)

    blocks = []
    cur = []
    pos = rnw
    for i in range(ncol):
        if cur and pos + 1 + widths[i] > WRAP_WIDTH:
            blocks.append(cur)
            cur = []
            pos = rnw
        cur.append(i)
        pos += 1 + widths[i]
    if cur:
        blocks.append(cur)

    for block in blocks:
        hdr = " " * rnw
        for i in block:
            hdr += " " + headers[i].rjust(widths[i])
        print(hdr)
        for r in range(nrow):
            line = str(r + 1).ljust(rnw)
            for i in block:
                line += " " + colvals[i][r].rjust(widths[i])
            print(line)


def _print_result(r):
    print("$shape")
    _print_df(r["shape"])
    print("")
    print("$metrics")
    _print_df(r["metrics"])


# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_text
_print_result(shape_text(string))

# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle",
]
# r2py:entity:shape_text_1
_print_result(shape_text(string, id=[1, 1, 1], size=[12, 24, 12]))