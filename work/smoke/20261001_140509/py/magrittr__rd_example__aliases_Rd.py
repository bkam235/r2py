# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_140509/py/magrittr__rd_example__aliases_Rd.py'
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
d = pd.DataFrame(np.load('iris.data') if False else None) # Using pandas built-in iris equivalent
from sklearn.datasets import load_iris
iris_data = load_iris()
d = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
print(d.head())

# good.times <- Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.Timestamp(datetime.now().date())
# r2py:entity:data.frame
good_times = pd.DataFrame({
# r2py:entity:seq
    'timestamp': pd.date_range(start=start_date, periods=100, freq='15min')
})

# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# r2py:entity:good.times$quarter
good_times['quarter'] = (
# r2py:entity:add
    good_times['timestamp'].dt.minute // 15 + 1
)