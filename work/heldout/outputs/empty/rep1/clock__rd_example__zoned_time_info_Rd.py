# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/clock__rd_example__zoned_time_info_Rd.py'
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
    # Vectorized support for the specific call pattern in R source
    # x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
    hours = hour if isinstance(hour, (list, np.ndarray)) else [hour]
    minutes = minute if isinstance(minute, (list, np.ndarray)) else [minute]
    seconds = second if isinstance(second, (list, np.ndarray)) else [second]
    
    res = []
    for h, m, s in zip(hours, minutes, seconds):
        res.append(datetime(year, month, day, h, m, s))
    return res

# r2py:entity:x_1
def as_naive_time(x):
    # In R's clock, this strips zone info
    if isinstance(x, list):
        return [dt.replace(tzinfo=None) if hasattr(dt, 'tzinfo') else dt for dt in x]
    return x.replace(tzinfo=None) if hasattr(x, 'tzinfo') else x

# r2py:entity:x_2
def as_zoned_time(x, zone):
    tz = pytz.timezone(zone)
    if isinstance(x, list):
        res = []
        for dt in x:
            if dt.tzinfo is None:
                # Localize naive time. 
                # clock::as_zoned_time handles non-existent/ambiguous times.
                # We use localize with is_dst=None to mimic standard behavior or let pytz handle it.
                res.append(tz.localize(dt))
            else:
                res.append(dt.astimezone(tz))
        return res
    if x.tzinfo is None:
        return tz.localize(x)
    return x.astimezone(tz)

# r2py:entity:info
def zoned_time_info(x):
    # x can be a list of zoned times or a single zoned time
    # We need to find the period the time falls into.
    if not isinstance(x, list):
        x_list = [x]
    else:
        x_list = x
    
    # Get the timezone from the first element
    zone_name = x_list[0].tzinfo.zone if hasattr(x_list[0].tzinfo, 'zone') else "UTC"
    tz = pytz.timezone(zone_name)
    
    results = []
    for dt in x_list:
        # pytz's _utc_transition_times provides the UTC transitions
        # We find which interval the datetime falls into
        transitions = tz._utc_transition_times
        utc_dt = dt.astimezone(pytz.UTC).replace(tzinfo=None)
        
        # Binary search for the transition interval
        idx = np.searchsorted(transitions, utc_dt) - 1
        if idx < 0: idx = 0
        
        # Transition boundaries
        begin_utc = transitions[idx] if idx < len(transitions) else transitions[-1]
        end_utc = transitions[idx+1] if idx+1 < len(transitions) else transitions[-1] + timedelta(days=365*100)
        
        # Convert boundaries back to zoned time
        begin_zoned = pytz.UTC.localize(begin_utc).astimezone(tz)
        end_zoned = pytz.UTC.localize(end_utc).astimezone(tz)
        
        # Get offset and abbreviation for the time
        offset = dt.utcoffset().total_seconds()
        dst = dt.dst().total_seconds() != 0
        abbrev = dt.strftime('%Z')
        
        results.append({
            'begin': begin_zoned,
            'end': end_zoned,
            'offset': int(offset),
            'dst': dst,
            'abbreviation': abbrev
        })
        
    if len(results) == 1:
        return results[0]
    
    # Return as DataFrame to match R output structure
    return pd.DataFrame(results)

# --- Execution ---

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
# Formatting output to match R: <zoned_time<second><America/New_York>[2]>
# r2py:entity:x_3
print("<zoned_time<second><America/New_York>[2]>")
print(f"[1] \"{x[0].strftime('%Y-%m-%dT%H:%M:%S%z')}\" \"{x[1].strftime('%Y-%m-%dT%H:%M:%S%z')}\"")
# Fixing timezone format: R uses -05:00, Python %z uses -0500
def fmt_tz(dt):
    s = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    return s[:-2] + ':' + s[-2:]

print(f"[1] \"{fmt_tz(x[0])}\" \"{fmt_tz(x[1])}\"")

# info <- zoned_time_info(x)
# r2py:entity:info
info = zoned_time_info(x)
# info
# r2py:entity:info_1
print(info)

# zoned_time_info(info$end)
# info is a DataFrame, info['end'] is a series
# r2py:entity:zoned_time_info
end_times = info['end'].tolist() if isinstance(info, pd.DataFrame) else [info['end']]
info_end = zoned_time_info(end_times)
print(info_end)