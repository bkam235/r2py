# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20260930_152523/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# magrittr is a piping package; logic is inline

# Load iris from shim
iris_df = pd.DataFrame(iris)

# Section 1: iris extract and head
# extract is .Primitive("["), used as extract(, 1:4)
# r2py:entity:extract
res_iris = iris_df.iloc[:, 0:4].head()
print(res_iris)

# Section 2: good.times creation
# r2py:entity:Sys.Date
start_date = pd.Timestamp.now().normalize()

# seq(by = "15 mins", length.out = 100)
# r2py:entity:seq
good_times_seq = pd.date_range(start=start_date, periods=100, freq='15min')

# data.frame(timestamp = .)
# r2py:entity:data.frame
good_times_df = pd.DataFrame({'timestamp': good_times_seq})
globals()['good.times'] = good_times_df

# Section 3: quarter calculation
# use_series is .Primitive("$")
# r2py:entity:good.times$quarter
series_timestamp = good_times_df['timestamp']

# format("%M") returns minutes as string
# r2py:entity:format
minutes_str = series_timestamp.dt.strftime('%M')

# as.numeric %>% divide_by_int(15)
# divide_by_int is .Primitive("%/%") (integer division)
# r2py:entity:divide_by_int
minutes_int = minutes_str.astype(int) // 15

# add(1)
# add is .Primitive("+")
# r2py:entity:add
quarter_vals = minutes_int + 1

globals()['good.times']['quarter'] = quarter_vals