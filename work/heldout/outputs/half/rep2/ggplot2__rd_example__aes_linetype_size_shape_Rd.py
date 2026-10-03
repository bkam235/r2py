# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep2/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Convert data shim dicts to DataFrames
economics = pd.DataFrame(economics)
economics_long = pd.DataFrame(economics_long)
mtcars = pd.DataFrame(mtcars)

# Initial data frame and line plots
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))
# R linetype 2 is 'dashed'
# r2py:entity:geom_line
(p + geom_line(linetype='dashed'))
# R 'dotdash' is 'dashdot' in matplotlib/plotnine
# r2py:entity:geom_line_1
(p + geom_line(linetype='dashdot'))
# R hex string '3313' is not directly supported as a string in plotnine's geom_line
# but plotnine accepts tuples for dash patterns: (offset, (on, off, on, off...))
# '3313' -> (3, 3, 1, 3)
# r2py:entity:geom_line_2
(p + geom_line(linetype=(3, 3, 1, 3)))

# Mapping line type from a grouping variable
# r2py:entity:ggplot
(ggplot(economics_long, aes('date', 'value01')) + 
# r2py:entity:geom_line_3
  geom_line(aes(linetype='variable')))

# Linewidth examples
# plotnine uses 'size' for both points and lines
# r2py:entity:ggplot_1
(ggplot(economics, aes('date', 'unemploy')) + 
# r2py:entity:geom_line_4
  geom_line(size=2, lineend='round'))
# r2py:entity:ggplot_2
(ggplot(economics, aes('date', 'unemploy')) + 
# r2py:entity:geom_line_5
  geom_line(aes(size='uempmed'), lineend='round'))

# Size examples
# r2py:entity:p_1
p = ggplot(mtcars, aes('wt', 'mpg'))
# r2py:entity:geom_point
(p + geom_point(size=4))
# r2py:entity:geom_point_1
(p + geom_point(aes(size='qsec')))
# r2py:entity:geom_hline
(p + geom_point(size=2.5) + geom_hline(yintercept=25, size=3.5))

# Shape examples
# r2py:entity:geom_point_3
(p + geom_point())
# r2py:entity:geom_point_4
(p + geom_point(shape=5))
# r2py:entity:geom_point_5
(p + geom_point(shape='k', size=3))
# r2py:entity:geom_point_6
(p + geom_point(shape='.'))
# r2py:entity:geom_point_7
(p + geom_point(shape=None))
# r2py:entity:geom_point_8
(p + geom_point(aes(shape='factor(cyl)')))

# A look at all 25 symbols
# r2py:entity:df2
df2 = pd.DataFrame({'x': np.tile(range(1, 6), 5), 
                    'y': range(1, 26), 
                    'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:geom_point_9
(p + geom_point(aes(shape='z'), size=4) + 
# r2py:entity:scale_shape_identity
  scale_shape_identity())
# r2py:entity:geom_point_10
(p + geom_point(aes(shape='z'), size=4, colour='Red') + 
# r2py:entity:scale_shape_identity_1
  scale_shape_identity())
# r2py:entity:geom_point_11
(p + geom_point(aes(shape='z'), size=4, colour='Red', fill='Black') + 
# r2py:entity:scale_shape_identity_2
  scale_shape_identity())