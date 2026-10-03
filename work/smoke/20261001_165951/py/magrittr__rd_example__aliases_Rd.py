# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Ensure iris is a DataFrame from the shim dictionary
iris_df = pd.DataFrame(iris)

# Part 1: Iris extraction
# iris %>% extract(, 1:4) %>% head
# R's extract(, 1:4) takes columns 1 to 4.
# r2py:entity:extract
res_iris = iris_df.iloc[:, 0:4].head()
print(res_iris)

# Part 2: good.times timestamp sequence
# Sys.Date() provides the current date.
# as.POSIXct converts it to a POSIXct date-time object.
# seq(by = "15 mins", length.out = 100) creates the sequence.
# r2py:entity:Sys.Date
start_date = pd.Timestamp(datetime.now().date())
# r2py:entity:seq
good_times_list = [start_date + timedelta(minutes=15 * i) for i in range(100)]
# data.frame(timestamp = .)
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': good_times_list})

# Part 3: quarter calculation
# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# use_series(timestamp) is essentially good.times[['timestamp']] or good.times['timestamp']
# format("%M") gets the minutes as a string.
# divide_by_int(15) is integer division.
# add(1) increments the result.
# r2py:entity:good.times$quarter
good_times['quarter'] = (
# r2py:entity:use_series
    good_times['timestamp']
# r2py:entity:format
    .dt.minute
# r2py:entity:add
    .apply(lambda x: int(x) // 15 + 1)
)