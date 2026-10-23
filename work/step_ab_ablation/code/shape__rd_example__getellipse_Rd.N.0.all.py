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

def getellipse(a, b=None, mid=(0, 0), from_val=0, to=2*pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse typically returns a matrix of coordinates
    # The number of points is usually 101 by default in shape package
    theta = np.linspace(from_val, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # angle is in degrees
    rad = np.radians(angle)
    cos_rad = np.cos(rad)
    sin_rad = np.sin(rad)
    
    # Rotation
    rot_x = x * cos_rad - y * sin_rad
    rot_y = x * sin_rad + y * cos_rad
    
    # Translation
    rot_x += mid[0]
    rot_y += mid[1]
    
    # Return as Nx2 array to mimic R matrix
    return np.column_stack((rot_x, rot_y))

def femmecol(n):
    # Approximation of a color palette returning a list of colors
    return cm.get_cmap('hsv', n)

def emptyplot(main=""):
    plt.figure(figsize=(6, 6))
    plt.title(main)
    plt.axis('equal')

# Plot 1
plt.figure(figsize=(6, 6))
plt.title("getellipse")
res1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(res1[:, 0], res1[:, 1], color='red', linewidth=2)

res2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(res2[:, 0], res2[:, 1], color='blue', linewidth=2)

res3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(res3[:, 0], res3[:, 1], color='green', linewidth=2)

res4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=0, to=pi/2)
plt.plot(res4[:, 0], res4[:, 1], color='orange', linewidth=2)

res5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=pi/2, to=0)
plt.plot(res5[:, 0], res5[:, 1], color='black', linewidth=2)

res6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_val=-pi/2, to=pi/2)
plt.plot(res6[:, 0], res6[:, 1], color='black', linewidth=2)
plt.axis('equal')
plt.show()

# Plot 2
emptyplot(main="getellipse")
col = femmecol(90)
for i_val in range(0, 181, 2):
    res_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    # R: col[(i/2)+1] -> Python: col[i//2]
    plt.plot(res_loop[:, 0], res_loop[:, 1], color=col(i_val // 2), linewidth=2)
plt.show()