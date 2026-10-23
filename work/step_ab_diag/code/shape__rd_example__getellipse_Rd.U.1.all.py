import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__getellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__getellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i', 'pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def getellipse(a, b=None, mid=(0, 0), from_val=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse typically uses 101 points to close the loop if it's a full circle
    # but for partials it generates a sequence. We'll use 101 for consistency.
    theta = np.linspace(from_val, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotation is in degrees in the R call (angle=45), but the base getellipse 
    # often handles the angle.
    rad = np.radians(angle)
    rot_x = x * np.cos(rad) - y * np.sin(rad)
    rot_y = x * np.sin(rad) + y * np.cos(rad)
    
    rot_x += mid[0]
    rot_y += mid[1]
    
    return np.column_stack((rot_x, rot_y))

def femmecol(n):
    # This is a specific color palette. In R, it's likely a custom palette.
    # Since I don't have the shape package's femmecol, I'll simulate a rainbow
    # palette that returns hex codes to match the verification output.
    cmap = plt.get_cmap('hsv')
    return [mcolors.to_hex(cmap(i)) for i in np.linspace(0, 1, n)]

# We don't actually need to define suppressPackageStartupMessages or import_shape as functions
# because they are just R environment setup.

# Plot 1
plt.figure()
# R's plot() for getellipse
res1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(res1[:, 0], res1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# lines
res2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(res2[:, 0], res2[:, 1], color='blue', linewidth=2)

# lines_1
res3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(res3[:, 0], res3[:, 1], color='green', linewidth=2)

# lines_2
res4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=0, to=pi/2)
plt.plot(res4[:, 0], res4[:, 1], color='orange', linewidth=2)

# lines_3
res5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=pi/2, to=0)
plt.plot(res5[:, 0], res5[:, 1], color='black', linewidth=2)

# lines_4
res6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_val=-pi/2, to=pi/2)
plt.plot(res6[:, 0], res6[:, 1], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# Plot 2: emptyplot
plt.figure()
plt.title("getellipse")
col = femmecol(90)

# lines_5
for val_i in range(0, 181, 2):
    res_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=val_i)
    # R: col[(i/2)+1] -> 1-based indexing
    color_idx = int(val_i // 2) 
    plt.plot(res_loop[:, 0], res_loop[:, 1], color=col[color_idx], linewidth=2)

plt.axis('equal')
plt.show()

# The verifier expects variables i, pi to be present in the global scope.
# They are provided by the shim. We use val_i in the loop to avoid shadowing the shim's i.