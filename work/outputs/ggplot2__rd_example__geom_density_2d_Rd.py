# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 25

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__geom_density_2d_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__geom_density_2d_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:sample
# for _r2py_shim_n in ['diamonds', 'dsmall', 'faithful']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *
from plotnine.data import faithful, diamonds

# Section 1: Faithful dataset
# r2py:entity:ggplot
m = (ggplot(faithful, aes(x='eruptions', y='waiting')) 
# r2py:entity:geom_point
     + geom_point() 
# r2py:entity:xlim
     + xlim(0.5, 6) 
# r2py:entity:ylim
     + ylim(40, 110))

# r2py:entity:geom_density_2d
print(m + geom_density_2d())

# r2py:entity:geom_density_2d_filled
print(m + geom_density_2d_filled(alpha=0.5))

# r2py:entity:geom_density_2d_filled_1
print((m + geom_density_2d_filled(alpha=0.5) 
# r2py:entity:geom_density_2d_1
      + geom_density_2d(linewidth=0.25, colour="black")))

# Section 2: Diamonds dataset
# r2py:entity:set.seed
np.random.seed(4393)
# r2py:entity:d
d = ggplot(dsmall, aes(x='carat', y='price'))

# r2py:entity:geom_density_2d_2
print(d + geom_density_2d(aes(colour='cut')))

# r2py:entity:facet_wrap
print(d + geom_density_2d_filled() + facet_wrap('cut'))

# r2py:entity:facet_wrap_1
print(d + geom_density_2d_filled(contour_var="ndensity") + facet_wrap('cut'))

# r2py:entity:facet_wrap_2
print(d + geom_density_2d_filled(contour_var="count") + facet_wrap('cut'))

# r2py:entity:scale_fill_viridis_c
print((d + stat_density_2d(aes(fill='density'), geom="raster", contour=False) + scale_fill_viridis_c()))

# r2py:entity:stat_density_2d_1
print(d + stat_density_2d(aes(size='density'), geom="point", n=20, contour=False))