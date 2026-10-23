# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringr__rd_example__str_detect_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringr__rd_example__str_detect_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re
import string

# r2py:entity:str_detect
def str_detect(string_val, pattern, negate=False):
    if isinstance(string_val, (list, tuple)):
        # Vectorized over string
        results = [bool(re.search(pattern, s)) for s in string_val]
    elif isinstance(pattern, (list, tuple)):
        # Vectorized over pattern
        results = [bool(re.search(p, string_val)) for p in pattern]
    else:
        # Single string and single pattern
        results = [bool(re.search(pattern, string_val))]
    
    if negate:
        return [not r for r in results]
    return results

# r2py:entity:fruit
fruit = ["apple", "banana", "pear", "pineapple"]
# r2py:entity:str_detect
print(str_detect(fruit, "a"))
# r2py:entity:str_detect_1
print(str_detect(fruit, "^a"))
# r2py:entity:str_detect_2
print(str_detect(fruit, "a$"))
# r2py:entity:str_detect_3
print(str_detect(fruit, "b"))
# r2py:entity:str_detect_4
print(str_detect(fruit, "[aeiou]"))

# Also vectorised over pattern
# r2py:entity:str_detect_5
print(str_detect("aecfg", letters))

# Returns TRUE if the pattern do NOT match
# r2py:entity:str_detect_6
print(str_detect(fruit, "^p", negate=True))