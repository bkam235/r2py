import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

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

def Arrowhead(x0, y0, angle=0, arr_length=0.4, arr_width=None, arr_adj=0.5, 
              arr_type="curved", lcol="black", lty=1, arr_col=None, arr_lwd=2, 
              npoint=5, ax=None, **kwargs):
    if arr_width is None:
        arr_width = arr_length / 2
    if arr_col is None:
        arr_col = lcol

    if arr_type == "none":
        return

    if arr_type == "curved":
        rad = 0.7
        len_val = 0.25 * np.pi
        mid_start = np.array([0, rad])
        x_vals = np.linspace(1.5 * np.pi + len_val, 1.5 * np.pi, npoint)
        rr = np.column_stack([mid_start[0] - rad * np.cos(x_vals), mid_start[1] + rad * np.sin(x_vals)])
        mid_end = np.array([0, -rad])
        x_vals_rev = x_vals[::-1]
        rr = np.vstack([rr, np.column_stack([mid_end[0] - rad * np.cos(x_vals_rev), mid_end[1] - rad * np.sin(x_vals_rev)])])
        mid_final = np.array([rr[-1, 0], 0])
        rd = rr[0, 1]
        x_final = np.linspace(np.pi/2, 3 * np.pi/2, 3 * npoint)
        rr = np.vstack([rr, np.column_stack([mid_final[0] - rd * 0.25 * np.cos(x_final), mid_final[1] - rd * np.sin(x_final)])])
        rr[:, 0] *= 2.6
        rr[:, 1] *= 3.45
    elif arr_type == "triangle":
        x_tri = np.array([-0.2, 0, -0.2])
        y_tri = np.array([-0.1, 0, 0.1])
        rr = 6.22 * np.column_stack([x_tri, y_tri])
    elif arr_type in ["circle", "ellipse"]:
        if arr_type == "circle":
            arr_width = arr_length
        rad = 0.1
        mid = np.array([-rad, 0])
        x_circ = np.linspace(0, 2 * np.pi, 15 * npoint)
        rr = 6.22 * np.column_stack([mid[0] + rad * np.sin(x_circ), mid[1] + rad * np.cos(x_circ)])
    else:
        return

    if arr_adj == 0.5:
        rr[:, 0] -= np.min(rr[:, 0]) / 2
    elif arr_adj == 0:
        rr[:, 0] -= np.min(rr[:, 0])

    user = ax.get_xlim() + ax.get_ylim()
    sx = (user[1] - user[0]) / 1.0
    sy = (user[3] - user[2]) / 1.0

    x0 = np.atleast_1d(x0)
    y0 = np.atleast_1d(y0)
    angle = np.atleast_1d(angle)
    arr_length = np.atleast_1d(arr_length)
    arr_width = np.atleast_1d(arr_width)
    lcol = np.atleast_1d(lcol)
    arr_col = np.atleast_1d(arr_col)

    nr = max(len(x0), len(y0), len(angle), len(arr_length), len(arr_width), len(lcol), len(arr_col))
    
    def repeat(a, length):
        return np.resize(a, length)

    x0 = repeat(x0, nr)
    y0 = repeat(y0, nr)
    angle = repeat(angle, nr)
    arr_length = repeat(arr_length, nr)
    arr_width = repeat(arr_width, nr)
    lcol = repeat(lcol, nr)
    arr_col = repeat(arr_col, nr)

    cmap = plt.get_cmap('jet')

    for i in range(nr):
        dx = rr[:, 0] * arr_length[i]
        dy = rr[:, 1] * arr_width[i]
        angpi = angle[i] / 180 * np.pi
        cosa, sina = np.cos(angpi), np.sin(angpi)
        
        rx = cosa * dx - sina * dy
        ry = sina * dx + cosa * dy
        
        final_x = x0[i] + rx * sx
        final_y = y0[i] + ry * sy
        
        c_face = cmap((arr_col[i]-1)/100) if isinstance(arr_col[i], (int, np.integer)) else arr_col[i]
        c_edge = cmap((lcol[i]-1)/100) if isinstance(lcol[i], (int, np.integer)) else lcol[i]

        poly = Polygon(np.column_stack([final_x, final_y]), 
                      facecolor=c_face, edgecolor=c_edge, 
                      linewidth=arr_lwd, clip_on=False)
        ax.add_patch(poly)

def Arrows(x0, y0, x1, y1, code=2, arr_length=0.4, arr_width=None, 
            arr_adj=0.5, arr_type="curved", segment=True, col="black", 
            lcol=None, lty=1, arr_col=None, lwd=1, arr_lwd=None, ax=None, **kwargs):
    if arr_width is None:
        arr_width = arr_length / 2
    if lcol is None:
        lcol = col
    if arr_col is None:
        arr_col = lcol
    if arr_lwd is None:
        arr_lwd = lwd

    x0, y0, x1, y1 = np.atleast_1d(x0), np.atleast_1d(y0), np.atleast_1d(x1), np.atleast_1d(y1)

    if arr_type == "simple":
        ax.quiver(x0, y0, x1-x0, y1-y0, angles='xy', scale_units='xy', scale=1, color=col, width=0.005)
        return
    if arr_type == "none":
        return
    if arr_type == "T":
        ax.quiver(x0, y0, x1-x0, y1-y0, angles='xy', scale_units='xy', scale=1, color=col, width=0.005)
        return

    if segment:
        cmap = plt.get_cmap('jet')
        for i in range(len(x0)):
            c_line = cmap((lcol[i]-1)/100) if isinstance(lcol, np.ndarray) and isinstance(lcol[i], (int, np.integer)) else lcol
            ax.plot([x0[i], x1[i]], [y0[i], y1[i]], color=c_line, 
                    linestyle='-' if lty == 1 else '--', linewidth=lwd)

    user = ax.get_xlim() + ax.get_ylim()
    sx = (user[1] - user[0]) / 1.0
    sy = (user[3] - user[2]) / 1.0
    
    angle = np.arctan2((y1 - y0), (x1 - x0)) * 180 / np.pi
    mask = x1 < x0
    angle[mask] += 180
    
    xx, yy = x1.copy(), y1.copy()
    
    if code == 3:
        Arrowhead(xx, yy, angle=angle, lcol=lcol, arr_col=arr_col, arr_adj=arr_adj, 
                  lty=lty, arr_length=arr_length, arr_width=arr_width, arr_type=arr_type, 
                  arr_lwd=arr_lwd, ax=ax)
    
    if code != 2:
        angle = 180 + angle
        xx, yy = x0, y0
        
    Arrowhead(xx, yy, angle=angle, lcol=lcol, arr_col=arr_col, arr_adj=arr_adj, 
              lty=lty, arr_length=arr_length, arr_width=arr_width, arr_type=arr_type, 
              arr_lwd=arr_lwd, ax=ax)

# r2py:entity:suppressPackageStartupMessages
# (Already handled by not calling any package that produces startup messages)
# r2py:entity:import_shape
# (shape is translated here via Arrows function)

# r2py:entity:xlim
xlim = np.array([-5, 5])
# r2py:entity:ylim
ylim = np.array([-10, 10])

# Plot 1
# r2py:entity:plot
plt.figure()
ax1 = plt.gca()
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.set_title("Arrows,  type = 'curved'")
# r2py:entity:runif
x0 = np.random.uniform(xlim[0], xlim[1], 100)
y0 = np.random.uniform(ylim[0], ylim[1], 100)
# r2py:entity:runif_1
x1 = x0 + np.random.uniform(-1, 1, 100)
y1 = y0 + np.random.uniform(-1, 1, 100)
# r2py:entity:Arrows
Arrows(x0, y0, x1, y1, code=2, arr_length=np.random.uniform(0, 1, 100), 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), ax=ax1)

# Plot 2
# r2py:entity:plot_1
plt.figure()
ax2 = plt.gca()
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2.set_title("Arrows,  type = 'circle'")
# r2py:entity:runif_2
x0_2 = np.random.uniform(xlim[0], xlim[1], 100)
y0_2 = np.random.uniform(ylim[0], ylim[1], 100)
# r2py:entity:runif_3
x1_2 = x0_2 + np.random.uniform(-1, 1, 100)
y1_2 = y0_2 + np.random.uniform(-1, 1, 100)
# r2py:entity:Arrows_1
Arrows(x0_2, y0_2, x1_2, y1_2, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey", ax=ax2)

# Plot 3
# r2py:entity:plot_2
plt.figure()
ax3 = plt.gca()
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)
ax3.set_title("Arrows,  type = 'ellipse'")
# r2py:entity:Arrows_2
Arrows(x0_2, y0_2, x1_2, y1_2, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey", ax=ax3)

# Plot 4
# r2py:entity:curve
plt.figure()
ax4 = plt.gca()
x_range = np.linspace(0, 2 * np.pi + 0.25, 100)
ax4.plot(x_range, np.sin(x_range))
ax4.set_title("Arrows")
# r2py:entity:x
x = np.linspace(0, 2 * np.pi, 10)
# r2py:entity:xd
xd = x + 0.025
# r2py:entity:Arrows_3
Arrows(x, np.sin(x), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False, ax=ax4)

# Plot 5
# r2py:entity:plot_3
plt.figure()
ax5 = plt.gca()
# r2py:entity:xx
xx = np.linspace(0, 10 * np.pi, 1000)
ax5.plot(np.sin(xx) * xx, np.cos(xx) * xx)
ax5.set_title("Arrows,  type = 'curved'")
ax5.set_xlabel("")
ax5.set_ylabel("")
# r2py:entity:x_1
x_5 = np.linspace(0, 10 * np.pi, 20)
# r2py:entity:x1_2
x1_5 = np.sin(x_5) * x_5
# r2py:entity:sin
# r2py:entity:cos
# r2py:entity:y1_2
y1_5 = np.cos(x_5) * x_5
# r2py:entity:xd_1
xd_5 = x_5 + 0.01
# r2py:entity:sin_1
# r2py:entity:x2
x2 = np.sin(xd_5) * xd_5
# r2py:entity:cos_1
# r2py:entity:y2
y2 = np.cos(xd_5) * xd_5
# r2py:entity:Arrows_4
Arrows(x1_5, y1_5, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5, ax=ax5)

# Plot 6
# r2py:entity:plot_4
plt.figure()
ax6 = plt.gca()
ax6.plot(np.sin(xx) * xx, np.cos(xx) * xx)
ax6.set_title("Arrows,  type = 'T'")
ax6.set_xlabel("")
ax6.set_ylabel("")
# r2py:entity:Arrows_5
Arrows(x1_5, y1_5, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2, ax=ax6)

# Plot 7
# r2py:entity:plot_5
plt.figure()
ax7 = plt.gca()
# r2py:entity:xlim_1
xlim_val2 = np.array([-5, 5])
# r2py:entity:ylim_1
ylim_val2 = np.array([-10, 10])
ax7.set_xlim(xlim_val2)
ax7.set_ylim(ylim_val2)
ax7.set_title("Arrows,  type = 'curved'")
# r2py:entity:x0_2
x0_3 = np.random.uniform(xlim_val2[0]-1, xlim_val2[1]+0.5, 100)
# r2py:entity:y0_2
y0_3 = np.random.uniform(ylim_val2[0], ylim_val2[1], 100)
# r2py:entity:runif_4
# r2py:entity:runif_5
x1_3 = x0_3 + np.random.uniform(-1, 1, 100)
# r2py:entity:y1_3
y1_3 = y0_3 + np.random.uniform(-1, 1, 100)
# r2py:entity:Arrows_6
Arrows(x0_3, y0_3, x1_3, y1_3, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), ax=ax7)