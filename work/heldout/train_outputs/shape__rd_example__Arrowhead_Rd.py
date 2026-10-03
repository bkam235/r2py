# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import *

# Initialize plot
# r2py:entity:emptyplot
fig, ax = plt.subplots()
ax.set_title("Arrowhead")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# r2py:entity:Arrowhead
def draw_arrowhead(x0, y0, angle, length, type_style, color):
    # Convert angle to radians
    rad = np.radians(angle)
    # Calculate tip of the arrow (assuming a small fixed offset for the arrowhead placement)
    # In R 'shape::Arrowhead', these parameters define the position and orientation of the head
    dx = np.cos(rad) * length
    dy = np.sin(rad) * length
    
    # Calculate flank points based on a 30 degree spread for the head
    spread = np.radians(30)
    x1 = x0 + np.cos(rad - spread) * (length * 0.5)
    y1 = y0 + np.sin(rad - spread) * (length * 0.5)
    x2 = x0 + np.cos(rad + spread) * (length * 0.5)
    y2 = y0 + np.sin(rad + spread) * (length * 0.5)
    
    if type_style == "circle":
        ax.scatter(x0, y0, c=color, s=length*100, marker='o')
    elif type_style == "curved":
        ax.plot([x1, x0, x2], [y1, y0, y2], color=color, lw=2)
    elif type_style == "triangle":
        ax.plot([x1, x0, x2], [y1, y0, y2], color=color, lw=2)

# First group: circle, green
# r2py:entity:Arrowhead
x0 = np.random.uniform(0, 1, 10)
y0 = np.random.uniform(0, 1, 10)
angle = np.random.uniform(0, 360, 10)
for i in range(10):
    draw_arrowhead(x0[i], y0[i], angle[i], 0.3, "circle", "green")

# Second group: curved, red
# r2py:entity:Arrowhead_1
x0 = np.random.uniform(0, 1, 10)
y0 = np.random.uniform(0, 1, 10)
angle = np.random.uniform(0, 360, 10)
for i in range(10):
    draw_arrowhead(x0[i], y0[i], angle[i], 0.4, "curved", "red")

# Third group: triangle, rainbow
# r2py:entity:Arrowhead_2
x0 = np.random.uniform(0, 1, 10)
y0 = np.random.uniform(0, 1, 10)
angle = np.random.uniform(0, 360, 10)
arr_length = np.random.uniform(0, 1, 10)
# Approximation of R's rainbow(10)
colors = plt.cm.hsv(np.linspace(0, 1, 10))
for i in range(10):
    draw_arrowhead(x0[i], y0[i], angle[i], arr_length[i], "triangle", colors[i])

plt.show()