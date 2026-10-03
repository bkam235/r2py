# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_191227/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

def hms_format(seconds):
    if seconds is None or (isinstance(seconds, float) and np.isnan(seconds)):
        return "hms()"
    # R's hms prints as HH:MM:SS.S
    total_seconds = float(seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    secs = total_seconds % 60
    # R uses a specific format for fractions of a second
    if secs == int(secs):
        return f"{hours:02}:{minutes:02}:{int(secs):02}"
    else:
        return f"{hours:02}:{minutes:02}:{secs:06.6f}".rstrip('0').rstrip('.')

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    total = 0.0
    if seconds is not None: total += float(seconds)
    if minutes is not None: total += float(minutes) * 60
    if hours is not None: total += float(hours) * 3600
    if days is not None: total += float(days) * 86400
    
    if total == 0 and seconds is None and minutes is None and hours is None and days is None:
        return None # Representing the empty hms()
    return total

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray)):
        return np.array(x, dtype=float)
    return float(x)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return h * 3600 + m * 60 + s
    if isinstance(x, datetime):
        return x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6
    return float(x)

# suppressPackageStartupMessages(library(hms))
# (No-op in Python)

# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(seconds=56, minutes=34, hours=12)
print(hms_format(res_hms))

# hms()
# r2py:entity:hms_1
res_hms_1 = hms()
print(hms_format(res_hms_1))

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
val_new_hms = new_hms(np.arange(1, 4).astype(float))
for v in val_new_hms:
    print(hms_format(v))

# try(new_hms(1:3))
# r2py:entity:try
try:
    res_try = new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# as_hms(1)
# r2py:entity:as_hms
res_as_hms = as_hms(1)
print(hms_format(res_as_hms))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_1 = as_hms("12:34:56")
print(hms_format(res_as_hms_1))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
res_as_hms_2 = as_hms(datetime.now())
print(hms_format(res_as_hms_2))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posixct = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=hms(1))
print(f'[1] "{res_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms_format(hms(1))]})
df_a.index = range(1, len(df_a) + 1)
print(df_a.to_string())

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: hms_format(hms(hours=x)))

# r2py:entity:d_1
# d
d.index = range(1, len(d) + 1)
print(d.to_string())