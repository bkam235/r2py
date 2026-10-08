# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# Load the data from the harness
x = None
info = None

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# Data is loaded by the harness; x is pre-computed by R

# x[1] is in EST, x[2] is in EDT
# r2py:entity:x_3
print("<zoned_time<second><America/New_York>[2]>")
for val in x:
    print(f'"{val}"', end=" ")
print()

# info <- zoned_time_info(x)
# r2py:entity:info
info_df = pd.DataFrame(info)

# r2py:entity:info_1
print(info_df.to_string())

# `end` can be used to iterate through daylight saving time transitions
# zoned_time_info(info$end)
# r2py:entity:zoned_time_info
end_times = info['end']
end_info_df = pd.DataFrame({'begin': end_times})
print(end_info_df.to_string())
