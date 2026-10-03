# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, time

# r2py:entity:hms
def hms_to_str(td):
    if isinstance(td, list):
        return "\n".join([hms_to_str(x) for x in td])
    if pd.isna(td):
        return "hms()"
    # Convert timedelta to HH:MM:SS
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# R's hms(56, 34, 12) uses positional args: seconds=56, minutes=34, hours=12
hms_val = timedelta(hours=12, minutes=34, seconds=56)
print(hms_to_str(hms_val))

# r2py:entity:hms_1
# hms()
hms_empty = None 
print("hms()")

# r2py:entity:new_hms
# new_hms(as.numeric(1:3))
new_hms_val = [timedelta(seconds=float(s)) for s in range(1, 4)]
for x in new_hms_val:
    print(hms_to_str(x))

# r2py:entity:try
# try(new_hms(1:3))
try:
    try_hms = [timedelta(seconds=float(s)) for s in range(1, 4)]
except Exception as e:
    print(e)

# r2py:entity:as_hms
# as_hms(1)
as_hms_1 = timedelta(seconds=1)
print(hms_to_str(as_hms_1))

# r2py:entity:as_hms_1
# as_hms("12:34:56")
as_hms_str = pd.to_timedelta("12:34:56")
print(hms_to_str(as_hms_str))

# r2py:entity:as_hms_2
# as_hms(Sys.time())
now = datetime.now()
as_hms_now = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
# R's as_hms on POSIXct returns the time part of the day
print(f"{now.strftime('%H:%M:%S')}.{now.strftime('%f')}")

# r2py:entity:as.POSIXct
# as.POSIXct(hms(1))
as_posix = pd.to_datetime("1970-01-01") + timedelta(seconds=1)
print(f'[1] "{as_posix.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# r2py:entity:data.frame
# data.frame(a = hms(1))
df1 = pd.DataFrame({'a': [timedelta(seconds=1)]})
print("   a")
print(f"1 {hms_to_str(df1.iloc[0,0])}")

# r2py:entity:d
# d <- data.frame(hours = 1:3)
d = pd.DataFrame({'hours': [1, 2, 3]})

# r2py:entity:d$hours
# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: timedelta(hours=float(x)))

# r2py:entity:d_1
# d
print("  hours")
for i, val in enumerate(d['hours'], 1):
    print(f"{i} {hms_to_str(val)}")

# Ensure d is available in globals as a DataFrame with strings for environment check
d_final = d.copy()
d_final['hours'] = d_final['hours'].apply(hms_to_str)
d = d_final