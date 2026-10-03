# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__plotellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__plotellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# r2py:entity:plotellipse
def get_ellipse_data(rx=1, ry=None, mid=(0, 0), dr=0.01, angle=0, from_val=-np.pi, to_val=np.pi):
    if ry is None:
        ry = rx
    
    if to_val < from_val:
        to_val = 2 * np.pi + to_val
    
    t = np.arange(from_val, to_val + dr, dr)
    if len(t) > 1 and t[-1] > to_val:
        t = t[:-1]
    if len(t) > 0:
        t = np.append(t, to_val)
    
    # Remove duplicates if dr is very small
    t = np.unique(t)

    x = mid[0] + rx * np.cos(t)
    y = mid[1] + ry * np.sin(t)
    
    if angle != 0:
        ang_rad = np.radians(angle)
        cosa = np.cos(ang_rad)
        sina = np.sin(ang_rad)
        dx = x - mid[0]
        dy = y - mid[1]
        x = mid[0] + cosa * dx - sina * dy
        y = mid[1] + sina * dx + cosa * dy
        
    return pd.DataFrame({'x': x, 'y': y})

def rainbow(n):
    return [f"rgb({int(255 * (i/n))}, 0, {int(255 * (1 - i/n))})" for i in range(n)] # Approximation

# In plotnine, we build layers. We'll collect all data and plot once to emulate R's plotting.
plot_layers = []
all_data = []

# emptyplot(c(-1, 1), main = "plotellipse")
# r2py:entity:emptyplot
xlim_val = (-1, 1)
ylim_val = (-1, 1)

# 1. plotellipse(rx = 0.8, ry = 0.3, angle = 60, col = "blue")
# r2py:entity:plotellipse
d1 = get_ellipse_data(rx=0.8, ry=0.3, angle=60)
d1['color'] = 'blue'
d1['type'] = 'fill'
all_data.append(d1)

# 2. plotellipse(rx = 1.0, ry = 0.6, angle = 0, from_val= pi, to = 2*pi, arrow = TRUE, ...)
# Python handles arrows better with geom_segment or custom marks, 
# but for a direct translation of the visual result into a dataframe:
# r2py:entity:plotellipse_1
d2 = get_ellipse_data(rx=1.0, ry=0.6, angle=0, from_val=np.pi, to_val=2*np.pi)
d2['color'] = 'black'
d2['type'] = 'line'
all_data.append(d2)
# Arrow positions: seq(0.1, 0.5, by = 0.1) -> 0.1, 0.2, 0.3, 0.4, 0.5
arr_pos = np.arange(0.1, 0.6, 0.1)
arr_cols = rainbow(5)
for pos, col in zip(arr_pos, arr_cols):
    idx = int(len(d2) * pos)
    if idx < len(d2) - 1:
        # Represent arrows as small segments for plotnine
        arrow_df = pd.DataFrame({
            'x': [d2.iloc[idx-1]['x'], d2.iloc[idx]['x']],
            'y': [d2.iloc[idx-1]['y'], d2.iloc[idx]['y']],
            'color': [col, col],
            'type': ['arrow', 'arrow']
        })
        all_data.append(arrow_df)

# 3. plotellipse(rx = 1.0, ry = 0.6, angle = 30, from_val= pi, to = 1.2*pi, col = "red")
# r2py:entity:plotellipse_2
d3 = get_ellipse_data(rx=1.0, ry=0.6, angle=30, from_val=np.pi, to_val=1.2*np.pi)
d3['color'] = 'red'
d3['type'] = 'fill'
all_data.append(d3)

# 4. plotellipse(rx = 0.1, ry = 0.6, from_val= 1.5*pi, to = pi, lcol = "orange", mid = c(0.2,0.2))
# r2py:entity:plotellipse_3
d4 = get_ellipse_data(rx=0.1, ry=0.6, from_val=1.5*np.pi, to_val=np.pi, mid=(0.2, 0.2))
d4['color'] = 'orange'
d4['type'] = 'line'
all_data.append(d4)

# 5. plotellipse(rx = 0.1, ry = 0.6, angle = 30, from_val= 1.5*pi, to = pi, lcol = "orange", mid = c(0.2,0.2))
# r2py:entity:plotellipse_4
d5 = get_ellipse_data(rx=0.1, ry=0.6, angle=30, from_val=1.5*np.pi, to_val=np.pi, mid=(0.2, 0.2))
d5['color'] = 'orange'
d5['type'] = 'line'
all_data.append(d5)

final_df = pd.concat(all_data)

p = (ggplot(final_df, aes('x', 'y', color='color')) 
     + geom_path(data=final_df[final_df['type'] == 'line'])
     + geom_polygon(data=final_df[final_df['type'] == 'fill'], fill='color', color=None)
     + scale_color_identity()
     + coord_fixed() 
     + xlim(xlim_val[0], xlim_val[1]) 
     + ylim(ylim_val[0], ylim_val[1]) 
     + labs(title="plotellipse")
     + theme_void())

print(p)