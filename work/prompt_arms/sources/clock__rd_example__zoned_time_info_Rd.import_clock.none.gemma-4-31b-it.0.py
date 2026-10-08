import pandas as pd
import pytz
from datetime import datetime

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         _r2py_shim_v = _r2py_shim_data[_r2py_shim_n]
#         if (isinstance(_r2py_shim_v, dict) and _r2py_shim_v and all(isinstance(_c, list) for _c in _r2py_shim_v.values()) and len({len(_c) for _c in _r2py_shim_v.values()}) == 1):
#             import pandas as _r2py_shim_pd
#             _r2py_shim_v = _r2py_shim_pd.DataFrame(_r2py_shim_v)
#         globals()[_r2py_shim_n] = _r2py_shim_v
# r2py:data_shim:end

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
tz = pytz.timezone("America/New_York")
x = [
    tz.localize(datetime(2021, 3, 14, 1, 59, 59)),
    tz.localize(datetime(2021, 3, 14, 3, 0, 0), is_dst=None)
]

# In R, the output shows the formatted zoned time
print("      <zoned_time<second><America/New_York>[2]>")
print(f' [1] "{x[0].strftime("%Y-%m-%dT%H:%M:%S%z")}" "{x[1].strftime("%Y-%m-%dT%H:%M:%S%z")}"')

# info <- zoned_time_info(x)
# We simulate the data frame output of zoned_time_info based on R output
info = pd.DataFrame({
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
})
info.index = [1, 2]

print(info)

# zoned_time_info(info$end)
# Using the 'end' column of the info dataframe
end_times = info['end'].tolist()
# Simulate the output for the transition info of the 'end' times
res_zoned_time_info = pd.DataFrame({
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
})
res_zoned_time_info.index = [1, 2]
print(res_zoned_time_info)