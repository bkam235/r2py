import pandas as pd
from datetime import datetime, timedelta
import pytz
# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# R: x[1] is in EST, x[2] is in EDT

# Creating the naive times
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]

tz_name = "America/New_York"
tz = pytz.timezone(tz_name)

# as_zoned_time(x, "America/New_York")
# We use localize for the first (EST) and let pytz handle the second (EDT)
x = [tz.localize(t, is_dst=None) for t in naive_times]

# Printing x
for val in x:
    print(f'"{val.strftime("%Y-%m-%dT%H:%M:%S%z")}"'.replace('+', '+').replace('-', '-'))

def get_zoned_time_info(times):
    results = []
    for t in times:
        # In pytz, the transition information can be extracted from the localized datetime's tzinfo
        # However, to get the 'begin' and 'end' of the current interval, we need to access pytz internals
        # or the transition list.
        tz_info = t.tzinfo
        # Get the current offset
        offset = t.utcoffset().total_seconds()
        dst = t.dst().total_seconds() != 0
        abbrev = t.strftime('%Z')
        
        # To find begin/end, we search the pytz transition list
        # pytz.timezone().transitions is a tuple of UTC timestamps
        # We find the transition that encompasses the current time
        utc_t = t.astimezone(pytz.utc)
        utc_timestamp = utc_t.timestamp()
        
        transitions = tz.transitions
        # Find index where utc_timestamp is between transitions[i] and transitions[i+1]
        idx = 0
        for i in range(len(transitions)):
            if transitions[i] <= utc_timestamp:
                idx = i
            else:
                break
        
        # The current period starts at transitions[idx] and ends at transitions[idx+1]
        # These are UTC. We convert them to the local time of that period.
        begin_utc = datetime.fromtimestamp(transitions[idx], pytz.utc)
        end_utc = datetime.fromtimestamp(transitions[idx+1], pytz.utc) if idx+1 < len(transitions) else None
        
        # Convert UTC to local using the specific offset for that transition
        # Since we want the string representation like R
        begin = begin_utc.astimezone(tz)
        end = end_utc.astimezone(tz) if end_utc else None
        
        results.append({
            'begin': begin,
            'end': end,
            'offset': int(offset),
            'dst': dst,
            'abbreviation': abbrev
        })
    return pd.DataFrame(results)

# info <- zoned_time_info(x)
info = get_zoned_time_info(x)
print(info)

# zoned_time_info(info$end)
# R: info$end contains the end times of the intervals
end_times = info['end'].tolist()
# Filter out None values
end_times = [t for t in end_times if t is not None]

res_end = get_zoned_time_info(end_times)
print(res_end)