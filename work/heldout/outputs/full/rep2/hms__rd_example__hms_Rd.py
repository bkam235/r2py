import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

class HMS:
    """Class to mimic R's hms object behavior and printing."""
    def __init__(self, seconds):
        self.seconds = float(seconds)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        total_seconds = self.seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        secs = total_seconds % 60
        
        if secs == int(secs):
            return f"{hours:02}:{minutes:02}:{int(secs):02}"
        else:
            # R typically prints fractional seconds with 6 digits if present
            return f"{hours:02}:{minutes:02}:{secs:06.6f}"

# r2py:entity:new_hms
def new_hms(x):
    """Approximate new_hms: converts numeric seconds to HMS object."""
    if isinstance(x, (list, np.ndarray, pd.Series)):
        return [HMS(v) for v in x]
    return HMS(x)

# r2py:entity:hms
def hms(seconds=None, minutes=None, hours=None, days=None):
    """Approximate hms() construction logic."""
    if seconds is None and minutes is None and hours is None and days is None:
        return "hms()"
        
    total_secs = 0.0
    if seconds is not None: total_secs += float(seconds)
    if minutes is not None: total_secs += float(minutes) * 60
    if hours is not None: total_secs += float(hours) * 3600
    if days is not None: total_secs += float(days) * 86400
    
    return new_hms(total_secs)

# r2py:entity:as_hms
def as_hms(x):
    """Approximate as_hms conversion."""
    if isinstance(x, str):
        parts = x.split(':')
        if len(parts) == 3:
            h, m, s = map(float, parts)
            return HMS(h * 3600 + m * 60 + s)
        return HMS(0)
    if isinstance(x, (datetime, pd.Timestamp)):
        return HMS(x.hour * 3600 + x.minute * 60 + x.second + x.microsecond / 1e6)
    if isinstance(x, (int, float, np.number)):
        return new_hms(x)
    return new_hms(x)

# r2py:entity:as.POSIXct
def as_posixct_hms(x):
    """Approximate as.POSIXct(hms_obj)."""
    epoch = datetime(1970, 1, 1)
    if isinstance(x, HMS):
        return epoch + timedelta(seconds=x.seconds)
    return epoch

# --- Execution ---

# suppressPackageStartupMessages(library(hms))
# hms(56, 34, 12)
# r2py:entity:hms
res_hms = hms(56, 34, 12)
print(res_hms)

# hms()
# r2py:entity:hms_1
res_hms_empty = hms()
print(res_hms_empty)

# new_hms(as.numeric(1:3))
# r2py:entity:new_hms
res_new_hms = new_hms(np.arange(1, 4))
for val in res_new_hms:
    print(val)

# try(new_hms(1:3))
# r2py:entity:try
try:
    new_hms(np.arange(1, 4))
except Exception:
    pass

# as_hms(1)
# r2py:entity:as_hms
res_as_hms_1 = as_hms(1)
print(res_as_hms_1)

# as_hms("12:34:56")
# r2py:entity:as_hms_1
res_as_hms_2 = as_hms("12:34:56")
print(res_as_hms_2)

# as_hms(Sys.time())
# r2py:entity:as_hms_2
res_as_hms_3 = as_hms(datetime.now())
print(res_as_hms_3)

# as.POSIXct(hms(1))
# r2py:entity:as.POSIXct
res_posix = as_posixct_hms(hms(1))
print(f'[1] "{res_posix.strftime("%Y-%m-%d %H:%M:%S")} UTC"')

# data.frame(a = hms(1))
# r2py:entity:data.frame
df_a = pd.DataFrame({'a': [str(hms(1))]})
print("   a")
print(f"1 {df_a['a'][0]}")

# d <- data.frame(hours = 1:3)
# r2py:entity:d
d = pd.DataFrame({'hours': np.arange(1, 4)})

# d$hours <- hms(hours = d$hours)
# r2py:entity:d$hours
d['hours'] = [str(hms(hours=h)) for h in d['hours']]

# d
# r2py:entity:d_1
print("  hours")
for i in range(len(d)):
    print(f"{i+1} {d['hours'][i]}")