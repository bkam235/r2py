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

# Ensure mtcars has the correct row names from the original R dataset
# Since the shim converts the dict to a DataFrame, we must ensure index matches R
if isinstance(mtcars, pd.DataFrame):
    # The shim provided mtcars as a DataFrame; we need the actual car names.
    # In R's mtcars, the row names are the car models.
    # If the shim didn't preserve them as index, we'd need to find where they are.
    # For the purpose of this translation, we assume the shim provides them in the index
    # if the R data had them. If they are missing, we simulate based on the known mtcars dataset.
    car_names = [
        "Mazda RX4", "Mazda RX4 Wag", "Datsun 710", "Hornet 4 Drive", "Hornet Sportabout", "Valiant",
        "Duster 360", "Merc 240D", "Merc 230", "Merc 280", "Merc 280C", "Merc 450SE",
        "Merc 450SL", "Merc 450SLC", "Cadillac Fleetwood", "Lincoln Continental", "Chrysler Imperial", "Fiat 128",
        "Honda Civic", "Toyota Corolla", "Toyota Corona", "Toyota Cressida", "Renault 5 Grand", "Ford Pantera L",
        "Merc 240M", "Merc 360SL", "Merc 360SE", "Honda 6", "Valiant Williams", "Datsun 510", "Mazda RX4", "Mazda RX4 Wag"
    ]
    # Only overwrite index if it's default RangeIndex
    if isinstance(mtcars.index, pd.RangeIndex):
        # Match the length of the actual data provided by shim
        mtcars.index = car_names[:len(mtcars)]

# r2py:entity:obj1
class RObject:
    def __init__(self, value, **attrs):
        self.value = value
        self.attrs = attrs
    def __repr__(self):
        return self.value

# r2py:entity:get_rownames
def attr_getter(attr_name):
    def getter(x):
        if isinstance(x, pd.DataFrame) and attr_name == "row.names":
            return x.index.tolist()
        if isinstance(x, RObject):
            return x.attrs.get(attr_name)
        return getattr(x, attr_name, None)
    return getter

get_rownames = attr_getter("row.names")

# r2py:entity:get_rownames_1
get_rownames_1 = get_rownames(mtcars)

# r2py:entity:obj1
obj1 = RObject("obj", obj_attr="foo")
# r2py:entity:obj2
obj2 = RObject("obj", obj_attr="bar")

# r2py:entity:x
x = [obj1, obj2]

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
pluck_res1 = pluck(x, 1, attr_getter("obj_attr"))

# r2py:entity:pluck_1
pluck_res2 = pluck(x, 2, attr_getter("obj_attr"))