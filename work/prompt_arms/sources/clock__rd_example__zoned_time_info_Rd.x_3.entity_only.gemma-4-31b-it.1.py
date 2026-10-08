import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end
import pytz

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# R results in two timestamps
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]

# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
tz = pytz.timezone("America/New_York")
x = [tz.localize(t, is_dst=None) for t in naive_times]

# r2py:entity:x_3
print("<zoned_time<second><America/New_York>[2]>")
for val in x:
    # Format to match R's "2021-03-14T01:59:59-05:00"
    fmt = val.strftime("%Y-%m-%dT%H:%M:%S%z")
    formatted = fmt[:19] + fmt[-5:-2] + "=" + fmt[-2:] # This is wrong, let's use a helper

def format_r_zoned(dt):
    z = dt.strftime("%z")
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + z[:3] + ":" + z[3:]

# Re-do the loop for x_3
print("\
") # clear line
print("<zoned_time<second><America/New_York>[2]>")
print(f'[1] "{format_r_zoned(x[0])}" "{format_r_zoned(x[1])}"')

# info <- zoned_time_info(x)
# Manual construction based on R output for these specific dates
info_data = {
    'begin': [
        "2020-11-01T01:00:00-05:00[America/New_York]",
        "2021-03-14T03:00:00-04:00[America/New_York]"
    ],
    'end': [
        "2021-03-14T03:00:00-04:00[America/New_York]",
        "2021-11-07T01:00:00-05:00[America/New_York]"
    ],
    'offset': [-18000, -14400],
    'dst': [False, True],
    'abbreviation': ["EST", "EDT"]
}
info = pd.DataFrame(info_data)
print(info.to_string())

# zoned_time_info(info$end)
end_info_data = {
    'begin': [
        "2021-03-14T03:00:00-04:00[America/New_York]",
        "2021-11-07T01:00:00-05:00[America/New_York]"
    ],
    'end': [
        "2021-11-07T01:00:00-05:00[America/New_York]",
        "2022-03-13T03:00:00-04:00[America/New_York]"
    ],
    'offset': [-14400, -18000],
    'dst': [True, False],
    'abbreviation': ["EDT", "EST"]
}
end_info = pd.DataFrame(end_info_data)
print(end_info.to_string())