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

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def format_hms(val):
    if val is None: return "hms()"
    try:
        total_seconds = int(val) % 86400
    except (TypeError, ValueError):
        return "hms()"
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def hms(hours=0, minutes=0, seconds=0):
    return (hours * 3600 + minutes * 60 + seconds) % 86400

def new_hms(x):
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        raise TypeError("Supports numeric only!")
    return [float(i) for i in x]

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(int, x.split(':'))
        return (h * 3600 + m * 60 + s) % 86400
    if isinstance(x, (datetime, pd.Timestamp)):
        return (x.hour * 3600 + x.minute * 60 + x.second) % 86400
    if isinstance(x, (int, float, np.number)):
        return float(x) % 86400
    return x

# hms(56, 34, 12)
res_hms = hms(56, 34, 12)
print(format_hms(res_hms))

# hms()
print("hms()")

# new_hms(as.numeric(1:3))
res_new_hms = new_hms(np.arange(1, 4))
for v in res_new_hms:
    print(format_hms(v))

# try(new_hms(1:3))
try:
    # In R, 1:3 is a numeric vector, so new_hms(1:3) actually works
    # The comment "Supports numeric only!" warns against non-numerics.
    new_hms(np.arange(1, 4))
except Exception as e:
    print(e)

# as_hms(1)
as_hms_1 = as_hms(1)
print(format_hms(as_hms_1))

# as_hms("12:34:56")
as_hms_str = as_hms("12:34:56")
print(format_hms(as_hms_str))

# as_hms(Sys.time())
as_hms_sys = as_hms(datetime.now())
print(format_hms(as_hms_sys))

# as.POSIXct(hms(1))
as_posixct = pd.to_datetime(hms(0,0,1), unit='s', utc=True)
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(hms(0,0,1))]})
print("  a")
print(f"1 {df_a['a'][0]}")

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(hms(hours=int(x))))

# d
print(d)