# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def format_hms(td):
    """Helper to format pandas Timedelta to R hms string HH:MM:SS"""
    if not isinstance(td, (pd.Timedelta, timedelta)):
        return str(td)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return pd.to_timedelta(x, unit='s')
    return pd.Timedelta(seconds=float(x))

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    if all(v is None for v in [seconds, minutes, hours, days]):
        return "hms()"
    
    total_secs = 0
    if seconds is not None: total_secs += seconds
    if minutes is not None: total_secs += minutes * 60
    if hours is not None: total_secs += hours * 3600
    if days is not None: total_secs += days * 86400
    return new_hms(total_secs)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        return pd.to_timedelta(x)
    if isinstance(x, (datetime, pd.Timestamp)):
        t = x.time()
        return pd.Timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
    if isinstance(x, (int, float)):
        return new_hms(x)
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct(x):
    origin = pd.Timestamp('1970-01-01', tz='UTC')
    return origin + x

# --- Script Execution ---

# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(seconds=56, minutes=34, hours=12)
print(format_hms(res_hms) if not isinstance(res_hms, str) else res_hms)

# hms()
# r2py:entity:hms_1
res_hms_1 = hms()
print(res_hms_1)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
res_new_hms = new_hms(np.arange(1, 4))
for val in res_new_hms:
    print(format_hms(val))

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
res_as_hms = as_hms(1)
print(format_hms(res_as_hms))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_1 = as_hms("12:34:56")
print(format_hms(res_as_hms_1))

# as_hms(Sys.time())
# Using a fixed-ish timestamp to mirror R's Sys.time() logic if needed, 
# but datetime.now() is the equivalent.
# r2py:entity:as_hms_2
res_as_hms_2 = as_hms(datetime.now())
# R output for Sys.time() often includes microseconds
t_obj = res_as_hms_2
print(f"{format_hms(t_obj)}.{int(t_obj.microseconds/1000):03}")

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posix = as_posixct(hms(seconds=1))
print(f'[1] "{res_posix.strftime("%Y-%m-%d %H:%M:%S")} UTC"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms(seconds=1)]})
df_a['a'] = df_a['a'].apply(format_hms)
df_a.index = df_a.index + 1
print(df_a)

# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})
# r2py:entity:d$hours
d['hours'] = pd.to_timedelta(d['hours'], unit='h')
# r2py:entity:d_1
d_final = d.copy()
d_final['hours'] = d_final['hours'].apply(format_hms)
d_final.index = d_final.index + 1
print(d_final)