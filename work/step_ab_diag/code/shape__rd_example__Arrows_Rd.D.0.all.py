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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=None, code=1, arr_type='triangle', 
           arr_col='black', lcol=None, segment=True, arr_adj=0.5, arr_lwd=1, xpd=False):
    x0, y0, x1, y1 = np.asarray(x0), np.asarray(y0), np.asarray(x1), np.asarray(y1)
    
    if isinstance(arr_length, (int, float)):
        arr_length = np.full(len(x0), arr_length)
    
    # Map R colors (1:100) to a colormap if numeric
    def get_color(c, idx):
        if isinstance(c, (list, np.ndarray)):
            val = c[idx]
            if isinstance(val, (int, float)):
                return plt.cm.tab20(val / 20 % 1)
            return val
        return c

    for i in range(len(x0)):
        dx, dy = x1[i] - x0[i], y1[i] - y0[i]
        mag = np.sqrt(dx**2 + dy**2)
        if mag == 0: continue
        ux, uy = dx/mag, dy/mag
        vx, vy = -uy, ux
        
        c_line = get_color(lcol if lcol is not None else arr_col, i)
        c_head = get_color(arr_col, i)
        
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=c_line, linewidth=arr_lwd)
        
        # Head construction
        if arr_type == 'triangle':
            # Simple triangle head
            h_len = arr_length[i]
            plt.plot([x1[i], x1[i] - h_len*ux + 0.2*vx], [y1[i], y1[i] - h_len*uy + 0.2*vy], color=c_head, linewidth=arr_lwd)
            plt.plot([x1[i], x1[i] - h_len*ux - 0.2*vx], [y1[i], y1[i] - h_len*uy - 0.2*vy], color=c_head, linewidth=arr_lwd)
        elif arr_type == 'curved':
            theta = np.linspace(0, np.pi, 15)
            hx = x1[i] - arr_length[i] * np.cos(theta)*ux + 0.1 * np.sin(theta)*vx
            hy = y1[i] - arr_length[i] * np.sin(theta)*uy + 0.1 * np.sin(theta)*vy
            plt.plot(hx, hy, color=c_head, linewidth=arr_lwd)
        elif arr_type == 'circle' or arr_type == 'ellipse':
            theta = np.linspace(0, 2*np.pi, 20)
            w = arr_width if arr_width else 0.1
            hx = x1[i] + arr_length[i] * np.cos(theta)*ux + w * np.sin(theta)*vx
            hy = y1[i] + arr_length[i] * np.sin(theta)*uy + w * np.sin(theta)*vy
            plt.plot(hx, hy, color=c_head, linewidth=arr_lwd)
        elif arr_type == 'T':
            h_len = arr_length[i]
            plt.plot([x1[i] - h_len*ux - 0.2*vx, x1[i] - h_len*ux + 0.2*vx], 
                     [y1[i] - h_len*uy - 0.2*vy, y1[i] - h_len*uy + 0.2*vy], color=c_head, linewidth=arr_lwd)

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
plt.show()

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
plt.show()

plt.figure()
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
plt.title("Arrows,  type = 'ellipse'")
Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")
plt.show()

plt.figure()
xx_c = np.linspace(0, 2*pi+0.25, 100)
plt.plot(xx_c, np.sin(xx_c))
plt.title("Arrows")
x = np.linspace(0, 2*pi, 10)
xd = x + 0.025
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)
plt.show()

xx = np.linspace(0, 10*pi, 1000)
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.axis('off')
plt.title("Arrows,  type = 'curved'")
x = np.linspace(0, 10*pi, 20)
x1 = np.sin(x)*x
y1 = np.cos(x)*x
xd = x+0.01
x2 = np.sin(xd)*xd
y2 = np.cos(xd)*xd
Arrows(x1, y1, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)
plt.show()

plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.axis('off')
plt.title("Arrows,  type = 'T'")
Arrows(x1, y1, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)
plt.show()

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
plt.show()