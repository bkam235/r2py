# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:m
m = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 2, 2, 2, 2, 0],
    [0, 2, 0, 0, 2, 0],
    [0, 2, 0, 0, 2, 0],
    [0, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 0, 0]
])

# r2py:entity:plot_iso
x = np.arange(m.shape[1])
y = np.arange(m.shape[0])
X, Y = np.meshgrid(x, y)

levels = [0.5, 1.5]

plt.contourf(X, Y, m, levels=levels, extend='both')
plt.colorbar()
plt.show()