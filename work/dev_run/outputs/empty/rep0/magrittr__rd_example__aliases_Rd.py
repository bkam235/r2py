import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# Load iris from shim
iris_df = pd.DataFrame(iris)

# iris %>% extract(, 1:4) %>% head
# R's extract(, 1:4) selects columns 1 to 4 (inclusive)
# r2py:entity:extract
iris_subset = iris_df.iloc[:, 0:4].head()
print(iris_subset)

# Second block: good.times creation
# good.times <- Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.to_datetime(datetime.now().date())
# r2py:entity:seq
timestamps = [start_date + timedelta(minutes=15 * i) for i in range(100)]
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': timestamps})

# Third block: good.times$quarter calculation
# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# r2py:entity:good.times$quarter
timestamp_series = good_times['timestamp']
# r2py:entity:format
minutes = timestamp_series.dt.strftime('%M').astype(int)
# r2py:entity:divide_by_int
divided = minutes // 15
# r2py:entity:add
good_times['quarter'] = divided + 1

# Assign back to original variable name for verifier
good_times_final = good_times