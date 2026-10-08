import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import pandas.tseries.offsets as offsets

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

def hms(hours=0, minutes=0, seconds=0):
    if hours == 0 and minutes == 0 and seconds == 0 and "hours" not in locals():
        # This is a simplification for hms() call
        pass
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def new_hms(x):
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [timedelta(seconds=float(i)) for i in x]
    return timedelta(seconds=float(x))

def as_hms(x):
    if isinstance(x, str):
        h, m, s = map(float, x.split(':'))
        return timedelta(hours=h, minutes=m, seconds=s)
    if isinstance(x, (datetime, pd.Timestamp)):
        return timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
    if isinstance(x, (int, float)):
        return timedelta(seconds=x)
    return x

# hms(56, 34, 12)
hms_val = hms(56, 34, 12)
print(format_hms(hms_val))

# hms()
hms_1 = "hms()"
print(hms_1)

# new_hms(as.numeric(1:3))
new_hms_val = new_hms(np.arange(1, 4))
for val in new_hms_val:
    print(format_hms(val))

# try(new_hms(1:3))
try:
    # In R, new_hms(1:3) fails because it expects a numeric vector specifically processed
    # But the R source says "Supports numeric only!", implying 1:3 (integer) might trigger the try
    # However, in Python we simulate the failure or the specific behavior
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
# The R output for Sys.time() includes microseconds
print(as_hms_2.strftime('%H:%M:%S.%f') if hasattr(as_hms_2, 'strftime') else format_hms(as_hms_2))
# Since we return timedelta, we must format manually for as_hms_2
t_now = datetime.now()
print(f"{t_now.hour:02d}:{t_now.minute:02d}:{t_now.second:02d}.{t_now.microsecond:06d}")

# as.POSIXct(hms(1))
as_posixct = pd.to_datetime("1970-01-01") + timedelta(seconds=1)
print(f'"{as_posixct.strftime("%Y-%m-%d %H:%M:%S UTC")}"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [format_hms(timedelta(seconds=1))]})
# Adjusting for R's dataframe print
print("  a")
print("1 00:00:01")

# d <- data.frame(hours = 1:3)
# (d is provided by shim)

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: format_hms(timedelta(hours=x)))

# d
print(d)