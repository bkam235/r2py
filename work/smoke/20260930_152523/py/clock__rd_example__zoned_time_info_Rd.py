# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
import pytz
from datetime import datetime

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# Note: 2021-03-14 02:00:00 is the DST transition in NY. 
# R's clock handles the gap/overlap. In Python, we create the naive datetimes then localize.
# r2py:entity:x_2
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# r2py:entity:info
# info <- zoned_time_info(x)
# In Python, we extract the timezone information from the datetime objects

# r2py:entity:info_1
print(info)

# r2py:entity:zoned_time_info
# zoned_time_info(info$end)
# Since info['end'] is a list of tzinfo objects, we print the first one's details
print(info["end"][0])