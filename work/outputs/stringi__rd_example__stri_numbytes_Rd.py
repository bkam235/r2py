# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringi__rd_example__stri_numbytes_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringi__rd_example__stri_numbytes_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# In Python, the equivalent of stri_numbytes (byte length of UTF-8 encoded string)
# is to encode the string to utf-8 and find the length of the resulting bytes object.

# r2py:entity:stri_numbytes
print([len(s.encode('utf-8')) for s in letters])

# r2py:entity:stri_numbytes_1
test_strings = ['abc', '123', '\u0105\u0104']
print([len(s.encode('utf-8')) for s in test_strings])

# Compare byte length vs character length
# r2py:entity:stri_numbytes_2
emoji = '\U0001F600'
print(len(emoji.encode('utf-8'))) # Equivalent to stri_numbytes
print(len(emoji))                 # Equivalent to stri_length