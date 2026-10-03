# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

# r2py:entity:hms
class HMS:
    def __init__(self, seconds=0):
        self.seconds = float(seconds)
    
    def __repr__(self):
        # Mimics R hms printing: HH:MM:SS
        total_seconds = int(self.seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def __str__(self):
        return self.__repr__()

def hms(seconds=None, minutes=None, hours=None, days=None):
    total_secs = 0
    if seconds is not None: total_secs += float(seconds)
    if minutes is not None: total_secs += float(minutes) * 60
    if hours is not None: total_secs += float(hours) * 3600
    if days is not None: total_secs += float(days) * 86400
    
    if seconds is None and minutes is None and hours is None and days is None:
        return "hms()"
        
    return HMS(total_secs)

# r2py:entity:new_hms
def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [HMS(float(val)) for val in x]
    return HMS(float(x))

# r2py:entity:as_hms
def as_hms(x):
    if isinstance(x, str):
        # Handle "HH:MM:SS"
        parts = x.split(':')
        if len(parts) == 3:
            h, m, s = map(float, parts)
            return HMS(h * 3600 + m * 60 + s)
        return HMS(0)
    if isinstance(x, datetime):
        return HMS(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond/1e6)
    try:
        return HMS(float(x))
    except:
        return HMS(0)

# r2py:entity:hms
val_hms1 = hms(56, 34, 12)
print(val_hms1)

# r2py:entity:hms_1
val_hms2 = hms()
print(val_hms2)

# r2py:entity:new_hms
new_hms_val = new_hms(np.arange(1, 4))
for item in new_hms_val:
    print(item)

# r2py:entity:try
try:
    _ = new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# r2py:entity:as_hms
as_hms1 = as_hms(1)
print(as_hms1)

# r2py:entity:as_hms_1
as_hms2 = as_hms("12:34:56")
print(as_hms2)

# r2py:entity:as_hms_2
as_hms3 = as_hms(datetime.now())
print(as_hms3)

# r2py:entity:as.POSIXct
posix_val = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=hms(1).seconds)
print(f'[1] "{posix_val.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [hms(1)]})
df_a.index = [1]
# Match R's data.frame printing (no extra space before values)
print(df_a.to_string(index=True))

# r2py:entity:d
d = pd.DataFrame({'hours': [1, 2, 3]})
d.index = [1, 2, 3]

# r2py:entity:d$hours
d['hours'] = d['hours'].apply(lambda x: hms(hours=x))

print(d.to_string(index=True))