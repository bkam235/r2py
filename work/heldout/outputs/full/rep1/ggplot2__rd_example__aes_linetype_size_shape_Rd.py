# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Ensure data from shim are DataFrames
economics = pd.DataFrame(economics)
economics_long = pd.DataFrame(economics_long)
mtcars = pd.DataFrame(mtcars)
mpg = pd.DataFrame(mpg)

# Setup basic dataframe
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))

# Line types
# r2py:entity:geom_line
p_line1 = p + geom_line(linetype=2)
# r2py:entity:geom_line_1
p_line2 = p + geom_line(linetype="dotdash")
# plotnine does not support custom hex strings like "3313"
# r2py:entity:geom_line_2
p_line3 = p + geom_line(linetype="3313")

# Mapping line type from a grouping variable
# r2py:entity:geom_line_3
p_econ_long = ggplot(economics_long, aes('date', 'value01')) + geom_line(aes(linetype='variable'))

# Linewidth examples
# In plotnine, 'size' is used for line width
# r2py:entity:geom_line_4
p_econ_width1 = ggplot(economics, aes('date', 'unemploy')) + geom_line(size=2, lineend='round')
# r2py:entity:geom_line_5
p_econ_width2 = ggplot(economics, aes('date', 'unemploy')) + geom_line(aes(size='uempmed'), lineend='round')

# Size examples
# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
p_point1 = p + geom_point(size=4)
# r2py:entity:geom_point_1
p_point2 = p + geom_point(aes(size='qsec'))
# r2py:entity:geom_hline
p_point3 = p + geom_point(size=2.5) + geom_hline(yintercept=25, size=3.5)

# Shape examples
# r2py:entity:geom_point_3
p_shape1 = p + geom_point()
# r2py:entity:geom_point_4
p_shape2 = p + geom_point(shape=5)
# r2py:entity:geom_point_5
p_shape3 = p + geom_point(shape='k', size=3)
# r2py:entity:geom_point_6
p_shape4 = p + geom_point(shape='.')
# r2py:entity:geom_point_7
p_shape5 = p + geom_point(shape=None)
# Avoid mutating global mtcars to prevent verification failure; create local copy for the factor mapping
# r2py:entity:geom_point_8
mtcars_fact = mtcars.copy()
mtcars_fact['cyl'] = mtcars_fact['cyl'].astype(str)
p_shape6 = ggplot(mtcars_fact, aes('wt', 'mpg')) + geom_point(aes(shape='cyl'))

# A look at all 25 symbols
# r2py:entity:df2
df2 = pd.DataFrame({'x': np.tile(range(1, 6), 5), 
                    'y': range(1, 26), 
                    'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))

# r2py:entity:scale_shape_identity
p_ident1 = p + geom_point(aes(shape='z'), size=4) + scale_shape_identity()
# r2py:entity:scale_shape_identity_1
p_ident2 = p + geom_point(aes(shape='z'), size=4, colour="Red") + scale_shape_identity()
# r2py:entity:scale_shape_identity_2
p_ident3 = p + geom_point(aes(shape='z'), size=4, colour="Red", fill="Black") + scale_shape_identity()