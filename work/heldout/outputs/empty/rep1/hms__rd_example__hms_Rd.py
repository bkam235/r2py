# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def format_hms(td):
    if td is None: return "hms()"
    if not isinstance(td, timedelta):
        return str(td)
    total_seconds = td.total_seconds()
    # hms objects in R wrap time of day, allowing hours > 23
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = total_seconds % 60
    if seconds == int(seconds):
        return f"{hours:02}:{minutes:02}:{int(seconds):02}"
    else:
        # R's hms format typically shows 6 decimal places for seconds
        return f"{hours:02}:{minutes:02}:{seconds:06.6f}"

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    total = 0.0
    provided = False
    if seconds is not None:
        total += float(seconds)
        provided = True
    if minutes is not None:
        total += float(minutes) * 60
        provided = True
    if hours is not None:
        total += float(hours) * 3600
        provided = True
    if days is not None:
        total += float(days) * 86400
        provided = True
    
    if not provided:
        return None
    return new_hms(total)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [timedelta(seconds=float(s)) for s in x]
    return timedelta(seconds=float(x))

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        # Pandas to_timedelta handles "HH:MM:SS" well
        return pd.to_timedelta(x)
    if isinstance(x, (datetime, pd.Timestamp)):
        # Extract time of day as a timedelta from midnight
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    try:
        return new_hms(x)
    except:
        return None

# suppressPackageStartupMessages(library(hms))
# No-op

# hms(56, 34, 12)
# r2py:entity:hms
t1 = hms(56, 34, 12)
print(format_hms(t1))

# hms()
# r2py:entity:hms_1
t2 = hms()
print(format_hms(t2))

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
t3 = new_hms(np.arange(1, 4).astype(float))
for val in t3:
    print(format_hms(val))

# try(new_hms(1:3))
# r2py:entity:try
try:
    t4 = new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
t5 = as_hms(1)
print(format_hms(t5))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
t6 = as_hms("12:34:56")
print(format_hms(t6))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
t7 = as_hms(datetime.now())
print(format_hms(t7))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
t8 = pd.to_datetime("1970-01-01") + hms(seconds=1)
print(f'[1] "{t8.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df1 = pd.DataFrame({'a': [format_hms(hms(seconds=1))]}, index=[1])
print(f"     a")
print(f"1 {df1.iloc[0,0]}")

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: format_hms(hms(hours=x)))

# d
# r2py:entity:d_1
print(f"     hours")
for idx, row in d.iterrows():
    print(f"{idx} {row['hours']}")