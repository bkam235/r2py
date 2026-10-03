# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__getellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__getellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i', 'pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt

# r2py:entity:plot
def getellipse(a, b=None, mid=(0, 0), from_=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # Create theta sequence
    theta = np.linspace(from_, to, 100)
    
    # Parametric ellipse equations
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotation matrix
    rad = np.radians(angle)
    rot_x = x * np.cos(rad) - y * np.sin(rad)
    rot_y = x * np.sin(rad) + y * np.cos(rad)
    
    # Translation
    rot_x += mid[0]
    rot_y += mid[1]
    
    return pd.DataFrame({'x': rot_x, 'y': rot_y})

# r2py:entity:col
def femmecol(n):
    # Approximation of R's color palettes using a colormap
    import matplotlib.cm as cm
    return cm.get_cmap('hsv', n)

# Plot 1
plt.figure(figsize=(6, 6))
plt.title("getellipse")

d1 = getellipse(1, from_=0, to=np.pi/2)
plt.plot(d1['x'], d1['y'], color='red', linewidth=2)

# r2py:entity:lines
d2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(d2['x'], d2['y'], color='blue', linewidth=2)

# r2py:entity:lines_1
d3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(d3['x'], d3['y'], color='green', linewidth=2)

# r2py:entity:lines_2
d4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=0, to=np.pi/2)
plt.plot(d4['x'], d4['y'], color='orange', linewidth=2)

# r2py:entity:lines_3
d5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=np.pi/2, to=0)
plt.plot(d5['x'], d5['y'], color='black', linewidth=2)

# r2py:entity:lines_4
d6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_=-np.pi/2, to=np.pi/2)
plt.plot(d6['x'], d6['y'], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# Plot 2
# r2py:entity:emptyplot
plt.figure(figsize=(6, 6))
plt.title("getellipse")
col = femmecol(90)

# r2py:entity:lines_5
for i in range(0, 181, 2):
    d_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i)
    plt.plot(d_loop['x'], d_loop['y'], color=col(i//2), linewidth=2)

plt.axis('equal')
plt.show()