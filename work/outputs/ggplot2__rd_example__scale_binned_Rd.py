# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__scale_binned_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__scale_binned_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from plotnine import ggplot, aes, geom_histogram

# Convert shim data to DataFrame
mtcars_df = pd.DataFrame(mtcars)

# In R, ggplot(mtcars) + geom_bar(aes(mpg)) + scale_x_binned() 
# creates a histogram by binning the continuous 'mpg' variable.
# In plotnine, the equivalent is geom_histogram().
plot = (
# r2py:entity:ggplot
    ggplot(mtcars_df) 
# r2py:entity:geom_bar
    + geom_histogram(mapping=aes(x='mpg'))
)

print(plot)