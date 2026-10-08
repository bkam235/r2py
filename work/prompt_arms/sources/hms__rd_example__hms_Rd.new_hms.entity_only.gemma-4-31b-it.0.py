import pandas as pd
import numpy as np
from datetime import timedelta, datetime, timezone

def format_hms(seconds):
    if pd.isna(seconds):
        return "hms()"
    s = float(seconds) % 86400
    hours = int(s // 3600)
    minutes = int((s % 3600) // 60)
    secs = s % 60
    if secs == 0:
        return f"{hours:02d}:{minutes:02d}:{int(secs):02d}"
    return f"{hours:02d}:{minutes:02d}:{secs:06.6f}".rstrip('0').rstrip('.')

def hms(hours=0, minutes=0, seconds=0):
    if isinstance(hours, (pd.Series, np.ndarray, list)):
        return np.array([float(h) * 3600 for h in hours])
    return float(hours * 3600 + minutes * 60 + seconds)

def new_hms(x):
    return np.array([float(i) for i in x])

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return h * 3600 + m * 60 + s
    if isinstance(x, datetime):
        return x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6
    return float(x)

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

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(format_hms(hms_val))

# hms()
hms_empty = hms()
print("hms()")

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for val in new_hms_val:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    new_hms_try = new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
as_hms_1 = as_hms(1)
print(format_hms(as_hms_1))

# as_hms("12:34:56")
as_hms_1_str = as_hms("12:34:56")
print(format_hms(as_hms_1_str))

# as_hms(Sys.time())
as_hms_2 = as_hms(datetime.now())
print(format_hms(as_hms_2))

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=hms(1))
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
data_frame_a = pd.DataFrame({'a': [format_hms(hms(1))]})
print(data_frame_a)

# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
d['hours'] = [format_hms(hms(h)) for h in d['hours']]

# d
d_1 = d
print(d_1)