# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 51

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__Arrows_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__Arrows_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi', 'x', 'x0', 'x1', 'y0', 'y1']:
#     if _r2py_shim_n in _r2py_shim_data:
# r2py:entity:y1_3
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=None, code=0, arr_type='triangle', arr_col='black', lcol=None, segment=True, arr_adj=0.5, arr_lwd=1, xpd=False):
    """
    Approximate the shape::Arrows function from R.
    """
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    # Handle scalars for length and color
    if isinstance(arr_length, (int, float)):
        arr_lengths = np.full(len(x0), arr_length)
    else:
        arr_lengths = np.asarray(arr_length)
        
    if isinstance(arr_col, str):
        colors = [arr_col] * len(x0)
    elif isinstance(arr_col, (int, float)):
        colors = [plt.cm.tab10(i % 10) for i in range(len(x0))]
    else:
        colors = np.asarray(arr_col)

    line_colors = lcol if lcol is not None else colors

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        
        # Segment line
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=line_colors[i], linewidth=arr_lwd)
        
        # Arrow head position adjustment
        # code 1: head at end, code 2: head at both, code 3: head at start
        heads = []
        if code == 1 or code == 2: heads.append((x1[i], y1[i], 1))
        if code == 2 or code == 3: heads.append((x0[i], y0[i], -1))
        
        for hx, hy, direction in heads:
            if arr_type == 'triangle':
                plt.annotate('', xy=(hx, hy), xytext=(hx - direction*arr_lengths[i]*ux, hy - direction*arr_lengths[i]*uy),
                             arrowprops=dict(arrowstyle='->', color=colors[i], linewidth=arr_lwd))
            elif arr_type == 'curved':
                # Approximation of a curved head
                plt.plot(hx, hy, marker='>', color=colors[i], markersize=arr_lengths[i]*10)
            elif arr_type == 'circle':
                plt.plot(hx, hy, marker='o', color=colors[i], markersize=arr_lengths[i]*10)
            elif arr_type == 'ellipse':
                plt.plot(hx, hy, marker=' ', color=colors[i], markersize=arr_lengths[i]*10)
            elif arr_type == 'T':
                # T-shape head
                vx, vy = -uy, ux
                plt.plot([hx - direction*0.2*vx, hx + direction*0.2*vx], 
                         [hy - direction*0.2*vy, hy + direction*0.2*vy], color=colors[i], linewidth=arr_lwd)

# r2py:entity:xlim
xlim = [-5, 5]
# r2py:entity:ylim
ylim = [-10, 10]

# Plot 1
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))

# Plot 2
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'circle'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey")

# Plot 3
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")

# Plot 4
plt.figure()
x_vals = np.linspace(0, 2*np.pi + 0.25, 100)
plt.plot(x_vals, np.sin(x_vals))
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

# Plot 5
plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, color='black', linewidth=1)
plt.axis('off')
plt.title("Arrows,  type = 'curved'")
x = np.linspace(0, 10*np.pi, 20)
x1 = np.sin(x)*x
y1 = np.cos(x)*x
xd = x + 0.01
x2 = np.sin(xd)*xd
y2 = np.cos(xd)*xd
Arrows(x1, y1, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)

# Plot 6
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, color='black', linewidth=1)
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

# Plot 7
plt.figure()
xlim = [-5, 5]
ylim = [-10, 10]
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)