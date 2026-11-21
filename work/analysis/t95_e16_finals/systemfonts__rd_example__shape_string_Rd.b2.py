# Translated from <R script> by r2py v0.3.0
# r2py:data_shim managed by the harness (loads input datasets)

# r2py:entity:import_systemfonts

import os
import math
import struct

# r2py:entity:shape_string


# ---------------------------------------------------------------------------
# Minimal TrueType font reader (head / hhea / maxp / hmtx / cmap)
# ---------------------------------------------------------------------------

def _font_path():
    windir = os.environ.get("WINDIR", r"C:\Windows")
    cands = [
        os.path.join(windir, "Fonts", "arial.ttf"),
        r"C:\Windows\Fonts\arial.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in cands:
        try:
            if os.path.exists(p):
                return p
        except Exception:
            pass
    return None


class _Font:
    def __init__(self, path):
        with open(path, "rb") as fh:
            self.data = fh.read()
        d = self.data
        num_tables = struct.unpack(">H", d[4:6])[0]
        self.tables = {}
        for i in range(num_tables):
            base = 12 + 16 * i
            tag = d[base:base + 4].decode("latin-1")
            off = struct.unpack(">I", d[base + 8:base + 12])[0]
            ln = struct.unpack(">I", d[base + 12:base + 16])[0]
            self.tables[tag] = (off, ln)
        head = self.tables["head"][0]
        self.upem = struct.unpack(">H", d[head + 18:head + 20])[0]
        hhea = self.tables["hhea"][0]
        self.ascender = struct.unpack(">h", d[hhea + 4:hhea + 6])[0]
        self.descender = abs(struct.unpack(">h", d[hhea + 6:hhea + 8])[0])
        self.num_hmetrics = struct.unpack(">H", d[hhea + 34:hhea + 36])[0]
        self._cmap = self._parse_cmap()
        self._cache = {}

    def _u16(self, off):
        return struct.unpack(">H", self.data[off:off + 2])[0]

    def _u32(self, off):
        return struct.unpack(">I", self.data[off:off + 4])[0]

    def _parse_cmap(self):
        d = self.data
        base = self.tables["cmap"][0]
        n = self._u16(base + 2)
        best = None
        for i in range(n):
            rec = base + 4 + 8 * i
            pid = self._u16(rec)
            eid = self._u16(rec + 2)
            off = base + self._u32(rec + 4)
            fmt = self._u16(off)
            if pid == 3 and eid == 1 and fmt == 4:
                best = ("f4", off)
                break
            if pid == 3 and eid == 10 and fmt == 12:
                best = ("f12", off)
        if best is None:
            for i in range(n):
                rec = base + 4 + 8 * i
                off = base + self._u32(rec + 4)
                fmt = self._u16(off)
                if fmt == 4:
                    best = ("f4", off)
                    break
                if fmt == 12:
                    best = ("f12", off)
        return best

    def glyph(self, ch):
        c = ord(ch)
        if c in self._cache:
            return self._cache[c]
        gid = 0
        if self._cmap is not None:
            kind, off = self._cmap
            if kind == "f4":
                gid = self._cmap_f4(c, off)
            else:
                gid = self._cmap_f12(c, off)
        self._cache[c] = gid
        return gid

    def _cmap_f4(self, c, base):
        if c > 0xFFFF:
            return 0
        segx2 = self._u16(base + 6)
        seg = segx2 // 2
        end_base = base + 14
        start_base = end_base + segx2 + 2
        delta_base = start_base + segx2
        ro_base = delta_base + segx2
        for i in range(seg):
            end = self._u16(end_base + 2 * i)
            if end >= c:
                start = self._u16(start_base + 2 * i)
                if start > c:
                    return 0
                delta = struct.unpack(">h", self.data[delta_base + 2 * i:delta_base + 2 * i + 2])[0]
                ro = self._u16(ro_base + 2 * i)
                if ro == 0:
                    return (c + delta) & 0xFFFF
                entry_local = (ro_base - base) + 2 * i
                glyph_local = entry_local + ro + 2 * (c - start)
                g = self._u16(base + glyph_local)
                if g == 0:
                    return 0
                return (g + delta) & 0xFFFF
        return 0

    def _cmap_f12(self, c, base):
        ngroups = self._u32(base + 12)
        for i in range(ngroups):
            g = base + 16 + 12 * i
            start = self._u32(g)
            end = self._u32(g + 4)
            if start <= c <= end:
                sg = self._u32(g + 8)
                return sg + (c - start)
        return 0

    def advance_units(self, gid):
        off = self.tables["hmtx"][0]
        if gid < self.num_hmetrics:
            return self._u16(off + 4 * gid)
        return self._u16(off + 4 * (self.num_hmetrics - 1))


_FONT = None
try:
    _p = _font_path()
    if _p is not None:
        _FONT = _Font(_p)
except Exception:
    _FONT = None


def _upem():
    return _FONT.upem if _FONT is not None else 2048


def _glyph_index(ch):
    if _FONT is None:
        return 0
    return _FONT.glyph(ch)


def _adv_units(ch):
    if _FONT is None:
        return 1024
    return _FONT.advance_units(_FONT.glyph(ch))


def _asc_units():
    return _FONT.ascender if _FONT is not None else 1854


def _desc_units():
    return _FONT.descender if _FONT is not None else 434


def _rep_len(x, n):
    if not isinstance(x, (list, tuple)):
        x = [x]
    x = list(x)
    if len(x) == 0:
        return [None] * n
    return [x[i % len(x)] for i in range(n)]


def _rnd(x):
    return math.floor(x + 0.5)


def _char_advance(ch, size, res):
    if ch == "\n":
        return 0
    units = _adv_units(ch)
    return _rnd(units * size * res / (_upem() * 72.0))


def _ascent(size):
    return math.floor((_asc_units() * size / _upem()) * 64.0 + 0.5) / 64.0


def _descent(size):
    return math.floor((_desc_units() * size / _upem()) * 64.0 + 0.5) / 64.0


_LINE_HEIGHT_FACTOR = 1553.0 / 768.0
_TB_FACTOR = 55.0 / 768.0
_BB_FACTOR = 163.0 / 768.0
_TOPBORDER_FACTOR = 695.0 / 768.0


def _sig_string(v):
    if v == int(v):
        return str(int(v))
    return "%.7g" % v


def _fmt_num_col(vals):
    sig = [_sig_string(float(v)) for v in vals]
    maxdec = 0
    for s in sig:
        if "." in s:
            maxdec = max(maxdec, len(s.split(".")[1]))
    out = []
    for s in sig:
        if maxdec == 0:
            out.append(s.split(".")[0])
        else:
            if "." in s:
                ip, fp = s.split(".")
            else:
                ip, fp = s, ""
            fp = fp + "0" * (maxdec - len(fp))
            out.append(ip + "." + fp)
    return out


class _RDataFrame:
    def __init__(self, colnames, columns, types, max_width=80):
        self.colnames = colnames
        self.columns = columns
        self.types = types
        self.max_width = max_width

    def lines(self):
        ncol = len(self.colnames)
        nrow = len(self.columns[0]) if self.columns else 0
        rnw = len(str(nrow)) if nrow > 0 else 1
        disp = []
        for j in range(ncol):
            t = self.types[j]
            col = self.columns[j]
            if t == "num":
                disp.append(_fmt_num_col(col))
            elif t == "int":
                disp.append([str(int(v)) for v in col])
            else:
                disp.append([str(v) for v in col])
        colwidths = []
        for j in range(ncol):
            w = len(self.colnames[j])
            for v in disp[j]:
                w = max(w, len(v))
            colwidths.append(w)
        blocks = []
        cur = []
        curlen = rnw + 1
        for j in range(ncol):
            add = colwidths[j] + 1
            if cur and (curlen + add > self.max_width):
                blocks.append(cur)
                cur = []
                curlen = rnw + 1
            cur.append(j)
            curlen += add
        if cur:
            blocks.append(cur)
        out = []
        for block in blocks:
            parts = [self.colnames[j].rjust(colwidths[j]) for j in block]
            out.append(" " * (rnw + 1) + " ".join(parts))
            for i in range(nrow):
                rn = str(i + 1).ljust(rnw)
                rowparts = [disp[j][i].rjust(colwidths[j]) for j in block]
                out.append(rn + " " + " ".join(rowparts))
        return out


class _RList:
    def __init__(self, items):
        self.items = items

    def __str__(self):
        parts = []
        for k, (name, df) in enumerate(self.items):
            if k > 0:
                parts.append("")
            parts.append("$" + name)
            parts.extend(df.lines())
        return "\n".join(parts)


def shape_string(strings, id_=None, size=12, res=72, lineheight=1,
                 align="left", max_width=float("nan"), tracking=0):
    if not isinstance(strings, (list, tuple)):
        strings = [strings]
    n = len(strings)

    if id_ is None:
        id_ = list(range(1, n + 1))
    ids = _rep_len(id_, n)
    uniq = []
    for x in ids:
        if x not in uniq:
            uniq.append(x)
    ids = [uniq.index(x) + 1 for x in ids]

    order = sorted(range(n), key=lambda k: ids[k])
    strings = [strings[k] for k in order]
    ids = [ids[k] for k in order]
    sizes = _rep_len(size if isinstance(size, (list, tuple)) else [size], n)
    sizes = [sizes[k] for k in order]

    # pieces with their global (ordered) string index and group id
    pieces = []
    for k in range(n):
        pieces.append({"text": strings[k], "size": sizes[k],
                       "sid": k + 1, "id": ids[k]})

    groups = {}
    group_order = []
    for pc in pieces:
        if pc["id"] not in groups:
            groups[pc["id"]] = []
            group_order.append(pc["id"])
        groups[pc["id"]].append(pc)

    gcol = []
    icol = []
    mcol = []
    scol = []
    xcol = []
    ycol = []
    xmcol = []

    mstr = []
    mwidth = []
    mheight = []
    mlb = []
    mrb = []
    mtb = []
    mbb = []
    mlbo = []
    mtbo = []
    mpenx = []
    mpeny = []

    for gid in group_order:
        gpieces = groups[gid]
        base_size = gpieces[0]["size"]

        # Build lines: list of {size, chars:[(ch,size,sid)]}
        lines = []
        current = None
        concat = ""
        for pc in gpieces:
            psize = pc["size"]
            concat += pc["text"]
            for ch in pc["text"]:
                if current is None:
                    current = {"size": psize, "chars": []}
                else:
                    current["size"] = max(current["size"], psize)
                if ch == "\n":
                    current["chars"].append((ch, psize, pc["sid"]))
                    lines.append(current)
                    current = {"size": psize, "chars": []}
                else:
                    current["chars"].append((ch, psize, pc["sid"]))
        if current is not None and current["chars"]:
            lines.append(current)

        # y offset per line
        ys = []
        y = 0.0
        for k in range(len(lines)):
            if k == 0:
                ys.append(0.0)
            else:
                step = _descent(lines[k - 1]["size"]) + _ascent(lines[k]["size"])
                y = ys[k - 1] - lineheight * step
                ys.append(y)

        line_widths = []
        for k, ln in enumerate(lines):
            pen_x = 0.0
            ly = ys[k]
            for ch, csize, sid in ln["chars"]:
                if ch == "\n":
                    gcol.append("\\n")
                    icol.append(0)
                    mcol.append(0)
                    scol.append(sid)
                    xcol.append(pen_x)
                    ycol.append(ly)
                    xmcol.append(csize * 0.375)
                    continue
                adv = _char_advance(ch, csize, res)
                gcol.append(ch)
                icol.append(_glyph_index(ch))
                mcol.append(0)
                scol.append(sid)
                xcol.append(pen_x)
                ycol.append(ly)
                xmcol.append(adv / 2.0)
                pen_x += adv
            line_widths.append(pen_x)

        width = max(line_widths) if line_widths else 0.0
        last_pen = line_widths[-1] if line_widths else 0.0
        y_last = ys[-1] if ys else 0.0
        last_size = lines[-1]["size"] if lines else base_size
        height = (-y_last) + last_size * _LINE_HEIGHT_FACTOR

        mstr.append(concat.replace("\n", "\\n"))
        mwidth.append(width)
        mheight.append(height)
        mlb.append(0.0)
        mrb.append(0.0)
        mtb.append(base_size * _TB_FACTOR)
        mbb.append(base_size * _BB_FACTOR)
        mlbo.append(0.0)
        mtbo.append(base_size * _TOPBORDER_FACTOR)
        mpenx.append(last_pen)
        mpeny.append(y_last)

    shape_df = _RDataFrame(
        ["glyph", "index", "metric_id", "string_id",
         "x_offset", "y_offset", "x_midpoint"],
        [gcol, icol, mcol, scol, xcol, ycol, xmcol],
        ["chr", "int", "int", "int", "num", "num", "num"],
    )
    met_df = _RDataFrame(
        ["string", "width", "height", "left_bearing", "right_bearing",
         "top_bearing", "bottom_bearing", "left_border", "top_border",
         "pen_x", "pen_y"],
        [mstr, mwidth, mheight, mlb, mrb, mtb, mbb, mlbo, mtbo, mpenx, mpeny],
        ["chr", "num", "num", "num", "num", "num", "num", "num", "num",
         "num", "num"],
    )
    return _RList([("shape", shape_df), ("metrics", met_df)])


# Section 1
# r2py:entity:string
string = "This is a long string\nLook; It spans multiple lines\nand all"
# r2py:entity:shape_string
print(shape_string(string))

# Section 2
# r2py:entity:string_1
string = [
    "This string will have\na ",
    "very large",
    " text style\nin the middle",
]
# r2py:entity:shape_string_1
print(shape_string(string, id_=[1, 1, 1], size=[12, 24, 12]))