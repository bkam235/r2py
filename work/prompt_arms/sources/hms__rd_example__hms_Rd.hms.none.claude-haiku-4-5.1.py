import pandas as pd
import numpy as np
from datetime import timedelta, datetime
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/hms__rd_example__hms_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'hms__rd_example__hms_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['d']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Custom class to mimic R's hms (time-of-day) class
class hms:
    """Represents time of day in HH:MM:SS format"""
    def __init__(self, hour=0, minute=0, second=0):
        # Handle both positional and keyword arguments
        self.hour = hour
        self.minute = minute
        self.second = second
        # Normalize to handle overflow (e.g., 56 hours becomes next day)
        total_seconds = self.hour * 3600 + self.minute * 60 + self.second
        self.total_seconds = total_seconds
        
    def __repr__(self):
        # Format as HH:MM:SS for times within a day
        h = self.hour % 24
        m = self.minute
        s = self.second
        return f"{h:02d}:{m:02d}:{s:02d}"
    
    def __str__(self):
        return self.__repr__()

def hms(hour=0, minute=0, second=0):
    """Create an hms time-of-day object"""
    return hms(hour, minute, second)

def new_hms(seconds):
    """Create hms object(s) from numeric seconds"""
    if isinstance(seconds, (list, np.ndarray)):
        result = []
        for s in seconds:
            h = int(s) // 3600
            m = (int(s) % 3600) // 60
            sec = int(s) % 60
            result.append(hms(h, m, sec))
        return result
    else:
        h = int(seconds) // 3600
        m = (int(seconds) % 3600) // 60
        sec = int(seconds) % 60
        return hms(h, m, sec)

def as_hms(x):
    """Convert to hms time-of-day"""
    if isinstance(x, (int, float)):
        # Treat as seconds
        h = int(x) // 3600
        m = (int(x) % 3600) // 60
        sec = int(x) % 60
        return hms(h, m, sec)
    elif isinstance(x, str):
        # Parse HH:MM:SS format
        parts = x.split(':')
        h = int(parts[0])
        m = int(parts[1])
        s = int(parts[2])
        return hms(h, m, s)
    elif isinstance(x, datetime):
        # Extract time from datetime
        return hms(x.hour, x.minute, x.second)
    return x

# hms(56, 34, 12)
print(hms(56, 34, 12))

# hms()
print(hms())

# new_hms(as.numeric(1:3))
for item in new_hms(np.arange(1, 4)):
    print(item)

# Supports numeric only!
# try(new_hms(1:3))
try:
    new_hms([1, 2, 3])
except Exception as e:
    print(e)

# as_hms(1)
print(as_hms(1))

# as_hms("12:34:56")
print(as_hms("12:34:56"))

# as_hms(Sys.time())
now = datetime.now()
print(as_hms(now))

# as.POSIXct(hms(1))
# Convert hms back to POSIXct (datetime from epoch)
epoch = datetime(1970, 1, 1)
posixct = epoch + timedelta(seconds=1)
print(f'[1] "{posixct.strftime("%Y-%m-%d %H:%M:%S")} UTC"')

# data.frame(a = hms(1))
df_a = pd.DataFrame({'a': [as_hms(1)]})
print(df_a)

# d <- data.frame(hours = 1:3)
d = pd.DataFrame({'hours': [1, 2, 3]})

# d$hours <- hms(hours = d$hours)
d['hours'] = d['hours'].apply(lambda x: as_hms(x * 3600))  # Convert hours to seconds then to hms

# d
print(d)
