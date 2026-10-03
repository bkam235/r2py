# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load iris dataset (using pandas' built-in or similar source)
# Assuming a standard iris dataframe is available
from sklearn.datasets import load_iris
iris_data = load_iris()

# iris %>% extract(, 1:4) %>% head
# r2py:entity:extract
iris = pd.DataFrame(iris)
iris = iris.iloc[:, 0:4]
# r2py:entity:Sys.Date
start_date = pd.Timestamp(datetime.now().date())
# r2py:entity:data.frame
good_times = pd.DataFrame({
# r2py:entity:seq
    'timestamp': pd.date_range(start=start_date, periods=100, freq='15min')
})

# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") ...
# Extracts minutes, divides by 15, and adds 1
# r2py:entity:good.times$quarter
good_times['quarter'] = (
# r2py:entity:add
    good_times['timestamp'].dt.minute // 15 + 1
).astype(int)