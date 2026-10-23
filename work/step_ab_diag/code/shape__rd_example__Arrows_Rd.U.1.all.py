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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, code=1, 
           arr_type="triangle", arr_col="black", lcol=None, 
           segment=True, arr_adj=1.0, arr_lwd=1, xpd=False):
    # Convert inputs to numpy arrays
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    # Handle scalar color/length
    if isinstance(arr_length, (int, float)):
        arr_length = np.full(len(x0), arr_length)
    if isinstance(arr_col, str):
        arr_col = np.full(len(x0), arr_col)
    elif isinstance(arr_col, (int, float)):
        arr_col = np.full(len(x0), arr_col)
    
    # For color sequence 1:100 in R, we'll map it to a colormap or just distinct colors
    if isinstance(arr_col, np.ndarray) and np.all(np.arange(len(x0)) == arr_col - 1 if len(arr_col) == len(x0) else False):
        cmap = plt.get_cmap('tab20')
        colors = [cmap(i % 20) for i in range(len(x0))]
    else:
        colors = arr_col

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        dist = np.sqrt(dx**2 + dy**2)
        if dist == 0: continue
        ux, uy = dx/dist, dy/dist
        
        # Line color
        lc = lcol[i] if lcol is not None else colors[i]
        
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=lc, linewidth=arr_lwd)
        
        # Tip position
        tx, ty = x1[i], y1[i]
        if arr_adj != 1.0:
            tx = x0[i] + arr_adj * dx
            ty = y0[i] + arr_adj * dy
            
        length = arr_length[i]
        
        if arr_type == "triangle":
            # Standard arrow head
            vx, vy = -uy, ux
            p1 = [tx - length*ux + 0.2*vx, ty - length*uy + 0.2*vy]
            p2 = [tx - length*ux - 0.2*vx, ty - length*uy - 0.2*vy]
            plt.plot([p1[0], tx, p2[0]], [p1[1], ty, p2[1]], color=colors[i], linewidth=arr_lwd)
        elif arr_type == "curved":
            # Approximated as a small arc
            theta = np.linspace(0, np.pi, 20)
            # Curved heads in 'shape' are half-circles perpendicular to direction
            cx = tx - length * ux
            cy = ty - length * uy
            # This is a simplification of R's curved arrow head
            arc_x = cx + (length*0.5) * np.cos(theta + np.arctan2(uy, ux))
            arc_y = cy + (length*0.5) * np.sin(theta + np.arctan2(uy, ux))
            plt.plot(arc_x, arc_y, color=colors[i], linewidth=arr_lwd)
        elif arr_type == "circle":
            # Small circle at tip
            circle = Circle((tx, ty), radius=length, color=colors[i])
            plt.gca().add_patch(circle)
        elif arr_type == "ellipse":
            # Small ellipse at tip
            ellipse = Ellipse((tx, ty), width=length, height=arr_width, color=colors[i])
            plt.gca().add_patch(ellipse)
        elif arr_type == "T":
            # T-bar at tip
            vx, vy = -uy, ux
            p1 = [tx - length*ux + length*vx, ty - length*uy + length*vy]
            p2 = [tx - length*ux - length*vx, ty - length*uy - length*vy]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=colors[i], linewidth=arr_lwd)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

plt.figure()
plt.plot(0, 0, 'none')
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
plt.plot(0, 0, 'none')
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
plt.plot(0, 0, 'none')
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse", arr_col="grey")

plt.figure()
xx_curve = np.linspace(0, 2*pi + 0.25, 100)
plt.plot(xx_curve, np.sin(xx_curve))
plt.title("Arrows")
x = np.linspace(0, 2*pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

plt.figure()
xx = np.linspace(0, 10*pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 'l')
plt.axis('off')
plt.title("Arrows,  type = 'curved'")
x = np.linspace(0, 10*pi, 20)
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
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])
plt.figure()
plt.plot(0, 0, 'none')
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'curved'")
x0 = np.random.uniform(xlim[0]-1, xlim[1]+0.5, 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)