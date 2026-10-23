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
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def getellipse(a, b=None, mid=(0, 0), from_=0, to=2*pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse typically uses a sequence of angles
    theta = np.linspace(from_, to, 100)
    
    # Base ellipse centered at origin
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotation angle in radians
    phi = np.radians(angle)
    
    # Rotate and translate
    # x' = x cos(phi) - y sin(phi) + mid_x
    # y' = x sin(phi) + y cos(phi) + mid_y
    res_x = x * np.cos(phi) - y * np.sin(phi) + mid[0]
    res_y = x * np.sin(phi) + y * np.cos(phi) + mid[1]
    
    return np.column_stack((res_x, res_y))

def femmecol(n):
    # femmecol in shape package provides a specific palette. 
    # 'hsv' or 'rainbow' are close approximations for these types of plots.
    return cm.get_cmap('hsv', n)

# Plot 1
plt.figure()
# plot(getellipse(1, from = 0, to = pi/2), type = "l", col = "red", lwd = 2, main = "getellipse")
ellipse1 = getellipse(1, from_=0, to=pi/2)
plt.plot(ellipse1[:, 0], ellipse1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5)), type = "l", col = "blue", lwd = 2)
ellipse2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(ellipse2[:, 0], ellipse2[:, 1], color='blue', linewidth=2)

# lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5), angle = 45), type = "l", col = "green", lwd = 2)
ellipse3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(ellipse3[:, 0], ellipse3[:, 1], color='green', linewidth=2)

# lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = 0, to = pi/2), type = "l", col = "orange", lwd = 2)
ellipse4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=0, to=pi/2)
plt.plot(ellipse4[:, 0], ellipse4[:, 1], color='orange', linewidth=2)

# lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = pi/2, to = 0), type = "l", col = "black", lwd = 2)
ellipse5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=pi/2, to=0)
plt.plot(ellipse5[:, 0], ellipse5[:, 1], color='black', linewidth=2)

# lines(getellipse(0.1, 0.1, mid = c(0.75, 0.5), from = -pi/2, to = pi/2), type = "l", col = "black", lwd = 2)
ellipse6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_=-pi/2, to=pi/2)
plt.plot(ellipse6[:, 0], ellipse6[:, 1], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# Plot 2
plt.figure()
plt.title("getellipse")
# emptyplot is just a plot initialization in the shape package
col = femmecol(90)
for i_val in range(0, 181, 2):
    # lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5), angle = i), type = "l", col = col[(i/2)+1], lwd = 2)
    ellipse_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    # indexing_1based: col[(i/2)+1] -> col[i//2]
    plt.plot(ellipse_loop[:, 0], ellipse_loop[:, 1], color=col(i_val // 2), linewidth=2)

plt.axis('equal')
plt.show()