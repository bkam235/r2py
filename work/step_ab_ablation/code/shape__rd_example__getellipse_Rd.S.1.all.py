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
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def getellipse(a, b=None, mid=(0, 0), from_val=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse produces 101 points by default (seq(from, to, length.out = 101))
    theta = np.linspace(from_val, to, 101)
    
    # Parametric coordinates before rotation
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotate by angle (degrees to radians)
    rad = np.radians(angle)
    cos_rad = np.cos(rad)
    sin_rad = np.sin(rad)
    
    rot_x = x * cos_rad - y * sin_rad
    rot_y = x * sin_rad + y * cos_rad
    
    # Translate to mid
    final_x = rot_x + mid[0]
    final_y = rot_y + mid[1]
    
    return np.column_stack((final_x, final_y))

def femmecol(n):
    # R's femmecol is a specific palette. Using hsv as a common approximation.
    cmap = cm.get_cmap('hsv')
    return [cmap(i/n) for i in range(n)]

# R: plot(getellipse(1, from = 0, to = pi/2), type = "l", col = "red", lwd = 2, main = "getellipse")
plt.figure()
ellipse1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(ellipse1[:, 0], ellipse1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# R: lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5)), type = "l", col = "blue", lwd = 2)
ellipse2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(ellipse2[:, 0], ellipse2[:, 1], color='blue', linewidth=2)

# R: lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5), angle = 45), type = "l", col = "green", lwd = 2)
ellipse3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(ellipse3[:, 0], ellipse3[:, 1], color='green', linewidth=2)

# R: lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = 0, to = pi/2), type = "l", col = "orange", lwd = 2)
ellipse4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=0, to=pi/2)
plt.plot(ellipse4[:, 0], ellipse4[:, 1], color='orange', linewidth=2)

# R: lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = pi/2, to = 0), type = "l", col = "black", lwd = 2)
ellipse5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=pi/2, to=0)
plt.plot(ellipse5[:, 0], ellipse5[:, 1], color='black', linewidth=2)

# R: lines(getellipse(0.1, 0.1, mid = c(0.75, 0.5), from = -pi/2, to = pi/2), type = "l", col = "black", lwd = 2)
ellipse6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_val=-pi/2, to=pi/2)
plt.plot(ellipse6[:, 0], ellipse6[:, 1], color='black', linewidth=2)
plt.show()

# R: emptyplot(main = "getellipse")
plt.figure()
plt.title("getellipse")

# R: col <- femmecol(90)
col = femmecol(90)

# R: for (i in seq(0, 180, by = 2)) 
#      lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5), angle = i), type = "l", col = col[(i/2)+1], lwd = 2)
for i_val in range(0, 181, 2):
    ellipse_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    plt.plot(ellipse_loop[:, 0], ellipse_loop[:, 1], color=col[int(i_val/2)], linewidth=2)

plt.show()