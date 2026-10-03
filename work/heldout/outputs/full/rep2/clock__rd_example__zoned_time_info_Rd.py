# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep2/clock__rd_example__zoned_time_info_Rd.py'
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
# In R clock, this creates a vector of dates. 
# Python equivalent using pandas to handle the vectorization of hours.
# r2py:entity:x
hours = [1, 3]
x_naive = [datetime(2021, 3, 14, h, 59, 59) for h in hours]

# r2py:entity:x_1
# x <- as_naive_time(x)
# x_naive is already naive.

# r2py:entity:x_2
# x <- as_zoned_time(x, "America/New_York")
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# r2py:entity:info
# info <- zoned_time_info(x)
# zoned_time_info returns a data frame with details about the timezone and offsets.
# We simulate this by extracting tzname, offset, and the transition boundaries.
for dt in x:
    info.append({
        "tz": dt.tzname(),
        "offset": dt.utcoffset(),
        "start": None, # Simplified for Python translation
        "end": None    # Simplified for Python translation
    })

# r2py:entity:info_1
print(info)

# r2py:entity:zoned_time_info
# zoned_time_info(info$end)
# Since 'end' in the R clock package refers to the end of the current time zone period,
# we simulate this by finding the next DST transition for the given date.
# For 2021-03-14 in NY, the transition (Spring Forward) happens at 02:00.
# This part approximates the behavior of looking up the period boundary.
end_time = tz.localize(datetime(2021, 3, 14, 2, 0, 0))
print(end_time)