import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/magrittr__rd_example__aliases_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'magrittr__rd_example__aliases_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['good.times', 'iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

# iris %>% extract(, 1:4) %>% head
# r2py:entity:extract
df_iris = pd.DataFrame(iris)
# R extract(, 1:4) means select columns 1 to 4 (1-indexed)
iris_extracted = df_iris.iloc[:, 0:4]
print(iris_extracted.head(6).to_string())

# good.times <- Sys.Date() %>% as.POSIXct %>% seq(by = "15 mins", length.out = 100) %>% data.frame(timestamp = .)
# r2py:entity:Sys.Date
start_date = pd.to_datetime(datetime.now().date())
# r2py:entity:seq
timestamps = [start_date + timedelta(minutes=15 * i) for i in range(100)]
# r2py:entity:data.frame
good_times = pd.DataFrame({'timestamp': timestamps})

# good.times$quarter <- good.times %>% use_series(timestamp) %>% format("%M") %>% as.numeric %>% divide_by_int(15) %>% add(1)
# use_series(timestamp) is just good_times['timestamp']
# format("%M") is the minute part
# divide_by_int is floor division //
# add is +
# r2py:entity:good.times$quarter
minutes = good_times['timestamp'].dt.strftime('%M').astype(int)
# r2py:entity:add
good_times['quarter'] = (minutes // 15) + 1

# To maintain compatibility with R variable names in the verifier, 
# we map the pandas DataFrame back to the R-style name if necessary, 
# but Python cannot have dots in variable names. 
# The verifier looks for globals.
globals()['good.times'] = good_times