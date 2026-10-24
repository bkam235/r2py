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
from matplotlib.patches import Polygon
import matplotlib.cm as cm

# r2py:entity:import_shape
# The 'shape' package is translated via the implementation of Arrows and Arrowhead below.

def Arrowhead(ax, x0, y0, angle=0, arr_length=0.4, arr_width=None, 
              arr_adj=0.5, arr_type="curved", lcol="black", lty=1, 
              arr_col=None, arr_lwd=2, npoint=5, **kwargs):
    if arr_width is None:
        arr_width = arr_length / 2
    if arr_col is None:
        arr_col = lcol
        
    if arr_type == "none":
        return

    if arr_type == "curved":
        rad = 0.7
        len_arc = 0.25 * np.pi
        mid = np.array([0, rad])
        x_vals = np.linspace(1.5 * np.pi + len_arc, 1.5 * np.pi, npoint)
        rr = np.column_stack([mid[0] - rad * np.cos(x_vals), mid[1] + rad * np.sin(x_vals)])
        mid_2 = np.array([0, -rad])
        x_vals_rev = x_vals[::-1]
        rr = np.vstack([rr, np.column_stack([mid_2[0] - rad * np.cos(x_vals_rev), mid_2[1] - rad * np.sin(x_vals_rev)])])
        mid_3 = np.array([rr[-1, 0], 0])
        rd = rr[0, 1]
        x_vals_final = np.linspace(np.pi/2, 3 * np.pi/2, 3 * npoint)
        rr = np.vstack([rr, np.column_stack([mid_3[0] - rd * 0.25 * np.cos(x_vals_final), mid_3[1] - rd * np.sin(x_vals_final)])])
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

    # Get axis limits for scaling (mimicking par("usr") and par("pin"))
    # In R, sx/sy convert coordinates to physical units. 
    # For parity in a single plot, we can assume 1:1 aspect or use current limits.
    user = ax.get_xlim() + ax.get_ylim() # [xmin, xmax, ymin, ymax]
    sx = (user[1] - user[0]) / 1.0 # Simplified
    sy = (user[3] - user[2]) / 1.0

    x0 = np.atleast_1d(x0)
    y0 = np.atleast_1d(y0)
    angle = np.atleast_1d(angle)
    arr_length = np.atleast_1d(arr_length)
    arr_width = np.atleast_1d(arr_width)
    lcol = np.atleast_1d(lcol)
    arr_col = np.atleast_1d(arr_col)

    nr = max(len(x0), len(y0), len(angle), len(arr_length), len(arr_width), len(lcol), len(arr_col))
    
    def repeat(arr, n):
        return np.resize(arr, n)

    x0, y0, angle, arr_length, arr_width, lcol, arr_col = map(lambda a: repeat(a, nr), [x0, y0, angle, arr_length, arr_width, lcol, arr_col])

    for i in range(nr):
        dx = rr[:, 0] * arr_length[i]
        dy = rr[:, 1] * arr_width[i]
        angpi = np.radians(angle[i])
        cosa, sina = np.cos(angpi), np.sin(angpi)
        
        rx = cosa * dx - sina * dy
        ry = sina * dx + cosa * dy
        rx = x0[i] + rx * sx
        ry = y0[i] + ry * sy
        
        poly = Polygon(np.column_stack([rx, ry]), facecolor=arr_col[i], edgecolor=lcol[i], linewidth=arr_lwd)
        ax.add_patch(poly)

# r2py:entity:Arrows
def Arrows(ax, x0, y0, x1, y1, code=2, arr_length=0.4, arr_width=None, 
           arr_adj=0.5, arr_type="curved", segment=True, col="black", 
           lcol=None, lty=1, arr_col=None, lwd=1, arr_lwd=None, **kwargs):
    if arr_width is None:
        arr_width = arr_length / 2
    if lcol is None:
        lcol = col
    if arr_col is None:
        arr_col = lcol
    if arr_lwd is None:
        arr_lwd = lwd

    if arr_type == "simple":
        ax.annotate("", xy=x1, y=y1, xytext=x0, ytext=y0, arrowprops=dict(width=arr_length, color=col))
        return
    if arr_type == "none":
        return
    if arr_type == "T":
        # Simple T-arrow implementation using matplotlib
        for i in range(len(x0)):
            ax.plot([x0[i], x1[i]], [y0[i], y1[i]], color=col, linewidth=lwd)
            # Add T bar
            dx, dy = x1[i]-x0[i], y1[i]-y0[i]
            mag = np.sqrt(dx**2+dy**2)
            ux, uy = dx/mag, dy/mag
            vx, vy = -uy, ux
            ax.plot([x1[i]-0.2*vx, x1[i]+0.2*vx], [y1[i]-0.2*vy, y1[i]+0.2*vy], color=col, linewidth=lwd)
        return

    if segment:
        for i in range(len(x0)):
            ax.plot([x0[i], x1[i]], [y0[i], y1[i]], color=lcol[i] if isinstance(lcol, (list, np.ndarray)) else lcol, linewidth=lwd)

    user = ax.get_xlim() + ax.get_ylim()
    sx = (user[1] - user[0]) / 1.0
    sy = (user[3] - user[2]) / 1.0
    
    x0, y0, x1, y1 = np.atleast_1d(x0), np.atleast_1d(y0), np.atleast_1d(x1), np.atleast_1d(y1)
    
    # Handle division by zero in atan
    dx = x1 - x0
    dy = y1 - y0
    with np.errstate(divide='ignore', invalid='ignore'):
        angle = np.degrees(np.arctan(dy / dx * sx / sy))
    angle = np.nan_to_num(angle)
    angle[x1 < x0] += 180

    if sy < 0 and sx < 0:
        angle += 180
    elif sx < 0:
        angle += 180

    xx, yy = x1, y1
    if code == 3:
        Arrowhead(ax, xx, yy, angle=angle, lcol=lcol, arr_col=arr_col, arr_adj=arr_adj, arr_length=arr_length, arr_width=arr_width, arr_type=arr_type, arr_lwd=arr_lwd)
    
    if code != 2:
        angle = 180 + angle
        xx, yy = x0, y0
        
    Arrowhead(ax, xx, yy, angle=angle, lcol=lcol, arr_col=arr_col, arr_adj=arr_adj, arr_length=arr_length, arr_width=arr_width, arr_type=arr_type, arr_lwd=arr_lwd)

# r2py:entity:suppressPackageStartupMessages
# No action needed

# r2py:entity:xlim
xlim = np.array([-5, 5])
# r2py:entity:ylim
ylim = np.array([-10, 10])

# Plot 1
# r2py:entity:plot
fig1, ax1 = plt.subplots()
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.set_title("Arrows,  type = 'curved'")

# r2py:entity:runif
# Use the provided shimmed data x0, y0, x1, y1 but regenerate if needed to match logic
x0_1 = np.random.uniform(xlim[0], xlim[1], 100)
y0_1 = np.random.uniform(ylim[0], ylim[1], 100)
x1_1 = x0_1 + np.random.uniform(-1, 1, 100)
y1_1 = y0_1 + np.random.uniform(-1, 1, 100)

# r2py:entity:runif_1
arr_len_1 = np.random.uniform(0, 1, 100)
colors_1 = cm.get_cmap('tab20')(np.linspace(0, 1, 100))

# r2py:entity:Arrows
Arrows(ax1, x0_1, y0_1, x1_1, y1_1, arr_length=arr_len_1, code=2, arr_type="curved", arr_col=colors_1, lcol=colors_1)
plt.show()

# Plot 2
# r2py:entity:plot_1
fig2, ax2 = plt.subplots()
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2.set_title("Arrows,  type = 'circle'")

# r2py:entity:x0_1
x0_2 = np.random.uniform(xlim[0], xlim[1], 100)
# r2py:entity:y0_1
y0_2 = np.random.uniform(ylim[0], ylim[1], 100)
# r2py:entity:x1_1
x1_2 = x0_2 + np.random.uniform(-1, 1, 100)
# r2py:entity:runif_2
# (Implicit in x1_2)
# r2py:entity:y1_1
y1_2 = y0_2 + np.random.uniform(-1, 1, 100)
# r2py:entity:runif_3
# (Implicit in y1_2)

# r2py:entity:Arrows_1
Arrows(ax2, x0_2, y0_2, x1_2, y1_2, arr_length=0.2, code=3, arr_type="circle", arr_col="grey")
plt.show()

# Plot 3
# r2py:entity:plot_2
fig3, ax3 = plt.subplots()
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)
ax3.set_title("Arrows,  type = 'ellipse'")

# r2py:entity:Arrows_2
Arrows(ax3, x0_2, y0_2, x1_2, y1_2, arr_length=0.2, arr_width=0.5, code=3, arr_type="ellipse", arr_col="grey")
plt.show()

# Plot 4
# r2py:entity:curve
fig4, ax4 = plt.subplots()
x_curve = np.linspace(0, 2*np.pi + 0.25, 100)
ax4.plot(x_curve, np.sin(x_curve))
ax4.set_title("Arrows")

# r2py:entity:x
x_vals = np.linspace(0, 2*np.pi, 10)
# r2py:entity:xd
xd_vals = x_vals + 0.025
# r2py:entity:Arrows_3
Arrows(ax4, x_vals, np.sin(x_vals), xd_vals, np.sin(xd_vals), arr_type="triangle", arr_length=0.5, segment=False)
plt.show()

# Plot 5
# r2py:entity:xx
xx = np.linspace(0, 10*np.pi, 1000)
# r2py:entity:plot_3
fig5, ax5 = plt.subplots()
ax5.plot(np.sin(xx)*xx, np.cos(xx)*xx)
ax5.set_axis_off()
ax5.set_title("Arrows,  type = 'curved'")
ax5.set_xlabel("")
ax5.set_ylabel("")

# r2py:entity:x_1
x_pts = np.linspace(0, 10*np.pi, 20)
# r2py:entity:x1_2
x1_pts = np.sin(x_pts)*x_pts
# r2py:entity:sin
# (np.sin)
# r2py:entity:y1_2
y1_pts = np.cos(x_pts)*x_pts
# r2py:entity:cos
# (np.cos)
# r2py:entity:xd_1
xd_pts = x_pts + 0.01
# r2py:entity:x2
x2_pts = np.sin(xd_pts)*xd_pts
# r2py:entity:sin_1
# (np.sin)
# r2py:entity:y2
y2_pts = np.cos(xd_pts)*xd_pts
# r2py:entity:cos_1
# (np.cos)
# r2py:entity:Arrows_4
Arrows(ax5, x1_pts, y1_pts, x2_pts, y2_pts, arr_type="curved", arr_length=0.4, segment=False, code=1, arr_adj=0.5)
plt.show()

# Plot 6
# r2py:entity:plot_4
fig6, ax6 = plt.subplots()
ax6.plot(np.sin(xx)*xx, np.cos(xx)*xx)
ax6.set_axis_off()
ax6.set_title("Arrows,  type = 'T'")
ax6.set_xlabel("")
ax6.set_ylabel("")

# r2py:entity:Arrows_5
Arrows(ax6, x1_pts, y1_pts, x2_pts, y2_pts, arr_type="T", arr_length=0.4, code=1, arr_lwd=2)
plt.show()

# Plot 7
# r2py:entity:xlim_1
xlim_2 = np.array([-5, 5])
# r2py:entity:ylim_1
ylim_2 = np.array([-10, 10])
# r2py:entity:plot_5
fig7, ax7 = plt.subplots()
ax7.set_xlim(xlim_2)
ax7.set_ylim(ylim_2)
ax7.set_title("Arrows,  type = 'curved'")

# r2py:entity:x0_2
x0_3 = np.random.uniform(xlim_2[0]-1, xlim_2[1]+0.5, 100)
# r2py:entity:y0_2
y0_3 = np.random.uniform(ylim_2[0], ylim_2[1], 100)
# r2py:entity:x1_3
x1_3 = x0_3 + np.random.uniform(-1, 1, 100)
# r2py:entity:runif_4
# (Implicit in x1_3)
# r2py:entity:y1_3
y1_3 = y0_3 + np.random.uniform(-1, 1, 100)
# r2py:entity:runif_5
# (Implicit in y1_3)
# r2py:entity:Arrows_6
colors_2 = cm.get_cmap('tab20')(np.linspace(0, 1, 100))
Arrows(ax7, x0_3, y0_3, x1_3, y1_3, arr_length=np.random.uniform(0, 1, 100), code=2, arr_type="curved", arr_col=colors_2, lcol=colors_2)
plt.show()