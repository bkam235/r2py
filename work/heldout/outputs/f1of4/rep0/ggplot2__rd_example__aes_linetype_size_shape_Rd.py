# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/f1of4/rep0/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Convert shim data to DataFrames
economics = pd.DataFrame(economics)
economics_long = pd.DataFrame(economics_long)
mtcars = pd.DataFrame(mtcars)

# Setup first dataframe
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))
# r2py:entity:geom_line
p + geom_line(linetype='dashed')
# r2py:entity:geom_line_1
p + geom_line(linetype='dotdash')
# r2py:entity:geom_line_2
p + geom_line(linetype='3313')

# Mapping line type from a grouping variable
# r2py:entity:geom_line_3
ggplot(economics_long, aes('date', 'value01')) + geom_line(aes(linetype='variable'))

# Linewidth examples - plotnine uses 'size' for line width
# r2py:entity:geom_line_4
ggplot(economics, aes('date', 'unemploy')) + geom_line(size=2, lineend='round')
# r2py:entity:geom_line_5
ggplot(economics, aes('date', 'unemploy')) + geom_line(aes(size='uempmed'), lineend='round')

# mtcars analysis
# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
p + geom_point(size=4)
# r2py:entity:geom_point_1
p + geom_point(aes(size='qsec'))
# r2py:entity:geom_hline
p + geom_point(size=2.5) + geom_hline(yintercept=25, size=3.5)

# Shape examples
# r2py:entity:geom_point_3
p + geom_point()
# r2py:entity:geom_point_4
p + geom_point(shape=5)
# r2py:entity:geom_point_5
p + geom_point(shape='k', size=3) 
# r2py:entity:geom_point_6
p + geom_point(shape='.')
# r2py:entity:geom_point_7
p + geom_point(shape=None)
# Convert cyl to factor for shape mapping without modifying original mtcars
# r2py:entity:geom_point_8
p + geom_point(aes(shape='factor(cyl)'))

# Custom shapes with identity scale
# R: data.frame(x = 1:5 , y = 1:25, z = 1:25)
# This results in x being recycled: 1,2,3,4,5,1,2,3,4,5...
# r2py:entity:df2
df2 = pd.DataFrame({
    'x': list(range(1, 6)) * 5,
    'y': range(1, 26),
    'z': range(1, 26)
})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:scale_shape_identity
p + geom_point(aes(shape='z'), size=4) + scale_shape_identity()
# r2py:entity:scale_shape_identity_1
p + geom_point(aes(shape='z'), size=4, colour='red') + scale_shape_identity()
# r2py:entity:scale_shape_identity_2
p + geom_point(aes(shape='z'), size=4, colour='red', fill='black') + scale_shape_identity()