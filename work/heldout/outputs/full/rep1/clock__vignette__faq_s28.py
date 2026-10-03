# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/clock__vignette__faq_s28.py'
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

# Python's standard datetime and pandas.to_datetime do not support leap seconds (60s).
# To approximate sys_time_parse, we handle the leap second by treating 60 as 00 of the next minute.
# r2py:entity:x
def parse_leap_seconds(ts_list):
    parsed = []
    for ts in ts_list:
        if ":60" in ts:
            # Replace :60 with :00 and add 1 second to the resulting timestamp
            normalized = ts.replace(":60", ":00")
            dt = pd.to_datetime(normalized) + pd.Timedelta(seconds=1)
            parsed.append(dt)
        else:
            parsed.append(pd.to_datetime(ts))
    return pd.DatetimeIndex(parsed)


# r2py:entity:x_1
print(x)