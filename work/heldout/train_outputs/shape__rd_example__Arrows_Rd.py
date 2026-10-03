# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 51

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__Arrows_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__Arrows_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi', 'x', 'x0', 'x1', 'y0', 'y1']:
#     if _r2py_shim_n in _r2py_shim_data:
# r2py:entity:y1_3
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# Since 'shape.Arrows' is a specialized R function for vector field visualization 
# with custom head shapes (curved, circle, ellipse, T), 
# we implement a helper to create these as dataframes for plotnine/matplotlib.
# r2py:entity:Arrows
def create_arrow_df(x0, y0, x1, y1, arr_type='triangle', arr_length=0.2, colors=None):
    df_list = []
    for i in range(len(x0)):
        # Line segment
        seg = pd.DataFrame({'x': [x0[i], x1[i]], 'y': [y0[i], y1[i]], 'group': [i, i]})
        
        # Approximate arrow heads
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        
        # Head geometry approximation
        if arr_type == 'triangle':
            vx, vy = -uy, ux
            head = pd.DataFrame({
                'x': [x1[i], x1[i] - arr_length*ux + 0.2*vx, x1[i] - arr_length*ux - 0.2*vx],
                'y': [y1[i], y1[i] - arr_length*uy + 0.2*vy, y1[i] - arr_length*uy - 0.2*vy],
                'group': [i, i, i]
            })
        elif arr_type == 'curved' or arr_type == 'circle' or arr_type == 'ellipse':
            # Approximated as a small circle/arc at the tip
            theta = np.linspace(0, np.pi, 10)
            vx, vy = -uy, ux
            head = pd.DataFrame({
                'x': x1[i] + arr_length * np.cos(theta)*ux + 0.1 * np.sin(theta)*vx,
                'y': y1[i] + arr_length * np.sin(theta)*uy + 0.1 * np.sin(theta)*vy,
                'group': [i] * 10
            })
        elif arr_type == 'T':
            vx, vy = -uy, ux
            head = pd.DataFrame({
                'x': [x1[i] - arr_length*ux - 0.2*vx, x1[i] - arr_length*ux + 0.2*vx],
                'y': [y1[i] - arr_length*uy - 0.2*vy, y1[i] - arr_length*uy + 0.2*vy],
                'group': [i, i]
            })
        else:
            head = pd.DataFrame()
            
        df_list.append(seg)
        df_list.append(head)
    return pd.concat(df_list)

# r2py:entity:xlim
xlim = [-5, 5]
# r2py:entity:ylim
ylim = [-10, 10]

# Plot 1
# r2py:entity:runif_1
d1 = create_arrow_df(x0, y0, x1, y1, arr_type='curved')
p1 = (ggplot() + geom_line(aes(x='x', y='y', group='group'), data=d1) + 
      xlim(xlim[0], xlim[1]) + ylim(ylim[0], ylim[1]) + 
      ggtitle("Arrows, type = 'curved'"))
print(p1)

# r2py:entity:plot_1
# Plot 2
# r2py:entity:Arrows_1
d2 = create_arrow_df(x0, y0, x1, y1, arr_type='circle', arr_length=0.2)
p2 = (ggplot() + geom_line(aes(x='x', y='y', group='group'), data=d2, color='grey') + 
      xlim(xlim[0], xlim[1]) + ylim(ylim[0], ylim[1]) + 
      ggtitle("Arrows, type = 'circle'"))
print(p2)

# r2py:entity:plot_2
# Plot 3
# r2py:entity:Arrows_2
d3 = create_arrow_df(x0, y0, x1, y1, arr_type='ellipse', arr_length=0.2)
p3 = (ggplot() + geom_line(aes(x='x', y='y', group='group'), data=d3, color='grey') + 
      xlim(xlim[0], xlim[1]) + ylim(ylim[0], ylim[1]) + 
      ggtitle("Arrows, type = 'ellipse'"))
print(p3)

# Plot 4
# r2py:entity:xd
xd = x + 0.025
# r2py:entity:Arrows_3
d4 = create_arrow_df(x, np.sin(x), xd, np.sin(xd), arr_type='triangle', arr_length=0.5)
# r2py:entity:curve
p4 = (ggplot() + geom_line(aes(x=np.linspace(0, 2*np.pi+0.25, 100), y=np.sin(np.linspace(0, 2*np.pi+0.25, 100)))) + 
      geom_line(aes(x='x', y='y', group='group'), data=d4) + 
      ggtitle("Arrows"))
print(p4)

# Plot 5
# r2py:entity:xx
xx = np.linspace(0, 10*np.pi, 1000)
x_curve = np.sin(xx) * xx
y_curve = np.cos(xx) * xx
# r2py:entity:x_1
x_pts = np.linspace(0, 10*np.pi, 20)
# r2py:entity:x1_2
x1_pts = np.sin(x_pts) * x_pts
# r2py:entity:y1_2
y1_pts = np.cos(x_pts) * x_pts
# r2py:entity:xd_1
xd_pts = x_pts + 0.01
# r2py:entity:x2
x2_pts = np.sin(xd_pts) * xd_pts
# r2py:entity:y2
y2_pts = np.cos(xd_pts) * xd_pts
# r2py:entity:Arrows_4
d5 = create_arrow_df(x1_pts, y1_pts, x2_pts, y2_pts, arr_type='curved', arr_length=0.4)
p5 = (ggplot() + geom_line(aes(x=x_curve, y=y_curve)) + 
      geom_line(aes(x='x', y='y', group='group'), data=d5) + 
      labs(x="", y="") + ggtitle("Arrows, type = 'curved'"))
print(p5)

# r2py:entity:plot_4
# Plot 6
# r2py:entity:Arrows_5
d6 = create_arrow_df(x1_pts, y1_pts, x2_pts, y2_pts, arr_type='T', arr_length=0.4)
p6 = (ggplot() + geom_line(aes(x=x_curve, y=y_curve)) + 
      geom_line(aes(x='x', y='y', group='group'), data=d6, size=1) + 
      labs(x="", y="") + ggtitle("Arrows, type = 'T'"))
print(p6)

# Plot 7 (xpd=TRUE equivalent)
# r2py:entity:xlim_1
xlim = [-5, 5]
# r2py:entity:ylim_1
ylim = [-10, 10]
# r2py:entity:Arrows_6
d7 = create_arrow_df(x0, y0, x1, y1, arr_type='curved')
p7 = (ggplot() + geom_line(aes(x='x', y='y', group='group'), data=d7) + 
      xlim(xlim[0], xlim[1]) + ylim(ylim[0], ylim[1]) + 
      ggtitle("Arrows, type = 'curved'"))
print(p7)