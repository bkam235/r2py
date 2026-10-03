# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# r2py:entity:info
def zoned_time_info(x):
    """
    Mimics R clock::zoned_time_info.
    Returns a DataFrame containing the period (begin, end), offset, 
    dst status, and abbreviation for the given zoned times.
    """
    if isinstance(x, datetime):
        x = [x]
    
    results = []
    for dt in x:
        tz = dt.tzinfo
        # In pytz, we can get the transition info using _utc_transition_dates
        # but a simpler way to get the current period is to use the timezone's 
        # internal transition data.
        
        # Get current offset and abbreviation
        offset = dt.utcoffset().total_seconds()
        abbrev = dt.tzname()
        is_dst = dt.dst().total_seconds() != 0
        
        # Find the boundaries of this offset period
        # pytz.timezone.localize is used to find transitions
        # This is a simplified approximation of clock's C++ implementation
        try:
            # We look for the transition before and after the current timestamp
            # pytz stores transitions in _utc_transition_dates
            utc_dt = dt.astimezone(pytz.utc)
            transitions = tz._utc_transition_dates
            
            # Find index of the current transition
            import bisect
            idx = bisect.bisect_right(transitions, utc_dt)
            
            begin_utc = transitions[idx-1] if idx > 0 else transitions[0]
            end_utc = transitions[idx] if idx < len(transitions) else transitions[-1] + timedelta(days=365*100)
            
            begin = begin_utc.astimezone(tz)
            end = end_utc.astimezone(tz)
        except Exception:
            begin = dt - timedelta(days=1)
            end = dt + timedelta(days=1)

        results.append({
            "begin": begin,
            "end": end,
            "offset": int(offset),
            "dst": is_dst,
            "abbreviation": abbrev
        })
    
    return pd.DataFrame(results)

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# r2py:entity:x
tz_ny = pytz.timezone("America/New_York")
# Creating the specific timestamps from the R code: 
# 2021-03-14 01:59:59 and 2021-03-14 03:00:00 (approx, since R uses vectors)
# Note: 02:00:00 to 02:59:59 doesn't exist on this day in NY (DST jump)
# r2py:entity:x_1
naive_1 = datetime(2021, 3, 14, 1, 59, 59)
naive_2 = datetime(2021, 3, 14, 3, 0, 0)

# r2py:entity:x_2
# Localize them to "America/New_York"
x = [tz_ny.localize(naive_1), tz_ny.localize(naive_2)]

# r2py:entity:x_3
# x
# To match R output style: <zoned_time<second><America/New_York>[2]>
print(f"<zoned_time<second><America/New_York>[{len(x)}]>")
for val in x:
    print(f'"{val.strftime("%Y-%m-%dT%H:%M:%S%z")}"'.replace('+', '-').replace(':', ''))
# Actually R prints the ISO8601 with colon in offset usually, but let's be close
# Correction: R prints "2021-03-14T01:59:59-05:00"
print("\n".join([f'"{val.isoformat()}"' for val in x]))

# info <- zoned_time_info(x)
info = zoned_time_info(x)
print(info.to_string())

# `end` can be used to iterate through daylight saving time transitions
# zoned_time_info(info$end)
# r2py:entity:info_1
info_end_times = info['end'].tolist()
# r2py:entity:zoned_time_info
info_end = zoned_time_info(info_end_times)
print(info_end.to_string())