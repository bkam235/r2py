# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/ragg__rd_example__agg_webp_anim_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'ragg__rd_example__agg_webp_anim_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['i']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import imageio
import tempfile
import os

# r2py:entity:import_ragg
# ragg is a graphics device; approximated by matplotlib + imageio

# r2py:entity:file
# Use tempfile.mktemp() or NamedTemporaryFile to get a path
temp_file_obj = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
file = temp_file_obj.name
temp_file_obj.close()

# r2py:entity:agg_webp_anim
frames = []
delay = 100
loop = 0

# Setup Figure for frame capturing to avoid backend issues
fig = Figure(figsize=(5, 4))
canvas = fig.canvas

for i_val in range(1, 11):
    # Clear previous plot for each frame
    fig.clf()
    
    # r2py:entity:plot
    ax = fig.add_subplot(111)
    x = np.arange(1, 101)
    y = np.sin(x + i_val/10)
    ax.plot(x, y)
    ax.set_ylim(-1, 1)
    
    # r2py:entity:dev.flush
    # Render the canvas and capture the image
    fig.canvas.draw()
    # Using buffer_rgba via the canvas
    rgba_buffer = np.asarray(fig.canvas.buffer_rgba())
    frames.append(rgba_buffer)

# r2py:entity:dev.off
# duration in imageio is usually seconds per frame
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)

# Ensure i matches R's final loop value
i = 10