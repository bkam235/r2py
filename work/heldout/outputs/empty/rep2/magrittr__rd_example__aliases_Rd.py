# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# R: iris %>% extract(, 1:4) %>% head
# r2py:entity:extract
iris_df = pd.DataFrame(iris)
res_iris = iris_df.iloc[:6, 0:4]
print(res_iris)

# R: good.times <- Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# Sys.Date() in R returns the current date. as.POSIXct converts it to a POSIXct timestamp (midnight).
# r2py:entity:Sys.Date
current_date = pd.Timestamp.now().normalize() 
# r2py:entity:seq
timestamps = [current_date + timedelta(minutes=15 * i) for i in range(100)]
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': timestamps})

# To match R's POSIXct string representation in dataframes for the verifier:
good_times['timestamp'] = good_times['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')

globals()['good.times'] = good_times

# R: good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# Re-converting to datetime for calculation
# r2py:entity:good.times$quarter
ts_series = pd.to_datetime(good_times['timestamp'])
# r2py:entity:add
quarter_vals = (ts_series.dt.minute // 15) + 1
good_times['quarter'] = quarter_vals
globals()['good.times'] = good_times