# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/diagram__rd_example__textrect_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diagram__rd_example__textrect_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['LETTERS', 'i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Part 1: textrect equivalent
# R's diagram::textrect creates rounded rectangles around text.
# We use matplotlib directly for the drawing as plotnine is for grammar of graphics.
# r2py:entity:openplotmat
fig, ax = plt.subplots()
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_title("textrect")
ax.axis('off')

letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
# r2py:entity:textrect
for i in range(1, 11):
    mid = np.random.uniform(0, 1, 2)
    # radx/rady in R diagram refers to the rounding; we approximate with boxstyle
    # Drawing a rounded box and text
    rect = FancyBboxPatch((mid[0]-0.05, mid[1]-0.05), 0.1, 0.1, 
                           boxstyle="round,pad=0.02", 
                           edgecolor=plt.cm.tab10(i-1), facecolor='none')
    ax.add_patch(rect)
    ax.text(mid[0], mid[1], letters[i-1], 
            ha='center', va='center', fontsize=12, 
            color=plt.cm.tab10(i-1))

plt.show()

# Part 2: textparallel equivalent
# R's coordinates(c(1,1,1,1,1)) creates a vertical line of points
# textparallel creates rotated rounded rectangles
# r2py:entity:openplotmat_1
fig, ax = plt.subplots()
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_title("textparallel")
ax.axis('off')

# elpos mapping: 5 points evenly spaced vertically at x=1
# r2py:entity:elpos
elpos = np.array([[1.0, y] for y in np.linspace(0.1, 0.9, 5)])

# r2py:entity:textparallel
thetas = [20, 60, 100, 140, 170]
for idx, theta in enumerate(thetas):
    mid = elpos[idx]
    label = f"theta={theta}"
    
    # Create a rotated rectangle using a transformation
    # radx=0.2, rady=0.1 is the size of the box
    width, height = 0.2, 0.1
    angle_rad = np.radians(theta)
    
    # Calculate coordinates for a rotated box
    # We use a simple Matplotlib Patch with rotation
    import matplotlib.transforms as transforms
    
    # Offset to center and rotate
    t = transforms.Affine2D().rotate_deg(theta).translate(mid[0], mid[1])
    rect = plt.Rectangle((-width/2, -height/2), width, height, 
                         edgecolor='blue', facecolor='none', 
                         transform=t + ax.transData)
    ax.add_patch(rect)
    
    # Rotate text to match
    ax.text(mid[0], mid[1], label, 
            ha='center', va='center', rotation=theta, 
            fontsize=10, color='blue')

plt.show()