# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/outputs/empty/rep1/ragg__rd_example__agg_png_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_png_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['pi']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# r2py:entity:file
file = tempfile.mktemp(suffix='.png')

# agg_png in R opens a graphics device. 
# In Python/Matplotlib, we create a figure and save it later or use a backend.
# r2py:entity:agg_png
plt.figure(figsize=(480/72, 480/72), dpi=72)

# plot(sin, -pi, 2*pi) in R plots the function 'sin' over the range [-pi, 2*pi]
# r2py:entity:plot
x = np.linspace(-np.pi, 2 * np.pi, 100)
y = np.sin(x)
plt.plot(x, y)

# dev.off() in R flushes the graphics device to the file.
# r2py:entity:dev.off
plt.savefig(file)
plt.close()