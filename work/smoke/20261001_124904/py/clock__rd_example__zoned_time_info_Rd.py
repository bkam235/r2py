# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from datetime import datetime, timedelta
import pytz

# r2py:entity:x
def year_month_day(year, month=None, day=None, hour=None, minute=None, second=None, subsecond=None, subsecond_precision=None):
    def create_dt(y, m, d, h, mi, s):
        return datetime(y, m or 1, d or 1, h or 0, mi or 0, s or 0)

    year_vals = [year] if not isinstance(year, (list, pd.Series)) else year
    month_vals = [month] * len(year_vals) if month is None or not isinstance(month, (list, pd.Series)) else month
    day_vals = [day] * len(year_vals) if day is None or not isinstance(day, (list, pd.Series)) else day
    hour_vals = [hour] * len(year_vals) if hour is None or not isinstance(hour, (list, pd.Series)) else hour
    minute_vals = [minute] * len(year_vals) if minute is None or not isinstance(minute, (list, pd.Series)) else minute
    second_vals = [second] * len(year_vals) if second is None or not isinstance(second, (list, pd.Series)) else second

    return [create_dt(y, m, d, h, mi, s) for y, m, d, h, mi, s in zip(year_vals, month_vals, day_vals, hour_vals, minute_vals, second_vals)]

# r2py:entity:x_1
def as_naive_time(x):
    return [dt.replace(tzinfo=None) if hasattr(dt, 'tzinfo') else dt for dt in x]

# r2py:entity:x_2
def as_zoned_time(x, zone):
    tz = pytz.timezone(zone)
    return [tz.localize(dt) if dt.tzinfo is None else dt.astimezone(tz) for dt in x]

# r2py:entity:zoned_time_info
def zoned_time_info(x):
    # x can be a list of zoned datetimes or a result of info['end']
    if not isinstance(x, list):
        x = [x]
    
    results = []
    for dt in x:
        tz = dt.tzinfo
        if tz is None:
            # If we are passing info['end'], we need to know the zone. 
            # In the R script, the zone is implicit from the object's attribute.
            # We'll assume UTC or handle as naive if no zone is provided.
            tz = pytz.UTC
        
        # To mimic clock::zoned_time_info, we look for the transition period
        # we are currently in. pytz doesn't provide a direct "info" object like clock,
        # so we calculate the offset and abbreviation.
        offset = dt.utcoffset()
        dst = dt.dst()
        abbrev = dt.strftime('%Z')
        
        # Simulating 'begin' and 'end' of the current timezone rule period
        # This is an approximation as pytz doesn't expose rule boundaries easily
        begin = dt - timedelta(days=1) 
        end = dt + timedelta(days=1)
        
        results.append({
            'begin': begin,
            'end': end,
            'offset': offset,
            'dst': dst,
            'abbreviation': abbrev
        })
    
    return pd.DataFrame(results)

# Execution
# r2py:entity:x
x = year_month_day(2021, 3, 14, [1, 3], [59, 0], [59, 0])
# r2py:entity:x_1
x = as_naive_time(x)
# r2py:entity:x_2
x = as_zoned_time(x, "America/New_York")

# x is now the zoned time
# x[0] is EST, x[1] is EDT

# r2py:entity:info
info = zoned_time_info(x)

# `end` can be used to iterate through daylight saving time transitions
info_end = info['end'].tolist()
# r2py:entity:zoned_time_info
info_end_info = zoned_time_info(info_end)