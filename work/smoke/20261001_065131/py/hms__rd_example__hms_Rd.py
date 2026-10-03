# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

def format_single_hms(seconds):
    if seconds is None or pd.isna(seconds):
        return "NA"
    
    # Handle float seconds for sub-second precision
    total_seconds = float(seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    secs = total_seconds % 60
    
    # Format seconds: if it's an integer, no decimals. If float, show decimals.
    if secs == int(secs):
        secs_str = f"{int(secs):02}"
    else:
        # R's hms often shows 6 decimal places
        secs_str = f"{secs:06.6f}".rstrip('0').rstrip('.')
        if '.' in secs_str:
            # Ensure at least 2 digits for the seconds part before decimal
            parts = secs_str.split('.')
            secs_str = f"{int(parts[0]):02}.{parts[1]}"
        else:
            secs_str = f"{int(secs_str):02}"

    return f"{hours:02}:{minutes:02}:{secs_str}"

def format_hms(seconds):
    if seconds is None:
        return "hms()"
    if isinstance(seconds, (list, np.ndarray, pd.Series)):
        return "\n".join([format_single_hms(s) for s in seconds])
    return format_single_hms(seconds)

def r_print_df(df):
    # Custom print to match R's data.frame output alignment
    print(df.to_string(index=True, justify='left').replace('  ', ' '))

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    total = 0
    # Support vectorization
    s_val = seconds if seconds is not None else 0
    m_val = minutes if minutes is not None else 0
    h_val = hours if hours is not None else 0
    d_val = days if days is not None else 0
    
    total = s_val + m_val * 60 + h_val * 3600 + d_val * 86400
    
    if seconds is None and minutes is None and hours is None and days is None:
        return None
    
    return total

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return np.array([format_single_hms(val) for val in x])
    return format_single_hms(x)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return format_single_hms(h * 3600 + m * 60 + s)
    if isinstance(x, datetime):
        # Calculate seconds from midnight
        total = x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6
        return format_single_hms(total)
    if isinstance(x, (int, float)):
        return format_single_hms(x)
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return np.array([format_single_hms(val) for val in x])
    return format_hms(x)

# suppressPackageStartupMessages(library(hms))
# (Handled by imports)

# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(56, 34, 12)
print(format_single_hms(res_hms))

# hms()
# r2py:entity:hms_1
res_hms_empty = hms()
print(format_hms(res_hms_empty))

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_vals = new_hms(np.arange(1, 4))
for val in new_hms_vals:
    print(val)

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms_try = new_hms(np.arange(1, 4))
except Exception as e:
    pass

# as_hms(1)
# r2py:entity:as_hms
print(as_hms(1))

# as_hms("12:34:56")
# r2py:entity:as_hms_1
print(as_hms("12:34:56"))

# as_hms(Sys.time())
# r2py:entity:as_hms_2
print(as_hms(datetime.now()))

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
posix_val = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=1)
print(f'[1] "{posix_val.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [format_single_hms(1)]}, index=[1])
r_print_df(df_a)

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = np.array([format_single_hms(h * 3600) for h in d['hours']])

# d
# r2py:entity:d_1
r_print_df(d)