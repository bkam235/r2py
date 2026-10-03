# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_124904/py/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Convert shim dicts to DataFrames
economics = pd.DataFrame(economics)
economics_long = pd.DataFrame(economics_long)
mtcars = pd.DataFrame(mtcars)
mpg = pd.DataFrame(mpg)

# Setup initial data
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))
# r2py:entity:geom_line
p_line1 = p + geom_line(linetype=2)
print(p_line1)
# r2py:entity:geom_line_1
p_line2 = p + geom_line(linetype="dotdash")
print(p_line2)
# r2py:entity:geom_line_2
p_line3 = p + geom_line(linetype="3313")
print(p_line3)

# Mapping line type from a grouping variable
# r2py:entity:geom_line_3
p_econ_long = ggplot(economics_long, aes('date', 'value01')) + geom_line(aes(linetype='variable'))
print(p_econ_long)

# Linewidth examples
# r2py:entity:geom_line_4
p_econ_lw1 = ggplot(economics, aes('date', 'unemploy')) + geom_line(linewidth=2, lineend='round')
print(p_econ_lw1)
# r2py:entity:geom_line_5
p_econ_lw2 = ggplot(economics, aes('date', 'unemploy')) + geom_line(aes(linewidth='uempmed'), lineend='round')
print(p_econ_lw2)

# Size examples
# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
p_point1 = p + geom_point(size=4)
print(p_point1)
# r2py:entity:geom_point_1
p_point2 = p + geom_point(aes(size='qsec'))
print(p_point2)
# r2py:entity:geom_hline
p_point3 = p + geom_point(size=2.5) + geom_hline(yintercept=25, size=3.5)
print(p_point3)

# Shape examples
# r2py:entity:geom_point_3
p_shape1 = p + geom_point()
print(p_shape1)
# r2py:entity:geom_point_4
p_shape2 = p + geom_point(shape=5)
print(p_shape2)
# r2py:entity:geom_point_5
p_shape3 = p + geom_point(shape='k', size=3)
print(p_shape3)
# r2py:entity:geom_point_6
p_shape4 = p + geom_point(shape='.')
print(p_shape4)
# r2py:entity:geom_point_7
p_shape5 = p + geom_point(shape=None)
print(p_shape5)

# R uses factor(cyl), we must transform the column in the df for plotnine
mtcars_fact = mtcars.copy()
mtcars_fact['cyl'] = mtcars_fact['cyl'].astype(str)
p_fact = ggplot(mtcars_fact, aes('wt', 'mpg'))
# r2py:entity:geom_point_8
p_shape6 = p_fact + geom_point(aes(shape='cyl'))
print(p_shape6)

# A look at all 25 symbols
# r2py:entity:df2
df2 = pd.DataFrame({'x': np.tile(range(1, 6), 5), 'y': range(1, 26), 'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:scale_shape_identity
p_ident1 = p + geom_point(aes(shape='z'), size=4) + scale_shape_identity()
print(p_ident1)
# r2py:entity:scale_shape_identity_1
p_ident2 = p + geom_point(aes(shape='z'), size=4, colour="Red") + scale_shape_identity()
print(p_ident2)
# r2py:entity:scale_shape_identity_2
p_ident3 = p + geom_point(aes(shape='z'), size=4, colour="Red", fill="Black") + scale_shape_identity()
print(p_ident3)