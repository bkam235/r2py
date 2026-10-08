import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import pandas as pd

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
    if pd.isna(td):
        return "hms()"
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# hms(56, 34, 12)
hms_val = timedelta(hours=56, minutes=34, seconds=12)
print(format_hms(hms_val))

# hms()
hms_empty = pd.NA
print(format_hms(hms_empty))

# new_hms(as.numeric(1:3))
new_hms = [timedelta(seconds=s) for s in range(1, 4)]
for val in new_hms:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # R's new_hms only supports numeric. 1:3 is numeric, but the try is likely
    # there to demonstrate behavior. In Python we just simulate the call.
    _ = [timedelta(seconds=s) for s in range(1, 4)]
except Exception as e:
    pass

# as_hms(1)
as_hms_1 = timedelta(seconds=1)
print(format_hms(as_hms_1))

# as_hms("12:34:56")
as_hms_str = pd.to_timedelta("12:34:56")
print(format_hms(as_hms_str))

# as_hms(Sys.time())
now = datetime.now()
as_hms_sys = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
# R's as_hms(Sys.time()) returns the time part of the current time
print(format_hms(as_hms_sys))

# as.POSIXct(hms(1))
as_posixct = pd.to_datetime("1970-01-01") + timedelta(seconds=1)
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
# Using a list for the column to mimic R's data.frame
# Note: We store the timedelta but the printer in R would show formatted strings
data_frame_a = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
# Adjusting to match R's print: index starts at 1
data_frame_a.index = range(1, len(data_frame_a) + 1)
print(data_frame_a)

# d <- data.frame(hours = 1:3)
# Provided by data_shim
d = pd.DataFrame(d)

# d$hours <- hms(hours = d$hours)
# R's hms(hours = ...) treats values as hours
d['hours'] = d['hours'].apply(lambda x: format_hms(timedelta(hours=int(x))))

# d
d.index = range(1, len(d) + 1)
print(d)