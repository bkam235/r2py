# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/rlang__rd_example__missing_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'rlang__rd_example__missing_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['na_int', 'na_lgl']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np

# r2py:entity:typeof
def typeof(x):
    if x is None:
        return "NULL"
    if isinstance(x, bool) or (isinstance(x, float) and np.isnan(x)):
        # In R, NA is logically a logical type by default
        return "logical"
    if isinstance(x, int):
        return "integer"
    if isinstance(x, float):
        return "double"
    return type(x).__name__

# Define rlang-style NA aliases

# r2py:entity:typeof
print(typeof(np.nan))
# r2py:entity:typeof_1
print(typeof(na_lgl))
# r2py:entity:typeof_2
print(typeof(na_int))

# Note that while the base R missing symbols cannot be overwritten,
# that's not the case for rlang's aliases:
# r2py:entity:na_dbl
na_dbl = np.nan
# r2py:entity:typeof_3
print(typeof(na_dbl))