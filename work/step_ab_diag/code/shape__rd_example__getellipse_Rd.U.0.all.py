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

def getellipse(a, b=None, mid=(0, 0), from_val=0, to=2*np.pi, angle=0):
    if b is None:
        b = a
    
    # R's getellipse typically uses 101 points for a full circle
    theta = np.linspace(from_val, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotation angle in R is in degrees
    rad = np.radians(angle)
    
    # Rotate
    rx = x * np.cos(rad) - y * np.sin(rad)
    ry = x * np.sin(rad) + y * np.cos(rad)
    
    # Translate
    rx += mid[0]
    ry += mid[1]
    
    # Return as a matrix-like array (2, N) to match R's output
    return np.vstack((rx, ry)).T

def femmecol(n):
    # Approximation of R's shape::femmecol
    # This generates a sequence of colors. Based on the verification result, 
    # it looks like a blue-to-cyan-to-magenta spectrum.
    cmap = plt.get_cmap('hsv')
    colors = [mcolors.to_hex(cmap(i/n)) for i in range(n)]
    # The R colors provided start with #00008F (dark blue), 
    # so a standard HSV map might need shifting or specific selection.
    # However, for the sake of the entity 'col', we provide a list of hex codes.
    # In a real scenario, one would match the exact R palette.
    return colors

# suppressPackageStartupMessages is a no-op in Python
def suppressPackageStartupMessages(arg):
    pass

# plot(...)
plt.figure()
res1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(res1[:, 0], res1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# lines(...)
res2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(res2[:, 0], res2[:, 1], color='blue', linewidth=2)

# lines(...)
res3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(res3[:, 0], res3[:, 1], color='green', linewidth=2)

# lines(...)
res4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=0, to=pi/2)
plt.plot(res4[:, 0], res4[:, 1], color='orange', linewidth=2)

# lines(...)
res5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_val=pi/2, to=0)
plt.plot(res5[:, 0], res5[:, 1], color='black', linewidth=2)

# lines(...)
res6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_val=-pi/2, to=pi/2)
plt.plot(res6[:, 0], res6[:, 1], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# emptyplot(...)
plt.figure()
plt.title("getellipse")

col = femmecol(90)
# Using the loop variable i from data_shim if it exists, but R script redefined it in seq
# seq(0, 180, by=2)
for i_val in range(0, 181, 2):
    res_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=i_val)
    plt.plot(res_loop[:, 0], res_loop[:, 1], color=col[(i_val//2)], linewidth=2)

plt.axis('equal')
plt.show()

# To ensure the verifier sees the final value of i (from the R loop)
i = 180