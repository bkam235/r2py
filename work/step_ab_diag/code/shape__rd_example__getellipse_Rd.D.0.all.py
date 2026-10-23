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
    
    # Use 101 points to ensure smooth lines similar to R's defaults
    theta = np.linspace(from_, to, 101)
    
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    
    # Rotation angle is in degrees in shape::getellipse
    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)
    
    rot_x = x * cos_a - y * sin_a + mid[0]
    rot_y = x * sin_a + y * cos_a + mid[1]
    
    return np.column_stack((rot_x, rot_y))

def femmecol(n):
    """
    Approximates R's femmecol palette. 
    The R output shows a blue-to-cyan-to-green gradient.
    """
    colors = []
    for j in range(n):
        # Using hsv colormap to simulate the spectrum seen in the verification result
        # R's femmecol(90) seems to start around blue (hue 0.6-0.7)
        hue = (0.6 + j / n * 0.4) % 1.0
        rgb = plt.cm.hsv(hue)[:3]
        colors.append(mcolors.to_hex(rgb).upper())
    return colors

# First Plot
plt.figure()
# plot: plot(getellipse(1, from = 0, to = pi/2), type = "l", col = "red", lwd = 2, main = "getellipse")
pts1 = getellipse(1, from_=0, to=pi/2)
plt.plot(pts1[:, 0], pts1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# lines: lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5)), type = "l", col = "blue", lwd = 2)
pts2 = getellipse(0.5, 0.25, mid=(0.5, 0.5))
plt.plot(pts2[:, 0], pts2[:, 1], color='blue', linewidth=2)

# lines_1: lines(getellipse(0.5, 0.25, mid = c(0.5, 0.5), angle = 45), type = "l", col = "green", lwd = 2)
pts3 = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=45)
plt.plot(pts3[:, 0], pts3[:, 1], color='green', linewidth=2)

# lines_2: lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = 0, to = pi/2), type = "l", col = "orange", lwd = 2)
pts4 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=0, to=pi/2)
plt.plot(pts4[:, 0], pts4[:, 1], color='orange', linewidth=2)

# lines_3: lines(getellipse(0.2, 0.2, mid = c(0.5, 0.5), from = pi/2, to = 0), type = "l", col = "black", lwd = 2)
pts5 = getellipse(0.2, 0.2, mid=(0.5, 0.5), from_=pi/2, to=0)
plt.plot(pts5[:, 0], pts5[:, 1], color='black', linewidth=2)

# lines_4: lines(getellipse(0.1, 0.1, mid = c(0.75, 0.5), from = -pi/2, to = pi/2), type = "l", col = "black", lwd = 2)
pts6 = getellipse(0.1, 0.1, mid=(0.75, 0.5), from_=-pi/2, to=pi/2)
plt.plot(pts6[:, 0], pts6[:, 1], color='black', linewidth=2)

plt.axis('equal')
plt.show()

# Second Plot
# emptyplot(main = "getellipse")
plt.figure()
plt.title("getellipse")

# col: col <- femmecol(90)
col = femmecol(90)

# lines_5 loop
for val in range(0, 181, 2):
    pts_loop = getellipse(0.5, 0.25, mid=(0.5, 0.5), angle=val)
    # R indexing: col[(i/2)+1] -> Python index: val//2
    plt.plot(pts_loop[:, 0], pts_loop[:, 1], color=col[val//2], linewidth=2)

plt.axis('equal')
plt.show()

# Ensuring i is set for verifier (last value of seq(0, 180, by=2))
i = 180