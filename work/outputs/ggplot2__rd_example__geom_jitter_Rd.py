# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__geom_jitter_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__geom_jitter_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:p
from plotnine import ggplot, aes, geom_point, geom_jitter
from plotnine.data import mpg

p = ggplot(mpg, aes('cyl', 'hwy'))
# r2py:entity:geom_point
p + geom_point()
# r2py:entity:geom_jitter
p + geom_jitter()

# r2py:entity:geom_jitter_1
p + geom_jitter(aes(colour='class'))

# r2py:entity:geom_jitter_2
ggplot(mpg, aes('cyl', 'hwy')) + geom_jitter()
# r2py:entity:geom_jitter_3
ggplot(mpg, aes('cyl', 'hwy')) + geom_jitter(width=0.25)

# r2py:entity:geom_jitter_4
ggplot(mpg, aes('cty', 'hwy')) + geom_jitter()
# r2py:entity:geom_jitter_5
ggplot(mpg, aes('cty', 'hwy')) + geom_jitter(width=0.5, height=0.5)