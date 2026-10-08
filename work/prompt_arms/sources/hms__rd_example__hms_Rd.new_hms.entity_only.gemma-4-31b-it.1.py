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

def format_hms(seconds):
    if pd.isna(seconds) or seconds is None:
        return "hms()"
    td = timedelta(seconds=float(seconds))
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    # R's hms can exceed 24 hours but doesn't show "days"
    return f"{hours:02}:{minutes:02}:{secs:02}"

def hms(hours=0, minutes=0, seconds=0):
    return hours * 3600 + minutes * 60 + seconds

def new_hms(x):
    return np.array(x)

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return h * 3600 + m * 60 + s
    if isinstance(x, datetime):
        return x.hour * 3600 + x.minute * 60 + x.second
    return float(x)

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(format_hms(hms_val))

# hms()
hms_1 = hms()
print(format_hms(np.nan))

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for val in new_hms_val:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    new_hms_try = new_hms(np.arange(1, 4))
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
# Note: R's Sys.time() result varies; using the logic to extract time
print(format_hms(as_hms_2))

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=hms(1))
print(f' [1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
data_frame_a = pd.DataFrame({'a': [format_hms(hms(1))]})
print(data_frame_a)

# d <- data.frame(hours = 1:3)
# d is provided by shim

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(x * 3600))

# d
d_1 = d
print(d_1)