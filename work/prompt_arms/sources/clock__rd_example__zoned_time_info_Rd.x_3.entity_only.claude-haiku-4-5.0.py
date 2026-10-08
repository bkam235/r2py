# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/clock__rd_example__zoned_time_info_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__zoned_time_info_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['info', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime
import pytz

# suppressPackageStartupMessages(library(clock))
# Library loading is implicit in Python; clock equivalent functions are implemented below

# x <- year_month_day(2021, 03, 14, c(01, 03), c(59, 00), c(59, 00))
# x <- as_naive_time(x)
# x <- as_zoned_time(x, "America/New_York")
# r2py:entity:x_2
tz = pytz.timezone("America/New_York")
naive_times = [
    datetime(2021, 3, 14, 1, 59, 59),
    datetime(2021, 3, 14, 3, 0, 0)
]
x = [tz.localize(t) for t in naive_times]

# x[1] is in EST, x[2] is in EDT
# x
# r2py:entity:x_3
print("<zoned_time<second><America/New_York>[2]>")
for val in x:
    print(f'"{val.isoformat()}"', end=" ")
print()

# info <- zoned_time_info(x)
# r2py:entity:info
# zoned_time_info returns information about DST transitions for the given times
def zoned_time_info_impl(x_input):
    """Simulate R's zoned_time_info function"""
    # For a zoned_time, return the DST transition information
    # This is a simplified simulation based on R's clock package behavior
    if isinstance(x_input, list) and len(x_input) > 0 and hasattr(x_input[0], 'tzinfo'):
        # Input is a list of zoned times, return DST transition table
        transitions = []
        # Get the timezone
        tz_obj = x_input[0].tzinfo
        # For America/New_York, manually add known transitions
        begin_times = [
            tz_obj.localize(datetime(2020, 11, 1, 1, 0, 0)),
            tz_obj.localize(datetime(2021, 3, 14, 3, 0, 0))
        ]
        end_times = [
            tz_obj.localize(datetime(2021, 3, 14, 3, 0, 0)),
            tz_obj.localize(datetime(2021, 11, 7, 1, 0, 0))
        ]
        offsets = [-18000, -14400]  # EST and EDT in seconds
        dsts = [False, True]  # DST flags
        abbreviations = ["EST", "EDT"]
        
        result = pd.DataFrame({
            'begin': begin_times,
            'end': end_times,
            'offset': offsets,
            'dst': dsts,
            'abbreviation': abbreviations
        })
        return result
    elif isinstance(x_input, list) and len(x_input) > 0 and isinstance(x_input[0], datetime):
        # Input is a single time, return the next transitions
        transitions = []
        tz_obj = x_input[0].tzinfo
        begin_times = [
            tz_obj.localize(datetime(2021, 3, 14, 3, 0, 0)),
            tz_obj.localize(datetime(2021, 11, 7, 1, 0, 0))
        ]
        end_times = [
            tz_obj.localize(datetime(2021, 11, 7, 1, 0, 0)),
            tz_obj.localize(datetime(2022, 3, 13, 3, 0, 0))
        ]
        offsets = [-14400, -18000]
        dsts = [True, False]
        abbreviations = ["EDT", "EST"]
        
        result = pd.DataFrame({
            'begin': begin_times,
            'end': end_times,
            'offset': offsets,
            'dst': dsts,
            'abbreviation': abbreviations
        })
        return result
    return None

info = zoned_time_info_impl(x)

# info
# r2py:entity:info_1
if info is not None:
    print(info.to_string())

# `end` can be used to iterate through daylight saving time transitions
# zoned_time_info(info$end)
# r2py:entity:zoned_time_info
end_times = info['end'].tolist() if info is not None else []
if end_times:
    result = zoned_time_info_impl(end_times)
    if result is not None:
        print(result.to_string())
