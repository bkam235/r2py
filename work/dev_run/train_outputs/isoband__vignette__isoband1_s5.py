# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

# r2py:entity:m
m = np.array([
    [0, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 0, 0],
    [0, 0, 0.8, 0]
])

# The R isoband plot_iso function visualizes contours of a matrix.
# To replicate this in Python, we create a grid and use a contour plot.
# r2py:entity:plot_iso
x = np.arange(m.shape[1])
y = np.arange(m.shape[0])
X, Y = np.meshgrid(x, y)

# plot_iso(m, 0.5, 1.5) suggests levels at 0.5 and 1.5
# Note: 1.5 is outside the range of m (0-1), so it won't appear.
levels = [0.5, 1.5]

plt.contourf(X, Y, m, levels=levels, extend='both')
plt.colorbar()
plt.show()