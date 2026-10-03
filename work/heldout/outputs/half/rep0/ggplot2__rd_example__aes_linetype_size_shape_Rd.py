# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 32

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/half/rep0/ggplot2__rd_example__aes_linetype_size_shape_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__aes_linetype_size_shape_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['economics', 'economics_long', 'mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Setup data
# r2py:entity:df
df = pd.DataFrame({'x': range(1, 11), 'y': range(1, 11)})

# Basic lines
# r2py:entity:p
p = ggplot(df, aes('x', 'y'))
# r2py:entity:geom_line
p + geom_line(linetype=2)
# r2py:entity:geom_line_1
p + geom_line(linetype="dotdash")
# r2py:entity:geom_line_2
p + geom_line(linetype="3313")

# Mapping line type from a grouping variable
# Convert dict to DataFrame first
economics_long_df = pd.DataFrame(economics_long)
# r2py:entity:ggplot
ggplot(economics_long_df, aes('date', 'value01')) + \
# r2py:entity:geom_line_3
  geom_line(aes(linetype='variable'))

# Linewidth examples
economics_df = pd.DataFrame(economics)
# r2py:entity:ggplot_1
ggplot(economics_df, aes('date', 'unemploy')) + \
# r2py:entity:geom_line_4
  geom_line(size=2) 

# r2py:entity:ggplot_2
ggplot(economics_df, aes('date', 'unemploy')) + \
# r2py:entity:geom_line_5
  geom_line(aes(size='uempmed'))

# Size examples
mtcars_df = pd.DataFrame(mtcars)
# r2py:entity:p_1
p = ggplot(mtcars_df, aes('wt', 'mpg'))
# r2py:entity:geom_point
p + geom_point(size=4)
# r2py:entity:geom_point_1
p + geom_point(aes(size='qsec'))
# r2py:entity:geom_point_2
p + geom_point(size=2.5) + \
# r2py:entity:geom_hline
  geom_hline(yintercept=25, size=3.5)

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
# r2py:entity:geom_point_8
mtcars_df['cyl_factor'] = mtcars_df['cyl'].astype(str)
p + geom_point(aes(shape='cyl_factor'))

# A look at all 25 symbols
# r2py:entity:df2
df2 = pd.DataFrame({'x': np.tile(range(1, 6), 5), 'y': range(1, 26), 'z': range(1, 26)})
# r2py:entity:p_2
p = ggplot(df2, aes('x', 'y'))
# r2py:entity:geom_point_9
p + geom_point(aes(shape='z'), size=4) + \
# r2py:entity:scale_shape_identity
  scale_shape_identity()
# r2py:entity:geom_point_10
p + geom_point(aes(shape='z'), size=4, colour="Red") + \
# r2py:entity:scale_shape_identity_1
  scale_shape_identity()
# r2py:entity:geom_point_11
p + geom_point(aes(shape='z'), size=4, colour="Red", fill="Black") + \
# r2py:entity:scale_shape_identity_2
  scale_shape_identity()