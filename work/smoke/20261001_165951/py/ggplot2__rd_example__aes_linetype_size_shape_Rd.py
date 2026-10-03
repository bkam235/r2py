# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/smoke/20261001_165951/py/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
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

# Setup data
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

# An example with hex strings
# r2py:entity:geom_line_2
p_line3 = p + geom_line(linetype="3313")
print(p_line3)

# Mapping line type from a grouping variable
# r2py:entity:ggplot
p_economics = (ggplot(economics_long, aes('date', 'value01')) +
# r2py:entity:geom_line_3
  geom_line(aes(linetype='variable')))
print(p_economics)

# Linewidth examples
# r2py:entity:ggplot_1
p_econ_width1 = (ggplot(economics, aes('date', 'unemploy')) +
# r2py:entity:geom_line_4
  geom_line(size=2))
print(p_econ_width1)
# r2py:entity:ggplot_2
p_econ_width2 = (ggplot(economics, aes('date', 'unemploy')) +
# r2py:entity:geom_line_5
  geom_line(aes(size='uempmed')))
print(p_econ_width2)

# Size examples
# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
p_point1 = p + geom_point(size=4)
print(p_point1)
# r2py:entity:geom_point_1
p_point2 = p + geom_point(aes(size='qsec'))
print(p_point2)
# r2py:entity:geom_point_2
p_point3 = (p + geom_point(size=2.5) +
# r2py:entity:geom_hline
  geom_hline(yintercept=25, size=3.5))
print(p_point3)

# Shape examples
# r2py:entity:geom_point_3
p_point4 = p + geom_point()
print(p_point4)
# r2py:entity:geom_point_4
p_point5 = p + geom_point(shape=5)
print(p_point5)
# r2py:entity:geom_point_5
p_point6 = p + geom_point(shape="k", size=3)
print(p_point6)
# r2py:entity:geom_point_6
p_point7 = p + geom_point(shape=".")
print(p_point7)
# r2py:entity:geom_point_7
p_point8 = p + geom_point(shape=None)
print(p_point8)

# Create a copy to avoid mutating the shim data for factor conversion
mtcars_copy = mtcars.copy()
mtcars_copy['cyl_factor'] = mtcars_copy['cyl'].astype(str)
p_mtcars_factor = ggplot(mtcars_copy, aes('wt', 'mpg'))
# r2py:entity:geom_point_8
p_point9 = p_mtcars_factor + geom_point(aes(shape='cyl_factor'))
print(p_point9)

# A look at all 25 symbols
# r2py:entity:df2
df2 = pd.DataFrame({'x': np.tile(range(1, 6), 5), 
                    'y': range(1, 26), 
                    'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:geom_point_9
p_symbols1 = (p + geom_point(aes(shape='z'), size=4) +
# r2py:entity:scale_shape_identity
  scale_shape_identity())
print(p_symbols1)

# While all symbols have a foreground colour, symbols 19-25 also take a
# background colour (fill)
# r2py:entity:geom_point_10
p_symbols2 = (p + geom_point(aes(shape='z'), size=4, colour="Red") +
# r2py:entity:scale_shape_identity_1
  scale_shape_identity())
print(p_symbols2)
# r2py:entity:geom_point_11
p_symbols3 = (p + geom_point(aes(shape='z'), size=4, colour="Red", fill="Black") +
# r2py:entity:scale_shape_identity_2
  scale_shape_identity())
print(p_symbols3)