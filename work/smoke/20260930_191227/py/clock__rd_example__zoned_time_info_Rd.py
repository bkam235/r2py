# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_191227/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# The R code creates two timestamps: 2021-03-14 01:59:59 and 2021-03-14 03:59:59
# These are interpreted as naive and then localized to New York (where DST transition occurs on March 14)
# r2py:entity:x
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 59, 59)
]
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# info <- zoned_time_info(x)
# In Python, we can extract the timezone information (offset and DST status)
# r2py:entity:info
for t in x:
    info.append({
        "offset": t.utcoffset(),
        "dst": t.dst(),
        "tzname": t.tzname()
    })

# r2py:entity:info_1
print(info)

# zoned_time_info(info$end)
# Since info is a list of dicts in Python, we simulate accessing the last element's offset info
# r2py:entity:zoned_time_info
last_info = info[-1]
print(last_info)