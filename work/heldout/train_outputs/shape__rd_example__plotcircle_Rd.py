# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__plotcircle_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__plotcircle_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# r2py:entity:plotcircle
def get_circle_data(mid, r, from_rad, to_rad, arrow=False, arr_pos=0.5):
    t = np.linspace(from_rad, to_rad, 100)
    x = mid[0] + r * np.cos(t)
    y = mid[1] + r * np.sin(t)
    df = pd.DataFrame({'x': x, 'y': y})
    if arrow:
        # Calculate point at arr_pos (relative to arc length)
        idx = int(len(t) * arr_pos)
        # Simple arrow head approximation using a point or custom logic
        # Plotnine handles lines; arrow heads are typically handled by matplotlib
        pass 
    return df

# r2py:entity:plotellipse
def get_ellipse_data(mid, rx, ry, arrow=False, arr_pos=0.5):
    t = np.linspace(0, 2 * np.pi, 100)
    x = mid[0] + rx * np.cos(t)
    y = mid[1] + ry * np.sin(t)
    df = pd.DataFrame({'x': x, 'y': y})
    return df

# First Plot
# r2py:entity:plotcircle
d1_red = get_circle_data(mid=(0.5, 0.5), r=0.25, from_rad=0, to_rad=3*np.pi/2)
# r2py:entity:plotellipse
d1_blue = get_ellipse_data(mid=(0.5, 0.5), rx=0.2, ry=0.2)
d1_red['color'] = 'red'
d1_blue['color'] = 'blue'
d1 = pd.concat([d1_red, d1_blue])

# r2py:entity:emptyplot
p1 = (ggplot(d1, aes('x', 'y', color='color')) 
      + geom_path() 
      + scale_color_identity() 
      + coord_fixed() 
      + xlim(0, 1) + ylim(0, 1) 
      + theme_void())
print(p1)

# Second Plot
# r2py:entity:plotcircle_1
d2_red = get_circle_data(mid=(0.5, 0.5), r=0.25, from_rad=0, to_rad=3*np.pi/2)
# r2py:entity:plotellipse_1
d2_blue = get_ellipse_data(mid=(0.5, 0.5), rx=0.25, ry=0.25)
d2_red['color'] = 'red'
d2_blue['color'] = 'blue'
d2 = pd.concat([d2_red, d2_blue])

# r2py:entity:emptyplot_1
p2 = (ggplot(d2, aes('x', 'y', color='color')) 
      + geom_path() 
      + scale_color_identity() 
      + labs(title="plotcircle") 
      + xlim(0, 1) + ylim(0, 2) 
      + theme_minimal())
print(p2)