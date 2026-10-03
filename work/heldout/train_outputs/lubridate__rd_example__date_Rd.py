import pandas as pd
import numpy as np
from datetime import datetime, date as py_date
import pytz

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'lubridate__rd_example__date_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:date
def r_print_date(d):
    """Helper to match R's print format for Date objects: [1] 'YYYY-MM-DD'"""
    print(f'[1] "{d}"')

def r_print_posix(ts):
    """Helper to match R's print format for POSIXct: [1] 'YYYY-MM-DD HH:MM:SS TZ'"""
    # R usually uses abbreviated TZ names (e.g., EST)
    tz_name = ts.tzname()
    print(f'[1] "{ts.strftime("%Y-%m-%d %H:%M:%S")} {tz_name}"')

# x <- ymd_hms("2012-03-26 23:12:13", tz = "America/New_York")
# r2py:entity:x
x = pd.Timestamp("2012-03-26 23:12:13", tz="America/New_York")

# date(x)
# R's date() on a POSIXct object extracts the date in the object's timezone.
# r2py:entity:date
r_print_date(x.date().isoformat())

# as.Date(x) # by default as.Date assumes you want to know the date in UTC
# R's as.Date(POSIXct) converts to UTC first.
# r2py:entity:as.Date
r_print_date(x.tz_convert("UTC").date().isoformat())

# as.Date(x, tz = "America/New_York")
# r2py:entity:as.Date_1
r_print_date(x.tz_convert("America/New_York").date().isoformat())

# date(x) <- as.Date("2000-01-02")
# In lubridate, date(x) <- value replaces the date part while keeping the time and timezone.
# r2py:entity:date(x)
target_date = pd.to_datetime("2000-01-02").date()
x = x.replace(year=target_date.year, month=target_date.month, day=target_date.day)

# x
# r2py:entity:x_1
r_print_posix(x)