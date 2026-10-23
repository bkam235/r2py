import numpy as np
import matplotlib.pyplot as plt

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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=None, code=None, 
           arr_type="triangle", arr_col="black", lcol=None, 
           arr_lwd=1, segment=True, arr_adj=0, xpd=False):
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    if isinstance(arr_length, (int, float)):
        arr_length = np.full(len(x0), arr_length)
    
    # Handle colors: R's 1:100 colors map to a colormap
    if isinstance(arr_col, (int, np.integer)) or (isinstance(arr_col, list) and len(arr_col) > 0 and isinstance(arr_col[0], (int, np.integer))):
        cmap = plt.get_cmap('tab20')
        if isinstance(arr_col, (int, np.integer)):
            arr_col = [cmap((arr_col - 1) % 20) for _ in range(len(x0))]
        else:
            arr_col = [cmap((val - 1) % 20) for val in arr_col]
    elif isinstance(arr_col, str):
        arr_col = [arr_col] * len(x0)

    if lcol is not None:
        if isinstance(lcol, (int, np.integer)) or (isinstance(lcol, list) and len(lcol) > 0 and isinstance(lcol[0], (int, np.integer))):
            cmap = plt.get_cmap('tab20')
            if isinstance(lcol, (int, np.integer)):
                lcol = [cmap((lcol - 1) % 20) for _ in range(len(x0))]
            else:
                lcol = [cmap((val - 1) % 20) for val in lcol]
        elif isinstance(lcol, str):
            lcol = [lcol] * len(x0)
    else:
        lcol = arr_col

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        vx, vy = -uy, ux
        
        # Main line segment
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=lcol[i], linewidth=arr_lwd)
        
        # Arrow head
        al = arr_length[i]
        if arr_type == "triangle":
            # Standard triangle head
            p1 = [x1[i] - al*ux + 0.2*vx, y1[i] - al*uy + 0.2*vy]
            p2 = [x1[i] - al*ux - 0.2*vx, y1[i] - al*uy - 0.2*vy]
            plt.plot([p1[0], x1[i], p2[0]], [p1[1], y1[i], p2[1]], color=arr_col[i], linewidth=arr_lwd)
        elif arr_type == "curved":
            # Approximate curved head as a small arc
            theta = np.linspace(0, np.pi, 10)
            hx = x1[i] - al * np.cos(theta) * ux + 0.1 * np.sin(theta) * vx
            hy = y1[i] - al * np.sin(theta) * uy + 0.1 * np.sin(theta) * vy
            plt.plot(hx, hy, color=arr_col[i], linewidth=arr_lwd)
        elif arr_type == "circle":
            # Circle at tip
            theta = np.linspace(0, 2*np.pi, 20)
            hx = x1[i] + al * np.cos(theta) * 0.1
            hy = y1[i] + al * np.sin(theta) * 0.1
            plt.plot(hx, hy, color=arr_col[i], linewidth=arr_lwd)
        elif arr_type == "ellipse":
            # Ellipse at tip
            theta = np.linspace(0, 2*np.pi, 20)
            w = arr_width if arr_width else 0.5
            hx = x1[i] + al * np.cos(theta) * 0.1
            hy = y1[i] + w * np.sin(theta) * 0.1
            plt.plot(hx, hy, color=arr_col[i], linewidth=arr_lwd)
        elif arr_type == "T":
            # T-bar head
            p1 = [x1[i] - al*ux + 0.2*vx, y1[i] - al*uy + 0.2*vy]
            p2 = [x1[i] - al*ux - 0.2*vx, y1[i] - al*uy - 0.2*vy]
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=arr_col[i], linewidth=arr_lwd)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

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

plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")

plt.figure()
xx_curve = np.linspace(0, 2*np.pi+0.25, 100)
plt.plot(xx_curve, np.sin(xx_curve))
plt.title("Arrows")
x = np.linspace(0, 2*np.pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx, 
         xlabel="", ylabel="", main="Arrows,  type = 'curved'") # Note: matplotlib uses plt.title
plt.title("Arrows,  type = 'curved'")
plt.axis('off')
x = np.linspace(0, 10*np.pi, 20)
x1 = np.sin(x)*x
y1 = np.cos(x)*x
xd = x + 0.01
x2 = np.sin(xd)*xd
y2 = np.cos(xd)*xd
Arrows(x1, y1, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)

plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.title("Arrows,  type = 'T'")
plt.axis('off')
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

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
Arrows(x0, y0, x1, y1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)