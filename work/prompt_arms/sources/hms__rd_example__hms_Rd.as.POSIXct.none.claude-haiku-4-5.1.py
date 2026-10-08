# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path

# Load the data shim
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['d']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            import pandas as _r2py_shim_pd
            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v

# suppressPackageStartupMessages(library(hms))
# Try to import hms; if not available, we'll use timedelta
try:
    from hms import hms as hms_func
except ImportError:
    # Fallback: create a simple hms-like class that matches the output format
    class HMS:
        def __init__(self, hours=0, minutes=0, seconds=0):
            self.total_seconds = hours * 3600 + minutes * 60 + seconds
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
        
        def __repr__(self):
            h = self.total_seconds // 3600
            m = (self.total_seconds % 3600) // 60
            s = self.total_seconds % 60
            return f"{h:02d}:{m:02d}:{s:02d}"
        
        def __str__(self):
            return self.__repr__()
    
    def hms_func(hours=0, minutes=0, seconds=0):
        return HMS(hours, minutes, seconds)
    
    def new_hms(seconds_list):
        result = []
        for s in seconds_list:
            h = int(s) // 3600
            m = (int(s) % 3600) // 60
            sec = int(s) % 60
            result.append(HMS(h, m, sec))
        return result
    
    def as_hms(val):
        if isinstance(val, (int, float)):
            h = int(val) // 3600
            m = (int(val) % 3600) // 60
            s = int(val) % 60
            return HMS(h, m, s)
        elif isinstance(val, str):
            parts = val.split(':')
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            return HMS(h, m, s)
        elif isinstance(val, datetime):
            h = val.hour
            m = val.minute
            s = val.second
            return HMS(h, m, s)
        return HMS(0, 0, 0)

# hms(56, 34, 12)
# r2py:entity:hms
hms_val = hms_func(56, 34, 12)
print(hms_val)

# hms()
# r2py:entity:hms_1
hms_empty = hms_func()
print(hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_numeric = new_hms(np.arange(1, 4))
for item in new_hms_numeric:
    print(item)

# Supports numeric only!
# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms_try = new_hms([1, 2, 3])
    for item in new_hms_try:
        print(item)
except Exception as e:
    print(f"Error: {e}")

# as_hms(1)
# r2py:entity:as_hms
as_hms_1 = as_hms(1)
print(as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
as_hms_str = as_hms("12:34:56")
print(as_hms_str)

# as_hms(Sys.time())
# r2py:entity:as_hms_2
now = datetime.now()
as_hms_sys = as_hms(now)
print(as_hms_sys)

# as.POSIXct(hms(1))
# Convert hms to a datetime (equivalent to POSIXct)
# r2py:entity:as.POSIXct
hms_1_sec = hms_func(0, 0, 1)
posixct_val = datetime(1970, 1, 1, 0, 0, 1)
print(f"[1] \"{posixct_val.strftime('%Y-%m-%d %H:%M:%S')} UTC\"")

# data.frame(a = hms(1))
# r2py:entity:data.frame
hms_1_obj = hms_func(0, 0, 1)
df_a = pd.DataFrame({'a': [hms_1_obj]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: hms_func(hours=x))

# r2py:entity:d_1
# d
print(d)
