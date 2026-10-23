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

def attr_getter(attr_name):
    """
    R's attr_getter(name) returns a function that extracts the attribute 'name' from an object.
    """
    def getter(x):
        # Special case for row.names on pandas DataFrames (matching R's mtcars behavior)
        if attr_name == "row.names" and isinstance(x, pd.DataFrame):
            return x.index.tolist()
        
        # Check for a custom __r_attrs__ dictionary to simulate R attributes
        if hasattr(x, "__r_attrs__"):
            return x.__r_attrs__.get(attr_name)
            
        # Fallback to standard getattr
        return getattr(x, attr_name, None)
    return getter

def structure(obj, **attrs):
    """
    Simulates R's structure() by attaching attributes to an object.
    """
    class Wrapped:
        def __init__(self, val, attrs):
            self.val = val
            self.__r_attrs__ = attrs
        def __repr__(self):
            return repr(self.val)
        def __str__(self):
            return str(self.val)
    return Wrapped(obj, attrs)

def pluck(x, *indices):
    """
    Extracts a value from a nested structure. 
    Supports numeric indices (1-based) and callable getters.
    """
    res = x
    for idx in indices:
        if callable(idx):
            res = idx(res)
        elif isinstance(res, (list, tuple)):
            # R uses 1-based indexing
            res = res[idx - 1]
        else:
            # Try as key/attribute
            try:
                res = res[idx]
            except (TypeError, KeyError, IndexError):
                res = getattr(res, str(idx), None)
    return res

# r2py:entity:get_rownames
get_rownames = attr_getter("row.names")

# r2py:entity:get_rownames_1
get_rownames_1 = get_rownames(mtcars)

# r2py:entity:obj1
obj1 = structure("obj", obj_attr="foo")
# r2py:entity:obj2
obj2 = structure("obj", obj_attr="bar")

# r2py:entity:x
x = [obj1, obj2]

# r2py:entity:pluck
pluck_res1 = pluck(x, 1, attr_getter("obj_attr"))

# r2py:entity:pluck_1
pluck_res2 = pluck(x, 2, attr_getter("obj_attr"))