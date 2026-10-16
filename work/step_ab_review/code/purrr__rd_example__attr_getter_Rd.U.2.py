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

# R's attr_getter returns a function that retrieves a specific attribute.
# In Python, we can simulate this using a class or a closure.
def attr_getter(attr_name):
    def getter(x):
        if isinstance(x, pd.DataFrame) and attr_name == "row.names":
            return x.index.tolist()
        if hasattr(x, 'attrs') and isinstance(x.attrs, dict):
            return x.attrs.get(attr_name)
        return getattr(x, attr_name, None)
    return getter

# r2py:entity:get_rownames
get_rownames = attr_getter("row.names")

# r2py:entity:get_rownames_1
get_rownames_res = get_rownames(mtcars)
print(get_rownames_res)

# To mimic R's structure(), we create a simple object that holds a value and attributes.
class RObject:
    def __init__(self, value, **attrs):
        self.value = value
        self.attrs = attrs
    def __repr__(self):
        return str(self.value)

# r2py:entity:obj1
obj1 = RObject("obj", obj_attr="foo")
# r2py:entity:obj2
obj2 = RObject("obj", obj_attr="bar")

# r2py:entity:x
x = [obj1, obj2]

# pluck implementation: extracts deeply into a data structure.
# Supports 1-based indexing for lists (R style) and callable getters.
def pluck(x, *indices, default=None):
    res = x
    for idx in indices:
        try:
            if callable(idx):
                res = idx(res)
            elif isinstance(res, (list, tuple)):
                # R's pluck is 1-indexed
                res = res[idx - 1]
            else:
                res = res[idx]
        except (IndexError, KeyError, TypeError):
            return default
    return res

# r2py:entity:pluck
pluck_1 = pluck(x, 1, attr_getter("obj_attr"))
print(pluck_1)

# r2py:entity:pluck_1
pluck_2 = pluck(x, 2, attr_getter("obj_attr"))
print(pluck_2)