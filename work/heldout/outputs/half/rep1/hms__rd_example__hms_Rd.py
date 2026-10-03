# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep1/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# hms(56, 34, 12)
# r2py:entity:hms
hms_1 = timedelta(hours=56, minutes=34, seconds=12)
print(hms_1)

# hms()
# r2py:entity:hms_1
hms_empty = timedelta()
print(hms_empty)

# new_hms(as.numeric(1:3))
# In R, new_hms creates hms objects from seconds
# r2py:entity:new_hms
new_hms_1 = [timedelta(seconds=float(s)) for s in range(1, 4)]
print(new_hms_1)

# try(new_hms(1:3))
# r2py:entity:try
try:
    # Simulating the behavior where non-numeric or incompatible types might fail
    # In Python, the list comprehension above handles ints, but we mimic the try block
    new_hms_try = [timedelta(seconds=s) for s in range(1, 4)]
except Exception as e:
    print(e)

# as_hms(1)
# r2py:entity:as_hms
as_hms_1 = timedelta(seconds=1)
print(as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
as_hms_2 = pd.to_timedelta("12:34:56")
print(as_hms_2)

# as_hms(Sys.time())
# Extracting time component from current time
# r2py:entity:as_hms_2
as_hms_3 = datetime.now().time()
print(as_hms_3)

# as.POSIXct(hms(1))
# Converting duration to a timestamp (usually relative to epoch)
# r2py:entity:as.POSIXct
as_posixct = pd.to_datetime(timedelta(seconds=1))
print(as_posixct)

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [timedelta(seconds=1)]})
print(df_a)

# d <- data.frame(hours = 1:3)
# r2py:entity:d

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: timedelta(hours=x))

# d
# r2py:entity:d_1
print(d)