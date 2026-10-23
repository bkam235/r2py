# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/stringr__vignette__from-base_s14.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'stringr__vignette__from-base_s14.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['fruit']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re


# base
# grep(pattern = "g", x = fruit, value = TRUE)
# r2py:entity:grep
res_grep = [s for s in fruit if re.search("g", s)]
print(res_grep)

# stringr
# str_subset(fruit, pattern = "g")
# r2py:entity:str_subset
res_str_subset = [s for s in fruit if re.search("g", s)]
print(res_str_subset)