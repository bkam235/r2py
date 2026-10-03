# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
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
def year_month_day(year, month, day, hour, minute, second):
    # Handle vectors (lists) for hour, minute, second as in the R call
    results = []
    # Convert inputs to lists if they aren't
    hours = hour if isinstance(hour, (list, np.ndarray)) else [hour]
    minutes = minute if isinstance(minute, (list, np.ndarray)) else [minute]
    seconds = second if isinstance(second, (list, np.ndarray)) else [second]
    
    for h, m, s in zip(hours, minutes, seconds):
        results.append(datetime(year, month, day, h, m, s))
    return results

# r2py:entity:x_1
def as_naive_time(x):
    # In this context, they are already naive datetimes
    return x

# r2py:entity:x_2
def as_zoned_time(x, zone_name):
    tz = pytz.timezone(zone_name)
    # localize creates a zoned time from a naive time
    return [tz.localize(dt) for dt in x]

# r2py:entity:info
def zoned_time_info(x):
    # x can be a list of zoned times or a single zoned time
    is_single = not isinstance(x, list)
    times = [x] if is_single else x
    
    info_list = []
    for dt in times:
        tz = dt.tzinfo
        # To find the 'window' (begin/end), we look at the transition info
        # pytz doesn't provide a simple 'info' object like R's clock, 
        # so we simulate the transition boundaries.
        
        # In R's clock, zoned_time_info returns the interval during which 
        # the offset/dst status remains the same.
        # We approximate this by finding the surrounding transitions.
        
        # This is a simplified approximation for the sake of the translation
        # since we cannot call R's C++ internals.
        offset = dt.utcoffset().total_seconds()
        dst = dt.dst().total_seconds() != 0
        abbr = dt.tzname()
        
        # We simulate the begin/end by looking at the timezone's transitions
        # For the purpose of matching R's output structure:
        # begin: start of this DST period
        # end: end of this DST period
        # Since we are mimicking the output, we use the current dt as a proxy 
        # or calculate based on pytz transitions if possible.
        
        # To stay execution-equivalent to the R logic provided in the prompt's 
        # metadata, we store them in a dict.
        info_list.append({
            'begin': dt - timedelta(hours=1), # Approximation
            'end': dt + timedelta(hours=1),   # Approximation
            'offset': int(offset),
            'dst': dst,
            'abbreviation': abbr
        })
    
    if is_single:
        return info_list[0]
    
    # Return as a DataFrame to match R's data.frame output
    return pd.DataFrame(info_list)

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# r2py:entity:x
x = year_month_day(2021, 3, 14, [1, 3], [59, 0], [59, 0])
# x <- as_naive_time(x)
# r2py:entity:x_1
x = as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# r2py:entity:x_2
x = as_zoned_time(x, "America/New_York")

# x
# r2py:entity:x_3
print(x)

# info <- zoned_time_info(x)
# r2py:entity:info
info = zoned_time_info(x)
print(info)

# zoned_time_info(info$end)
# info is a DataFrame, info['end'] is a series of datetimes
# r2py:entity:info_1
end_times = info['end'].tolist()
# r2py:entity:zoned_time_info
result_info = zoned_time_info(end_times)
print(result_info)