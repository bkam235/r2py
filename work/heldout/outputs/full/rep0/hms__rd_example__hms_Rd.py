# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep0/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# r2py:entity:hms
class HMS:
    """Mimics R's hms class: stores seconds since midnight."""
    def __init__(self, seconds=0):
        self.seconds = float(seconds) if seconds is not None else np.nan

    def __repr__(self):
        if np.isnan(self.seconds):
            return "hms()"
        
        total_seconds = self.seconds
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = total_seconds % 60
        
        if s % 1 == 0:
            return f"{h:02d}:{m:02d}:{int(s):02d}"
        else:
            return f"{h:02d}:{m:02d}:{s:06.6f}"

    def __str__(self):
        return self.__repr__()

def hms(seconds=None, minutes=None, hours=None, days=None):
    # Vectorized input handling
    is_vector = False
    if hours is not None and hasattr(hours, '__iter__') and not isinstance(hours, (str, bytes)):
        is_vector = True
        h_vals = hours
    elif seconds is not None and hasattr(seconds, '__iter__') and not isinstance(seconds, (str, bytes)):
        is_vector = True
        s_vals = seconds
    elif minutes is not None and hasattr(minutes, '__iter__') and not isinstance(minutes, (str, bytes)):
        is_vector = True
        m_vals = minutes
    elif days is not None and hasattr(days, '__iter__') and not isinstance(days, (str, bytes)):
        is_vector = True
        d_vals = days
    else:
        h_vals = m_vals = s_vals = d_vals = None

    if is_vector:
        # Ensure all are arrays for vectorized addition
        h_arr = np.array(h_vals if 'h_vals' in locals() and h_vals is not None else 0)
        m_arr = np.array(m_vals if 'm_vals' in locals() and m_vals is not None else 0)
        s_arr = np.array(s_vals if 's_vals' in locals() and s_vals is not None else 0)
        d_arr = np.array(d_vals if 'd_vals' in locals() and d_vals is not None else 0)
        
        total_secs = h_arr * 3600 + m_arr * 60 + s_arr + d_arr * 86400
        return pd.Series([HMS(s) for s in total_secs])

    # Scalar handling
    total_secs = 0
    has_arg = False
    if hours is not None: 
        total_secs += hours * 3600
        has_arg = True
    if minutes is not None: 
        total_secs += minutes * 60
        has_arg = True
    if seconds is not None: 
        total_secs += seconds
        has_arg = True
    if days is not None: 
        total_secs += days * 86400
        has_arg = True
        
    if not has_arg:
        return HMS(np.nan)
        
    return HMS(total_secs)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [HMS(val) for val in x]
    return HMS(x)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        h = float(parts[0])
        m = float(parts[1])
        s = float(parts[2]) if len(parts) > 2 else 0.0
        return HMS(h * 3600 + m * 60 + s)
    elif isinstance(x, (datetime, pd.Timestamp)):
        return HMS(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6)
    elif isinstance(x, (int, float, np.number)):
        return HMS(float(x))
    else:
        return new_hms(x)

# suppressPackageStartupMessages(library(hms))
# (Implicitly handled)

# hms(56, 34, 12)
# r2py:entity:hms
hms_val = hms(56, 34, 12)
print(hms_val)

# hms()
# r2py:entity:hms_1
hms_empty = hms()
print(hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_vals = new_hms(np.arange(1, 4).astype(float))
for val in new_hms_vals:
    print(val)

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# as_hms(1)
# r2py:entity:as_hms
as_hms_1 = as_hms(1)
print(as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
as_hms_str = as_hms("12:34:56")
print(as_hms_str)

# as_hms(Sys.time())
# r2py:entity:as_hms_2
as_hms_now = as_hms(datetime.now())
print(as_hms_now)

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=1)
print(f'[{1}] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(hms(1))]}, index=[1])
# To match R output "1 00:00:01", we print without the index name/extra spacing if possible
# but a simple print of the dataframe is usually close enough.
print(df_a.to_string(index=True))

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': range(1, 4)}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
res_hms = hms(hours=d['hours'].values)
d['hours'] = [str(val) for val in res_hms]

# d
# r2py:entity:d_1
print(d.to_string())