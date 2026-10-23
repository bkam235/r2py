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

def Arrows(x0, y0, x1, y1, arr_length=0.2, arr_width=0.5, code=1, arr_type='triangle', 
           arr_col='black', lcol=None, segment=True, arr_adj=1, arr_lwd=1, xpd=False):
    """Implementation of shape::Arrows for matplotlib."""
    x0 = np.asarray(x0)
    y0 = np.asarray(y0)
    x1 = np.asarray(x1)
    y1 = np.asarray(y1)
    
    # Handle scalar or array for colors/lengths
    if isinstance(arr_col, (int, float)):
        arr_col = plt.cm.tab10(arr_col / 10.0 if arr_col <= 10 else arr_col % 10 / 10.0)
    if isinstance(lcol, (int, float)):
        lcol = plt.cm.tab10(lcol / 10.0 if lcol <= 10 else lcol % 10 / 10.0)
    
    colors = arr_col if isinstance(arr_col, (list, np.ndarray)) else [arr_col] * len(x0)
    line_colors = lcol if lcol is not None else colors

    for i in range(len(x0)):
        dx = x1[i] - x0[i]
        dy = y1[i] - y0[i]
        dist = np.sqrt(dx**2 + dy**2)
        if dist == 0: continue
        ux, uy = dx/dist, dy/dist
        
        # Calculate arrow placement
        length = arr_length[i] if isinstance(arr_length, (list, np.ndarray)) else arr_length
        
        # Line segment
        if segment:
            plt.plot([x0[i], x1[i]], [y0[i], y1[i]], color=line_colors[i], linewidth=arr_lwd)
        
        # Head coordinates
        # R code=1: head at (x1, y1), code=2: head at (x0, y0), code=3: both
        heads = []
        if code & 1: heads.append((x1[i], y1[i], ux, uy))
        if code & 2: heads.append((x0[i], y0[i], -ux, -uy))
        
        for hx, hy, hux, huy in heads:
            # Adjustment for head position
            curr_x = hx - hux * (length * (1 - arr_adj) if arr_type == 'curved' else 0)
            curr_y = hy - huy * (length * (1 - arr_adj) if arr_type == 'curved' else 0)
            
            if arr_type == 'triangle':
                vx, vy = -huy, hux
                p1 = [curr_x, curr_y]
                p2 = [curr_x - length*hux + 0.2*vx, curr_y - length*huy + 0.2*vy]
                p3 = [curr_x - length*hux - 0.2*vx, curr_y - length*huy - 0.2*vy]
                plt.gca().add_patch(Polygon([p1, p2, p3], color=colors[i], fill=True))
            elif arr_type == 'circle':
                circle = plt.Circle((curr_x, curr_y), length/2, color=colors[i])
                plt.gca().add_patch(circle)
            elif arr_type == 'ellipse':
                ellipse = Ellipse((curr_x, curr_y), length, length*arr_width, angle=np.degrees(np.arctan2(huy, hux)), color=colors[i])
                plt.gca().add_patch(ellipse)
            elif arr_type == 'curved':
                # Curved arrows are usually arcs in shape package
                theta1, theta2 = np.pi/2, -np.pi/2 # Semi-circle
                arc = Arc((curr_x - length*hux, curr_y - length*huy), length*2, length*2, 
                          angle=np.degrees(np.arctan2(huy, hux)), theta1=theta1, theta2=theta2, color=colors[i])
                plt.gca().add_patch(arc)
            elif arr_type == 'T':
                vx, vy = -huy, hux
                plt.plot([curr_x - length*hux + 0.2*vx, curr_x - length*hux - 0.2*vx],
                         [curr_y - length*huy + 0.2*vy, curr_y - length*huy - 0.2*vy], 
                         color=colors[i], linewidth=arr_lwd)

xlim = np.array([-5, 5])
ylim = np.array([-10, 10])

# Plot 1
plt.figure()
plt.title("Arrows,  type = 'curved'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
x0_1 = np.random.uniform(xlim[0], xlim[1], 100)
y0_1 = np.random.uniform(ylim[0], ylim[1], 100)
x1_1 = x0_1 + np.random.uniform(-1, 1, 100)
y1_1 = y0_1 + np.random.uniform(-1, 1, 100)
Arrows(x0_1, y0_1, x1_1, y1_1, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101))

# Plot 2
plt.figure()
plt.title("Arrows,  type = 'circle'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
x0_2 = np.random.uniform(xlim[0], xlim[1], 100)
y0_2 = np.random.uniform(ylim[0], ylim[1], 100)
x1_2 = x0_2 + np.random.uniform(-1, 1, 100)
y1_2 = y0_2 + np.random.uniform(-1, 1, 100)
Arrows(x0_2, y0_2, x1_2, y1_2, arr_length=0.2, code=3, 
       arr_type="circle", arr_col="grey")

# Plot 3
plt.figure()
plt.title("Arrows,  type = 'ellipse'")
plt.xlim(xlim[0], xlim[1])
plt.ylim(ylim[0], ylim[1])
Arrows(x0_2, y0_2, x1_2, y1_2, arr_length=0.2, arr_width=0.5, 
       code=3, arr_type="ellipse",  arr_col="grey")

# Plot 4
plt.figure()
plt.title("Arrows")
x_vals = np.linspace(0, 2*np.pi + 0.25, 100)
plt.plot(x_vals, np.sin(x_vals))
x_seq = np.linspace(0, 2*np.pi, 10)
xd = x_seq + 0.025
Arrows(x_seq, np.sin(x_seq), xd, np.sin(xd), arr_type="triangle", 
       arr_length=0.5, segment=False)

# Plot 5
plt.figure()
xx = np.linspace(0, 10*np.pi, 1000)
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.title("Arrows,  type = 'curved'")
plt.xlabel(""); plt.ylabel("")
plt.axis('off')
x_seq2 = np.linspace(0, 10*np.pi, 20)
x1_3 = np.sin(x_seq2)*x_seq2
y1_3 = np.cos(x_seq2)*x_seq2
xd_2 = x_seq2 + 0.01
x2 = np.sin(xd_2)*xd_2
y2 = np.cos(xd_2)*xd_2
Arrows(x1_3, y1_3, x2, y2, arr_type="curved", arr_length=0.4, 
       segment=False, code=1, arr_adj=0.5)

# Plot 6
plt.figure()
plt.plot(np.sin(xx)*xx, np.cos(xx)*xx)
plt.title("Arrows,  type = 'T'")
plt.xlabel(""); plt.ylabel("")
plt.axis('off')
Arrows(x1_3, y1_3, x2, y2, arr_type="T", arr_length=0.4, 
       code=1, arr_lwd=2)

# Plot 7
plt.figure()
plt.title("Arrows,  type = 'curved'")
xlim_final = np.array([-5, 5])
ylim_final = np.array([-10, 10])
plt.xlim(xlim_final[0], xlim_final[1])
plt.ylim(ylim_final[0], ylim_final[1])
x0_3 = np.random.uniform(xlim_final[0]-1, xlim_final[1]+0.5, 100)
y0_3 = np.random.uniform(ylim_final[0], ylim_final[1], 100)
x1_4 = x0_3 + np.random.uniform(-1, 1, 100)
y1_4 = y0_3 + np.random.uniform(-1, 1, 100)
Arrows(x0_3, y0_3, x1_4, y1_4, arr_length=np.random.uniform(0, 1, 100), code=2, 
       arr_type="curved", arr_col=np.arange(1, 101), lcol=np.arange(1, 101), xpd=True)