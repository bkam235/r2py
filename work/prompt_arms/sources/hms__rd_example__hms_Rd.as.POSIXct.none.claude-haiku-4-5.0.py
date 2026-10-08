# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from hms import hms as hms_class

# suppressPackageStartupMessages(library(hms))
# In Python, imports don't produce startup messages by default
# r2py:entity:suppressPackageStartupMessages
# r2py:entity:import_hms

# hms(56, 34, 12)
# r2py:entity:hms
hms_val = hms_class(56, 34, 12)
print(hms_val)

# hms()
# r2py:entity:hms_1
hms_empty = hms_class()
print(hms_empty)

# new_hms(as.numeric(1:3))
# hms stores time as seconds from midnight/start
# r2py:entity:new_hms
new_hms_numeric = hms_class(as.numeric(list(range(1, 4))))
print(new_hms_numeric)

# try(new_hms(1:3))
# r2py:entity:try
try:
    # Attempting to pass a sequence/vector to new_hms
    new_hms_try = hms_class([1, 2, 3])
    print(new_hms_try)
except Exception as e:
    print(f"Error: {e}")

# as_hms(1)
# r2py:entity:as_hms
as_hms_1 = hms_class(seconds=1)
print(as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
as_hms_str = hms_class("12:34:56")
print(as_hms_str)

# as_hms(Sys.time())
# r2py:entity:as_hms_2
now = datetime.now()
as_hms_sys = hms_class(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
print(as_hms_sys)

# as.POSIXct(hms(1))
# Convert hms to a datetime (equivalent to POSIXct)
# r2py:entity:as.POSIXct
hms_one = hms_class(seconds=1)
as_posixct = pd.Timestamp(hms_one).to_pydatetime()
print(as_posixct)

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms_class(seconds=1)]})
print(df_a)

# r2py:entity:d
# d <- data.frame(hours = 1:3)
d = pd.DataFrame({'hours': list(range(1, 4))})

# r2py:entity:d$hours
# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: hms_class(hours=x))

# r2py:entity:d_1
# d
print(d)
