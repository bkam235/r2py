# Translated from <R script> by r2py v0.3.0

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

# Custom hms class to mimic R's hms package
class hms_time:
    """Represents time-of-day in seconds"""
    def __init__(self, hours=0, minutes=0, seconds=0):
        # Store as total seconds
        self.seconds_val = hours * 3600 + minutes * 60 + seconds
    
    def __repr__(self):
        return format_hms(self)
    
    def __str__(self):
        return format_hms(self)

def format_hms(h):
    """Format hms object as HH:MM:SS.ffffff"""
    if isinstance(h, hms_time):
        total_secs = h.seconds_val
    else:
        total_secs = h
    
    # Extract hours, minutes, seconds
    hours_val = int(total_secs // 3600)
    minutes_val = int((total_secs % 3600) // 60)
    seconds_val = total_secs % 60
    
    # Format with microseconds if needed
    if seconds_val == int(seconds_val):
        return f"{hours_val:02d}:{minutes_val:02d}:{int(seconds_val):02d}"
    else:
        return f"{hours_val:02d}:{minutes_val:02d}:{seconds_val:06.3f}".rstrip('0').rstrip('.')

def hms(hours=0, minutes=0, seconds=0):
    """Create an hms object"""
    return hms_time(hours=hours, minutes=minutes, seconds=seconds)

def new_hms(seconds_list):
    """Create hms objects from a numeric list of seconds"""
    return [hms(seconds=s) for s in seconds_list]

def as_hms(x):
    """Convert to hms from various formats"""
    if isinstance(x, (int, float, np.integer, np.floating)):
        # Interpret as seconds
        return hms(seconds=float(x))
    elif isinstance(x, str):
        # Parse "HH:MM:SS" format
        parts = x.split(':')
        h = int(parts[0]) if len(parts) > 0 else 0
        m = int(parts[1]) if len(parts) > 1 else 0
        s = float(parts[2]) if len(parts) > 2 else 0
        return hms(hours=h, minutes=m, seconds=s)
    elif isinstance(x, datetime):
        # Extract time component
        return hms(hours=x.hour, minutes=x.minute, seconds=x.second + x.microsecond/1e6)
    else:
        return hms(seconds=float(x))

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(hms_val)

# hms()
hms_empty = hms()
print(hms_empty)

# new_hms(as.numeric(1:3))
new_hms_result = new_hms(np.arange(1, 4))
for item in new_hms_result:
    print(item)

# try(new_hms(1:3))
try:
    new_hms_try = new_hms([1, 2, 3])
except Exception as e:
    print(str(e))

# as_hms(1)
as_hms_1 = as_hms(1)
print(as_hms_1)

# as_hms("12:34:56")
as_hms_str = as_hms("12:34:56")
print(as_hms_str)

# as_hms(Sys.time())
now = datetime.now()
as_hms_time = as_hms(now)
print(as_hms_time)

# as.POSIXct(hms(1))
hms_1_val = hms(seconds=1)
as_posixct_result = datetime(1970, 1, 1) + timedelta(seconds=1)
print(f"[1] \"{as_posixct_result.strftime('%Y-%m-%d %H:%M:%S')} UTC\"")

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [hms(seconds=1)]})
print(df_a)

# d <- data.frame(hours = 1:3)
d = pd.DataFrame({'hours': [1, 2, 3]})

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: hms(hours=x))

# d
print(d)