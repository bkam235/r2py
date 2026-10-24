import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/purrr__rd_example__attr_getter_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__rd_example__attr_getter_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# R's attr_getter returns a function that accesses an attribute
def attr_getter(attr):
    def getter(x):
        if isinstance(x, pd.DataFrame) and attr == "row.names":
            return x.index.tolist()
        if hasattr(x, 'attrs') and isinstance(x.attrs, dict):
            return x.attrs.get(attr)
        return getattr(x, attr, None)
    return getter

# r2py:entity:get_rownames
get_rownames = attr_getter("row.names")

# r2py:entity:get_rownames_1
# Use print to mimic R's auto-printing
print(get_rownames(mtcars))

# Custom object to mimic R's structure() which adds attributes to a value
class RObject(str):
    def __new__(cls, value, **attrs):
        obj = super(RObject, cls).__new__(cls, value)
        obj.attrs = attrs
        return obj

# r2py:entity:obj1
obj1 = RObject("obj", obj_attr="foo")
# r2py:entity:obj2
obj2 = RObject("obj", obj_attr="bar")

# r2py:entity:x
x = [obj1, obj2]

# pluck implementation: supports positional indexing and attribute getters
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
# Use print to mimic R's auto-printing
print(pluck(x, 1, attr_getter("obj_attr")))

# r2py:entity:pluck_1
# Use print to mimic R's auto-printing
print(pluck(x, 2, attr_getter("obj_attr")))