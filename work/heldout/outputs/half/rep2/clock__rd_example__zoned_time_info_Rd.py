# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# R: x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# Creating a list of datetime objects to simulate the vector nature of the R clock call
# r2py:entity:x
x_naive = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]

# r2py:entity:x_1
# R: x <- as_naive_time(x)
# x_naive is already naive

# r2py:entity:x_2
# R: x <- as_zoned_time(x, "America/New_York")
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# r2py:entity:info
# R: info <- zoned_time_info(x)
# In Python, timezone information for a specific instance is accessed via the tzinfo object
# and the utcoffset() / dst() methods.
for dt in x:
    info.append({
        'start': dt.tzinfo,
        'offset': dt.utcoffset(),
        'dst': dt.dst(),
        'zone': dt.tzinfo.zone
    })

# r2py:entity:info_1
print(info)

# r2py:entity:zoned_time_info
# R: zoned_time_info(info$end)
# The 'end' in clock's zoned_time_info refers to the transition boundary.
# In Python, we can approximate this by checking the offset of the specific timestamp.
for item in info:
    print(item['start'])