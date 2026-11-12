import pandas as pd
import numpy as np

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/clock__rd_example__posixt-group_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__posixt-group_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['y']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def format_posix(idx, include_time=False):
    """Helper to mimic R's POSIXct print format."""
    fmt = '%Y-%m-%d %H:%M:%S %Z' if include_time else '%Y-%m-%d %Z'
    res = []
    for ts in idx:
        s = ts.strftime(fmt)
        s = s.rstrip()
        res.append(s)
    return res

def date_group(x, precision, n=1):
    idx = pd.DatetimeIndex(x)
    
    if precision == "day":
        day_of_month = idx.day
        group_idx = (day_of_month - 1) // n
        # Create base: floor to start of month without using to_period (to avoid warnings)
        # We create a timestamp at the start of the month with the same timezone
        year_month = idx.to_period('M').year * 100 + idx.to_period('M').month # Not quite right for vector
        # Correct vectorized way to get start of month:
        base = pd.DatetimeIndex([pd.Timestamp(year=ts.year, month=ts.month, day=1).tz_localize(idx.tz[0]) if hasattr(idx, 'tz') and idx.tz else pd.Timestamp(year=ts.year, month=ts.month, day=1) for ts in idx])
        res = base + pd.to_timedelta(group_idx * n, unit='D')
        return res
        
    elif precision == "month":
        base = pd.DatetimeIndex([pd.Timestamp(year=ts.year, month=ts.month, day=1).tz_localize(idx.tz[0]) if hasattr(idx, 'tz') and idx.tz else pd.Timestamp(year=ts.year, month=ts.month, day=1) for ts in idx])
        return base
        
    elif precision == "hour":
        hour_of_day = idx.hour
        group_idx = hour_of_day // n
        base = idx.normalize()
        res = base + pd.to_timedelta(group_idx * n, unit='h')
        return res
    
    return None

# x <- as.POSIXct("2019-01-01", "America/New_York")
x = pd.to_datetime("2019-01-01").tz_localize("America/New_York")

# x <- add_days(x, -3:5)
# We use the original x to generate the sequence, then update x
x_start = x
x = pd.DatetimeIndex([x_start + pd.Timedelta(days=i) for i in range(-3, 6)])

# date_group(x, "day", n = 2)
res_date_group = date_group(x, "day", n=2)
print(format_posix(res_date_group))

# date_group(x, "month")
res_date_group_month = date_group(x, "month")
print(format_posix(res_date_group_month))

# y <- as.POSIXct("2019-12-30", "America/New_York")
y_start = pd.to_datetime("2019-12-30").tz_localize("America/New_York")

# y <- add_hours(y, 0:12)
y = pd.DatetimeIndex([y_start + pd.Timedelta(hours=i) for i in range(13)])

# y
print(format_posix(y, include_time=True))

# date_group(y, "hour", n = 3)
res_date_group_hour = date_group(y, "hour", n=3)
print(format_posix(res_date_group_hour, include_time=True))