# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/clock__rd_example__posixt-group_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__posixt-group_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def format_posix(idx, include_time=False):
    """Helper to mimic R's POSIXct print format."""
    fmt = '%Y-%m-%d %H:%M:%S %Z' if include_time else '%Y-%m-%d %Z'
    # R's %Z usually prints "EST", "UTC", etc.
    # Pandas %Z can be empty or "UTC-05:00". We ensure it's clean.
    res = []
    for ts in idx:
        s = ts.strftime(fmt)
        # Remove trailing space if %Z was empty
        s = s.rstrip()
        # R uses 'EST' for America/New_York. Pandas often uses 'EST'.
        res.append(s)
    return res

# r2py:entity:date_group
def date_group(x, precision, n=1):
    idx = pd.DatetimeIndex(x)
    
    if precision == "day":
        day_of_month = idx.day
        group_idx = (day_of_month - 1) // n
        # Create base: floor to start of month
        base = idx.to_period('M').to_timestamp()
        # Ensure base preserves timezone
        base = base.tz_localize(idx.tz) if base.tz is None else base.tz_convert(idx.tz)
        res = base + pd.to_timedelta(group_idx * n, unit='D')
        return res
        
    elif precision == "month":
        base = idx.to_period('M').to_timestamp()
        base = base.tz_localize(idx.tz) if base.tz is None else base.tz_convert(idx.tz)
        return base
        
    elif precision == "hour":
        hour_of_day = idx.hour
        group_idx = hour_of_day // n
        base = idx.normalize()
        res = base + pd.to_timedelta(group_idx * n, unit='h')
        return res
    
    return None

# x <- as.POSIXct("2019-01-01", "America/New_York")
# r2py:entity:x
x_start = pd.to_datetime("2019-01-01").tz_localize("America/New_York")

# x <- add_days(x, -3:5)
# r2py:entity:x_1
x = pd.DatetimeIndex([x_start + pd.Timedelta(days=i) for i in range(-3, 6)])

# date_group(x, "day", n = 2)
# r2py:entity:date_group
date_group_res = date_group(x, "day", n=2)
print(format_posix(date_group_res))

# date_group(x, "month")
# r2py:entity:date_group_1
date_group_month_res = date_group(x, "month")
print(format_posix(date_group_month_res))

# y <- as.POSIXct("2019-12-30", "America/New_York")
# y <- add_hours(y, 0:12)
# r2py:entity:y_1
y_start = pd.to_datetime("2019-12-30").tz_localize("America/New_York")
y = pd.DatetimeIndex([y_start + pd.Timedelta(hours=i) for i in range(13)])

# y
# r2py:entity:y_2
print(format_posix(y, include_time=True))

# date_group(y, "hour", n = 3)
# r2py:entity:date_group_2
date_group_hour_res = date_group(y, "hour", n=3)
print(format_posix(date_group_hour_res, include_time=True))