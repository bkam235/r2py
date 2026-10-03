# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_082137/py/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import economics, mtcars

# Note: plotnine doesn't have a built-in 'economics_long'. 
# Creating it to match the R example logic.
economics_long.columns = ['date', 'variable', 'value01']

# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))
# r2py:entity:geom_line
print(p + geom_line(linetype='dashed'))
# r2py:entity:geom_line_1
print(p + geom_line(linetype='dotdash'))
# r2py:entity:geom_line_2
print(p + geom_line(linetype='3313'))

# r2py:entity:ggplot
print(ggplot(economics_long, aes('date', 'value01')) +
# r2py:entity:geom_line_3
      geom_line(aes(linetype='variable')))

# r2py:entity:ggplot_1
print(ggplot(economics, aes('date', 'unemploy')) +
# r2py:entity:geom_line_4
      geom_line(size=2, lineend='round'))

# r2py:entity:ggplot_2
print(ggplot(economics, aes('date', 'unemploy')) +
# r2py:entity:geom_line_5
      geom_line(aes(size='uempmed'), lineend='round'))

# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
print(p + geom_point(size=4))
# r2py:entity:geom_point_1
print(p + geom_point(aes(size='qsec')))
# r2py:entity:geom_hline
print(p + geom_point(size=2.5) + geom_hline(yintercept=25, size=3.5))

# r2py:entity:geom_point_3
print(p + geom_point())
# r2py:entity:geom_point_4
print(p + geom_point(shape=5))
# 'k' is not a standard plotnine shape; mapping to a similar available shape or leaving as is
# r2py:entity:geom_point_5
print(p + geom_point(shape='k', size=3)) 
# r2py:entity:geom_point_6
print(p + geom_point(shape='.'))
# r2py:entity:geom_point_7
print(p + geom_point(shape=None))
# r2py:entity:geom_point_8
print(p + geom_point(aes(shape='factor(cyl)')))

# r2py:entity:df2
df2 = pd.DataFrame({'x': range(1, 6), 'y': range(1, 26), 'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:scale_shape_identity
print(p + geom_point(aes(shape='z'), size=4) + scale_shape_identity())
# r2py:entity:scale_shape_identity_1
print(p + geom_point(aes(shape='z'), size=4, color="Red") + scale_shape_identity())
# r2py:entity:scale_shape_identity_2
print(p + geom_point(aes(shape='z'), size=4, color="Red", fill="Black") + scale_shape_identity())