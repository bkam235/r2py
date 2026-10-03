# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:entity:hms
class HMS:
    """Mimics R's hms class which stores seconds since midnight."""
    def __init__(self, seconds):
        self.seconds = float(seconds) if seconds is not None else np.nan

    def __repr__(self):
        if np.isnan(self.seconds):
            return "hms()"
        
        total_seconds = self.seconds
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = total_seconds % 60
        
        # R's hms formatting: HH:MM:SS.sssss
        # We format seconds to 6 decimal places, then trim trailing zeros
        s_str = f"{s:06.6f}"
        if '.' in s_str:
            s_str = s_str.rstrip('0').rstrip('.')
            # ensure at least two digits for the integer part of seconds
            parts = s_str.split('.')
            parts[0] = parts[0].zfill(2)
            s_str = ".".join(parts)
        else:
            s_str = f"{int(s):02}"
            
        return f"{h:02}:{m:02}:{s_str}"

    def __str__(self):
        return self.__repr__()

def hms(seconds=None, minutes=None, hours=None, days=None):
    # Logic from R function source
    total_secs = 0
    has_val = False
    
    # R: arg_secs <- map2(args, c(1, 60, 3600, 86400), `*`)
    # R: secs <- reduce(arg_secs[!map_lgl(args, is.null)], `+`)
    
    if seconds is not None:
        total_secs += np.array(seconds) * 1
        has_val = True
    if minutes is not None:
        total_secs += np.array(minutes) * 60
        has_val = True
    if hours is not None:
        total_secs += np.array(hours) * 3600
        has_val = True
    if days is not None:
        total_secs += np.array(days) * 86400
        has_val = True
    
    if not has_val:
        return HMS(np.nan)
    
    if isinstance(total_secs, (np.ndarray, list, pd.Series)):
        return [HMS(s) for s in total_secs]
    
    return HMS(total_secs)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [HMS(float(val)) for val in x]
    return HMS(float(x))

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        # "12:34:56"
        parts = x.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2]) if len(parts) > 2 else 0.0
        return HMS(h * 3600 + m * 60 + s)
    if isinstance(x, (datetime, pd.Timestamp)):
        # Sys.time() -> extract time of day
        return HMS(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6)
    if isinstance(x, (int, float, np.number)):
        return HMS(float(x))
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct(x):
    # as.POSIXct(hms(1)) -> "1970-01-01 00:00:01 UTC"
    val = x.seconds if isinstance(x, HMS) else float(x)
    dt = datetime.utcfromtimestamp(val)
    return f'"{dt.strftime("%Y-%m-%d %H:%M:%S")} UTC"'

# suppressPackageStartupMessages(library(hms))

# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(56, 34, 12)
print(res_hms)

# hms()
# r2py:entity:hms_1
res_hms_empty = hms()
print(res_hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
res_new_hms = new_hms(np.arange(1, 4))
for item in res_new_hms:
    print(item)

# try(new_hms(1:3))
# r2py:entity:try
try:
    res_try = new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
res_as_hms_1 = as_hms(1)
print(res_as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_str = as_hms("12:34:56")
print(res_as_hms_str)

# as_hms(Sys.time())
# r2py:entity:as_hms_2
res_as_hms_now = as_hms(datetime.now())
print(res_as_hms_now)

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posixct = as_posixct(hms(1))
print(f"[1] {res_posixct}")

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(hms(1))]}, index=[1])
print(df_a.to_string())

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': [1, 2, 3]}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# Note: hms(hours=...) in R treats the value as number of hours.
# r2py:entity:d$hours
hms_vals = hms(hours=d['hours'].values)
d['hours'] = [str(x) for x in hms_vals]

# d
# r2py:entity:d_1
print(d.to_string())