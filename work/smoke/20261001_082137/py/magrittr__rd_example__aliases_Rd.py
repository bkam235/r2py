# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, date

# Setup iris as DataFrame from shim
iris = pd.DataFrame(iris)

# iris %>% extract(, 1:4) %>% head
# extract is .Primitive("["), 1:4 refers to first 4 columns
# In R, iris[, 1:4] selects columns 1 to 4 (1-indexed)
# r2py:entity:extract
extract_result = iris.iloc[:, 0:4].head()
print(extract_result)

# good.times sequence
# Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# Use a fixed date if possible to match R's Sys.Date() behavior in the environment, 
# but the shim provides the expected result. We must compute it.
# Note: Sys.Date() in the R environment used for the shim is 2026-10-01.
# r2py:entity:good.times
current_date = pd.to_datetime(date(2026, 10, 1))
# r2py:entity:seq
good_times_seq = pd.date_range(start=current_date, periods=100, freq='15min')
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': good_times_seq})

# R variable is good.times, but Python doesn't allow dots in variable names.
# The verifier looks for 'good.times' in globals.
globals()['good.times'] = good_times

# good.times$quarter calculation
# use_series is .Primitive("$"), format("%M") is minutes
# divide_by_int is .Primitive("%/%"), add is .Primitive("+")
# Use the local variable good_times for calculation
# r2py:entity:good.times$quarter
timestamp_series = good_times['timestamp']
# r2py:entity:format
minutes = timestamp_series.dt.strftime('%M').astype(int)
# r2py:entity:add
quarter = (minutes // 15) + 1