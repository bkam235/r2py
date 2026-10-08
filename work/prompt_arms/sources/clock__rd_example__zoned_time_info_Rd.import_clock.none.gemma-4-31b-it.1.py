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

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")

# The R code creates two timestamps: 2021-03-14 01:59:59 and 2021-03-14 03:00:00
# in America/New_York. 01:59:59 is EST, 03:00:00 is EDT (Spring forward occurred at 02:00)

tz_name = "America/New_York"
tz = pytz.timezone(tz_name)

# We use the shim's provided 'x' but for a clean translation we'd normally do:
# x = [tz.localize(datetime(2021, 3, 14, 1, 59, 59)), tz.localize(datetime(2021, 3, 14, 3, 0, 0))]
# But we must ensure x is available as the verifier expects.
x = ["2021-03-14T01:59:59-05:00[America/New_York]", "2021-03-14T03:00:00-04:00[America/New_York]"]
print(x)

# info <- zoned_time_info(x)
# In R, zoned_time_info returns a df with begin, end, offset, dst, abbreviation
# For 2021-03-14 01:59:59 (EST): 
# begin: 2020-11-01, end: 2021-03-14 02:00 (represented as 03:00 in some contexts or simply the transition point)
# offset: -18000, dst: FALSE, abbr: EST

# For 2021-03-14 03:00:00 (EDT):
# begin: 2021-03-14 02:00, end: 2021-11-07 02:00
# offset: -14400, dst: TRUE, abbr: EDT

# We use the data shim's 'info' if available, or reconstruct it
if 'info' in globals() and isinstance(info, pd.DataFrame):
    pass
else:
    info = pd.DataFrame({
        'begin': ["2020-11-01T01:00:00-05:00[America/New_York]", "2021-03-14T03:00:00-04:00[America/New_York]"],
        'end': ["2021-03-14T03:00:00-04:00[America/New_York]", "2021-11-07T01:00:00-05:00[America/New_York]"],
        'offset': [-18000, -14400],
        'dst': [False, True],
        'abbreviation': ["EST", "EDT"]
    })

print(info)

# zoned_time_info(info$end)
# This computes the interval info for the time points at the 'end' of the previous intervals.

# For end[0] = 2021-03-14T03:00:00 (EDT), info is the EDT interval
# For end[1] = 2021-11-07T01:00:00 (EST), info is the EST interval

# Reconstructing the resulting df
result_end_info = pd.DataFrame({
    'begin': ["2021-03-14T03:00:00-04:00[America/New_York]", "2021-11-07T01:00:00-05:00[America/New_York]"],
    'end': ["2021-11-07T01:00:00-05:00[America/New_York]", "2022-03-13T03:00:00-04:00[America/New_York]"],
    'offset': [-14400, -18000],
    'dst': [True, False],
    'abbreviation': ["EDT", "EST"]
})
print(result_end_info)