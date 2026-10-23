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
from matplotlib.patches import Arc, Circle, Ellipse

def Arrows(x0, y0, x1, y1, arr_type='triangle', arr_length=0.2, arr_width=0.2, code=1, 
           arr_col='black', lcol=None, arr_lwd=1, segment=True, arr_adj=1.0, xpd=False):
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    if lcol is None:
        lcol = arr_col
    
    # Ensure colors are iterable
    if isinstance(arr_col, str):
        arr_cols = [arr_col] * len(x0)
    else:
        arr_cols = arr_col
        
    if isinstance(lcol, str):
        lcols = [lcol] * len(x0)
    else:
        lcols = lcol

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        
        # Draw line segment
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=lcols[i], linewidth=arr_lwd)
        
        # Arrow head position
        hx, hy = x1[i] - (1 - arr_adj) * ux * 0.1, y1[i] - (1 - arr_adj) * uy * 0.1
        
        # head length
        length = arr_length if isinstance(arr_length, (int, float)) else arr_length[i]
        
        if arr_type == 'triangle':
            # Simple triangle approximation
            vx, vy = -uy, ux
            p1 = [hx - length * ux + 0.2 * vx, hy - length * uy + 0.2 * vy]
            p2 = [hx - length * ux - 0.2 * vx, hy - length * uy - 0.2 * vy]
            plt.plot([p1[0], hx, p2[0]], [p1[1], hy, p2[1]], color=arr_cols[i], linewidth=arr_lwd)
            
        elif arr_type == 'curved':
            # R's shape::Arrows 'curved' is often a small arc
            angle = np.degrees(np.arctan2(uy, ux))
            arc = Arc((hx, hy), 2*length, 2*length, angle=angle-180, theta1=0, theta2=180, color=arr_cols[i])
            plt.gca().add_patch(arc)
            
        elif arr_type == 'circle':
            circ = Circle((hx, hy), radius=length, color=arr_cols[i])
            plt.gca().add_patch(circ)
            
        elif arr_type == 'ellipse':
            # Simplified ellipse
            ell = Ellipse((hx, hy), width=length*2, height=arr_width*2, angle=np.degrees(np.arctan2(uy, ux)), color=arr_cols[i])
            plt.gca().add_patch(ell)
            
        elif arr_type == 'T':
            vx, vy = -uy, ux
            p1 = [hx - length * ux + 0.2 * vx, hy - length * uy + 0.2 * vy]
            p2 = [hx - length * ux - 0.2 * vx, hy - length * uy - 0.2 * vy]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=arr_cols[i], linewidth=arr_lwd)

# r2py:entity:xlim
xlim = [-5, 5]
# r2py:entity:ylim
ylim = [-10, 10]

# Plot 1
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
# Use existing x0, y0, x1, y1 from shim
# Generating runif equivalents for the R script logic
np.random.seed(42)
x0_r = np.random.uniform(xlim[0], xlim[1], 100)
y0_r = np.random.uniform(ylim[0], ylim[1], 100)
x1_r = x0_r + np.random.uniform(-1, 1, 100)
y1_r = y0_r + np.random.uniform(-1, 1, 100)
Arrows(x0_r, y0_r, x1_r, y1_r, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))
plt.show()

# Plot 2
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'circle'")
x0_r2 = np.random.uniform(xlim[0], xlim[1], 100)
y0_r2 = np.random.uniform(ylim[0], ylim[1], 100)
x1_r2 = x0_r2 + np.random.uniform(-1, 1, 100)
y1_r2 = y0_r2 + np.random.uniform(-1, 1, 100)
Arrows(x0_r2, y0_r2, x1_r2, y1_r2, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey")
plt.show()

# Plot 3
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0_r2, y0_r2, x1_r2, y1_r2, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")
plt.show()

# Plot 4
plt.figure()
x_vals = np.linspace(0, 2*np.pi+0.25, 100)
plt.plot(x_vals, np.sin(x_vals))
plt.title("Arrows")
# Entity x is from shim
x_seq = np.linspace(0, 2*np.pi, 10)
xd = x_seq + 0.025
Arrows(x_seq, np.sin(x_seq), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)
plt.show()

# Plot 5
plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, linewidth=1)
plt.axis('off')
plt.title("Arrows,  type = 'curved'")
x_seq2 = np.linspace(0, 10*np.pi, 20)
x1_val = np.sin(x_seq2)*x_seq2
y1_val = np.cos(x_seq2)*x_seq2
xd_val = x_seq2 + 0.01
x2_val = np.sin(xd_val)*xd_val
y2_val = np.cos(xd_val)*xd_val
Arrows(x1_val, y1_val, x2_val, y2_val, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)
plt.show()

# Plot 6
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, linewidth=1)
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1_val, y1_val, x2_val, y2_val, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)
plt.show()

# Plot 7
plt.figure()
xlim = [-5, 5]
ylim = [-10, 10]
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0_r3 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0_r3 = np.random.uniform(ylim[0], ylim[1], 100)
x1_r3 = x0_r3 + np.random.uniform(-1, 1, 100)
y1_r3 = y0_r3 + np.random.uniform(-1, 1, 100)
# xpd=TRUE in R allows drawing outside plot region
Arrows(x0_r3, y0_r3, x1_r3, y1_r3, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)
plt.show()