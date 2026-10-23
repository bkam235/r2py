import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Ellipse

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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=None, code=0, arr_type="triangle", 
           arr_col="black", lcol=None, arr_lwd=1, segment=True, arr_adj=0, xpd=False):
    # Convert inputs to arrays for vectorization
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    # Handle colors (R allows vectors for colors)
    if isinstance(arr_col, (int, float)):
        # Simple mapping for 1:100 colors if numeric
        colors = plt.cm.tab20(np.linspace(0, 1, len(x0))) if isinstance(arr_col, int) else [arr_col]
    elif isinstance(arr_col, (list, np.ndarray)):
        colors = arr_col
    else:
        colors = [arr_col] * len(x0)

    line_colors = lcol if lcol is not None else colors

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        dist = np.sqrt(dx**2 + dy**2)
        if dist == 0: continue
        
        # Main line
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=line_colors[i % len(line_colors)], linewidth=arr_lwd)
        
        # Arrow Head
        # R's 'shape' package has very specific head types. 
        # code=2 typically means arrow at the end, code=3 both ends, etc.
        # Here we implement the head at the end (x1, y1)
        
        # Normalizing vector
        ux, uy = dx/dist, dy/dist
        vx, vy = -uy, ux # Perpendicular
        
        length = arr_length[i] if isinstance(arr_length, (list, np.ndarray)) else arr_length
        
        if arr_type == "triangle":
            # Simple triangle
            p1 = [x1[i] - length*ux + 0.2*length*vx, y1[i] - length*uy + 0.2*length*vy]
            p2 = [x1[i] - length*ux - 0.2*length*vx, y1[i] - length*uy - 0.2*length*vy]
            plt.plot([x1[i], p1[0], p2[0], x1[i]], [y1[i], p1[1], p2[1], y1[i]], color=colors[i % len(colors)], linewidth=arr_lwd)
            
        elif arr_type == "curved":
            # Approximated by a small arc
            t = np.linspace(0, np.pi, 10)
            cx = x1[i] - length*ux + 0.1*length*np.cos(t)*vx
            cy = y1[i] - length*uy + 0.1*length*np.sin(t)*vy
            plt.plot(cx, cy, color=colors[i % len(colors)], linewidth=arr_lwd)
            
        elif arr_type == "circle":
            # Simple circle at the tip
            circle = Circle((x1[i], y1[i]), radius=length/2, color=colors[i % len(colors)], fill=False)
            plt.gca().add_patch(circle)
            
        elif arr_type == "ellipse":
            width = arr_width if arr_width is not None else 0.2
            ellipse = Ellipse((x1[i], y1[i]), width=length, height=width, angle=np.degrees(np.arctan2(uy, ux)), 
                              color=colors[i % len(colors)], fill=False)
            plt.gca().add_patch(ellipse)
            
        elif arr_type == "T":
            p1 = [x1[i] - length*ux + 0.2*length*vx, y1[i] - length*uy + 0.2*length*vy]
            p2 = [x1[i] - length*ux - 0.2*length*vx, y1[i] - length*uy - 0.2*length*vy]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=colors[i % len(colors)], linewidth=arr_lwd)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

plt.figure()
plt.plot(0, 0) # Initialize
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))

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

plt.figure()
plt.plot(0, 0)
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")

plt.figure()
x_curve = np.linspace(0, 2*np.pi+0.25, 100)
plt.plot(x_curve, np.sin(x_curve), label="sin(x)")
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

xx = np.linspace(0, 10*np.pi, 1000)
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 'l')
plt.axis('off')
plt.xlabel("")
plt.ylabel("")
plt.title("Arrows,  type = 'curved'")
x = np.linspace(0, 10*np.pi, 20)
x1 = np.sin(x)*x
y1 = np.cos(x)*x
xd = x + 0.01
x2 = np.sin(xd)*xd
y2 = np.cos(xd)*xd
Arrows(x1, y1, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)

plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 'l')
plt.axis('off')
plt.xlabel("")
plt.ylabel("")
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])
plt.figure()
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