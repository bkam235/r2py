# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/full/rep1/ragg__rd_example__agg_png_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_png_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# The ragg package in R provides a high-quality graphics device.
# In Python, matplotlib.pyplot provides equivalent functionality for rendering to files.

# Create a temporary file path for the PNG
# r2py:entity:file
file = tempfile.mktemp(suffix='.png')

# agg_png(file) equivalent:
# Matplotlib uses plt.figure() and plt.savefig() to handle device creation and output.
# r2py:entity:agg_png
plt.figure(figsize=(480/72, 480/72), dpi=72) # Default agg_png: 480px, 72dpi

# plot(sin, -pi, 2*pi) equivalent:
# In R, plot(sin, -pi, 2*pi) plots the function 'sin' over the range [-pi, 2*pi].
# r2py:entity:plot
x = np.linspace(-np.pi, 2 * np.pi, 500)
y = np.sin(x)
plt.plot(x, y)

# dev.off() equivalent:
# Save the current figure to the specified file and close the plot.
# r2py:entity:dev.off
plt.savefig(file)
plt.close()