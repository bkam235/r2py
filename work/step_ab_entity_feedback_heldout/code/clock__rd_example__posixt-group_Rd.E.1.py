# Translated from <R script> by r2py v0.3.0

import pandas as pd
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/clock__rd_example__posixt-group_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__posixt-group_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
import numpy as np
from pandas.tseries.offsets import MonthBegin

def format_posix(idx, include_time=False):
    """Helper to mimic R's POSIXct print format."""
    fmt = '%Y-%m-%d %H:%M:%S %Z' if include_time else '%Y-%m-%d %Z'
    res = []
    for ts in idx:
        s = ts.strftime(fmt)
        s = s.rstrip()
        res.append(s)
    return res

# r2py:entity:date_group
def date_group(x, precision, n=1):
    idx = pd.DatetimeIndex(x)
    
    if precision == "day":
        # R's date_group(x, "day", n=2) groups by n days within the month.
        # It resets at the start of the month.
        day_of_month = idx.day
        group_idx = (day_of_month - 1) // n
        
        # Calculate the start of the month for each element
        # Using MonthBegin(1) and adjusting to get the 1st of the current month
        bases = (idx - pd.to_timedelta(idx.day - 1, unit='D')).normalize()
        
        res = bases + pd.to_timedelta(group_idx * n, unit='D')
        return res
        
    elif precision == "month":
        # Group by month means floor to the 1st of the month
        bases = (idx - pd.to_timedelta(idx.day - 1, unit='D')).normalize()
        return bases
        
    elif precision == "hour":
        # Group by hour of the day.
        hour_of_day = idx.hour
        group_idx = hour_of_day // n
        base = idx.normalize()
        res = base + pd.to_timedelta(group_idx * n, unit='h')
        return res
    
    return None

# x <- as.POSIXct("2019-01-01", "America/New_York")
# r2py:entity:x
x = pd.Timestamp("2019-01-01").tz_localize("America/New_York")

# x <- add_days(x, -3:5)
# r2py:entity:x_1
x = pd.DatetimeIndex([x + pd.Timedelta(days=i) for i in range(-3, 6)])

# date_group(x, "day", n = 2)
# r2py:entity:date_group
date_group_res = date_group(x, "day", n=2)
print(format_posix(date_group_res))

# date_group(x, "month")
# r2py:entity:date_group_1
date_group_month_res = date_group(x, "month")
print(format_posix(date_group_month_res))

# y <- as.POSIXct("2019-12-30", "America/New_York")
# r2py:entity:y_1
y = pd.Timestamp("2019-12-30").tz_localize("America/New_York")

# y <- add_hours(y, 0:12)
# r2py:entity:y_1_update
y = pd.DatetimeIndex([y + pd.Timedelta(hours=i) for i in range(13)])

# y
# r2py:entity:y_2
print(format_posix(y, include_time=True))

# date_group(y, "hour", n = 3)
# r2py:entity:date_group_2
date_group_hour_res = date_group(y, "hour", n=3)
print(format_posix(date_group_hour_res, include_time=True))