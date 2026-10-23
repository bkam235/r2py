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

# suppressPackageStartupMessages(library(reshape2))
# No direct Python equivalent for suppressPackageStartupMessages; library import handled.

# names(airquality) <- tolower(names(airquality))
# r2py:entity:names(airquality)
airquality.columns = [c.lower() for c in airquality.columns]
names_airquality = airquality.columns.tolist()

# melt(airquality, id=c("month", "day"))
# r2py:entity:melt
melt = airquality.melt(id_vars=["month", "day"], var_name="variable", value_name="value")

# names(ChickWeight) <- tolower(names(ChickWeight))
# r2py:entity:names(ChickWeight)
ChickWeight.columns = [c.lower() for c in ChickWeight.columns]
names_chickweight = ChickWeight.columns.tolist()

# melt(ChickWeight, id=2:4)
# R indices 2:4 are 1-based: indices 1, 2, 3 in 0-based Python
# r2py:entity:melt_1
id_cols = ChickWeight.columns[1:4].tolist()
melt_1 = ChickWeight.melt(id_vars=id_cols, var_name="variable", value_name="value")