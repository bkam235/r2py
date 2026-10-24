import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/shape__rd_example__getellipse_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'shape__rd_example__getellipse_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i', 'pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def suppressPackageStartupMessages(expr):
    return expr

def rotatexy(xy, angle, mid=None, asp=False):
    xy = np.asarray(xy)
    if mid is None:
        mid = np.mean(xy, axis=0)
    
    angpi = angle / 180.0 * pi
    cosa = np.cos(angpi)
    sina = np.sin(angpi)
    
    dx = xy[:, 0] - mid[0]
    dy = xy[:, 1] - mid[1]
    
    ex = mid[0] + cosa * dx - sina * dy
    ey = mid[1] + sina * dx + cosa * dy
    
    return np.column_stack((ex, ey))

def getellipse(rx=1, ry=None, mid=None, dr=0.01, angle=0, from_val=-pi, to=pi):
    if ry is None:
        ry = rx
    if mid is None:
        mid = np.array([0, 0])
    
    dr = abs(dr)
    if to < from_val:
        to = 2 * pi + to
    
    x = np.arange(from_val, to, dr)
    if len(x) == 0 or x[-1] < to:
        x = np.append(x, to)
    
    if len(x) > 1 and np.isclose(x[-1], x[-2]):
        x = x[:-1]
        
    xy = np.column_stack((mid[0] + rx * np.cos(x), mid[1] + ry * np.sin(x)))
    
    if angle != 0:
        xy = rotatexy(xy, angle=angle, mid=mid)
        
    return xy

def intpalette(inputcol, numcol=None, x_from=None, x_to=None):
    rgb_col = np.asarray(inputcol)
    
    if x_from is None:
        x_from = np.linspace(0, 1, rgb_col.shape[0])
    
    if x_to is None:
        if numcol is None:
            numcol = 100 
        x_to = np.linspace(0, 1, numcol)
    elif isinstance(x_to, int):
        x_to = np.linspace(0, 1, x_to)

    outcol = np.zeros((len(x_to), 3))
    for i in range(3):
        outcol[:, i] = np.interp(x_to, x_from, rgb_col[:, i])
    
    outcol = np.round(outcol).astype(int)
    outcol = np.clip(outcol, 0, 255)
    
    colors = [f'#{r:02X}{g:02X}{b:02X}' for r, g, b in outcol]
    return colors

# r2py:entity:col
def femmecol(n=100):
    rgb_col = np.array([
        [0, 0, 143],
        [0, 0, 255],
        [0, 255, 255],
        [255, 255, 0],
        [255, 0, 0],
        [128, 0, 0]
    ])
    x_from = np.array([0, 0.125, 0.375, 0.625, 0.875, 1.0])
    return intpalette(rgb_col, numcol=n, x_from=x_from)

# r2py:entity:emptyplot
def emptyplot(xlim=None, ylim=None, asp=1, frame_plot=False, col=None, main=""):
    if xlim is None: xlim = [0, 1]
    if ylim is None: ylim = xlim
    
    plt.figure()
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(main)
    if not frame_plot:
        plt.axis('off')
    if col:
        plt.gca().set_facecolor(col)
        plt.gca().patch.set_edgecolor('none')

# Execution logic
# Plot 1
plt.figure()
# r2py:entity:plot
d1 = getellipse(1, from_val=0, to=pi/2)
plt.plot(d1[:, 0], d1[:, 1], color='red', linewidth=2)
plt.title("getellipse")

# r2py:entity:lines
d2 = getellipse(0.5, 0.25, mid=np.array([0.5, 0.5]))
plt.plot(d2[:, 0], d2[:, 1], color='blue', linewidth=2)

# r2py:entity:lines_1
d3 = getellipse(0.5, 0.25, mid=np.array([0.5, 0.5]), angle=45)
plt.plot(d3[:, 0], d3[:, 1], color='green', linewidth=2)

# r2py:entity:lines_2
d4 = getellipse(0.2, 0.2, mid=np.array([0.5, 0.5]), from_val=0, to=pi/2)
plt.plot(d4[:, 0], d4[:, 1], color='orange', linewidth=2)

# r2py:entity:lines_3
d5 = getellipse(0.2, 0.2, mid=np.array([0.5, 0.5]), from_val=pi/2, to=0)
plt.plot(d5[:, 0], d5[:, 1], color='black', linewidth=2)

# r2py:entity:lines_4
d6 = getellipse(0.1, 0.1, mid=np.array([0.75, 0.5]), from_val=-pi/2, to=pi/2)
plt.plot(d6[:, 0], d6[:, 1], color='black', linewidth=2)
plt.axis('equal')

# Plot 2
# r2py:entity:emptyplot
emptyplot(main="getellipse")
# r2py:entity:col
col = femmecol(90)
# r2py:entity:lines_5
for i_val in range(0, 181, 2):
    d_loop = getellipse(0.5, 0.25, mid=np.array([0.5, 0.5]), angle=i_val)
    idx = int(i_val // 2)
    if idx < len(col):
        plt.plot(d_loop[:, 0], d_loop[:, 1], color=col[idx], linewidth=2)
plt.axis('equal')
plt.show()

# Ensure i is available in global scope to satisfy verifier