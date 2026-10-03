# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_112951/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# magrittr provides piping and aliases; Python uses pandas method chaining

# (No Python equivalent needed for suppressing library messages)

# iris section
# r2py:entity:extract
iris_df = pd.DataFrame(iris)
iris_extracted = iris_df.iloc[:, 0:4]
# R's head() prints the first 6 rows by default
print(iris_extracted.head())

# good.times section
# r2py:entity:Sys.Date
# Sys.Date() returns the current date.
current_date = pd.to_datetime(datetime.now().date())

# r2py:entity:seq
# seq(by = "15 mins", length.out = 100)
timestamps = pd.date_range(start=current_date, periods=100, freq='15min')

# r2py:entity:data.frame
# data.frame(timestamp = .)
good_times = pd.DataFrame({'timestamp': timestamps})

# quarter calculation
# use_series(timestamp) selects the column as a series
ts_series = good_times['timestamp']

# r2py:entity:format
# format("%M") extracts minutes as string
minutes_str = ts_series.dt.strftime('%M')

# r2py:entity:divide_by_int
# as.numeric %>% divide_by_int(15)
# divide_by_int is %/% in R (integer division)
minutes_num = minutes_str.astype(int)
div_res = minutes_num // 15

# r2py:entity:add
# add(1)
good_times['quarter'] = div_res + 1

# Assigning to global variable to match R's good.times
globals()['good.times'] = good_times

# r2py:entity:good.times$quarter
# Ensuring the column exists (already done above)