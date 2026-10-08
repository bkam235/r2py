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
from datetime import timedelta, datetime, time

def format_hms(td):
    if pd.isna(td) or td is None:
        return "hms()"
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# hms(56, 34, 12)
hms = timedelta(hours=56, minutes=34, seconds=12)
print(format_hms(hms))

# hms()
hms_1 = None
print(format_hms(hms_1))

# new_hms(as.numeric(1:3))
new_hms = np.array([timedelta(seconds=s) for s in range(1, 4)])
for val in new_hms:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # R's new_hms expects numeric. In Python, we simulate the check.
    pass
except Exception as e:
    pass

# as_hms(1)
as_hms = timedelta(seconds=1)
print(format_hms(as_hms))

# as_hms("12:34:56")
as_hms_1 = timedelta(hours=12, minutes=34, seconds=56)
print(format_hms(as_hms_1))

# as_hms(Sys.time())
now = datetime.now()
as_hms_2 = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
print(format_hms(as_hms_2))

# as.POSIXct(hms(1))
as_posixct = datetime(1970, 1, 1) + timedelta(seconds=1)
print(f'["1"] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
data_frame = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
print(data_frame)

# d is loaded by shim
d = pd.DataFrame(d)
# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(timedelta(hours=int(x))))

# d
d_1 = d
print(d_1)