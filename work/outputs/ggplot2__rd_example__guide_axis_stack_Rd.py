# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__guide_axis_stack_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__guide_axis_stack_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import mpg

# r2py:entity:p
p = (
# r2py:entity:ggplot
    ggplot(mpg, aes(x='displ', y='hwy')) 
# r2py:entity:geom_point
    + geom_point() 
# r2py:entity:theme
    + theme(axis_line=element_line())
)

# Note: plotnine does not currently have a direct equivalent to guide_axis_stack.
# The following renders the base plot with the specified theme.
# r2py:entity:guides
print(p)