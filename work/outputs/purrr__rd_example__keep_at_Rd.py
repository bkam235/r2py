# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/purrr__rd_example__keep_at_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'purrr__rd_example__keep_at_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import string

# r2py:entity:x
x = pd.Series({'a': 1, 'b': 2, 'cat': 10, 'dog': 15, 'elephant': 5, 'e': 10})

# keep_at(letters)
# r2py:entity:keep_at
print(x[x.index.isin(list(string.ascii_lowercase))])

# discard_at(letters)
# r2py:entity:discard_at
print(x[~x.index.isin(list(string.ascii_lowercase))])

# keep_at(\(x) nchar(x) == 3)
# r2py:entity:keep_at_1
print(x[x.index.map(lambda x: len(x) == 3)])

# discard_at(\(x) nchar(x) == 3)
# r2py:entity:discard_at_1
print(x[~x.index.map(lambda x: len(x) == 3)])