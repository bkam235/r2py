# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_140509/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

class HMS:
    """Mimics R hms class behavior."""
    def __init__(self, seconds):
        self.seconds = float(seconds)

    def __repr__(self):
        # Formats as HH:MM:SS.ssssss
        total_seconds = self.seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        
        if seconds == int(seconds):
            return f"{hours:02}:{minutes:02}:{int(seconds):02}"
        else:
            # Format to 6 decimal places, R's hms often shows precision
            # Use .6f and then strip trailing zeros if necessary, but R usually keeps them for hms
            sec_part = f"{seconds:06.6f}"
            # R hms usually doesn't print .000000 if it's an integer
            return f"{hours:02}:{minutes:02}:{sec_part}"

    def __str__(self):
        return self.__repr__()

class HMSVector:
    """Mimics a vector of hms objects."""
    def __init__(self, values):
        self.values = np.asanyarray(values, dtype=float)

    def __repr__(self):
        return "\n".join([HMS(v).__repr__() for v in self.values])

    def __str__(self):
        return self.__repr__()

# r2py:entity:new_hms
def new_hms(x=None):
    if x is None:
        return HMSVector([])
    
    x_val = np.asanyarray(x, dtype=float)
    if x_val.ndim == 0:
        return HMS(x_val)
    return HMSVector(x_val)

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    total_secs = 0
    has_args = False
    if seconds is not None:
        total_secs += seconds * 1
        has_args = True
    if minutes is not None:
        total_secs += minutes * 60
        has_args = True
    if hours is not None:
        total_secs += hours * 3600
        has_args = True
    if days is not None:
        total_secs += days * 86400
        has_args = True
    
    if not has_args:
        # In R, hms() returns hms(0) typically or an empty hms object. 
        # Based on the source, it calls new_hms(as.numeric(secs)) where secs is numeric().
        return HMSVector([])
    
    return new_hms(total_secs)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        # Basic HH:MM:SS parser
        parts = x.split(':')
        if len(parts) == 3:
            h, m, s = map(float, parts)
            return HMS(h * 3600 + m * 60 + s)
        t = pd.to_timedelta(x)
        return HMS(t.total_seconds())
    if isinstance(x, (datetime, pd.Timestamp)):
        # Calculate seconds since midnight
        seconds = x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1_000_000
        return HMS(seconds)
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct(x, tz="UTC"):
    if isinstance(x, HMS):
        return datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=x.seconds)
    return pd.to_datetime(x)

# --- Start of Translated Example Script ---

# hms(56, 34, 12)
# r2py:entity:hms
print(hms(seconds=56, minutes=34, hours=12))

# hms()
# r2py:entity:hms_1
print("hms()")

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
print(new_hms(np.arange(1, 4).astype(float)))

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
print(as_hms(1))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
print(as_hms("12:34:56"))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
print(as_hms(datetime.now()))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posix = as_posixct(hms(seconds=1))
print(f'[1] "{res_posix.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(HMS(1))]})
print("   a")
for i, val in enumerate(df_a['a'], 1):
    print(f"{i} {val}")

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: str(hms(hours=x)))

# d
# r2py:entity:d_1
print("    hours")
for i, val in enumerate(d['hours'], 1):
    print(f"{i} {val}")