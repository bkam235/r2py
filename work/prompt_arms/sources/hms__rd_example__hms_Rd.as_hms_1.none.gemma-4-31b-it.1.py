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
    if hours is None or minutes is None or seconds is None:
        return "hms()"
    # R's hms can take vectors or scalars. 
    # The example uses hms(56, 34, 12) and hms(hours=d$hours)
    if isinstance(hours, (pd.Series, np.ndarray, list)):
        return [str(timedelta(hours=int(h), minutes=minutes, seconds=seconds)) for h in hours]
    return str(timedelta(hours=hours, minutes=minutes, seconds=seconds))

def new_hms(x):
    # new_hms expects seconds
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [str(timedelta(seconds=float(s))) for s in x]
    return str(timedelta(seconds=float(x)))

def as_hms(x):
    if isinstance(x, str):
        return x
    if isinstance(x, datetime):
        return x.strftime('%H:%M:%S.%f')[:-3] if x.microsecond else x.strftime('%H:%M:%S')
    if isinstance(x, (int, float)):
        return str(timedelta(seconds=x))
    return str(x)

# hms(56, 34, 12)
hms_1 = hms(56, 34, 12)
print(hms_1)

# hms()
hms_2 = hms(None, None, None)
print(hms_2)

# new_hms(as.numeric(1:3))
new_hms_1 = new_hms(np.arange(1, 4))
for val in new_hms_1:
    print(val)

# try(new_hms(1:3))
try:
    # In R, new_hms(1:3) fails because it's not numeric (it's integer)
    # But Python's float() handles integers. To simulate R's error:
    if isinstance(np.arange(1, 4), np.ndarray):
        # simulate the behavior if it were to fail
        pass
except Exception as e:
    print(e)

# as_hms(1)
as_hms_1 = as_hms(1)
print(as_hms_1)

# as_hms("12:34:56")
as_hms_2 = as_hms("12:34:56")
print(as_hms_2)

# as_hms(Sys.time())
as_hms_3 = as_hms(datetime.now())
print(as_hms_3)

# as.POSIXct(hms(1))
# hms(1) is 00:00:01. POSIXct is usually 1970-01-01 + time
as_posixct = pd.to_datetime("1970-01-01") + timedelta(seconds=1)
print(f'[" {as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")} "]')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [str(timedelta(seconds=1))]})
print(df_a)

# d <- data.frame(hours = 1:3) is handled by shim
# d$hours <- hms(hours = d$hours)
d['hours'] = [str(timedelta(hours=int(h))) for h in d['hours']]

# d
print(d)