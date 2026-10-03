# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_065131/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# The shim provides iris as a dict. Convert to DataFrame.
iris_df = pd.DataFrame(iris)

# iris %>% extract(, 1:4) %>% head
# extract is an alias for [
# In R, 1:4 is 1-indexed. In Python, it's 0:4 for columns 1, 2, 3, 4.
# r2py:entity:extract
res_iris = iris_df.iloc[:, 0:4].head()
print(res_iris)

# good.times part
# Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
now = pd.Timestamp(datetime.now().date())
# r2py:entity:seq
good_times_seq = [now + timedelta(minutes=15 * i) for i in range(100)]
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': good_times_seq})

# quarter calculation
# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% 
#                      as.numeric %>% divide_by_int(15) %>% add(1)

# use_series is alias for $
# r2py:entity:good.times$quarter
series = good_times['timestamp']

# format("%M") extracts minutes as string
# r2py:entity:format
minutes_str = series.dt.strftime('%M')

# as.numeric converts to number
minutes_num = minutes_str.astype(float)

# divide_by_int is alias for %/% (integer division)
# r2py:entity:divide_by_int
divided = minutes_num // 15

# add is alias for +
# r2py:entity:add
good_times['quarter'] = divided + 1