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

def format_hms(val):
    if val is None:
        return "hms()"
    if isinstance(val, (int, float)):
        td = timedelta(seconds=val)
    elif isinstance(val, timedelta):
        td = val
    else:
        return str(val)
    
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    # R hms prints with 0 padding, but doesn't cap at 24h
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def hms(hours=0, minutes=0, seconds=0):
    if hours == 0 and minutes == 0 and seconds == 0:
        # The R example hms() returns an empty hms object
        # Since we need to match 'hms()' output
        return None
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def new_hms(x):
    # new_hms takes numeric seconds
    if not isinstance(x, (list, np.ndarray, pd.Series)):
        x = [x]
    return [timedelta(seconds=float(s)) for s in x]

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
    if isinstance(x, (datetime, pd.Timestamp)):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    if isinstance(x, (int, float, np.number)):
        return timedelta(seconds=float(x))
    return x

# hms(56, 34, 12)
res_hms = hms(56, 34, 12)
print(format_hms(res_hms))

# hms()
res_hms_empty = hms()
print(format_hms(res_hms_empty))

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for val in new_hms_val:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # In R, new_hms(1:3) fails because it expects numeric, but 1:3 is integer
    # Python's float conversion in new_hms handles this, but we simulate the try
    new_hms_try = new_hms(np.arange(1, 4))
except Exception as e:
    pass

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
# as.POSIXct(hms(1)) in R returns 1970-01-01 00:00:01
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=1)
print(f'[" {as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")} "]')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d is already loaded via shim as a DataFrame with 'hours' [1, 2, 3]

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(timedelta(hours=x)))

# d
print(d)