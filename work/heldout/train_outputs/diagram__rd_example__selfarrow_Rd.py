# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/diagram__rd_example__selfarrow_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__selfarrow_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# Setup plot
# r2py:entity:openplotmat
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("selfarrow")
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.axis('off')

# pos <- coordinates(3, mx = 0.05)
# coordinates(3) typically places points in a circle
# r2py:entity:pos
n = 3
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
pos = np.column_stack([np.cos(angles), np.sin(angles)]) * 0.4 + 0.5
# Adjust mx offset approximation
pos += 0.05 

# text(pos, LETTERS[1:3], cex = 2)
# r2py:entity:text
labels = ['A', 'B', 'C']
for i in range(n):
    ax.text(pos[i, 0], pos[i, 1], labels[i], fontsize=20, 
            ha='center', va='center', fontweight='bold')

# r2py:entity:selfarrow
def draw_self_arrow(pos, path='R', arr_pos=0.5, curve=(0.05, 0.1), lcol='black', arr_type='standard'):
    x, y = pos
    # Approximation of selfarrow geometry
    # Path R = Right, L = Left
    direction = 1 if path == 'R' else -1
    
    # Define arc parameters
    theta1 = -90 if direction == 1 else 90
    theta2 = 90 if direction == 1 else -90
    # Use a small radius for the loop
    radius = 0.08 
    
    # Create the arc
    # We simulate the curve by adjusting the arc's center and span
    arc = Arc((x + (radius * direction), y), 2*radius, 2*radius, 
              theta1=theta1, theta2=theta2, color=lcol, linewidth=2)
    ax.add_patch(arc)
    
    # Add arrowhead (simplified as a small dot or triangle)
    # Calculate point on the arc based on arr_pos
    angle_deg = theta1 + (theta2 - theta1) * arr_pos
    angle_rad = np.radians(angle_deg)
    ax_x = (x + radius * direction) + radius * np.cos(angle_rad)
    ax_y = y + radius * np.sin(angle_rad)
    
    if arr_type == 'triangle':
        ax.plot(ax_x, ax_y, marker='>', color=lcol, markersize=8)
    else:
        ax.plot(ax_x, ax_y, marker='o', color=lcol, markersize=4)

# for (i in 1:3) selfarrow(pos = pos[i, ], path = "R", arr.pos = 0.2, curve = c(0.05, 0.1), lcol = "darkred")
# r2py:entity:selfarrow
for i in range(n):
    draw_self_arrow(pos[i], path="R", arr_pos=0.2, curve=(0.05, 0.1), lcol="darkred")

# for (i in 1:3) selfarrow(pos = pos[i, ], path = "L", arr.pos = 0.7, lcol = "darkblue", curve = c(0.05, 0.05))
# r2py:entity:selfarrow_1
for i in range(n):
    draw_self_arrow(pos[i], path="L", arr_pos=0.7, curve=(0.05, 0.05), lcol="darkblue")

# for (i in 1:3) selfarrow(pos = pos[i, ], path = "L", arr.pos = 0.5, lcol = "darkgreen", code = i, arr.type = "triangle")
# r2py:entity:selfarrow_2
for i in range(n):
    draw_self_arrow(pos[i], path="L", arr_pos=0.5, lcol="darkgreen", arr_type="triangle")

plt.show()