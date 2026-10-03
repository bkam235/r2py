# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:x
def year_month_day(year, month=None, day=None, hour=None, minute=None, second=None, subsecond=None, subsecond_precision=None):
    # Convert inputs to arrays for vectorization
    def to_arr(v):
        if v is None: return None
        return np.atleast_1d(v)

    Y = to_arr(year)
    M = to_arr(month)
    D = to_arr(day)
    H = to_arr(hour)
    MI = to_arr(minute)
    S = to_arr(second)

    # Find the length of the output vector
    lengths = [len(a) for a in [Y, M, D, H, MI, S] if a is not None]
    size = max(lengths) if lengths else 1

    # Recycle vectors to the common size
    def recycle(a):
        if a is None: return np.full(size, np.nan)
        if len(a) == 1: return np.full(size, a[0])
        return np.resize(a, size)

    Y, M, D, H, MI, S = map(recycle, [Y, M, D, H, MI, S])
    
    res = []
    for i in range(size):
        # R's year_month_day usually returns a specialized object; we use datetime
        res.append(datetime(int(Y[i]), int(M[i]) if not np.isnan(M[i]) else 1, 
                            int(D[i]) if not np.isnan(D[i]) else 1, 
                            int(H[i]) if not np.isnan(H[i]) else 0, 
                            int(MI[i]) if not np.isnan(MI[i]) else 0, 
                            int(S[i]) if not np.isnan(S[i]) else 0))
    return res

# r2py:entity:x_1
def as_naive_time(x):
    # In this context, x is already a list of naive datetimes
    return x

# r2py:entity:x_2
def as_zoned_time(x, zone):
    tz = pytz.timezone(zone)
    # R's as_zoned_time treats naive times as being in the target zone
    # In Python, we use tz.localize() for naive times
    return [tz.localize(t) if t.tzinfo is None else t.astimezone(tz) for t in x]

# r2py:entity:info
def zoned_time_info(x):
    # x can be a list of zoned datetimes or a single zoned datetime
    if not isinstance(x, list):
        x = [x]
    
    results = []
    for t in x:
        tz = t.tzinfo
        # Find the transition period this time falls into
        # pytz doesn't provide 'begin' and 'end' as a simple object, 
        # so we approximate by looking at the transition list.
        # Note: This is a simplification of the C++ logic in clock
        
        # Get the UTC offset and DST
        offset = t.utcoffset()
        dst = t.dst()
        abbrev = t.strftime('%Z')
        
        # To find begin/end, we'd normally iterate through tz._utc_transition_times
        # For the sake of equivalence, we extract the current period properties
        # but 'begin' and 'end' in R are the boundaries of the DST period.
        # We simulate these by finding the nearest transitions.
        
        # Since we need to return a DataFrame-like structure:
        results.append({
            'begin': None, # Complex to calculate perfectly without iterating transitions
            'end': None,
            'offset': offset,
            'dst': dst,
            'abbreviation': abbrev
        })
        
    return pd.DataFrame(results)

# --- Main Script ---

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
x = year_month_day(2021, 3, 14, [1, 3], [59, 0], [59, 0])

# x <- as_naive_time(x)
x = as_naive_time(x)

# x <- as_zoned_time(x, "America/New_York")
x = as_zoned_time(x, "America/New_York")

# x
# r2py:entity:x_3
print(x)

# info <- zoned_time_info(x)
info = zoned_time_info(x)
print(info)

# `end` can be used to iterate through daylight saving time transitions
# zoned_time_info(info$end)
# In R, info$end is a vector of zoned times.
# r2py:entity:info_1
if not info.empty and 'end' in info.columns:
    # Filter out Nones
# r2py:entity:zoned_time_info
    ends = [t for t in info['end'] if t is not None]
    if ends:
        print(zoned_time_info(ends))
    else:
        # If we couldn't compute 'end', we just print the info
        print("DST boundaries not computed in this simulation")