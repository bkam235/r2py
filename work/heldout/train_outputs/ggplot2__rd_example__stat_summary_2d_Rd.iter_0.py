# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ggplot2__rd_example__stat_summary_2d_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__stat_summary_2d_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['diamonds']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import diamonds

# Base plot object
# r2py:entity:d
d = ggplot(diamonds, aes(x='carat', y='depth', z='price'))

# stat_summary_2d() default (mean)
# plotnine uses geom_bin2d or stat_summary_2d equivalent logic via stat_summary_bin2d
# r2py:entity:stat_summary_2d
p1 = d + stat_summary_bin2d()
print(p1)

# stat_summary_2d(fun = \(x) sum(x^2))
# r2py:entity:stat_summary_2d_1
p2 = d + stat_summary_bin2d(fun=lambda x: np.sum(x**2))
print(p2)

# stat_summary_2d(fun = ~ sum(.x^2))
# r2py:entity:stat_summary_2d_2
p3 = d + stat_summary_bin2d(fun=lambda x: np.sum(x**2))
print(p3)

# stat_summary_2d(fun = var)
# r2py:entity:stat_summary_2d_3
p4 = d + stat_summary_bin2d(fun=np.var)
print(p4)

# stat_summary_2d(fun = "quantile", fun.args = list(probs = 0.1))
# r2py:entity:stat_summary_2d_4
p5 = d + stat_summary_bin2d(fun=lambda x: np.quantile(x, 0.1))
print(p5)

# stat_summary_hex()
# r2py:entity:stat_summary_hex
p6 = d + stat_summary_bin2d(binwidth=None) # plotnine handles hex via geom_hex, but for summary:
# Note: plotnine does not have a direct 'stat_summary_hex', approximating with stat_summary_bin2d
# or geom_hex for density. For summary value:
p6 = d + stat_summary_bin2d() 
print(p6)

# stat_summary_hex(fun = ~ sum(.x^2))
# r2py:entity:stat_summary_hex_1
p7 = d + stat_summary_bin2d(fun=lambda x: np.sum(x**2))
print(p7)