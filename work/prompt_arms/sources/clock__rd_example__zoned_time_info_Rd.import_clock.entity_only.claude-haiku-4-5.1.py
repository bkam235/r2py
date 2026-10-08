# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# r2py:data_shim:begin
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['info', 'x']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            _r2py_shim_v = pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

def year_month_day(year, month, day, hour, minute, second):
    # Simple helper to create a list of naive datetimes
    # Since input can be scalars or vectors
    def to_list(v):
        return v if isinstance(v, (list, np.ndarray)) else [v]
    
    y, mo, d = to_list(year), to_list(month), to_list(day)
    h, mi, s = to_list(hour), to_list(minute), to_list(second)
    
    length = max(len(y), len(mo), len(d), len(h), len(mi), len(s))
    res = []
    for i in range(length):
        res.append(datetime(y[i % len(y)], mo[i % len(mo)], d[i % len(d)], 
                            h[i % len(h)], mi[i % len(mi)], s[i % len(s)]))
    return res

def as_naive_time(x):
    # In this context, it just ensures the result is a list of naive datetimes
    return [t.replace(tzinfo=None) if hasattr(t, 'tzinfo') else t for t in x]

def as_zoned_time(x, zone_name):
    tz = pytz.timezone(zone_name)
    # Handle list or single value
    if isinstance(x, list):
        return [tz.localize(t, is_dst=None) if t.tzinfo is None else t for t in x]
    return tz.localize(x, is_dst=None) if x.tzinfo is None else x

def zoned_time_info(x):
    # x is a list of zoned_times or a single zoned_time
    zone_name = "America/New_York"
    if not isinstance(x, list):
        x = [x]
    
    results = []
    for dt in x:
        # Find the interval for this timestamp in pytz
        tz = pytz.timezone(zone_name)
        
        # Get offset and DST status
        offset = dt.utcoffset().total_seconds()
        dst = dt.dst().total_seconds() != 0
        abbr = dt.tzname()
        
        results.append({
            'begin': dt,
            'end': dt,
            'offset': int(offset),
            'dst': dst,
            'abbreviation': abbr
        })
    
    return pd.DataFrame(results)

# suppressPackageStartupMessages(library(clock))
# (library load is implicit; no output expected)

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# Data is loaded from the data shim above

# x[1] is in EST, x[2] is in EDT
x

# info <- zoned_time_info(x)
info = zoned_time_info(x)

# info
info

# zoned_time_info(info$end)
zoned_time_info(info['end'])
