# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 37

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/train_outputs/ggplot2__rd_example__geom_dotplot_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__geom_dotplot_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Ensure mtcars is a DataFrame
if not isinstance(mtcars, pd.DataFrame):
    mtcars = pd.DataFrame(mtcars)

# 1
# r2py:entity:ggplot
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot
 + geom_dotplot())
print(plot)

# 2
# r2py:entity:ggplot_1
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_1
 + geom_dotplot(binwidth=1.5))
print(plot)

# 3
# method="histodot" not supported in plotnine
# r2py:entity:ggplot_2
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_2
 + geom_dotplot(binwidth=1.5))
print(plot)

# 4
# stackdir="center" not supported in plotnine
# r2py:entity:ggplot_3
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_3
 + geom_dotplot(binwidth=1.5))
print(plot)

# 5
# stackdir="centerwhole" not supported in plotnine
# r2py:entity:ggplot_4
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_4
 + geom_dotplot(binwidth=1.5))
print(plot)

# 6
# r2py:entity:ggplot_5
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_5
 + geom_dotplot(binwidth=1.5) 
# r2py:entity:scale_y_continuous
 + scale_y_continuous(breaks=[]) + labs(y=None))
print(plot)

# 7
# stackratio not supported in plotnine
# r2py:entity:ggplot_6
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_6
 + geom_dotplot(binwidth=1.5))
print(plot)

# 8
# dotsize not supported in plotnine geom_dotplot
# r2py:entity:ggplot_7
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_7
 + geom_dotplot(binwidth=1.5))
print(plot)

# 9
# stroke not supported in plotnine geom_dotplot
# r2py:entity:ggplot_8
plot = (ggplot(mtcars, aes(x='mpg')) 
# r2py:entity:geom_dotplot_8
 + geom_dotplot(binwidth=1.5, fill="white"))
print(plot)

# 10
# binaxis="y" is approximated by mapping to y and using coord_flip
# r2py:entity:ggplot_9
plot = (ggplot(mtcars, aes(x=1, y='mpg')) 
# r2py:entity:geom_dotplot_9
 + geom_dotplot() 
 + coord_flip())
print(plot)

# 11
mtcars['cyl_f'] = mtcars['cyl'].astype(str)
# r2py:entity:ggplot_10
plot = (ggplot(mtcars, aes(x='cyl_f', y='mpg')) 
# r2py:entity:geom_dotplot_10
 + geom_dotplot() 
 + coord_flip())
print(plot)

# 12
# r2py:entity:ggplot_11
plot = (ggplot(mtcars, aes(x='cyl_f', y='mpg')) 
# r2py:entity:geom_dotplot_11
 + geom_dotplot() 
 + coord_flip())
print(plot)

# 13
mtcars['vs_f'] = mtcars['vs'].astype(str)
# r2py:entity:ggplot_12
plot = (ggplot(mtcars, aes(x='vs_f', y='mpg', fill='cyl_f')) 
# r2py:entity:geom_dotplot_12
 + geom_dotplot(position="dodge") 
 + coord_flip())
print(plot)

# 14
mtcars['am_f'] = mtcars['am'].astype(str)
# r2py:entity:ggplot_13
plot = (ggplot(mtcars, aes(x='am_f', y='mpg')) 
# r2py:entity:geom_dotplot_13
 + geom_dotplot() 
 + coord_flip())
print(plot)

# 15
# stackgroups not supported in plotnine
# r2py:entity:ggplot_14
plot = (ggplot(mtcars, aes(x='mpg', fill='cyl_f')) 
# r2py:entity:geom_dotplot_14
 + geom_dotplot(binwidth=1))
print(plot)

# 16
# r2py:entity:ggplot_15
plot = (ggplot(mtcars, aes(x='mpg', fill='cyl_f')) 
# r2py:entity:geom_dotplot_15
 + geom_dotplot(binwidth=1))
print(plot)

# 17
# r2py:entity:ggplot_16
plot = (ggplot(mtcars, aes(x=1, y='mpg', fill='cyl_f')) 
# r2py:entity:geom_dotplot_16
 + geom_dotplot(binwidth=1) 
 + coord_flip())
print(plot)