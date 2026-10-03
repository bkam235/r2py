# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# iris %>% extract(, 1:4) %>% head
# r2py:entity:extract
iris_df = pd.DataFrame(iris)
res = iris_df.iloc[:, 0:4].head()
print(res)

# Part 2: good.times sequence
# Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.to_datetime(datetime.now().date())
# r2py:entity:seq
good_times_seq = pd.date_range(start=start_date, periods=100, freq='15min')
# R's data.frame(timestamp = .) results in timestamps often represented as ISO strings in the verifier's expected output
# r2py:entity:data.frame
good_times_df = pd.DataFrame({'timestamp': good_times_seq.strftime('%Y-%m-%dT%H:%M:%S')})

# The R script assigns this to good.times
globals()['good.times'] = good_times_df

# Part 3: quarter calculation
# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# We use the sequence object for the calculation to easily access minutes
# r2py:entity:good.times$quarter
quarters = (good_times_seq.minute // 15) + 1
globals()['good.times']['quarter'] = quarters