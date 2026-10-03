import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def format_hms(td):
    """Helper to format pandas Timedelta to R's hms format 'HH:MM:SS'."""
    if isinstance(td, pd.TimedeltaIndex):
        return "\n".join([format_hms(x) for x in td])
    if not isinstance(td, pd.Timedelta):
        return str(td)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# r2py:entity:new_hms
def new_hms(x):
    """Equivalent to new_hms in R: creates an hms object from seconds."""
    if x is None or (isinstance(x, (list, np.ndarray, pd.Series)) and len(x) == 0):
        return pd.to_timedelta([], unit='s')
    return pd.to_timedelta(x, unit='s')

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    """Equivalent to hms in R: creates an hms object from time components."""
    if seconds is None and minutes is None and hours is None and days is None:
        return new_hms(np.array([]))
    
    total_secs = 0
    if seconds is not None: total_secs += seconds
    if minutes is not None: total_secs += minutes * 60
    if hours is not None: total_secs += hours * 3600
    if days is not None: total_secs += days * 86400
    
    return new_hms(total_secs)

# r2py:entity:as_hms
def as_hms(x):
    """Equivalent to as_hms in R: converts various inputs to hms."""
    if isinstance(x, str):
        return pd.to_timedelta(x)
    if isinstance(x, (datetime, pd.Timestamp)):
        return pd.to_timedelta(x.hour, unit='h') + \
               pd.to_timedelta(x.minute, unit='m') + \
               pd.to_timedelta(x.second, unit='s')
    if isinstance(x, (int, float, np.number)):
        return new_hms(x)
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct(x, tz=None):
    """Equivalent to as.POSIXct for hms objects."""
    if isinstance(x, pd.Timedelta):
        return pd.to_datetime('1970-01-01') + x
    return pd.to_datetime(x, tz=tz)

# --- Execution ---
# suppressPackageStartupMessages(library(hms))

# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(seconds=56, minutes=34, hours=12)
print(format_hms(res_hms))

# hms()
# r2py:entity:hms_1
res_hms_empty = hms()
print("hms()")

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
res_new_hms = new_hms(np.arange(1, 4))
print(format_hms(res_new_hms))

# try(new_hms(1:3))
# r2py:entity:try
try:
    res_try = new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
res_as_hms_1 = as_hms(1)
print(format_hms(res_as_hms_1))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_2 = as_hms("12:34:56")
print(format_hms(res_as_hms_2))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
res_as_hms_3 = as_hms(datetime.now())
print(format_hms(res_as_hms_3))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posixct = as_posixct(hms(1))
print(f'[1] "{res_posixct.strftime("%Y-%m-%d %H:%M:%S")} UTC"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms(1)]})
df_a_fmt = df_a.copy()
df_a_fmt['a'] = df_a_fmt['a'].apply(format_hms)
df_a_fmt.index = df_a_fmt.index + 1
print(df_a_fmt)

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: hms(hours=x))

# d
# r2py:entity:d_1
d_out = d.copy()
d_out['hours'] = d_out['hours'].apply(format_hms)
d_out.index = d_out.index + 1
print(d_out)