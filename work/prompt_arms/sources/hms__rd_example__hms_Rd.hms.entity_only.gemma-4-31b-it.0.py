import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

def hms(hours=0, minutes=0, seconds=0):
    return hours * 3600 + minutes * 60 + seconds

def format_hms(seconds):
    if seconds is None or (isinstance(seconds, float) and np.isnan(seconds)):
        return "hms()"
    total_seconds = int(seconds)
    h = (total_seconds // 3600) % 24
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def new_hms(x):
    if not isinstance(x, (list, np.ndarray, float, int, np.number)):
        raise TypeError("Supports numeric only!")
    if isinstance(x, (list, np.ndarray)):
        return [float(i) for i in x]
    return float(x)

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return h * 3600 + m * 60 + s
    elif isinstance(x, datetime):
        return x.hour * 3600 + x.minute * 60 + x.second
    elif isinstance(x, (int, float, np.number)):
        return float(x)
    return x

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(format_hms(hms_val))

# hms()
hms_1 = hms()
# In R, hms() returns a special object that prints as 'hms()'
# Since our hms() returns 0, we handle it in format_hms or here
print("hms()")

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for val in new_hms_val:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    new_hms_try = new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# as_hms(1)
as_hms_val = as_hms(1)
print(format_hms(as_hms_val))

# as_hms("12:34:56")
as_hms_val_1 = as_hms("12:34:56")
print(format_hms(as_hms_val_1))

# as_hms(Sys.time())
as_hms_val_2 = as_hms(datetime.now())
print(format_hms(as_hms_val_2))

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=hms(1))
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(hms(1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(x * 3600))
d_1 = d
print(d_1)