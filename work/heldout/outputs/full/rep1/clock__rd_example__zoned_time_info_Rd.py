# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/clock__rd_example__zoned_time_info_Rd.py'
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
# R: x <- as_naive_time(x)
# R: x <- as_zoned_time(x, "America/New_York")
# Creating timestamps for the DST transition gap in NY (2021-03-14 02:00:00)
# r2py:entity:x_2
times_naive = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]
tz = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# R: info <- zoned_time_info(x)
# Note: zoned_time_info in R returns a list of transition info. 
# In Python, we can access the tzinfo and transition details.

# r2py:entity:info_1
print(info)

# R: zoned_time_info(info$end)
# Since 'info' in R is a structured object containing the transition window:
# We simulate getting the info for the end of the transition period
# r2py:entity:zoned_time_info
end_time = datetime(2021, 3, 14, 3, 0, 0)
end_zoned = tz.localize(end_time)
info_end = end_zoned.tzinfo

print(info_end)