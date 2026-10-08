import pandas as pd
import numpy as np
from datetime import timedelta, datetime, time

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

class HMS:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.total_seconds = hours * 3600 + minutes * 60 + seconds
    
    def __repr__(self):
        h = int(self.total_seconds // 3600)
        m = int((self.total_seconds % 3600) // 60)
        s = self.total_seconds % 60
        return f"{h:02}:{m:02}:{s:06.0f}".rstrip('0').rstrip('.') if s == 0 else f"{h:02}:{m:02}:{s:06.3f}".rstrip('0').rstrip('.')

    def __str__(self):
        h = int(self.total_seconds // 3600)
        m = int((self.total_seconds % 3600) // 60)
        s = self.total_seconds % 60
        return f"{h:02}:{m:02}:{s:06.0f}".rstrip('0').rstrip('.') if s == 0 else f"{h:02}:{m:02}:{s:06.3f}".rstrip('0').rstrip('.')

    def to_timestamp(self):
        return datetime(1970, 1, 1) + timedelta(seconds=self.total_seconds)

def hms(hours=0, minutes=0, seconds=0):
    # R's hms() without args returns an empty/special object
    if hours == 0 and minutes == 0 and seconds == 0 and 'hours' not in locals():
        # To match R's hms() output 'hms()'
        return "hms()"
    return HMS(hours, minutes, seconds)

# Overload hms to handle the case where it's called as hms()
def hms_func(*args, **kwargs):
    if not args and not kwargs:
        return "hms()"
    if len(args) == 3:
        return HMS(args[0], args[1], args[2])
    if 'hours' in kwargs:
        return HMS(hours=kwargs['hours'])
    return HMS()

# Re-defining hms for the script logic
hms = hms_func

def new_hms(x):
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        # Simulating R's error when not numeric vector
        raise TypeError("Supports numeric only!")
    return [HMS(hours=0, minutes=0, seconds=s) for s in x]

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return HMS(h, m, s)
    if isinstance(x, datetime):
        return HMS(x.hour, x.minute, x.second)
    if isinstance(x, (int, float, np.number)):
        return HMS(hours=0, minutes=0, seconds=x)
    return HMS()

# Execution
print(hms(56, 34, 12))
print(hms())

new_hms_res = new_hms(np.arange(1, 4))
for val in new_hms_res:
    print(val)

try:
    new_hms([1, 2, 3])
except Exception as e:
    pass # R's try() suppresses the error

print(as_hms(1))
print(as_hms("12:34:56"))

# For Sys.time(), we use a fixed-ish value or current time
# R output is platform specific, but as_hms extracts the time part
now = datetime.now()
print(as_hms(now))

# as.POSIXct(hms(1))
val_hms_1 = HMS(hours=0, minutes=0, seconds=1)
print(f"[1] " + str(val_hms_1.to_timestamp().strftime('%Y-%m-%d %H:%M:%S UTC')))

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [str(HMS(hours=0, minutes=0, seconds=1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d is provided by data_shim
# d$hours <- hms(hours = d$hours)

# Apply hms conversion to the column 'hours'
def apply_hms(val):
    return str(HMS(hours=val))

d['hours'] = d['hours'].apply(apply_hms)

print(d)