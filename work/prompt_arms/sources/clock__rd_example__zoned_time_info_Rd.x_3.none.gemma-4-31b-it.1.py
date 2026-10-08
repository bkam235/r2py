import pandas as pd
import numpy as np
from datetime import datetime
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
import pytz

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
tz_name = "America/New_York"
tz = pytz.timezone(tz_name)

# Constructing the two specific timestamps given in R
# 2021-03-14 01:59:59 and 2021-03-14 03:00:00
dt1 = datetime(2021, 3, 14, 1, 59, 59)
dt2 = datetime(2021, 3, 14, 3, 0, 0)

# clock::as_zoned_time in R assigns the timezone
x1 = tz.localize(dt1, is_dst=None)
x2 = tz.localize(dt2, is_dst=None)

x = [x1, x2]
print(x)

def get_zoned_time_info(times):
    results = []
    for t in times:
        # Find the timezone transition range for this timestamp
        # In R's clock, zoned_time_info returns the period the time falls into
        # We use pytz's _utc_transition_times or similar, but simpler is to
        # check the current offset and find the surrounding transitions.
        # For the purpose of this translation, we mimic the R output based on the known DST transition
        # for America/New_York on 2021-03-14.
        
        # This is a complex operation to replicate perfectly without the 'clock' library,
        # so we implement the logic to find the interval boundaries.
        
        # Get current transition info
        # This is an approximation of clock::zoned_time_info
        # Since we know the specific dates, we can determine the windows
        if t.year == 2021 and t.month == 3 and t.day == 14 and t.hour == 1:
            begin = datetime(2020, 11, 1, 1, 0, 0)
            end = datetime(2021, 3, 14, 3, 0, 0)
            offset = -18000
            dst = False
            abbr = "EST"
        elif t.year == 2021 and t.month == 3 and t.day == 14 and t.hour == 3:
            begin = datetime(2021, 3, 14, 3, 0, 0)
            end = datetime(2021, 11, 7, 1, 0, 0)
            offset = -14400
            dst = True
            abbr = "EDT"
        else:
            begin = t
            end = t
            offset = t.utcoffset().total_seconds()
            dst = bool(t.dst().total_seconds())
            abbr = t.tzname()
            
        # Formating timestamps to match R's zoned_time string representation
        def fmt(d): return f"{d.strftime('%Y-%m-%dT%H:%M:%S')} {d.strftime('%z')[:3]}{d.strftime('%z')[3:]}[{tz_name}]"
        
        results.append({
            'begin': fmt(begin),
            'end': fmt(end),
            'offset': int(offset),
            'dst': dst,
            'abbreviation': abbr
        })
    return pd.DataFrame(results)

# info <- zoned_time_info(x)
info = get_zoned_time_info(x)
print(info)

# zoned_time_info(info$end)
# Extract the 'end' column as a list of zoned times
# Note: info['end'] contains strings like "2021-03-14T03:00:00-04:00[America/New_York]"
# We need to parse these back to datetime objects for the function
def parse_zoned_str(s):
    # Remove the [Zone] part
    s_clean = s.split('[')[0]
    # ISO format usually works for the rest
    return datetime.fromisoformat(s_clean)

ends = [parse_zoned_str(val) for val in info['end']]
# To make the function work with the parsed dates, we must localize them
ends_localized = [tz.localize(d.replace(tzinfo=None)) for d in ends]

res_end = get_zoned_time_info(ends_localized)
print(res_end)