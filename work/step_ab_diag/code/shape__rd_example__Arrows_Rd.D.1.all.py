import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Ellipse, Polygon

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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.2, code=1, arr_type='triangle', 
           arr_col='black', lcol=None, arr_lwd=1, segment=True, arr_adj=1.0, xpd=True):
    """
    Approximates the behavior of shape::Arrows in R.
    """
    x0 = np.atleast_1d(x0)
    y0 = np.atleast_1d(y0)
    x1 = np.atleast_1d(x1)
    y1 = np.atleast_1d(y1)
    
    # R's 1:100 colors can be approximated via a colormap
    def get_color(c, idx):
        if isinstance(c, (list, np.ndarray)):
            return c[idx] if hasattr(c, '__getitem__') else c
        if isinstance(c, (int, float)) and not isinstance(c, str):
            cmap = plt.get_cmap('tab20')
            return cmap(int(c) % 20)
        return c

    for i in range(len(x0)):
        c_arr = get_color(arr_col, i)
        c_line = get_color(lcol, i) if lcol is not None else c_arr
        
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=c_line, linewidth=arr_lwd)
        
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        dist = np.sqrt(dx**2 + dy**2)
        if dist == 0: continue
        
        ux, uy = dx/dist, dy/dist
        vx, vy = -uy, ux
        
        l = arr_length[i] if isinstance(arr_length, (list, np.ndarray)) else arr_length
        
        # The head position
        hx = x1[i] - ux * (l * dist * (1 - arr_adj))
        hy = y1[i] - uy * (l * dist * (1 - arr_adj))
        
        if arr_type == 'triangle':
            p1 = [hx, hy]
            p2 = [hx - l * ux + 0.2 * vx, hy - l * uy + 0.2 * vy]
            p3 = [hx - l * ux - 0.2 * vx, hy - l * uy - 0.2 * vy]
            plt.gca().add_patch(Polygon([p1, p2, p3], color=c_arr))
        elif arr_type == 'curved':
            angle = np.degrees(np.arctan2(uy, ux))
            arc = Arc((hx, hy), 2*l, 2*l, theta1=angle-30, theta2=angle+30, 
                      color=c_arr, linewidth=arr_lwd)
            plt.gca().add_patch(arc)
        elif arr_type == 'circle':
            plt.gca().add_patch(plt.Circle((hx, hy), l, color=c_arr))
        elif arr_type == 'ellipse':
            ellipse = Ellipse((hx, hy), 2*l, 2*l*arr_width, angle=np.degrees(np.arctan2(uy, ux)), 
                               color=c_arr)
            plt.gca().add_patch(ellipse)
        elif arr_type == 'T':
            p1 = [hx - l*vx, hy - l*vy]
            p2 = [hx + l*vx, hy + l*vy]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=c_arr, linewidth=arr_lwd)

# --- Execution ---

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

# Plot 1
plt.figure()
plt.title("Arrows,  type = 'curved'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))

# Plot 2
plt.figure()
plt.title("Arrows,  type = 'circle'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey")

# Plot 3
plt.figure()
plt.title("Arrows,  type = 'ellipse'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")

# Plot 4
plt.figure()
xv = np.linspace(0, 2*np.pi + 0.25, 100)
plt.plot(xv, np.sin(xv))
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

# Plot 5
plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
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
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

# Plot 7
plt.figure()
xlim = np.array([-5, 5])
ylim = np.array([-10, 10])
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)