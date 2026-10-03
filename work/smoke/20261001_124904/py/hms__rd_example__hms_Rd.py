# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

# r2py:entity:hms
class HMS:
    """Custom class to mimic R's hms behavior."""
    def __init__(self, total_seconds):
        self.total_seconds = float(total_seconds) if total_seconds is not None else np.nan

    def __repr__(self):
        if np.isnan(self.total_seconds):
            return "hms()"
        
        total_sec_int = int(self.total_seconds)
        hours = total_sec_int // 3600
        minutes = (total_sec_int % 3600) // 60
        seconds = total_sec_int % 60
        
        if self.total_seconds == total_sec_int:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            # R's hms prints fractional seconds up to 6 digits
            frac = self.total_seconds % 1
            # Use format to get exactly 6 decimals, then strip trailing zeros
            # but R's print.hms is often quite specific.
            # The verification shows 12:58:49.080661
            sec_full = self.total_seconds % 60
            return f"{hours:02}:{minutes:02}:{sec_full:06.6f}".rstrip('0').rstrip('.') if sec_full % 1 == 0 else f"{hours:02}:{minutes:02}:{sec_full:06.6f}"

    def __str__(self):
        return self.__repr__()

def hms(seconds=None, minutes=None, hours=None, days=None):
    total = 0.0
    has_val = False
    if seconds is not None: 
        total += float(seconds)
        has_val = True
    if minutes is not None: 
        total += float(minutes) * 60
        has_val = True
    if hours is not None: 
        total += float(hours) * 3600
        has_val = True
    if days is not None: 
        total += float(days) * 86400
        has_val = True
    
    if not has_val:
        return HMS(np.nan)
    return HMS(total)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [HMS(val) for val in x]
    return HMS(x)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2])
        return HMS(h * 3600 + m * 60 + s)
    if isinstance(x, (datetime, pd.Timestamp)):
        return HMS(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6)
    if isinstance(x, (int, float, np.number)):
        return HMS(x)
    return HMS(x)

# hms(56, 34, 12)
# r2py:entity:hms
hms_val = hms(56, 34, 12)
print(hms_val)

# hms()
# r2py:entity:hms_1
hms_empty = hms()
print(hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_vals = new_hms(np.arange(1, 4))
for val in new_hms_vals:
    print(val)

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms_vals_try = new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

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
as_hms_now = as_hms(datetime.now())
print(as_hms_now)

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
as_posixct = datetime.fromtimestamp(HMS(1).total_seconds, tz=timezone.utc)
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(HMS(1))]})
print("   a")
print(f"1 {df_a['a'][0]}")

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': range(1, 4)})
# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: str(hms(hours=x)))

# d
# r2py:entity:d_1
print("  hours")
for i, val in enumerate(d['hours'], 1):
    print(f"{i} {val}")