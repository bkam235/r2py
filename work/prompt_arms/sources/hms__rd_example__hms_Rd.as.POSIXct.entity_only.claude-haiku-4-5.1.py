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
import json as _r2py_shim_json
from pathlib import Path as _r2py_shim_Path
import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# Load data from shim
_r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
for _r2py_shim_n in ['d']:
    if _r2py_shim_n in _r2py_shim_data:
        _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
        if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
            _r2py_shim_v = pd.DataFrame(_r2py_shim_v)
        globals()[_r2py_shim_n] = _r2py_shim_v

# Create hms class to represent time-of-day in HH:MM:SS format
class hms:
    def __init__(self, hours=0, minutes=0, seconds=0):
        # Store as total seconds from midnight
        self.seconds = int(hours * 3600 + minutes * 60 + seconds)
        # Normalize to [0, 86400) range (24 hours)
        self.seconds = self.seconds % 86400
    
    def __repr__(self):
        h = self.seconds // 3600
        m = (self.seconds % 3600) // 60
        s = self.seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def __str__(self):
        return self.__repr__()

def new_hms(values):
    """Create hms objects from numeric seconds"""
    if isinstance(values, (list, np.ndarray)):
        return [hms(seconds=int(v)) for v in values]
    else:
        return hms(seconds=int(values))

def as_hms(value):
    """Convert various formats to hms"""
    if isinstance(value, (int, float)):
        # Numeric value interpreted as seconds
        return hms(seconds=int(value))
    elif isinstance(value, str):
        # String in HH:MM:SS format
        parts = value.split(':')
        if len(parts) == 3:
            h, m, s = map(int, parts)
            return hms(hours=h, minutes=m, seconds=s)
        else:
            raise ValueError(f"Invalid time string: {value}")
    elif isinstance(value, datetime):
        # Extract time of day from datetime
        return hms(hours=value.hour, minutes=value.minute, seconds=value.second)
    else:
        raise TypeError(f"Cannot convert {type(value)} to hms")

# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(hms))
# No-op in Python since hms is now defined above

# r2py:entity:hms
hms_result = hms(56, 34, 12)
print(hms_result)

# r2py:entity:hms_1
hms_empty = hms()
print(hms_empty)

# r2py:entity:new_hms
new_hms_result = new_hms(np.arange(1, 4))
for item in new_hms_result:
    print(item)

# r2py:entity:try
try:
    new_hms_error = new_hms(np.arange(1, 4))
except Exception as e:
    print(f"Error: {e}")

# r2py:entity:as_hms
as_hms_1_result = as_hms(1)
print(as_hms_1_result)

# r2py:entity:as_hms_1
as_hms_2_result = as_hms("12:34:56")
print(as_hms_2_result)

# r2py:entity:as_hms_2
as_hms_3_result = as_hms(datetime.now())
print(as_hms_3_result)

# r2py:entity:as.POSIXct
# as.POSIXct(hms(1))
as_posixct_result = datetime.min + timedelta(seconds=1)
print(as_posixct_result)

# r2py:entity:data.frame
# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [hms(seconds=1)]})
print(df_a)

# r2py:entity:d
# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
if isinstance(d, pd.DataFrame):
    d['hours'] = d['hours'].apply(lambda x: hms(hours=int(x)))
else:
    # If d is loaded as a dict, convert to DataFrame
    d = pd.DataFrame(d)
    d['hours'] = d['hours'].apply(lambda x: hms(hours=int(x)))

# r2py:entity:d_1
print(d)