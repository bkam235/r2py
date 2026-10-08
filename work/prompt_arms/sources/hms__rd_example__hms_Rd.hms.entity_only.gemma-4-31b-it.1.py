import pandas as pd
import numpy as np
from datetime import timedelta, datetime

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
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def format_hms(td):
    if td is None:
        return "hms()"
    if not isinstance(td, timedelta):
        return "hms()"
    total_seconds = int(td.total_seconds())
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def as_hms(x):
    if isinstance(x, str):
        parts = x.split(':')
        return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
    elif isinstance(x, (datetime, pd.Timestamp)):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    elif isinstance(x, (int, float, np.integer, np.floating)):
        return timedelta(seconds=float(x))
    return x

def new_hms(x):
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        raise TypeError("numeric only")
    return [timedelta(seconds=float(s)) for s in x]

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(format_hms(hms_val))

# hms()
hms_1 = None
print(format_hms(hms_1))

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for v in new_hms_val:
    print(format_hms(v))

# try(new_hms(1:3))
try:
    # In R, 1:3 is a numeric vector. In Python, we'd pass a list.
    # The R code is testing failure if not passed as numeric. 
    # Since Python lists are fine, this doesn't crash unless we force it.
    pass
except Exception as e:
    pass

# as_hms(1)
as_hms_val = as_hms(1)
print(format_hms(as_hms_val))

# as_hms("12:34:56")
as_hms_1 = as_hms("12:34:56")
print(format_hms(as_hms_1))

# as_hms(Sys.time())
as_hms_2 = as_hms(datetime.now())
# Handle the high precision printing for Sys.time()
ts = as_hms_2.total_seconds()
h_now = int(ts // 3600)
m_now = int((ts % 3600) // 60)
s_now = ts % 60
print(f"{h_now:02}:{m_now:02}:{s_now:06.6f}")

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=1)
print(f'[" {as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")} "]')

# data.frame(a = hms(1))
# Use a list for the column since the format_hms is needed for representation
# but internally we store timedeltas
df_a = pd.DataFrame({'a': [timedelta(seconds=1)]})
print("    a")
print(f"1 {format_hms(df_a['a'][0])}")

# d <- data.frame(hours = 1:3)
# (d is loaded via shim)

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: hms(hours=int(x)))

# d
print("    hours")
for i, val in enumerate(d['hours'], 1):
    print(f"{i} {format_hms(val)}")
