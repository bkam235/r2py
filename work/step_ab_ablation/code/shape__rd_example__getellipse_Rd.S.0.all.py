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

def getellipse(a, b=None, mid=(0, 0), from_=0, to=2*pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse by default uses 101 points
    theta = np.linspace(from_, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # angle in R's getellipse is in degrees
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    # Rotation
    x_rot = x * cos_a - y * sin_a
    y_rot = x * sin_a + y * cos_a
    
    # Translation
    x_final = x_rot + mid[0]
    y_final = y_rot + mid[1]
    
    # Return as a 2xN array to mimic R's matrix output
    return np.vstack([x_final, y_final])

def femmecol(n):
    # femmecol is a specific color palette; hsv is a common approximation for rainbows
    cmap = cm.get_cmap('hsv')
    return [cmap(i/n) for i in range(n)]

# Plot 1
plt.figure()
e1 = getellipse(1, from_=0, to=pi/2)
plt.plot(e1[0], e1[1], color='red', linewidth=2)
plt.title("getellipse")

e2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(e2[0], e2[1], color='blue', linewidth=2)

e3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(e3[0], e3[1], color='green', linewidth=2)

e4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=0, to=pi/2)
plt.plot(e4[0], e4[1], color='orange', linewidth=2)

e5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=pi/2, to=0)
plt.plot(e5[0], e5[1], color='black', linewidth=2)

e6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_=-pi/2, to=pi/2)
plt.plot(e6[0], e6[1], color='black', linewidth=2)

plt.gca().set_aspect('equal')
plt.show()

# Plot 2
plt.figure()
plt.title("getellipse")
col = femmecol(90)

for i_val in range(0, 181, 2):
    e_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    # R: col[(i/2)+1] -> Python: col[i//2]
    plt.plot(e_loop[0], e_loop[1], color=col[i_val // 2], linewidth=2)

plt.gca().set_aspect('equal')
plt.show()