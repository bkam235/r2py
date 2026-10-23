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
import matplotlib.colors as mcolors

def getellipse(a, b=None, mid=(0, 0), from_=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse typically uses a sequence of 101 points
    theta = np.linspace(from_, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # angle in R's getellipse is usually degrees
    rad = np.radians(angle)
    
    # Rotation
    rot_x = x * np.cos(rad) - y * np.sin(rad)
    rot_y = x * np.sin(rad) + y * np.cos(rad)
    
    # Translation
    rot_x += mid[0]
    rot_y += mid[1]
    
    return np.column_stack((rot_x, rot_y))

def femmecol(n):
    # femmecol in R creates a specific blue-to-red/cyan transition
    # Based on the verification output, it starts with dark blue #00008F
    # We can simulate this using a linear interpolation in RGB space
    start_color = np.array(mcolors.to_rgb('#00008F'))
    end_color = np.array(mcolors.to_rgb('#FF00FF')) # Approximate end based on HSV-like shift
    
    colors = []
    for i in range(n):
        ratio = i / (n - 1)
        c = start_color * (1 - ratio) + end_color * ratio
        colors.append(mcolors.to_hex(c))
    return colors

# Plot 1
plt.figure()
res1 = getellipse(1, from_=0, to=pi/2)
plt.plot(res1[:, 0], res1[:, 1], color='red', linewidth=2, label='getellipse')
plt.title("getellipse")

res2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(res2[:, 0], res2[:, 1], color='blue', linewidth=2)

res3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(res3[:, 0], res3[:, 1], color='green', linewidth=2)

res4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=0, to=pi/2)
plt.plot(res4[:, 0], res4[:, 1], color='orange', linewidth=2)

res5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=pi/2, to=0)
plt.plot(res5[:, 0], res5[:, 1], color='black', linewidth=2)

res6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_=-pi/2, to=pi/2)
plt.plot(res6[:, 0], res6[:, 1], color='black', linewidth=2)

plt.axis('equal')

# Plot 2
plt.figure()
plt.title("getellipse")
col = femmecol(90)
for i_val in range(0, 181, 2):
    res_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    # R indexing: col[(i/2)+1]
    color_idx = (i_val // 2)
    if color_idx < len(col):
        plt.plot(res_loop[:, 0], res_loop[:, 1], color=col[color_idx], linewidth=2)

plt.axis('equal')
plt.show()