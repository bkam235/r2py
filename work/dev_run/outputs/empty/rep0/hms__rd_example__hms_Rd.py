# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/empty/rep0/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

def format_hms(td):
    if td is None:
        return "hms()"
    if isinstance(td, str) and td == "hms()":
        return "hms()"
    
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    if seconds is None and minutes is None and hours is None and days is None:
        return "hms()"
    total = 0
    if seconds is not None: total += seconds
    if minutes is not None: total += minutes * 60
    if hours is not None: total += hours * 3600
    if days is not None: total += days * 86400
    return timedelta(seconds=total)

# hms(56, 34, 12)
res_hms = hms(seconds=56, minutes=34, hours=12)
print(format_hms(res_hms))

# hms()
# r2py:entity:hms_1
res_hms_empty = hms()
print(format_hms(res_hms_empty))

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray)):
        return [timedelta(seconds=float(s)) for s in x]
    return timedelta(seconds=float(x))

# new_hms(as.numeric(1:3))
res_new_hms = new_hms(np.arange(1, 4))
for val in res_new_hms:
    print(format_hms(val))

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception:
    pass

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, (int, float)):
        return timedelta(seconds=x)
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
    if isinstance(x, datetime):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    return timedelta(seconds=float(x))

# as_hms(1)
res_as_hms_1 = as_hms(1)
print(format_hms(res_as_hms_1))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_str = as_hms("12:34:56")
print(format_hms(res_as_hms_str))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
res_as_hms_now = as_hms(datetime.now())
print(format_hms(res_as_hms_now))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
epoch = datetime(1970, 1, 1)
res_posixct = epoch + hms(1)
print(f'[1] "{res_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [format_hms(hms(1))]}, index=[1])
print(df_a.to_string())

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: format_hms(hms(hours=x)))

# d
# r2py:entity:d_1
print(d.to_string())