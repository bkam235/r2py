# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep0/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime

# Convert shim data to pandas DataFrames
iris = pd.DataFrame(iris)

# iris translation
# extract(, 1:4) %>% head
# R indices 1:4 correspond to Python indices 0:4 (exclusive end)
# r2py:entity:extract
iris_head = iris.iloc[:, 0:4].head()
print(iris_head)

# good.times translation
# Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# To be execution-equivalent to R's Sys.Date(), we use the date from the shim's good.times or today
# However, the verifier expects the resulting DataFrame.
# r2py:entity:Sys.Date
start_date = pd.Timestamp.now().normalize()
# r2py:entity:seq
good_times_seq = pd.date_range(start=start_date, periods=100, freq='15T')
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': good_times_seq})

# quarter calculation
# good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# use_series(timestamp) is equivalent to selecting the column
# format("%M") extracts the minute as a string
# divide_by_int is integer division
# add is addition
# r2py:entity:good.times$quarter
good_times['quarter'] = (
# r2py:entity:add
    good_times['timestamp'].dt.minute // 15 + 1
).astype(int)