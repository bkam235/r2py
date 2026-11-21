# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/textshaping__rd_example__get_font_features_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'textshaping__rd_example__get_font_features_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['random_font']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import os
import random
import pandas as pd
from fontTools.ttLib import TTFont

try:
    import winreg
except ImportError:
    winreg = None


# r2py:entity:suppressPackageStartupMessages
# no-op: library(textshaping) has no Python equivalent
suppressPackageStartupMessages = lambda *a, **k: None


# r2py:entity:sys_fonts
_WEIGHT_NAMES = {
    100: "thin",
    200: "extralight",
    300: "light",
    350: "semilight",
    400: "normal",
    500: "medium",
    600: "semibold",
    700: "bold",
    800: "extrabold",
    900: "heavy",
}

_WIDTH_NAMES = {
    1: "ultra-condensed",
    2: "extra-condensed",
    3: "condensed",
    4: "normal",
    5: "semi-expanded",
    6: "expanded",
    7: "extra-expanded",
    8: "ultra-expanded",
    9: "ultra-expanded",
}


def _weight_name(w):
    try:
        w = int(w)
    except (TypeError, ValueError):
        return "normal"
    if w in _WEIGHT_NAMES:
        return _WEIGHT_NAMES[w]
    best = min(_WEIGHT_NAMES, key=lambda k: abs(k - w))
    return _WEIGHT_NAMES[best]


def _font_dirs():
    dirs = []
    windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot") or r"C:\Windows"
    dirs.append(os.path.join(windir, "Fonts"))
    localappdata = os.environ.get("LOCALAPPDATA")
    if localappdata:
        dirs.append(os.path.join(localappdata, "Microsoft", "Windows", "Fonts"))
    return dirs


def _font_record(font, path, index):
    name_table = None
    try:
        if "name" in font:
            name_table = font["name"]
    except Exception:
        name_table = None

    def _get(nid):
        if name_table is None:
            return None
        try:
            return name_table.getDebugName(nid)
        except Exception:
            return None

    family = _get(16) or _get(1) or ""
    style = _get(17) or _get(2) or "Regular"
    psname = _get(6) or _get(4) or os.path.splitext(os.path.basename(path))[0]

    weight = "normal"
    width = "normal"
    italic = "italic" in style.lower()
    try:
        if "OS/2" in font:
            os2 = font["OS/2"]
            weight = _weight_name(getattr(os2, "usWeightClass", 400))
            wc = getattr(os2, "usWidthClass", 4)
            width = _WIDTH_NAMES.get(int(wc), "normal")
            fs = getattr(os2, "fsSelection", 0)
            if fs & 1:
                italic = True
    except Exception:
        pass

    monospace = False
    try:
        if "post" in font:
            monospace = bool(getattr(font["post"], "isFixedPitch", 0))
    except Exception:
        pass

    variable = False
    try:
        variable = "fvar" in font
    except Exception:
        pass

    return {
        "path": path,
        "index": index,
        "name": psname,
        "family": family,
        "style": style,
        "weight": weight,
        "width": width,
        "italic": italic,
        "monospace": monospace,
        "variable": variable,
    }


def _registry_font_files():
    """Return list of font filenames registered in the Windows Fonts registry."""
    files = []
    if winreg is None:
        return files
    subkey = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            key = winreg.OpenKey(hive, subkey)
        except OSError:
            continue
        i = 0
        while True:
            try:
                _name, value, _vt = winreg.EnumValue(key, i)
            except OSError:
                break
            i += 1
            if isinstance(value, str) and value:
                files.append(value)
        try:
            winreg.CloseKey(key)
        except Exception:
            pass
    return files


def _process_font_file(fp, rows, seen_paths):
    try:
        _tt = TTFont(fp, fontNumber=0)
    except Exception:
        return
    try:
        _num = getattr(_tt.reader, "numFonts", 1) or 1
    except Exception:
        _num = 1
    for _i in range(_num):
        try:
            if _i == 0:
                _f = _tt
            else:
                _f = TTFont(fp, fontNumber=_i)
            rows.append(_font_record(_f, fp, _i))
            if _i != 0:
                try:
                    _f.close()
                except Exception:
                    pass
        except Exception:
            continue
    try:
        _tt.close()
    except Exception:
        pass
    seen_paths.add(fp.lower())


_rows = []
_seen = set()
_allowed = (".ttf", ".ttc", ".otf", ".fon")

_primary_dir = _font_dirs()[0]

# 1) Registry-registered fonts, in registry order
for _regname in _registry_font_files():
    _base = os.path.basename(_regname)
    _fp = os.path.join(_primary_dir, _base)
    if not os.path.isfile(_fp):
        continue
    if _fp.lower() in _seen:
        continue
    if not _base.lower().endswith(_allowed):
        continue
    _process_font_file(_fp, _rows, _seen)

# 2) Remaining files in the font directories, alphabetical
for _d in _font_dirs():
    if not os.path.isdir(_d):
        continue
    try:
        _entries = sorted(os.listdir(_d), key=lambda s: s.upper())
    except OSError:
        continue
    for _fn in _entries:
        if not _fn.lower().endswith(_allowed):
            continue
        _fp = os.path.join(_d, _fn)
        if _fp.lower() in _seen:
            continue
        _process_font_file(_fp, _rows, _seen)

sys_fonts = pd.DataFrame(
    _rows,
    columns=[
        "path",
        "index",
        "name",
        "family",
        "style",
        "weight",
        "width",
        "italic",
        "monospace",
        "variable",
    ],
)


# r2py:entity:sample
# random_font <- sys_fonts$family[sample(nrow(sys_fonts), 1)]
try:
    _had_rf = isinstance(globals().get("random_font"), str)
except Exception:
    _had_rf = False
if not _had_rf:
    random.randrange(max(len(sys_fonts), 1))
    if len(sys_fonts) > 0:
        random_idx = random.randrange(len(sys_fonts))
        random_font = sys_fonts["family"].iloc[random_idx]
    else:
        random_font = ""
else:
    # keep RNG parity with R's single sample() draw
    random.randrange(max(len(sys_fonts), 1))


def _scan_find_family(family):
    """Fallback: scan font dirs for a family, returning (path, index) pairs."""
    fam_l = str(family).lower()
    found = []
    for _d in _font_dirs():
        if not os.path.isdir(_d):
            continue
        try:
            _entries = os.listdir(_d)
        except OSError:
            continue
        for _fn in _entries:
            if not _fn.lower().endswith((".ttf", ".ttc", ".otf")):
                continue
            _fp = os.path.join(_d, _fn)
            try:
                _tt = TTFont(_fp, fontNumber=0)
            except Exception:
                continue
            try:
                _num = getattr(_tt.reader, "numFonts", 1) or 1
            except Exception:
                _num = 1
            for _i in range(_num):
                try:
                    _f = _tt if _i == 0 else TTFont(_fp, fontNumber=_i)
                    _rec = _font_record(_f, _fp, _i)
                    if _rec["family"].lower() == fam_l:
                        found.append((_fp, _i))
                    if _i != 0:
                        try:
                            _f.close()
                        except Exception:
                            pass
                except Exception:
                    continue
            try:
                _tt.close()
            except Exception:
                pass
    return found


# r2py:entity:get_font_features
def get_font_features(family="", italic=False, bold=False, path=None, index=0):
    if path is None:
        sel = sys_fonts[sys_fonts["family"] == family]
        if len(sel) == 0:
            sel = sys_fonts[sys_fonts["family"].str.lower() == str(family).lower()]
        if len(sel) > 0:
            paths = list(sel["path"])
            indices = list(sel["index"])
        else:
            found = _scan_find_family(family)
            if len(found) == 0:
                return [[]]
            paths = [fp for fp, _ in found]
            indices = [ix for _, ix in found]
    else:
        if not isinstance(path, (list, tuple)):
            path = [path]
        paths = list(path)
        if not isinstance(index, (list, tuple)):
            index = [index] * len(paths)
        indices = list(index)

    out = []
    for p, idx in zip(paths, indices):
        feats = []
        try:
            font = TTFont(str(p), fontNumber=int(idx))
            if "GSUB" in font:
                gsub = font["GSUB"].table
                fl = getattr(gsub, "FeatureList", None)
                if fl is not None and getattr(fl, "FeatureRecord", None):
                    for fr in fl.FeatureRecord:
                        feats.append(fr.FeatureTag)
            font.close()
        except Exception:
            feats = []
        seen = []
        for x in feats:
            if x not in seen:
                seen.append(x)
        out.append(seen)
    return out


result = get_font_features(family=random_font)

if len(result) == 0:
    pass
else:
    for _i, _v in enumerate(result, 1):
        print("[[%d]]" % _i)
        if len(_v) == 0:
            print("character(0)")
        else:
            print("[1] " + " ".join('"%s"' % _x for _x in _v))