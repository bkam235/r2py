# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__scale_size_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__scale_size_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
from plotnine import *

# Convert shim dict to DataFrame
mpg_df = pd.DataFrame(mpg)

# Basic plot
# r2py:entity:ggplot
p = (ggplot(mpg_df, aes('displ', 'hwy', size='hwy')) 
# r2py:entity:geom_point
     + geom_point())
# r2py:entity:p_1
print(p)

# Scale size with a label
# r2py:entity:scale_size
print(p + scale_size(name="Highway mpg"))

# Scale size with a specific range
# r2py:entity:scale_size_1
print(p + scale_size(range=(0, 10)))

# Scale size area (maps area to value instead of radius)
# r2py:entity:scale_size_area
print(p + scale_size_area())

# Binning can sometimes make it easier to match the scaled data to the legend
# plotnine does not have scale_size_binned; using scale_size as closest approximation
# r2py:entity:scale_size_binned
print(p + scale_size())

# This is most useful when size is a count
# r2py:entity:ggplot_1
print((ggplot(mpg_df, aes('class', 'cyl')) 
# r2py:entity:geom_count
       + geom_count() 
# r2py:entity:scale_size_area_1
       + scale_size_area()))

# If you want to map size to radius (usually bad idea), use scale_radius
# plotnine does not have scale_radius; using scale_size as closest approximation
# r2py:entity:scale_radius
print(p + scale_size())