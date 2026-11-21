import numpy as np
from skimage import color

# r2py:data_shim managed by the harness

# ---- farver-exact colour conversions (sRGB / D65) ----
_M_RGB2XYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
])

_CX, _CY = 0.31271, 0.32902
_tmp = 100.0 / _CY
_WHITE = np.array([_tmp * _CX, 100.0, _tmp * (1.0 - _CX - _CY)])


def _srgb_lin(rgb):
    c = np.asarray(rgb, dtype=float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _rgb_to_xyz(rgb):
    lin = _srgb_lin(rgb)
    return (lin @ _M_RGB2XYZ.T) * 100.0


def _xyz_to_lab(xyz):
    xyz = np.asarray(xyz, dtype=float)
    t = xyz / _WHITE
    eps = (6.0 / 29.0) ** 3

    def f(v):
        return np.where(v > eps, np.cbrt(v), v / (3 * (6.0 / 29.0) ** 2) + 4.0 / 29.0)

    fx, fy, fz = f(t[..., 0]), f(t[..., 1]), f(t[..., 2])
    L = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return np.stack([L, a, b], axis=-1)


def _xyz_to_luv(xyz):
    xyz = np.asarray(xyz, dtype=float)
    X, Y, Z = xyz[..., 0], xyz[..., 1], xyz[..., 2]
    den = X + 15.0 * Y + 3.0 * Z
    up = np.where(den != 0, 4.0 * X / den, 0.0)
    vp = np.where(den != 0, 9.0 * Y / den, 0.0)
    Xn, Yn, Zn = _WHITE
    dn = Xn + 15.0 * Yn + 3.0 * Zn
    unp = 4.0 * Xn / dn
    vnp = 9.0 * Yn / dn
    yr = Y / Yn
    eps = (6.0 / 29.0) ** 3
    L = np.where(yr > eps, 116.0 * np.cbrt(yr) - 16.0, (29.0 / 3.0) ** 3 * yr)
    u = 13.0 * L * (up - unp)
    v = 13.0 * L * (vp - vnp)
    return np.stack([L, u, v], axis=-1)


# ---- R-style matrix printing ----
def _r_format_col(col, digits=7):
    col = np.asarray(col, dtype=float)
    d = 0
    for v in col:
        s = f"{v:.{digits}g}"
        mant = s.split('e')[0].split('E')[0]
        dd = len(mant.split('.')[1]) if '.' in mant else 0
        if dd > d:
            d = dd
    return [f"{v:.{d}f}" for v in col]


def _print_matrix(m, digits=7, width=80):
    m = np.asarray(m, dtype=float)
    if m.ndim == 1:
        m = m.reshape(-1, 1)
    nrow, ncol = m.shape
    colstr = [_r_format_col(m[:, j], digits) for j in range(ncol)]
    colw = []
    for j in range(ncol):
        w = max(len(s) for s in colstr[j])
        w = max(w, len(f"[,{j + 1}]"))
        colw.append(w)
    labelw = len(f"[{nrow},]")

    blocks = []
    cur = []
    curw = labelw + 1
    for j in range(ncol):
        add = colw[j] + (1 if cur else 0)
        if cur and curw + add > width:
            blocks.append(cur)
            cur = []
            curw = labelw + 1
        cur.append(j)
        curw += colw[j] + (1 if len(cur) > 1 else 0)
    if cur:
        blocks.append(cur)

    out_lines = []
    for blk in blocks:
        header = " " * (labelw + 1) + " ".join(f"[,{j + 1}]".rjust(colw[j]) for j in blk)
        out_lines.append(header)
        for i in range(nrow):
            lbl = f"[{i + 1},]".rjust(labelw)
            cells = " ".join(colstr[j][i].rjust(colw[j]) for j in blk)
            out_lines.append(lbl + " " + cells)
    print("\n".join(out_lines))


# r2py:entity:r
def decode_colour(colour, alpha=False, to='rgb', white='D65', na_value=None):
    return np.array(colour, dtype=float)


# r2py:entity:h_luv
def convert_colour(colour, from_space, to_space, white_from='D65', white_to='D65'):
    arr = np.asarray(colour, dtype=float)
    if from_space == 'rgb':
        xyz = _rgb_to_xyz(arr)
    elif from_space == 'xyz':
        xyz = arr
    else:
        xyz = arr

    if to_space == 'xyz':
        return xyz
    elif to_space == 'lab':
        return _xyz_to_lab(xyz)
    elif to_space == 'luv':
        return _xyz_to_luv(xyz)
    return xyz


def _arr_to_lab(arr, space):
    arr = np.asarray(arr, dtype=float)
    if space == 'lab':
        return arr
    if space == 'rgb':
        return _xyz_to_lab(_rgb_to_xyz(arr))
    if space == 'xyz':
        return _xyz_to_lab(arr)
    return arr


# r2py:entity:compare_colour
def compare_colour(from_cols, to=None, from_space='rgb', to_space=None,
                   method='euclidean', white_from='D65', white_to='D65',
                   lightness=2, chroma=1):
    if to_space is None:
        to_space = from_space

    from_arr = np.asarray(from_cols, dtype=float)
    if to is None:
        to_arr = from_arr
        sym = True
    else:
        to_arr = np.asarray(to, dtype=float)
        sym = False

    if method == 'euclidean':
        res = np.zeros((len(from_arr), len(to_arr)))
        for i in range(len(from_arr)):
            res[i] = np.sqrt(((to_arr - from_arr[i]) ** 2).sum(axis=1))
    else:
        lab1 = _arr_to_lab(from_arr, from_space)
        lab2 = _arr_to_lab(to_arr, to_space)
        res = np.zeros((len(lab1), len(lab2)))
        if method == 'cie2000':
            for i in range(len(lab1)):
                res[i] = color.deltaE_ciede2000(lab1[i][None, :], lab2)
        elif method == 'cmc':
            for i in range(len(lab1)):
                res[i] = color.deltaE_cmc(lab1[i][None, :], lab2, kL=lightness, kC=chroma)

    if sym:
        res = np.triu(res)
        np.fill_diagonal(res, 0.0)
    return res


def r_rainbow(n):
    import colorsys
    h_vals = np.linspace(0, 1, n, endpoint=False)
    rgb = []
    for h in h_vals:
        rgb.append(colorsys.hsv_to_rgb(h, 1.0, 1.0))
    return np.array([[int(round(x * 255)) for x in c] for c in rgb])


# r2py:entity:h
def r_heat_colors(n):
    res = []
    for i in range(n):
        if i < 12:
            g = int(round(i * (255 / 11)))
            b = 0
        elif i == 12:
            g = 255
            b = 42
        elif i == 13:
            g = 255
            b = 128
        else:
            g = 255
            b = 213
        res.append([255, g, b])
    return np.array(res)


# r <- decode_colour(rainbow(10))
# r2py:entity:r
r = decode_colour(r_rainbow(10))

# h <- decode_colour(heat.colors(15))
# r2py:entity:h
h = decode_colour(r_heat_colors(15))

# Compare two sets of colours
# r2py:entity:compare_colour
res1 = compare_colour(r, h, from_space='rgb', method='cie2000')
_print_matrix(res1)

# Compare a set of colours with itself
# r2py:entity:compare_colour_1
res2 = compare_colour(r, from_space='rgb', method='cmc')
_print_matrix(res2)

# Compare colours from different colour spaces
# r2py:entity:h_luv
h_luv = convert_colour(h, 'rgb', 'luv')
# r2py:entity:compare_colour_2
res3 = compare_colour(r, h_luv, from_space='rgb', to_space='luv')
_print_matrix(res3)