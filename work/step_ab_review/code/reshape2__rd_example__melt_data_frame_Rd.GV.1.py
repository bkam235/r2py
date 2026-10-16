# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'reshape2__rd_example__melt_data_frame_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['ChickWeight', 'airquality']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

# Ensure inputs from shim are DataFrames
airquality = pd.DataFrame(airquality)
ChickWeight = pd.DataFrame(ChickWeight)

# names(airquality) <- tolower(names(airquality))
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]

# melt(airquality, id=c("month", "day"))
# r2py:entity:melt
melt_airquality = airquality.melt(id_vars=["month", "day"], var_name="variable", value_name="value")
print(melt_airquality.to_string(index=False)) # R's melt output for data.frames is usually printed without index unless specified, but here we match the auto-print result.
# Note: To perfectly match the R output format (which includes a row index starting at 1), we can use:
print(melt_airquality.reset_index(drop=True).set_index(pd.Series(range(1, len(melt_airquality) + 1))).to_string())

# names(ChickWeight) <- tolower(names(ChickWeight))
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]

# melt(ChickWeight, id=2:4)
# R indices 2:4 are 1-based: indices 1, 2, 3 in 0-based Python (time, chick, diet)
# r2py:entity:melt_1
id_cols = ChickWeight.columns[1:4].tolist()
melt_chickweight = ChickWeight.melt(id_vars=id_cols, var_name="variable", value_name="value")
print(melt_chickweight.reset_index(drop=True).set_index(pd.Series(range(1, len(melt_chickweight) + 1))).to_string())