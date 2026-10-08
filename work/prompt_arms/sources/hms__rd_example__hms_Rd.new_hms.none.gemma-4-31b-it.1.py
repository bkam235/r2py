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
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# hms(56, 34, 12)
hms = timedelta(hours=56, minutes=34, seconds=12)
print(format_hms(hms))

# hms()
hms_1 = pd.NA
print(format_hms(hms_1))

# new_hms(as.numeric(1:3))
new_hms = [timedelta(seconds=s) for s in range(1, 4)]
for val in new_hms:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # In R, 1:3 is numeric, so new_hms(1:3) works. 
    # The comment says "Supports numeric only!", implying it would fail on chars.
    new_hms_try = [timedelta(seconds=s) for s in range(1, 4)]
except Exception as e:
    print(e)

# as_hms(1)
as_hms = timedelta(seconds=1)
print(format_hms(as_hms))

# as_hms("12:34:56")
h, m, s = map(int, "12:34:56".split(':'))
as_hms_1 = timedelta(hours=h, minutes=m, seconds=s)
print(format_hms(as_hms_1))

# as_hms(Sys.time())
now = datetime.now()
as_hms_2 = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
print(format_hms(as_hms_2))

# as.POSIXct(hms(1))
as_posixct = pd.to_datetime("1970-01-01") + timedelta(seconds=1)
print(f'[1] "{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
print(df_a)

# d <- data.frame(hours = 1:3)
# d is already provided by data_shim as a DataFrame

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(timedelta(hours=int(x))))

# d
print(d)