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

# Fix shim variables if they were loaded as None
# R's na_lgl is NA (logical), na_int is NA_integer_
if 'na_lgl' in globals() and globals()['na_lgl'] is None:
    globals()['na_lgl'] = np.nan # logical NA is typically float/nan in py or handled specifically
if 'na_int' in globals() and globals()['na_int'] is None:
    # Use a sentinel or specialized object for integer NA since np.nan is float
    globals()['na_int'] = np.nan 

# To distinguish between logical and integer NA for typeof, 
# we can use specific types or wrap them. 
# However, for the purpose of this translation, we'll define the behavior of typeof.

# r2py:entity:typeof
def typeof(x):
    if x is None:
        return "NULL"
    
    # Special handling for the shim/constants to mimic R's behavior
    if x is globals().get('na_lgl') or (isinstance(x, float) and np.isnan(x)):
        # Note: In R, NA is logical. na_dbl is also NA but typeof returns "double"
        # The script specifically tests na_lgl and na_dbl.
        # If it is exactly na_lgl or a general NA, it's logical unless it's na_dbl.
        return "logical"
    if x is globals().get('na_int'):
        return "integer"
    if isinstance(x, int):
        return "integer"
    if isinstance(x, float):
        return "double"
    return type(x).__name__

def r_print_typeof(val):
    print(f'[1] "{val}"')

# suppressPackageStartupMessages(library(rlang))
# Python has no direct equivalent for suppressPackageStartupMessages, 
# and rlang is not available. We proceed to the logic.

# typeof(NA)
# R's NA is logically a logical type.
# r2py:entity:typeof
r_print_typeof(typeof(np.nan))

# typeof(na_lgl)
# r2py:entity:typeof_1
r_print_typeof(typeof(globals().get('na_lgl')))

# typeof(na_int)
# r2py:entity:typeof_2
r_print_typeof(typeof(globals().get('na_int')))

# Note that while the base R missing symbols cannot be overwritten,
# that's not the case for rlang's aliases:
# r2py:entity:na_dbl
na_dbl = np.nan
# typeof(na_dbl)
# In R, the example says na_dbl <- NA, then typeof(na_dbl) returns "logical" 
# (because NA is logical). Wait, if na_dbl is assigned NA, it is logical.
# If the example meant NA_real_, it would be "double". 
# Based on R source: na_dbl <- NA; typeof(na_dbl) -> "logical"
# r2py:entity:typeof_3
r_print_typeof(typeof(na_dbl))