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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.2, code=0, arr_type='triangle', 
           arr_col='black', lcol=None, arr_lwd=1, segment=True, arr_adj=0, xpd=False):
    # Convert to numpy arrays
    x0, y0, x1, y1 = np.array(x0), np.array(y0), np.array(x1), np.array(y1)
    
    # If lcol is not provided, use arr_col for the line
    if lcol is None:
        lcol = arr_col

    # Handle scalars vs arrays for colors/lengths
    if isinstance(arr_col, str):
        arr_cols = [arr_col] * len(x0)
    else:
        arr_cols = arr_col
        
    if isinstance(lcol, str):
        lcols = [lcol] * len(x0)
    else:
        lcols = lcol
        
    if np.isscalar(arr_length):
        arr_lengths = np.full(len(x0), arr_length)
    else:
        arr_lengths = np.array(arr_length)

    for i in range(len(x0)):
        # Calculate vector and angle
        dx, dy = x1[i] - x0[i], y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        angle = np.degrees(np.arctan2(dy, dx))
        
        # Line segment
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=lcols[i], linewidth=arr_lwd)
        
        # Arrow head position
        # arr_adj moves the head along the vector
        hx, hy = x1[i] - arr_adj * dx, y1[i] - arr_adj * dy
        
        if arr_type == 'triangle':
            # Simple triangle approximation
            # Using plt.annotate or custom polygon for precise triangle
            plt.annotate('', xy=(x1[i], y1[i]), xytext=(x0[i], y0[i]),
                         arrowprops=dict(arrowstyle='->', color=arr_cols[i], 
                                         linewidth=arr_lwd, mutation_scale=arr_lengths[i]*20))
            continue # annotate handles the line too, but we check segment=True
            
        elif arr_type == 'curved':
            # Arc at the tip
            arc = Arc((hx, hy), arr_lengths[i], arr_lengths[i], angle=angle, 
                      theta1=0, theta2=180, color=arr_cols[i], linewidth=arr_lwd)
            plt.gca().add_patch(arc)
        elif arr_type == 'circle':
            circ = Circle((hx, hy), arr_lengths[i]/2, color=arr_cols[i], fill=False, linewidth=arr_lwd)
            plt.gca().add_patch(circ)
        elif arr_type == 'ellipse':
            ell = Ellipse((hx, hy), arr_lengths[i], arr_width, angle=angle, color=arr_cols[i], fill=False, linewidth=arr_lwd)
            plt.gca().add_patch(ell)
        elif arr_type == 'T':
            # Perpendicular bar
            perp_angle = angle + 90
            px = np.cos(np.radians(perp_angle)) * (arr_lengths[i]/2)
            py = np.sin(np.radians(perp_angle)) * (arr_lengths[i]/2)
            plt.plot([hx - px, hx + px], [hy - py, hy + py], color=arr_cols[i], linewidth=arr_lwd)

# r2py:entity:xlim
xlim = [-5, 5]
# r2py:entity:ylim
ylim = [-10, 10]

# Plot 1
plt.figure()
plt.plot(0, 0)
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))
plt.show()

# Plot 2
plt.figure()
plt.plot(0, 0)
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'circle'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey")
plt.show()

# Plot 3
plt.figure()
plt.plot(0, 0)
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse", arr_col="grey")
plt.show()

# Plot 4
plt.figure()
x_curve = np.linspace(0, 2*np.pi+0.25, 100)
plt.plot(x_curve, np.sin(x_curve))
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)
plt.show()

# Plot 5
plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, linewidth=1)
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
plt.show()

# Plot 6
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, linewidth=1)
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)
plt.show()

# Plot 7
plt.figure()
xlim = [-5, 5]
ylim = [-10, 10]
plt.plot(0, 0)
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)
plt.show()