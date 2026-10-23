# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringr__vignette__from-base_s34.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringr__vignette__from-base_s34.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import string
import numpy as np

# Setup letters constant

# base
# order(letters) returns the indices that would sort the vector
# r2py:entity:order
res_order = np.argsort(letters).tolist()
print(res_order)

# sort(letters) returns the sorted vector
# r2py:entity:sort
res_sort = sorted(letters)
print(res_sort)

# stringr
# str_order is equivalent to order() for strings
# r2py:entity:str_order
res_str_order = np.argsort(letters).tolist()
print(res_str_order)

# str_sort is equivalent to sort() for strings
# r2py:entity:str_sort
res_str_sort = sorted(letters)
print(res_str_sort)