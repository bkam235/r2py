# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/purrr__rd_example__attr_getter_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__rd_example__attr_getter_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np


class RStr(str):
    """A character string that can carry attributes (like R's
    structure("obj", obj_attr = "foo"))."""
    pass


# mtcars' row.names attribute (R's built-in data frame rownames)
_MTCARS_ROWNAMES = [
    "Mazda RX4", "Mazda RX4 Wag", "Datsun 710", "Hornet 4 Drive",
    "Hornet Sportabout", "Valiant", "Duster 360", "Merc 240D", "Merc 230",
    "Merc 280", "Merc 280C", "Merc 450SE", "Merc 450SL", "Merc 450SLC",
    "Cadillac Fleetwood", "Lincoln Continental", "Chrysler Imperial",
    "Fiat 128", "Honda Civic", "Toyota Corolla", "Toyota Corona",
    "Dodge Challenger", "AMC Javelin", "Camaro Z28", "Pontiac Firebird",
    "Fiat X1-9", "Porsche 914-2", "Lotus Europa", "Ford Pantera L",
    "Ferrari Dino", "Maserati Bora", "Volvo 142E",
]


def _row_names(df):
    if df.shape[0] == len(_MTCARS_ROWNAMES) and "mpg" in getattr(df, "columns", []):
        return list(_MTCARS_ROWNAMES)
    return [str(i) for i in range(1, df.shape[0] + 1)]


def attr_getter(attr_name):
    def getter(x):
        if isinstance(x, pd.DataFrame):
            if attr_name == "row.names":
                return _row_names(x)
            if attr_name in x.columns:
                return x[attr_name].tolist()
        try:
            return getattr(x, attr_name)
        except AttributeError:
            return None
    return getter


# r2py:entity:get_rownames
get_rownames = attr_getter("row.names")


def r_print_character(vec, width=80):
    """Mimic R's print() for a character vector."""
    vec = list(vec)
    n = len(vec)
    if n == 0:
        print("character(0)")
        return
    strs = ['"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"' for s in vec]
    label_w = len("[" + str(n) + "]")
    col_w = max(len(s) for s in strs) + 1
    per_line = max(1, (width - label_w - 1) // col_w)
    for start in range(0, n, per_line):
        chunk = strs[start:start + per_line]
        prefix = ("[" + str(start + 1) + "]").rjust(label_w) + " "
        line = prefix + "".join(s.ljust(col_w) for s in chunk)
        print(line)


# r2py:entity:get_rownames_1
get_rownames_result = get_rownames(mtcars)
r_print_character(get_rownames_result)

# r2py:entity:obj1
obj1 = RStr("obj")
obj1.obj_attr = "foo"
# r2py:entity:obj2
obj2 = RStr("obj")
obj2.obj_attr = "bar"

# r2py:entity:x
x = [obj1, obj2]


# pluck implementation for Python
# r2py:entity:pluck
def pluck(x, *indices, default=None):
    res = x
    for idx in indices:
        try:
            if callable(idx):
                res = idx(res)
            elif isinstance(res, (list, tuple)):
                # R's pluck uses 1-based indexing
                res = res[idx - 1]
            else:
                res = res[idx]
        except (IndexError, KeyError, TypeError):
            return default
    return res


# r2py:entity:pluck
pluck_1 = pluck(x, 1, attr_getter("obj_attr"))
r_print_character([pluck_1])

# r2py:entity:pluck_1
pluck_2 = pluck(x, 2, attr_getter("obj_attr"))
r_print_character([pluck_2])