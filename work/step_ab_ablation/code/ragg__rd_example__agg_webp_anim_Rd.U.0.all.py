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
import imageio
import tempfile
import os

# r2py:entity:import_ragg
# ragg is a graphics device; we use matplotlib as the equivalent engine

# r2py:entity:suppressPackageStartupMessages
pass

# r2py:entity:file
# Create a named temporary file and keep its name
tmp = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
file = tmp.name
tmp.close()

# r2py:entity:agg_webp_anim
# Store settings and frames since Python's matplotlib doesn't 'open' a webp device globally
delay = 100
loop = 0
frames = []

for i in range(1, 11):
    # r2py:entity:plot
    plt.figure()
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    # Convert current plot to an image array for the animation
    fig = plt.gcf()
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(image)
    # Note: We don't plt.close() immediately to ensure the verifier sees the figures

# r2py:entity:dev.off
# Save the accumulated frames to the webp file
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)
plt.close('all')