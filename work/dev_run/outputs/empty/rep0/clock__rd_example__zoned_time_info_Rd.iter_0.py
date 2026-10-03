# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# In Python, we use datetime and pytz to handle zoned time
# Constructing the specific timestamps
# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# r2py:entity:x
dt_list = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 59, 59)
]

# r2py:entity:x_1
# x <- as_naive_time(x) 
# dt_list is already naive

# r2py:entity:x_2
# x <- as_zoned_time(x, "America/New_York")
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# r2py:entity:info
# info <- zoned_time_info(x)
# Python doesn't have a direct 'zoned_time_info' object, 
# but we can extract the timezone metadata and offsets.
for dt in x:
    info.append({
        'tz': dt.tzinfo,
        'utc_offset': dt.utcoffset(),
        'dst': dt.dst()
    })

print(info)

# r2py:entity:zoned_time_info
# zoned_time_info(info$end)
# Approximating the 'end' of the timezone info (the last element)
# r2py:entity:info_1
last_info = info[-1]
print(last_info)