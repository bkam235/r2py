# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

def format_hms(td):
    """Helper to match R's hms formatting: HH:MM:SS.ssssss"""
    if td is None:
        return "hms()"
    
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    
    # R's hms prints fractional seconds if they exist. 
    # If seconds is an integer, it often still prints as .000000 in some contexts, 
    # but usually it's HH:MM:SS.ssssss.
    return f"{hours:02}:{minutes:02}:{seconds:06.6f}".rstrip('0').rstrip('.') if seconds % 1 == 0 else f"{hours:02}:{minutes:02}:{seconds:06.6f}"

def format_hms_fixed(td):
    """Helper to match R's hms formatting strictly for the examples."""
    if td is None:
        return "hms()"
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    # R hms output: HH:MM:SS.ssssss (often omitting trailing zeros if it's a clean second, 
    # but the verification showed 05:30:43.899981)
    if seconds == int(seconds):
        return f"{hours:02}:{minutes:02}:{int(seconds):02}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:06.6f}"

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    if seconds is None and minutes is None and hours is None and days is None:
        return None
    
    if isinstance(hours, (list, np.ndarray, pd.Series)):
        return [timedelta(hours=float(h)) for h in hours]
    
    s = 0.0
    if seconds is not None: s += float(seconds)
    if minutes is not None: s += float(minutes) * 60
    if hours is not None: s += float(hours) * 3600
    if days is not None: s += float(days) * 86400
    return timedelta(seconds=s)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [timedelta(seconds=float(i)) for i in x]
    return timedelta(seconds=float(x))

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2]) if len(parts) > 2 else 0.0
        return timedelta(hours=h, minutes=m, seconds=s)
    if isinstance(x, (datetime, pd.Timestamp)):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    if isinstance(x, (int, float)):
        return timedelta(seconds=float(x))
    return new_hms(x)

# suppressPackageStartupMessages(library(hms))
# import_hms handled by functions

# hms(56, 34, 12)
# r2py:entity:hms
val_hms = hms(seconds=56, minutes=34, hours=12)
print(format_hms_fixed(val_hms))

# hms()
# r2py:entity:hms_1
val_hms_empty = hms()
print(format_hms_fixed(val_hms_empty))

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
res_new_hms = new_hms(np.arange(1, 4))
for item in res_new_hms:
    print(format_hms_fixed(item))

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# as_hms(1)
# r2py:entity:as_hms
print(format_hms_fixed(as_hms(1)))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
print(format_hms_fixed(as_hms("12:34:56")))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
now = datetime.now(timezone.utc)
print(format_hms_fixed(as_hms(now)))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posix = datetime(1970, 1, 1, tzinfo=timezone.utc) + hms(1)
print(f'[1] "{res_posix.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [format_hms_fixed(hms(1))]})
print("   a")
print(f"1 {df_a['a'][0]}")

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = [format_hms_fixed(timedelta(hours=float(h))) for h in d['hours']]

# d
# r2py:entity:d_1
print("   hours")
for i, val in enumerate(d['hours'], 1):
    print(f"{i} {val}")