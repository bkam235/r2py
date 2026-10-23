# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__sys_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__sys_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'info2', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# Define the times
# R's year_month_day is essentially creating timestamps
# r2py:entity:x
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]

# r2py:entity:x_2
# x <- as_zoned_time(x, "America/New_York")
tz_ny = pytz.timezone("America/New_York")

# r2py:entity:x_3
print(x)

# r2py:entity:x_sys
# x_sys <- as_sys_time(x)
# System time in Python is typically UTC
x_sys = [t.astimezone(pytz.UTC) for t in x]

# r2py:entity:sys_time_info
def get_sys_time_info(sys_time, zone_name):
    tz = pytz.timezone(zone_name)
    # Get the timezone transition info for the specific timestamp
    # In Python, we can get the offset for a specific datetime
    localized = sys_time.astimezone(tz)
    offset = localized.utcoffset()
    
    # sys_time_info in R provides the boundaries of the current offset period
    # Python's pytz doesn't have a direct 'begin/end' method for intervals, 
    # so we simulate the info object
    return {
        "offset": offset,
        "begin": localized, # Simplified substitute
        "end": localized    # Simplified substitute
    }

# r2py:entity:info_1
print(info)

# data_frame creation
# r2py:entity:data_frame
df = pd.DataFrame({
    "x": x,
    "begin": [info["begin"]], 
    "end": [info["end"]]
})
print(df)

# sys_time_info(info$end, zoned_time_zone(x))
info_end = get_sys_time_info(info["end"], "America/New_York")
print(info_end)

# r2py:entity:zones
zones = ["America/New_York", "America/Los_Angeles"]

# r2py:entity:info2
# info2 <- sys_time_info(x_sys[1], zones)
info2_list = [get_sys_time_info(x_sys[0], z) for z in zones]
# r2py:entity:info2_1
print(info2_list)

# r2py:entity:data_frame_1
# data_frame(zone = zones, naive_time = x_sys[1] + info2$offset)
naive_times_calc = [x_sys[0] + info["offset"] for info in info2_list]
df2 = pd.DataFrame({
    "zone": zones,
    "naive_time": naive_times_calc
})
print(df2)