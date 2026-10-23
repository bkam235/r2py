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

# ragg is a graphics device. In Python, we emulate agg_webp_anim by collecting
# matplotlib frames and saving them as a webp animation using imageio.

# r2py:entity:file
# Create a temporary file path
temp_file = tempfile.NamedTemporaryFile(suffix='.webp', delete=False)
file = temp_file.name
temp_file.close()

# r2py:entity:agg_webp_anim
# R's agg_webp_anim opens a device. We store frames in a list.
frames = []
delay = 100 # ms
loop = 0

# The R loop: for(i in 1:10)
for i in range(1, 11):
    # r2py:entity:plot
    plt.figure(figsize=(5, 4))
    x = np.arange(1, 101)
    y = np.sin(x + i/10)
    plt.plot(x, y)
    plt.ylim(-1, 1)
    
    # r2py:entity:dev.flush
    # Render current figure to an array
    fig = plt.gcf()
    fig.canvas.draw()
    # Capture RGBA buffer
    image = np.frombuffer(fig.canvas.buffer_rgba(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    # Convert RGBA to RGB for webp
    frames.append(image[:, :, :3])
    plt.close(fig)

# r2py:entity:dev.off
# Save the frames as a webp animated file.
# duration is per frame in seconds. R delay 100 is 0.1s.
imageio.mimsave(file, frames, duration=delay/1000, loop=loop)

# Ensure i is set to the last value of the loop for verification
i = 10