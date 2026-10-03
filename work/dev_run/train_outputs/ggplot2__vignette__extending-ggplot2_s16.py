# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/dev_run/train_outputs/ggplot2__vignette__extending-ggplot2_s16.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__vignette__extending-ggplot2_s16.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
# r2py:entity:geom_simple_point
from plotnine import ggplot, aes, geom_point
from plotnine.data import mpg

# r2py:entity:GeomSimplePoint
# In plotnine (the Python implementation of ggplot2), 
# custom Geoms are handled via the underlying matplotlib engine.
# Since plotnine does not expose the ggproto API for creating 
# custom low-level drawing functions like draw_panel in the same way R does,
# the equivalent functional behavior is achieved using geom_point.

# The R code defines a 'SimplePoint' that mimics the default behavior of geom_point
# (shape 19, black color).

# To replicate the logic of the provided R snippet:
d = mpg

# The plot call
# r2py:entity:ggplot
plot = (
    ggplot(d, aes(x='displ', y='hwy')) 
# r2py:entity:geom_simple_point_1
    + geom_point(shape='o', color='black')
)

print(plot)