# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim managed by the harness (loads R's input data) - do not write it

import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import json
from pathlib import Path

# r2py:data_shim:begin
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['d']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            import pandas as _r2py_shim_pd
            _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

# Create an hms class that behaves like R's hms
class hms:
    """Time of day class mimicking R's hms package"""
    def __init__(self, hours=0, minutes=0, seconds=0):
        # Store as total seconds since midnight
        self.seconds = hours * 3600 + minutes * 60 + seconds
        if self.seconds < 0:
            self.seconds = 0
    
    def __repr__(self):
        # Format as HH:MM:SS
        total_seconds = int(self.seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        microseconds = int((self.seconds - int(self.seconds)) * 1e6)
        if microseconds > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def __str__(self):
        return self.__repr__()

def new_hms(times):
    """Create hms objects from numeric seconds"""
    if isinstance(times, (list, np.ndarray)):
        result = []
        for t in times:
            hours = int(t) // 3600
            minutes = (int(t) % 3600) // 60
            seconds = int(t) % 60
            result.append(hms(hours, minutes, seconds))
        return result
    else:
        hours = int(times) // 3600
        minutes = (int(times) % 3600) // 60
        seconds = int(times) % 60
        return hms(hours, minutes, seconds)

def as_hms(x):
    """Convert to hms"""
    if isinstance(x, (int, float)):
        # x is in seconds
        hours = int(x) // 3600
        minutes = (int(x) % 3600) // 60
        seconds = int(x) % 60
        microseconds = (x - int(x)) * 1e6
        h = hms(hours, minutes, seconds)
        h.seconds = x  # Keep fractional seconds
        return h
    elif isinstance(x, str):
        # Parse time string
        parts = x.split(':')
        h = int(parts[0])
        m = int(parts[1])
        s = float(parts[2])
        return hms(h, m, int(s))
    elif isinstance(x, datetime):
        # Extract time of day
        h = x.hour
        m = x.minute
        s = x.second
        microseconds = x.microsecond
        hms_obj = hms(h, m, s)
        hms_obj.seconds = h * 3600 + m * 60 + s + microseconds / 1e6
        return hms_obj
    return x

# suppressPackageStartupMessages(library(hms))
# r2py:entity:suppressPackageStartupMessages
# (In Python, we define our own hms class above, no library needed)

# hms(56, 34, 12)
# r2py:entity:hms
print(hms(56, 34, 12))

# hms()
# r2py:entity:hms_1
print(hms())

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_result = new_hms(np.arange(1, 4))
for item in new_hms_result:
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
print(as_hms(1))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
print(as_hms("12:34:56"))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
now = datetime.now()
print(as_hms(now))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
# In R, as.POSIXct on an hms returns a datetime at epoch + hms value
epoch = datetime(1970, 1, 1)
posixct_result = epoch + timedelta(seconds=1)
print(posixct_result.strftime('[1] "%Y-%m-%d %H:%M:%S UTC"'))

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms(0, 0, 1)]})
print(df_a)

# r2py:entity:d
# d <- data.frame(hours = 1:3)
# d is already loaded by data shim

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: hms(hours=int(x)))

# r2py:entity:d_1
# d
print(d)
