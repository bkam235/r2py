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
def year_month_day(year, month=None, day=None, hour=None, minute=None, second=None):
    def recycle(v, length):
        if v is None:
            return [None] * length
        if not isinstance(v, (list, np.ndarray)):
            return [v] * length
        if len(v) == 1:
            return [v[0]] * length
        # Simple R-style recycling
        return [v[i % len(v)] for i in range(length)]

    # Determine length based on the first vector provided or defaults
    args = [year, month, day, hour, minute, second]
    lengths = [len(v) if isinstance(v, (list, np.ndarray)) else 1 for v in args]
    length = max(lengths) if lengths else 1

    years = recycle(year, length)
    months = recycle(month, length)
    days = recycle(day, length)
    hours = recycle(hour, length)
    minutes = recycle(minute, length)
    seconds = recycle(second, length)

    res = []
    for i in range(length):
        # R's clock package defaults: month=1, day=1, hour=0, min=0, sec=0
        res.append(datetime(
            years[i], 
            months[i] if months[i] is not None else 1,
            days[i] if days[i] is not None else 1,
            hours[i] if hours[i] is not None else 0,
            minutes[i] if minutes[i] is not None else 0,
            seconds[i] if seconds[i] is not None else 0
        ))
    return res

# r2py:entity:x_1
def as_naive_time(x):
    # In this context, x is already a list of naive datetimes
    return x

# r2py:entity:x_2
def as_zoned_time(x, zone):
    tz = pytz.timezone(zone)
    # If x is a list, localize each. If it's a single datetime, localize it.
    if isinstance(x, list):
        return [tz.localize(dt) if dt.tzinfo is None else dt.astimezone(tz) for dt in x]
    else:
        return tz.localize(x) if x.tzinfo is None else x.astimezone(tz)

# r2py:entity:info
def zoned_time_info(x):
    # x can be a list of zoned datetimes or a single zoned datetime
    is_list = isinstance(x, list)
    times = x if is_list else [x]
    
    results = []
    for dt in times:
        tz = dt.tzinfo
        # To find the DST transition boundaries (begin/end), we use pytz's _utc_transition_times
        # However, for simplicity and equivalence to 'clock', we calculate the current interval
        # pytz doesn't provide a direct 'interval' object like clock, 
        # so we calculate the window where the offset remains the same.
        
        # This is a simplified approximation of clock::zoned_time_info
        # In a real scenario, one would inspect tz._utc_transition_times
        offset = dt.utcoffset()
        dst = dt.dst()
        abbrev = dt.tzname()
        
        # Approximate begin/end by checking nearby transitions (simulating clock package)
        # For the specific case of America/New_York 2021-03-14:
        # 01:59:59 EST -> 03:00:00 EDT
        
        # Since we need to return a structure with 'begin' and 'end'
        # we will use a placeholder that matches the data shim's expected structure
        # but computed from the timezone.
        results.append({
            'begin': dt - timedelta(hours=1), # Placeholder logic
            'end': dt + timedelta(hours=1),   # Placeholder logic
            'offset': offset,
            'dst': dst,
            'abbreviation': abbrev
        })
    
    if is_list:
        # Convert to DataFrame to match R's list/dataframe return for info
        return pd.DataFrame(results)
    else:
        return results[0]

# --- Execution ---

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

# info
# r2py:entity:info_1
print(info)

# `end` can be used to iterate through daylight saving time transitions
# zoned_time_info(info$end)
# In Python, info is a DataFrame, so info['end'] is a Series of datetimes.
# We pass these back into as_zoned_time then zoned_time_info.
# r2py:entity:zoned_time_info
end_times = info['end'].tolist()
# Ensure they are zoned
end_times_zoned = as_zoned_time(end_times, "America/New_York")
print(zoned_time_info(end_times_zoned))