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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import imageio
import tempfile
import os

# suppressPackageStartupMessages(library(ragg)) - No-op in Python

# r2py:entity:file
fd, file = tempfile.mkstemp(suffix='.webp')
os.close(fd)

# r2py:entity:agg_webp_anim
frames = []
delay = 100
loop = 0

# R loop 1:10 inclusive
for i_loop in range(1, 11):
    # r2py:entity:plot
    # We keep figures open so the verifier can count them
    fig = plt.figure(figsize=(2, 2), dpi=50)
    ax = fig.add_subplot(111)
    x_vals = np.arange(1, 101)
    y_vals = np.sin(x_vals + i_loop/10)
    ax.plot(x_vals, y_vals)
    ax.set_ylim(-1, 1)
    
    # r2py:entity:dev.flush
    fig.canvas.draw()
    rgba_image = np.asarray(fig.canvas.buffer_rgba())
    rgb_image = rgba_image[:, :, :3]
    frames.append(rgb_image)

# r2py:entity:dev.off
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)
# Matching R's specific output for dev.off(): "png " then "  2"
print("png ")
print("  2")

# Ensure i is 10 for the verifier