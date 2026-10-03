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

# Convert shimmed data to DataFrames
iris = pd.DataFrame(iris)

# Section 1: Iris extract
# iris %>% extract(, 1:4) %>% head
# extract is [], 1:4 in R is 0:4 in Python slicing
# r2py:entity:extract
extract_result = iris.iloc[:, 0:4].head()
print(extract_result)

# Section 2: good.times generation
# Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.Timestamp.now().normalize()
# r2py:entity:seq
good_times_seq = [start_date + timedelta(minutes=15 * i) for i in range(100)]
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': good_times_seq})

# Section 3: quarter calculation
# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# use_series is $, divide_by_int is //, add is +
# r2py:entity:good.times$quarter
minutes = good_times['timestamp'].dt.minute
# r2py:entity:add
good_times['quarter'] = (minutes // 15) + 1