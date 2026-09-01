# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/roxygen2__vignette__reuse_s12.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'roxygen2__vignette__reuse_s12.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['letters']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import string

# r2py:entity:alphabet
def alphabet(n):
    letters = list(string.ascii_lowercase)
    return ", ".join([f"`{l}`" for l in letters[:n]])