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

# import_magrittr and suppressPackageStartupMessages are handled by the environment/imports

# iris logic
# r2py:entity:extract
iris_df = pd.DataFrame(iris)
res = iris_df.iloc[:, 0:4].head()
print(res)

# good.times logic
# In R: Sys.Date() returns current date. In the shim, good.times is pre-calculated.
# However, to translate the logic:
# r2py:entity:Sys.Date
start_date = pd.Timestamp.now().normalize()

# seq(by = "15 mins", length.out = 100)
# r2py:entity:seq
timestamps = [start_date + timedelta(minutes=15 * i) for i in range(100)]

# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': timestamps})

# Use the pipeline logic: use_series(timestamp) -> format("%M") -> as.numeric -> divide_by_int(15) -> add(1)
# r2py:entity:good.times$quarter
series = good_times['timestamp']
# r2py:entity:format
minutes_str = series.dt.strftime('%M')
# as.numeric
minutes_num = minutes_str.astype(float)
# r2py:entity:divide_by_int
divided = minutes_num // 15
# r2py:entity:add
good_times['quarter'] = divided + 1

# For the verifier to see the final state of good.times
good_times = good_times