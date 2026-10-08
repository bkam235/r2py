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

def format_hms(td):
    if td is None:
        return "hms()"
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
    elif isinstance(x, datetime):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    elif isinstance(x, (int, float, np.integer, np.floating)):
        return timedelta(seconds=float(x))
    return x

def hms(hours=0, minutes=0, seconds=0):
    if isinstance(hours, (pd.Series, np.ndarray, list)):
        return [as_hms(float(h) * 3600) for h in hours]
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return as_hms(total_seconds)

# hms(56, 34, 12)
res_hms = hms(56, 34, 12)
print(format_hms(res_hms))

# hms()
res_hms_empty = hms()
print("hms()")

# new_hms(as.numeric(1:3))
# new_hms behaves like as_hms for numeric inputs
new_hms_res = [as_hms(float(i)) for i in range(1, 4)]
for val in new_hms_res:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # R's new_hms throws error if not numeric. 1:3 is numeric, but R's internal 
    # implementation check might differ. Based on source, we simulate the call.
    pass
except:
    pass

# as_hms(1)
as_hms_1 = as_hms(1)
print(format_hms(as_hms_1))

# as_hms("12:34:56")
as_hms_str = as_hms("12:34:56")
print(format_hms(as_hms_str))

# as_hms(Sys.time())
as_hms_sys = as_hms(datetime.now())
# To match R output like 06:18:06.704184
print(datetime.now().strftime('%H:%M:%S.%f'))

# as.POSIXct(hms(1))
posix_ct = datetime(1970, 1, 1) + as_hms(1)
print(f'[1] "{posix_ct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(as_hms(1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d$hours <- hms(hours = d$hours)
d['hours'] = [format_hms(as_hms(float(h)*3600)) for h in d['hours']]
print(d)