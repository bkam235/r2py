# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/clock__rd_example__seq_clock_time_point_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__rd_example__seq_clock_time_point_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

def clock_print(data, precision):
    """Helper to mimic clock's printing behavior"""
    if data is None or len(data) == 0:
        return
    
    print(f"      <naive_time<{precision}>[{len(data)}]>")
    
    # R's clock printing often uses a width of 4 for these specific sequences
    width = 4
    for i in range(0, len(data), width):
        chunk = data[i : i + width]
        line_num = i + 1
        formatted_vals = " ".join([f'"{v}"' for v in chunk])
        print(f"[{line_num}] {formatted_vals}")

# r2py:entity:from
def year_month_day(year, month=None, day=None, hour=None, minute=None, second=None, subsecond=None, subsecond_precision=None):
    if month is None:
        return pd.Timestamp(year=year, month=1, day=1)
    if day is None:
        return pd.Timestamp(year=year, month=month, day=1)
    if hour is None:
        return pd.Timestamp(year=year, month=month, day=day)
    if minute is None:
        return pd.Timestamp(year=year, month=month, day=day, hour=hour)
    if second is None:
        return pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute)
    return pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

# r2py:entity:from
def as_naive_time(x):
    return pd.to_datetime(x)

# r2py:entity:seq_2
def duration_days(n):
    return pd.Timedelta(days=n)

# r2py:entity:from_1
def time_point_cast(x, precision):
    return x

# Daily sequence
# r2py:entity:seq
start_1 = as_naive_time(year_month_day(2019, 1, 1))
end_1 = as_naive_time(year_month_day(2019, 2, 4))
seq_res = pd.date_range(start=start_1, end=end_1, freq='5D')
clock_print(seq_res.strftime('%Y-%m-%d').tolist(), "day")

# Minutely sequence using minute precision naive-time
# r2py:entity:x
x = as_naive_time(year_month_day(2019, 1, 2, 3, 3))
# r2py:entity:x_1
clock_print([x.strftime('%Y-%m-%dT%H:%M')], "minute")

# seq(x, by = 4, length.out = 10)
# r2py:entity:seq_1
seq_x_1 = pd.date_range(start=x, periods=10, freq='4min')
clock_print(seq_x_1.strftime('%Y-%m-%dT%H:%M').tolist(), "minute")

# You can use larger step sizes by using a duration-based `by`
# r2py:entity:seq_2
seq_x_2 = pd.date_range(start=x, periods=5, freq='D')
clock_print(seq_x_2.strftime('%Y-%m-%dT%H:%M').tolist(), "minute")

# Nanosecond sequence
# r2py:entity:from
from_val = as_naive_time(year_month_day(2019, 1, 1))
# r2py:entity:from_1
from_val = time_point_cast(from_val, "nanosecond")
# r2py:entity:to
to_val = from_val + pd.Timedelta(nanoseconds=100)
# r2py:entity:seq_3
seq_nano = pd.date_range(start=from_val, end=to_val, freq='10ns')
formatted_nano = [t.strftime('%Y-%m-%dT%H:%M:%S') + f'.{t.nanosecond:09d}' for t in seq_nano]
clock_print(formatted_nano, "nanosecond")