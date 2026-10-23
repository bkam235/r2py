import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Ellipse

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

def Arrows(x0, y0, x1, y1, arr_type='triangle', arr_length=0.2, arr_width=0.5, code=1, arr_col='black', lcol=None, segment=True, arr_adj=0, arr_lwd=1, xpd=False):
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    # Handle colors
    if isinstance(arr_col, (int, float)):
        # Basic mapping for numeric colors like R 1:100
        colors = plt.cm.jet(np.linspace(0, 1, len(x0))) if np.isscalar(arr_col) else plt.cm.jet(np.linspace(0, 1, len(arr_col)))
    elif isinstance(arr_col, list) or isinstance(arr_col, np.ndarray):
        colors = arr_col
    else:
        colors = [arr_col] * len(x0)

    if lcol is None:
        l_colors = colors
    elif isinstance(lcol, (int, float)):
        l_colors = plt.cm.jet(np.linspace(0, 1, len(x0))) if np.isscalar(lcol) else plt.cm.jet(np.linspace(0, 1, len(lcol)))
    else:
        l_colors = [lcol] * len(x0)

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        
        # Line segment
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=l_colors[i], linewidth=arr_lwd)
        
        # Head position
        hx, hy = x1[i], y1[i]
        if arr_adj != 0:
            hx = x0[i] + arr_adj * dx
            hy = y0[i] + arr_adj * dy
            
        # Head geometry
        if arr_type == 'triangle':
            v_len = arr_length
            # Perpendicular vector
            px, py = -uy, ux
            p1 = [hx - v_len*ux + 0.2*px, hy - v_len*uy + 0.2*py]
            p2 = [hx - v_len*ux - 0.2*px, hy - v_len*uy - 0.2*py]
            poly = Polygon([ [hx, hy], p1, p2], closed=True, color=colors[i])
            plt.gca().add_patch(poly)
        elif arr_type == 'curved':
            # Approximation of curved head
            circle = Circle((hx - 0.1*ux, hy - 0.1*uy), radius=arr_length*0.5, color=colors[i])
            plt.gca().add_patch(circle)
        elif arr_type == 'circle':
            circle = Circle((hx, hy), radius=arr_length/2, color=colors[i])
            plt.gca().add_patch(circle)
        elif arr_type == 'ellipse':
            ellipse = Ellipse((hx, hy), width=arr_length, height=arr_width, color=colors[i])
            plt.gca().add_patch(ellipse)
        elif arr_type == 'T':
            px, py = -uy, ux
            plt.plot([hx - arr_length*px, hx + arr_length*px], [hy - arr_length*py, hy + arr_length*py], color=colors[i], linewidth=arr_lwd)

# Main Execution
xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
# Use shimmed x0, y0, x1, y1
x0 = np.asarray(x0)
y0 = np.asarray(y0)
x1 = np.asarray(x1)
y1 = np.asarray(y1)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, arr_type='curved', arr_col=np.arange(1, 101), lcol=np.arange(1, 101))

plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'circle'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=0.2, code=3, arr_type='circle', arr_col='grey')

plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, code=3, arr_type='ellipse', arr_col='grey')

plt.figure()
xx_curve = np.linspace(0, 2*np.pi + 0.25, 100)
plt.plot(xx_curve, np.sin(xx_curve))
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type='triangle', arr_length=0.5, segment=False)

xx = np.linspace(0, 10*np.pi, 1000)
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 'l')
plt.axis('off')
plt.title("Arrows,  type = 'curved'")
x = np.linspace(0, 10*np.pi, 20)
x1 = np.sin(x)*x
y1 = np.cos(x)*x
xd = x + 0.01
x2 = np.sin(xd)*xd
y2 = np.cos(xd)*xd
Arrows(x1, y1, x2, y2, arr_type='curved', arr_length=0.4, segment=False, code=1, arr_adj=0.5)

plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 'l')
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type='T', arr_length=0.4, code=1, arr_lwd=2)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])
plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, arr_type='curved', arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)