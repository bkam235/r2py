# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_191227/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime

# iris section
# The shim provides 'iris' as a dict.
df_iris = pd.DataFrame(iris)
# R: iris %>% extract(, 1:4) %>% head
# extract is an alias for [
# r2py:entity:extract
res_iris = df_iris.iloc[:, 0:4].head()
print(res_iris)

# good.times section
# R: good.times <- Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.Timestamp.now().normalize()
# r2py:entity:seq
good_times_range = pd.date_range(start=start_date, periods=100, freq='15min')
# r2py:entity:data.frame
good_times_df = pd.DataFrame({'timestamp': good_times_range})

# Assign to globals to match R variable name 'good.times'
globals()['good.times'] = good_times_df

# quarter section
# R: good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# use_series is an alias for $
# r2py:entity:good.times$quarter
timestamp_series = globals()['good.times']['timestamp']
# R's format("%M") extracts minutes as a string
# r2py:entity:format
minutes_str = timestamp_series.dt.strftime('%M')
minutes_num = minutes_str.astype(float)
# divide_by_int is an alias for %/% (integer division)
# r2py:entity:divide_by_int
div_res = minutes_num // 15
# add is an alias for +
# r2py:entity:add
quarter_res = div_res + 1

globals()['good.times']['quarter'] = quarter_res