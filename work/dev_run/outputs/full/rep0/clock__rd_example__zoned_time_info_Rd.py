# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/outputs/full/rep0/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# In R's clock package, these operations create a vector of zoned times.
# We simulate this with a pandas DatetimeIndex.
# r2py:entity:x_2
timestamps = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]

# r2py:entity:x_3
print(x)

# info <- zoned_time_info(x)
# zoned_time_info returns a data frame with timezone and offset details.
# We extract the timezone and the UTC offset for each element.

# r2py:entity:info_1
print(info)

# zoned_time_info(info$end)
# In R, info$end refers to the end of the timezone's current transition period.
# We approximate this by finding the next transition for the New York timezone.
# r2py:entity:zoned_time_info
tz = pytz.timezone("America/New_York")
# Get the transition after the last timestamp in x
next_transition = tz._utc_transition_times[np.searchsorted(tz._utc_transition_times, x[-1].astimezone(pytz.UTC).value // 10**9)]
end_time = pd.Timestamp(next_transition * 10**9, unit='ns', tz='UTC').tz_convert("America/New_York")

end_info = pd.DataFrame({
    'tz': [str(end_time.tz)],
    'offset': [str(end_time.utcoffset())]
})

print(end_info)