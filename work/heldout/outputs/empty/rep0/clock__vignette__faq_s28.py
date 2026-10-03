# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/clock__vignette__faq_s28.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__vignette__faq_s28.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# r2py:entity:raw
raw = [
    "2015-12-31T23:59:59", 
    "2015-12-31T23:59:60", # A real leap second!
    "2016-01-01T00:00:00"
]

# r2py:entity:x
# Python's datetime and pandas.to_datetime generally do not support leap seconds (60).
# To handle the leap second without crashing and preserve the sequence, 
# we replace '23:59:60' with '23:59:59' or use a custom parser.
# Standard behavior in data science stacks is to treat the 60th second as the start of the next second or the end of current.
processed_raw = [s.replace("23:59:60", "23:59:59") for s in raw]

# r2py:entity:x_1
print(x)