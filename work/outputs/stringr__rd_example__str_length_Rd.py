# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringr__rd_example__str_length_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringr__rd_example__str_length_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# In Python, len() is the equivalent of str_length()
# For handling NA, we use pandas series or numpy arrays

# str_length(letters)
# r2py:entity:str_length
print([len(s) for s in letters])

# str_length(NA)
# r2py:entity:str_length_1
print(len(None) if None else None) # Returns None/Error; in pandas:
print(pd.Series([None]).str.len().tolist())

# str_length(factor("abc"))
# Factors are categorical; usually converted to string
# r2py:entity:str_length_2
print(len(str("abc")))

# str_length(c("i", "like", "programming", NA))
# r2py:entity:str_length_3
vec = pd.Series(["i", "like", "programming", None])
print(vec.str.len().tolist())

# x <- c("\u6c49\u5b57", "\U0001f60a")
# r2py:entity:x
x = ["\u6c49\u5b57", "\U0001f60a"]
# r2py:entity:str_view
print(x) # str_view equivalent
# str_width is specific to display columns; Python's len() counts code points
# r2py:entity:str_length_4
print([len(s) for s in x]) # str_length equivalent

# u <- c("\u00fc", "u\u0308")
# r2py:entity:u
u = ["\u00fc", "u\u0308"]
# Python len() counts code points. 
# For combined characters (u + umlaut), len is 2.
# r2py:entity:str_length_5
print([len(s) for s in u]) 

# str_sub(u, 1, 1)
# r2py:entity:str_sub
print([s[0:1] for s in u])