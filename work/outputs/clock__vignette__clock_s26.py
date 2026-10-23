# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/clock__vignette__clock_s26.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'clock__vignette__clock_s26.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(clock))
# No Python equivalent needed for startup message suppression

# x <- seq(
#   date_time_build(2019, 1, 1, 1, 55, zone = "UTC"),
#   date_time_build(2019, 1, 1, 2, 15, zone = "UTC"),
#   by = 120
# )
# r2py:entity:x
start = pd.Timestamp(year=2019, month=1, day=1, hour=1, minute=55, tz="UTC")
end = pd.Timestamp(year=2019, month=1, day=1, hour=2, minute=15, tz="UTC")
x = pd.date_range(start=start, end=end, freq="120S")

# x
# R print format: [1] "YYYY-MM-DD HH:MM:SS UTC" ...
# We need to format the output to match R's console display
# r2py:entity:x_1
x_str = [t.strftime("%Y-%m-%d %H:%M:%S UTC") for t in x]
# Printing in chunks of 2 as R does for this specific output
for i in range(0, len(x_str), 2):
    chunk = x_str[i:i+2]
    prefix = f" [{i+1}] " if i == 0 else f" [{i+1}] "
    # R's specific formatting for the first line vs others
    line = " ".join([f'"{s}"' for s in chunk])
    print(f"{prefix}{line}")

# date_group(x, "minute", n = 5)
# date_group in clock package groups by rounding down to the nearest n-unit boundary.
# For "minute" and n=5, this is essentially floor to 5 minutes.
# r2py:entity:date_group
grouped = x.floor("5min")
grouped_str = [t.strftime("%Y-%m-%d %H:%M:%S UTC") for t in grouped]
for i in range(0, len(grouped_str), 2):
    chunk = grouped_str[i:i+2]
    prefix = f" [{i+1}] " if i == 0 else f" [{i+1}] "
    line = " ".join([f'"{s}"' for s in chunk])
    print(f"{prefix}{line}")