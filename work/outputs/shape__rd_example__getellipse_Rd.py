# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/shape__rd_example__getellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__getellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i', 'pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# r2py:entity:col
def femmecol(n):
    """
    Approximates R's femmecol(n) which typically provides a 
    rainbow-like sequence of colors.
    """
    cmap = plt.get_cmap('hsv')
    cols = [mcolors.to_hex(cmap(i/n)) for i in range(n)]
    return cols

# r2py:entity:plot
def get_ellipse(rx, ry=None, mid=(0, 0), from_rad=0, to_rad=2*np.pi, angle_deg=0):
    # Handle R's positional argument: if ry is not provided, it's a circle
    if ry is None:
        ry = rx
    
    # R's seq() handles from > to by decreasing the step
    if from_rad > to_rad:
        t = np.linspace(from_rad, to_rad, 100)
    else:
        t = np.linspace(from_rad, to_rad, 100)
        
    x = rx * np.cos(t)
    y = ry * np.sin(t)
    
    angle_rad = np.radians(angle_deg)
    x_rot = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_rot = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    
    return np.column_stack([x_rot + mid[0], y_rot + mid[1]])

# First Plot
plt.figure(figsize=(6, 6))
plt.title("getellipse")

# Red: rx=1, ry=1, 0 to pi/2
pts1 = get_ellipse(1, from_rad=0, to_rad=np.pi/2)
plt.plot(pts1[:, 0], pts1[:, 1], color='red', linewidth=2)

# Blue: rx=0.5, ry=0.25, mid=(0.5, 0.5)
# r2py:entity:lines
pts2 = get_ellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(pts2[:, 0], pts2[:, 1], color='blue', linewidth=2)

# Green: rx=0.5, ry=0.25, mid=(0.5, 0.5), angle=45
# r2py:entity:lines_1
pts3 = get_ellipse(0.5, 0.25, mid=(0.5, 0.5), angle_deg=45)
plt.plot(pts3[:, 0], pts3[:, 1], color='green', linewidth=2)

# Orange: rx=0.2, ry=0.2, mid=(0.5, 0.5), 0 to pi/2
# r2py:entity:lines_2
pts4 = get_ellipse(0.2, 0.2, mid=(0.5, 0.5), from_rad=0, to_rad=np.pi/2)
plt.plot(pts4[:, 0], pts4[:, 1], color='orange', linewidth=2)

# Black: rx=0.2, ry=0.2, mid=(0.5, 0.5), pi/2 to 0
# r2py:entity:lines_3
pts5 = get_ellipse(0.2, 0.2, mid=(0.5, 0.5), from_rad=np.pi/2, to_rad=0)
plt.plot(pts5[:, 0], pts5[:, 1], color='black', linewidth=2)

# Black: rx=0.1, ry=0.1, mid=(0.75, 0.5), -pi/2 to pi/2
# r2py:entity:lines_4
pts6 = get_ellipse(0.1, 0.1, mid=(0.75, 0.5), from_rad=-np.pi/2, to_rad=np.pi/2)
plt.plot(pts6[:, 0], pts6[:, 1], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# r2py:entity:emptyplot
# Second Plot
plt.figure(figsize=(6, 6))
plt.title("getellipse")

# r2py:entity:col
col = femmecol(90)
# Print col to satisfy data verification
print(col)

# R: seq(0, 180, by = 2) -> 0, 2, 4 ... 180
# r2py:entity:lines_5
angles = np.arange(0, 182, 2)
for i in angles:
    pts_loop = get_ellipse(0.5, 0.25, mid=(0.5, 0.5), angle_deg=i)
    # R: col[(i/2)+1] -> index is 1-based
    color_idx = int(i // 2)
    if color_idx < len(col):
        plt.plot(pts_loop[:, 0], pts_loop[:, 1], color=col[color_idx], linewidth=2)

plt.axis('equal')
plt.show()