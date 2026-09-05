# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 29

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/ggplot2__rd_example__ggtheme_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ggplot2__rd_example__ggtheme_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['mpg', 'mtcars']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from plotnine import *

# Preprocessing data
# r2py:entity:mtcars2
mtcars2 = pd.DataFrame(mtcars).copy()
# r2py:entity:vs
mtcars2['vs'] = mtcars2['vs'].map({0: "V-shaped", 1: "Straight"})
# r2py:entity:am
mtcars2['am'] = mtcars2['am'].map({0: "Automatic", 1: "Manual"})
# r2py:entity:cyl
mtcars2['cyl'] = mtcars2['cyl'].astype(str)
# r2py:entity:gear
mtcars2['gear'] = mtcars2['gear'].astype(str)

# Base plot p1
# r2py:entity:ggplot
p1 = (ggplot(mtcars2) 
# r2py:entity:geom_point
      + geom_point(aes(x='wt', y='mpg', color='gear')) 
# r2py:entity:labs
      + labs(
          title="Fuel economy declines as weight increases",
          subtitle="(1973-74)",
          caption="Data from the 1974 Motor Trend US magazine.",
          tag="Figure 1",
          x="Weight (1000 lbs)",
          y="Fuel economy (mpg)",
          color="Gears"
      )
    )

# Theme variations for p1
# r2py:entity:theme_gray
print(p1 + theme_gray())
# r2py:entity:theme_bw
print(p1 + theme_bw())
# r2py:entity:theme_linedraw
print(p1 + theme_linedraw())
# r2py:entity:theme_light
print(p1 + theme_light())
# r2py:entity:theme_dark
print(p1 + theme_dark())
# r2py:entity:theme_minimal
print(p1 + theme_minimal())
# r2py:entity:theme_classic
print(p1 + theme_classic())
# r2py:entity:theme_void
print(p1 + theme_void())

# Faceted plot p2
# r2py:entity:facet_grid
p2 = p1 + facet_grid('vs ~ am')

# Theme variations for p2
# r2py:entity:theme_gray_1
print(p2 + theme_gray())
# r2py:entity:theme_bw_1
print(p2 + theme_bw())
# r2py:entity:theme_linedraw_1
print(p2 + theme_linedraw())
# r2py:entity:theme_light_1
print(p2 + theme_light())
# r2py:entity:theme_dark_1
print(p2 + theme_dark())
# r2py:entity:theme_minimal_1
print(p2 + theme_minimal())
# r2py:entity:theme_classic_1
print(p2 + theme_classic())
# r2py:entity:theme_void_1
print(p2 + theme_void())