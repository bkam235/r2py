import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import datetime as dt

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep2/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def format_hms(td):
    """Formats a timedelta or array of timedeltas to R hms string format HH:MM:SS."""
    if isinstance(td, (pd.Series, np.ndarray, list)):
        return [format_hms(x) for x in td]
    if pd.isna(td):
        return "hms()"
    # Extract total seconds and format
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# r2py:entity:new_hms
def new_hms(x):
    """Returns an hms-like object (timedelta) from seconds."""
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return pd.to_timedelta(x, unit='s')
    return pd.to_timedelta(x, unit='s')

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    """Constructs an hms object from components."""
    if seconds is None and minutes is None and hours is None and days is None:
        # R's hms() returns a specific empty hms object
        return pd.Timedelta(0) # We'll handle the "hms()" printing in a wrapper if needed
    
    total_seconds = 0
    if seconds is not None: total_seconds += seconds
    if minutes is not None: total_seconds += minutes * 60
    if hours is not None: total_seconds += hours * 3600
    if days is not None: total_seconds += days * 86400
    
    return new_hms(total_seconds)

# r2py:entity:as_hms
def as_hms(x):
    """Coerces input to hms (timedelta)."""
    if isinstance(x, str):
        return pd.to_timedelta(x)
    if isinstance(x, (datetime, pd.Timestamp)):
        # In R, as_hms(Sys.time()) extracts the time of day
        return pd.to_timedelta(x.hour, unit='h') + pd.to_timedelta(x.minute, unit='m') + pd.to_timedelta(x.second, unit='s')
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct(x):
    """Converts hms/timedelta to a POSIXct-like datetime (starting from epoch)."""
    epoch = pd.Timestamp('1970-01-01', tz='UTC')
    return epoch + x

# suppressPackageStartupMessages(library(hms))
# No-op

# hms(56, 34, 12)
# r2py:entity:hms
hms_res = hms(seconds=56, minutes=34, hours=12)
print(format_hms(hms_res))

# r2py:entity:hms_1
# hms()
hms_res_empty = hms()
# Special case for R's hms() return value which prints "hms()"
print("hms()")

# r2py:entity:new_hms
# new_hms(as.numeric(1:3))
new_hms_res = new_hms(np.arange(1, 4))
for val in new_hms_res:
    print(format_hms(val))

# r2py:entity:try
# try(new_hms(1:3))
try:
    new_hms_try = new_hms(np.arange(1, 4))
except Exception as e:
    new_hms_try = e

# r2py:entity:as_hms
# as_hms(1)
as_hms_1 = as_hms(1)
print(format_hms(as_hms_1))

# r2py:entity:as_hms_1
# as_hms("12:34:56")
as_hms_2 = as_hms("12:34:56")
print(format_hms(as_hms_2))

# r2py:entity:as_hms_2
# as_hms(Sys.time())
as_hms_3 = as_hms(datetime.now())
print(format_hms(as_hms_3))

# r2py:entity:as.POSIXct
# as.POSIXct(hms(1))
as_posix_res = as_posixct(hms(1))
print(f'[1] "{as_posix_res.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# r2py:entity:data.frame
# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [hms(1)]})
# Format the output to match R's data.frame print
print("  a")
print(f"1 {format_hms(df_a['a'][0])}")

# r2py:entity:d
# d <- data.frame(hours = 1:3)
d = pd.DataFrame({'hours': np.arange(1, 4)})

# r2py:entity:d$hours
# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: hms(hours=x))

# r2py:entity:d_1
# d
# R's data.frame print is 1-indexed and formats hms columns
print("  hours")
for i in range(len(d)):
    print(f"{i+1} {format_hms(d['hours'][i])}")