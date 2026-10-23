import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__rd_example__date-time-zone_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__date-time-zone_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x', 'y', 'y_nt']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# r2py:entity:x
def date_parse(x):
    # R's date_parse returns a Date object (naive)
    return pd.to_datetime(x).date()

# r2py:entity:date_time_zone
def date_time_zone(x):
    # In R clock, date_time_zone returns the zone name
    if hasattr(x, 'tz') and x.tz is not None:
        return x.tz.zone
    # If it's a date object, R's clock throws an error
    if isinstance(x, (datetime.date, pd.Timestamp)) and (not hasattr(x, 'tz') or x.tz is None):
        raise TypeError("Date is considered a naive time with an unspecified time zone.")
    return None

# r2py:entity:try_1
def date_time_set_zone(x, zone):
    # R's date_time_set_zone is like tz_convert (keeps underlying duration)
    if hasattr(x, 'tz_convert'):
        return x.tz_convert(zone)
    raise TypeError("Time zones can only be get or set for date-times.")

# r2py:entity:x_1
def date_time_parse(x, zone, format=None):
    # Parses string as naive then localizes to zone
    ts = pd.to_datetime(x)
    return ts.tz_localize(zone)

# r2py:entity:as_naive_time
def as_naive_time(x):
    # Drops the timezone information
    if hasattr(x, 'tz_localize'):
        return x.tz_localize(None)
    return x

# r2py:entity:as_date_time
def as_date_time(x, zone, nonexistent=None):
    # Localizes naive time to zone, handling nonexistent times
    # nonexistent = "roll-forward" -> shift_forward
    # nonexistent = "roll-backward" -> shift_backward
    nonexistent_map = {
        "roll-forward": "shift_forward",
        "roll-backward": "shift_backward"
    }
    mode = nonexistent_map.get(nonexistent, 'raise')
    return x.tz_localize(zone, nonexistent=mode)

# --- Execution ---

# x <- date_parse("2019-01-01")
# r2py:entity:x
x = date_parse("2019-01-01")

# try(date_time_zone(x))
# r2py:entity:try
try:
    date_time_zone(x)
except Exception as e:
    pass # R's try() just suppresses/reports, we follow the logic

# try(date_time_set_zone(x, "America/New_York"))
# r2py:entity:try_1
try:
    date_time_set_zone(x, "America/New_York")
except Exception as e:
    pass

# x <- date_time_parse("2019-01-02 01:30:00", "America/New_York")
# r2py:entity:x_1
x = date_time_parse("2019-01-02 01:30:00", "America/New_York")
print(f'[{x.strftime("%Y-%m-%d %H:%M:%S %Z")}]')

# r2py:entity:x_2
# date_time_zone(x)
# r2py:entity:date_time_zone
print(f'["{date_time_zone(x)}"]')

# r2py:entity:date_time_set_zone
# date_time_set_zone(x, "America/Los_Angeles")
x_la = date_time_set_zone(x, "America/Los_Angeles")
print(f'["{x_la.strftime("%Y-%m-%d %H:%M:%S %Z")}]')

# x %>% as_naive_time() %>% as_date_time("America/Los_Angeles")
# r2py:entity:as_naive_time
x_naive = as_naive_time(x)
# r2py:entity:as_date_time
x_final = as_date_time(x_naive, "America/Los_Angeles")
print(f'["{x_final.strftime("%Y-%m-%d %H:%M:%S %Z")}]')

# y <- date_time_parse("2021-03-28 03:30:00", "America/New_York")
# r2py:entity:y
y = date_time_parse("2021-03-28 03:30:00", "America/New_York")
print(f'["{y.strftime("%Y-%m-%d %H:%M:%S %Z")}]')
# r2py:entity:y_1

# y_nt <- as_naive_time(y)
# r2py:entity:y_nt
y_nt = as_naive_time(y)
print("<naive_time<second>[1]>")
print(f'["{y_nt.strftime("%Y-%m-%dT%H:%M:%S")}]')

# r2py:entity:y_nt_1
# try(as_date_time(y_nt, "Europe/Helsinki"))
# r2py:entity:try_2
try:
    as_date_time(y_nt, "Europe/Helsinki")
except Exception as e:
    pass

# as_date_time(y_nt, "Europe/Helsinki", nonexistent = "roll-forward")
# r2py:entity:as_date_time_1
y_fwd = as_date_time(y_nt, "Europe/Helsinki", nonexistent="roll-forward")
print(f'["{y_fwd.strftime("%Y-%m-%d %H:%M:%S %Z")}]')

# as_date_time(y_nt, "Europe/Helsinki", nonexistent = "roll-backward")
# r2py:entity:as_date_time_2
y_bwd = as_date_time(y_nt, "Europe/Helsinki", nonexistent="roll-backward")
print(f'["{y_bwd.strftime("%Y-%m-%d %H:%M:%S %Z")}]')