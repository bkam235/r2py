# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/clock__vignette__faq_s28.py'
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

# sys_time_parse in the clock package returns NA for leap seconds (seconds == 60)
# because POSIX time (which sys_time represents) does not support them.
# r2py:entity:x
def sys_time_parse(raw_vals):
    parsed = []
    for val in raw_vals:
        # Check for leap second pattern :60
        if ":60" in val:
            parsed.append(pd.NaT)
        else:
            try:
                parsed.append(pd.to_datetime(val))
            except:
                parsed.append(pd.NaT)
    return pd.DatetimeIndex(parsed)

x = sys_time_parse(raw)

# The R output for x shows the type <sys_time<second>[3]> and the values.
# We print the result to match the expected logic.
# r2py:entity:x_1
print(x)