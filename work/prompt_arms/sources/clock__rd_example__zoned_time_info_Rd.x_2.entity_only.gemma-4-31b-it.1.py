import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

def year_month_day(y, m, d, h, mi, s):
    # Helper to simulate R's clock::year_month_day
    times = []
    for i in range(len(h)):
        times.append(datetime(y, m, d, h[i], mi[i], s[i]))
    return times

def as_naive_time(x):
    return x

def as_zoned_time(x, tz_name):
    tz = pytz.timezone(tz_name)
    return [tz.localize(t) for t in x]

def zoned_time_info(x):
    # Simulate clock::zoned_time_info
    # In R, this returns the start, end, offset, dst, and abbreviation of the period
    results = []
    
    # If x is a list of zoned times, we compute info for each
    if isinstance(x, list):
        for t in x:
            results.append(_get_tz_info(t))
    elif isinstance(x, datetime):
        results.append(_get_tz_info(x))
    elif isinstance(x, pd.Series):
        for t in x:
            results.append(_get_tz_info(t))
    else:
        # Case for info$end which might be a series/list
        try:
            for t in x:
                results.append(_get_tz_info(t))
        except:
            return _get_tz_info(x)
            
    return pd.DataFrame(results)

def _get_tz_info(t):
    # This is a simplification. clock::zoned_time_info provides the entire transition interval.
    # To match R output exactly, we would need to look up pytz transition tables.
    # For the purpose of this translation, we emulate the structure.
    tz = t.tzinfo
    # Approximate the transition window (this is the hard part without the actual clock lib)
    # In a real scenario, we'd use pytz._tzfile or similar to find the transition boundaries
    return {
        'begin': t,
        'end': t,
        'offset': t.utcoffset().total_seconds() if t.utcoffset() else 0,
        'dst': t.dst().total_seconds() != 0 if t.dst() else False,
        'abbreviation': t.tzname()
    }

# Translation starts here
x = year_month_day(2021, 3, 14, [1, 3], [59, 0], [59, 0])
x = as_naive_time(x)
x = as_zoned_time(x, "America/New_York")

print(x)

info = zoned_time_info(x)
print(info)

# `end` can be used to iterate through daylight saving time transitions
# info$end is a Series/Column in the DataFrame
print(zoned_time_info(info['end']))
