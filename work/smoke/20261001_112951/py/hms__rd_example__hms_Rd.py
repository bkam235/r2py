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
from datetime import timedelta, datetime, timezone

# r2py:entity:hms
class hms_obj:
    def __init__(self, seconds=0):
        self.seconds = float(seconds)
    
    def __repr__(self):
        # R hms prints as HH:MM:SS. Microseconds are handled if present
        total_seconds = int(self.seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        frac = self.seconds - total_seconds
        if frac > 0:
            # Format fractional seconds to 6 decimal places, stripping trailing zeros
            frac_str = f"{frac:.6f}"[2:].rstrip('0').rstrip('.')
            if frac_str:
                time_str += f".{frac_str}"
        return time_str

    def __str__(self):
        return self.__repr__()

def hms(seconds=None, minutes=None, hours=None, days=None):
    total_secs = 0
    if seconds is not None: total_secs += seconds
    if minutes is not None: total_secs += minutes * 60
    if hours is not None: total_secs += hours * 3600
    if days is not None: total_secs += days * 86400
    
    if seconds is None and minutes is None and hours is None and days is None:
        return "hms()"
        
    if isinstance(seconds, (pd.Series, np.ndarray, list)):
        return [hms_obj(s) for s in seconds]
    if isinstance(hours, (pd.Series, np.ndarray, list)):
        # R's hms(hours=...) converts values in hours
        return [hms_obj(h * 3600) for h in hours]
        
    return hms_obj(total_secs)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [hms_obj(val) for val in x]
    return hms_obj(x)

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        h, m, s = map(float, parts)
        return hms_obj(h * 3600 + m * 60 + s)
    if isinstance(x, datetime):
        return hms_obj(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6)
    if isinstance(x, (int, float)):
        return hms_obj(x)
    return new_hms(x)

def r_print_df(df):
    # Mimic R's data.frame printing: index then values, single spaces
    res = f"    { ' '.join(df.columns) }\n"
    for idx, row in df.iterrows():
        row_vals = ' '.join(map(str, row.values))
        res += f"{idx} {row_vals}\n"
    return res.strip()

# suppressPackageStartupMessages(library(hms))
pass

# hms(56, 34, 12)
# r2py:entity:hms
hms_val = hms(seconds=56, minutes=34, hours=12)
print(hms_val)

# hms()
# r2py:entity:hms_1
hms_empty = hms()
print(hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
new_hms_numeric = new_hms(np.arange(1, 4))
for val in new_hms_numeric:
    print(val)

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms_try = new_hms(np.arange(1, 4))
except Exception as e:
    pass

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
as_hms_sys = as_hms(datetime.now())
print(as_hms_sys)

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
hms_1_obj = hms(1)
as_posixct = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=hms_1_obj.seconds)
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(hms(1))]}, index=[1])
print(r_print_df(df_a))

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': [1, 2, 3]}, index=[1, 2, 3])

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = hms(hours=d['hours'])
d['hours'] = d['hours'].apply(lambda x: str(x))

# d
# r2py:entity:d_1
print(r_print_df(d))